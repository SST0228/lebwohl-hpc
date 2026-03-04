import numpy as np
import importlib.util
from pathlib import Path

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

s_base = base.get_order(arr, nmax)
s_npv  = npv.get_order(arr, nmax)

print("baseline:", s_base)
print("numpy   :", s_npv)
print("abs diff:", abs(s_base - s_npv))
