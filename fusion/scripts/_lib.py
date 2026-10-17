# Shared helpers for the Lada taxi build scripts. Each build script does
#   exec(open(LIB).read(), globals())
# at the top. Coordinates in the helpers are in MILLIMETRES (converted to Fusion cm internally).
# Frame: X along the car (0 = front bumper face, + towards the rear), Y up (0 = ground),
#        Z lateral (0 = centreline, +Z = car's right-hand side). Fusion "Front" view looks at the +Z side.
import math, os, re, tempfile
import adsk.core, adsk.fusion

DOC_NAME = globals().get('TARGET_DOC', 'Alexandria Lada Taxi')   # loader may set TARGET_DOC for the 2105 variant
IS_2105 = DOC_NAME.endswith('2105')
# Parameter values that differ on the VAZ-2105 variant document (applied by param(), so every script stays shared)
OVERRIDES_2105 = {
    'variant_2105': ('1', 'VAZ-2105 variant: low flat grille, separate bumper indicators, flat bonnet, tail lamps with vertical stop segments'),
    'len_overall': ('4130 mm', 'VAZ-2105 overall length (ru.wikipedia / auto.ru, MED)'),
    'pillars_yellow': ('0', 'Black pillars + door frames (most Alexandria cars) on the 2105 variant'),
    'bulge_h': ('0.5 mm', 'No raised bonnet centre on the 2105 (flat bonnet)'),
    'grille_bot': ('600 mm', '2105 grille: low and flat, same band as the headlamps (photos, MED)'),
    'grille_top': ('745 mm', '2105 grille top (photos, MED)'),
    'grille_hw': ('352 mm', '2105 grille spans between the headlamp units (photos, MED)'),
    'lamp_top': ('745 mm', '2105 headlamp unit top (photos, MED)'),
    'door_txt_x': ('1700 mm', 'Door lettering centre x (photos, MED)'),
}
# Paths are relative to this repo. The exec loader passes __file__ (the build script's path, in fusion/scripts/).
ROOT = os.path.dirname(os.path.abspath(__file__))                       # <repo>/fusion/scripts
REPO = os.path.normpath(os.path.join(ROOT, '..', '..')) + os.sep         # <repo>/
HERE = REPO                                                              # kept for older call sites

app = adsk.core.Application.get()

def activate():
    doc = [d for d in app.documents if d.name == DOC_NAME][0]
    doc.activate()
    return doc, adsk.fusion.Design.cast(app.activeProduct)

doc, design = activate()
root = design.rootComponent
um = design.unitsManager
tbm = adsk.fusion.TemporaryBRepManager.get()
V3 = adsk.core.Vector3D.create
VI = adsk.core.ValueInput.createByReal
NEW = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
JOIN = adsk.fusion.FeatureOperations.JoinFeatureOperation
CUT = adsk.fusion.FeatureOperations.CutFeatureOperation
INTERSECT = adsk.fusion.FeatureOperations.IntersectFeatureOperation

def P(x, y, z=0.0):
    """Point from mm."""
    return adsk.core.Point3D.create(x / 10.0, y / 10.0, z / 10.0)

def ev(expr):
    """Evaluate a length expression/parameter -> mm."""
    return um.evaluateExpression(expr, 'cm') * 10.0

def evu(expr):
    return um.evaluateExpression(expr, '')

def evdeg(expr):
    return math.degrees(um.evaluateExpression(expr, 'rad'))

def param(name, expr, unit, comment, update=False):
    if IS_2105 and name in OVERRIDES_2105:
        expr, comment = OVERRIDES_2105[name]
        update = True
    up = design.userParameters
    p = up.itemByName(name)
    if p is None:
        up.add(name, adsk.core.ValueInput.createByString(expr), unit, comment)
    elif update:
        p.expression = expr
        p.comment = comment
    return up.itemByName(name)

def base_name(n):
    return re.sub(r'( \(\d+\))+$', '', n)

def get_comp(name, parent=None, create=True):
    parent = parent or root
    for o in parent.occurrences:
        if o.component.name == name:
            return o.component
    if not create:
        return None
    occ = parent.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = name
    return occ.component

def get_occ(name):
    for o in root.occurrences:
        if o.component.name == name:
            return o
    return None

