---
name: gauntlet-mode
description: Execute an explicitly requested task in high-reliability Gauntlet mode. Use when the user invokes /gauntlet-mode with a task, when resuming with "continue", when cancelling with "cancel", or when /loop invokes "/gauntlet-mode continue". This is an execution mode, not a prompt generator.
argument-hint: [task | continue | cancel]
hooks:
  Stop:
    - hooks:
        - type: agent
          prompt: |
            You are the independent GAUNTLET RELEASE VERIFIER for the active gauntlet-mode run.

            Inspect the actual project and available evidence rather than trusting the builder's summary.

            Read `.claude/gauntlet-state.md` if it exists.

            If status is CANCELLED, return {"ok": true} immediately.

            Return {"ok": true} only when:
            1. mandatory criteria that are feasible in this environment are evidenced PASS, or genuine external blockers are explicitly recorded;
            2. no P0/P1 actionable gap remains against the user's requested quality bar;
            3. the artifact was re-observed after the latest meaningful change;
            4. no important criterion is merely claimed complete without evidence;
            5. remaining items are P2/P3 optional polish, alternate-preference suggestions, or genuine external blockers.

            Return {"ok": false, "reason": "..."} only when more useful work should be done now. Name at most the 1-3 highest-impact concrete gaps and the evidence/action needed next.

            You MUST NOT block solely for:
            - P2/P3 polish
            - stylistic preference
            - speculative optimization
            - alternative architecture preference
            - impossible literal equality with an aspirational reference
            - already-recorded external blockers

            You SHOULD block for:
            - mandatory FAIL
            - feasible mandatory UNVERIFIED
            - P0/P1 correctness/regression/UX/visual/gameplay/security/integration defects
            - claimed completion without adequate evidence
            - failure to re-observe after the latest meaningful change

            Hook context:
            $ARGUMENTS
          timeout: 120
---

# Gauntlet Mode

You are an **execution orchestrator**, not a prompt generator.

When invoked, directly work in the current repository/project using an evidence-driven Gauntlet process.

Do not answer with "here is a prompt to paste" unless the user explicitly asks for prompt-only output.

Read [reference/CORE.md](reference/CORE.md) for controller semantics and [reference/REVIEW-PROTOCOL.md](reference/REVIEW-PROTOCOL.md) for critic/evidence details when needed.

Use `$ARGUMENTS` to choose the entry mode.

Supported entry forms:

```text
/gauntlet-mode <task>       # START
/gauntlet-mode continue     # one more fresh quality pass
/gauntlet-mode cancel       # stop Gauntlet mode cleanly
```

# 1. Entry modes

## START

START when `$ARGUMENTS` is not exactly `continue` or `cancel`.

1. Normalize the rough request into Goal Ledger `G1`.
2. Inspect repo/project instructions and current artifact before prescribing architecture.
3. Select Gauntlet depth: LIGHT / STANDARD / DEEP.
4. Establish mandatory criteria, quality bar, evidence plan, and implementation freedom.
5. Detect task shape and choose coherent workstreams.
6. Implement.
7. Observe the real artifact.
8. Run fresh independent critics where useful.
9. Consolidate findings by root cause.
10. Fix the highest-impact 1–3 gaps.
11. Re-observe.
12. Repeat useful immediate iterations.
13. Update `.claude/gauntlet-state.md`.
14. Attempt to finish.
15. Let the independent Stop verifier challenge completion.
16. If blocked, address its concrete gaps and verify again.

Do not ask the user to re-enter generated instructions.

## CONTINUE

CONTINUE only when `$ARGUMENTS` is exactly:

```text
continue
```

Meaning:

> Run one more serious Gauntlet pass from the CURRENT state.

Do NOT:
- create a new Goal Ledger from scratch;
- reinterpret the project as a new task;
- restart planning without evidence the plan is invalid;
- redo proven-good work without regression evidence;
- discard earlier unfinished criteria;
- create or schedule `/loop`;
- recursively invoke gauntlet-mode.

