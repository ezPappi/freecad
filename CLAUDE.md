# CLAUDE.md

This repo is a collection of standalone FreeCAD 1.x Python macros. Each one builds a single 3D-printable part, mostly firearm accessories and IKEA Skådis pegboard parts. There is no package, no build system, no tests and no dependencies beyond FreeCAD's bundled modules (`FreeCAD`, `Part`, `Mesh`, `FreeCADGui`).

## Running

Run a script inside FreeCAD, either with **Macro > Macros… > Execute** or by pasting it into the Python console. To build headless (no GUI; every script guards its GUI calls):

```sh
freecadcmd grip-hammerli-208.py
```

Each run creates a new document with `App.newDocument(...)`. A few scripts (`magazine_holder_glock_open.py`, `skadis_*.py`) reuse `App.activeDocument()` if one is open. Results such as validity, volume, bounding box and "NEXT: measure…" hints go to the Report view through `App.Console.Print*`.

To check a change, run the script and confirm that `Shape.isValid()` is reported True and that the volume and dimensions look sensible. FreeCAD is installed as the flatpak `org.freecad.FreeCAD`. The wrappers `~/.local/bin/freecad` (GUI) and `~/.local/bin/freecadcmd` (headless) call `flatpak run [--command=freecadcmd] org.freecad.FreeCAD "$@"`. Claude Code's shell may or may not run inside a flatpak sandbox (it does when launched from the VS Code flatpak). The wrappers handle both cases: when `/.flatpak-info` exists they go through `flatpak-spawn --host`, otherwise they call `flatpak run` directly. Either way `freecadcmd <script>.py` works from here (verified with FreeCAD 1.1.4). Run a script after you change it. `try_op` warnings such as a skipped fillet are expected and don't mean the build failed.

## Files

| File | Part | Notes |
|---|---|---|
| `grip-hammerli-208.py` | Anatomical (Nill-style) target grip for Hämmerli 208, left/right halves | Outline traced from a photo in pixel coords (`OUTLINE`, `P()`), scaled by `GRIP_HEIGHT_MM`; ellipse loft cross-section; tenon, frame pocket, checkering. `LAYOUT` = `"print"`/`"assembled"`, `PRINT_TEST` for a fit test. English. |
| `ammo_boxes.py` | Ammo box + sliding lid sized to a CCI crate | Largest script. `CALIBER` selects from a caliber table (22LR, 9MM, 357MAG, 38SPL, 40SW, 45ACP, 10MM, 223, 6.5X55); staggered/checker hole pockets, lid detents, pry notch, engraved text. Norwegian. |
| `chamber_flag_22LR.py` | Chamber safety flag for S&W Model 41 (.22 LR) | Cartridge plug + octagon flag with stencil text cut through (auto-bridges letter islands). `PLUG_ONLY` for a quick fit test. Norwegian. |
| `reddot_mount_sw_41.py` | Red dot mount plate for S&W Model 41 | Dimensions in **inches**, converted with `mm()`. Exports STEP+STL to the FreeCAD user data dir when `EXPORT_FILES`. |
| `red_dot_hammerli208.py` | Hämmerli 208 front-face profile | Exports to a hardcoded `/tmp/...stl`. Norwegian. |
| `magazine-holder-glock.py`, `magazine-holder-glock-v2.py`, `magazine-holder-1911-v2.py` | Skådis-mounted magazine trays | Older lowercase-variable style. `-glock-v2` adds hook root/neck fillets and deeper peg anchoring over `-glock`. |
| `magazine_holder_glock_open.py` | Open Glock magazine rack with flared blades and Skådis hooks | Norwegian comments. |
| `ikea_skadis_pegboard-30x30.py` | Lightweight custom Skådis pegboard | Ribbed hollow back, 300×300 mm by default. |
| `skadis_wide_mount.py`, `skadis_mount_screws.py` | Wide Skådis mount and matching printable plastic screws | Screws use a helical thread sweep. |

## Conventions

Follow the newer scripts (`grip-hammerli-208.py`, `ammo_boxes.py`, `chamber_flag_22LR.py`) when writing new code:

- **Header docstring** with `# -*- coding: utf-8 -*-`: what the part is, the version, what changed, how it is built, and caveats about which dimensions are estimates.
- **Parameter block at the top** in `UPPER_CASE`, all in mm, each with an inline comment. Mark values the user must measure on the real object with `MEASURE`. Use `None` for "auto-derive".
- Sections separated by `# ----` banner comments; derived values are computed after the parameters.
- `V = App.Vector` alias.
- **Pure `Part` (OCC) geometry**: build `Part.Shape` objects with `makeBox`/`extrude`/`makeLoft`/`fuse`/`cut`/`common`, then put the final shape in one `Part::Feature` via `doc.addObject(...)`. No PartDesign bodies, sketches or spreadsheets.
- Wrap fragile boolean/fillet ops in `try_op(label, fn, shape)`, which returns the original shape and logs a warning on failure instead of aborting. Call `.removeSplitter()` on final shapes.
- Make GUI calls optional: `try: import FreeCADGui as Gui` / `HAS_GUI`, or `if App.GuiUp:`.
- **STL export** goes through `Mesh.export` when `EXPORT_DIR` is non-empty (empty = no export).
- Quick-test toggles (`PRINT_TEST`, `PLUG_ONLY`, `CHECKERING=False`) let the user print or preview a small piece before the full part.
- Text engraving uses `Part.makeWireString` with a `find_font()` that searches system/user font dirs (including snap/flatpak paths) for a bold TTF.
- Keep each script self-contained. Helpers such as `try_op`, `find_font` and `yz_prism` are copied between files on purpose, not shared.

## Language & context

- The user is Norwegian. Comments, console messages and commit messages mix Norwegian and English, so match the language already used in the file you edit. The latest grip script is in English.
- Parts are designed for FDM printing with a 0.4 mm nozzle. Keep clearances, wall thicknesses and print orientation (e.g. "print" layouts lying flat) in mind.
- Many dimensions come from photos or estimates. When changing geometry, keep measurement parameters exposed and documented rather than hardcoding them.
- Commits are small, one per design tweak, directly on `main`.
