import FreeCAD as App
import Part
from FreeCAD import Vector

# 1. Opprett eller hent aktivt dokument
doc = App.activeDocument()
if not doc:
    doc = App.newDocument("Glock_Mag_Skadis_5Slot")

# ==========================================
# PARAMETRE (Opprinnelig design - 5 plasser)
# ==========================================
num_slots = 5             # 5 magasinplasser
slot_width = 25.5         # Glock double-stack bredde (mm)
divider_thickness = 7.0   # Skilleveggtykkelse (mm)
rack_depth = 38.0         # Dybde på veggene (mm)
rack_height = 55.0        # Høyde på bakplaten (mm)
back_thickness = 6.0      # Tykkelse på bakplaten (mm)

# Skådis-spesifikasjon & Krok-parametre fra ny krok-kode
board_t = 5.0          # Skådis platetykkelse
board_gap = 0.3        # Klaring
peg_width = 4.6        # X-bredde på kroken
stem_h = 5.5           # Høyde på stilken
drop = 4.8             # Låsetapp-lengde nedover
tab_root_t = 5.0       # Tapered rot
tab_tip_t = 5.0        # Tapered spiss
lead_chamfer = 2.5     # Fasing
num_pegs = 3           # 3 kroker fordelt på 40mm pitch
peg_pitch = 40.0       # Skådis modulavstand

total_width = (num_slots * slot_width) + ((num_slots + 1) * divider_thickness)
stem_len = board_t + board_gap
peg_z = rack_height - 14.0

shapes = []

# ==========================================
# 1. OPPRINNELIG BAKPLATE
# ==========================================
back_plate = Part.makeBox(total_width, back_thickness, rack_height)
shapes.append(back_plate)

# ==========================================
# 2. OPPRINNELIGE SKILLEVEGGER MED SPOR
# ==========================================
for i in range(num_slots + 1):
    x_pos = i * (slot_width + divider_thickness)
    div = Part.makeBox(divider_thickness, rack_depth, rack_height)
    div.translate(Vector(x_pos, back_thickness, 0))
    
    # Rille/spor i midten av de indre skilleveggene (som på bildet)
    if 0 < i < num_slots:
        slot_cut = Part.makeBox(1.5, rack_depth + 2.0, rack_height + 2.0)
        slot_cut.translate(Vector(x_pos + (divider_thickness / 2.0) - 0.75, back_thickness - 1.0, -1.0))
        div = div.cut(slot_cut)
        
    shapes.append(div)

# ==========================================
# 3. KROKER BUBGET MED DEN NYE PROFIL-FUNKSJONEN
# ==========================================
def yz_prism(points_yz, x0, x_len):
    """Extrude a polygon given as (y, z) points along +X, starting at x0."""
    pts = [Vector(x0, y, z) for (y, z) in points_yz]
    pts.append(pts[0])
    f = Part.Face(Part.makePolygon(pts))
    return f.extrude(Vector(x_len, 0, 0))

def create_skadis_hook():
    anchor_y = 2.0  # Går inn i bakplaten for solid fusjon
    sl = stem_len
    ch = lead_chamfer

    profile = [
        (anchor_y, 0.0),                             # Stilken under, inne i platen
        (-sl, 0.0),                                  # Stilken under ved brettets baksid
        (-sl, -drop),                                # Låseleppen nedover
        (-(sl + tab_tip_t) + ch, -drop),             # Bakkant under
        (-(sl + tab_tip_t), -drop + ch),             # Nederste fasing
        (-(sl + tab_root_t), stem_h - ch),           # Tapered bakside
        (-(sl + tab_root_t) + ch, stem_h),           # Øverste fasing
        (anchor_y, stem_h),                          # Stilk topp, inne i platen
    ]
    return yz_prism(profile, 0.0, peg_width)

# Sentrer krokene med 40 mm Skådis-pitch over totalbredden
start_x = (total_width - ((num_pegs - 1) * peg_pitch)) / 2.0

for i in range(num_pegs):
    p = create_skadis_hook()
    p_x = start_x + (i * peg_pitch) - (peg_width / 2.0)
    p.translate(Vector(p_x, 0, peg_z))
    shapes.append(p)

# ==========================================
# 4. SAMMENSMELTING OG SENTRERING
# ==========================================
final_shape = shapes[0]
for s in shapes[1:]:
    final_shape = final_shape.fuse(s)

# Sentrer geometrien om origo (X-akse)
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