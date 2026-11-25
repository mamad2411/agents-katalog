---
name: cad-edit
description: Read, edit and plot AutoCAD DWG files headlessly — no AutoCAD window, no COM/MCP — by driving accoreconsole.exe (the console engine that ships with AutoCAD and AutoCAD LT 2024+) with AutoLISP scripts. Use for any "change this drawing / edit the DWG / batch-edit sheets / update keynotes, schedules, title blocks, tags / add notes, dimensions, revision clouds / plot to PDF / export DXF / what's in this drawing" task. Don't use an AutoCAD MCP or COM (needs the window open and idle). Paths must be ≤ 240 chars and written as C:/…; back up before editing and read back to verify.
---

# cad-edit — edit DWGs without opening AutoCAD

## What this is

`accoreconsole.exe` lives in every AutoCAD install folder. It is **AutoCAD without a UI**: give it a
DWG and a script, it opens, runs, saves and exits in 1–3 s per drawing, in its own process. The user can
keep working in AutoCAD on other drawings meanwhile. It edits the same DWG file, so what the user opens
afterwards is the edited drawing.

| Engine | Can do |
|---|---|
| **Full AutoCAD 2024+** (default) | Everything below, plus `--dyn`: NETLOAD `dynblock.dll` → dynamic-block states/parameters, table API, xref paths |
| AutoCAD LT 2024+ | Plain AutoLISP (entget / entmod / entmake / command). No .NET, so no dynamic-block parameters and no table API — use the DXF route for tables |

Don't drive a live AutoCAD through COM / an MCP: if AutoCAD isn't open it spawns an empty window that sits
busy; if it is open, COM is rejected the moment the user is inside a command.

## Tools

`scripts/core.py` writes the `.scr`, loads the LISP library, starts the process and filters the output:

```bash
S=<skill dir>/scripts
python $S/core.py info    "C:/path/A-101.dwg"                        # version, units, layout names, entity counts, xref status
python $S/core.py survey  "C:/path/A-101.dwg" --type MULTILEADER --out C:/tmp/ml.txt   # entity list with handles
python $S/core.py run     "C:/path/A-101.dwg" --readonly --cmd '(princ (ml-get-attr "97753" "TAG"))'   # dry run
python $S/core.py run     "C:/path/A-101.dwg" --save --file edits.lsp.txt        # real edit: timestamped backup, then QSAVE
python $S/core.py run     "C:/path/A-101.dwg" --save --dyn --file x.lsp.txt     # + dynblock.dll (full AutoCAD)
python $S/core.py plot    "C:/path/A-101.dwg" --layout "A-101 FLOOR PLAN" --out C:/tmp/A-101.pdf [--pre '(lisp)']
python $S/core.py dxf     "C:/path/A-101.dwg" --out C:/tmp/A-101.dxf             # DXFOUT for ezdxf / dxf_table.py
python $S/core.py ctb     "C:/path/A-101.dwg"                                    # plot style per layout + what's installed
python $S/core.py exe                                                            # which accoreconsole will be used
```

`survey` prints one entity per row: `handle|type|layer|space|xmin,ymin,xmax,ymax|name|attrs|text`.
**The handle is the key for every edit** — survey first, never guess.

`lisp/lib.lsp` (always loaded):

| Function | Does |
|---|---|
| `(set-text h "new")` | TEXT / MTEXT content |
| `(get-insert-attr h "TAG")` `(set-insert-attr h "TAG" "val")` | block-reference attributes (title blocks, door/room tags) |
| `(ml-get-attr h "TAG")` `(ml-set-attr h "TAG" "val")` | attributes of a block inside a multileader (keynote bubbles) |
| `(ml-set-text h "txt")` | multileader MTEXT |
| `(del-handle h)` `(move-handle h dx dy)` `(set-layer h "L")` `(set-color h 1)` | delete / move / relayer / recolor |
| `(ensure-layer "L" color)` `(layer-onoff "L" nil)` `(layer-freeze "L")` `(freeze-off-layers)` | layers |
| `(ensure-review-layer "Z-REVIEW" 6)` `(review-box …)` `(review-note …)` | non-plotting review layer marking each change |
| `(hl-get h 8)` `(hl-set-group h 1 "x" T)` | raw DXF group read/write for anything else |

