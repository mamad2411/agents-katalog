---
name: vibe-deep-research
description: Research a product idea or existing project before planning or building. Use for evidence-backed product and competitor research, frontend interaction and UI reference research, backend/data/Agent architecture research, open-source reference discovery, implementation trade-off analysis, and recommendations that need a user's decision before Context and decision documents are written.
---

# Vibe Deep Research

Research the decisions behind a product idea; do not start writing its product, technical, or UI specification yet. This Skill has two explicit stages: research and decision request first, then Context synthesis only after the user has made the material choices.

## Stage A — research and decision request

### 1. Establish the research brief

Extract the target user, job, desired result, current state, known constraints, source material, access boundaries, and decisions retained by the user. Ask only for facts whose absence would materially change the research, such as an existing repository, target data access, budget/privacy limit, expected deployment shape, or required output directory.

For an existing project, read its instructions, README, relevant source, configuration, tests, and Git history before generalizing. For external facts that may change, prefer authoritative primary sources. Treat inaccessible/private material as an access boundary, not evidence.

### 2. Research the relevant dimensions

Use [the research lens](references/research-lens.md) selectively. Depending on the idea, research product/competitor patterns, frontend and responsive interaction references, backend/data/integration options, Agent/RAG/workflow fit, open-source implementation references and licenses, and deployment/lifecycle constraints.

Do not turn this into a catalogue of tools. For each reference, state whether it is product inspiration, implementation evidence, or a reusable asset, and do not copy third-party material without checking its license.

### 3. Produce research, not a hidden specification

Use [the research decision memo template](assets/research-decision-memo-template.md). Produce or save `research.md` when an output directory is supplied; otherwise provide the memo in the conversation and ask where it should be saved before a file write.

Separate confirmed facts, evidence, recommendations, assumptions, and unknowns. End `research.md` with a `Decision request` section containing only decisions the user must make. Each decision must state why it matters now, options, a recommendation with evidence, and consequences for scope, cost, data, privacy, and deployment where relevant.

Do not choose a product direction, data source, model/Agent architecture, external dependency, recurring cost, privacy exposure, publication target, or production deployment on the user's behalf.

## Stage B — synthesize the confirmed Context

Run this stage only after the user has answered the decision request or explicitly authorized the remaining assumptions. Use [the Build Context template](assets/build-context-template.md) to turn the original idea, research evidence, and the user's decisions into a compact, stable `context.md`.

Fill every applicable section from the source project-start prompt: background and goal; focus areas; the three required deliverables; technology and target constraints; existing Context; work order; and tool authority/decision boundaries. Do not force Next.js, a directory layout, a UI tool, or a handoff policy when the user did not specify one; label a suggested default as a suggestion.

Set `Status: User-confirmed` only when the user has confirmed the research-level direction and the authority boundary for the three document drafts. Keep any explicitly permitted document-level options labelled `Draft` and require final human confirmation before Build. Link the research memo and the user's decision record. Then hand off to `$vibe-decision-docs`.

## Stop boundary

Do not implement, create accounts, deploy, copy third-party code, expose secrets, or publish. If a material direction remains unresolved, stop at the decision request rather than treating a recommendation as a decision.

## Quality check

Before completion, verify that material claims are traceable or labelled as assumptions; references are accessible to the next agent; recommendations match the evidence; real, fixture, proposed, and verified capabilities are not conflated; and the Context tells the next agent exactly what it may and may not decide.
