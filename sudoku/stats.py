class Stats:

    def __init__(self, start_time, heuristic_field, heuristic_value):
        """An object to keep statistics of the search."""
        self.start_time = start_time
        self.end_time = None
        self.timeout = False
        self.correct = None

        self.nodecount = 0
        self.domainspace_init = 0 # number possible of value assignments at the start
        self.domainspace_dfs = 0  # number possible of value assignments after ac3.check_all()

        self.heuristic_field = heuristic_field
        self.heuristic_value = heuristic_value


    @classmethod
    def domainspace_size(cls, domain):
        count = 1
        for y in range(9):
            for x in range(9):
                count *= len(domain[y][x])
        return count


    def __str__(self):
        builder = "\n".join([
            "total time: {}ms".format(round(self.end_time - self.start_time, 3)),
            "timeout: {}".format(self.timeout),
            "correct: {}\n".format(self.correct),
            "nodecount: {}".format(self.nodecount),
            "domainspace init: {:.1e}".format(self.domainspace_init),
            "domainspace dfs: {:.1e}\n".format(self.domainspace_dfs),
            "heuristic field: {}".format(self.heuristic_field.__name__),
            "heuristic value: {}".format(self.heuristic_value.__name__),
            "",
        ])
        return builder
