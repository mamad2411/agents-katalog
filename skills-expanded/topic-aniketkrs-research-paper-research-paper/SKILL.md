---
name: research-paper
description: Enterprise-grade autonomous research paper generation skill for AI coding agents — full papers, literature reviews, theses, whitepapers, surveys, policy briefs — with rigorous methodology, statistical validation, multi-style citations (Harvard / APA / IEEE / MLA / Chicago / Nature / arXiv-numeric), and rich visualizations. Activates on slash commands (`/research`, `/paper`, `/literature-review`, `/whitepaper`, `/thesis`, `/survey`, `/policy`) and on natural-language academic-writing requests. Runtime-neutral — works with Claude Code, OpenCode, Cursor, Cline, Codex, Aider, Amp, Antigravity, and 50+ agents via the `npx skills` installer.
license: MIT
version: 2.4.0
---

# Research Paper

A production-grade agent skill that turns any compatible coding agent
(Claude Code, OpenCode, Cursor, Cline, Codex, Aider, Amp, Antigravity,
and 50+ others) into a **multi-agent research system**:

> Orchestrator → Researcher → Methodologist → Analyst → Visualizer
> → Writer → Citation engine → Validator → Reviewer → Publisher.

It produces full, citation-heavy, visually rich, publication-ready outputs in
**arXiv / IEEE / ACM / Nature / Harvard** styles, plus literature reviews,
theses, technical whitepapers, survey papers, and policy briefs.

This file is the **entry point**. It is intentionally compact. Heavier
guidance (instructions, workflows, engines, validators, rubrics) lives in
the topic folders below and is loaded **on demand** via Claude Code's
filesystem tools (progressive disclosure).

---

## 1. When to activate

### Slash commands (preferred)

| Command                | What it does                                       |
| ---------------------- | -------------------------------------------------- |
| `/research <topic>`     | Full empirical research paper                      |
| `/paper <topic>`        | Same as `/research`, more permissive               |
| `/literature-review <topic>` | Systematic / scoping / narrative literature review |
| `/whitepaper <topic>`   | Industry / technical whitepaper                    |
| `/thesis <topic>`       | Thesis / dissertation chapter                      |
| `/survey <topic>`       | State-of-the-art / survey paper                    |
| `/policy <topic>`       | Policy brief or full policy paper                  |

Common options (any command):
`--style [harvard|apa|ieee|mla|chicago|nature|arxiv-numeric]`,
`--format [arxiv|ieee|acm|nature|harvard|...]`,
`--depth [quick|standard|comprehensive]`,
`--sources [N]`,
`--visualizations [auto|N|none]`,
`--audience [academic|technical|executive|general]`.

### Natural-language triggers

- "Write a research paper / academic paper / scientific paper on …"
- "Do a literature review / systematic review on …"
- "Format this draft as IEEE / ACM / arXiv / Nature / Harvard / APA …"
- "Write a thesis chapter / dissertation chapter on …"
- "Produce a whitepaper / survey paper / policy brief on …"
- "Analyze this dataset and write up the findings as a paper."
- "Add citations / bibliography / references in `<style>`."
- "Peer-review this draft / validate the methodology."

### Do NOT activate for

Blog posts, marketing copy, tweets, casual answers, or single-paragraph
explanations. Those are handled normally without this skill.

---

## 2. Operating principles (read every time)

0. **Anchor to TODAY's date FIRST.** Before any planning, search,
   or writing, determine today's actual date — via system clock
   (`date -u +%Y-%m-%d`), runtime context, or asking the user.
   **Never default silently to the training-data cutoff.** Year
   ranges (`--years last-3`) are computed from today, not from
   the model's training year. Full protocol:
   `instructions/freshness.md`.
1. **Plan before writing.** Always start with the research plan in
   `orchestration/pipeline.md`. Never jump into prose.
2. **Progressive disclosure.** Only read the file you need for the current
   step. Never preload the whole skill.
3. **Evidence first.** Every non-trivial claim is backed by a citation,
   dataset, equation, or explicit derivation.
4. **No hallucinated citations.** Never invent DOIs, page numbers,
   authors, or volumes. Mark gaps with `[CITATION NEEDED]` or
   `[UNVERIFIED]` and surface them in `Known gaps`.
5. **Reproducibility.** Datasets, code, environments, seeds, and
   hyperparameters are documented end-to-end.
6. **Dual register.** Maintain academic rigor *and* a "Plain-English
   summary" for non-specialists (see `prompts/simplification-prompts.md`).
