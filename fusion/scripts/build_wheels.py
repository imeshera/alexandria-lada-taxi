# Wheel assembly: component "Wheel" (tyre, steel rim, hubcap, nuts, brake disc/drum stub), four root occurrences.
# Local frame: wheel centre at origin, axis along Z, OUTER face towards +Z.
# Occurrences: right side (+Z) as-is; left side rotated 180 deg about Y.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())

def thick_line(mid, t):
    """Closed polygon of a polyline (z, r) thickened by t (mm) to both sides."""
    a, b = [], []
    n = len(mid)
    for i in range(n):
        p0 = mid[max(i - 1, 0)]; p1 = mid[min(i + 1, n - 1)]
        dz, dr = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dz, dr)
        nz, nr = -dr / L, dz / L
        a.append((mid[i][0] + nz * t / 2, mid[i][1] + nr * t / 2))
        b.append((mid[i][0] - nz * t / 2, mid[i][1] - nr * t / 2))
    return a + b[::-1]

def revolve(c, pts_zr, name, op=NEW, spline=False, participants=None):
    """pts as (z, r) mm; sketch on YZ plane (sketch x = -Z, sketch y = Y); revolve about Z."""
    sk = c.sketches.add(c.yZConstructionPlane)
    sk.name = name
    sk.isComputeDeferred = True
    pts = [(-z, r) for z, r in pts_zr]
    if spline:
        oc = adsk.core.ObjectCollection.create()
        for p in pts + [pts[0]]:
            oc.add(P(p[0], p[1]))
        s = sk.sketchCurves.sketchFittedSplines.add(oc)
        s.isClosed = True
    else:
        sk_poly(sk, pts)
    sk.isComputeDeferred = False
    pr = largest_profile(sk)
    ri = c.features.revolveFeatures.createInput(pr, c.zConstructionAxis, op)
    ri.setAngleExtent(False, VI(2 * math.pi))
    if participants is not None:
        ri.participantBodies = participants
    f = c.features.revolveFeatures.add(ri)
    f.name = name
    if op == NEW:
        for b in f.bodies:
            b.name = name
    sk.isVisible = False
    return f

