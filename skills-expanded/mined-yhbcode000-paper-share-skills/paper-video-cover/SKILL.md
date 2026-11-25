---
name: paper-video-cover
description: |
  Generate a deterministic 16:10 video-cover poster from a paper directory.
  Extracts paper metadata and figures and atomically produces poster.tex,
  poster.pdf, and poster.png. Use for paper-video covers, not conference posters.
argument-hint: "<paper_dir>"
---

# Paper Video Cover

Generate a Gemini/SUSTech 16:10 cover from a paper directory. The generator
installs output only after LaTeX compilation and PNG conversion both succeed.

## Package and setup

The installed uv project is:

```text
<SKILLS_DIR>/paper-video-cover
```

It manages its Pillow dependency and includes both required themes:

```text
<SKILLS_DIR>/paper-video-cover/templates/beamerthemegemini.sty
<SKILLS_DIR>/paper-video-cover/templates/beamercolorthemesustech.sty
```

LuaLaTeX and Poppler `pdftoppm` are external tools. Both must resolve before
generation. Each tool is resolved in order: explicit CLI flag, `LUALATEX` or
`PDFTOPPM` environment variable, then `PATH`. An invalid higher-priority override
is fatal and is not bypassed.

## Run

```powershell
uv run --project "<SKILLS_DIR>/paper-video-cover" `
  "<SKILLS_DIR>/paper-video-cover/scripts/generate_poster.py" `
  "<paper_dir>"
```

Default output is `<paper_dir>/poster`. Select another directory with:

```powershell
uv run --project "<SKILLS_DIR>/paper-video-cover" `
  "<SKILLS_DIR>/paper-video-cover/scripts/generate_poster.py" `
  "<paper_dir>" --output-dir "<output_dir>"
```

Options:

- `--data <json>`: optional JSON overrides.
- `--scheme <default|lab|bilibili>`: SUSTech colour scheme (default `default`; 实验室调研 uses `bilibili` to match the lab-survey deck).
- `--title-font <points>`: override the automatic title size.
- `--output-dir <directory>`: final output directory.
- `--lualatex <path-or-command>`: explicit LuaLaTeX executable.
- `--pdftoppm <path-or-command>`: explicit `pdftoppm` executable.

PNG generation is mandatory; a successful output contains non-empty
`poster.tex`, `poster.pdf`, and `poster.png`, plus copied themes and converted
figures. The build occurs in a sibling temporary directory, so a failed build
does not replace an existing final output.

## Lab survey poster generator (实验室调研, generate_lab_poster.py)

For 实验室调研 surveys use `scripts/generate_lab_poster.py` instead of the generic
path — it fills the repo poster template
(`<TEMPLATE_DIR>/main_template_lab_poster.tex`, source of truth;
fallback copy in `templates/`) with the DECK's 可视化分析 section-divider format:
full-bleed `slides-beamer/figures/background.png` (REQUIRED — fatal if missing;
if the deck lacks one, build it with
`paper-group-to-beamer/scripts/gen_viz_background.py --survey-dir "<LAB_DIR>"`)
+ FOUR white rounded shadow boxes (rows): 实验室调研+date pair / institute
block (brand-colour eyebrow + English line) / Prof. name / title_2+title_3 with
emph rule. NO metric row, NO blurb, NO lab-name line.

NOTE (2026-08-07 default change): the poster is the REQUIRED ARTIFACT for lab
dirs (the uploader fails closed without poster/poster.png), but the Bilibili
UPLOAD COVER defaults to the deck's FIRST SLIDE (video/cover.png) — do NOT
copy the poster over video/cover.png; keep the pipeline's slide-001 render.
See lab-survey-to-bilibili-runbook.

```bash
uv run --project "<SKILLS_DIR>/paper-video-cover" \
  "<SKILLS_DIR>/paper-video-cover/scripts/generate_lab_poster.py" \
  "<LAB_DIR>" --data "<LAB_DIR>/poster_data.json"
```