Instead:
1. Recover latest Goal Ledger from state/conversation/repo.
2. Inspect current repo and working tree.
3. Re-observe the actual artifact.
4. Reclassify important criteria as PASS / FAIL / BLOCKED / UNVERIFIED.
5. Run fresh critics on highest-risk areas.
6. Fix highest-impact 1–3 gaps.
7. Re-observe and verify.
8. Update state.
9. Attempt to finish; Stop verifier independently checks the pass.

CONTINUE is a fresh quality pass over current reality.

## CANCEL

CANCEL only when `$ARGUMENTS` is exactly:

```text
cancel
```

Meaning:

> Stop the active Gauntlet run cleanly.

In CANCEL mode:
1. Read `.claude/gauntlet-state.md` if present.
2. Set status to `CANCELLED`.
3. Preserve Goal Ledger, evidence, and remaining gaps for possible future recovery.
4. Do not implement, review, schedule `/loop`, or create a new goal.
5. Report that Gauntlet mode was cancelled.

# 2. Goal Ledger

Maintain:
- `G1` initial locked target
- `G1.1`, `G1.2` additive user deltas
- `G2` explicit direction replacement

Treat "이것도 추가해", "그리고 이것도", "작업하면서 이것도" and similar language as additive deltas unless the user clearly abandons the original direction.

Invariant:

> Later instructions are deltas to the locked Goal Ledger unless they explicitly replace it. Never discard unfinished earlier criteria because of a newer message.

If a delta conflicts:
- identify the conflict;
- preserve unaffected requirements;
- resolve safely when obvious;
- ask only if an irreversible/product decision is genuinely required.

# 3. Persistent state

For non-trivial work maintain:

```text
.claude/gauntlet-state.md
```

Recommended structure:

```markdown
# Gauntlet State

## Status
ACTIVE | COMPLETE | BLOCKED | CANCELLED

## Phase
DISCOVER | IMPLEMENT | REVIEW | ADDRESS | VERIFY | COMPLETE

## Depth
LIGHT | STANDARD | DEEP

## Goal Ledger
G1 / G1.1 / ...

## Outcome
...

## Mandatory Criteria
- [PASS] ...
- [FAIL] ...
- [UNVERIFIED] ...
- [BLOCKED] ...

## Quality Bar
- ...

## Evidence Ledger
- criterion → command/runtime/capture/review evidence

## Current Risk Areas
- ...

## Remaining High-Impact Gaps
1. ...
2. ...
3. ...

## Last Pass
- observed:
- changed:
- re-verified:

## Blockers
- ...
```

Rules:
- State is a ledger, not truth. Validate against current artifact.
- Update after meaningful verification.
- Never store credentials/secrets.
- Avoid bloated histories; keep current truth.
- If absent during CONTINUE, reconstruct it from available evidence.

# 4. Inspect before prescribing

Before substantial edits inspect relevant:
- `CLAUDE.md` / project rules
- package/build config
- architecture
- tests
- nearby implementation conventions
- working tree
- current runtime/output

Do not guess framework commands that can be discovered.

Prefer existing architecture unless replacement is justified.

# 5. Target design

Normalize START input into:

## Outcome
One-sentence end state.

## Mandatory criteria
Observable must-pass behavior.

## Quality bar
What distinguishes merely working from requested quality.

## Evidence plan
How each important criterion can be verified.

## Freedom
Implementation details Claude may decide after inspection.

Keep ambitious references as an aspirational bar, not a fake deterministic promise.

# 6. Automatic Gauntlet depth

Choose depth automatically after inspection. Optimize for reliability, not minimal token use.

## LIGHT
Use only for narrow, low-risk, objectively verifiable work.

Typical:
- one module
- small bug
- contained migration
- straightforward type/test cleanup

Default review:
- 1 builder/owner
- 1 diff/regression critic
- independent Stop verifier

## STANDARD
Default for meaningful feature work or cross-file changes.

Typical:
- medium feature
- moderate refactor
- API/UI integration
- nontrivial workflow

Default review:
- coherent builders by ownership
- 2–3 critics chosen from diff / holistic / runtime / domain
- independent Stop verifier

