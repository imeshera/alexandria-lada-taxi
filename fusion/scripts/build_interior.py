# Cabin (component "Interior"): VAZ-2107 dashboard (padded top, instrument hood, 4-dial cluster, centre console
# with heater sliders / clock / radio / ashtray, vents, glovebox), steering column + 2-spoke wheel, pedals,
# gear lever + boot, handbrake, door cards (armrest, pull, handle, window winder, pocket), carpet, headliner,
# sun visors, rear-view mirror with prayer beads (misbaha), dome light, rear parcel shelf.
# LHD: the driver sits on the car's left = -Z.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())
exec(open(os.path.join(ROOT, '_geom.py')).read(), globals())

PARAMS = [
    ('dash_face_x', '1430 mm', 'Dashboard face x (2107 interior photos + package est., LOW)'),
    ('dash_top_y', '935 mm', 'Dashboard top height (est. just under the belt, MED)'),
    ('wheel_d', '390 mm', 'Steering wheel diameter (2107: ~390 mm, MED)'),
    ('wheel_x', '1650 mm', 'Steering wheel centre x (package est., LOW)'),
    ('wheel_y', '815 mm', 'Steering wheel centre height (package est., LOW)'),
    ('column_deg', '24 deg', 'Steering column angle above horizontal (est.)'),
]

