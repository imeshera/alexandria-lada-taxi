# Egyptian 2008-format taxi plates (component "Plate"), front + rear occurrences.
# 350 x 170 mm embossed aluminium: orange top band "EGYPT" (left) / "مصر" (right); white field with
# Eastern Arabic digits on the LEFT and letters on the RIGHT, split by a thin divider. Plate "٨٣٤ س ل م".
# Local frame: plate face in the YZ plane, readable from -X (the front); body behind it (+X).
# On the YZ plane sketch +x = -Z = the viewer's LEFT seen from -X, hence the mirrored (_L) SVGs.
# Rear occurrence = rotated 180 deg about Y (a rotation, so the text still reads correctly).
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())

def run(_context: str):
    for n, e, cmt in [
        ('plate_w', '350 mm', 'Egyptian plate width (Wikipedia, HIGH)'),
        ('plate_h', '170 mm', 'Egyptian plate height (Wikipedia, HIGH)'),
        ('plate_band_h', '57 mm', 'Orange top band height ~1/3 (photos, MED)'),
        ('plate_t', '1.2 mm', 'Plate thickness (est.)'),
        ('plate_f_x', '-6 mm', 'Front plate face x (on the bumper, MED)'),
        ('plate_f_y', '390 mm', 'Front plate centre (hangs from the bumper bar, photos, MED)'),
        ('plate_r_x', '4104 mm', 'Rear plate face x (tail panel, MED)'),
        ('plate_r_y', '595 mm', 'Rear plate centre height (tail panel above the bumper, MED)'),
    ]:
        param(n, e, 'mm', cmt, update=True)
    C = get_comp('Plate')
    wipe(C)
    w, h, bh, t = ev('plate_w'), ev('plate_h'), ev('plate_band_h'), ev('plate_t')
    white = color_app('Plate White', 'Paint - Enamel Glossy (White)', (236, 236, 228))
    orange = color_app('Plate Taxi Orange (faded)', 'Paint - Enamel Glossy (Red)', (238, 120, 48))
    ink = color_app('Plate Black', 'Paint - Enamel Glossy (Black)', (20, 20, 20))
    parts = [
        ('Plate base', tbox(t / 2, 0, 0, t, h, w), white),
        ('Plate band', tbox(-0.15, h / 2 - bh / 2, 0, 0.3, bh - 6, w - 6), orange),
        ('Plate divider', tbox(-0.3, -bh / 2 + 4, 0, 0.6, h - bh - 18, 2.5), ink),
    ]
    # raised border rim (4 strips)
    for (cy, cz, ly, lz) in [(h / 2 - 2.5, 0, 3, w - 2), (-h / 2 + 2.5, 0, 3, w - 2), (0, w / 2 - 2.5, h - 2, 3), (0, -w / 2 + 2.5, h - 2, 3)]:
        parts.append(('Plate rim', tbox(-0.3, cy, cz, 0.6, ly, lz), ink))
    # band/field separator line
    parts.append(('Plate rim', tbox(-0.3, h / 2 - bh, 0, 0.6, 2, w - 6), ink))
    # mounting screws in the band
    chrome = lib_app('Chrome')
    for z in (-w / 2 + 40, w / 2 - 40):
        parts.append(('Plate screw', tcyl((-0.4, h / 2 - bh / 2, z), (-2.2, h / 2 - bh / 2, z), 4.5, 3.5), chrome))
    commit(C, parts, 'Plate blank')

    pl = offset_plane(C, C.yZConstructionPlane, -0.3, 'Plate face')
    d = -0.5    # decal height (embossed characters)
    yb = h / 2 - bh                                  # band bottom
    place_svg(C, pl, 'plate_egypt_L.svg', 82, yb + 18, 22, d, 'Plate text EGYPT', ink)
    place_svg(C, pl, 'plate_misr_L.svg', -95, yb + 13, 32, d, 'Plate text Misr', ink)
    place_svg(C, pl, 'plate_dig_L.svg', 88, -h / 2 + 22, 62, d, 'Plate digits', ink)
    place_svg(C, pl, 'plate_let_L.svg', -86, -h / 2 + 18, 70, d, 'Plate letters', ink)
    place_plates()

def place_plates():
    C = get_comp('Plate')
    occs = [o for o in root.occurrences if o.component.name == 'Plate']
    for o in occs[1:]:
        o.deleteMe()
    occs[0].isLightBulbOn = False
    for x, y, flip in [(ev('plate_f_x'), ev('plate_f_y'), False), (ev('plate_r_x'), ev('plate_r_y'), True)]:
        m = adsk.core.Matrix3D.create()
        if flip:
            m.setToRotation(math.pi, V3(0, 1, 0), P(0, 0, 0))
        m.translation = V3(x / 10, y / 10, 0)
        o = root.occurrences.addExistingComponent(C, m)
        o.isLightBulbOn = True
    print('plates placed')
