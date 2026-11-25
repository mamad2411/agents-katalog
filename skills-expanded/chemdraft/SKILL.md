---
name: chemdraft
description: Use ChemDraft to draw or show molecules; make structure images for documents, exams, slides and handouts, multiple-choice structure grids and reaction schemes; convert chemical names to structures; answer R/S and E/Z questions; compute molecular properties including formula, exact and average mass, m/z, isotope patterns, logP, TPSA, pKa and the property suite; predict NMR shifts; export CDXML, SDF, MOL, PDF and SMILES; make styled publication figures (coloured or shaded rings, ring letters, highlighted substructures, colour-coded atoms, hand-sketched looks, a named chemist's or journal's drawing style, arrows and annotations); and work with ChemDraft plugins. Make same-scale document-style figures inserted at natural size; name a structure through the app plugin, not headless. Never draw molecules by hand or quote chemistry numbers from memory.
---

# ChemDraft

## Two non-negotiables

1. Never hand-draw a molecule or invent or recall a structure-to-name result
   from memory: no ASCII structure, hand-written SVG, HTML
   canvas, matplotlib, or ad-hoc RDKit/Python drawing script. Use ChemDraft's
   shared depiction and export path.
2. Never quote a chemistry number from memory when ChemDraft computes it.
   Obtain its result and report the method, units, interpretation and limits.

If ChemDraft is unreachable, say so and stop the chemistry drawing or
calculation. Do not replace it with a guessed structure or number.

## Reach ChemDraft

Use these routes in order.

### 1. MCP

Use tools from the `chemdraft` MCP server when present. MCP (Model Context
Protocol) lets the assistant call a local program through typed tools.
The registered names are:

- `render_structure`
- `render_grid`
- `render_reaction`
- `analyze_structure`
- `name_to_structure`
- `check_stereo`
- `predict_nmr`
- `export_structure`
- `build_document`
- `render_document`

Use the server's supplied input schemas. For `build_document`, the first
text block is the JSON summary; the second text block is the document JSON.
Style that second block, or read the file named by the summary's `document`
field. Other tools return their JSON result first; PNG images, SVG text and
export resources follow it.
Check `isError` and the JSON `ok` field before using an output.
Each call gets a fresh output directory. Any returned payload is limited
to 5 MB; reduce image width if a visual payload is too large.
These tools create headless outputs; they do not edit the user's open canvas.

### 2. CLI

If MCP is absent and a local shell is available, locate the checkout from
this skill directory. A normal installation is a symlink from
`<checkout>/skills/chemdraft`. Resolve the directory's real path, then go
two levels up. Do not infer the checkout from the current working directory.

POSIX shell (macOS; select the installed Claude Code or Codex skill path):

```sh
skillDir="$HOME/.claude/skills/chemdraft"
checkout=$(node -p "require('node:path').resolve(require('node:fs').realpathSync(process.argv[1]), '..', '..')" "$skillDir")
if [ -n "$checkout" ]; then pnpm -s --config.shell-emulator=true --dir "$checkout" chemdraft --help; else echo "No ChemDraft checkout found from $skillDir" >&2; false; fi
```

For Codex, set `skillDir="$HOME/.codex/skills/chemdraft"` instead.
If the assistant already knows the loaded skill's directory, use that path.

PowerShell (Windows; a directory junction also resolves to its target):

```powershell
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$skillDir = Join-Path $HOME '.codex/skills/chemdraft'
$checkout = node -p "require('node:path').resolve(require('node:fs').realpathSync(process.argv[1]), '..', '..')" $skillDir
if (-not $checkout) { throw "No ChemDraft checkout found from $skillDir" }
pnpm -s --config.shell-emulator=true --dir "$checkout" chemdraft --help
```

For Claude Code, set the `$skillDir` line to `.claude/skills/chemdraft`.
If installed as a copy, the resolved directory is not the checkout. Use the
user's checkout path and confirm it with the same help command.

The check passes only if help lists all ten ChemDraft subcommands: render,
document, render-document, grid, reaction, analyze, name, stereo, nmr and
export. pnpm's own help means
the checkout path is wrong. Shell state may reset between tool calls; set
variables and console encoding again in each call, or use literal paths.

The command form is `pnpm -s --config.shell-emulator=true --dir <checkout> chemdraft <subcommand>`.
Without this flag, pnpm on Windows doubles backslashes
in arguments, changing SMILES bond-direction marks and paths. Use the flag
on both platforms.
Replace placeholders with actual paths and quote paths containing spaces.
`-s` is mandatory: a pnpm script banner on stdout corrupts JSON Lines
and, when launching `chemdraft-mcp`, stdio MCP framing.
Run from either platform without requiring bash on Windows.

### 3. Neither route is available

Point the user to [setup](references/setup.md) and stop. Local setup and
MCP registration belong on the computer that will run ChemDraft.
Do not simulate a successful ChemDraft response.

## Choose the operation

