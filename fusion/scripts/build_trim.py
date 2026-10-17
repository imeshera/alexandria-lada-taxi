# Exterior trim (component "Trim"): window chrome, windscreen/rear-screen rubbers with chrome inserts, belt mouldings,
# drip rails, door handles + lock, door rubbing strips, door mirrors, wipers, side markers, C-pillar vents, fuel flap.
# Outlines come from _geom.py so they follow the openings.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())
exec(open(os.path.join(ROOT, '_geom.py')).read(), globals())

PARAMS = [
    ('handle_y', '805 mm', 'Door handle centre height (drawing ~790-826, MED)'),
    ('handle_f_x', '1985 mm', 'Front door handle centre x (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('handle_r_x', '2840 mm', 'Rear door handle centre x (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('rub_y', '462 mm', 'Door rubbing strip centre height (drawing ~450, photos; MED)'),
    ('rub_h', '26 mm', 'Door rubbing strip height (photos, MED)'),
    ('mirror_x', '1215 mm', 'Door mirror base x (photos, MED)'),
    ('marker_x', '200 mm', 'Front wing side repeater x (drawing, MED)'),
    ('marker_y', '640 mm', 'Front wing side repeater height (drawing, MED)'),
    ('fuel_x', '3560 mm', 'Fuel filler flap centre x, right rear wing (photos, LOW)'),
    ('fuel_y', '740 mm', 'Fuel filler flap centre height (photos, LOW)'),
]

def run(_context: str):
    for n, e, c in PARAMS:
        param(n, e, 'mm', c, update=True)
    C = get_comp('Trim')
    wipe(C)
    g = G()
    chrome = lib_app('Chrome')
    rubber = color_app('Black Rubber', 'Rubber - Soft', (22, 22, 22))
    blackp = color_app('Black Plastic (weathered)', 'Plastic - Matte (Black)', (34, 34, 33))
    amber = color_app('Amber Lens (opaque)', 'Plastic - Glossy (Red)', (250, 140, 20))
    mirror_glass = lib_app('Chrome', 'Mirror Glass')

    # ---- side window chrome rings + belt mouldings (both sides)
    for side, tag in ((1, ' R'), (-1, ' L')):
        outer = side_window_polys(g, grow=18)
        inner = side_window_polys(g, grow=2)
        for o, i, nm in zip(outer, inner, ('front', 'rear')):
            plate3d(C, on_side(g, o, 1.5, side), 3, 'Window chrome ' + nm + tag, holes=[on_side(g, i, 1.5, side)], ap=chrome)
        # belt moulding: a thin chrome strip along the window base, A-pillar to C-pillar
        x0, x1 = wsk_x(g, g['belt_h']) + g['pillar_w'] - 25, g['rdw_x1'] + 20
        yb = g['belt_h']
        poly = [(x0, yb - 14), (x1, yb - 14), (x1, yb + 2), (x0, yb + 2)]
        plate3d(C, [(x, y, side * (side_hw(g, yb) - 4 + 2.5)) for x, y in poly], 5, 'Belt moulding' + tag, ap=chrome)

    # ---- rear door fixed quarter-light divider (black channel)
    for side in (1, -1):
        dx = ev('rdw_div_x')
        poly = [(dx - 9, g['belt_h'] - 2), (dx + 9, g['belt_h'] - 2), (dx + 9, g['win_top'] + 4), (dx - 9, g['win_top'] + 4)]
        plate3d(C, on_side(g, poly, -2, side), 16, 'Quarter-light divider', ap=rubber)

    # ---- windscreen / rear screen: black rubber ring + chrome insert, following the curved screens
    for b in screen_band(C, g, -1.5, 3.5, 22, -4, 'Screen rubber', ap=rubber):
        b.name = ('Windscreen' if b.name.endswith('ws') else 'Rear screen') + ' rubber'
    for b in screen_band(C, g, 2.5, 5.0, 15, 9, 'Screen chrome', ap=chrome):
        b.name = ('Windscreen' if b.name.endswith('ws') else 'Rear screen') + ' chrome'

    parts = []
    # ---- drip rails: along the roof edge and down the A-pillar (both sides)
    ydr = g['win_top'] + 38
    for side in (1, -1):
        pts = []
        for y in (g['belt_h'] + 40, (g['belt_h'] + ydr) / 2, ydr):
            pts.append((wsk_x(g, y) + 14, y, side * (hw_at(g, y) + 5)))
        pts.append((rsk_x(g, ydr) - 30, ydr, side * (hw_at(g, ydr) + 5)))
        parts.append(('Drip rail', tpipe(pts, 5), chrome))

    # ---- door handles (chrome pull bar + black recess plate) and front-door lock cylinders
    hy = ev('handle_y')
    zs = side_hw(g, hy)
    for side in (1, -1):
        for hx in (ev('handle_f_x'), ev('handle_r_x')):
            parts.append(('Door handle recess', tbox(hx, hy, side * (zs + 1), 120, 36, 2), blackp))
            bar = tbox(hx, hy + 2, side * (zs + 7), 104, 18, 10)
            parts.append(('Door handle', bar, chrome))
        parts.append(('Door lock', tcyl((ev('handle_f_x') + 85, hy + 2, side * zs), (ev('handle_f_x') + 85, hy + 2, side * (zs + 6)), 9), chrome))

    # ---- rubbing strips on the doors (black rubber, chrome insert), split at the door shut line
    ry, rh_ = ev('rub_y'), ev('rub_h')
    zr = side_hw(g, ry)
    segs = [(ev('door_f_x0') + 6, g['b_pillar_x'] - 5), (g['b_pillar_x'] + 5, ev('door_r_x1') - 6)]
    for side in (1, -1):
        for a, b in segs:
            parts.append(('Rubbing strip', tbox((a + b) / 2, ry, side * (zr + 5), b - a, rh_, 12), rubber))
            parts.append(('Rubbing strip chrome', tbox((a + b) / 2, ry, side * (zr + 11.2), b - a - 4, 4, 1.5), chrome))

    # ---- door mirrors (black): base on the door at the front of the glass, arm, head with glass facing back
    mx = ev('mirror_x')
    for side in (1, -1):
        zb = side_hw(g, g['belt_h']) - 6
        parts.append(('Mirror base', tbox(mx + 10, g['belt_h'] + 30, side * (zb + 6), 80, 50, 14), blackp))
        parts.append(('Mirror arm', tcyl((mx + 20, g['belt_h'] + 40, side * (zb + 12)), (mx + 40, g['belt_h'] + 85, side * (zb + 75)), 11), blackp))
        head = tbox(mx + 50, g['belt_h'] + 95, side * (zb + 100), 55, 100, 150)
        parts.append(('Mirror head', head, blackp))
        parts.append(('Mirror glass', tbox(mx + 79, g['belt_h'] + 95, side * (zb + 100), 3, 88, 138), mirror_glass))

    # ---- wipers parked along the curved windscreen base (LHD: park towards the left), blades follow the glass
    yw = g['cowl_h'] + 50
    for zc in (-250, 290):
        zs_ = [zc - 440 + 440 * k / 8 for k in range(9)]
        parts.append(('Wiper blade', tpipe([(front_x(g, yw, z, 9), yw, z) for z in zs_], 5), blackp))
        parts.append(('Wiper arm', tpipe([(front_x(g, yw + 18, z, 15), yw + 18, z) for z in zs_[1:]], 4), blackp))
        x0 = front_x(g, g['cowl_h'], zc, 0) - 45
        parts.append(('Wiper spindle', tcyl((x0, g['cowl_h'] - 10, zc), (x0, g['cowl_h'] + 22, zc), 12), blackp))
        parts.append(('Wiper arm', tpipe([(x0, g['cowl_h'] + 22, zc), (front_x(g, yw + 18, zc, 15), yw + 18, zc)], 5), blackp))

    # ---- front wing side markers (amber)
    mkx, mky = ev('marker_x'), ev('marker_y')
    for side in (1, -1):
        parts.append(('Side marker', tbox(mkx, mky, side * (side_hw(g, mky) - 20 + 3), 58, 24, 8), amber))

    # ---- C-pillar air extractor vents (black, horizontal slats)
    for side in (1, -1):
        # louvred extractor low on the C-pillar, just above the belt (CC0 side photo, Moscow 2025)
        x0, x1, y0, y1 = g['rdw_x1'] + 75, g['rdw_x1'] + 290, g['belt_h'] + 40, g['belt_h'] + 105
        poly = [(x0, y0), (x1, y0), (x1 - (y1 - y0) * 0.6, y1), (x0, y1)]
        plate3d(C, on_side(g, poly, 1.5, side), 3, 'C-pillar vent', ap=blackp)
        for k in range(4):
            yk = y0 + 10 + k * 15
            parts.append(('C-pillar vent slat', tbox((x0 + x1) / 2 - 15, yk, side * (hw_at(g, yk) + 4), x1 - x0 - 60, 5, 3), rubber))

    # ---- fuel filler flap (right rear wing)
    fx, fy = ev('fuel_x'), ev('fuel_y')
    zf = side_hw(g, fy)
    parts.append(('Fuel flap', tcyl((fx, fy, zf - 2), (fx, fy, zf + 1.2), 52), None))
    commit(C, parts, 'Trim hardware')
    print('trim bodies:', C.bRepBodies.count)
