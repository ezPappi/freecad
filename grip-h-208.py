# -*- coding: utf-8 -*-
"""
Hämmerli 208 - anatomical target grip (Nill style), left/right halves  -  FreeCAD 1.x, parametric   (v5.1)

v5.1: flange shortened to 70 mm (tip to rear end; it now ends at the rear edge, no rear overhang), 11.8 mm thick all along and 10 mm tall,
 with a 3 mm wide, 4 mm deep notch along the top on the inner side (FLANGE_NOTCH_W / FLANGE_NOTCH_D). The 4 mm inner recess of v5 is gone.

v5: THE TOP FLANGE (from your sketch and photos of the original). The original is T-shaped: a 92 mm long flange, 10 mm tall, sits on top, sticks
 ~23 mm out in front of the front strap (with a 11 mm deep arc under it, 25.5 mm tall, and a pointed toe 34.5 mm below the top) and
 ~20 mm out behind. The flange is a thin plate: 7.7 mm thick at the front, 11.6 mm at the rear, and its inner face is cut in 4 mm
 (FLANGE_REBATE). The overhang in front is a thin plate (NECK_T) at pocket-floor level. Replaces the 4 mm top cut-in of v4.2.
 The rear: the flange's underside runs 29 mm (REAR_ARC_LEN) back from the body to the flange end.
 Support: the flange and the front overhang lie in the air when the half is printed on its inner face - use slicer supports there.

v4.3: both halves are now built in a guarded way (a failing half is retried without the thumb rest and reported in the Report view),
 removeSplitter() can no longer swallow a half, and every half prints its volume and bounding box so a missing half shows up as a message.

v4.2 changes (from your sketch + answers):
 - SCREWS from the sketch: screw 1 is 33.5 mm below the top edge of the tenon and 4 mm behind its rear side; screw 2 is 25.5 mm above the
   bottom and 24.5 mm from the rear edge (SCREW_POS now takes (from top, "front" or "rear", distance)).
 - TOP RABBET: a 4 mm cut-in along the whole top edge, 9 mm tall (the hatched strip; 34.5 - 25.5 = 9), from the inner face.
 - RELIEF above the tenon: a 33 mm long cut-in, 5.5 mm tall at the front end and 10.5 mm at the rear end, 2.88 mm deep, right under the rabbet.
 - The tenon is clipped to the outline so it can never stick out of the grip.
 NOT yet done: the front arc (34.5 / 25.5 mm) - I need to know what the left column of the sketch is.

v4.1 changes (from your pencil sketch of the original):
 - Pocket width (front to rear wall) is now 38.0 mm as on the sketch (was 37.9): PAD_TO_POCKET_WALL 11.8.
 - Depth of the grip at the heel is now 68 mm as on the sketch (was ~70 mm): the rear heel corner of the outline moved 2.4 mm forward.
   The 67 mm at the palm and 43 mm at the narrowest are unchanged.

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
REAR_ARC_ROLL_R = 10.0     # rounding of the outer edge along the curve from the flange down the back of the raised rear part (the cut-in edge). 0 = off
REAR_ROLL_R = 9.05         # (9.0 gave a face that cannot be meshed; 9.05 is the same to the eye)  # the outer rear edge of the grip rolls over in a large radius toward the inner side (as on the wooden grip). 0 = off
EDGE_R = 2.5               # rounding of the outer edges (straps, top, heel). 0 = sharp

# metal grip between the halves (MEASURE)
POCKET_DEPTH = 8.7         # depth of the pocket in each half (measured on the original)
FRAME_W = 2.0 * POCKET_DEPTH   # = thickness of the metal grip in the pocket
FIT_CLEARANCE = 0.2        # per side: pocket and tang cut-in grow, tenon shrinks by this (0.15 - 0.25 for a 0.4 mm nozzle)

# v3: THICKNESS (side to side) from your measurement: the thinnest place of one half is 10.3 mm, measured from the inner face.
# (Your 67 mm / 43 mm are the front-to-back WIDTH of the grip - the traced outline already gives 67 mm at the palm and
#  43 mm at the narrowest, so those are unchanged.)
MIN_HALF_T = 3.0           # thinnest place of one half, measured from the pocket floor (mm); 8.7 + 3.0 = 11.7 mm from the frame side
MAX_HALF_T = 9.8           # thickest place of one half, from the pocket floor; 8.7 + 9.8 = 18.5 mm from the frame side to the outside (v5.1: grip was too thick)
_SWELL = [(0.00, 0.0), (0.20, 0.2), (0.50, 0.85), (0.80, 1.0), (1.00, 0.75)]   # share of the swell, from the heel up
# thicknesses are measured from the flat inner face = the pocket floor (POCKET_DEPTH from the centre plane):
_HALF_MIN = POCKET_DEPTH + MIN_HALF_T      # outer surface where the flat part is thinnest: 8.7 + 10.3 = 19.0 from the centre
_HALF_MAX = POCKET_DEPTH + MAX_HALF_T      # outer surface at the palm swell:             8.7 + 18.5 = 27.2 from the centre
WIDTH_PROFILE = [(f, 2.0 * (_HALF_MIN + k * (_HALF_MAX - _HALF_MIN))) for f, k in _SWELL]   # total width of the grip
PALM_EXTRA = 0.0           # extra thickness at the swell peak on the palm-side half only (follows _SWELL). 0 = as measured

# the square tenon that plugs into the metal grip (your measurements)
PAD_L, PAD_W = 55.2, 22.2  # long side (along the grip) x short side (front-to-back)
PAD_TOP_DROP = 17.8        # from the top of the finished grip down to the top edge of the tenon: the tenon's lower edge is 43 mm above the heel (tilted: ~41 .. 45 mm)
WALL_SHIFT = 21.05 - PAD_TOP_DROP   # the wall features below were measured against the old tenon position (21.05); this keeps them where they were
PAD_R = 4.0                # corner radius
PAD_PROTRUSION = 3.0       # how far the tenon stands out from the pocket floor (MEASURE: depth of the hole in the metal grip)

# the pocket (zigzag cut-in) is open at the front. Its rear wall follows from your measurements:
PAD_FRONT_INSET = 4.0      # tenon front side  -> front edge of the grip
PAD_TO_POCKET_WALL = 11.8  # tenon rear side   -> rear wall (back edge) of the pocket
#   => pocket depth from the front edge = 4.0 + 22.2 + 11.8 = 38.0 mm (sketch: 38)
POCKET_BOTTOM_MARGIN = 3.0  # the pocket ends this far below the lower side of the tenon (below it the face is flat, as on the original)
PAD_SHIFT_FRONT = 2.0      # v5.40: the tenon (both halves) moved this far toward the front of the grip (mm, in grip coordinates) ...
PAD_SHIFT_UP = 2.0         # ... and this far up toward the top / the cut-in (mm). Only the tenon moves: the pocket and the screws stay where they were.
PAD_X_SHIFT = 0.0          # extra shift of the tenon forward (+) / back (-) along the grip
# v3: top trim and the black-marked cut-in at the top rear
TOP_TRIM = 10.0            # lower the top of the grip by this much (test print was ~10 mm too high)
TANG_CUT = True            # cut in the top rear (from the pocket's rear wall to the rear edge)
TANG_DROP_OLD = 30.0       # bottom of the marked area, measured down from the OLD (untrimmed) top; 30 = 20 mm below the top of the finished grip
TANG_TAPER = True          # the raised rear part narrows to a thin spur at its upper end (as on the original)
TANG_SPUR_BELOW_FLANGE = 13.0  # the spur tip ends this far below the flange underside (v5.32: 13.0 = wall 5 mm longer upward; was 18.0)
TANG_SPUR_W = 1.2          # width of the spur tip (front-to-back); v5.40: 1.2 mm (was 2.0), the spur runs out gradually to this at its top (both halves)
TANG_TAPER_SCALE = 1.0
TANG_CURVE = [(0.0, 0.0), (2.7, 16.5), (9.4, 29.7), (18.7, 40.7), (30.0, 51.0), (45.0, 62.0), (70.0, 75.0)]   # (mm rearward, mm below the tip)
# v4.2: cut-ins at the top, from the inner face (from your sketch)
TOP_RABBET = False         # replaced by the flange (FLANGE_REBATE)
TOP_RABBET_H = 10.0        # the relief below sits right under the flange (FLANGE_T)
TOP_RABBET_D = 4.0         # depth, beyond the pocket floor
LOBE = True                # relief right under the rabbet, above the tenon
LOBE_L, LOBE_H_FRONT, LOBE_H_REAR, LOBE_D = 33.0, 5.5, 10.5, 2.88
LOBE_BOTTOM_FRONT, LOBE_BOTTOM_REAR = 12.5, 15.5   # underside of the relief, measured down from the TOP of the grip (user setting)
LOBE_FROM_FRONT = 0.0      # ESTIMATE: where the front end of the relief starts, behind the front edge
FLANGE_REMOVE_SIDE = "left"   # v5.40: this half has NO flange ("left" / "right" = the gun's side, None = flange on both): it is cut flat at the underside of the flange, and the toe lip / front overhang are left off
LOBE_DEEP_SIDE = "left"   # v5.40: this half gets a DEEPER relief under the flange ("left" / "right" = the gun's side, None = both halves as LOBE_D)
LOBE_DEEP_D = 7.0          # depth of that relief, measured from the pocket floor (mm); it never gets closer than LOBE_DEEP_WALL to the outside of the grip
LOBE_DEEP_WALL = 2.0       # wall that is left on the outside (mm)
LOBE_DEEP_RAMP = False     # the top of the deeper relief is a 45 degree slope instead of a flat 4 mm wide ledge (the ledge was a horizontal overhang: a 'shelf' that would need support)
LOBE_DEEP_W = 30.0        # v5.40: on the half WITHOUT flange (FLANGE_REMOVE_SIDE) the deep relief is a cut-in of exactly this width (mm) ...
LOBE_DEEP_H = 10.0        # ... and this height, counted down from the flat top (the old flange underside). The ordinary 33 mm relief is not cut on that half, so a wall is left behind the cut-in.
LOBE_DEEP_BACK = 1.2       # v5.40: the cut-in (half without flange) is moved this far to the rear so the walls in front of and behind it are about equally thick (mm)
LOBE_DEEP_FRONT_WALL = 1.5 # v5.40: wall between the cut-in and the front edge of the grip (mm), the cut-in's front end runs parallel to the front edge (replaces LOBE_DEEP_BACK while the straight front is used)
FLANGE_REMOVE_STRAIGHT_FRONT = True   # v5.40: on the half without flange the front edge is the straight strap line (11 deg) carried on up to the top: no front arc, no neck
FRONT_TAPER_SIDE = "right"   # v5.40: this half gets a thin, evenly thick front edge ("left" / "right" = the gun's side, None = off)
FRONT_TAPER_L = 20.0         # the outer surface runs down to the front edge over this length (mm), smoothly (the blunt front face of 3-5 mm is gone)
FRONT_EDGE_ROUND = 0.6      # v5.40: radius of the rounding on the front edge itself (mm, 0 = sharp)
FRONT_TAPER_BLEND = 10.0     # v5.40: the run-out changes length gradually over about this height (mm) around the emblem
FRONT_EDGE_T = 1.5           # thickness of the front edge itself, from the pocket floor (mm), the same as the run-out at the bottom of the grip and at the tip of the flange
FRONT_EDGE_T_BOTTOM = 2.2    # v5.41: the front edge is thicker and rounder in the lower part of the grip (mm above the pocket floor; it was almost sharp, 0.3 mm). = FRONT_EDGE_T for no change
FRONT_EDGE_BOTTOM_Z0 = 16.0  # v5.41: full thickness up to this height (mm above the heel) ...
FRONT_EDGE_BOTTOM_Z1 = 46.0  # ... and then smoothly down to FRONT_EDGE_T at this height
FRONT_EDGE_SMOOTH = 2.2      # v5.41: mm; how softly the thicker edge merges into the surface behind it (no crease)
LOBE_DEEP_SHIFT = 0.0      # moves the deeper relief down from the ordinary relief (mm). 0 = same outline as the relief on the other side: its top is the floor of the notch in the flange

# top flange (sketch + photos)
FLANGE = True
FLANGE_LEN = 60.0          # length of the flange, front tip to rear end (was 70: now 10 mm shorter at the rear)
FLANGE_BLEND = 18.0        # the outside of the flange fades into the body over this many mm below the flange underside (no visible line). 0 = old step
FLANGE_SKIRT_LEN = 45.0    # the part that fills in under the flange where the body is thin (e.g. along the rear edge, the 'triangle') fades out over this length: it runs down into the grip without an edge
FLANGE_BLEND_MAX = 36.0    # half-thickness above the pocket floor beyond which the blend never reaches (thicker than any body)
REAR_TRIM = False         # cut the body back so that nothing sticks out behind the (shortened) flange
FLANGE_LEN_BASE = 70.0     # the old length: the body outline behind/under the flange and the tilt angle still refer to it
FLANGE_T = 10.0            # height of the flange
FLANGE_FRONT_OVERHANG = 23.0   # how far the front tip sticks out in front of the front strap (sketch ~24)
FLANGE_W_FRONT, FLANGE_W_REAR = 11.8, 11.8   # side-to-side thickness of the flange (front, rear); 11.8 mm all along
HEAD_AS_BODY = True        # v5.40: the top (flange + front overhang with the neck plate and the arc) is no longer a separate plate with its own flat faces: it is cut out of the
                           # grip's own swelling surface (the grip is extended to the top and forward over the toe) and gets the same inner cut-ins as before. False = old flange (v5.39)
HEAD_REAR_FOLLOW = True     # v5.40: the rear end of the top does not stick out behind the grip: its rear wall continues straight up from the wall of the raised rear part, and the edge roll (REAR_ARC_ROLL_R) continues up along it
HEAD_REAR_LEAN = 0.15       # the rear wall of the top starts with the lean of the arc below and eases off to this lean (mm forward per mm up) at the top
FRONT_FLARE_START = 13.5   # v5.40: mm below the toe where the inside corner under the toe leaves the front strap edge (tangent, no step)
REAR_ARC_STRAIGHT = True    # v5.40: the rear edge from the spur tip up to the top notch (the arc behind the wall, and its continuation up the rear end of the top) is ONE straight line, no outward bulge
HEAD_REAR_WALL = True       # v5.40: the part of the wall behind the pocket that lies outside the pocket floor continues up along the rear arc and closes the end of the relief under the flange, up to the top notch (the spur inside the pocket keeps its v5.39 length)
HEAD_MIN_WALL = 1.4         # v5.40: the top layer is at least FLANGE_NOTCH_W + this thick (outside the pocket floor), so the notch never eats right through the thin rear end of the swelling (kept small: a thicker floor made a shelf where it meets the grip below)
FLANGE_REBATE = 0.0        # the flange's inner face sits this much beyond the pocket floor (0 = on the floor)
FLANGE_NOTCH_W, FLANGE_NOTCH_D = 4.0, 4.0    # notch along the top of the flange, inner side: 4 mm wide (side to side, from the pocket floor), 4 mm deep (down)
FLANGE_TILT_DROP = 3.5     # the whole flange (with its top notch) is tilted about its front underside corner: the rear end sits this much lower
HEEL_REAR_DROP = 3.5       # the rear of the heel is extended this much further down (the heel line slopes down toward the rear)
FLANGE_REAR_DEEP = 3.0     # the rearmost part of the flange, right behind the relief under the flange, is cut this much deeper into its inner face (like the relief)
NECK_T = 7.7               # thickness of the thin plate under the flange in front (the arc), from the pocket floor. ESTIMATE
NECK_EDGE_BACK = 2.0       # below the toe the front edge of the neck plate sinks this much (mm) behind the front edge of the grip, so the plate disappears into the body instead of lying
                           # exactly on its edge (that left a hairline sliver ending in a point = the 'notch'). 0 = old (plate edge flush with the strap)
NECK_ARC_R_OUT = 3.0       # rounding of the outer edge of the front arc (the arc around the trigger where the finger rests), mm. 0 = sharp as before. Max about 3.5 (plate is NECK_T thick)
NECK_ARC_R_IN = 0.0        # same for the inner edge of the arc (facing the other half / the metal grip). 0 = off (it would leave a small step against the flange's square inner edge)
HEAD_TOE_DROP = 34.5       # top of the grip -> the toe (bottom of the front arc)
TOE_UNDER_RELIEF = 2.5     # v5.41: mm the lower part of the inside rounding under the toe is pulled back (it pressed into the index finger); 0 = as before
ARC_SPAN = 25.5            # height of the front arc
ARC_FRONT_DEPTH = 11.0     # how far the front arc goes in from the flange tip
REAR_ARC_LEN = 0.8         # from the flange's rear end forward to where the flange meets the body (0.8 = the flange ends at the rear edge)
UPPER_START_FRAC = 0.58    # from this height up the pocket may be deeper (tang / trigger-guard clearance)
UPPER_EXTRA_BACK = 0.0     # how much deeper toward the rear in that upper part (0 = same as below)
FRONT_BIAS = 0.10          # moves the swell forward so the open front edge keeps thickness (0 = symmetric)

# thumb rest shelf on the thumb-side half
THUMB_REST = False          # thumb rest off (not wanted for now)
THUMB_DROP = 25.0          # MEASURE: from the top of the grip down to the top of the shelf (where your thumb lies)
THUMB_LEN = 42.0           # length of the shelf from the front edge backward
THUMB_OUT = 7.0            # how far the shelf stands out from the grip surface
THUMB_LIP = 4.0            # thickness of the shelf's outer edge (underside slopes 45 deg back into the grip)

# finger grooves on the front edge: list of (height of groove centre above the heel, depth). [] = none
FINGER_GROOVES = []        # e.g. [(22.0, 1.5), (42.0, 1.5)] - MEASURE with your hand on the gun
FINGER_GROOVE_R = 11.0     # radius of each groove (about half a finger width)

# screws, one per hole: (from the top of the grip down, "front" or "rear", distance from that edge at that height) - from your sketch
SCREW_POS = [(PAD_TOP_DROP + 33.5, "front", PAD_FRONT_INSET + PAD_W + 4.0),   # 33.5 below the tenon top, 4 mm behind its rear side
             (GRIP_HEIGHT_MM - 25.5, "rear", 24.5)]                            # 25.5 above the bottom, 24.5 from the rear edge
SCREW_D = 3.4              # M3 clearance
HEAD_D, HEAD_DEPTH = 6.4, 2.0
SCREW_RING = 1.5           # smooth (unchecked) ring around each screw head
# v5.40: the halves are screwed together from the gun's LEFT side. The half named in INSERT_SIDE gets a blind hole for a threaded (heat-set) insert at each screw
# instead of the through hole and the screw-head recess, so its outside stays smooth. The hole starts where the screw comes in (the pocket floor, or the joint face
# where the screw passes through the wall) and is INSERT_L + INSERT_MELT deep, but always leaves INSERT_MIN_WALL of plastic on the outside.
INSERT_SIDE = "right"      # "right" / "left" = the gun's side that gets the inserts, None = through holes + screw heads on both halves as before
INSERT_D = 4.2             # hole diameter (mm): M3 heat-set insert of 4.6 mm outer diameter in PETG. Check against YOUR insert / print a test hole first
INSERT_L = 5.7             # length of the insert (mm) (M3 x 5.7 is the common short one)
INSERT_MELT = 1.0          # extra depth for the molten plastic displaced by the insert (mm)
INSERT_MIN_WALL = 1.6      # least plastic left between the end of the hole and the outside of the grip (mm)
INSERT_THROUGH = True      # the hole carries on through to the outside as a SCREW_D clearance hole (the screw tip may pass the insert); False = blind hole

# v5.40: EMBLEM (a shield with a cross, as on the photo you sent), part of the grip itself and printed with it as a pattern on the outside: a smooth rim and a smooth
# cross stay at the surface, the field between them is sunk LOGO_DEPTH (plain recess - the fine hatching of the original is too fine for FDM).
# LOGO_MODE = "integrated": cut into the outside of the half (no extra part).
# LOGO_MODE = "overlay" / "inlay": the emblem is made as a SEPARATE object (glued ON the surface, LOGO_T proud / glued into a shield pocket with a flat floor).
LOGO_MODE = "integrated"
LOGO = True               # True = cut the emblem into the grip (LOGO_MODE below); False = off, the grip is left plain
LOGO_SIDE = "both"         # the gun's side that gets it: "left" (the side with the screw heads, as on your photo) / "right" / "both"
LOGO_W, LOGO_H = 26.0, 31.0   # width / height of the shield (mm)
LOGO_FROM_FRONT = 22.0     # centre of the shield this far behind the front edge of the grip (mm)
LOGO_Z = 42.7              # height of the centre above the heel (mm)
LOGO_T = 2.0               # overlay: height of the rim and the cross above the grip surface (mm)
LOGO_DEPTH = 0.8           # depth of the sunken field in the emblem (mm)
LOGO_RIM = 1.4             # width of the smooth rim (mm)
LOGO_CROSS = 0.62          # extent of the cross as a fraction of the shield width (arm width = 0.3 of that, as on the Swiss flag)
LOGO_ROT = 0.0             # rotation (degrees, + = counter-clockwise seen from the outside of the left half)
LOGO_POCKET_MIN = 2.4      # inlay: thickness of the emblem at the lowest point of the surface under it = depth of the pocket there (mm)
LOGO_FIT = 0.15            # inlay: the pocket is this much bigger than the emblem all round (mm)

# recessed checkering panel with border
PANEL = False              # recessed checkered panel: OFF (the checkering crashed FreeCAD). Leave False in future models.
GROOVES = False            # simple pattern instead: straight vertical V-grooves on the lower part (few, simple cuts: light on FreeCAD)
GROOVE_PITCH = 2.4         # mm between the grooves
GROOVE_HALF = 0.5          # half-diagonal of the V-groove
GROOVE_DEPTH = 0.4         # groove depth below the surface
GROOVE_SEG = 18.0          # longest straight piece of a groove (the grooves follow the surface in pieces)
PANEL_FLAT_Y = _HALF_MAX - 2.0   # half-thickness at the panel floor (smaller = deeper recess): 2 mm recess at the palm swell
CHECKERING = True          # diamond checkering (slower to compute: set False for a quick preview)
CHECKER_PITCH = 1.6        # mm between grooves (0.4 mm nozzle: 1.6 - 2.4 works)
CHECKER_DEPTH = 0.40
PANEL_CURVED = True        # the panel follows the curved surface of the grip (recess PANEL_RECESS deep, checkering swept along the surface). False = old flat panel
PANEL_RECESS = 0.5         # how far the checkered panel sits below the smooth rim (mm)
CHECKER_HALF = 0.55        # half-diagonal of the groove cross-section (V-groove depth below the panel surface)

# breakaway ribs under the pocket floor and the tang cut-in (overhangs when the half lies on its inner face)
SUPPORT_RIBS = False        # v5.40: off at the user's request (the halves are printed standing); True = breakaway ribs under the pocket floor, tang cut-in, toe and the deeper relief
RIB_T = 0.8                # rib thickness (2 perimeters)
RIB_PITCH = 6.0            # spacing between ribs
RIB_GAP = 0.25             # air gap up to the pocket floor / tenon (about one layer)
RIB_PAD_GAP = 0.0          # v5.40: gap under the raised tenon pad. 0 = the ribs touch it, so the slicer sees it as supported (with 0.25 Orca warns "floating regions"); the stubs must be scraped off before the tenon is fitted
RIB_SIDE_GAP = 1.2         # gap to walls beside the rib (was 0.6; raised to keep the slicer from flagging path conflicts)
RIB_UNDER_TOE = True       # also ribs under the front overhang (toe + neck plate in front of the strap), so no slicer support is needed anywhere

LAYOUT = "print"           # "print" = halves flat on their inner faces, "assembled" = as on the gun
SHOW_FRAME_REF = True
PRINT_TEST = False         # True = only the band with the tenon and the upper screw, for a fit test
FIT_PLATE = False          # True = only a thin plate (pocket + tenon), printed on its outer cut face. Overrides PRINT_TEST
FIT_PLATE_T = 3.0          # plate thickness above the pocket floor
EXPORT_DIR = ""

# ----------------------------------------------------------------------------
# TRACED OUTLINE (photo pixels, front is on the LEFT in the photo; x is flipped so front = +X)
# ----------------------------------------------------------------------------
# where the flange meets the body at the rear, in photo pixels (derived from the flange parameters)
_SX0 = 112.0 / 940.0
FRONT_PX = 540.0                                       # front strap line (photo pixels)
JUNC_PX = min(FRONT_PX - FLANGE_FRONT_OVERHANG / _SX0 + (FLANGE_LEN_BASE - REAR_ARC_LEN) / _SX0, 930.0)    # = flange end minus REAR_ARC_LEN
_HEEL_REAR_PY = 985.0 + HEEL_REAR_DROP / ((GRIP_HEIGHT_MM + TOP_TRIM) / 940.0)   # rear heel corner, lowered by HEEL_REAR_DROP
# v5.39: the front edge (the strap) follows the metal frame instead of bowing out: from FRONT_FOLLOW_PY0 (photo row, just below the rounding under the toe) it runs
# straight down at the same angle as the pocket (= the lower part of the pocket's rear wall, the rake of the frame), after a soft run-in over FRONT_FOLLOW_BLEND rows.
# Above that row nothing changes. FRONT_FOLLOW = False gives the old traced curve back (v5.32).
FRONT_FOLLOW = True
FRONT_FOLLOW_PY0 = 480.0
FRONT_FOLLOW_BLEND = 120.0
FRONT_FOLLOW_STRAIGHT = True                               # v5.40: the strap edge between the rounding under the toe and the straight 11 deg run is a straight line (the old blend bulged out a little)
FRONT_FLARE_LOWER = 3.0                                     # mm: the flare under the toe begins this far below the end of the straight strap line (tangent to it)
FRONT_FOLLOW_PX0 = 540.0                                    # front edge at that row on the traced curve
RAKE_FIXED = 11.0294607910                                  # pocket rake of the traced outline (v5.32): the pocket and tenon must not tilt when the front edge changes
if FRONT_FOLLOW:
    _kf = math.tan(math.radians(RAKE_FIXED)) * ((GRIP_HEIGHT_MM + TOP_TRIM) / 940.0) / _SX0     # photo pixels sideways per photo pixel down, at the pocket angle
    _py_b = FRONT_FOLLOW_PY0 + FRONT_FOLLOW_BLEND
    _x_b = FRONT_FOLLOW_PX0 + _kf * FRONT_FOLLOW_BLEND / 2.0
    _blend = [(FRONT_FOLLOW_PX0 + _kf * (py - FRONT_FOLLOW_PY0) ** 2 / (2.0 * FRONT_FOLLOW_BLEND), py) for py in (_py_b, _py_b - 30.0, _py_b - 60.0, _py_b - 90.0, FRONT_FOLLOW_PY0)]
    _HEEL_FRONT = (_x_b + _kf * (990.0 - _py_b), 990.0)
    _FRONT = [("L", [_HEEL_FRONT, (_x_b, _py_b)]),
              ("S", _blend + [(538, 390), (541, 230), (546, 50)])]
    if FRONT_FOLLOW_STRAIGHT:
        # v5.40: no bulge on the strap: the 11 deg line (the frame's rake) simply runs on STRAIGHT, from the heel all the way up to FRONT_FOLLOW_PY0 (where the rounding under the toe begins).
        # Above that the outline eases back (over 80 rows, tangent to the line) onto the old curve, so the toe area further up (xs, the flange) does not move at all.
        _old = Part.BSplineCurve()
        _old.interpolate([V(px_, 0.0, py_) for px_, py_ in _blend + [(538, 390), (541, 230), (546, 50)]])
        _dp = _old.discretize(Number=1200)

        def _old_at(row):
            for a_, b_ in zip(_dp, _dp[1:]):
                if (a_.z - row) * (b_.z - row) <= 0 and abs(b_.z - a_.z) > 1e-9:
                    return (a_.x + (b_.x - a_.x) * (row - a_.z) / (b_.z - a_.z), row)
            return None
        _x_l = _x_b - _kf * FRONT_FOLLOW_BLEND                                    # the 11 deg line at FRONT_FOLLOW_PY0
        _Lt = 80.0
        _ease = []
        for _d in (12.0, 25.0, 40.0, 55.0, 68.0):
            _r = FRONT_FOLLOW_PY0 - _d
            _o = _old_at(_r)
            _s = _d / _Lt
            _w = 1.0 - 3.0 * _s * _s + 2.0 * _s ** 3
            _ease.append(None if _o is None else (_o[0] + (_x_l - _kf * _d - _o[0]) * _w, _r))
        _up = [(_x_l, FRONT_FOLLOW_PY0)] + _ease + [_old_at(r_) for r_ in (390.0, 330.0, 270.0, 210.0, 150.0, 100.0)] + [(546, 50)]
        if all(q_ is not None for q_ in _up):
            _FRONT = [("L", [_HEEL_FRONT, (_x_l, FRONT_FOLLOW_PY0)]), ("S", _up)]
else:
    _FRONT = [("S", [(615, 990), (590, 900), (562, 800), (548, 700), (543, 600), (540, 480), (538, 390), (541, 230), (546, 50)])]
    _HEEL_FRONT = (615, 990)
OUTLINE = [
    ("L", [(546, 50), (JUNC_PX, 50)]),                                                    # top (above the flange underside it is replaced by the flange)
    ("S", [(JUNC_PX, 50), (JUNC_PX, 145)] + [(JUNC_PX + (940 - JUNC_PX) * (py - 145) / 155.0, py) for py in (200, 250)] + [(940, 300)]),   # rear, up to the flange
    ("S", [(940, 300), (990, 400), (1060, 560), (1110, 690), (1150, 830), (1185, _HEEL_REAR_PY)]),          # rear edge (heel depth 68 mm)
    ("L", [(1185, _HEEL_REAR_PY), _HEEL_FRONT]),                                                     # heel
] + _FRONT                                                                                # front strap, straight up (the flange overhang is added separately)
PANEL_PX = [(560, 392), (640, 368), (720, 358), (800, 380), (875, 420), (940, 470), (995, 540), (1040, 620),
            (1085, 740), (1115, 860), (1155, 960), (1125, 968), (640, 972), (578, 900), (565, 800), (560, 700),
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
            try:
                if shape.Volume > 1.0 and (len(r.Solids) == 0 or r.Volume < 0.3 * shape.Volume):      # an 'empty but valid' result is a failed boolean, not a result
                    App.Console.PrintWarning("%s emptied the shape (volume %.0f -> %.0f) - skipped.\n" % (label, shape.Volume, r.Volume))
                    return shape
            except Exception:
                pass
            return r
        App.Console.PrintWarning("%s gave invalid geometry - skipped.\n" % label)
    except Exception as e:
        App.Console.PrintWarning("%s failed (%s) - skipped.\n" % (label, e))
    return shape


def _tangent_groups(shape, idx):
    """edges (indices) that run on into each other tangentially (angle < 8 deg at the shared vertex) belong together: a fillet can only start or stop at a corner, not in the middle of such a chain"""
    parent = {i: i for i in idx}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for ai, i in enumerate(idx):
        for j in idx[ai + 1:]:
            ei, ej = shape.Edges[i], shape.Edges[j]
            for vi in ei.Vertexes:
                for vj in ej.Vertexes:
                    if not vi.isSame(vj):
                        continue
                    try:
                        ti = ei.tangentAt(ei.parameterAt(vi))
                        tj = ej.tangentAt(ej.parameterAt(vj))
                        if ti.Length > 1e-9 and tj.Length > 1e-9 and abs(ti.normalize().dot(tj.normalize())) > math.cos(math.radians(8.0)):
                            parent[find(i)] = find(j)
                    except Exception:
                        pass
    groups = {}
    for i in idx:
        groups.setdefault(find(i), []).append(i)
    return sorted(groups.values(), key=lambda g: min(g))


def fillet_soft(label, shape, r, edges, legacy=False):
    """fillet as many of the edges as OCC will take (one failing edge no longer drops them all); edges that run on tangentially are tried together first.
    Every step is checked: one solid, valid, bounding box not larger, and no more material removed than rounding those edges can explain (a broken fillet can be 'valid' and still be wrong)."""
    sel = [i for i, e in enumerate(shape.Edges) if any(e.isSame(x) for x in edges)]
    base_bb = shape.BoundBox
    base_vol = shape.Volume if not legacy else 0.0
    state = {"res": None}

    def _try(lst, check_vol=False):
        try:
            res = shape.makeFillet(r, [shape.Edges[j] for j in lst])
            if res.isNull() or not res.isValid() or len(res.Solids) != 1:
                return None
            if check_vol:                                       # (slow, so only for the steps that round several edges at once)
                b = res.BoundBox
                if b.XMin < base_bb.XMin - 0.05 or b.XMax > base_bb.XMax + 0.05 or b.YMin < base_bb.YMin - 0.05 or b.YMax > base_bb.YMax + 0.05 or b.ZMin < base_bb.ZMin - 0.05 or b.ZMax > base_bb.ZMax + 0.05:
                    return None
                if abs(base_vol - res.Volume) > 0.6 * r * r * sum(shape.Edges[j].Length for j in lst) + 5.0:
                    return None
            return res
        except Exception:
            return None
    used = []
    refused = []
    for i in sel:                                               # 1. one edge at a time, exactly as in v5.39 (these edges come out the same everywhere)
        res = _try(used + [i])
        if res is not None:
            used.append(i)
            state["res"] = res
        elif shape.Edges[i].Length > 1e-3:
            refused.append(i)
    if refused and not legacy:                                  # 2. a chain of edges that run on into each other can only be rounded as a whole: take every edge OCC refused together with
        try:                                                    #    the edges it runs on into (and the refused chains next to it) and round that set in one go
            parts = [g for g in _tangent_groups(shape, [i for i in sel if shape.Edges[i].Length > 1e-3]) if any(i in refused for i in g)]
            merged = []
            for g_ in parts:
                g_ = list(g_)
                rest = []
                for m_ in merged:
                    if any(v.isSame(w) for a_ in g_ for v in shape.Edges[a_].Vertexes for b_ in m_ for w in shape.Edges[b_].Vertexes):
                        g_ += m_
                    else:
                        rest.append(m_)
                merged = rest + [g_]
            for m_ in merged:
                trial = [u for u in used if u not in m_] + m_
                res = _try(trial, True)
                if res is not None:
                    used = trial
                    state["res"] = res
                    App.Console.PrintMessage("%s: %d connected edges rounded together.\n" % (label, len(m_)))
        except Exception:
            pass
    # edges that run on into each other tangentially (a long front edge made of several pieces) cannot be rounded one piece at a time: try the left-over ones in connected groups
    try:
        failed = [i for i in sel if i not in used and shape.Edges[i].Length > 1e-3]
        groups = []
        for i in failed:
            g_ = [i]
            rest = []
            for g2 in groups:
                if any(v.isSame(w) for a_ in g_ for v in shape.Edges[a_].Vertexes for b_ in g2 for w in shape.Edges[b_].Vertexes):
                    g_ += g2
                else:
                    rest.append(g2)
            groups = rest + [g_]
        for g_ in sorted(groups, key=lambda g: -len(g)):
            if len(g_) < 2:
                continue
            res = _try(used + g_, True)
            if res is not None:
                used += g_
                state["res"] = res
                App.Console.PrintMessage("%s: %d connected edges rounded together.\n" % (label, len(g_)))
    except Exception:
        pass
    if len(used) < len(edges):
        App.Console.PrintWarning("%s: rounded %d of %d edges.\n" % (label, len(used), len(edges)))
        for i_, e_ in enumerate(shape.Edges):                          # say which ones were left sharp (where they are), so a sharp spot can be found
            if i_ not in used and any(e_.isSame(x_) for x_ in edges):
                b_ = e_.BoundBox
                App.Console.PrintMessage("  left sharp: x %.1f..%.1f  y %.1f..%.1f  z %.1f..%.1f  length %.1f\n" % (b_.XMin, b_.XMax, b_.YMin, b_.YMax, b_.ZMin, b_.ZMax, e_.Length))
    if not legacy and used and state["res"] is not None:         # final check of the whole result; if it does not hold, do it the old way (one edge at a time)
        if abs(base_vol - state["res"].Volume) > 0.6 * r * r * sum(shape.Edges[j].Length for j in used) + 5.0:
            App.Console.PrintWarning("%s: grouped rounding gave a doubtful result - rounding one edge at a time instead.\n" % label)
            return fillet_soft(label, shape, r, edges, True)
    return state["res"] if (used and state["res"] is not None) else shape


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


# v5.40: outline of the half WITHOUT flange: the straight strap line (the frame's rake) simply carried on from the heel up to the top row, instead of the curve with the toe / neck
prism_left = None
x_line_front = None
if FRONT_FOLLOW and "_kf" in globals():
    try:
        _hp = P(*_HEEL_FRONT)                                           # heel end of the straight front line (grip mm)
        _zq = 50.0
        _sl = (x_range(_zq)[1] - _hp.x) / (_zq - _hp.z)               # lean of the straight lower part of the front edge, mm per mm (the rake of the frame)
        x_line_front = lambda z_: _hp.x + _sl * (z_ - _hp.z)           # that line carried on up
        _zT = P(0.0, 50.0).z                                            # top row of the outline
        _T = V(x_line_front(_zT), 0, _zT)
        _el = Part.makePolygon([_T, V(P(JUNC_PX, 50.0).x, 0, _zT)]).Edges
        for _kind, _pts in OUTLINE[1:4]:
            _vs = [P(*p_) for p_ in _pts]
            if _kind == "L":
                _el += Part.makePolygon(_vs).Edges
            else:
                _bs = Part.BSplineCurve()
                _bs.interpolate(_vs)
                _el.append(_bs.toShape())
        _el += Part.makePolygon([V(_hp.x, 0, _hp.z), _T]).Edges
        prism_left = Part.Face(Part.Wire(_el)).extrude(V(0, 140, 0))
        prism_left.translate(V(0, -70, 0))
    except Exception as e:
        App.Console.PrintWarning("Straight front outline could not be made (%s) - the original outline is used.\n" % e)
        prism_left = None
        x_line_front = None

BODY_PRISM = prism                                  # outline of the body (with HEAD_AS_BODY: body outline + the head outline, set after the flange block)
HEAD_PTS = None                                     # discretised head outline (HEAD_AS_BODY): the swelling must also cover the front overhang


def head_front(z):
    z = min(max(z, 0.5), H - 0.5)
    best = -1.0e9
    for a, b in zip(HEAD_PTS, HEAD_PTS[1:] + HEAD_PTS[:1]):
        if (a.z - z) * (b.z - z) <= 0 and abs(b.z - a.z) > 1e-9:
            best = max(best, a.x + (b.x - a.x) * (z - a.z) / (b.z - a.z))
    return best


def ellipse_params(z, palm):
    rear, front = x_range(z)
    if HEAD_PTS is not None:
        front = max(front, head_front(z))
    depth = front - rear
    xc = (rear + front) / 2.0 + FRONT_BIAS * depth
    a = EDGE_FULLNESS * depth * (0.5 + FRONT_BIAS) + 2.0
    b = width_at(z) / 2.0 + (PALM_EXTRA * interp(_SWELL, z / H) if palm else 0.0)
    return xc, max(a, b + 1.0), b


def surface_y(x, z, palm):
    """approximate half-thickness of the swell at (x, z)"""
    xc, a, b = ellipse_params(z, palm)
    return b * math.sqrt(max(0.0, 1.0 - ((x - xc) / a) ** 2))


def rear_roll_tool(palm):
    """corner cutter along the rear edge: removes the sharp outer rear corner so that the outside rolls over in a radius REAR_ROLL_R toward the inner side"""
    secs = []
    n = 16
    for i in range(n + 1):
        z = -2.0 + (H + 4.0) * i / float(n)
        rear = x_range(min(max(z, 0.0), H))[0]
        xc_, a_, b_ = ellipse_params(min(max(z, 0.0), H), palm)
        R0 = REAR_ROLL_R
        Ys = surface_y(rear + R0, z, palm)                        # outer surface level just in front of the rear edge
        R = min(R0, Ys - FLOOR_Y - 0.4)
        if R < 1.0:
            R = 1.0
            Ys = FLOOR_Y + R + 0.4
        cx_, cy_ = rear + R, Ys - R                               # centre of the rounding circle
        pts = [V(rear - 2.0, Ys + 2.0, z), V(rear + R, Ys + 2.0, z), V(rear + R, Ys, z)]
        for k in range(1, 12):                                    # quarter circle from the top (rear+R, Ys) round to the rear plane (rear, Ys-R)
            ang = math.pi / 2.0 + (math.pi / 2.0) * k / 11.0
            pts.append(V(cx_ + R * math.cos(ang), cy_ + R * math.sin(ang), z))
        pts.append(V(rear - 2.0, cy_, z))
        secs.append(Part.makePolygon(pts + [pts[0]]))
    return Part.makeLoft(secs, True, True, False)


def round_rear_edge(body):
    """real fillet on the sharp crease where the flat rear wall of the outline meets the swelling outer surface (on both sides of the mid plane).
    Tries REAR_ROLL_R first and then smaller radii until OCC accepts one."""
    sel = []
    for e in body.Edges:
        try:
            pts = e.discretize(Number=6)
        except Exception:
            continue
        if e.Length < 4.0:
            continue
        ok = True
        for p in pts:
            zc = min(max(p.z, 0.0), H)
            if abs(p.y) < 4.0 or abs(p.x - x_range(zc)[0]) > 1.2:
                ok = False
                break
        if ok:
            sel.append(e)
    App.Console.PrintMessage("Rear edge: %d crease edge(s) found.\n" % len(sel))
    if not sel:
        App.Console.PrintWarning("Rear edge: no crease edge found - nothing rounded.\n")
        return body
    for r in (REAR_ROLL_R, 0.75 * REAR_ROLL_R, 0.55 * REAR_ROLL_R, 0.4 * REAR_ROLL_R, 0.3 * REAR_ROLL_R):
        try:
            res = body.makeFillet(r, sel)
            if res.isValid() and not res.isNull() and res.Volume > 0.5 * body.Volume:
                App.Console.PrintMessage("Rear edge rounded with radius %.1f mm.\n" % r)
                return res
        except Exception:
            pass
    App.Console.PrintWarning("Rear edge: OCC refused every radius - left sharp.\n")
    return body


def make_body(palm, bprism=None):
    secs = []
    for fz in (-0.04, 0.10, 0.28, 0.46, 0.64, 0.82, 1.04):
        z = fz * H
        xc_, a_, b_ = ellipse_params(z, palm)
        secs.append(Part.Wire([Part.Ellipse(V(xc_, 0, z), a_, b_).toShape()]))
    body = (BODY_PRISM if bprism is None else bprism).common(Part.makeLoft(secs, True, False, False))
    for zg, depth in FINGER_GROOVES:
        r = FINGER_GROOVE_R
        body = try_op("Finger groove at %.0f mm" % zg, lambda s: s.cut(Part.makeCylinder(
            r, 140.0, V(x_range(zg)[1] + r - depth, -70.0, zg), V(0, 1, 0))), body)
    if REAR_ROLL_R > 0:
        body = round_rear_edge(body)
    if EDGE_R > 0:
        body = fillet_soft("Edge rounding", body, EDGE_R, body.Edges)
    return body


# ----------------------------------------------------------------------------
# 3. FRAME POCKET (rotated to the grip's own rake, so it follows the traced outline)
# ----------------------------------------------------------------------------
z1, z2 = 0.25 * H, 0.65 * H
m1, m2 = sum(x_range(z1)) / 2.0, sum(x_range(z2)) / 2.0
RAKE = math.degrees(math.atan2(m2 - m1, z2 - z1))           # positive = bottom is rearward
if FRONT_FOLLOW:
    RAKE = RAKE_FIXED
TR, CR = math.tan(math.radians(RAKE)), math.cos(math.radians(RAKE))

pad_zc = H - PAD_TOP_DROP - PAD_L / 2.0                       # tenon centre height (21.05 mm below the top of the finished grip)
front_edge = x_range(pad_zc)[1]
if FRONT_FOLLOW and FRONT_FOLLOW_STRAIGHT and "_dp" in globals():
    # the straight strap line (v5.40) lies a little in front of the old curve up here: the pocket must NOT move with it, so it keeps being measured from the old front edge (v5.39)
    _ref = [P(q_.x, q_.z) for q_ in _dp]
    for _a, _b in zip(_ref, _ref[1:]):
        if (_a.z - pad_zc) * (_b.z - pad_zc) <= 0 and abs(_b.z - _a.z) > 1e-9:
            front_edge = _a.x + (_b.x - _a.x) * (pad_zc - _a.z) / (_b.z - _a.z)
            break
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


# the pocket's rear wall is not straight on the original: it bulges rearward around the middle and returns at a knee further down
# (traced from the pencil sketch; depth = mm below the TOP of the tenon, extra = mm the wall moves rearward). Tune WALL_BULGE_SCALE if needed.
WALL_BULGE = True
WALL_BULGE_SCALE = 0.6
WALL_BULGE_PROFILE = [(0.0, 0.0), (36.0, 0.0), (40.5, 3.0), (45.5, 9.5), (51.0, 6.0), (56.0, 2.0), (61.0, 0.0), (999.0, 0.0)]
if WALL_BULGE:
    def _bulge(t):
        for (t0, e0), (t1, e1) in zip(WALL_BULGE_PROFILE, WALL_BULGE_PROFILE[1:]):
            if t0 <= t <= t1:
                k = (t - t0) / (t1 - t0)
                return WALL_BULGE_SCALE * (e0 + (e1 - e0) * 0.5 * (1.0 - math.cos(math.pi * k)))
        return 0.0
    _tt = [36.0 + WALL_SHIFT + 0.5 * i for i in range(0, 52)]                       # 36 ... 61.5 mm below the tenon top
    _zl = lambda t: PAD_L / 2.0 - t                                     # local z (0 = tenon centre)
    _pb = [V(-C - _bulge(t - WALL_SHIFT), 0, _zl(t)) for t in _tt] + [V(1.0, 0, _zl(_tt[-1])), V(1.0, 0, _zl(_tt[0]))]
    _bulge_solid = Part.Face(Part.makePolygon(_pb + [_pb[0]])).extrude(V(0, 2.0 * FLOOR_Y, 0))
    _bulge_solid.translate(V(0, -FLOOR_Y, 0))
    cavity = try_op("Rear wall bulge", lambda sh: sh.fuse(to_pocket_frame(_bulge_solid)), cavity)

# lower part of the wall: wider around the screw hole (the hole sits in the wall), and an incision at the very bottom (as on the original)
WALL_LOWER = True
WALL_SCREW_WIDEN = 4.0     # the wall is this much wider (pocket narrower) around the lower screw
WALL_SCREW_PROFILE = [(0.0, 0.0), (60.0, 0.0), (65.0, 1.0), (76.0, 1.0), (82.0, 0.0), (999.0, 0.0)]   # (mm below the tenon top, fraction of WALL_SCREW_WIDEN)
WALL_BOTTOM_NOTCH = 8.0    # incision at the bottom of the wall (pocket wider), mm rearward
WALL_NOTCH_PROFILE = [(0.0, 0.0), (82.0, 0.0), (91.0, 1.0), (999.0, 1.0)]                              # (mm below the tenon top, fraction of WALL_BOTTOM_NOTCH)
wall_addon = None
wall_addon_clear = None
if WALL_LOWER:
    def _prof(table, t):
        for (t0, e0), (t1, e1) in zip(table, table[1:]):
            if t0 <= t <= t1:
                k = (t - t0) / (t1 - t0)
                return e0 + (e1 - e0) * 0.5 * (1.0 - math.cos(math.pi * k))
        return 0.0
    _zl2 = lambda t: PAD_L / 2.0 - t
    _t_bot = PAD_L / 2.0 + pad_zc                                       # depth of the grip's bottom below the tenon top
    _tn = [78.0 + WALL_SHIFT + 0.5 * i for i in range(0, int((_t_bot + 6.0 - 78.0 - WALL_SHIFT) / 0.5) + 1)]
    _pn = [V(-C - WALL_BOTTOM_NOTCH * _prof(WALL_NOTCH_PROFILE, t - WALL_SHIFT), 0, _zl2(t)) for t in _tn] + [V(1.0, 0, _zl2(_tn[-1])), V(1.0, 0, _zl2(_tn[0]))]
    _notch = Part.Face(Part.makePolygon(_pn + [_pn[0]])).extrude(V(0, 2.0 * FLOOR_Y, 0))
    _notch.translate(V(0, -FLOOR_Y, 0))
    cavity = try_op("Wall bottom incision", lambda sh: sh.fuse(to_pocket_frame(_notch)), cavity)
    _ta = [58.0 + WALL_SHIFT + 0.5 * i for i in range(0, 49)]                        # 58 ... 82 mm below the tenon top
    _pa = [V(-C + WALL_SCREW_WIDEN * _prof(WALL_SCREW_PROFILE, t - WALL_SHIFT), 0, _zl2(t)) for t in _ta] + [V(-C - 1.0, 0, _zl2(_ta[-1])), V(-C - 1.0, 0, _zl2(_ta[0]))]
    wall_addon = Part.Face(Part.makePolygon(_pa + [_pa[0]])).extrude(V(0, FLOOR_Y + 1.0, 0))
    wall_addon = to_pocket_frame(wall_addon)
    # the same shape a little larger (for the support ribs: they keep clear of the widened wall)
    _tc = [56.5 + WALL_SHIFT + 0.5 * i for i in range(0, 56)]
    _pc = [V(-C + WALL_SCREW_WIDEN * _prof(WALL_SCREW_PROFILE, t - WALL_SHIFT) + RIB_SIDE_GAP + 0.4, 0, _zl2(t)) for t in _tc] + [V(-C - 1.0, 0, _zl2(_tc[-1])), V(-C - 1.0, 0, _zl2(_tc[0]))]
    wall_addon_clear = Part.Face(Part.makePolygon(_pc + [_pc[0]])).extrude(V(0, 200.0, 0))
    wall_addon_clear.translate(V(0, -50.0, 0))
    wall_addon_clear = to_pocket_frame(wall_addon_clear)


def pocket_rear(z):
    return wall_x0 - C + TR * (z - pad_zc) - (UPPER_EXTRA_BACK if z >= zu else 0.0)


# top-rear cut-in (the black-marked area): from the pocket's rear wall back through the rear edge, down to TANG_Z0
TANG_Z0 = H + TOP_TRIM - TANG_DROP_OLD - C
rear_cut = None
REAR_ARC_PTS = []
if TANG_CUT:
    zs = [TANG_Z0 + i * (H - TANG_Z0) / 10.0 for i in range(11)]
    tx_min = min(x_range(z)[0] for z in zs) - 20.0
    tx_max = pocket_rear(H) + 3.0                      # reaches into the pocket at every height (no wood sliver)
    tang = Part.makeBox(tx_max - tx_min, 2.0 * FLOOR_Y, H + 6.0 - TANG_Z0, V(tx_min, -FLOOR_Y, TANG_Z0))
    if TANG_TAPER:
        # the raised rear part (the "wall" behind the pocket) narrows to a thin spur at its upper end, under the flange; the cut-in above it
        # follows a concave curve (traced from the photo of the original): dx = mm rearward of the pocket wall, dz = mm below the spur tip
        z_sp = H - FLANGE_T - TANG_SPUR_BELOW_FLANGE
        # the raised rear part must not reach further back than the (shortened) flange: shift the spur tip forward to the flange's rear end
        # and let the shift fade out down the concave curve (so it still runs out nicely into the rear edge of the grip)
        _x_end_fl = x_range(H - HEAD_TOE_DROP)[1] + FLANGE_FRONT_OVERHANG - FLANGE_LEN
        _x_t0 = pocket_rear(z_sp) - TANG_SPUR_W
        _shift = max(0.0, (_x_end_fl + 0.3) - _x_t0)
        App.Console.PrintMessage("Raised rear part: spur tip shifted %.1f mm forward (flange rear end x=%.1f).\n" % (_shift, _x_end_fl))
        _cv = [V(pocket_rear(z_sp - dz) - TANG_SPUR_W - dx * TANG_TAPER_SCALE + _shift * max(0.0, 1.0 - dz / 45.0), 0, z_sp - dz)
               for dx, dz in TANG_CURVE]
        _bs = Part.BSplineCurve()
        _bs.interpolate(_cv)
        _pts = _bs.discretize(Number=40)
        _keep = []
        for p in _pts:
            _keep.append(p)
            if p.x <= x_range(p.z)[0] - 1.0:           # the curve has reached the rear edge of the grip
                break
        _poly = [V(tx_max, 0, H + 6.0), V(tx_max, 0, z_sp), V(pocket_rear(z_sp) - TANG_SPUR_W + _shift, 0, z_sp)] + _keep
        _poly += [V(tx_min, 0, _keep[-1].z), V(tx_min, 0, H + 6.0)]
        tang_t = Part.Face(Part.makePolygon(_poly + [_poly[0]])).extrude(V(0, 2.0 * FLOOR_Y, 0))
        tang_t.translate(V(0, -FLOOR_Y, 0))
        tang = tang_t
        # the whole thickness behind the spur is cut away too: the rear edge follows the same concave curve, and from the spur tip it
        # rises in a short arc up to the flange underside (the flange itself is added afterwards and is not touched)
        z_fl_ = H - FLANGE_T
        x_t = pocket_rear(z_sp) - TANG_SPUR_W + _shift
        x_a = pocket_rear(z_fl_) - 1.0
        # the arc must end at the rear end of the (shortened) flange, not behind it: nothing may stick out behind the flange
        _x_end_fl = x_range(H - HEAD_TOE_DROP)[1] + FLANGE_FRONT_OVERHANG - FLANGE_LEN
        if x_a < _x_end_fl + 0.3:
            App.Console.PrintMessage("Rear arc end moved forward from x=%.1f to the flange's rear end x=%.1f.\n" % (x_a, _x_end_fl + 0.3))
            x_a = _x_end_fl + 0.3
        h_ = z_fl_ - z_sp
        _ab = Part.BSplineCurve()
        _ab.interpolate([V(x_t, 0, z_sp), V(x_t + 0.8, 0, z_sp + 0.45 * h_), V(x_t + 0.55 * (x_a - x_t), 0, z_sp + 0.8 * h_), V(x_a, 0, z_fl_)])
        _arc = _ab.discretize(Number=14)
        if REAR_ARC_STRAIGHT:
            _arc = [V(x_t + (x_a - x_t) * k_ / 14.0, 0, z_sp + h_ * k_ / 14.0) for k_ in range(15)]      # straight from the spur tip to the flange underside
        _rp = [V(tx_min, 0, z_fl_)] + list(reversed(_arc)) + _keep[1:] + [V(tx_min, 0, _keep[-1].z)]
        REAR_ARC_PTS = [(p.x, p.z) for p in (list(reversed(_arc)) + _keep[1:])]       # the curve of the cut-in in the XZ plane (for rounding its outer edge)
        rear_cut = Part.Face(Part.makePolygon(_rp + [_rp[0]])).extrude(V(0, 140.0, 0))
        rear_cut.translate(V(0, -20.0, 0))
        TANG_Z_LOW = _keep[-1].z
    else:
        TANG_Z_LOW = TANG_Z0
    cavity = cavity.fuse(tang)
    App.Console.PrintMessage("Tang cut-in: from z=%.1f up to the top (%.1f mm tall), x from %.1f back to the rear edge.\n"
                             % (TANG_Z0, H - TANG_Z0, tx_max))


if TOP_RABBET:
    cavity = cavity.fuse(Part.makeBox(400.0, 2.0 * (FLOOR_Y + TOP_RABBET_D), TOP_RABBET_H + 6.0,
                                      V(-200.0, -(FLOOR_Y + TOP_RABBET_D), H - TOP_RABBET_H)))
cavity_nolobe = cavity
if LOBE:
    zt = H - TOP_RABBET_H
    z_base = H - FLANGE_NOTCH_D                       # the 5.5 / 10.5 mm are measured down from the top of the relief (bottom of the top notch)
    xf = x_range(zt)[1] - LOBE_FROM_FRONT
    pl = [V(xf, 0, zt + 0.5), V(xf - LOBE_L, 0, zt + 0.5), V(xf - LOBE_L, 0, H - LOBE_BOTTOM_REAR), V(xf, 0, H - LOBE_BOTTOM_FRONT)]
    lobe = Part.Face(Part.makePolygon(pl + [pl[0]])).extrude(V(0, 2.0 * (FLOOR_Y + LOBE_D), 0))
    lobe.translate(V(0, -(FLOOR_Y + LOBE_D), 0))
    cavity_nolobe = cavity
    cavity = cavity.fuse(lobe)
    # same relief again, cut AFTER the flange/neck is fused on (the neck would otherwise fill it); top stops at the flange underside
    # the relief continues up through the flange's inner face to the bottom of the top notch (6 mm above the flange underside), so it joins the notch
    z_lobe_top = H - FLANGE_NOTCH_D
    _pl2 = [V(xf, 0, z_lobe_top), V(xf - LOBE_L, 0, z_lobe_top), V(xf - LOBE_L, 0, H - LOBE_BOTTOM_REAR), V(xf, 0, H - LOBE_BOTTOM_FRONT)]
    lobe_post = Part.Face(Part.makePolygon(_pl2 + [_pl2[0]])).extrude(V(0, 2.0 * (FLOOR_Y + LOBE_D), 0))
    lobe_post.translate(V(0, -(FLOOR_Y + LOBE_D), 0))
    _lobe_deep_poly = [V(_q.x, _q.y, _q.z - LOBE_DEEP_SHIFT) for _q in _pl2]
    _lobe_deep_cache = {}

    def lobe_deep_tool(palm):
        """the deeper part of the relief: from the pocket floor LOBE_DEEP_D mm in, but nowhere closer than LOBE_DEEP_WALL to the outer surface (the swell shrunk by that wall)"""
        if palm not in _lobe_deep_cache:
            secs_ = []
            for fz_ in (-0.04, 0.10, 0.28, 0.46, 0.64, 0.82, 1.04):
                z_ = fz_ * H
                xc_, a_, b_ = ellipse_params(z_, palm)
                secs_.append(Part.Wire([Part.Ellipse(V(xc_, 0, z_), a_ - LOBE_DEEP_WALL, b_ - LOBE_DEEP_WALL).toShape()]))
            inner_ = Part.makeLoft(secs_, True, False, False)
            blk_ = Part.Face(Part.makePolygon(_lobe_deep_poly + [_lobe_deep_poly[0]])).extrude(V(0, LOBE_DEEP_D + 0.5, 0))
            blk_.translate(V(0, FLOOR_Y - 0.5, 0))
            tool_ = blk_.common(inner_)
            if LOBE_DEEP_RAMP:
                # material is left as a 45 degree wedge under the flange: above the line from (y = ordinary relief depth, z = top of the deep relief) down and out at 45 degrees
                zt_ = max(q.z for q in _lobe_deep_poly)
                y0_ = FLOOR_Y + LOBE_D
                x0_ = min(q.x for q in _lobe_deep_poly) - 3.0
                x1_ = max(q.x for q in _lobe_deep_poly) + 3.0
                wp_ = [V(x0_, y0_, zt_ + 1.0), V(x0_, y0_ + 30.0, zt_ + 1.0), V(x0_, y0_ + 30.0, zt_ - 30.0), V(x0_, y0_, zt_)]
                wedge_ = Part.Face(Part.makePolygon(wp_ + [wp_[0]])).extrude(V(x1_ - x0_, 0, 0))
                _t2 = tool_.cut(wedge_)
                if not _t2.isNull() and _t2.isValid() and _t2.Volume > 100.0:
                    tool_ = _t2
                else:
                    App.Console.PrintWarning("Ramp on the deeper relief failed - flat ledge kept.\n")
            _lobe_deep_cache[palm] = tool_
        return _lobe_deep_cache[palm]


_logo_cache = {}
EMBLEMS = {}


def logo_tool(palm, cx, cz):
    """returns (the field of the shield minus the cross as a tall slab along y, outline face of the shield in the XZ plane)"""
    key = (palm, round(cx, 2), round(cz, 2))
    if key in _logo_cache:
        return _logo_cache[key]
    a = LOGO_W / 2.0
    top = LOGO_H / 2.0
    v1 = top - 0.38 * LOGO_H                     # the sides are straight down to here, then run in to the point
    vb = -top
    n = 12
    right, left = [], []
    for i in range(n + 1):
        t = i / float(n)
        u = a * (1.0 - t ** 1.8)
        v = v1 - t * (v1 - vb)
        right.append((u, v))
        left.append((-u, v))

    def pt(u, v):
        ang = math.radians(LOGO_ROT)
        uu, vv = u * math.cos(ang) - v * math.sin(ang), u * math.sin(ang) + v * math.cos(ang)
        return V(cx + uu, 0, cz + vv)
    rc = Part.BSplineCurve()
    rc.interpolate([pt(u, v) for u, v in right])
    lc = Part.BSplineCurve()
    lc.interpolate([pt(u, v) for u, v in left])
    edges = [Part.makeLine(pt(-a, top), pt(a, top)), Part.makeLine(pt(a, top), pt(a, v1)), rc.toShape(),
             lc.toShape(), Part.makeLine(pt(-a, v1), pt(-a, top))]
    shield = Part.Face(Part.Wire(Part.__sortEdges__(edges)))
    field = shield.makeOffset2D(-LOGO_RIM, 0, False, False, True)
    if isinstance(field, Part.Compound) and field.Faces:
        field = field.Faces[0]
    # the cross (centre 40 % down from the top of the shield)
    ext = LOGO_CROSS * LOGO_W
    wid = 0.3 * ext
    vc = top - 0.40 * LOGO_H
    h_ = Part.Face(Part.makePolygon([pt(-ext / 2.0, vc - wid / 2.0), pt(ext / 2.0, vc - wid / 2.0), pt(ext / 2.0, vc + wid / 2.0),
                                     pt(-ext / 2.0, vc + wid / 2.0), pt(-ext / 2.0, vc - wid / 2.0)]))
    v_ = Part.Face(Part.makePolygon([pt(-wid / 2.0, vc - ext / 2.0), pt(wid / 2.0, vc - ext / 2.0), pt(wid / 2.0, vc + ext / 2.0),
                                     pt(-wid / 2.0, vc + ext / 2.0), pt(-wid / 2.0, vc - ext / 2.0)]))
    slab_f = field.extrude(V(0, 60.0, 0))
    cross = h_.extrude(V(0, 60.0, 0)).fuse(v_.extrude(V(0, 60.0, 0)))
    tool = slab_f.cut(cross)
    _logo_cache[key] = (tool, shield)
    return tool, shield


def logo_inner(palm):
    """the analytic swell surface moved LOGO_DEPTH inward (inlay mode)"""
    secs_ = []
    for fz_ in (-0.04, 0.10, 0.28, 0.46, 0.64, 0.82, 1.04):
        z_ = fz_ * H
        xc_, a_, b_ = ellipse_params(z_, palm)
        secs_.append(Part.Wire([Part.Ellipse(V(xc_, 0, z_), a_, max(b_ - LOGO_DEPTH, 0.5)).toShape()]))
    return Part.makeLoft(secs_, True, False, False)


# ----------------------------------------------------------------------------
# TOP FLANGE + front overhang (a separate piece, added to each half after the pocket is cut)
# ----------------------------------------------------------------------------
head_solid = None
flange_keep = None                                  # the finished (tilted) flange plate: the arc rounding must not cut into it
if FLANGE:
    z_top, z_fl, z_toe = H, H - FLANGE_T, H - HEAD_TOE_DROP
    xs = x_range(z_toe)[1]                       # front strap line at the toe
    x_tip = xs + FLANGE_FRONT_OVERHANG
    x_end = x_tip - FLANGE_LEN
    x_j = x_end + REAR_ARC_LEN
    arc_top = z_toe + ARC_SPAN
    D = ARC_FRONT_DEPTH

    def Q(x, z):
        return V(x, 0.0, z)

    def _xb(z):                                  # front edge of the grip body at height z
        return x_range(z)[1]

    # front arc as a true circular arc from the toe up to the flange: chord = ARC_SPAN tall, sagitta = ARC_FRONT_DEPTH - 1.2 (rearward)
    _p0, _p1 = (x_tip - 1.5, z_toe), (x_tip - 1.0, arc_top)
    _ch = math.hypot(_p1[0] - _p0[0], _p1[1] - _p0[1])
    _sg = max(D - 1.2, 1.0)
    _R = (_ch * _ch / 4.0 + _sg * _sg) / (2.0 * _sg)
    _mx, _mz = (_p0[0] + _p1[0]) / 2.0, (_p0[1] + _p1[1]) / 2.0
    _ux, _uz = (_p1[0] - _p0[0]) / _ch, (_p1[1] - _p0[1]) / _ch       # along the chord (upward)
    _nx, _nz = -_uz, _ux                                                # normal, pointing rearward (-x)
    if _nx > 0:
        _nx, _nz = -_nx, -_nz
    _cx, _cz = _mx + _nx * (_sg - _R), _mz + _nz * (_sg - _R)           # circle centre (on the front side)
    _a0 = math.atan2(_p0[1] - _cz, _p0[0] - _cx)
    _a1 = math.atan2(_p1[1] - _cz, _p1[0] - _cx)
    while _a1 - _a0 > math.pi:
        _a1 -= 2.0 * math.pi
    while _a1 - _a0 < -math.pi:
        _a1 += 2.0 * math.pi
    _arc_pts = [Q(_cx + _R * math.cos(_a0 + (_a1 - _a0) * k / 8.0), _cz + _R * math.sin(_a0 + (_a1 - _a0) * k / 8.0)) for k in range(9)]
    _arc_pts[0], _arc_pts[-1] = Q(*_p0), Q(*_p1)

    # the inside corner under the toe: with HEAD_AS_BODY the outline of the head is part of the grip's own outline, so it must leave the front strap edge SMOOTHLY (it used to cross it at an angle
    # at z_toe-13.5, which made a step / ledge in the front edge). Below FRONT_FLARE_START it runs a hair behind the strap edge, at the start it is tangent to it, then it bends forward.
    if HEAD_AS_BODY:
        _zT = (P(FRONT_FOLLOW_PX0, FRONT_FOLLOW_PY0).z - FRONT_FLARE_LOWER) if (FRONT_FOLLOW and FRONT_FOLLOW_STRAIGHT) else z_toe - FRONT_FLARE_START   # the flare starts a little BELOW the end of the straight line, so its start point does not fall on the vertex of the traced outline
        _fd = z_toe - _zT                                  # mm below the toe where the flare starts (= the top of the straight strap line)
        _sm = (_xb(_zT - 2.0) - _xb(_zT - 10.0)) / 8.0 if (FRONT_FOLLOW and FRONT_FOLLOW_STRAIGHT) else 0.0     # lean of the straight strap line, mm per mm
        _xbase = lambda z_: _xb(min(z_, _zT)) + _sm * max(0.0, z_ - _zT)   # the straight line carried on a little above its end: the flare starts tangent to it

        def _dfl(zz):                                     # zz = mm below the toe; offset from the strap line (negative = behind it)
            t_ = _fd - zz                                 # mm above the start of the flare
            return 0.03 * t_ if t_ < 0 else 0.03 * t_ + 0.007 * t_ * t_
        _fds = [23.0, 20.0, _fd, 11.0, 7.5]
        _fds = [d_ for d_ in _fds if d_ == _fd or abs(d_ - _fd) > 1.5]                  # no two points closer than 1.5 mm (the spline would wiggle)
        _FLARE_PTS = [Q(_xbase(z_toe - d_) + _dfl(d_) - TOE_UNDER_RELIEF * {7.5: 0.35, 11.0: 0.15}.get(d_, 0.0), z_toe - d_) for d_ in _fds]
    else:
        _FLARE_PTS = [Q(_xb(z_toe - 20) - 0.65 * NECK_EDGE_BACK, z_toe - 20), Q(_xb(z_toe - 15) - 0.2 * NECK_EDGE_BACK, z_toe - 15),
                      Q(xs + 0.3, z_toe - 11), Q(xs + 1.8, z_toe - 7.5)]
    _h0_back = 0.4 if (HEAD_AS_BODY and FRONT_FOLLOW and FRONT_FOLLOW_STRAIGHT) else NECK_EDGE_BACK + (0.5 if NECK_EDGE_BACK <= 0 else 0.0)   # the head outline starts just behind the straight strap line
    HEAD = [
        ("L", [Q(x_tip - 3, z_top), Q(x_end + 3, z_top)]),                                       # top
        ("S", [Q(x_end + 3, z_top), Q(x_end + 0.4, z_top - 2.0), Q(x_end - 0.2, z_top - FLANGE_T / 2.0),
               Q(x_end + 0.4, z_fl + 2.0), Q(x_end + 3, z_fl)]),                                  # rounded rear end
        ("L", [Q(x_end + 3, z_fl), Q(x_end + 3.5, z_fl)]),                                       # underside of the rear overhang
        ("L", [Q(x_end + 3.5, z_fl), Q(x_end + 3.5, z_toe - 26)]),                               # (inside the body from here; the plate now reaches all the way back to the flange end)
        ("L", [Q(x_end + 3.5, z_toe - 26), Q(_xb(z_toe - 26) - _h0_back, z_toe - 26)]),
        ("S", [Q(_xb(z_toe - 26) - _h0_back, z_toe - 26)] + _FLARE_PTS + [
               Q(xs + 5.0 - 0.95 * TOE_UNDER_RELIEF, z_toe - 4.0), Q(xs + 10.0 - 1.05 * TOE_UNDER_RELIEF, z_toe - 2.3),
               Q(xs + 17.0 - 0.8 * TOE_UNDER_RELIEF, z_toe - 1.2), Q(x_tip - 1.5, z_toe)]),   # as on the original: rounded inside corner (r ~8 mm) from the front strap into an almost flat underside of the toe lip
        ("S", _arc_pts),   # the front arc: a smooth circular arc (was a few straight-ish segments)
        ("S", [Q(x_tip - 1, arc_top), Q(x_tip + 0.2, arc_top + 2), Q(x_tip + 0.3, z_top - 3.5), Q(x_tip - 3, z_top)]),  # front tip
    ]
    hedges = []
    for kind, pts in HEAD:
        if kind == "L":
            hedges += Part.makePolygon(pts).Edges
        else:
            bs_ = Part.BSplineCurve()
            bs_.interpolate(pts)
            hedges.append(bs_.toShape())
    TILT = math.degrees(math.atan2(FLANGE_TILT_DROP, FLANGE_LEN_BASE))
    _tt = math.tan(math.radians(TILT))
    _lz = lambda x: H - FLANGE_NOTCH_D - (x_tip - x) * _tt          # bottom of the (tilted) top notch at x
    if LOBE:
        # the top of the relief goes 0.5 mm into the air of the notch above it: ending exactly on the notch floor left a paper-thin horizontal fin (0.01 mm) inside the relief
        _pl3 = [V(xf, 0, _lz(xf) + 0.5), V(xf - LOBE_L, 0, _lz(xf - LOBE_L) + 0.5), V(xf - LOBE_L, 0, H - LOBE_BOTTOM_REAR), V(xf, 0, H - LOBE_BOTTOM_FRONT)]
        lobe_post = Part.Face(Part.makePolygon(_pl3 + [_pl3[0]])).extrude(V(0, 2.0 * (FLOOR_Y + LOBE_D), 0))
        lobe_post.translate(V(0, -(FLOOR_Y + LOBE_D), 0))
        # the deeper relief (LOBE_DEEP_SIDE) gets the same outline as the ordinary one: its top is the (tilted) floor of the notch in the flange, 0.03 mm into the notch so no fin is left
        _lobe_deep_poly = [V(xf, 0, _lz(xf) + 0.03 - LOBE_DEEP_SHIFT), V(xf - LOBE_L, 0, _lz(xf - LOBE_L) + 0.03 - LOBE_DEEP_SHIFT),
                           V(xf - LOBE_L, 0, H - LOBE_BOTTOM_REAR), V(xf, 0, H - LOBE_BOTTOM_FRONT)]
        if FLANGE_REMOVE_SIDE is not None and FLANGE_REMOVE_SIDE == LOBE_DEEP_SIDE:
            # no flange on this half: the cut-in is a plain LOBE_DEEP_W x LOBE_DEEP_H rectangle from the flat top (1 mm into the air above it) down; the wall behind it (x < xf - LOBE_DEEP_W) stays
            _zt = H - FLANGE_T
            _za, _zb = _zt + 1.0, _zt - LOBE_DEEP_H
            if FLANGE_REMOVE_STRAIGHT_FRONT and x_line_front is not None:
                # front end of the cut-in LOBE_DEEP_FRONT_WALL behind the (straight, leaning) front edge and parallel to it; the rear end LOBE_DEEP_W further back
                _xa, _xb2 = x_line_front(_za) - LOBE_DEEP_FRONT_WALL, x_line_front(_zb) - LOBE_DEEP_FRONT_WALL
            else:
                _xa = _xb2 = xf - LOBE_DEEP_BACK
            _lobe_deep_poly = [V(_xa, 0, _za), V(_xa - LOBE_DEEP_W, 0, _za), V(_xb2 - LOBE_DEEP_W, 0, _zb), V(_xb2, 0, _zb)]
        _lobe_deep_cache.clear()
    # rear trim: the body behind the shortened flange is cut back along a straight line from the rear edge (at the pencil-sketch point 940/300)
    # up to the rear end of the flange, so nothing sticks out behind the flange (the rear edge simply continues up to the flange)
    rear_trim = None
    if REAR_TRIM:
        _pa = P(940.0, 300.0)
        _pa = (_pa.x, _pa.z)
        _pb = (x_end - 0.6, z_fl + 0.3)
        _tp = [V(_pa[0], 0, _pa[1]), V(_pb[0], 0, _pb[1]), V(_pb[0] - 60.0, 0, _pb[1]), V(_pa[0] - 60.0, 0, _pa[1])]
        rear_trim = Part.Face(Part.makePolygon(_tp + [_tp[0]])).extrude(V(0, 200.0, 0))
        rear_trim.translate(V(0, -100.0, 0))
    flange_rear_cut = None
    if LOBE and FLANGE_REAR_DEEP > 0:
        _xa, _xb = x_end - 6.0, xf - LOBE_L               # from beyond the rear end up to the rear end of the relief
        _zu = lambda x: z_fl - (x_tip - x) * _tt - 0.3     # tilted underside of the flange
        _pr = [V(_xa, 0, _zu(_xa)), V(_xb, 0, _zu(_xb)), V(_xb, 0, H + 2.0), V(_xa, 0, H + 2.0)]
        flange_rear_cut = Part.Face(Part.makePolygon(_pr + [_pr[0]])).extrude(V(0, 2.0 * (FLOOR_Y + FLANGE_REAR_DEEP), 0))
        flange_rear_cut.translate(V(0, -(FLOOR_Y + FLANGE_REAR_DEEP), 0))
    head_side = Part.Face(Part.Wire(hedges)).extrude(V(0, 140, 0))
    head_side.translate(V(0, -70, 0))

    y_in = FLOOR_Y + FLANGE_REBATE

    def w_at(x):
        return FLANGE_W_FRONT + (FLANGE_W_REAR - FLANGE_W_FRONT) * (x_tip - x) / FLANGE_LEN

    xa, xb = x_tip + 4.0, x_end - 4.0
    tp = [V(xa, y_in, 0), V(xb, y_in, 0), V(xb, y_in + w_at(xb), 0), V(xa, y_in + w_at(xa), 0)]
    trap = Part.Face(Part.makePolygon(tp + [tp[0]])).extrude(V(0, 0, FLANGE_T + 2.0))
    trap.translate(V(0, 0, z_fl))               # flange starts exactly at z_fl (was 1 mm lower, which left a lip under the relief)
    flange_solid = head_side.common(trap)
    flange_solid = try_op("Flange notch", lambda sh: sh.cut(Part.makeBox(
        FLANGE_LEN + 20.0, FLANGE_NOTCH_W + 0.1, FLANGE_NOTCH_D + 1.0, V(x_end - 10.0, y_in - 0.1, H - FLANGE_NOTCH_D))), flange_solid)
    outer = [e for e in flange_solid.Edges if min(v.Y for v in e.Vertexes) > y_in + 7.0]
    flange_solid = fillet_soft("Flange rounding", flange_solid, 2.0, outer) if outer else flange_solid
    # tilt the flange about its front underside corner so that the rear end is FLANGE_TILT_DROP lower
    flange_solid.rotate(V(x_tip, 0, z_fl), V(0, 1, 0), -TILT)
    if flange_solid.BoundBox.ZMax > H + 0.5:                      # wrong direction on this build: rotate back and the other way
        flange_solid.rotate(V(x_tip, 0, z_fl), V(0, 1, 0), 2.0 * TILT)
    App.Console.PrintMessage("Flange tilt %.2f deg, top now z %.1f - %.1f.\n" % (TILT, flange_solid.BoundBox.ZMin, flange_solid.BoundBox.ZMax))
    # the neck plate: NECK_T thick down to the toe, then it fades smoothly to nothing under the toe (no flat bottom edge / box-like step)
    _yb, _zb = FLOOR_Y, z_toe - 28.0
    _fade = [(NECK_T, z_toe), (NECK_T - 0.15, z_toe - 3.0), (NECK_T - 0.9, z_toe - 7.0), (NECK_T - 2.6, z_toe - 12.0),
             (NECK_T - 4.7, z_toe - 17.0), (NECK_T - 6.3, z_toe - 22.0), (NECK_T - 7.2, z_toe - 26.0), (0.1, _zb)]
    _fade = [(_yb + max(t, 0.1), z) for t, z in _fade]
    neck_prof = None
    try:
        _bs = Part.BSplineCurve()
        _bs.interpolate([V(-200.0, y_, z_) for y_, z_ in _fade])
        _nedges = [_bs.toShape()] + Part.makePolygon([V(-200.0, _fade[-1][0], _zb), V(-200.0, _yb, _zb), V(-200.0, _yb, z_fl),
                                                       V(-200.0, _yb + NECK_T, z_fl), V(-200.0, _fade[0][0], _fade[0][1])]).Edges
        neck_prof = Part.Face(Part.Wire(Part.__sortEdges__(_nedges))).extrude(V(400.0, 0, 0))
        neck = head_side.common(neck_prof)
    except Exception as e:
        App.Console.PrintWarning("Neck fade failed (%s) - using the plain neck plate.\n" % e)
        neck_prof = Part.makeBox(400, NECK_T, z_fl - _zb, V(-200, FLOOR_Y, _zb))
        neck = head_side.common(neck_prof)

    def round_neck_arc(nk):
        """round the edges of the front arc (the arc around the trigger, where the finger rests) on the neck plate. Guarded: the result must be valid,
        keep the same number of solids and lose only a little volume - otherwise the plate stays as it was (and the Report view says so)."""
        for y_lvl, r_, name_ in ((FLOOR_Y + NECK_T, NECK_ARC_R_OUT, "outer"), (FLOOR_Y, NECK_ARC_R_IN, "inner")):
            if r_ <= 0:
                continue
            try:
                es_ = [e for e in nk.Edges
                       if abs(e.BoundBox.YMin - y_lvl) < 0.05 and abs(e.BoundBox.YMax - y_lvl) < 0.05
                       and e.BoundBox.XLength > 4.0 and e.BoundBox.ZLength > 15.0
                       and e.BoundBox.ZMin > z_toe - 0.5 and e.BoundBox.ZMax < z_fl + 0.5]
                if not es_:
                    App.Console.PrintWarning("Front arc rounding (%s): arc edge not found - skipped.\n" % name_)
                    continue
                n2 = nk.makeFillet(min(r_, NECK_T / 2.0 - 0.3), es_)
                lost = nk.Volume - n2.Volume
                if (n2.isNull() or not n2.isValid() or len(n2.Solids) != len(nk.Solids)
                        or lost < 0.0 or lost > 0.03 * nk.Volume):
                    App.Console.PrintWarning("Front arc rounding (%s) gave a bad result (volume change %.1f mm3) - skipped.\n" % (name_, lost))
                    continue
                nk = n2
                App.Console.PrintMessage("Front arc rounded (%s edge, r=%.1f mm, %d edge(s)).\n" % (name_, r_, len(es_)))
            except Exception as e:
                App.Console.PrintWarning("Front arc rounding (%s) failed (%s) - skipped.\n" % (name_, e))
        return nk

    if NECK_ARC_R_OUT > 0 or NECK_ARC_R_IN > 0:
        neck = round_neck_arc(neck)
    if LOBE:                                     # relief runs all the way up to the flange underside (neck top = z_fl)
        _pt = [V(xf, 0, z_fl + 1.0), V(xf - LOBE_L, 0, z_fl + 1.0), V(xf - LOBE_L, 0, H - LOBE_BOTTOM_REAR), V(xf, 0, H - LOBE_BOTTOM_FRONT)]
        _lt = Part.Face(Part.makePolygon(_pt + [_pt[0]])).extrude(V(0, 2.0 * (FLOOR_Y + LOBE_D), 0))
        _lt.translate(V(0, -(FLOOR_Y + LOBE_D), 0))
        neck = try_op("Lobe in neck", lambda sh: sh.cut(_lt), neck)
    # the neck plate continues backwards, past the flange's rear end, to the rear end of the grip; it is cut by the same cut-in behind the raised
    # rear part, so its rear edge follows the soft arc from the flange down to the end of the grip
    if neck_prof is not None:
        try:
            rear_plate = neck_prof.common(Part.makeBox(14.0, 200.0, z_fl - (z_toe - 26.0), V(x_end - 8.0, -100.0, z_toe - 26.0)))
            if rear_cut is not None:
                rear_plate = rear_plate.cut(rear_cut)
            neck = neck.fuse(rear_plate)
        except Exception as e:
            App.Console.PrintWarning("Rear plate failed (%s).\n" % e)
    head_solid = flange_solid.fuse(neck)
    flange_keep = flange_solid.copy()
    layer_clip = None
    layer_parts = None
    notch_tool = None
    layer_floor = None
    layer_rear_cut = None
    rear_wall = None
    if HEAD_AS_BODY:
        try:
            _hp = Part.Wire(hedges).discretize(Number=400)
            # only the FRONT part of the head outline is added to the grip (the overhang with the toe, neck plate and arc); at the rear the top simply follows the grip's own rear edge
            _xcut = 0.5 * (x_end + x_tip)
            _hfront = head_side.common(Part.makeBox(400.0, 200.0, 300.0, V(_xcut, -100.0, -100.0)))
            _bp = prism.fuse(_hfront)
            if not (_bp.isValid() and not _bp.isNull() and len(_bp.Solids) == 1):
                raise ValueError("outline union not valid")
            # the top layer: the band between the flange underside and the top, tilted exactly like the old flange, inside the head outline, from the pocket floor outwards
            _ang = -TILT
            _band = Part.makeBox(400.0, 200.0, FLANGE_T, V(-200.0, -100.0, z_fl))
            _band.rotate(V(x_tip, 0, z_fl), V(0, 1, 0), _ang)
            if not _band.isInside(V(x_end + 5.0, 0.0, z_fl - 1.5), 1e-6, True):          # wrong direction on this build: the rear end must dip below the flange underside
                _ang = TILT
                _band = Part.makeBox(400.0, 200.0, FLANGE_T, V(-200.0, -100.0, z_fl))
                _band.rotate(V(x_tip, 0, z_fl), V(0, 1, 0), _ang)
            _ylim = Part.makeBox(400.0, 100.0, 300.0, V(-200.0, y_in, -100.0))
            layer_clip = _band.common(head_side).common(_ylim)
            layer_parts = [_band, head_side, _ylim]
            layer_floor = _band.common(head_side).common(Part.makeBox(400.0, FLANGE_NOTCH_W + HEAD_MIN_WALL, 300.0, V(-200.0, y_in, -100.0))).common(_bp)
            if layer_floor.isNull() or not layer_floor.isValid() or layer_floor.Volume < 1.0:
                layer_floor = None
            notch_tool = Part.makeBox(FLANGE_LEN + 20.0, FLANGE_NOTCH_W + 0.1, FLANGE_NOTCH_D + 1.0, V(x_end - 10.0, y_in - 0.1, H - FLANGE_NOTCH_D))
            notch_tool.rotate(V(x_tip, 0, z_fl), V(0, 1, 0), _ang)
            if layer_clip.isNull() or not layer_clip.isValid() or layer_clip.Volume < 1.0:
                raise ValueError("top layer clip empty")
            HEAD_PTS = _hp
            BODY_PRISM = _bp
            flange_keep = layer_clip.copy()
            layer_rear_cut = None
            if HEAD_REAR_FOLLOW and len(REAR_ARC_PTS) >= 3:
                try:
                    _orig = list(REAR_ARC_PTS)
                    _p0 = _orig[0]                                          # (x, z) where the arc of the raised rear part meets the flange underside
                    _zt = H + 3.0
                    # the rear wall continues the arc: it starts with the arc's own lean (so there is no kink where the arc ends) and eases off to HEAD_REAR_LEAN at the top
                    _q = next((q for q in _orig[1:] if q[1] <= _p0[1] - 1.5), _orig[min(3, len(_orig) - 1)])
                    _s0 = min(max((_p0[0] - _q[0]) / max(_p0[1] - _q[1], 1e-6), 0.05 if REAR_ARC_STRAIGHT else 0.3), 1.0)
                    _s1 = _s0 if REAR_ARC_STRAIGHT else min(HEAD_REAR_LEAN, _s0)          # straight: keep the lean of the line below all the way to the top

                    def _ext(dz, _L=10.0):
                        if dz <= _L:
                            return _s0 * dz + 0.5 * (_s1 - _s0) * dz * dz / _L
                        return _s0 * _L + 0.5 * (_s1 - _s0) * _L + _s1 * (dz - _L)

                    _lx = lambda z: _p0[0] + _ext(z - _p0[1])
                    _ex = [(_lx(_p0[1] + dz), _p0[1] + dz) for dz in (1.5, 3.0, 4.5, 6.0, 8.0, 10.0, 13.0)]
                    _path = list(reversed(_ex)) + _orig                      # top -> down along the rear wall
                    _low = [q for q in _orig if q[1] >= 98.0] or list(_orig[:3])
                    _poly = [V(q[0], 0, q[1]) for q in (list(reversed(_ex)) + _low)]
                    _poly += [V(_low[-1][0] - 60.0, 0, _low[-1][1]), V(_low[-1][0] - 60.0, 0, _zt)]
                    layer_rear_cut = Part.Face(Part.makePolygon(_poly + [_poly[0]])).extrude(V(0, 200.0, 0))
                    layer_rear_cut.translate(V(0, -100.0, 0))
                    if HEAD_REAR_WALL and TANG_TAPER:
                        # the wall: from just below the spur tip up along the rear arc (and its continuation) to the bottom of the top notch; TANG_SPUR_W wide, from the pocket floor out
                        # to the width of the top notch (the spur inside the pocket is left as in v5.39). Added after the relief and the deeper rear cut, so neither removes it.
                        _lft = [q for q in reversed(_orig) if q[1] >= z_sp - 1.5 and q[1] <= _p0[1] + 1e-6]
                        _lft += [(_lx(z_), z_) for z_ in (_p0[1] + 1.5, _p0[1] + 3.0)]
                        _lft = [(x_, z_) for x_, z_ in _lft if z_ <= _p0[1] + 3.0 + 1e-6]
                        _lft[-1] = (_lft[-1][0], _lz(_lft[-1][0]) + 0.05)
                        _rgt = [(x_ + TANG_SPUR_W + 0.05, z_) for x_, z_ in _lft]
                        _rgt[-1] = (_rgt[-1][0], _lz(_rgt[-1][0]) + 0.05)
                        _wp = [V(x_, 0, z_) for x_, z_ in _lft + list(reversed(_rgt))]
                        rear_wall = Part.Face(Part.makePolygon(_wp + [_wp[0]])).extrude(V(0, FLANGE_NOTCH_W + 0.3, 0))
                        rear_wall.translate(V(0, FLOOR_Y - 0.3, 0))          # only the part outside the pocket floor (pocket floor -> as wide as the top notch); the spur inside the pocket keeps its v5.39 length
                        if rear_wall.isNull() or not rear_wall.isValid() or rear_wall.Volume < 1.0:
                            rear_wall = None
                    REAR_ARC_PTS = _path
                    flange_keep = None                                       # the edge roll continues over the top
                except Exception as e:
                    App.Console.PrintWarning("Top rear wall: could not be prepared (%s) - the rear end stays as it was.\n" % e)
                    layer_rear_cut = None
            head_solid = None
            App.Console.PrintMessage("Head as part of the grip: top layer clip %.0f mm3, outline union valid.\n" % layer_clip.Volume)
        except Exception as e:
            App.Console.PrintWarning("HEAD_AS_BODY failed (%s) - using the separate flange plate (v5.39).\n" % e)
            HEAD_AS_BODY = False
            layer_clip = None
    App.Console.PrintMessage("Flange: tip x=%.1f, rear end x=%.1f, strap line x=%.1f, toe z=%.1f, flange z %.1f-%.1f, thickness %.1f-%.1f mm.\n"
                             % (x_tip, x_end, xs, z_toe, z_fl, z_top, FLANGE_W_FRONT, FLANGE_W_REAR))


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
# the tenon's extra shift (grip coordinates) -> the pocket's own (rotated) frame
_p0 = to_pocket_frame(Part.Vertex(V(0, 0, 0))).Point
_pu = to_pocket_frame(Part.Vertex(V(1, 0, 0))).Point
_pw = to_pocket_frame(Part.Vertex(V(0, 0, 1))).Point
_a11, _a21, _a12, _a22 = _pu.x - _p0.x, _pu.z - _p0.z, _pw.x - _p0.x, _pw.z - _p0.z
_det = _a11 * _a22 - _a12 * _a21
pad_su = (PAD_SHIFT_FRONT * _a22 - _a12 * PAD_SHIFT_UP) / _det                 # local x shift
pad_sw = (_a11 * PAD_SHIFT_UP - _a21 * PAD_SHIFT_FRONT) / _det                 # local z shift
pad_xl += pad_su
App.Console.PrintMessage("Tenon moved %.1f mm toward the front and %.1f mm up (pocket frame: %.2f / %.2f).\n" % (PAD_SHIFT_FRONT, PAD_SHIFT_UP, pad_su, pad_sw))
pad_tip = POCKET_DEPTH - PAD_PROTRUSION + 2.0 * C             # tenon face toward the centre (pocket floor is FLOOR_Y)
App.Console.PrintMessage("Tenon: front side %.1f mm behind the front edge, rear side %.1f mm in front of the pocket's rear wall.\n"
                         % (PAD_FRONT_INSET - PAD_X_SHIFT * CR, PAD_TO_POCKET_WALL + PAD_X_SHIFT * CR))

# screw centres in grip coordinates
screws = []
for from_top, ref_edge, dist in SCREW_POS:
    z = H - from_top
    rear_x, front_x = x_range(z)
    screws.append((front_x - dist if ref_edge == "front" else rear_x + dist, z))

# checkered panel outline as on the reference photo: its upper edge is a long arc that is lowest at the front strap and rises toward the rear,
# smooth wood above it and a narrow smooth rim around the other three sides. (u, h) = (fraction of the grip's depth from the front edge, height above the heel in mm)
PANEL_FROM_PHOTO = True
PANEL_UH = [(0.04, 47.1), (0.06, 56.9), (0.121, 63.1), (0.219, 68.8), (0.338, 73.8), (0.463, 76.9), (0.614, 78.1), (0.788, 77.9), (0.931, 75.4), (0.965, 70.6),
            (0.965, 59.4), (0.965, 40.6), (0.965, 21.9), (0.965, 4.4), (0.965, 3.0), (0.04, 3.0), (0.04, 9.4), (0.04, 21.9), (0.04, 34.4)]


def _panel_pt(u, h):
    z = min(max(h, 1.0), H - 1.0)
    rear, front = x_range(z)
    return V(front - u * (front - rear), 0.0, z)


if PANEL_FROM_PHOTO:
    _arc_pts = [_panel_pt(u, h) for u, h in PANEL_UH[:10]]
    _arc_bs = Part.BSplineCurve()
    _arc_bs.interpolate(_arc_pts)
    _pp = _arc_bs.discretize(Number=36) + [_panel_pt(u, h) for u, h in PANEL_UH[10:]]
    panel_face = Part.Face(Part.makePolygon(_pp + [_pp[0]]))
else:
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


def make_inner(palm):
    """the smooth swell surface moved PANEL_RECESS inward (same loft, smaller half-thickness): the floor of the curved panel"""
    secs = []
    for fz in (-0.04, 0.10, 0.28, 0.46, 0.64, 0.82, 1.04):
        z = fz * H
        xc_, a_, b_ = ellipse_params(z, palm)
        secs.append(Part.Wire([Part.Ellipse(V(xc_, 0, z), a_, max(b_ - PANEL_RECESS, 0.5)).toShape()]))
    return prism.common(Part.makeLoft(secs, True, False, False))


_panel_poly = None
_checker_cache = {}


def _in_panel(x, z, margin):
    """inside the panel outline, at least `margin` mm from its edge (2D test in the XZ plane)"""
    global _panel_poly
    if _panel_poly is None:
        _panel_poly = [(v.x, v.z) for v in panel_face.OuterWire.discretize(Number=240)]
    inside = False
    n = len(_panel_poly)
    dmin = 1e9
    for i in range(n):
        x1, z1 = _panel_poly[i]
        x2, z2 = _panel_poly[(i + 1) % n]
        if (z1 > z) != (z2 > z):
            if x < x1 + (z - z1) * (x2 - x1) / (z2 - z1):
                inside = not inside
        dx, dz = x2 - x1, z2 - z1
        t = 0.0 if (dx == 0 and dz == 0) else max(0.0, min(1.0, ((x - x1) * dx + (z - z1) * dz) / (dx * dx + dz * dz)))
        dmin = min(dmin, math.hypot(x - (x1 + t * dx), z - (z1 + t * dz)))
    return inside and dmin >= margin


def surface_correction(half, palm):
    """measured panel floor minus the analytic one (median over a few points); keeps the grooves on the real surface"""
    bb = panel_face.BoundBox
    deltas = []
    for fx in (0.3, 0.5, 0.7):
        for fz in (0.25, 0.5, 0.75):
            x, z = bb.XMin + fx * bb.XLength, bb.ZMin + fz * bb.ZLength
            if not _in_panel(x, z, 2.0):
                continue
            try:
                ys = [v.Y for v in half.common(Part.makeLine(V(x, 0, z), V(x, 80, z))).Vertexes]
                if ys:
                    deltas.append(max(ys) - (surface_y(x, z, palm) - PANEL_RECESS))
            except Exception:
                pass
    if not deltas:
        return 0.0
    deltas.sort()
    d = max(-1.5, min(1.5, deltas[len(deltas) // 2]))
    App.Console.PrintMessage("Panel floor: measured minus analytic = %.2f mm (%d points).\n" % (d, len(deltas)))
    return d


def checker_runs(palm, dy=0.0):
    """centre lines of the +-45 degree grooves, as 3D points on the panel floor (in runs inside the panel, clear of the screw rings)"""
    bb = panel_face.BoundBox
    cx, cz = (bb.XMin + bb.XMax) / 2.0, (bb.ZMin + bb.ZMax) / 2.0
    diag = math.hypot(bb.XLength, bb.ZLength)
    n = int(diag / (2.0 * CHECKER_PITCH)) + 2
    step = 2.5
    ring_r = HEAD_D / 2.0 + SCREW_RING
    runs = []
    for sign in (1, -1):
        ang = math.radians(45.0 * sign)
        dx, dz = math.cos(ang), math.sin(ang)
        nx, nz = -math.sin(ang), math.cos(ang)
        for k in range(-n, n + 1):
            bx, bz = cx + k * CHECKER_PITCH * nx, cz + k * CHECKER_PITCH * nz
            run = []
            m = int(diag / step) + 1
            for i in range(-m, m + 1):
                x, z = bx + i * step * dx, bz + i * step * dz
                ok = _in_panel(x, z, 0.8) and all(math.hypot(x - sx, z - sz) > ring_r for sx, sz in screws)
                if ok:
                    run.append(V(x, surface_y(x, z, palm) - PANEL_RECESS + dy, z))
                if (not ok or i == m) and run:
                    if len(run) >= 3:
                        runs.append((run, V(nx, 0, nz)))
                    run = []
    return runs


def _diamond(p, t, nn, d):
    e2 = t.cross(nn)
    e2.normalize()
    pv = [p + e2 * d, p + nn * d, p - e2 * d, p - nn * d]
    return Part.makePolygon(pv + [pv[0]])


def sweep_tools(runs):
    tools = []
    for pts, nn in runs:
        try:
            bs_ = Part.BSplineCurve()
            bs_.interpolate(pts)
            path = Part.Wire([bs_.toShape()])
            t0 = pts[1] - pts[0]
            t0.normalize()
            tool = path.makePipeShell([Part.Wire(_diamond(pts[0], t0, nn, CHECKER_HALF))], True, False)
            if tool.Volume < 0:
                tool.reverse()
            if tool.isValid() and abs(tool.Volume) > 1e-3:
                tools.append(tool)
        except Exception as e:
            App.Console.PrintWarning("Groove sweep skipped (%s).\n" % e)
    return tools


def segment_tools(runs):
    """fallback: every groove built from short straight diamond prisms (robust, but many)"""
    tools = []
    for pts, nn in runs:
        sel = pts[::2] if len(pts) > 4 else pts
        if sel[-1] != pts[-1]:
            sel = sel + [pts[-1]]
        for a, b in zip(sel, sel[1:]):
            t = b - a
            L = t.Length
            if L < 1e-6:
                continue
            t.normalize()
            a2 = a - t * 0.3
            try:
                prof = Part.Face(_diamond(a2, t, nn, CHECKER_HALF))
                tools.append(prof.extrude(t * (L + 0.6)))
            except Exception:
                pass
    return tools


def cut_tools(shape, tools, label, chunk=40):
    """cut the tools in chunks; returns (shape, ok)"""
    v0 = shape.Volume
    for i in range(0, len(tools), chunk):
        part = tools[i:i + chunk]
        try:
            try:
                r = shape.cut(part)
            except Exception:
                r = shape.cut(Part.makeCompound(part))
            if r.isValid() and not r.isNull() and r.Volume > 0.5 * v0:
                shape = r
            else:
                App.Console.PrintWarning("%s: chunk %d gave invalid geometry - skipped.\n" % (label, i // chunk))
        except Exception as e:
            App.Console.PrintWarning("%s: chunk %d failed (%s).\n" % (label, i // chunk, e))
    removed = v0 - shape.Volume
    App.Console.PrintMessage("%s: removed %.1f mm3 with %d tools.\n" % (label, removed, len(tools)))
    return shape, removed > 1.0


def _smooth(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3.0 - 2.0 * u)


def flange_blend(half):
    """no step line on the outside under the flange: where the body is thicker the flange face is carved smoothly into the body,
    where it is thinner a skirt grows out of the flange face and fades into it (both with zero slope at the flange underside)"""
    L = FLANGE_BLEND
    n = 10
    zs = [z_fl - L * i / n for i in range(n + 1)]
    xa, xb = x_end - 2.0, x_tip + 2.0
    xs_len = xb - xa

    def sweep(face_pts):
        return Part.Face(Part.makePolygon([V(xa, y, z) for y, z in face_pts] + [V(xa, face_pts[0][0], face_pts[0][1])])).extrude(V(xs_len, 0, 0))

    def spline_edges(pts):
        bs_ = Part.BSplineCurve()
        bs_.interpolate([V(xa, y, z) for y, z in pts])
        return bs_.toShape()

    # skirt (adds material where the body is thinner than the flange)
    try:
        n2 = 16
        zs2 = [z_fl - FLANGE_SKIRT_LEN * i / n2 for i in range(n2 + 1)]
        pts = [(FLOOR_Y + max(FLANGE_W_FRONT * (1.0 - _smooth(i / float(n2))), 0.05), zs2[i]) for i in range(n2 + 1)]
        zs_end = zs2[-1]
        wire = Part.Wire([spline_edges(pts)] + Part.makePolygon([V(xa, pts[-1][0], zs_end), V(xa, FLOOR_Y, zs_end),
                                                                  V(xa, FLOOR_Y, z_fl), V(xa, pts[0][0], z_fl)]).Edges)
        skirt = Part.Face(Part.Wire(Part.__sortEdges__(wire.Edges))).extrude(V(xs_len, 0, 0))
        skirt = skirt.common(prism.fuse(head_side))        # one single skirt over the whole flange length (body outline + neck outline): one continuous face
        if rear_cut is not None:                       # do not fill the cut-in behind the raised rear part again: the rear edge follows the arc up to the flange
            skirt = skirt.cut(rear_cut)
        half = try_op("Flange skirt", lambda sh: sh.fuse(skirt), half)
    except Exception as e:
        App.Console.PrintWarning("Flange skirt failed (%s).\n" % e)
    # carve (removes material where the body is thicker than the flange)
    try:
        pts = [(FLOOR_Y + FLANGE_W_FRONT + (FLANGE_BLEND_MAX - FLANGE_W_FRONT) * _smooth(i / float(n)), zs[i]) for i in range(n + 1)]
        top = FLOOR_Y + FLANGE_BLEND_MAX + 30.0
        wire = Part.Wire([spline_edges(pts)] + Part.makePolygon([V(xa, pts[-1][0], zs[-1]), V(xa, top, zs[-1]),
                                                                  V(xa, top, z_fl), V(xa, pts[0][0], z_fl)]).Edges)
        carve = Part.Face(Part.Wire(Part.__sortEdges__(wire.Edges))).extrude(V(xs_len, 0, 0))
        half = try_op("Flange blend", lambda sh: sh.cut(carve), half)
    except Exception as e:
        App.Console.PrintWarning("Flange blend failed (%s).\n" % e)
    return half


def round_rear_arc(half, palm):
    """roll over the outer edge along the curve from the flange down the back of the raised rear part: the cut-in wall (made of many flat facets, so a
    normal fillet cannot take it) is rounded with a cutter swept along the curve. The profile is the corner outside a circle of radius REAR_ARC_ROLL_R
    that touches both the wall and the outer surface."""
    pts = REAR_ARC_PTS
    if REAR_ARC_ROLL_R <= 0 or len(pts) < 3:
        return half
    # resample the curve by arc length
    seg = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    total = sum(seg)
    ns = 30
    path = []
    for k in range(ns + 1):
        d = total * k / float(ns)
        acc = 0.0
        for i, sl in enumerate(seg):
            if acc + sl >= d - 1e-9 or i == len(seg) - 1:
                t = 0.0 if sl == 0 else min(1.0, max(0.0, (d - acc) / sl))
                path.append((pts[i][0] + t * (pts[i + 1][0] - pts[i][0]), pts[i][1] + t * (pts[i + 1][1] - pts[i][1])))
                break
            acc += sl
    secs = []
    for k, (px, pz) in enumerate(path):
        a_, b_ = path[max(k - 1, 0)], path[min(k + 1, len(path) - 1)]
        tx, tz = b_[0] - a_[0], b_[1] - a_[1]
        tl = math.hypot(tx, tz) or 1.0
        tx, tz = tx / tl, tz / tl
        nx, nz = -tz, tx                                   # normal in the XZ plane, pointing to the cut-away (rear) side
        if nx > 0 or (abs(nx) < 1e-6 and nz < 0):
            nx, nz = -nx, -nz
        # outer surface level a little in front of the wall: measured on the real half, else the analytic swell
        R0 = REAR_ARC_ROLL_R
        qx, qz = px - nx * 0.7 * R0, pz - nz * 0.7 * R0
        try:
            ys = max(v.Y for v in half.common(Part.makeLine(V(qx, 0, qz), V(qx, 80, qz))).Vertexes)
        except Exception:
            ys = surface_y(qx, min(max(qz, 0.0), H), palm)
        R = min(R0, ys - FLOOR_Y - 0.4)
        if R < 1.0:
            R = 1.0
            ys = FLOOR_Y + R + 0.4
        prof = [(2.0, ys + 2.0), (-R, ys + 2.0), (-R, ys)]
        for j in range(1, 11):
            ang = (math.pi / 2.0) * (1.0 - j / 10.0)
            prof.append((-R + R * math.cos(ang), ys - R + R * math.sin(ang)))
        prof.append((2.0, ys - R))
        vv = [V(px + nx * u, v, pz + nz * u) for u, v in prof]
        secs.append(Part.makePolygon(vv + [vv[0]]))
    cutter = None
    for ruled in (False, True):
        try:
            cutter = Part.makeLoft(secs, True, ruled, False)
            if cutter.isValid() and cutter.Volume > 1.0:
                break
        except Exception as e:
            App.Console.PrintWarning("Rear arc cutter (ruled=%s) failed: %s\n" % (ruled, e))
            cutter = None
    if cutter is None:
        App.Console.PrintWarning("Rear arc rounding: no cutter - left sharp.\n")
        return half
    def _ok(r):
        return (r is not None and not r.isNull() and r.isValid() and r.Volume > 0.5 * half.Volume
                and len(r.Solids) <= len(half.Solids))              # no loose pieces

    res = half.cut(cutter)
    if not _ok(res):
        App.Console.PrintWarning("Rear arc rounding gave invalid geometry - left sharp.\n")
        return half
    if flange_keep is not None:
        # the flange must stay exactly as it was: whatever the cutter took out of the flange is put back (only that part, so the earlier
        # flange cuts - rear relief, blend - are not undone)
        try:
            lost = half.common(cutter).common(flange_keep)
            if not lost.isNull() and lost.Volume > 0.01:
                res2 = res.fuse(lost)
                if _ok(res2):
                    App.Console.PrintMessage("Rear arc rounding: %.0f mm3 put back into the flange.\n" % lost.Volume)
                    res = res2
                else:
                    App.Console.PrintWarning("Rear arc rounding: could not protect the flange - left sharp.\n")
                    return half
        except Exception as e:
            App.Console.PrintWarning("Rear arc rounding: flange protection failed (%s) - left sharp.\n" % e)
            return half
    App.Console.PrintMessage("Rear arc edge rolled over with radius %.1f mm (removed %.0f mm3).\n" % (REAR_ARC_ROLL_R, half.Volume - res.Volume))
    return res


def _mesh_parts(shape, tol=0.05):
    """number of separate pieces of the tessellated shape (vertices welded to 1 micron): 1 = one object in a slicer"""
    vs, ts = shape.tessellate(tol)
    key = {}
    ids = []
    for p in vs:
        ids.append(key.setdefault((round(p.x, 3), round(p.y, 3), round(p.z, 3)), len(key)))
    par = list(range(len(key)))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for a, b, c in ts:
        ra, rb, rc = find(ids[a]), find(ids[b]), find(ids[c])
        par[rb] = ra
        par[rc] = ra
    return len(set(find(i_) for i_ in range(len(key))))


def _front_edge_bottom_fill(half, Tz, rz):
    """v5.41: makes the front edge thicker and fully rounded in the lower part of the grip (it was a 0.3 mm wedge): a lofted filler from the real sections of the half. The extra height is
    A(z) at the edge (so the edge is Tz(z) thick, rounded with radius rz(z)) and dies away smoothly (smooth-step) over the first 9-16 mm behind the edge - so it never reaches the emblem's
    shield - and A(z) itself fades smoothly to 0 higher up (no step, no ridge). Returns the half unchanged if anything fails (or if the result is not one single piece)."""
    try:
        if FRONT_EDGE_T_BOTTOM <= FRONT_EDGE_T + 0.01:
            return half
        n_x, A_MIN = 24, 0.06

        def _ss(t_):
            t_ = min(1.0, max(0.0, t_))
            return t_ * t_ * (3.0 - 2.0 * t_)

        def Lg(z_):                                                    # reach behind the edge: wide in the lower part, 9.5 mm where the emblem's shield is (it starts 11 mm behind the edge)
            return 16.0 - 6.5 * _ss((z_ - 24.0) / 8.0)
        z_a, z_b = 0.3, FRONT_EDGE_BOTTOM_Z1
        n_a = int(round((z_b - z_a) / 1.5))
        secs = []
        for k in range(n_a + 1):
            z = z_a + (z_b - z_a) * k / float(n_a)
            segs = []
            for w in half.slice(V(0, 0, 1), z):
                pp = w.discretize(Distance=0.25)
                segs += [((a.x, a.y), (b.x, b.y)) for a, b in zip(pp, pp[1:])]
            if not segs:
                raise ValueError("empty section at z=%.1f" % z)
            xF0 = max(max(a[0], b[0]) for a, b in segs)
            xF = xF0 - 0.03                                              # a hair inside the front face (no coincident faces)
            yfl = min([p[1] for sg in segs for p in sg if p[0] > xF0 - 1.0 and p[1] > 8.0] or [9.0])
            ybot = yfl + 0.08

            def env(x_):
                best = None
                for (xa, ya), (xb, yb) in segs:
                    if (xa - x_) * (xb - x_) <= 0 and abs(xb - xa) > 1e-9:
                        yy = ya + (yb - ya) * (x_ - xa) / (xb - xa)
                        best = yy if best is None else max(best, yy)
                return best
            yE, rr = FLOOR_Y + Tz(z), rz(z)
            ys_e = env(xF0 - 0.9)                                        # surface height just behind the rounded corner
            if ys_e is None:
                raise ValueError("no surface at the edge at z=%.1f" % z)
            A = yE - ys_e
            if A < A_MIN:
                if z > 20.0:
                    break                                                # the thickening has faded out: the filler ends here (a step of less than 0.1 mm)
                A = 0.0                                                  # (lower down it only dips to nothing for a moment: keep the section, nothing is added there)
            L = Lg(z)
            x0 = xF - L - 0.5
            xe = xF - rr - 0.15
            pts = [(x0, ybot)]
            for i in range(n_x + 1):
                x_ = x0 + (xe - x0) * i / float(n_x)
                ys = env(min(x_, xF0 - 0.02))
                if ys is None:
                    ys = yE
                d_ = xF0 - x_
                ad = A * (1.0 - _ss(d_ / L))                            # the extra height at this distance behind the edge
                inset = 0.4 * (1.0 - min(1.0, ad / 0.5)) * min(1.0, d_ / 2.5)   # 0.4 mm inside the surface where (almost) nothing is added: no coincident faces
                pts.append((x_, ys + ad - inset))
            ysq = max(yE, pts[-1][1])
            rr = max(0.05, min(rr, ysq - ybot - 0.05))                  # the round must fit between the top and the bottom of the filler
            for k in range(1, 6):
                ph = math.radians(90.0 - 90.0 * k / 5.0)
                pts.append((xF - rr + rr * math.cos(ph), ysq - rr + rr * math.sin(ph)))
            pts.append((xF, ybot))
            secs.append(Part.makePolygon([V(x_, y_, z) for x_, y_ in pts] + [V(pts[0][0], pts[0][1], z)]))
        if len(secs) < 4:
            raise ValueError("too few sections")
        tool = Part.makeLoft(secs, True, True, False)
        if tool.isNull() or not tool.isValid() or tool.Volume < 5.0:
            raise ValueError("filler invalid")
        v0 = half.Volume
        for fz in (None, 0.005, 0.02):                                  # the plain fuse works (a fuzzy fuse of this filler returns a null shape)
            try:
                r_ = half.fuse(tool) if fz is None else half.fuse(tool, fz)
            except Exception:
                continue
            if (not r_.isNull() and r_.isValid() and len(r_.Solids) == 1 and len(r_.Shells) == 1 and 10.0 < r_.Volume - v0 < 3000.0
                    and _mesh_parts(r_) == _mesh_parts(half)):          # still ONE object
                App.Console.PrintMessage("Front edge: thicker and rounder in the lower part (+%.0f mm3, edge %.1f mm, %d sections up to z=%.0f).\n"
                                         % (r_.Volume - v0, FRONT_EDGE_T_BOTTOM, len(secs), secs[-1].BoundBox.ZMax))
                return r_
        raise ValueError("fuse gave no usable (single-piece) result")
    except Exception as e:
        App.Console.PrintWarning("Front edge filler failed (%s) - lower front edge left as it was.\n" % e)
        return half


def front_edge_taper(half, side=None):
    """v5.40: the front edge of the half gets the same thin run-out all the way up (as at the bottom of the grip): from FRONT_TAPER_L mm behind the edge the outer surface
    glides down (smooth-step) to FRONT_EDGE_T mm above the pocket floor, and the edge itself is rounded (FRONT_EDGE_ROUND). Built from the real sections of the half (so it starts
    exactly on its surface), as a lofted cutter from the heel up to the underside of the flange. Around the emblem the run-out is shorter, following the outline of the shield
    (wide at the top, pointed at the bottom) and changing length gradually (FRONT_TAPER_BLEND). Returns the half unchanged if anything fails."""
    try:
        z_lo, z_hi = 6.0, H - FLANGE_T - 0.2
        n_z, n_x = 50, 20
        def _ss(t_):
            t_ = min(1.0, max(0.0, t_))
            return t_ * t_ * (3.0 - 2.0 * t_)

        def Tz(z_):                                                      # thickness of the front edge at height z (thicker, rounder at the bottom)
            T_ = FRONT_EDGE_T + (FRONT_EDGE_T_BOTTOM - FRONT_EDGE_T) * (1.0 - _ss((z_ - FRONT_EDGE_BOTTOM_Z0) / (FRONT_EDGE_BOTTOM_Z1 - FRONT_EDGE_BOTTOM_Z0)))
            return 0.3 + (T_ - 0.3) * _ss(z_ / 3.0)                      # the very bottom (heel) blends into the natural thin edge

        def rz(z_):
            return FRONT_EDGE_ROUND + (Tz(z_) - FRONT_EDGE_T) * 0.7 if Tz(z_) > FRONT_EDGE_T else FRONT_EDGE_ROUND
        zs = [z_lo + (z_hi - z_lo) * kz / float(n_z) for kz in range(n_z + 1)]
        segl, xFl = [], []
        for z in zs:
            segs = []
            for w in half.slice(V(0, 0, 1), z):
                pp = w.discretize(Distance=0.25)
                segs += [((a.x, a.y), (b.x, b.y)) for a, b in zip(pp, pp[1:])]
            if not segs:
                raise ValueError("empty section at z=%.1f" % z)
            segl.append(segs)
            xFl.append(max(max(a[0], b[0]) for a, b in segs))
        # run-out length per section: full length, but behind the emblem's front edge where the emblem is (the shield outline, wide at the top and pointed at the bottom, not its bounding box)
        Ls = [FRONT_TAPER_L] * len(zs)
        if LOGO and LOGO_SIDE in ("both", side):
            cx = x_range(LOGO_Z)[1] - LOGO_FROM_FRONT
            a_, top_ = LOGO_W / 2.0, LOGO_H / 2.0
            v1_ = top_ - 0.38 * LOGO_H

            def u_sh(v):                                              # half width of the shield at height v above its centre
                if v > top_ or v < -top_:
                    return None
                if v >= v1_:
                    return a_
                return a_ * (1.0 - ((v1_ - v) / (v1_ + top_)) ** 1.8)
            req = []
            for z, xF in zip(zs, xFl):
                us = [u_sh(z - LOGO_Z + dv) for dv in (-FRONT_TAPER_BLEND * 0.5, 0.0, FRONT_TAPER_BLEND * 0.5)]   # a little wider than the shield above and below it
                us = [u for u in us if u is not None]
                req.append(FRONT_TAPER_L if not us else min(FRONT_TAPER_L, max(7.0, xF - (cx + max(us) + 1.5))))
            dz_ = zs[1] - zs[0]
            wnd = max(1, int(round(FRONT_TAPER_BLEND / dz_)))
            ero = [min(req[max(0, k - wnd):k + wnd + 1]) for k in range(len(zs))]       # shortest length within the window ...
            hw = max(1, wnd // 2)
            Ls = [sum(ero[max(0, k - hw):k + hw + 1]) / float(len(ero[max(0, k - hw):k + hw + 1])) for k in range(len(zs))]   # ... then averaged (never longer than allowed)
        secs = []
        for kz, z in enumerate(zs):
            segs, xF, Lz = segl[kz], xFl[kz], Ls[kz]
            yE, rr = FLOOR_Y + Tz(z), rz(z)

            def env(x_):
                best = None
                for (xa, ya), (xb, yb) in segs:
                    if (xa - x_) * (xb - x_) <= 0 and abs(xb - xa) > 1e-9:
                        yy = ya + (yb - ya) * (x_ - xa) / (xb - xa)
                        best = yy if best is None else max(best, yy)
                return best
            x0 = xF - Lz
            xe = xF - rr - 0.15                                         # the grid ends here, then a quarter round (radius rr) over the corner of the front face
            pts = []
            yb0 = env(x0 - 1.0)
            if yb0 is None:
                raise ValueError("no surface at z=%.1f" % z)
            pts.append((x0 - 1.0, yb0 + 0.4))
            for i in range(n_x + 1):
                t = i / float(n_x)
                x_ = x0 + (xe - x0) * t
                tt = (x_ - x0) / Lz
                ys = env(min(x_, xF - 0.02))
                if ys is None:
                    ys = yE
                e = 0.88 * (3 * tt * tt - 2 * tt ** 3) + 0.12 * tt
                pts.append((x_, ys - e * (ys - yE)))                    # below the surface where it is thicker than the edge, above it (in the air) where it is already thinner
            for k in range(1, 6):                                       # quarter round: from the top of the front face down onto the face
                ph = math.radians(90.0 - 90.0 * k / 5.0)
                pts.append((xF - rr + rr * math.cos(ph), yE - rr + rr * math.sin(ph)))
            pts += [(xF + 2.0, yE - rr), (xF + 2.0, 26.0), (x0 - 1.0, 26.0)]
            secs.append(Part.makePolygon([V(x_, y_, z) for x_, y_ in pts] + [V(pts[0][0], pts[0][1], z)]))
        tool = Part.makeLoft(secs, True, True, False)
        if tool.isNull() or not tool.isValid() or tool.Volume < 10.0:
            raise ValueError("cutter invalid")
        v0 = half.Volume
        res = None
        for fz in (0.01, 0.03, 0.06):                                   # the plain cut silently removes nothing (the cutter starts tangent to the surface): small fuzzy tolerance
            try:
                r_ = half.cut(tool, fz)
            except Exception:
                continue
            if (not r_.isNull() and r_.isValid() and len(r_.Solids) == 1 and 100.0 < v0 - r_.Volume < 0.2 * v0):
                res = r_
                break
        if res is None:
            raise ValueError("cut gave no usable result")
        res = _front_edge_bottom_fill(res, Tz, rz)
        App.Console.PrintMessage("Front edge run-out: %.0f mm3 removed (edge %.1f mm thick, rounded r %.1f, run-out %.0f mm, %.0f-%.0f mm round the emblem).\n"
                                 % (v0 - res.Volume, FRONT_EDGE_T, rr, FRONT_TAPER_L, min(Ls), max(Ls)))
        return res
    except Exception as e:
        App.Console.PrintWarning("Front edge run-out failed (%s) - front edge left as it was.\n" % e)
        return half


def groove_tools(half, palm):
    """straight vertical V-grooves inside the panel outline (clear of the screws), each cut as short straight prisms that follow the surface"""
    d0 = surface_correction(half, palm) - PANEL_RECESS            # measured surface minus analytic surface
    bb = panel_face.BoundBox
    ring_r = HEAD_D / 2.0 + SCREW_RING
    nx = int(bb.XLength / GROOVE_PITCH)
    x0 = (bb.XMin + bb.XMax) / 2.0 - nx * GROOVE_PITCH / 2.0
    tools = []
    for i in range(nx + 1):
        x = x0 + i * GROOVE_PITCH
        zs = [bb.ZMin + 0.5 * k for k in range(int(bb.ZLength / 0.5) + 1)]
        runs, run = [], []
        for z in zs:
            ok = _in_panel(x, z, 1.2) and all(math.hypot(x - sx, z - sz) > ring_r for sx, sz in screws)
            if ok:
                run.append(z)
            if (not ok or z == zs[-1]) and run:
                if run[-1] - run[0] > 3.0:
                    runs.append((run[0], run[-1]))
                run = []
        for za, zb in runs:
            n = max(1, int(math.ceil((zb - za) / GROOVE_SEG)))
            for j in range(n):
                z1, z2 = za + (zb - za) * j / n, za + (zb - za) * (j + 1) / n
                p1 = V(x, surface_y(x, z1, palm) + d0 + GROOVE_HALF - GROOVE_DEPTH, z1)
                p2 = V(x, surface_y(x, z2, palm) + d0 + GROOVE_HALF - GROOVE_DEPTH, z2)
                t = p2 - p1
                L = t.Length
                if L < 1e-6:
                    continue
                t.normalize()
                try:
                    a = p1 - t * 0.3
                    tools.append(Part.Face(_diamond(a, t, V(1, 0, 0), GROOVE_HALF)).extrude(t * (L + 0.6)))
                except Exception:
                    pass
    return tools


def build_half(palm, thumb, side=None):
    no_flange = bool(FLANGE_REMOVE_SIDE is not None and side == FLANGE_REMOVE_SIDE and (head_solid is not None or layer_clip is not None))
    body_full = make_body(palm, prism_left) if (no_flange and FLANGE_REMOVE_STRAIGHT_FRONT and prism_left is not None) else make_body(palm)
    # the half with the 30 x 10 cut-in: the ordinary 33 mm relief is left out of its cavity (the cut-in replaces it and the wall behind it stays)
    own_deep = bool(no_flange and LOBE and LOBE_DEEP_SIDE is not None and side == LOBE_DEEP_SIDE and LOBE_DEEP_D > LOBE_D)
    half = body_full.cut(cavity_nolobe if own_deep else cavity).common(Part.makeBox(400, 200, 400, V(-200, 0, -100)))
    top_layer = None
    if HEAD_AS_BODY and layer_clip is not None and not no_flange:
        # the top layer is cut out of the grip's own swelling body (before the rear cut-in is made), inner face on the pocket floor, tilted like the old flange
        try:
            # one clip at a time (the three clips in one go made OCC return an invalid shape)
            top_layer = body_full
            for _clip in layer_parts:
                _nx = top_layer.common(_clip)
                if _nx.isNull() or not _nx.isValid() or _nx.Volume < 1000.0:
                    raise ValueError("clip step gave %s" % ("nothing" if _nx.isNull() else "volume %.0f, valid=%s" % (_nx.Volume, _nx.isValid())))
                top_layer = _nx
            if top_layer.isNull() or not top_layer.isValid() or top_layer.Volume < 1000.0:
                raise ValueError("top layer empty or invalid (%.0f mm3)" % (0.0 if top_layer.isNull() else top_layer.Volume))
            if layer_floor is not None:
                _done = False
                for _fz in (None, 1e-3, 5e-3, 2e-2):                    # OCC sometimes returns an empty fuse: retry with a small fuzzy tolerance
                    try:
                        _tf = top_layer.fuse(layer_floor) if _fz is None else top_layer.fuse(layer_floor, _fz)
                    except Exception:
                        continue
                    if (not _tf.isNull() and _tf.isValid() and len(_tf.Solids) == 1 and _tf.Volume >= top_layer.Volume - 1.0):
                        top_layer = _tf
                        _done = True
                        break
                if not _done:
                    App.Console.PrintWarning("Top minimum thickness skipped (result not valid).\n")
            if layer_rear_cut is not None:
                top_layer = try_op("Top rear wall", lambda sh: sh.cut(layer_rear_cut), top_layer)
            top_layer = try_op("Top notch", lambda sh: sh.cut(notch_tool), top_layer)
        except Exception as e:
            App.Console.PrintWarning("Top layer failed (%s) - this half gets no top.\n" % e)
            top_layer = None
    if wall_addon is not None:
        half = try_op("Wall wider at the screw", lambda sh: sh.fuse(wall_addon), half)
    if rear_cut is not None:
        half = try_op("Rear cut behind the spur", lambda sh: sh.cut(rear_cut), half)
    if no_flange:
        # no flange on this half: the rear trim as on the other half, then everything above the flange underside is cut off, and the original outline (without the head / toe lip /
        # front overhang) is kept; the relief(s) under the flange are cut as usual (they are now open at the top)
        if rear_trim is not None:
            half = try_op("Rear trim", lambda sh: sh.cut(rear_trim), half)
        half = half.cut(Part.makeBox(400, 200, 80, V(-200, -100, H - FLANGE_T)))
        half = try_op("Original outline (no head)", lambda sh: sh.common(prism_left if (FLANGE_REMOVE_STRAIGHT_FRONT and prism_left is not None) else prism), half)
        App.Console.PrintMessage("No flange on the %s half: cut flat at z = %.1f.\n" % (side, H - FLANGE_T))
        if LOBE:
            if not own_deep:
                half = try_op("Lobe after flange", lambda sh: sh.cut(lobe_post), half)
            if LOBE_DEEP_SIDE is not None and side == LOBE_DEEP_SIDE and LOBE_DEEP_D > LOBE_D:
                half = try_op("Deeper relief (%s half)" % side, lambda sh: sh.cut(lobe_deep_tool(palm)), half)
        half = try_op("Rear arc rounding", lambda sh: round_rear_arc(sh, palm), half)
    elif head_solid is not None or top_layer is not None:        # the body stops under the flange; the flange is a thin plate (or, HEAD_AS_BODY, a layer of the body itself)
        if rear_trim is not None:
            half = try_op("Rear trim", lambda sh: sh.cut(rear_trim), half)
        half = half.cut(Part.makeBox(400, 200, 80, V(-200, -100, H - FLANGE_T))).fuse(top_layer if top_layer is not None else head_solid)
        if FLANGE_BLEND > 0 and top_layer is None:
            half = flange_blend(half)
        if LOBE:
            half = try_op("Lobe after flange", lambda sh: sh.cut(lobe_post), half)
            if LOBE_DEEP_SIDE is not None and side == LOBE_DEEP_SIDE and LOBE_DEEP_D > LOBE_D:
                _v0 = half.Volume
                half = try_op("Deeper relief (%s half)" % side, lambda sh: sh.cut(lobe_deep_tool(palm)), half)
                App.Console.PrintMessage("Deeper relief under the flange on the %s half: %.0f mm3 removed (%.1f mm beyond the pocket floor, %.1f mm wall left outside).\n" % (side, _v0 - half.Volume, LOBE_DEEP_D, LOBE_DEEP_WALL))
        if flange_rear_cut is not None:
            half = try_op("Flange rear deeper", lambda sh: sh.cut(flange_rear_cut), half)
        if top_layer is not None and rear_wall is not None:
            _hw = try_op("Rear wall up to the notch", lambda sh: sh.fuse(rear_wall), half)
            if len(_hw.Solids) == 1 and _hw.Volume > half.Volume:
                half = _hw
            else:
                App.Console.PrintWarning("Rear wall up to the notch skipped (%d solids).\n" % len(_hw.Solids))
        half = try_op("Rear arc rounding", lambda sh: round_rear_arc(sh, palm), half)
        if FRONT_TAPER_SIDE is not None and side == FRONT_TAPER_SIDE:
            half = front_edge_taper(half, side)
    panel_y = PANEL_FLAT_Y + (PALM_EXTRA if palm else 0.0)    # the panel floor moves out with the palm swell

    panel_curved_ok = False
    if PANEL and PANEL_CURVED:
        try:
            deep = panel_face.extrude(V(0, 80.0, 0)).cut(make_inner(palm))
            half2 = half.cut(deep)
            if half2.isValid() and not half2.isNull():
                half = half2
                panel_curved_ok = True
        except Exception as e:
            App.Console.PrintWarning("Curved panel failed (%s) - using the flat panel.\n" % e)
    if PANEL and not panel_curved_ok:
        deep = panel_face.extrude(V(0, 80.0 - panel_y, 0))
        deep.translate(V(0, panel_y, 0))
        half = try_op("Recessed panel", lambda s: s.cut(deep), half)

    # counterbores from the local surface (inside or outside the panel)
    for x, z in screws:
        try:
            ys = max(v.Y for v in half.common(Part.makeLine(V(x, 0, z), V(x, 80, z))).Vertexes)
        except Exception:
            ys = min(surface_y(x, z, palm), panel_y)
        if INSERT_SIDE is not None and side == INSERT_SIDE:
            # hole for a threaded insert, carried on through the wall as a clearance hole (no screw-head recess on this half)
            try:
                y_in = min(v.Y for v in half.common(Part.makeLine(V(x, 0, z), V(x, 80, z))).Vertexes)
            except Exception:
                y_in = 0.0
            y_in = max(y_in, 0.0)
            y_end = min(y_in + INSERT_L + INSERT_MELT, ys - INSERT_MIN_WALL)
            App.Console.PrintMessage("Insert hole at x=%.1f z=%.1f (%s half): starts y=%.1f, ends y=%.1f (depth %.1f mm, insert %.1f mm), outer surface y=%.1f, wall left %.1f mm.\n"
                                     % (x, z, side, y_in, y_end, y_end - y_in, INSERT_L, ys, ys - y_end))
            if y_end - y_in < INSERT_L:
                App.Console.PrintWarning("Insert hole is shorter than the insert (%.1f < %.1f mm) - thicken the wall or use a shorter insert.\n" % (y_end - y_in, INSERT_L))
            half = half.cut(Part.makeCylinder(INSERT_D / 2.0, y_end - y_in + 1.0, V(x, y_in - 1.0, z), V(0, 1, 0)))
            if INSERT_THROUGH:
                half = half.cut(Part.makeCylinder(SCREW_D / 2.0, 80.0, V(x, y_end - 0.5, z), V(0, 1, 0)))
            continue
        y_fl = None
        if INSERT_SIDE is not None:
            try:
                y_fl = max(min(v.Y for v in half.common(Part.makeLine(V(x, 0, z), V(x, 80, z))).Vertexes), 0.0)
            except Exception:
                y_fl = None
        half = half.cut(Part.makeCylinder(SCREW_D / 2.0, 80.0, V(x, 0, z), V(0, 1, 0)))
        half = half.cut(Part.makeCylinder(HEAD_D / 2.0, 40.0, V(x, ys - HEAD_DEPTH, z), V(0, 1, 0)))
        if y_fl is not None:
            App.Console.PrintMessage("Screw at x=%.1f z=%.1f (%s half): head recess bottom y=%.1f, floor y=%.1f -> %.1f mm of screw in this half.\n"
                                     % (x, z, side, ys - HEAD_DEPTH, y_fl, ys - HEAD_DEPTH - y_fl))

    # emblem (separate part, handed back in EMBLEMS)
    if LOGO and LOGO_SIDE in (side, "both") and screws:
        try:
            _rear, _front = x_range(LOGO_Z)
            lcx, lcz = _front - LOGO_FROM_FRONT, LOGO_Z
            field_, shield_ = logo_tool(palm, lcx, lcz)
            App.Console.PrintMessage("Emblem (%s half, %s): centre x=%.1f z=%.1f, %.1f mm behind the front edge, %.1f mm in front of the upper screw; shield %.0f x %.0f mm.\n"
                                     % (side, LOGO_MODE, lcx, lcz, _front - lcx, lcx - screws[0][0], LOGO_W, LOGO_H))
            emb = None
            if LOGO_MODE == "integrated":
                down_ = half.copy()
                down_.translate(V(0, -LOGO_DEPTH, 0))
                cut_ = field_.common(half).cut(down_)          # the top layer (LOGO_DEPTH thick, following the real surface) inside the field
                _v0 = half.Volume
                half = try_op("Emblem", lambda sh: sh.cut(cut_), half)
                App.Console.PrintMessage("Emblem cut into the grip: %.0f mm3 removed (%.1f mm deep).\n" % (_v0 - half.Volume, LOGO_DEPTH))
            elif LOGO_MODE == "overlay":
                up_ = half.copy()
                up_.translate(V(0, LOGO_T, 0))
                up_d = half.copy()
                up_d.translate(V(0, LOGO_T - LOGO_DEPTH, 0))
                emb = shield_.extrude(V(0, 60.0, 0)).common(up_).cut(half)
                emb = emb.cut(field_.common(up_).cut(up_d))
            else:
                _ys = []
                bbs = shield_.BoundBox
                for fx in (0.0, 0.25, 0.5, 0.75, 1.0):
                    for fz in (0.0, 0.25, 0.5, 0.75, 1.0):
                        px_, pz_ = bbs.XMin + fx * bbs.XLength, bbs.ZMin + fz * bbs.ZLength
                        if not shield_.isInside(V(px_, 0, pz_), 0.01, True):
                            continue
                        try:                                    # the real outer surface of this half under the shield
                            _ys.append(max(v.Y for v in half.common(Part.makeLine(V(px_, 0, pz_), V(px_, 80, pz_))).Vertexes))
                        except Exception:
                            _ys.append(surface_y(px_, pz_, palm))
                y_floor = min(_ys) - LOGO_POCKET_MIN
                App.Console.PrintMessage("Emblem pocket: floor y=%.1f (surface y %.1f..%.1f).\n" % (y_floor, min(_ys), max(_ys)))
                emb = shield_.extrude(V(0, 60.0, 0))
                emb.translate(V(0, y_floor, 0))
                emb = emb.common(half).cut(field_.cut(logo_inner(palm)))
                pocket = shield_.makeOffset2D(LOGO_FIT, 0, False, False, True)
                if isinstance(pocket, Part.Compound) and pocket.Faces:
                    pocket = pocket.Faces[0]
                pocket = pocket.extrude(V(0, 60.0, 0))
                pocket.translate(V(0, y_floor, 0))
                _v0 = half.Volume
                half = try_op("Emblem pocket", lambda sh: sh.cut(pocket), half)
                App.Console.PrintMessage("Emblem pocket: %.0f mm3 removed from the grip.\n" % (_v0 - half.Volume))
            if emb is not None:
                emb = emb.removeSplitter()
                App.Console.PrintMessage("Emblem: %.0f mm3, %d solid(s), valid=%s.\n" % (emb.Volume, len(emb.Solids), emb.isValid()))
                if emb.isValid() and len(emb.Solids) == 1 and emb.Volume > 100.0:
                    EMBLEMS[side] = emb
        except Exception as e:
            App.Console.PrintWarning("Emblem failed (%s) - left out.\n" % e)

    # the square tenon that goes into the metal grip (stands out from the pocket floor toward the centre)
    pad = Part.makeBox(pad_w, FLOOR_Y - pad_tip + 1.0, pad_l, V(-pad_w / 2.0, pad_tip, -pad_l / 2.0))
    pad = try_op("Tenon corner rounding", lambda sh: sh.makeFillet(
        PAD_R, [e for e in sh.Edges if abs(e.Vertexes[0].Y - e.Vertexes[-1].Y) > 1e-6]), pad)
    pad.translate(V(pad_xl, 0, pad_sw))
    # the tenon is trimmed by the outline of THIS half (with the head / the straight front), not by the old plain outline: moved forward it would otherwise be cut flat at the front
    _pad_clip = prism_left if (no_flange and FLANGE_REMOVE_STRAIGHT_FRONT and prism_left is not None) else BODY_PRISM
    half = half.fuse(to_pocket_frame(pad).common(_pad_clip))
    if own_deep:                                                  # the top of the tenon now reaches the cut-in: its 1 mm overlap into the wood must not fill the cut-in again
        half = try_op("Cut-in again after the tenon", lambda sh: sh.cut(lobe_deep_tool(palm)), half)

    if CHECKERING and PANEL and panel_curved_ok:
        try:
            key = PALM_EXTRA if palm else 0.0
            if key not in _checker_cache:
                _checker_cache[key] = checker_runs(palm, surface_correction(half, palm))
            runs = _checker_cache[key]
            App.Console.PrintMessage("Checkering: %d groove lines.\n" % len(runs))
            half, ok = cut_tools(half, sweep_tools(runs), "Checkering (swept grooves)")
            if not ok:
                App.Console.PrintWarning("Swept grooves did nothing - trying short straight segments instead (slower).\n")
                half, ok = cut_tools(half, segment_tools(runs), "Checkering (segments)", chunk=60)
            if not ok:
                App.Console.PrintWarning("Checkering produced nothing - see the messages above.\n")
        except Exception as e:
            App.Console.PrintWarning("Curved checkering failed (%s) - continuing without it.\n" % e)
    elif CHECKERING and PANEL:
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

    if GROOVES:
        try:
            tl = groove_tools(half, palm)
            App.Console.PrintMessage("Grooves: %d straight pieces.\n" % len(tl))
            half, ok = cut_tools(half, tl, "Vertical grooves", chunk=20)
        except Exception as e:
            App.Console.PrintWarning("Grooves failed (%s) - continuing without them.\n" % e)

    if thumb and THUMB_REST:
        half = try_op("Thumb rest", lambda s: s.fuse(thumb_shelf(palm)), half)
    return half


def support_ribs():
    """breakaway ribs standing on the bed (y = 0) under the pocket floor and the tang cut-in, RIB_GAP short of the
    floor and the tenon and RIB_SIDE_GAP away from the walls beside them"""
    ribs = []
    x = RIB_PITCH / 2.0
    _toe_on = bool(RIB_UNDER_TOE and FLANGE and (head_solid is not None or HEAD_AS_BODY))
    # with RIB_UNDER_TOE the ribs continue forward under the overhang (the flange tip, toe lip and neck plate stick out FLANGE_FRONT_OVERHANG in front of the strap)
    _x_front = POCKET_FROM_FRONT / CR + 5.0 + ((FLANGE_FRONT_OVERHANG / CR + 4.0) if _toe_on else 0.0)
    while x < _x_front:
        ribs.append(Part.makeBox(RIB_T, FLOOR_Y - RIB_GAP, H + 12.0 - pk_z0, V(x - RIB_T / 2.0, 0, pk_z0)))
        x += RIB_PITCH
    keep_out = Part.makeBox(pad_w + 2.0 * RIB_SIDE_GAP, FLOOR_Y, pad_l + 2.0 * RIB_SIDE_GAP,
                            V(pad_xl - pad_w / 2.0 - RIB_SIDE_GAP, pad_tip - RIB_PAD_GAP, pad_sw - pad_l / 2.0 - RIB_SIDE_GAP))
    ribs = to_pocket_frame(Part.makeCompound(ribs).cut(keep_out))
    if TANG_CUT:
        behind = to_pocket_frame(Part.makeBox(200, 200, 400, V(-200 - RIB_SIDE_GAP, -100, -200)))  # behind the rear wall
        tribs = []
        x = pocket_rear(H) - RIB_PITCH / 2.0
        # these ribs only belong under the flange: none behind its rear end (the outline still reaches 10 mm further back than the shortened flange,
        # so ribs there stood in the air beside the part)
        _x_lim = (x_end + 1.0 + RIB_T / 2.0) if (FLANGE and (head_solid is not None or HEAD_AS_BODY)) else tx_min
        while x > max(tx_min, _x_lim):
            tribs.append(Part.makeBox(RIB_T, FLOOR_Y - RIB_GAP, H + 6.0 - TANG_Z0 - RIB_SIDE_GAP,
                                      V(x - RIB_T / 2.0, 0, TANG_Z0 + RIB_SIDE_GAP)))
            x -= RIB_PITCH
        ribs = Part.makeCompound(ribs.Solids + Part.makeCompound(tribs).common(behind).Solids)
    _clip = prism
    if _toe_on:
        # the ribs may also stand under the head plate (flange + front overhang), whose outline reaches beyond the body outline in front
        try:
            _c = prism.fuse(head_side)
            if _c.isValid() and not _c.isNull():
                _clip = _c
            else:
                App.Console.PrintWarning("Ribs under the toe: outline union invalid - no ribs under the overhang.\n")
        except Exception as e:
            App.Console.PrintWarning("Ribs under the toe failed (%s) - no ribs under the overhang.\n" % e)
    ribs = ribs.common(_clip)
    if wall_addon_clear is not None:
        ribs = try_op("Ribs clear of the widened wall", lambda sh: sh.cut(wall_addon_clear), ribs)
    return ribs.cut(rear_cut) if rear_cut is not None else ribs


def band(shape, z0, z1, y1=200.0):
    return shape.common(Part.makeBox(400, y1, z1 - z0, V(-200, 0, z0)))


thumb_side = {"right": "left", "left": "right"}.get(HAND)
palm_side = {"right": "right", "left": "left"}.get(HAND)
def unmeshable_faces(shape):
    """faces the STL export cannot turn into triangles (a face with a degenerate hole in it): they would be MISSING in the slicer. Returns [(face no., area)]"""
    bad = []
    for i, f in enumerate(shape.Faces):
        try:
            if f.Area < 20.0:
                continue
            v, t = f.tessellate(0.1)
            a = sum(0.5 * (v[k[1]] - v[k[0]]).cross(v[k[2]] - v[k[0]]).Length for k in t)
            if abs(a / f.Area - 1.0) > 0.08:
                bad.append((i, round(f.Area)))
        except Exception:
            bad.append((i, -1))
    return bad


def safe_half(label, palm, thumb, side=None):
    global REAR_ROLL_R
    r0 = REAR_ROLL_R
    try:
        best = None
        for eps in (0.05, 0.0, -0.05, 0.1, -0.1, 0.2):             # if the result has a face that cannot be meshed, the rear roll radius is changed by a hair (mm) and the half built again
            REAR_ROLL_R = r0 + eps if r0 > 0 else r0
            h = build_half(palm, thumb, side)
            if h.isNull() or h.Volume < 1000.0:
                raise ValueError("empty result")
            bad = unmeshable_faces(h)
            if not bad:
                if eps != 0.0:
                    App.Console.PrintMessage("%s half: a face could not be meshed - rear roll radius %.2f instead of %.2f mm, now fine.\n" % (label, REAR_ROLL_R, r0))
                return h
            App.Console.PrintWarning("%s half: %d face(s) cannot be meshed (%s) - trying again with a tiny change.\n" % (label, len(bad), bad))
            if best is None:
                best = h
        App.Console.PrintError("%s half: could not get a fully meshable result - the STL may have a hole.\n" % label)
        return best
    except Exception as e:
        App.Console.PrintError("%s half failed (%s) - retrying without the thumb rest.\n" % (label, e))
        return build_half(palm, False, side)
    finally:
        REAR_ROLL_R = r0


plus_y = safe_half("Gun's left", palm_side == "left", thumb_side == "left", "left")                 # gun's left side
minus_y = plus_y if HAND not in ("right", "left") else safe_half("Gun's right", palm_side == "right", thumb_side == "right", "right")
ribs = support_ribs() if (SUPPORT_RIBS and LAYOUT == "print" and not FIT_PLATE) else None

test_z = (pad_zc - PAD_L / 2.0 - 5.0, pad_zc + PAD_L / 2.0 + 5.0)
if FIT_PLATE:
    plus_y, minus_y = [band(s, test_z[0], test_z[1], FLOOR_Y + FIT_PLATE_T) for s in (plus_y, minus_y)]
elif PRINT_TEST:
    plus_y, minus_y = [band(s, *test_z) for s in (plus_y, minus_y)]
    if ribs is not None:
        ribs = band(ribs, *test_z)

def deep_relief_ribs(half, base_ribs):
    """v5.40: breakaway ribs that continue up through the deeper relief (its roof is LOBE_DEEP_D above the pocket floor, further than the ordinary ribs reach):
    thin walls on the same pitch as the other ribs, standing on the bed, RIB_GAP short of the roof (the half pushed RIB_GAP towards the bed is cut out of them)
    and RIB_SIDE_GAP in from the edge of the relief. Returns base_ribs with them fused on (unchanged if anything fails)."""
    try:
        foot = Part.Face(Part.makePolygon(_lobe_deep_poly + [_lobe_deep_poly[0]]))
        foot = foot.makeOffset2D(-RIB_SIDE_GAP)
        prism_f = foot.extrude(V(0, FLOOR_Y + LOBE_DEEP_D + 5.0, 0))
        cols = []
        for k in range(-12, 30):
            x_ = RIB_PITCH / 2.0 + k * RIB_PITCH
            cols.append(Part.makeBox(RIB_T, FLOOR_Y + LOBE_DEEP_D - RIB_GAP, H + 12.0 - pk_z0, V(x_ - RIB_T / 2.0, 0, pk_z0)))
        cols = to_pocket_frame(Part.makeCompound(cols))
        lowered = half.copy()
        lowered.translate(V(0, -RIB_GAP, 0))
        extra = cols.common(prism_f).cut(lowered)
        extra = Part.makeCompound([s for s in extra.Solids if s.Volume > 5.0])
        n_ = len(extra.Solids)
        if n_ == 0:
            App.Console.PrintWarning("Ribs under the deeper relief: none needed.\n")
            return base_ribs
        res = base_ribs.fuse(extra).removeSplitter()
        if res.isNull() or not res.isValid():
            App.Console.PrintWarning("Ribs under the deeper relief: result invalid - left out.\n")
            return base_ribs
        App.Console.PrintMessage("Ribs under the deeper relief: %d rib pieces added (%.0f mm3).\n" % (n_, extra.Volume))
        return res
    except Exception as e:
        App.Console.PrintWarning("Ribs under the deeper relief failed (%s) - left out.\n" % e)
        return base_ribs


ribs_x_l = ribs_x_r = ribs
if ribs is not None and LOBE and LOBE_DEEP_SIDE is not None and LOBE_DEEP_D > LOBE_D and not PRINT_TEST and not FIT_PLATE:
    if LOBE_DEEP_SIDE == "left":
        ribs_x_l = deep_relief_ribs(plus_y, ribs)
    elif LOBE_DEEP_SIDE == "right":
        ribs_x_r = deep_relief_ribs(minus_y, ribs)

left = plus_y
right = minus_y.mirror(V(0, 0, 0), V(0, 1, 0))
ribs_l = ribs_x_l
ribs_r = ribs_x_r.mirror(V(0, 0, 0), V(0, 1, 0)) if ribs_x_r is not None else None

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
    try:
        clean = shp.removeSplitter()
        ok = (not clean.isNull()) and clean.isValid() and clean.Volume > 0.5 * abs(shp.Volume)
    except Exception:
        ok = False
    o.Shape = clean if ok else shp
    if not ok:
        App.Console.PrintWarning("%s: removeSplitter() failed, using the raw shape.\n" % nm)
    objs.append(o)
rib_objs = []
for nm, shp in (("Support_Right", ribs_r), ("Support_Left", ribs_l)):
    if shp is not None:
        o = doc.addObject("Part::Feature", nm)
        o.Shape = shp
        rib_objs.append(o)
emblem_obj = None
_emb = EMBLEMS.get("left") if LOGO_SIDE in ("left", "both") else EMBLEMS.get("right")
if LOGO and _emb is not None:
    _emb = _emb.copy()
    if LAYOUT != "assembled":
        _eb = _emb.optimalBoundingBox()
        if LOGO_MODE == "inlay":
            # back face (flat, y = floor of the pocket) down on the bed, next to the halves
            _emb.rotate(V(0, 0, 0), V(1, 0, 0), 90 if LOGO_SIDE in ("left", "both") else -90)
            _eb = _emb.optimalBoundingBox()
            _emb.translate(V(75.0 - _eb.XMin, -60.0 - (_eb.YMin + _eb.YMax) / 2.0, -_eb.ZMin))
        else:
            # overlay: stands as on the grip (z up), the curved plate prints without support; next to the halves
            _emb.translate(V(75.0 - _eb.XMin, -60.0 - (_eb.YMin + _eb.YMax) / 2.0, -_eb.ZMin))
    emblem_obj = doc.addObject("Part::Feature", "Emblem")
    emblem_obj.Shape = _emb
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
        if emblem_obj is not None:
            Mesh.export([emblem_obj], os.path.join(EXPORT_DIR, "emblem.stl"))
    except Exception as e:
        App.Console.PrintError("STL export failed: %s\n" % e)

for o in objs:
    bb_ = o.Shape.BoundBox
    App.Console.PrintMessage("%s: valid=%s, %.1f cm3, box x %.0f..%.0f  y %.0f..%.0f  z %.0f..%.0f\n" % (
        o.Name, o.Shape.isValid(), o.Shape.Volume / 1000.0, bb_.XMin, bb_.XMax, bb_.YMin, bb_.YMax, bb_.ZMin, bb_.ZMax))
if emblem_obj is not None:
    _b = emblem_obj.Shape.optimalBoundingBox()
    App.Console.PrintMessage("Emblem: valid=%s, %.2f cm3, %d solid(s), box %.1f x %.1f x %.1f mm\n" % (emblem_obj.Shape.isValid(), emblem_obj.Shape.Volume / 1000.0,
                             len(emblem_obj.Shape.Solids), _b.XLength, _b.YLength, _b.ZLength))
for o in rib_objs:
    App.Console.PrintMessage("%s: %d ribs, valid=%s\n" % (o.Name, len(o.Shape.Solids), o.Shape.isValid()))
App.Console.PrintMessage(
    "NEXT: measure the metal grip (thickness, depth of the hole for the tenon), the pocket's rear wall, "
    "the screw positions and THUMB_DROP. Print FIT_PLATE = True first to check pocket and tenon, "
    "then the halves on their inner faces (the orange ribs are breakaway supports under the pocket floor).\n")