def wipe(c):
    f = c.features
    for coll in (f.circularPatternFeatures, f.rectangularPatternFeatures, f.splitFaceFeatures, f.splitBodyFeatures, f.mirrorFeatures, f.filletFeatures, f.chamferFeatures,
                 f.shellFeatures, f.combineFeatures, f.loftFeatures, f.revolveFeatures, f.sweepFeatures,
                 f.extrudeFeatures, f.patchFeatures, f.thickenFeatures, f.baseFeatures):
        for i in range(coll.count - 1, -1, -1):
            try:
                coll.item(i).deleteMe()
            except Exception:
                pass
    for i in range(c.sketches.count - 1, -1, -1):
        c.sketches.item(i).deleteMe()
    for i in range(c.constructionPlanes.count - 1, -1, -1):
        c.constructionPlanes.item(i).deleteMe()
    for i in range(c.constructionAxes.count - 1, -1, -1):
        c.constructionAxes.item(i).deleteMe()
    for i in range(c.bRepBodies.count - 1, -1, -1):
        c.bRepBodies.item(i).deleteMe()

def delete_comp(name):
    for o in [o for o in root.occurrences if o.component.name == name][::-1]:
        o.deleteMe()

def offset_plane(c, base, d_mm, name=None):
    pi = c.constructionPlanes.createInput()
    pi.setByOffset(base, VI(d_mm / 10.0))
    p = c.constructionPlanes.add(pi)
    p.isLightBulbOn = False
    if name:
        p.name = name
    return p

# ---------------------------------------------------------------- temporary B-rep primitives (mm)
def tbox(cx, cy, cz, lx, ly, lz, xd=(1, 0, 0), yd=(0, 1, 0)):
    ob = adsk.core.OrientedBoundingBox3D.create(P(cx, cy, cz), V3(*xd), V3(*yd), lx / 10, ly / 10, lz / 10)
    return tbm.createBox(ob)

def tcyl(p0, p1, r0, r1=None):
    """Cylinder / cone between two (x,y,z) mm points."""
    r1 = r0 if r1 is None else r1
    return tbm.createCylinderOrCone(P(*p0), r0 / 10, P(*p1), r1 / 10)

def tsphere(c, r):
    return tbm.createSphere(P(*c), r / 10)

def ttorus(c, axis, R, r):
    t = tbm.createTorus(P(0, 0, 0), V3(*axis), R / 10, r / 10)   # centre argument is ignored: translate after
    tbm.transform(t, mat_tr(*c))
    return t

def tpipe(pts, r, closed=False):
    """Tube through a polyline of mm points: cylinders + spheres at the joints, unioned."""
    body = None
    segs = list(zip(pts, pts[1:])) + ([(pts[-1], pts[0])] if closed else [])
    for a, b in segs:
        c = tcyl(a, b, r)
        if body is None:
            body = c
        else:
            tbm.booleanOperation(body, c, adsk.fusion.BooleanTypes.UnionBooleanType)
    for p in (pts if closed else pts[1:-1]):
        tbm.booleanOperation(body, tsphere(p, r), adsk.fusion.BooleanTypes.UnionBooleanType)
    return body

def tunion(a, b):
    tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.UnionBooleanType)
    return a

def tsub(a, b):
    tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)
    return a

def tmove(body, m):
    tbm.transform(body, m)
    return body

def mat_rot(axis, deg, origin=(0, 0, 0)):
    m = adsk.core.Matrix3D.create()
    m.setToRotation(math.radians(deg), V3(*axis), P(*origin))
    return m

def mat_tr(dx, dy, dz):
    m = adsk.core.Matrix3D.create()
    m.translation = V3(dx / 10, dy / 10, dz / 10)
    return m

def mirror_z(body):
    """Return a mirrored copy (z -> -z) of a temporary body."""
    b = tbm.copy(body)
    m = adsk.core.Matrix3D.create()
    m.setCell(2, 2, -1)
    tbm.transform(b, m)
    return b

def commit(c, parts, feature_name):
    """parts: list of (name, tempBody, appearance or None). One base feature per call."""
    bf = c.features.baseFeatures.add()
    bf.name = feature_name
    bf.startEdit()
    for name, b, ap in parts:
        rb = c.bRepBodies.add(b, bf)
        rb.name = name
        if ap is not None:
            try:
                rb.appearance = ap
            except Exception:
                pass
    bf.finishEdit()
    # body references can change after finishEdit: re-apply by order of the feature's bodies
    bodies = [bb for bb in bf.bodies]
    if len(bodies) == len(parts):
        for (name, b, ap), bb in zip(parts, bodies):
            if ap is not None and (bb.appearance is None or bb.appearance.name != ap.name):
                bb.appearance = ap
    return bodies

