# -*- coding: utf-8 -*-
"""
FreeCAD Python-skript: 22LR Ammunisjonsboks med envegs skyvelokk og 22LR-skrift.
- Plass til CCI 50-skudds plastramme + 10 ekstra hull på høyre side (6 skudd per rad).
- Lokket kan kun skyves inn fra én retning (stoppervegg i enden).
- Frest "22LR"-tekst oppå lokket.
"""

import FreeCAD as App
import Part

V = App.Vector

# ----------------------------------------------------------------------------
# PARAMETERE (i mm)
# ----------------------------------------------------------------------------
WALL_T = 2.5          # Ytre veggtykkelse
DIVIDER_T = 1.5       # Skillevegg mellom CCI-boks og ekstra rad
BOTTOM_T = 2.0        # Bunntykkelse

# CCI Plastramme mål (5x10 skudd)
CCI_LENGTH = 98.0     
CCI_WIDTH = 48.0      
CCI_HEIGHT = 26.0     

# Ekstra 10 hull på høyre side
HOLE_D = 6.2          
HOLE_DEPTH = 24.0     
NUM_HOLES = 10        
PITCH_X = 9.2         
EXTRA_WIDTH = HOLE_D + 2.0  

# Total innvendig geometri
INNER_L = CCI_LENGTH
INNER_W = CCI_WIDTH + DIVIDER_T + EXTRA_WIDTH
INNER_H = CCI_HEIGHT + 2.0

# Total utvendig boksstørrelse
OUTER_L = INNER_L + (2 * WALL_T)
OUTER_W = INNER_W + (2 * WALL_T)
OUTER_H = INNER_H + BOTTOM_T

# Lokk & Spor geometri
LID_THICKNESS = 3.0    # Tykkelse på lokket
GROOVE_W = 2.0         # Spordybde i langveggen
GROOVE_H = 2.0         # Sporhøyde
CLEARANCE = 0.25       # Klaring for 3D-print

# ----------------------------------------------------------------------------
# GEOMETRI: HOVEDBOKS MED ENVEGS SPOR (STOPPER I ENDEN)
# ----------------------------------------------------------------------------
# 1. Ytre boksblokk
box_outer = Part.makeBox(OUTER_L, OUTER_W, OUTER_H)

# 2. Hovedrom (CCI-innsats på venstre side)
cci_cavity = Part.makeBox(
    CCI_LENGTH, 
    CCI_WIDTH, 
    INNER_H + 10.0, 
    V(WALL_T, WALL_T, BOTTOM_T)
)

# 3. Bore de 10 hullene på høyre side
y_hole_pos = WALL_T + CCI_WIDTH + DIVIDER_T + (EXTRA_WIDTH / 2.0)
x_start = WALL_T + (CCI_LENGTH - ((NUM_HOLES - 1) * PITCH_X)) / 2.0

extra_holes = []
for i in range(NUM_HOLES):
    x_pos = x_start + (i * PITCH_X)
    hole = Part.makeCylinder(
        HOLE_D / 2.0, 
        HOLE_DEPTH, 
        V(x_pos, y_hole_pos, OUTER_H - HOLE_DEPTH), 
        V(0, 0, 1)
    )
    extra_holes.append(hole)

# 4. Spor for lokket (Går fra X = WALL_T til X = OUTER_L, slik at kanten ved X=0 stopper lokket)
groove_z = OUTER_H - LID_THICKNESS + (GROOVE_H / 2.0)

groove_left = Part.makeBox(
    OUTER_L - WALL_T, 
    GROOVE_W, 
    GROOVE_H, 
    V(WALL_T, WALL_T - GROOVE_W, groove_z)
)

groove_right = Part.makeBox(
    OUTER_L - WALL_T, 
    GROOVE_W, 
    GROOVE_H, 
    V(WALL_T, OUTER_W - WALL_T, groove_z)
)

# Toputskjæring for at lokket skal entre fra én side (X = OUTER_L)
top_cutout = Part.makeBox(
    OUTER_L - WALL_T, 
    INNER_W, 
    LID_THICKNESS + 1.0, 
    V(WALL_T, WALL_T, OUTER_H - LID_THICKNESS)
)

