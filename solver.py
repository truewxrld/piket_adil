from dataclasses import dataclass
from time import perf_counter


ALGORITHMS = {
    "bt": "Backtracking",
    "fc": "Backtracking + FC",
    "mrv": "Backtracking + MRV",
}


def can_place(schedule, day, person, unavailable):
    if day + 1 in unavailable.get(person, set()):
        return False
    for neighbor in (day - 1, day + 1):
        if 0 <= neighbor < len(schedule) and schedule[neighbor] == person:
            return False
    return True


@dataclass
class Statistics:
    assignments: int = 0
    backtracks: int = 0
    time_ms: float = 0.0


class Solver:
    def __init__(self, day_count, residents, unavailable, algorithm="bt"):
        if day_count < 1 or not residents or len(set(residents)) != len(residents):
            raise ValueError("Jumlah hari harus positif dan nama penghuni harus unik.")
        if algorithm not in ALGORITHMS:
            raise ValueError("Algoritma tidak dikenal.")
        self.day_count = day_count
        self.residents = list(residents)
        self.unavailable = {name: set(unavailable.get(name, ())) for name in residents}
        self.algorithm = algorithm
        self.schedule = [None] * day_count
        self.stats = Statistics()
        self.finished = False
        self.solved = False
        self.active_day = None
        self.event = "ready"
        self._steps = self._run()

    def _run(self):
        domains = [
            [name for name in self.residents if day + 1 not in self.unavailable[name]]
            for day in range(self.day_count)
        ]
        if all(domains):
            self.solved = yield from self._search(domains)

    def _search(self, domains):
        empty_days = [day for day, person in enumerate(self.schedule) if person is None]
        if not empty_days:
            return True

        day = empty_days[0]
        if self.algorithm == "mrv":
            day = min(empty_days, key=lambda d: sum(
                can_place(self.schedule, d, name, self.unavailable)
                for name in domains[d]
            ))

        for person in domains[day]:
            legal = can_place(self.schedule, day, person, self.unavailable)
            self.stats.assignments += 1
            self.schedule[day] = person
            yield "assign", day

            if not legal:
                self.schedule[day] = None
                yield "reject", day
                continue

            next_domains = domains
            possible = True
            if self.algorithm == "fc":
                next_domains = [values.copy() for values in domains]
                for neighbor in (day - 1, day + 1):
                    if 0 <= neighbor < self.day_count and self.schedule[neighbor] is None:
                        next_domains[neighbor] = [
                            name for name in next_domains[neighbor] if name != person
                        ]
                        if not next_domains[neighbor]:
                            possible = False

            if possible and (yield from self._search(next_domains)):
                return True

            self.schedule[day] = None
            self.stats.backtracks += 1
            yield "backtrack", day
        return False

    def advance(self):
        if self.finished:
            return
        start = perf_counter()
        try:
            self.event, self.active_day = next(self._steps)
        except StopIteration:
            self.finished = True
            self.event = "done"
            self.active_day = None
        finally:
            self.stats.time_ms += (perf_counter() - start) * 1000

    def solve(self):
        while not self.finished:
            self.advance()
        return self.schedule.copy() if self.solved else None
