---
name: ai-agents-meta-core
description: "Shared reference for the ai-agents-meta cluster: the eval-first + default-deny-autonomy model every spoke turns on, plus shared conventions (the agent stack, cold-start briefs, cost routing tiers) and the gate/loop/cost matrix. USE WHEN wiring an autonomous loop, granting an agent tools, setting an eval gate, or routing by model cost — the interlocking rules every meta spoke shares."
cluster: ai-agents-meta
version: 1.0.0
---

# AI Agents Meta Core

Shared model for the `ai-agents-meta` cluster. The planning, orchestration, loop, audit, and
cost spokes all depend on these interlocking ideas — keep them consistent here so no spoke
contradicts another.

## 1. The decision this cluster turns on: eval-first × default-deny autonomy

Every spoke is an answer to one question: **how much can this agent do on its own, and how do
we know it did it right?** The cluster's stance is two coupled rules:

```
Plan ──gated by──> Eval ──authorizes──> Autonomous step ──bounded by──> Tool / loop budget
```

- **Eval-first** — no step that an agent runs unattended ships without a *gate that can fail
  it* (a test, a review, a schema/assertion, a screenshot diff). The gate is designed *before*
  the step, not bolted on after. → `agentic-engineering`, `dynamic-workflow-mode`, `continuous-agent-loop`
- **Default-deny autonomy** — an agent gets the **narrowest** tool set, permission, and loop
  budget that lets the gated step pass. Widening any of them (a new tool, a higher iteration
  cap, write access) is a governance change worth stating out loud. → `team-agent-orchestration`, `agentic-os`

**Rule:** if you can't name the gate that fails the step, the step isn't ready to be
autonomous — drop it back to a human checkpoint.

## 2. The agent stack (what the audit spokes inspect)

Agent failures localize to a layer. Reason top-down before patching:

| Layer (top → bottom) | Typical failure | Spoke |
|---|---|---|
| Prompt / intent | vague ask, missing constraints | `prompt-optimizer` |
| Plan / decomposition | steps too big, no cold-start brief | `blueprint`, `plan-orchestrate` |
| Orchestration | ownership unclear, merge collisions | `team-agent-orchestration` |
| Loop / control | runs forever, no recovery | `continuous-agent-loop` |
| Tool discipline | wrong tool, hidden repair loops | `agent-architecture-audit` |
| Memory / state | pollution, cross-project bleed | `agentic-os`, `continuous-learning-v2` |
| Model / cost | over-powered model for trivial step | `cost-aware-llm-pipeline`, `token-budget-advisor` |

When something breaks: `agent-architecture-audit` localizes the layer →
`agent-introspection-debugging` runs the contained recovery.

## 3. Shared conventions

- **Research before building.** Every build path opens with `search-first` — find the existing
  tool/lib/skill before hand-rolling one. The cheapest agent step is the one you didn't write.
- **Cold-start briefs.** A planned step must be executable by a *fresh* agent with no prior
  context — self-contained inputs, outputs, and done-criteria. → `blueprint`.
- **Generative, not executive, advisors.** `prompt-optimizer` and `plan-orchestrate` *emit*
  paste-ready artifacts; they never run the task themselves. Keep that boundary.
- **Project-scoped learning.** Instincts/skills minted from one project stay scoped to it;
  never let learned state contaminate another repo. → `continuous-learning-v2`.

## 4. Cost-routing tiers

Route by **task complexity, not habit**:

| Task shape | Route | Spoke |
|---|---|---|
| Deterministic / structured | code or a small/cheap model | `cost-aware-llm-pipeline` |
| Bounded reasoning, repeatable | mid-tier model + cache | `cost-aware-llm-pipeline` |
| Open-ended / high-stakes | top model, gated | `agentic-engineering` |
| Per-answer depth control | offer the user a budget | `token-budget-advisor` |

Prompt caching, retry-with-backoff, and budget tracking are baseline, not optional →
`cost-aware-llm-pipeline`.

## 5. Gate / loop / cost matrix

| Concern | Default posture | Widen only when… |
|---|---|---|
| Autonomy | human checkpoint at each handoff | the step has a failing-capable gate |
| Tools granted | read-only, minimal set | the gated step provably needs more |
| Loop budget | hard iteration + time cap | recovery + eval prove convergence |
| Model tier | cheapest that passes the gate | complexity demands it |

## 6. Version / tooling

- Built for **Claude Code** as the primary host (slash commands, skills, hooks, file-based
  memory) but the patterns are host-agnostic. → `agentic-os`, `dynamic-workflow-mode`.
- `continuous-learning-v2` is **v2.1** (project-scoped instincts; supersedes v1's global store).
- Orchestrators that namespace agent/command names by install form keep **one form per output**
  — never mix plugin-prefixed and bare names. → `plan-orchestrate`.

## 7. Shared guardrails

- **Eval-first**: no autonomous step without a gate that can fail it.
- **Default-deny autonomy**: narrowest tool/permission/loop budget that works; state every widening.
- **Search before build**: `search-first` opens every build path.
- **Route by complexity**: cheapest model/tier that passes the gate; caching + retries baseline.
- **Human at the handoff**: every orchestration boundary keeps a decision point.
- **Generative advisors stay advisory**: prompt/plan emitters never self-execute.
- **Sibling cluster**: this cluster owns eval-first *discipline*; for the eval harness / agent
  benchmarking *tooling* itself → `quality-eval` cluster (`agent-eval`, `eval-harness`,
  `verification-loop`, `benchmark`, `production-audit`).
- This cluster is the **meta** layer — for a concrete domain agent (scraping, trading, a product
  feature), build it *with* these patterns rather than reaching for a one-off domain skill.
