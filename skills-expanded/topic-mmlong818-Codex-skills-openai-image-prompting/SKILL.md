---
name: openai-image-prompting
description: Create, improve, and evaluate prompts for OpenAI image generation or editing, including exact text, reference preservation, transparent assets, diagrams, UI mockups, and iterative edits. Use when the user needs an image prompt or a prompt-driven image workflow; do not use for image understanding alone.
metadata:
  short-description: OpenAI image generation and editing prompt craft
---

# OpenAI Image Prompting

Turn the user's visual goal into an executable image brief, then generate or edit the image when the request includes execution.

## Workflow

1. Identify the deliverable and intended use: generation or edit, subject, canvas/aspect ratio, audience, and success criteria.
2. For model names, parameters, limits, availability, or migration advice, verify the current [official image prompting guide](https://developers.openai.com/api/docs/guides/image-prompting) before recommending values. Keep request parameters separate from prompt prose.
3. Write the prompt in the simplest maintainable form. For complex work, use labeled sections such as `Goal`, `Scene`, `Subject`, `Composition`, `Style`, `Text`, `Preserve`, and `Constraints`.
4. Describe visible evidence: placement, scale, materials, lighting, texture, color, atmosphere, and medium. Treat lens or camera terms as appearance cues, not physical guarantees.
5. For edits, state the one intended change first, then explicitly list what must remain unchanged. Assign each reference image a role when several are supplied.
6. If the user asked for an image rather than prompt text, use the available image-generation capability. Do not stop after drafting the prompt.
7. Inspect the result against the brief. Refine one variable per turn so the effect of each change is observable.

## Non-negotiable checks

- Exact text: quote the copy verbatim, specify how many times it appears, prohibit extra text, then verify spelling and legibility.
- Identity or product fidelity: preserve defining features, geometry, labels, pose, framing, lighting, and any other locked details relevant to the request.
- Local edits: name the target precisely and say that all unrelated regions must remain unchanged. Prompting cannot guarantee pixel identity; use compositing when exact unchanged pixels are required.
- Transparency: request an isolated subject in the prompt and set a transparent background in the request. Use PNG or WebP and verify a real alpha channel; a checkerboard drawn into the image is not transparency.
- Diagrams, charts, slides, and historical scenes: verify facts, labels, relationships, dates, and supplied data independently. Visual plausibility is not factual proof.
- Repeated edits: restate preservation constraints and inspect every output because details can drift across turns.

## Detailed patterns

Read [references/prompt-patterns.md](references/prompt-patterns.md) when the task involves exact text, logos, UI, educational visuals, multi-reference edits, character consistency, transparency, or production evaluation.

Source basis: [OpenAI Image Prompting](https://developers.openai.com/api/docs/guides/image-prompting), reviewed 2026-09-10.
