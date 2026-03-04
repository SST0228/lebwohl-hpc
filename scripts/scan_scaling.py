import csv, time, re, pathlib, subprocess

def parse_out(out: str):
    def grab(pat, name):
        m = re.search(pat, out)
        if not m:
            raise RuntimeError(f"Cannot parse {name} from:\n{out}")
        return m.group(1)
    size  = int(grab(r"Size:\s*([0-9]+)", "Size"))
    steps = int(grab(r"Steps:\s*([0-9]+)", "Steps"))
    temp  = float(grab(r"T\*:\s*([0-9.]+)", "T*"))
    order = float(grab(r"Order:\s*([0-9.]+)", "Order"))
    rep_t = float(grab(r"Time:\s*([0-9.]+)\s*s", "Time"))
    return steps, size, temp, order, rep_t

def run_cmd(cmd):
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    t1 = time.time()
    out = (r.stdout or "").strip()
    return out, (t1 - t0)

def run_base(steps, size, temp, plotflag):
    out, wall = run_cmd(["python","src/LebwohlLasher.py",str(steps),str(size),str(temp),str(plotflag)])
    steps,size,temp,order,rep_t = parse_out(out)
    return {"method":"base","np":1,"steps":steps,"size":size,"temp":temp,"order":order,"reported_time_s":rep_t,"wall_time_s":wall}

def run_numba(steps, size, temp, plotflag, warmup=True):
    cmd = ["python","experiments/numba/LebwohlLasher_numba.py",str(steps),str(size),str(temp),str(plotflag)]
    if warmup:
        run_cmd(cmd)  # compile warmup
    out, wall = run_cmd(cmd)
    steps,size,temp,order,rep_t = parse_out(out)
    return {"method":"numba(one_energy_njit)","np":1,"steps":steps,"size":size,"temp":temp,"order":order,"reported_time_s":rep_t,"wall_time_s":wall}

def run_numpy(steps, size, temp, plotflag):
    out, wall = run_cmd(["python","experiments/numpy/LebwohlLasher_numpy.py",str(steps),str(size),str(temp),str(plotflag)])
    steps,size,temp,order,rep_t = parse_out(out)
    return {"method":"numpy(get_order_vec)","np":1,"steps":steps,"size":size,"temp":temp,"order":order,"reported_time_s":rep_t,"wall_time_s":wall}


def run_mpi(np_, steps, size, temp, plotflag, seed=123):
    # MPI script prints aggregated line; we benchmark wall time only
    cmd = ["mpirun","-np",str(np_),"python","experiments/mpi/LebwohlLasher_mpi.py",str(steps),str(size),str(temp),str(plotflag),str(seed)]
    out, wall = run_cmd(cmd)
    # Try parse mean_runtime from MPI output if present
    m = re.search(r"mean_runtime=([0-9.]+)s", out)
    mean_rt = float(m.group(1)) if m else float("nan")
    return {"method":"mpi(replicas)","np":np_,"steps":steps,"size":size,"temp":temp,"order":float("nan"),"reported_time_s":mean_rt,"wall_time_s":wall}

def main():
    pathlib.Path("results").mkdir(exist_ok=True)
    outcsv = pathlib.Path("results/scan.csv")
    new = not outcsv.exists()
    with outcsv.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["method","np","steps","size","temp","order","reported_time_s","wall_time_s"])
        if new:
            w.writeheader()

        sizes = [20, 30, 50, 80, 100]
        steps = 300
        temp  = 0.5
        plotflag = 0

        # base + numba across sizes
        for L in sizes:
            w.writerow(run_base(steps, L, temp, plotflag))
            w.writerow(run_numba(steps, L, temp, plotflag, warmup=True))
            w.writerow(run_numpy(steps, L, temp, plotflag))

        # mpi scaling at one representative size
        L = 50
        for np_ in [1,2,4,8]:
            w.writerow(run_mpi(np_, steps, L, temp, plotflag, seed=123))

    print("Wrote", outcsv)

if __name__ == "__main__":
    main()
