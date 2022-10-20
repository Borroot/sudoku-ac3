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
    def load(cls, filename):
        """Load all the sudokus from a file with the long or short format."""
        if not os.path.exists(filename):
            return []

        with open(filename) as fp:
            lines = list(map(str.strip, fp.readlines()))
            lines = list(filter(str.isdigit, lines))

            if len(lines) == 0:
                return []

            # convert the long format to the short format
            if len(lines[0]) == 9:
                lines = ["".join(lines[i : i + 9]) for i in range(0, len(lines), 9)]

            return [cls(codex) for codex in lines]

        return []


    def check_solution(self):
        pass


if __name__ == "__main__":
    for sudoku in Sudoku.load("data/sudoku1.txt"):
        print(sudoku)
