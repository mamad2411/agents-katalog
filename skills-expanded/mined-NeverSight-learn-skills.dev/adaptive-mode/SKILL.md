---
name: adaptive-mode
description: Explicit-only Adaptive Mode for mixed coding, game, design, planning, research, writing, data, automation, and prompt/skill work. The current host routes by dominant risk, loads only required playbooks, executes directly, observes real evidence, and verifies the outcome.
argument-hint: "[quick|standard|deep|continue|status|cancel] [task]"
disable-model-invocation: true
hooks:
  Stop:
    - hooks:
        - type: agent
          prompt: |
            You are the independent Adaptive Mode release verifier. Inspect current reality, not the host summary. Read `.adaptive/state.json` if present and inspect feasible artifact, repository, tests, runtime, captures, sources, or calculations. Hook JSON: $ARGUMENTS

            Lifecycle: CANCELLED -> {"ok": true}. Do not block solely for non-empty background_tasks or session_crons. When stop_hook_active is true, block only for a concrete immediately actionable P0/P1; otherwise allow stopping to avoid a non-resolving loop. No state is acceptable for narrow QUICK or conversational work. Respect action_mode: REVIEW_ONLY, PLAN_ONLY, RESEARCH_ONLY, and EXPLAIN do not require target edits.

            Return {"ok": false, "reason": "..."} only for at most 1-3 useful gaps: mandatory FAIL, feasible mandatory UNVERIFIED, actionable P0/P1, stale evidence after a relevant change, or unsupported completion. Return {"ok": true} when mandatory criteria are evidenced, no actionable P0/P1 remains, latest meaningful changes were re-observed, and remaining work is optional polish or a genuine recorded blocker. Never demand literal perfection, taste changes, speculative optimization, or impossible equality with an aspirational reference.
          timeout: 120
          continueOnBlock: true
license: MIT
compatibility: Claude Code v2.1.218+ and Codex. Manual invocation only. Claude Code may use the optional agent Stop hook; Codex uses agents/openai.yaml for explicit-only invocation and relies on the in-task release challenge.
metadata:
  version: "2.0.0"
  mode: adaptive-execution
---

# Adaptive Mode

The **current host agent** is the execution owner. The user's request accompanying this invocation is the active task.

Adaptive Mode is not a detached planner and not a prompt generator by default. Unless the requested artifact is itself a prompt, agent instruction, workflow, or skill, perform the task directly with the tools and permissions actually available.

## Invocation

Interpret the invocation as one of:

```text
<task>                    START with automatic depth routing
quick <task>              START with QUICK depth preference
standard <task>           START with STANDARD depth preference
deep <task>               START with DEEP depth preference
continue [focus]          run one fresh improvement pass over the current run
status                    inspect current state and evidence without changing the artifact
cancel                    mark the run cancelled and stop enforcement
```

Depth prefixes are preferences, not permission to skip safety, mandatory evidence, or explicit constraints. If the requested depth is badly mismatched to the actual risk, preserve the user's intent while applying the minimum safeguards needed for correctness.

For Claude Code, the typical form is `/adaptive-mode <task>`. For Codex, use `$adaptive-mode <task>`.

## 1. Non-negotiable invariants

1. **Outcome over wording.** Convert rough language into the intended end state without turning assumptions into requirements.
2. **Inspect before prescribing.** Read the real project, artifact, references, instructions, and current output before choosing architecture or edits when inspection is possible.
3. **Evidence over claims.** Code existence, a written file, a passing typecheck, or an agent summary is not proof unless it demonstrates the requested outcome.
4. **Implemented is not verified.** Re-observe every materially changed behavior or artifact.
5. **One coherent owner for coupled work.** Parallelize independent work; keep tightly coupled systems or arguments under one owner.
6. **Fresh review where independence matters.** A reviewer should see the goal, artifact, and evidence, not the builder's self-praise or hidden rationale.
7. **Preserve the Goal Ledger.** Later additions are deltas unless the user explicitly replaces the core direction.
8. **Quality bar is not a fake binary promise.** Separate aspirational comparison targets from mandatory release gates.
9. **Capability honesty.** Never claim to have run, viewed, searched, tested, delegated, or measured something the current host could not actually do.
10. **Process is proportional.** Do not turn a small reversible task into a ceremonial multi-agent project, and do not treat a high-risk compound task as a one-pass edit.