Other LISP files (`(load "<skill>/lisp/x.lsp")`): `census.lsp` `(text-census)` text-style census ·
`mlclone.lsp` `(ml-clone src dx dy ax ay "txt")` copy a note · `mlarrow.lsp` `(ml-arrow h ax ay)` pin an
arrowhead · `mtedit.lsp` `mt-get`/`mt-put`/`(BR)` long MTEXT · `revcloud.lsp` `revpoly`/`revcloud`/`cloudtag`/`find-clouds` revision clouds + deltas.

Add new helpers to lib.lsp using only entget / entmod / entmake / entdel / `(command …)`.
**No `vla-*` / `vlax-*`**: accoreconsole has no ActiveX; those calls fail silently.

## Per-machine setup

| Item | Default | If different |
|---|---|---|
| accoreconsole.exe | `cadcore.json` in the skill folder (written by install.ps1) + `C:/Program Files/Autodesk/AutoCAD*`; full AutoCAD first, newest year first | re-run `install.ps1 -AutoCAD "<folder>"` (only Autodesk-signed executables are accepted); `install.ps1 -PreferLT` or `--lt` to prefer LT. No environment variables are used |
| Plot style (.ctb/.stb) | each layout's saved page setup; ask the user before plotting (see Plotting) | `core.py ctb` shows what's used / installed; `plot --ctb <name>` overrides; missing files go in the Plot Styles folder (`STYLESMANAGER` opens it) |
| PDF driver | `DWG To PDF.pc3` | `--device "Name.pc3"` |
| dynblock.dll | built for AutoCAD 2027 | rebuild for your release, see `dotnet/dynblock/README.md` |

## First use (plugin installs)

`install.ps1` normally does this; a Claude Code plugin install doesn't run it. Before the first job:
1. `python <skill dir>/scripts/core.py exe` — prints the accoreconsole it will use. If it fails or picks AutoCAD LT
   while the user has full AutoCAD elsewhere, ask where AutoCAD is installed and write
   `<skill dir>/cadcore.json` as `{"accoreconsole": ["D:/Path/To/AutoCAD 2026/accoreconsole.exe"]}`.
2. `python -m pip install --user pymupdf numpy ezdxf` (ask the user first).

## Workflow

1. **Look**: `info` (units, layouts, xrefs resolved?), `survey` for handles and current values.
2. **Plan**: in Python, read the survey and write an edit script, one LISP line per change.
   Optionally mark each change with `review-box` + `review-note` on a non-plotting `Z-REVIEW` layer.
3. **Dry run**: `run --readonly --file edits.lsp.txt`; every lib call prints `… OK|FAIL`.
4. **Edit**: `run --save --file edits.lsp.txt` (backup `*.bak.dwg` next to the DWG first).
5. **Verify**: read the values back; `plot` the **whole sheet**, render with PyMuPDF and look at it —
   zoom into every changed spot and check the knock-on effects (see "After every edit").
6. **Report**: what changed, where the backup is, how to remove the review layer.

When the drawing lives in a shared/synced folder: ask before editing, check for a `.dwl` lock (the user
has it open — their next save would overwrite yours), and keep temp PDFs/PNGs out of the project folder.

## Hard rules (each one learned the hard way)

**Engine & scripts**
- Paths ≤ 240 chars, written `C:/…` with forward slashes. Longer or `/c/…` → `Improper drawing name, ErrorStatus=360`.
  core.py works in `%LOCALAPPDATA%\Temp\cadcore` for this reason.
