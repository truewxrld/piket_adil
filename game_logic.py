from dataclasses import dataclass
from solver import ALGORITHMS, Solver


@dataclass
class Level:
    title: str
    days: int
    residents: tuple
    unavailable: dict


NAMES = ("Daffa", "Elmiro", "Bima", "Raka", "Nadia", "Salsa")
LEVELS = (
    Level("Santai", 5, NAMES[:4], {
        "Daffa": {2}, "Elmiro": {3}, "Bima": {1, 5}, "Raka": {4},
    }),
    Level("Sibuk", 7, NAMES[:5], {
        "Daffa": {2, 4, 6}, "Elmiro": {1, 3, 7}, "Bima": {2, 5},
        "Raka": {3, 4, 6}, "Nadia": {1, 5, 7},
    }),
    Level("Padat", 14, NAMES, {
        "Daffa": {9, 10, 11, 12, 13, 14},
        "Elmiro": {10, 11, 12, 13, 14},
        "Bima": {1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14},
        "Raka": {1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13},
        "Nadia": {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14},
        "Salsa": {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
    }),
)


def find_conflicts(schedule, unavailable):
    errors = {}
    for day, person in enumerate(schedule):
        if person is None:
            continue
        if day + 1 in unavailable.get(person, set()):
            errors.setdefault(day, []).append("Penghuni berhalangan.")
        if day > 0 and schedule[day - 1] == person:
            for index in (day - 1, day):
                errors.setdefault(index, []).append("Piket dua hari berturut-turut.")
    return errors


class Game:
    SPEEDS = (("Lambat", 220), ("Normal", 70), ("Cepat", 0))

    def __init__(self):
        self.level_index = 0
        self.algorithm = "bt"
        self.speed_index = 0
        self.reset()

    @property
    def level(self):
        return LEVELS[self.level_index]

    def reset(self):
        self.schedule = [None] * self.level.days
        self.selected_day = None
        self.active_day = None
        self.solver = None
        self.running = False
        self.paused = False
        self.wait_ms = 0
        self.message = "Klik satu hari, lalu pilih penghuni. Atau tekan Solver."

    def set_level(self, index):
        if not self.running and 0 <= index < len(LEVELS):
            self.level_index = index
            self.reset()

    def set_algorithm(self, algorithm):
        if not self.running and algorithm in ALGORITHMS:
            self.algorithm = algorithm
            self.reset()

    def select_day(self, day):
        if not self.running and 0 <= day < self.level.days:
            self.selected_day = day
            self.message = f"Hari {day + 1}: pilih penghuni atau kosongkan isinya."

    def assign(self, person):
        if self.running or self.selected_day is None:
            return
        if person is not None and person not in self.level.residents:
            return
        self.schedule[self.selected_day] = person
        self.solver = None  # Statistik lama tidak mewakili hasil edit manual.
        self.active_day = None
        errors = find_conflicts(self.schedule, self.level.unavailable)
        if errors:
            self.message = f"Ada pelanggaran pada {len(errors)} hari. Periksa kartu merah."
        elif all(name is not None for name in self.schedule):
            self.message = "Berhasil! Semua hari terisi dan kedua aturan terpenuhi."
        else:
            self.message = "Pilihan tersimpan. Lanjutkan mengisi hari yang kosong."

    def start_solver(self):
        if self.running:
            return
        self.reset()
        self.solver = Solver(
            self.level.days, self.level.residents, self.level.unavailable, self.algorithm
        )
        self.running = True
        self.message = "Solver dimulai dari jadwal kosong."

    def toggle_pause(self):
        if self.running:
            self.paused = not self.paused

    def cycle_speed(self):
        self.speed_index = (self.speed_index + 1) % len(self.SPEEDS)

    def update(self, dt_ms):
        if not self.running or self.paused:
            return
        self.wait_ms += dt_ms
        delay = self.SPEEDS[self.speed_index][1]
        if self.wait_ms < delay:
            return
        self.wait_ms = 0
        for _ in range(100 if delay == 0 else 1):
            self.solver.advance()
            if self.solver.finished:
                break
        self.schedule = self.solver.schedule.copy()
        self.active_day = self.solver.active_day
        if self.solver.finished:
            self.running = False
            self.message = (
                "Solver selesai. Jadwal memenuhi kedua aturan."
                if self.solver.solved else "Tidak ada solusi untuk data level ini."
            )
        else:
            action = {"assign": "mencoba penghuni", "reject": "menolak pilihan",
                      "backtrack": "mundur untuk mencari pilihan lain"}
            self.message = f"Hari {self.active_day + 1}: {action[self.solver.event]}."
