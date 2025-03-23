import argparse
import time
import psutil
import os


def parse_cnf_file(file_path):
    """
    Parse a CNF file in DIMACS format and return the number of variables, clauses, and the list of clauses.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

    clauses = []
    for line in lines:
        if line.startswith("c"):
            continue
        if line.startswith("p"):
            _, _, nvars, nclauses = line.split()
            nvars, nclauses = int(nvars), int(nclauses)
        else:
            clause = list(map(int, line.split()[:-1]))
            clauses.append(clause)

    return nvars, nclauses, clauses


def res_sat(nvars, clauses):
    """
    Implement the RES-SAT algorithm to find a satisfying interpretation T.
    Based on the pseudocode from "Prosedur RES-SAT (Textbook Figure 4.15)".
    """
    T = set()  # Initialize interpretation T as an empty set

    # Iterate over each atom p_i from 1 to n
    for i in range(1, nvars + 1):
        p_i = i
        add_neg_pi = False

        # Check if there exists a clause c such that ~c ⊆ T ∪ {p_i}
        for clause in clauses:
            neg_c = [-lit for lit in clause]  # Compute ~c (negation of clause c)
            if all(lit in T or lit == p_i for lit in neg_c):
                add_neg_pi = True
                break

        # Update T based on the condition
        if add_neg_pi:
            T.add(-p_i)  # Add ~p_i to T
        else:
            T.add(p_i)  # Add p_i to T

    return T


def is_satisfied(clause, T):
    """
    Check if a clause is satisfied by the interpretation T.
    A clause is satisfied if at least one of its literals is in T.
    """
    for lit in clause:
        if lit in T:
            return True
    return False


def check_satisfiability(clauses, T):
    """
    Check if all clauses are satisfied by T.
    Returns True if all clauses are satisfied, False otherwise.
    """
    for clause in clauses:
        if not is_satisfied(clause, T):
            return False
    return True


def format_interpretation(T, nvars):
    """
    Format the interpretation T as a readable list of literals for each variable.
    """
    interpretation = []
    for i in range(1, nvars + 1):
        if i in T:
            interpretation.append(f"p{i}")
        elif -i in T:
            interpretation.append(f"~p{i}")
        else:
            interpretation.append(f"Undefined for p{i}")
    return interpretation


if __name__ == "__main__":
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(
        description="Solve a 2-SAT instance using RES-SAT and check for satisfiability."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="satisfiable_2sat.cnf",
        help="CNF file to solve (default: satisfiable_2sat.cnf)",
    )

    # Parse arguments
    args = parser.parse_args()

    # Parse the CNF file
    nvars, nclauses, clauses = parse_cnf_file(args.output)

    # Measure execution time and memory usage
    process = psutil.Process(os.getpid())
    start_time = time.time()
    T = res_sat(nvars, clauses)
    end_time = time.time()
    memory_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB

    # Format and print the interpretation T
    interpretation = format_interpretation(T, nvars)
    print("\nFinal Interpretation T:")
    for lit in interpretation:
        print(lit)

    # Check satisfiability and alert if necessary
    if check_satisfiability(clauses, T):
        print("\nThe interpretation satisfies all clauses.")
    else:
        print(
            "\nThe interpretation does not satisfy all clauses. The instance might be unsatisfiable."
        )

    # Print execution time and memory usage
    print(f"\nExecution Time: {end_time - start_time:.4f} seconds")
    print(f"Memory Used: {memory_usage:.2f} MB")