- `.scr` must be CRLF (core.py writes it that way). If you call accoreconsole by hand from Git Bash, set `MSYS_NO_PATHCONV=1` so `/i` and `/s` aren't rewritten as paths. `SECURELOAD 0` before any `load`.
- Script lines longer than ~2000 chars get truncated (you see `((((_>` prompts): put long code in a `.lsp` and `(load …)` it.
- A script that hangs is almost always a command waiting for an answer you didn't give. core.py kills it at the timeout; rerun with `-v` to see the prompt.
- `(setvar "OSMODE" 0)` first — running object snaps pull scripted points onto nearby lines.
- `(command "_.EXPLODE" en)` ends by itself; an extra `""` repeats the last command and the script stalls.
- entdel / MOVE only work in the **current space**: `(setvar "CTAB" "Model")` or switch to the layout first.
  `(command "_.PSPACE")` before a paper-space `-INSERT` (entmake'd paper-space blocks may not plot).
- With a UCS active, command points are UCS points: `(command "_.UCS" "_W")` first, restore after.
- `run --cmd … --file …`: `--cmd` lines run **before** the file; put SAVEAS-type endings at the end of the file.
- Each run is a fresh process: system variables you set never leak into the user's AutoCAD.
- AutoCAD 2027 writes `ErrorReports\<hash>\cer.log` into the current directory on every start (not a crash).
  Keep the working directory out of synced/shared project folders so these don't get uploaded.
- LISP variables are case-insensitive (`d` and `D` are the same symbol). No inline `;` comments in script files; use `(chr 59)` for a literal `;` in strings.
- Backslashes: build `\P`, `\f`, `\X`, `\W` in MTEXT/DIMPOST with `(chr 92)`. Shell and Python layers eat backslashes and
  LISP drops unknown escapes, so `\P` ends up printed as a letter P. Inch marks inside LISP strings are `\"`; grep the generated file before running.

**Entities**
- Multileader attributes are not in the ATTRIB chain; they're in the MLEADER's own 330/302 pairs. lib handles both.
- Multi-line attributes (`101 Embedded Object`): change **every** code-1 value including the embedded MTEXT copy, otherwise the old tail remains.
- `move-handle` on a multileader moves the arrowhead too; pin it back with `ml-arrow`. New notes: `ml-clone` an existing one (same style, mask, frame).
- A keynote usually exists as several unrelated entities (bubble on the plan, bubble in the legend, legend text); change all of them.
- Compare text **by position**, never by counting strings (counting once mistook 20 legitimate "TYP." for extras).
- Annotative dims/mleaders: set `CANNOSCALE` before creating them or they come out at 1:1 (invisible).
- Radius dimension by entmake: DIMENSION 70=164, 10=center, 15=point on arc, 11=text position; `-DIMSTYLE` / setvar DIM* in scripts get refused.
- Block definitions: entmake BLOCK/ENDBLK with bare geometry; hidden lines need an explicit linetype (group 6).
- `-INSERT` of a whole DWG can rescale imported block definitions by 1/25.4 while nested inserts keep their scale — explode to bare geometry in an intermediate file, or fix scales afterwards and measure with ezdxf.
- Xref copies: entmake an INSERT (`-INSERT` refuses xref names), then `(command "_.XCLIP" (entlast) "" "_N" "_R" p1 p2)`.
- Don't use `-XREF _P` (its path prompt chokes on spaces); use `(xrefpath name path)` from dynblock.dll.
- Blocks with -Z extrusion (ARC/SPLINE from mirrored content): flatten with `ezdxf.path.make_path(e).flattening()` before copying, or mirroring/offsets go wrong.
- Break lines: copy the office's existing break-line block and scale it; on the cut side nothing continues (walls, hidden lines, hatch all stop).

**DXF round trips**
- Reopening a DXF and SAVEAS-ing to DWG loses xref layer overrides (VISRETAIN) if the xrefs don't resolve: put the DXF in the DWG's folder (relative xref paths), or restore layer 62/70/6 afterwards.
- Viewport view changes (entmod 12/40/41/45) are refused in the console: COPY a viewport, `core.py dxf`, edit that VIEWPORT's 10/20/40/41/45/12/22 in the DXF, SAVEAS back. Image xrefs (logos in the title block) need their folder next to the DXF too.
- ezdxf helpers with a `color=7` default **override** your color: `add_hatch(color=7, …)`, `set_solid_fill(color=7)`.
  Order: `h = msp.add_hatch(dxfattribs={"layer": L}); h.set_solid_fill(); h.dxf.color = 256` — and verify after saving to DWG.
- **Never load/save a DXF that contains tables with ezdxf** (it drops table content). See `reference/table-edit.md`.

**PDF**
- `-PDFIMPORT` returns 0 objects in the console (LT and full). Instead: PyMuPDF `page.get_drawings()` → one LWPOLYLINE per path via entmake; map grey fills to hatch layers; white masks → WIPEOUT. Raster stamps can't be converted — redraw.
- Stamp-style PDF markups are not FreeText annotations; `page.annots()` misses their text. Render the page and look.

## Dynamic blocks (full AutoCAD, `--dyn`)

- `(dynget h)` properties, `(dynallowed h "Visibility1")` allowed states, `(dynset h "Visibility1" "State")`, numbers for distances/angles/flips.
- After a state switch, ATTRIB positions don't follow — entmod their 10/11 points and fill them.
- Editing a **definition**: walk `(tblobjname "BLOCK" name)` with entnext, entmod the geometry, then `(dynupdate name)`
  to rebuild all `*U` representations. `dynupdate`/`dynreset` reset ATTRIB positions — re-apply moves afterwards.
- Try on a copy in the same folder first (so xrefs resolve), check the plot, then edit the real sheet.
- On LT there is no way to set parameters: ask the user to switch one instance in AutoCAD and copy it. Don't substitute a different block.

## Tables / schedules

See **`reference/table-edit.md`**: dynblock.dll `tbl*` functions on full AutoCAD (preferred), DXF surgery
(`scripts/dxf_table.py`, `scripts/table_rowedit.py`) as the LT fallback.

## Plotting & sets

- **Ask which plot style (CTB) to use before plotting** — the first time the user asks for a PDF in a project.
  Run `core.py ctb <dwg>` first: it lists the CTB each layout has saved, whether that file exists on this machine, and
  every CTB installed. Show the user the drawing's own CTB as the default plus the alternatives, and ask. Remember the
  answer for the rest of the project; don't ask again for every sheet.
  - Drawing's own CTB → plain `plot`. Another one → `plot --ctb <name>` (for that plot only; the DWG isn't changed).
  - If the layout's CTB is missing, `plot` stops. Tell the user which file is missing — never plot with a substitute
    silently; line weights and screening would be wrong. `--allow-missing-ctb` only if the user says so.