| Need | CLI subcommand | MCP tool |
|---|---|---|
| One molecule image | `render` | `render_structure` |
| Editable native document and ring ids | `document` | `build_document` |
| Styled native document figure | `render-document` | `render_document` |
| Multiple-choice structure grid | `grid` | `render_grid` |
| Reaction scheme | `reaction` | `render_reaction` |
| Properties, masses, pKa, isotope envelope | `analyze` | `analyze_structure` |
| Chemical name to structure | `name` | `name_to_structure` |
| R/S and E/Z assignments | `stereo` | `check_stereo` |
| Predicted ¹H/¹³C NMR shifts and spectra | `nmr` | `predict_nmr` |
| CDXML, PDF, SDF, MOL, SMILES files | `export` | `export_structure` |

PDF output currently misplaces atom labels and text. View every PDF
before delivering it, and prefer SVG or PNG figures until this is fixed.

## Fixed-scale figures for documents

For every structure going into Word, a handout, an exam, slides or a report,
use `--style document` and SVG: `render`, `grid`, `reaction`, `document`, and
`render-document` all accept it. With MCP, send `style: "document"` to the
corresponding tool. Document style fixes one bond at 14.4 pt, the plain line
width at 1.134 pt, and labels at Arial 10 pt; its SVG root dimensions and
viewBox are in points. Insert the SVG at its natural size (100%). Use the
returned `widthPt` and `heightPt` when software needs dimensions.

Never scale, zoom, stretch or crop a structure to fit a page, cell or slide.
Change the layout around it instead: wrap text, use fewer structures per row,
start a new page, or use a two-column table. Every structure in one document
must share the same scale.

Use document-style PNG only for a viewer that cannot show SVG: add `--dpi`
(default 300; 72–1200), then insert the PNG at the SVG's reported physical
`widthPt` and `heightPt`, never at a fitted width. `--dpi` is only valid with
document style. Keep width-fitted `--style fit` for a one-off image only when
the user asks for a particular size; do not combine document style with
`--width`, `--bond-length`, or `--padding`.

## Core workflow

1. Decide what chemistry the user intends: compounds, charges, isotopes,
   stereochemistry and, for reactions, component roles. Preserve salts and
   counterions. A drawing instruction does not authorize changing chemistry.
2. Then obtain the SMILES, a text encoding of atoms and bonds. If only a
   chemical name is known, use `name` or `name_to_structure`. ChemDraft checks its built-in
   structure templates before OPSIN. For hosts such as beta-cyclodextrin, β-CD,
   cucurbit[7]uril and 18-crown-6, use the template name rather than writing SMILES.
   Templates work without Java and supply an original layout at default bond length.
   Only exact canonical isomeric SMILES matches receive that layout; never remove
   stereo or charge to force a match. OPSIN parses
   systematic names, not every trivial or trade name. When it fails on a
   common name, look the compound up in PubChem and cite the CID (recipes
   11 and 12 show the lookup), or supply a systematic name and say it came
   from memory. Either way, confirm the formula with `analyze` and the
   stereocentres with `stereo` before using the structure. If a name is
   ambiguous, explain it and obtain a clearer one; never guess a structure.
3. Read only the reference for the operation you need. Choose output paths
   outside the repository, in a scratch or user-chosen output directory.
   Run the command or tool with the confirmed input.
4. Read each JSON line. Require `ok: true`; examine `warnings` even on
   success. A batch can contain successful and failed jobs together.
   For depictions, inspect `stereoCenters`, `unspecifiedStereoCenters` and
   `unspecifiedDoubleBonds` wherever the result provides them.
5. Look at the rendered image at least once before placing it. Check atom
   labels, charges, bonds, wedge/hash bonds, clipping, grid labels and
   reaction roles. If the image viewer cannot display SVG, request PNG
   from ChemDraft for inspection.
6. Place the verified figure in the requested document. Keep its SMILES,
   relevant options and warnings alongside the document so it can be
   regenerated. Retain the answer key separately from student-facing art.

`@` and `@@` in SMILES depend on atom order; they are not literal R/S
labels. Use `stereo` to state R/S. For a question asserting a fully
specified stereoisomer, both unspecified counts must be zero. An exercise
explicitly asking about unspecified stereochemistry can retain it and
must say so. E/Z geometry is also checked through `stereo`.

## Structure to name

The desktop app can name a drawn structure only through the Orthonym plugin
from `github.com/jgassens/ChemDraft-Orthonym-Plugin`. Once installed, it adds
Structure > Convert Structure to Name, Analyze-menu entries, and Insert Name
as Text. Its local naming engine installs only when the user asks. Before a
name is shown, OPSIN parses it back and RDKit compares its canonical isomeric
SMILES with the drawn structure exactly; a mismatch shows no name. Metals,
charged zwitterions, and some radicals can be declined with a plain reason.

The CLI and MCP cannot name a structure today: `name` and `name_to_structure`
only convert a name to a structure using templates before OPSIN. Do not offer a
structure-to-name result from a headless route, invent or recall one from
memory, or claim a name that Orthonym declined. Point a user who needs a name
to the app's Orthonym plugin.

## Appearance and style requests

