---
name: benchmark-agent-review
description: Review persisted benchmark run outputs with one or more agent graders and report subjective ergonomic quality separately from deterministic benchmark scores
type: analysis
version: v0.3
required_conventions: [alignment-page]
argument-hint: "<skill name or run path> [--reviewers codex,claude] [--runs N]"
---

# Benchmark Agent Review

Invoke as `$benchmark-agent-review <skill-or-run-path>`.

Use this skill after `$benchmark-test-skill <skill>` when the deterministic benchmark in `agentic-skills-benchmarks` passed but the user wants agent judgment on whether the generated artifacts are actually excellent, ergonomic, and useful for the next caller.

Act as a follow-up review workflow. It does not replace hard benchmark assertions, deterministic output-quality rubrics, or verify/bench commands.

The primary object of review is the generated skill output, not the benchmark harness. Treat hard assertions and deterministic output-quality scores as context and triage signals only. Lead with whether each retained output is excellent, good, usable, weak, or failing under the agent-review rubric; discuss deterministic rubric tightening only after output-quality findings, and only when it would help future triage surface the same output-quality issue.

## Input

- Required: a benchmark target skill name such as `run`, or a raw run directory in `agentic-skills-benchmarks`, such as `tests/benchmarks/runs/run-codex-47e0dd54/`.
- Optional: `--reviewers codex,claude` to request named reviewer families when both outputs are available.
- Optional: `--runs N` to request multiple independent review passes. Default to 3 when practical; use 1 when only one reviewer pass is available in the active environment.

## Process

