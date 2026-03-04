import numpy as np
import importlib.util

def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

base = load_module("src/LebwohlLasher.py", "base")
npv  = load_module("experiments/numpy/LebwohlLasher_numpy.py", "npv")

np.random.seed(123)
nmax = 50
arr = np.random.rand(nmax, nmax).astype(np.float64)

e_base = base.all_energy(arr, nmax)
e_npv  = npv.all_energy(arr, nmax)

print("baseline:", e_base)
print("numpy   :", e_npv)
print("abs diff:", abs(e_base - e_npv))
