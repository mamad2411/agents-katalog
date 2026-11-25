---
name: taste-brief
description: Turns a PRD, feature list, user story dump, screenshot or one-line app idea into a BUILD_MANIFEST.md (users, jobs, flows, views, states, data contracts, component inventory) before any UI is generated. Use when the user says "build this app", pastes requirements, or starts a new product in a vibe-coding tool. Part of the Tastemaker suite; prevents scope drift and generic layouts.
---

# Taste Brief: requirements to Build Manifest

Generic UI comes from generic understanding. This skill extracts what is specific about the product, then fixes it in a manifest every later step reads.

## Procedure

1. **Extract** from the input: product one-liner, primary and secondary users, the 3 jobs each user hires the product for, risk level (regulated, money, health, safety), data density, devices, locale/RTL, existing stack and brand assets.
2. **Classify the archetype** (drives taste-direction): `data-workspace` · `crud-admin` · `consumer-app` · `marketing-site` · `content/editorial` · `commerce` · `devtool` · `form-heavy/workflow` · `realtime/monitoring`.
3. **Derive flows**: for each job, the shortest path as numbered steps ending in a success state. Mark the one critical flow.
4. **Derive views** from flows, not from habit. Each view lists: purpose (one line), the user's top 3 questions on that view, primary action, data it reads/writes.
5. **State matrix** per view: loading, empty, error, permission, success, plus domain states (e.g. "invoice overdue").
6. **Data contracts**: `METHOD /path -> TypeName` with a TypeScript type per entity (realistic field names, units, enums).
7. **Component inventory** bottom-up (atoms, molecules, organisms, templates), each marked `reuse` (exists in kit/project) or `new`. Delete anything not traceable to a flow.
8. **Gaps**: list unknowns. If one would change architecture, ask (max 3 questions, one message). Otherwise record an assumption and continue.

## Output: `BUILD_MANIFEST.md`

Use `references/manifest-template.md`. Keep it under 120 lines; it is a working document, not a spec novel. In chat platforms show a 10-line summary and keep the rest internal unless asked.

## Rules

- Never invent business facts (prices, customer names, compliance claims). Mark them `ASSUMPTION:` or `DATA NEEDED:`.
- Seed data must look true for the domain: plausible names across cultures, realistic amounts and dates, edge cases (long names, zero values, nulls).
- Screenshot or competitor input: extract structure and jobs, never copy brand, copy or distinctive visuals.
- Archetype + top-3-questions are mandatory; taste-direction refuses to choose a layout without them.
