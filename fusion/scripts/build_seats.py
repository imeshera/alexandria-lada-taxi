# Seats. "Front seat" component (cushion, reclined backrest, headrest on two posts, side panels, ribbed centre
# panels, recliner knob, runners) built centred on z = 0 and instanced at +/- seat_f_z (hidden master + instances
# created with their matrix, see BUILD-LOG). "Rear bench": cushion + backrest + centre armrest recess, between the
# wheelhouses. All soft parts are filleted after creation.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())

PARAMS = [
    ('seat_f_x', '2040 mm', 'Front seat cushion centre x (2107 interior photos + H-point est., LOW)'),
    ('seat_f_z', '365 mm', 'Front seat centreline |z| (2107 interior photos, MED)'),
    ('seat_f_y', '560 mm', 'Front seat cushion top height (H-point est., LOW)'),
    ('seat_f_w', '500 mm', 'Front seat width (2107 interior photos, MED)'),
    ('seat_back_deg', '14 deg', 'Front backrest recline from vertical (est.)'),
    ('bench_x', '2800 mm', 'Rear bench cushion centre x (est. from photos, LOW)'),
    ('bench_y', '545 mm', 'Rear bench cushion top height (est., LOW)'),
    ('bench_hw', '560 mm', 'Rear bench cushion half width between the wheelhouses (est.)'),
]

def soft_fillet(c, bodies, r):
    oc = adsk.core.ObjectCollection.create()
    for b in bodies:
        for e in b.edges:
            oc.add(e)
    fi = c.features.filletFeatures.createInput()
    fi.addConstantRadiusEdgeSet(oc, VI(r / 10), True)
    try:
        c.features.filletFeatures.add(fi)
    except Exception as ex:
        print('fillet failed', ex)

def rot_about_z(body, deg, pivot):
    tbm.transform(body, mat_rot((0, 0, 1), deg, pivot))
    return body