# ---------------------------------------------------------------- sketch helpers (mm)
def sk_poly(sk, pts, closed=True):
    L = sk.sketchCurves.sketchLines
    ls = []
    n = len(pts)
    for i in range(n if closed else n - 1):
        a, b = pts[i], pts[(i + 1) % n]
        ls.append(L.addByTwoPoints(P(a[0], a[1]) if not ls else ls[-1].endSketchPoint, P(b[0], b[1])))
    if closed and ls:
        # close exactly
        ls[-1].endSketchPoint.merge(ls[0].startSketchPoint)
    return ls

def sk_spline(sk, pts):
    oc = adsk.core.ObjectCollection.create()
    for p in pts:
        oc.add(P(p[0], p[1]))
    return sk.sketchCurves.sketchFittedSplines.add(oc)

def sk_rrect(sk, x0, y0, x1, y1, r):
    L, A = sk.sketchCurves.sketchLines, sk.sketchCurves.sketchArcs
    c = [P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)]
    ls = [L.addByTwoPoints(c[i], c[(i + 1) % 4]) for i in range(4)]
    if r > 0:
        for i in range(4):
            a, b = ls[i], ls[(i + 1) % 4]
            A.addFillet(a, a.endSketchPoint.geometry, b, b.startSketchPoint.geometry, r / 10)
    return ls

def extrude(c, prof, d0_mm, d1_mm, op=NEW, name=None, participants=None):
    """Extrude profile(s) from offset d0 to d1 (mm, along sketch normal)."""
    ei = c.features.extrudeFeatures.createInput(prof, op)
    start = adsk.fusion.OffsetStartDefinition.create(VI(d0_mm / 10))
    ei.startExtent = start
    ei.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI((d1_mm - d0_mm) / 10)),
                        adsk.fusion.ExtentDirections.PositiveExtentDirection)
    if participants is None and op in (CUT, INTERSECT):
        participants = list(c.bRepBodies)     # never let a cut reach other components (e.g. the wheels)
    if participants is not None:
        ei.participantBodies = participants
    f = c.features.extrudeFeatures.add(ei)
    if name:
        f.name = name
        if op == NEW:
            for b in f.bodies:
                b.name = name
    return f

def profiles(sk, pick=None):
    oc = adsk.core.ObjectCollection.create()
    for i in range(sk.profiles.count):
        pr = sk.profiles.item(i)
        if pick is None or pick(pr):
            oc.add(pr)
    return oc

def largest_profile(sk):
    best = None
    for i in range(sk.profiles.count):
        pr = sk.profiles.item(i)
        a = pr.areaProperties().area
        if best is None or a > best[0]:
            best = (a, pr)
    return best[1]

# ---------------------------------------------------------------- appearances
_lib_apps = None
def lib_app(name, new_name=None):
    global _lib_apps
    a = design.appearances.itemByName(new_name or name)
    if a:
        return a
    if _lib_apps is None:
        _lib_apps = app.materialLibraries.itemByName('Fusion Appearance Library')
    src = _lib_apps.appearances.itemByName(name)
    return design.appearances.addByCopy(src, new_name or name)

def color_app(name, base, rgb, gloss=None):
    """Custom appearance copied from library `base` with colour rgb (0-255)."""
    a = design.appearances.itemByName(name)
    if a is None:
        a = lib_app(base, name)
    for i in range(a.appearanceProperties.count):
        p = a.appearanceProperties.item(i)
        if isinstance(p, adsk.core.ColorProperty):
            pid = p.id.lower()
            if 'color' in pid or 'albedo' in pid or 'diffuse' in pid:
                try:
                    p.value = adsk.core.Color.create(rgb[0], rgb[1], rgb[2], 255)
                except Exception:
                    pass
    return a

def set_view(target_mm, eye_dir, extent_mm, ortho=True):
    """Point the camera at target (mm) from direction eye_dir, showing ~extent_mm."""
    vp = app.activeViewport
    cam = vp.camera
    cam.isFitView = False
    cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType if ortho else adsk.core.CameraTypes.PerspectiveCameraType
    t = P(*target_mm)
    d = V3(*eye_dir); d.normalize(); d.scaleBy(1000)
    e = t.copy(); e.translateBy(d)
    cam.target = t
    cam.eye = e
    cam.upVector = V3(0, 1, 0)
    cam.viewExtents = extent_mm / 10
    vp.camera = cam
    vp.refresh()

