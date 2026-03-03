import subprocess, re

def test_baseline_runs():
    r = subprocess.run(
        ["python", "src/LebwohlLasher.py", "50", "30", "0.5", "0"],
        capture_output=True, text=True, check=True
    )
    out = r.stdout.strip()
    assert "Size:" in out and "Steps:" in out and "Order:" in out and "Time:" in out
    m = re.search(r"Order:\s*([0-9.]+)", out)
    assert m
    order = float(m.group(1))
    assert 0.0 <= order <= 1.0

def test_numba_runs():
    r = subprocess.run(
        ["python", "experiments/numba/LebwohlLasher_numba.py", "50", "30", "0.5", "0"],
        capture_output=True, text=True, check=True
    )
    out = r.stdout.strip()
    assert "Order:" in out and "Time:" in out
