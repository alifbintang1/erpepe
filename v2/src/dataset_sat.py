import argparse
from pysat.formula import CNF
from random import sample, choice, random


def generate_satisfiable_2sat(n, m):
    """
    Generate a satisfiable 2-SAT instance with n variables and m clauses.

    Args:
        n (int): Number of variables.
        m (int): Number of clauses.

    Returns:
        CNF: A PySAT CNF object representing the 2-SAT instance.

    Notes:
        Each clause has exactly two literals, and satisfiability is guaranteed
        by ensuring that each clause has at least one positive literal, making
        the all-true assignment a satisfying solution.
    """
    # Initialize an empty CNF formula
    cnf = CNF()

    # List of variables (1 to n, following DIMACS convention)
    variables = list(range(1, n + 1))

    # Generate m clauses
    for _ in range(m):
        # Randomly select two distinct variables
        i, j = sample(variables, 2)

        # Choose signs: 0 for positive, 1 for negative
        sign_i = choice([0, 1])
        sign_j = choice([0, 1])

        # If both literals would be negative, flip one to positive
        if sign_i == 1 and sign_j == 1:
            # Randomly decide which literal to make positive
            if random() < 0.5:
                sign_i = 0
            else:
                sign_j = 0

        # Create literals (positive if sign is 0, negative if sign is 1)
        lit_i = i if sign_i == 0 else -i
        lit_j = j if sign_j == 0 else -j

        # Add the clause to the CNF formula
        cnf.append([lit_i, lit_j])

    return cnf


if __name__ == "__main__":
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(
        description="Generate a satisfiable 2-SAT instance."
    )
    parser.add_argument("--nvars", type=int, required=True, help="Number of variables")
    parser.add_argument("--nclauses", type=int, required=True, help="Number of clauses")
    parser.add_argument(
        "--output",
        type=str,
        default="satisfiable_2sat.cnf",
        help="Output file name (default: satisfiable_2sat.cnf)",
    )

    # Parse arguments
    args = parser.parse_args()

    # Generate the 2-SAT instance
    cnf = generate_satisfiable_2sat(args.nvars, args.nclauses)

    # Save to file in DIMACS CNF format
    cnf.to_file(args.output)

    # Confirmation message
    print(
        f"Generated satisfiable 2-SAT instance with {args.nvars} variables and "
        f"{args.nclauses} clauses, saved to {args.output}"
    )
