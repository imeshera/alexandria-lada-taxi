# Calibrated reference underlays (component "Underlays"), one canvas per entry in CANVASES.
# Each underlay image is pre-oriented (references/images/derived/) so that, seen from the view the plane faces,
# image-right = model +X (side, top) or image-right = model +Z (front, seen from -X ... see notes).
# Calibration: mm_per_px and the pixel (u0, v0) (from the image's top-left) that lands on the model origin
# point (x = 0 front bumper face, y = 0 ground). See references/notes/lada-dossier.md (Underlays).
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())

DER = os.path.join(REPO, 'references', 'images', 'derived') + os.sep   # local only (gitignored)
# name, file, plane ('side' | 'front' | 'top'), plane offset mm, mm_per_px, u0 px, v0 px (from top), img w, img h
CANVASES = []
try:
    exec(open(os.path.join(ROOT, 'canvases.cfg')).read())   # defines CANVASES (kept next to this script)
except FileNotFoundError:
    pass

def run(_context: str):
    C = get_comp('Underlays')
    for i in range(C.canvases.count - 1, -1, -1):
        C.canvases.item(i).deleteMe()
    for i in range(C.constructionPlanes.count - 1, -1, -1):
        C.constructionPlanes.item(i).deleteMe()
    for name, fn, kind, off, s, u0, v0, iw, ih in CANVASES:
        base = {'side': C.xYConstructionPlane, 'front': C.yZConstructionPlane, 'top': C.xZConstructionPlane}[kind]
        pl = offset_plane(C, base, off, 'Underlay plane ' + name)
        ci = C.canvases.createInput(DER + fn, pl)
        W, H = iw * s / 10.0, ih * s / 10.0          # image size in cm
        uo, vo = u0 / iw, 1.0 - v0 / ih              # normalised origin, v from the bottom
        m = adsk.core.Matrix2D.create()
        if kind == 'front':
            # YZ plane: canvas U = +Y, V = +Z. Image rows -> Y, image columns -> +Z (viewer's right seen from ahead)
            m.setCell(0, 0, 0); m.setCell(0, 1, H); m.setCell(0, 2, -H * vo)
            m.setCell(1, 0, W); m.setCell(1, 1, 0); m.setCell(1, 2, -W * uo)
        else:
            m.setCell(0, 0, W); m.setCell(0, 2, -W * uo)
            m.setCell(1, 1, H); m.setCell(1, 2, -H * vo)
        ci.transform = m
        ci.opacity = 50
        ci.isDisplayedThrough = False
        cv = C.canvases.add(ci)
        cv.name = name
    print('canvases:', C.canvases.count)
