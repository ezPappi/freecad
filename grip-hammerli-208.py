# -*- coding: utf-8 -*-
"""
Hämmerli 208 - anatomical target grip (Nill style), left/right halves  -  FreeCAD 1.x, parametric   (v2)

v2 changes, from your measurements:
 - The square TENON on each inner face (55.2 x 22.2 mm, top edge 21.7 mm below the top of the grip) is modelled
   toward the FRONT: its front side is 4 mm behind the front edge and its rear side 11.7 mm in front of the
   rear wall of the pocket (zigzag cut-in), so the pocket is 37.9 mm deep from the front edge.
   It stands out from the pocket floor toward the metal grip (PAD_PROTRUSION, MEASURE).
 - The grip is OPEN AT THE FRONT: the frame pocket runs out through the front edge, so the metal grip's front
   is exposed between the halves. Only the rear is closed (the halves meet there).

How it is built:
 1. SIDE OUTLINE: traced from the outer-face photo. One number (GRIP_HEIGHT_MM) scales it to mm.
 2. CROSS SECTION: a loft of ellipses (WIDTH_PROFILE), shifted forward (FRONT_BIAS) so the open front edge keeps
    wood thickness, intersected with the outline.
 3. Each half: frame pocket on the inner face (open to the front), tenon, recessed checkering panel, two screws.
    The left half is a mirror of the right.

!! The outline is a trace of a photo and the pocket depth, pocket rear wall and screw positions are estimates.
   Check the fit with PRINT_TEST before printing a whole grip.
"""

import FreeCAD as App
import Part
import math

V = App.Vector
try:
    import FreeCADGui as Gui
    HAS_GUI = True
except ImportError:
    HAS_GUI = False

# ----------------------------------------------------------------------------
# PARAMETERS (mm)
# ----------------------------------------------------------------------------
GRIP_HEIGHT_MM = 112.0     # MEASURE: real height of the grip from top to heel (scales the whole traced outline)

# total grip width (both halves together) as (fraction of height from the heel, width). Interpolated.
WIDTH_PROFILE = [(0.00, 38.0), (0.20, 44.0), (0.50, 48.0), (0.80, 52.0), (1.00, 52.0)]
EDGE_FULLNESS = 1.06       # >1 = blunter/rounder front and back straps, closer to 1 = sharper

# metal grip between the halves (MEASURE)
FRAME_W = 16.0             # thickness of the metal grip where the halves sit on it (pocket floor is at +/- half of this)

# the square tenon that plugs into the metal grip (your measurements)
PAD_L, PAD_W = 55.2, 22.2  # long side (along the grip) x short side (front-to-back)
PAD_TOP_DROP = 21.7        # from the top of the grip down to the top edge of the tenon
PAD_R = 4.0                # corner radius
PAD_PROTRUSION = 3.0       # how far the tenon stands out from the pocket floor (MEASURE: depth of the hole in the metal grip)

# the pocket (zigzag cut-in) is open at the front. Its rear wall follows from your measurements:
PAD_FRONT_INSET = 4.0      # tenon front side  -> front edge of the grip
PAD_TO_POCKET_WALL = 11.7  # tenon rear side   -> rear wall (back edge) of the pocket
#   => pocket depth from the front edge = 4.0 + 22.2 + 11.7 = 37.9 mm
PAD_X_SHIFT = 0.0          # extra shift of the tenon forward (+) / back (-) along the grip
UPPER_START_FRAC = 0.58    # from this height up the pocket may be deeper (tang / trigger-guard clearance)
UPPER_EXTRA_BACK = 0.0     # how much deeper toward the rear in that upper part (0 = same as below)
FRONT_BIAS = 0.10          # moves the swell forward so the open front edge keeps thickness (0 = symmetric)

# screws, one per hole: positions taken from the photo (pixels) - MEASURE/adjust for your frame
SCREW_PX = [(832, 488), (1030, 850)]
SCREW_D = 3.4              # M3 clearance
HEAD_D, HEAD_DEPTH = 6.4, 3.0

# recessed checkering panel with border
PANEL = True
PANEL_FLAT_Y = 21.0        # half-thickness at the panel floor (smaller = deeper recess)
CHECKERING = True          # diamond checkering (slower to compute: set False for a quick preview)
CHECKER_PITCH = 2.0        # mm between grooves (0.4 mm nozzle: 1.6 - 2.4 works)
CHECKER_DEPTH = 0.45

LAYOUT = "print"           # "print" = halves flat on their inner faces, "assembled" = as on the gun
SHOW_FRAME_REF = True
PRINT_TEST = False         # True = only the lowest 35 mm, for a fit test
EXPORT_DIR = ""

