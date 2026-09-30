import math
import FreeCAD as App
import Part
from FreeCAD import Vector

doc = App.activeDocument()
if not doc:
    doc = App.newDocument("Skadis_Combined_Mount")

# ==========================================
# SCREW PARAMETERS
# ==========================================
# 4x Corner Screws (fits 2.5 mm holes)
corner_screw_dia = 2.4        # Outer thread diameter
corner_screw_pitch = 0.8      # Printable pitch
corner_screw_length = 8.0     # Thread shank length
corner_head_width = 5.0       # External hex width across flats
corner_head_h = 3.0           # Head height

# 1x Center Screw (fits 4.5 mm hole)
center_screw_dia = 4.3        # Outer thread diameter
center_screw_pitch = 1.0      # Printable pitch
center_screw_length = 9.5     # Thread shank length
center_head_width = 12.0      # External hex width across flats
center_head_h = 3.5           # Head height

# Hole positions from your model
mounting_hole_pos = 16.0
corner_positions = [
    Vector(mounting_hole_pos, 0, 0),
    Vector(-mounting_hole_pos, 0, 0),
    Vector(0, mounting_hole_pos, 0),
    Vector(0, -mounting_hole_pos, 0)
]

# ==========================================
# HELPER: ROBUST PLASTIC SCREW GENERATOR
# ==========================================
def make_robust_plastic_screw(outer_dia, pitch, length, head_w, head_h):
    """Generates a screw with external hex head, finger grip flutes, and a flathead slot."""
    thread_depth = pitch * 0.4
    core_rad = (outer_dia / 2.0) - thread_depth
    head_rad = head_w / (2.0 * math.cos(math.radians(30)))  # Outer radius for external hex
    
    # 1. External Hex Head
    hex_pts = [
        Vector(head_rad * math.cos(math.radians(a)), head_rad * math.sin(math.radians(a)), 0)
        for a in range(0, 360, 60)
    ]
    hex_pts.append(hex_pts[0])
    hex_wire = Part.makePolygon(hex_pts)
    head_face = Part.Face(hex_wire)
    head = head_face.extrude(Vector(0, 0, head_h))

    # Add flathead screwdriver slot across the top
    slot_w = max(1.2, outer_dia * 0.3)
    slot_d = head_h * 0.5
    slot_box = Part.makeBox(head_rad * 2.5, slot_w, slot_d)
    slot_box.translate(Vector(-head_rad * 1.25, -slot_w / 2.0, head_h - slot_d))
    head = head.cut(slot_box)

    # 2. Screw Shank Core
    core = Part.makeCylinder(core_rad, length, Vector(0, 0, -length), Vector(0, 0, 1))
    
    # 3. Stacked 45° Thread Ridges
    num_threads = int(length / pitch)
    thread_shapes = []
    
    for i in range(num_threads):
        z_pos = -length + (i * pitch)
        c1 = Part.makeCone(core_rad, outer_dia / 2.0, pitch / 2.0, Vector(0, 0, z_pos), Vector(0, 0, 1))
        c2 = Part.makeCone(outer_dia / 2.0, core_rad, pitch / 2.0, Vector(0, 0, z_pos + pitch / 2.0), Vector(0, 0, 1))
        thread_shapes.append(c1.fuse(c2))

    threaded_shank = core
    for t in thread_shapes:
        threaded_shank = threaded_shank.fuse(t)

    # Fuse Head and Shank
    screw = head.fuse(threaded_shank)
    return screw

# ==========================================
# GENERATE AND PLACE SCREWS
# ==========================================
# Create 4x Corner Screws
for idx, pos in enumerate(corner_positions):
    c_screw = make_robust_plastic_screw(
        corner_screw_dia,
        corner_screw_pitch,
        corner_screw_length,
        corner_head_width,
        corner_head_h
    )
    c_screw.translate(pos + Vector(0, 0, 3.0))
    
    obj = doc.addObject("Part::Feature", f"Corner_Screw_{idx+1}")
    obj.Shape = c_screw

# Create 1x Center Screw
center_screw = make_robust_plastic_screw(
    center_screw_dia,
    center_screw_pitch,
    center_screw_length,
    center_head_width,
    center_head_h
)
center_screw.translate(Vector(0, 0, 10.2))

obj_center = doc.addObject("Part::Feature", "Center_Screw_M4")
obj_center.Shape = center_screw

doc.recompute()

if App.GuiUp:
    import FreeCADGui as Gui
    Gui.SendMsgToActiveView("ViewSelection")