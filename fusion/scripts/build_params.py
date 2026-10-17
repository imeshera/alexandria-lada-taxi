# Master parameter table for the VAZ-2107 Alexandria taxi. Every dimension the build scripts use is a Fusion
# user parameter; the comment records source + confidence (see references/notes/lada-dossier.md).
# Re-running this script UPDATES expressions and comments to the values below (the table is the source of truth).
# Frame: X from the front bumper face rearwards, Y up from the ground, Z lateral (+Z = car's right side).
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())

MM = 'mm'
TABLE = [
    # ---- overall (factory data)
    ('len_overall', '4145 mm', MM, 'Overall length incl. bumpers (VAZ factory data, HIGH)'),
    ('width_body', '1620 mm', MM, 'Overall width excl. mirrors (VAZ factory data, HIGH)'),
    ('roof_h', '1446 mm', MM, 'Overall height unladen (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; HIGH)'),
    ('wheelbase', '2424 mm', MM, 'Wheelbase (VAZ factory data, HIGH)'),
    ('track_f', '1365 mm', MM, 'Front track (VAZ factory data, HIGH)'),
    ('track_r', '1321 mm', MM, 'Rear track (VAZ factory data, HIGH)'),
    ('axle_f_x', '664 mm', MM, 'Front overhang, bumper face to front axle (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; HIGH)'),
    ('wheel_cy', '287 mm', MM, 'Wheel centre height (175/70R13 static radius, MED)'),
    # ---- side-profile stations (x from front bumper face), from the calibrated blueprint
    ('body_front_x', '60 mm', MM, 'Front panel x behind the bumper face (side photo 2006, wheelbase-scaled, MED)'),
    ('body_rear_x', '4100 mm', MM, 'Rear panel x (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('ws_base_x', '1000 mm', MM, 'Windscreen base x on the centreline at the scuttle (factory side view, MED)'),
    ('ws_top_x', '1420 mm', MM, 'Windscreen top x on the centreline at the roof edge (factory side view, MED)'),
    ('rs_top_x', '3030 mm', MM, 'Rear screen top x on the centreline (factory side view 3015 silhouette, MED)'),
    ('rs_base_x', '3338 mm', MM, 'Rear screen base x on the centreline (factory side view, MED)'),
    ('ws_base_k_x', '1195 mm', MM, 'Windscreen base x at the corners / A-pillar foot - wrap-around (side photos, MED)'),
    ('ws_top_k_x', '1480 mm', MM, 'Windscreen top x at the corners (factory side view + photos, MED)'),
    ('rs_top_k_x', '2985 mm', MM, 'Rear screen top x at the corners / C-pillar top (factory side view, MED)'),
    ('rs_base_k_x', '3255 mm', MM, 'Rear screen base x at the corners (wraps forward) (photos, LOW)'),
    ('screen_wrap_exp', '2.3', '', 'Plan-view screen curvature exponent: x = xc + (xk - xc) * t^n, t = |z| / half width'),
    ('b_pillar_x', '2120 mm', MM, 'B-pillar / door seam x (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('pillar_w', '48 mm', MM, 'A-pillar visible width behind the windscreen wrap, side view (photos, MED)'),
    ('b_pillar_w', '84 mm', MM, 'B-pillar width between the door glasses (drawing, MED)'),
    ('c_pillar_w', '260 mm', MM, 'C-pillar width at belt between rear door glass and rear screen (blueprint, MED)'),
    # ---- heights
    ('bonnet_front_h', '830 mm', MM, 'Bonnet front edge height (drawing 812-850; MED)'),
    ('cowl_h', '985 mm', MM, 'Scuttle / windscreen base height (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('belt_h', '947 mm', MM, 'Beltline: bottom of side glass (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('deck_h', '950 mm', MM, 'Boot lid front edge at the rear screen base (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('rear_top_h', '792 mm', MM, 'Boot lid rear edge / top of tail panel (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('swage_in', '16 mm', MM, 'Inward set-back of the flank above the upper swage line, at the belt (photos, MED)'),
    ('low_crease_h', '470 mm', MM, 'Lower crease line height along the flanks (factory side view ~450-480, MED)'),
    ('bonnet_step', '8 mm', MM, 'Wing tops sit below the bonnet edge by this step (photos, MED)'),
    ('bonnet_hw', '640 mm', MM, 'Bonnet half width at the shut line (factory front view, MED)'),
    ('bulge_hw', '300 mm', MM, 'Raised bonnet centre half width (follows the grille) (photos, MED)'),
    ('bulge_h', '16 mm', MM, 'Raised bonnet centre height (photos, LOW)'),
    ('lip_r', '9 mm', MM, 'Rolled wheel-arch lip tube radius (photos, MED)'),
    ('edge_r', '14 mm', MM, 'General sheet-metal edge radius (wing tops, front/rear top edges) (modelling choice)'),
    ('crease_h', '780 mm', MM, 'Upper swage line (crisp flank crease just under the door handles) (factory side view ~778, MED)'),
    ('sill_h', '300 mm', MM, 'Sill bottom height (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; MED)'),
    ('front_bot_h', '320 mm', MM, 'Front valance bottom (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; LOW)'),
    ('rear_bot_h', '340 mm', MM, 'Rear valance bottom (factory dimensioned drawing (carblueprints 1109x717), 6.73 mm/px H, 6.89 mm/px V; LOW)'),
    ('variant_2105', '0', '', 'Body variant: 0 = VAZ-2107 (this document), 1 = VAZ-2105'),
    ('roof_edge_r', '45 mm', MM, 'Roof perimeter edge radius (photos, MED)'),
    ('pillar_r', '25 mm', MM, 'A/C pillar edge radius (photos, MED)'),
    ('roof_crown', '25 mm', MM, 'Roof transverse crown (est., LOW)'),
    ('drip_h', '35 mm', MM, 'Window top below the roof edge (drip rail band) (photos, MED)'),
    # ---- widths
    ('belt_hw', '730 mm', MM, 'Half width at the side-glass base (factory drawing front view, 6.83 mm/px, MED)'),
    ('roof_hw', '630 mm', MM, 'Half width of the roof at the drip rails (factory drawing front view, 6.83 mm/px, MED)'),
    ('tuck_in', '30 mm', MM, 'Body side tuck-under at the sill (photos, LOW)'),
    ('plan_r_f', '80 mm', MM, 'Plan-view front corner radius (headlamps reach |z| 728: factory drawing front view, 6.83 mm/px, MED)'),
    ('plan_r_r', '100 mm', MM, 'Plan-view rear corner radius (blueprint top view, MED)'),
    # ---- wheel arches
    ('arch_r', '345 mm', MM, 'Wheel-arch cut-out radius (blueprint, MED)'),
    ('arch_depth', '260 mm', MM, 'Wheelhouse depth inboard from the body side (est., LOW)'),
    # ---- skin
    ('skin_t', '3 mm', MM, 'Body skin thickness (modelling choice, printable at ~1:18)'),
    ('gap_w', '4 mm', MM, 'Panel shut-line width (photos, MED)'),
    ('gap_d', '2 mm', MM, 'Panel shut-line depth (modelling choice)'),
]

def run(_context: str):
    for n, e, u, c in TABLE:
        param(n, e, u, c, update=True)
    print('parameters:', design.userParameters.count)
