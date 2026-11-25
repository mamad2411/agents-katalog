---
name: plugin-evolution
description: Use when a coding plugin, skill bundle, command pack, or multi-agent CLI workflow needs output evaluation, baseline comparison, regression testing, or evidence-based improvement across its skills, scripts, commands, agents, configs, routing, and validation.
compatibility: Requires Python 3.11+ and a host capable of running the target coding CLI or agent workflow. Git is recommended. External agent CLIs are optional and must be invoked for real when claimed.
---

# Plugin Evolution

## Overview

Evaluate a coding plugin as an engineered system, not as a prompt that merely sounds good. Measure whether it improves real coding outcomes, explain why, change the smallest causal component, and re-run the same evidence-bearing tests before accepting the change.

**Core principle:** no plugin change is an improvement until a controlled candidate beats its frozen baseline without creating a meaningful regression.

## Use Modes

Choose the narrowest mode that matches the request.

| Mode | Use it for | Mutates target plugin? |
|---|---|---:|
| `audit` | Static structure, broken references, invalid scripts/configs, unclear routing | No |
| `evaluate` | One plugin version on real coding tasks | No |
| `compare` | Candidate versus baseline, paired and blinded | No |
| `improve` | Diagnose, patch a candidate copy, re-evaluate | Candidate copy only |
| `benchmark` | Repeated runs, variance, cost, latency, stability | No |
| `promote` | Decide whether a validated candidate may replace baseline | Only with explicit human approval |
| `trigger-optimize` | Skill/command description triggering accuracy | Candidate copy only |

If intent is clear, proceed. If it is not, present the modes and ask for one choice.

## Non-Negotiable Rules

1. Freeze the baseline before analysis or edits.
2. Run candidate and baseline against the same task, fixture, environment, budgets, and verification commands.
3. Never claim an agent CLI participated unless its process returned evidence: command, exit code, timestamps, stdout/stderr or structured result.
4. Run deterministic checks before model graders. Tests, typecheck, lint, build, schema checks, and file assertions outrank prose judgments.
5. Keep task-outcome quality separate from plugin-execution quality.
6. Attribute failure before editing. A bad output may come from the task, fixture, environment, runner, executor model, evaluator, or plugin.
7. Change one coherent causal hypothesis per iteration.
8. Edit only an allowlisted candidate copy. Protect secrets, git metadata, eval fixtures, and baseline snapshots.
9. Re-run targeted failures and a holdout regression set.
10. Reject or roll back candidates that do not clear promotion gates.
11. Do not let the plugin grade or approve its own work without independent checks.
12. Stop honestly when evidence is insufficient, external tools are unavailable, or the budget is exhausted.

## Resolve Paths

Set `PLUGIN_EVOLUTION_ROOT` to the directory containing this `SKILL.md`. When this skill runs from the `plugin-developer` plugin, that is `${CLAUDE_PLUGIN_ROOT}/skills/plugin-evolution`.

```bash
export PLUGIN_EVOLUTION_ROOT="${CLAUDE_PLUGIN_ROOT}/skills/plugin-evolution"
python "$PLUGIN_EVOLUTION_ROOT/scripts/plugin_evolution.py" --help
```

Run harness commands from the project or evaluation workspace, not from inside the target plugin unless the runner requires it.

## Required Inputs

Collect or infer these from the repository before asking the user:

- Target plugin root and primary entrypoints.
- Coding task or evaluation suite.
- Repository fixture or reproducible checkout.
- Host runner command that loads the plugin for real.
- Verification commands and expected artifacts.
- Mutable and protected plugin paths.
- Baseline policy: current plugin snapshot, previous release, or no-plugin control.
- Repeats, timeout, token/tool-call budgets, and promotion gates.

Use `templates/plugin-profile.example.json` and `templates/eval-suite.example.json` as the machine-readable contracts. Read `references/schemas.md` when creating or changing them.

## End-to-End Workflow

