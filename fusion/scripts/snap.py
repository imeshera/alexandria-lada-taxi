# Screenshot helper: loader sets SHOTS = [(name, view, w, h), ...]; optional FOLDER and HIDE (component names hidden
# for the shots, restored afterwards).
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())
def run(_context: str):
    hide = globals().get('HIDE', ())
    masters = {'Wheel:1', 'Plate:1', 'Front seat:1'}
    hidden = []
    for o in root.occurrences:
        if o.component.name in hide and o.isLightBulbOn:
            o.isLightBulbOn = False; hidden.append(o)
    hb = []
    for o in root.occurrences:
        for b in o.component.bRepBodies:
            if base_name(b.name) in globals().get('HIDE_BODIES', ()) and b.isLightBulbOn:
                b.isLightBulbOn = False; hb.append(b)
    for name, view, w, h in SHOTS:
        print(snap(name, view, w, h, globals().get('FOLDER')))
    for o in hidden:
        o.isLightBulbOn = True
    for b in hb:
        b.isLightBulbOn = True
