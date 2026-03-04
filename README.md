# Lebwohl-Lasher 2D HPC Acceleration

## Run (baseline)
```bash
python src/LebwohlLasher.py <steps> <size> <temperature> <plotflag>
# example
python src/LebwohlLasher.py 500 50 0.5 0

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p results
python -m cProfile -o results/base.prof src/LebwohlLasher.py 500 50 0.5 0
python -m pstats results/base.prof
pytest -q

提交并推送：
```bash id="n2ekx1"
git add .gitignore requirements.txt README.md
git commit -m "Add README, requirements, and gitignore"
git push
mkdir -p tests
cat > tests/test_smoke.py << 'EOF'
import subprocess, re

def test_program_runs_and_outputs_order_time():
    r = subprocess.run(
        ["python", "src/LebwohlLasher.py", "50", "30", "0.5", "0"],
        capture_output=True, text=True, check=True
    )
    out = r.stdout.strip()
    assert "Order:" in out and "Time:" in out
    m = re.search(r"Order:\s*([0-9.]+),\s*Time:\s*([0-9.]+)", out)
    assert m, f"Unexpected output: {out}"
    order = float(m.group(1))
    t = float(m.group(2))
    assert 0.0 <= order <= 1.0
    assert t > 0.0
