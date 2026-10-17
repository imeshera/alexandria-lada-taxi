# Openings and shut lines in the Body shell (component "Body"), after build_body.py.
#  - Side glass openings (front door, rear door) cut through both sides.
#  - Windscreen / rear screen openings cut along X from front-view outlines.
#  - Doors, bonnet and boot lid are separated from the shell by through-slits (gap_w) along their shut lines,
#    so each panel becomes its own body (named here) - handy for the two-tone livery and for print parts.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())
exec(open(os.path.join(ROOT, '_geom.py')).read(), globals())

PARAMS = [
    ('door_f_x0', '1184 mm', 'Front door leading edge x (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('door_r_x1', '3001 mm', 'Rear door trailing edge x (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('door_bot_h', '370 mm', 'Door bottom edge height (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('door_notch_r', '390 mm', 'Rear door rear-lower notch radius round the rear arch (photos, MED)'),
    ('rdw_x1', '2934 mm', 'Rear door glass trailing edge x at the belt (factory drawing, MED)'),
    ('rdw_top_x', '2735 mm', 'Rear door glass trailing edge x at the top - sloped, follows the C-pillar (factory drawing, MED)'),
    ('rdw_div_x', '2712 mm', 'Rear door fixed quarter-light divider x (factory drawing, MED)'),
    ('rdw_r', '120 mm', 'Rear door glass upper-rear corner radius (photos, MED)'),
    ('win_r', '35 mm', 'Side glass corner radius (photos, MED)'),
    ('ws_pillar_w', '75 mm', 'Front-view A-pillar width (windscreen inset) (photos, MED)'),
    ('ws_r', '70 mm', 'Windscreen opening corner radius (photos, MED)'),
    ('boot_hw', '650 mm', 'Boot lid half width at the shut line (top view, MED)'),
]

def ring_xy(sk, outer, inner):
    """Two closed polylines -> the slit region is the profile with 2 loops."""
    sk_poly(sk, outer)
    sk_poly(sk, inner)

def offset_poly(pts, d):
    """Offset a closed CCW/CW polygon outward by d (mm) using vertex normals (adequate for convex-ish shapes)."""
    n = len(pts)
    # signed area -> orientation
    a = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    s = 1 if a > 0 else -1
    out = []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        def nrm(a, b):
            dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy)
            return (s * dy / L, -s * dx / L)
        n1, n2 = nrm(p0, p1), nrm(p1, p2)
        bx, by = n1[0] + n2[0], n1[1] + n2[1]
        L = math.hypot(bx, by)
        cosh = (n1[0] * n2[0] + n1[1] * n2[1] + 1) / 2
        k = d / max(math.sqrt(max(cosh, 1e-6)), 0.3)
        out.append((p1[0] + bx / L * k, p1[1] + by / L * k))
    return out

def arc_pts(cx, cy, r, a0, a1, n=10):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

def slit(B, sk, name, extent=None):
    """Cut the 2-loop profiles of sketch sk (through all, symmetric about the sketch plane, or extent=(d0,d1))."""
    profs = profiles(sk, lambda pr: pr.profileLoops.count >= 2)
    if extent:
        f = extrude(B, profs, extent[0], extent[1], CUT, name=name)
    else:
        ei = B.features.extrudeFeatures.createInput(profs, CUT)
        ei.setSymmetricExtent(VI(120), False)
        ei.participantBodies = list(B.bRepBodies)
        f = B.features.extrudeFeatures.add(ei); f.name = name
    sk.isVisible = False
    return f

def run(_context: str):
    for n, e, c in PARAMS:
        param(n, e, 'mm', c, update=True)
    B = get_comp('Body')
    # remove a previous openings pass (features after the shell)
    names = ('Side glass', 'Windscreen opening', 'Rear screen opening', 'Door slits', 'Bonnet slit', 'Boot slit')
    for coll in (B.features.extrudeFeatures,):
        for i in range(coll.count - 1, -1, -1):
            if coll.item(i).name.startswith(names):
                coll.item(i).deleteMe()
    for i in range(B.sketches.count - 1, -1, -1):
        if B.sketches.item(i).name.startswith(names):
            B.sketches.item(i).deleteMe()

    hw = ev('width_body') / 2
    rh, crown, belt, cw, deck = ev('roof_h'), ev('roof_crown'), ev('belt_h'), ev('cowl_h'), ev('deck_h')
    wsx, wtx, rtx, rsx = ev('ws_base_x'), ev('ws_top_x'), ev('rs_top_x'), ev('rs_base_x')
    bx, pw = ev('b_pillar_x'), ev('pillar_w')
    gap = ev('gap_w')
    top = rh - crown - ev('drip_h') - ev('roof_edge_r') * 0.6     # side glass top
    # A-line (rear edge of the A pillar in side view): windscreen line shifted back by pillar_w
    def a_x(y):
        return wsx + (wtx - wsx) * (y - cw) / (rh - 6 - cw) + pw
    def c_x(y):   # rear-screen line in side view
        return rsx + (rtx - rsx) * (y - deck) / (rh - 6 - deck)

    # ---- side glass openings
    g = G()
    sk = B.sketches.add(B.xYConstructionPlane); sk.name = 'Side glass'
    sk.isComputeDeferred = True
    for poly in side_window_polys(g):
        sk_poly(sk, poly)
    sk.isComputeDeferred = False
    ei = B.features.extrudeFeatures.createInput(profiles(sk), CUT)
    ei.setSymmetricExtent(VI(hw / 10 + 5), False)
    ei.participantBodies = list(B.bRepBodies)
    B.features.extrudeFeatures.add(ei).name = 'Side glass'
    sk.isVisible = False

    # ---- windscreen + rear screen (front-view outlines on the YZ plane, sketch x = -Z)
    for name, kind, x0, x1 in (('Windscreen opening', 'ws', wsx - 60, ev('ws_top_k_x') + 25),
                               ('Rear screen opening', 'rs', ev('rs_top_k_x') - 25, rsx + 60)):
        sk = B.sketches.add(B.yZConstructionPlane); sk.name = name
        sk_poly(sk, [(-z, y) for z, y in screen_poly(g, kind, g['ws_pillar_w'])])
        extrude(B, profiles(sk), x0, x1, CUT, name=name)
        sk.isVisible = False

    # ---- door shut lines (through-slits)
    sk = B.sketches.add(B.xYConstructionPlane); sk.name = 'Door slits'
    xf0, xr1, yb = ev('door_f_x0'), ev('door_r_x1'), ev('door_bot_h')
    yt = belt - 5
    xr_ax, cy = ev('axle_f_x') + ev('wheelbase'), ev('wheel_cy')
    nr = ev('door_notch_r')
    front = [(xf0, yb + 40), (xf0 + 40, yb), (bx - gap, yb), (bx - gap, yt), (xf0, yt)]
    # rear door: lower trailing corner notched round the rear wheel arch (circle nr about the rear axle)
    t0 = 180 - math.degrees(math.asin(max(-1.0, min(1.0, (yb - cy) / nr))))
    t1 = math.degrees(math.acos(max(-1.0, min(1.0, (xr1 - xr_ax) / nr))))
    rear_clean = [(bx + gap, yb)] + arc_pts(xr_ax, cy, nr, t0, t1, 12) + [(xr1, yt), (bx + gap, yt)]
    for poly in (front, rear_clean):
        sk_poly(sk, offset_poly(poly, gap / 2))
        sk_poly(sk, offset_poly(poly, -gap / 2))
    slit(B, sk, 'Door slits')

    # ---- bonnet + boot lid shut lines (top view on XZ, cut vertically over a limited Y band)
    fx, rx = ev('body_front_x'), ev('body_rear_x')
    for name, x0, x1, h, ylo, yhi in (('Bonnet slit', fx + 12, wsx - 75, ev('bonnet_hw'), ev('bonnet_front_h') - 120, cw + 20),
                                      ('Boot slit', rsx + 45, rx - 10, ev('boot_hw'), ev('rear_top_h') - 120, deck + 20)):
        sk = B.sketches.add(B.xZConstructionPlane); sk.name = name
        poly = [(x0, -h), (x1, -h), (x1, h), (x0, h)]
        sk_poly(sk, offset_poly(poly, gap / 2))
        sk_poly(sk, offset_poly(poly, -gap / 2))
        slit(B, sk, name, (ylo, yhi))

    # ---- name the separated panels
    for b in B.bRepBodies:
        bb = b.boundingBox
        cx, cy_, cz = [(bb.minPoint.asArray()[i] + bb.maxPoint.asArray()[i]) * 5 for i in range(3)]
        sx = (bb.maxPoint.x - bb.minPoint.x) * 10
        if sx > 3500:
            b.name = 'Body shell'
        elif cy_ > 700 and cx < wsx:
            b.name = 'Bonnet'
        elif cy_ > 700 and cx > rsx:
            b.name = 'Boot lid'
        else:
            both = bb.minPoint.z < 0 < bb.maxPoint.z
            b.name = ('Front door' if cx < bx else 'Rear door') + ('s' if both else (' R' if cz > 0 else ' L'))
    print('bodies:', [b.name for b in B.bRepBodies])
