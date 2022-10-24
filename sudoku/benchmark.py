from sudoku import Sudoku
from stats import Stats
from solver import solve
import heuristic as h


def benchmark(sudokus, heuristic_field, heuristic_value, timeout):
    """Benchmark the given set of sudokus using the provides heuristics."""
    timeouts = 0
    nodecounts = []
    times = []

    for index, sudoku in enumerate(sudokus):
        solution, stats = solve(sudoku, heuristic_field, heuristic_value, timeout)
        if solution is not None:
            times.append(stats.end_time - stats.start_time)
            nodecounts.append(stats.nodecount)
        else:
            timeouts += 1

    nodecounts.sort()
    times.sort()

    total = len(sudokus)
    if total == timeouts: return total, timeouts, 0, 0, 0, 0, 0

    mean_time = round(times[len(times) // 2], 4)
    max_time = round(times[-1], 4)
    mean_visited = nodecounts[len(nodecounts) // 2]
    max_visited = nodecounts[-1]
    visited_per_second = round(sum(nodecounts) / sum(times))

    return total, timeouts, mean_time, max_time, mean_visited, max_visited, visited_per_second


if __name__ == "__main__":
    """Benchmark the provided sudokus and output a latex formatted table."""
    filename = "data/sudoku.txt"
    maxcases = 100

    heuristic_field = [h.nop, h.lf, h.mf, h.lrv, h.mrv]
    heuristic_value = [h.nop, h.lcv, h.mcv]
    timeout = 1

    # ---------------------------------------------------------------------------------------------

    builder = ""
    builder += "\\begin{tabular}{|c|c|c|c|c|c|c|c|c|}\\hline\n"

    bold = lambda s: "\\textbf{{{}}}".format(s)
    headers = ["heuristic field", "heuristic value", "total", "timeouts", "mean time",\
            "max time", "mean count", "max count", "count per sec"]
    builder += " & ".join(map(bold, headers)) + " \\\\\\hline\n"

    for hf in heuristic_field:
        for hv in heuristic_value:
            sudokus = Sudoku.load(filename)[:maxcases]
            results = benchmark(sudokus, hf, hv, timeout)

            results = [hf.__name__, hv.__name__] + list(map(str, results))
            builder += " & ".join(results) + " \\\\\\hline\n"

    builder += "\\end{tabular}\n"

    print()
    print(builder)
