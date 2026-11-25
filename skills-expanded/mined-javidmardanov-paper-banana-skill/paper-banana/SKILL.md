---
name: paper-banana
description: >-
  Generates publication-ready academic illustrations using the PaperBanana
  five-agent pipeline (arXiv:2601.23265). Diagram mode runs 5 VLM/image-model
  agents (Gemini by default; OpenAI, Anthropic, OpenRouter supported) with
  multimodal in-context learning from curated reference images, venue style
  packs, and an improve-existing-figure mode. Plot mode generates executable
  Python matplotlib/seaborn code sized to the venue's column width.
  Use when the user asks for: research paper figures, academic diagrams,
  methodology illustrations, architecture diagrams, statistical plots,
  conference-quality visualizations, flowcharts for papers, NeurIPS/ICML/CVPR
  figures, or improving existing paper figures.
license: MIT
compatibility: >-
  Python 3.10+, network access to the Gemini API, and GOOGLE_API_KEY or
  GEMINI_API_KEY set. Needs google-genai>=2, matplotlib, seaborn, numpy, pillow.
metadata:
  version: "1.2.0"
  paper: "arXiv:2601.23265"
---

# PaperBanana: Academic Illustration Pipeline

Automates publication-ready academic illustrations via 5 specialized agents, each a separate call to the configured VLM or image model (Gemini by default):
**Retriever** (categorize & select references) -> **Planner** (multimodal description) -> **Stylist** (polish) -> **Visualizer** (render) -> **Critic** (evaluate & refine).

Two output modes:
- **DIAGRAM MODE**: Each agent is a Python script calling the configured VLM / image model. Run `scripts/orchestrate.py` for end-to-end execution.
- **PLOT MODE**: Statistical plots generated as executable Python matplotlib/seaborn code (code-based to eliminate data hallucination).

**Requirements**: Python 3.10+ with `google-genai>=2`, `matplotlib`, `seaborn`, `numpy`, `pillow`, and an API key for the provider in use (default Gemini: `GOOGLE_API_KEY` or `GEMINI_API_KEY`). Optional: `openai` (for `openai/...` and `openrouter/...` models), `anthropic`, `pypdf` (PDF input).

**Models**: named `provider/model`; unprefixed names are inferred. Defaults are `gemini-3.5-flash` (Retriever/Planner/Stylist/Critic) and `gemini-3-pro-image` (Visualizer, "Nano Banana Pro"). Override with `PAPERBANANA_VLM_MODEL` / `PAPERBANANA_IMAGE_MODEL` or the orchestrator's `--vlm-model` / `--image-model` flags.

| Provider | Key | Reasoning | Image | Examples |
|----------|-----|-----------|-------|----------|
| gemini (default) | `GOOGLE_API_KEY` | yes | yes | `gemini-3.5-flash`, `gemini-3.1-flash-lite`, `gemini-3-pro-image`, `gemini-3.1-flash-image` |
| openai | `OPENAI_API_KEY` | yes | yes | `openai/gpt-5.5`, `openai/gpt-5.4-mini`, `openai/gpt-image-2`, `openai/gpt-image-1.5` |
| anthropic | `ANTHROPIC_API_KEY` | yes | no | `anthropic/claude-opus-5`, `anthropic/claude-sonnet-5` |
| openrouter | `OPENROUTER_API_KEY` | yes | yes | `openrouter/google/gemini-3.5-flash`, `openrouter/google/gemini-3-pro-image` |

If the user names a provider or model, pass it via `--vlm-model` / `--image-model`. If a run fails with a missing-key or model error, run `python scripts/validate_output.py --check-api` and report which key or model is the problem.

Paper: *PaperBanana: Automating Academic Illustration for AI Scientists* (arXiv:2601.23265, Google/PKU). Official code: https://github.com/dwzhu-pku/PaperBanana

---

## Step 1: Determine Output Mode

Decide which track to follow:

| Signal | Mode |
|--------|------|
| User provides raw data, table, CSV + visual intent (bar chart, scatter, etc.) | **PLOT MODE** |
| User provides methodology text, description, or figure caption | **DIAGRAM MODE** |
| User provides existing figure to improve | Match original type |

