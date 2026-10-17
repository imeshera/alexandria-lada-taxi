# Body shell of the VAZ-2107, component "Body" (v2 surfacing).
#  1. Lower body = side profile (XY) extruded across ∩ plan (XZ) ∩ flank section (YZ) with the crisp upper swage line,
#     the lower crease and the set-back shoulder; wing tops stepped below the bonnet edge; raised bonnet centre;
#     sheet-metal edge radii on the wing/boot tops and the front/rear top edges.
#  2. Greenhouse = loft between two plan sections (curved wrap-around windscreen and rear screen, tumblehome),
#     trimmed by the roof crown (see _geom.gh_loft).
#  3. Join, wheel-arch cut-outs, roof + pillar fillets, hollow shell (skin_t), rolled wheel-arch lips.
# Openings, glass and shut lines are in build_openings.py.
# Sketch planes: XY -> (X, Y); XZ -> (X, -Z), normal +Y; YZ -> (-Z, Y), normal +X.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())
exec(open(os.path.join(ROOT, '_geom.py')).read(), globals())

def bonnet_y(x):
    """Bonnet top line (side profile) between its front edge and the scuttle."""
    fx, bf, cw, wsx = ev('body_front_x'), ev('bonnet_front_h'), ev('cowl_h'), ev('ws_base_x')
    return bf + (cw - 6 - bf) * (x - (fx + 45)) / (wsx - 60 - (fx + 45))

def side_lower():
    fx, bx = ev('body_front_x'), ev('body_rear_x')
    xf, xr = ev('axle_f_x'), ev('axle_f_x') + ev('wheelbase')
    bf, cw, belt, deck, rt = ev('bonnet_front_h'), ev('cowl_h'), ev('belt_h'), ev('deck_h'), ev('rear_top_h')
    sill, fb, rb = ev('sill_h'), ev('front_bot_h'), ev('rear_bot_h')
    wsx, rsx = ev('ws_base_x'), ev('rs_base_x')
    # boot lid: slight convex crown in side view (front edge -> rear edge)
    bx0, by0, bx1, by1 = rsx + 60, deck, bx - 40, rt + 4
    boot = [(bx0 + (bx1 - bx0) * t, by0 + (by1 - by0) * t + 22 * math.sin(math.pi * t)) for t in (0.25, 0.5, 0.75)]
    return ([(fx + 40, fb), (fx + 5, fb + 60), (fx, bf - 40), (fx + 12, bf - 8), (fx + 45, bf),      # front panel
             (wsx - 60, cw - 6), (wsx + 40, belt),                                                   # bonnet -> scuttle
             (rsx - 40, belt), (bx0, by0)] + boot +                                                  # belt -> boot lid
            [(bx1, by1), (bx - 8, rt - 10), (bx, rt - 60), (bx - 2, rb + 60), (bx - 30, rb),         # rear panel
             (xr + 520, rb), (xr + 440, sill), (xf - 380, sill), (xf - 470, fb)])                    # underside

def edges_where(body, pred):
    oc = adsk.core.ObjectCollection.create()
    for e in body.edges:
        bb = e.boundingBox
        mn, mx = bb.minPoint, bb.maxPoint
        if pred([v * 10 for v in (mn.x, mn.y, mn.z)], [v * 10 for v in (mx.x, mx.y, mx.z)], e):
            oc.add(e)
    return oc

def fillet(B, body, pred, r, name):
    oc = edges_where(body, pred)
    if oc.count == 0:
        print('fillet', name, ': no edges'); return
    fi = B.features.filletFeatures.createInput()
    fi.addConstantRadiusEdgeSet(oc, VI(r / 10), True)
    try:
        f = B.features.filletFeatures.add(fi); f.name = name
        print('fillet', name, oc.count, 'edges ok')
    except Exception as ex:
        print('fillet', name, 'FAILED', str(ex)[:80])

def shell_body(B):
    return [b for b in B.bRepBodies if b.name == 'Body shell'][0]

