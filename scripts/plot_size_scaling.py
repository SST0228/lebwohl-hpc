import csv, pathlib
import matplotlib.pyplot as plt

pathlib.Path("figures").mkdir(exist_ok=True)

rows=[]
with open("results/size_scaling.csv", newline="") as f:
    r=csv.DictReader(f)
    for row in r:
        rows.append(row)

def get(method):
    sub=[x for x in rows if x["method"]==method]
    sub.sort(key=lambda x:int(x["size"]))
    return [int(x["size"]) for x in sub], [float(x["wall_time_s"]) for x in sub]

sizes_b, t_b = get("base")
sizes_n, t_n = get("numba")

plt.figure()
plt.plot(sizes_b, t_b, marker="o", label="base")
plt.plot(sizes_n, t_n, marker="o", label="numba(one_energy njit)")
plt.xlabel("Size (L)")
plt.ylabel("Wall time (s)")
plt.title("Size scaling (steps=300, T*=0.5)")
plt.legend()
plt.grid(True, linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig("figures/size_scaling_base_numba.png", dpi=200)
plt.close()

print("Saved figures/size_scaling_base_numba.png")
