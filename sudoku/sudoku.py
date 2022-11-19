import os


class Sudoku:

    def __init__(self, codex):
        """Create a sudoku from a 9 * 9 long string."""
        codex = list(map(int, codex))
        self.grid = [codex[i : i + 9] for i in range(0, 9 * 9, 9)]


    def __str__(self):
        builder = "╔═══════╦═══════╦═══════╗\n"
        for y in range(9):
            if y == 3 or y == 6:
                builder += "╠═══════╬═══════╬═══════╣\n"
            builder += "║ "

            for x in range(9):
                if x == 3 or x == 6:
                    builder += "║ "
                builder += str(self.grid[y][x]) + " " if self.grid[y][x] > 0 else "  "
            builder += "║\n"

        builder += "╚═══════╩═══════╩═══════╝\n"
        return builder


    @classmethod
    def load(cls, filename, maxnum = -1):
        """Load all the sudokus from a file with the long or short format."""
        if not os.path.exists(filename):
            return []

        with open(filename) as fp:
            lines = list(map(str.strip, fp.readlines()[:maxnum]))
            lines = list(filter(str.isdigit, lines))

            if not lines:
                return []

            # convert the long format to the short format
            if len(lines[0]) == 9:
                lines = ["".join(lines[i : i + 9]) for i in range(0, len(lines), 9)]

            return [cls(codex) for codex in lines]

        return []


    def isvalid(self):
        """Check whether the current sudoku (solution) is valid."""
        # check horizontal
        for y in range(9):
            seen = [False] * 9
            for x in range(9):
                if seen[self.grid[y][x] - 1]:
                    print("horizontal", x, y)
                    return False
                else:
                    seen[self.grid[y][x] - 1] = True

        # check vertical
        for x in range(9):
            seen = [False] * 9
            for y in range(9):
                if seen[self.grid[y][x] - 1]:
                    print("vertical", x, y)
                    return False
                else:
                    seen[self.grid[y][x] - 1] = True

        # check blocks
        for bx in range(0, 9, 3):
            for by in range(0, 9, 3):
                seen = [False] * 9
                for x in range(3):
                    for y in range(3):
                        if seen[self.grid[by + y][bx + x] - 1]:
                            print("block", bx + x, by + y)
                            return False
                        else:
                            seen[self.grid[by + y][bx + x] - 1] = True

        return True


if __name__ == "__main__":
    for sudoku in Sudoku.load("data/sudoku.txt"):
        print(sudoku)
