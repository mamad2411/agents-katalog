---
name: research-essay
description: >
  Develop a research idea into a literature-grounded, standalone HTML essay with verified full texts,
  reproducible analysis, and a tutorial narrative. Use for requests to develop or situate an idea in
  the literature and write it up, or to revise an existing essay after new evidence, analysis, or
  reader feedback. Also supports historical and comparative essays and an explicitly requested
  LaTeX variant.
license: MIT
metadata:
  version: "1.3.2"
  source: https://github.com/chemaoxfz/idea-to-essay
---

# Research essay

Build a project whose central deliverable teaches an idea in conversation with the literature.
The default is one standalone HTML file, backed by full texts on disk and reproducible analysis.
Respect the user's chosen scope, audience, and format. A focused revision is not a new project.

## Non-negotiables

1. **Read the evidence.** Retrieve, verify, and inspect the full text of sources that materially
   inform the argument. Abstracts, snippets, and memory cannot establish a load-bearing claim.
   If full text is unavailable, record the gap and qualify or defer the dependent claim.
2. **Let evidence change the idea.** Log genuine corrections and fix the argument. Report negative
   results, weakened intuitions, and contrary evidence. Do not manufacture a correction or a result.
3. **Make the correspondence exact.** An analogy is not an argument. Name the shared mathematical
   object or mechanism, its assumptions, and where the correspondence breaks.
4. **Make numbers traceable.** Quantitative claims come from runnable project code, an inspected
   source, or documented figure digitization. Distinguish measurements, assumptions, and model outputs.
5. **Teach before using.** Define concepts, quantities, and named cases before interpreting them.
   A citation does not supply missing context. Keep meanings, units, and notation consistent.
   Separate derived accounting from assumed response curves. Explain why each chosen form is useful.
6. **Give each section a point.** Its question, reasoning, evidence, and takeaway must agree.
   A definition, limitation, or unresolved decision can be the point. Keep its conditions intact.
7. **Deliver a standalone argument.** The reader has neither the chat nor earlier drafts.
   The prose and the visual sequence must each make sense without that history.
   In a model-led essay, connect applications and conclusions to that model and name its extensions.
8. **Typeset all mathematics.** Use proper mathematical rendering in inline prose, display equations,
   tables, captions, figure labels, and interactive controls and readouts. Native MathML is the HTML
   default. Equivalent offline rendering is acceptable. Render figure mathematics with a math engine
   or properly positioned SVG glyphs. Raw TeX, ASCII subscripts, and monospace approximations are not
   finished mathematics. Follow the rendering rules in [house-style.md](references/house-style.md).

## Start or resume

For a new project, follow the workflow below. For a revision, first read the existing prompt, design,
outline, literature index and corrections, relevant code, and assembled essay. Resume at the stage
the request affects. Preserve working material and inspect related sections for the same problem.

Read [conventions.md](references/conventions.md) for the house defaults. Explicit user and project
instructions take precedence. Consult [exemplars.md](references/exemplars.md) when choosing the size
and form of a new essay, not as a quota of sections, figures, or papers.

The bundled helpers use Python 3.9+ and its standard library. Literature fetching also needs network
access, `pdftotext` from Poppler, and a contact email (`LIT_EMAIL` or `git config user.email`).
A TeX installation is optional. Mathematical typesetting is required. The figure-rendering fallback
is in `conventions.md`. Check the tools needed for the current stage before promising verification.

## Workflow

### 1. Frame and scaffold

Save the founding prompt verbatim in `idea.md`, including typos and asides. Never overwrite it with
your interpretation. In `design.md`, record a disputable thesis, the chain of argument, what would
refute it, and the existing research programmes it engages. For a historical or comparative essay,
state the organizing question and what evidence would change its interpretation.

Use only the parts of this layout the project needs:

```text
idea.md                  original request, preserved
design.md                thesis, argument, assumptions, decisions, project state
outline.md               section blueprint and revision addenda
literature/              verified full texts, INDEX.md, NEEDED.md
analysis/ or sim/         reproducible calculations and figure generators
figures/                 generated SVG and PDF figures
src/                     HTML parts, when a single source becomes unwieldy
<project-name>.html       standalone deliverable
README.md                entry points, established results, open work
handoff/                 actionable research briefs, when useful
```

