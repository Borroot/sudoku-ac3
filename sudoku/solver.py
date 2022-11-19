from sudoku import Sudoku
from ac3 import Ac3
from stats import Stats
import heuristic as h

from threading import Thread, Event
import copy
import time
import queue
import math


def field(ac3, heuristic):
    """Give the next best field using the heuristic."""
    best_value = -math.inf
    best_field = None

    for y in range(9):
        for x in range(9):
            if len(ac3.domain[y][x]) > 1 and (value := heuristic(ac3, x, y)) > best_value:
                best_value = value
                best_field = (x, y)

    return best_field


def values(ac3, heuristic, x, y):
    """Give a sorted list of the possible values using the heuristic."""
    domain = copy.deepcopy(ac3.domain[y][x])
    domain = list(map(lambda v: (heuristic(ac3, x, y, v), v), domain))
    domain.sort(reverse = True)
    domain = list(map(lambda entry: entry[1], domain))
    return domain


def dfs(ac3, heuristic_field, heuristic_value, stats, timeout_event):
    """Run a depth first search using the heuristics and AC-3."""
    if timeout_event is not None and timeout_event.is_set():
        return None

    stats.nodecount += 1

    if (solution := ac3.solution()) is not None:
        return solution

    next_field = field(ac3, heuristic_field)
    if next_field is None:
        return None

    x, y = next_field
    for value in values(ac3, heuristic_value, x, y):
        if ac3.check_set(x, y, value):
            solution = dfs(ac3, heuristic_field, heuristic_value, stats, timeout_event)
            if solution is not None:
                return solution
        ac3.uncheck()

    return None


def dfs_timed(ac3, heuristic_field, heuristic_value, stats, timeout):
    """Request a solution within the given number of seconds."""
    if timeout is None:
        return dfs(ac3, heuristic_field, heuristic_value, stats)

    timeout_event = Event()
    que = queue.Queue()

    thread = Thread(
            target = lambda q, *args: q.put(dfs(*args)),
            args = (que, ac3, heuristic_field, heuristic_value, stats, timeout_event)
    )

    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        timeout_event.set()
        thread.join()
        stats.timeout = True
        return None
    else:
        return que.get()


def solve(sudoku, heuristic_field = h.nop, heuristic_value = h.nop, timeout=None):
    """Solve the sudoku using AC-3 and possible a DFS with the given heuristics."""
    ac3 = Ac3(sudoku)

    stats = Stats(time.time(), heuristic_field, heuristic_value)
    stats.domainspace_init = stats.domainspace_size(ac3.domain)

    ac3.check_all()
    solution = ac3.solution()

    stats.domainspace_dfs = stats.domainspace_size(ac3.domain)

    if (solution := ac3.solution()) is None:
        solution = dfs_timed(ac3, heuristic_field, heuristic_value, stats, timeout)
        stats.end_time = time.time()
        if solution is not None: stats.correct = solution.isvalid()
        return solution, stats
    else:
        stats.end_time = time.time()
        stats.correct = solution.isvalid()
        return solution, stats


if __name__ == "__main__":
    for index, sudoku in enumerate(Sudoku.load("data/unbiased.txt", 10)):
        solution, stats = solve(sudoku, h.lrv, h.mcv, timeout = 10)

        print(sudoku)
        if solution is not None: print(solution)

        print(stats)
