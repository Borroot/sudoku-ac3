"""
For all the heuristics a higher value means a better value.
We have 5 heuristics for choosing a field: nop, lf, mf, lrv, mrv.
We have 3 heuristics for choosing a value: nop, lcv, mcv.
"""

def nop(_ac3, _x=None, _y=None, _value=None):
    """No operation heuristic."""
    return 0


def lf(ac3, x, y):
    """Least finalized values heuristic."""
    return -mf(ac3, x, y)


def mf(ac3, x, y):
    """Most finalized values heuristic."""
    return sum(1 for rx, ry in ac3.relations[y][x] if len(ac3.domain[ry][rx]) == 1)


def lrv(ac3, x, y):
    """Least remaining values heuristic."""
    return -mrv(ac3, x, y)


def mrv(ac3, x, y):
    """Most remaining values heuristic."""
    return len(ac3.domain[y][x])


def lcv(ac3, x, y, value):
    """Least constraining value heuristic."""
    return -mcv(ac3, x, y, value)


def mcv(ac3, x, y, value):
    """Most constraining value heuristic."""
    return sum(1 for rx, ry in ac3.relations[y][x] if value in ac3.domain[ry][rx])
