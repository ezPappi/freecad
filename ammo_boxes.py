# -*- coding: utf-8 -*-
"""
Ammunisjonsboks v2.3 for FreeCAD 1.x
"""

import FreeCAD as App
import Part
import os

V = App.Vector

# ----------------------------------------------------------------------------
# BRUKERVALG
# ----------------------------------------------------------------------------
CALIBER = "22LR"       # 22LR, 9MM, 357MAG, 38SPL, 40SW, 45ACP, 10MM, 223, 6.5X55
LID_TEXT = "AUTO"      # "AUTO" = kalibernavn, ellers valgfri tekst
TEXT_DEPTH = 0.8       # Dybde på innfrest tekst
TEXT_SIZE = 10.0       # Tekststørrelse
FONT_FILE = ""         # Full sti til .ttf, tom = auto

BOX_OVERRIDE = None        # (lengde, bredde, høyde) på originaleska
HOLE_D_OVERRIDE = None     # Hulldiameter
NUM_HOLES_OVERRIDE = None  # Antall hull per rad; None = auto

# 1. Eskerom (50 skudd)
POCKETS_IN_CAVITY = True
CAVITY_FLOOR_RAISE = 13.0  # Hev bunnen i eskerommet (for bruk uten/med CCI-ramme)
POCKET_DEPTH = 13.0        # Dybde på de LAVE radene i eskerommet
STAGGER = 3.0              # Hvor mye høyere hver annen rad står
RAISED_ROW_PARITY = 1      # 1 = rad 2, 4, ... står høyest; 0 = rad 1, 3, 5, ...

# 2. Den 6. ekstra raden (10 skudd)
# Hvor mange mm av patronen som skal stikke opp over sin indre hylle:
STRIP_EXPOSED_HEIGHT = 2.0 

# Fileter / faser
OUTER_FILLET = 3.0         # Avrunding på lukkede hjørner
EDGE_CHAMFER = 0.8         # Fase topp/bunn
HOLE_CHAMFER = 0.6         # Innløpsfase på hull
LID_CHAMFER = 0.6          # Fase på toppen av lokket

# Lokkets "klikk"
BUMP_R = 0.6               # Bule i sporet
DIMPLE_R = 0.8             # Fordypning i lokkskinnen
BUMP_X_FROM_END = 8.0      # Avstand fra lukket ende

LAYOUT = "print"           # "print" = lokk flatt ved siden av, "assembled" = montert
EXPORT_DIR = ""            # Sti for STL-eksport, tom = ingen

# ----------------------------------------------------------------------------
# KALIBERTABELL (mm)
# ----------------------------------------------------------------------------
CALIBERS = {
    "22LR":   dict(label="22LR",    rim=7.1,   oal=25.4, hole_d=6.2,  box=(98.0, 48.0, 26.0),  box_est=False),
    "9MM":    dict(label="9MM",     rim=9.96,  oal=29.7, hole_d=None, box=(118.0, 62.0, 34.0), box_est=True),
    "357MAG": dict(label="357 MAG", rim=11.18, oal=40.4, hole_d=None, box=(125.0, 63.0, 40.0), box_est=True),
    "38SPL":  dict(label="38 SPL", rim=11.2,  oal=39.4, hole_d=None, box=(125.0, 63.0, 40.0), box_est=True),
    "40SW":   dict(label="40 S&W", rim=10.8,  oal=28.8, hole_d=None, box=(118.0, 62.0, 34.0), box_est=True),
    "45ACP":  dict(label="45 ACP", rim=12.2,  oal=32.4, hole_d=None, box=(125.0, 68.0, 38.0), box_est=True),
    "10MM":   dict(label="10MM",    rim=10.8,  oal=32.0, hole_d=None, box=(120.0, 62.0, 36.0), box_est=True),
    "223":    dict(label="223 REM", rim=9.6,   oal=57.4, hole_d=None, box=(150.0, 70.0, 64.0), box_est=True),
    "6.5X55": dict(label="6.5x55",  rim=12.2,  oal=80.0, hole_d=12.6, box=(165.0, 85.0, 85.0), box_est=True),
}

