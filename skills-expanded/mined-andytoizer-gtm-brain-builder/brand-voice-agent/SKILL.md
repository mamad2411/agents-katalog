---
name: brand-voice-agent
description: Build brand guidance and separate speaker-tone profiles for a GTM brain, keeping person-specific tone distinct from sales-copy substance and buyer language.
---

# Brand Voice Agent

Owns `brand/` and tone files under `company/` when present.

## Inputs

- Brand system, website, design files, lifecycle messages, and approved public copy.
- Claude.ai/design projects or exports when the operator is using it to create or refine a brand kit.
- Person-specific writing/speaking samples for each speaker profile.
- Operator/accountable-owner taste review.

## Outputs

- `brand/brandkit.md`
- `brand/design-resources.md`
- `brand/voice-system.md`
- `brand/speaker-tone-{person}.md`
- `company/tone-of-voice.md`

## Claude.ai/Design Workflow

Use Claude.ai/design when the operator wants help turning GTM Brain context into a practical brand kit.

1. Read the smallest useful source set: product truth, approved claims, ICP, messaging, proof approvals, voice system, and existing visual assets.
2. Draft a Claude.ai/design prompt that includes audience, category, desired perception, tone boundaries, visual references, proof constraints, and do-not-claim rules.
3. Tell the operator to open `https://claude.ai/design`, create a brand-kit or design-system project, paste the prompt, and upload approved visual assets.
4. Ask Claude.ai/design for logo usage, color palette with hex values, typography recommendations, layout rules, image style, component examples, slide/social examples, and do/don't examples.
5. Bring the output back into the GTM Brain only after review: approved choices go in `brand/brandkit.md`, project links and exports go in `brand/design-resources.md`, and voice implications go in `brand/voice-system.md`.

## Rules

- Tone is separate from sales copy.
- Speaker tone comes from that speaker's own samples.
- Sales calls and campaign tools inform buyer language, objections, proof, and message performance, not the speaker's voice by themselves.
- Claude.ai/design output is a visual draft until an accountable owner approves it.
- Do not let Claude.ai/design invent positioning, customer proof, or product claims that are not already supported by the brain.
- Use `$design-system-agent` when the user needs a structured design brief, Claude.ai/design walkthrough, Codex implementation/import instructions, or design-system token/component guidance.
- Ask Grill-me before durable taste or tone decisions.
