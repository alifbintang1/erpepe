from typing import List, Tuple
from utils.Parser import Parser
from tqdm import tqdm

class RSSolver:
    def __init__(self, file_path: str, verbose: bool = False):
        self.parser = Parser(file_path)
        self.T = []
        self.res = [False for x in range(self.parser.num_clauses)]
        self.verbose = verbose

    def solve(self)-> bool:
        for i in tqdm(range(1, self.parser.num_vars + 1), desc="Processing Variables",disable = not self.verbose):
            self.T.append(i)
            if self.__validate__():
                self.T[-1] = -self.T[-1]

        # Second loop with progress bar
        for i, clause in tqdm(enumerate(self.parser.data), total=len(self.parser.data), desc="Processing Clauses", disable = not self.verbose):
            if any(var in self.T for var in clause):
                self.res[i] = True
        
        return self.res #debug
        # return all(self.res)


    def __validate__(self)->bool:
        for clause in self.parser.data:
            if all(-oth in self.T for oth in clause):
                return True
        return False
    
                
     