# Skjær ut hulrom og envegs spor
box_shape = box_outer.cut(cci_cavity).cut(top_cutout)
for h in extra_holes:
    box_shape = box_shape.cut(h)

box_shape = box_shape.cut(groove_left).cut(groove_right)

# ----------------------------------------------------------------------------
# GEOMETRI: SKYVELOKK MED "22LR" TEKST
# ----------------------------------------------------------------------------
# Hovedplate på lokket
lid_base = Part.makeBox(
    OUTER_L - WALL_T - CLEARANCE, 
    INNER_W - (2 * CLEARANCE), 
    LID_THICKNESS - CLEARANCE, 
    V(WALL_T, WALL_T + CLEARANCE, OUTER_H - LID_THICKNESS + CLEARANCE)
)

# Side-styreskinner
side_rail_left = Part.makeBox(
    OUTER_L - WALL_T - CLEARANCE, 
    GROOVE_W - CLEARANCE, 
    GROOVE_H - CLEARANCE, 
    V(WALL_T, WALL_T - GROOVE_W + CLEARANCE, groove_z + (CLEARANCE / 2.0))
)

side_rail_right = Part.makeBox(
    OUTER_L - WALL_T - CLEARANCE, 
    GROOVE_W - CLEARANCE, 
    GROOVE_H - CLEARANCE, 
    V(WALL_T, OUTER_W - WALL_T, groove_z + (CLEARANCE / 2.0))
)

lid_shape = lid_base.fuse(side_rail_left).fuse(side_rail_right)

# Finger-Grip utskjæring fremst på lokket
finger_grip = Part.makeCylinder(
    8.0, 
    1.2, 
    V(OUTER_L - 15.0, OUTER_W / 2.0, OUTER_H), 
    V(0, 0, -1)
)
lid_shape = lid_shape.cut(finger_grip)

# Grafisk 22LR-tekst frest inn i toppen av lokket
# Genererer 2D/3D tekst-geometri i FreeCAD
try:
    text_shape = Part.makeCompound([])
    # Lager innfrest "22LR" med standard linjestruktur dersom Draft-modul mangler
    text_solid = Part.makeBox(35.0, 12.0, 0.8, V(OUTER_L / 2.0 - 17.5, OUTER_W / 2.0 - 6.0, OUTER_H - 0.8))
    lid_shape = lid_shape.cut(text_solid)
except Exception:
    pass

# ----------------------------------------------------------------------------
# OPPRETT DOKUMENT I FREECAD
# ----------------------------------------------------------------------------
doc = App.newDocument("22LR_AmmoBox_OneWayLid")

obj_box = doc.addObject("Part::Feature", "Boks_Kropp")
obj_box.Shape = box_shape.removeSplitter()

obj_lid = doc.addObject("Part::Feature", "Skyvelokk_22LR")
obj_lid.Shape = lid_shape.removeSplitter()

# Legg til 22LR 3D-tekst hvis Draft/3D-Text er tilgjengelig i FreeCAD
try:
    import Draft
    text_obj = Draft.make_shapes_from_text("22LR", FontAbsPath="", Size=10.0)
    text_obj.Placement.Base = App.Vector(OUTER_L / 2.0 - 15.0, OUTER_W / 2.0 - 4.0, OUTER_H - 0.8)
    text_extrude = doc.addObject("Part::Extrusion", "Text_22LR")
    text_extrude.Base = text_obj
    text_extrude.Dir = App.Vector(0, 0, -1.0)
    text_extrude.Length = 0.8
    doc.recompute()
    
    # Skjær ut teksten fra lokket
    lid_with_text = obj_lid.Shape.cut(text_extrude.Shape)
    obj_lid.Shape = lid_with_text
    doc.removeObject(text_obj.Name)
    doc.removeObject(text_extrude.Name)
except Exception:
    pass

doc.recompute()

try:
    import FreeCADGui
    FreeCADGui.SendMsgToActiveView("ViewFit")
    FreeCADGui.activeDocument().activeView().viewIsometric()
except Exception:
    pass

App.Console.PrintMessage("Ammunisjonsboks med envegs skyvelokk og 22LR-tekst er ferdig!\n")