### 1. Inventory the Plugin

Map the full plugin, not only its entry skill.

```bash
python "$PLUGIN_EVOLUTION_ROOT/scripts/plugin_evolution.py" inventory \
  --plugin /path/to/plugin \
  --output workspace/plugin-inventory.json

python "$PLUGIN_EVOLUTION_ROOT/scripts/plugin_evolution.py" validate \
  --plugin /path/to/plugin \
  --output workspace/static-validation.json
```

Inventory and classify:

- `SKILL.md` and referenced skills
- commands and slash-command entrypoints
- agent prompts and role contracts
- Python, shell, TypeScript, or other helper scripts
- config, roster, model routing, defaults, budgets, and fallbacks
- templates, schemas, references, and examples
- validation gates, stop conditions, and result artifacts

Create a component map that explains how a user request becomes dispatch, execution, verification, synthesis, and final output.

### 2. Define the Evaluation Contract

Each task must specify:

- realistic prompt and fixture
- task category and risk
- observable expected outcome
- deterministic verification commands
- required and forbidden files or changes
- critical invariants and safety checks
- optional qualitative rubric
- whether the task belongs to train, targeted regression, or holdout

Use at least three task shapes for broad plugins:

1. straightforward implementation
2. ambiguous or failure-prone debugging/integration task
3. adversarial or degraded-tool task that tests fallback and honesty

For multi-agent plugins, also include a task where one panelist is unavailable and a task where fast and expert workers disagree.

### 3. Freeze Baseline and Candidate

```bash
python "$PLUGIN_EVOLUTION_ROOT/scripts/plugin_evolution.py" prepare \
  --plugin /path/to/plugin \
  --workspace workspace \
  --iteration 1
```

The command creates immutable baseline evidence and an editable candidate copy. Record tree hashes, git state, tool versions, profile, suite, and timestamps.

Do not edit the original plugin during an evaluation loop.

### 4. Execute Paired Runs

Run baseline and candidate in the same batch so timing and environment drift are minimized.

```bash
python "$PLUGIN_EVOLUTION_ROOT/scripts/plugin_evolution.py" run \
  --profile profile.json \
  --suite eval-suite.json \
  --baseline workspace/snapshots/baseline \
  --candidate workspace/candidates/iteration-1 \
  --workspace workspace/iteration-1
```

The runner must capture:

- exact prompt and fixture hash
- plugin tree hash and configuration
- runner argv without secret values
- start/end time, duration, exit code, timeout state
- stdout, stderr, transcript, output files, and repository diff
- verifier commands and results
- agent participation receipts
- errors, retries, fallbacks, and stop reason

Randomize A/B labels for blind comparison. Keep the mapping outside comparator context.

### 5. Grade Task Outcomes

Deterministic checks run first. Then spawn the `plugin-developer:task-outcome-grader` agent for dimensions that cannot be established mechanically.

Evaluate:

- functional correctness
- completeness and acceptance criteria
- regressions and blast radius
- scope discipline
- code quality and maintainability
- tests and verification quality
- security, privacy, and data integrity
- framework and repository convention fit
- user-facing quality where relevant

A passing filename or plausible explanation is not proof. Inspect actual code, diffs, files, and test output.

### 6. Grade Plugin Execution

Spawn the `plugin-developer:orchestration-grader` agent. This score is separate from task quality.

Inspect:

- correct route/workflow selection
- plan quality and decomposition
- agent assignment and real CLI participation
- parallelism where independent
- maker/checker separation
- handoff completeness and context preservation
- verification and escalation behavior
- synthesis quality and contradiction resolution
- fallback behavior and honest degradation
- token, latency, tool-call, and retry discipline
- adherence to plugin-specific invariants

A good task result produced by ignoring the plugin is not strong evidence that the plugin works.

### 7. Audit Evidence and Claims

