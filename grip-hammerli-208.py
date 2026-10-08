# -*- coding: utf-8 -*-
"""
Hämmerli 208 - anatomical target grip (Nill style), left/right halves  -  FreeCAD 1.x, parametric   (v4)

v4 changes:
 - HANDED halves (HAND): thumb rest shelf on the thumb side, optional extra palm swell on the palm side (PALM_EXTRA,
   0 = both halves as thick as measured on the original). HAND = "none" gives two mirror-image halves like v3.
 - Fit clearance (FIT_CLEARANCE) on the frame pocket, the tang cut-in and the tenon.
 - Rounded outer edges (EDGE_R). Edges OCC cannot round are left sharp and reported.
 - Screw positions in mm (SCREW_POS), measured on the gun, instead of photo pixels. Counterbores are measured from
   the local surface (in v3 the lower screw got no counterbore: the surface there is below the panel floor).
 - Smooth unchecked ring around the screw heads (SCREW_RING).
 - Optional finger grooves on the front edge (FINGER_GROOVES, off by default).
 - Breakaway support ribs under the pocket floor and the tang cut-in (SUPPORT_RIBS), so no slicer supports touch the
   fit surfaces. Exported in the same STL as their half.
 - PRINT_TEST now keeps the band with the tenon (it used to keep only the lowest 35 mm, which has no tenon), and
   FIT_PLATE prints just a thin plate with pocket and tenon, lying on its outer cut face (no supports needed).
 - Halves are named by the side of the gun (+X = muzzle, +Z = up, so +Y is the shooter's LEFT). v3 had the names swapped.

v3 changes (from the photos of the test print):
 - TOP_TRIM: the top of the grip was ~10 mm too high. The upper part of the outline is moved down 10 mm
   (smoothly, so the thumb scoop and rear hook keep their shape). The tenon is 21.05 mm below the top of the finished grip (your measurement of the original).
 - THINNER: see MIN_HALF_T / MAX_HALF_T; pocket 8.7 mm deep per half (measured).
 - FLAT LOWER PART: the pocket now runs down to the heel, so everything under the tenon is flat and thin, at the level of the area around the
   tenon. The thickened rear part (behind the pocket wall) goes all the way down to the bottom of the grip.
   The flat part is exactly MIN_HALF_T = 10.3 mm thick from the flat inner face; the thickest place is MAX_HALF_T = 18.5 mm, also from the flat face.
 - FRONT LIP removed: the small shelf that stuck out at the top front is gone; the front edge now runs straight up to the top.
 - TANG CUT-IN: the area you marked black (top rear, from the pocket's rear wall back to the rear edge, about 21 mm
   down from the OLD top) is now cut in to full frame thickness, so the rear horn of the metal grip fits.

v2 changes, from your measurements:
 - The square TENON on each inner face (55.2 x 22.2 mm, top edge 21.7 mm below the top of the grip) is modelled
   toward the FRONT: its front side is 4 mm behind the front edge and its rear side 11.7 mm in front of the
   rear wall of the pocket (zigzag cut-in), so the pocket is 37.9 mm deep from the front edge.
   It stands out from the pocket floor toward the metal grip (PAD_PROTRUSION, MEASURE).
 - The grip is OPEN AT THE FRONT: the frame pocket runs out through the front edge, so the metal grip's front
   is exposed between the halves. Only the rear is closed (the halves meet there).

How it is built:
 1. SIDE OUTLINE: traced from the outer-face photo. GRIP_HEIGHT_MM sets the height (116 mm); front-to-back it is scaled so the width is 67 mm at the palm and 43 mm at the narrowest.
 2. CROSS SECTION: a loft of ellipses (WIDTH_PROFILE), shifted forward (FRONT_BIAS) so the open front edge keeps
    wood thickness, intersected with the outline and edge-rounded.
 3. Each half: frame pocket on the inner face (open to the front), tenon, recessed checkering panel, two screws,
    thumb rest on the thumb side. Built on +Y; the right half is mirrored to -Y.

!! The outline is a trace of a photo and the pocket depth, pocket rear wall, screw and thumb-rest positions are
   estimates. Check the fit with FIT_PLATE / PRINT_TEST before printing a whole grip.
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
GRIP_HEIGHT_MM = 116.0     # real height of the finished grip from top to heel (measured on the original)
HAND = "right"             # shooting hand: "right" (thumb rest on the left half, palm on the right), "left", "none"

# total grip width (both halves together) as (fraction of height from the heel, width). Interpolated.
WIDTH_SCALE = 1.0          # quick tuning of the total width: 0.9 = 10 % thinner, 1.1 = 10 % thicker (all heights)
EDGE_FULLNESS = 1.06       # >1 = blunter/rounder front and back straps, closer to 1 = sharper
EDGE_R = 2.5               # rounding of the outer edges (straps, top, heel). 0 = sharp

# metal grip between the halves (MEASURE)
POCKET_DEPTH = 8.7         # depth of the pocket in each half (measured on the original)
FRAME_W = 2.0 * POCKET_DEPTH   # = thickness of the metal grip in the pocket
FIT_CLEARANCE = 0.2        # per side: pocket and tang cut-in grow, tenon shrinks by this (0.15 - 0.25 for a 0.4 mm nozzle)

# v3: THICKNESS (side to side) from your measurement: the thinnest place of one half is 10.3 mm, measured from the inner face.
# (Your 67 mm / 43 mm are the front-to-back WIDTH of the grip - the traced outline already gives 67 mm at the palm and
#  43 mm at the narrowest, so those are unchanged.)
MIN_HALF_T = 10.3          # thinnest place of one half (mm)
MAX_HALF_T = 18.5          # thickest place of one half, at the palm swell (measured on the original)
_SWELL = [(0.00, 0.0), (0.20, 0.2), (0.50, 0.85), (0.80, 1.0), (1.00, 0.75)]   # share of the swell, from the heel up
# thicknesses are measured from the flat inner face = the pocket floor (POCKET_DEPTH from the centre plane):
_HALF_MIN = POCKET_DEPTH + MIN_HALF_T      # outer surface where the flat part is thinnest: 8.7 + 10.3 = 19.0 from the centre
_HALF_MAX = POCKET_DEPTH + MAX_HALF_T      # outer surface at the palm swell:             8.7 + 18.5 = 27.2 from the centre
WIDTH_PROFILE = [(f, 2.0 * (_HALF_MIN + k * (_HALF_MAX - _HALF_MIN))) for f, k in _SWELL]   # total width of the grip
PALM_EXTRA = 0.0           # extra thickness at the swell peak on the palm-side half only (follows _SWELL). 0 = as measured

# the square tenon that plugs into the metal grip (your measurements)
PAD_L, PAD_W = 55.2, 22.2  # long side (along the grip) x short side (front-to-back)
PAD_TOP_DROP = 21.05       # from the top of the finished grip down to the top edge of the tenon (measured on the original)
PAD_R = 4.0                # corner radius
PAD_PROTRUSION = 3.0       # how far the tenon stands out from the pocket floor (MEASURE: depth of the hole in the metal grip)

# the pocket (zigzag cut-in) is open at the front. Its rear wall follows from your measurements:
PAD_FRONT_INSET = 4.0      # tenon front side  -> front edge of the grip
PAD_TO_POCKET_WALL = 11.7  # tenon rear side   -> rear wall (back edge) of the pocket
#   => pocket depth from the front edge = 4.0 + 22.2 + 11.7 = 37.9 mm
POCKET_BOTTOM_MARGIN = 3.0  # the pocket ends this far below the lower side of the tenon (below it the face is flat, as on the original)
PAD_X_SHIFT = 0.0          # extra shift of the tenon forward (+) / back (-) along the grip
# v3: top trim and the black-marked cut-in at the top rear
TOP_TRIM = 10.0            # lower the top of the grip by this much (test print was ~10 mm too high)
TANG_CUT = True            # cut in the top rear (from the pocket's rear wall to the rear edge)
TANG_DROP_OLD = 21.0       # bottom of the marked area, measured down from the OLD (untrimmed) top (about 21 mm in the photo)
UPPER_START_FRAC = 0.58    # from this height up the pocket may be deeper (tang / trigger-guard clearance)
UPPER_EXTRA_BACK = 0.0     # how much deeper toward the rear in that upper part (0 = same as below)
FRONT_BIAS = 0.10          # moves the swell forward so the open front edge keeps thickness (0 = symmetric)

# thumb rest shelf on the thumb-side half
THUMB_REST = True
THUMB_DROP = 25.0          # MEASURE: from the top of the grip down to the top of the shelf (where your thumb lies)
THUMB_LEN = 42.0           # length of the shelf from the front edge backward
THUMB_OUT = 7.0            # how far the shelf stands out from the grip surface
THUMB_LIP = 4.0            # thickness of the shelf's outer edge (underside slopes 45 deg back into the grip)

# finger grooves on the front edge: list of (height of groove centre above the heel, depth). [] = none
FINGER_GROOVES = []        # e.g. [(22.0, 1.5), (42.0, 1.5)] - MEASURE with your hand on the gun
FINGER_GROOVE_R = 11.0     # radius of each groove (about half a finger width)

# screws, one per hole: (from the top of the grip down, from the front edge backward at that height) - MEASURE
SCREW_POS = [(48.7, 34.8), (97.2, 54.2)]
SCREW_D = 3.4              # M3 clearance
HEAD_D, HEAD_DEPTH = 6.4, 2.0
SCREW_RING = 1.5           # smooth (unchecked) ring around each screw head

# recessed checkering panel with border
PANEL = True
PANEL_FLAT_Y = _HALF_MAX - 2.0   # half-thickness at the panel floor (smaller = deeper recess): 2 mm recess at the palm swell
CHECKERING = True          # diamond checkering (slower to compute: set False for a quick preview)
CHECKER_PITCH = 2.0        # mm between grooves (0.4 mm nozzle: 1.6 - 2.4 works)
CHECKER_DEPTH = 0.45

# breakaway ribs under the pocket floor and the tang cut-in (overhangs when the half lies on its inner face)
SUPPORT_RIBS = True
RIB_T = 0.8                # rib thickness (2 perimeters)
RIB_PITCH = 6.0            # spacing between ribs
RIB_GAP = 0.25             # air gap up to the pocket floor / tenon (about one layer)
RIB_SIDE_GAP = 0.6         # gap to walls beside the rib (more than a line width, so the slicer keeps it)

LAYOUT = "print"           # "print" = halves flat on their inner faces, "assembled" = as on the gun
SHOW_FRAME_REF = True
PRINT_TEST = False         # True = only the band with the tenon and the upper screw, for a fit test
FIT_PLATE = False          # True = only a thin plate (pocket + tenon), printed on its outer cut face. Overrides PRINT_TEST
FIT_PLATE_T = 3.0          # plate thickness above the pocket floor
EXPORT_DIR = ""

# ----------------------------------------------------------------------------
# TRACED OUTLINE (photo pixels, front is on the LEFT in the photo; x is flipped so front = +X)
# ----------------------------------------------------------------------------
OUTLINE = [
    ("L", [(546, 70), (580, 66), (620, 62)]),                                              # top (front shelf removed)
    ("S", [(620, 62), (655, 78), (700, 86), (745, 78), (775, 64)]),                       # thumb/trigger-guard scoop
    ("L", [(775, 64), (990, 50)]),
    ("S", [(990, 50), (1004, 95), (1010, 128), (985, 160), (938, 178), (905, 205), (898, 228), (912, 248)]),  # rear hook
    ("S", [(912, 248), (940, 300), (990, 400), (1060, 560), (1110, 690), (1160, 830), (1205, 985)]),          # rear edge
    ("L", [(1205, 985), (615, 990)]),                                                     # heel
    ("S", [(615, 990), (590, 900), (562, 800), (548, 700), (543, 600), (540, 480), (538, 390),
           (541, 230), (546, 70)]),                                                       # front edge, straight up, no forward lean (no front lip)
]
PANEL_PX = [(560, 392), (640, 368), (720, 358), (800, 380), (875, 420), (940, 470), (995, 540), (1040, 620),
            (1085, 740), (1125, 860), (1170, 960), (1140, 968), (640, 972), (578, 900), (565, 800), (560, 700),
            (558, 600), (556, 490)]

PX_TOP, PX_BOTTOM, X_REF = 50.0, 990.0, 800.0
SX = 112.0 / (PX_BOTTOM - PX_TOP)               # mm per pixel front-to-back: gives 67 mm at the palm and 43 mm at the narrowest, as measured
S = (GRIP_HEIGHT_MM + TOP_TRIM) / (PX_BOTTOM - PX_TOP)   # mm per pixel in height (the outline is trimmed by TOP_TRIM afterwards)
H = (PX_BOTTOM - PX_TOP) * S - TOP_TRIM         # = GRIP_HEIGHT_MM, height of the finished grip
PY_TRIM_END = 420.0                             # below this pixel row nothing moves (under the front shelf)
C = FIT_CLEARANCE
FLOOR_Y = POCKET_DEPTH + C                      # pocket floor (inner face of the wood) of the +Y half


def _trim(py):
    """downward shift in mm: full TOP_TRIM at the top row, fading linearly to 0 at PY_TRIM_END"""
    return TOP_TRIM * min(1.0, max(0.0, (PY_TRIM_END - py) / (PY_TRIM_END - PX_TOP)))


def P(px, py, y=0.0):
    return V((X_REF - px) * SX, y, (PX_BOTTOM - py) * S - _trim(py))


def try_op(label, fn, shape):
    try:
        r = fn(shape)
        if r.isValid() and not r.isNull():
            return r
        App.Console.PrintWarning("%s gave invalid geometry - skipped.\n" % label)
    except Exception as e:
        App.Console.PrintWarning("%s failed (%s) - skipped.\n" % (label, e))
    return shape


def fillet_soft(label, shape, r, edges):
    """fillet as many of the edges as OCC will take (one failing edge no longer drops them all)"""
    used = []
    for i, e in enumerate(shape.Edges):
        if not any(e.isSame(x) for x in edges):
            continue
        try:
            if shape.makeFillet(r, [shape.Edges[j] for j in used + [i]]).isValid():
                used.append(i)
        except Exception:
            pass
    if len(used) < len(edges):
        App.Console.PrintWarning("%s: rounded %d of %d edges.\n" % (label, len(used), len(edges)))
    return shape.makeFillet(r, [shape.Edges[j] for j in used]) if used else shape


def interp(table, f):
    f = min(max(f, table[0][0]), table[-1][0])
    for (f0, v0), (f1, v1) in zip(table, table[1:]):
        if f0 <= f <= f1:
            return v0 + (v1 - v0) * (f - f0) / (f1 - f0)
    return table[-1][1]


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
    return WIDTH_SCALE * interp(WIDTH_PROFILE, min(max(z / H, 0.0), 1.0))


# ----------------------------------------------------------------------------
# 2. BODY = outline prism  ∩  elliptical loft (anatomical swell), one per side (palm side may be thicker)
# ----------------------------------------------------------------------------
prism = Part.Face(outline_wire).extrude(V(0, 140, 0))
prism.translate(V(0, -70, 0))


def ellipse_params(z, palm):
    rear, front = x_range(z)
    depth = front - rear
    xc = (rear + front) / 2.0 + FRONT_BIAS * depth
    a = EDGE_FULLNESS * depth * (0.5 + FRONT_BIAS) + 2.0
    b = width_at(z) / 2.0 + (PALM_EXTRA * interp(_SWELL, z / H) if palm else 0.0)
    return xc, max(a, b + 1.0), b


def surface_y(x, z, palm):
    """approximate half-thickness of the swell at (x, z)"""
    xc, a, b = ellipse_params(z, palm)
    return b * math.sqrt(max(0.0, 1.0 - ((x - xc) / a) ** 2))


def make_body(palm):
    secs = []
    for fz in (-0.04, 0.10, 0.28, 0.46, 0.64, 0.82, 1.04):
        z = fz * H
        xc_, a_, b_ = ellipse_params(z, palm)
        secs.append(Part.Wire([Part.Ellipse(V(xc_, 0, z), a_, b_).toShape()]))
    body = prism.common(Part.makeLoft(secs, True, False, False))
    for zg, depth in FINGER_GROOVES:
        r = FINGER_GROOVE_R
        body = try_op("Finger groove at %.0f mm" % zg, lambda s: s.cut(Part.makeCylinder(
            r, 140.0, V(x_range(zg)[1] + r - depth, -70.0, zg), V(0, 1, 0))), body)
    if EDGE_R > 0:
        body = fillet_soft("Edge rounding", body, EDGE_R, body.Edges)
    return body


# ----------------------------------------------------------------------------
# 3. FRAME POCKET (rotated to the grip's own rake, so it follows the traced outline)
# ----------------------------------------------------------------------------
z1, z2 = 0.25 * H, 0.65 * H
m1, m2 = sum(x_range(z1)) / 2.0, sum(x_range(z2)) / 2.0
RAKE = math.degrees(math.atan2(m2 - m1, z2 - z1))           # positive = bottom is rearward
TR, CR = math.tan(math.radians(RAKE)), math.cos(math.radians(RAKE))

pad_zc = H - PAD_TOP_DROP - PAD_L / 2.0                       # tenon centre height (21.05 mm below the top of the finished grip)
front_edge = x_range(pad_zc)[1]
POCKET_FROM_FRONT = PAD_FRONT_INSET + PAD_W + PAD_TO_POCKET_WALL
wall_x0 = front_edge - POCKET_FROM_FRONT / CR                 # rear wall of the pocket at the tenon's height


def to_pocket_frame(shape):
    """local pocket frame (x = 0 at the rear wall, z = 0 at the tenon centre) -> grip coordinates"""
    shape.rotate(V(0, 0, 0), V(0, 1, 0), RAKE)
    shape.translate(V(wall_x0, 0, pad_zc))
    return shape


OPEN = 120.0                                                   # pocket continues this far forward = open front
pk_z0 = -pad_zc - 6.0                                          # the pocket runs all the way down to the heel (flat, thin floor below the tenon)
cavity = to_pocket_frame(Part.makeBox(POCKET_FROM_FRONT / CR + OPEN + C, 2.0 * FLOOR_Y, (H - pad_zc) + 12.0 - pk_z0,
                                      V(-C, -FLOOR_Y, pk_z0)))
zu = UPPER_START_FRAC * H
if UPPER_EXTRA_BACK > 0.0:
    upper = to_pocket_frame(Part.makeBox(UPPER_EXTRA_BACK + OPEN + C, 2.0 * FLOOR_Y, H - zu + 6.0,
                                         V(-UPPER_EXTRA_BACK - C, -FLOOR_Y, zu - pad_zc)))
    cavity = cavity.fuse(upper)


def pocket_rear(z):
    return wall_x0 - C + TR * (z - pad_zc) - (UPPER_EXTRA_BACK if z >= zu else 0.0)


# top-rear cut-in (the black-marked area): from the pocket's rear wall back through the rear edge, down to TANG_Z0
TANG_Z0 = H + TOP_TRIM - TANG_DROP_OLD - C
if TANG_CUT:
    zs = [TANG_Z0 + i * (H - TANG_Z0) / 10.0 for i in range(11)]
    tx_min = min(x_range(z)[0] for z in zs) - 20.0
    tx_max = pocket_rear(H) + 3.0                      # reaches into the pocket at every height (no wood sliver)
    tang = Part.makeBox(tx_max - tx_min, 2.0 * FLOOR_Y, H + 6.0 - TANG_Z0, V(tx_min, -FLOOR_Y, TANG_Z0))
    cavity = cavity.fuse(tang)
    App.Console.PrintMessage("Tang cut-in: from z=%.1f up to the top (%.1f mm tall), x from %.1f back to the rear edge.\n"
                             % (TANG_Z0, H - TANG_Z0, tx_max))


# checks: wood left behind the pocket's rear wall, and wood left at the open front edge outside the pocket floor
# (thinnest side, i.e. without palm extra)
walls = []
for fz in [(pad_zc - PAD_L / 2.0) / H + d for d in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5)]:
    if fz > 0.95:
        continue
    z = fz * H
    rear, front = x_range(z)
    walls.append((fz, pocket_rear(z) - rear, surface_y(front, z, False) - FLOOR_Y))
bad = [w for w in walls if min(w[1], w[2]) < 3.0]
App.Console.PrintMessage("Grip: %.0f mm tall, rake %.1f deg, pocket %.1f mm deep from the front edge. Min wood behind the pocket %.1f mm, at the open front edge %.1f mm.\n"
                         % (H, RAKE, POCKET_FROM_FRONT, min(w[1] for w in walls), min(w[2] for w in walls)))
if bad:
    App.Console.PrintWarning("Thin wood (<3 mm) at heights %s: raise FRONT_BIAS or widen WIDTH_PROFILE.\n"
                             % ", ".join("%.0f%%" % (w[0] * 100) for w in bad))

# tenon: front side PAD_FRONT_INSET behind the front edge, rear side PAD_TO_POCKET_WALL in front of the pocket wall.
# Shrunk by the clearance on every side, and its tip stops the clearance short of the bottom of the hole.
pad_xl = POCKET_FROM_FRONT / CR - (PAD_FRONT_INSET + PAD_W / 2.0) / CR + PAD_X_SHIFT   # tenon centre, pocket frame
pad_w, pad_l = PAD_W - 2.0 * C, PAD_L - 2.0 * C
pad_tip = POCKET_DEPTH - PAD_PROTRUSION + 2.0 * C             # tenon face toward the centre (pocket floor is FLOOR_Y)
App.Console.PrintMessage("Tenon: front side %.1f mm behind the front edge, rear side %.1f mm in front of the pocket's rear wall.\n"
                         % (PAD_FRONT_INSET - PAD_X_SHIFT * CR, PAD_TO_POCKET_WALL + PAD_X_SHIFT * CR))

# screw centres in grip coordinates
screws = []
for from_top, from_front in SCREW_POS:
    z = H - from_top
    screws.append((x_range(z)[1] - from_front, z))

panel_face = Part.Face(Part.makePolygon([P(*p) for p in PANEL_PX] + [P(*PANEL_PX[0])]))


# ----------------------------------------------------------------------------
# 4. ONE HALF, built on +Y (the gun's left side). The right half is the mirror of a +Y build.
# ----------------------------------------------------------------------------
def thumb_shelf(palm):
    z_top = H - THUMB_DROP
    x_front = x_range(z_top)[1] + 2.0
    x_back = x_front - 2.0 - THUMB_LEN
    secs = []
    for i in range(7):
        x = x_back + (x_front - x_back) * i / 6.0
        out = THUMB_OUT * min(1.0, 0.15 + i / 3.0)                # tapers in at the rear end
        ys = max(surface_y(min(x, x_front - 2.0), z_top, palm), FLOOR_Y + 5.0)
        y0 = max(ys - 3.0, FLOOR_Y + 1.5)
        pts = [V(x, y0, z_top), V(x, ys + out, z_top), V(x, ys + out, z_top - THUMB_LIP),
               V(x, y0, z_top - THUMB_LIP - out - (ys - y0))]
        secs.append(Part.makePolygon(pts + [pts[0]]))
    shelf = Part.makeLoft(secs, True, True, False).common(prism)
    return fillet_soft("Thumb rest rounding", shelf, min(EDGE_R, THUMB_LIP / 2.0 - 0.2),
                       [e for e in shelf.Edges if e.BoundBox.YMax > FLOOR_Y + 4.0])


def build_half(palm, thumb):
    half = make_body(palm).cut(cavity).common(Part.makeBox(400, 200, 400, V(-200, 0, -100)))
    panel_y = PANEL_FLAT_Y + (PALM_EXTRA if palm else 0.0)    # the panel floor moves out with the palm swell

    if PANEL:
        deep = panel_face.extrude(V(0, 80.0 - panel_y, 0))
        deep.translate(V(0, panel_y, 0))
        half = try_op("Recessed panel", lambda s: s.cut(deep), half)

    # counterbores from the local surface (inside or outside the panel)
    for x, z in screws:
        try:
            ys = max(v.Y for v in half.common(Part.makeLine(V(x, 0, z), V(x, 80, z))).Vertexes)
        except Exception:
            ys = min(surface_y(x, z, palm), panel_y)
        half = half.cut(Part.makeCylinder(SCREW_D / 2.0, 80.0, V(x, 0, z), V(0, 1, 0)))
        half = half.cut(Part.makeCylinder(HEAD_D / 2.0, 40.0, V(x, ys - HEAD_DEPTH, z), V(0, 1, 0)))

    # the square tenon that goes into the metal grip (stands out from the pocket floor toward the centre)
    pad = Part.makeBox(pad_w, FLOOR_Y - pad_tip + 1.0, pad_l, V(-pad_w / 2.0, pad_tip, -pad_l / 2.0))
    pad = try_op("Tenon corner rounding", lambda sh: sh.makeFillet(
        PAD_R, [e for e in sh.Edges if abs(e.Vertexes[0].Y - e.Vertexes[-1].Y) > 1e-6]), pad)
    pad.translate(V(pad_xl, 0, 0))
    half = half.fuse(to_pocket_frame(pad))

    if CHECKERING and PANEL:
        try:
            bb = panel_face.BoundBox
            cx, cz = (bb.XMin + bb.XMax) / 2.0, (bb.ZMin + bb.ZMax) / 2.0
            diag = math.hypot(bb.XLength, bb.ZLength)
            n = int(diag / (2.0 * CHECKER_PITCH)) + 2
            d = CHECKER_DEPTH
            clip = panel_face.extrude(V(0, 2.0 * d + 1.0, 0))
            clip.translate(V(0, panel_y - d - 0.5, 0))
            for x, z in screws:
                clip = clip.cut(Part.makeCylinder(HEAD_D / 2.0 + SCREW_RING, 80.0, V(x, 0, z), V(0, 1, 0)))
            for sign in (1, -1):
                ang = math.radians(45.0 * sign)
                nx, nz = -math.sin(ang), math.cos(ang)          # unit normal to the groove direction in the XZ plane
                grooves = []
                for k in range(-n, n + 1):
                    g = Part.makeBox(diag + 10.0, d * 1.4142, d * 1.4142, V(-(diag + 10.0) / 2.0, -d * 0.7071, -d * 0.7071))
                    g.rotate(V(0, 0, 0), V(1, 0, 0), 45)         # diamond cross-section = V-groove
                    g.rotate(V(0, 0, 0), V(0, 1, 0), -45.0 * sign)  # groove direction in the XZ plane
                    g.translate(V(cx + k * CHECKER_PITCH * nx, panel_y, cz + k * CHECKER_PITCH * nz))
                    grooves.append(g)
                half = half.cut(Part.makeCompound(grooves).common(clip))
        except Exception as e:
            App.Console.PrintWarning("Checkering failed (%s) - continuing without it.\n" % e)

    if thumb and THUMB_REST:
        half = try_op("Thumb rest", lambda s: s.fuse(thumb_shelf(palm)), half)
    return half


def support_ribs():
    """breakaway ribs standing on the bed (y = 0) under the pocket floor and the tang cut-in, RIB_GAP short of the
    floor and the tenon and RIB_SIDE_GAP away from the walls beside them"""
    ribs = []
    x = RIB_PITCH / 2.0
    while x < POCKET_FROM_FRONT / CR + 5.0:
        ribs.append(Part.makeBox(RIB_T, FLOOR_Y - RIB_GAP, H + 12.0 - pk_z0, V(x - RIB_T / 2.0, 0, pk_z0)))
        x += RIB_PITCH
    keep_out = Part.makeBox(pad_w + 2.0 * RIB_SIDE_GAP, FLOOR_Y, pad_l + 2.0 * RIB_SIDE_GAP,
                            V(pad_xl - pad_w / 2.0 - RIB_SIDE_GAP, pad_tip - RIB_GAP, -pad_l / 2.0 - RIB_SIDE_GAP))
    ribs = to_pocket_frame(Part.makeCompound(ribs).cut(keep_out))
    if TANG_CUT:
        behind = to_pocket_frame(Part.makeBox(200, 200, 400, V(-200 - RIB_SIDE_GAP, -100, -200)))  # behind the rear wall
        tribs = []
        x = pocket_rear(H) - RIB_PITCH / 2.0
        while x > tx_min:
            tribs.append(Part.makeBox(RIB_T, FLOOR_Y - RIB_GAP, H + 6.0 - TANG_Z0 - RIB_SIDE_GAP,
                                      V(x - RIB_T / 2.0, 0, TANG_Z0 + RIB_SIDE_GAP)))
            x -= RIB_PITCH
        ribs = Part.makeCompound(ribs.Solids + Part.makeCompound(tribs).common(behind).Solids)
    return ribs.common(prism)


def band(shape, z0, z1, y1=200.0):
    return shape.common(Part.makeBox(400, y1, z1 - z0, V(-200, 0, z0)))


thumb_side = {"right": "left", "left": "right"}.get(HAND)
palm_side = {"right": "right", "left": "left"}.get(HAND)
plus_y = build_half(palm_side == "left", thumb_side == "left")                 # gun's left side
minus_y = plus_y if HAND not in ("right", "left") else build_half(palm_side == "right", thumb_side == "right")
ribs = support_ribs() if (SUPPORT_RIBS and LAYOUT == "print" and not FIT_PLATE) else None

test_z = (pad_zc - PAD_L / 2.0 - 5.0, pad_zc + PAD_L / 2.0 + 5.0)
if FIT_PLATE:
    plus_y, minus_y = [band(s, test_z[0], test_z[1], FLOOR_Y + FIT_PLATE_T) for s in (plus_y, minus_y)]
elif PRINT_TEST:
    plus_y, minus_y = [band(s, *test_z) for s in (plus_y, minus_y)]
    if ribs is not None:
        ribs = band(ribs, *test_z)

left = plus_y
right = minus_y.mirror(V(0, 0, 0), V(0, 1, 0))
ribs_l = ribs
ribs_r = ribs.mirror(V(0, 0, 0), V(0, 1, 0)) if ribs is not None else None

# ----------------------------------------------------------------------------
# 5. LAYOUT AND DOCUMENT
# ----------------------------------------------------------------------------
doc = App.newDocument("Hammerli_208_Grip_Anatomical")
ref = None
if LAYOUT == "assembled":
    if SHOW_FRAME_REF:
        ref = cavity.copy()
else:
    # inner face (y = 0) down on the bed; a fit plate lies on its outer cut face instead, so nothing overhangs
    a = -90 if FIT_PLATE else 90
    for s in (left, ribs_l):
        if s is not None:
            s.rotate(V(0, 0, 0), V(1, 0, 0), a)
    for s in (right, ribs_r):
        if s is not None:
            s.rotate(V(0, 0, 0), V(1, 0, 0), -a)
            s.translate(V(0, 15.0, 0))            # left half is at y' in [-H, 0], right at [15, H+15]
    if FIT_PLATE:                                 # side by side, cut face on the bed
        bl = left.optimalBoundingBox()
        left.translate(V(0, 0, -bl.ZMin))
        br = right.optimalBoundingBox()
        right.translate(V(0, bl.YMax + 15.0 - br.YMin, -br.ZMin))

objs = []
for nm, shp in (("Grip_Right", right), ("Grip_Left", left)):
    o = doc.addObject("Part::Feature", nm)
    o.Shape = shp.removeSplitter()
    objs.append(o)
rib_objs = []
for nm, shp in (("Support_Right", ribs_r), ("Support_Left", ribs_l)):
    if shp is not None:
        o = doc.addObject("Part::Feature", nm)
        o.Shape = shp
        rib_objs.append(o)
if ref is not None:
    r = doc.addObject("Part::Feature", "Frame_pocket_reference")
    r.Shape = ref
doc.recompute()

if HAS_GUI:
    try:
        if ref is not None:
            r.ViewObject.Transparency = 75
            r.ViewObject.ShapeColor = (0.8, 0.2, 0.2)
        for o in rib_objs:
            o.ViewObject.ShapeColor = (0.9, 0.6, 0.1)
        Gui.activeDocument().activeView().viewIsometric()
        Gui.SendMsgToActiveView("ViewFit")
    except Exception:
        pass

if EXPORT_DIR:
    try:
        import Mesh, os
        # each half together with its support ribs, so they stay aligned in the slicer
        Mesh.export([objs[0]] + rib_objs[:1], os.path.join(EXPORT_DIR, "grip_right.stl"))
        Mesh.export([objs[1]] + rib_objs[1:], os.path.join(EXPORT_DIR, "grip_left.stl"))
    except Exception as e:
        App.Console.PrintError("STL export failed: %s\n" % e)

for o in objs:
    App.Console.PrintMessage("%s: valid=%s, %.1f cm3\n" % (o.Name, o.Shape.isValid(), o.Shape.Volume / 1000.0))
for o in rib_objs:
    App.Console.PrintMessage("%s: %d ribs, valid=%s\n" % (o.Name, len(o.Shape.Solids), o.Shape.isValid()))
App.Console.PrintMessage(
    "NEXT: measure the metal grip (thickness, depth of the hole for the tenon), the pocket's rear wall, "
    "the screw positions and THUMB_DROP. Print FIT_PLATE = True first to check pocket and tenon, "
    "then the halves on their inner faces (the orange ribs are breakaway supports under the pocket floor).\n")
