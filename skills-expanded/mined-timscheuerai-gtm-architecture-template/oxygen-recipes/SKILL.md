---
name: oxygen-recipes
description: Search, read and install OXYGEN plays: proven GTM motions with prerequisites, credit posture, approval gates and an optional kit of native stages, then adapt the play to the reader's company.
---

# Borrow a proven play

Read the user's goal and [first-batch guide](../../../docs/first-batch.md). A play is advisory: business case, outcome, leading metric, prerequisites, credit posture, approval gates and optionally a kit of native stages.

- Search by goal or constraint: `oxygen recipes list "<goal>" --view summary --limit 6 --json`.
- Read one: `oxygen recipes show <slug> --json`. It reports which kit stages the workspace already has.
- Forecast a kit: `oxygen recipes apply <slug> --dry-run --json`.
- Install a kit: `oxygen recipes apply <slug> --json`. It costs 0 credits, makes no provider calls, leaves every Workflow disabled and skips stages that already exist.

A play the user already selected wins over any default. Installing grants nothing further: running, enabling, enrolling, sending and spending each keep their own preview, cap and approval. To design a motion for this company rather than borrow one, use [oxygen-gtm-consultant](../oxygen-gtm-consultant/SKILL.md). For this repo's functions, prefer [the existing installer](../../../docs/oxygen-setup.md) over duplicate equivalents.

Present a play in plain words: what it gets them, its steps, what the workspace still lacks, what it costs and what each approval asks. Return deep links for every object created.
