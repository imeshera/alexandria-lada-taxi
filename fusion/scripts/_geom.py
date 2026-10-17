# Shared body geometry derived from the document's user parameters (mm). exec'd after _lib.py by the build scripts, so the
# openings, glass and trim all follow the same outlines.

def G():
    g = {k: ev(k) for k in ('width_body', 'roof_h', 'roof_crown', 'belt_h', 'cowl_h', 'deck_h', 'ws_base_x', 'ws_top_x',
                            'rs_top_x', 'rs_base_x', 'b_pillar_x', 'pillar_w', 'belt_hw', 'roof_hw', 'drip_h',
                            'roof_edge_r', 'crease_h', 'sill_h', 'tuck_in', 'b_pillar_w', 'ws_base_k_x', 'ws_top_k_x',
                            'rs_top_k_x', 'rs_base_k_x', 'swage_in', 'low_crease_h')}
    g['wrap_n'] = evu('screen_wrap_exp')
    g['roof_e'] = g['roof_h'] - g['roof_crown']          # roof edge height (top of the tumblehome sides)
    g['hw'] = g['width_body'] / 2
    g['L'] = ev('len_overall')
    for k in ('rdw_x1', 'rdw_top_x', 'rdw_div_x', 'rdw_r', 'win_r', 'ws_pillar_w', 'ws_r'):
        try:
            g[k] = ev(k)
        except Exception:
            pass
    g['win_top'] = g['roof_h'] - g['roof_crown'] - g['drip_h'] - g['roof_edge_r'] * 0.6
    return g

def hw_at(g, y):
    """Greenhouse (tumblehome) half width at height y."""
    return g['belt_hw'] + (g['roof_hw'] - g['belt_hw']) * (y - g['belt_h']) / (g['roof_h'] - g['roof_crown'] - g['belt_h'])

def side_section(g):
    """Half section of the lower body (z, y) from the sill up: tuck-under, lower crease kink, crisp upper swage line,
    set-back shoulder to the belt (shared by build_body.py and the trim/decal scripts)."""
    hw, ti, sill, cr, belt, lc, si = g['hw'], g['tuck_in'], g['sill_h'], g['crease_h'], g['belt_h'], g['low_crease_h'], g['swage_in']
    return [(hw - ti, sill - 20), (hw - 12, sill + 60), (hw - 6, lc - 30), (hw - 3, lc), (hw - 1, cr - 10), (hw, cr),
            (hw - 6, cr + 12), (hw - si, belt), (hw - si - 2, g['roof_h'] + 50)]

def side_hw(g, y):
    """Lower-body side surface half width at height y."""
    pts = [(yy, z) for z, yy in side_section(g)]
    for (y0, z0), (y1, z1) in zip(pts, pts[1:]):
        if y0 <= y <= y1:
            return z0 + (z1 - z0) * (y - y0) / (y1 - y0)
    return pts[0][1] if y < pts[0][0] else pts[-1][1]

def _lin(x0, y0, x1, y1, y):
    return x0 + (x1 - x0) * (y - y0) / (y1 - y0)

def ws_x(g, y):
    """Windscreen surface x on the centreline at height y."""
    return _lin(g['ws_base_x'], g['cowl_h'], g['ws_top_x'], g['roof_e'], y)

def wsk_x(g, y):
    """Windscreen surface x at the corners (A-pillar line) at height y."""
    return _lin(g['ws_base_k_x'], g['cowl_h'], g['ws_top_k_x'], g['roof_e'], y)

def rs_x(g, y):
    return _lin(g['rs_base_x'], g['deck_h'], g['rs_top_x'], g['roof_e'], y)

def rsk_x(g, y):
    return _lin(g['rs_base_k_x'], g['deck_h'], g['rs_top_k_x'], g['roof_e'], y)

def wrap(g, t):
    return min(1.0, max(0.0, t)) ** g['wrap_n']

def front_x(g, y, z, off=0.0):
    """x of the (curved, wrap-around) windscreen surface at (y, z), offset `off` outward (approx.)."""
    w = hw_at(g, y)
    return ws_x(g, y) + (wsk_x(g, y) - ws_x(g, y)) * wrap(g, abs(z) / w) - off

