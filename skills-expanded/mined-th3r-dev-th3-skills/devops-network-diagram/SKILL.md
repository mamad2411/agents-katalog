---
name: devops-network-diagram
description: >-
  A system / network diagram kept as one editable draw.io file where every version is a board on
  the same page, shipped as a one-page PDF per version. Lists the version boards, starts the next
  version as a draft board, exports one version to a clean one-page PDF named like the final file,
  rebuilds an editable .drawio from a final PDF when the source is lost, and benchmarks a PDF
  against the final one (text, layout, pixels). Icons come from the team's own logos or draw.io's
  built-in library — never cut out of a PDF, never an emoji. Use WHENEVER the work is "system
  diagram", "network diagram", "update the diagram", "new diagram version", "export drawio to pdf",
  "the drawio exports several pages / a blank page", "we only have the PDF, not the drawio",
  "compare the pdf with the final one", "แก้ diagram ระบบ", "ออก diagram version ใหม่".
---

# devops-network-diagram

The team keeps **every version on one draw.io page**, one board per page tile (`pageWidth` ×
`pageHeight`, e.g. A2 landscape 2336 × 1654 px): Non-prod 1.1.3 beside Prod 1.1.5, then 1.1.6 and
1.1.7 stacked under it. A board is the tile that holds a `Version x.y.z Update dd/mm/yyyy` label,
and its title is the text ending with `System Diagram` (`--title-suffix` to change).

That layout is why a plain `draw.io -x -f pdf` is wrong: it prints every tile, blank ones included.
Everything below goes through one script that understands boards:

```bash
B="uv run skills/devops/network-diagram/scripts/drawio_board.py"
$B list    <file.drawio>                                            # boards: tile, version, date, cells, title
$B clone   <file.drawio> --from 1.1.7 --version 1.1.8 --date 06/11/2026   # draft board, in place, .bak kept
$B export  <file.drawio> --version 1.1.8 [--out DIR] [--name "{title} {env} {version} - {ddmmyy}"] [--title "…"]
$B trace   <final.pdf> --out X.drawio [--assign X,Y=slug]           # PDF -> editable drawio (source lost)
$B compare <final.pdf> <candidate.pdf> [--no-image-check] [--diff-png d.png]   # benchmark, exit 1 on FAIL
$B --env-map "Production=Prd,Non Production=Uat" export …          # global options go before the subcommand
```

Needs the draw.io desktop app (`/Applications/draw.io.app`, or `drawio` on PATH). Output defaults to
`./diagram-out/` — keep diagrams out of the skills repo.

## Get the source

The team `.drawio` usually lives on a shared drive. If a connector returns it as base64, decode it
straight to disk (`jq -r .content <result> | base64 -d > src.drawio`) — it is too big for context.
Run `list` first: it tells you which versions exist and catches a board without a version label.

## Draft a new version

1. `clone --from <latest> --version <next> --date <dd/mm/yyyy>` copies the latest board into the free
   tile under it, with new cell ids and the new label. The old boards stay as history.
2. Change the new board only: edit the XML for small things (an IP, a port, a hostname), or open the
   file in draw.io for layout work. Keep the house style so the PDF still reads as the same document.
3. `export --version <next>` writes the PDF and a standalone `.drawio` of that board. Hand back both:
   the standalone file is the editable draft for reviewers; the multi-board file goes back to the drive.

`export` keeps only the page holding the version label. A cell poking a few px over the tile edge
makes draw.io open a blank sliver page; that page is dropped. A dropped page **with words on it**
fails the export, because a cell really did spill out of the board — move it back inside.

## House style (read it off the team file, then keep it)

- One page size for every board; white; no grid in the PDF.
- Title (`Production Environment System Diagram` / `Non Production …`) bold ~35 px, underlined,
  centred; under it `Version x.y.z Update dd/mm/yyyy` ~18 px, underlined.
- Subnet bars: label above (`10.0.0.0/26`), full-width bar under it; one colour per role
  (load balancer, workload…).
- Clusters are dashed boxes, one colour per kind. Each node shows a bold name, then `Hostname:`,
  `IP:` and `Port:` lines at ~9 px.
- Edges orthogonal, 1 px black, classic arrowheads, port as a plain label beside the line (`80, 443`).
  URL labels sit on a white box framed `| https://… |` so the line does not cross the text.
- Thai text uses a Thai font (`fontFamily=Sarabun`, `--thai-font`); everything else Helvetica.

## Icons

`assets/icons/icons.json` is the library, in order of preference:

| source | what | shipped here |
|---|---|---|
| `team` | the real logo already embedded in the team .drawio, saved as a file | Argo, AVI service / controller, Tanzu supervisor, container |
| `builtin` | draw.io's own library, by style string | user, mobile, VPN, firewall, server |
| `fetched` | the product's official logo from its own site or repo, sized with `web-asset-generator` | add a row with `"source": "fetched"` and where it came from |

Add your customers' and products' logos as `team` rows with a `match` regex on the label beside the
icon. A product icon must be **that product's real logo** — not an emoji, a look-alike, or a generic
glyph. Never lift an icon out of a PDF: the PDF is the output and its bitmaps are rasterised copies.

## Rebuild from a final PDF (`trace`)

When only the PDF survives, `trace` gives back an editable drawio: one text cell per line (font,
size, colour, bold, rotation, on the PDF baseline — `--baseline 0.97 --baseline-px 4.4` fitted on a
draw.io web export at 7–25 pt), boxes with fill + stroke merged into one cell, dashed boxes and lines
measured off the dash pieces, polylines with waypoints and arrowheads attached to the nearest line
end, paint order kept, and every bitmap / vector icon turned into a slot filled from the library by
the nearest label (or the label of the box it sits in).

It prints one line per icon with the label it used. A slot whose name is inside the logo itself (Argo
has no text label) gets the wrong neighbour's icon: look at the render, then pass `--assign X,Y=argo`
with the coordinates from that line. Edges come out as free polylines, not glued to shapes —
reconnect the ones you are about to move.

## Benchmark (`compare`)

```
PASS  one page / same page size / same text / same images / same vector paths
PASS  same layout   114 anchor words, worst 1.29pt after scale 0.9762 shift (19.4,13.5)pt
PASS  same pixels   0.12% of ink differs (2 px tolerance, limit 2%)
```

- **same layout** fits one uniform scale and shift on every word that occurs once on both pages and
  reports the worst residual (limit 3 pt). The draw.io *web* export shrinks the page by ~2.4% with a
  ~19 pt margin; the desktop CLI does not — a scale near 0.976 against a web-exported final is
  expected, the residual is what counts.
- **same pixels** renders the candidate through that fit and compares ink with a 2 px tolerance.
- `--no-image-check` is for a redrawn diagram: it drops the bitmap / path counts and masks every
  reference icon slot, because icons were swapped on purpose.
- A reference printed with text as outlines (no text layer) cannot be aligned; the script says so.
