---
name: paperbanana-teaser
description: Use this skill when the user wants to turn a paper idea, methodology section, figure caption, or teaser concept into a structured academic-figure prompting workflow. Best for NeurIPS/ICML/ICLR/CVPR/ACL-style teaser figures, method overviews, system diagrams, and PaperBanana-style planner-stylist-visualizer-critic prompt chains.
---

# PaperBanana Teaser

## Overview

This skill converts a research paper's method or teaser idea into a reusable multi-stage prompting workflow for academic illustrations. It is optimized for PaperBanana-style generation: retrieve context, plan the diagram, refine the visual style, generate the figure, critique the result, and iterate.

## When To Use

Use this skill when the user asks for any of the following:

- A teaser figure prompt for a paper
- A PaperBanana-style workflow or prompt chain
- A method section turned into a diagram description
- A NeurIPS, ICML, ICLR, CVPR, ACL, or EMNLP-style academic figure prompt
- A critique-and-revise loop for generated research figures

Do not use this skill when the user primarily needs:

- Pixel-perfect SVG, TikZ, Figma, PowerPoint, or HTML/CSS implementation
- A direct image edit without prompt engineering
- A non-academic marketing illustration

## Required Inputs

Gather as many of these as available before writing prompts:

- Paper topic
- Core problem
- Limitation of prior work
- Proposed method or system
- Main technical components
- Main takeaway or result
- Methodology section
- Figure caption
- Target venue or desired visual style
- Optional reference figures for style only

If the user provides only partial information, proceed with the available content and keep the prompt faithful to it. Simplify missing details instead of inventing modules.

## Default Workflow

Follow this sequence unless the user asks for only one stage:

1. `Planner`
   Convert the methodology and caption into a dense, structured figure description.
2. `Stylist`
   Refine the description into a polished top-conference visual specification without changing the science.
3. `Visualizer`
   Produce the final model-facing image-generation prompt.
4. `Critic`
   Compare the generated image against the source method, caption, and description; return concrete fixes plus a revised description when needed.

## Working Rules

- Preserve scientific fidelity. Do not add claims, modules, or arrows not supported by the paper.
- Never place the figure title, paper title, caption, or `Figure 1` inside the image.
- Prefer natural-language color descriptions over hex codes, pixel sizes, CSS values, or implementation-specific styling.
- Keep labels short, explicit, and readable.
- Choose aspect ratio from content structure instead of defaulting blindly.
- If uncertainty remains, simplify the drawing rather than hallucinating details.

## Output Modes

Pick the lightest useful deliverable for the user:

- `planner-only`: return the structured figure description and recommended aspect ratio
- `prompt-chain`: return planner, stylist, visualizer, and critic prompts as separate blocks
- `paste-ready`: return one long prompt for Gemini, GPT Image, Nano Banana, or similar image models
- `critic-pass`: analyze a generated figure and return revision instructions plus a revised prompt

## Reference File

When you need the full reusable templates, read:

- [references/prompt-templates.md](./references/prompt-templates.md)

Use that file for the exact long-form prompt text, field names, and the consolidated paste-ready prompt.
