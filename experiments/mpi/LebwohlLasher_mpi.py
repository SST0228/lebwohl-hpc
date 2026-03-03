import sys, os, time
import numpy as np
from mpi4py import MPI

# Import baseline functions safely
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.LebwohlLasher import initdat, MC_step, all_energy, get_order

def run_one(nsteps, nmax, T, seed):
    np.random.seed(seed)
    lattice = initdat(nmax)

    t0 = time.time()
    for _ in range(nsteps):
        MC_step(lattice, T, nmax)
    t1 = time.time()

    # measure on final lattice
    energy = all_energy(lattice, nmax)
    order = get_order(lattice, nmax)
    return (t1 - t0), energy, order

def main():
    if len(sys.argv) < 5:
        print("Usage: mpirun -np P python experiments/mpi/LebwohlLasher_mpi.py <steps> <size> <temp> <plotflag> [base_seed]")
        sys.exit(1)

    nsteps = int(sys.argv[1])
    nmax   = int(sys.argv[2])
    T      = float(sys.argv[3])
    # plotflag ignored in MPI version (avoid GUI issues)
    base_seed = int(sys.argv[5]) if len(sys.argv) > 5 else 12345

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    runtime, energy, order = run_one(nsteps, nmax, T, base_seed + rank*1000)

    runtimes = comm.gather(runtime, root=0)
    orders   = comm.gather(order, root=0)

    if rank == 0:
        mean_rt  = float(np.mean(runtimes))
        mean_ord = float(np.mean(orders))
        std_ord  = float(np.std(orders))
        print(f"MPI replicas: ranks={size}, Steps={nsteps}, Size={nmax}, T*={T:.3f}: "
              f"mean_runtime={mean_rt:.6f}s, Order(mean±std)={mean_ord:.3f}±{std_ord:.3f}")

if __name__ == "__main__":
    main()