if CALIBER not in CALIBERS:
    raise ValueError("Ukjent kaliber '%s'." % CALIBER)
C = CALIBERS[CALIBER]

if LID_TEXT.strip().upper() == "AUTO":
    LID_TEXT = C["label"]

# ----------------------------------------------------------------------------
# PARAMETERE OG GEOMETRIBASIS
# ----------------------------------------------------------------------------
WALL_T = 3.0
DIVIDER_T = 1.5
BOTTOM_T = 2.0
LID_THICKNESS = 4.0
CLEARANCE = 0.25
GROOVE_W = 1.6
RAIL_H = 2.2

GRIP_R = 8.0
GRIP_DEPTH = 1.2

CCI_LENGTH, CCI_WIDTH, CCI_HEIGHT = BOX_OVERRIDE if BOX_OVERRIDE else C["box"]

HOLE_D = HOLE_D_OVERRIDE or C["hole_d"] or round(C["rim"] + 0.4, 1)
PITCH = HOLE_D + 3.0
EXTRA_WIDTH = HOLE_D + 2.0

NUM_COLS = NUM_HOLES_OVERRIDE or int((CCI_LENGTH - HOLE_D) / PITCH + 1e-6) + 1
NUM_ROWS = int((CCI_WIDTH - HOLE_D) / PITCH + 1e-6) + 1

# Beregn effektiv gulvhøyde i eskerommet
FLOOR_Z = BOTTOM_T + CAVITY_FLOOR_RAISE

MIN_FLOOR_UNDER_POCKET = 1.5
_max_depth = FLOOR_Z - MIN_FLOOR_UNDER_POCKET
if POCKET_DEPTH > _max_depth:
    POCKET_DEPTH_E = max(_max_depth, 2.0)
    App.Console.PrintWarning(
        "POCKET_DEPTH %.1f mm er justert til %.1f mm basert på CAVITY_FLOOR_RAISE.\n"
        % (POCKET_DEPTH, POCKET_DEPTH_E))
else:
    POCKET_DEPTH_E = POCKET_DEPTH

RAISED_DEPTH = max(POCKET_DEPTH_E - STAGGER, 2.0)

# Dybde og nedsenking for den 6. raden
STRIP_HOLE_DEPTH = max(C["oal"] - STRIP_EXPOSED_HEIGHT, 5.0)
STRIP_STEP_DOWN = STRIP_EXPOSED_HEIGHT + 0.5  # Senk skillevegg og hylle slik at lokket går over

CAV_H = max(CCI_HEIGHT - CAVITY_FLOOR_RAISE + 1.0, C["oal"] - RAISED_DEPTH + 1.0)
HOLE_DEPTH = round(C["oal"] + LID_THICKNESS + 0.5, 1)

OUTER_L = CCI_LENGTH + 2 * WALL_T
INNER_W = CCI_WIDTH + DIVIDER_T + EXTRA_WIDTH
OUTER_W = INNER_W + 2 * WALL_T
OUTER_H = max(FLOOR_Z + CAV_H + LID_THICKNESS, HOLE_DEPTH + 2.0)

Z_SLOT = OUTER_H - LID_THICKNESS
ZB = Z_SLOT + CLEARANCE
GRIP_X = OUTER_L - 15.0

# ----------------------------------------------------------------------------
# HJELPEFUNKSJONER
# ----------------------------------------------------------------------------
def try_op(label, fn, shape):
    try:
        res = fn(shape)
        if res.isValid() and not res.isNull():
            return res
    except Exception as e:
        App.Console.PrintWarning("%s feilet (%s) - hoppet over.\n" % (label, e))
    return shape

