---
name: benchmark-test-skill
description: Run verify and benchmark tests for one agentic-skills skill, producing pass-rate, latency, cost, and consistency metrics
type: execution
version: v0.4
required_conventions: [alignment-page]
argument-hint: "<skill name>"
---

# Benchmark Test Skill

Invoke as `$benchmark-test-skill <skill>`.

Use this skill when the user wants to benchmark-test a skill from the public `agentic-skills` catalog using the separate `agentic-skills-benchmarks` repository. The trailing argument is the skill under test, not a mode for that skill. For example, `$benchmark-test-skill design-system` tests the `design-system` skill with the benchmark harness; it does not run `design-system` against the current app or website.

Run the benchmark repo verification gate followed by the benchmark extension for a single skill. By default, benchmark both Claude and Codex runners and report them separately.

Produce deterministic benchmark evidence only. It should hand off to `$benchmark-agent-review <skill>` as a separate step when the user needs subjective ergonomic judgment or remediation planning for the generated skill outputs.

## Input

- Required: one skill name, such as `design-system`.
- If no skill name is provided, ask the user which skill to benchmark-test.
- When invoked as `$benchmark-test-skill <skill>`, resolve `benchmark-test-skill` as the active command first, including this project-local pack path, before treating the trailing argument as the skill under test.
- Do not reinterpret the trailing argument as the active workflow unless the benchmark-test-skill command cannot be found after checking project-local packs.

## Execution

Run commands from `/Users/georgele/projects/tools/agentic-skills-benchmarks` (or the local checkout of the public `agentic-skills-benchmarks` repo). If the checkout is missing, stop and ask for its path instead of running benchmark commands from `agentic-skills`.

### Step 0 - Command Resolution Guard

Confirm the active workflow is this `packs/agentic-skills-bench` skill. The requested target skill is data for the benchmark harness, not a command to execute directly.

- For command-like invocations, preserve the leading command and route by the pack command first.
- If a target such as `design-system`, `run`, or `ship` is provided, never run that skill directly as the benchmark action.
- If command resolution is ambiguous, stop and report the ambiguity instead of running the target skill.

### Step 1 - Eligibility Preflight

Before running verify, check whether the requested skill is a repository skill known to the benchmark harness:

```bash
SKILLS_REPO_URL=/Users/georgele/projects/tools/agentic-skills SKILLS_REPO_REF=WORKTREE pnpm catalog:check
pnpm bench -- --list-skills
```

- If `<SKILL>` is not listed, stop immediately and report `unknown skill: <SKILL>`.
- List the known repository skills from the command output.
- Do not run `pnpm verify` or `pnpm bench` for unknown skills.
- Read and report the listed coverage status for `<SKILL>`: `custom`, `generic`, or `blocked`.
- Skills with custom layer4 setups use skill-specific fixtures and hard assertions. Some setups also include deterministic output-quality rubrics.
- Skills without custom layer4 setups use the harness generic smoke benchmark. Treat that as invocation/compliance evidence, not deep domain-quality evidence.
- If the row is `blocked`, stop before verify and bench. Report the blocked reason and next command from the list output.
- If the row is `generic`, continue only as generic smoke evidence and route missing custom coverage to `$targeted-skill-builder <SKILL> benchmark coverage`.

### Step 2 - Verify

```bash
SKILLS_REPO_URL=/Users/georgele/projects/tools/agentic-skills SKILLS_REPO_REF=WORKTREE pnpm verify -- --skill <SKILL>
```

- Expect layer1 to pass and layer2 to pass when target-specific tests exist.
- Treat layer1 as the static harness-contract gate, including basic benchmark setup alignment checks such as expected next-route handoffs, runner command conventions, output file expectations, and quality-rubric facts against the current skill contract.
- If layer1 fails because a benchmark setup is misaligned with the skill contract, classify it as a harness/benchmark coverage defect and route to `$targeted-skill-builder <SKILL> benchmark failure`; do not spend agent budget on `pnpm bench`.
- If layer2 reports no tests matched `<SKILL>`, treat that layer as skipped and continue to the benchmark step. Record the skip clearly because generic benchmark coverage is weaker than target-specific layer2 verification.
- Record pass/fail and wall time per layer.
- If verify fails, stop and report the failure. Do not run the benchmark step.

### Step 3 - Bench

Run only if verify passes:

```bash
pnpm bench -- --skill <SKILL> --agent both --runs 3 --chunk-size 3 --pause 0
```

- Use 3 iterations by default.
- Use `--agent both` by default. Only use `--agent claude` or `--agent codex` when the user explicitly asks to isolate one runner.
- The expected budget is about $1 per run for the current design-system variant; report actual cost from the benchmark output when available.
- The bench system persists raw data inside `agentic-skills-benchmarks` at `tests/benchmarks/runs/<skill>-<agent>-<sessionId>/` and generates `report.json`.
- Treat rate limits, quota exhaustion, and similar runner-capacity errors as infrastructure-blocked runs, not skill failures. Report them separately from evaluated pass rate.
- If recent same-skill benchmark reports or triage reports show repeated same-family benchmark false negatives, do not recommend another blind rerun as the next step. Report the recurrence and route to `$targeted-skill-builder <SKILL> benchmark repeated false-negative generalization` so the harness/setup gets a family-level semantic evaluator, fixture set, or infrastructure classifier instead of another one-off tolerance patch.

