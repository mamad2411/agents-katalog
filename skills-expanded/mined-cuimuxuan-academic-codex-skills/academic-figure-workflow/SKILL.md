---
name: academic-figure-workflow
description: "Create, revise, or inspect evidence-backed academic plots and diagrams with editable sources. Use for figure work itself, not manuscript prose or page formatting. 适用于论文作图、修图与图形质量检查。"
---

# Academic Figure Workflow

Preserve scientific meaning and the user's requested scope. Do not invent
data, mechanisms, code structure, or experimental images. Retain editable
sources and notation; a screenshot is not a replacement for a figure source.

## Choose The Task Mode

| Request | Work and completion |
|---|---|
| Local edit or read-only inspection | Work with the existing SVG, Draw.io, or plotting source. Preserve user styling; do not redraw or migrate to YAML unless requested. Inspect affected rendering/exports, report the change or findings, and do not claim whole-figure publication approval from a local check. Read-only inspection does not modify the source. |
| New draft or design exploration | Use supplied facts and clearly identified assumptions. Choose an appropriate editable format; no full manuscript intake is needed. Missing evidence limits claims and publication status, not the ability to make a labelled concept draft or storyboard. |
| Reproducible or submission package | Use the bundled YAML generator and [package workflow](references/figure-package-workflow.md). Preserve its provenance, editable-source, export, and QA contract. Draft package generation is available without claiming submission readiness. |

Choose from the requested deliverable; ask only when an unresolved choice
materially changes the result. A simple edit does not require claim anchors,
new sidecars, or full-package QA unless it modifies an existing package whose
consistency must be maintained. In that case update its canonical source and
rebuild affected outputs; do not leave a stale manifest or approval.

## Choose Relevant Guidance

Read the relevant branch, not this entire reference collection.

| Decision or task | Reference |
|---|---|
| Chart selection, data mappings, or statistical encodings | [Data visualization advisor](references/data-visualization-advisor.md), before plotting |
| Complex, multi-panel, or evidence-sensitive figure argument | [Figure argument contract](references/figure-argument-contract.md) |
| New SVG mechanism or Draw.io engineering diagram | [SVG and Draw.io diagrams](references/svg-and-drawio-diagrams.md) |
| Authoring a generator spec | [FigureSpec schema](references/figure-spec-schema.md); for diagrams, [diagram spec](references/diagram-figure-spec.md) |
| Model architecture layout | [Architecture contract](references/architecture-figure-contract.md) |
| Dense workflow layout or engine comparison | [Flowchart engine comparison](references/flowchart-engine-comparison.md) |
| Microscopy, photographs, or other image panels | [Image integrity](references/image-panel-integrity.md), before image processing |
| AI-generated supporting bitmap | [AI image-generation gate](references/ai-image-generation-gate.md), before generation |
| Choosing between production methods | [Method selection](references/figure-method-selection.md) |
| Final submission inspection without a package | [Rendered figure QA](references/rendered-figure-qa.md) |
| Publication package acceptance | [Package QA](references/qa-and-visual-regression.md) |
| Design examples or an unfamiliar figure type | [Reference gallery](references/reference-gallery.md); obey its asset licence and private-reference restrictions |

For new work, prefer Matplotlib for quantitative plots, Draw.io for editable
workflows/engineering diagrams, and SVG for precise mechanism figures. Respect
an existing source or explicitly chosen tool. Office/PPT/WPS support in the
bundled generator is capability detection only, not native editing; use
`python scripts/figure_package.py capabilities` when that capability matters.

## Defaults And Exceptions

Scientific integrity and authorization boundaries always apply. Within those
boundaries, use the requested purpose and target venue/template first, then
the matching profile, then defaults for unspecified details. If the request
conflicts with the target submission guide, resolve that conflict rather than
silently choosing one or claiming compliance.

For submission styling, consult [publication standards](references/publication-visual-standards.md).
For format, resolution, or font requirements, consult [export standards](references/export-and-editability-standards.md).
For colour/encoding decisions, consult [accessibility standards](references/accessibility-and-color-standards.md).
These are conditional references, not a prerequisite for every edit. Nature-like
dimensions and external-title conventions are defaults for that use, not rules
for all figures. Do not waive a failing package check to claim a venue override;
if the generator cannot express a requirement, report the limitation and retain
a draft or use a suitable authorized source/export workflow.

## Finish The Requested Work

Continue source corrections and relevant checks while they make progress.
Repeated failure without progress calls for a different layout/chart strategy,
simplification within scope, or a concrete blocker—not a fixed pass-count cap.
Do not reset the recorded review count to obtain approval.

Return the requested source/export or inspection findings, relevant validation
status, and unresolved issues. A publication claim requires actual final-size
visual inspection and applicable export/evidence checks; command success alone
is insufficient. Do not expand a local edit into a manuscript audit or return
an unfinished first implementation when the requested checks remain feasible.
