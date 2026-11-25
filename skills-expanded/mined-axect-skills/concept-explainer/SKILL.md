---
name: concept-explainer
description: >
  Create rigorous teaching explanations as a single markdown document with
  equations, assumptions, derivations, plots, optional schematic prompts, and
  PDF export. Use when the user asks to explain a physics, math, ML, statistics,
  or CS concept; write lecture, tutorial, or seminar notes; derive results step
  by step; build a kind but rigorous walkthrough; or turn a paper section into
  classroom-ready material. Finished explanations are archived to
  ~/Dropbox/ConceptExplainer/<Topic>/<YYYYMMDD>_<concept-slug>/ automatically,
  regardless of language, date-prefixed so name order matches time order.
---

# concept-explainer — Kind, Rigorous, Visualization-Heavy Explanations

Produce a single explanation document that walks a named audience through a
specific concept **without logical leaps** and **without sacrificing
mathematical rigor**. Equations carry their weight, every symbol is defined,
every step in a derivation names the rule it applies, and visualizations
appear wherever they shorten the gap between a formula and an intuition.

The skill writes:

```text
<out-dir>/                   # <YYYYMMDD>_<concept-slug>, e.g. 20260728_lagrangian-mechanics
├── explanation.md           # the document (language follows user's request)
├── plots/                   # matplotlib scripts + their rendered PNGs
│   ├── *.py
│   └── *.png
└── schematics/              # OPTIONAL — only when conceptual diagrams help
    ├── *_prompt.md          # copy-pasteable wide-slide-illustrator prompts
    └── *.png                # rendered images (user fills these in, or codex-image)
```

`<out-dir>` is `<YYYYMMDD>_<concept-slug>`: the day the directory is created
(`date +%Y%m%d`) followed by the kebab-case concept slug. Alphabetical order
then equals chronological order in any folder that collects explanations.

After the document is complete, the skill invokes `md2pdf-typora` to produce
`<out-dir>/explanation.pdf`, then mirrors the explanation (markdown, PDF,
plots, schematics) into `~/Dropbox/ConceptExplainer/<Topic>/<out-dir>/`,
organised by topic. The archive folder keeps the same name as the local
directory; the date prefix carries the ordering, so there is no separate index.
This archive step runs for every explanation regardless of language.

## Mandatory invariants (non-negotiable)

These hold across every explanation produced by this skill.

### Rigor invariants

1. **Define before use.** Every symbol that appears in an equation is defined
   before its first non-definitional use, on the same line or in the line
   above. Quantities with units carry the unit on first appearance.
2. **Name the rule.** Every step in a derivation states the rule it applies
   ("by the chain rule", "integrating both sides", "using assumption A1",
   "Taylor-expanding around `x = 0` to second order"). Never write "it can
   be shown that" without either a one-line sketch or a citation.
3. **Mark approximations.** Use `=` for exact equalities, `≈` for
   approximations (state the order: "to leading order in `ε`"), `∼` for
   asymptotic behavior, `∝` for proportionality. Mixing these silently is a
   logical leap and is forbidden.
4. **State assumptions up front.** A boxed `## Assumptions` block lists the
   regime / smoothness / boundary conditions you depend on. When you later
   drop or generalize one, say so explicitly.
5. **No forward references.** A concept cannot appear in prose before its
   definition. If the reader needs `X` to understand `Y`, `X` is in an
   earlier section.
6. **Cite the non-derivable.** Empirical facts, named theorems used without
   proof, and any numerical constant beyond textbook precision need a
   citation. Invoke the `reference-search` skill to find sources rather than
   guessing.
7. **Forbidden hedges.** "Obviously", "clearly", "trivially", "it is
   well-known that" — strip them. If a step is genuinely one line, write the
   line. If it isn't, write the steps.

### Visualization invariants

8. **scienceplots ["science", "nature"], always.** Every matplotlib script
   uses `import scienceplots` (registered by side-effect, never referenced),
   wraps all plotting in `with plt.style.context(["science", "nature"]):`,
   and saves with `dpi=300, bbox_inches='tight'`. **The `no-latex` style is
   forbidden.** Plots must render LaTeX through the system TeX install.
9. **Raw-string LaTeX labels.** Every axis label, title, legend entry, and
   text annotation uses `r'...'`. Non-raw strings silently break the moment
   a backslash appears.
