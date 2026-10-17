# Alexandria taxi livery + materials (run after any rebuild of the body/openings).
# Split on the panel shut lines (references/notes/livery-and-plates.md):
#   BLACK : front wings, rear quarters incl. C-pillars, sills, roof, front-panel corners, rear corners
#   YELLOW: doors, bonnet (+ bulge), boot lid, tail panel between the lamps, front panel/valance between the lamps,
#           and - on the reference car (pillars_yellow = 1) - A/B pillars and door window frames
# Slightly weathered: faded yellow, oxidised black, dusty lower sills, dirtier door bottoms below the rubbing strip.
# Face splits: greenhouse sides at the C-pillar line, front face at the headlamp outer edges, rear face at the
# tail-lamp inner edges, doors at the dirt line.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())
exec(open(os.path.join(ROOT, '_geom.py')).read(), globals())

TAG = 'Livery split'

def run(_context: str):
    param('pillars_yellow', '1', '', 'A/B pillars + door frames yellow (reference photo) = 1, black (most Alexandria cars) = 0', update=False)
    g = G()
    py = round(evu('pillars_yellow')) == 1
    yellow = color_app('Taxi Yellow (faded)', 'Paint - Enamel Glossy (Yellow)', (234, 194, 38))
    yellow_dirty = color_app('Taxi Yellow (dirty)', 'Paint - Enamel Glossy (Yellow)', (196, 164, 58))
    black = color_app('Taxi Black (oxidised)', 'Paint - Enamel Glossy (Black)', (40, 41, 43))
    black_dusty = color_app('Taxi Black (dusty)', 'Paint - Enamel Glossy (Black)', (66, 62, 56))
    inner = color_app('Body Interior Grey', 'Paint - Enamel Glossy (Dark Grey)', (88, 88, 86))
    under = color_app('Underbody (dirty)', 'Paint - Enamel Glossy (Dark Grey)', (48, 44, 40))
    B = get_comp('Body')

    # ---- remove previous splits
    for c in (B,):
        for i in range(c.features.splitFaceFeatures.count - 1, -1, -1):
            if c.features.splitFaceFeatures.item(i).name.startswith(TAG):
                c.features.splitFaceFeatures.item(i).deleteMe()
        for i in range(c.constructionPlanes.count - 1, -1, -1):
            if c.constructionPlanes.item(i).name.startswith(TAG):
                c.constructionPlanes.item(i).deleteMe()
        for i in range(c.sketches.count - 1, -1, -1):
            if c.sketches.item(i).name.startswith(TAG):
                c.sketches.item(i).deleteMe()

    def plane3(pts, name):
        sk = B.sketches.add(B.xYConstructionPlane); sk.name = TAG + ' pts ' + name
        sp = [sk.sketchPoints.add(P(*p)) for p in pts]
        sk.isVisible = False
        pi = B.constructionPlanes.createInput(); pi.setByThreePoints(sp[0], sp[1], sp[2])
        pl = B.constructionPlanes.add(pi); pl.name = TAG + ' ' + name; pl.isLightBulbOn = False
        return pl

    def split(bodies, plane_base, off, pick, name):
        pl = plane_base if off is None else offset_plane(B, plane_base, off, TAG + ' ' + name)
        faces = adsk.core.ObjectCollection.create()
        for b in bodies:
            for f in b.faces:
                if pick(f):
                    faces.add(f)
        if faces.count == 0:
            print('no faces for', name); return
        si = B.features.splitFaceFeatures.createInput(faces, pl, True)
        try:
            B.features.splitFaceFeatures.add(si).name = TAG + ' ' + name
        except Exception as ex:
            print('split failed', name, ex)

    def shell():
        return [b for b in B.bRepBodies if b.name == 'Body shell'][0]

    def spans(f, axis, v):
        bb = f.boundingBox
        lo, hi = getattr(bb.minPoint, axis) * 10, getattr(bb.maxPoint, axis) * 10
        return lo + 1 < v < hi - 1

    xc = g['rdw_x1'] + 45                                  # C-pillar front line at the belt (rear door frame ends)
    # sloped C-pillar line parallel to the rear door glass trailing edge, 45 mm behind it
    xt = g.get('rdw_top_x', g['rdw_x1']) + 45
    cpl = plane3([(xc, g['belt_h'], 0), (xt, g['win_top'], 0), (xc, g['belt_h'], 500)], 'C-pillar')
    split([shell()], cpl, None, lambda f: spans(f, 'x', (xc + xt) / 2) and f.boundingBox.minPoint.y * 10 > g['belt_h'] - 30, 'C-pillar')
    for zz, nm in ((ev('lamp_zo'), 'front L'), (-ev('lamp_zo'), 'front R')):
        split([shell()], B.xYConstructionPlane, zz, lambda f, zz=zz: spans(f, 'z', zz) and f.boundingBox.maxPoint.x * 10 < ev('body_front_x') + 60, nm)
    for zz, nm in ((ev('tail_zi') - 5, 'rear L'), (-(ev('tail_zi') - 5), 'rear R')):
        split([shell()], B.xYConstructionPlane, zz, lambda f, zz=zz: spans(f, 'z', zz) and f.boundingBox.minPoint.x * 10 > ev('body_rear_x') - 60, nm)
    dirt_y = ev('rub_y') - 45
    doors = [b for b in B.bRepBodies if b.name.startswith(('Front door', 'Rear door'))]
    split(doors, B.xZConstructionPlane, dirt_y, lambda f: spans(f, 'y', dirt_y), 'door dirt line')

    # ---- paint the shell face by face
    ctr = adsk.core.Point3D.create(207, 75, 0)
    n_y = n_b = 0
    for f in shell().faces:
        c = f.centroid
        ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
        x, y, z = c.x * 10, c.y * 10, c.z * 10
        d = (c.x - ctr.x) * n.x + (c.y - ctr.y) * n.y + (c.z - ctr.z) * n.z
        if d < 0:                                           # inside skin / wheelhouses
            f.appearance = black if (n.y < -0.5 and y < 700) or abs(z) > g['hw'] - ev('arch_depth') - 5 and y < 700 else inner
            continue
        if n.y < -0.6:                                      # underside
            f.appearance = under; continue
        col = black
        if y > g['belt_h'] + 8:                             # greenhouse
            if n.y > 0.35:
                col = black                                 # roof + roof edge
            elif n.x < -0.3:
                col = yellow if py else black               # windscreen frame / A-pillar fronts
            elif n.x > 0.3:
                col = black                                 # rear-screen frame (C-pillars / roof)
            else:
                xl = xc + (xt - xc) * (y - g['belt_h']) / (g['win_top'] - g['belt_h'])
                col = (yellow if py else black) if x < xl else black
        else:
            if n.x < -0.7 and abs(z) < ev('lamp_zo'):
                col = yellow                                # front panel + valance between the lamps
            elif n.x > 0.7 and abs(z) < ev('tail_zi') - 5:
                col = yellow                                # tail panel
            elif y < ev('door_bot_h') + 10 and abs(n.y) < 0.6:
                col = black_dusty                           # sills / lower valances
        f.appearance = col
        n_y += col == yellow; n_b += col != yellow
    # ---- separate panels
    # panels cut out of the shell inherit the shell's face-level paint, so paint every face explicitly
    for b in B.bRepBodies:
        if b.name.startswith(('Bonnet', 'Boot lid')):
            b.appearance = yellow
            for f in b.faces:
                f.appearance = yellow
        elif b.name.startswith(('Front door', 'Rear door')):
            b.appearance = yellow
            for f in b.faces:
                f.appearance = yellow_dirty if f.centroid.y * 10 < dirt_y else yellow
    F = get_comp('Front End')
    for b in F.bRepBodies:
        if b.name == 'Bonnet bulge':
            b.appearance = yellow
    T = get_comp('Trim')
    for b in T.bRepBodies:
        if base_name(b.name) == 'Fuel flap':
            b.appearance = black
    # mirrors etc. built before the commit() fix: re-assert trim colours by name
    blackp = color_app('Black Plastic (weathered)', 'Plastic - Matte (Black)', (34, 34, 33))
    chrome = lib_app('Chrome')
    for b in T.bRepBodies:
        n = base_name(b.name)
        if n.startswith(('Mirror base', 'Mirror arm', 'Mirror head', 'Wiper', 'Door handle recess', 'C-pillar vent')):
            b.appearance = blackp
        elif n.startswith(('Door handle', 'Door lock', 'Drip rail', 'Rubbing strip chrome', 'Mirror glass')):
            b.appearance = chrome
    print('shell faces yellow/black:', n_y, n_b)
