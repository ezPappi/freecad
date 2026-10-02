# -*- coding: utf-8 -*-
"""
FreeCAD Python-skript: 22LR Ammunisjonsboks med envegs skyvelokk.
Dynamisk tekstgenerering med Part.makeWireString (rettet versjon).

Rettelser:
 - Teksten ble aldri flyttet: 'shape.Placement.Base = ...' virker ikke på
   Part.Shape (Placement returneres som kopi), så teksten ble liggende i
   origo og traff aldri lokket. Nå brukes translate().
 - Bruker ShapeString-flatene direkte (ikke Face() av alle wires), slik at
   hull i bokstaver (O, 0, A, R ...) blir riktige og flatene ikke overlapper.
 - Teksten sentreres på selve bounding box (XMin/YMin ble ignorert før).
 - Teksten plasseres/skaleres slik at den ikke havner i fingergrepet.
 - Feilmeldinger skrives nå alltid ut (Report view), ingen stille feil.
"""

import FreeCAD as App
import Part
import os

V = App.Vector

# ----------------------------------------------------------------------------
# BRUKERKONFIGURASJON / DYNAMISK TEKSTVARIABEL
# ----------------------------------------------------------------------------
LID_TEXT = "22LR MATCH"   # Skriv HVA SOM HELST her
TEXT_DEPTH = 0.8          # Dybde på den innfreste teksten (mm)
TEXT_SIZE = 10.0          # Tekststørrelse (høyde i mm)
FONT_FILE = ""            # Sett evt. full sti til en .ttf her; tom = auto

# ----------------------------------------------------------------------------
# PARAMETERE FOR BOKSEN
# ----------------------------------------------------------------------------
WALL_T = 2.5
DIVIDER_T = 1.5
BOTTOM_T = 2.0

CCI_LENGTH = 98.0
CCI_WIDTH = 48.0
CCI_HEIGHT = 26.0

HOLE_D = 6.2
HOLE_DEPTH = 24.0
NUM_HOLES = 10
PITCH_X = 9.2
EXTRA_WIDTH = HOLE_D + 2.0

INNER_L = CCI_LENGTH
INNER_W = CCI_WIDTH + DIVIDER_T + EXTRA_WIDTH
INNER_H = CCI_HEIGHT + 2.0

OUTER_L = INNER_L + (2 * WALL_T)
OUTER_W = INNER_W + (2 * WALL_T)
OUTER_H = INNER_H + BOTTOM_T

LID_THICKNESS = 3.0
GROOVE_W = 2.0
GROOVE_H = 2.0
CLEARANCE = 0.25

GRIP_R = 8.0
GRIP_X = OUTER_L - 15.0

# ----------------------------------------------------------------------------
# GEOMETRI: HOVEDBOKS & LOKK
# ----------------------------------------------------------------------------
box_outer = Part.makeBox(OUTER_L, OUTER_W, OUTER_H)

cci_cavity = Part.makeBox(
    CCI_LENGTH, CCI_WIDTH, INNER_H + 10.0,
    V(WALL_T, WALL_T, BOTTOM_T)
)

y_hole_pos = WALL_T + CCI_WIDTH + DIVIDER_T + (EXTRA_WIDTH / 2.0)
x_start = WALL_T + (CCI_LENGTH - ((NUM_HOLES - 1) * PITCH_X)) / 2.0

extra_holes = []
for i in range(NUM_HOLES):
    x_pos = x_start + (i * PITCH_X)
    hole = Part.makeCylinder(
        HOLE_D / 2.0, HOLE_DEPTH,
        V(x_pos, y_hole_pos, OUTER_H - HOLE_DEPTH), V(0, 0, 1)
    )
    extra_holes.append(hole)

groove_z = OUTER_H - LID_THICKNESS + (GROOVE_H / 2.0)

