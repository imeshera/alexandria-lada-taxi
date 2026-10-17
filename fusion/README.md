# Fusion build scripts

The model is generated entirely by the Python scripts in [`scripts/`](scripts/), run inside Autodesk Fusion against
an open document named **Alexandria Lada Taxi** (Fusion project **Eshera-Personal**, folder **Alexandria Lada Taxi**).
Every dimension is a Fusion user parameter, written by `build_params.py` and the per-subsystem `PARAMS` tables, so
the usual loop is: change a parameter, re-run the affected scripts.

## Exec loader
The scripts are not Fusion add-ins; they are plain modules with a `run(context)` function, executed by a tiny
loader. Run it from Fusion's *Scripts and Add-Ins* (as a one-off script), the Text Commands Python prompt, or any
tool that can execute Python inside Fusion. The loader must pass `__file__`, because every script finds `_lib.py`,
`_geom.py`, `canvases.cfg` and the lettering SVGs relative to its own location:

```python
def run(_context: str):
    path = '<repo>/fusion/scripts/<script>.py'          # e.g. .../alexandria-lada-taxi/fusion/scripts/build_body.py
    ns = {'__name__': 'fusion_script', '__file__': path}
    # optional: ns['TARGET_DOC'] = 'Alexandria Lada Taxi 2105'   (build the 2105 variant document instead)
    exec(compile(open(path).read(), path, 'exec'), ns)
    ns['run'](_context)
```

Every script first execs `_lib.py`, which activates the target document **by name** (`TARGET_DOC`, default
`Alexandria Lada Taxi`) and provides millimetre-based helpers. Paths inside the repo:
`ROOT` = `fusion/scripts/`, `REPO` = repo root, `SVG_DIR` = `tools/lettering/svg/`.

## Build order
Start from an empty Fusion design named **Alexandria Lada Taxi** (Hybrid design intent), saved in the project/folder
above (or edit `PROJECT_NAME` / `FOLDER_NAME` in `_lib.py` to match your own). Then run:

| # | Script | Builds |
|---|---|---|
| 1 | `build_params.py` | Master parameter table: overall dimensions, stations, heights, widths, screen wrap, swage lines |
| 2 | `build_body.py` | Body shell: lower body (side ∩ plan ∩ swage-line section), lofted wrap-around greenhouse, wheel arches, fillets, 3 mm shell, arch lips |
| 3 | `build_openings.py` | Side glass, windscreen and rear-screen openings; shut-line slits that separate doors, bonnet and boot lid |
| 4 | `build_glazing.py` | Curved windscreen and rear screen, planar door glass |
| 5 | `build_trim.py` | Window chrome, screen rubbers, belt mouldings, drip rails, handles, rubbing strips, mirrors, wipers, quarter-light divider, C-pillar vents, fuel flap |
| 6 | `build_ends.py` | Grille + badge, headlamp units, bonnet bulge, tail lamps, wrap-around bumpers with rubber strips and over-riders |
| 7 | `build_wheels.py` | 175/70 R13 tyre, 5J×13 steel wheel, hubcap, nuts, brake disc; places the 4 instances |
| 8 | `build_plates.py` | Egyptian taxi plates, front + rear |
| 9 | `build_roof.py` | Tubular roof rack and roof light ("TAXI" / "للأجرة") |
| 10 | `build_lettering.py` | Plate number on both front doors |
| 11 | `build_chassis.py` | Suspension, axle, drivetrain, exhaust (schematic, dimensionally placed) |
| 12 | `build_seats.py` | Front seats (2 instances) and rear bench |
| 13 | `build_interior.py` | Dashboard, steering wheel, pedals, levers, door cards, mats, headliner, visors, mirror + prayer beads |
| 14 | `build_weathering.py` | Seeded rust blisters and scuffs |
| 15 | `build_appearance.py` | Two-tone livery split on the shut lines, weathered paints, all materials (run last, after any body rebuild) |
| - | `build_canvases.py` + `canvases.cfg` | Optional calibrated underlays (needs the local reference images, see `references/SOURCES.md`) |
| - | `snap.py`, `view.py` | Screenshots / camera presets: set `SHOTS` or `VIEW` in the loader namespace |
| - | `make_2105.py` | Cloud copy of the document as "Alexandria Lada Taxi 2105"; then run 1-15 with `TARGET_DOC` set |

Shared modules: `_lib.py` (document activation, mm helpers, temporary B-rep primitives, `plate3d`, `place_svg`,
appearances, `snap`, guarded saving) and `_geom.py` (outlines shared by the openings, glass and trim).

## Saving
Scripts never save implicitly. Save from the loader with `safe_save('message')` (from `_lib.py`): it refuses unless
the document's data file lives in project `PROJECT_NAME` and folder `FOLDER_NAME`. New documents go through
`safe_save_as()`, which looks the project up by name in the active hub (never `app.data.activeProject`).

## Gotchas worth knowing before editing
See [`../docs/BUILD-LOG.md`](../docs/BUILD-LOG.md). The important ones: occurrence moves don't persist (instances
are created with `addExistingComponent(comp, matrix)` from a hidden master); cut extrudes must set
`participantBodies`; bodies split off the shell inherit face-level appearances; re-running an early script
recomputes everything after it, so long scripts can take minutes.