# ---------------------------------------------------------------- SVG lettering (CoreText outlines, see ../lettering)
SVG_DIR = os.path.join(REPO, 'tools', 'lettering', 'svg') + os.sep
PX_PER_MM = 3.7795275591      # Fusion reads SVG user units as 96-dpi px

def place_svg(c, plane, svg, cx, by, h, depth, name, ap=None):
    """Import an SVG onto `plane`, scaled so the ink is h mm tall, ink-box centre at sketch x=cx, bottom y=by (mm);
    extrude glyph regions (holes dropped) by depth mm along the sketch normal. Returns bodies."""
    sk = c.sketches.add(plane)
    sk.importSVG(SVG_DIR + svg, 0, 0, PX_PER_MM)
    bbs = [cv.boundingBox for cv in sk.sketchCurves]   # not sketchPoints: those include the sketch origin
    x0, y0 = min(b.minPoint.x for b in bbs), min(b.minPoint.y for b in bbs)
    x1, y1 = max(b.maxPoint.x for b in bbs), max(b.maxPoint.y for b in bbs)
    sk.deleteMe()
    s = (h / 10.0) / (y1 - y0)
    sk = c.sketches.add(plane); sk.name = name
    sk.isComputeDeferred = True
    sk.importSVG(SVG_DIR + svg, cx / 10.0 - s * (x0 + x1) / 2, by / 10.0 - s * y0, PX_PER_MM * s)
    sk.isComputeDeferred = False
    def key(loop):
        pts = []
        for cv in loop.profileCurves:
            b = cv.boundingBox; pts += [b.minPoint, b.maxPoint]
        return (round(min(p.x for p in pts), 3), round(min(p.y for p in pts), 3),
                round(max(p.x for p in pts), 3), round(max(p.y for p in pts), 3))
    holes = set()
    for i in range(sk.profiles.count):
        for lp in sk.profiles.item(i).profileLoops:
            if not lp.isOuter:
                holes.add(key(lp))
    profs = adsk.core.ObjectCollection.create()
    for i in range(sk.profiles.count):
        pr = sk.profiles.item(i)
        outer = [lp for lp in pr.profileLoops if lp.isOuter][0]
        if key(outer) not in holes:
            profs.add(pr)
    ei = c.features.extrudeFeatures.createInput(profs, NEW)
    ei.setDistanceExtent(False, VI(depth / 10.0))
    f = c.features.extrudeFeatures.add(ei); f.name = name
    for b in f.bodies:
        b.name = name
        if ap: b.appearance = ap
    sk.isVisible = False
    return list(f.bodies)

def ghost(opacity=1.0, names=('Body',)):
    """Set occurrence opacity (for underlay comparisons)."""
    for o in root.occurrences:
        if o.component.name in names:
            o.opacity = opacity

# ---------------------------------------------------------------- planar plates from 3D polygons (mm)
def fillet_poly(pts, r, n=5):
    """Round every corner of a closed 2D polygon with radius r (list or scalar), n points per corner."""
    out = []
    N = len(pts)
    rs = r if isinstance(r, (list, tuple)) else [r] * N
    for i in range(N):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % N]
        ri = rs[i]
        if ri <= 0:
            out.append(p1); continue
        a = (p0[0] - p1[0], p0[1] - p1[1]); b = (p2[0] - p1[0], p2[1] - p1[1])
        la, lb = math.hypot(*a), math.hypot(*b)
        a = (a[0] / la, a[1] / la); b = (b[0] / lb, b[1] / lb)
        cosang = max(-1.0, min(1.0, a[0] * b[0] + a[1] * b[1]))
        ang = math.acos(cosang)
        d = min(ri / math.tan(ang / 2), la * 0.45, lb * 0.45)
        t1 = (p1[0] + a[0] * d, p1[1] + a[1] * d); t2 = (p1[0] + b[0] * d, p1[1] + b[1] * d)
        # quadratic Bezier through the corner approximates the arc well enough for trim/glass outlines
        for k in range(n + 1):
            t = k / n
            out.append(((1 - t) ** 2 * t1[0] + 2 * (1 - t) * t * p1[0] + t * t * t2[0],
                        (1 - t) ** 2 * t1[1] + 2 * (1 - t) * t * p1[1] + t * t * t2[1]))
    return out

