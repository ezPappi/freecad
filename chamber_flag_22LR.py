# -*- coding: utf-8 -*-
"""
Kammerflagg (chamber safety flag) for S&W Model 41, .22 LR  -  FreeCAD 1.x

Hva det er: en "patronplugg" som legges i kammeret gjennom utkastvinduet, med en flat flaggplate
som stikker ut av vinduet. Flagget viser at kammeret er tomt og hindrer at sleiden går igjen.
Modellen bygger på samme prinsipp som AR-15-flagget det ble vist til (patronformet plugg + flagg),
men er tilpasset .22 LR.

ALLE MÅL ER NOMINELLE .22 LR-MÅL OG ESTIMATER FOR PISTOLEN. Mål utkastvinduet og sleiden på din
egen pistol (se sjekklisten i Report view) og juster parameterne. Print gjerne først bare pluggen
(PLUG_ONLY = True, ca. 10 min) og prøv den i kammeret.

SIKKERHET:
 - Sett inn flagget først etter at du har kontrollert at pistolen er tom (magasin ut, kammer
   sjekket visuelt og med fingeren).
 - Sett aldri inn plast i et varmt kammer.
 - Flagget er et synlig hjelpemiddel, ikke en erstatning for å kontrollere pistolen.

Koordinater: X = langs løpsaksen (bunnflaten/kanten på pluggen ved X = 0, nesen mot +X),
Y = sidelengs ut av utkastvinduet (flagget går mot +Y), Z = opp. Flaggplaten ligger flatt på
byggeplaten (Z = 0), så delen printes uten støtte.
"""

import FreeCAD as App
import Part
import os

V = App.Vector

# ----------------------------------------------------------------------------
# BRUKERVALG
# ----------------------------------------------------------------------------
FLAG_TEXT = "22LR"         # tekst gravert i flagget ("" = ingen)
TEXT_SIZE = 7.0            # tekststørrelse (skaleres ned automatisk)
TEXT_DEPTH = 0.6           # graveringsdybde
FONT_FILE = ""             # full sti til .ttf, tom = auto

FLAG_SIDE = "right"        # "right" = utkast på høyre side (S&W 41 standard), "left" = speilvendt
PLUG_ONLY = False          # True = kun pluggen (hurtig test av passform i kammeret)
EXPORT_DIR = ""            # sti for STL-eksport, tom = ingen

# --- Plugg i kammeret (nominelle .22 LR-mål, mm) ---
CASE_D = 5.50              # pluggdiameter (hylse ca. 5.74, kammer ca. 5.8). 0,2-0,3 mm under gir lett innsetting
RIM_D = 7.00               # kantdiameter (rim er maks ca. 7.06)
RIM_T = 1.10               # kanttykkelse
CASE_L = 15.6              # kroppslengde (hylselengde)
PLUG_L = 21.0              # total pluggslengde fra kanten (patron er 25.4; litt kortere nese)
NOSE_TIP_D = 3.2           # diameter på tuppen av nesen
FLAT_CUT = 0.5             # flat bunn for å kunne printes liggende (mm kuttet av sylinderen)

# --- Flaggplate (ligger flatt, går ut av utkastvinduet) ---
PLATE_T = 2.0              # platetykkelse (må få plass i utkastvinduet sammen med sleidekanten)
NECK_X0 = -6.0             # halsens start langs X relativt til kanten (negativ = bak kanten)
NECK_W = 14.0              # halsens bredde langs X (må være mindre enn utkastvinduets lengde)
NECK_L = 14.0              # fra pluggaksen og ut til flaggets hode (må nå forbi sleidens utside)
HEAD_W = 28.0              # hodets bredde langs X
HEAD_L = 16.0              # hodets lengde sidelengs
HEAD_FILLET = 5.0          # avrunding av hodets ytre hjørner
NECK_FILLET = 2.0          # avrunding der hals møter hode
LANYARD_D = 3.0            # hull til snor/paracord (0 = ingen)

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


def is_vertical(e):
    return abs(e.Vertexes[0].Z - e.Vertexes[-1].Z) > 1e-6


# ----------------------------------------------------------------------------
# GEOMETRI: PLUGG
# ----------------------------------------------------------------------------
ZC = CASE_D / 2.0 - FLAT_CUT          # pluggaksens høyde over byggeplaten
AX = V(1, 0, 0)

