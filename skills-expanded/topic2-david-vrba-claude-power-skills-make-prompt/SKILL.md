---
name: make-prompt
description: Craft a high-quality, ready-to-paste prompt for whatever you describe. Adapts to the target — LLM/chat prompt, image-gen, or system/agent prompt — and applies the right prompt-engineering best practices. Produces the prompt, not advice about prompts.
---

The user wants you to **build them a prompt**, not perform the task the prompt describes. Your output is a finished, copy-ready prompt.

The request is in `$ARGUMENTS` (if empty, use the user's most recent message describing what they want a prompt for).

## Step 0 — Identify target and goal

From the request, work out two things:
1. **The goal** — what the finished prompt should make the AI do, and what a good result looks like.
2. **The target system** the prompt is for, which decides the best-practices to apply:
   - **LLM / chat** (Claude, GPT, etc.) — the default if unstated.
   - **Image generation** (Imagen, Midjourney, Stable Diffusion, etc.).
   - **System / agent prompt** (a reusable role/instruction block for an AI agent or app).
   - **Other generative target** (video like Veo/Sora, audio/music, a search query, etc.) — apply that specific tool's known conventions.

Detect the target from the request. **Only ask a question if something essential is genuinely missing** (e.g. the goal is too vague to write a useful prompt, or it could mean two very different things). If you must ask, batch everything into **one** short round, then proceed. If it's clear, just build it.

## Step 1 — Build the prompt using the right best-practices

**LLM / chat prompts:**
- Give role/context, then a single clear task.
- State constraints explicitly (length, tone, what to avoid, what NOT to do).
- Specify the exact output format (structure, headings, JSON, etc.).
- Add a short example (few-shot) only when it genuinely sharpens the result.
- Ask for step-by-step reasoning only when the task needs it.
- Define "done" — the success criteria.
- For Claude specifically, structure with clear sections (and XML-style tags when separating instructions from content helps).

**Image-generation prompts:**
- Cover: subject, style/medium, composition/framing, lighting, mood, color, level of detail.
- Add aspect ratio and any negatives (what to exclude).
- Apply the target model's own conventions. If the user has a model-specific required suffix or boilerplate they always append, include it verbatim at the end of the prompt.

**System / agent prompts:**
- Define the role and scope, the tools/inputs available, hard constraints and refusal boundaries, tone, and the output contract.

Adapt depth to the task — don't over-engineer a prompt for something simple.

## Step 2 — Deliver

1. Output the finished prompt **in a single fenced code block**, ready to copy and paste verbatim. Nothing inside the block but the prompt itself. If the prompt itself contains code fences (e.g. an example with backticks), wrap it in a longer outer fence (````` ```` `````) so it stays one clean block.
2. Below it, **2–3 short bullets** explaining the key choices you made (why this structure / what to tweak). Keep it brief.
3. Offer one quick refinement: e.g. *"Want it shorter, more detailed, with an example, or aimed at a different model?"*

## Principles
- **Ship a usable prompt**, not a discussion about prompting.
- The prompt must be **self-contained and unambiguous** — someone pasting it cold should get a good result.
- Match the **target system's conventions**; don't write a Claude prompt for an image model.
- **One round of questions, only when blocking.** Otherwise build immediately.