# ----------------------------------------------------------------------------
# TRACED OUTLINE (photo pixels, front is on the LEFT in the photo; x is flipped so front = +X)
# ----------------------------------------------------------------------------
OUTLINE = [
    ("L", [(365, 72), (500, 68), (620, 62)]),
    ("S", [(620, 62), (655, 78), (700, 86), (745, 78), (775, 64)]),                       # thumb/trigger-guard scoop
    ("L", [(775, 64), (990, 50)]),
    ("S", [(990, 50), (1004, 95), (1010, 128), (985, 160), (938, 178), (905, 205), (898, 228), (912, 248)]),  # rear hook
    ("S", [(912, 248), (940, 300), (990, 400), (1060, 560), (1110, 690), (1160, 830), (1205, 985)]),          # rear edge
    ("L", [(1205, 985), (615, 990)]),                                                     # heel
    ("S", [(615, 990), (590, 900), (562, 800), (548, 700), (543, 600), (540, 480), (538, 390)]),               # front edge
    ("S", [(538, 390), (515, 350), (470, 336), (442, 325)]),                              # underside of front shelf
    ("S", [(442, 325), (436, 290), (415, 200), (385, 125), (365, 72)]),                   # front of shelf
]
PANEL_PX = [(560, 392), (640, 368), (720, 358), (800, 380), (875, 420), (940, 470), (995, 540), (1040, 620),
            (1085, 740), (1125, 860), (1170, 960), (1140, 968), (640, 972), (578, 900), (565, 800), (560, 700),
            (558, 600), (556, 490)]

PX_TOP, PX_BOTTOM, X_REF = 50.0, 990.0, 800.0
S = GRIP_HEIGHT_MM / (PX_BOTTOM - PX_TOP)       # mm per pixel
H = (PX_BOTTOM - PX_TOP) * S


def P(px, py, y=0.0):
    return V((X_REF - px) * S, y, (PX_BOTTOM - py) * S)


def try_op(label, fn, shape):
    try:
        r = fn(shape)
        if r.isValid() and not r.isNull():
            return r
        App.Console.PrintWarning("%s gave invalid geometry - skipped.\n" % label)
    except Exception as e:
        App.Console.PrintWarning("%s failed (%s) - skipped.\n" % (label, e))
    return shape


# ----------------------------------------------------------------------------
# 1. OUTLINE WIRE + helper: front/rear x at a given height
# ----------------------------------------------------------------------------
edges = []
for kind, pts in OUTLINE:
    vs = [P(*p) for p in pts]
    if kind == "L":
        edges += Part.makePolygon(vs).Edges
    else:
        bs = Part.BSplineCurve()
        bs.interpolate(vs)
        edges.append(bs.toShape())
outline_wire = Part.Wire(edges)
outline_pts = outline_wire.discretize(Number=600)


def x_range(z):
    z = min(max(z, 0.5), H - 0.5)
    xs = []
    for a, b in zip(outline_pts, outline_pts[1:] + outline_pts[:1]):
        if (a.z - z) * (b.z - z) <= 0 and abs(b.z - a.z) > 1e-9:
            xs.append(a.x + (b.x - a.x) * (z - a.z) / (b.z - a.z))
    return (min(xs), max(xs)) if xs else (0.0, 0.0)       # (rear, front)


def width_at(z):
    f = min(max(z / H, 0.0), 1.0)
    for (f0, w0), (f1, w1) in zip(WIDTH_PROFILE, WIDTH_PROFILE[1:]):
        if f0 <= f <= f1:
            return w0 + (w1 - w0) * (f - f0) / (f1 - f0)
    return WIDTH_PROFILE[-1][1]


# ----------------------------------------------------------------------------
# 2. BODY = outline prism  ∩  elliptical loft (anatomical swell)
# ----------------------------------------------------------------------------
prism = Part.Face(outline_wire).extrude(V(0, 140, 0))
prism.translate(V(0, -70, 0))

def ellipse_params(z):
    rear, front = x_range(z)
    depth = front - rear
    xc = (rear + front) / 2.0 + FRONT_BIAS * depth
    a = EDGE_FULLNESS * depth * (0.5 + FRONT_BIAS) + 2.0
    b = width_at(z) / 2.0
    return xc, max(a, b + 1.0), b


secs = []
for fz in (-0.04, 0.10, 0.28, 0.46, 0.64, 0.82, 1.04):
    z = fz * H
    xc_, a_, b_ = ellipse_params(z)
    secs.append(Part.Wire([Part.Ellipse(V(xc_, 0, z), a_, b_).toShape()]))
swell = Part.makeLoft(secs, True, False, False)
body = prism.common(swell)