Spawn the `plugin-developer:evidence-auditor` agent to verify that claims in the final response are supported by receipts, test output, diffs, and artifacts. Treat missing evidence as a failure of observability even when the result appears correct.

### 8. Blindly Compare Candidate and Baseline

Spawn the `plugin-developer:blind-comparator` agent with A/B paths and the original task contract. Do not expose plugin identity, version, model, or expected winner.

The comparator chooses based on output quality. Assertions are supporting evidence, not a substitute for judgment.

### 9. Diagnose Causality

Spawn the `plugin-developer:root-cause-analyzer` agent after unblinding.

Classify each material failure:

| Cause | Examples |
|---|---|
| `plugin-instruction` | ambiguous routing, missing invariant, bad output contract |
| `plugin-script` | parsing bug, race, timeout, invalid path, weak validation |
| `plugin-command` | wrong entrypoint, missing arguments, lost context |
| `plugin-agent` | overlapping roles, self-approval, weak handoff |
| `plugin-config` | bad roster, model mismatch, budget too low, fallback absent |
| `executor` | ignored clear instruction, unrelated model failure |
| `runner-environment` | CLI unavailable, auth failure, fixture corruption |
| `task-contract` | ambiguous prompt or unverifiable expected result |
| `evaluator` | weak assertion, biased rubric, grading inconsistency |
| `nondeterminism` | unstable result not attributable from current evidence |

Require evidence, confidence, affected tasks, and likely generalization. Do not patch the plugin for an eval bug.

### 10. Propose One Improvement Hypothesis

Spawn the `plugin-developer:patch-planner` agent. The proposal must name:

- observed failure and evidence
- causal plugin component
- exact files and symbols to change
- smallest change likely to fix it
- expected measurable effect
- possible regressions
- targeted tests and holdout checks
- rollback condition

Improvement categories may include:

- skill structure or instruction clarity
- command routing or argument contracts
- agent role boundaries and handoffs
- Python/shell/TypeScript implementation
- model/agent routing and fallback
- evidence, logging, and receipts
- validation gates and stop conditions
- examples, schemas, references, and trigger descriptions

Do not combine unrelated cleanup with the hypothesis.

### 11. Patch Only the Candidate Copy

Before editing, read the relevant component and its callers. Apply the smallest coherent change. Then compare candidate and baseline paths:

```bash
python "$PLUGIN_EVOLUTION_ROOT/scripts/plugin_evolution.py" diff \
  --baseline workspace/snapshots/baseline \
  --candidate workspace/candidates/iteration-1 \
  --profile profile.json \
  --output workspace/iteration-1/plugin-diff.json
```

Reject protected-path changes and unexplained generated artifacts.

### 12. Validate the Candidate Itself

Run static validation, script/unit tests, command schema checks, broken-reference checks, and plugin-specific self-tests before task reruns.

```bash
python "$PLUGIN_EVOLUTION_ROOT/scripts/plugin_evolution.py" validate \
  --plugin workspace/candidates/iteration-1 \
  --output workspace/iteration-1/candidate-validation.json

python -m unittest discover -s "$PLUGIN_EVOLUTION_ROOT/tests" -v
```

### 13. Re-run Targeted and Holdout Tasks

First rerun failures expected to change. Then run the untouched holdout set. Use multiple repetitions where model variance can change the conclusion.

Do not tune against holdout details. A candidate that wins targeted tasks and loses the holdout is not ready.

### 14. Aggregate and Gate Promotion

```bash
python "$PLUGIN_EVOLUTION_ROOT/scripts/plugin_evolution.py" aggregate \
  --workspace workspace/iteration-1 \
  --output workspace/iteration-1/benchmark.json

python "$PLUGIN_EVOLUTION_ROOT/scripts/plugin_evolution.py" gate \
  --benchmark workspace/iteration-1/benchmark.json \
  --profile profile.json \
  --output workspace/iteration-1/promotion-decision.json
```

Promotion requires all configured gates, typically:

