import math
import FreeCAD as App
import Part
from FreeCAD import Vector

# 1. Opprett eller hent aktivt dokument
doc = App.activeDocument()
if not doc:
    doc = App.newDocument("Glock_Mag_Skadis_5Slot")

# ==========================================
# PARAMETRE
# ==========================================
num_slots = 5             # 5 magasinplasser
slot_width = 25.5         # Glock double-stack bredde (mm)
divider_thickness = 7.0   # Skilleveggtykkelse / bladbredde (mm)
rack_depth = 38.0         # Dybde på veggene/bladene (mm)
rack_height = 55.0        # Høyde på bakplaten (mm)
back_thickness = 6.0      # Tykkelse på bakplaten (mm)

# Skådis-spesifikasjon & Krok-parametre
board_t = 5.0          # Skådis platetykkelse
board_gap = 0.3        # Klaring
peg_width = 4.6        # X-bredde på kroken
stem_h = 5.5           # Høyde på stilken
drop = 4.8             # Låsetapp-lengde nedover
tab_root_t = 5.0       # Tapered rot
tab_tip_t = 5.0        # Tapered spiss
lead_chamfer = 2.5     # Fasing
num_pegs = 3           # 3 kroker
peg_pitch = 40.0       # Skådis modulavstand

# Blad-vinkel og geometri
blade_tilt_deg = 8.0   # Vipp på blader (grader)

# Trakt i endene av bladene (Går fra toppen til bunnen i full høyde)
flare_extra_x = 2.0        # Hvor mye bredere trakten er i fronten per side (mm)
flare_depth = 15.0         # Hvor langt bakover langs bladet trakten strekker seg (Y-retning, mm)
front_edge_fillet_r = 2.0  # Radius for avrunding av fremre ytterkanter på trakten/bladene (mm)

# Avrunding på bakplate
edge_fillet_r = 1.2        # Fillet på bakplaten

total_width = (num_slots * slot_width) + ((num_slots + 1) * divider_thickness)
stem_len = board_t + board_gap
peg_z = rack_height - 14.0

shapes = []

def vertical_edges(solid, tol=0.01):
    """Finner vertikale kanter langs Z."""
    edges = []
    for e in solid.Edges:
        v1, v2 = e.Vertexes[0].Point, e.Vertexes[-1].Point
        if abs(v1.x - v2.x) < tol and abs(v1.y - v2.y) < tol and abs(v1.z - v2.z) > tol:
            edges.append(e)
    return edges

def fillet_box_corners(box_shape, width, depth, radius):
    """Runder vertikale hjørner på enkle bokser før fusion."""
    r = min(radius, width / 2.0 - 0.3, depth / 2.0 - 0.3)
    if r <= 0.05:
        return box_shape
    edges = vertical_edges(box_shape)
    if not edges:
        return box_shape
    try:
        return box_shape.makeFillet(r, edges)
    except Exception as err:
        App.Console.PrintWarning("Hjørne-avrunding hoppet over: %s\n" % err)
        return box_shape

# ==========================================
# 1. BAKPLATE
# ==========================================
back_plate = Part.makeBox(total_width, back_thickness, rack_height)
back_plate = fillet_box_corners(back_plate, total_width, back_thickness, edge_fillet_r)
shapes.append(back_plate)

# ==========================================
# 2. BLADER MED FULL-HØYDE TRAKT OG AVRUNDEDE YTTERKANTER
# ==========================================
tilt_rad = math.radians(blade_tilt_deg)
wedge_extra_y = (rack_height * math.tan(tilt_rad)) + 5.0  

# Kutteboks for å renskjære alt som måtte stikke ut BAK bakplaten (Y < 0)
rear_cutter = Part.makeBox(total_width + 20.0, wedge_extra_y + 20.0, rack_height + 40.0)
rear_cutter.translate(Vector(-10.0, -(wedge_extra_y + 20.0), -20.0))

def create_flared_blade_solid(x_pos, is_leftmost, is_rightmost):
    """Bygger 2D-profilen av et blad med traktutvidelse i fronten og ekstruderer fra topp til bunn."""
    y_back = back_thickness
    y_front = back_thickness + rack_depth
    y_flare = y_front - flare_depth

    x_l_back = x_pos
    x_r_back = x_pos + divider_thickness

    # Trakt-utvidelse retning
    flare_l = 0.0 if is_leftmost else flare_extra_x
    flare_r = 0.0 if is_rightmost else flare_extra_x

    x_l_front = x_l_back - flare_l
    x_r_front = x_r_back + flare_r

    # Definer 2D-hjørnepunkter (XY-plan)
    pts = [
        Vector(x_l_back, y_back, 0),
        Vector(x_r_back, y_back, 0),
        Vector(x_r_back, y_flare, 0),
        Vector(x_r_front, y_front, 0),
        Vector(x_l_front, y_front, 0),
        Vector(x_l_back, y_flare, 0),
        Vector(x_l_back, y_back, 0)
    ]

    # Fjern dupliserte/kolineære punkter dersom flare_l eller flare_r er 0
    clean_pts = [pts[0]]
    for p in pts[1:]:
        if (p - clean_pts[-1]).Length > 0.001:
            clean_pts.append(p)

    poly = Part.makePolygon(clean_pts)

    # 2D-avrunding av ytterkantene i fronten og overgangene
    if front_edge_fillet_r > 0.05:
        target_edges = []
        for e in poly.Edges:
            v1, v2 = e.Vertexes[0].Point, e.Vertexes[-1].Point
            # Velg kanter som ligger i fremre del av bladet (fra flare-start og fremover)
            if v1.y > y_flare - 0.1 or v2.y > y_flare - 0.1:
                target_edges.append(e)

        if target_edges:
            try:
                max_r = min(front_edge_fillet_r, flare_depth * 0.4, (divider_thickness + flare_l + flare_r) * 0.4)
                poly = poly.makeFillet(max_r, target_edges)
            except Exception as err:
                App.Console.PrintWarning("2D Fillet hoppet over: %s\n" % err)

    face = Part.Face(poly)
    # Ekstruder i full høyde fra bunn til topp (Z = 0 til Z = rack_height)
    return face.extrude(Vector(0, 0, rack_height))