def prism_yz(points_yz, x0, length):
    pts = [V(x0, y, z) for (y, z) in points_yz]
    pts.append(pts[0])
    face = Part.Face(Part.makePolygon(pts))
    return face.extrude(V(length, 0, 0))

def mirror_y(points_yz):
    return [(OUTER_W - y, z) for (y, z) in points_yz]

def is_vertical(e):
    return abs(e.Vertexes[0].Z - e.Vertexes[-1].Z) > 1e-6

def all_at(e, attr, val):
    return all(abs(getattr(v, attr) - val) < 1e-6 for v in e.Vertexes)

# ----------------------------------------------------------------------------
# BOKSKROPP GEOMETRI
# ----------------------------------------------------------------------------
box_outer = Part.makeBox(OUTER_L, OUTER_W, OUTER_H)

box_outer = try_op("Avrunding lukket ende", lambda s: s.makeFillet(
    OUTER_FILLET, [e for e in s.Edges if is_vertical(e) and all_at(e, "X", 0.0)]), box_outer)
box_outer = try_op("Fase åpen ende", lambda s: s.makeChamfer(
    EDGE_CHAMFER, [e for e in s.Edges if is_vertical(e) and all_at(e, "X", OUTER_L)]), box_outer)
box_outer = try_op("Fase bunn", lambda s: s.makeChamfer(
    EDGE_CHAMFER, [e for e in s.Edges if all_at(e, "Z", 0.0)]), box_outer)
box_outer = try_op("Fase topp", lambda s: s.makeChamfer(
    EDGE_CHAMFER, [e for e in s.Edges if all_at(e, "Z", OUTER_H)]), box_outer)

# Eskerommet (50 skudd)
cavity = Part.makeBox(CCI_LENGTH, CCI_WIDTH, OUTER_H - FLOOR_Z + 1.0,
                      V(WALL_T, WALL_T, FLOOR_Z))

# Spor for skyvelokket (innvendig bredde INNER_W)
slot = Part.makeBox(OUTER_L - WALL_T + 1.0, INNER_W, LID_THICKNESS + 1.0,
                    V(WALL_T, WALL_T, Z_SLOT))

# *** NEDSENKING AV INDRE SKILLEVEGG OG HYLLE (Ytterveggen forblir hel) ***
# Start Y: fra den indre skilleveggen (WALL_T + CCI_WIDTH)
# Slutt Y: ut til INNER_W (før den ytre veggen som starter på WALL_T + INNER_W)
y_divider_start = WALL_T + CCI_WIDTH
width_to_cut = DIVIDER_T + EXTRA_WIDTH

divider_cutout = Part.makeBox(
    CCI_LENGTH, 
    width_to_cut, 
    STRIP_STEP_DOWN,
    V(WALL_T, y_divider_start, Z_SLOT - STRIP_STEP_DOWN)
)

y_p = WALL_T + CLEARANCE
y_o = y_p - GROOVE_W - CLEARANCE
OV = 0.5
groove_l = [
    (WALL_T + OV, ZB),
    (WALL_T, ZB),
    (y_o, ZB + GROOVE_W),
    (y_o, ZB + RAIL_H + CLEARANCE),
    (WALL_T + OV, ZB + RAIL_H + CLEARANCE),
]
groove_len = OUTER_L - WALL_T + 1.0
groove_left = prism_yz(groove_l, WALL_T, groove_len)
groove_right = prism_yz(mirror_y(groove_l), WALL_T, groove_len)

box_shape = box_outer.cut(cavity).cut(slot).cut(divider_cutout).cut(groove_left).cut(groove_right)

# ----------------------------------------------------------------------------
# PATRONHULL GENERERING
# ----------------------------------------------------------------------------
x_start = WALL_T + (CCI_LENGTH - (NUM_COLS - 1) * PITCH) / 2.0
y_start = WALL_T + (CCI_WIDTH - (NUM_ROWS - 1) * PITCH) / 2.0
y_strip = y_divider_start + DIVIDER_T + EXTRA_WIDTH / 2.0
r_hole = HOLE_D / 2.0
DOWN = V(0, 0, -1)

