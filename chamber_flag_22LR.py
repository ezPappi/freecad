# -*- coding: utf-8 -*-
"""
Kammerflagg (chamber safety flag) for S&W Model 41, .22 LR  -  FreeCAD 1.x   (v2)

Utseende etter referansebildet (6.5 Creedmoor-flagget): patronformet plugg bak en tykk blokk,
en hals som går sidelengs ned fra blokken, og et åttekantet "stoppskilt"-flagg med kant og
gjennomskåret tekst ("CLEAR"). Teksten er skåret HELT GJENNOM (sjablong). Bokstaver med
"øyer" (A, R, O, D ...) får automatisk en liten bro, så øya ikke faller ut.

ALLE MÅL ER NOMINELLE .22 LR-MÅL OG ESTIMATER FOR PISTOLEN. Mål utkastvinduet og sleiden på din
pistol (sjekkliste i Report view) og juster parameterne. Print gjerne først bare pluggen
(PLUG_ONLY = True, ca. 10 min) og prøv den i kammeret.

SIKKERHET:
 - Sett inn flagget først etter at du har kontrollert at pistolen er tom (magasin ut, kammer
   sjekket visuelt og med fingeren). Sett aldri inn plast i et varmt kammer.
 - Flagget er et synlig hjelpemiddel, ikke en erstatning for å kontrollere pistolen.

Koordinater: X = langs løpsaksen (patronens bunn/kant ved X = 0, nesen mot +X, blokken bak ved
negativ X), Y = sidelengs ut av utkastvinduet (flagget går mot +Y), Z = opp. Alt ligger flatt
på byggeplaten (Z = 0), så delen printes uten støtte.
"""

import FreeCAD as App
import Part
import math
import os

V = App.Vector

# ----------------------------------------------------------------------------
# BRUKERVALG
# ----------------------------------------------------------------------------
FLAG_TEXT = "CLEAR"        # gjennomskåret tekst ("" = ingen). Prøv også "22LR" eller "SAFE"
TEXT_SIZE = 7.0            # tekststørrelse (skaleres ned automatisk så den passer i flagget)
STENCIL_BRIDGE_W = 1.2     # bredde på broene som holder øyene i A, R, O ... på plass
FONT_FILE = ""             # full sti til .ttf, tom = auto

FLAG_SIDE = "right"        # "right" = utkast på høyre side (S&W 41 standard), "left" = speilvendt
PLUG_ONLY = False          # True = kun patronpluggen (hurtig test av passform i kammeret)
EXPORT_DIR = ""            # sti for STL-eksport, tom = ingen

# --- Patronplugg (nominelle .22 LR-mål, mm) ---
CASE_D = 4.50              # hylsediameter på pluggen (ekte hylse ca. 5.74, kammer ca. 5.8)
RIM_D = 7.00               # kantdiameter (rim er maks ca. 7.06)
RIM_T = 0.40               # kanttykkelse
CASE_L = 20.2              # hylselengde
BULLET_D = 4.50            # kuledelen (litt smalere enn hylsa, gir synlig trinn som på bildet)
OGIVE_START = 20.0         # her begynner den avrundede nesen
PLUG_L = 24.0              # total lengde fra kanten (ekte patron er 25.4)
NOSE_TIP_D = 1.8           # diameter på tuppen
FLAT_CUT = 0.5             # flat bunn på pluggen for å kunne printes liggende

# --- Blokken bak kanten (stopper sleiden, bærer halsen) ---
BLOCK_D = 9.0              # diameter (må få plass bak kammeret når sleiden står bak)
BLOCK_L = 10.0             # lengde bakover fra kanten
BLOCK_GROOVES = True       # to små ringspor, som på referansen

