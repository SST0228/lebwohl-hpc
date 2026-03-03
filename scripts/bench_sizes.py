import subprocess, csv, time, pathlib, re

def parse(out: str):
    def g(pat):
        m = re.search(pat, out)
        return m.group(1)
    size  = int(g(r"Size:\s*([0-9]+)"))
    steps = int(g(r"Steps:\s*([0-9]+)"))
    temp  = float(g(r"T\*:\s*([0-9.]+)"))
    order = float(g(r"Order:\s*([0-9.]+)"))
    rep_t = float(g(r"Time:\s*([0-9.]+)\s*s"))
    return steps,size,temp,order,rep_t

def run(cmd):
    t0=time.time()
    r=subprocess.run(cmd,capture_output=True,text=True,check=True)
    t1=time.time()
    out=r.stdout.strip()
    steps,size,temp,order,rep_t=parse(out)
    return steps,size,temp,order,rep_t,(t1-t0)

def main():
    pathlib.Path("results").mkdir(exist_ok=True)
    outcsv = pathlib.Path("results/size_scaling.csv")
    new = not outcsv.exists()
    with outcsv.open("a", newline="") as f:
        w=csv.writer(f)
        if new:
            w.writerow(["method","steps","size","temp","wall_time_s"])
        for size in [20, 30, 50, 80, 100]:
            steps=300
            temp="0.5"
            plot="0"
            # base
            w.writerow(["base", steps, size, temp, run(["python","src/LebwohlLasher.py",str(steps),str(size),temp,plot])[5]])
            # numba (run twice, take second)
            run(["python","experiments/numba/LebwohlLasher_numba.py",str(steps),str(size),temp,plot])
            w.writerow(["numba", steps, size, temp, run(["python","experiments/numba/LebwohlLasher_numba.py",str(steps),str(size),temp,plot])[5]])
    print("Wrote", outcsv)

if __name__=="__main__":
    main()