10. **`pparam` dict + `ax.set(**pparam)` + `ax.autoscale(tight=True)`.** Same
    structural invariants as `scienceplot-py`. Do not inline
    `ax.set_xlabel(...)` calls when `pparam` would do.
11. **Caption discipline.** Every figure in `explanation.md` carries a
    caption that says **what to look at**, not just what the plot contains.
    The caption interprets the figure for the named audience.
12. **Schematic vs data plot — pick the right tool.** Conceptual diagrams
    (boxes, arrows, "pipeline overview", "what each component does") are
    composed via `wide-slide-illustrator` Friendly Whiteboard style and live
    in `schematics/`. Mathematical visualizations (functions, parameter
    sweeps, fields, phase portraits, convergence plots) are matplotlib
    scripts in `plots/`. Do not draw boxes-and-arrows with matplotlib; do not
    plot `f(x)` curves through an image-gen model.

### Output invariants

13. **Language follows user's request.** If the user wrote in Korean, the
    document is in Korean. If in English, English. Equations are
    language-independent and stay verbatim. Section headings, prose,
    figure captions all match the request language.
14. **One concept per run.** This skill produces one focused explanation.
    For a multi-concept curriculum, run the skill once per concept and let
    the user thread them.
15. **No co-author tags in any generated file.** Per the user's global rule.

## Workflow

### 1. Gather inputs

Ask only for what is missing. Required:

- **Concept**: the thing to explain. Be specific — "the Lagrangian
  formulation of classical mechanics" rather than "Lagrangians".
- **Audience**: a free-form one-liner describing the reader. Examples:
  "학부 2학년 물리, 라그랑지안 모름, 미적분은 됨" or "ML PhD student new to
  measure-theoretic probability".
- **Concept slug**: kebab-case directory name. Default: derived from the
  concept (e.g. `lagrangian-mechanics`).
- **Output directory**: default `<cwd>/<YYYYMMDD>_<concept-slug>/`, referred to
  as `<out-dir>` below. Take the date from `date +%Y%m%d`.

Optional:

- **Length target**: short (~800 words), standard (~2000 words), or long
  (~4000 words). Default: standard.
- **Schematic figures**: yes / no / "only if it helps". Default: "only if
  it helps" — produce schematics only for genuinely conceptual structure
  (architectures, pipelines, taxonomy), never for purely mathematical
  content.
- **Reference search**: yes / no. Default: yes for non-derivable claims.

### 2. Calibrate to the audience

Translate the free-form audience description into a calibration table.
See `references/audience-calibration.md` for the full protocol. The output
is an internal dict (do **not** put this in the document):

```text
- prerequisite_knowledge:  [list of concepts treated as known]
- needs_definition:        [list of concepts that must be defined inline]
- notation_conventions:    [e.g. "physicist's index notation", "ML-style E[·]"]
- math_density:            low | moderate | high
- worked_example_density:  low | moderate | high
- approximation_tolerance: how casually the audience treats "≈"
```

If the audience description is too vague to calibrate (e.g. just "학생"),
ask one targeted clarifying question. Do not guess.

### 3. Plan the section structure

Use the skeleton in `references/structure-template.md`. The default 10
sections (translate headings to match the requested language):

1. **Why this matters** — the motivating question. 1–2 paragraphs.
2. **Setup** — the simplest non-trivial case that still exhibits the
   phenomenon.
3. **Definitions and assumptions** — every symbol, every regime constraint.
4. **Intuition** — verbal picture + (optional) schematic figure.
5. **Step-by-step derivation** — each step names its rule; show the
   intermediate equations.
6. **Worked example** — concrete numbers, with a function plot or sweep.
7. **Visualizations** — parameter dependence, limits, edge cases.
8. **Generalization** — how the result extends; what assumptions can be
   relaxed.
9. **Limitations and common misconceptions** — failure modes, pitfalls,
   numbered "Misconception N → 오개념 N" callouts.
10. **Where to go next** — references, follow-up concepts, exercises.

Drop or merge sections only when the concept genuinely doesn't need them
(e.g. a definition-only note may not need §8). Adding sections is fine.

### 4. Draft the document

Write `<out-dir>/explanation.md` with the structure from step 3.
While drafting, the rigor invariants from above are **load-bearing** — read
`references/rigor-checklist.md` and apply each item to every paragraph.

Equation typesetting in markdown:

