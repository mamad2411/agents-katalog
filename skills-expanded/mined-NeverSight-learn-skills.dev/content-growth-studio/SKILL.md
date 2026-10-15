---
name: content-growth-studio
description: Use when planning, analyzing, rewriting, packaging, producing, or systemizing growth-oriented content across article, video, and social channels. Trigger on requests involving content research from URLs, transcripts, existing articles or scripts, competitor examples, uploaded notes, topic ideation, positioning, title and hook generation, article rewrites, video scripting, repurposing, thumbnail or CTA concepts, editorial workflow design, or repeatable content SOPs. Supports both source-led and brief-led work. Default output is Traditional Chinese for Taiwan unless the user's material clearly indicates another language.
---

# Content Growth Studio

## Overview

Orchestrate cross-channel content growth work from raw sources or a lightweight brief.
Use this skill to decide the right mode, shape the output for the target channel, and hand off narrow subtasks to more specialized skills when deeper logic is needed.

## Workflow Decision Tree

1. Detect `entry_path`.
   - Choose `source-led` when the user provides URLs, transcripts, article text, scripts, title plus outline, competitor examples, or evidence artifacts.
   - Choose `brief-led` when the user mainly provides topic, audience, channel, goal, and voice.
2. Detect `mode`.
   - `analyze`: reverse-engineer what is already working.
   - `ideate`: create niches, positioning, topics, names, or angle sets.
   - `rewrite`: improve an existing draft without changing its core intent.
   - `package`: generate titles, hooks, thumbnail concepts, CTA variants, and interaction assets.
   - `produce`: generate a finished article, script, repurposed assets, or channel-specific draft.
   - `system`: design a repeatable workflow, batch cadence, tool stack, or budgeted SOP.
3. Run the data sufficiency gate.
   - If core inputs are missing and the user did not ask for speed, ask concise follow-up questions.
   - If the user asks for a quick draft, list assumptions first and continue.
4. Select `channel_family`.
   - `article-newsletter-long-form-written`
   - `long-form-video`
   - `short-form-video`
   - `social-engagement-asset`
5. Apply the mode-specific output contract.
6. Invoke other skills only when they own deeper logic. This skill owns routing, scope control, and final assembly.

## Entry Paths

### `source-led`

Use when the user wants analysis, rewrite, extraction, or repurposing from existing material.

Common source artifacts:

- URLs
- transcripts
- article text
- existing script
- title plus outline
- competitor or channel examples
- review, support, or social evidence

### `brief-led`

Use when the user starts from a topic or desired outcome.

Common brief ingredients:

- `topic_or_subject`
- `target_audience`
- `primary_channel`
- `goal`
- `brand_or_voice`
- `constraints`

## Mode Routing

Use `mode: auto` by default.

Auto rules:

- If the request asks "analyze", "拆解", "研究成功內容", "整理公式", or compares sources, choose `analyze`.
- If the request asks for topics, series ideas, channel names, niches, or positioning, choose `ideate`.
- If the request includes an existing draft and asks to polish, tighten, humanize, or improve, choose `rewrite`.
- If the request centers on titles, hooks, thumbnail ideas, CTA, comments, polls, or social prompts, choose `package`.
- If the request asks for a finished article, full script, repurposed post set, or channel-ready draft, choose `produce`.
- If the request asks for workflow, tool stack, SOP, budget, cadence, or batch production planning, choose `system`.

Boundary routing:

- If the request is mainly "build the landing page itself", use `landing-page-studio` for the page and keep this skill only for content packaging.
- If the request is purely about persona definition, use `customer-persona-framer`.
- If the request is strategy-first and behavior-design-first, use `sor-marketing-strategy`.
- If the request needs deep trigger design or CTA psychology, use `psychological-trigger-marketing` or `maslow-five-needs-marketing`.
- If the request is mainly about structured idea expansion, use `scamper`.
- If the request supplies review-like corpora and asks for evidence-backed segmentation, use `review-mining-stp` and related theory skills upstream.

## Input Contract

Need at least one of:

- `source_artifacts`
- `topic_or_subject`

Strongly recommended:

- `target_audience`
- `primary_channel`
- `goal`
- `brand_or_voice`
- `constraints`

See [references/02-input-contracts-and-gates.md](./references/02-input-contracts-and-gates.md) for the compact contract and assumptions policy.

## Data Sufficiency Gate

If the available inputs are enough to produce a useful output, generate directly.

If information is incomplete and the user asks for speed:

1. List `3-5` assumptions first.
2. Keep assumptions concrete and business-relevant.
3. Continue with the requested output.

Do not invent:

- traffic or conversion results
- source facts not present in the material
- competitor data you did not actually observe
- audience insights that should have come from evidence

If the user provides URLs but the linked content is not accessible, ask for transcript, excerpt, notes, or screenshots instead of hallucinating.

## Shared Rules

- Default to Traditional Chinese with Taiwan phrasing unless the user's material clearly indicates another language.
- Preserve the source meaning in `rewrite` mode unless the user explicitly asks for repositioning.
- Keep outputs channel-specific. Do not return a generic structure that ignores the target channel.
- Keep packaging tied to the actual promise of the content, not generic clickbait.
- When ranking titles or hooks, explain the ranking logic briefly if the user asked for prioritization.
- When repurposing one source into multiple channels, preserve the core promise but adapt hook speed, pacing, and CTA to the channel.
- Use specialist skills for deep logic, then reassemble the result into one coherent final output.

## References

- Scope, routing, and boundaries: [references/01-scope-and-mode-routing.md](./references/01-scope-and-mode-routing.md)
- Input contract and missing-data rules: [references/02-input-contracts-and-gates.md](./references/02-input-contracts-and-gates.md)
- Source-led analysis workflow: [references/03-source-analysis-playbook.md](./references/03-source-analysis-playbook.md)
- Channel-specific rules: [references/04-channel-playbooks.md](./references/04-channel-playbooks.md)
- Packaging systems: [references/05-packaging-systems.md](./references/05-packaging-systems.md)
- Output templates by mode: [references/06-output-contracts.md](./references/06-output-contracts.md)
- Handoff matrix to other skills: [references/07-handoff-matrix.md](./references/07-handoff-matrix.md)

## Suggested Prompt

Use `$content-growth-studio` to analyze, ideate, package, produce, rewrite, or systemize growth content across article, video, and social channels.
