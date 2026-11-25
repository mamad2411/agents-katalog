---
name: research-neural-network-figure
description: Use when creating, planning, auditing, or choosing tools for neural-network architecture figures, CNN diagrams, AI model schematic diagrams, NN-SVG, PlotNeuralNet, draw_convnet, LaTeX/TikZ neural-network figures, or publication-ready model architecture visuals.
---

# Research Neural Network Figure

Use this skill to choose and govern neural-network architecture figure workflows. It is a tool-selection and figure-quality skill, not a source of evidence.

## First Gate

Before selecting a tool, identify:

- figure purpose: explanation, paper figure, slide, appendix, GitHub README, or concept sketch;
- architecture status: confirmed from source/code, user-specified, or illustrative only;
- output target: SVG, PDF, PNG, LaTeX/TikZ, Word-compatible image, or README image;
- privacy boundary: no private model code, participant data, proprietary client material, or confidential architecture should be uploaded to an online tool.

For formal research outputs, pair this skill with source-first, privacy/compliance, figure-quality, and document-quality gates.

## Tool Choice

| Tool | Use When | Boundary |
|---|---|---|
| NN-SVG | quick editable SVG neural-network sketches; architecture is simple enough for manual configuration | Online tool; do not upload private or sensitive data; user may need to export manually |
| PlotNeuralNet | paper-grade LaTeX/TikZ architecture diagrams; reproducible figure code is useful | Do not run external repo scripts unless the user asks; check local LaTeX availability first |
| draw_convnet | lightweight convolutional-network figure only | Check licence before copying or redistributing code |
| Custom Mermaid / TikZ / Python / SVG | the figure is conceptual, non-standard, or external tools do not fit | Keep diagram source and export path auditable |

## Workflow

1. State the selected figure route and why.
2. Create a figure contract:
   - title or caption job;
   - architecture source;
   - visual grammar;
   - required labels;
   - output format;
   - unresolved confirmations.
3. If generating code, keep it minimal and reproducible.
4. If using external tools, do not install dependencies without explicit user confirmation.
5. For formal outputs, record how the figure was produced and whether external-tool or AI-assisted generation needs disclosure.
6. Before delivery, inspect the rendered figure for text legibility, label overlap, export quality, and mismatch between architecture and caption.

## Do Not

- Do not treat a schematic as evidence that the model/tool exists or was evaluated.
- Do not invent architecture layers, dimensions, datasets, or performance claims.
- Do not copy third-party code into a public repository without licence review.
- Do not use this for ordinary conceptual frameworks unless a neural-network or model architecture visual is actually needed.
