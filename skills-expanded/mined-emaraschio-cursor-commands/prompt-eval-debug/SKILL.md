---
name: prompt-eval-debug
description: >-
  Debug and improve any prompt without rewriting blindly. Builds a tiny eval
  suite (control, edge, capability-boundary cases), diagnoses failures as
  prompt issue, missing tool or capability, or harness/workflow issue, and
  proposes the smallest next change. Use for prompt debugger, eval suite, improve
  prompt, or before editing catalog eval/cases.md.
user-invocable: false
---
# Prompt eval debug

## Role

You act as a **prompt debugger** for an arbitrary prompt the user is iterating on. You help them improve it by designing a tiny eval suite, classifying failures, and suggesting the **smallest next change**, not a blind full rewrite. You do not claim this repository's CI scored their ad-hoc suite.

## When to use

Use when a prompt or skill underperforms and the user might otherwise rewrite it on vibes. For shipped commands in this catalog, stable cases eventually belong in `skill-contracts/<name>/eval/cases.md` per [EVAL_GUIDE.md](../docs/EVAL_GUIDE.md). For delegation design before autonomous work, use `define-agent-goal`. For code/runtime bugs, use `debug-issue`.

## Workflow

Run phases in order.

### Phase 0: Intake

1. Require **Prompt** (paste the prompt under test) and **Task** (what the AI should do when given that prompt).
2. If either is missing, ask one focused question for each gap before proceeding.
3. Produce a one-paragraph **summary** of what the prompt is trying to accomplish.

### Phase 1: Tiny eval suite

Produce exactly **five** cases in a table with columns: **ID**, **Type**, **Input / scenario**, **Expected behavior**, **Notes**.

| ID | Type | Requirement |
|----|------|-------------|
| **C0** | control | Should always pass when the prompt is healthy |
| **E1 to E3** | edge | Scenarios where the prompt could fail; use prior failure modes if the user supplied them |
| **B1** | capability-boundary | Agent should escalate, ask for help, or refuse (not hallucinate success) |

Cases must use concrete inputs and expected behaviors, not vague "should work."

### Phase 2: Run guidance

Tell the user to run each case against the **current** prompt (manual chat, script, or their harness). Do not execute the target prompt as production traffic unless the user explicitly asks you to run a case. Do not claim automated pass/fail scores unless the user reports results.

### Phase 3: Diagnosis

For each case (or for failures the user reports), classify the root cause as exactly one primary type:

- **prompt issue**: wording, missing instruction, wrong order, ambiguous criteria
- **missing tool or capability**: task needs a tool, MCP server, API, or skill the prompt does not provide (**instructions are not capabilities**)
- **harness / workflow issue**: wrong model, missing context, bad orchestration, eval setup bug

Fix **one failure mode** at a time in recommendations. If the user has not run cases yet, provide likely failure hypotheses per edge/boundary case.

### Phase 4: Smallest next change

Propose **one** targeted edit (sentence- or section-level), not a full rewrite. If the diagnosis is **missing tool or capability**, recommend adding a tool/MCP/skill, not more instructions pretending the model can do it without capability.

For agentic tasks, prefer **generate → evaluate → repair** loops over a single megaprompt when recommending workflow changes.

### Phase 5: Deliver

Post in chat:

1. The eval suite table
2. Diagnosis (per case or per reported failure)
3. The smallest next change to test

Note optional follow-up: re-run the suite after the change; for catalog commands, translate stable cases into `eval/cases.md` with PASS/FAIL rubrics.

## Principles

- **Instructions are not capabilities**: e.g. "calculate tax correctly" without a calculator is a **missing tool or capability** diagnosis, not fixed by louder instructions.
- Do not **rewrite blindly**. Always surface the eval suite before recommending a large rewrite.
- One failure mode per iteration.

## Safety

- Redact secrets, tokens, credentials, PII, and PHI in pasted prompts and case tables.
- Do not replace the user's entire prompt in one shot unless they explicitly request a full rewrite **after** seeing the suite and diagnoses.
- Do not conflate this workflow with Codex, Braintrust, or other product-specific eval APIs.

## Distinction from other commands

- **`define-agent-goal`**: six-part delegation Goal before autonomous work, not prompt rubric design.
- **`instruction-ablation`**: strips toward a bare baseline and rebuilds instructions from repeated in-session failures. This skill edits an **existing** pasted prompt via a tiny eval suite.
- **`debug-issue`**: application/runtime debugging, not prompt evaluation.
- **Catalog `eval/` trees**: regression contract for **shipped** commands; this skill designs **ad-hoc** cases for any prompt.

## Guardrails

- Do not rewrite blindly: surface the tiny eval suite and the smallest next change before any full rewrite, and rewrite fully only on explicit request.
- Keep the capability-boundary case; diagnose missing tool or capability instead of assuming instructions are capabilities.
- Do not claim catalog CI scored an ad-hoc suite; the user runs these cases manually.
