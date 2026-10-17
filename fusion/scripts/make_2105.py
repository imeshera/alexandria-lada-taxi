# Creates the "Alexandria Lada Taxi 2105" design as a cloud copy of the 2107 document, in the Fusion project
# 'Eshera-Personal', folder 'Alexandria Lada Taxi' (looked up by name in the active hub - never the active project),
# renames and opens it.
# Then rebuild it with the normal scripts and TARGET_DOC = 'Alexandria Lada Taxi 2105' set in the loader namespace:
# _lib.param() applies OVERRIDES_2105 (variant_2105 = 1, black pillars, flat bonnet, 2105 grille/lamps, 4130 mm).
import adsk.core, adsk.fusion

SRC, DST = 'Alexandria Lada Taxi', 'Alexandria Lada Taxi 2105'
PROJECT_NAME, FOLDER_NAME = 'Eshera-Personal', 'Alexandria Lada Taxi'

def run(_context: str):
    app = adsk.core.Application.get()
    if [d for d in app.documents if d.name == DST]:
        print('already open'); return
    proj = [p for p in app.data.activeHub.dataProjects if p.name == PROJECT_NAME][0]
    folder = proj.rootFolder.dataFolders.itemByName(FOLDER_NAME)
    assert folder is not None, 'folder %r not found in %s' % (FOLDER_NAME, PROJECT_NAME)
    existing = [f for f in folder.dataFiles if f.name == DST]
    if existing:
        df = existing[0]
    else:
        src = [d for d in app.documents if d.name == SRC][0].dataFile
        assert src.parentProject.name == PROJECT_NAME and src.parentFolder.name == FOLDER_NAME
        df = src.copy(folder)
        df.name = DST
    doc = app.documents.open(df, True)
    print('opened', doc.name, df.parentProject.name, df.parentFolder.name)