# ----------------------------------------------------------------------------
# 3. FRAME POCKET (rotated to the grip's own rake, so it follows the traced outline)
# ----------------------------------------------------------------------------
z1, z2 = 0.25 * H, 0.65 * H
m1, m2 = sum(x_range(z1)) / 2.0, sum(x_range(z2)) / 2.0
RAKE = math.degrees(math.atan2(m2 - m1, z2 - z1))           # positive = bottom is rearward
TR, CR = math.tan(math.radians(RAKE)), math.cos(math.radians(RAKE))

pad_zc = H - PAD_TOP_DROP - PAD_L / 2.0                       # tenon centre height
front_edge = x_range(pad_zc)[1]
POCKET_FROM_FRONT = PAD_FRONT_INSET + PAD_W + PAD_TO_POCKET_WALL
wall_x0 = front_edge - POCKET_FROM_FRONT / CR                 # rear wall of the pocket at the tenon's height
OPEN = 120.0                                                   # pocket continues this far forward = open front
pocket = Part.makeBox(POCKET_FROM_FRONT / CR + OPEN, FRAME_W, H + 12.0, V(0, -FRAME_W / 2.0, -pad_zc - 6.0))
pocket.rotate(V(0, 0, 0), V(0, 1, 0), RAKE)
pocket.translate(V(wall_x0, 0, pad_zc))
cavity = pocket
zu = UPPER_START_FRAC * H
if UPPER_EXTRA_BACK > 0.0:
    upper = Part.makeBox(UPPER_EXTRA_BACK + OPEN, FRAME_W, H - zu + 6.0, V(-UPPER_EXTRA_BACK, -FRAME_W / 2.0, zu - pad_zc))
    upper.rotate(V(0, 0, 0), V(0, 1, 0), RAKE)
    upper.translate(V(wall_x0, 0, pad_zc))
    cavity = pocket.fuse(upper)


def pocket_rear(z):
    return wall_x0 + TR * (z - pad_zc) - (UPPER_EXTRA_BACK if z >= zu else 0.0)


# checks: wood left behind the pocket's rear wall, and wood left at the open front edge outside the pocket floor
walls = []
for fz in (0.1, 0.25, 0.4, 0.55, 0.7, 0.85):
    z = fz * H
    rear, front = x_range(z)
    xc_, a_, b_ = ellipse_params(z)
    y_front = b_ * math.sqrt(max(0.0, 1.0 - ((front - xc_) / a_) ** 2))
    walls.append((fz, pocket_rear(z) - rear, y_front - FRAME_W / 2.0))
bad = [w for w in walls if min(w[1], w[2]) < 3.0]
App.Console.PrintMessage("Grip: %.0f mm tall, rake %.1f deg, pocket %.1f mm deep from the front edge. Min wood behind the pocket %.1f mm, at the open front edge %.1f mm.\n"
                         % (H, RAKE, POCKET_FROM_FRONT, min(w[1] for w in walls), min(w[2] for w in walls)))
if bad:
    App.Console.PrintWarning("Thin wood (<3 mm) at heights %s: raise FRONT_BIAS or widen WIDTH_PROFILE.\n"
                             % ", ".join("%.0f%%" % (w[0] * 100) for w in bad))

body = body.cut(cavity)

# ----------------------------------------------------------------------------
# 4. RIGHT HALF (y > 0): recessed panel, screws, checkering. Left half = mirror.
# ----------------------------------------------------------------------------
right = body.common(Part.makeBox(400, 200, 400, V(-200, 0, -100)))

panel_face = Part.Face(Part.makePolygon([P(*p) for p in PANEL_PX] + [P(*PANEL_PX[0])]))
if PANEL:
    deep = panel_face.extrude(V(0, 80.0 - PANEL_FLAT_Y, 0))
    deep.translate(V(0, PANEL_FLAT_Y, 0))
    right = try_op("Recessed panel", lambda s: s.cut(deep), right)

for (px, py) in SCREW_PX:
    sp = P(px, py)
    right = right.cut(Part.makeCylinder(SCREW_D / 2.0, 80.0, V(sp.x, 0, sp.z), V(0, 1, 0)))
    right = right.cut(Part.makeCylinder(HEAD_D / 2.0, 40.0, V(sp.x, PANEL_FLAT_Y - HEAD_DEPTH, sp.z), V(0, 1, 0)))

# the square tenon that goes into the metal grip (stands out from the pocket floor toward the centre)
# tenon sits toward the front: front side PAD_FRONT_INSET behind the front edge, rear side PAD_TO_POCKET_WALL in front of the pocket wall
pad_xc = front_edge - (PAD_FRONT_INSET + PAD_W / 2.0) / CR + PAD_X_SHIFT
App.Console.PrintMessage("Tenon: front side %.1f mm behind the front edge, rear side %.1f mm in front of the pocket's rear wall.\n"
                         % (PAD_FRONT_INSET - PAD_X_SHIFT * CR, PAD_TO_POCKET_WALL + PAD_X_SHIFT * CR))
