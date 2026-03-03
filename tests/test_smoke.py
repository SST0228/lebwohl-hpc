import subprocess, re

def test_program_runs():
    r = subprocess.run(
        ["python", "src/LebwohlLasher.py", "50", "30", "0.5", "0"],
        capture_output=True, text=True, check=True
    )
    out = r.stdout.strip()
    assert "Order:" in out
    m = re.search(r"Order:\s*([0-9.]+),\s*Time:\s*([0-9.]+)", out)
    assert m, f"Unexpected output: {out}"
    order = float(m.group(1))
    t = float(m.group(2))
    assert 0.0 <= order <= 1.0
    assert t > 0.0
