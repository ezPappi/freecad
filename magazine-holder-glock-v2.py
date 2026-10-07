import FreeCAD as App
import Part

# Create a new document
doc = App.newDocument("Skadis_Glock_6Mag_Tray")

# ==========================================
# PARAMETERS (Dimensions in mm - Glock Spec)
# ==========================================
compartment_w = 23.0   # Width for double-stack Glock mags (~22.5mm actual)
num_compartments = 6   # 6 magazine slots
num_dividers = num_compartments - 1

depth = 38.0           # 30mm magazine depth + walls
height = 80.0          # 8 cm back wall height for tray
front_height = 50.0    # 5 cm front lip height (creates the access slant)
wall_thick = 2.5       # Wall thickness
backplate_extra = 20.0 # Extra height on back for Skådis stability
fillet_radius = 3.0    # Radius for outer vertical corners

# Dynamically compute total width based on 6 Glock magazine slots
width = (num_compartments * compartment_w) + ((num_compartments + 1) * wall_thick)
total_height = height + backplate_extra

# ---- Skådis board (IKEA: 5 mm board, 5 x 15 mm slots, 40 mm pitch) ----
board_t = 5.0          # board thickness
board_gap = 0.3        # clearance between board rear face and the hook tab
slot_h = 15.0          # slot height (measured boards are often ~15.2)
peg_pitch = 40.0       # horizontal slot pitch

# ---- Hook geometry (all values are for ONE hook) ----
peg_width = 4.6        # X width; slot is 5.0-5.2, leaves 0.2-0.3 mm per side
stem_h = 7.5           # stem thickness (bending stiffness ~ stem_h^2)
drop = 5.0             # how far the tab reaches below the slot.
                       # Lowered from 6.0: stem_h + drop must clear the 15 mm
                       # slot with some margin (see check below) - at 6.0 the
                       # hook was exactly at the limit, with zero margin for a
                       # tight or slightly undersized real-world slot.
tab_root_t = 5.0       # tab thickness where it joins the stem
tab_tip_t = 5.0        # tab thickness at its tip (uniform, not tapered - thicker/stronger)
lead_chamfer = 0.8     # lead-in chamfer on rear corners so it enters the slot easily
num_pegs = 4           # 4 pegs share the load
edge_margin = 8.0      # minimum distance from the outer pegs to the tray edge
peg_z = total_height - 14.0   # Z of the stem underside

# How far the stem is embedded into the (reinforced) back plate before it
# becomes a free cantilever. Deeper embedment = more glued/fused cross-section
# resisting the root bending load, which is where these hooks actually snap.
anchor_y = 3.0         # was 2.0; header_thick below is 4.0, so this still
                       # leaves 1.0 mm of solid material behind the peg

# Fillet radii at the two spots that concentrate stress in FDM prints:
#  - root_fillet_r: where the peg exits the flat back-plate face (this is
#    where a cantilevered peg carries its maximum bending moment, AND it's a
#    sharp reentrant corner, AND it sits on a single print layer boundary -
#    all three make it the most likely place for a peg to snap clean off)
#  - neck_fillet_r: where the stem meets the drop of the tab (same idea, on
#    the underside where the tab catches the board)
root_fillet_r = 1.5
neck_fillet_r = 1.0

# Breakaway support web: a thin 45-degree web under each tab so the tab prints
# without slicer supports. It sits inside the board thickness, so SNAP IT OFF
# with pliers before hanging the tray.
support_web = True
web_w = 1.0

# Extra thickness of the back plate above the tray (stiffens the hook area)
header_thick = 4.0

# ---- Sanity checks ----
stem_len = board_t + board_gap                  # stem length from tray back to tab
slot_margin = slot_h - 1.5 - (stem_h + drop)
if slot_margin < 0:
    raise ValueError("Hook (stem_h + drop) is too tall to pass through a 15 mm slot")
if (num_pegs - 1) * peg_pitch + peg_width > width - 2 * edge_margin:
    raise ValueError("Too many pegs for this tray width")
if peg_z + stem_h + 3.0 > total_height:
    raise ValueError("Hook sticks out above the back plate")
if anchor_y >= header_thick:
    raise ValueError("anchor_y must stay inside header_thick, or the peg pokes through")
App.Console.PrintMessage("Slot clearance margin: %.2f mm\n" % slot_margin)

# ==========================================
# 1. OUTER TRAY (FILLETED FIRST) & BACKPLATE
# ==========================================
outer_box = Part.makeBox(width, depth, total_height)

outer_vertical_edges = []
for edge in outer_box.Edges:
    v1, v2 = edge.Vertexes[0].Point, edge.Vertexes[1].Point
    if abs(v1.x - v2.x) < 0.001 and abs(v1.y - v2.y) < 0.001:
        outer_vertical_edges.append(edge)

outer_box_filleted = outer_box.makeFillet(fillet_radius, outer_vertical_edges)

inner_w = width - (2 * wall_thick)
inner_d = depth - (2 * wall_thick)
inner_h = height - wall_thick

pocket = Part.makeBox(inner_w, inner_d, inner_h)
pocket.translate(App.Vector(wall_thick, wall_thick, wall_thick))

tray_shell = outer_box_filleted.cut(pocket)

# Cut away everything above the tray except the back plate
back_cut = Part.makeBox(width + 10.0, depth - wall_thick, backplate_extra)
back_cut.translate(App.Vector(-5.0, wall_thick, height))
tray_body = tray_shell.cut(back_cut)

# ==========================================
# 2. CREATE SLANTED FRONT & SIDES
# ==========================================
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
    div = div.cut(slant_cutter)
    dividers.append(div)

