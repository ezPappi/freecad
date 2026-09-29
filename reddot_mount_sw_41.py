# -*- coding: utf-8 -*-
"""
Red dot mount plate for Smith & Wesson Model 41 (EGW-style, dovetail-key underside)
FreeCAD Python script - run via  Macro > Macros...  or paste into the Python console.

All dimensions below are in INCHES (taken from the dimensioned side-view photo)
and converted to mm for FreeCAD.

Coordinate system
    X = along the slide/rib (left end of the side-view photo = X 0)
    Y = across the plate (centered on 0)
    Z = up.  Z = 0 is the underside of the MIDDLE section (the part that
        sits on the gun); the dovetail key projects downward to Z = -0.100"
        and the flat top face of the plate is at Z = PLATE_TOP.

!! Values marked (ESTIMATE) were scaled from photos, not from a drawing.
!! Verify against your gun and your optic before machining / printing.
"""

import FreeCAD as App
import Part
from FreeCAD import Vector

IN = 25.4  # inch -> mm


def mm(v):
    return v * IN


# ----------------------------------------------------------------------
# Dimensions taken directly from the annotated side-view photo (inches)
# ----------------------------------------------------------------------
STEP_LEFT = 0.095      # left (thin) section's underside sits this far ABOVE the middle underside
STEP_RIGHT = 0.062     # right section's underside sits this far above the middle underside
LEN_A = 0.198          # full-depth stretch between left step and dovetail
LEN_B = 0.313          # full-depth stretch between dovetail and right step
KEY_BOTTOM_W = 0.430   # dovetail key width at its bottom
KEY_H = 0.100          # dovetail key height

# ----------------------------------------------------------------------
# Dimensions scaled from the photos (ESTIMATES)
# ----------------------------------------------------------------------
KEY_TOP_W = 0.393      # key width where it meets the plate (ESTIMATE)
PLATE_L = 1.70         # overall length along the gun (ESTIMATE)
PLATE_W = 1.10         # overall width across the gun (ESTIMATE)
PLATE_TOP = 0.215      # top face height above the middle underside (ESTIMATE)
RIGHT_LEN = 0.22       # length of the thin right-hand section (ESTIMATE)

CORNER_R = 0.05        # vertical corner fillet (ESTIMATE)

# Locating pads on top face (the 4 small round nubs)
PAD_D = 0.10           # (ESTIMATE)
PAD_H = 0.030          # (ESTIMATE)
PAD_INSET = 0.09       # from plate edges to pad centre (ESTIMATE)

# Optic screw holes - three holes, roughly in a row across the width.
# Positions are (X offset from key centre, Y from plate centre)  (ESTIMATE, from photo)
# Check against your optic's footprint (Vortex Viper/Venom, Burris FastFire).
HOLE_D = 0.120         # ~#31 tap drill for 6-48. Change for your screw (ESTIMATE)
# Measured from the underside photo (a2.jpg): the pattern is SYMMETRIC about the
# plate centreline. Outer holes are ~0.60 in apart (+/-0.30 in), the centre hole
# sits on the centreline and ~0.04 in closer to the left (thin) end than the outer two.
HOLES = [
    (0.05, -0.30),   # outer hole
    (0.01, 0.00),    # centre hole (slightly offset in X)
    (0.05, 0.30),    # outer hole
]

EXPORT_FILES = False   # set True to write STEP + STL next to your FreeCAD home dir


# ----------------------------------------------------------------------
# Derived values
# ----------------------------------------------------------------------
z_left = STEP_LEFT
z_right = STEP_RIGHT
mid_len = LEN_A + KEY_TOP_W + LEN_B
left_len = PLATE_L - mid_len - RIGHT_LEN
if left_len <= 0:
    raise ValueError("Plate length too short for the given section lengths")

x_step_left = left_len
x_key0 = x_step_left + LEN_A          # key starts (top edge)
x_key1 = x_key0 + KEY_TOP_W           # key ends (top edge)
x_step_right = x_key1 + LEN_B
flare = (KEY_BOTTOM_W - KEY_TOP_W) / 2.0