# --- Hals og flagg ---
PLATE_T = 2.0              # tykkelse på hals og flaggkant (må få plass i utkastvinduet)
NECK_W = 9.0               # halsbredde langs X (må være mindre enn utkastvinduets lengde)
NECK_L = 12.0              # fra pluggaksen ut til flaggets underkant (må nå forbi sleidens utside)
NECK_FILLET = 1.5          # avrunding der hals møter flagg
FLAG_AF = 28.0             # åttekantens bredde (mellom parallelle sider)
BORDER_W = 2.5             # bredde på den hevede kanten rundt
FACE_T = 1.2               # tykkelse på selve flaggflaten (der teksten skjæres ut)

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


def octagon_face(af, cx, cy):
    """Regulær åttekant (flate sider opp/ned/sidelengs), 'af' = avstand mellom parallelle sider."""
    R = af / 2.0 / math.cos(math.radians(22.5))
    pts = [V(cx + R * math.cos(math.radians(22.5 + 45 * k)),
             cy + R * math.sin(math.radians(22.5 + 45 * k)), 0) for k in range(8)]
    pts.append(pts[0])
    return Part.Face(Part.makePolygon(pts))


# ----------------------------------------------------------------------------
# GEOMETRI: PATRONPLUGG + BLOKK
# ----------------------------------------------------------------------------
ZC = CASE_D / 2.0 - FLAT_CUT          # akseløyde over byggeplaten
AX = V(1, 0, 0)

rim = Part.makeCylinder(RIM_D / 2.0, RIM_T, V(0, 0, ZC), AX)
case = Part.makeCylinder(CASE_D / 2.0, CASE_L - RIM_T + 0.2, V(RIM_T - 0.1, 0, ZC), AX)
bullet = Part.makeCylinder(BULLET_D / 2.0, OGIVE_START - CASE_L + 0.2, V(CASE_L - 0.1, 0, ZC), AX)

# avrundet kulenese (revolvert profil); faller tilbake til en kjegle ved feil
try:
    r0, r1 = BULLET_D / 2.0, NOSE_TIP_D / 2.0
    L = PLUG_L - OGIVE_START
    mid = V(OGIVE_START + 0.55 * L, r1 + (r0 - r1) * 0.62, 0)
    arc = Part.Arc(V(OGIVE_START, r0, 0), mid, V(PLUG_L, r1, 0)).toShape()
    prof = Part.Wire([Part.makeLine(V(OGIVE_START, 0, 0), V(OGIVE_START, r0, 0)), arc,
                      Part.makeLine(V(PLUG_L, r1, 0), V(PLUG_L, 0, 0)),
                      Part.makeLine(V(PLUG_L, 0, 0), V(OGIVE_START, 0, 0))])
    nose = Part.Face(prof).revolve(V(0, 0, 0), V(1, 0, 0), 360)
    nose.translate(V(0, 0, ZC))
except Exception as e:
    App.Console.PrintWarning("Avrundet nese feilet (%s) - bruker kjegle.\n" % e)
    nose = Part.makeCone(BULLET_D / 2.0, NOSE_TIP_D / 2.0, PLUG_L - OGIVE_START, V(OGIVE_START, 0, ZC), AX)

flag = rim.fuse(case).fuse(bullet).fuse(nose)

if not PLUG_ONLY:
    block = Part.makeCylinder(BLOCK_D / 2.0, BLOCK_L + 0.1, V(-BLOCK_L, 0, ZC), AX)
    if BLOCK_GROOVES:
        for gx in (-BLOCK_L + 2.2, -2.6):
            ring = Part.makeCylinder(BLOCK_D / 2.0 + 1.0, 0.8, V(gx, 0, ZC), AX).cut(
                Part.makeCylinder(BLOCK_D / 2.0 - 0.4, 0.8, V(gx, 0, ZC), AX))
            block = block.cut(ring)
    flag = flag.fuse(block)

flag = flag.cut(Part.makeBox(400, 400, 20, V(-200, -200, -20)))      # flat bunn (Z = 0)

# ----------------------------------------------------------------------------
# GEOMETRI: HALS + ÅTTEKANTET FLAGG MED KANT
# ----------------------------------------------------------------------------
x_n = -BLOCK_L + 1.0 + NECK_W / 2.0          # halsens midtlinje (under venstre del av blokken, som på bildet)
oct_cy = NECK_L + FLAG_AF / 2.0

