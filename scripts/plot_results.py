import csv, pathlib, math
import matplotlib.pyplot as plt

pathlib.Path("figures").mkdir(exist_ok=True)

# ---- 1) base vs numba from results/bench.csv ----
bench = []
with open("results/bench.csv", newline="") as f:
    r = csv.DictReader(f)
    for row in r:
        bench.append(row)

# take the first base row and the fastest numba row (min wall time)
base_rows = [b for b in bench if b["method"]=="base"]
numba_rows = [b for b in bench if b["method"]=="numba"]
base = base_rows[0]
numba = min(numba_rows, key=lambda x: float(x["wall_time_s"]))

methods = ["base", "numba(one_energy njit)"]
times = [float(base["wall_time_s"]), float(numba["wall_time_s"])]

plt.figure()
plt.bar(methods, times)
plt.ylabel("Wall time (s)")
plt.title("Baseline vs Numba (steps=500, size=50)")
plt.xticks(rotation=15, ha="right")
plt.tight_layout()
plt.savefig("figures/compare_base_numba.png", dpi=200)
plt.close()

# ---- 2) MPI scaling from results/mpi_scaling.csv ----
mpi = []
with open("results/mpi_scaling.csv", newline="") as f:
    r = csv.DictReader(f)
    for row in r:
        mpi.append((int(row["np"]), float(row["real_time_s"])))
mpi.sort()

nps = [x[0] for x in mpi]
ts  = [x[1] for x in mpi]
t1 = ts[0]
speedup = [t1/t for t in ts]

plt.figure()
plt.plot(nps, ts, marker="o")
plt.xlabel("MPI ranks (np)")
plt.ylabel("Real time (s)")
plt.title("MPI replicas scaling (steps=500, size=50)")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig("figures/mpi_time_scaling.png", dpi=200)
plt.close()

plt.figure()
plt.plot(nps, speedup, marker="o")
plt.xlabel("MPI ranks (np)")
plt.ylabel("Speedup (T1/Tp)")
plt.title("MPI replicas speedup")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig("figures/mpi_speedup.png", dpi=200)
plt.close()

print("Saved figures into figures/")