**Critical rule**: PLOT MODE always generates Python code (never image generation for data visualizations). Code-based generation eliminates data hallucination errors that corrupt numerical accuracy in image-based approaches.

---

## Step 2: Execute Pipeline

### DIAGRAM MODE — Automated Pipeline

**Primary entry point**: Run the end-to-end orchestrator:

```bash
python scripts/orchestrate.py \
  --methodology-file methodology.txt \
  --caption "Figure 1: Overview of proposed framework" \
  --mode diagram \
  --output output/diagram.png
```

Useful flags (combine as needed):

| Flag | Use when |
|------|----------|
| `--methodology-file paper.pdf --pages 3-5` | The user gives a PDF (or `.tex`); page ranges keep only the method section |
| `--venue icml --figure-width single` | The user names a venue or column width. Venues: neurips (default), iclr, icml, cvpr, acl, aaai |
| `--num-candidates 4` | Quality matters more than cost: renders 4 images in parallel, the Critic keeps the best |
| `--input-image old_figure.png` | The user wants an existing figure improved (Planner sees it, Visualizer edits it) |
| `--image-size 4K` | Print-quality output (default 2K) |
| `--resume` | Re-render after a failed or unsatisfying image step without re-running Retriever/Planner/Stylist |
| `--vlm-model` / `--image-model` | The user asks for a specific provider or model |

Or with inline text:
```bash
python scripts/orchestrate.py \
  --methodology "Our framework consists of three modules..." \
  --caption "Figure 1: System overview" \
  --mode diagram \
  --output output/diagram.png
```

The orchestrator chains all 5 agents automatically and handles the Critic's refinement loop (up to 3 iterations). Intermediate outputs, including every Visualizer attempt (`diagram_iter{N}[_c{K}].png`), are saved to `output/work/`; the best-scoring image is copied to `--output`. The run ends with a per-model token/image usage summary; relay it to the user.

#### Pipeline Details

Read `references/DIAGRAM-PROMPTS.md` for the actual Gemini prompt templates used by each agent.

**Phase 1: RETRIEVER** (`scripts/retriever.py`) — VLM call
- Classifies methodology into 1 of 4 categories from `references/DIAGRAM-CATEGORIES.md`
- Selects 2 most relevant reference diagrams from the 13 curated examples in `assets/references/`
- Identifies visual intent: Framework Overview, Pipeline/Flow, Detailed Module, Architecture Diagram

**Phase 2: PLANNER** (`scripts/planner.py`) — Multimodal VLM call
- Sends the 2 selected reference images + methodology text to Gemini as a multimodal prompt
- The VLM "sees" what good methodology diagrams look like (in-context learning from images)
- Generates an extremely detailed textual description of the target diagram
- With `--input-image`, the existing figure is attached too and the Planner must preserve its content while improving layout and legibility
- **Critical**: Natural language only for all visual attributes. NEVER hex codes or pixel dimensions

**Phase 3: STYLIST** (`scripts/stylist.py`) — VLM call
- Takes the Planner's description + full NeurIPS 2025 style guide + the target venue's typeset width and notes (`--venue`, `--figure-width`; data in `assets/venues.json`)
- Applies domain-specific styling based on the category from Phase 1
- Follows 5 critical rules: preserve aesthetics, intervene minimally, respect domain, enrich details, preserve content
- Outputs the polished description only

**Phase 4: VISUALIZER** (`scripts/generate_image.py`) — Image model call
- Renders the styled description with the configured image model: `gemini-3-pro-image` (Nano Banana Pro) by default; `openai/gpt-image-2`, `gemini-3.1-flash-image`, or an OpenRouter image model via `--image-model`
- With `--input-image`, the existing figure is passed as the edit source instead of generating from scratch
- With `--num-candidates N`, N images are rendered in parallel and all are scored by the Critic; the best is kept
- Prepends quality prefix (high-res, legible text, clean background, no watermarks)
- Aspect ratio selected based on visual intent (16:9 for pipelines, 3:2 for modules); output resolution 2K by default

**Phase 5: CRITIC** (`scripts/critic.py`) — Multimodal VLM call
- Sends the generated image + methodology text to Gemini for multimodal evaluation
- Scores on 4 dimensions (faithfulness, readability, conciseness, aesthetics)
- If faithfulness < 7 OR readability < 7: generates revised description → loops to Phase 4
- Maximum 3 refinement iterations