- `--layout` must be the full layout name as `info` lists it (`A-120 FURNITURE PLAN`, not `A-120`), or -PLOT waits for input until timeout.
- **Always put `(freeze-off-layers)` in `--pre`**: DWG To PDF writes OFF layers as hidden PDF layers; merging PDFs drops the hidden state and switched-off geometry reappears. Frozen layers aren't exported.
  Standard: `--pre '(setvar "CLAYER" "0") (freeze-off-layers)'`, plus freezing any layers you want out of the print (e.g. clouds: `(command "_.-LAYER" "_F" "*CLOUD*,*|*CLOUD*" "")` — xref layers need the `*|` prefix).
- `--pre` runs before -PLOT and is never saved.
- Merge a set with `scripts/merge_pdfs.py out.pdf a.pdf b.pdf …` — it renders each merged page and compares with its source.
- A line "striking through" a table row may be a paper-space LINE over the viewport — search both spaces.
- Paper coordinates from a plot: PyMuPDF `get_text("words"/"blocks")` with the page rotation matrix → inches; viewport content via the viewport's model window and scale.

## Notes, leaders, text

- **Before creating any text, copy the drawing's own style** — never `Standard`, never from memory.
  `(load ".../census.lsp") (text-census)` prints `TYPE|space|layer|style|height|count`; copy the dominant row for the same kind of thing (same entity type, same space, same layer purpose). Cloning an existing entity and changing the text is safest.
