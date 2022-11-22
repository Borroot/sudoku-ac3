from sudoku import Sudoku
from stats import Stats
from solver import solve
import heuristic as h
import multiprocessing as mp
import os
import time


def process_benchmark(sudokus, hf, hv, timeout, q, index, total_count):
    hfn = hf.__name__
    hvn = hv.__name__

    start = time.time()
    print(f"\033[{index + 4};0f{index + 1:2d}/{total_count} benchmark with hf = {hfn:3s} and hv = {hvn}...",
          end='', flush=True)

    results = benchmark(sudokus, hf, hv, timeout, index)
    print(f"\033[{index + 4};46f done in {(time.time() - start)/60:.2f} minutes", end='', flush=True)

    if results[0] == results[1]: # only timeouts
        results = [hfn, hvn] + list(map(str, results[:2])) + 5 * ["-"]
    else:
        results = [hfn, hvn] + list(map(str, results))

    q.put(" & ".join(results) + " \\\\\\hline\n")


def benchmark(sudokus, heuristic_field, heuristic_value, timeout, process_index):
    """Benchmark the given set of sudokus using the provided heuristics."""
    timeouts = 0
    nodecounts = []
    times = []

    for index, sudoku in enumerate(sudokus):
        print(f"\033[{process_index + 4};46f at {index + 1}", end='', flush=True)
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
    filename = "data/unbiased.txt"
    maxcases = 200

    heuristic_field = [h.nop, h.lf, h.mf, h.lrv, h.mrv]
    heuristic_value = [h.nop, h.lcv, h.mcv]
    timeout = 10

    os.system("clear")

    print(f"loading {maxcases} sudokus from {filename}...", end='', flush=True)
    sudokus = Sudoku.load(filename, maxcases)
    print("done")

    print(mp.cpu_count(), "cpu's detected")

    builder = ""
    builder += "\\begin{tabular}{|c|c|c|c|c|c|c|c|c|}\\hline\n"

    bold = lambda s: "\\textbf{{{}}}".format(s)
    headers = ["heuristic field", "heuristic value", "total", "timeouts", "mean time",\
            "max time", "mean count", "max count", "count per sec"]
    builder += " & ".join(map(bold, headers)) + " \\\\\\hline\n"

    total_count = len(heuristic_field) * len(heuristic_value)
    queues = [mp.Queue() for _ in range(total_count)]
    processes = []

    index = 0
    for hf in heuristic_field:
        for hv in heuristic_value:
            # start a new process to run benchmarks concurrently
            processes.append(
                mp.Process(
                    target = process_benchmark,
                    args = (sudokus, hf, hv, timeout, queues[index], index, total_count,)
                )
            )
            processes[index].start()
            index += 1

    for index in range(total_count):
        builder += queues[index].get()
        processes[index].join()

    builder += "\\end{tabular}\n"

    print(f"\033[{total_count + 4};0f")
    print(builder)