def run(_context: str):
    B = get_comp('Body')
    wipe(B)
    g = G()
    hw, L, rh = g['hw'], g['L'], g['roof_h']
    fx, bx = ev('body_front_x'), ev('body_rear_x')

    # ---- 1. lower body
    sk = B.sketches.add(B.xYConstructionPlane); sk.name = 'Side profile lower'
    sk.isComputeDeferred = True
    sk_poly(sk, side_lower())
    sk.isComputeDeferred = False
    ei = B.features.extrudeFeatures.createInput(largest_profile(sk), NEW)
    ei.setSymmetricExtent(VI((hw + 20) / 10), False)
    f = B.features.extrudeFeatures.add(ei); f.name = 'Lower body'
    f.bodies.item(0).name = 'Body shell'
    sk.isVisible = False

    sk = B.sketches.add(B.xZConstructionPlane); sk.name = 'Plan'
    rf, rr = ev('plan_r_f'), ev('plan_r_r')
    Ls, A = sk.sketchCurves.sketchLines, sk.sketchCurves.sketchArcs
    c = [P(fx, -hw), P(bx, -hw), P(bx, hw), P(fx, hw)]
    ls = [Ls.addByTwoPoints(c[i], c[(i + 1) % 4]) for i in range(4)]
    for i, r in zip(range(4), (rr, rr, rf, rf)):
        a, b = ls[i], ls[(i + 1) % 4]
        A.addFillet(a, a.endSketchPoint.geometry, b, b.startSketchPoint.geometry, r / 10)
    extrude(B, largest_profile(sk), -50, rh + 100, INTERSECT, participants=[shell_body(B)], name='Plan trim')
    sk.isVisible = False

    sk = B.sketches.add(B.yZConstructionPlane); sk.name = 'Section lower (swage lines)'
    half = side_section(g)
    sk_poly(sk, [(-z, y) for z, y in half] + [(z, y) for z, y in half[::-1]])
    extrude(B, largest_profile(sk), -100, L + 100, INTERSECT, participants=[shell_body(B)], name='Section trim')
    sk.isVisible = False

    # wing tops stepped below the bonnet edge (cut a bonnet_step band off the wings, outboard of the bonnet)
    st, bhw_ = ev('bonnet_step'), ev('bonnet_hw')
    x0, x1 = fx + 30, ev('ws_base_k_x') + 40
    xs = [x0 + (x1 - x0) * k / 12 for k in range(13)]
    yb = lambda x: bonnet_y(min(x, ev('ws_base_x') - 60)) if x < ev('ws_base_x') - 60 else ev('cowl_h') - 6
    band = [(x, yb(x) - st) for x in xs] + [(x, yb(x) + 80) for x in xs[::-1]]
    sk = B.sketches.add(B.xYConstructionPlane); sk.name = 'Wing step'
    sk_poly(sk, band)
    for s in (1, -1):
        extrude(B, largest_profile(sk), s * (bhw_ + 3), s * (hw + 40), CUT, participants=[shell_body(B)], name='Wing step %+d' % s)
    sk.isVisible = False
    # raised bonnet centre (bulge) continuing the grille line back to the scuttle
    bh, bw = ev('bulge_h'), ev('bulge_hw')
    if bh < 2:
        bh = 0
    xb0, xb1 = fx + 40, ev('ws_base_x') - 70
    xs = [xb0 + (xb1 - xb0) * k / 10 for k in range(11)]
    prof = [(x, bonnet_y(x) - 6) for x in xs] + [(x, bonnet_y(x) + bh * min(1.0, (x - xb0) / 60.0)) for x in xs[::-1]]
    sk = B.sketches.add(B.xYConstructionPlane); sk.name = 'Bonnet bulge'
    if bh == 0:
        prof = [(x, bonnet_y(x) - 6) for x in xs] + [(x, bonnet_y(x) - 2) for x in xs[::-1]]   # 2105: flat bonnet (no-op join)
    sk_poly(sk, prof)
    ei = B.features.extrudeFeatures.createInput(largest_profile(sk), JOIN)
    ei.setSymmetricExtent(VI(bw / 10), False)
    ei.participantBodies = [shell_body(B)]
    B.features.extrudeFeatures.add(ei).name = 'Bonnet bulge'
    sk.isVisible = False
    # sheet-metal edge radii on the lower body
    er = ev('edge_r')
    body = shell_body(B)
    fillet(B, body, lambda a, b, e: min(a[1], b[1]) > 600 and abs(abs(a[2]) - (bw)) < 2 and abs(abs(b[2]) - bw) < 2, 6, 'Bulge edges')
    fillet(B, shell_body(B), lambda a, b, e: min(a[1], b[1]) > 650 and abs(a[2]) > hw - 40 and abs(b[2]) > hw - 40 and abs(a[2] - b[2]) < 5 and b[0] - a[0] > 150, er, 'Wing and boot top edges')
    fillet(B, shell_body(B), lambda a, b, e: b[0] < fx + 80 and min(a[1], b[1]) > ev('bonnet_front_h') - 60 and abs(a[2] - b[2]) > 400, er, 'Front top edge')
    fillet(B, shell_body(B), lambda a, b, e: a[0] > bx - 80 and min(a[1], b[1]) > ev('rear_top_h') - 80 and abs(a[2] - b[2]) > 400, er * 1.5, 'Rear top edge')

    # ---- 2. greenhouse (loft) + join
    gh = gh_loft(B, g, 0.0, 'Greenhouse')
    tools = adsk.core.ObjectCollection.create(); tools.add(gh)
    ci = B.features.combineFeatures.createInput(shell_body(B), tools)
    ci.operation = JOIN
    B.features.combineFeatures.add(ci).name = 'Join greenhouse'
    print('solid built; bodies:', B.bRepBodies.count)
    finish(B, g)

