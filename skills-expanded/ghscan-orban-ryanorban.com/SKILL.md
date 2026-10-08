---
title: "Autoresearch Skill: autonomous skill optimization via eval loops"
date: 2026-03-18
categories:
  - claude-code
  - skills
  - prompt-engineering
  - automation
  - developer-tools
description: A Claude Code skill that autonomously optimizes other skills by running eval loops — binary scoring, targeted mutation, keep/discard decisions. Andrej Karpathy's training loop methodology applied to prompt engineering.
params:
  source: pinboard
  sourceUrl: https://github.com/olelehmann100kMRR/autoresearch-skill
---

![Autoresearch Skill: autonomous skill optimization via eval loops](/images/notes/autoresearch-skill.png)

## Summary

Autoresearch is a Claude Code skill that uses an autonomous iteration loop to improve other skills — applying the same methodology that makes machine learning training effective to the problem of prompt engineering. It runs repeated experiments, scores outputs against binary evaluation criteria, mutates prompts, and preserves improvements without requiring user approval between iterations.

The evaluation design uses 3-6 yes/no criteria per test rather than subjective scoring. This binary approach, adapted from Andrej Karpathy's experimental methodology, makes scoring consistent and automatable. The mutation strategy is targeted: single changes that address specific failure patterns, rather than broad rewrites that obscure what actually helped.

The workflow is: establish a baseline, run an autonomous loop of hypothesis → mutation → test → score → keep/discard, log results in real-time through an auto-refreshing HTML dashboard, and output an improved `SKILL.md` plus research documentation. The tool works best when a skill already functions about 70% of the time — it's a tightening mechanism, not a redesign tool.

## Key points

- Binary evaluation (yes/no criteria) enables consistent, automatable scoring across iterations — no subjective judgment needed.
- Single targeted mutations per experiment isolates what causes improvement vs. noise from multi-change experiments.
- Runs autonomously between experiments — no user approval required until a meaningful improvement threshold is hit.
- Live HTML dashboard with real-time score progression — lets you watch the optimization happen.
- Works on skills that are 70% effective needing systematic improvement, not skills that fundamentally don't work.

[Original](https://github.com/olelehmann100kMRR/autoresearch-skill)