Route every request about how a structure looks to [art](references/art.md):
"in the style of" a chemist or journal, coloured or shaded rings, ring
letters, highlighting part of a molecule, colour-coded atoms, explicit H
or Me at stereocentres, hand-drawn or sketched looks, publication or
journal figures, annotations, arrows and brackets. The workflow is
`document` (MCP `build_document`) → edit the native JSON →
`render-document` (MCP `render_document`) → look → iterate.

- Appearance changes never change chemistry, and they are always allowed.
  Confirm after every edit that the reported canonical SMILES still
  matches the source (art.md shows how when explicit H is added).
- A named chemist's or journal's drawing style is a set of visual
  conventions to reproduce, not something to refuse or to call
  impossible.
- "Nicolaou style" is a style for any molecule, not one structure: loud,
  saturated fills, one per lettered ring with no two neighbours alike,
  are the core of the look, with italic serif ring letters, fusion H and
  Me labels on top. Deliver the coloured figure as the answer, not as an
  optional variant; black and white with ring letters, or pale pastels,
  is not the style. `scripts/ring-style.mjs` applies it to any molecule
  and checks the result against PubChem (recipe 11). Its figure checks
  fail a drawing with sliver rings, stretched bonds or wedges, shrunk
  letters, hidden rings or dropped fusion H: such a figure is not
  finished. Say what failed and offer the plain drawing, or the coloured
  one with the failures named.
- A label such as Me set as an atom's element replaces that carbon with
  a placeholder atom. Keep the editable file with real carbons and use
  the Me-labelled copy only as the picture (art.md, pattern 2).
- Look at every wedge and hash at full size after a sketched render, and
  offer an unsketched version when stereochemistry must be unambiguous.
- Never tell a user ChemDraft cannot produce a visual style until you
  have read art.md and tried it. If one detail truly cannot be done,
  name that detail, say why, and deliver the rest.

## Report honestly

- Quote a number with the method, units and interval the result gives.
  Retain its interpretation label when it describes a derived structure.
  Read method metadata and conventions in `run.results` and engine versions
  in `run.engines`, not only `summary`; see [analysis](references/analysis.md).
- Report a declined value as **not computed**, with its reason. Never
  fill it from memory, another species, or a fallback calculation.
  Distinguish declined results from `not-requested` methods.
- Keep estimates labelled estimates, including NMR multiplicities and J
  couplings. Predicted shifts are predictions, not measurements.
- Isotopes and their positions are preserved, including D/T and labelled C, N and O.
- Refused radicals remain refusals. Do not remove their SMILES
  notation to make a command succeed. `render`, `document` and `export`
  refuse a radical such as `C[CH2]`, while `analyze` keeps it and reports
  its composition (C2H5) and masses. Say which part was refused.
- Request only the analysis methods you need (`--methods` or MCP
  `methods`): an unrestricted `analyze` returns every method, over 100 KB
  of JSON even for ethanol.
- MCP `export_structure` takes one molecule. A multi-record SDF or SMILES
  file needs the CLI `export --batch` ([files](references/files.md)).
- The m/z table is exact-mass arithmetic, not fragmentation prediction;
  it gives no claim about observed ion intensity or whether a loss occurs.
- Isotope-envelope numbers need the IsoSpec abundance disclosure in
  [analysis](references/analysis.md) beside the numbers they qualify.

## Output contract

Normal CLI jobs emit JSON Lines on stdout: one complete JSON object per
line. Progress goes to stderr. Help output is human-readable, not JSON.
Do not combine stderr into a JSON parser's input.

Exit codes are 0 for all jobs successful, 1 for any attempted job failed,
and 2 for invalid arguments or batch input. `ok: true` for an analysis job
does not mean every method computed a value; inspect method statuses.

Keep chemical input within 5000 characters and 500 heavy atoms (atoms
other than hydrogen), and batches within 500 jobs. PNG widths must be
16–4000 pixels. Apply these limits yourself even where a particular
command path does not enforce every one of them.

Batch files are JSON arrays. Most jobs have `name` and `smiles`; name
conversion uses `name` and `query`, and reactions have role-specific
shapes. Names are trimmed and must match
`^[A-Za-z0-9][A-Za-z0-9 _-]{0,99}$`. They must be unique ignoring case.
No path separators, leading dot, blank name or unsafe output name is
allowed. See the relevant reference for combined versus per-job files.

## Read next

- [Setup](references/setup.md): installation, both platforms, skill and MCP registration, plugin trust.
- [Drawing](references/drawing.md): render/grid/reaction options, salts and stereo image checks.
- [Analysis](references/analysis.md): method IDs, statuses, interpretations, intervals and mass conventions.
- [NMR](references/nmr.md): predictor setup, spectra, omitted environments and experimental comparisons.
- [Files](references/files.md): OPSIN names, export formats and the human CDXML editing loop.
- [Plugins](references/plugins.md): official catalog, headless reach, permissions and plugin authoring.
- [Art](references/art.md): styled figures, ring fills and letters, highlights, sketch look, arrows, known limits.
- [Recipes](references/recipes.md): worked commands for exams, figures, properties, datasets and styled figures.
- `scripts/ring-style.mjs`: Nicolaou-style ring fills, letters, fusion H and Me for any molecule, with the identity and figure checks (recipe 11; `--help` lists commands and options).
