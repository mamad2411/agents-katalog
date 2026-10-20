---
name: academic-perspective-builder
description: Define the writing strategy for an academic piece — target audience, writing lens, and key sub-themes — through a short interactive interview. Stage 2 of the academic-pipeline. Use when the user asks to develop a writing perspective, plan an article approach, define who a paper is for, or decide which sub-themes to emphasize.
license: Proprietary - MoxyWolf LLC
---

# Academic Perspective Builder — Stage 2

Lock the writing strategy before any drafting begins: **what lens**, **which audience**, **which sub-themes**. These three decisions shape the whole article.

## Role in the pipeline

Second stage of the `academic-pipeline`. Consumes Stage 1's `TARGET_TITLE` and Mermaid theme tree; produces `perspective.json`, which Stage 5 (`research-analyst`) uses to plan structure.

## Inputs

- **Required:** the topic — Stage 1's `target_title`, or a user-provided title.
- **Optional:** Stage 1's `<target-slug>-themes.md` and theme synthesis (lets you suggest sub-themes from real branches).
- **Optional run folder** — from the orchestrator. If absent, write `perspective.json` beside the Stage 1 outputs (`<run folder>/pipeline/`).

## Human-in-the-loop

This is an **interactive** stage. Collect three decisions with the **AskUserQuestion tool** — one question per decision, each offering concrete options plus a free-text path. Do not write a HITL request file and do not block; just ask. If the orchestrator front-loaded the answers, skip the questions and go straight to *Generate output*.

### Question 1 — Writing perspective

Ask which lens to take for the topic. Offer, as options, the 2–3 perspectives that best fit the bibliography (see *Perspective suggestion logic*), and make the rest available:

- **Critical / skeptical** — questions assumptions, surfaces limitations
- **Historical development** — traces evolution, contextualizes the present
- **Practical applications** — emphasizes real-world implementation
- **Theoretical framework** — prioritizes conceptual foundations
- **Integration** — bridges theory and practice
- **Innovation-focused** — highlights cutting-edge developments
- **Comparative analysis** — examines competing methods or approaches

### Question 2 — Target market

Ask who the primary audience is. Push for specifics: background (academic, industry, policy, general public), expertise level (novice, intermediate, expert), and what they need from the piece (practical guidance, theoretical grounding, critical analysis). Offer representative options but expect a free-text refinement.

### Question 3 — Sub-themes

If a Mermaid diagram is available, list its major branches and ask which 3–5 to emphasize for the chosen audience and lens. If not, ask which 3–5 sub-themes within the topic to emphasize, framed by audience needs and the chosen lens. Use a multi-select AskUserQuestion so the user can pick several.

After all three are in, restate the full strategy (topic, perspective, audience, sub-themes) in one short confirmation message before generating the file.

## Perspective suggestion logic

When proposing perspectives in Question 1, read the bibliography signal:

- Competing approaches across sources → suggest **Comparative analysis**
- Heavy 2024–2025 presence → suggest **Innovation-focused**
- Applied frameworks / case studies → suggest **Practical applications**
- Ethical concerns or limitations foregrounded → suggest **Critical / skeptical**
- Development traced over time → suggest **Historical development**
- Theory plus practice → suggest **Integration**
- Foundational concepts → suggest **Theoretical framework**

Suggest 2–3 aligned options, but always let the user reach any of the seven.

## Generate output

Write **`<run folder>/pipeline/perspective.json`**:

```json
{
  "topic": "<confirmed TARGET_TITLE>",
  "target_market": "<detailed audience: background, expertise level, needs>",
  "writing_perspective": "<one of the seven lenses>",
  "sub_themes": ["<theme 1>", "<theme 2>", "<theme 3>"],
  "key_source_areas": "<Mermaid branch names if available, else empty string>",
  "created_at": "<ISO 8601 timestamp>"
}
```

Confirm to the user that the perspective is saved and note what it will drive: which sources get prioritized, how arguments get structured, which examples lead, and the tone/register.

## Return to the orchestrator

```json
{
  "status": "complete",
  "output_file": "<run folder>/pipeline/perspective.json",
  "topic": "<TARGET_TITLE>",
  "writing_perspective": "<lens>",
  "target_market": "<audience>",
  "sub_themes": ["<theme 1>", "<theme 2>", "<theme 3>"]
}
```
