---
name: academic-presentation-crafter
description: "Creates and refines academic presentations from research papers. Use this skill for tasks involving the conversion of scientific or technical documents into slide decks for conferences, seminars, lectures, thesis defenses, or academic reviews. Supports beamer LaTeX (.tex), PowerPoint (.pptx), and Markdown output formats."
---

# Academic Presentation Crafter

## Overview

This skill provides a structured, multi-phase workflow for transforming dense research papers into clear, concise, and academically rigorous presentations. It ensures the final slide deck accurately reflects the paper's core contributions, data, and terminology.

## Workflow

The process is divided into four distinct phases. Follow these steps sequentially to ensure a high-quality outcome. For detailed checklists on rigor and visual polish, refer to the `references/` directory.

## External Advisor Mode (Required for committee/group reports)

When the audience is external (advisor, committee, collaborator), enforce:
1. English-only slide text.
2. No local machine/repo disclosure:
   - remove absolute paths,
   - remove local usernames/hostnames,
   - replace run IDs/version-like suffixes with semantic labels (e.g., `Baseline`, `Variant-B`).
3. Prefer neutral artifact naming in slides (`Case-A`, `Case-B`) and move raw identifiers to private appendix only if requested.
4. If slide tooling allows, produce `beamer` (`.tex`) and compile to `.pdf`; otherwise keep a clean Markdown deck as fallback.

Action: follow `references/external_reporting_sanitization_checklist.md` before finalizing.

### Phase 1: Foundational Analysis & Outline Generation

The goal of this phase is to deeply understand the source material and create a logical structure for the presentation.

1.  **Initial Skim & Core Contribution Identification**: Read the paper's abstract, introduction, and conclusion to grasp the main argument, key contributions, and overall narrative.
2.  **Identify Key Figures & Data**: Scan the paper for essential figures, charts, tables, and equations that are critical for explaining the methodology and results. Note their figure numbers and captions.
3.  **Generate a Comprehensive Outline**: Create a slide outline. If slide tooling is unavailable, generate a Markdown deck (`.md`) with `---` page separators. A typical academic structure is recommended (Motivation, Methods, Results, Conclusion). Start with 8-12 slides and expand only if necessary.

### Phase 2: Content Drafting & Asset Integration

This phase focuses on populating the slides with content and integrating the necessary visual aids.

1.  **Draft Slide Content**: Write the content for each slide. Paraphrase the paper's content into concise bullet points and short sentences.
2.  **Integrate Visuals**: Incorporate the key figures and diagrams identified in Phase 1. Ensure images are high-resolution and placed logically.
3.  **Data Placeholders**: For slides that will contain charts or graphs, clearly note the data source from the paper. Do not invent or approximate data.

### Phase 3: Academic Rigor & Content Refinement

This phase ensures the presentation meets academic standards. Apply the full checklist in `references/academic_rigor_checklist.md`, paying special attention to these critical items:

1. **Data and Metrics Verification**: Cross-check every number, table entry, and graph value against the source paper. Flag any discrepancy before proceeding.
2. **Terminology and Acronyms**: Define all acronyms on first use. Ensure domain-specific terms (e.g., PPA, timing closure, netlist) match the paper's definitions exactly.
3. **Claims and Contributions**: Verify that no slide overstates or understates the paper's claims. Each contribution slide must trace back to a specific section of the paper.
4. **Citations**: Include inline citations for all borrowed figures, data, and direct quotes. Use the paper's citation style consistently.

**Feedback loop**: After applying the checklist, revisit Phase 2 slides, update any corrected content, and re-verify data placeholders.

### Phase 4: Visual Polish & Final Review

Apply the full checklist in `references/visual_polish_checklist.md`, focusing on these high-impact items:

1. **Typography**: Minimum 18pt body font, 24pt+ for slide titles. Ensure a consistent font family across all slides.
2. **Layout consistency**: Use uniform margins, bullet indentation, and figure placement. Align elements to a clear grid.
3. **Visual cohesion**: Use a single color palette derived from the institution or conference theme. Limit accent colors to 2-3.

**Feedback loop**: Do a full sequential walkthrough of the deck. If any slide feels unclear or visually inconsistent, return to the relevant earlier phase before finalizing.

## Example Output

A results slide in Markdown format:

```markdown
## Results: Timing Closure Improvement

- Proposed flow achieves **12% WNS reduction** vs. baseline (Table 3)
- Area overhead: +2.1% (within PPA budget)
- Runtime: 3.2x faster than conventional approach

![Timing comparison](figures/fig5_timing_comparison.png)
<!-- Source: Fig. 5, Section IV-B -->

> Speaker notes: Emphasize the WNS improvement first, then address
> the area-runtime tradeoff. Reference Table 3 for detailed breakdowns.
```
