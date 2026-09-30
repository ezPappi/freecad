import math
import FreeCAD as App
import Part
from FreeCAD import Vector

# 1. Get or create active document
doc = App.activeDocument()
if not doc:
    doc = App.newDocument("Skadis_Combined_Mount")

# ==========================================
# PARAMETERS
# ==========================================
# Base / Flared Skirt
base_width = 38.0          # Base length & width (mm)
base_corner_r = 10.0        # Corner fillet radius
flare_height = 3.0         # Height of the flared base transition

# Center Column
col_radius = 13.0         # Column radius (Ø25 mm)
col_height = 2.0          # Column height above base flare

# Skådis Top Peg
peg_width = 4.8            # Width (fits 5 mm Skådis slot)
peg_length = 14.5          # Length (fits 15 mm Skådis slot)
peg_height = 5.3           # Peg height
peg_notch_w = 3.2          # Cross-slot notch width

# Cutouts & Holes
center_hole_dia = 4.5      # Through-hole diameter (e.g., M4)
counterbore_dia = 4.5      # Top recess diameter
counterbore_depth = 3.5    # Recess depth
mounting_hole_dia = 2.5    # 4x mounting holes in flared skirt
mounting_hole_pos = 16.0   # Offset from center for mounting holes

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def make_8edge_wire(w, l, r, z=0.0):
    """Creates a closed 8-edge wire (4 lines, 4 arcs) to guarantee robust lofting."""
    r = min(r, (w / 2.0) - 0.01, (l / 2.0) - 0.01)
    dx = (w / 2.0) - r
    dy = (l / 2.0) - r

    p1 = Vector(-dx, -l/2.0, z)
    p2 = Vector(dx, -l/2.0, z)
    p3 = Vector(w/2.0, -dy, z)
    p4 = Vector(w/2.0, dy, z)
    p5 = Vector(dx, l/2.0, z)
    p6 = Vector(-dx, l/2.0, z)
    p7 = Vector(-w/2.0, dy, z)
    p8 = Vector(-w/2.0, -dy, z)

    c1 = Vector(dx, -dy, z)
    c2 = Vector(dx, dy, z)
    c3 = Vector(-dx, dy, z)
    c4 = Vector(-dx, -dy, z)

    def make_arc(p_start, p_end, center):
        v1 = p_start - center
        v2 = p_end - center
        vm = (v1 + v2).normalize() * r
        pm = center + vm
        return Part.Arc(p_start, pm, p_end).toShape()

    e1 = Part.makeLine(p1, p2)
    e2 = make_arc(p2, p3, c1)
    e3 = Part.makeLine(p3, p4)
    e4 = make_arc(p4, p5, c2)
    e5 = Part.makeLine(p5, p6)
    e6 = make_arc(p6, p7, c3)
    e7 = Part.makeLine(p7, p8)
    e8 = make_arc(p8, p1, c4)

    return Part.Wire([e1, e2, e3, e4, e5, e6, e7, e8])

# ==========================================
# 1. GEOMETRY GENERATION
# ==========================================
# A. Flared Base (Loft between two matched 8-edge wires)
w_bottom = make_8edge_wire(base_width, base_width, base_corner_r, z=0.0)
w_top = make_8edge_wire(col_radius * 2.0, col_radius * 2.0, col_radius - 0.01, z=flare_height)
flared_base = Part.makeLoft([w_bottom, w_top], True)

# B. Center Column (Slight overlap at bottom to ensure clean fusion)
column = Part.makeCylinder(col_radius, col_height + 1.0, Vector(0, 0, flare_height - 0.5))

# C. Skådis Top Peg
top_z = flare_height + col_height
w_peg = make_8edge_wire(peg_length, peg_width, (peg_width / 2.0) - 0.01, z=top_z - 0.5)
f_peg = Part.Face(w_peg)
peg_solid = f_peg.extrude(Vector(0, 0, peg_height + 0.5))

# Fuse main shape
main_body = flared_base.fuse(column).fuse(peg_solid)

# ==========================================
# 2. CUTOUTS & HOLES
# ==========================================
total_h = top_z + peg_height + 10.0

# Center Through-Hole
center_hole = Part.makeCylinder(center_hole_dia / 2.0, total_h, Vector(0, 0, -5.0))
main_body = main_body.cut(center_hole)

# Top Counterbore
if counterbore_depth > 0:
    cb = Part.makeCylinder(counterbore_dia / 2.0, counterbore_depth + 1.0, Vector(0, 0, top_z + peg_height - counterbore_depth))
    main_body = main_body.cut(cb)

# Peg Notch / Slot
notch = Part.makeBox(peg_notch_w, peg_width + 10.0, peg_height + 2.0)
notch.translate(Vector(-peg_notch_w / 2.0, -(peg_width + 10.0) / 2.0, top_z + peg_height - 3.0))
main_body = main_body.cut(notch)

# 4x Base Mounting Holes
hole_offsets = [
    Vector(mounting_hole_pos, 0, 0),
    Vector(-mounting_hole_pos, 0, 0),
    Vector(0, mounting_hole_pos, 0),
    Vector(0, -mounting_hole_pos, 0)
]
for pos in hole_offsets:
    h = Part.makeCylinder(mounting_hole_dia / 2.0, flare_height + 10.0, pos + Vector(0, 0, -5.0))
    main_body = main_body.cut(h)

# ==========================================
# 3. RENDER IN FREECAD
# ==========================================
obj = doc.addObject("Part::Feature", "Skadis_Combined_Mount")
obj.Shape = main_body
doc.recompute()

if App.GuiUp:
    import FreeCADGui as Gui
    Gui.SendMsgToActiveView("ViewSelection")