## 2. START: build the execution brief

Before substantial work, derive a compact execution brief:

```text
Outcome             one-sentence desired end state
Action mode          EXECUTE | CREATE | REVIEW_ONLY | PLAN_ONLY | RESEARCH_ONLY | EXPLAIN
Artifacts           what must be changed or produced
Mandatory criteria  observable must-pass conditions
Quality bar         what distinguishes merely working from requested quality
Constraints         safety, compatibility, scope, format, anti-goals
Freedom             decisions the host may make autonomously
Dominant risks       what can make the result appear complete while still failing
Playbooks            only the references required for this task
Depth                QUICK | STANDARD | DEEP
Evidence plan        how each important criterion will be proven
```

Keep this internal unless showing it helps the user. For STANDARD or DEEP work, record it in state when a writable workspace exists.

Respect the action mode and distinguish the **target artifact** from the **requested deliverable**:

- `EXECUTE`: modify the target only within the authorized task scope.
- `CREATE`: create the requested artifact; do not perform unrelated external actions.
- `REVIEW_ONLY`: do not modify the target artifact; an explicitly requested review report may be created.
- `PLAN_ONLY`: do not implement the plan or change the target; a plan artifact may be created.
- `RESEARCH_ONLY`: gather and synthesize evidence without changing the target; a research artifact may be created.
- `EXPLAIN`: explain from available evidence without changing the target unless the user separately authorizes a change.

Never deploy, publish, send, merge, delete, purchase, rotate credentials, or mutate an external/production system merely because it would finish the task. Consequential actions require explicit authorization and available permissions.

## 3. Route by dominant risk, not one category

A task may activate multiple playbooks. Choose the smallest useful set, normally one or two and at most three unless the task is genuinely compound.

| Dominant work or risk | Required reference |
|---|---|
| code, refactor, migration, debugging, automation, technical data processing | [ENGINEERING.md](references/ENGINEERING.md) |
| visual design, UI/UX, interaction, games, animation, reference fidelity | [CREATIVE.md](references/CREATIVE.md) |
| product planning, strategy, prioritization, architecture choice, roadmap, ambiguous decision | [DECISION.md](references/DECISION.md) |
| research, analysis, reports, documentation, writing, quantitative interpretation | [KNOWLEDGE.md](references/KNOWLEDGE.md) |
| prompts, agents, reusable skills, evaluator prompts, orchestration instructions | [PROMPT-DESIGN.md](references/PROMPT-DESIGN.md) |

**Mandatory routing rule:** after classifying the task and before substantial execution, read every selected playbook. Do not read all playbooks "just in case."

For STANDARD and DEEP work, also read [REVIEW.md](references/REVIEW.md) before the first independent review. Read [EVIDENCE.md](references/EVIDENCE.md) for DEEP work or whenever reproducibility, captures, benchmarks, sources, or measurement freshness matter. Read [STATE-AND-CONTINUATION.md](references/STATE-AND-CONTINUATION.md) when using `continue`, durable state, or recovering after compaction. Read [HOST-ADAPTERS.md](references/HOST-ADAPTERS.md) only when native host features matter. If the user explicitly combines Adaptive Mode with Agent Relay, read [AGENT-RELAY-INTEGRATION.md](references/AGENT-RELAY-INTEGRATION.md); Adaptive Mode must not invoke Agent Relay automatically.

Typical combinations:

```text
small bug                         ENGINEERING / QUICK
large migration                   ENGINEERING + REVIEW / DEEP
UI implementation from reference  CREATIVE + ENGINEERING + REVIEW / STANDARD or DEEP
new high-quality game             CREATIVE + ENGINEERING + REVIEW / DEEP
product strategy                  DECISION + REVIEW / STANDARD or DEEP
decision-ready market report      KNOWLEDGE + DECISION + REVIEW / DEEP
agent or skill design             PROMPT-DESIGN + relevant domain playbook + REVIEW
```

## 4. Select execution depth

### QUICK

Use when the task is narrow, reversible, low-risk, and objectively verifiable. An explicit `quick` prefix prefers this depth, but cannot waive essential correctness or safety checks.

- no persistent state by default;
- no subagent swarm;
- inspect enough to avoid mistakes;
- make the change or produce the artifact;
- run the smallest meaningful check;
- finish.

### STANDARD