---

### DIAGRAM MODE — Manual Execution

You can also run each agent individually for more control:

```bash
# Phase 1: Retriever
python scripts/retriever.py --methodology-file text.txt --output work/retriever.json

# Phase 2: Planner (add --input-image old.png to improve an existing figure)
python scripts/planner.py --methodology-file text.txt --caption "Figure 1: ..." \
  --references work/retriever.json --output work/planner.json

# Phase 3: Stylist (venue defaults to neurips)
python scripts/stylist.py --description work/planner.json --venue icml --figure-width single \
  --output work/stylist.json

# Phase 4: Visualizer (extract styled_description from JSON, pass to generate_image.py;
# add --reference-image old.png to edit an existing figure, --model openai/gpt-image-2 to switch renderer)
python scripts/generate_image.py --prompt-file work/styled_desc.txt --aspect-ratio 16:9 \
  --image-size 2K --output output/diagram.png

# Phase 5: Critic
python scripts/critic.py --image output/diagram.png --methodology-file text.txt \
  --description work/stylist.json --output work/critic.json
```

---

### PLOT MODE

Read `references/PLOT-PROMPTS.md` for detailed agent prompts. Read `references/PLOT-STYLE-GUIDE.md` for aesthetic rules.

Plot mode uses the host agent for reasoning and code generation — no image-model API calls are needed for plot generation itself.

#### Phase 1: CATEGORIZE (Retriever)

Match data characteristics and visual intent:

| Data Type | Plot Types |
|-----------|------------|
| Categorical comparison | Bar chart, grouped bar, stacked bar |
| Continuous trends | Line chart, area chart |
| Correlation/distribution | Scatter plot, histogram, box plot, violin |
| Matrix/similarity | Heatmap, confusion matrix |
| Multi-dimensional | Radar/spider chart |
| Proportional | Pie/donut chart, treemap |

#### Phase 2: PLAN (Planner)

Create a detailed specification that explicitly enumerates:
- Every raw data point with exact coordinates/values
- Axis ranges, labels, tick marks, scales (linear/log)
- Color assignments for each series/category
- Font sizes for title, axis labels, tick labels, legend
- Line widths, marker sizes, marker shapes
- Legend placement and formatting
- Grid style (major/minor, dashed/solid)
- Figure dimensions and DPI

#### Phase 3: STYLE (Stylist)

Read `references/PLOT-STYLE-GUIDE.md` for NeurIPS 2025 plot aesthetics.

Key styling rules:
- White backgrounds only
- Colorblind-friendly palettes (see `assets/palettes/colorblind_safe.json`)
- Sans-serif fonts (Helvetica, Arial, or DejaVu Sans)
- Markers on line charts for print readability
- Inward-facing tick marks
- Subtle grid lines (light gray, dashed)

#### Phase 4: VISUALIZE (Visualizer — Code Generation)

Generate complete, self-contained Python matplotlib/seaborn code. Use `scripts/plot_generator.py` as a reference implementation or run it directly with a JSON config:

```bash
python scripts/plot_generator.py --config plot_config.json --venue icml --width single --output figure.pdf
```

`--venue` and `--width` size the figure to the venue's column (`single`) or text (`double`) width from `assets/venues.json`; use the same widths for `figsize` when writing custom code.

Code requirements:
- Self-contained: all data defined inline, no external file dependencies
- Apply `.mplstyle` from `assets/matplotlib_styles/academic_default.mplstyle`
- Set `OUTPUT_PATH` variable for output file location
- 300 DPI, `bbox_inches='tight'`
- No `plt.show()` — save only
- Support both PDF and PNG output

After generating the code, execute it to produce the plot image.

#### Phase 5: CRITIQUE (Critic)

Same rubric as diagram mode, plus plot-specific checks:
- Data fidelity: Every data point correctly plotted
- Axis accuracy: Ranges, labels, scales match specification
- Layout: No overlapping labels, legends, or data points
- Code correctness: Syntax valid, imports available, output saved

If code execution failed, analyze the error, simplify the approach, and regenerate.

---

## Quick Start Examples

**Diagram (automated)**: Run `scripts/orchestrate.py` with your methodology text file and caption.

