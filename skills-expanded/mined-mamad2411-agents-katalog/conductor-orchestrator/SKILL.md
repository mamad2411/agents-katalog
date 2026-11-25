---
name: conductor-orchestrator
description: "Run a spec-driven build through the closed conductor loop — shape → plan → execute → verify → improve → review → ship — dispatching each task to the right skill-cluster and closing the feedback loop. USE WHEN executing a spec-kit feature/tasks.md, orchestrating multi-step build work that needs review + verification, or running the conducty loop. Pairs with conductor-core (the integration contract)."
cluster: conductor
version: 1.0.0
origin: "skill-clusters (original) — integrates conducty (MIT), spec-kit, PAI"
---

# Conductor Orchestrator

The single entry for **closed-loop, spec-driven build work**. It runs conducty's conductor cycle,
but with the one organ conducty lacks: each task is dispatched to the **right skill-cluster** via
the resolver, and deferred clusters are activated on demand. Read `conductor-core` for the full
integration contract; this routes the loop.

## The loop (conducty cycle) → spokes

| Phase | Spoke | What |
|---|---|---|
| **Shape** | `conducty-shape` | appetite, no-go zones — fed by the spec-kit `spec.md` (the *what/why*). |
| **Plan** | `conducty-plan` | acceptance criteria, verification, reviewLevel — fed by `plan.md` (the *how/stack*). |
| **Trace** | `conducty-execute` (tracer) | run ONE tracer task per group alone; fail → revise the plan, not the prompt. |
| **Execute** | `conducty-execute` + **resolver** | dispatch each `tasks.md` task to its cluster (see below). |
| **Verify** | `conducty-verify`, `conducty-checkpoint` | Iron Law: no advancement without independent evidence per task. |
| **Debug** | `conducty-debug` | classify failure **plan > prompt > code**; 3 strikes on one task → STOP/escalate. |
| **Improve** | `conducty-improve` | Toyota-Kata; append to **Failure Patterns** → next Plan reads it. |
| **Review/Ship** | `conducty-code-review`, `conducty-ship` | 5-lens review + ship battery. conducty's battery is *advisory*; run `scripts/ship-battery.mjs` to make it **fail-closed** — non-zero exit on any required gate (structural/secrets/lint/typecheck/tests) → do not ship, escalate. |
| State | `conducty-obsidian`, `conducty-vault-graph`, `conducty-bootstrap` | durable loop memory in the vault. |

## Execute — the integration (THIS is the new organ)

conducty's Execute dispatches to `general-purpose`. Instead, **resolve each task to a cluster** and
load that cluster's orchestrator into the subagent:

1. **Resolve the dispatch plan:**
   `node ~/.agents/skill-clusters/scripts/resolve-task.mjs <tasks.md> <plan.md> --json`
   → per task: `{cluster, dispatch: <cluster>-orchestrator, tier, activate?, spokes[], confidence}`.
2. **Classifier proposes, resolver validates** (the chosen triage): for each task, propose the
   cluster/skill from the task intent, then trust the resolver's validation — it rejects phantom
   clusters (only real ones in `skill-index.json`), flags **low-confidence/unresolved → escalate to human**,
   and marks **deferred clusters to activate**.
3. **Activate deferred clusters** the wave touches: `node ~/.agents/skill-clusters/scripts/tier.mjs --activate <cluster> --apply`.
4. **Dispatch** a `conducty-execute` subagent whose loaded skill is the resolved `<cluster>-orchestrator`
   (the hub then routes to the spoke on demand). Respect `[P]` for parallel waves; tracer-first per group.
5. **Taste — the right brain** (`je-ne-sais-quoi`). For **visual/frontend** clusters (creative-frontend ·
   astro · react-native · expo · design · electron · tauri UI), consult the taste engine *before* the
   subagent builds:
   `node ~/.agents/skill-clusters/taste/scripts/taste-resolve.mjs "<task>" --brand <brand> --json`
   → inject the returned **taste brief** (aesthetic classification · top-K on-brand Codrops exemplars +
   code links · conformance directive · steerable axes) into the subagent's context. The left brain picks
   the *technique*; the right brain says how it should *feel*, on-brand. Skip for non-visual clusters.
6. **Gate** via PAI hooks (`SkillClusterResolver` denies non-enumerated skills; fail-closed `exit(2)` gates;
   commit-on-criterion). The orchestrator never writes the verdict — it synthesizes the subagents' status.
   After ship, **record the cycle** for taste learning: `node taste/scripts/taste-feedback.mjs --record …`.

## Delivery modality — local subagents vs GitHub multi-agent

Before Execute, pick the modality (see `conductor-core` §4). Propose it from the work shape; let the
resolver validate it (work-shape signals + orchestrator availability):

```bash
node ~/.agents/skill-clusters/scripts/resolve-task.mjs <tasks.md> <plan.md> --modality github-delivery --json
```

- **local** (default) — Execute as above: `conducty-execute` dispatches subagents loaded with the
  resolved `<cluster>-orchestrator`.
- **github-delivery** — work is issue-tracked / multi-agent / Copilot-dispatchable / team-scale. Hand
  the loop to the user's two orchestrators (kept in place; full trees in their **source repos**):
  1. **Plan → `swarm-architect`** — decompose into phase→wave→swarm (~80 schema'd tasks), freeze
     contracts, map tasks to GitHub issues, mark `copilot_eligible`. *(Source: `thoughtseed/swarm-architect-skill/` — its runbooks/playbooks/schemas live there, not in the trimmed spoke copy.)*
  2. **Execute → `github-next-wave-orchestrator`** — repo reality scan → ranked next wave → dispatch
     each task to its lane: `human` or autonomous `copilot-swe-agent[bot]` (via the `agent-ready`
     label). `resolve-task` still resolves each task's **cluster**, so every worker — human or bot —
     carries the right capability loadout; the resolver also emits the per-task lane hint (👤/🤖).
  3. **Gate → `ship-battery.mjs`** (fail-closed) wraps swarm verification-gates + the next-wave review
     checkpoint. Never auto-merge a Copilot PR; a second reviewer (not the issue author) approves.
  4. **Close → `loop-feedback.mjs`** records the cycle (now with modality + the human/copilot lane
     split) alongside swarm OpenViking memory capture.

The conductor proposes the modality; `resolve-task` validates (real orchestrators? signals agree?); a
phantom or low-signal mismatch → escalate to the human, exactly like the cluster-name audit.

## Standard flow

spec-kit `/specify → /plan → /tasks` → **conductor-orchestrator**: shape→plan from the spec →
trace → (resolve) execute per cluster → verify/checkpoint → debug (leverage points) → improve
(Failure Patterns) → code-review → ship → **close**: write outcomes to the vault graph so the next
cycle is sharper.

## Guardrails

See `conductor-core`. In short: tracer before multiplying; independent verification per task (no
self-attested "done"); leverage-point debug (fix at plan level, not code, when 2+ tasks fail);
3-strike circuit breaker; never auto-merge (ship is advisory until PAI gates pass); resolve to
**real** clusters only (phantom-proof); escalate low-confidence tasks to a human.

## Loading spokes on demand

This cluster's spokes (the `conducty-*` loop skills) are not separately enumerated — only this
orchestrator and `conductor-core` are. Load a spoke on demand from
`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`.
