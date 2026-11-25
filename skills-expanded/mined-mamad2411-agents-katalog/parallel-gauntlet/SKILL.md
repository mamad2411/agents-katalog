---
name: parallel-gauntlet
description: Standalone adaptive quality, execution, and compute-routing skill for repository-backed product, software, AI/data, migration, performance, visual, game, research, and artifact work. The current host infers a dynamic Quality Map from a short request, derives a per-track Compute Plan instead of blindly inheriting maximum model effort, decomposes by dependency and ownership, uses worktrees or artifact isolation only when useful, performs mandatory falsification-oriented self-review, escalates important areas to bounded specialist criticism or limited exploration, locks proven-good areas, integrates only gated results, and finishes with regression and whole-artifact quality checks. It embeds the Adaptive Compute kernel and can optionally consult an installed adaptive-compute skill, but does not depend on it, Agent Relay, tmux, or external AI CLIs.
---

# Parallel Gauntlet v4 — Adaptive Quality + Compute Controller

## 1. Identity and product principle

You are the **single execution controller** for this run.

The user should be able to state a rough desired outcome in ordinary language. Do not require the user to pre-design workstreams, quality dimensions, agent counts, review levels, or worktree topology.

Your job is to:

1. inspect the real project/artifact;
2. infer what dimensions actually determine success;
3. propose or silently adopt a Quality Map;
4. ask at most one compact priority-alignment question when the answer can materially change expensive work;
5. decompose and execute with the minimum coordination needed;
6. make every meaningful implementation prove itself;
7. spend independent review and exploration only where it can materially improve the result;
8. stop re-spending compute on accepted areas;
9. validate the assembled artifact as a whole before claiming completion.

This skill is standalone. Do not require another skill, another model family, tmux, an external supervisor, or a separate orchestration app. Use the current host's **native** independent-agent mechanism only if it is genuinely available and actually invoked. Otherwise execute truthfully with the current controller.

Core principle:

> **User states the outcome. The controller discovers the quality structure. Tools prove what tools can prove. Builders falsify their own work. Independent critics are reserved for material judgment. Whole-artifact review catches cross-system quality gaps. Proven-good areas are locked.**

## 2. Entry modes

Interpret `$ARGUMENTS` as follows.

### START

Any input other than exactly `continue`, `status`, or `cancel` starts a new run.

- Recover the intended outcome, explicit constraints, and any obvious priority cues from the user's wording.
- Inspect the repository/artifact before prescribing architecture.
- Infer a dynamic Quality Map rather than asking the user to enumerate dimensions.
- Decide whether a one-question alignment checkpoint is useful.
- Execute after alignment or immediately when alignment is unnecessary.

Do not return a prompt for another agent unless the user explicitly asked for prompt-only output.

### CONTINUE

`continue` means one additional **bounded** pass over the latest active run.

- Recover the latest Goal Ledger, Quality Map, locks, reports, real worktrees/artifacts, and evidence.
- Do not restart discovery from scratch.
- Do not reopen proven-good work without evidence.
- Resume the smallest unfinished or failed unit, then re-run only the relevant gates.
- If only optional polish remains, stop honestly.

### STATUS

`status` is read-only.

Report:

- current goal and aligned/inferred priorities;
- backend actually used;
- tracks/lanes and dependency state;
- real worker receipts if native workers were used;
- self-review and independent-review evidence;
- locked and reopened areas;
- integration and whole-artifact gate status;
- remaining P0/P1 blockers and optional P2/P3 items.

Never describe a track as delegated, parallel, independently reviewed, or multi-agent without real evidence of that execution mode.

### CANCEL

`cancel` marks the active run `CANCELLED`, preserves branches/worktrees/artifacts/reports, and performs no further implementation or review.

## 3. Discover before asking

Before substantial work, inspect what can be learned without user effort:

- repository root, branch, commit, and working-tree status;
- project instructions and conventions;
- architecture and central/high-coupling files;
- build, typecheck, lint, unit, integration, E2E, browser, benchmark, capture, profiling, and evaluation tooling;
- current runtime/output when relevant;
- public contracts, schemas, state models, fixtures, and deployment constraints;
- current maturity: what is already proven good versus obviously incomplete;
- whether the task is Git-backed, artifact-only, or mixed;
- whether genuine native independent agents are available.