pad = Part.makeBox(PAD_W, PAD_PROTRUSION + 1.0, PAD_L, V(-PAD_W / 2.0, FRAME_W / 2.0 - PAD_PROTRUSION, -PAD_L / 2.0))
pad = try_op("Tenon corner rounding", lambda sh: sh.makeFillet(
    PAD_R, [e for e in sh.Edges if abs(e.Vertexes[0].Y - e.Vertexes[-1].Y) > 1e-6]), pad)
pad.rotate(V(0, 0, 0), V(0, 1, 0), RAKE)
pad.translate(V(pad_xc, 0, pad_zc))
right = right.fuse(pad)

if CHECKERING and PANEL:
    try:
        bb = panel_face.BoundBox
        cx, cz = (bb.XMin + bb.XMax) / 2.0, (bb.ZMin + bb.ZMax) / 2.0
        diag = math.hypot(bb.XLength, bb.ZLength)
        n = int(diag / (2.0 * CHECKER_PITCH)) + 2
        d = CHECKER_DEPTH
        clip = panel_face.extrude(V(0, 2.0 * d + 1.0, 0))
        clip.translate(V(0, PANEL_FLAT_Y - d - 0.5, 0))
        for sign in (1, -1):
            ang = math.radians(45.0 * sign)
            nx, nz = -math.sin(ang), math.cos(ang)          # unit normal to the groove direction in the XZ plane
            grooves = []
            for k in range(-n, n + 1):
                g = Part.makeBox(diag + 10.0, d * 1.4142, d * 1.4142, V(-(diag + 10.0) / 2.0, -d * 0.7071, -d * 0.7071))
                g.rotate(V(0, 0, 0), V(1, 0, 0), 45)         # diamond cross-section = V-groove
                g.rotate(V(0, 0, 0), V(0, 1, 0), -45.0 * sign)  # groove direction in the XZ plane
                g.translate(V(cx + k * CHECKER_PITCH * nx, PANEL_FLAT_Y, cz + k * CHECKER_PITCH * nz))
                grooves.append(g)
            cutters = Part.makeCompound(grooves).common(clip)
            right = right.cut(cutters)
    except Exception as e:
        App.Console.PrintWarning("Checkering failed (%s) - continuing without it.\n" % e)

if PRINT_TEST:
    right = right.cut(Part.makeBox(400, 400, 400, V(-200, -200, 35.0)))

left = right.mirror(V(0, 0, 0), V(0, 1, 0))

# ----------------------------------------------------------------------------
# 5. LAYOUT AND DOCUMENT
# ----------------------------------------------------------------------------
doc = App.newDocument("Hammerli_208_Grip_Anatomical")
ref = None
if LAYOUT == "assembled":
    if SHOW_FRAME_REF:
        ref = cavity.copy()
else:
    right.rotate(V(0, 0, 0), V(1, 0, 0), 90)      # inner face (y = 0) down on the bed
    left.rotate(V(0, 0, 0), V(1, 0, 0), -90)
    left.translate(V(0, 15.0, 0))                 # right half is at y' in [-H, 0], left at [15, H+15]

objs = []
for nm, shp in (("Grip_Right", right), ("Grip_Left", left)):
    o = doc.addObject("Part::Feature", nm)
    o.Shape = shp.removeSplitter()
    objs.append(o)
if ref is not None:
    r = doc.addObject("Part::Feature", "Frame_pocket_reference")
    r.Shape = ref
doc.recompute()

if HAS_GUI:
    try:
        if ref is not None:
            r.ViewObject.Transparency = 75
            r.ViewObject.ShapeColor = (0.8, 0.2, 0.2)
        Gui.activeDocument().activeView().viewIsometric()
        Gui.SendMsgToActiveView("ViewFit")
    except Exception:
        pass

if EXPORT_DIR:
    try:
        import Mesh, os
        Mesh.export([objs[0]], os.path.join(EXPORT_DIR, "grip_right.stl"))
        Mesh.export([objs[1]], os.path.join(EXPORT_DIR, "grip_left.stl"))
    except Exception as e:
        App.Console.PrintError("STL export failed: %s\n" % e)

for o in objs:
    App.Console.PrintMessage("%s: valid=%s, %.1f cm3\n" % (o.Name, o.Shape.isValid(), o.Shape.Volume / 1000.0))
App.Console.PrintMessage(
    "NEXT: set GRIP_HEIGHT_MM from your real grip, then measure the metal grip (thickness, depth of the hole for the tenon), "
    "the pocket's rear wall and the screw positions. Print inner face down with supports under the pocket floor, "
    "and check the fit with PRINT_TEST = True.\n")