def plate3d(c, outer, t, name, holes=(), ap=None, spline=False):
    """Planar polygon(s) given as 3D mm points -> sketch on a plane through the outer polygon, extruded by t mm
    (signed, along the plane normal from the first three points). holes: inner 3D polygons (same plane)."""
    sk0 = c.sketches.add(c.xYConstructionPlane)
    sk0.isComputeDeferred = True
    n = len(outer)
    i1, i2 = n // 3, (2 * n) // 3
    sp = [sk0.sketchPoints.add(P(*outer[i])) for i in (0, i1, i2)]
    sk0.isVisible = False
    pi = c.constructionPlanes.createInput()
    pi.setByThreePoints(sp[0], sp[1], sp[2])
    pl = c.constructionPlanes.add(pi); pl.isLightBulbOn = False
    sk = c.sketches.add(pl); sk.name = name
    sk.isComputeDeferred = True
    for poly in [outer] + list(holes):
        q = [sk.modelToSketchSpace(P(*p)) for p in poly]
        if spline:
            oc = adsk.core.ObjectCollection.create()
            for p in q + [q[0]]:
                oc.add(p)
            s = sk.sketchCurves.sketchFittedSplines.add(oc); s.isClosed = True
        else:
            L = sk.sketchCurves.sketchLines
            first = prev = None
            for k in range(len(q)):
                a = prev.endSketchPoint if prev else q[k]
                prev = L.addByTwoPoints(a, q[(k + 1) % len(q)] if k < len(q) - 1 else first.startSketchPoint)
                if first is None:
                    first = prev
    sk.isComputeDeferred = False
    sk0.isComputeDeferred = False
    prof = adsk.core.ObjectCollection.create()
    best = None
    for i in range(sk.profiles.count):
        pr = sk.profiles.item(i)
        if pr.profileLoops.count == 1 + len(holes) or (best is None and not holes):
            prof.add(pr)
    if prof.count == 0:
        prof.add(largest_profile(sk))
    ei = c.features.extrudeFeatures.createInput(prof, NEW)
    ei.setSymmetricExtent(VI(abs(t) / 10.0), True)        # centred on the given points, total thickness |t|
    f = c.features.extrudeFeatures.add(ei); f.name = name
    for b in f.bodies:
        b.name = name
        if ap: b.appearance = ap
    sk.isVisible = False
    return list(f.bodies)

SNAP_DIR = globals().get('SNAP_DIR') or os.path.join(tempfile.gettempdir(), 'alexandria-lada-taxi-snaps') + os.sep   # loader may override

def snap(name, view=None, w=1400, h=800, folder=None):
    """Activate our doc, set the view (target_mm, eye_dir, extent_mm[, ortho]) and save a screenshot in the same call
    (atomic even if the active document changes between API calls). Returns the file path."""
    activate()
    if view:
        set_view(*view)
    folder = folder or SNAP_DIR
    os.makedirs(folder, exist_ok=True)
    path = folder + name + '.png'
    app.activeViewport.saveAsImageFile(path, w, h)
    return path

# ---------------------------------------------------------------- saving (guarded)
# The model lives in Fusion project PROJECT_NAME, folder FOLDER_NAME. Saves never go to app.data.activeProject:
# the project is looked up by name in the active hub, and a version save is refused unless the document already
# lives in that project + folder.
PROJECT_NAME = 'Eshera-Personal'
FOLDER_NAME = 'Alexandria Lada Taxi'

def model_folder():
    """The FOLDER_NAME data folder of PROJECT_NAME, looked up by name in the ACTIVE HUB (never the active project)."""
    projs = [p for p in app.data.activeHub.dataProjects if p.name == PROJECT_NAME]
    if not projs:
        raise RuntimeError('%s project not found in the active hub' % PROJECT_NAME)
    folder = projs[0].rootFolder.dataFolders.itemByName(FOLDER_NAME)
    if folder is None:
        raise RuntimeError('folder %r not found in project %s' % (FOLDER_NAME, PROJECT_NAME))
    return folder

def safe_save(message):
    """Save a new version only if this document already lives in PROJECT_NAME / FOLDER_NAME; otherwise refuse."""
    d, _ = activate()
    df = d.dataFile
    if df is None or df.parentProject.name != PROJECT_NAME or df.parentFolder.name != FOLDER_NAME:
        raise RuntimeError('refusing to save: %s is not in %s / %s' % (d.name, PROJECT_NAME, FOLDER_NAME))
    return d.save(message)

def safe_save_as(d, name, description):
    """saveAs into PROJECT_NAME / FOLDER_NAME (found by name), never the active project."""
    return d.saveAs(name, model_folder(), description, '')