- positive paired quality delta
- no critical deterministic regression
- no safety or honesty regression
- acceptable variance
- bounded latency and token/tool cost increase
- all static candidate checks passing
- enough completed paired runs

Spawn the `plugin-developer:regression-judge` agent for a final evidence-based recommendation. The human owns promotion.

### 15. Report and Stop

Produce the report defined in `references/report-template.md` with links to evidence. State:

- what was tested
- what changed
- candidate versus baseline results
- causality and uncertainty
- accepted/rejected gates
- residual risks
- exact recommendation

Stop when any of these applies:

- candidate clears gates and human promotion is pending
- two iterations fail to improve the same hypothesis
- results are too noisy to distinguish
- evaluation contract is invalid
- required CLI or verification dependency is unavailable
- budget or time limit is reached

## Fusion-ML Evaluation Profile

When the target is Fusion-ML or a similar multi-agent orchestration plugin, read `references/fusion-ml-profile.md` before writing the suite.

At minimum, evaluate:

- deterministic startup option ranking
- correct workflow choice after user selection
- real participation receipts for Codex/OpenCode/Grok/Agy/Copilot or configured roster
- expert versus fast-layer routing
- concurrency of independent work
- conductor ownership of high-impact work
- maker/checker separation
- escalation to advisor/critic only when warranted
- Validation Pyramid evidence for ML claims
- honest solo/degraded mode when a CLI fails
- fixed eval ownership and safe mutation boundaries for Auto Research
- stop conditions, budgets, and no fabricated panel consensus

## Quick Reference

| Need | First action |
|---|---|
| Understand plugin structure | `inventory` + `validate` |
| Evaluate current plugin | snapshot baseline, create suite, `run` |
| Compare old and new | paired runs + blind comparator |
| Improve plugin | root-cause analysis, one hypothesis, candidate patch |
| Measure stability | 3+ repeats and benchmark variance |
| Change skill trigger text | separate trigger eval with holdout queries |
| Accept candidate | aggregate, gates, regression judge, human approval |
| CLI unavailable | record failure receipt and run declared degraded mode or stop |

## Common Mistakes

- Evaluating only the final prose response while ignoring repository state and tests.
- Editing the original plugin before preserving a baseline.
- Using one impressive task as proof of general improvement.
- Letting candidate and baseline run with different prompts, tools, or budgets.
- Treating every output failure as a prompt problem.
- Adding more agents when role overlap is the real issue.
- Rewarding verbose orchestration instead of useful work.
- Counting an attempted CLI call as participation.
- Allowing a grader to see candidate identity.
- Optimizing assertions until the candidate passes.
- Promoting from mean score while hiding a critical regression or high variance.
- Changing many plugin components at once, making causality unknowable.

## Output Contract

Every completed evaluation or improvement loop returns:

1. **Decision**: promote, reject, revise, or inconclusive.
2. **Task outcome summary**: deterministic and qualitative results.
3. **Plugin execution summary**: routing, delegation, verification, and evidence quality.
4. **Paired comparison**: candidate versus baseline with variance and costs.
5. **Causal findings**: plugin-caused versus non-plugin-caused failures.
6. **Plugin diff**: exact changed files and reasons.
7. **Gate results**: each promotion gate and evidence.
8. **Residual risks**: untested paths, noisy results, external dependencies.
9. **Next action**: one concrete step, not an open-ended backlog.

## References

- `references/architecture.md` - system boundaries and evidence flow.
- `references/evaluation-rubric.md` - task and orchestration scoring.
- `references/schemas.md` - profile, suite, run, grading, comparison, and proposal contracts.
- `references/runner-adapters.md` - safe CLI runner configuration.
- `references/fusion-ml-profile.md` - Fusion-ML-specific evaluation coverage.
- `references/safety-governance.md` - mutation boundaries and promotion controls.
- `references/report-template.md` - final report structure.
- `agents/*.md` - specialized evaluator and improvement roles.