def run(_context: str):
    for n, e, c in PARAMS:
        param(n, e, 'deg' if n.endswith('_deg') else 'mm', c, update=True)
    C = get_comp('Interior')
    wipe(C)
    g = G()
    dash_black = color_app('Dash Black (sun-faded)', 'Plastic - Matte (Black)', (38, 37, 36))
    vinyl = color_app('Seat Vinyl (black, worn)', 'Leather - Weathered', (32, 30, 29))
    card = color_app('Door Card Vinyl (brown)', 'Leather - Weathered', (74, 56, 44))
    carpet = color_app('Carpet (dark grey, dirty)', 'Fabric (Grey)', (54, 52, 50))
    liner = color_app('Headliner (beige, stained)', 'Fabric (White)', (200, 190, 168))
    chrome = lib_app('Chrome')
    white = lib_app('Plastic - Matte (White)')
    dial = color_app('Dial Face Black', 'Plastic - Matte (Black)', (14, 14, 16))
    red = color_app('Red Lens (opaque)', 'Plastic - Glossy (Red)', (185, 22, 18))
    green = color_app('Prayer Beads Green', 'Plastic - Glossy (Green)', (20, 120, 70))
    glass = lib_app('Glass (Clear)')
    floor = g['sill_h'] + 3
    dfx, dty = ev('dash_face_x'), ev('dash_top_y')
    iw = g['hw'] - 70                                  # interior half width at dash height

    # ---- dashboard main moulding: side-view profile extruded across
    sk = C.sketches.add(C.xYConstructionPlane); sk.name = 'Dash profile'
    prof = [(ws_x(g, dty) + 25, dty + 5), (dfx - 40, dty), (dfx + 20, dty - 35), (dfx + 15, dty - 160), (dfx - 30, dty - 260),
            (dfx - 60, dty - 330), (ws_x(g, g['cowl_h']) - 30, dty - 330)]
    sk_poly(sk, prof)
    ei = C.features.extrudeFeatures.createInput(largest_profile(sk), NEW)
    ei.setSymmetricExtent(VI(iw / 10), False)
    f = C.features.extrudeFeatures.add(ei); f.name = 'Dashboard'
    for b in f.bodies:
        b.name = 'Dashboard'; b.appearance = dash_black
    sk.isVisible = False
    parts = []
    zd = -ev('seat_f_z')                                # driver centreline (LHD, car's left)
    # instrument hood + cluster (2 big dials: speedometer, tachometer; 2 small: fuel, coolant temp)
    # binnacle: rectangular hood ~400 wide with a rounded top, overhanging the dials
    hood = tbox(dfx + 5, dty - 25, zd, 110, 70, 400)
    tunion(hood, tcyl((dfx + 5, dty + 10, zd - 200), (dfx + 5, dty + 10, zd + 200), 55))
    tsub(hood, tbox(dfx - 60, dty + 10, zd, 130, 160, 410))
    parts.append(('Instrument hood', hood, dash_black))
    # padded top roll along the dash face, knee panel below
    parts.append(('Dash top roll', tcyl((dfx + 5, dty - 20, -iw + 10), (dfx + 5, dty - 20, iw - 10), 24), vinyl))
    parts.append(('Knee panel', tbox(dfx - 25, dty - 285, zd, 30, 90, 520), dash_black))
    parts.append(('Cluster face', tbox(dfx + 12, dty - 90, zd, 6, 120, 370), dial))
    # driver faces -X, so the driver's left is +Z: tachometer left (+85), speedometer right (-85),
    # two pairs of small gauges (fuel / coolant, econometer / voltmeter) stacked on the outer flanks
    dials = [(85, 0, 52), (-85, 0, 52), (165, 22, 20), (165, -26, 20), (-165, 22, 20), (-165, -26, 20)]
    for dz, dy, r in dials:
        yy = dty - 90 + dy
        parts.append(('Dial', tcyl((dfx + 16, yy, zd + dz), (dfx + 18, yy, zd + dz), r), dial))
        parts.append(('Dial bezel', ttorus((dfx + 18, yy, zd + dz), (1, 0, 0), r + 2, 3), chrome))
        parts.append(('Dial ticks', ttorus((dfx + 18.5, yy, zd + dz), (1, 0, 0), r - 0.16 * r - 3, 1.4), white))
        nd = tbox(dfx + 19.5, yy + r * 0.3, zd + dz - r * 0.2, 1, r * 0.75, 3)
        tbm.transform(nd, mat_rot((1, 0, 0), 35, (dfx + 19.5, yy, zd + dz)))
        parts.append(('Dial needle', nd, red))
    parts.append(('Warning lamps', tbox(dfx + 16, dty - 90, zd, 2, 90, 14), red))
    # centre console: heater panel, clock, radio, ashtray, switches
    cx0 = dfx - 30
    # centre console sloping from the dash down to the tunnel
    cons = tbox(cx0 + 40, (dty - 120 + floor + 190) / 2, 0, 120, dty - 120 - floor - 190, 250)
    tbm.transform(cons, mat_rot((0, 0, 1), -12, (cx0 + 40, floor + 190, 0)))
    parts.append(('Centre console', cons, dash_black))
    parts.append(('Clock', tcyl((dfx + 18, dty - 60, 0), (dfx + 22, dty - 60, 0), 35), dial))
    parts.append(('Clock bezel', ttorus((dfx + 22, dty - 60, 0), (1, 0, 0), 37, 3), chrome))
    parts.append(('Heater panel', tbox(dfx + 12, dty - 150, 0, 6, 70, 200), dial))
    for k in range(3):
        parts.append(('Heater slider', tbox(dfx + 18, dty - 150, -60 + 60 * k, 10, 14, 18), white))
    parts.append(('Radio', tbox(cx0 + 25, dty - 235, 0, 10, 50, 180), dial))
    parts.append(('Radio knobs', tcyl((cx0 + 30, dty - 235, -75), (cx0 + 42, dty - 235, -75), 9), chrome))
    parts.append(('Radio knobs', tcyl((cx0 + 30, dty - 235, 75), (cx0 + 42, dty - 235, 75), 9), chrome))
    parts.append(('Ashtray', tbox(cx0 + 22, dty - 300, 0, 8, 40, 150), chrome))
    for k in range(4):
        parts.append(('Rocker switch', tbox(dfx + 18, dty - 200, -150 - 30 * k, 8, 24, 16), white))
    # air vents (2 centre + 2 outer), glovebox
    for z in (-130, 130, -(iw - 70), iw - 70):
        parts.append(('Air vent', tbox(dfx + 14, dty - 40, z, 6, 50, 90), dial))
        for k in range(4):
            parts.append(('Vent vane', tbox(dfx + 17, dty - 58 + 12 * k, z, 4, 3, 86), dash_black))
    parts.append(('Glovebox lid', tbox(dfx + 17, dty - 140, ev('seat_f_z'), 6, 140, 360), dash_black))
    parts.append(('Glovebox lock', tcyl((dfx + 20, dty - 100, ev('seat_f_z')), (dfx + 26, dty - 100, ev('seat_f_z')), 10), chrome))
    # steering column + wheel (rim torus, 2 spokes, hub pad, horn badge)
    wx, wy, wd = ev('wheel_x'), ev('wheel_y'), ev('wheel_d')
    a = math.radians(evdeg('column_deg'))
    ax = (math.cos(a), math.sin(a), 0)               # column axis pointing up/rearwards to the driver
    base = (wx - 330 * ax[0], wy - 330 * ax[1], zd)
    parts.append(('Steering column', tcyl(base, (wx - 40 * ax[0], wy - 40 * ax[1], zd), 28), dash_black))
    parts.append(('Column shroud', tcyl((base[0] + 60 * ax[0], base[1] + 60 * ax[1], zd), (wx - 110 * ax[0], wy - 110 * ax[1], zd), 55, 45), dash_black))
    # late (2000s) 4-spoke wheel with a round concave LADA hub (Egyptian-assembled taxis are 2002-2015 cars)
    rim = ttorus((0, 0, 0), (0, 0, 1), wd / 2 - 14, 14)
    hub = tcyl((0, 0, -30), (0, 0, 25), 62)
    tsub(hub, tsphere((0, 0, 95), 75))                  # concave face
    sp = []
    for ang in (-10, 190, 245, 295):
        a2 = math.radians(ang)
        r0, r1 = 55, wd / 2 - 18
        sp.append(tcyl((r0 * math.cos(a2), r0 * math.sin(a2), -6), (r1 * math.cos(a2), r1 * math.sin(a2), -14), 11, 8))
    for bdy in [rim, hub] + sp:
        # local Z -> column axis, then move to the wheel centre
        m = adsk.core.Matrix3D.create()
        m.setToRotateTo(V3(0, 0, 1), V3(*ax))
        tbm.transform(bdy, m)
        tbm.transform(bdy, mat_tr(wx, wy, zd))
    parts += [('Steering wheel rim', rim, vinyl), ('Steering wheel hub', hub, dash_black)] + [('Steering wheel spoke', b, dash_black) for b in sp]
    badge = tcyl((0, 0, 14), (0, 0, 20), 24)
    m = adsk.core.Matrix3D.create(); m.setToRotateTo(V3(0, 0, 1), V3(*ax)); tbm.transform(badge, m); tbm.transform(badge, mat_tr(wx, wy, zd))
    parts.append(('Horn badge', badge, chrome))
    # pedals (clutch, brake, throttle) for the driver
    for dz, w in ((-90, 70), (0, 70), (90, 50)):
        parts.append(('Pedal pad', tbox(1330, floor + 120, zd + dz, 12, 70, w), dash_black))
        parts.append(('Pedal arm', tcyl((1335, floor + 150, zd + dz), (1420, dty - 330, zd + dz), 8), dash_black))
    # gear lever + boot, handbrake
    parts.append(('Gear lever boot', tcyl((1790, floor + 180, 0), (1770, floor + 260, 0), 70, 30), vinyl))
    parts.append(('Gear lever', tcyl((1770, floor + 250, 0), (1700, floor + 480, 0), 7), chrome))
    parts.append(('Gear knob', tsphere((1696, floor + 490, 0), 24), dash_black))
    parts.append(('Handbrake lever', tcyl((2140, floor + 190, 0), (1990, floor + 250, 0), 14), dash_black))
    parts.append(('Handbrake boot', tbox(2130, floor + 185, 0, 120, 20, 70), vinyl))
    # carpet (front + rear foot wells) and rear parcel shelf
    parts.append(('Carpet', tbox(2200, floor + 5, 0, 2000, 10, 2 * iw), carpet))
    mat = color_app('Rubber Mat (worn)', 'Rubber - Soft', (30, 30, 30))
    for mx0, mz in ((1480, -360), (1480, 360), (2420, -360), (2420, 360)):
        parts.append(('Floor mat', tbox(mx0 + 200, floor + 12, mz, 420, 6, 420), mat))
        for k in range(8):
            parts.append(('Floor mat rib', tbox(mx0 + 30 + 48 * k, floor + 16, mz, 10, 4, 380), mat))
    rsx = g['rs_base_x']
    parts.append(('Parcel shelf', tbox(rsx - 120, g['deck_h'] - 20, 0, 260, 14, 2 * iw - 20), carpet))
    for z in (-420, 420):
        parts.append(('Shelf speaker grille', tcyl((rsx - 120, g['deck_h'] - 12, z), (rsx - 120, g['deck_h'] - 9, z), 70), dial))
    # headliner, sun visors, dome light, rear-view mirror + misbaha
    rh = g['roof_h']
    hx0, hx1 = g['ws_top_x'] + 30, g['rs_top_x'] - 30
    parts.append(('Headliner', tbox((hx0 + hx1) / 2, rh - 48, 0, hx1 - hx0, 8, 2 * (g['roof_hw'] - 60)), liner))
    for z, zz in ((-1, 260), (1, 260)):
        parts.append(('Sun visor', tbox(g['ws_top_x'] + 140, rh - 70, z * zz, 170, 20, 390), liner))
    parts.append(('Dome light', tbox(2150, rh - 56, 0, 120, 10, 70), white))
    mx = g['ws_top_x'] + 70
    parts.append(('Mirror stalk', tcyl((mx, rh - 52, 0), (mx + 10, rh - 120, 0), 6), dash_black))
    parts.append(('Rear-view mirror', tbox(mx + 15, rh - 140, 0, 25, 60, 210), dash_black))
    parts.append(('Rear-view mirror glass', tbox(mx + 28.5, rh - 140, 0, 2, 50, 200), chrome))
    # prayer beads (33 beads on a loop) hanging from the mirror stalk
    cxm, cym = mx + 20, rh - 260
    for k in range(33):
        t = 2 * math.pi * k / 33
        parts.append(('Misbaha bead', tsphere((cxm, cym + 95 * math.cos(t), 40 * math.sin(t)), 6), green))
    parts.append(('Misbaha tassel', tcyl((cxm, cym - 95, 0), (cxm, cym - 150, 0), 9, 3), green))
    # door cards (both sides, front and rear doors)
    hy = ev('handle_y')
    for s in (1, -1):
        for x0, x1, front in ((ev('door_f_x0') + 25, g['b_pillar_x'] - 25, True), (g['b_pillar_x'] + 25, ev('door_r_x1') - 60, False)):
            y0, y1 = ev('door_bot_h') + 40, g['belt_h'] - 15
            zc = s * (side_hw(g, (y0 + y1) / 2) - 3 - 12)
            parts.append(('Door card', tbox((x0 + x1) / 2, (y0 + y1) / 2, zc, x1 - x0, y1 - y0, 10), card))
            zi = zc - s * 5
            parts.append(('Door armrest', tbox((x0 + x1) / 2 + 40, hy - 160, zi - s * 30, (x1 - x0) * 0.5, 40, 60), vinyl))
            parts.append(('Door inner handle', tbox(x0 + 120, hy - 20, zi - s * 6, 90, 22, 12), chrome))
            wcx = (x0 + x1) / 2 - 60
            parts.append(('Window winder', tcyl((wcx, hy - 70, zi), (wcx, hy - 70, zi - s * 30), 16), chrome))
            parts.append(('Window winder', tbox(wcx + 45, hy - 70, zi - s * 32, 100, 14, 6), chrome))
            parts.append(('Window winder knob', tcyl((wcx + 90, hy - 70, zi - s * 32), (wcx + 90, hy - 70, zi - s * 62), 10), dash_black))
            if front:
                parts.append(('Door pocket', tbox((x0 + x1) / 2, y0 + 90, zi - s * 18, (x1 - x0) * 0.7, 120, 26), card))
            parts.append(('Door lock knob', tcyl((x1 - 60, y1 - 5, zi - s * 15), (x1 - 60, y1 + 35, zi - s * 15), 6), dash_black))
    commit(C, parts, 'Cabin parts')
    print('interior bodies:', C.bRepBodies.count)
