import glob, re, csv, pathlib

outcsv = pathlib.Path("results/mpi_scaling.csv")
outcsv.parent.mkdir(parents=True, exist_ok=True)

rows = []
for fn in sorted(glob.glob("results/mpi_np*_time.txt")):
    m = re.search(r"mpi_np(\d+)_time\.txt$", fn)
    if not m:
        continue
    np_ = int(m.group(1))
    txt = pathlib.Path(fn).read_text()
    m2 = re.search(r"real\s+([0-9.]+)", txt)
    if not m2:
        continue
    real = float(m2.group(1))
    rows.append((np_, real))

rows.sort()

with outcsv.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["np","real_time_s"])
    w.writerows(rows)

print("Wrote", outcsv)
