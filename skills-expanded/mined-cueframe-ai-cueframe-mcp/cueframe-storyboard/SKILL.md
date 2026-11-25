---
name: cueframe-storyboard
description: >-
  Use BEFORE composing when starting a NEW video from scratch and you need to plan its structure — turning a rough ask ("make a launch video", "30s promo", "an explainer for our API") into a concrete beat flow. Owns the intake + storyboard step: interview the user for the brief, resolve the format from the platform, and plan beats from the leading material and requested format. Triggers on "plan a video", "storyboard", "structure this video", "outline the video", "where do I start", or any new-video ask that has no structure yet. Hand off to composing-video for per-beat craft.
---

# CueFrame Storyboard: brief → flow

Use the [project and capability policy](../composing-video/references/project-policy.md) for scope, current state and metered work.

This is a new-video planning workflow. For revisions to an approved plan, preserve its structure
and use `cueframe-compose-loop`'s [preview workflow](../cueframe-compose-loop/references/preview-workflow.md)
to verify the requested change; do not restart intake, Director authoring, or final export by default.

Plan here from the user's context. Direct authoring uses the available composition/component tools; hosted Director authoring is an optional execution lane when `create_brief` and `compose` are actually exposed. Neither lane substitutes for deciding the user's acceptance criteria.

## 1. Interview for the brief — ask only what you can't infer

Fill the brief from the conversation first; ask the user **only for the 1–2 things you genuinely cannot
infer**, and STATE what you assume for the rest. Never wall them with a form.

- **Goal / intent** *(required)* — what is this video FOR? launch, promo, explainer, demo, teaser, recap.
- **Platform** *(sets the format)* — reels / tiktok / shorts → **9:16, ~20s** · youtube → **16:9, ~45s** ·
  linkedin / x → **1:1, ~20s** · web → **16:9, ~30s**. (Or an explicit aspect ratio + duration.)
- **Audience**, **tone** (punchy / premium-calm / playful / authoritative), optional **CTA**, **must-includes**
  (a number, a name, a screen), **references** (a style to echo), **brand kit**.

If the ask is "make a launch video for our API," you already have goal + a hint of audience — ask "Reels,
YouTube, or your site?" and infer the rest: *"I'll assume a developer audience and a punchy tone — say if
you'd rather it feel calm/premium."* One or two questions, not seven.

## 2. Structure the flow — the storyboard

Lay the requested duration into **beats** using the available editorial vocabulary
**hook → context → body → proof → cta → outro** (use only what the piece needs; no fixed count or required CTA). For each beat decide:

- a one-line **intent** (what this beat does for the viewer),
- a **duration** (they sum to the target; the hook earns attention in ~3s),
- a **media need**, if any: actual footage, product action, sourced data, diagrams, typography or abstract motion as requested,
- optional graphics, captions and voice; preserve requested silence and deliberate holds.

Choose the leading material first: narration, recorded speech, product action, visual/music motion or observational sequence. Read `get_media_context` when source facts or transcript timings affect the plan. Discover existing primitives with `list_catalog` when available; custom authored graphics are also valid. Never invent a catalog entry, media ID, transcript or factual product capture.

## 3. Execute the plan in the available lane

Give a concise outline when useful. Continue within existing authorization; request approval only when the user requested a review gate or a decision is genuinely missing.

**Direct authoring:** use the exposed composition operations and existing project assets, then the scoped preview workflow. A local project does not require hosted registration, `create_brief`, `compose` or a paid judge. Read the actual local contracts; desktop setup is documented at https://docs.cueframe.ai.

**Hosted Director, when available and selected:** check `get_account` and current quotes before metered imports, generation or composition. Persist the accepted plan with `create_brief`, including only supported fields. Pin recorded moments with `source: {mediaId, startSec, endSec}` where supported. Relay its compose/render quote before `compose {briefId}`. Use `holdAt` only for a requested gate and `autoApprove` only when authorized and supported. Do not silently upload local content or move to a different project to obtain this lane.

Review with stills plus motion/audio evidence appropriate to the affected content. Cards can animate; a still alone cannot verify their motion. Use `score_composition` for broader review only when useful; export with `create_render` when final delivery is requested. Then load **composing-video** for applicable craft guidance.

## Related skills & positioning

This skill owns **structure/intake**; its siblings own execution and craft — defer to them:

- **composing-video** — the craft/quality layer (grounded specificity vs. slop, the vision → rubric →
  verify loop). Load it *after* you have a flow; it makes each beat good.
- **cueframe-compose-loop** — the author → render → verify → fix convergence loop + the ship bar.
- **cueframe-product-video** — click-points → auto-zoom tiling + PiP for screen demos.
- **cueframe-brand-demo** — brand-token vocabulary + auto intro/outro/logo for branded launches.
- **cueframe-component-authoring** — fork → preview → push for a custom graphic a beat needs.
- **cueframe-cli** — the `cueframe` binary + wire mechanics.

## The boundary

You own the **vision** (the one idea and the flow for *this* video) and **data correctness** (a wrong
number you supply is rendered faithfully — the mistake is yours). CueFrame owns being faithful, legible,
and giving you real footage + real components to plan against. Reason from this; use this planning flow only when new work needs structure.
