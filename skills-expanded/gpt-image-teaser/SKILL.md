---
name: gpt-image-teaser
description: Use this skill when the user wants a GPT Image-specific workflow for generating or revising academic teaser figures, method overviews, and research illustrations from paper summaries, methodology sections, captions, or structured figure briefs.
---

# GPT Image Teaser

## Overview

This skill turns paper content into prompts tailored for GPT Image style academic figure generation. It is best when the user wants a compact, paste-ready OpenAI image prompt plus a practical revision loop for teaser figures and method diagrams.

## When To Use

Use this skill when the user asks for any of the following:

- A GPT Image prompt for a paper teaser
- An OpenAI image-model workflow for academic diagrams
- A one-shot or two-pass prompt for method figures
- A revision prompt to fix labels, arrows, layout, or caption leakage in a generated academic figure

Prefer `paperbanana-teaser` instead when the user explicitly wants the full planner-stylist-visualizer-critic decomposition. Use this skill when the user wants the GPT Image-facing layer distilled into a simpler workflow.

## Inputs

Collect as many of these as possible:

- Paper topic
- Core problem
- Prior-work limitation
- Proposed method or system
- Main technical components
- Main takeaway
- Methodology section
- Figure caption
- Target conference style
- Optional reference image for style only

If the input is incomplete, preserve what is known and simplify the visual narrative instead of inventing unsupported details.

## Default Workflow

Use this lightweight sequence:

1. Build a `Figure Brief`
   Summarize the problem, method, and outcome into a faithful teaser narrative.
2. Draft the `GPT Image Prompt`
   Convert the brief into a model-facing prompt with explicit text, layout, and academic-style constraints.
3. Run a `Revision Pass`
   If the first image has bad text, wrong arrows, clutter, or title leakage, issue a focused correction prompt instead of rewriting everything from scratch.

## Working Rules

- Preserve scientific fidelity. No invented modules, claims, or evidence.
- Do not place paper titles, figure captions, figure numbers, watermarks, or UI chrome inside the image.
- Keep labels short, exact, and readable.
- Prefer white or very light backgrounds and a restrained academic color palette.
- Use natural-language visual descriptions, not CSS, hex colors, or pixel specs.
- If the figure has many components, group them into panels or bounded regions to maintain readability.

## Output Modes

- `brief-only`: return the structured figure brief
- `gpt-image-prompt`: return a paste-ready prompt for GPT Image
- `prompt-plus-revise`: return an initial prompt plus a follow-up repair prompt template
- `caption-safe`: emphasize title and caption exclusion for models that often leak text

## Reference File

Read the full templates here when prompt text is needed:

- [references/gpt-image-prompts.md](./references/gpt-image-prompts.md)

Use that file for the figure brief schema, the main GPT Image prompt, and the revision prompt templates.