def run(_context: str):
    for n, e, c in PARAMS:
        param(n, e, 'deg' if n.endswith('_deg') else 'mm', c, update=True)
    fabric = color_app('Seat Cloth Bolster (charcoal, worn)', 'Fabric (Grey)', (56, 56, 60))
    insert = color_app('Seat Cloth Insert (grey)', 'Fabric (Grey)', (104, 104, 108))
    stripe_a = color_app('Seat Cloth Stripe (light grey)', 'Fabric (Grey)', (146, 144, 138))
    stripe_b = color_app('Seat Cloth Stripe (blue-grey)', 'Fabric (Grey)', (72, 82, 104))
    vinyl = color_app('Seat Vinyl (black, worn)', 'Leather - Weathered', (32, 30, 29))
    steel = color_app('Chassis Black (dusty)', 'Paint - Enamel Glossy (Black)', (46, 45, 42))
    chrome = lib_app('Chrome')
    sx, sy, sw = ev('seat_f_x'), ev('seat_f_y'), ev('seat_f_w')
    back = evdeg('seat_back_deg')
    floor = ev('sill_h') + 3

    # ================= front seat (local z centred, absolute x/y)
    S = get_comp('Front seat')
    wipe(S)
    cl, ch = 480, 120                          # cushion length / thickness
    cush = tbox(sx, sy - ch / 2, 0, cl, ch, sw)
    rot_about_z(cush, 6, (sx, sy, 0))          # front edge raised a little
    bx0 = sx + cl / 2 - 20                     # backrest pivot
    # 2107 'anatomic' seat: one tall backrest with an integrated headrest and an opening below it
    bl, bt = 600, 125
    br = tbox(bx0 + bt / 2, sy + bl / 2 - 10, 0, bt, bl, sw - 10)
    hr = tbox(bx0 + bt / 2 + 5, sy + bl + 95, 0, bt - 25, 230, 290)
    tunion(br, hr)
    tsub(br, tbox(bx0 + bt / 2, sy + bl + 20, 0, bt + 20, 70, 170))       # opening between backrest and headrest
    rot_about_z(br, -back, (bx0, sy, 0))
    soft = [('Seat cushion', cush, fabric), ('Seat backrest', br, fabric)]
    bodies = commit(S, soft, 'Seat soft parts')
    soft_fillet(S, [b for b in S.bRepBodies if b.name == 'Seat cushion'], 40)
    soft_fillet(S, [b for b in S.bRepBodies if b.name == 'Seat backrest'], 14)
    parts = []
    # headrest posts, ribbed centre panels (cushion + backrest), side bolster piping, recliner knob, frame + runners
    ins = tbox(sx + 10, sy - 2, 0, cl - 110, 8, sw - 150)
    rot_about_z(ins, 6, (sx, sy, 0))
    parts.append(('Seat insert', ins, insert))
    ins = tbox(bx0 - 2, sy + bl / 2 + 10, 0, 8, bl - 120, sw - 160)
    rot_about_z(ins, -back, (bx0, sy, 0))
    parts.append(('Seat insert', ins, insert))
    for k in range(6):
        x = sx - cl / 2 + 90 + k * 55
        rib = tbox(x, sy + 4, 0, 26, 12, sw - 160)
        rot_about_z(rib, 6, (sx, sy, 0))
        parts.append(('Seat stripe', rib, stripe_a if k % 2 == 0 else stripe_b))
    for k in range(7):
        y = sy + 90 + k * 60
        rib = tbox(bx0 - 7, y, 0, 12, 28, sw - 170)
        rot_about_z(rib, -back, (bx0, sy, 0))
        parts.append(('Seat stripe', rib, stripe_a if k % 2 == 0 else stripe_b))
    parts.append(('Recliner knob', tcyl((bx0, sy - 20, sw / 2), (bx0, sy - 20, sw / 2 + 25), 28), vinyl))
    parts.append(('Seat frame', tbox(sx, (floor + sy - ch) / 2 + 10, 0, cl - 60, sy - ch - floor - 20, sw - 80), steel))
    for z in (-sw / 2 + 60, sw / 2 - 60):
        parts.append(('Seat runner', tbox(sx - 20, floor + 15, z, cl + 120, 30, 40), steel))
    parts.append(('Seat adjuster bar', tcyl((sx - cl / 2 - 10, floor + 60, -sw / 2 + 60), (sx - cl / 2 - 10, floor + 60, sw / 2 - 60), 7), chrome))
    commit(S, parts, 'Seat hardware')
    # instances
    occs = [o for o in root.occurrences if o.component.name == 'Front seat']
    for o in occs[1:]:
        o.deleteMe()
    occs[0].isLightBulbOn = False
    for s in (1, -1):
        m = adsk.core.Matrix3D.create(); m.translation = V3(0, 0, s * ev('seat_f_z') / 10)
        o = root.occurrences.addExistingComponent(S, m); o.isLightBulbOn = True

    # ================= rear bench
    R = get_comp('Rear bench')
    wipe(R)
    bx, by, bhw = ev('bench_x'), ev('bench_y'), ev('bench_hw')
    cl2 = 470
    cush = tbox(bx, by - 70, 0, cl2, 140, 2 * bhw)
    rot_about_z(cush, 5, (bx, by, 0))
    px = bx + cl2 / 2 - 10
    rb = tbox(px + 65, by + 270, 0, 130, 560, 2 * bhw + 120)
    rot_about_z(rb, -20, (px, by, 0))
    commit(R, [('Bench cushion', cush, fabric), ('Bench backrest', rb, fabric)], 'Bench soft parts')
    soft_fillet(R, list(R.bRepBodies), 45)
    parts = []
    for zc in (-bhw * 0.62, 0, bhw * 0.62):            # three seating positions, each with its own insert
        ins = tbox(bx + 10, by - 2, zc, cl2 - 110, 8, 2 * bhw * 0.28)
        rot_about_z(ins, 5, (bx, by, 0)); parts.append(('Seat insert', ins, insert))
        ins = tbox(px - 4, by + 280, zc, 8, 440, 2 * bhw * 0.28)
        rot_about_z(ins, -20, (px, by, 0)); parts.append(('Seat insert', ins, insert))
        for k in range(6):
            rib = tbox(bx - cl2 / 2 + 90 + k * 55, by + 3, zc, 26, 12, 2 * bhw * 0.26)
            rot_about_z(rib, 5, (bx, by, 0))
            parts.append(('Seat stripe', rib, stripe_a if k % 2 == 0 else stripe_b))
        for k in range(7):
            rib = tbox(px - 9, by + 90 + k * 60, zc, 12, 28, 2 * bhw * 0.26)
            rot_about_z(rib, -20, (px, by, 0))
            parts.append(('Seat stripe', rib, stripe_a if k % 2 == 0 else stripe_b))
    parts.append(('Bench base', tbox(bx + 20, (floor + by - 140) / 2, 0, cl2 - 40, by - 140 - floor, 2 * bhw - 40), steel))
    commit(R, parts, 'Bench hardware')
    print('seats ok')