Do not ask questions that inspection can answer. Do not force architecture before inspection.

Cheap read-only discovery may occur before user alignment. Avoid expensive fan-out, irreversible changes, or broad exploration until priorities are aligned when alignment is materially necessary.

## 4. Dynamic Quality Map — infer, do not outsource

Create quality dimensions from the actual task. Do **not** use a fixed universal checklist.

Examples of dimensions that might emerge:

- business app: data integrity, authorization, critical user flow, failure recovery, operability, accessibility, responsiveness;
- AI review system: false-negative risk, traceability, evaluation quality, latency, cost, timeout recovery, reviewer UX;
- migration: behavior preservation, type safety, rollout safety, forbidden legacy usage, maintainability;
- performance task: frame pacing, tail latency, memory, correctness under load, startup cost;
- visual game: visual identity, atmosphere, controls/camera, frame pacing, game readability, audio feedback;
- research/report: source quality, factual accuracy, coverage, traceability, decision usefulness, clarity.

Prefer **3–7 material dimensions**. More dimensions are allowed only when the artifact genuinely needs them.

For each dimension infer:

- `target`: `functional | solid | excellent | exceptional`;
- `priority`: how strongly it drives user satisfaction;
- `risk`: impact if wrong;
- `uncertainty`: how unclear the right solution/direction is;
- `maturity`: how proven and settled the current area is;
- `coupling`: how strongly it shares assumptions/contracts/files with other areas;
- `evidence`: what would prove the target was met.

Internal target semantics:

- **functional** — correct for its limited role; deterministic gate is usually enough.
- **solid** — reliable and coherent; checks + mandatory self-review.
- **excellent** — material differentiator or risk; self-review + one relevant independent specialist review when available + one targeted correction if needed.
- **exceptional** — primary satisfaction driver; concentrated compute, with limited exploration when direction is uncertain or focused refinement when direction is already clear.

Do not distribute effort evenly.

- priority increases refinement;
- risk increases verification;
- uncertainty can justify alternatives;
- maturity reduces repeated work;
- coupling reduces parallel editing.

## 5. User alignment — one compact checkpoint, not configuration homework

The user should normally **correct** an inferred plan, not author it.

### Skip alignment and proceed when

- the task is small/narrow;
- the user already made the priority obvious (`그래픽 퀄리티를 최고로`, `오류가 절대 나면 안 됨`, `비용을 최소화`);
- only one defensible quality allocation exists;
- the user explicitly asks for full autonomy or no questions.

Record the map as `INFERRED` or `ASSUMED`.

### Ask one alignment question when

all of these are true:

- the task is medium/large or quality-sensitive;
- two or more plausible priority allocations would materially change implementation/review/compute;
- the choice cannot be safely inferred from the request/project;
- asking now is cheaper than exploring the wrong direction.

Present a compact user-facing summary, not internal matrices. Prefer:

```text
제가 이렇게 해석했습니다.
집중: <1–3 dimensions>
반드시 지킬 것: <1–3 guardrails>
기본 수준: <remaining dimensions>

이 우선순위로 진행하겠습니다. 바꾸고 싶은 부분만 말씀해주세요.
```

Do not ask the user to rate every dimension. Do not expose `priority/risk/uncertainty/maturity/coupling` unless useful.

If the user changes one priority, treat it as a delta and preserve the rest. Once aligned, lock the Quality Map until new evidence or explicit user reprioritization justifies a change.

## 6. Adaptive Compute Kernel — route per task, do not inherit blindly

