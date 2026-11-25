---
name: paper-to-beamer
description: |
  Automated pipeline: paper (PDF or TeX source) → SUSTech Beamer slides (11-section 论文分享 structure) → compiled PDF.
  When TeX source is available, skip MinerU and extract content directly from LaTeX.
  Use when the user asks to create Beamer slides from an academic paper, or says "论文分享", "paper to slides", "make beamer from paper".
  Invoke with an absolute or relative path to a PDF, .tar.gz TeX archive, .tex file, or an arXiv URL/ID (source TeX is downloaded first via skill://paper-download-arxiv-paper-source).
user-invocable: true
argument-hint: "<input.{pdf,tar.gz,tex}|arxiv-url|arxiv-id>"
---

# Paper → Beamer Slides Pipeline

Given a paper (PDF or TeX source), produce a compiled SUSTech-themed Beamer presentation under
`论文分享/<VENUE> - <SHORT_TITLE>/`.


**Theme variant**: `\usetheme{sustech}` (lowercase, Variant A), from
`https://github.com/yhbcode000/sustech-slides-template.git`.
Do NOT use `\usetheme{SUSTech}` (Variant B, used in MT3) — it has different
macros and no section-separator pages.

**Default aspect ratio**: `aspectratio=1610` (16:10). Do NOT use 169 (16:9) —
1610 is preferred for laptop/projector compatibility and gives slightly more
vertical space for dense content.

**Bash runtime**: All shell commands run under the session's `bash` tool,
which on Windows is Git Bash. Unix-style `rm -rf`, `cp -r`,
`mkdir -p` are available. Working directory is set per-block via `cwd`.

## Requirements (COMPULSORY)

Every slide deck MUST satisfy these rules. No exceptions except where noted.

1. **No slide overflow (strict)** — all slides MUST compile without `Overfull \hbox` or `Overfull \vbox` warnings. Follow `skill://sustech-beamer-overflow`: single-column only, max 3 blocks + 1 callout, tables ≤5 columns with `\footnotesize`, no `\resizebox`. The ONLY exception is the index/TOC page (`\twopane` layout) — slight vertical overflow (`Overfull \vbox`) on the TOC frame is tolerated.

---

## Phase 1 — Setup directory

1. Accept `$ARGUMENTS` — a PDF path, `.tar.gz` TeX archive, or `.tex` file (absolute or relative from session cwd), or an arXiv URL / bare arXiv ID.
2. If the input is an arXiv URL or bare ID (matches `^\d{4}\.\d{4,5}(v\d+)?$` or contains `arxiv.org/(abs|pdf|e-print)/`), download the TeX source first:

   ```bash
   uv run --no-project python \
     "<SKILLS_DIR>/paper-download-arxiv-paper-source/scripts/download_source.py" \
     "<arxiv-ref>"        # default output = session cwd
   ```

   - If stdout ends with `TEX_SOURCES:`: derive `DIR_NAME` — venue from `\setsource{Venue}{Year}` in the extracted `paper_src/` TeX (fallback `\markboth`, then `arXiv <year>`); short title = first 1–3 significant words of `\title{...}` (fallback: ask the user, existing rule). Then `mkdir -p "论文分享/<DIR_NAME>"` and `mv arXiv-<id>.tar.gz paper_src "论文分享/<DIR_NAME>/"`.
   - If stdout ends with `PDF_ONLY: <path>`: the paper has no TeX source on arXiv — copy that PDF to `论文分享/<DIR_NAME>/` per the `.pdf` branch below (MinerU path applies, Phase 2 DECISION GATE unchanged).
   - If the command exits nonzero: stop and report the stderr message to the user.

3. Derive a short directory name `<VENUE> - <SHORT_TITLE>` (arXiv-input runs already derived it in step 2):
   - Strip `.pdf` / `.tar.gz` / `.tgz` / `.tex`, replace spaces/hyphens/special chars.
   - Ask the user for the name if venue/title are not inferrable from the
     filename.
   - Convention: existing examples are `SCIENCE ROBOTICS - HIL SERL`,
     `SCIENCE ROBOTICS - MT3`.
4. Create `论文分享/<DIR_NAME>/` and extract/copy the source there (arXiv-input runs already moved the archive + `paper_src/` in step 2):
   - `.tar.gz` / `.tgz`: extract with `tar -xzf` into `paper_src/`.
   - `.pdf`: copy directly to paper dir root.
   - `.tex`: copy source files into `paper_src/`.

---

## Phase 2 — Content extraction

**DECISION GATE**: If TeX source is available (`.tar.gz` archive containing `.tex`, or direct `.tex` file),
**skip MinerU entirely**. Read all content (title, authors, abstract, sections, tables, references)
directly from the TeX source using `read` — it's more accurate than MinerU output
and preserves table structures exactly.

**Only run MinerU when the input is a PDF with no TeX source available:**

```bash
"$MINERU_PYTHON" \
  "<SKILLS_DIR>/pdf-to-markdown/convert.py" \
  "论文分享/<DIR_NAME>/<pdf_filename>.pdf" \
  "论文分享/<DIR_NAME>/md_output" \
  --lang en
```

- English papers: `--lang en`.  Chinese/mixed: `--lang ch`.
- The wrapper prints `DONE -> ...md` on success.
- Output lands at `md_output/<name>/auto/<name>.md`.

If MinerU env is missing, stop and tell the user to install it per the
`pdf-to-markdown` skill preflight.

---

---

## Phase 3 — Install the packaged template

The promoted `paper-to-beamer` package is the primary, offline template source:

```bash
uv run --project "<SKILLS_DIR>/paper-to-beamer" python \
  "<SKILLS_DIR>/paper-to-beamer/scripts/copy_template.py" \
  --output "论文分享/<DIR_NAME>/slides-template"
```

This copies the verified `main_template.tex`, `latexmkrc`, and
`sustech-theme/` bundle. A network clone is never a fallback. Only when the
user explicitly requests a template refresh may the upstream repository be
cloned into a separate temporary directory for review before package release.

---

## Phase 4 — Create working dir and copy essentials

```bash
# cwd: $PP_ROOT
mkdir -p "论文分享/<DIR_NAME>/slides-beamer"
cp -r "论文分享/<DIR_NAME>/slides-template/sustech-theme" \
  "论文分享/<DIR_NAME>/slides-beamer/"
cp "论文分享/<DIR_NAME>/slides-template/latexmkrc" \
  "论文分享/<DIR_NAME>/slides-beamer/"
cp "论文分享/<DIR_NAME>/slides-template/main_template.tex" \
  "论文分享/<DIR_NAME>/slides-beamer/main.tex"
mkdir -p "论文分享/<DIR_NAME>/slides-beamer/figures"
```

**All subsequent edits target `slides-beamer/` only.**
`slides-template/` is kept pristine as a reference.

---

## Phase 5 — Read and extract content

**When TeX source available** (preferred — `.tar.gz` archive or `.tex` file):
read the main `.tex` from `paper_src/` directly using `read`. All content
(title, authors, abstract, sections, tables, references) is extracted from the
structured LaTeX source. Tables can be recreated directly from `tabular`
environments — no MinerU needed.

**When only Markdown available** (PDF-only input):
read `md_output/<name>/auto/<name>.md`. Extract these data points:
---

## Phase 6 — Fill `slides-beamer/main.tex`

**This is the core creative phase.** Read `main.tex` (copied from template),
then edit it section by section to replace every `\ph{…}` placeholder and
`\phfig` with real content from the Markdown.

Use the **HIL SERL example** as a filled-in style reference:
`论文分享/SCIENCE ROBOTICS - HIL SERL/slides-beamer/main.tex`.

### 6.0 Preamble metadata

- `\title[ACRONYM 论文分享]{Chinese descriptive title}` — Chinese title as main; short title MUST include "论文分享" suffix. Follow HIL SERL: `\title[HIL-SERL 论文分享]{...}`.
- `\subtitle{English original paper title}` — English original as subtitle.
- `\author[short]{…}` — full author list from paper.
- `\institute[short]{…}` — primary institutions.
- `\setsource{Venue}{Year}` — paper venue.
- `\setdomains{\domaintag{...}\domaintag{...}\domaintag{...}}` — 3-4 research domain tags displayed on the title page as colored pills. Tags MUST be in Chinese (e.g. `多智能体RL`, `LLM Agent`, `RL后训练`). English terms like `Multi-Agent RL`, `RL Post-Training` are NEVER allowed — they look inconsistent next to Chinese text and break the SUSTech theme's bilingual presentation style.
- `\setpresenter{$PRESENTER}` (default) or ask the user.
- `\setvenue{<venue location>}` (default: ask the user).
- 标题页出处脚注 `\creditline`（默认显示：`哔哩哔哩 · 白拾的物理AI组会 · github.com/yhbcode000/sustech-slides-template`）。公开分享/发布视频建议保留；汇报/答辩需要干净版式时在导言区加 `\hidecredits` 关闭，或 `\setcreditline{}` 置空、`\setcreditline{...}` 自定义文案。

Delete the placeholder-helper macros `\ph` and `\phfig` — they're no longer needed.

### 6.1 首页 (Title page)

The `\titlepage` frame stays as-is. Preamble metadata drives it.

### 6.2 📑 目录页（增强版 TOC）

The template now uses a two-pane `\twopane` layout (from the theme). The left pane contains a compact TOC via `{\tocdense\small\tableofcontents[hideallsubsections]}`. The right pane contains three blocks:

1. `\block{核心观察}` — 3-5 key metrics/insights from the paper
2. `\block{附录讨论}` — 3-5 appendix highlights (Oral signal, comparisons, method explainers)
3. `\callout[一句话概括]` — one-sentence paper summary

**The separate 论文信息 frame is DELETED**. Title/venue/authors are already in the preamble. The one-sentence summary lives in the TOC callout. No separate info frame needed.

**TOC spacing**: Use `{\tocdense\small\tableofcontents[hideallsubsections]}` — `\tocdense` (from theme) compacts the beamer TOC spacing. Prefix with `\vspace{-0.6em}` to pull content up closer to the title.

**Left margin**: The theme's `\tocdense` adds `\hskip2em` left margin for balanced TOC layout.
### 6.3 👤 作者介绍 — CROSS-VALIDATE ONLINE BEFORE WRITING

**CRITICAL: You MUST search online for author bios BEFORE writing this frame.**
Paper PDFs only provide names and affiliations — they lack Chinese names,
current positions, prior notable work, lab names, and recent recognitions.
Generic entries like "Tsinghua University, first author" are UNACCEPTABLE.

**Search procedure (execute BEFORE writing the frame):**
1. Write to `xd://web_search` with `{"query": "<first author> <institution> <paper domain>", "limit": 5}` — get Chinese name, current role, prior work, lab.
2. Write to `xd://web_search` with `{"query": "<corr author 1> <institution>", "limit": 5}` — same for each corresponding author.
3. Cross-reference at least 2 sources per author. Prefer personal homepages or Google Scholar.
4. Also search via `xd://web_search` with `{"query": "<institution> <lab/prof> <domain>", "limit": 5}` for lab context.

**What to extract from search results:**
- Chinese name (paper PDFs often lack Chinese characters)
- Current position (assistant prof? PhD student? industry? paper affiliation may be stale)
- Notable prior work (what is this person known for? e.g. MAPPO, RLinf, GRPO)
- Lab / group name (e.g. EDI Lab, NICS-EFC, RAIL)
- Recent recognitions (papers at top venues, awards, leadership roles)

**Fill the frame with telegraphic, sourced bios:**
```latex
\begin{frame}{作者介绍}
  \begin{block}{核心作者}
    \begin{itemize}
      \item \shl{<first author>}（<Chinese>）：<dept>, <role>。以 \keyword{<prior work>} 著称。在本文中<role>。
      \item 合作者来自 <institutions>，构成<description>团队。
    \end{itemize}
  \end{block}
  \tightgap
  \begin{block}{通讯作者}
    \begin{itemize}
      \item \shl{<corr 1>}（<Chinese>）：<position> @ <inst>，<lab> PI。研究方向为 \keyword{<f1>}、\keyword{<f2>}。<notable work>。本文<role>。
      \item \shl{<corr 2>}（<Chinese>）：<position> @ <inst>，<lab>。<notable>。本文<role>。
    \end{itemize}
  \end{block}
  \tightgap
  \begin{callout}[研究脉络]
    <team trajectory leading to this paper>。
  \end{callout}
\end{frame}
```

### 6.4 📋 背景与动机

Map to the `研究背景与动机` section in the template:
- Set `\renewcommand{\secblurb}{…}` (one-sentence summary) before `\section`.
- Fill bullet placeholders with telegraphic motivation from abstract/intro.
- Move the figure to a dedicated `[plain,c]` slide after this content slide: `\fitfigure{fig1_overview.jpg}` + `\figcap{1}{caption}`. Remove the `\begin{columns}` wrapper — this slide stays text-only.
- Fill `\metric{…}{…}` with up to 3 key numbers from the paper.

### 6.5 相关工作

Map to the `相关工作` section:
- Fill research areas from the paper's Related Work section.
- List actual baseline methods and their relationships.
- State the key differentiator in the callout.

If the paper has a clear "Related Work" section, use it. Otherwise
condense from scattered references in the introduction.

### 6.6 🔧 方法

Map to the `方法` section (2 frames: overview + core design).

**Frame 1 (Overview)**:
- List system components from the paper's method section.
- Move the figure to a dedicated `[plain,c]` slide after this content slide: `\fitfigure{fig2_system.jpg}` + `\figcap{2}{caption}`. Remove the `\begin{columns}` wrapper.

**Frame 2 (Core design)**:
- List up to 4 key design elements.
- Add one-line takeaway in the callout.

### 6.7 🧪 实验设计

Map to the `实验设计` section:
- List task categories/datasets.
- State evaluation protocol and baselines.
- Move the figure to a dedicated `[plain,c]` slide after this content slide: `\fitfigure{fig3_tasks.jpg}` + `\figcap{3}{caption}`. Remove the `\begin{columns}` wrapper.

### 6.8 📈 结果与分析

Map to the `实验结果` section (2 frames: main table + analysis).

**Frame 1 (Main table)**:
- Recreate the table with real data from the paper.
- Keep ≤5 columns, ≤6 rows.
- Highlight best results with `\shl{…}`.
- Use `\theadrow`, `\altrow`, `\thc{…}` with `booktabs`.
- One-line conclusion in the callout.

**Frame 2 (Analysis)**:
- Bullet-point analysis (3–4 observations).
- Analysis figure on a dedicated `[plain,c]` slide after the analysis bullets.

### 6.9 💡 要点总结

Map to the `要点总结` section (corresponds to "核心贡献"):
- 3 enumerated key takeaways.
- One-sentence summary in the callout.

### 6.10 ⚠️ 局限与讨论

Map to the `局限性` section:
- 3–4 limitations.
- Author-identified future directions in the callout.

### 6.11 📚 参考文献

Map to the `参考文献` frame:
- Fill `bibitem` entries with actual references from the paper.
- First `bibitem` should be the paper itself (marked `（本文）`).
- Include 3–5 key baselines.

### 6.12 💬 Q&A

Replace placeholder text in the Q&A frame with:
- Presenter name, institution, contact info.
- Keep the `Q&A` styling (`\fontsize{40}{44}` etc.).

### 6.13 Figures handling

For every placeholder that needs a figure:

1. **TeX source available** (preferred): copy figures from `paper_src/figures/`
   to `slides-beamer/figures/` with semantic names: `fig1_overview.pdf`,
   `fig2_system.pdf`, etc. TeX sources use vector `.pdf` figures — superior quality.
2. **Markdown available**: list images from `md_output/<name>/auto/images/`.
   Each is a hash-named `.jpg`. Pick the relevant figure by inspecting with
   `inspect_image` or from the markdown's `![](images/...)` references.
   is ONLY for content frames where the figure shares space with text.
5. Place the figure on its own dedicated slide — NEVER inside a `\begin{columns}` block:
   ```latex
   \begin{frame}[plain,c]
     \centering
     \includegraphics[height=0.92\textheight,width=\textwidth,keepaspectratio]{filename}
     \figcap{N}{caption text}
   \end{frame}
   ```


If a figure is missing or uncapturable, insert a placeholder callout instead
(the `\phfig` helper was deleted in 6.0, so do NOT reference it):

```latex
\begin{callout}[Figure]
  [Figure N: <description> — to be added]
\end{callout}
```

Note this in the Phase 8 report so the user knows to source the figure manually.

### 6.14 Writing style

- **Telegraphic**: keyword phrases, not full sentences. Bullets ≤2 lines.

- **TOC frame uses `\twopane` layout** (from theme): left pane = `{\tocdense\small\tableofcontents[hideallsubsections]}`, right pane = `\block{核心观察}` (3-5 key metrics) + `\block{附录讨论}` (3-4 appendix highlights) + `\callout[一句话概括]`. Thin vertical rule separates panes. NEVER use bare `\tableofcontents` or a separate 论文信息 frame.
- **No two-columns for figures**: AVOID `\begin{columns}` — every figure gets its own `[plain,c]` slide.
- **Figures on own slides**: `\includegraphics[height=0.92\textheight,width=\textwidth,keepaspectratio]{...}` + `\figcap{N}{caption}`.

### 6.15 Historical-view appendix slide (MANDATORY — NEVER SKIP)

EVERY deck MUST include a final appendix slide placing the paper's key method/contribution in a broader historical arc.

**Step 1 — Search 论文调研 (REQUIRED)**:
1. Use the built-in `grep` tool over
   `$PP_ROOT/论文调研/` for the main method name and 1–2
   spelling variants. Do not invoke shell grep.
2. Read at least 2-3 matching survey Markdown files for detailed context:
   `论文调研/<survey>/md_output/<name>/auto/<name>.md`

**Step 2 — Construct the timeline** (3 phases):
- Origin: the current paper (year + venue + what was proposed)
- Scaling: follow-up work that scaled/adapted the method (year + paper name)
- Downstream adoption: how the method is used in downstream fields
  (year range + representative works, sourced from survey papers)

**Step 3 — Insert the slide** as the LAST appendix frame before `\end{document}`, using this exact template:

```latex
% --- H: METHOD 历史视角 -----------------------------------------------------
\begin{frame}{附录 H —— METHOD 的历史贡献}
  \small
  \begin{block}{METHOD 的诞生与传播}
    \begin{itemize}\setlength{\itemsep}{0.15em}
      \item YEAR — \shl{OriginPaper}：first proposal, what it solved.
      \item YEAR — \shl{ScalingWork}：scaled/adapted to broader domain.
      \item YEAR–YEAR — \shl{Downstream Community}：adoption in VLA/robotics/
        world-models. Representative works: A, B, C.
    \end{itemize}
  \end{block}
  \tightgap
  \begin{block}{为何 METHOD 对 DOWNSTREAM 至关重要}
    \begin{itemize}\setlength{\itemsep}{0.15em}
      \item \shl{Property 1}：explanation.
      \item \shl{Property 2}：explanation.
      \item \shl{Property 3}：explanation.
    \end{itemize}
  \end{block}
  \tightgap
  \begin{callout}[历史定位]
    METHOD 从 ORIGIN (YEAR) $\to$ SCALING (YEAR) $\to$ DOWNSTREAM (YEAR–YEAR)，
    完成从 DOMAIN_A 到 DOMAIN_B 的技术迁移。
  \end{callout}
  {\fontsize{6}{7}\selectfont\color{sustechgrey}
    Ref: OriginPaper (arXiv:XXXX, YEAR); ScalingWork (arXiv:XXXX, YEAR);
    SurveyRef (Authors, YEAR); DownstreamA; DownstreamB.}
\end{frame}
```


**Sizing rules**:
- Use `\small` for the frame body.
- Use `\setlength{\itemsep}{0.15em}` in every `itemize`.
- Keep each bullet to 1 line max.
- Ref line uses `\fontsize{6}{7}\selectfont` (very compact, fits 3+ citations).
- **Frame title MUST be short**: ≤ 30 characters including "附录 H —— " prefix. Drop the subtitle ("从 ORIGIN_DOMAIN 到 DOWNSTREAM") — the content blocks carry that information. Long titles cause persistent line-wrap overflow in the SUSTech frametitle.
- If still overflowing (check with compile), merge two blocks into one or shorten bullet text — but NEVER drop this slide entirely.



### 6.16 Oral signal analysis appendix slide (MANDATORY — NEVER SKIP)

EVERY deck MUST include this appendix slide. Evaluate the paper's innovation
patterns regardless of whether it actually earned Oral/Spotlight status.

Analyze the paper using the ResearchStudio-Idea framework
(Zhao, Huang et al., arXiv 2607.04439 — 1,947-paper analysis, 15 innovation
patterns). Map the paper's contributions to 2-3 of the 15 patterns and cite
the specific ablation/efficiency/OOD evidence that proves execution quality.

**Step 1 — Read the 15 patterns when available**:
If
`$PP_ROOT/系统课程/顶会写作指南课程/slides-beamer/main.tex`
exists, read it before writing this optional enrichment frame and use its
current P1–P15 descriptions. If the course deck is absent, omit the
Oral-signal enrichment instead of guessing or failing the paper deck.

**Step 2 — Map 2–3 patterns to the paper**:
For each pattern, extract SPECIFIC quantitative evidence from the paper that
proves execution quality:
- Ablation numbers (component removal → performance degradation)
- Efficiency metrics (speed, compute, parameter count)
- OOD generalization (unseen domains/tasks where method still works)
- Monotonic scaling (performance vs data/compute curves without plateau)

**Step 3 — Insert the slide** BEFORE the historical-view slide, using this template:

```latex
% --- C: METHOD Oral 信号分析 -------------------------------------------------
\begin{frame}{附录 C —— METHOD 的Oral信号分析}
  \small
  \begin{block}{METHOD 命中的创新模式及Oral证据}
    \begin{enumerate}\setlength{\itemsep}{0.1em}
      \item \shl{<P1_NAME>}（<P1_STAT>）：\\
        <one-line mapping of paper idea to pattern>。\\
        \textbf{Oral验证}：<specific quantitative evidence>。
      \item \shl{<P2_NAME>}：\\
        <one-line mapping>。\\
        \textbf{Oral验证}：<evidence>。
      \item \shl{<P3_NAME>}：\\
        <one-line mapping>。\\
        \textbf{Oral验证}：<evidence>。
    \end{enumerate}
  \end{block}
  \tightgap
  \begin{callout}[Oral关键因素]
    <one-line synthesis of why execution quality earned Oral or would have>。
  \end{callout}
  {\fontsize{6}{7}\selectfont\color{sustechgrey}
    Ref: Zhao, Huang et al., ResearchStudio-Idea (arXiv 2607.04439, 2026);
    <AUTHOR_SHORT>, <METHOD> (<VENUE> <YEAR>).}
\end{frame}
```

**Sizing rules**:
- Use `\small` for the frame body.
- Use `\setlength{\itemsep}{0.1em}` in `enumerate`.
- Each pattern entry ≤ 3 lines (name + mapping + evidence).
- Ref line uses `\fontsize{6}{7}\selectfont` (compact, fits 2+ citations).
- If overflowing, shorten evidence text — NEVER drop this slide.
- **Oral appendix frame title ≤ 25 chars**: "附录 C —— METHOD 的Oral信号分析" is the maximum. Do NOT append subtitles or domain qualifiers after the method name. Overflow here is a persistent bug.

**Step 4 — PC vs Society classification (MANDATORY — NEVER SKIP)**:

After inserting the oral signal slide, classify the paper's contribution as PC-aligned
or Society-aligned based on the ResearchStudio-Idea 大局观 3 finding that **PC and
community evaluation are nearly orthogonal** (程序委员会和社区的评价几乎正交):

| PC values (🏆) | Society values (🎓) |
|---|---|
| 结构性洞察 (structural insight) | 可复用基础设施 (reusable infrastructure) |
| 紧度证明 (tightness proofs) | 跨领域适用性 (cross-domain applicability) |
| 验证，不是假设是实测 | 大规模受控实验 |

**Classification rule**:
- **PC (🏆)**: contribution centers on structural insight + tightness proof +
  verification. The paper *proves* something rigorously, reframes a problem to
  expose hidden structure, or characterizes and surpasses a formal limit.
  Key signal: "we measured it, it's real" not "we can reasonably assume."
- **Society (🎓)**: contribution centers on reusable infrastructure + cross-domain
  applicability + large-scale experiments. The paper *builds* something others will
  use — a unified representation space, a diagnostic framework, a liberated
  component — and demonstrates it works across domains.
  Key signal: high downstream adoption potential, community builds on it.
- **Both (🥇)**: contribution satisfies BOTH value axes (rare "双赢").
  The paper provides structural insight AND creates reusable infrastructure.
  Example: P6 Reframe as Solvable Object (Δ_OR=+2.9pp, Δ_OH=+7.1pp — both PC
  and community positive). Key signal: the same contribution is both a rigorous
  insight AND something others will build on.
Emit a machine-readable comment on the line immediately after the oral signal
appendix slide's `\end{frame}` (before the blank line that separates it from the
next slide):

