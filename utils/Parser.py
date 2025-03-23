from typing import List, Set
from itertools import combinations
from tqdm import tqdm

class Parser:
    def __init__(self, file_path: str):
        self.path = file_path
        self.num_vars = 0
        self.num_clauses = 0
        self.R = set()
        self.data = self.__read_cnf__()
        self.compute_RES()
        print(self.data)
        print(self.R)
    def __read_cnf__(self) -> Set[frozenset]:
        clauses = set()
        with open(self.path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('c') or "%" in line:
                    continue
                if line.startswith('p cnf'):
                    _, _, num_vars, num_clauses = line.split()
                    self.num_vars, self.num_clauses = int(num_vars), int(num_clauses)
                    continue
                literals = set(map(int, line.split()))
                literals.discard(0)
                if literals:  # Ensure non-empty clause before adding
                    clauses.add(frozenset(literals))
        return clauses
    
    def resolve(self, c1: frozenset, c2: frozenset) -> Set[frozenset]:
        """
        Perform binary resolution on two clauses c1 and c2.
        Returns a set of resolvent clauses (if any).
        """
        resolvents = set()
        for lit in c1:
            if -lit in c2:  # Complementary literals found
                new_clause = (c1 - {lit}) | (c2 - {-lit})
                if len(new_clause) > 0:
                    resolvents.add(frozenset(new_clause))
        return resolvents
    
    def compute_RES(self):
        """
        Computes the resolution closure of the given CNF formula.
        """
        self.R = set(self.data)  # Start with original clauses
        new_resolvents = set()
        
        print("Computing RES closure...")
        while True:
            for c1, c2 in tqdm(list(combinations(self.R, 2))):
                resolvents = self.resolve(c1, c2)
                new_resolvents.update(resolvents - self.R)
                # if len(self.R) + len(new_resolvents) > self.max_clauses:
                #     print("Max clause limit reached. Stopping RES computation.")
                #     return
            
            if not new_resolvents:
                break  # No new resolvents, stop
            
            self.R.update(new_resolvents)
            new_resolvents.clear()
        print("RES computation complete.")