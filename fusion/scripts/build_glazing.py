# Glass (component "Glazing"): windscreen, rear screen, front/rear door glass both sides.
# Windscreen and rear screen are curved (offset greenhouse lofts, _geom.screen_band); door glass is planar.
# Each pane follows the opening outline (shared with build_openings.py via _geom.py), grown by glass_overlap and
# set glass_inset behind the outer skin so it reads as glass seated in a rubber channel.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())
exec(open(os.path.join(ROOT, '_geom.py')).read(), globals())

PARAMS = [
    ('glass_t', '5 mm', 'Glass thickness (laminated windscreen ~5.5, side 4) (est.)'),
    ('glass_overlap', '12 mm', 'Glass edge overlap behind the opening (modelling choice)'),
    ('glass_inset', '7 mm', 'Glass plane inset behind the outer skin (photos, MED)'),
]

def run(_context: str):
    for n, e, c in PARAMS:
        param(n, e, 'mm', c, update=True)
    C = get_comp('Glazing')
    wipe(C)
    g = G()
    t, ov, ins = ev('glass_t'), ev('glass_overlap'), ev('glass_inset')
    glass = lib_app('Glass (Clear)')
    tint = color_app('Lada Glass (green tint)', 'Glass (Clear)', (200, 226, 214))
    # curved, wrap-around windscreen and rear screen: a band between two offset greenhouse lofts, cut to the outline
    for b in screen_band(C, g, -(ins + t), -ins, ov, None, 'Screen glass', ap=tint):
        b.name = 'Windscreen' if b.name.endswith('ws') else 'Rear screen'
    names = ('Front door glass', 'Rear door glass')
    for side, tag in ((1, ' R'), (-1, ' L')):
        for poly, name in zip(side_window_polys(g, grow=ov), names):
            plate3d(C, on_side(g, poly, -ins, side), t, name + tag, ap=tint)
    print('glass bodies:', C.bRepBodies.count)
