# Door lettering (component "Lettering"): the plate number repeated in small black Arabic on both front doors,
# just behind and above the door handle - the usual Alexandria practice (livery-and-plates.md). CoreText SVG
# outlines; the -Z side uses the mirrored (_L) SVG because its sketch +x is the viewer's left.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())
exec(open(os.path.join(ROOT, '_geom.py')).read(), globals())

PARAMS = [
    ('door_txt_x', '1720 mm', 'Door lettering centre x on the front doors (photos 2006/2011, MED)'),
    ('door_txt_h', '42 mm', 'Door lettering ink height (photos: 3-5 cm, MED)'),
]

def run(_context: str):
    for n, e, c in PARAMS:
        param(n, e, 'mm', c, update=True)
    C = get_comp('Lettering')
    wipe(C)
    g = G()
    ink = color_app('Sign Black', 'Paint - Enamel Glossy (Black)', (18, 18, 18))
    x, h = ev('door_txt_x'), ev('door_txt_h')
    yb = ev('handle_y') + 30
    zs = side_hw(g, yb + h / 2)
    for s, svg in ((1, 'door_plate_R.svg'), (-1, 'door_plate_L.svg')):
        pl = offset_plane(C, C.xYConstructionPlane, s * (zs - 0.4), 'Door text plane %+d' % s)
        place_svg(C, pl, svg, x, yb, h, s * 1.8, 'Door text', ink)
    print('lettering bodies:', C.bRepBodies.count)