def run(_context: str):
    for n, e, u, cmt in [
        ('tyre_w', '175 mm', 'mm', 'Tyre section width, 175/70 R13 (factory, HIGH)'),
        ('tyre_ar', '0.70', '', 'Tyre aspect ratio 70 (factory 175/70 R13, HIGH)'),
        ('rim_d', '13 in', 'mm', 'Rim diameter 13 in (HIGH)'),
        ('rim_w', '5 in', 'mm', 'Rim width 5J (HIGH)'),
        ('rim_et', '29 mm', 'mm', 'Rim offset ET29 (VAZ 2101-2107 steel wheel, MED)'),
        ('bolt_pcd', '98 mm', 'mm', 'Bolt circle 4 x 98 (HIGH)'),
    ]:
        param(n, e, u, cmt, update=True)
    W = get_comp('Wheel')
    wipe(W)
    tw, ar = ev('tyre_w'), evu('tyre_ar')
    rb = ev('rim_d') / 2              # bead seat radius
    rw = ev('rim_w') / 2              # half rim width (flange to flange inside)
    et = ev('rim_et')
    R = rb + tw * ar                  # tyre outer radius (575 mm diameter)
    sw = tw * ar

    # ---- tyre: closed spline section (z, r)
    h = tw / 2
    sec = [(rw + 2, rb + 2), (h - 2, rb + 0.35 * sw), (h, rb + 0.55 * sw), (h - 5, rb + 0.85 * sw),
           (h - 16, R - 3), (h - 30, R), (0, R + 1.5), (-(h - 30), R), (-(h - 16), R - 3), (-(h - 5), rb + 0.85 * sw),
           (-h, rb + 0.55 * sw), (-(h - 2), rb + 0.35 * sw), (-(rw + 2), rb + 2), (0, rb - 3)]
    tyre = revolve(W, sec, 'Tyre', spline=True)
    # circumferential tread grooves
    tb = list(tyre.bodies)
    for zc in (-38, 0, 38):
        g = [(zc - 4, R - 8), (zc + 4, R - 8), (zc + 4, R + 10), (zc - 4, R + 10)]
        revolve(W, g, 'Tread groove', op=CUT, participants=tb)
    # lateral tread slots: one cut, circular pattern
    sk = W.sketches.add(W.xYConstructionPlane); sk.name = 'Tread slot'
    sk_poly(sk, [(-5, R - 7), (5, R - 7), (5, R + 10), (-5, R + 10)])
    pr = largest_profile(sk)
    ei = W.features.extrudeFeatures.createInput(pr, CUT)
    ei.setSymmetricExtent(VI((h + 2) / 10), False)
    ei.participantBodies = tb
    slot = W.features.extrudeFeatures.add(ei); slot.name = 'Tread slot'
    oc = adsk.core.ObjectCollection.create(); oc.add(slot)
    ci = W.features.circularPatternFeatures.createInput(oc, W.zConstructionAxis)
    ci.quantity = VI(64); ci.totalAngle = adsk.core.ValueInput.createByString('360 deg'); ci.isSymmetric = False
    cp = W.features.circularPatternFeatures.add(ci); cp.name = 'Tread pattern'
    sk.isVisible = False

    # ---- rim: thickened mid-line (z, r): outer flange curl -> bead seat -> drop well -> bead seat -> inner flange
    t = 3.5
    mid = [(rw + 8, rb + 18), (rw + 4, rb + 16), (rw, rb + 6), (rw - 2, rb), (rw - 20, rb), (rw - 28, rb - 14),
           (-10, rb - 16), (-rw + 30, rb - 16), (-rw + 22, rb), (-rw + 2, rb), (-rw, rb + 6), (-rw - 4, rb + 16),
           (-rw - 8, rb + 18)]
    revolve(W, thick_line(mid, t), 'Rim')
    # wheel disc: from the drop well out to the mounting face at ET, with a raised ring
    dmid = [(-6, rb - 16), (8, rb - 30), (et + 6, 132), (et + 6, 92), (et + 6, 74), (et, 66), (et, 31)]
    disc = revolve(W, thick_line(dmid, 4.0), 'Wheel disc')
    # VAZ classic steel wheel: a ring of 16 small round holes in the disc (CC0 side photo, Moscow 2025)
    sk = W.sketches.add(W.xYConstructionPlane); sk.name = 'Disc vents'
    for k in range(16):
        a = math.radians(11.25 + 22.5 * k)
        cx, cy = 112 * math.cos(a), 112 * math.sin(a)
        sk.sketchCurves.sketchCircles.addByCenterRadius(P(cx, cy), 0.9)
    ei = W.features.extrudeFeatures.createInput(profiles(sk), CUT)
    ei.setSymmetricExtent(VI(10), True)
    ei.participantBodies = list(disc.bodies)
    f = W.features.extrudeFeatures.add(ei); f.name = 'Disc vents'
    sk.isVisible = False

    # ---- nuts, hubcap, hub, brake disc (front) / drum look-alike
    chrome = lib_app('Chrome')
    parts = []
    pc = ev('bolt_pcd') / 2
    for k in range(4):
        a = math.radians(45 + 90 * k)
        x, y = pc * math.cos(a), pc * math.sin(a)
        nut = tcyl((x, y, et + 2), (x, y, et + 16), 9.5)
        tunion(nut, tcyl((x, y, et + 16), (x, y, et + 21), 9.5, 5))
        parts.append(('Wheel nut', nut, chrome))
    cap = tcyl((0, 0, et + 4), (0, 0, et + 18), 34)
    tunion(cap, tcyl((0, 0, et + 18), (0, 0, et + 26), 34, 22))
    parts.append(('Hubcap', cap, chrome))
    parts.append(('Hub', tcyl((0, 0, et - 40), (0, 0, et), 50), None))
    parts.append(('Brake disc', tcyl((0, 0, et - 58), (0, 0, et - 46), 126), None))
    commit(W, parts, 'Wheel hardware')

    # ---- appearances
    rubber = color_app('Tyre Rubber', 'Rubber - Soft', (34, 34, 34))
    wheelp = color_app('Lada Wheel Silver (weathered)', 'Paint - Enamel Glossy (Grey)', (150, 150, 146))
    iron = lib_app('Steel - Rough')
    for b in W.bRepBodies:
        n = base_name(b.name)
        if n == 'Tyre': b.appearance = rubber
        elif n in ('Rim', 'Wheel disc'): b.appearance = wheelp
        elif n in ('Hub', 'Brake disc'): b.appearance = iron
    place_wheels()

def place_wheels():
    for n, e, cmt in [('wheelbase', '2424 mm', 'Wheelbase (factory, HIGH)'),
                      ('track_f', '1365 mm', 'Front track (factory, HIGH)'),
                      ('track_r', '1321 mm', 'Rear track (factory, HIGH)'),
                      ('axle_f_x', '615 mm', 'Front axle x from front bumper face (side photo, MED)'),
                      ('wheel_cy', '288 mm', 'Wheel centre height above ground (tyre static radius, MED)')]:
        param(n, e, 'mm', cmt)   # owned by build_params.py
    # Moving occurrences + snapshot does not persist in this design (positions revert on compute), so the
    # master occurrence (which owns the timeline features) stays hidden at the origin and the four visible
    # wheels are (re)created with their transform: addExistingComponent(comp, matrix) persists.
    W = get_comp('Wheel')
    occs = [o for o in root.occurrences if o.component.name == 'Wheel']
    master = occs[0]
    for o in occs[1:]:
        o.deleteMe()
    master.isLightBulbOn = False
    tl = design.timeline
    for i in range(tl.count - 1, -1, -1):
        if tl.item(i).name.startswith('Position'):
            tl.item(i).deleteMe()
    xf, xr = ev('axle_f_x'), ev('axle_f_x') + ev('wheelbase')
    cy = ev('wheel_cy')
    spots = [(xf, ev('track_f') / 2, False), (xf, -ev('track_f') / 2, True),
             (xr, ev('track_r') / 2, False), (xr, -ev('track_r') / 2, True)]
    for x, z, flip in spots:
        m = adsk.core.Matrix3D.create()
        if flip:
            m.setToRotation(math.pi, V3(0, 1, 0), P(0, 0, 0))
        m.translation = V3(x / 10, cy / 10, z / 10)
        o = root.occurrences.addExistingComponent(W, m)
        o.isLightBulbOn = True
    print('wheels placed')