7. **Visual-by-default.** Comparisons, trends, distributions, structure,
   geography, and processes always get a figure or table
   (see `visualization_engine/decision-engine.md`).
8. **Self-review.** Run the simulated peer-review pass
   (`review_pipeline/`) and the publication checklist
   (`quality_control/publication-checklist.md`) before delivery.
9. **No silent failures.** Anything missing surfaces in a `Known gaps`
   block at the end of the paper.
10. **Multi-agent ready.** For long papers, dispatch sub-agents per
    `orchestration/agents.md`.

---

## 3. Top-level workflow

```
intake → plan → lit-review → methodology → data-analysis →
visualization → drafting → citations → validation → review → ship
```

Each step has a dedicated playbook. Read it, do the step, persist the
artifact to disk, move on. Detailed master pipeline:
**`orchestration/pipeline.md`**.

---

## 4. Format selection

When the user does not specify a format, infer it:

| Signal                                                | Use template                     |
| ----------------------------------------------------- | -------------------------------- |
| ML / NLP / AI / preprint / arxiv-style                | `templates/arxiv-paper.md`        |
| Engineering / hardware / signal / IEEE conference      | `templates/ieee-paper.md`         |
| HCI / systems / SIGCHI / SIGGRAPH / ACM                | `templates/acm-paper.md`          |
| Biology / medicine / Nature / Science / structured     | `templates/nature-paper.md`       |
| Social science / business / humanities / Harvard       | `templates/harvard-paper.md`      |
| Literature / systematic / scoping / meta review        | `templates/literature-review.md`  |
| Thesis chapter / dissertation                          | `templates/thesis-chapter.md`     |
| Whitepaper / industry / enterprise                     | `templates/whitepaper.md`         |
| Survey / state-of-the-art                              | `templates/survey-paper.md`       |
| Policy brief / regulatory                              | `templates/policy-paper.md`       |

If still ambiguous, ask once, then proceed.

---

## 5. Citation style selection

Map domain → default style if not specified:

- CS / engineering / physics → **IEEE numeric**
- ML / AI / preprint → **author–year (Harvard / APA-compatible)**
- Biology / medicine / Nature → **Nature numeric superscript**
- Social science / business / humanities → **Harvard** (or APA)
- Law / history → **Chicago**

Style rules: `citation_engine/citation-styles.md`. Per-style modules:
`citation_engine/styles/`. The deterministic formatter is
`toolchains/format_bibliography.py`.

---

## 6. Visualization decision (summary)

Full rules: `visualization_engine/decision-engine.md` and
`visualization_engine/visualization-guide.md`. Rendering happens via
`toolchains/generate_charts.py`; if Python is unavailable, the skill
falls back to **Markdown tables + Mermaid diagrams** — never silently
skips a planned figure.

| Communication goal             | Recommended figure                      |
| ------------------------------ | --------------------------------------- |
| Compare discrete categories     | Bar / horizontal bar / lollipop        |
| Show trend over time           | Line / multi-line                       |
| Show distribution              | Histogram / violin / box plot           |
| Show relationship              | Scatter + regression line               |
| Show correlation among many vars | Heatmap                                |
| Show parts of a whole           | Stacked bar (preferred over pie)       |
| Show flow / transformation      | Sankey                                  |
| Show structure / pipeline       | Architecture / flowchart                |
| Show process / decision         | Mermaid flowchart                       |
| Show geography                  | Choropleth / point map                  |
| Show timeline of events         | Timeline / Gantt                        |
| Show conceptual hierarchy       | Mind map / tree                         |
| Side-by-side metrics            | Comparative table                       |

---

## 7. Tooling expectations

This skill works in three tiers, gracefully degrading:

| Tier                                  | Capabilities                                                       |
| ------------------------------------- | ------------------------------------------------------------------ |
| **0. Pure prose** (no tools)           | Outline + draft + Markdown tables + Mermaid diagrams              |
| **1. + Filesystem read/write**          | Persist sections, bibliography, validation reports                 |
| **2. + Python (pandas/matplotlib)**    | Real charts (PNG + SVG), statistical validation, data analysis    |
| **2+. + Web search / fetch**            | DOI verification, source retrieval, retraction checks              |
| **2+. + Pandoc** (optional)             | Output to PDF / DOCX / HTML / LaTeX / RTF / EPUB / ODT / PPTX     |

