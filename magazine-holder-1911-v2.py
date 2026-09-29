import FreeCAD as App
import Part

# Create a new document
doc = App.newDocument("Skadis_1911_Magazine_Tray")

# ==========================================
# PARAMETERS (Dimensions in mm)
# ==========================================
compartment_w = 14.0   # Fixed width for 1911 magazines
num_compartments = 6   # Number of slots desired
num_dividers = num_compartments - 1

depth = 40.0           # 4.0 cm
height = 70.0          # 7 cm back wall height for tray
front_height = 55.0    # Front lip height (creates the slant)
wall_thick = 2.0       # Wall thickness
backplate_extra = 20.0 # Extra height on back for stability
fillet_radius = 3.0    # Radius for outer vertical corners

# Dynamically compute total width
width = (num_compartments * compartment_w) + ((num_compartments + 1) * wall_thick)

# Skådis Peg Parameters (Reinforced Break-Resistant Geometry)
peg_spacing = 40.0     # 40mm between hole centers
peg_width = 4.5        # Reinforced thickness (fits 5.0mm slot)
peg_depth = 10.0       # Depth into board
peg_drop = 9.0         # Locking tab drop length

total_height = height + backplate_extra

# ==========================================
# 1. OUTER TRAY (FILLETED FIRST) & BACKPLATE
# ==========================================
# Main outer block
outer_box = Part.makeBox(width, depth, total_height)

# --- APPLY FILLET TO OUTER VERTICAL EDGES FIRST ---
outer_vertical_edges = []
for edge in outer_box.Edges:
    v1, v2 = edge.Vertexes[0].Point, edge.Vertexes[1].Point
    # Identify vertical edges along Z-axis
    if abs(v1.x - v2.x) < 0.001 and abs(v1.y - v2.y) < 0.001:
        outer_vertical_edges.append(edge)

outer_box_filleted = outer_box.makeFillet(fillet_radius, outer_vertical_edges)

# Inner pocket cut-out
inner_w = width - (2 * wall_thick)
inner_d = depth - (2 * wall_thick)
inner_h = height - wall_thick

pocket = Part.makeBox(inner_w, inner_d, inner_h)
pocket.translate(App.Vector(wall_thick, wall_thick, wall_thick))

# Hollow tray body from filleted block
tray_shell = outer_box_filleted.cut(pocket)

# Cut back top plate height on sides to expose backplate
back_cut = Part.makeBox(width + 10.0, depth - wall_thick, backplate_extra)
back_cut.translate(App.Vector(-5.0, wall_thick, height))
tray_body = tray_shell.cut(back_cut)

# ==========================================
# 2. CREATE SLANTED FRONT & SIDES
# ==========================================
# Create angled cutting tool using a polygon wire extrude
p1 = App.Vector(-5.0, wall_thick, height)
p2 = App.Vector(-5.0, depth + 5.0, height)
p3 = App.Vector(-5.0, depth + 5.0, front_height)
wire = Part.makePolygon([p1, p2, p3, p1])
face = Part.Face(wire)
slant_cutter = face.extrude(App.Vector(width + 10.0, 0, 0))

tray_body = tray_body.cut(slant_cutter)

# ==========================================
# 3. INTERNAL DIVIDER WALLS
# ==========================================
dividers = []
for i in range(1, num_dividers + 1):
    div_x = wall_thick + (i * compartment_w) + ((i - 1) * wall_thick)
    div = Part.makeBox(wall_thick, inner_d, inner_h)
    div.translate(App.Vector(div_x, wall_thick, wall_thick))
    # Apply slant cut to dividers as well
    div = div.cut(slant_cutter)
    dividers.append(div)

for div in dividers:
    tray_body = tray_body.fuse(div)

# ==========================================
# 4. HEAVY-DUTY REINFORCED SKÅDIS HOOKS
# ==========================================
def create_reinforced_skadis_hook():
    """
    Generates a high-strength Skådis hook with:
    1. A 45-degree self-supporting drop wedge (requires NO supports).
    2. A neck reinforcement gusset under the stem to resist shearing.
    """
    stem_h = 5.0
    
    # Horizontal stem protruding backward
    stem = Part.makeBox(peg_width, peg_depth + wall_thick, stem_h)
    stem.translate(App.Vector(0, -(peg_depth + wall_thick), 0))
    
    # 45-degree self-supporting drop wedge tab
    p1 = App.Vector(0, -(peg_depth + wall_thick), stem_h)
    p2 = App.Vector(0, -peg_depth, stem_h)
    p3 = App.Vector(0, -peg_depth, -peg_drop)
    p4 = App.Vector(0, -(peg_depth + wall_thick), -peg_drop + (wall_thick * 1.2)) # 45deg self-supporting angle
    
    w_pts = [p1, p2, p3, p4, p1]
    tab_wire = Part.makePolygon(w_pts)
    tab_face = Part.Face(tab_wire)
    tab_solid = tab_face.extrude(App.Vector(peg_width, 0, 0))
    
    # Lower neck support gusset (triangular fillet under hook to prevent snapping)
    g1 = App.Vector(0, 0, 0)
    g2 = App.Vector(0, -4.0, 0)
    g3 = App.Vector(0, 0, -4.0)
    gusset_wire = Part.makePolygon([g1, g2, g3, g1])
    gusset_face = Part.Face(gusset_wire)
    gusset_solid = gusset_face.extrude(App.Vector(peg_width, 0, 0))
    
    return stem.fuse(tab_solid).fuse(gusset_solid)

# Position hooks matching standard Skådis 40mm grid spacing
num_pegs = max(2, int(width // peg_spacing))
start_x = (width - ((num_pegs - 1) * peg_spacing)) / 2.0
peg_z = total_height - 14.0

pegs = []
for i in range(num_pegs):
    p = create_reinforced_skadis_hook()
    p_x = start_x + (i * peg_spacing) - (peg_width / 2.0)
    p.translate(App.Vector(p_x, 0, peg_z))
    pegs.append(p)

final_model = tray_body
for p in pegs:
    final_model = final_model.fuse(p)

# ==========================================
# 5. RENDER TO FREECAD WORKSPACE
# ==========================================
part_obj = doc.addObject("Part::Feature", "Skadis_1911_Tray")
part_obj.Shape = final_model

doc.recompute()
App.Gui.SendMsgToActiveView("ViewFit")