def finish(B, g):
    hw, rh, belt = g['hw'], g['roof_h'], g['belt_h']
    xf, xr, cy = ev('axle_f_x'), ev('axle_f_x') + ev('wheelbase'), ev('wheel_cy')
    ar, ad = ev('arch_r'), ev('arch_depth')
    sk = B.sketches.add(B.xYConstructionPlane); sk.name = 'Arches'
    for x in (xf, xr):
        sk.sketchCurves.sketchCircles.addByCenterRadius(P(x, cy), ar / 10)
    sk.isVisible = False
    for side in (1, -1):
        extrude(B, profiles(sk), side * (hw - ad), side * (hw + 40), CUT, participants=[shell_body(B)], name='Wheel arches %+d' % side)
    fillet(B, shell_body(B), lambda a, b, e: a[1] > rh - 120 and b[1] > rh - 120, ev('roof_edge_r'), 'Roof edges')
    fillet(B, shell_body(B), lambda a, b, e: a[1] > belt + 20 and b[1] < rh - 40 and b[1] - a[1] > 200, ev('pillar_r'), 'Pillar edges')
    shi = B.features.shellFeatures.createInput(adsk.core.ObjectCollection.createWithArray([shell_body(B)]), False)
    shi.insideThickness = VI(ev('skin_t') / 10)
    B.features.shellFeatures.add(shi).name = 'Skin shell'
    # rolled wheel-arch lips: half-tori round the arch edge, above the sill, joined to the shell
    lr = ev('lip_r')
    parts = []
    for x in (xf, xr):
        for s in (1, -1):
            zl = s * (side_hw(g, cy + ar * 0.7) - lr * 0.6)
            t = ttorus((x, cy, zl), (0, 0, 1), ar + lr * 0.4, lr)
            tsub(t, tbox(x, ev('sill_h') - 300, zl, 2 * ar + 100, 600, 100))                     # nothing below the sill
            tsub(t, tbox(x, cy, zl - s * (lr + 1), 2 * ar + 60, 2 * ar + 60, 2 * lr + 2))   # keep the outboard half
            parts.append(('Arch lip', t, None))
    commit(B, parts, 'Arch lips')
    lips = [b for b in B.bRepBodies if b.name == 'Arch lip']
    if lips:
        tools = adsk.core.ObjectCollection.create()
        for b in lips:
            tools.add(b)
        ci = B.features.combineFeatures.createInput(shell_body(B), tools)
        ci.operation = JOIN
        B.features.combineFeatures.add(ci).name = 'Join arch lips'
    print('shelled, lips', len(lips))