# ----------------------------------------------------------------------
# Side profile (XZ plane), extruded across Y
# ----------------------------------------------------------------------
profile_pts_in = [
    (0.0, z_left),
    (x_step_left, z_left),
    (x_step_left, 0.0),
    (x_key0, 0.0),
    (x_key0 - flare, -KEY_H),
    (x_key1 + flare, -KEY_H),
    (x_key1, 0.0),
    (x_step_right, 0.0),
    (x_step_right, z_right),
    (PLATE_L, z_right),
    (PLATE_L, PLATE_TOP),
    (0.0, PLATE_TOP),
]
pts = [Vector(mm(x), 0, mm(z)) for x, z in profile_pts_in]
pts.append(pts[0])

wire = Part.makePolygon(pts)
face = Part.Face(wire)
body = face.extrude(Vector(0, mm(PLATE_W), 0))
body.translate(Vector(0, -mm(PLATE_W) / 2.0, 0))

# ----------------------------------------------------------------------
# Round the four vertical corners of the plate
# ----------------------------------------------------------------------
try:
    corner_edges = []
    tol = 1e-6
    for e in body.Edges:
        v0, v1 = e.Vertexes[0].Point, e.Vertexes[-1].Point
        vertical = abs(v0.x - v1.x) < tol and abs(v0.y - v1.y) < tol and abs(v0.z - v1.z) > tol
        on_x_end = abs(v0.x) < tol or abs(v0.x - mm(PLATE_L)) < tol
        on_y_side = abs(abs(v0.y) - mm(PLATE_W) / 2.0) < tol
        if vertical and on_x_end and on_y_side:
            corner_edges.append(e)
    if corner_edges:
        body = body.makeFillet(mm(CORNER_R), corner_edges)
except Exception as err:  # fillet is cosmetic; never block the model
    App.Console.PrintWarning("Corner fillet skipped: %s\n" % err)

# ----------------------------------------------------------------------
# Locating pads on the top face
# ----------------------------------------------------------------------
pad_x = [PAD_INSET, PLATE_L - PAD_INSET]
pad_y = [-(PLATE_W / 2.0 - PAD_INSET), PLATE_W / 2.0 - PAD_INSET]
for px in pad_x:
    for py in pad_y:
        pad = Part.makeCylinder(
            mm(PAD_D / 2.0), mm(PAD_H),
            Vector(mm(px), mm(py), mm(PLATE_TOP)), Vector(0, 0, 1))
        body = body.fuse(pad)

# ----------------------------------------------------------------------
# Screw holes (through, from top face through the key)
# ----------------------------------------------------------------------
key_center_x = (x_key0 + x_key1) / 2.0
for dx, y in HOLES:
    hole = Part.makeCylinder(
        mm(HOLE_D / 2.0), mm(PLATE_TOP + KEY_H + 0.2),
        Vector(mm(key_center_x + dx), mm(y), mm(-KEY_H - 0.1)), Vector(0, 0, 1))
    body = body.cut(hole)

body = body.removeSplitter()

# ----------------------------------------------------------------------
# Add to document
# ----------------------------------------------------------------------
doc = App.newDocument("SW_M41_RedDot_Mount")
obj = doc.addObject("Part::Feature", "M41_RDS_Mount")
obj.Shape = body
doc.recompute()

if App.GuiUp:
    import FreeCADGui as Gui
    Gui.ActiveDocument.ActiveView.viewIsometric()
    Gui.SendMsg("View.ViewFit")

if EXPORT_FILES:
    import os, Mesh
    out = os.path.join(App.getUserAppDataDir(), "M41_RDS_Mount")
    Part.export([obj], out + ".step")
    Mesh.export([obj], out + ".stl")
    App.Console.PrintMessage("Exported to %s.step/.stl\n" % out)

App.Console.PrintMessage(
    "Plate %.2f x %.2f in, height %.3f in (+%.3f in key). Volume %.1f mm3\n"
    % (PLATE_L, PLATE_W, PLATE_TOP, KEY_H, body.Volume))