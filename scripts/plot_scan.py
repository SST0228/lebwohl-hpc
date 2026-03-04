import csv, pathlib
import matplotlib.pyplot as plt

pathlib.Path("figures").mkdir(exist_ok=True)

rows=[]
with open("results/scan.csv", newline="") as f:
    r=csv.DictReader(f)
    for row in r:
        row["np"]=int(row["np"])
        row["steps"]=int(row["steps"])
        row["size"]=int(row["size"])
        row["temp"]=float(row["temp"])
        row["wall_time_s"]=float(row["wall_time_s"])
        rows.append(row)

# 1) size scaling: base vs numba (np=1)
base=[x for x in rows if x["method"]=="base" and x["np"]==1]
numba=[x for x in rows if x["method"].startswith("numba") and x["np"]==1]
base.sort(key=lambda x:x["size"])
numba.sort(key=lambda x:x["size"])

plt.figure()
plt.plot([x["size"] for x in base], [x["wall_time_s"] for x in base], marker="o", label="base")
plt.plot([x["size"] for x in numba], [x["wall_time_s"] for x in numba], marker="o", label="numba(one_energy njit)")
plt.xlabel("Size (L)")
plt.ylabel("Wall time (s)")
plt.title("Size scaling (steps fixed)")
plt.legend()
plt.grid(True, linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig("figures/scan_size_scaling.png", dpi=200)
plt.close()

# 2) MPI scaling: np vs wall time (size=50)
mpi=[x for x in rows if x["method"].startswith("mpi") and x["size"]==50]
mpi.sort(key=lambda x:x["np"])

plt.figure()
plt.plot([x["np"] for x in mpi], [x["wall_time_s"] for x in mpi], marker="o")
plt.xlabel("MPI ranks (np)")
plt.ylabel("Wall time (s)")
plt.title("MPI replicas scaling (size=50)")
plt.grid(True, linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig("figures/scan_mpi_scaling.png", dpi=200)
plt.close()

print("Saved figures/scan_size_scaling.png and figures/scan_mpi_scaling.png")