If a tier is missing, the skill detects it and adapts — no silent failures.
See **`toolchains/README.md`** for setup.

### Output formats

The skill produces Markdown by default. For other formats, run the
output converter:

```bash
python toolchains/convert_output.py --input paper-final.md --to pdf --out paper.pdf
python toolchains/convert_output.py --input paper-final.md --to docx
python toolchains/convert_output.py --input paper-final.md --to html
python toolchains/convert_output.py --input paper-final.md --to tex
python toolchains/convert_output.py --input paper-final.md --to epub
```

Supported targets (via Pandoc): `md` (always), `html`, `docx`, `pdf`
(needs LaTeX), `tex`, `rtf`, `epub`, `odt`, `pptx`.

Self-test:
```bash
python toolchains/convert_output.py --self-test
```

The user can also request a non-Markdown output directly:

```
/research "topic" --output paper.pdf
/research "topic" --output paper.docx
```

---

## 8. Output contract

Every artifact this skill produces includes, at minimum:

1. **Title** — specific, ≤ 15 words.
2. **Authors / Affiliation block** — placeholders if not provided.
3. **Abstract** — 150–300 words, structured.
4. **Keywords** — 4–8.
5. **Plain-English summary** — 5–10 sentences.
6. **Numbered sections** following the chosen template.
7. **At least one figure and one table** for any paper > 1500 words
   (unless purely theoretical and explicitly opted out).
8. **In-text citations** in the chosen style.
9. **Full reference list** with DOIs / URLs.
10. **Limitations** section.
11. **Future work** section.
12. **Reproducibility statement** (data, code, environment, seeds).
13. **Appendices** for derivations, hyperparameters, prompts, raw outputs.

Anything missing is surfaced in a final **`Known gaps`** block —
never silently swallowed.

---

## 9. Long-context strategy

For papers > ~10,000 words:
- Persist every artifact to disk before moving on
  (`paper-spec.md` → `outline.md` → `bibliography.yaml` →
  `methodology.md` → `analysis/findings.md` → `figures-plan.md` →
  `sections/<NN>-<name>.md` → `paper-draft.md` → `paper-cited.md` →
  `paper-final.md`).
- Read only the section being drafted (plus the outline) at any time.
- Cross-section consistency is enforced by the outline + a final
  cover-to-cover read pass.

Full strategy: **`long_context/strategy.md`**.

---

## 10. Multi-agent orchestration

For deep / parallel runs, dispatch sub-agents:

| Agent           | Reads                                | Writes                          |
| --------------- | ------------------------------------ | ------------------------------- |
| Researcher      | `prompts/literature-search.md`        | `bibliography.yaml`, `lit-themes.md` |
| Methodologist   | `prompts/methodology-design.md`       | `methodology.md`                |
| Analyst         | `prompts/data-analysis.md`            | `analysis/findings.md`          |
| Visualizer      | `prompts/visualization-planning.md`   | `figures-plan.md`, `figures/`   |
| Writer (×N)     | `prompts/writing-prompts.md`          | `sections/<NN>-<name>.md`       |
| Citator         | `prompts/citation-prompts.md`         | `paper-cited.md`                |
| Validator       | `validators/`                         | `validation/`                   |
| Reviewer (×3)   | `prompts/review-prompts.md`           | `review/`                       |

Topology: **`orchestration/agents.md`**.

---

## 11. Failure handling

- **Missing data** → synthetic illustrative dataset, clearly labeled.
- **Unverifiable source** → `[UNVERIFIED]`, listed in `Known gaps`.
- **Conflicting evidence** → explicit "Contradictions in the literature"
  subsection.
- **Out-of-scope request** → narrow scope, list dropped sub-topics in
  `Future work`.
- **Token / context pressure** → see §9.

Full failure-handling matrix: **`orchestration/failure-handling.md`**.

---

## 12. Where to look next

- **Plan a paper** → `orchestration/pipeline.md`
- **Pick a template** → `templates/`
- **Write a section** → `prompts/writing-prompts.md`
- **Add citations** → `citation_engine/`, `workflows/citation-pipeline.md`
- **Make charts** → `visualization_engine/`, `workflows/visual-generation-pipeline.md`
- **Validate stats** → `methodology_engine/statistical-methods.md`,
  `toolchains/statistical_validation.py`
- **Self-review** → `review_pipeline/`, `rubrics/academic-quality.md`
- **Ship it** → `quality_control/publication-checklist.md`

Always prefer reading the *specific* file you need over re-reading this one.