def rear_x(g, y, z, off=0.0):
    w = hw_at(g, y)
    return rs_x(g, y) + (rsk_x(g, y) - rs_x(g, y)) * wrap(g, abs(z) / w) + off

T_SAMPLES = (0.0, 0.3, 0.5, 0.65, 0.78, 0.88, 0.95, 1.0)

def gh_section(g, y, off=0.0):
    """Closed plan-view outline (x, z) of the greenhouse at height y, grown by `off` (front spline, side, rear spline, side)."""
    w = hw_at(g, y) + off
    xc, xk = ws_x(g, y) - off, wsk_x(g, y) - off
    rc, rk = rs_x(g, y) + off, rsk_x(g, y) + off
    front = [(xc + (xk - xc) * wrap(g, t), -t * w) for t in T_SAMPLES[::-1]] + [(xc + (xk - xc) * wrap(g, t), t * w) for t in T_SAMPLES[1:]]
    rear = [(rc + (rk - rc) * wrap(g, t), t * w) for t in T_SAMPLES[::-1]] + [(rc + (rk - rc) * wrap(g, t), -t * w) for t in T_SAMPLES[1:]]
    return front, rear

def gh_loft(c, g, off, name, y0=None, y1=None):
    """Greenhouse solid: loft between two plan sections (curved screens, tumblehome), trimmed by the roof crown.
    off grows the solid (used for glass / rubber / chrome bands). Returns the body."""
    y0 = g['belt_h'] - 70 if y0 is None else y0
    y1 = g['roof_h'] + 15 if y1 is None else y1
    profs = []
    for y in (y0, y1):
        pl = offset_plane(c, c.xZConstructionPlane, y, name + ' plane')
        sk = c.sketches.add(pl); sk.name = name + ' section'
        sk.isComputeDeferred = True
        front, rear = gh_section(g, y, off)
        sp = adsk.core.ObjectCollection.create()
        for x, z in front:
            sp.add(P(x, -z))
        s1 = sk.sketchCurves.sketchFittedSplines.add(sp)
        sp = adsk.core.ObjectCollection.create()
        for x, z in rear:
            sp.add(P(x, -z))
        s2 = sk.sketchCurves.sketchFittedSplines.add(sp)
        L = sk.sketchCurves.sketchLines
        L.addByTwoPoints(s1.endSketchPoint, s2.startSketchPoint)
        L.addByTwoPoints(s2.endSketchPoint, s1.startSketchPoint)
        sk.isComputeDeferred = False
        sk.isVisible = False
        profs.append(largest_profile(sk))
    li = c.features.loftFeatures.createInput(NEW)
    for p in profs:
        li.loftSections.add(p)
    li.isSolid = True
    lf = c.features.loftFeatures.add(li); lf.name = name
    body = lf.bodies.item(0); body.name = name
    # roof crown: arc through (+-roof_hw, roof edge) and (0, roof_h), grown by off
    sk = c.sketches.add(c.yZConstructionPlane); sk.name = name + ' crown'
    rw, re_, rh = g['roof_hw'] + off, g['roof_e'] + off, g['roof_h'] + off
    arc = sk.sketchCurves.sketchArcs.addByThreePoints(P(-rw, re_), P(0, rh), P(rw, re_))
    a0, a1 = arc.startSketchPoint, arc.endSketchPoint
    if a0.geometry.x > a1.geometry.x:
        a0, a1 = a1, a0
    L = sk.sketchCurves.sketchLines
    hw = g['hw'] + 150
    l1 = L.addByTwoPoints(a1, P(rw + 280, re_ - 200))
    l2 = L.addByTwoPoints(l1.endSketchPoint, P(hw, 0))
    l3 = L.addByTwoPoints(l2.endSketchPoint, P(-hw, 0))
    l4 = L.addByTwoPoints(l3.endSketchPoint, P(-rw - 280, re_ - 200))
    L.addByTwoPoints(l4.endSketchPoint, a0)
    sk.isVisible = False
    extrude(c, largest_profile(sk), -200, g.get('L', 4400) + 200, INTERSECT, participants=[body])
    return [b for b in c.bRepBodies if b.name == name][-1]

