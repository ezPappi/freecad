# -*- coding: utf-8 -*-
"""
Ammunisjonsboks v2.16 for FreeCAD 1.x  -  tilpasset CCI Standard Velocity-krate

Nytt i v2.16:
 - Lirkespor (Pry Notch) på fremkanten for enkel fjerning av full krate med kniv/skrutrekker.
 - Doble låsebuler/detenter (foran og bak) for å forhindre at lokket glir opp utilsiktet.
 - Korrigert tekstgenerering og rotasjon på bakveggen (X = 0).
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
TEXT_DEPTH = 0.8       # Dybde på innfrest tekst på lokket
TEXT_SIZE = 10.0       # Tekststørrelse på lokket
FONT_FILE = ""         # Full sti til .ttf, tom = auto

# Tekst på bakveggen (X = 0, endeveggen motsatt av lirkespor/åpning)
BACK_TEXT = "eit.no"           # Tekst som skal freses inn på bakveggen
BACK_TEXT_SIZE = 8.0           # Tekststørrelse for bakveggen
BACK_TEXT_DEPTH = 0.8          # Dybde på innfrest tekst på bakveggen
BACK_TEXT_Z = 4.0              # Z-posisjon (høyde fra bunnen) for teksten
BACK_TEXT_Y_OFFSET = 0.0       # Horisontal forskyvning (0.0 = midtstilt, pos. = mot høyre, neg. = mot venstre)

# Nytt: Lirkespor for verktøy (kniv, skrutrekker, bilnøkkel)
PRY_NOTCH = True               # Aktiver lirkespor i forkant av boksen
PRY_NOTCH_W = 4.0             # Bredde på lirkesporet (mm)
PRY_NOTCH_DEPTH = 3.8          # Dybde inn i fremveggen (mm)
PRY_NOTCH_HEIGHT = 11.0         # Høyde på utskjæringen fra toppkanten (mm)

BOX_OVERRIDE = None        # (lengde, bredde, høyde) på originaleska
HOLE_D_OVERRIDE = None     # Hulldiameter
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
RAISED_ROW_PARITY = 1      # bytter hvilke som er høye: 0/1 (1 = patron nr. 2 i første rad er høy)
STAGGER_MODE = "checker"   # "checker" = sjakkbrett, "rows" = annenhver rad, "none" = alle like høye
STRIP_STAGGER = 1.5        # høydeforskjell på rad 6 (sjakkbrett). Må være mindre enn STRIP_EXPOSED_HEIGHT - rimtykkelseSTRIP_STAGGER = 1.5        

# Lettere boks: innfelte paneler på yttersidene av underdelen
LIGHTEN_PANELS = True
PANEL_DEPTH = 1.6              # dybde inn i veggen (underdelen er massiv blokk, så dette svekker ingenting)
PANEL_MARGIN = 8.0             # ramme som blir stående ved hjørnene (mm)
PANEL_BOTTOM = 3.0             # ramme nederst (mm)
PANEL_TOP_BELOW_SLOT = 5.0     # avstand mellom panelets topp og lokksonen (mm)  

# Doble fingerspor for klypetak rundt kraten
FINGER_NOTCH = True
NOTCH_W = 14.0
NOTCH_DEPTH_FRONT = 1.6        # inn i framveggen (tykk vegg, ok)
NOTCH_DEPTH_REAR = 1.0         # inn i skilleveggen (tynn, ikke gå dypere)
NOTCH_MIN_WALL_ABOVE = 4.0     # minst så mye massiv vegg mellom sporets topp og lokksporet    

# 2. Den 6. ekstra raden (10 skudd)
STRIP_EXPOSED_HEIGHT = 3.0     # Hvor mange mm patronen stikker opp på ekstraraden

# Fileter / faser
OUTER_FILLET = 3.0         # Avrunding på lukkede hjørner
EDGE_CHAMFER = 0.8         # Fase topp/bunn
HOLE_CHAMFER = 0.6         # Innløpsfase på hull
LID_CHAMFER = 0.6          # Fase på toppen av lokket        

# Lokkets låsebuler (detenters) - Nå med doble sikringspunkter!
BUMP_R = 0.45              # Bule i sporet
DIMPLE_R = 0.65            # Fordypning i lokkskinnen
BUMP_X_REAR = 8.0          # Avstand fra lukket ende (bakre låsepunkt)
BUMP_X_FRONT = 25.0        # Avstand fra lukket ende (fremre/midtre låsepunkt)

LAYOUT = "print"           # "print" = lokk flatt ved siden av, "assembled" = montert
EXPORT_DIR = ""            # Sti for STL-eksport, tom = ingen

# ----------------------------------------------------------------------------
# KALIBERTABELL (mm)
# ----------------------------------------------------------------------------
CALIBERS = {
    "22LR":   dict(label="22LR",   rim=7.1,   oal=25.4, hole_d=6.1,  box=(98.0, 48.0, 26.0),  box_est=False,
                   rim_t=1.1,
                   crate=dict(L=71.30, W=37.15, T=3.25, cols=10, rows=5)),
    "9MM":    dict(label="9MM",     rim=9.96,  oal=29.7, hole_d=None, box=(118.0, 62.0, 34.0), box_est=True),
    "357MAG": dict(label="357 MAG", rim=11.18, oal=40.4, hole_d=None, box=(125.0, 63.0, 40.0), box_est=True),
    "38SPL":  dict(label="38 SPL",  rim=11.2,  oal=39.4, hole_d=None, box=(125.0, 63.0, 40.0), box_est=True),
    "40SW":   dict(label="40 S&W",  rim=10.8,  oal=28.8, hole_d=None, box=(118.0, 62.0, 34.0), box_est=True),
    "45ACP":  dict(label="45 ACP",  rim=12.2,  oal=32.4, hole_d=None, box=(125.0, 68.0, 38.0), box_est=True),
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
WALL_T = 3.6                
DIVIDER_T = 2.0             
BOTTOM_T = 2.0              
LID_THICKNESS = 4.5         
CLEARANCE = 0.25
GROOVE_W = 1.6              
RAIL_H = 2.0                

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
if HOLE_CHAMFER_E < 0.3:
    HOLE_CHAMFER_E = 0.0       

# ----------------------------------------------------------------------------
# HULLDYBDE OG STAGGER
# ----------------------------------------------------------------------------
STAGGER_E = STAGGER if STAGGER_MODE != "none" else 0.0

if CRATE:
    _auto_depth = C["oal"] - EXPOSED_LOW_ROW - CRATE["T"]
else:
    _auto_depth = 13.0

POCKET_DEPTH_E = POCKET_DEPTH or _auto_depth
RAISED_DEPTH = max(POCKET_DEPTH_E - STAGGER_E, 2.0)

FLOOR_RAISE = CAVITY_FLOOR_RAISE or POCKET_DEPTH_E
FLOOR_Z = BOTTOM_T + FLOOR_RAISE

_max_depth = FLOOR_Z - 1.5
if POCKET_DEPTH_E > _max_depth:
    POCKET_DEPTH_E = _max_depth
    RAISED_DEPTH = max(POCKET_DEPTH_E - STAGGER_E, 2.0)

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

def prism_xz(points_xz, y0, length):
    pts = [V(x, y0, z) for (x, z) in points_xz]
    pts.append(pts[0])
    face = Part.Face(Part.makePolygon(pts))
    return face.extrude(V(0, length, 0))

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

if LIGHTEN_PANELS:
    try:
        _z0 = PANEL_BOTTOM
        _z1 = Z_SLOT - PANEL_TOP_BELOW_SLOT
        _D = PANEL_DEPTH
        _m = PANEL_MARGIN
        if _z1 - _z0 > 2 * _D + 2.0 and _D < WALL_T - 1.5:
            prof = [(-0.5, _z0), (_D, _z0), (_D, _z1 - _D), (0.0, _z1), (-0.5, _z1)]
            ranges = [(_m, OUTER_L - _m)]
            if FINGER_NOTCH:
                _nx0 = WALL_T + (CCI_LENGTH - NOTCH_W) / 2.0 - 4.0
                _nx1 = _nx0 + NOTCH_W + 8.0
                ranges = [(_m, _nx0), (_nx1, OUTER_L - _m)]
            panel_cuts = []
            for (xa, xb) in ranges:
                panel_cuts.append(prism_yz(prof, xa, xb - xa))
            panel_cuts.append(prism_yz(mirror_y(prof), _m, OUTER_L - 2 * _m))
            panel_cuts.append(prism_xz(prof, _m, OUTER_W - 2 * _m))
            panel_cuts.append(prism_xz([(OUTER_L - x, z) for (x, z) in prof], _m, OUTER_W - 2 * _m))
            _trial = box_outer
            for pc in panel_cuts:
                _trial = _trial.cut(pc)
            if _trial.isValid() and not _trial.isNull() and len(_trial.Solids) == 1:
                box_outer = _trial
    except Exception:
        pass

cavity = Part.makeBox(CCI_LENGTH, CCI_WIDTH, OUTER_H - FLOOR_Z + 1.0,
                      V(WALL_T, WALL_T, FLOOR_Z))

slot = Part.makeBox(OUTER_L - WALL_T + 1.0, INNER_W, LID_THICKNESS + 1.0,
                    V(WALL_T, WALL_T, Z_SLOT))

y_divider_start = WALL_T + CCI_WIDTH
width_to_cut = DIVIDER_T + EXTRA_WIDTH

divider_cutout = Part.makeBox(
    CCI_LENGTH, width_to_cut, STRIP_STEP_DOWN,
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

# 1. LIRKESPOR (Pry notch) for skrutrekker/kniv/nøkkel
if PRY_NOTCH:
    pry_x0 = OUTER_L - PRY_NOTCH_DEPTH
    pry_y0 = (OUTER_W - PRY_NOTCH_W) / 2.0
    pry_z0 = Z_SLOT - PRY_NOTCH_HEIGHT
    pry_cut = Part.makeBox(PRY_NOTCH_DEPTH + 1.0, PRY_NOTCH_W, PRY_NOTCH_HEIGHT + 1.0, V(pry_x0, pry_y0, pry_z0))
    box_shape = box_shape.cut(pry_cut)

# 2. Fingerspor
if FINGER_NOTCH:
    notch_x = WALL_T + (CCI_LENGTH - NOTCH_W) / 2.0
    notch_h = max(min(CCI_HEIGHT + 1.0, Z_SLOT - FLOOR_Z - NOTCH_MIN_WALL_ABOVE), 1.0)
    notch_front = Part.makeBox(NOTCH_W, NOTCH_DEPTH_FRONT + 0.5, notch_h,
                               V(notch_x, WALL_T - NOTCH_DEPTH_FRONT, FLOOR_Z))
    notch_rear = Part.makeBox(NOTCH_W, NOTCH_DEPTH_REAR + 0.5, notch_h,
                              V(notch_x, y_divider_start - 0.5, FLOOR_Z))
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

def is_raised(r, i):
    if STAGGER_MODE == "checker":
        return ((r + i) % 2) == RAISED_ROW_PARITY
    if STAGGER_MODE == "rows":
        return (r % 2) == RAISED_ROW_PARITY
    return False

tools = []
z_strip_top = Z_SLOT - STRIP_STEP_DOWN
for i in range(NUM_COLS):
    if STAGGER_MODE == "checker":
        exposed = STRIP_EXPOSED_HEIGHT if is_raised(NUM_ROWS, i) else STRIP_EXPOSED_HEIGHT - STRIP_STAGGER
    else:
        exposed = STRIP_EXPOSED_HEIGHT
    strip_depth = max(C["oal"] - exposed, 5.0)
    tools.append(make_hole_tool(x_start + i * PITCH_X, y_strip, z_strip_top, strip_depth))

if POCKETS_IN_CAVITY:
    for r in range(NUM_ROWS):
        for i in range(NUM_COLS):
            depth = RAISED_DEPTH if is_raised(r, i) else POCKET_DEPTH_E
            tools.append(make_hole_tool(x_start + i * PITCH_X, y_start + r * PITCH_Y, FLOOR_Z, depth))

try:
    box_shape = box_shape.cut(Part.makeCompound(tools))
except Exception:
    for t in tools:
        box_shape = box_shape.cut(t)

# 3. DOBLE LÅSEBULER (DETENTS) - Lås både foran og bak på skinnene
y_mid_l = y_p - GROOVE_W / 2.0
z_ceiling = ZB + RAIL_H + CLEARANCE
detent_positions = [WALL_T + BUMP_X_REAR, WALL_T + BUMP_X_FRONT]

for x_pos in detent_positions:
    for yb in (y_mid_l, OUTER_W - y_mid_l):
        box_shape = box_shape.fuse(Part.makeSphere(BUMP_R, V(x_pos, yb, z_ceiling)))

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
    (y_p + 0.2, ZB), (y_p, ZB), (y_p - GROOVE_W, ZB + GROOVE_W),
    (y_p - GROOVE_W, ZB + RAIL_H), (y_p + 0.2, ZB + RAIL_H),
]
rail_left = prism_yz(rail_l, x_l0, lid_len)
rail_right = prism_yz(mirror_y(rail_l), x_l0, lid_len)
lid_shape = plate.fuse(rail_left).fuse(rail_right)

# Låsefordypninger i lokket (matchet med begge bulene)
for x_pos in detent_positions:
    for yb in (y_mid_l, OUTER_W - y_mid_l):
        lid_shape = lid_shape.cut(Part.makeSphere(DIMPLE_R, V(x_pos, yb, ZB + RAIL_H)))

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

def make_back_wall_text_cutter(text, size, depth, cy, cz_bottom, max_width, x_wall):
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
    cx = (bb.XMin + bb.XMax) / 2.0
    
    dx = x_wall + depth
    dy = cy + cx      
    dz = cz_bottom - bb.YMin

    height = depth + 0.5
    solids = [f.extrude(V(0, 0, height)) for f in faces]
    cutter = Part.makeCompound(solids)
    
    cutter.rotate(V(0, 0, 0), V(1, 0, 0), 90)
    cutter.rotate(V(0, 0, 0), V(0, 0, 1), -90)
    cutter.translate(V(dx, dy, dz))
    return cutter

# Generer tekst på lokket
if LID_TEXT.strip():
    try:
        x_min = x_l0 + 3.0
        x_max = GRIP_X - GRIP_R - 3.0
        avail = x_max - x_min
        cutter = make_text_cutter(LID_TEXT, TEXT_SIZE, TEXT_DEPTH, (x_min + x_max) / 2.0, OUTER_W / 2.0, OUTER_H, avail)
        if cutter is not None:
            lid_shape = lid_shape.cut(cutter)
    except Exception as e:
        App.Console.PrintError("Feil ved tekstgenerering for lokk: %s\n" % e)

# Generer tekst på bakveggen (X = 0)
if BACK_TEXT.strip():
    try:
        max_w = OUTER_W - 2 * PANEL_MARGIN
        x_back = PANEL_DEPTH if (LIGHTEN_PANELS and BACK_TEXT_Z >= PANEL_BOTTOM) else 0.0
        cy_target = (OUTER_W / 2.0) + BACK_TEXT_Y_OFFSET
        wall_cutter = make_back_wall_text_cutter(BACK_TEXT, BACK_TEXT_SIZE, BACK_TEXT_DEPTH, cy_target, BACK_TEXT_Z, max_w, x_back)
        if wall_cutter is not None:
            box_shape = box_shape.cut(wall_cutter)
    except Exception as e:
        App.Console.PrintError("Feil ved tekstgenerering for bakvegg: %s\n" % e)

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

App.Console.PrintMessage("Ferdig. Boks v2.16 for %s generert.\n" % CALIBER)