import math
import FreeCAD as App
import Part
from FreeCAD import Vector

doc = App.activeDocument()
if not doc:
    doc = App.newDocument("Skadis_Combined_Mount")

# ==========================================
# SCREW PARAMETERS (Matched to your model)
# ==========================================
# 4x Base Corner Screws (fits 2.5 mm holes)
corner_screw_dia = 2.4        # Outer thread diameter (0.1 mm clearance for Ø2.5mm hole)
corner_screw_pitch = 0.8      # Coarse printable pitch
corner_screw_length = 8.0     # Thread shank length
corner_head_dia = 4.5         # Head diameter
corner_head_h = 2.2           # Head height
corner_hex_size = 2.0         # Allen key drive size (2.0 mm hex)

# 1x Center Screw (fits 4.5 mm hole)
center_screw_dia = 4.3        # Outer thread diameter (0.2 mm clearance for Ø4.5mm hole)
center_screw_pitch = 1.0      # Coarse printable pitch
center_screw_length = 10.3    # Thread shank length
center_head_dia = 7.5         # Head diameter
center_head_h = 3.0           # Head height
center_hex_size = 3.0         # Allen key drive size (3.0 mm hex)

# Hole positions from your model
mounting_hole_pos = 16.0
corner_positions = [
    Vector(mounting_hole_pos, 0, 0),
    Vector(-mounting_hole_pos, 0, 0),
    Vector(0, mounting_hole_pos, 0),
    Vector(0, -mounting_hole_pos, 0)
]

# ==========================================
# HELPER: GENERATE PRINTABLE THREADED SCREW
# ==========================================
def make_printable_screw(outer_dia, pitch, length, head_dia, head_h, hex_size):
    """Generates a 3D printable screw with 45-degree threads and a hex socket head."""
    thread_depth = pitch * 0.4
    core_rad = (outer_dia / 2.0) - thread_depth
    
    # 1. Main Head Cylinder
    head = Part.makeCylinder(head_dia / 2.0, head_h, Vector(0,0,0), Vector(0,0,1))
    
    # Cut Hex Drive Socket in Head
    hex_wire = Part.makePolygon([
        Vector(hex_size/2.0 * math.cos(math.radians(a)), hex_size/2.0 * math.sin(math.radians(a)), head_h)
        for a in range(0, 360, 60)
    ] + [Vector(hex_size/2.0, 0, head_h)])
    hex_face = Part.Face(hex_wire)
    hex_cut = hex_face.extrude(Vector(0, 0, -head_h * 0.75))
    head = head.cut(hex_cut)

    # 2. Screw Shank Core
    core = Part.makeCylinder(core_rad, length, Vector(0,0,-length), Vector(0,0,1))
    
    # 3. Stacked 45° Thread Ridges
    num_threads = int(length / pitch)
    thread_shapes = []
    
    for i in range(num_threads):
        z_pos = -length + (i * pitch)
        
        # Conical ridge bottom half
        c1 = Part.makeCone(core_rad, outer_dia / 2.0, pitch / 2.0, Vector(0, 0, z_pos), Vector(0, 0, 1))
        # Conical ridge top half
        c2 = Part.makeCone(outer_dia / 2.0, core_rad, pitch / 2.0, Vector(0, 0, z_pos + pitch / 2.0), Vector(0, 0, 1))
        
        ridge = c1.fuse(c2)
        thread_shapes.append(ridge)

    # Fuse all thread ridges onto the core shank
    threaded_shank = core
    for t in thread_shapes:
        threaded_shank = threaded_shank.fuse(t)

    # Fuse Head and Shank into single Solid
    screw = head.fuse(threaded_shank)
    return screw

# ==========================================
# GENERATE AND PLACE SCREWS
# ==========================================
# Create 4x Corner Screws
for idx, pos in enumerate(corner_positions):
    c_screw = make_printable_screw(
        corner_screw_dia,
        corner_screw_pitch,
        corner_screw_length,
        corner_head_dia,
        corner_head_h,
        corner_hex_size
    )
    # Position screw aligned with base hole top surface (z = flare_height)
    c_screw.translate(pos + Vector(0, 0, 3.0))
    
    obj = doc.addObject("Part::Feature", f"Corner_Screw_{idx+1}")
    obj.Shape = c_screw

# Create 1x Center Screw
center_screw = make_printable_screw(
    center_screw_dia,
    center_screw_pitch,
    center_screw_length,
    center_head_dia,
    center_head_h,
    center_hex_size
)
# Position center screw at top peg recess level (z = 10.2 mm)
center_screw.translate(Vector(0, 0, 10.2))

obj_center = doc.addObject("Part::Feature", "Center_Screw_M4")
obj_center.Shape = center_screw

doc.recompute()

if App.GuiUp:
    import FreeCADGui as Gui
    Gui.SendMsgToActiveView("ViewSelection")