A small essay can keep its design and outline in brief project notes. Do not create empty scaffolding.
When using the bundled helpers, copy `scripts/` to project `tools/`, including its README, so the
project reproduces without an installed skill. Preserve any existing project-specific tool changes.

### 2. Retrieve and read the literature

Read [literature.md](references/literature.md) before searching or fetching. Search by research
programme: founding work, current statement, reviews, critics, and citations in both directions.
Check relevant local archives before downloading. Resolve identifiers instead of guessing them.

Archive important full texts in the project's designated `literature/`. Verify each file's identity,
then read the passages, methods, and qualifications the argument needs. Maintain `INDEX.md` with
citation, stable identifier, source URL, filename, retrieval date, relevance, and checksum.
Keep unavailable items priority-ranked in `NEEDED.md`, with access problems and dependent claims.

For a new full essay, search again after the outline exposes its gaps. On a focused revision, target
the changed claims and follow their dependencies. Each step in the argument must be supported,
derived explicitly, or clearly identified as a new hypothesis or an unresolved gap.

### 3. Do the analytical work

For a quantitative idea, produce a simulation, derivation, re-analysis, or estimate that makes it
precise enough to be wrong. For a historical or conceptual question, do the source comparison the
claim requires; do not invent a numerical exercise just to fill this stage.

Keep code, inputs, dependencies, and run instructions together in `analysis/` or `sim/`. Generate
figures from that code and label digitized data with its method and uncertainty. Prefer a bound
that needs no fit over a weakly determined fit when both answer the same question. Report what
the calculation actually establishes, including failures and limits.

### 4. Outline the argument

Read [narrative.md](references/narrative.md) before outlining or revising the prose. For each section,
record its role, the reader's entry knowledge, motivating question, reasoning and evidence,
takeaway, and the next question it makes possible. Identify concepts that need introducing and
the figure, formula, or table that earns its place.

Group sections by their jobs in the argument. Update the working outline as needed and append a
brief addendum for substantive changes, so later readers can reconstruct the decisions.

### 5. Write and assemble

For HTML, read [house-style.md](references/house-style.md) and start from `assets/template.html`.
The page supplies inline CSS, SVG, and JavaScript, a table of contents, citations, and light and dark
themes. Add interactive demos only where changing a parameter teaches something.

Apply the narrative guide's section beats, context-and-continuity pass, and visual argument pass.
Repeat a key formula where the local reasoning needs it. Main figures must show the conclusion
and essential conditions without relying on fine-print captions.

When the source becomes hard to edit reliably, use `src/part*.html` and `src/refs.html`.
Read [build.md](references/build.md) for citation renumbering, SVG inlining, and assembly.
Edit the source or figure generator, then rebuild. Do not patch generated output alone.

### 6. Verify the assembled result

Use the verification gate in [build.md](references/build.md). It has four complementary checks:

- **Mechanical:** run `tools/check.py`, repair broken anchors and literature links, and review warnings.
- **Reproducibility:** rerun the relevant analysis and figure entry points. Search all project outputs
  for stale numbers, assumptions, and notation after a change.
- **Browser:** inspect both themes and a narrow viewport, console errors, controls, navigation, and
  rendered mathematics and figure geometry. Inspect inline and display math, figure labels, and
  changing readouts. Use the measurement pass in `house-style.md` for label collisions.
- **Reader:** read the essay without the chat, then skim only headings, formulas, figures, and
  takeaways. Repair missing premises, unexplained cases, unsupported conclusions, and weak transitions.

A clean automated report does not establish scientific or narrative correctness. If a check cannot
run, name it and the remaining uncertainty instead of reporting it as passed.

### 7. Hand off and, when requested, publish

Keep `README.md`, the literature index, `NEEDED.md`, and the project state current. Record substantive
repairs in project notes, not in the essay. Apply the narrative guide's final standalone pass so the
essay ends on its argument rather than a changelog. Where useful, provide research briefs with a
claim, mechanism, evidence, cheapest test, refutation criterion, and limits.

Publishing is a separate, authorized action. Follow the publishing section of `build.md` to derive
a web copy while preserving the local original. Do not redistribute the local full-text archive or
private project notes. Verify the published copy's links and standalone behavior after conversion.
