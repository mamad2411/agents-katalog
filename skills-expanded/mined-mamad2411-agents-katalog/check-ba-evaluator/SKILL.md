---
name: check-ba-evaluator
description: Instructions for invoking a Senior PM Evaluator subagent to review BA artifacts (Architecture or Backlog).
---

Use this skill when you need to verify the quality of Business Analysis artifacts like `SYSTEM_ARCHITECTURE.md` or `.harness/features.json` before presenting them to the user.

> **Batched, single-pass review (performance).** This evaluator reviews the **whole artifact (or section) in one shot** and reports **every** finding together. Never review a fragment, fix one finding, then re-spawn for the next — each spawn is a cold subagent that re-reads the files, and per-finding round-trips are the dominant cost. The loop is: **one review → apply all fixes in a single revision pass → at most one confirmation re-review.** When several independent artifacts are ready at once (e.g. multiple `docs/spec/*` files), evaluate them in **one** subagent pass covering all of them rather than one spawn per file.

**Instructions for the Orchestrating Agent:**
To perform the evaluation, you MUST spawn a dedicated subagent using your `invoke_subagent` tool.

1. Set `Role` to: `Senior PM Evaluator`
2. Set `TypeName` to: `pm_evaluator` (or `research` if `pm_evaluator` is not registered).
3. Set `Prompt` to the following text (replace placeholders with actual file paths):

"You are a strict Senior Product Manager. Your task is to evaluate the drafted Business Analysis documents: [File Paths].
Check for the following:
1. **Completeness**: Are all core entities, business rules, and edge cases explicitly defined?
2. **RBAC**: Is there a clear Role-Based Access Control matrix?
3. **Logic**: Are there any glaring logical holes in the user journeys?
4. **Actionability**: Is it detailed enough for developers to implement without guessing?

Write a strict, detailed markdown report to `.harness/reports/ba-evaluation.md`. Your chat response must ONLY be the path to this file. Do NOT output the report text in the chat. If the documents lack depth or fail any of the above checks, FAIL them in the report and list explicitly what the main agent must ask the user or revise."

Wait for the subagent to return its report. If the subagent fails the document, apply **all** of its findings in a **single revision pass** (bundle any clarifying questions to the user into one ask-user round), then re-spawn the evaluator **at most once** to confirm before moving to the next phase. Do not fix one finding and re-review per finding. If the single confirmation still fails on substantive points, surface the remainder to the user instead of looping further.

## Mode B — Backlog coverage review (SPEC → US)

Use this mode to verify the **User-Story backlog actually covers every item in the SPECs** before it is confirmed (driven by [plan-us-backlog-generator](../plan-us-backlog-generator/SKILL.md) Step 2.5). The recurring failure it catches: a backlog generated from the high-level architecture that **misses User Stories** only defined in the detailed SPECs.

Spawn the subagent with `Role: Senior PM Evaluator` and set `Prompt` to:

"You are a strict Senior Product Manager who knows these SPECs cold. Read the detailed SPECs ([docs/spec/*.md]) and the drafted backlog (`.harness/features.json`).
Build a **coverage matrix**: every screen in the FE SPEC, every endpoint/function in the BE SPEC, every entity/migration in the DB SPEC, and every business rule in the BA → mapped to the User Story (or stories) that covers it.
List explicitly **every SPEC item that NO User Story covers** — these are the gaps. For each gap, propose the missing User Story (title, area, behavior, a verification command).
Write the coverage matrix and the gap list to `.harness/reports/backlog-coverage.md`. Your chat response must ONLY be the path to this file. If any SPEC item is uncovered, FAIL the backlog and list the missing stories the main agent must add."

Wait for the report. If it fails, add **all** of the missing User Stories in a **single pass**, then re-run this coverage review **at most once** to confirm full coverage before presenting the backlog to the user. Do not add one story and re-run the coverage review per gap — collect the full gap list from the one report and close it in a single revision.
