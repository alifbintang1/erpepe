import argparse
from pysat.formula import CNF
from random import sample, choice, random


def generate_unsatisfiable_2sat(n, m):
    """
    Generate an unsatisfiable 2-SAT instance with n variables and m clauses.

    Args:
        n (int): Number of variables.
        m (int): Number of clauses.

    Returns:
        CNF: A PySAT CNF object representing the unsatisfiable 2-SAT instance.

    Notes:
        Unsatisfiability is ensured by including four contradictory clauses:
        (p ∨ q), (p ∨ ¬q), (¬p ∨ q), (¬p ∨ ¬q), which force p and ¬p,
        making the instance unsatisfiable. The remaining m-4 clauses are added randomly.
        Requires m >= 4 to guarantee unsatisfiability.
    """
    if m < 4:
        raise ValueError(
            "Cannot create an unsatisfiable 2-SAT instance with fewer than 4 clauses."
        )

    # Initialize an empty CNF formula
    cnf = CNF()

    # List of variables (1 to n, following DIMACS convention)
    variables = list(range(1, n + 1))

    # Select two distinct variables for the contradictory clauses
    p, q = sample(variables, 2)

    # Add the four contradictory clauses
    cnf.append([p, q])  # p ∨ q
    cnf.append([p, -q])  # p ∨ ¬q
    cnf.append([-p, q])  # ¬p ∨ q
    cnf.append([-p, -q])  # ¬p ∨ ¬q

    # Generate the remaining m-4 clauses (following the satisfiable pattern)
    for _ in range(m - 4):
        # Randomly select two distinct variables
        i, j = sample(variables, 2)

        # Choose signs: 0 for positive, 1 for negative
        sign_i = choice([0, 1])
        sign_j = choice([0, 1])

        # If both literals would be negative, flip one to positive
        if sign_i == 1 and sign_j == 1:
            if random() < 0.5:
                sign_i = 0
            else:
                sign_j = 0

        # Create literals
        lit_i = i if sign_i == 0 else -i
        lit_j = j if sign_j == 0 else -j

        # Add the clause
        cnf.append([lit_i, lit_j])

    return cnf


if __name__ == "__main__":
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(
        description="Generate an unsatisfiable 2-SAT instance."
    )
    parser.add_argument("--nvars", type=int, required=True, help="Number of variables")
    parser.add_argument("--nclauses", type=int, required=True, help="Number of clauses")
    parser.add_argument(
        "--output",
        type=str,
        default="unsatisfiable_2sat.cnf",
        help="Output file name (default: unsatisfiable_2sat.cnf)",
    )

    # Parse arguments
    args = parser.parse_args()

    if args.nclauses < 4:
        print(
            "Error: Cannot create an unsatisfiable 2-SAT instance with fewer than 4 clauses."
        )
    else:
        # Generate the unsatisfiable 2-SAT instance
        cnf = generate_unsatisfiable_2sat(args.nvars, args.nclauses)

        # Save to file in DIMACS CNF format
        cnf.to_file(args.output)

        # Confirmation message
        print(
            f"Generated unsatisfiable 2-SAT instance with {args.nvars} variables and "
            f"{args.nclauses} clauses, saved to {args.output}"
        )
