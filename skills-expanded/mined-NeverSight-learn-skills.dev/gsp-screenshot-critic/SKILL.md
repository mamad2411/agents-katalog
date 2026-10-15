---
name: gsp-screenshot-critic
description: "Use when critiquing screenshots or visual captures for readability, hierarchy, and target-quality fit."
---

# Game Screenshot Critic

## Goal
Use visual evidence to judge whether the build actually looks understandable and good enough for the target.

## Use
- `../../shared/checklists/screenshot-critic-output-checklist.md`
- `../../shared/checklists/ui-ux-hard-rules.md`

## Focus
- information hierarchy
- clutter
- readability
- playfield protection
- visual coherence
- perceived completeness
- whether feedback cues are visible
- whether persistent HUD feels disciplined or bloated

## By target
- **first-playable**: look for basic readability and affordance
- **polished-prototype**: hold a higher bar for coherence and perceived finish
- **production-feature / live-patch**: check consistency with the rest of the product

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present critique findings and repair priorities in conversation.
- **minimal** or **full**: append to `docs/game-studio/quality-report.md`.

## Reporting rules
Separate:
- confirmed strengths
- confirmed issues
- inferred risks
- repair priorities

## Important
Do not overstate what a screenshot proves.
Use screenshots to strengthen evidence, not to hallucinate certainty.
