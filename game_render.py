import pygame
from game_logic import LEVELS, find_conflicts
from solver import ALGORITHMS


SIZE = (1200, 720)
BG = (245, 243, 236)
INK = (30, 47, 65)
MUTED = (100, 113, 124)
WHITE = (255, 255, 255)
LINE = (220, 225, 224)
TEAL = (18, 116, 115)
RED = (174, 51, 65)
RED_BG = (255, 226, 229)
GREEN_BG = (225, 241, 233)
AMBER = (230, 165, 48)


def make_fonts():
    return {size: pygame.font.SysFont("Arial", size, bold=(size >= 24))
            for size in (14, 16, 18, 20, 24, 32)}


def draw(screen, game, fonts):
    screen.fill(BG)
    buttons = {}

    def text(value, x, y, size=18, color=INK):
        screen.blit(fonts[size].render(str(value), True, color), (x, y))

    def box(rect, color, border=None):
        pygame.draw.rect(screen, color, rect, border_radius=10)
        if border:
            pygame.draw.rect(screen, border, rect, 2, border_radius=10)

    def button(action, rect, label, selected=False, enabled=True):
        rect = pygame.Rect(rect)
        fill = TEAL if selected and enabled else WHITE
        box(rect, fill, LINE)
        color = WHITE if selected and enabled else (INK if enabled else MUTED)
        surface = fonts[16].render(label, True, color)
        screen.blit(surface, surface.get_rect(center=rect.center))
        if enabled:
            buttons[action] = rect

    text("PIKET ADIL", 28, 18, 32)
    text("Jadwal Piket Kos/Asrama  /  Simulasi CSP", 29, 57, 18, MUTED)
    text("KKA  |  KELOMPOK 11", 968, 32, 16, TEAL)
    for i, level in enumerate(LEVELS):
        label = f"Level {i + 1}  /  {level.days} hari, {len(level.residents)} orang"
        button(("level", i), (28 + i * 272, 100, 258, 38), label,
               i == game.level_index, not game.running)
    for i, (key, label) in enumerate(ALGORITHMS.items()):
        button(("algorithm", key), (28 + i * 272, 148, 258, 38), label,
               key == game.algorithm, not game.running)

    errors = find_conflicts(game.schedule, game.level.unavailable)
    text(f"JADWAL / {game.level.title.upper()}", 28, 205, 16, MUTED)
    filled = sum(name is not None for name in game.schedule)
    text(f"{filled}/{game.level.days} hari terisi", 684, 205, 16, MUTED)
    weekdays = ("Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min")
    for day, person in enumerate(game.schedule):
        x, y = 28 + (day % 7) * 116, 238 + (day // 7) * 94
        rect = pygame.Rect(x, y, 104, 82)
        fill = RED_BG if day in errors else (GREEN_BG if person else WHITE)
        border = TEAL if day == game.selected_day else LINE
        if day == game.active_day:
            border = AMBER
        box(rect, fill, border)
        text(f"{weekdays[day % 7]} / {day + 1:02}", x + 10, y + 10, 16, MUTED)
        text(person or "Pilih...", x + 10, y + 37, 18, RED if day in errors else INK)
        if not game.running:
            buttons[("day", day)] = rect

    selected = game.selected_day
    heading = f"PENGHUNI / HARI {selected + 1}" if selected is not None else "PENGHUNI / PILIH HARI DAHULU"
    text(heading, 28, 438, 16, MUTED)
    for i, person in enumerate(game.level.residents):
        blocked = selected is not None and selected + 1 in game.level.unavailable[person]
        label = person + ("  /  berhalangan" if blocked else "")
        button(("person", person), (28 + (i % 3) * 272, 467 + (i // 3) * 48, 258, 40),
               label, selected is not None and game.schedule[selected] == person,
               not game.running and selected is not None)
    button(("clear", None), (28, 572, 190, 36), "Kosongkan hari",
           enabled=selected is not None and not game.running)
    detail = "Merah: melanggar aturan. Bingkai kuning: langkah solver."
    if selected in errors:
        detail = " ".join(dict.fromkeys(errors[selected]))
    text(detail, 238, 581, 16, RED if selected in errors else MUTED)
    box((28, 634, 802, 52), WHITE)
    text("Animasi dijeda." if game.paused else game.message, 42, 651, 16)

    box((850, 94, 322, 592), WHITE)
    button(("solve", None), (866, 110, 290, 44), "SOLVER  /  mulai dari kosong",
           selected=True, enabled=not game.running)
    button(("reset", None), (866, 166, 100, 36), "Reset")
    speed = game.SPEEDS[game.speed_index][0]
    button(("speed", None), (976, 166, 180, 36), f"Kecepatan: {speed}")
    button(("pause", None), (866, 214, 290, 36), "Lanjutkan" if game.paused else "Jeda animasi",
           enabled=game.running)

    text("STATISTIK SOLVER", 866, 268, 16, TEAL)
    stats = game.solver.stats if game.solver else None
    values = (
        ("Assignment (percobaan)", str(stats.assignments) if stats else "-"),
        ("Backtrack", str(stats.backtracks) if stats else "-"),
        ("Waktu komputasi", f"{stats.time_ms:.3f} ms" if stats else "-"),
    )
    for i, (label, value) in enumerate(values):
        y = 300 + i * 33
        text(label, 866, y, 16, MUTED)
        surface = fonts[18].render(value, True, INK)
        screen.blit(surface, surface.get_rect(topright=(1155, y)))
    text("Waktu tidak mencakup jeda animasi.", 866, 403, 14, MUTED)
    text("HARI BERHALANGAN", 866, 440, 16, TEAL)
    for i, person in enumerate(game.level.residents):
        days = ", ".join(str(d) for d in sorted(game.level.unavailable[person])) or "-"
        y = 469 + i * 33
        text(person, 866, y, 14, INK)
        text(days, 866, y + 15, 14, MUTED)

    text("1/2/3: level   Tab: algoritma   S: solver   Spasi: jeda   R: reset   F: kecepatan   Del: kosongkan   Esc: keluar",
         28, 697, 14, MUTED)
    return buttons
