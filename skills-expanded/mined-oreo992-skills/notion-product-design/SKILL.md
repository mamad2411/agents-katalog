---
name: notion-product-design
description: Use when analyzing, designing, critiquing, or explaining a product, feature, workflow, UI/UX interaction, design journey, or AI agent through Notion's product-design philosophy and source-backed cases; especially for composability, blocks, progressive disclosure, flexibility versus simplicity, direct manipulation, system consistency, and craft details. Also trigger for Chinese requests about Notion 产品设计理念、设计旅程、UI/UX、交互细节、block、Synced Blocks, or using Notion as design guidance.
---

# Notion Product Design

## Core principle

Treat Notion as a design system for user agency, not a visual style. Analyze how a small set of composable primitives becomes approachable through familiar actions, progressive disclosure, templates, contextual UI, and meticulous state design.

## Workflow

1. **Name the user's real goal.** State the desired user feeling and job before discussing UI.
2. **Classify the problem scale.** Use Chair, Car, or City; read `references/design-process.md` when scope or reversibility is unclear.
3. **Model the system.** Identify objects, identity, relationships, permissions, views, and shared versus local state. Read `references/primitives-and-interactions.md`.
4. **Walk the full journey.** Cover discovery, creation, empty state, reading, editing, collaboration, errors, destructive actions, recovery, mobile, keyboard, performance, and accessibility.
5. **Inspect the tensions.** Explicitly weigh flexibility/opinionation, power/approachability, quietness/discoverability, consistency/contextual exceptions, and automation/control.
6. **Retrieve only relevant Notion evidence.** Route to the references below; do not load every file by default.
7. **Separate evidence levels.** Label claims as **Fact**, **Inference**, or **Guidance**. Before calling present behavior a Fact, open the primary source and verify it in the current turn. A URL listed in a reference is a route, not proof that it was checked. If current verification is unavailable, say “as documented on [source date]; not rechecked today.”
8. **Lead with the verdict.** Explain what the user feels, why the design produces that feeling, how the interaction produces it, tradeoffs, and recommendations.

Answer in the user's language unless they ask otherwise.

## Reference routing

| Need | Read |
|---|---|
| Mission, origins, Kyoto rebuild, product eras, design DNA | `references/history-and-philosophy.md` |
| Block/Page/Database/View/Template mental models and UI grammar | `references/primitives-and-interactions.md` |
| Chair/Car/City, fitness, exploration, state and risk methods | `references/design-process.md` |
| Comments, Synced Blocks, spacing, sidebar, search, mobile cases | `references/case-studies.md` |
| Calendar, Mail, AI, Agents, Developer Platform | `references/product-evolution.md` |
| URLs, dates, authority, freshness, citation selection | `references/source-index.md` |
| Full Chinese research journey and integrated synthesis | `references/research-report.zh.md` |
| Exact 2022 talk wording or timestamp | `references/design-matters-2022.en.srt` |

## UI/UX inspection contract

For an interaction review, always answer these seven slots:

1. **Feeling:** What should the user feel—control, calm, speed, safety, possibility, continuity?
2. **Prior intuition:** What familiar mental model does the user bring?
3. **Signal:** What makes a special object or state recognizable before consequences occur?
4. **Mechanism:** Which primitive, state transition, or information relationship makes it work?
5. **State journey:** What changes between rest, hover, focus, edit, success, conflict, and delete?
6. **Tradeoff:** What became quieter, harder to discover, more powerful, or riskier?
7. **Recovery:** How can users inspect impact, undo, unsync, restore, or request permission?

Use a state table when three or more states differ. Use a flow only when sequence or branching is the core issue.

## Notion-derived heuristics

- Keep normal actions normal; make exceptional semantics explicit at the decision point.
- Use familiar actions to enter unfamiliar models, but never silently change the familiar action's default meaning.
- Keep reading surfaces quiet; reveal structure on hover, focus, edit, or risk.
- Let visual weight track consequence: light for reversible exploration, heavy for shared, destructive, public, or autonomous actions.
- Preserve user intent through reversible transformations.
- Share identity and data; allow local views when the job requires them.
- Design relationships and combinations, not isolated components.
- Let templates package proven assemblies without creating a second underlying product.
- Treat latency as interaction design: a tool for thought must respond at the speed of thought.
- For agents, make scope, evidence, permissions, logs, cost, and reversal first-class UI.

## Evidence discipline

- Prefer Notion design/engineering posts, help docs, release notes, first-person talks, and founder interviews.
- Use launch materials for historical intent and current help docs for current behavior.
- Treat the analytical frameworks and recommendations in these references as guidance, never as proof that Notion currently implements them.
- Do not present remembered UI copy, color, version, team size, or permission behavior as current fact without verification.
- Cite the closest source to the claim; do not use a broad company-history source for a specific interaction detail.
- When evidence is incomplete, say so and continue with a clearly marked inference.

## Common mistakes

- Copying Notion's monochrome look, emojis, or sparse layout without its object model.
- Calling every simple surface “progressive disclosure” without identifying the trigger and hidden capability.
- Treating flexibility as free; account for onboarding, governance, performance, permissions, and edge-state costs.
- Enforcing mechanical consistency when context requires an explicit exception.
- Describing a feature without explaining the user's prior intuition and resulting feeling.
- Treating Notion as universally exemplary; audit accessibility, mobile behavior, and current limitations independently.
- Promoting a recommended governance mechanism—such as approval, rollback, budgets, or logs—into a claimed Notion feature without opening a primary source that states it.
- Turning this skill into a Notion tutorial when the task is product-design guidance.

## Output shape

Use the smallest structure that fits:

1. Verdict
2. Intended user feeling
3. Why the design creates it
4. Interaction/state details
5. Tensions and failure modes
6. Actionable recommendation
7. Evidence and inference notes

For historical research, replace sections 2–6 with a sourced timeline plus invariant principles and changed assumptions.