def make_hole_tool(x, y, z_top, depth):
    cyl = Part.makeCylinder(r_hole, depth + 0.5, V(x, y, z_top - depth), V(0, 0, 1))
    cone = Part.makeCone(r_hole + HOLE_CHAMFER, r_hole, HOLE_CHAMFER, V(x, y, z_top), DOWN)
    return cyl.fuse(cone)

tools = []
# Ekstra 6. rad: Bores fra den nedsenkede hylla
z_strip_top = Z_SLOT - STRIP_STEP_DOWN
for i in range(NUM_COLS):
    tools.append(make_hole_tool(x_start + i * PITCH, y_strip, z_strip_top, STRIP_HOLE_DEPTH))

# Hull i eskerommet (på den hevede sokkelen)
if POCKETS_IN_CAVITY:
    for r in range(NUM_ROWS):
        depth = RAISED_DEPTH if (r % 2) == RAISED_ROW_PARITY else POCKET_DEPTH_E
        for i in range(NUM_COLS):
            tools.append(make_hole_tool(x_start + i * PITCH, y_start + r * PITCH, FLOOR_Z, depth))

try:
    box_shape = box_shape.cut(Part.makeCompound(tools))
except Exception:
    for t in tools:
        box_shape = box_shape.cut(t)

# Låsebule i sporet
x_b = WALL_T + BUMP_X_FROM_END
y_mid_l = y_p - GROOVE_W / 2.0
z_ceiling = ZB + RAIL_H + CLEARANCE
for yb in (y_mid_l, OUTER_W - y_mid_l):
    box_shape = box_shape.fuse(Part.makeSphere(BUMP_R, V(x_b, yb, z_ceiling)))

# ----------------------------------------------------------------------------
# SKYVELOKK
# ----------------------------------------------------------------------------
x_l0 = WALL_T + CLEARANCE
lid_len = OUTER_L - WALL_T - 2 * CLEARANCE
plate = Part.makeBox(lid_len, OUTER_W - 2 * y_p, OUTER_H - ZB, V(x_l0, y_p, ZB))
plate = try_op("Lokk fase topp", lambda s: s.makeChamfer(
    LID_CHAMFER, [e for e in s.Edges if all_at(e, "Z", OUTER_H)]), plate)
plate = try_op("Lokk fase ender", lambda s: s.makeChamfer(
    0.4, [e for e in s.Edges if all_at(e, "Z", ZB) and abs(e.Vertexes[0].X - e.Vertexes[-1].X) < 1e-6]), plate)

rail_l = [
    (y_p + 0.2, ZB),
    (y_p, ZB),
    (y_p - GROOVE_W, ZB + GROOVE_W),
    (y_p - GROOVE_W, ZB + RAIL_H),
    (y_p + 0.2, ZB + RAIL_H),
]
rail_left = prism_yz(rail_l, x_l0, lid_len)
rail_right = prism_yz(mirror_y(rail_l), x_l0, lid_len)
lid_shape = plate.fuse(rail_left).fuse(rail_right)

for yb in (y_mid_l, OUTER_W - y_mid_l):
    lid_shape = lid_shape.cut(Part.makeSphere(DIMPLE_R, V(x_b, yb, ZB + RAIL_H)))

finger_grip = Part.makeCylinder(GRIP_R, GRIP_DEPTH, V(GRIP_X, OUTER_W / 2.0, OUTER_H), DOWN)
lid_shape = lid_shape.cut(finger_grip)

