# Agent Shape Decision Frame

## Summary

**One-sentence:** Playbook that frames "what shape of agent do we build" — single-turn, multi-turn, single-agent, multi-agent, hosted vs custom — into a step-by-step decision with named exit criteria, branches, and owner.

**One-paragraph:** Teams often start building an agent by picking a framework (LangChain, CrewAI, Claude Agent SDK) before deciding what shape the agent should be. This playbook reverses the order: it walks an operator through five framing questions (turn count, agent count, tool surface, deployment surface, evaluation surface), produces a structured decision record naming the chosen shape and the rejected shapes with reasons, and hands that off to architecture for framework selection. Output is one decision record per agent feature.

**Ефективно для:** Команд, які тиждень обговорюють «давайте multi-agent» без чітких критеріїв; playbook за дві години дає документований вибір форми, де кожна гілка має сигнал і відповідального — і його можна показати CTO без переробки.

## Applies If (ALL must hold)

- New agent feature is being scoped (no shape committed yet).
- At least two candidate shapes are plausible (otherwise the decision is trivial).
- A named architecture owner can sign off on the final shape.
- Token budget for the feature has at least a rough ceiling.
- Evaluation strategy is open — not pre-locked by an existing harness.

## Skip If (ANY kills it)

- Shape is already implemented and shipped — use a refactor playbook instead.
- Feature is so narrow that a single tool call solves it (no agent needed).
- Team has < 2 weeks of agent experience — pick the smallest shape (single-turn single-agent) without ceremony.
- Decision has been made by leadership for reasons outside this frame.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Feature brief | 1-2 page Markdown | Product / sponsor |
| Token / cost ceiling | $ or tokens / month | Finance |
| Existing eval surface (if any) | list of evals + golden sets | QA |
| Named owner | handle | Architecture |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/agent-patterns/AGENTS.md` | Once shape is picked, pattern selection runs next. |
| `geek/ai/ai-agents/ai-agent-patterns/AGENTS.md` | Overview of pattern landscape. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: named steps, explicit branches, deviation log, named owner | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the agent-shape decision record | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns (vague branch, missing owner, etc.) | ~900 |
| `content/04-procedure.xml` | medium | 5 framing questions and the order in which they bind | ~900 |
| `content/05-examples.xml` | medium | Worked example: shape decision for a customer-support agent | ~900 |
| `content/06-decision-tree.xml` | essential | Tree from turn-count → agent-count → tool-surface → deployment-surface → eval-surface | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `input_collection` | haiku | Structured gather from inputs |
| `decision_steps` | sonnet | Apply playbook branches against state |
| `synthesis_writeup` | sonnet | Final artefact authoring |
| `executive_review` | opus | Architecture sign-off on multi-agent shapes |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the agent-shape decision record. |
| `templates/shape-record.example.json` | Filled minimal valid example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the decision record against the schema. | After subagent emits record, before architecture review. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[agent-patterns]] — pattern selection inside a chosen shape.
- peer: [[bundle-vs-split-tools]] — single-agent vs multi-agent tool partition.

## Decision tree

See `content/06-decision-tree.xml`. Asks five framing questions in order: turn count, agent count, tool surface size, deployment surface (hosted / custom), eval surface availability. Leaves point to one of: single-turn-single-agent, multi-turn-single-agent, multi-agent, hosted-only (use Claude Code headless), or escalate-to-research.
