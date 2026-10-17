# Running gear (component "Chassis"), schematic but dimensionally placed:
#  front: double wishbones, uprights, coil-over-shock (coils as stacked rings), anti-roll bar, crossmember, steering
#         linkage; drivetrain: engine block + sump, gearbox, propshaft with centre bearing;
#  rear: live axle (tubes + banjo diff housing), 4 trailing links, Panhard rod, coil springs, shocks;
#  exhaust: down-pipe, resonator, main silencer, tailpipe (exits rear left, LOW confidence).
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())

def coil(cx, y0, y1, cz, R, r, n):
    """Coil spring approximated by n tilted rings + a centre core removed later (visual)."""
    body = None
    for k in range(n):
        y = y0 + (k + 0.5) * (y1 - y0) / n
        t = ttorus((cx, y, cz), (0.12, 1, 0), R, r)
        body = t if body is None else tunion(body, t)
    return body

def run(_context: str):
    C = get_comp('Chassis')
    wipe(C)
    xf, xr = ev('axle_f_x'), ev('axle_f_x') + ev('wheelbase')
    cy = ev('wheel_cy')
    tf, trr = ev('track_f') / 2, ev('track_r') / 2
    steel = color_app('Chassis Black (dusty)', 'Paint - Enamel Glossy (Black)', (46, 45, 42))
    spring = color_app('Spring Steel (worn)', 'Paint - Enamel Glossy (Dark Grey)', (70, 70, 68))
    rust = color_app('Exhaust Rust', 'Steel - Rough', (112, 68, 40))
    alu = lib_app('Aluminum - Satin')
    iron = lib_app('Steel - Cast')
    parts = []
    for s in (1, -1):
        zk = s * (tf - 110)
        # front upright / knuckle
        parts.append(('Front upright', tbox(xf, cy, zk, 60, 230, 40), iron))
        # lower wishbone (two arms to inner pivots on the crossmember)
        for xi in (xf - 150, xf + 140):
            parts.append(('Lower wishbone', tcyl((xf, cy - 90, zk), (xi, cy - 60, s * 300), 16), steel))
        # upper wishbone
        for xi in (xf - 100, xf + 90):
            parts.append(('Upper wishbone', tcyl((xf, cy + 120, s * (tf - 130)), (xi, cy + 190, s * 360), 13), steel))
        # coil spring + shock between the lower arm and the body tower
        parts.append(('Front spring', coil(xf + 10, cy - 60, cy + 210, s * 420, 55, 7, 7), spring))
        parts.append(('Front shock', tcyl((xf + 10, cy - 70, s * 420), (xf + 10, cy + 260, s * 420), 20), steel))
        # rear: springs, shocks, trailing links
        parts.append(('Rear spring', coil(xr, cy + 40, cy + 280, s * 500, 60, 7, 6), spring))
        parts.append(('Rear shock', tcyl((xr + 60, cy - 40, s * 560), (xr - 40, cy + 300, s * 600), 20), steel))
        parts.append(('Lower trailing link', tcyl((xr, cy - 50, s * 520), (xr - 640, cy + 40, s * 560), 18), steel))
        parts.append(('Upper trailing link', tcyl((xr - 40, cy + 80, s * 260), (xr - 330, cy + 140, s * 330), 16), steel))
    # anti-roll bar, crossmember, steering track rod
    parts.append(('Anti-roll bar', tpipe([(xf - 40, cy - 70, 560), (xf - 260, cy - 30, 520), (xf - 260, cy - 30, -520), (xf - 40, cy - 70, -560)], 11), steel))
    parts.append(('Front crossmember', tbox(xf + 20, cy + 60, 0, 120, 80, 860), steel))
    parts.append(('Track rod', tcyl((xf + 130, cy - 20, -(tf - 160)), (xf + 130, cy - 20, tf - 160), 12), steel))
    parts.append(('Steering box', tbox(xf + 190, cy + 140, -360, 110, 90, 90), iron))
    # rear axle: tubes + banjo housing + pinion nose; Panhard rod
    parts.append(('Rear axle tube', tcyl((xr, cy, -(trr - 90)), (xr, cy, trr - 90), 38), steel))
    banjo = tsphere((xr, cy, 0), 135)
    tsub(banjo, tbox(xr, cy, 0, 400, 400, 200))           # flatten to a disc-like housing
    banjo = tunion(banjo, tcyl((xr, cy, -100), (xr, cy, 100), 135))
    parts.append(('Differential housing', banjo, steel))
    parts.append(('Pinion nose', tcyl((xr - 60, cy + 10, 0), (xr - 230, cy + 20, 0), 60, 45), steel))
    parts.append(('Panhard rod', tcyl((xr + 70, cy - 10, -(trr - 120)), (xr + 70, cy + 90, trr - 120), 14), steel))
    # drivetrain: engine block, sump, gearbox, propshaft (2 pieces + centre bearing)
    parts.append(('Engine block', tbox(620, 590, 0, 520, 360, 430), iron))
    parts.append(('Sump', tbox(600, 380, 0, 420, 90, 300), steel))
    parts.append(('Gearbox', tcyl((900, 470, 0), (1500, 430, 0), 150, 90), alu))
    parts.append(('Propshaft', tcyl((1500, 420, 0), (2250, 380, 0), 36), steel))
    parts.append(('Propshaft centre bearing', tbox(2250, 380, 0, 60, 80, 120), steel))
    parts.append(('Propshaft', tcyl((2250, 380, 0), (xr - 230, cy + 20, 0), 36), steel))
    # exhaust (car's left = -Z): down-pipe, resonator, over the axle, main silencer, tailpipe
    ex = [(820, 520, 160), (980, 300, 160), (1300, 290, 150), (1700, 290, 150)]
    parts.append(('Exhaust pipe', tpipe(ex, 24), rust))
    parts.append(('Resonator', tcyl((1700, 290, 150), (2150, 290, 150), 60), rust))
    ex2 = [(2150, 290, 150), (2600, 300, 160), (2850, 380, 200), (3200, 380, 230), (3350, 320, -200)]
    parts.append(('Exhaust pipe', tpipe(ex2, 22), rust))
    parts.append(('Main silencer', tbox(3500, 320, -380, 420, 120, 260), rust))
    parts.append(('Tailpipe', tpipe([(3710, 320, -450), (4000, 330, -460), (4160, 330, -460)], 22), rust))
    # fuel tank (in the boot floor, right side) and spare wheel well bulge are hidden; floor tunnel cover:
    parts.append(('Transmission tunnel', tbox(1900, ev('sill_h') + 90, 0, 1300, 180, 260), steel))
    commit(C, parts, 'Running gear')
    print('chassis bodies:', C.bRepBodies.count)
