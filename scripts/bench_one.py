import subprocess, re, csv, time, sys, pathlib

def parse_fields(out: str):
    def grab(pattern, name):
        m = re.search(pattern, out)
        if not m:
            raise RuntimeError(f"Cannot parse {name} from output:\n{out}")
        return m.group(1)

    size  = int(grab(r"Size:\s*([0-9]+)", "Size"))
    steps = int(grab(r"Steps:\s*([0-9]+)", "Steps"))
    temp  = float(grab(r"T\*:\s*([0-9.]+)", "T*"))
    order = float(grab(r"Order:\s*([0-9.]+)", "Order"))
    reported_time = float(grab(r"Time:\s*([0-9.]+)\s*s", "Time"))
    return steps, size, temp, order, reported_time

def run(cmd):
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    t1 = time.time()
    out = (r.stdout or "").strip()
    steps, size, temp, order, reported = parse_fields(out)
    wall = t1 - t0
    return steps, size, temp, order, reported, wall, out

def main():
    if len(sys.argv) != 6:
        print("Usage: python scripts/bench_one.py base|numba <steps> <size> <temp> <plotflag>")
        sys.exit(1)

    method = sys.argv[1]
    steps, size, temp, plotflag = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]

    if method == "base":
        cmd = ["python", "src/LebwohlLasher.py", steps, size, temp, plotflag]
    elif method == "numba":
        cmd = ["python", "experiments/numba/LebwohlLasher_numba.py", steps, size, temp, plotflag]
    else:
        raise ValueError("method must be base or numba")

    res = run(cmd)

    outcsv = pathlib.Path("results/bench.csv")
    outcsv.parent.mkdir(parents=True, exist_ok=True)
    new = not outcsv.exists()

    with outcsv.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["method","steps","size","temp","order","reported_time_s","wall_time_s"])
        w.writerow([method, res[0], res[1], res[2], res[3], res[4], res[5]])

    print("OK:", res[6])
    print("Wrote:", outcsv)

if __name__ == "__main__":
    main()
