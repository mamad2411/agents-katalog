---
name: research-nature-figure
description: Use when creating, revising, or auditing high-impact journal style scientific figures, Nature-style figure logic, multi-panel research figures, manuscript-ready plots, figure contracts, panel narratives, SVG/PDF/TIFF export checks, or publication-grade visual argumentation.
---

# Research Nature Figure

This skill adapts high-impact scientific figure-contract logic into a safe general research-agent workflow.

## Position In The Stack

Use after:

- source/privacy/compliance checks for the underlying data or claim;
- project-specific figure planning when the output is part of a formal report, thesis, article, grant, or public documentation.

Use before:

- final document-quality review;
- Word/PDF/render delivery;
- public README or manuscript figure export.

## Figure Contract

Before drawing or revising the figure, define:

- main conclusion the figure should make visible;
- evidence or source behind each panel;
- audience: supervisor, reviewer, journal reader, client, funder, GitHub reader, or presentation audience;
- figure type: conceptual model, process diagram, data plot, architecture schematic, or multi-panel summary;
- export target and constraints;
- review risk: unsupported claim, overcrowding, inaccessible colour, weak caption, unclear panel order, or privacy risk.

## Workflow

1. Decide whether this is a data plot, conceptual figure, or architecture figure.
2. For data plots, inspect or request the data source before plotting.
3. For conceptual or process figures, use claim/source mapping instead of numerical-data assumptions.
4. Choose the simplest tool that can produce the required output: Python/R for data plots, Mermaid/SVG/PowerPoint/draw.io-style routes for conceptual diagrams, or `research-neural-network-figure` for neural-network architecture.
5. Check:
   - one visual argument per figure;
   - one job per panel;
   - captions explain what to see and why it matters;
   - colours work in greyscale or colour-blind-safe viewing where possible;
   - labels remain legible after Word/PDF export.

## Boundaries

- This skill does not make a figure journal-submission-ready by itself.
- It does not replace source, data, privacy, compliance, or document-quality checks.
- It does not prove data validity or citation support.
- Do not use polished visual style to make weak evidence look stronger.
