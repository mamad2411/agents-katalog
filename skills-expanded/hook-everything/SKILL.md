---
name: hook-everything
description: Build ethical psychological hooks, trust signals, and human-sounding copy across writing and product UX. Use when drafting or auditing copy, campaigns, or onboarding flows.
---
# Hook Everything (v5.1)

Architect invisible psychological pull, live market relevance, deep credibility, and natural human prose across marketing, writing, and product projects in any language.

## When to Use

Use this suite when researching live market trends and Voice-of-Customer (VoC) language via `skills/market-intelligence` (while filtering out forced trend-jacking), calibrating tone and proof density to specific audiences via `skills/audience-calibration`, or brainstorming non-cliche hook concepts via `skills/creative-ideation`. It also governs layering 3-4 mechanisms simultaneously via `skills/hook-compounding`, designing zero-scam marketing campaigns (`skills/marketing-hooks`), structuring spatial layouts (`skills/visual-ux-hooks`), building product flows (`skills/product-hooks`), writing long-form pieces (`skills/writing-hooks`), and auditing text in any language so it passes all 85 rules in `skills/anti-slop` and scores `<= 15/100` on `tools/slop_scan.py`.

## The 7-Stage Execution Pipeline

1. **Scan Live Market & Filter for Organic Fit (`skills/market-intelligence/SKILL.md`)**
   Query live market signals and 2-to-4 star user reviews. Apply the **Organic Fit Gate** so a market trend is woven in only if it causally impacts the user's problem.
2. **Calibrate to Audience & Channel (`skills/audience-calibration/SKILL.md`)**
   Check whether the audience is in Central Route (high scrutiny, low construal) or Peripheral Route (fast-scrolling, low ability) processing, then set register and evidence density.
3. **Ideate via Bisociation (`skills/creative-ideation/SKILL.md`)**
   Discard the first 3 default LLM ideas (`First-3 Graveyard`) and collide real user friction with 6 structural lenses.
4. **Establish Trust & Compose Hook Chords (`skills/trust-architecture/SKILL.md` + `skills/hook-compounding/SKILL.md`)**
   Combine `Trust Damper + Cognitive Anchor + Active Generator + Forward Vector` and rotate chords horizontally.
5. **Apply Spatial & Perceptual Structure (`skills/visual-ux-hooks/SKILL.md`)**
   Structure visual isolation (Von Restorff), choice caps (Iyengar & Lepper), skimmer eye-brakes, and response timing.
6. **Execute Domain Playbook (`marketing-hooks`, `writing-hooks`, or `product-hooks`)**
   Draft the deliverables with micro-commitment ladders, regret elimination, and earned payoffs.
7. **Enforce 85-Rule Anti-Slop, Self-Review & 13-Point Value Gate (`anti-slop` + `self-review` + `value-check`)**
   Run `python3 tools/slop_scan.py <file> --fix-hints` (target `<= 15/100`) and reread the draft as a native reader with `skills/self-review/SKILL.md` and rewrite anything that still sounds machine-made, then verify all 13 checks in `value-check`.

## Bundled Skills & Tools (13 Skills + CLI Scanner)

| Resource Path | Role in the Suite |
|---|---|
| `skills/psychology-map/SKILL.md` | 30 empirical behavioral and trust mechanisms across 6 layers. |
| `skills/trust-architecture/SKILL.md` | ABI trust model, inoculation, operational transparency, and costly signaling. |
| `skills/market-intelligence/SKILL.md` | Live web VoC/competitor mining and the Organic Fit Gate (no forced trends). |
| `skills/audience-calibration/SKILL.md` | ELM Central/Peripheral routing and Construal Level calibration. |
| `skills/creative-ideation/SKILL.md` | First-3 Graveyard pruning and Koestler Bisociation hook generator. |
| `skills/hook-compounding/SKILL.md` | Combining 3-4 hooks simultaneously (5 Master Chords) and horizontal rotation. |
| `skills/visual-ux-hooks/SKILL.md` | Von Restorff isolation, Choice Overload, eye-tracking brakes, and timing thresholds. |
| `skills/marketing-hooks/SKILL.md` | High-conversion, zero-scam behavioral conversion architecture. |
| `skills/writing-hooks/SKILL.md` | Openers, False-Summit retention bridges, 90/10 generation gaps, and pacing. |
| `skills/product-hooks/SKILL.md` | Sandbox onboarding, Day 1-30 habit graduation, multiplayer loops, and offboarding. |
| `skills/anti-slop/SKILL.md` | 85 deep stylometric, cross-linguistic, and anti-hype rules. |
| `skills/self-review/SKILL.md` | Cold reread as a native reader in any language, with up to 3 rewrite rounds. |
| `skills/value-check/SKILL.md` | 13-point ethical, payoff, organic-fit, and subtlety gate. |
| `tools/slop_scan.py` | Zero-dependency Python CLI scanner (v5.1) measuring 18 stylometric and anti-hype indicators. |
| `research/SOURCES.md` | 31-row primary academic literature, rating key, and replication audit. |
| `examples/before-after.md` | 16 annotated transformations across all domains. |