### Step 3.5 - Regression Check

Run only if the bench step produced an evaluated report (skip if every run was infrastructure-blocked). This closes the benchmark loop by comparing the fresh grade to the prior grade in `benchmark/grade-history.json` in the benchmark repo:

```bash
node scripts/benchmark-regression-check.mjs <SKILL>
```

- The script reads the newest `report.json` per agent, appends the new grade to `benchmark/grade-history.json` in `agentic-skills-benchmarks`, and prints an `improvement` / `stable` / `regression` verdict per agent.
- A `regression` verdict (passRate, Wilson lower bound, or output-quality drop >= 10pp, or a status-badge demotion) is distinct from an absolute benchmark failure: the skill may still pass its thresholds yet score materially worse than its last graded run. The script exits non-zero on regression.
- On a `regression` verdict, carry the printed prior-vs-new delta block into the next step and route to `$session-triage <SKILL> benchmark regression` so a human decides whether it is a real behavioral regression or harness/rubric drift. Do not auto-fix.
- On `improvement` or `stable`, continue to the report; note the verdict in the report.
- See `docs/benchmark-improvement-loop.md` for the full human-approved cycle this step participates in.

### Step 4 - Report

Write results to `benchmark/test-<SKILL>-<YYYY-MM-DD>.md` in `agentic-skills-benchmarks`. Use the current date.

Populate the report from `report.json` and verify the output includes:

- verify table with layer status and wall time
- agent name, evaluated pass rate, blocked-run count, and Wilson 95% confidence interval
- failed assertions, if any
- output-quality score summary when the setup defines a quality evaluator, including threshold failures, critical failures, and lowest-scoring criteria when present
- infrastructure-blocked runs, if any
- regression verdict from Step 3.5 (`improvement` / `stable` / `regression`) with the prior-vs-new delta when a prior grade existed
- latency p50, p95, and p99
- cost per run and total cost
- mean pairwise similarity and outlier count
- raw session path
- recommended next route, using a literal label such as `Recommended next command:` or `Recommended next skill:`

After writing the report, verify the file exists and contains the benchmark target, agent rows, pass-rate or blocked-run data, latency, cost, and raw session path. If any required report field is missing, treat the workflow as incomplete and fix the report before marking the benchmark done.

## Output

Print a concise benchmark summary:

- verify pass/fail
- hard assertion pass rate
- output-quality score when present, labeled as an additional rubric score rather than a statistical confidence measure
- infrastructure-blocked count, if any
- p50 latency
- total cost
- report path
- next review handoff when subjective output-quality judgment or remediation planning is still needed

The Markdown report and the final assistant response must both include a literal next-route label accepted by the harness, such as `Recommended next skill: $benchmark-agent-review <skill>` or `Recommended next command: $ship`.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/benchmark-test-skill-{topic}.html`. By default, report results inline and write only this skill's normal durable artifacts; create an alignment page only when explicitly requested or when a concrete clarification/review need cannot be handled cleanly inline.

## Constraints

- Do not audit or benchmark the app, website, docs, or product surface unless the user explicitly asks for a separate website/product benchmark workflow.
- Do not run `pnpm bench` when `pnpm verify` fails.
- Do not fabricate benchmark metrics. Use the command output and `report.json`.
- Do not present quality score as a replacement for hard assertion pass rate, or present a small benchmark run as statistically definitive.
- Do not omit the final next-step route. Completion output must include either `Recommended next skill: <command>` or the two-line pair `**Next work:** <specific task or "none">` and `**Recommended next command:** <one command or route>`.
- Do not create or modify GitHub Actions workflows.

## Next-Step Routing

If the skill is unknown to the repository, recommend checking the skill name or creating the skill first with `$create-agentic-skill`.

If the skill has blocked benchmark coverage, recommend the row's `next_command`.

If the skill only has generic smoke benchmark coverage or otherwise lacks custom domain-quality assertions, recommend `$targeted-skill-builder <skill> benchmark coverage`.

If the skill fails verification, hard benchmark assertions, or configured quality thresholds, recommend `$session-triage <skill> benchmark failure`.

If `scripts/benchmark-regression-check.mjs` reports a `regression` verdict (the skill still grades but materially worse than its last graded run), recommend `$session-triage <skill> benchmark regression` and carry the prior-vs-new delta block into that handoff.

If benchmark runs are blocked only by rate limits or quota exhaustion, recommend re-running `$benchmark-test-skill <skill>` after the reset instead of treating the skill as failed.

If the failure pattern has already been triaged as a repeated same-family benchmark false negative, recommend `$targeted-skill-builder <skill> benchmark repeated false-negative generalization` instead of another `$benchmark-test-skill <skill>` rerun.

If evaluated benchmark runs completed and subjective output-quality review or remediation planning has not yet been performed, recommend `$benchmark-agent-review <skill>` as the next separate step.

If the skill passes, the report is written, and no subjective review is needed or the separate `$benchmark-agent-review <skill>` step has already been completed, recommend `$ship`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