def side_window_polys(g, grow=0.0):
    """Side-view (x, y) outlines of the front and rear door glass openings, corners rounded, grown by `grow` mm."""
    y0, top = g['belt_h'] + 4 - grow, g['win_top'] + grow
    pw, bx, bw = g['pillar_w'], g['b_pillar_x'], g['b_pillar_w']
    a_x = lambda y: wsk_x(g, y) + pw
    fw = [(a_x(y0) - grow, y0), (bx - bw / 2 + grow, y0), (bx - bw / 2 + grow, top), (a_x(top) - grow, top)]
    rt = g.get('rdw_top_x', g['rdw_x1'])
    rw = [(bx + bw / 2 - grow, y0), (g['rdw_x1'] + grow, y0), (rt + grow, top), (bx + bw / 2 - grow, top)]
    wr = g['win_r'] + grow
    return [fillet_poly(fw, [0, 0, wr, wr * 2], 6), fillet_poly(rw, [0, 0, g['rdw_r'] + grow, wr], 8)]

def screen_poly(g, kind, inset, grow=0.0):
    """Front-view (z, y) outline of the windscreen / rear screen opening, rounded, grown by `grow`."""
    ylo = (g['cowl_h'] if kind == 'ws' else g['deck_h']) + 30 - grow
    yhi = g['roof_h'] - g['roof_crown'] - 45 + grow
    q = [(-(hw_at(g, ylo) - inset) - grow, ylo), ((hw_at(g, ylo) - inset) + grow, ylo),
         ((hw_at(g, yhi) - inset) + grow, yhi), (-(hw_at(g, yhi) - inset) - grow, yhi)]
    return fillet_poly(q, g['ws_r'] + grow, 6)

def on_side(g, poly_xy, dz=0.0, side=1):
    """Map side-view points onto the tumblehome glass plane (offset dz outward), side +1/-1."""
    return [(x, y, side * (hw_at(g, y) + dz)) for x, y in poly_xy]

def on_screen(g, poly_zy, kind, dn=0.0):
    """Map front-view (z, y) points onto the curved windscreen ('ws') or rear screen ('rs'), offset dn outward."""
    f = front_x if kind == 'ws' else rear_x
    return [(f(g, y, z, dn), y, z) for z, y in poly_zy]

def screen_band(c, g, off_in, off_out, grow_out, grow_in, name, ap=None, kinds=('ws', 'rs'), inset=None):
    """Curved band following the windscreen / rear screen surfaces: (loft grown off_out) minus (loft grown off_in),
    intersected with the front-view outline prism (screen_poly grown grow_out; minus grow_in if given -> a ring).
    Returns the new bodies (one per kind)."""
    inset = g['ws_pillar_w'] if inset is None else inset
    outer = gh_loft(c, g, off_out, name + ' outer')
    inner = gh_loft(c, g, off_in, name + ' inner')
    tools = adsk.core.ObjectCollection.create(); tools.add(inner)
    ci = c.features.combineFeatures.createInput(outer, tools)
    ci.operation = CUT
    c.features.combineFeatures.add(ci)
    shellb = [b for b in c.bRepBodies if b.name == name + ' outer'][-1]
    out = []
    for k, kind in enumerate(kinds):
        if k < len(kinds) - 1:
            commit(c, [(name + ' ' + kind, tbm.copy(shellb), None)], name + ' copy')
            target = [b for b in c.bRepBodies if b.name == name + ' ' + kind][-1]
        else:
            target = shellb
            target.name = name + ' ' + kind
        sk = c.sketches.add(c.yZConstructionPlane); sk.name = name + ' ' + kind + ' outline'
        sk_poly(sk, [(-z, y) for z, y in screen_poly(g, kind, inset, grow_out)])
        if grow_in is not None:
            sk_poly(sk, [(-z, y) for z, y in screen_poly(g, kind, inset, grow_in)])
            pick = lambda pr: pr.profileLoops.count == 2
        else:
            pick = None
        if kind == 'ws':
            x0, x1 = g['ws_base_x'] - 160, g['ws_top_k_x'] + 80
        else:
            x0, x1 = g['rs_top_k_x'] - 80, g['rs_base_x'] + 160
        extrude(c, profiles(sk, pick), x0, x1, INTERSECT, participants=[target])
        sk.isVisible = False
        b = [bb for bb in c.bRepBodies if bb.name == name + ' ' + kind]
        for bb in b:
            if ap is not None:
                bb.appearance = ap
        out += b
    return out
