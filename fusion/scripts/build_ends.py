# Front and rear ends:
#  "Front End": 2107 chrome grille (frame, slats, bars, badge), rectangular headlamp units with outer amber
#               indicators, bonnet centre bulge, valance air slot, tow eye.
#  "Rear End":  tail-lamp clusters (indicator / tail-brake / reverse / fog segments), boot lock, LADA badge.
#  "Bumpers":   front + rear wrap-around bumpers (chrome top bar + black rubber/plastic lower + black end caps),
#               rear plate lamps, front plate bracket.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())
exec(open(os.path.join(ROOT, '_geom.py')).read(), globals())

PARAMS = [
    ('grille_hw', '345 mm', 'Grille half width incl. frame (factory drawing front view, 6.83 mm/px, MED)'),
    ('grille_bot', '570 mm', 'Grille bottom height (factory drawing front view, 6.83 mm/px, MED)'),
    ('grille_top', '828 mm', 'Grille top height, flush with the bonnet notch (factory drawing front view, 6.83 mm/px, MED)'),
    ('lamp_zi', '362 mm', 'Headlamp unit inner edge |z| (factory drawing front view, 6.83 mm/px, MED)'),
    ('lamp_zo', '728 mm', 'Headlamp unit outer edge |z| (factory drawing front view, 6.83 mm/px, MED)'),
    ('lamp_bot', '600 mm', 'Headlamp unit bottom height (factory drawing front view, 6.83 mm/px, MED)'),
    ('lamp_top', '790 mm', 'Headlamp unit top height (factory drawing front view, 6.83 mm/px, MED)'),
    ('ind_w', '85 mm', 'Amber indicator section width at the outer end of each unit (photos, MED)'),
    ('bump_f_bot', '380 mm', 'Front bumper bottom (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('bump_f_top', '510 mm', 'Front bumper top (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('bump_r_bot', '360 mm', 'Rear bumper bottom (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('bump_r_top', '490 mm', 'Rear bumper top (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('bump_corner_r', '185 mm', 'Bumper plan-view corner radius (photos, MED)'),
    ('tail_zi', '300 mm', 'Tail-lamp cluster inner edge |z| (rear photo 2017, MED)'),
    ('tail_bot', '585 mm', 'Tail-lamp cluster bottom height (drawing rear view, MED)'),
    ('tail_top', '770 mm', 'Tail-lamp cluster top height (drawing rear view, MED)'),
]

def bumper_plan(fx_face, depth, cr, hw_out, wrap_deg, rear=False, L=0):
    """Plan-view band (x, z) for a wrap-around bumper: outer face at x = fx_face, thickness depth."""
    cz = hw_out - cr
    def pts(r):
        out = []
        # front straight + corner arc on +z, mirrored to -z
        n = 10
        arc = []
        for k in range(n + 1):
            a = math.radians(wrap_deg * k / n)
            arc.append((fx_face + cr - r * math.cos(a), cz + r * math.sin(a)))
        return arc
    outer = pts(cr); inner = pts(cr - depth)
    poly = [(x, -z) for x, z in outer[::-1]] + outer + inner[::-1] + [(x, -z) for x, z in inner]
    if rear:
        poly = [(L - x, z) for x, z in poly]
    return poly

def run(_context: str):
    for n, e, c in PARAMS:
        param(n, e, 'mm', c, update=True)
    g = G()
    chrome = lib_app('Chrome')
    blackp = color_app('Black Plastic (weathered)', 'Plastic - Matte (Black)', (34, 34, 33))
    rubber = color_app('Black Rubber', 'Rubber - Soft', (22, 22, 22))
    clear = color_app('Headlamp Lens', 'Glass (Clear)', (235, 238, 240))
    refl = lib_app('Aluminum - Polished')
    amber = color_app('Amber Lens (opaque)', 'Plastic - Glossy (Red)', (250, 140, 20))
    red = color_app('Red Lens (opaque)', 'Plastic - Glossy (Red)', (185, 22, 18))
    fx, rx, L = ev('body_front_x'), ev('body_rear_x'), ev('len_overall')

    # ======================= FRONT END
    F = get_comp('Front End'); wipe(F)
    parts = []
    v2105 = round(evu('variant_2105')) == 1
    if not v2105:
        gw, gb, gt = ev('grille_hw'), ev('grille_bot'), ev('grille_top')
        gx = fx - 22                                    # grille face x (proud of the front panel)
        fr = 26                                         # chrome frame width
        # frame = 4 bars, black backing, slats + bars
        parts.append(('Grille frame', tbox(gx + 10, gt - fr / 2, 0, 20, fr, 2 * gw), chrome))
        parts.append(('Grille frame', tbox(gx + 10, gb + fr / 2, 0, 20, fr, 2 * gw), chrome))
        for s in (1, -1):
            parts.append(('Grille frame', tbox(gx + 10, (gb + gt) / 2, s * (gw - fr / 2), 20, gt - gb, fr), chrome))
        parts.append(('Grille backing', tbox(gx + 22, (gb + gt) / 2, 0, 6, gt - gb - 10, 2 * gw - 10), blackp))
        ns_ = 7
        for k in range(ns_):
            y = gb + fr + (k + 0.5) * (gt - gb - 2 * fr) / ns_
            parts.append(('Grille slat', tbox(gx + 12, y, 0, 6, 8, 2 * gw - 2 * fr), chrome))
        nb = 13
        for k in range(nb):
            z = -gw + fr + (k + 0.5) * (2 * gw - 2 * fr) / nb
            parts.append(('Grille bar', tbox(gx + 16, (gb + gt) / 2, z, 6, gt - gb - 2 * fr, 4), blackp))
        # VAZ badge: chrome shield with a red field at the top centre of the grille
        parts.append(('Badge', tbox(gx - 2, gt - fr - 40, 0, 6, 70, 52), chrome))
        parts.append(('Badge field', tbox(gx - 5.5, gt - fr - 40, 0, 1.5, 56, 40), red))
        # headlamp units: chrome/black bezel, clear lens (with a raised lens pattern), silver reflector, amber indicator
        zi, zo, lb, lt, iw = ev('lamp_zi'), ev('lamp_zo'), ev('lamp_bot'), ev('lamp_top'), ev('ind_w')
        for s in (1, -1):
            zc = s * (zi + zo) / 2
            parts.append(('Headlamp bezel', tbox(fx - 6, (lb + lt) / 2, zc, 12, lt - lb, zo - zi), blackp))
            zh0, zh1 = zi + 12, zo - iw - 6                # main headlamp lens span
            parts.append(('Headlamp reflector', tbox(fx - 4, (lb + lt) / 2, s * (zh0 + zh1) / 2, 4, lt - lb - 26, zh1 - zh0 - 6), refl))
            parts.append(('Headlamp lens', tbox(fx - 15, (lb + lt) / 2, s * (zh0 + zh1) / 2, 6, lt - lb - 22, zh1 - zh0), clear))
            for k in range(1, 6):                          # lens flutes
                z = zh0 + k * (zh1 - zh0) / 6
                parts.append(('Headlamp lens', tbox(fx - 18.5, (lb + lt) / 2, s * z, 1.5, lt - lb - 30, 3), clear))
            parts.append(('Indicator lens', tbox(fx - 14, (lb + lt) / 2, s * (zo - 6 - iw / 2), 8, lt - lb - 22, iw), amber))
            parts.append(('Headlamp trim', tbox(fx - 19, lt - 9, zc, 4, 6, zo - zi), chrome))
    else:
        # ---- VAZ-2105: low, flat black grille with fine horizontal bars spanning between plain rectangular
        # headlamps; the amber indicators sit in the bumper below the headlamps.
        gw, gb, gt = ev('grille_hw'), ev('grille_bot'), ev('grille_top')
        gx = fx - 14
        parts.append(('Grille backing', tbox(gx + 14, (gb + gt) / 2, 0, 6, gt - gb, 2 * gw), blackp))
        for k in range(9):
            y = gb + 8 + k * (gt - gb - 16) / 8
            parts.append(('Grille slat', tbox(gx + 8, y, 0, 8, 5, 2 * gw - 10), blackp))
        parts.append(('Grille frame', tbox(gx + 4, gt - 3, 0, 8, 6, 2 * gw), chrome))
        parts.append(('Badge', tbox(gx - 2, (gb + gt) / 2, 0, 6, 46, 46), chrome))
        parts.append(('Badge field', tbox(gx - 5.5, (gb + gt) / 2, 0, 1.5, 36, 36), red))
        zi, zo, lb, lt = ev('lamp_zi'), ev('lamp_zo'), ev('lamp_bot'), ev('lamp_top')
        for s in (1, -1):
            zc = s * (zi + zo) / 2
            parts.append(('Headlamp bezel', tbox(fx - 6, (lb + lt) / 2, zc, 12, lt - lb, zo - zi), chrome))
            parts.append(('Headlamp reflector', tbox(fx - 4, (lb + lt) / 2, zc, 4, lt - lb - 26, zo - zi - 30), refl))
            parts.append(('Headlamp lens', tbox(fx - 15, (lb + lt) / 2, zc, 6, lt - lb - 20, zo - zi - 20), clear))
            for k in range(1, 7):
                z = zi + 10 + k * (zo - zi - 20) / 7
                parts.append(('Headlamp lens', tbox(fx - 18.5, (lb + lt) / 2, s * z, 1.5, lt - lb - 30, 3), clear))
            parts.append(('Indicator lens', tbox(-4, (ev('bump_f_bot') + ev('bump_f_top')) / 2 - 10, s * (zo - 80), 10, 45, 120), amber))
    # (the raised bonnet centre is part of the body solid now - build_body.py)
    # valance air slot + tow eye
    parts.append(('Valance slot', tbox(fx - 1, ev('front_bot_h') + 40, 0, 4, 30, 520), blackp))
    parts.append(('Tow eye', ttorus((fx - 30, ev('front_bot_h') - 5, 420), (0, 0, 1), 22, 6), blackp))
    commit(F, parts, 'Front end parts')

    # ======================= REAR END
    R = get_comp('Rear End'); wipe(R)
    parts = []
    ti, tb, tt = ev('tail_zi'), ev('tail_bot'), ev('tail_top')
    to = g['hw'] - 95
    for s in (1, -1):
        parts.append(('Tail lamp housing', tbox(rx + 5, (tb + tt) / 2, s * (ti + to) / 2, 10, tt - tb, to - ti), chrome))
        # segments from outer to inner: indicator (amber), tail/brake (red), reverse (clear), fog (red)
        segs = [(amber, 0.24), (red, 0.36), (clear, 0.18), (red, 0.22)]
        if round(evu('variant_2105')) == 1:
            segs = [(amber, 0.22), (red, 0.30), (clear, 0.16), (red, 0.32)]   # 2105: tall vertical stop segment inboard
        z = to - 6
        span = to - ti - 12
        for ap, frac in segs:
            w = span * frac
            hh = tt - tb - 14
            if round(evu('variant_2105')) == 1 and ap is red and frac == 0.32:
                hh += 50                                       # the 2105's vertical stop lamp stands proud of the cluster
            parts.append(('Tail lamp lens', tbox(rx + 13, (tb + tt) / 2, s * (z - w / 2), 8, hh, w - 5), ap))
            z -= w
    # boot lock + LADA script badge on the boot lid rear edge
    parts.append(('Boot lock', tcyl((rx + 2, ev('rear_top_h') - 70, 0), (rx + 10, ev('rear_top_h') - 70, 0), 14), chrome))
    parts.append(('Rear badge', tbox(rx + 4, tt + 40, 0, 4, 18, 90), chrome))
    commit(R, parts, 'Rear end parts')

    # ======================= BUMPERS (plan-view bands extruded vertically)
    Bm = get_comp('Bumpers'); wipe(Bm)
    cr = ev('bump_corner_r')
    hwb = g['hw'] + 8
    if round(evu('variant_2105')) == 1:
        chrome = lib_app('Aluminum - Satin')              # 2105: aluminium bumpers with rubber strips
    specs = [
        ('Front bumper chrome', False, 0, ev('bump_f_top') - 40, ev('bump_f_top'), 42, 55, chrome),
        ('Front bumper rubber', False, 6, ev('bump_f_bot'), ev('bump_f_top') - 40, 40, 55, rubber),
        ('Rear bumper chrome', True, 0, ev('bump_r_top') - 36, ev('bump_r_top'), 42, 55, chrome),
        ('Rear bumper rubber', True, 6, ev('bump_r_bot'), ev('bump_r_top') - 36, 40, 55, rubber),
    ]
    for name, rear, inset, y0, y1, depth, wrap, ap in specs:
        sk = Bm.sketches.add(Bm.xZConstructionPlane); sk.name = name
        poly = bumper_plan(inset, depth, cr - inset, hwb - inset, wrap, rear, L)
        sk_poly(sk, [(x, -z) for x, z in poly])
        f = extrude(Bm, largest_profile(sk), y0, y1, NEW, name=name)
        for b in f.bodies:
            b.appearance = ap
        sk.isVisible = False
    # plate recess in the rear bumper centre (2107 rear bumper; the Egyptian plate is mounted on the tail panel above)
    sk = Bm.sketches.add(Bm.yZConstructionPlane); sk.name = 'Rear plate recess'
    sk_rrect(sk, -190, ev('bump_r_bot') + 12, 190, ev('bump_r_top') - 8, 12)
    extrude(Bm, profiles(sk), L - 14, L + 10, CUT, participants=[b for b in Bm.bRepBodies if b.name.startswith('Rear bumper')], name='Rear plate recess')
    sk.isVisible = False
    parts = []
    # rubber insert strips along the chrome bars, and rubber over-riders
    for x0, yb0, yb1, zo in ((0, ev('bump_f_top') - 40, ev('bump_f_top'), 300), (L, ev('bump_r_top') - 36, ev('bump_r_top'), 420)):
        sgn = -1 if x0 == 0 else 1
        parts.append(('Bumper rubber strip', tbox(x0 + sgn * 1.5, (yb0 + yb1) / 2, 0, 5, 12, 2 * (hwb - cr) - 20), rubber))
        for zz in (-zo, zo):
            ov = tbox(x0 + sgn * 6, (yb0 + yb1) / 2 - 20, zz, 26, yb1 - yb0 + 70, 55)
            parts.append(('Over-rider', ov, rubber))
    # black end caps where the bumpers wrap onto the body sides
    for s in (1, -1):
        for x, y0, y1 in ((fx + 140, ev('bump_f_bot'), ev('bump_f_top')), (rx - 140, ev('bump_r_bot'), ev('bump_r_top'))):
            parts.append(('Bumper end cap', tbox(x, (y0 + y1) / 2, s * (hwb - 12), 130, y1 - y0 + 6, 26), blackp))
    # mounting brackets (front + rear), rear plate lamps in the bumper top
    for s in (1, -1):
        parts.append(('Bumper bracket', tbox(fx - 10, ev('bump_f_bot') + 20, s * 420, 70, 30, 40), blackp))
        parts.append(('Bumper bracket', tbox(rx + 10, ev('bump_r_bot') + 20, s * 420, 70, 30, 40), blackp))
        parts.append(('Plate lamp', tbox(L - 40, ev('bump_r_top') + 6, s * 120, 40, 12, 70), clear))
    parts.append(('Front plate bracket', tbox(12, ev('bump_f_bot') - 25, 0, 10, 60, 300), blackp))
    commit(Bm, parts, 'Bumper parts')
    print('front', F.bRepBodies.count, 'rear', R.bRepBodies.count, 'bumpers', Bm.bRepBodies.count)