groove_left = Part.makeBox(OUTER_L - WALL_T, GROOVE_W, GROOVE_H, V(WALL_T, WALL_T - GROOVE_W, groove_z))
groove_right = Part.makeBox(OUTER_L - WALL_T, GROOVE_W, GROOVE_H, V(WALL_T, OUTER_W - WALL_T, groove_z))
top_cutout = Part.makeBox(OUTER_L - WALL_T, INNER_W, LID_THICKNESS + 1.0, V(WALL_T, WALL_T, OUTER_H - LID_THICKNESS))

box_shape = box_outer.cut(cci_cavity).cut(top_cutout)
for h in extra_holes:
    box_shape = box_shape.cut(h)
box_shape = box_shape.cut(groove_left).cut(groove_right)

# Lokk-geometri
lid_base = Part.makeBox(
    OUTER_L - WALL_T - CLEARANCE,
    INNER_W - (2 * CLEARANCE),
    LID_THICKNESS - CLEARANCE,
    V(WALL_T, WALL_T + CLEARANCE, OUTER_H - LID_THICKNESS + CLEARANCE)
)

side_rail_left = Part.makeBox(
    OUTER_L - WALL_T - CLEARANCE, GROOVE_W - CLEARANCE, GROOVE_H - CLEARANCE,
    V(WALL_T, WALL_T - GROOVE_W + CLEARANCE, groove_z + (CLEARANCE / 2.0))
)
side_rail_right = Part.makeBox(
    OUTER_L - WALL_T - CLEARANCE, GROOVE_W - CLEARANCE, GROOVE_H - CLEARANCE,
    V(WALL_T, OUTER_W - WALL_T, groove_z + (CLEARANCE / 2.0))
)

lid_shape = lid_base.fuse(side_rail_left).fuse(side_rail_right)

finger_grip = Part.makeCylinder(GRIP_R, 1.2, V(GRIP_X, OUTER_W / 2.0, OUTER_H), V(0, 0, -1))
lid_shape = lid_shape.cut(finger_grip)

# ----------------------------------------------------------------------------
# DYNAMISK TEKSTGENERERING (makeWireString)
# ----------------------------------------------------------------------------
doc = App.newDocument("22LR_AmmoBox_DynamicText")


def find_font():
    """Finner en .ttf. Håndterer Snap/Flatpak, der FreeCAD ikke ser /usr/share/fonts."""
    if FONT_FILE:
        if os.path.exists(FONT_FILE):
            return FONT_FILE
        App.Console.PrintWarning("FONT_FILE finnes ikke for FreeCAD: %s\n" % FONT_FILE)

    env = os.environ
    homes = [os.path.expanduser("~")]
    if env.get("SNAP_REAL_HOME"):          # Snap: ekte hjemmemappe
        homes.append(env["SNAP_REAL_HOME"])

    roots = [
        "/usr/share/fonts", "/usr/local/share/fonts",
        "/run/host/fonts", "/run/host/usr/share/fonts",        # Flatpak
        "/var/lib/snapd/hostfs/usr/share/fonts",               # Snap (classic)
    ]
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

    preferred = ["dejavusans-bold", "liberationsans-bold", "ubuntu-b",
                 "freesansbold", "arialbd", "dejavusans", "liberationsans",
                 "arial"]
    for p in preferred:
        for f in found:
            if os.path.basename(f).lower().startswith(p):
                return f
    if found:
        return found[0]

    App.Console.PrintError(
        "Ingen .ttf funnet. Miljø: SNAP=%s FLATPAK_ID=%s APPIMAGE=%s HOME=%s\n"
        % (env.get("SNAP"), env.get("FLATPAK_ID"), env.get("APPIMAGE"),
           os.path.expanduser("~")))
    return ""


def _wire_string(text, font, size):
    """Part.makeWireString finnes i alle FreeCAD-versjoner, men signaturen varierer."""
    try:
        return Part.makeWireString(text, font, size, 0.0)
    except Exception:
        fdir, fname = os.path.split(font)
        return Part.makeWireString(text, fdir, fname, size, 0.0)


