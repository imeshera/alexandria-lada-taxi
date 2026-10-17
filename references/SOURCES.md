# Reference sources

The reference images used to build this model are **not** included in the repository: most are third-party photos
(Wikimedia Commons CC BY / BY-SA, some CC0 / public domain) or copyrighted press and manual material used as a
private modelling reference only. Instead, every image is listed with its source URL, author and licence in a
`MANIFEST.csv` per category:

| Manifest | Contents |
|---|---|
| [`sources/drawings/MANIFEST.csv`](sources/drawings/MANIFEST.csv) | Factory dimensioned 4-view and repair-manual 3-view (primary dimension source) |
| [`sources/derived/MANIFEST.csv`](sources/derived/MANIFEST.csv) | Underlay images derived from the drawings and the 2006 side photo (crop, isotropic resample, mirror) used by `build_canvases.py` |
| [`sources/livery/MANIFEST.csv`](sources/livery/MANIFEST.csv) | ~35 dated Alexandria taxi photos used for the livery map |
| [`sources/plates/MANIFEST.csv`](sources/plates/MANIFEST.csv) | Egyptian plate diagrams and photos |
| [`sources/exterior/MANIFEST.csv`](sources/exterior/MANIFEST.csv) | Exterior detail photos (ends, lamps, wheels, boot, cutaway) |
| [`sources/interior/MANIFEST.csv`](sources/interior/MANIFEST.csv) | Dashboard, seats, door cards, console |

To rebuild the calibrated underlays, download the listed images into `references/images/<category>/` (the folder is
gitignored) and recreate the files in `derived/` as described in its manifest and in
[`notes/lada-dossier.md`](notes/lada-dossier.md) (Underlays). The model geometry itself does not need the images:
every dimension is in `fusion/scripts/build_params.py`.

Further sources (factory figures, Wikipedia, Sketchfab models consulted) are cited inline in
[`notes/vaz2107-specs.md`](notes/vaz2107-specs.md) and [`notes/livery-and-plates.md`](notes/livery-and-plates.md).
