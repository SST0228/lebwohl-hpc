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
    steps, size, temp, order, rep_t = parse_out(out)
    return {
        "method": None,
        "steps": steps,
        "size": size,
        "temp": temp,
        "order": order,
        "reported_time_s": rep_t,
        "wall_time_s": (t1 - t0),
    }, out

def run_one(method, steps, size, temp=0.5, plotflag=0):
    if method == "base":
        cmd = ["python","src/LebwohlLasher.py",str(steps),str(size),str(temp),str(plotflag)]
        row, out = run_cmd(cmd)
        row["method"] = "base"
        return row
    if method == "numba":
        cmd = ["python","experiments/numba/LebwohlLasher_numba.py",str(steps),str(size),str(temp),str(plotflag)]
        # warmup once per (steps,size) to avoid counting compile cost
        _ = subprocess.run(cmd, capture_output=True, text=True, check=True)
        row, out = run_cmd(cmd)
        row["method"] = "numba(one_energy_njit)"
        return row
    if method == "numpy":
        cmd = ["python","experiments/numpy/LebwohlLasher_numpy.py",str(steps),str(size),str(temp),str(plotflag)]
        row, out = run_cmd(cmd)
        row["method"] = "numpy(vec get_order+all_energy)"
        return row
    raise ValueError("method must be base/numba/numpy")

def main():
    pathlib.Path("results").mkdir(exist_ok=True)
    outcsv = pathlib.Path("results/grid_steps_sizes.csv")

    methods = ["base","numba","numpy"]
    steps_list = [300, 400, 500]
    size_list  = [30, 40, 50]
    temp = 0.5
    plotflag = 0

    with outcsv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["method","steps","size","temp","order","reported_time_s","wall_time_s"])
        w.writeheader()
        for size in size_list:
            for steps in steps_list:
                for method in methods:
                    row = run_one(method, steps, size, temp=temp, plotflag=plotflag)
                    w.writerow(row)
                    print(f"OK {method:5s} size={size} steps={steps} wall={row['wall_time_s']:.3f}s")

    print("Wrote", outcsv)

if __name__ == "__main__":
    main()