rim = Part.makeCylinder(RIM_D / 2.0, RIM_T, V(0, 0, ZC), AX)
body = Part.makeCylinder(CASE_D / 2.0, CASE_L - RIM_T + 0.2, V(RIM_T - 0.1, 0, ZC), AX)
nose = Part.makeCone(CASE_D / 2.0, NOSE_TIP_D / 2.0, PLUG_L - CASE_L, V(CASE_L, 0, ZC), AX)
flag = rim.fuse(body).fuse(nose)
flag = flag.cut(Part.makeBox(400, 400, 20, V(-200, -200, -20)))      # flat bunn (Z = 0)

# ----------------------------------------------------------------------------
# GEOMETRI: FLAGGPLATE
# ----------------------------------------------------------------------------
x_c = NECK_X0 + NECK_W / 2.0
if not PLUG_ONLY:
    neck = Part.makeBox(NECK_W, NECK_L + 0.5, PLATE_T, V(NECK_X0, 0, 0))
    head = Part.makeBox(HEAD_W, HEAD_L, PLATE_T, V(x_c - HEAD_W / 2.0, NECK_L, 0))
    plate = neck.fuse(head).removeSplitter()

    y_end = NECK_L + HEAD_L
    plate = try_op("Avrunding hodet", lambda s: s.makeFillet(
        HEAD_FILLET, [e for e in s.Edges if is_vertical(e) and abs(e.Vertexes[0].Y - y_end) < 1e-6]), plate)
    plate = try_op("Avrunding hals/hode", lambda s: s.makeFillet(
        NECK_FILLET, [e for e in s.Edges if is_vertical(e) and abs(e.Vertexes[0].Y - NECK_L) < 1e-6]), plate)

    if LANYARD_D > 0:
        plate = plate.cut(Part.makeCylinder(LANYARD_D / 2.0, PLATE_T + 2.0,
                                            V(x_c, y_end - 3.5, -1.0), V(0, 0, 1)))
    flag = flag.fuse(plate)

# ----------------------------------------------------------------------------
# TEKST (Part.makeWireString)
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



if FLAG_TEXT.strip() and not PLUG_ONLY:
    try:
        y_end = NECK_L + HEAD_L
        text_cx = x_c
        text_cy = NECK_L + HEAD_L * 0.40            # litt under midten, så det ikke kolliderer med snorhullet
        avail = HEAD_W - 2 * 4.0
        cutter = make_text_cutter(FLAG_TEXT, TEXT_SIZE, TEXT_DEPTH, text_cx, text_cy, PLATE_T, avail)
        if cutter is not None:
            flag = flag.cut(cutter)
        else:
            App.Console.PrintWarning("Ingen font funnet - flagget lages uten tekst (sett FONT_FILE).\n")
    except Exception as e:
        App.Console.PrintError("Feil ved tekstgenerering: %s\n" % e)

# ----------------------------------------------------------------------------
# FERDIG DEL
# ----------------------------------------------------------------------------
flag = flag.removeSplitter()
if FLAG_SIDE.lower() == "left":
    flag = flag.mirror(V(0, 0, 0), V(0, 1, 0))      # speil om XZ-planet: flagget peker mot -Y

doc = App.newDocument("Kammerflagg_SW41_22LR")
obj = doc.addObject("Part::Feature", "Kammerflagg")
obj.Shape = flag
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
        Mesh.export([obj], os.path.join(EXPORT_DIR, "kammerflagg_sw41_22lr.stl"))
        App.Console.PrintMessage("STL eksportert til %s\n" % EXPORT_DIR)
    except Exception as e:
        App.Console.PrintError("STL-eksport feilet: %s\n" % e)

bb = flag.BoundBox
App.Console.PrintMessage(
    "Kammerflagg (%s): %.1f x %.1f x %.1f mm, gyldig=%s, volum %.2f cm3.\n"
    % ("kun plugg" if PLUG_ONLY else FLAG_SIDE, bb.XLength, bb.YLength, bb.ZLength, flag.isValid(), flag.Volume / 1000.0))
App.Console.PrintMessage(
    "SJEKKLISTE (mål på din pistol): 1) kammerdiameter (skal være > %.2f mm) og at pluggen går lett inn, "
    "2) utkastvinduets lengde (> %.1f mm) og høyde (> %.1f mm), 3) avstand fra løpsaksen til sleidens utside "
    "(< %.1f mm), 4) at sleiden ikke kan gå igjen med flagget i.\n"
    % (CASE_D, NECK_W, PLATE_T, NECK_L))