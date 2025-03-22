# utils/Solver.py

from utils.Parser import Parser

class RSSolver:
    def __init__(self, file_path: str, verbose: bool = False):
        self.parser = Parser(file_path)
        self.T = []
        self.res = [False for _ in range(self.parser.num_clauses)]

    def solve(self) -> bool:
        for i in range(1, self.parser.num_vars + 1):
            self.T.append(i)
            if self.__validate__():
                self.T[-1] = -self.T[-1]

        for i, clause in enumerate(self.parser.data):
            if any(var in self.T for var in clause):
                self.res[i] = True

        return all(self.res)

    def __validate__(self) -> bool:
        for clause in self.parser.data:
            if all(-oth in self.T for oth in clause):
                return True
        return False