```latex
\end{frame}
% PREFERENCE: pc
```

or:

```latex
\end{frame}
% PREFERENCE: society
```

or:

```latex
\end{frame}
% PREFERENCE: both
```

This comment is parsed by the paper-slides-to-video pipeline to inject a 🏆, 🎓, or 🥇
emoji into the Bilibili video title.

---
## Phase 7 — Compile

```bash
# cwd: $PP_ROOT/论文分享/<DIR_NAME>/slides-beamer
latexmk -xelatex main.tex
```

On success: copy `main.pdf` → `../<DIR_NAME>.pdf` at the paper dir root
(matching the HIL SERL convention).

Post-compile checks (use the **built-in `grep` tool**, not shell `grep`):

- Grep `main.log` for `Overfull \\hbox` — report count.
- Grep for `Undefined control sequence` — flag if any.
- Report: page count, build status.


## Phase 7.5 — Extract venue and rename directory

Many papers are published at venues (ICML, RSS, CoRL, etc.) not listed in
the README. The preamble should already contain `\setsource{Venue}{Year}`.
After compilation, extract this venue and rename the paper directory if it
still uses the default "arXiv" prefix.

**Extract venue** from the compiled `.tex` preamble:
```bash
uv run --project "<SKILLS_DIR>/paper-to-beamer" python - \
  "<PAPER_DIR>/slides-beamer/main.tex" <<'PY'
import re
import sys
from pathlib import Path

tex_path = Path(sys.argv[1])
if not tex_path.is_file():
    raise SystemExit(f"main.tex not found: {tex_path}")
main_tex = tex_path.read_text(encoding="utf-8")
match = re.search(r'\\setsource\{([^{}]+)\}\{([^{}]+)\}', main_tex)
if match is None:
    raise SystemExit(r"no \setsource{venue}{year} declaration found")
print(f"{match.group(1)} {match.group(2)}")
PY
```

