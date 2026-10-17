# Light weathering (component "Weathering"): irregular rust blisters on the sills, wheel-arch lips and door bottoms
# (the typical rot points on old Ladas - see the CC0 Moscow 2025 side photo and the Alexandria photos), plus a
# couple of scuffs on the bumper ends. Thin (0.5 mm) blob decals following the side surface. Seeded, repeatable.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())
exec(open(os.path.join(ROOT, '_geom.py')).read(), globals())
import random

def blob(cx, cy, r, rnd, n=11):
    return [(cx + r * (0.55 + 0.45 * rnd.random()) * math.cos(2 * math.pi * k / n) * 1.6,
             cy + r * (0.55 + 0.45 * rnd.random()) * math.sin(2 * math.pi * k / n)) for k in range(n)]

def run(_context: str):
    C = get_comp('Weathering')
    wipe(C)
    g = G()
    rust = color_app('Rust (blistered)', 'Steel - Rough', (122, 62, 30))
    rnd = random.Random(2107)
    xf, xr, cy = ev('axle_f_x'), ev('axle_f_x') + ev('wheelbase'), ev('wheel_cy')
    ar = ev('arch_r')
    spots = []
    # arch lips: just outside the arch cut-out, rear arches worse than front
    for xa, n, a0, a1 in ((xf, 2, 40, 140), (xr, 4, 25, 155)):
        for k in range(n):
            a = math.radians(a0 + (a1 - a0) * (k + 0.5) / n + rnd.uniform(-8, 8))
            spots.append((xa + (ar + 22) * math.cos(a), cy + (ar + 22) * math.sin(a), rnd.uniform(9, 16)))
    # sills and door bottoms
    for x in (1300, 1650, 2300, 2650, 3150):
        spots.append((x + rnd.uniform(-60, 60), ev('sill_h') + rnd.uniform(15, 40), rnd.uniform(8, 15)))
    for x in (ev('door_f_x0') + 40, ev('b_pillar_x') - 60, ev('door_r_x1') - 260):
        spots.append((x, ev('door_bot_h') + 25, rnd.uniform(7, 12)))
    nb = 0
    for side in (1, -1):
        for x, y, r in spots:
            if rnd.random() < 0.25:
                continue                                # not every spot on both sides
            pts = blob(x, y, r, rnd)
            plate3d(C, [(px, py, side * (side_hw(g, py) + 0.25)) for px, py in pts], 0.5, 'Rust spot', ap=rust)
            nb += 1
    print('rust spots:', nb)
