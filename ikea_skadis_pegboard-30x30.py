import FreeCAD as App
import Part

# Create a new document
doc = App.newDocument("Custom_Skadis_Lightweight")

# ==========================================
# PARAMETERS (Dimensions in mm)
# ==========================================
width = 300.0          # 30 cm wide
height = 300.0         # 30 cm high
total_thickness = 5.0  # Overall thickness for Skådis hooks
face_thickness = 1.6   # Front skin thickness (approx 4-5 top layers)
chamfer_size = 1.0     # Outer front edge chamfer

# Structural Rib Parameters
rib_thickness = 2.0    # Thickness of structural wall ribs around holes & perimeter
rib_depth = total_thickness - face_thickness # Depth of backside hollow pockets (3.4mm)

# Skådis Hole Geometry Specs
hole_width = 5.0       # Slot width
hole_length = 15.0     # Slot vertical length
hole_radius = hole_width / 2.0
spacing = 40.0         # Grid spacing
min_margin = 10.0      # Minimum edge margin

# ==========================================
# 1. BASE SOLID & HOLLOW POCKET CREATION
# ==========================================
# Main outer slab
outer_board = Part.makeBox(width, height, total_thickness)

# Backside hollow pocket cutter (recessed inside outer frame)
pocket_width = width - (2 * rib_thickness)
pocket_height = height - (2 * rib_thickness)
pocket_cutter = Part.makeBox(pocket_width, pocket_height, rib_depth + 0.1)
pocket_cutter.translate(App.Vector(rib_thickness, rib_thickness, -0.05))

# Shell board with outer perimeter rim
shelled_board = outer_board.cut(pocket_cutter)

# Apply front edge chamfer
front_edges = []
for edge in shelled_board.Edges:
    v1, v2 = edge.Vertexes[0].Point, edge.Vertexes[1].Point
    if abs(v1.z - total_thickness) < 0.001 and abs(v2.z - total_thickness) < 0.001:
        front_edges.append(edge)

if front_edges:
    try:
        shelled_board = shelled_board.makeChamfer(chamfer_size, front_edges)
    except Exception:
        pass

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def create_skadis_slot(x_center, y_center):
    """Generates a through-hole slot cutter at (x, y)."""
    straight_len = hole_length - hole_width
    half_straight = straight_len / 2.0

    center_box = Part.makeBox(hole_width, straight_len, total_thickness + 4.0)
    center_box.translate(App.Vector(x_center - hole_radius, y_center - half_straight, -2.0))

    top_cyl = Part.makeCylinder(hole_radius, total_thickness + 4.0, App.Vector(x_center, y_center + half_straight, -2.0))
    bot_cyl = Part.makeCylinder(hole_radius, total_thickness + 4.0, App.Vector(x_center, y_center - half_straight, -2.0))

    return center_box.fuse(top_cyl).fuse(bot_cyl)

def create_slot_boss_rib(x_center, y_center):
    """Creates a raised boss/wall around each slot to maintain 5mm hook depth."""
    boss_width = hole_width + (2 * rib_thickness)
    boss_radius = boss_width / 2.0
    straight_len = hole_length - hole_width
    half_straight = straight_len / 2.0

    center_box = Part.makeBox(boss_width, straight_len, rib_depth)
    center_box.translate(App.Vector(x_center - boss_radius, y_center - half_straight, 0))

    top_cyl = Part.makeCylinder(boss_radius, rib_depth, App.Vector(x_center, y_center + half_straight, 0))
    bot_cyl = Part.makeCylinder(boss_radius, rib_depth, App.Vector(x_center, y_center - half_straight, 0))

    return center_box.fuse(top_cyl).fuse(bot_cyl)

# ==========================================
# 3. GRID POSITIONS
# ==========================================
num_cols = int((width - (2 * min_margin)) // spacing) + 1
num_rows = int((height - (2 * min_margin)) // spacing) + 1

start_x = (width - ((num_cols - 1) * spacing)) / 2.0
start_y = (height - ((num_rows - 1) * spacing)) / 2.0

slot_positions = []

# Main grid
for c in range(num_cols):
    for r in range(num_rows):
        slot_positions.append((start_x + (c * spacing), start_y + (r * spacing)))

# Staggered grid
stagger_start_y = start_y + (spacing / 2.0)
stagger_num_rows = num_rows - 1
potential_stagger_x = [start_x - (spacing / 2.0)] + [start_x + (c * spacing) + (spacing / 2.0) for c in range(num_cols)]

for sx in potential_stagger_x:
    if min_margin <= sx <= (width - min_margin):
        for r in range(stagger_num_rows):
            slot_positions.append((sx, stagger_start_y + (r * spacing)))

# ==========================================
# 4. BUILD RIBS & CUT HOLES
# ==========================================
boss_ribs = []
slot_cutters = []

for cx, cy in slot_positions:
    boss_ribs.append(create_slot_boss_rib(cx, cy))
    slot_cutters.append(create_skadis_slot(cx, cy))

# Fuse all slot support bosses onto the shelled board
if boss_ribs:
    all_bosses = Part.makeCompound(boss_ribs)
    shelled_board = shelled_board.fuse(all_bosses)

# Cut through-holes for all slots
compound_cutters = Part.makeCompound(slot_cutters)
final_pegboard = shelled_board.cut(compound_cutters)

# ==========================================
# 5. RENDER TO WORKSPACE
# ==========================================
part_obj = doc.addObject("Part::Feature", "Custom_Skadis_Lightweight")
part_obj.Shape = final_pegboard

doc.recompute()
App.Gui.SendMsgToActiveView("ViewFit")