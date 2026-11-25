---
name: fusion-swarms
description: >-
  Advanced multi-agent swarm patterns for Fusion, ported from the Swarms framework and run
  over the live CLIs (codex/copilot/opencode/grok) via a Python engine. Use when a plain
  panel/council isn't the right shape: layered refinement (MoA), deep role-specialized
  research (heavy), shared-thread brainstorm (discuss), director→workers (hierarchy), a DAG
  of stages (graph), a custom flow (flow), iterative quality-gated refine, best-of-N, or
  agent-level reasoning wrappers (reflexion / self-consistency / GKP). Triggers: "moa",
  "mixture of agents", "heavy swarm", "discuss/brainstorm with the models", "hierarchy",
  "graph workflow", "reflexion", "self-consistency", "best of N", "refine until good".
---

# Fusion — Swarm patterns (Python-orchestrated)

These are the structured swarms that need real loops, layers, DAGs, or growing state —
things bash + prose handle poorly. They run through a small **stdlib-only Python engine**
(`python/fusion_swarm/`) that shells every "agent call" out to Fusion's *verified* CLI
adapters. No `swarms` dependency, no API keys — it rides the same codex/copilot/opencode/grok
you already use, so all the injection-safety, timeout, and sandbox logic is reused.
In Codex, resolve `FUSION_PLUGIN_ROOT` from the loaded `SKILL.md` path: it is two
directories above `skills/fusion-swarms/SKILL.md`.

## MANDATORY
- The Python engine **really dispatches** the CLIs. You are PROHIBITED from simulating its
  output. Run it, read its JSON, then judge.
- You (Codex) remain the **final judge.** The engine can pre-aggregate with a CLI, but the
  best path is: run with `--json`, read the transcript + per-round outputs, and write the
  final Fusion verdict yourself. Pass `--aggregator none` to skip the CLI synthesis when you
  intend to do it all.
- **Absent ≠ agreement** still holds — a panelist with no output didn't contribute.

## How to run
```
bash "$FUSION_PLUGIN_ROOT/scripts/swarm.sh" <pattern> "<task>" [opts] --json
```
Read the JSON (`pattern`, `transcript`, optional `synthesis`/`final`, `panel`, statuses),
then synthesize the final answer in Fusion's voice + the audit trail, and record the run.

## The patterns — when to reach for each

| Pattern | Use when | Invocation |
|---------|----------|------------|
| **moa** | hard, open-ended work that benefits from *iterative* cross-pollination | `swarm.sh moa "<task>" --layers 2` |
| **heavy** | research-grade depth: decompose into Research/Analysis/Alternatives/Verification | `swarm.sh heavy "<task>" --loops 1` |
| **discuss** | brainstorm where ideas should compound across a shared thread | `swarm.sh discuss "<task>" --rounds 2` |
| **hierarchy** | a director should split *different* subtasks across workers | `swarm.sh hierarchy "<task>" --director codex` |
| **graph** | an explicit DAG of stages with fan-out/fan-in | `swarm.sh graph "<task>" --nodes "r=codex,a=copilot,m=grok" --edges "r>a,r>m,a>m"` |
| **flow** | a custom sequential/parallel pipeline over named providers | `swarm.sh flow "<task>" --flow "codex -> copilot, opencode -> grok"` |
| **refine** | you want a deterministic quality gate (generate → score → fix → repeat) | `swarm.sh refine "<task>" --generator codex --evaluator copilot --threshold 85 --rounds 3` |
| **bestof** | one model's best possible answer (sample N, fold to a champion) | `swarm.sh bestof "<task>" --provider codex --samples 5` |
| **reflexion** | harden one panelist: draft → self-critique → revise | `swarm.sh reflexion "<task>" --provider codex --iterations 2` |
| **selfconsist** | a single panelist's majority answer over N samples | `swarm.sh selfconsist "<task>" --provider grok --samples 5` |
| **gkp** | seed grounded facts first, then answer (generated-knowledge prompting) | `swarm.sh gkp "<task>" --provider copilot` |

### Coding structures (gate-backed) — the verification gate is the arbiter

For code, a *hard* gate (the test runner / typecheck / build) outranks any model vote. These
structures make that real:

