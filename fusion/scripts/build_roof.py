# Roof equipment (component "Roof Rack"): tubular steel rack clamped to the drip rails (4 feet, perimeter frame,
# cross bars, longitudinal slats) and the small yellow-orange taxi roof light on the front cross bar with
# "TAXI" (front) / "للأجرة" (rear) lettering (CoreText SVG outlines, see ../lettering).
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())
exec(open(os.path.join(ROOT, '_geom.py')).read(), globals())

PARAMS = [
    ('rack_x0', '1640 mm', 'Roof rack front rail x (photos 2011/2014, MED)'),
    ('rack_x1', '2900 mm', 'Roof rack rear rail x (photos 2011/2014, MED)'),
    ('rack_hw', '570 mm', 'Roof rack frame half width (photos, MED)'),
    ('rack_h', '95 mm', 'Rack rail centre height above the roof crown (photos, MED)'),
    ('rack_tube_r', '12 mm', 'Rack tube radius (25 mm tube, est.)'),
    ('sign_w', '300 mm', 'Taxi roof light width (livery notes: ~250 +/-20 %, MED)'),
    ('sign_h', '125 mm', 'Taxi roof light height (livery notes, MED)'),
    ('sign_d', '120 mm', 'Taxi roof light depth along the car (livery notes, MED)'),
]

def run(_context: str):
    for n, e, c in PARAMS:
        param(n, e, 'mm', c, update=True)
    C = get_comp('Roof Rack')
    wipe(C)
    g = G()
    rh = g['roof_h']
    x0, x1, rw, hr, tr = ev('rack_x0'), ev('rack_x1'), ev('rack_hw'), ev('rack_h'), ev('rack_tube_r')
    yr = rh + hr
    steel = color_app('Rack Steel (black, worn)', 'Paint - Enamel Glossy (Black)', (40, 40, 38))
    rubber = color_app('Black Rubber', 'Rubber - Soft', (22, 22, 22))
    parts = []
    # perimeter frame with rounded corners (pipe through corner points)
    k = 60
    frame = [(x0 + k, yr, -rw), (x1 - k, yr, -rw), (x1, yr, -rw + k), (x1, yr, rw - k), (x1 - k, yr, rw), (x0 + k, yr, rw),
             (x0, yr, rw - k), (x0, yr, -rw + k)]
    parts.append(('Rack frame', tpipe(frame, tr, closed=True), steel))
    # cross bars and longitudinal slats
    for x in [x0 + (x1 - x0) * f for f in (0.25, 0.5, 0.75)]:
        parts.append(('Rack cross bar', tcyl((x, yr, -rw), (x, yr, rw), tr * 0.8), steel))
    for z in (-rw / 3, rw / 3):
        parts.append(('Rack slat', tcyl((x0, yr - 2, z), (x1, yr - 2, z), tr * 0.6), steel))
    # feet: leg from the frame corner down to a gutter clamp on the drip rail
    yd = g['win_top'] + 38
    zd = hw_at(g, yd) + 5
    for x in (x0 + 90, x1 - 90):
        for s in (1, -1):
            top = (x, yr, s * rw)
            foot = (x, yd + 20, s * (zd - 8))
            parts.append(('Rack leg', tcyl(top, foot, tr * 0.9), steel))
            parts.append(('Rack foot pad', tbox(x, rh - g['roof_crown'] + 4, s * (zd - 40), 70, 12, 60), rubber))
            parts.append(('Rack gutter clamp', tbox(x, yd + 8, s * (zd + 2), 50, 40, 10), steel))
    commit(C, parts, 'Roof rack')

    # ---- taxi roof light on the front cross bar (rounded-top trapezoid box)
    sw, sh, sd = ev('sign_w'), ev('sign_h'), ev('sign_d')
    xs, yb = x0 + 10, yr + tr
    sign_mat = color_app('Taxi Sign Yellow-Orange', 'Plastic - Glossy (Yellow)', (246, 176, 20))
    base = tbox(xs, yb + 8, 0, sd + 20, 16, sw + 20)
    body = tbox(xs, yb + 16 + (sh - 30) / 2, 0, sd, sh - 30, sw)
    top = tcyl((xs, yb + sh - 30, -sw / 2), (xs, yb + sh - 30, sw / 2), sd / 2)
    tsub(top, tbox(xs, yb + sh - 30 - sd / 2, 0, sd + 2, sd, sw + 2))
    tunion(body, top)
    commit(C, [('Roof sign base', base, steel), ('Roof sign', body, sign_mat)], 'Roof sign')
    ink = color_app('Sign Black', 'Paint - Enamel Glossy (Black)', (18, 18, 18))
    # front face (normal -X): YZ-parallel plane; seen from ahead sketch +x is the viewer's left -> mirrored SVG
    pf = offset_plane(C, C.yZConstructionPlane, xs - sd / 2 + 0.2, 'Sign front plane')
    place_svg(C, pf, 'sign_taxi_L.svg', 0, yb + 34, 46, -0.8, 'Roof sign text TAXI', ink)
    pr = offset_plane(C, C.yZConstructionPlane, xs + sd / 2 - 0.2, 'Sign rear plane')
    place_svg(C, pr, 'sign_ujra_R.svg', 0, yb + 30, 58, 0.8, 'Roof sign text Ujra', ink)
    print('roof bodies:', C.bRepBodies.count)
