---
name: grimoire-loop
description: Orchestrate implement→check+review+test→fix loop until clean, then format. Use when implementation is complete and needs verification, or when code changes must pass all quality gates automatically.
disable-model-invocation: true
---

# Purpose

Orchestrate a quality assurance loop: implement code from a plan, run check+review+test in parallel against the actual changes, fix blocking findings, repeat until clean, then format.

# Scope

This skill controls the QA loop that runs after initial implementation. It orchestrates grimoire-implement, grimoire-check, grimoire-test, and grimoire-review.

Outside scope: writing plans, writing specs, decomposing tickets, recording ADRs, clarifying requirements.

# Leading words

- **iteration** — one complete cycle of implement → QA → assess
- **finding** — an issue reported by check, review, or test
- **clean** — zero blocking findings from all three QA skills
- **blocking finding** — a gap, blocking deviation, test failure, or blocking review issue

# Workflow

## 1. Pre-flight

Determine the plan source:

- Plan file path provided by user → use it directly.
- No plan given → ask: "Which plan should I implement and verify?"

Read the plan. Confirm it is a valid grimoire plan file (`.grimoire/plans/NNNN-title.html`).

Completion: Plan path is resolved and plan content is loaded.

---

## 2. Implement

Invoke grimoire-implement against the plan. Produce all code changes.

Completion: Implementation complete. All planned changes are coded and compiles.

---

## 3. Capture changes

Capture the diff of all changes produced by implement:

```
git diff
```

Also capture untracked new files:

```
git diff --cached && git diff && git ls-files --others --exclude-standard
```

Prefer: `git diff HEAD` if changes are unstaged, or `git diff --cached` if staged.

Save the diff content. It will be injected into every QA sub-agent.

Completion: Diff captured. Contains every line added, modified, or removed by implement.

---

## 4. Parallel QA — use sub-agents

**Mandatory: use the Agent tool to launch sub-agents.** Do NOT run check, review, or test inline in the main agent. Each must be a separate sub-agent so they execute in parallel.

Launch all three sub-agents in one message with `run_in_background: true` on each:

| Sub-agent    | Invoke skill    | Injected context        | Writes files? |
| ------------ | --------------- | ----------------------- | :-----------: |
| Check agent  | grimoire-check  | plan content + git diff |      No       |
| Review agent | grimoire-review | git diff                |      No       |
| Test agent   | grimoire-test   | git diff                |      Yes      |

Prompt templates live in [references/agent-prompts.md](./references/agent-prompts.md).

Rules:
- Launch all three sub-agents in a single message. All three MUST use `run_in_background: true`.
- Use `get_subagent_result` to collect results. Do not poll — wait for completion notifications.
- Check and Review agents read and analyze only — they do not modify files.
- Test agent writes test files and executes them.

Completion: All three sub-agents have returned results. All three reports collected via `get_subagent_result`.

---

## 5. Assess

Collect all three reports. Classify every finding:

| Source | Blocking                 | Advisory                           |
| ------ | ------------------------ | ---------------------------------- |
| Check  | gap, blocking deviation  | advisory deviation, harmless extra |
| Review | blocking issue           | suggestion, praise                 |
| Test   | test failure, test error | uncovered edge case noted          |

Decision tree:

```
Blocking findings = 0?
├── Yes → proceed to step 6 (Format)
└── No
    └── Iteration count < 3?
        ├── Yes → feed blocking findings to step 2 (Implement), increment counter
        └── No → report remaining blocking findings, stop
```

When feeding findings back to implement: include the concrete file paths, line references, and the exact issue description from each finding. The implement step uses these as fix targets.

Completion: Decision recorded. Either exit-clean, iterate, or exit-with-issues.

---

## 6. Format

Detect project formatters. See [references/format-detection.md](./references/format-detection.md).

Run the detected formatter on all modified files. Verify formatting produces no unexpected changes.

Completion: All modified files pass the project formatter.

---

## 7. Report

Deliver final summary:

- Iterations completed.
- Final status: **clean** or **issues remaining**.
- Per-skill summary: check matches/gaps/deviations, review blocking/suggestions, test pass/fail counts.
- If issues remain: list each blocking finding with location and description.

Completion: Report delivered.

---

# Rules

- Max 3 iterations. After 3 iterations with remaining blocking findings, stop and report.
- Feed only blocking findings back to implement. Advisory findings are noted but do not block progress.
- Parallel QA must use sub-agents (Agent tool with `run_in_background: true`). Never run QA inline or sequentially.
- Format only after QA is clean. Do not format between iterations.
- Every iteration re-runs all three QA skills — do not skip a skill because it was clean before.
- Do not modify files during assessment. Only the implement step writes code.
