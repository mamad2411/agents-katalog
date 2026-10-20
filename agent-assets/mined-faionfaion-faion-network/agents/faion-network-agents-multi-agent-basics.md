# Multi-Agent Systems Basics

## Summary

**One-sentence:** Produces a multi-agent orchestration spec — agent roster (role + model + system prompt), coordination pattern, message schema, and termination/budget guards — that can be wired into AutoGen, CrewAI, or LangGraph.

**One-paragraph:** Multi-agent systems split one hard task across multiple specialized LLM calls so each agent works in a smaller context and a focused role. This methodology produces the upstream design artefact — not running code — that downstream framework-specific methodologies (`multi-agent-hierarchical`, `multi-agent-conversational`, `multi-agent-collaborative`, `multi-agent-production-bus`) consume. Roles are non-overlapping ("if you see an `and` in a role, split it"), all communication is structured JSON through the orchestrator, every agent has an explicit token budget, and there is one named decision-making authority.

**Ефективно для:** солопрейнера/арх-інженера на старті агентного проєкту — щоб роли не перетиналися, а пайплайн не зациклювався на координацію.

## Applies If (ALL must hold)

- Task is complex enough that a single agent runs out of context, mixes responsibilities, or produces low-quality output on its own.
- Roles can be made non-overlapping — "researcher / writer / reviewer" is workable, "researcher-and-writer" is not.
- Decision authority for conflicts is nameable upfront (orchestrator, judge, majority vote, human approver).
- Inter-agent contract can be expressed as structured JSON (not free-form prose).
- Budget constraints (tokens / wall-clock) can be assigned per agent and per overall run.

## Skip If (ANY kills it)

- Simple single-step task — orchestration overhead exceeds value.
- Cannot persist messages (no DB, no file, no in-memory store) — agents lose context on transient failure.
- Roles are inherently overlapping and refuse to split — multi-agent will produce duplicated / conflicting outputs.
- Latency budget < 2 s — coordinated multi-agent runs almost always exceed that.
- One-shot proof-of-concept — multi-agent debugging cost outweighs the design payoff at PoC stage.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task description + acceptance criteria | text | product brief |
| Available models + per-model cost | YAML (`{name, in_cost_per_mtok, out_cost_per_mtok}`) | infra config |
| Token / wall-clock budget for full run | int (tokens) + int (seconds) | finance / SLO |
| Failure-handling preference | one of `retry`, `degrade`, `escalate-human` | ops handbook |
| Decision-authority rule | one of `orchestrator`, `judge`, `majority-vote`, `human-in-loop` | governance |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/role-specialized-models` | Pairs each role to the right model (planner=opus, executor=sonnet, classifier=haiku). |
| `geek/ai/ai-agents/multi-agent-design-patterns` | Eight downstream patterns this spec picks from. |
| `geek/ai/ai-agents/schema-version-pinning` | Every inter-agent message carries `schema_version` so role contracts can evolve. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules: non-overlapping roles, structured JSON only, full context per handoff, per-agent budgets, no bidirectional dependencies, explicit termination, named decision authority | ~950 |
| `content/02-output-contract.xml` | essential | JSON Schema for the multi-agent spec deliverable (agents[], pattern, message_schema, termination, budget, decision_authority) + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: role overlap, deadlock, echo chamber, context loss on handoff, synthesizer anchoring, rate-limit amplification | ~800 |
| `content/04-procedure.xml` | medium | 6-step build: task split → role draft → pattern pick → message schema → budget assign → termination + DoR/DoD | ~900 |
| `content/05-examples.xml` | medium | One full worked spec: research → write → edit content pipeline with budgets, model assignment, and termination rules | ~550 |
| `content/06-decision-tree.xml` | essential | Pick coordination pattern (sequential / parallel / hierarchical / debate / collaborative) from task shape | ~350 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Split task into non-overlapping roles | opus | Decomposition needs strong reasoning; cheap models miss role overlap. |
| Draft per-agent system prompts | sonnet | Reliable structured writing of role + constraints. |
| Pick coordination pattern | sonnet | Reads the decision tree; not generative. |
| Estimate per-agent token budgets | haiku | Numeric estimation against a fixed schema. |

## Templates

| File | Purpose |
|------|---------|
| `templates/multi-agent-spec.yaml` | Canonical spec skeleton: roster, pattern, message_schema, budgets, termination, decision_authority. |
| `templates/system-prompt.txt` | One-agent system-prompt skeleton with placeholders for role, responsibilities, forbidden actions, output schema. |
| `templates/_smoke-test.yaml` | Minimum-viable filled spec (3-agent research→write→edit pipeline) usable as eval fixture. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-agent-basics.py` | Validates a multi-agent spec against the output contract (non-overlapping roles, structured message schema, budget present, decision authority named). | Pre-merge of any multi-agent design PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[multi-agent-design-patterns]] — picks one of eight downstream patterns this spec selects from.
- [[multi-agent-hierarchical]] — concrete impl shape for hierarchical pattern.
- [[multi-agent-conversational]] — concrete impl shape for free-turn conversation.
- [[multi-agent-collaborative]] — concrete impl shape for shared-workspace iteration.
- [[multi-agent-production-bus]] — production-grade async message bus that ships any pattern.
- [[role-specialized-models]] — picks model per role.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides coordination pattern from task shape: known decomposition + parallel-safe steps → parallel; known decomposition + dependent steps → sequential; unknown decomposition + clear roles → hierarchical; high-stakes verification → debate; creative open-ended → collaborative. Run it after the role split is drafted, before writing any system prompts.
