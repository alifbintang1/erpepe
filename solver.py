import argparse

from utils import RSSolver

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RES-SAT Solver")
    parser.add_argument("-f", type=str, required=True, help="Path to the CNF file")
    args = parser.parse_args()

    SOLVER = RSSolver(args.f)
    print(SOLVER.solve())