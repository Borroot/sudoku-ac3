from sudoku import Sudoku
import copy
import itertools


class Ac3:

    def __init__(self, sudoku):
        self._history = [] # contains sets of [((x, y), [removed number from domain])]

        # create the domains and the binairy relations from the given sudoku
        d = lambda x, y: list(range(1, 10)) if sudoku.grid[y][x] == 0 else [sudoku.grid[y][x]]
        self.domain = [[d(x, y) for x in range(9)] for y in range(9)]
        self.relations = [[self._gen_relations(x, y) for x in range(9)] for y in range(9)]


    def _gen_relations(self, x, y):
        """Generate all the binairy constraint relations for the given field."""
        relations = []

        # add horizontal constraints
        relations.extend((_x, y) for _x in range(9) if _x != x)

        # add vertical constraints
        relations.extend((x, _y) for _y in range(9) if _y != y)

        # add block constraints
        bx = (x // 3) * 3
        by = (y // 3) * 3
        relations.extend(\
                (bx + _x, by + _y) for _y in range(3) for _x in range(3)\
                if (bx + _x, by + _y) != (x, y))

        return relations


    def uncheck(self):
        """Remove the last operations done on domains during the last check."""
        for ((x, y), removed) in self._history.pop():
            self.domain[y][x].extend(removed)
            self.domain[y][x].sort()


    def _check_worklist(self, worklist, history = []):
        """Check all the arcs given in the worklist."""
        def arc_reduce(arc):
            (x1, y1), (x2, y2) = arc
            if len(self.domain[y2][x2]) > 1:
                return False # we can always find a vx and vy satisfying the constraint

            value = self.domain[y2][x2][0]
            try:
                index = self.domain[y1][x1].index(value)
                del self.domain[y1][x1][index]
                history.append(((x1, y1), [value]))
                return True
            except:
                return False

        while worklist:
            arc = worklist.pop()
            if arc_reduce(arc):
                (x1, y1), _ = arc
                if self.domain[y1][x1]:
                    worklist.extend(list(map(lambda field: (field, (x1, y1)),\
                            copy.deepcopy(self.relations[y1][x1]))))
                else:
                    self._history.append(history)
                    return False

        self._history.append(history)
        return True


    def check_all(self):
        """Check if all of the arcs are consistent, should be run at the start only."""
        worklist = list(itertools.chain.from_iterable(list(map(lambda field: ((x, y), field),\
                copy.deepcopy(self.relations[y][x]))) for y in range(9) for x in range(9)))
        return self._check_worklist(worklist)


    def check_set(self, x, y, value):
        """Check if the arcs are consistent after setting a value."""
        assert value in self.domain[y][x]

        domain = copy.deepcopy(self.domain[y][x])
        domain.remove(value)
        history = [((x, y), domain)]
        self.domain[y][x] = [value]

        worklist = list(map(lambda field: ((x, y), field), copy.deepcopy(self.relations[y][x])))
        return self._check_worklist(worklist, history)


    def solution(self):
        """Return the solution if available."""
        codex = ""
        for y in range(9):
            for x in range(9):
                if len(self.domain[y][x]) != 1:
                    return None
                else:
                    codex += str(self.domain[y][x][0])
        return Sudoku(codex)


    def __str__(self):
        """Return the current solution."""
        codex = ""
        for y in range(9):
            for x in range(9):
                if len(self.domain[y][x]) == 1:
                    codex += str(self.domain[y][x][0])
                else:
                    codex += "0"
        return str(Sudoku(codex))


if __name__ == "__main__":
    for sudoku in Sudoku.load("data/sudoku.txt"):
        print(sudoku)

        ac3 = Ac3(sudoku)
        ac3.check_all()

        solution = ac3.solution()
        if solution is None:
            print("no solution found with pure AC-3")
        else:
            if solution.isvalid():
                print(solution)
            else:
                print("incorrect solution")
        print("--------------------------------\n")

        # print all of the relations
        # for y in range(9):
        #     for x in range(9):
        #         print(f"({x},{y}) ->", end="")
        #         print(  " h:", ac3.relations[y][x][:8])
        #         print("\t v:", ac3.relations[y][x][8:2*8])
        #         print("\t b:", ac3.relations[y][x][2*8:])
        #     print()

        # print all of the domains
        # for y in range(9):
        #     for x in range(9):
        #         print(f"({x},{y}) ->", ac3.domain[y][x])
        #     print()
