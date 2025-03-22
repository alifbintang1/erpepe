from typing import List, Set, Dict
from utils.Parser import Parser
import sys

class RSSolver:
    def __init__(self, file_path: str, verbose: bool = True):
        self.parser = Parser(file_path)
        self.clauses = self.parser.data
        self.num_vars = self.parser.num_vars
        self.assignment: Dict[int, bool] = {}
        self.verbose = verbose
        self.decision_count = 0
        self.backtrack_count = 0
        self.unit_prop_count = 0
        self.pure_lit_count = 0
        self.max_decisions = 150_000  # Safety net to prevent infinite loops
        self.remaining_vars = set(range(1, self.num_vars+1))

    def solve(self) -> Set[int]:
        print("🔄 Starting SAT solver...")
        try:
            result = self.dpll()
            print("\n🔍 Search completed")
            return {var if val else -var for var, val in self.assignment.items()} if result else None
        except RecursionError:
            print("\n❌ Recursion depth exceeded - formula too complex")
            return None
        finally:
            print(f"\n📊 Solver statistics:")
            print(f"→ Decisions: {self.decision_count}")
            print(f"→ Backtracks: {self.backtrack_count}")
            print(f"→ Unit propagations: {self.unit_prop_count}")
            print(f"→ Pure literals: {self.pure_lit_count}")

    def simplify_clauses(self, clauses: List[List[int]]) -> List[List[int]]:
        simplified = []
        for clause in clauses:
            new_clause = []
            satisfied = False
            for lit in clause:
                var = abs(lit)
                if var in self.assignment:
                    if (lit > 0 and self.assignment[var]) or (lit < 0 and not self.assignment[var]):
                        satisfied = True
                        break
                else:
                    new_clause.append(lit)
            if not satisfied:
                if not new_clause: return None  # Conflict
                simplified.append(new_clause)
        return simplified

    def select_variable(self):
        """VSIDS-inspired variable selection"""
        return next(iter(self.remaining_vars), None)

    def dpll(self):
        # Decision safety check
        if self.decision_count > self.max_decisions:
            raise Exception(f"⚠️ Decision limit {self.max_decisions} reached - aborting")

        # Simplify clauses
        simplified = self.simplify_clauses(self.clauses)
        if simplified is None: return False
        if not simplified: return True

        # Unit propagation
        unit_clauses = [c for c in simplified if len(c) == 1]
        if unit_clauses:
            lit = unit_clauses[0][0]
            var = abs(lit)
            val = lit > 0
            if var in self.assignment:
                return self.assignment[var] == val and self.dpll()
            self.assignment[var] = val
            self.remaining_vars.discard(var)
            self.unit_prop_count += 1
            result = self.dpll()
            if not result:
                del self.assignment[var]
                self.remaining_vars.add(var)
            return result

        # Pure literal elimination
        lit_counts = {}
        for clause in simplified:
            for lit in clause:
                lit_counts[lit] = lit_counts.get(lit, 0) + 1
                
        for lit, count in lit_counts.items():
            if -lit not in lit_counts:
                var = abs(lit)
                if var not in self.assignment:
                    self.assignment[var] = lit > 0
                    self.remaining_vars.discard(var)
                    self.pure_lit_count += 1
                    result = self.dpll()
                    if result: return True
                    del self.assignment[var]
                    self.remaining_vars.add(var)
                    return False

        # Variable splitting with VSIDS-like heuristic
        var = self.select_variable()
        if not var: return False  # Should never reach here

        # Try positive first
        self.decision_count += 1
        if self.verbose and self.decision_count % 1000 == 0:
            print(f"🔀 Decision {self.decision_count} (Vars left: {len(self.remaining_vars)})")
            
        self.assignment[var] = True
        self.remaining_vars.discard(var)
        if self.dpll(): return True
        
        # Backtrack negative
        self.backtrack_count += 1
        del self.assignment[var]
        self.remaining_vars.add(var)
        
        self.assignment[var] = False
        self.remaining_vars.discard(var)
        result = self.dpll()
        if not result:
            del self.assignment[var]
            self.remaining_vars.add(var)
        return result

    def validate(self) -> bool:
        T = self.solve()
        if T is None: return False
        for clause in self.clauses:
            if not any(lit in T for lit in clause):
                return False
        return True
    

# # utils/Solver.py
# from utils.Parser import Parser

# class RSSolver:
#     def __init__(self, file_path: str, verbose: bool = False):
#         self.parser = Parser(file_path)
#         self.T = []
#         self.res = [False for _ in range(self.parser.num_clauses)]

#     def solve(self) -> bool:
#         for i in range(1, self.parser.num_vars + 1):
#             self.T.append(i)
#             if self.__validate__():
#                 self.T[-1] = -self.T[-1]

#         for i, clause in enumerate(self.parser.data):
#             if any(var in self.T for var in clause):
#                 self.res[i] = True

#         return all(self.res)

#     def __validate__(self) -> bool:
#         for clause in self.parser.data:
#             if all(-oth in self.T for oth in clause):
#                 return True
#         return False


