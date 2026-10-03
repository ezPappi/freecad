# -*- coding: utf-8 -*-
"""
Ammunisjonsboks v2.8.1 for FreeCAD 1.x  -  tilpasset CCI Standard Velocity-krate

Nytt i v2.8.1:
 - Oppdatert med DOBLE fingerspor (framvegg + skillevegg) for klypetak rundt kraten.
 - Beholder den 6. ekstra raden (10 skudd) og alle v2.8-oppdateringer intact.
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

BOX_OVERRIDE = None        # (lengde, bredde, høyde) på originaleska (brukes ikke når kratemål er aktive)
HOLE_D_OVERRIDE = None     # Hulldiameter (22LR: 6.2; prøv 6.0 hvis veggene mellom hullene blir for tynne)
NUM_HOLES_OVERRIDE = None  # Antall hull per rad; None = auto

# CCI-krate (flat plate med 50 hull som patronene står i)
USE_CRATE = True            # True: eskerommet tilpasses kraten (mål i kalibertabellen under)
CRATE_CLEARANCE = 0.4       # luft rundt kraten, per side (mm)
CRATE_HOLE_OFFSET_X = 0.0   # flytt hullmønsteret langs lengden hvis hullene ikke flukter helt (mm)
CRATE_HOLE_OFFSET_Y = 0.0   # flytt hullmønsteret langs bredden (mm)
CRATE_PITCH_X = None        # hullavstand langs lengden; None = kratelengde / antall hull
CRATE_PITCH_Y = None        # hullavstand langs bredden; None = kratebredde / antall hull

# 1. Eskerom (50 skudd)
POCKETS_IN_CAVITY = True
CAVITY_FLOOR_RAISE = None  # Høyde på hullblokken. None = auto
POCKET_DEPTH = None        # Hulldybde. None = auto
EXPOSED_LOW_ROW = 3.0      # Hvor mange mm laveste rad skal stikke opp over kraten
STAGGER = 3.0              # Hvor mange mm høyere hver annen rad står
RAISED_ROW_PARITY = 1      # 1 = rad 2, 4, ... står høyest; 0 = rad 1, 3, 5, ... står høyest

# Doble fingerspor i langveggene for klypetak rundt kraten
FINGER_NOTCH = True
NOTCH_W = 14.0
NOTCH_DEPTH = 1.6          # inn i veggene (både framvegg og skillevegg)

# 2. Den 6. ekstra raden (10 skudd)
STRIP_EXPOSED_HEIGHT = 3.0 # Hvor mange mm patronen stikker opp på ekstraraden

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
    "22LR":   dict(label="22LR",    rim=7.1,   oal=25.4, hole_d=6.1,  box=(98.0, 48.0, 26.0),  box_est=False,
                   rim_t=1.1,
                   crate=dict(L=71.30, W=37.15, T=3.25, cols=10, rows=5)),
    "9MM":    dict(label="9MM",     rim=9.96,  oal=29.7, hole_d=None, box=(118.0, 62.0, 34.0), box_est=True),
    "357MAG": dict(label="357 MAG", rim=11.18, oal=40.4, hole_d=None, box=(125.0, 63.0, 40.0), box_est=True),
    "38SPL":  dict(label="38 SPL",  rim=11.2,  oal=39.4, hole_d=None, box=(125.0, 63.0, 40.0), box_est=True),
    "40SW":   dict(label="40 S&W",  rim=10.8,  oal=28.8, hole_d=None, box=(118.0, 62.0, 34.0), box_est=True),
    "45ACP":  dict(label="45 ACP",  rim=12.2,  oal=32.4, hole_d=None, box=(125.0, 68.0, 38.0), box_est=True),
    "10MM":   dict(label="10MM",    rim=10.8,  oal=32.0, hole_d=None, box=(120.0, 62.0, 36.0), box_est=True),
    "223":    dict(label="223 REM", rim=9.6,   oal=57.4, hole_d=None, box=(150.0, 70.0, 64.0), box_est=True),
    "6.5X55": dict(label="6.5x55", rim=12.2,  oal=80.0, hole_d=12.6, box=(165.0, 85.0, 85.0), box_est=True),
}

if CALIBER not in CALIBERS:
    raise ValueError("Ukjent kaliber '%s'." % CALIBER)
C = CALIBERS[CALIBER]

if LID_TEXT.strip().upper() == "AUTO":
    LID_TEXT = C["label"]

# ----------------------------------------------------------------------------
# PARAMETERE OG GEOMETRIBASIS
# ----------------------------------------------------------------------------
WALL_T = 4.5                # Solid skinnevegg (~2.9 mm massivt gods bak sporet)
DIVIDER_T = 2.0             # Skillevegg mot 6. rad
BOTTOM_T = 2.5              # Bunntykkelse
LID_THICKNESS = 4.5         # Lokktykkelse
CLEARANCE = 0.25
GROOVE_W = 1.6
RAIL_H = 2.2

GRIP_R = 8.0
GRIP_DEPTH = 1.2

HOLE_D = HOLE_D_OVERRIDE or C["hole_d"] or round(C["rim"] + 0.4, 1)
EXTRA_WIDTH = HOLE_D + 2.0

CRATE = C.get("crate") if USE_CRATE else None
RIM_T = C.get("rim_t", 1.2)

if CRATE:
    CCI_LENGTH = CRATE["L"] + 2 * CRATE_CLEARANCE
    CCI_WIDTH = CRATE["W"] + 2 * CRATE_CLEARANCE
    CCI_HEIGHT = CRATE["T"]
    NUM_COLS = NUM_HOLES_OVERRIDE or CRATE["cols"]
    NUM_ROWS = CRATE["rows"]
    PITCH_X = CRATE_PITCH_X or CRATE["L"] / CRATE["cols"]
    PITCH_Y = CRATE_PITCH_Y or CRATE["W"] / CRATE["rows"]
else:
    CCI_LENGTH, CCI_WIDTH, CCI_HEIGHT = BOX_OVERRIDE if BOX_OVERRIDE else C["box"]
    PITCH_X = PITCH_Y = HOLE_D + 3.0
    NUM_COLS = NUM_HOLES_OVERRIDE or int((CCI_LENGTH - HOLE_D) / PITCH_X + 1e-6) + 1
    NUM_ROWS = int((CCI_WIDTH - HOLE_D) / PITCH_Y + 1e-6) + 1

_wall_between = min(PITCH_X, PITCH_Y) - HOLE_D
HOLE_CHAMFER_E = min(HOLE_CHAMFER, (_wall_between - 0.6) / 2.0)
if HOLE_CHAMFER_E < 0.2:
    HOLE_CHAMFER_E = 0.0

# ----------------------------------------------------------------------------
# HULLDYBDE OG STAGGER BEREGNING
# ----------------------------------------------------------------------------
STAGGER_E = STAGGER

if CRATE:
    _auto_depth = C["oal"] - EXPOSED_LOW_ROW - CRATE["T"]
else:
    _auto_depth = 13.0

POCKET_DEPTH_E = POCKET_DEPTH or _auto_depth
RAISED_DEPTH = max(POCKET_DEPTH_E - STAGGER_E, 2.0)

FLOOR_RAISE = CAVITY_FLOOR_RAISE or POCKET_DEPTH_E
FLOOR_Z = BOTTOM_T + FLOOR_RAISE

if CRATE:
    CAV_H = CRATE["T"] + EXPOSED_LOW_ROW + STAGGER_E + 1.5
else:
    CAV_H = max(CCI_HEIGHT - FLOOR_RAISE + 1.0, C["oal"] - RAISED_DEPTH + 1.0)

STRIP_HOLE_DEPTH = max(C["oal"] - STRIP_EXPOSED_HEIGHT, 5.0)
STRIP_STEP_DOWN = STRIP_EXPOSED_HEIGHT + 0.5

HOLE_DEPTH = round(C["oal"] + LID_THICKNESS + 0.5, 1)

OUTER_L = CCI_LENGTH + 2 * WALL_T
INNER_W = CCI_WIDTH + DIVIDER_T + EXTRA_WIDTH
OUTER_W = INNER_W + 2 * WALL_T
OUTER_H = max(FLOOR_Z + CAV_H + LID_THICKNESS, HOLE_DEPTH + 2.0)

Z_SLOT = OUTER_H - LID_THICKNESS
ZB = Z_SLOT + CLEARANCE
GRIP_X = OUTER_L - 15.0

App.Console.PrintMessage(
    "v2.8 Kaliber %s: hull %.1f mm, godstykkelse bak spor %.1f mm.\n"
    "Laveste rad stikker %.1f mm over krate, hevet rad stikker %.1f mm over krate.\n"
    % (CALIBER, HOLE_D, WALL_T - GROOVE_W, EXPOSED_LOW_ROW, EXPOSED_LOW_ROW + STAGGER_E))

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

cavity = Part.makeBox(CCI_LENGTH, CCI_WIDTH, OUTER_H - FLOOR_Z + 1.0,
                      V(WALL_T, WALL_T, FLOOR_Z))

slot = Part.makeBox(OUTER_L - WALL_T + 1.0, INNER_W, LID_THICKNESS + 1.0,
                    V(WALL_T, WALL_T, Z_SLOT))

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

# DOBLE FINGERSPOR (Tommel på framvegg, pekefinger på skillevegg)
if FINGER_NOTCH:
    notch_x = WALL_T + (CCI_LENGTH - NOTCH_W) / 2.0
    notch_h = Z_SLOT - FLOOR_Z
    
    # 1. Fingerspor i framvegg (tommel)
    notch_front = Part.makeBox(NOTCH_W, NOTCH_DEPTH + 0.5, notch_h,
                               V(notch_x, WALL_T - NOTCH_DEPTH, FLOOR_Z))
    
    # 2. Fingerspor i skillevegg mot 6. rad (pekefinger)
    notch_rear = Part.makeBox(NOTCH_W, NOTCH_DEPTH + 0.5, notch_h,
                              V(notch_x, WALL_T + CCI_WIDTH - 0.5, FLOOR_Z))
    
    box_shape = box_shape.cut(notch_front).cut(notch_rear)

# ----------------------------------------------------------------------------
# PATRONHULL GENERERING
# ----------------------------------------------------------------------------
x_start = WALL_T + (CCI_LENGTH - (NUM_COLS - 1) * PITCH_X) / 2.0 + CRATE_HOLE_OFFSET_X
y_start = WALL_T + (CCI_WIDTH - (NUM_ROWS - 1) * PITCH_Y) / 2.0 + CRATE_HOLE_OFFSET_Y
y_strip = y_divider_start + DIVIDER_T + EXTRA_WIDTH / 2.0
r_hole = HOLE_D / 2.0
DOWN = V(0, 0, -1)

def make_hole_tool(x, y, z_top, depth):
    cyl = Part.makeCylinder(r_hole, depth + 0.5, V(x, y, z_top - depth), V(0, 0, 1))
    if HOLE_CHAMFER_E > 0.0:
        cone = Part.makeCone(r_hole + HOLE_CHAMFER_E, r_hole, HOLE_CHAMFER_E, V(x, y, z_top), DOWN)
        return cyl.fuse(cone)
    return cyl

tools = []
# Ekstra 6. rad (10 skudd)
z_strip_top = Z_SLOT - STRIP_STEP_DOWN
for i in range(NUM_COLS):
    tools.append(make_hole_tool(x_start + i * PITCH_X, y_strip, z_strip_top, STRIP_HOLE_DEPTH))

# Hull i eskerommet (med stagger)
if POCKETS_IN_CAVITY:
    for r in range(NUM_ROWS):
        depth = RAISED_DEPTH if (r % 2) == RAISED_ROW_PARITY else POCKET_DEPTH_E
        for i in range(NUM_COLS):
            tools.append(make_hole_tool(x_start + i * PITCH_X, y_start + r * PITCH_Y, FLOOR_Z, depth))

try:
    box_shape = box_shape.cut(Part.makeCompound(tools))
except Exception:
    for t in tools:
        box_shape = box_shape.cut(t)

# Låsebule
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

if EXPORT_DIR:
    try:
        import Mesh
        Mesh.export([obj_box], os.path.join(EXPORT_DIR, "ammoboks_%s_kropp.stl" % CALIBER))
        Mesh.export([obj_lid], os.path.join(EXPORT_DIR, "ammoboks_%s_lokk.stl" % CALIBER))
    except Exception as e:
        App.Console.PrintError("STL-eksport feilet: %s\n" % e)

App.Console.PrintMessage("Ferdig. Boks v2.8.1 for %s med doble fingerspor generert.\n" % CALIBER)