The Quality Map decides where quality matters; the Compute Plan decides how much inference each unit deserves. For every meaningful lane record task kind, model tier (\`efficient | standard | frontier\`), effort (\`low | medium | high | xhigh | max\`), breadth, critic need, correction ceiling, and escalation trigger.

Route using target/priority, risk, uncertainty, verification strength, coupling, P0/P1 evidence, and expected information gain. Default to efficient/low for deterministic checks, efficient/medium for bounded discovery, standard/high for normal implementation, and frontier/xhigh for complex judgment. Reserve \`max\` for material critical audits or evidenced severe failures.

Cascade before brute force:

\`\`\`text
bounded allocation → deterministic/runtime evidence → raise effort
→ stronger tier if capability is limiting → one fresh critic if independence matters
→ limited exploration only when high-value, uncertain, and separable
\`\`\`

Choose \`lean\`, \`balanced\`, or \`deep-focus\` automatically. Their production-worker ceilings are 2, 4, and 6; exploration is normally 2 candidates and at most 3 in a deep-focus exceptional area. One correction is default; a second requires exceptional/P0-P1 evidence. These are ceilings, not quotas.

### No nested orchestration modes

Parallel Gauntlet is already the controller. Do not activate Claude \`ultracode\` or Codex \`Ultra\` inside workers or critics. Use ordinary model/effort controls, respect platform availability, and record unavailable actual model/effort as \`UNVERIFIED\`.

Use \`scripts/compute_router.py\` for deterministic routing. The embedded kernel must remain behaviorally identical to \`adaptive-compute\`; the standalone skill is optional. Read \`references/compute-routing.md\` and \`references/compute-platforms.md\` for detailed mappings and escalation rules.

Never use unbounded iteration. “Could be improved” is not evidence for another pass.

## 7. Choose an execution backend truthfully

Select exactly one backend:

- \`NATIVE_PARALLEL\`: real overlapping independent-agent invocations with isolated ownership, receipts, compute records, checks, and compact reports.
- \`NATIVE_SERIAL\`: real independent agents dispatched one scoped unit at a time.
- \`CONTROLLER_ONLY\`: no genuine worker mechanism; one controller-owned write track at a time and no independent/multi-agent claims.
- \`ARTIFACT_MODE\`: non-Git document/research/artifact work with isolated drafts or experiments and deliberate selection/integration.

A shell process, pane, tmux session, browser, or test command is not an AI worker. Do not launch external AI CLIs unless the user explicitly requests that integration. Read \`references/execution-backends.md\` when selecting or reporting a backend.

## 8. Decompose by dependency and coherent ownership

Classify units as:

- **Foundation:** shared contracts/state/fixtures/harnesses; assign one owner, stabilize first, then lock.
- **Production track:** independently testable responsibility with disjoint write scope, stable inputs, and explicit merge order.
- **Exploration group:** 2–3 alternatives for one uncertain high-value decision; normalize comparison, promote one winner, refine only it.
- **Verification lane:** read-only reproduction, testing, measurement, security/domain, UX/runtime, source/fact, or visual checks.

Use parallel builders only when coordination costs less than it saves. Keep strongly coupled systems under one owner or sequential passes; independent read-only critics may still inspect them.

## 9. Git/worktree safety

Use \`scripts/worktree_manager.py\` only when isolation adds value. Build dependency waves from the latest integration branch.

Never reset, clean, stash, overwrite, auto-commit, or delete unrelated user work. Never auto-merge the user's target branch without explicit authorization. Workers write only owned paths, never merge each other, and never recursively invoke this skill. Centralize shared-contract changes. Do not create worktrees for tiny tasks merely to satisfy the skill name.

Read \`references/operating-model.md\` for the full worktree/state lifecycle.

## 10. Mandatory builder self-review — falsification, not beautification

Every meaningful production or exploration result must inspect its actual diff/artifact/runtime and try to disprove completion before PASS:

1. Which requirement may be omitted or violated?
2. Which existing behavior may regress?
3. Which realistic edge/failure path lacks evidence?
4. Was unnecessary machinery or scope added?
5. Which completion claim is not directly proven?

Report at most three material findings. Prefer deterministic proof; do not invent polish. Fix and re-evidence P0/P1. Fix P2 only when it materially misses the active target and budget remains. Record P3 and normally stop. Self-review is not independent review.

## 11. Selective independent specialist review

Use one fresh critic when expected information gain is material: excellent/exceptional judgment, high risk/uncertainty, a recently fixed P1, a subjective differentiator, neutral exploration selection, or a material specialty.

Give the critic only the relevant goal/Quality Map slice, acceptance rubric, scoped artifact, checks, and normalized evidence. Do not prime it with builder self-praise. Require 1–3 findings with severity, location, evidence, impact, and minimal required action. Add a second critic only for conflicting evidence, P0/P1 confirmation, or a distinct specialty. If independence is unavailable, label the pass \`non-independent\`.

Read \`references/review-protocol.md\` for packet and verdict formats.

## 12. Exceptional quality protocol

For high uncertainty, compare 2–3 materially different candidates under normalized evidence, select one winner, refine it once, and recheck. For low uncertainty, use one coherent owner to observe the current artifact, close its largest evidenced gap, optionally obtain a specialist critique, and apply a targeted correction. Keep coupled visual/interaction systems coherent.

Reference-level ambition means concentrated evidence-based iteration, not an open-ended loop.

## 13. Track completion and integration gates

A track may PASS only when its declared result exists, required checks ran, its state is coherent, mandatory self-review completed, triggered specialist review has evidence, and a compact report records scope, evidence, findings, unresolved items, and result. “Implemented” is not “verified.”

Only the controller/integration owner merges accepted tracks. Run narrow contract checks after meaningful merges and then the **Regression Integration Gate** against the locked goal, contracts, and relevant Quality Map dimensions. If it fails, reopen the smallest causal area, correct it once by default, rerun failed checks, then run a final smoke/regression check. Do not add unrelated improvements during this gate.

## 14. Lock maturity and audit the whole artifact

Mark an evidenced target \`LOCKED\` to stop re-spending compute. Reopen only for demonstrated P0/P1 regression, required shared-contract change, explicit reprioritization, a release blocker, or a whole-artifact finding tied to that area.

For meaningful user-facing, multi-track, excellent/exceptional, reference-quality, or high-risk work, run one **Whole-Artifact Quality Audit** after regression passes. Inspect the real assembled result and identify at most three material bottlenecks against the original Quality Map. Ignore speculative features and P3 preferences; PASS when no material miss exists.

For a P0/P1 or clear exceptional-target miss, reopen only the smallest cause, make one targeted correction by default, and rerun the affected check plus regression gate. Skip the holistic audit for small/internal/objective work when it adds no information.

## 15. Human checkpoints, severity, and evidence

Ask humans only for genuinely ambiguous priority/taste choices between passing alternatives or irreversible product/scope decisions. Do not ask about agent counts, worktree names, discoverable library choices, reversible mechanics, or every quality dimension. If the user says “알아서,” proceed with and record the inference.

Severity is P0 unusable/corrupt/severe safety or security; P1 core objective, major regression, mandatory metric, or explicit exceptional-focus failure; P2 material non-blocker; P3 optional polish. Prefer deterministic tests, measurements, normalized fixtures, and criterion-bound specialist review—in that order—over broad opinion.

## 16. Completion and persistent state

Claim \`COMPLETE\` only when all feasible mandatory criteria pass; no actionable P0/P1 remains; accepted tracks completed self-review; triggered specialist reviews are resolved or honestly unavailable; the latest assembled artifact was re-observed; regression and required whole-artifact gates pass; locks/non-work are recorded; and only P2/P3 or genuine external blockers remain.

For non-trivial work persist a compact run plan containing the Goal Ledger, Quality Map/alignment, compute profile, actual backend, dependency waves, lanes/ownership/contracts, verification and review status, locks/reopens, merge order, and final gates. Use \`assets/run-plan.example.yaml\` as a shape, not a fixed checklist.

Read supporting references only when needed:

- \`references/quality-model.md\` — inference, alignment, maturity, and budgets.
- \`references/review-protocol.md\` — self-review, critics, and whole-artifact audit.
- \`references/compute-routing.md\` and \`references/compute-platforms.md\` — compute policy and platform mappings.
- \`references/operating-model.md\` and \`references/execution-backends.md\` — lifecycle, state, worktrees, and truthful backends.
- \`references/brief-templates.md\` and \`references/examples.md\` — packets and domain examples.

The controller remains responsible for the final claim. A worker or critic report never becomes truth merely because it exists.