1. Resolve benchmark evidence:
   - Work from `/Users/georgele/projects/tools/agentic-skills-benchmarks` (or the user's local benchmark repo checkout). Do not look for benchmark runs in the `agentic-skills` source repo.
   - If the input is a run directory, inspect that directory.
   - If the input is a skill name, find the newest matching directories under `tests/benchmarks/runs/<skill>-*/`.
   - Prefer the latest Claude and Codex run directories when both exist.
   - Read `report.md`, `report.json`, each `run-*.json`, and any persisted generated artifact content visible in stdout/stderr or file snapshots.
   - If generated artifact content is not fully available, state that limitation and grade only the retained evidence.

2. Extract outputs under review:
   - Identify the artifact path the benchmark expected, such as `run-plan.md` or `benchmark/test-*.md`.
   - Extract the generated artifact text when available.
   - Preserve runner identity, run index, hard assertions, deterministic quality score, and infrastructure-blocked status.
   - Exclude infrastructure-blocked runs from subjective scoring.

3. Build the review packet:
   - Include the original benchmark prompt.
   - Include the benchmark fixture facts.
   - Include the output artifact text or retained summary.
   - Include hard assertions and deterministic quality scores for context.
   - Include the target skill contract only when needed to judge ergonomics.

4. Grade each evaluated output with this rubric:
   - **Task selection clarity**: the selected work is unambiguous and traceable to fixture evidence.
   - **Implementation specificity**: the output gives a next caller concrete enough steps to act without redoing basic discovery.
   - **Validation strength**: proposed checks prove behavior or artifact quality, not just file existence or generic completion.
   - **Scope control**: the output respects the fixture and user constraints without becoming timid or incomplete.
   - **Next-route ergonomics**: the next command is correct for the runner mode and explains what it will do.
   - **No invented facts**: the output avoids unsupported services, files, metrics, commands, deploys, or repository claims.
   - **Residual-risk awareness**: the output names meaningful uncertainty, missing evidence, or follow-up risk when relevant.

5. Score:
   - Use a 0-100 integer score per reviewed output.
   - Treat 90-100 as excellent, 80-89 as good, 70-79 as usable but meaningfully incomplete, 60-69 as weak, and below 60 as failing human review.
   - When multiple review passes are available, report median score, score range, and common findings.
   - Do not blend subjective scores into hard assertion pass rate or deterministic quality score.

6. Optional multi-reviewer handling:
   - Use subagents only when the active Codex tool instructions permit them and the user explicitly requested multiple agent review passes.
   - Assign each reviewer one independent grading pass over the same review packet.
   - Do not let reviewers edit repository files.
   - Synthesize reviewer findings into a normalized score table.

7. Write the report:
   - Create `benchmark/review-<SKILL>-<YYYY-MM-DD>.md` in `agentic-skills-benchmarks` when the input resolves to a skill.
   - Create `benchmark/review-<RUN-DIR-NAME>-<YYYY-MM-DD>.md` in `agentic-skills-benchmarks` when the input is one run directory.
   - If the review is exploratory and the user asks for chat-only output, do not write a file.

8. Build the remediation handoff:
   - Convert every material weakness into a remediation target instead of stopping at broad advice.
   - Classify each target as target-skill contract, benchmark rubric, retained-evidence gap, harness/setup issue, or one-off run behavior.
   - Name the exact owner file, skill contract, benchmark setup, or report artifact when known; when the exact file is not proven, name the narrowest known owner surface and state the lookup needed to confirm it.
   - Propose the exact contract, rubric, fixture, or evidence-capture behavior to add or tighten; avoid vague changes such as "update the skill" without naming the behavior that changes.
   - Include the validation command or contract-lint assertion that would prove the issue is fixed; a focused fixture rerun is acceptable only when it names the expected assertion or artifact-quality behavior.
   - When retained artifact text contains placeholder risk, monitoring, validation, or known-unknown sections such as `Not captured`, `Not specified`, `TBD`, `None`, or `N/A`, the remediation must identify the owner target that should reject or repair that placeholder and the validation check that would fail before the fix.
   - Choose one definitive next route from the highest-impact verified remediation; do not leave the next caller to choose among generic options.

## Output

Report:

- Source benchmark report paths.
- Reviewed run directories and run indexes.
- Hard assertion pass rate and deterministic output-quality score from the benchmark report.
- Output-quality verdict against the agent-review rubric, explicitly focused on the generated skill artifacts rather than the benchmark's ease or strictness.
- Agent-review score table with reviewer, runner, run index, score, and grade band.
- Median subjective score and score range when multiple scores exist.
- Common strengths.
- Common weaknesses.
- Remediation table with finding, classification, owner target, proposed change, validation check, and route.
- Remediation rows must be implementation-ready: each material finding needs a concrete owner target, a proposed behavior change, and a validation check or command. Broad rows like "tighten the rubric" or "update the skill" are incomplete unless they also name the owning file/surface, exact behavior, and proof.
- Optional deterministic-rubric notes only when the retained output-quality findings show the deterministic rubric failed to surface a meaningful issue or produced misleading context.
- **Next work:** the one definitive remediation selected from the remediation table, or no follow-up when all evaluated outputs are excellent and no meaningful issue remains.
- **Recommended next command:** one command derived from that remediation, usually `$targeted-skill-builder <skill> <specific output-quality gap>`, `$targeted-skill-builder <benchmark setup or reviewed skill> <specific rubric gap>`, `$session-triage <skill> benchmark review`, or `$ship` only when no remediation is needed.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/benchmark-agent-review-{topic}.html`. By default, report results inline and write only this skill's normal durable artifacts; create an alignment page only when explicitly requested or when a concrete clarification/review need cannot be handled cleanly inline.

## Constraints

- Do not re-run `$benchmark-test-skill` unless the requested benchmark artifacts are missing or stale and the user explicitly asks for a fresh benchmark.
- Do not present subjective agent-review scores as statistically definitive.
- Do not merge subjective scores into deterministic output-quality scores.
- Do not frame benchmark pass/fail laxness as the primary problem when the task is to judge skill output quality. If the benchmark intentionally passes weak-but-compliant outputs, grade the output quality directly and use deterministic-rubric notes only as supporting context.
- Do not grade infrastructure-blocked runs as skill outputs.
- Do not fabricate missing artifact content. State when only stdout summaries, assertions, or quality results are available.
- Do not collapse multiple material weaknesses into a vague handoff such as "tighten the rubric"; the remediation table must preserve the responsible target, exact behavior change, and validation check for each issue.
- Do not create or modify GitHub Actions workflows.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
