import csv
import pathlib
import matplotlib.pyplot as plt

INFILE = "results/grid_steps_sizes.csv"
OUTDIR = pathlib.Path("figures")
OUTDIR.mkdir(exist_ok=True)

# read data
rows = []
with open(INFILE, newline="") as f:
    r = csv.DictReader(f)
    for row in r:
        rows.append({
            "method": row["method"],
            "steps": int(row["steps"]),
            "size": int(row["size"]),
            "wall": float(row["wall_time_s"]),
        })

methods = [
    "base",
    "numba(one_energy_njit)",
    "numpy(vec get_order+all_energy)",
]

sizes = sorted(set(x["size"] for x in rows))
steps_list = sorted(set(x["steps"] for x in rows))

def series(filter_key, filter_val, xkey):
    # returns dict method -> (xs, ys)
    out = {}
    for m in methods:
        sub = [x for x in rows if x["method"] == m and x[filter_key] == filter_val]
        sub.sort(key=lambda z: z[xkey])
        out[m] = ([z[xkey] for z in sub], [z["wall"] for z in sub])
    return out

# ---- Plot 1: per-size, steps vs wall time ----
fig = plt.figure()
# make 3 subplots in a row
for idx, L in enumerate(sizes, start=1):
    ax = fig.add_subplot(1, len(sizes), idx)
    data = series("size", L, "steps")
    for m in methods:
        xs, ys = data[m]
        ax.plot(xs, ys, marker="o", label=m)
    ax.set_title(f"size={L}")
    ax.set_xlabel("steps")
    if idx == 1:
        ax.set_ylabel("wall time (s)")
    ax.grid(True, linestyle="--", linewidth=0.5)
    ax.set_xticks(steps_list)
fig.tight_layout()
fig.savefig(OUTDIR / "grid_steps_vs_time_by_size.png", dpi=200)
plt.close(fig)

# ---- Plot 2: per-steps, size vs wall time ----
fig = plt.figure()
for idx, S in enumerate(steps_list, start=1):
    ax = fig.add_subplot(1, len(steps_list), idx)
    data = series("steps", S, "size")
    for m in methods:
        xs, ys = data[m]
        ax.plot(xs, ys, marker="o", label=m)
    ax.set_title(f"steps={S}")
    ax.set_xlabel("size (L)")
    if idx == 1:
        ax.set_ylabel("wall time (s)")
    ax.grid(True, linestyle="--", linewidth=0.5)
    ax.set_xticks(sizes)
fig.tight_layout()
fig.savefig(OUTDIR / "grid_size_vs_time_by_steps.png", dpi=200)
plt.close(fig)

# ---- Legend-only figure (optional but convenient for report) ----
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for m in methods:
    ax.plot([], [], marker="o", label=m)
ax.legend(loc="center")
ax.axis("off")
fig.tight_layout()
fig.savefig(OUTDIR / "grid_legend.png", dpi=200)
plt.close(fig)

print("Saved:")
print(" - figures/grid_steps_vs_time_by_size.png")
print(" - figures/grid_size_vs_time_by_steps.png")
print(" - figures/grid_legend.png")
