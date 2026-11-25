---
name: agentic-marketing-levels
description: The 3 levels of agentic marketing (Assist, Scale, Orchestrate) with what each looks like and the next move, and a self-assessment to place a team. Use when the user asks how far their marketing team is with AI agents or what to do next. Source NipPro AI / Marceline Tsobgny infographic "The 3 Levels of Agentic Marketing" (Batch 102). The percentages are the author's survey figures with no source cited on the slide.
---

# The 3 levels of agentic marketing

| Level | Name | Share of teams (slide) | Looks like | Next move |
|---|---|---|---|---|
| 1 | Assist - "AI writes. Humans do the rest." | 42% | Copy on demand; one task at a time; pilots that stall | Take one workflow end to end |
| 2 | Scale - "AI inside the workflow." | 26% | Content at scale; pilots in production; same old workflows | Redesign the workflow, not the task |
| 3 | Orchestrate - "Agents run it. Humans steer." | 32% | Agents across workflows; human oversight built in; workflows rebuilt; multi-agent campaigns | Give agents your brand rules |

Footer stats on the slide: 96% of CMOs claim a full AI transformation; 8% run campaigns where agents work on their own. The three level shares sum to 100% and the two footer figures do not reconcile with them (32% orchestrate vs 8% autonomous); treat all figures as unsourced.

## Self-assessment (added here)
1. Is each AI task a one-off prompt? -> Level 1.
2. Is AI embedded in a repeatable workflow, but the workflow itself unchanged from before AI? -> Level 2.
3. Were workflows redesigned around agents, with approvals and brand rules written down? -> Level 3.

## In this repo
Level 3 is what `governed-marketing-team`, `governed-marketing` and the `brand-reviewer` agent implement: brand rules in context files, a reviewer gate, a human approving. The AI Entrepreneur OS (`ai-entrepreneur-os`) keeps every agent at draft-only; do not promote anything to "agents work on their own" before you have read 20+ of its drafts.
