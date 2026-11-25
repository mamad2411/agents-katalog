---
name: mythos-scaffold
description: Push Opus 4.x-class and smaller models toward Mythos/Fable-grade agentic behavior. Kernel of Fable-distilled patterns (decomposition, verification, next-action, context economy) plus demand-loaded skills, persistent mission files, named sub-agents, enforcement hooks, and domain modes (research, migration). Use when starting complex multi-step work, long-horizon tasks, or anything needing systematic persistence and verification. Do NOT fully load on Claude 5 models (Fable 5 / Mythos 5 / Opus 5 and later); over-scaffolding degrades them.
---

# Mythos scaffold

Agentic discipline framework anchored by working patterns distilled from Claude Fable 5
itself (2026-07-06, revised 2026-07-21). v2 adds a persistent mission file, harness-enforced
persistence (Stop/SessionStart hooks), named worker agents with explicit model routing, a
headless profile, and an eval harness that measures the scaffold instead of trusting it.

**Honest expectation:** the scaffold transfers process discipline, not capability. It makes
Opus 4.8 a disciplined Opus 4.8. See `eval/` for measured deltas.

## Model gating (check first)

| Session model | What to load |
|---|---|
| Opus 4.8 / Opus 4.x / Sonnet 4.x / Haiku | Kernel, then tiered (below) |
| Claude 5 family (Fable 5 / Mythos 5 / Opus 5 / Sonnet 5) and later | Nothing, or at most the kernel's verification section. State goal and constraints; do not enumerate steps. |

When in doubt (a model newer than this table): treat it as Claude 5 family — under-scaffolding costs less than over-scaffolding on capable models.

## Activation

Always load exactly one file: the kernel, [`core/fable-distilled.md`](./core/fable-distilled.md).
It carries the binding rules and the load map for every other file (mode, tool-stack,
context-priming, decomposition, agent-loop, verification, failure-recovery, memory, headless,
domains). Open others only when their load-map trigger fires.

## Mission file

Long-horizon runs externalize state to `~/.claude/mythos/missions/<slug>--<stamp>.md` with an
active-mission pointer at `~/.cache/mythos/active`. The `/mythos-mode` command owns the
lifecycle (`<task>` / `resume` / `status` / `close`); the hooks in [`hooks/`](./hooks/) read
it to block premature stops and to re-surface the mission after compaction. Schema: see the
command's mission template.

## Sub-agents

[`agents/`](./agents/) ships four workers installed into `~/.claude/agents/`: `mythos-scout`
(haiku, mechanical bulk), `mythos-builder` (sonnet, light code), `mythos-heavy` (opus, hard
code), `mythos-verifier` (sonnet, adversarial check, never edits). Every spawn names its
model explicitly.

## Domain modes

- **Research:** [`domains/research/`](./domains/research/) (retrieval tiers, claim graph,
  cite-verify, output formats)
- **Migration:** [`domains/migration/`](./domains/migration/) (audit, plan, execute, rollback)

## Integration

The scaffold routes to neighbors instead of duplicating them: see
[`INTEGRATION.md`](./INTEGRATION.md).

## When to use

- Multi-step tasks where the model might stall, drift, or miss verification
- Long-horizon research or migrations (domain modes)
- Debugging cycles where naive retry fails
- Unattended runs (cron, loops): [`core/headless.md`](./core/headless.md)

## When not to use

- Single tool call, single answer questions: overhead not worth it
- Tasks already covered by a more specific skill
- Sessions running on Claude 5 family models — Fable 5 / Mythos 5 / Opus 5 / Sonnet 5 (model gating above)

## Changelog

- **2026-07-21 (v0.3):** kernel recompiled (mode rules folded in, context economy, escalation
  protocol); mission file + pointer; Stop/SessionStart enforcement hooks; four named worker
  agents; headless profile; eval harness (T1 persistence, T2 verification) and distillation
  curation procedure; command grows `resume`/`status`/`close`; installed command becomes a
  symlink; stale references fixed; dead sync hook removed.
- **2026-07-06:** Fable-distilled patterns added; read-all-8 replaced with tiered loading;
  model gating; sub-agent model routing.
- **2026-04-27:** initial 6-skill framework plus research and migration domains.

## Source

https://github.com/kasparovabi/claude-mythos-scaffold (MIT, by kasparovabi). Inspired by
Claude Mythos Preview behaviors, not affiliated with Anthropic.