for i in range(num_slots + 1):
    x_pos = i * (slot_width + divider_thickness)
    is_interior = 0 < i < num_slots

    # --- 2a. Ekstrudert blad med full-høyde trakt og avrunding ---
    blade = create_flared_blade_solid(x_pos, is_leftmost=(i == 0), is_rightmost=(i == num_slots))

    # --- 2b. Tett gapet nede mot bakplaten (Kile/Filler) ---
    wedge = Part.makeBox(divider_thickness, wedge_extra_y, rack_height)
    wedge.translate(Vector(x_pos, back_thickness - wedge_extra_y, 0))
    blade = blade.fuse(wedge)

    # --- 2c. CSG-renskjæring av ytterste vertikale front-hjørner ---
    if front_edge_fillet_r > 0.05:
        r = min(front_edge_fillet_r, (divider_thickness / 2.0) - 0.1)
        h_cut = rack_height + 40.0
        front_y = back_thickness + rack_depth

        box_l = Part.makeBox(r, r, h_cut)
        box_l.translate(Vector(x_pos - (flare_extra_x if i > 0 else 0), front_y - r, -20.0))
        cyl_l = Part.makeCylinder(r, h_cut, Vector(x_pos - (flare_extra_x if i > 0 else 0) + r, front_y - r, -20.0), Vector(0, 0, 1))
        cutter_l = box_l.cut(cyl_l)

        box_r = Part.makeBox(r, r, h_cut)
        box_r.translate(Vector(x_pos + divider_thickness + (flare_extra_x if i < num_slots else 0) - r, front_y - r, -20.0))
        cyl_r = Part.makeCylinder(r, h_cut, Vector(x_pos + divider_thickness + (flare_extra_x if i < num_slots else 0) - r, front_y - r, -20.0), Vector(0, 0, 1))
        cutter_r = box_r.cut(cyl_r)

        blade = blade.cut(cutter_l).cut(cutter_r)

    # --- 2d. Rille/spor i midten av de indre skilleveggene ---
    if is_interior:
        slot_cut = Part.makeBox(1.5, rack_depth + wedge_extra_y + 10.0, rack_height + 10.0)
        slot_cut.translate(Vector(x_pos + (divider_thickness / 2.0) - 0.75, back_thickness - wedge_extra_y - 2.0, -5.0))
        blade = blade.cut(slot_cut)

    # --- 2e. Vinkling/Vipp av HELE bladet om bakplatens toppkant ---
    if blade_tilt_deg:
        blade.rotate(Vector(0, back_thickness, rack_height), Vector(1, 0, 0), blade_tilt_deg)

    # --- 2f. RENKSJÆRING: Kutt bort alt som stikker ut bak bakplaten (Y < 0) ---
    blade = blade.cut(rear_cutter)

    shapes.append(blade)

# ==========================================
# 3. SKÅDIS-KROKER
# ==========================================
def yz_prism(points_yz, x0, x_len):
    pts = [Vector(x0, y, z) for (y, z) in points_yz]
    pts.append(pts[0])
    f = Part.Face(Part.makePolygon(pts))
    return f.extrude(Vector(x_len, 0, 0))

def create_skadis_hook():
    anchor_y = 2.0
    sl = stem_len
    ch = lead_chamfer

    profile = [
        (anchor_y, 0.0),
        (-sl, 0.0),
        (-sl, -drop),
        (-(sl + tab_tip_t) + ch, -drop),
        (-(sl + tab_tip_t), -drop + ch),
        (-(sl + tab_root_t), stem_h - ch),
        (-(sl + tab_root_t) + ch, stem_h),
        (anchor_y, stem_h),
    ]
    return yz_prism(profile, 0.0, peg_width)

start_x = (total_width - ((num_pegs - 1) * peg_pitch)) / 2.0

for i in range(num_pegs):
    p = create_skadis_hook()
    p_x = start_x + (i * peg_pitch) - (peg_width / 2.0)
    p.translate(Vector(p_x, 0, peg_z))
    shapes.append(p)

# ==========================================
# 4. SAMMENSMELTING OG SENTRERING
# ==========================================
App.Console.PrintMessage("Fuser %d deler...\n" % len(shapes))
final_shape = shapes[0]
for s in shapes[1:]:
    final_shape = final_shape.fuse(s)

final_shape.translate(Vector(-total_width / 2.0, 0, 0))

# ==========================================
# 5. GENERER I FREECAD
# ==========================================
obj = doc.addObject("Part::Feature", "GlockMagSkadisRack_CustomHooks")
obj.Shape = final_shape
doc.recompute()

if App.GuiUp:
    import FreeCADGui as Gui
    Gui.SendMsgToActiveView("ViewSelection")