| Pattern | Use when | Invocation |
|---------|----------|------------|
| **ladder** | high-volume routine work — spend the minimum, escalate only on failure | `swarm.sh ladder "<task>" [--gate-cmd "pytest -q"] [--cwd .]` |
| **speclock** | a feature that decomposes into modules with clean seams (integration is the hard part) | `swarm.sh speclock "<task>" [--gate-cmd "npx tsc --noEmit"]` |
| **breaker** | security/auth/payments/parsers — "looks right" is dangerous | `swarm.sh breaker "<task>" --builder codex --breaker grok [--gate-cmd "pytest -q"]` |
| **ballot** | "which approach" decisions, API design, refactor strategy | `swarm.sh ballot "<decision>" [--gate-cmd "..."]` |
| **gate** | run a check standalone (the hard arbiter, on demand) | `swarm.sh gate --gate-cmd "pytest -q" --cwd .` |

- **ladder** — cheapest model first; a `--gate-cmd` failure (or low `CONFIDENCE`) escalates to a
  stronger model with the failure log attached. Stops at the first tier that passes.
- **speclock** — contract (types+signatures+stubs) first → modules implemented in parallel
  against it → gate integrates. If it typechecks, the pieces fit by construction.
- **breaker** — builder writes code, an adversary writes *runnable* failing tests; with a
  `--gate-cmd` the gate judges (hard mode), else the builder hardens defensively. Keep the
  breaker's tests as free regression coverage.
- **ballot** — blind propose → anonymize → each votes for two (barred from voting for its own,
  anti-self-vote) with reasons → ties break on the gate. Group-think-proof.

**The verification gate (`gate.py`) is the key idea.** A judge model is a soft opinion; a green
test run is ground truth. Wherever a test can decide, let it — reserve model judgment for
design questions tests can't settle. SAFETY: `--gate-cmd` executes a command, so only ever
pass non-destructive verification (pytest / `tsc --noEmit` / build / lint); the conductor owns
the approval boundary and any patch *application* to the repo.

**Reusable modifiers** (`modifiers.py`) compose into any structure: `anonymize` (strip identity
before review/vote), anti-self-vote (`tally`), `parse_confidence` (a 0-1 stake), and
`decision_baton` (a structured handoff: decisions / assumptions / open questions / risks — so
reviewers can see where context was lost).

The reasoning wrappers (reflexion/selfconsist/gkp) operate on **one** provider — compose
them: run a reflexion-hardened codex as one member of a `panel`, or `gkp` as a pre-pass that
seeds facts for a `moa`.

## Mechanics (so you can judge the output honestly)
- **moa** — every panelist answers; their answers are fed back so the next layer *refines*;
  repeat `--layers` times; then synthesize. `panel` is moa with one layer.
- **heavy** — a question-generator splits the task into four specialist questions
  (Research/Analysis/Alternatives/Verification), each answered by a panelist in parallel,
  then integrated; `--loops` adds refinement passes.
- **discuss** — multi-round shared thread; each round every panelist sees the running
  transcript and adds one contribution (within a round they're blind to peers — an honest
  port, since uniform speak-or-stay tool-calling isn't available across CLIs).
- **graph** — topological waves; independent nodes run in parallel; each node sees its
  upstream outputs. Cycles are reported, not hung.
- **refine** — generator answers, evaluator scores 0-100 + concrete feedback, generator
  revises; stops at `--threshold` or `--rounds`. A real gate, not "looks good".
- **bestof** — Self-MoA-Seq: sample one provider N times, fold a few at a time carrying the
  current champion forward (bounded context, quality ratchets up).

## Cost & honesty
These run more calls than a single `panel` (layers × panelists, loops, samples). Show the
cost banner first and pick the lightest pattern that fits — `discuss`/`heavy`/`moa` are the
expensive ones; `reflexion`/`gkp` are single-provider and cheap. Record every run
(`task_type: swarm:<pattern>`) so the ledger learns which swarm wins which task.
```
✦ FUSION swarm · pattern=<p> · panel: 🔴codex 🔷copilot 🟢opencode ⬛grok · est ≈ <n> calls
```