for div in dividers:
    tray_body = tray_body.fuse(div)

# ==========================================
# 3b. THICKER BACK PLATE ABOVE THE TRAY (stiffens the hook zone)
# ==========================================
if header_thick > wall_thick:
    header = Part.makeBox(width - 2 * fillet_radius,
                          header_thick - wall_thick + 0.5,   # +0.5 overlaps the plate
                          backplate_extra)
    header.translate(App.Vector(fillet_radius, wall_thick - 0.5, height))
    tray_body = tray_body.fuse(header)

# ==========================================
# 4. REINFORCED SKÅDIS HOOKS
# ==========================================
def yz_prism(points_yz, x0, x_len):
    """Extrude a polygon given as (y, z) points along +X, starting at x0."""
    pts = [App.Vector(x0, y, z) for (y, z) in points_yz]
    pts.append(pts[0])
    f = Part.Face(Part.makePolygon(pts))
    return f.extrude(App.Vector(x_len, 0, 0))


def fillet_edge_at(solid, y_val, radius, tol=0.01):
    """Fillet the edge(s) running along X at a given constant Y (both
    vertices at that Y). Used to round the neck of a single hook before it's
    fused to anything else, where an exact-match edge search is reliable."""
    try:
        edges = []
        for e in solid.Edges:
            v1, v2 = e.Vertexes[0].Point, e.Vertexes[-1].Point
            if abs(v1.y - y_val) < tol and abs(v2.y - y_val) < tol:
                edges.append(e)
        if edges:
            return solid.makeFillet(radius, edges)
    except Exception as err:
        App.Console.PrintWarning("Neck fillet skipped: %s\n" % err)
    return solid


def create_skadis_hook():
    """
    Local origin: x = left edge of hook, y = rear face of the tray (0),
    z = underside of the stem.  The hook extends toward -Y (into the board).

      * stem is 7.5 mm tall, embedded anchor_y=3.0 mm into the header
      * stem length = board thickness + 0.3 mm, so the tab sits right behind
        the board instead of several mm away (no leverage / wobble)
      * tab is a uniform 5 mm thick catch (short and thick: strong, easy print)
      * the neck (where the tab drops away from the stem) gets a small fillet
        - this is a reentrant corner and, in an FDM print, sits on a single
          layer boundary, so a sharp corner there is a natural crack start
    """
    sl = stem_len
    ch = lead_chamfer

    profile = [
        (anchor_y, 0.0),                             # stem underside, inside plate
        (-sl, 0.0),                                  # stem underside at tab front face
        (-sl, -drop),                                # tab front face (bears on board rear)
        (-(sl + tab_tip_t) + ch, -drop),             # tab bottom
        (-(sl + tab_tip_t), -drop + ch),             # lower rear chamfer
        (-(sl + tab_root_t), stem_h - ch),           # rear face of tab
        (-(sl + tab_root_t) + ch, stem_h),           # upper rear chamfer
        (anchor_y, stem_h),                          # stem top, inside plate
    ]
    hook = yz_prism(profile, 0.0, peg_width)
    hook = fillet_edge_at(hook, -sl, neck_fillet_r)

    if support_web:
        # 45-degree breakaway web from the plate up to the tab bottom
        y1, z1 = -sl, -drop + 0.2
        y2, z2 = -(sl + tab_tip_t) + ch, -drop + 0.2
        web_pts = [
            (y1, z1),
            (y2, z2),
            (1.0, z2 - (abs(y2) + 1.0)),
            (1.0, z1 - (abs(y1) + 1.0)),
        ]
        web = yz_prism(web_pts, (peg_width - web_w) / 2.0, web_w)
        hook = hook.fuse(web)

    return hook


# Position hooks on the standard 40 mm Skådis pitch, centered on the tray
start_x = (width - ((num_pegs - 1) * peg_pitch)) / 2.0
peg_x_list = [start_x + (i * peg_pitch) - (peg_width / 2.0) for i in range(num_pegs)]

final_model = tray_body
for p_x in peg_x_list:
    p = create_skadis_hook()
    p.translate(App.Vector(p_x, 0, peg_z))
    final_model = final_model.fuse(p)

# ==========================================
# 4b. FILLET THE PEG ROOTS - the most common real-world break point
# ==========================================
# Each peg meets the flat header face at y=0 as a sharp rectangular step
# (like a boss sticking out of a wall). That step is a stress concentrator,
# and it's also exactly where the peg carries its maximum bending moment as a
# cantilever, so it's the single highest-value place to add a fillet.
try:
    tol = 0.01
    root_edges = []
    for p_x in peg_x_list:
        for e in final_model.Edges:
            bb = e.BoundBox
            if (bb.YMin > -tol and bb.YMax < tol
                    and bb.XMin > p_x - tol and bb.XMax < p_x + peg_width + tol
                    and bb.ZMin > -tol and bb.ZMax < stem_h + tol):
                root_edges.append(e)
    if root_edges:
        final_model = final_model.makeFillet(root_fillet_r, root_edges)
    else:
        App.Console.PrintWarning("No root edges matched - check peg geometry.\n")
except Exception as err:
    App.Console.PrintWarning("Root fillet skipped: %s\n" % err)

# ==========================================
# 5. RENDER TO WORKSPACE
# ==========================================
part_obj = doc.addObject("Part::Feature", "Skadis_Glock_6Mag_Tray")
part_obj.Shape = final_model

doc.recompute()
if App.GuiUp:
    import FreeCADGui
    FreeCADGui.SendMsgToActiveView("ViewFit")