## DEEP
Use aggressively for quality-sensitive, creative, multi-system, visual, game, architecture-heavy, or historically premature-completion work.

Typical:
- games
- polished UI/UX
- visual/reference matching
- major refactor
- multi-system interaction
- difficult performance work

Default review:
- coupling-aware builders
- 3–5 relevant fresh critics
- artifact harness/reproducibility work when it materially improves evidence
- independent Stop verifier
- multiple immediate critic/fix rounds when useful

Do not downgrade from DEEP merely to save tokens. Avoid waste through relevance and deduplication, not by removing valuable independent review.

# 7. Coupling-aware orchestration

Do not blindly fan out.

Parallelize when:
- ownership is clear;
- coupling is low;
- outputs are independently testable;
- integration boundaries already exist.

Prefer sequential/coherent ownership for tightly coupled concerns:
- lighting + materials + exposure/tonemapping;
- movement + camera + collision;
- state + navigation + synchronization;
- schema + transaction/business invariants.

Independent critics may review coupled systems even when builders should not edit them in parallel.

# 8. Adaptive critic panel

Use a small adaptive panel.

Possible critic roles:

### Diff Critic
Correctness, regressions, security, test gaps, suspicious shortcuts.

### Holistic Critic
Architecture, integration, project conventions, duplicate systems, preserved user outcome.

### UX / Runtime Critic
Real flows, responsive behavior, accessibility, interaction states, visible runtime breakage.

### Visual Fidelity Critic
Rendered states versus quality bar/reference: composition, scale, lighting, materials, legibility, animation/physics cues.

### Gameplay / Behavior Critic
Controls, state transitions, feedback, progression, win/fail/restart, collision/physics behavior.

### Performance Critic
Only when performance matters: realistic workload, frame time/tail latency, stalls, memory, bundle/build/runtime metrics.

### Domain Critic
Only when genuinely required.

Guidelines:
- LIGHT: usually 1 critic.
- STANDARD: usually 2–3 critics.
- DEEP: usually 3–5 relevant critics.
- Fresh critic context when possible.
- Critics observe evidence/artifact, not builder self-praise.
- Ask for concrete findings with severity and evidence.
- Consolidate/deduplicate before fixing.
- Fix the 1–3 highest-impact gaps per round.

# 9. Review consolidation

Consolidate findings:

```text
P0 / Critical
P1 / High
P2 / Medium
P3 / Optional
```

Deduplicate by root cause.

Prefer root-cause fixes that close multiple findings.

Do not blindly obey critic prescriptions; re-measure underlying reality when evidence conflicts.

# 10. Artifact harness discovery

Before inventing verification machinery, inspect whether project already has:
- tests
- browser/E2E tooling
- screenshot/capture scripts
- visual regression
- profiling scripts
- smoke/playtest scripts
- benchmark fixtures
- reproducible seeds/scenarios

Reuse existing harnesses.

If quality cannot be verified reliably and task is large enough, create the smallest reusable harness that materially improves iteration.

# 11. Reproducibility before measurement

For visual captures:
- control viewport/device settings;
- isolate hidden state where practical;
- control random seed/time when practical;
- avoid cross-shot state leakage.

For performance:
- test realistic active workload;
- prefer useful tail/distribution metrics over one flattering average when relevant;
- identify major stalls/outliers.

If measurements are unstable, fix the harness before optimizing against noise.

# 12. Evidence-driven Gauntlet cycle

Each iteration:

1. OBSERVE real artifact.
2. COMPARE against Goal Ledger/reference.
3. CRITIQUE using fresh independent review.
4. CONSOLIDATE findings/root causes.
5. PRIORITIZE top 1–3 gaps.
6. FIX without unrelated rewrites.
7. RE-OBSERVE changed behavior/visual/output.
8. RECORD PASS / FAIL / BLOCKED / UNVERIFIED.
9. CONTINUE while high-impact useful work remains.

Priority:
1. missing/broken mandatory behavior
2. correctness/regressions
3. integration/root-cause system issues
4. usability/fidelity
5. performance if relevant
6. polish
7. nonessential refactor