**Diagram (via agent)**: "Generate a methodology diagram for my transformer architecture. Here is the methodology section: [paste text]. Caption: Overview of our proposed multi-head attention framework."

**Plot**: "Create a bar chart comparing model performance. Data: {BERT: 92.3, GPT-4: 88.1, Claude: 95.7, Gemini: 91.2}. Intent: F1 score comparison across language models."

**Improve**: "Improve this figure: [attach image] using this methodology: [paste text]" → run `scripts/orchestrate.py --input-image figure.png --methodology-file text.txt`.

**From a paper**: "Make the method figure for paper.pdf" → `scripts/orchestrate.py --methodology-file paper.pdf --pages 3-5` (ask for or infer the method-section pages).

**Other provider**: "Use GPT Image for rendering" → add `--image-model openai/gpt-image-2` (needs `OPENAI_API_KEY`).

---

## File Reference

| File | Purpose | When to Read |
|------|---------|-------------|
| `scripts/orchestrate.py` | End-to-end pipeline runner | Diagram mode primary entry point |
| `scripts/providers.py` | Gemini / OpenAI / Anthropic / OpenRouter adapters, model routing, usage tracking | When a provider or key error needs diagnosing |
| `scripts/common.py` | Input loading (.txt/.tex/.pdf), venue lookup, re-exports of providers | Imported by all diagram scripts |
| `scripts/retriever.py` | VLM-based reference selection | Phase 1 (diagram mode) |
| `scripts/planner.py` | Multimodal description generation | Phase 2 (diagram mode) |
| `scripts/stylist.py` | VLM-based style application | Phase 3 (diagram mode) |
| `scripts/generate_image.py` | Gemini Image API call | Phase 4 (diagram mode) |
| `scripts/critic.py` | VLM-based image evaluation | Phase 5 (diagram mode) |
| `scripts/plot_generator.py` | Template-based matplotlib generator | Phase 4 (plot mode) |
| `scripts/validate_output.py` | Output validation and dependency check | Post-generation validation |
| `references/DIAGRAM-PROMPTS.md` | Actual Gemini prompt templates for diagrams | All diagram phases |
| `references/PLOT-PROMPTS.md` | Agent prompts for plots | All plot phases |
| `references/DIAGRAM-STYLE-GUIDE.md` | NeurIPS 2025 diagram aesthetics | Phase 3 (Style) |
| `references/PLOT-STYLE-GUIDE.md` | NeurIPS 2025 plot aesthetics | Phase 3 (Style) |
| `references/EVALUATION-RUBRIC.md` | Critic scoring criteria (4 dimensions) | Phase 5 (Critique) |
| `references/DIAGRAM-CATEGORIES.md` | 4 diagram categories with keywords | Phase 1 (Categorize) |
| `assets/references/index.json` | 13 curated reference diagram metadata | Phase 1 (Retriever) |
| `assets/references/*.jpg` | 13 curated reference diagram images | Phase 2 (Planner multimodal input) |
| `assets/venues.json` | Column/text widths and style notes per venue | Phase 3 (Style) and plot sizing |
| `assets/palettes/*.json` | Color palette definitions | Phase 3 (Style) |
| `assets/matplotlib_styles/*.mplstyle` | Matplotlib style sheets | Phase 4 (plot mode) |

## Environment Setup

```bash
# Default provider (Gemini) for all agents
export GOOGLE_API_KEY="your-api-key-here"   # GEMINI_API_KEY also works

# Optional: other providers (install with: pip install openai anthropic)
export OPENAI_API_KEY="..."        # openai/gpt-5.5, openai/gpt-image-2, and openrouter/... via OPENROUTER_API_KEY
export ANTHROPIC_API_KEY="..."     # anthropic/claude-opus-5 (reasoning agents only)

# Optional: swap models (defaults shown). Cheaper: gemini-3.1-flash-lite / gemini-3.1-flash-image
export PAPERBANANA_VLM_MODEL="gemini-3.5-flash"
export PAPERBANANA_IMAGE_MODEL="gemini-3-pro-image"

# Install dependencies (add pypdf for PDF input)
pip install "google-genai>=2" matplotlib seaborn numpy pillow
```

Verify setup: `python scripts/validate_output.py --check-deps --check-api` (checks packages, the API keys, and that both configured models are reachable).