`--data` JSON: `title_1_pi` is REQUIRED (≤30 chars). Naming convention:
中文名 PI → `xxx教授`（如 `李飞飞教授`、`刘华平教授`）; 非教授角色不加
`Prof.`/`教授`（如 `Sergey Levine 等联合创始人`）; 英文名教授 →
`Prof. First Last`（如 `Prof. Yann LeCun`）.
`title_1_uni` optional (width budget 40 units, CJK glyph = 2 units, other =
1, e.g. `纽约大学` = 8, `Physical Intelligence` = 21; empty → line dropped),
`title_1_uni_color` optional (`#RRGGBB` — the institute's LOGO brand colour,
e.g. NYU `57068B`, Stanford `8C1515`, CMU `C41230`, Berkeley `003262`,
Tsinghua `660874`, SUSTech `2C5F7C`, HKUST `003366`; institutes without a
brand colour default to black `000000`),
`title_1_uni_en` optional (≤40 chars, e.g. `NEW YORK UNIVERSITY`) — the title
block renders the university as an **institute-brand-colour eyebrow** (25pt
semibold in `title_1_uni_color`, 0.25em CJK tracking auto-inserted by the
generator, side dashes 80×3px at 50% of the brand colour), the English small
line (13pt #8A8F98), then the Prof. name (55pt pink bold, single line). `title_2`/`title_3` optional (width budget 30 units each,
e.g. `从卷积网络到世界模型` = 18, `IEEE Fellow 2026` = 15; empty parts drop
their line). `date` (optional, default today) fills the date block. Corpus
stats from `papers.json` are informational only — a missing file degrades with
a warning, never fails the run. NO lab-name line, NO blurb line, NO metric row,
and NO `·` separators. Example:
`title_1_uni="纽约大学"`, `title_1_uni_en="NEW YORK UNIVERSITY"`,
`title_1_pi="Prof. Yann LeCun"`, `title_2="从卷积网络到世界模型"`,
`title_3="图灵奖得主的40年深度学习谱系"`. The upload title in
`video_meta.json` keeps the full `{机构缩写} {PI姓名}教授：主题 — Hook` format
independently. Poster layout (tikz rounded boxes with drop shadows over the
deck's 可视化分析 background): FOUR rows in a `0.6971\textwidth` container,
**absolutely centered** on the page (fixed top `0.107\textheight` / bottom
`0.103\textheight` offsets; stack ≈ 77% of the page): row 1 =
`实验室调研` + `〈DATE〉` pair (`0.3092\textwidth` text width each, 32pt, height
`0.1250\textheight`); row 2 = institute block — NYU Purple eyebrow (25pt
semibold, side dashes) + English line 13pt (`0.6706\textwidth`, height
`0.1250\textheight`); row 3 = Prof. name block (55pt pink bold single line,
`0.6706\textwidth`, height `0.1806\textheight`); row 4 = title_2/title_3 + rule
at 37pt (height `0.2153\textheight`). Gaps: horizontal `0.0258\textwidth` /
vertical `0.0417\textheight` (60 px both ways in the 2324×1440 reference
canvas).
`--scheme` default `bilibili`
(deck-matching); `--template`/`--theme-dir` override the repo paths (deck
`sustech-theme` is copied into the build). Token contract (fatal if unreplaced
on code lines): `〈DATE〉〈TITLE1UNI〉〈TITLE1UNIEN〉〈TITLE1PI〉〈TITLE2〉〈TITLE3〉`.
Compiles with xelatex (two passes; the deck theme is xelatex-only) and renders
`poster.png` at 300 dpi (32×20 cm page → ~3780×2363 px); output `<LAB_DIR>/poster/`.

**Gotcha — spaces in large title text**: TikZ nodes + `\fontsize{72}{84}` under
the sustech theme drop interword spaces (even `\ `); the generator therefore
converts plain spaces in `title_1/2/3` to `\hspace{0.25em}` glue (verified via
pdftotext: `NYU Prof. Yann LeCun` keeps its spaces).

**Gotcha — row centering and block widths**: (1) an `\hbox to \containerwidth`
is NOT a paragraph line and `\centering` will not center it — rows must be
`\hbox to \textwidth{\hss … \hss}` so the content centers inside the full line.
(2) tikz `text width` with a `\dimexpr`-based macro can raise `Dimension too
large` on the 32 cm paper — use literal widths (e.g. `0.44\textwidth`). (3) a
tikz node's outer width = `text width` + 2×`inner sep` — subtract the sep
padding from the width macros so box edges land exactly on the container.

**Gotcha — full-bleed background**: the poster geometry MUST be
`\geometry{papersize={32cm,20cm},margin=0cm}`. Any positive margin offsets
beamer's background-canvas origin to the text-area top, producing a white strip
across the top (~1.1 cm for `margin=1.1cm`) and clipping the background image's
top edge. Verify after every poster build: top/bottom 3% rows of `poster.png`
must have ~0 white pixels (PIL scan).

## Lab survey posters (实验室调研)

Chinese titles are supported (the generated preamble loads `ctex`; the beamer
title fallback no longer strips CJK). The poster title follows the upload-title
format `{机构缩写} {PI姓名}教授：主题 — Hook` (e.g.
`NYU 杨立昆教授：从卷积网络到世界模型 — 图灵奖得主的40年深度学习谱系` /
`清华刘华平教授：机器人具身智能 — 从视触觉到操作学习`). Run with
`--scheme bilibili` and a `--data` JSON:

```json
{
  "title_1_uni": "纽约大学",
  "title_1_uni_en": "NEW YORK UNIVERSITY",
  "title_1_uni_color": "57068B",
  "title_1_pi": "Prof. Yann LeCun",
  "title_2": "从卷积网络到世界模型",
  "title_3": "图灵奖得主的40年深度学习谱系",
  "date": "2026-08-06"
}
```

The palette source of truth is `<TEMPLATE_DIR>/sustech-theme/beamercolorthemesustech.sty`
(default blue / lab red / bilibili pink); the deck theme is copied into the
build and the frame compiles under xelatex (the deck's engine). The background
`slides-beamer/figures/background.png` must exist (the deck's 可视化分析 divider
background) — the generator fails closed without it.

Example with explicit tools:

```powershell
uv run --project "<SKILLS_DIR>/paper-video-cover" `
  "<SKILLS_DIR>/paper-video-cover/scripts/generate_poster.py" `
  "<paper_dir>" `
  --lualatex "C:/path/to/lualatex.exe" `
  --pdftoppm "C:/path/to/pdftoppm.exe"
```

Example with environment configuration:

```powershell
$env:LUALATEX = "C:/path/to/lualatex.exe"
$env:PDFTOPPM = "C:/path/to/pdftoppm.exe"
uv run --project "<SKILLS_DIR>/paper-video-cover" `
  "<SKILLS_DIR>/paper-video-cover/scripts/generate_poster.py" `
  "<paper_dir>"
```

## Inputs

The generator extracts title, venue, project URL, figures, and metrics from the
first MinerU markdown file under `md_output/*/auto/`. If caption-based extraction
finds no figures, it searches `slides-beamer/figures/`, `paper-source/image/`,
`source/image/`, `Figures/`, then `md_output/*/auto/images/`.

PNG, JPEG, and PDF sources are supported. PDFs use the resolved `pdftoppm`.
Missing, unsupported, empty, or unconvertible referenced figures are fatal.

All JSON fields are optional. `figure_map` paths are absolute or relative to the
paper directory:

```json
{
  "title": "Override Title",
  "venue": "CVPR 2025",
  "title_font": 220,
  "cards_col1": [],
  "cards_col2": [],
  "figures": {"col1": ["fig1"], "col2": ["fig2"]},
  "figure_map": {
    "fig1": "md_output/1234.5678/auto/images/figure-1.png"
  }
}
```

## Batch

Use a UTF-8 file with one paper directory per line; `start` and `count` are
optional positional arguments:

```powershell
uv run --project "<SKILLS_DIR>/paper-video-cover" `
  "<SKILLS_DIR>/paper-video-cover/scripts/batch_generate.py" `
  "<papers_file>" 0 20
```

The batch uses the uv-selected interpreter, requires all three artifacts for each
paper, and returns nonzero if any item fails.

## Failure behavior

The generator returns nonzero if a required executable or packaged theme is
missing, a child command returns nonzero, or a required artifact is missing or
empty. Treat any nonzero result as no publication; the failed temporary build is
removed and the previous final output remains unchanged.

## Related skills

- skill://lab-survey-to-bilibili-runbook
- skill://paper-group-to-beamer
- skill://lab-poster-deck-format
- skill://paper-bilibili-uploader
- skill://paper-lab-survey-to-bilibili
- skill://paper-to-bilibili