# ----------------------------------------------------------------------------
# DYNAMISK TEKSTGENERERING
# ----------------------------------------------------------------------------
def find_font():
    if FONT_FILE and os.path.exists(FONT_FILE):
        return FONT_FILE
    env = os.environ
    homes = [os.path.expanduser("~")]
    if env.get("SNAP_REAL_HOME"):
        homes.append(env["SNAP_REAL_HOME"])
    roots = ["/usr/share/fonts", "/usr/local/share/fonts", "/run/host/fonts"]
    for h in homes:
        for d in ("fonts", "Fonts", ".fonts", ".local/share/fonts"):
            roots.append(os.path.join(h, d))
    found = []
    for r in roots:
        if os.path.isdir(r):
            for dp, _dn, fns in os.walk(r):
                for fn in fns:
                    if fn.lower().endswith(".ttf"):
                        found.append(os.path.join(dp, fn))
    preferred = ["dejavusans-bold", "liberationsans-bold", "ubuntu-b", "arialbd"]
    for p in preferred:
        for f in found:
            if os.path.basename(f).lower().startswith(p):
                return f
    return found[0] if found else ""

def _wire_string(text, font, size):
    try:
        return Part.makeWireString(text, font, size, 0.0)
    except Exception:
        fdir, fname = os.path.split(font)
        return Part.makeWireString(text, fdir, fname, size, 0.0)

def build_text_shape(text, font, size):
    char_wires = _wire_string(text, font, size)
    faces = []
    for wires in char_wires:
        if not wires:
            continue
        try:
            f = Part.makeFace(wires, "Part::FaceMakerBullseye")
            faces.extend(f.Faces)
        except Exception:
            pass
    if not faces:
        return None, None
    return Part.makeCompound(faces), faces

def make_text_cutter(text, size, depth, cx, cy, z_top, max_width):
    font = find_font()
    if not font:
        return None
    shp, faces = build_text_shape(text, font, size)
    if shp is None:
        return None

    width = shp.BoundBox.XMax - shp.BoundBox.XMin
    if width > max_width:
        new_size = size * (max_width / width)
        shp, faces = build_text_shape(text, font, new_size)
        if shp is None:
            return None

    bb = shp.BoundBox
    dx = cx - (bb.XMin + bb.XMax) / 2.0
    dy = cy - (bb.YMin + bb.YMax) / 2.0
    dz = (z_top - depth) - bb.ZMin

    height = depth + 0.5
    solids = [f.extrude(V(0, 0, height)) for f in faces]
    cutter = Part.makeCompound(solids)
    cutter.translate(V(dx, dy, dz))
    return cutter

if LID_TEXT.strip():
    try:
        x_min = x_l0 + 3.0
        x_max = GRIP_X - GRIP_R - 3.0
        avail = x_max - x_min
        cutter = make_text_cutter(LID_TEXT, TEXT_SIZE, TEXT_DEPTH, (x_min + x_max) / 2.0, OUTER_W / 2.0, OUTER_H, avail)
        if cutter is not None:
            lid_shape = lid_shape.cut(cutter)
    except Exception as e:
        App.Console.PrintError("Feil ved tekstgenerering: %s\n" % e)

# ----------------------------------------------------------------------------
# OPPRETT I FREECAD
# ----------------------------------------------------------------------------
doc = App.newDocument("AmmoBox_%s" % CALIBER)

box_final = box_shape.removeSplitter()
lid_final = lid_shape.removeSplitter()

if LAYOUT == "print":
    lid_final = lid_final.copy()
    lid_final.translate(V(0, OUTER_W + 15.0, -ZB))

obj_box = doc.addObject("Part::Feature", "Boks_Kropp")
obj_box.Shape = box_final
obj_lid = doc.addObject("Part::Feature", "Skyvelokk")
obj_lid.Shape = lid_final
doc.recompute()

try:
    import FreeCADGui
    FreeCADGui.SendMsgToActiveView("ViewFit")
    FreeCADGui.activeDocument().activeView().viewIsometric()
except Exception:
    pass

App.Console.PrintMessage("Ammunisjonsboks ferdig generert med hel yttervegg og senket skillevegg.\n")