Default for meaningful features, multi-step artifacts, moderate redesigns, analysis, or planning. An explicit `standard` prefix prevents unnecessary DEEP ceremony unless evidence reveals material hidden risk.

- normalize outcome and criteria;
- inspect current reality;
- execute coherently;
- obtain artifact-appropriate evidence;
- run one focused fresh review when useful;
- fix the highest-impact gaps;
- re-observe.

### DEEP

Use when failure can hide behind apparent completion. An explicit `deep` prefix requests the strongest relevant process, not an unbounded loop. Typical cases include:

- games and high-polish visual/interactive work;
- major migrations, architecture, multi-system changes, or regression-sensitive work;
- high-stakes or decision-critical planning/research;
- long-form artifacts whose argument, evidence, or structure matters;
- open-ended prompt/agent systems;
- work historically prone to premature stopping.

DEEP requires:

- an explicit Goal Ledger and evidence plan;
- persistent state when the workspace permits it;
- coupling-aware ownership;
- actual artifact observation;
- fresh specialist criticism;
- multiple immediate observe-review-improve rounds while P0/P1 or mandatory failures remain;
- a release challenge before completion.

Do not downgrade DEEP merely to save tokens. Remove irrelevant review instead.

## 5. Goal Ledger, state, and user deltas

Use:

```text
G1      initial locked target
G1.1    additive user delta
G1.2    another additive delta
G2      explicit replacement of core direction
```

Treat “also add,” “and fix,” “while doing that,” new screenshots, and newly reported bugs as additive by default. Preserve all unfinished earlier criteria. If a delta conflicts, preserve unaffected requirements and ask only when the conflict requires an irreversible product decision.

For DEEP work in a writable workspace, create or update `.adaptive/state.json` from [state-template.json](assets/state-template.json). Use it for STANDARD work when continuation, compaction, or multiple passes are likely. Record a stable `run_id`, a short `task_fingerprint`, and the `action_mode`. On a materially different START, archive the previous state under `.adaptive/history/` when practical rather than accidentally continuing the wrong goal. On `continue`, confirm the fingerprint against the current artifact and conversation before resuming.

State is a compact ledger, not truth. The current repository, artifact, runtime, sources, and measurements outrank stale state. Do not create state files for trivial tasks or pure conversational answers when they add no value.

## 6. Execution kernel

Use this kernel in a form appropriate to the artifact:

```text
INSPECT
→ FRAME
→ EXECUTE
→ OBSERVE
→ REVIEW
→ CONSOLIDATE
→ IMPROVE
→ RE-OBSERVE
→ RELEASE CHALLENGE
```

### INSPECT

Read current instructions, relevant files/material, working tree, architecture, constraints, references, tests, and actual output. Reuse existing verification harnesses before inventing new ones.

### FRAME

Lock the execution brief. Identify coupled work, safe autonomy, dominant risks, and evidence needed. Do not over-plan a QUICK task.

### EXECUTE

Produce the requested result. Prefer existing systems and conventions over parallel replacements unless replacement is justified. Do not expand scope simply because more work is possible.

### OBSERVE

Run, render, play, query, calculate, or read the actual artifact. Source inspection alone is insufficient when the request concerns runtime, visual quality, interaction, or user experience.

### REVIEW

Use a fresh subagent/context when available and valuable. Select critics based on the artifact, not a fixed panel. Ask for evidence-backed gaps that affect mandatory criteria or the requested quality bar, not stylistic nitpicks.

### CONSOLIDATE

Deduplicate findings by root cause. Classify:

```text
P0 Critical  core outcome impossible, destructive or severe correctness/safety failure
P1 High      major requirement, regression, experience, evidence, or decision-quality gap
P2 Medium    meaningful improvement that normally does not block release
P3 Optional  preference, alternate approach, speculative optimization, minor polish
```

Choose the highest-impact one to three gaps for the next change set.

### IMPROVE AND RE-OBSERVE

Address underlying problems rather than critic wording. Re-run only the evidence affected by the change plus necessary regressions. Invalidate stale PASS results when a relevant subsystem changed.

Do not thrash. If the same approach fails twice, evidence does not improve across two rounds, or fixes oscillate, stop repeating parameter tweaks: re-inspect assumptions, change the harness, simplify the scope, or choose a different root-cause strategy and record why.

### RELEASE CHALLENGE

