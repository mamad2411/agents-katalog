---
name: test-design-review
description: |
  Use this skill to verify TDD test design completeness for a user-specified codebase, plan, or change set, against the project's TDD standard document (`.claude/skills/control-tower/rules/TDD.md`). Trigger this skill whenever the user says any of: "test design review", "TDD review", "test completeness review", "test coverage design check", "review my test design", "did we plan enough tests", "what tests are missing", "audit our test plan", or any phrase asking *what tests should exist* (as opposed to *whether existing tests pass*). Bilingual triggers like "TDD 테스트 설계 검토", "테스트 완전성 리뷰", "테스트 누락 점검" also apply. The skill dispatches the `test-design-reviewer` subagent against the specified path and saves a standardized report as `test-design-review.md` at the codebase root. Use this proactively when a feature plan is finalized, when implementation is about to start, after a major step ships, or whenever a developer asks "did we plan enough tests?" — missing test *design* is far cheaper to fix before code ships than after.
---

# Test Design Review

Dispatch a `test-design-reviewer` subagent to verify whether the test design for a target codebase or change set is complete according to the project's TDD standard (`.claude/skills/control-tower/rules/TDD.md`).

**Announce at start:** "I'm using the test-design-review skill."

## What this skill verifies

This skill checks **test *design* completeness** — *"are the right kinds of tests planned or present?"* — based on the four-stage pyramid, decision trees, and matrix defined in `TDD.md` (chapters 1, 2, 3, 4). It does **not** judge implementation correctness of individual tests (use `code-review` for that) or architectural fitness (use `arch-review`).

## Bootstrap: Read Rules

Before dispatching the review subagent, read this rule as the authority document:

| Rule file | Why |
|---|---|
| `.claude/skills/control-tower/rules/TDD.md` | The sole authority for test design completeness — every recommendation traces back to it |

## Process

1. **Identify the review scope.** Confirm with the user (or infer from context):
   - **Codebase path** — the directory the reviewer should evaluate. Default: current working directory.
   - **Target items** — the feature, plan, or change set to review. Examples: a `plan.md`, a recently merged feature, a specific module path, a commit-hash range. If only a path is given, treat *"all items implied by recent changes or open plan documents in that path"* as the target.
   - **Output path** — where to save the report. Default: `<codebase-path>/test-design-review.md`.
   - **TDD standard location** — default: `<codebase-path>/.claude/skills/control-tower/rules/TDD.md`. If absent, halt and tell the user to provide one (the skill cannot run without a standard document).

2. **Locate skill resources.** This skill bundles two files the agent needs:
   - `test-design-review-agent-prompt.md` — the full review protocol.
   - `test-design-review-report-template.md` — the exact output format.

   Resolve their absolute paths from this skill's directory.

3. **Dispatch the `test-design-reviewer` subagent.**
   - Use the Agent tool with `subagent_type: test-design-reviewer` if it appears in the available agent list; otherwise use `general-purpose`.
   - Description: `Test design review: <short scope>`.
   - Prompt: include the full contents of `test-design-review-agent-prompt.md`, then append a context block with:
     - Absolute codebase path.
     - Target items (paths, commit range, plan file, etc.).
     - Output path for the report.
     - Absolute path to the report template.
     - Absolute path to `TDD.md`.

4. **The subagent performs:** READ STANDARD → DISCOVER → CLASSIFY → APPLY DECISION TREES → COMPARE → REPORT.

5. **Receive the agent summary** containing report path, verdict, and gap counts.

6. **Verify the report file was written** to the expected path. If not, surface the failure to the user.

7. **Report back to the user**:
   - Where the report was saved (absolute path).
   - Verdict (Ready / Needs fixes / Blocked).
   - Gap counts (Critical / Important / Minor).
   - Top 3 actions from the agent summary.

   Keep the user-facing summary short — the full reasoning lives in the report file.

## When to use

- Before starting implementation, after a `plan.md` is finalized.
- After a major implementation step lands, before the next step begins.
- When a development skill (planning, subagent-driven-development, code-review) wants a test-design check before handoff.
- When the user explicitly asks for a test design review, test completeness audit, or a "did we plan enough tests?" check.

## Key rules

- **Never run the review in the main context.** Always dispatch the subagent. The protocol is heavy and self-contained; running it inline pollutes context and slows the main loop.
- **Always pass `TDD.md` as the authority.** Do not let the agent invent its own standard. If `TDD.md` is missing, halt and inform the user.
- **The report file is mandatory.** The agent's job isn't done until `test-design-review.md` exists at the output path. The chat summary is for the dispatcher; the file is for the human (and for follow-up agents).
- **Mermaid for diagrams.** Project standard. The template enforces this; do not let the agent substitute ASCII or images.