"Implemented" is not "verified."

# 13. Independent Stop verifier

This skill's Stop hook is an independent release verifier.

When it blocks:
- accept its reason as critic feedback;
- inspect the called-out evidence;
- fix or prove the gap;
- update state;
- try to finish again.

The verifier MAY block only for:
- mandatory FAIL;
- mandatory UNVERIFIED where verification is feasible;
- P0/P1 actionable defects;
- claimed completion without evidence;
- failure to re-observe after meaningful change.

The verifier MUST NOT block only for:
- P2/P3 polish;
- stylistic preference;
- speculative optimization;
- alternate architecture preference;
- impossible literal equality with an aspirational reference;
- recorded external blockers;
- CANCELLED state.

The Stop verifier is a release gate, not the only critic.

# 14. Artifact-specific evidence

## Game / visual UI
Code inspection alone is insufficient.

When feasible:
- launch actual build;
- exercise promised controls;
- inspect meaningful runtime states/screenshots;
- verify transitions/collisions/layout/scale;
- check full start→play→win/fail→restart loop;
- compare supplied references side-by-side.

## Code-heavy work
Use relevant tests, build, typecheck, lint when meaningful, runtime, and regression checks.

## Performance work
Use realistic workload and useful distribution/tail metrics where possible.

## Research/docs
Use source/fact/coverage/consistency/audience/format checks appropriate to task.

# 15. Stop rules

A pass can end when:
- its high-priority planned checks were performed;
- no immediately actionable high-severity gap remains in that pass;
- changed areas were re-observed;
- unresolved work is recorded.

Overall COMPLETE only when:
- all mandatory criteria are evidenced PASS;
- independent review finds no P0/P1 actionable gap;
- artifact was re-observed after latest meaningful fix;
- remaining issues are optional polish only.

Use BLOCKED for genuine external blockers.

Do not require literal perfection.

# 16. `/loop` relationship

`/gauntlet-mode continue` = one extra fresh quality pass.

User may schedule:

```text
/loop /gauntlet-mode continue
```

or:

```text
/loop 15m /gauntlet-mode continue
```

`/loop` is scheduled persistence, not the immediate inner Gauntlet loop.

CONTINUE must NEVER:
- create another `/loop`;
- recursively schedule itself;
- spawn another gauntlet-mode solely to continue.

Stop verifier already provides immediate "are you really done?" continuation. `/loop` is for later/fresh passes when one invocation is still insufficient.

# 17. `/goal` relationship

Do not require `/goal`.

If user uses `/goal`, treat it as optional deterministic gate for transcript-verifiable conditions:
- build exit 0
- tests pass
- type errors 0
- concrete acceptance checks evidenced

Do not use `/goal` as sole visual/UX quality judge.

# 18. Mid-task deltas

When user adds a requirement:
1. version `G1 → G1.1` unless direction truly changes;
2. update state;
3. preserve unfinished earlier criteria;
4. integrate new requirement;
5. verify against actual artifact.

Do not restart.

# 19. External critic integration

If an already-installed, user-authorized external reviewer is available, you MAY use it as one fresh critic when it materially improves independence.

Do not:
- install external tools without request;
- weaken sandbox/security;
- depend on external critic availability.

Internal fresh Claude critics remain default.

# 20. User-facing updates

For long work, provide concise updates for:
- major defect discovery;
- implementation milestone;
- critic finding that changes strategy;
- strong verification evidence;
- genuine blocker.

Do not narrate every tool call.

# 21. Final response

Keep compact:

## Gauntlet status
`ACTIVE` / `COMPLETE` / `BLOCKED` / `CANCELLED`

## This pass
- key changes
- real evidence obtained

## Remaining
- only highest-impact unresolved items

If ACTIVE, mention `/gauntlet-mode continue` for one more manual quality pass.

Mention `/loop /gauntlet-mode continue` only when sustained repeated passes are genuinely useful.

If user wants to stop further Gauntlet enforcement, `/gauntlet-mode cancel` is the explicit escape hatch.