Before COMPLETE, challenge the result against the Goal Ledger using current evidence. For DEEP work, use fresh independent review when available.

## 7. Orchestration rules

Use subagents to isolate noisy or independent work such as repository exploration, source gathering, test/log analysis, competing plans, and criticism. Return distilled findings to the main thread instead of raw noise. Use continuity for implementation/debugging and fresh contexts for adversarial or final review.

Parallelize write work only when ownership is explicit, coupling is low, outputs are independently testable, and integration boundaries already exist.

Keep coherent ownership for examples such as:

- movement + camera + collision;
- lighting + materials + exposure/tonemapping;
- shared state + navigation + synchronization;
- schema + transactions + business invariants;
- one core argument or tightly linked strategy;
- one prompt's authority, state, and completion semantics.

Do not create agents for ceremony. A strong single-agent pass is better than redundant workers with overlapping prompts.

## 8. Evidence minimums

Match proof to the requested artifact:

| Artifact | Minimum meaningful evidence |
|---|---|
| code/system | relevant tests/build/typecheck, runtime or contract behavior, diff/regression inspection |
| visual/UI | real render at meaningful states/viewports, interaction checks, comparison to references when provided |
| game | actual play of the core loop, controls, feedback, collisions/scale/camera, success/fail/restart, active performance when relevant |
| plan/decision | assumptions, materially different options, decision criteria, feasibility, dependencies, risks, sequencing |
| research/report | authoritative sources, contradiction and recency checks, fact/inference separation, coverage of load-bearing claims |
| writing/document | requested-section coverage, coherence, audience/format, factual consistency, constraint compliance |
| data/quantitative | source/definitions/units/formulas, sanity checks, edge cases, reproducibility and sensitivity when relevant |
| prompt/skill | target-host fit, authority, execution-vs-description behavior, observable success, delta/continuation handling, adversarial simulation |

If direct verification is unavailable, mark the criterion UNVERIFIED or BLOCKED and state exactly what would prove it. Never silently downgrade it to PASS.

## 9. Completion gate

A run is `COMPLETE` only when:

- every feasible mandatory criterion has current evidence PASS;
- no actionable P0/P1 gap remains;
- the artifact was re-observed after the latest meaningful change;
- relevant independent review challenged completion for STANDARD/DEEP work;
- remaining items are optional P2/P3 polish or genuine external blockers.

Use `ACTIVE` when meaningful high-impact work remains. Use `BLOCKED` only for a concrete external blocker. Use `CANCELLED` only after explicit cancel.

Do not block forever for taste, speculative optimization, an alternative architecture that is not materially better, or impossible literal equality with an aspirational reference.

## 10. CONTINUE, STATUS, and CANCEL

### continue

Recover the latest Goal Ledger and current artifact. Do not restart. Treat any trailing text as a focus for this pass, not a replacement of G1. Reclassify criteria from current evidence, use fresh review on the highest-risk areas, address the top one to three gaps, re-observe, and update state.

### status

Inspect state and current reality without modifying the target or state. Report outcome, depth, action mode, selected playbooks, criteria status, strongest evidence, stale-state discrepancies, top gaps, assumptions, and blockers. Use `continue` to repair state or resume work.

### cancel

Set state to CANCELLED if state exists. Preserve evidence and unfinished criteria. Stop implementation, review, and continuation behavior.

## 11. Host capability policy

Use only capabilities that actually exist. When host-specific behavior matters, read [HOST-ADAPTERS.md](references/HOST-ADAPTERS.md).

- Prefer native run/browser/verification tools over textual simulation.
- Prefer fresh subagents for independent review and read-heavy exploration.
- Prefer a single owner or isolated worktree for write-heavy parallelism.
- Use long-running goal/loop/workflow features only when the user requested sustained work or the task genuinely requires it.
- If a feature is unavailable, degrade to the portable kernel rather than inventing it.

## 12. Progress and final response

For long work, give concise updates only at meaningful points: important discovery, strategy change, implementation milestone, review finding that changes direction, strong verification evidence, or genuine blocker.

The final response should be proportional and evidence-based:

```text
Status       COMPLETE | ACTIVE | BLOCKED | CANCELLED
Result       what materially changed or was produced
Evidence     what was actually observed or verified
Remaining    only important unresolved items or limitations
```

Do not expose private chain-of-thought. Do not tell the user to paste another prompt into the same host unless that prompt is the requested artifact.
