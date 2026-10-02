# -*- coding: utf-8 -*-
"""
Hämmerli 208 - Framsiden (Frontprofil)
Basert nøyaktig på bildet og måleskissen.
"""
import FreeCAD as App
import Part

V = App.Vector

# ----------------------------------------------------------------------------
# MÅL HENTET FRA SKISSE OG BILDE (mm)
# ----------------------------------------------------------------------------
W = 26.5           # Total bredde nederst (fra skisse)
D = 28.7           # Dybde / lengde
H = 34.7           # Høyde til toppflaten (uten sikteblad)

# Tunnel / U-bue
ARCH_W = 22.5     # Bredde på tunnelen
ARCH_BOTTOM = 10.7 # Høyde fra bunn opp til start av buen
ARCH_TOP = 26.4    # Høyde til topp av buen

# Festetapp i midten (framside)
TAB_W = 10.7       # Bredde på tappen
TAB_T = 3.5        # Tykkelse i dybden (Y)
TAB_H = 10.7       # Høyde på tappen fra bunnen
HOLE_D = 3.5       # Gjennomgående skruehull
CSINK_D = 7.0      # Forsenkning for skruehode
CSINK_DEPTH = 1.8  # Dybde på forsenkning
HOLE_Z = 7.0       # Senterhøyde for skruen

# Sideslisser (åpningene på sidene av tappen)
SLOT_W = 5.0       # Bredde på utskjæringene
SLOT_X = 8.25      # Sentral plassering på X-aksen
SLOT_Z0 = 1.5
SLOT_Z1 = 10.2

# Ytre fas/skråkant nederst (se bilde)
BOTTOM_CHAMFER = 2.0
STEP_W = 1.0       # Innsnevring på yttersiden midt på kroppen

EXPORT_STL = False
STL_PATH = "/tmp/haemmerli208_front_face.stl"

# ----------------------------------------------------------------------------
# GEOMETRI (PART SOLIDS)
# ----------------------------------------------------------------------------
Y_DIR = V(0, 1, 0)

# 1. Hovedkropp (Blokk)
body = Part.makeBox(W, D, H, V(-W / 2, 0, 0))

# 2. Ytre fas nederst på sidene (Chamfers på bunnhjørnene som vist på bildet)
bc_l = Part.makeBox(BOTTOM_CHAMFER * 2, D + 2, BOTTOM_CHAMFER * 2, V(-W / 2 - BOTTOM_CHAMFER, -1, -BOTTOM_CHAMFER))
bc_l.rotate(V(-W / 2, 0, 0), Y_DIR, 45)

bc_r = Part.makeBox(BOTTOM_CHAMFER * 2, D + 2, BOTTOM_CHAMFER * 2, V(W / 2 - BOTTOM_CHAMFER, -1, -BOTTOM_CHAMFER))
bc_r.rotate(V(W / 2, 0, 0), Y_DIR, -45)

shape = body.cut(bc_l).cut(bc_r)

# 3. Ytre innsnevring (Trinn på siden som smalner av delen mot toppen)
step_l = Part.makeBox(STEP_W, D + 2, H - 10.0, V(-W / 2, -1, 10.0))
step_r = Part.makeBox(STEP_W, D + 2, H - 10.0, V(W / 2 - STEP_W, -1, 10.0))
shape = shape.cut(step_l).cut(step_r)

# 4. Hovedtunnel (U-formet bue som går gjennom delen)
r = ARCH_W / 2.0
zc = ARCH_TOP - r
arch_box = Part.makeBox(ARCH_W, D + 2, zc - ARCH_BOTTOM, V(-r, -1, ARCH_BOTTOM))
arch_cyl = Part.makeCylinder(r, D + 2, V(0, -1, zc), Y_DIR)
tunnel = arch_box.fuse(arch_cyl)

shape = shape.cut(tunnel)

# 5. Sideslisser (Utskårede rom på venstre og høyre side i tunnelen)
for sx in (-SLOT_X, SLOT_X):
    sr = SLOT_W / 2.0
    sbox = Part.makeBox(SLOT_W, D + 2, SLOT_Z1 - SLOT_Z0 - 2 * sr, V(sx - sr, -1, SLOT_Z0 + sr))
    c_lo = Part.makeCylinder(sr, D + 2, V(sx, -1, SLOT_Z0 + sr), Y_DIR)
    c_hi = Part.makeCylinder(sr, D + 2, V(sx, -1, SLOT_Z1 - sr), Y_DIR)
    shape = shape.cut(sbox.fuse(c_lo).fuse(c_hi))

# 6. Innvendig festetapp i forkant (med forsenket skruehull)
tab = Part.makeBox(TAB_W, TAB_T, TAB_H, V(-TAB_W / 2.0, 0, 0))

# Skruehull gjennom tappen
screw_hole = Part.makeCylinder(HOLE_D / 2.0, TAB_T + 2, V(0, -1, HOLE_Z), Y_DIR)

# Forsenkning på framsiden av tappen
screw_csink = Part.makeCylinder(CSINK_D / 2.0, CSINK_DEPTH + 1, V(0, -1, HOLE_Z), Y_DIR)
screw_cone = Part.makeCone(CSINK_D / 2.0, HOLE_D / 2.0, (CSINK_D - HOLE_D) / 2.0, V(0, CSINK_DEPTH, HOLE_Z), Y_DIR)

tab = tab.cut(screw_hole).cut(screw_csink).cut(screw_cone)

# Legg tappen til på framsiden
shape = shape.fuse(tab)
shape = shape.removeSplitter()

# ----------------------------------------------------------------------------
# OPPRETT I FREECAD
# ----------------------------------------------------------------------------
doc = App.newDocument("Haemmerli208_FrontFace")
obj = doc.addObject("Part::Feature", "Front_Face")
obj.Shape = shape
doc.recompute()

try:
    import FreeCADGui
    FreeCADGui.SendMsgToActiveView("ViewFit")
    FreeCADGui.activeDocument().activeView().viewFront()  # Setter visningen rett mot framsiden
except Exception:
    pass

if EXPORT_STL:
    import Mesh
    Mesh.export([obj], STL_PATH)
    App.Console.PrintMessage("Eksportert: %s\n" % STL_PATH)

App.Console.PrintMessage("Framsiden er generert! Volum: %.1f mm3\n" % shape.Volume)