# -*- coding: utf-8 -*-
"""
Snap cap (tørrtrenings-/slagsikring-innsats) for 9x19 mm hylse  -  v1.0

Dummy-"prosjektil" som skyves inn i hylsemunningen. Delen består av
  * en sylindrisk tapp (BODY_DIA) som sitter i hylsemunningen,
  * en liten krage/flens (OGIVE_DIA) som hviler mot hylsemunningen,
  * en avrundet nese (ellipse eller tangent-ogive) som gir riktig OAL.

Bygget som ett omdreiningslegeme (revolve) av en 2D-profil, ren Part/OCC.
Printes stående med tappen ned mot byggeplata (ingen støtte nødvendig;
kragen er bare ca. 0.3-0.5 mm overheng).

Antakelser (MÅL på ditt eget hylse og juster!):
  - 9x19: hylse-lengde 19.15, munningens ytre diameter ca. 9.65 mm,
    indre diameter i munningen ca. 8.8-8.9 mm, total OAL ca. 29.7 mm.
  - BODY_DIA er MEASURE: FDM krymper/utvider litt. Print en test med
    TAPP_TEST = True først og tilpass til friksjonspass.
"""
import math
import FreeCAD as App
import Part

try:
    import FreeCADGui as Gui
    HAS_GUI = App.GuiUp
except Exception:
    HAS_GUI = False

V = App.Vector

# ----------------------------------------------------------------------
# PARAMETERE (alle mål i mm)
# ----------------------------------------------------------------------
BODY_DIA      = 8.85   # MEASURE: tappens diameter (hylsens indre dia. i munningen minus klaring)
INSERT_DEPTH  = 7.0    # hvor langt tappen går ned i hylsa
BODY_CHAMFER  = 0.4    # innføringsfas på tappens underkant
OGIVE_DIA     = 9.40   # MEASURE: krage/nese-diameter (litt under hylsens ytre dia. 9.65 så den ikke henger i matingen)
CASE_LENGTH   = 19.15  # 9x19 hylselengde (kun til OAL-beregning)
OAL           = 29.70  # ønsket total patronlengde (hylse + nese)
NOSE_LEN      = None   # None = OAL - CASE_LENGTH (ca. 10.55)
NOSE_SHAPE    = "ELLIPSE"   # "ELLIPSE" (rund, som bildet) eller "TANGENT" (spissere ogive)
PROFILE_PTS   = 48     # antall punkter i nesekurven

TAPP_TEST     = False  # True = kun tappen + en kort nese for rask passtest
EXPORT_DIR    = ""     # tom = ingen eksport, ellers f.eks. "/tmp"

# ----------------------------------------------------------------------
# AVLEDEDE VERDIER
# ----------------------------------------------------------------------
R_BODY = BODY_DIA / 2.0
R_NOSE = OGIVE_DIA / 2.0
L_NOSE = NOSE_LEN if NOSE_LEN is not None else (OAL - CASE_LENGTH)
if TAPP_TEST:
    L_NOSE = min(L_NOSE, 2.5)   # kort nese -> nesten bare tapp + krage


def try_op(label, fn, shape):
    """Kjør en fragil operasjon; ved feil returneres original-formen."""
    try:
        res = fn(shape)
        if res is None or res.isNull():
            raise RuntimeError("tomt resultat")
        return res
    except Exception as e:
        App.Console.PrintWarning("try_op '%s' hoppet over: %s\n" % (label, e))
        return shape


# ----------------------------------------------------------------------
# NESEKURVE  (r(z) fra krage z=0 til tupp z=L_NOSE)
# ----------------------------------------------------------------------
def nose_points():
    pts = []
    n = PROFILE_PTS
    if NOSE_SHAPE.upper() == "TANGENT" and not TAPP_TEST:
        rho = (R_NOSE ** 2 + L_NOSE ** 2) / (2.0 * R_NOSE)   # ogive-radius
        for i in range(n + 1):
            z = L_NOSE * i / n
            r = math.sqrt(max(rho ** 2 - z ** 2, 0.0)) - (rho - R_NOSE)
            pts.append(V(max(r, 0.0), 0, z))
    else:
        for i in range(n + 1):                 # jevn vinkelsampling gir pen tupp
            t = (math.pi / 2.0) * i / n
            pts.append(V(R_NOSE * math.cos(t), 0, L_NOSE * math.sin(t)))
    pts[-1] = V(0, 0, L_NOSE)                  # tuppen skal ligge nøyaktig på aksen
    return pts


# ----------------------------------------------------------------------
# PROFIL + REVOLVE
# ----------------------------------------------------------------------
D = INSERT_DEPTH
ch = min(BODY_CHAMFER, R_BODY * 0.5)

edges = []
edges.append(Part.makeLine(V(0, 0, -D), V(R_BODY - ch, 0, -D)))            # bunn
edges.append(Part.makeLine(V(R_BODY - ch, 0, -D), V(R_BODY, 0, -D + ch)))  # fas
edges.append(Part.makeLine(V(R_BODY, 0, -D + ch), V(R_BODY, 0, 0)))        # tapp
edges.append(Part.makeLine(V(R_BODY, 0, 0), V(R_NOSE, 0, 0)))              # krage
spline = Part.BSplineCurve()
spline.interpolate(nose_points())
edges.append(spline.toShape())                                             # nese
edges.append(Part.makeLine(V(0, 0, L_NOSE), V(0, 0, -D)))                  # akse

wire = Part.Wire(edges)
face = Part.Face(wire)
shape = face.revolve(V(0, 0, 0), V(0, 0, 1), 360)
shape = Part.Solid(shape) if shape.ShapeType == "Shell" else shape

# Flytt slik at underkanten ligger på z=0 (klar for print)
shape.translate(V(0, 0, D))
shape = try_op("removeSplitter", lambda s: s.removeSplitter(), shape)

# ----------------------------------------------------------------------
# DOKUMENT
# ----------------------------------------------------------------------
doc = App.newDocument("SnapCap9mm")
obj = doc.addObject("Part::Feature", "SnapCap9mm")
obj.Shape = shape
doc.recompute()

if HAS_GUI:
    try:
        Gui.ActiveDocument.ActiveView.viewIsometric()
        Gui.SendMsgToActiveView("ViewFit")
    except Exception:
        pass

bb = obj.Shape.BoundBox
App.Console.PrintMessage("Snap cap 9mm: valid=%s  volum=%.1f mm3  BB=%.2f x %.2f x %.2f mm\n"
                         % (obj.Shape.isValid(), obj.Shape.Volume,
                            bb.XLength, bb.YLength, bb.ZLength))
App.Console.PrintMessage("Over hylsemunning: %.2f mm (OAL ~ %.2f mm med hylse %.2f mm)\n"
                         % (L_NOSE, CASE_LENGTH + L_NOSE, CASE_LENGTH))
App.Console.PrintMessage("NEXT: mål hylsas indre dia. i munningen og juster BODY_DIA; "
                         "print TAPP_TEST=True først.\n")

if EXPORT_DIR:
    import os
    import Mesh
    path = os.path.join(EXPORT_DIR, "snap_cap_9mm.stl")
    Mesh.export([obj], path)
    App.Console.PrintMessage("Eksportert: %s\n" % path)
