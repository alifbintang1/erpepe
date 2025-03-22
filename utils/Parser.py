# utils/Parser.py

from typing import List, Tuple, Set
from collections import Counter

class Parser:
    def __init__(self, file_path: str):
        self.path = file_path
        self.num_vars = 0
        self.num_clauses = 0
        self.priority = []
        self.data = self.__read_cnf__()
        self.__process__()
    def __read_cnf__(self)->List[Set[int]]:
        clauses = []
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
                clauses.append(literals)
        
        return clauses
    
    def __process__(self)->None:
        counter = Counter()
        
        for clause in self.data:
            for literal in clause:
                counter[abs(literal)] += 1  
        
        self.priority = dict(sorted(counter.items(), key=lambda x: -x[1]))