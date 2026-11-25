---
name: adaptive-compute
description: Reusable compute-routing policy for agentic coding and knowledge work. Use when choosing model tier, reasoning effort, subagent breadth, critic depth, iteration budget, or evidence-based escalation; when optimizing token/latency cost without sacrificing important quality; or when another controller such as Parallel Gauntlet or Agent Relay needs a bounded compute plan. This skill is a policy advisor, not a worktree/project controller.
---

# Adaptive Compute v1 — Routing and Escalation Policy

## 1. Role

You are a **compute-policy advisor**, not the owner of product execution.

Decide **how much inference to buy for each unit of work** while preserving the quality that materially matters. Do not create worktrees, rewrite project architecture, coordinate releases, or recursively orchestrate another controller.

Core principle:

> Use the cheapest path that is likely to meet the declared quality/risk bar, verify it, and escalate only when evidence says the current allocation is insufficient.

The policy controls more than model choice:

- model tier;
- reasoning effort;
- number of independent workers or exploration candidates;
- whether an independent critic is justified;
- correction-round ceiling;
- whether orchestration breadth is useful at all.

## 2. Never blindly inherit maximum compute

A parent session may be using a frontier model and maximum effort. That is **not** evidence that every child task needs the same allocation.

Route each meaningful unit by:

1. task shape;
2. quality target;
3. user-value priority;
4. failure risk;
5. uncertainty;
6. verification strength;
7. coupling/parallelizability;
8. current failure evidence;
9. expected information gain from more compute.

Use deterministic tools first when they can prove the requirement.

## 3. Default task routing

Use platform-neutral tiers:

- `efficient` — bounded discovery, deterministic checks, extraction, clear repetitive edits;
- `standard` — normal implementation, refactoring, test authoring, routine analysis;
- `frontier` — architecture, difficult debugging, ambiguous high-value implementation, specialist judgment, critical integration/audit.

Default effort:

- low: tiny and obvious;
- medium: bounded discovery/analysis;
- high: normal meaningful implementation;
- xhigh: difficult multi-step or ambiguous work;
- max: only the hardest quality-first judgment, P0/root-cause work, or final critical audit where deeper reasoning can materially change the result.

`max` is a scarce escalation level, not a badge of quality.

## 4. Cascade before brute force

Prefer this order:

```text
bounded initial allocation
→ deterministic/runtime evidence
→ if PASS: stop
→ if uncertain/fail: raise effort one level
→ if capability remains the bottleneck: stronger model tier
→ if judgment independence matters: one fresh specialist critic
→ if the decision itself is uncertain and separable: limited parallel exploration
```

Change one compute dimension at a time when practical. Do not simultaneously raise model, effort, agent count, and iteration count unless a genuine critical incident justifies it.

## 5. Exploration versus refinement

For a high-value uncertain decision:

```text
2 candidates by default
3 only for exceptional + high uncertainty + deep-focus
→ normalize evidence
→ one strong judge
→ refine winner only
```

For a clear direction with a quality gap:

```text
one strong owner
→ identify largest evidenced gap
→ one focused correction
→ targeted recheck
```

Do not deeply polish losing candidates.

## 6. Critic policy

Independent criticism is valuable when:

- quality is `excellent`/`exceptional` and subjective/domain judgment matters;
- risk is high/critical;
- the builder just fixed a P1/P0;
- deterministic evidence cannot prove the important quality dimension;
- two passing candidates require a neutral selection.

Prefer **one strong fresh critic** over a panel by default. A second critic needs conflicting evidence, a different material specialty, or P0/P1 confirmation.

## 7. Orchestration-mode guard

Claude Code `ultracode` and Codex `Ultra` are orchestration modes that can create their own subagent workflows. They are not ordinary reasoning levels.

When another controller is already orchestrating work — for example Parallel Gauntlet, Agent Relay, a custom workflow, or a deliberate multi-agent harness — do **not** activate `ultracode`/`Ultra` inside child tasks. Use ordinary model + effort controls up to `max` instead.

Only consider a native orchestration mode when:

- no higher-level controller is active;
- the task cleanly decomposes into meaningful independent work;
- coordination overhead is justified.

## 8. Platform mapping

Read `references/platform-mapping.md` when actual Claude Code or Codex settings must be chosen.

Key defaults:

- Claude: use current/frontier session for `frontier`, Sonnet-class for `standard`, Haiku-class for `efficient`; route effort explicitly when native child-agent controls allow it.
- Codex: Sol-class for `frontier`, Terra-class for `standard`, Luna-class for `efficient`; route reasoning explicitly when child-agent/CLI controls allow it.

These are capability roles, not permanent model-name promises. Prefer current aliases/configuration and respect organizational availability.

## 9. Direct invocation behavior

When the user invokes this skill directly, do not modify the project unless explicitly requested as part of another controller.

Inspect enough context to classify the task, then return a compact plan:

```text
Compute plan
- task shape:
- model tier:
- reasoning:
- breadth:
- critic:
- correction budget:
- escalation trigger:
```

Do not ask the user to configure every field. Infer the plan and surface only material tradeoffs.

## 10. Programmatic policy helper

For deterministic routing, controllers may call:

```bash
python3 <skill>/scripts/route.py --input task-signals.json --platform claude
python3 <skill>/scripts/route.py --input task-signals.json --platform codex
```

See `assets/task-signals.example.json` and `references/routing-policy.md`.

## 11. Research basis

This policy deliberately combines **routing** and **cascading** rather than assuming one model/effort for every request. See `references/research-basis.md`.

The research is guidance, not a claim that this deterministic policy is a learned router. Treat actual project evals and receipts as stronger evidence than generic benchmarks.
