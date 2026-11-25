---
name: ai-drawing-prompt
description: Create safe, production-ready AI image prompt packs with model-specific controls and iteration plans for OpenAI GPT Image, Midjourney, SDXL, and FLUX. Use when requests involve generating, refining, translating, or debugging image prompts; converting a creative brief into provider parameters; producing negative or avoidance constraints per model; or delivering multiple prompt variants from text briefs and reference images.
---

# AI Drawing Prompt

Build prompts as a reproducible package, not a single line.
Load only the references needed for the target model.

## 1. Lock The Prompt Contract

Capture and confirm:
1. Subject and scene.
2. Visual goal (mood, style, era, lighting, composition).
3. Delivery target (model, aspect ratio, quality/speed preference, output format).
4. Hard exclusions (objects, artifacts, unsafe elements, brand/legal constraints).
5. Number of variants and iteration budget.
6. Reference image plan (optional): source image(s), what to preserve, what must change, and strength (`low`/`medium`/`high`).

If the model is unknown, propose one model choice plus one fallback.

## 2. Load Model References

Always read:
- `references/model_profiles.md`
- `references/safety_and_negative_guidance.md`

Read when needed:
- `references/iteration_playbook.md` for troubleshooting and iterative refinement.
- `references/source_selection.md` when provider rules may have changed and source confidence matters.

## 3. Build The Prompt Package

Produce all blocks:
1. `Primary prompt`: final production prompt.
2. `Parameter block`: model-specific controls only.
3. `Negative/Avoidance block`: provider-correct form (or explicit "not supported").
4. `Reference image block` (if provided): adapter instructions and preserve/change list.
5. `Variant set`: at least 3 controlled variants (style, composition, lighting, camera distance, or detail level).
6. `Iteration plan`: 2-3 rounds with expected failure checks and next edits.

## 4. Enforce Model-Correct Constraints

Apply these hard rules:
- Do not invent unsupported parameters.
- Keep parameter names and ranges aligned with the selected provider profile.
- FLUX: do not emit classic negative prompts as a separate field.
- Midjourney: use `--no` only for allowed, concrete exclusions.
- SDXL: use prompt weights for de-emphasis only when the caller supports weighted prompts.
- OpenAI GPT Image: encode avoidances in natural-language prompt constraints.
- When reference image is provided, explicitly separate `preserve` from `change` instructions.

## 5. Return In A Standard Output Shape

Use this structure in responses:

```markdown
### Prompt Pack
Model: <provider/model>
Intent summary: <1-2 lines>

Primary prompt:
<text>

Parameter block:
<provider-specific key/value or CLI parameters>

Negative/Avoidance block:
<model-correct form or "Not supported by model; constraints folded into main prompt.">

Reference image block:
<optional: input image usage, preserve list, change list, strength>

Variants:
1) <variant A>
2) <variant B>
3) <variant C>

Iteration plan:
Round 1 -> <what to evaluate>
Round 2 -> <what to adjust>
Round 3 -> <final polish controls>
```

## 6. Safety Boundary

If the request is unsafe, illegal, or policy-violating:
1. Refuse the harmful part directly.
2. Offer a safe alternative prompt objective.
3. Continue with compliant prompt construction.