- Leaders never cross. Order a column of notes by arrowhead height (higher target → higher note); at equal height, the target nearer the column goes higher.
- One note, one leader. A note pointing two places becomes two notes.
- Arrowheads land exactly **on the edge** of the thing they name — compute the point from the geometry, zero gap. One object per arrow.
- Leader-to-landing angle is obtuse (arrow heads away from the text). Near-horizontal-but-not-quite leaders look worst: make them horizontal or ≥ 15°.
- Adding words makes notes taller; re-check the note/datum below. Shorten wording rather than add lines; break long lines manually.
- Right column: left-justified (71=1); left column: right-justified (71=3) so text hugs the leader.
- Anything on the sheet a reader could ask "what is that?" about gets a short note: what it is + where to find the spec ("TASK LIGHT (TL), TYP.; SEE LIGHTING SCHEDULE ON A-141").
- More detail for interior elevations and enlarged plans: **`reference/graphic-standard.md`**.

## Revision clouds

- Copy the office's existing cloud style first (entget one: layer, color, chord length, bulge, calligraphy widths, delta block + scale). Set the `*rc-…*` variables at the top of `lisp/revcloud.lsp` to match, then `revpoly` (any CCW polygon), `revcloud` (rectangle), `cloudtag` (cloud + delta at a corner).
- Baseline = the last **issued, signed** set, not your own later plots.
- Clouds hug the change (tight bounding box + small margin), don't overlap text, symbols, other clouds, or the border. Deleted things aren't clouded. Only-moved-but-unchanged content isn't clouded.
- Delta triangle sits outside the cloud, touching distance, preferably top-right; never on text or lines.
- Find leftovers from previous rounds first with `(find-clouds)` so rounds don't mix.
- Details: `reference/graphic-standard.md` §13.

## After every edit

Anything you change can push something else: a taller table row shifts the notes below; a 3-line tag now
covers a stair; a longer note overlaps the next. **Re-plot the whole sheet**, crop 200–300 dpi images around
every changed object into a contact sheet, check below/right of anything that grew and around anything that
moved, then look at the full sheet once more.

## Working alongside a person in AutoCAD

- They must close the file before you edit (check the `.dwl` lock); reopen it for them after.
- Make a timestamped backup before every `--save`.
- **Never re-run a "rebuild from backup" script** once the person has edited the drawing — only targeted
  entmod/entdel, or you overwrite their work.

## Plan poché (wall fill) from base plans

- Fill only cut solid walls; never glass. Pair wall faces using the **union** of both faces' extents (door openings stay open, one-sided gaps get closed); verify every door block lies outside the fill.
- Cut glass out across the **full wall thickness** (the glazing block is often thinner than the wall). Removing fill ≠ deleting lines: the two parallel lines at glazing are the **sill**, keep them (sill layer), trimmed to the glass length.
- Close T-junction gaps with a morphological close (`buffer(+6).buffer(-6)`, mitre joins); the area should grow by only a few sq ft.
- Connected walls = one closed LWPOLYLINE + one SOLID hatch, color BYLAYER.

## Reference

- `reference/graphic-standard.md` — interior elevation / enlarged plan drafting standard + checklist.
- `reference/table-edit.md` — tables and schedules.
- `reference/pdf-align.md` — rolling a DWG back to match a signed PDF (`pdf_posdiff.py`, `pdf_overlay.py`).
