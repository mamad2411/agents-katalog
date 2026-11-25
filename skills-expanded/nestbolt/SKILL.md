---
name: nestbolt
description: "Nest parts on sheets for laser cutting, CNC routing, plasma, waterjet, fabric or leather: fit SVG or DXF part outlines onto fixed stock sheets with spacing and margins so the job uses the least material, check the layout and save per-sheet SVG/DXF cut files. Use when someone asks to nest parts, fit parts on a sheet or plate, cut down material waste, or work out how many sheets a job needs. Free, local, no account, nothing uploaded."
license: MIT
compatibility: "Needs the nestbolt-mcp executable on PATH, from the Nestbolt v0.1.0 release (Windows x64, Linux x64, macOS Apple silicon)."
---

# Nestbolt sheet nesting

Nestbolt arranges parts on fixed sheets so they use the least material, for laser cutters, CNC
routers, plasma, waterjet, fabric and leather. It runs on this computer: no account, no network,
nothing uploaded. Every layout it returns has passed an independent geometry check, and exports
keep the original arcs and curves.

## When to use it, and when not

| Request | Use |
| --- | --- |
| Fit these SVG or DXF parts on 600 x 400 mm sheets with 2 mm spacing | `import_parts`, then `nest` |
| How many sheets will this order need, roughly, before I buy material? | `estimate_sheets` (a lower bound), then `nest` for a real layout |
| Is this layout file still valid for these parts and sheets? | `validate_layout` |
| Write the cut files again as DXF | `export_layout` |
| Toolpaths, G-code, feeds and speeds, or machine settings | Not Nestbolt: it writes nested SVG or DXF files (or LightBurn projects, a preview feature) for the user's CAM or laser software |
| A guarantee that parts fit the machine or are safe to cut | Not given: Nestbolt gives no machine-safety or fit certification |

LightBurn projects (`.lbrn2`, `.lbrn`) are a preview feature. The
[v0.2.0-alpha.1 preview](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1) adds
editable LightBurn project nesting; say it is a preview whenever you use or mention it.

## Workflow

All lengths are millimetres. Every path must be inside the workspace: the folder Claude Code was
started in (or `NESTBOLT_WORKSPACE` when set). Paths with `..` or outside it are refused, and
Nestbolt never overwrites a file: outputs go to new files and new or empty folders.

1. **Import.** `import_parts` with `paths` (SVG or DXF files inside the workspace). It writes a
   part library and returns part ids, areas, bounds and import warnings. Read the warnings: they
   say when units, open contours or layers need attention (`dxf_unit_mm`, `svg_user_unit_mm`,
   `layers`, `close_gaps_mm`).
2. **Nest.** `nest` with the `library_path` and a `request`: parts by id with quantities, the sheets
   in mm, and spacing. For example:

   ```json
   {
     "parts": [{"id": "parts-1", "quantity": 4}, {"id": "parts-2", "quantity": 12, "rotations": {"kind": "free"}}],
     "sheets": [{"width_mm": 600, "height_mm": 400, "margins_mm": {"left": 5, "right": 5, "bottom": 5, "top": 5}}],
     "spacing_mm": 1.0,
     "edge_spacing_mm": 1.0
   }
   ```

   Rotations default to 0, 90, 180 and 270 degrees, and mirroring to off. Small parts may go inside
   the holes of larger ones. `time_budget_s` (1 to 300, default 10) is the search budget; the same
   library, request, budget and `seed` repeat the same layout unless the reply says
   `"repeatable": false`. The reply gives the sheets used, material use and the per-sheet SVG and
   DXF files it wrote.
3. **Report.** Tell the user the sheets used and the material figures from the reply, and where the
   cut files are. `validate_layout` re-checks a layout file; `export_layout` writes SVG, DXF (or
   LBRN2 for a LightBurn library, a preview feature) into a new folder.

v0.1.0 doesn't accept the `quick_start` request field (it came later), and its request schema
refuses unknown fields, so leave it out.

`estimate_sheets` is net part area over usable sheet area: a necessary lower bound for planning
and quotes, never a layout. It also flags parts that fit no sheet in any allowed rotation.

## If Nestbolt's tools are missing

The Claude Code plugin registers the `nestbolt` server and this skill, but it doesn't install the
program. Without `nestbolt-mcp` on PATH, the server fails to start (`/mcp` shows
`plugin:nestbolt:nestbolt` failed) and no Nestbolt tools appear. With the user's agreement:

1. Download the archive for their computer from the
   [v0.1.0 release](https://github.com/skulitom/Nestbolt/releases/tag/v0.1.0):
   `nestbolt-v0.1.0-x86_64-pc-windows-msvc.zip`, `nestbolt-v0.1.0-x86_64-unknown-linux-gnu.tar.gz`
   or `nestbolt-v0.1.0-aarch64-apple-darwin.tar.gz`, and check it against `SHA256SUMS` from the
   same release.
2. Extract `nestbolt-mcp` (`nestbolt-mcp.exe` on Windows) into a folder on the user's PATH.
3. Restart Claude Code from a new terminal, so the plugin finds it.

Without installing anything, the [browser app](https://skulitom.github.io/Nestbolt/) nests SVG and
DXF files on the user's own computer; nothing is uploaded. More: the
[README](https://github.com/skulitom/Nestbolt#readme) and the
[agent interface](https://github.com/skulitom/Nestbolt/blob/main/docs/AGENT_INTERFACE.md).