```markdown
Inline math: $\alpha = 0.05$, $\hat{\theta} \in \mathbb{R}^d$.

Display math on its own line:

$$
\mathcal{L}(q, \dot{q}, t) = T(\dot{q}) - V(q)
$$

with $T$ the kinetic energy, $V$ the potential, $q$ the generalized
coordinate, and $\dot{q} = \mathrm{d}q/\mathrm{d}t$.
```

The line after a display equation defines every symbol introduced in it.
This is the **define-before-use** rule operationalized.

### 5. Plan visualizations

For each section that benefits from a figure, decide schematic vs plot
using `references/visualization-playbook.md`. Common patterns:

| Need                                          | Tool                                                  |
|-----------------------------------------------|-------------------------------------------------------|
| Closed-form function `f(x)` over a range      | `plot_skeletons/function_plot.py` → matplotlib        |
| "How does the answer change with `α`?"        | `plot_skeletons/parametric_sweep.py` → multi-panel    |
| 2D scalar field (potential, density, energy)  | `plot_skeletons/heatmap.py` → matplotlib `imshow`     |
| Convergence / error scaling                   | `plot_skeletons/function_plot.py` with log-log scales |
| Comparing exact vs approximation              | `plot_skeletons/function_plot.py`, multi-line variant |
| Pipeline / architecture / "the big picture"   | `wide-slide-illustrator` Friendly Whiteboard prompt   |
| Taxonomy / decision tree                      | `wide-slide-illustrator` Friendly Whiteboard prompt   |

For more advanced data sources (parquet/CSV/npy/npz) or plot variants
(scatter/errorbar, generic subplots), defer to the `scienceplot-py` skill
templates — do **not** duplicate them here.

### 6. Render the plots

For each matplotlib plot:

1. Adapt the matching skeleton from `references/plot_skeletons/` into a
   concrete `.py` file under `<out-dir>/plots/<plot_name>.py`. Keep
   every invariant from `scienceplot-py` intact.
2. Execute it: `uv run <out-dir>/plots/<plot_name>.py`. This skill
   **does** execute its own plot scripts (unlike `scienceplot-py`, which
   does not). The PDF assembly later depends on the PNGs existing.
3. Verify the PNG exists and is non-empty: `ls -la
   <out-dir>/plots/<plot_name>.png`.
4. Reference the PNG in `explanation.md` with a caption that says what to
   look at:

   ```markdown
   ![Action vs path length for three trajectories. The straight-line path
   minimizes the action; small wiggles raise it; large wiggles raise it
   much more. The minimum here corresponds to the classical trajectory.](
   plots/action_vs_path.png)
   ```

If a plot script fails to render, **fix the script** — do not silently
remove the figure from the document. Common causes: missing TeX system
package, wrong column name, math expression that needs raw-string.

### 7. Compose schematic prompts (only if planned in step 5)

For each schematic figure:

1. Invoke the `wide-slide-illustrator` skill with the Friendly Whiteboard
   style. See `references/schematic_friendly.md` for the brief — it gives
   the panel-count guidance, the on-canvas-text-is-English rule, and the
   per-panel content fields needed.
2. Save the composed prompt as
   `<out-dir>/schematics/<schematic_name>_prompt.md`.
3. The user feeds this prompt to ChatGPT Image / DALL-E / Sora / Midjourney
   and saves the result as `schematics/<schematic_name>.png`. (Alternative:
   the `codex-image` skill can run this automatically — mention this option
   to the user but do not auto-invoke unless they ask.)
4. Reference the image in `explanation.md` with a caption. If the image
   does not yet exist, write the markdown reference anyway and tell the
   user explicitly which files they need to generate before the PDF step.

### 8. Reference search (when needed)

For any non-derivable claim flagged in step 4, invoke the `reference-search`
skill to find supporting references. Inline citations use a short
parenthetical like `(Goldstein 2002, §1.4)` or a numeric `[1]` style with
the source list in §10. Do **not** fabricate citations.

### 9. Validate the draft

Before assembling the PDF, run the checklist in
`references/rigor-checklist.md`:

- Every display equation followed by a symbol-definition line.
- No forbidden hedges ("obviously", "clearly", etc.) — grep for them.
- Every figure referenced from the markdown exists in `plots/` or
  `schematics/`.
- Every figure has a caption that interprets the figure.
- Every cited reference appears in §10.
- No forward references.

If any item fails, fix the document — do not paper over it.

### 10. Assemble the PDF and archive to Dropbox (automatic)

