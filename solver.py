# solver.py

import argparse

from utils import RSSolver

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RES-SAT Solver")
    parser.add_argument("-f", type=str, required=True, help="Path to the CNF file")
    args = parser.parse_args()

    solver = RSSolver(args.f)  # Replace with your CNF file path
    solution = solver.solve()
    print("Solution:", solution)

    is_valid = solver.validate()
    print("Is solution valid?", is_valid)

    # print(SOLVER.validate()) #debug