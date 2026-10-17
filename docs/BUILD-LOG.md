# Lada taxi build log

Decisions, measurements and gotchas, newest section last. The published model in `models/` is the state at the end of
**"Recalibrated to the factory drawing"** + **"Factory underlay checks"** (Fusion version 5: livery, weathering,
late-spec interior, lettering). The **"Refinement pass (scripts only)"** section below is not in the published model yet.

## 2026-10-17 — Setup, research, block-out
- Fusion document **Alexandria Lada Taxi** (project Eshera-Personal, folder Alexandria Lada Taxi), Hybrid design
  intent. Frame: X from the front bumper face rearwards, Y up from the ground, Z lateral (+Z = car's right).
  Side view from +Z = Fusion "Front" view.
- All scripts exec `fusion/scripts/_lib.py`, which activates this document **by name** and provides mm-based helpers
  (temporary-B-rep primitives, sketch helpers, 3D planar plates, SVG lettering, appearances, atomic screenshots).
- Research in two strands: livery + plates (`references/notes/livery-and-plates.md`) and VAZ-2107
  dimensions/blueprints/interior (`references/notes/vaz2107-specs.md`).
- Livery (from ~15 dated Alexandria photos): split on panel shut lines, not a horizontal line. Black: front wings,
  rear quarters incl. C-pillars, sills, roof. Yellow: doors, bonnet, boot lid, tail panel, front valance.
  Pillars/door frames vary (black on most, yellow on the reference car) -> parameter `pillars_yellow`.
- Egyptian 2008 plate: 350 x 170 mm, orange band = taxi, "EGYPT" left / "مصر" right, digits left / letters right.
  First letter س = Alexandria, so the reference car's "٨٣٤ س ل م" is a valid Alexandria plate.

### Fusion API gotchas
- **Occurrence moves do not persist in this document.** `transform2` + `snapshots.add()` reverts to identity on the
  next compute (even after deleting all Position snapshots). Work-around: keep a hidden *master* occurrence that owns
  the component's features at the origin, and create the visible instances with
  `occurrences.addExistingComponent(comp, matrix)` - the matrix persists. Copies inherit the master's hidden state,
  so set `isLightBulbOn = True` on each.
- `pcd` is not a valid parameter name (it is a unit). Used `bolt_pcd`.
- `setSymmetricExtent(d, True)` means *full length* d (i.e. +/- d/2), not +/- d.
- **Cut extrudes reach into other components.** The wheel-arch cut also cut the (shared) wheel component, leaving
  zero-volume wheel bodies and an `Extrude` feature inside `Wheel`. Always set `participantBodies` (the lib's
  `extrude()` defaults cuts/intersects to the sketch component's own bodies).
- `SketchArcs.addByThreePoints` with a SketchPoint as the first argument produced a huge arc going the wrong way;
  pass Point3D for all three points and connect lines to the arc's end points afterwards.
- When several documents are open, the active document can change between separate API calls, so a separate
  screenshot call can capture the wrong model. `snap.py` activates this document, sets the camera and calls
  `viewport.saveAsImageFile` in one script.
- Patterns (`circularPatternFeatures`) must be deleted before the features they pattern, or the wipe leaves orphans.
- Fusion de-duplicates body names ("Door (1)") - match on the base name (`base_name()` in the lib).

### Geometry (pass 1, photo-calibrated)
- Side elevation from the 2006 Commons photo (`side_2107_full-side-elevation_2006.jpg`, see
  `references/sources/livery/MANIFEST.csv`), scaled by the wheelbase (916 px = 2424 mm -> 2.646 mm/px), heights
  re-scaled x0.976 so the drip line sits at ~1405 mm under the 1440 mm roof. Overhangs from the photo ratio: front
  axle 615 mm behind the bumper face.
- Stations: windscreen base 1180, roof front 1440, B-pillar 2080, roof rear 3010, rear screen base 3300,
  front door 1148-2080, rear door 2080-2948, belt 985, bonnet front 785, cowl 945, boot 975 -> 920.
  (Superseded by the factory drawing, below.)
- Body = (side profile ∩ plan ∩ section) ∪ (greenhouse side profile ∩ tumblehome section with roof crown),
  wheel arches cut 260 mm in from each side, roof fillet, 3 mm hollow shell (wheelhouses come out of the shell).
- Doors, bonnet and boot lid are separated by 4 mm through-slits on their shut lines -> separate bodies (two-tone
  livery by body + print parts). Both front doors end up as one 2-lump body ("Front doors").
- Calibrated canvas: the side photo mirrored (front left) on a plane at z = -1500 mm (`canvases.cfg`).

## 2026-10-17 — Detail pass: glass, trim, ends, roof, running gear, interior, livery
- `build_glazing.py`, `build_trim.py`, `build_ends.py`, `build_roof.py`, `build_chassis.py`, `build_seats.py`,
  `build_interior.py`, `build_plates.py`, `build_lettering.py`, `build_appearance.py` (see the README table).
- `_geom.py` holds the shared outlines (side glass, screens, tumblehome and lower-side half widths) so openings,
  glass, chrome rings and rubbers always agree.
- `plate3d()` (lib): planar plate from a 3D polygon via a construction plane through three sketch points; used for
  glass, window chrome rings, screen rubbers, C-pillar vents and the bonnet bulge.
- Lettering: plate (front + rear, rotated instance reads correctly), roof light "TAXI" (front, mirrored SVG on the
  YZ plane) and "للأجرة" (rear), plate number on both front doors (mirrored SVG on -Z).
- Livery pass splits faces at the C-pillar line, at the headlamp outer edges (front panel) and tail-lamp inner edges
  (tail panel), and paints face-by-face (outer/inner by normal vs. car centre); doors/bonnet/boot lid by body.
  Weathering: faded yellow, oxidised black, dusty sills, dirtier door bottoms (faces split at the dirt line).
- Gotchas: `TemporaryBRepManager.createTorus` ignores its centre (translate afterwards); appearances set on
  base-feature bodies after `finishEdit()` were sometimes lost - `commit()` now sets them inside the edit too.
  Transparent coloured glass reads almost black for lamp lenses; lamp lenses use opaque glossy plastics.

## 2026-10-17 — Recalibrated to the factory drawing
- The VAZ-2107 research found the AvtoVAZ factory dimensioned 4-view (4145 = 664 + 2424 + 1057, 1446 high).
  It disagreed with the street-photo calibration: the photo camera sat above the car, so its heights read 5-8 %
  high (belt 985 vs 947, handle 893 vs ~805, sill 340 vs ~300) and its overhangs were compressed (front 615 vs 664).
- All stations and heights now come from the drawing (MED, ±15-25 mm); the photo is kept as a second underlay
  and for lengths cross-checks only. Height 1446 (unladen, factory) replaces 1440.
- The drawing's scan is anisotropic (6.73 mm/px H, 6.89 V); the derived underlay is resampled to isotropic.
- A-pillar: the drawing's windscreen line is the centreline (base ~1000) while the photo's pillar foot is ~1200;
  a flat screen can't satisfy both, so ws_base_x = 1080 and pillar_w = 125 (door glass front corner ~1200 at the
  belt). B-pillar width split out as `b_pillar_w` (84).
- Interior switched to the late (2002-2015, Egyptian-assembled) spec: 4-spoke wheel with concave hub, seats with
  integrated headrests, grey cloth, tacho left / speedo right + 4 small gauges, rubber mats.

## 2026-10-17 — Factory underlay checks
- Factory side view (isotropic, `factory_side_iso.png`) overlaid at 45 % opacity: wheels, overhangs, door shut lines,
  glass, roof, boot and bumpers line up within ~1-2 %.
- Front-view widths from the factory front view (track arrows 1365 mm = 200 px): body 1628 (1620), glass base half
  width 730 (was 765), roof at the drip 630 (was 655), grille ~690 wide x 570-828 high, headlamp units |z| 362-728,
  600-790 high -> plan front corner radius reduced to 80 mm.
- Found from the overlay: the 2107 rear door glass has a **sloped trailing edge** (2934 at the belt -> 2735 at the top,
  parallel to the C-pillar) and a vertical **fixed quarter-light divider** at x = 2712. Added `rdw_top_x`/`rdw_div_x`,
  a divider channel in Trim, and a sloped C-pillar livery split (plane through three sketch points).
- Wheels: VAZ classic steel wheel = flat disc with a ring of 16 small round holes (CC0 Moscow 2025 photo), not slots.
- Light weathering added (`build_weathering.py`): seeded rust blisters on arch lips (rear worse), sills, door bottoms.
- Gotcha: bodies separated from the shell by the shut-line slits inherit the shell's **face-level** appearances, which
  override a later body-level appearance. The livery pass paints every face of the doors/bonnet/boot explicitly.
- **This is the published model (Fusion version 5).**

## 2026-10-17 — Saving guard
- All saves go through `_lib.safe_save()`, which refuses unless the document's data file lives in project
  **Eshera-Personal**, folder **Alexandria Lada Taxi**. New documents go through `safe_save_as()`, which looks the
  project up by name in `app.data.activeHub.dataProjects` and the folder by name inside it.
  `app.data.activeProject` is never used, because it follows whatever the Data panel happens to show.
- `make_2105.py` uses the same lookup for the cloud copy of the 2107 document.

## 2026-10-17 — Lettering size fix (script only)
- `place_svg()` originally built the ink box from `sketch.sketchPoints`. Those include the sketch origin, so the box
  grew by the font ascent and decals came out at 50-93 % of their specified height (Arabic worst).
- Fix: the box now comes from the sketch curves' bounding boxes. The published v5 model still has the old lettering
  size; the next rebuild picks the fix up.
- Display gotcha: decals stand 0.3 mm proud of the skin. In distant views Fusion's depth buffer drops some glyph
  pieces (alifs, dots, small numerals), so they look missing. Check lettering from close range.

## 2026-10-17 — Refinement pass (scripts only, not yet rebuilt)
Script changes made after the v5 model; a partial rebuild exists in Fusion as
"Alexandria Lada Taxi (partial refinement rebuild)" and is not published.
- **Body v2 surfacing** (`build_body.py`, `_geom.py`): lower body section with the crisp upper swage line
  (`crease_h` 780, `swage_in` 16) and the lower crease (`low_crease_h` 470); wing tops stepped `bonnet_step` (8 mm)
  below the bonnet edge; raised bonnet centre; sheet-metal edge radii (`edge_r`); rolled wheel-arch lips
  (half-tori, `lip_r` 9) joined to the shell.
- **Curved wrap-around greenhouse:** `_geom.gh_loft()` lofts between two plan sections whose screen lines follow
  `x = xc + (xk - xc) * t^n` (`screen_wrap_exp` 2.3) from the centreline stations (`ws_base_x` 1000, `ws_top_x`,
  `rs_top_x`, `rs_base_x`) to the corner stations (`ws_base_k_x` 1195, `ws_top_k_x`, `rs_top_k_x`, `rs_base_k_x`),
  trimmed by the roof crown. This resolves the flat-screen A-pillar compromise above (`pillar_w` 125 -> 48).
- **Curved screen glass** (`build_glazing.py`): windscreen and rear screen are bands between two offset greenhouse
  lofts (`_geom.screen_band`), cut to the outline; door glass stays planar.
- **Bumpers** (`build_ends.py`): rubber insert strips along the chrome bars and rubber over-riders.
- **Quarter-light divider** (`build_trim.py`): now a separate black rubber channel body ("Quarter-light divider");
  the v5 renders show the divider line, but the v5 export has no body of that name.
- **Interior/seats** (`build_interior.py`, `build_seats.py`): padded dash top roll and knee panel; seat inserts with the
  striped two-tone cloth pattern.
- Check: body names in the scripts but absent from the v5 STEP export are exactly these refinement parts
  (Arch lip, Bumper rubber strip, Over-rider, Quarter-light divider, Dash top roll, Knee panel, Seat insert, Seat stripe).
- **2105 variant switch:** parameter `variant_2105` and `OVERRIDES_2105` in `_lib.py` (applied by `param()` when
  `TARGET_DOC` ends in "2105"): 4130 mm, black pillars, flat bonnet, low flat grille, separate bumper indicators,
  tail lamps with vertical stop segments, aluminium bumpers. `make_2105.py` creates the 2105 document as a cloud copy.