Every finished explanation is exported to PDF and mirrored into the user's
`~/Dropbox/ConceptExplainer` archive, organised by topic. Do this automatically
for every explanation regardless of language — do not wait to be asked.

1. **Export the PDF** with the `md2pdf-typora` skill on
   `<out-dir>/explanation.md`, producing `<out-dir>/explanation.pdf`.
   The Whitey theme handles Korean and English both.
2. **Pick the topic folder.** The archive is organised as
   `~/Dropbox/ConceptExplainer/<Topic>/<out-dir>/`, reusing the same
   `<YYYYMMDD>_<concept-slug>` folder name used locally, so the topic listing
   sorts chronologically without a separate index.
   - List the existing topics (`ls ~/Dropbox/ConceptExplainer`) and choose the
     one that fits the concept. If none fits, ask the user which topic to use or
     whether to create a new one (reuse the JournalClub topic vocabulary —
     `InverseProblem`, `NeuralOperators`, `PBH`, `SMEFT`, `Unfolding`, ... —
     when sensible); create it only after they confirm the name. Do not silently
     invent a topic.
   - If the local directory predates the convention and has no date prefix,
     prepend one for the archive copy only, taken from the `explanation.md`
     mtime. Leave the local directory alone.
   - If the concept is already archived under an older name, update that folder
     in place rather than creating a second, renamed copy.
3. **Copy the artifacts** into
   `~/Dropbox/ConceptExplainer/<Topic>/<out-dir>/`: `explanation.md`,
   `explanation.pdf`, the `plots/` directory (scripts + rendered PNGs), and the
   `schematics/` directory if it exists. Match the existing layout in sibling
   explanation folders.
4. **Confirm** the destination path and file sizes to the user.

### 11. Report and stop

Report to the user:

- The output directory.
- The list of generated plot scripts and which produced PNGs.
- The list of schematic prompts (and which images still need to be
  generated by the user).
- The PDF path.
- The Dropbox archive path.

Do **not** push, commit, or otherwise touch git state. The
`commit-triage` skill handles that when the user is ready.

## Audience calibration

See `references/audience-calibration.md` for the full protocol. Short
version: convert a free-form one-liner into a calibration table covering
prerequisite knowledge, vocabulary that needs inline definition, notation
conventions, and density dials. When in doubt, ask one targeted question
rather than guessing — getting the audience wrong wastes the rest of the
workflow.

## Rigor checklist

See `references/rigor-checklist.md`. Apply every item to every paragraph
before declaring the draft complete. The checklist exists because every
item on it is a failure mode I have seen in unaudited "kind explanations":
silent assumption-dropping, ambiguous `=`/`≈`, hidden forward references,
"obviously" used as a load-bearing inference, fabricated citations,
mismatched units.

## Visualization playbook

See `references/visualization-playbook.md`. Picks the right tool per
visualization need, lists which plot skeleton to start from, and gives the
"what to look at" caption pattern.

## Plot skeletons

Self-contained, runnable matplotlib templates that satisfy every
visualization invariant.

| Skeleton                                 | Purpose                                        |
|------------------------------------------|------------------------------------------------|
| `plot_skeletons/function_plot.py`        | One or more closed-form `f(x)` over a range    |
| `plot_skeletons/parametric_sweep.py`     | Multi-panel "vary one parameter" comparison    |
| `plot_skeletons/heatmap.py`              | 2D scalar field over `(x, y)`                  |

For other variants (scatter/errorbar, data files from parquet/CSV/npy),
generate the script through the `scienceplot-py` skill and place the
output under `plots/`.

## What this skill does NOT do

- It does not produce slide decks. For talks, hand the markdown to a
  slide-generation pipeline (`claude-typst-slides:slides-present`,
  `frontend-slides`).
- It does not run hyperparameter sweeps or fit models. If the explanation
  needs experimental data, run that out of band and pass the resulting
  parquet/CSV through `scienceplot-py`.
- It does not turn an entire textbook chapter into a single document.
  One concept per run. Threading is the user's job.
- It does not invent citations. If `reference-search` returns nothing
  usable, leave the claim un-cited and flag it to the user, or rewrite the
  claim so it no longer needs a citation.
- It does not skip the auto-PDF step on success. Every explanation always
  reaches `~/Dropbox/ConceptExplainer/<Topic>/<YYYYMMDD>_<concept-slug>/`.
- It does not commit anything. `commit-triage` does that, when the user
  asks.
