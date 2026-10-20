---
name: unitree-unifolm-wla-open-data
description: Applies Unitree's Sept 10, 2026 full open-source release of UnifoLM-WLA-1.0 — a 6B-parameter humanoid robot foundation model released with code, weights, and ~2,500 hours of real-world robot data (trained on 5M+ embodied-reasoning samples) — as the reference case for embodied-AI data-layer openness, including the credibility questions (the leaderboard showed UnifoLM-ER-1-4B in first place, not WLA-1.0; no company response at writing). Use when [tracking open embodied-AI stacks, evaluating robotics data-moat strategies, or building on open humanoid models]. NOT for [general LLM open-weight economics (see china-open-source-llm-arr-tracker) or hardware specs of humanoid platforms].
---

# Unitree UnifoLM-WLA-1.0: The Data-Layer Open Stack

## Overview
Unitree moved beyond the now-common open-weights release in robotics to open the expensive layer: real-world robot operation data. The 6B model handles 64 tasks spanning desktop manipulation and whole-body mobile operations, but the strategic substance is Unitree staking the underlying execution layer of embodied AI rather than competing purely on hardware sales.

## When to Use
- Evaluating whether to build on open humanoid/embodied stacks (fine-tuning without your own data collection)
- Comparing open-weights-only vs open-data releases in robotics
- Assessing credibility of SOTA claims in vendor-led embodied benchmarks
- Strategy work on where robotics value accrues (foundation models vs execution layer vs hardware)

## Core Process / Workflow
1. **Inventory the release.** UnifoLM-WLA-1.0: 6B parameters; code + model weights + training dataset, all released (Sept 10, 2026, official WeChat announcement). Trained on 5M+ embodied-reasoning samples and ~2,500 hours of high-quality physical-robot data.
2. **Test the claims.** Unitree says single-model handling of 64 tasks (desktop manipulation + whole-body mobile operation), generalizing across tasks and end effectors, supporting parallel grippers and five-finger dexterous hands; claimed top-7-benchmark open-source ranking and matching of leading closed models.
3. **Flag the inconsistency.** The leaderboard in the same posting shows UnifoLM-ER-1-4B in first place, not WLA-1.0 — the SOTA claim's referent is ambiguous; the Yangtzeer queried Unitree with no response at publication. Treat vendor benchmarks as unverified.
4. **Weigh the data layer properly.** Real-robot data is expensive: a robot may yield only a few usable hours of operation data per day, requiring cleaning, alignment, labeling. Opening ~2,500 hours lowers the barrier for outside developers to fine-tune or test new architectures — that, not the 6B weights, is the differentiator.
5. **Read the strategic layer.** Positioning as the execution layer beneath general-purpose semantic/task-planning models: large general models handle semantics and planning; embodied models translate plans into physical actions. For competitors, the move pressures the "who owns the software layer between general AI and physical robots" question.

## Key Evidence
- Announcement Sept 10, 2026 (Unitree official WeChat); parameters and data figures from the announcement.
- The library's `humanoid-embodied-ai-open-stack-2026` already tracks the open humanoid datasets layer (EgoHumanoid/RoboCOIN/AgiBot World on G1/H1/Kuavo platforms) — WLA-1.0 adds the first full model+data stack from the dominant hardware vendor itself.

## Pairs-with
- `humanoid-embodied-ai-open-stack-2026` (the broader open-stack map), `ai-sovereignty-hardware-stack`, `china-open-source-llm-arr-tracker` (weights-verification discipline applies to robotics too), `open-source-agency-argument`.

## A-Tech Alignment
- **Open source:** model + data + code in one release — the fullest embodiment of "open source is more than open weights" in robotics to date.
- **Privacy:** real-robot datasets raise capture-context questions (homes/workspaces in frame); a watch item for any data reuse.
- **Financial freedom:** free 2,500 hours of embodied data materially de-risks small robotics/AI ventures that cannot afford fleet collection.
- **Practical:** the credibility checklist (which model actually tops which leaderboard) is the reusable method.

## Honesty Caveats
- All performance claims vendor-sourced via official WeChat; benchmark-table inconsistency unresolved at writing.
- "State of the art" may refer to a different model in the same family than the released weights — verify against the actual WLA-1.0 artifacts before citing.

*Source: Unitree official WeChat (Sept 10, 2026) via The Yangtzeer (Sept 11, 2026).*