if not PLUG_ONLY:
    neck = Part.makeBox(NECK_W, NECK_L + 0.5, PLATE_T, V(x_n - NECK_W / 2.0, 0, 0))
    head = octagon_face(FLAG_AF, x_n, oct_cy).extrude(V(0, 0, PLATE_T))
    # innfelt flate: kanten blir stående hevet rundt
    inner = octagon_face(FLAG_AF - 2 * BORDER_W, x_n, oct_cy)
    inner.translate(V(0, 0, FACE_T))
    head = head.cut(inner.extrude(V(0, 0, PLATE_T - FACE_T + 1.0)))

    plate = neck.fuse(head).removeSplitter()
    plate = try_op("Avrunding hals/flagg", lambda s: s.makeFillet(
        NECK_FILLET, [e for e in s.Edges if is_vertical(e)
                      and abs(e.Vertexes[0].Y - NECK_L) < 1e-6
                      and abs(abs(e.Vertexes[0].X - x_n) - NECK_W / 2.0) < 1e-6]), plate)
    flag = flag.fuse(plate)

# ----------------------------------------------------------------------------
# TEKST: GJENNOMSKÅRET (SJABLONG) MED BROER (Part.makeWireString)
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

def make_text_cutter(text, size, z0, z1, cx, cy, max_width, stencil=True):
    """Gjennomskåret tekst fra z0 til z1. Bokstaver med 'øyer' får en bro nedover, så øya ikke faller ut."""
    font = find_font()
    if not font:
        return None
    shp, faces = build_text_shape(text, font, size)
    if shp is None:
        return None

    width = shp.BoundBox.XMax - shp.BoundBox.XMin
    if width > max_width:
        shp, faces = build_text_shape(text, font, size * (max_width / width))
        if shp is None:
            return None

    bb = shp.BoundBox
    dx = cx - (bb.XMin + bb.XMax) / 2.0
    dy = cy - (bb.YMin + bb.YMax) / 2.0
    h = z1 - z0
    solids = []
    n_bridges = 0
    for f in faces:
        sol = f.extrude(V(0, 0, h))
        if stencil:
            try:
                outer = f.OuterWire
                inner = [w for w in f.Wires if not w.isSame(outer)]
            except Exception:
                inner = []
            fb = f.BoundBox
            for w in inner:
                wb = w.BoundBox
                xc = (wb.XMin + wb.XMax) / 2.0
                y_top = (wb.YMin + wb.YMax) / 2.0
                y_bot = fb.YMin - 1.0
                bridge = Part.makeBox(STENCIL_BRIDGE_W, y_top - y_bot, h + 2.0,
                                      V(xc - STENCIL_BRIDGE_W / 2.0, y_bot, -1.0))
                sol = sol.cut(bridge)
                n_bridges += 1
        solids.append(sol)
    cutter = Part.makeCompound(solids)
    cutter.translate(V(dx, dy, z0 - bb.ZMin))
    App.Console.PrintMessage("Tekst '%s': %d bokstavflater, %d broer for øyer.\n" % (text, len(faces), n_bridges))
    return cutter


if FLAG_TEXT.strip() and not PLUG_ONLY:
    try:
        avail = FLAG_AF - 2 * BORDER_W - 3.0
        cutter = make_text_cutter(FLAG_TEXT, TEXT_SIZE, -0.5, PLATE_T + 1.0, x_n, oct_cy, avail)
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
    "2) utkastvinduets lengde (> %.1f mm) og høyde (> %.1f mm), 3) at blokken (%.1f mm tykk, %.1f mm lang) får plass bak kammeret, "
    "4) avstand fra løpsaksen til sleidens utside (< %.1f mm), 5) at sleiden ikke kan gå igjen med flagget i.\n"
    % (CASE_D, NECK_W, PLATE_T, BLOCK_D, BLOCK_L, NECK_L))