def build_text_shape(text, font, size):
    """Bygger bokstavflater direkte (uten Part::ShapeString-objekt, som ikke
    finnes i nyere FreeCAD). Returnerer (compound, flateliste)."""
    char_wires = _wire_string(text, font, size)
    faces = []
    for wires in char_wires:
        if not wires:          # mellomrom
            continue
        try:
            f = Part.makeFace(wires, "Part::FaceMakerBullseye")  # håndterer hull
            faces.extend(f.Faces)
        except Exception as e:
            App.Console.PrintWarning("Hoppet over et tegn: %s\n" % e)
    if not faces:
        return None, None
    return Part.makeCompound(faces), faces


def make_text_cutter(text, size, depth, cx, cy, z_top, max_width):
    font = find_font()
    if not font:
        App.Console.PrintError(
            "Fant ingen font. Sett FONT_FILE til full sti til en .ttf-fil.\n")
        return None

    shp, faces = build_text_shape(text, font, size)
    if shp is None:
        App.Console.PrintError("ShapeString ga ingen geometri (sjekk font/tekst).\n")
        return None

    width = shp.BoundBox.XMax - shp.BoundBox.XMin
    if width > max_width:
        new_size = size * (max_width / width)
        App.Console.PrintWarning(
            "Teksten er for bred (%.1f mm > %.1f mm). Skalerer ned til %.1f mm.\n"
            % (width, max_width, new_size))
        shp, faces = build_text_shape(text, font, new_size)
        if shp is None:
            return None

    bb = shp.BoundBox
    dx = cx - (bb.XMin + bb.XMax) / 2.0
    dy = cy - (bb.YMin + bb.YMax) / 2.0
    dz = (z_top - depth) - bb.ZMin

    height = depth + 0.5  # stikker 0.5 mm ut over lokket for ren kutt
    solids = [f.extrude(V(0, 0, height)) for f in faces]
    cutter = Part.makeCompound(solids)
    cutter.translate(V(dx, dy, dz))   # <-- DETTE var det som manglet
    return cutter


if LID_TEXT.strip():
    try:
        # Tilgjengelig plass på lokket, utenom fingergrepet
        x_min = WALL_T + 3.0
        x_max = GRIP_X - GRIP_R - 3.0
        avail = x_max - x_min
        cx = (x_min + x_max) / 2.0
        cy = OUTER_W / 2.0

        cutter = make_text_cutter(LID_TEXT, TEXT_SIZE, TEXT_DEPTH,
                                  cx, cy, OUTER_H, avail)
        if cutter is not None:
            before = lid_shape.Volume
            lid_shape = lid_shape.cut(cutter)
            removed = before - lid_shape.Volume
            App.Console.PrintMessage("Tekst frest ut: %.1f mm3 fjernet.\n" % removed)
            if removed < 0.1:
                App.Console.PrintWarning("Teksten traff ikke lokket - sjekk posisjon.\n")
    except Exception as e:
        App.Console.PrintError("Feil ved generering av dynamisk tekst: %s\n" % e)

# ----------------------------------------------------------------------------
# OPPRETT OBJEKTER I FREECAD
# ----------------------------------------------------------------------------
obj_box = doc.addObject("Part::Feature", "Boks_Kropp")
obj_box.Shape = box_shape.removeSplitter()

obj_lid = doc.addObject("Part::Feature", "Skyvelokk")
obj_lid.Shape = lid_shape.removeSplitter()

doc.recompute()

try:
    import FreeCADGui
    FreeCADGui.SendMsgToActiveView("ViewFit")
    FreeCADGui.activeDocument().activeView().viewIsometric()
except Exception:
    pass

App.Console.PrintMessage("Ferdig. Boks med tekst '%s' er opprettet.\n" % LID_TEXT)