If the extracted venue differs from the current directory prefix (for example,
`arXiv` → `ICRA 2026`), rename the paper directory and its root PDF to match.
The short title must use a recognizable acronym or at least two meaningful
title keywords. For batch processing, update `papers.json` and `state.json`
paths after the move.

---

## Phase 7.6 — Index slides with section-based numbering

After successful compilation, add section-based frame numbering (§.N format)
so the audience can follow the presentation structure:

```js
// Run in eval (js) — section-based slide numbering
// Reads main.tex, numbers frames as "section.frame", then re-compiles

const fs = await import('node:fs');
const path = await import('node:path');

const texPath = (process.env.PP_ROOT || '.') + '/论文分享/<DIR_NAME>/slides-beamer/main.tex';
let text = fs.readFileSync(texPath, 'utf-8');

let sectionNum = 0; // 0 = before first section (no numbering)
let frameInSection = 0;

const lines = text.split('\n');
const result = [];

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];

  // Detect \section{} commands — increment section counter
  const secMatch = line.match(/\\section\{([^}]*)\}/);
  if (secMatch) {
    if (sectionNum === 0) sectionNum = 1;
    else sectionNum++;
    frameInSection = 0;
    result.push(line);
    continue;
  }

  // Detect \begin{frame}{Title} — prepend section.frame number
  const frameMatch = line.match(/^(\\begin\{frame\})\{(.+)\}/);
  if (frameMatch) {
    frameInSection++;
    let title = frameMatch[2].replace(/^\d+\.\d*\s*/, ''); // strip existing number

    if (sectionNum === 0) {
      // Before first section — keep original title unnumbered (TOC, etc.)
      result.push(`\\begin{frame}{${title}}`);
    } else {
      result.push(`\\begin{frame}{${sectionNum}.${frameInSection} ${title}}`);
    }
    continue;
  }

  result.push(line);
}

fs.writeFileSync(texPath, result.join('\n'), 'utf-8');
console.log(`Indexed: sections up to ${sectionNum}`);
```

After running the script, re-compile:

```bash
# cwd: $PP_ROOT/论文分享/<DIR_NAME>/slides-beamer
latexmk -xelatex -g main.tex
```

**Rules**:
- Frames before the first `\section{}` stay unnumbered (title page, TOC).
- Each `\section{}` starts a new section counter; frames within get `§.N` prefix.
- If a title already has a numbering prefix, it's stripped before renumbering (idempotent).
- NEVER use `\setbeamertemplate{frametitle}` — it breaks the SUSTech theme styling.
- This phase runs AFTER the initial compile succeeds, and the re-compile must also succeed.

## Phase 8 — Report

Tell the user:

- Directory: `论文分享/<DIR_NAME>/`
- Output: `slides-beamer/main.pdf` + `../<DIR_NAME>.pdf`
- Slide count
- Any figure placeholders (callout boxes with "to be added")
- Any compilation warnings

## Related skills

- skill://paper-download-arxiv-paper-source
- skill://paper-slides-to-video
- skill://sustech-beamer-overflow
- skill://batch-papers-full-pipeline
- skill://batch-papers-single-omp-full-pipeline
- skill://batch-papers-to-beamer-omp
