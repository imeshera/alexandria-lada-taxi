# Camera helper: set VIEW = (target_mm, eye_dir, extent_mm[, ortho]) in the loader before exec.
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lib.py')).read(), globals())
def run(_context: str):
    set_view(*VIEW)
