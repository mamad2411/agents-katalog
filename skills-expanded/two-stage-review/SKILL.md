---
name: two-stage-review
description: Auto-dispatches spec compliance and code quality review subagents after any builder completes a task during Director/Builder workflows. Enforces ordered two-stage review (spec first, then quality), manages fix-and-re-review loops, and escalates when loops exceed 3 iterations.
slug: two-stage-review
category: operations
complexity: complex
version: "1.0.0"
author: "id8Labs"
triggers:
  - "two-stage-review"
  - "two stage review"
  - "review builder output"
  - "post-builder review"
tags:
  - development
  - director-builder
  - code-review
  - quality-assurance
---

# Two-Stage Review

Automated post-builder review gate for Director/Builder workflows. After any builder (Codex, subagent, or manual) reports completion, this skill dispatches two sequential review subagents: spec compliance first, then code quality. No task moves to "completed" without both passing.

## When to Use

- After ANY builder reports DONE or DONE_WITH_CONCERNS during a Director/Builder workflow
- After ANY builder reports DONE or DONE_WITH_CONCERNS during a Ralph Loop build phase
- When manually reviewing code that was written to a specification
- Never skip this process — it is mandatory for all Director/Builder task completions

## Prerequisites

Before invoking this review:
1. Builder has reported status: DONE or DONE_WITH_CONCERNS
2. The original task requirements are available (from IMPLEMENTATION_PLAN.md or task description)
3. The builder's completion report is available (what they claim they built)
4. Files modified by the builder are known

## Builder Status Handling

Handle builder status BEFORE dispatching reviews:

| Status | Action |
|--------|--------|
| **DONE** | Proceed directly to Stage 1 (Spec Compliance Review) |
| **DONE_WITH_CONCERNS** | Read concerns first. If correctness/scope issue: address before review. If observation only: note and proceed to Stage 1 |
| **NEEDS_CONTEXT** | Do NOT review. Provide missing context to builder, re-dispatch builder. Review only after builder returns DONE/DONE_WITH_CONCERNS |
| **BLOCKED** | Do NOT review. Assess blocker: context problem -> re-dispatch with more context. Reasoning limit -> re-dispatch with more capable model. Task too large -> break into pieces. Plan wrong -> escalate to human |

## Review Process

### Stage 1: Spec Compliance Review (MUST pass before Stage 2)

Dispatch a subagent with the following prompt template. Fill in the bracketed sections with actual task context.

```
Agent tool (general-purpose):
  description: "Spec compliance: Task {TASK_NUMBER} — {TASK_NAME}"
  prompt: |
    You are reviewing whether an implementation matches its specification.

    ## What Was Requested
    {FULL task requirements from IMPLEMENTATION_PLAN.md or task description.
     Include every requirement, acceptance criterion, and constraint.
     Copy the exact text — do not summarize or paraphrase.}

    ## What Builder Claims They Built
    {Paste the builder's completion report verbatim.
     Include any file paths, status, and notes they provided.}

    ## Files to Review
    {List every file the builder created or modified, with full paths.}

    ## CRITICAL: Do Not Trust the Report
    The builder's report may be incomplete or optimistic. Verify independently.

    DO NOT: Take their word, trust claims about completeness, accept their interpretation.
    DO: Read actual code, compare to requirements line by line, check for missing/extra work.

    ## Your Job
    Read the implementation code and verify:
    - Missing requirements? (skipped, missed, claimed but not implemented)
    - Extra/unneeded work? (over-engineered, unnecessary features, scope creep)
    - Misunderstandings? (wrong interpretation, wrong problem solved)

    For each requirement in the spec, state whether it is:
    - IMPLEMENTED: found at [file:line]
    - MISSING: not found in code
    - PARTIAL: partially implemented, missing [specifics]
    - EXTRA: not in spec, found at [file:line]

    ## Report Format
    Respond with EXACTLY one of:

    SPEC_COMPLIANT: YES
    Summary: [1-2 sentence confirmation]

    — OR —

    SPEC_COMPLIANT: NO
    Issues:
    - [MISSING/PARTIAL/EXTRA]: [description] — [file:line reference]
    - ...
    Fixes needed:
    - [Specific action the builder must take]
    - ...
```

**On SPEC_COMPLIANT: YES** -> Proceed to Stage 2 (Code Quality Review).

**On SPEC_COMPLIANT: NO** -> Enter fix loop (see Review Fix Loop below). Do NOT proceed to Stage 2.

### Stage 2: Code Quality Review (ONLY after Stage 1 passes)

Dispatch a subagent with the following prompt template. Only invoke this AFTER spec compliance has returned SPEC_COMPLIANT: YES.

```
Agent tool (general-purpose):
  description: "Quality review: Task {TASK_NUMBER} — {TASK_NAME}"
  prompt: |
    You are reviewing code quality for a task that has already passed spec compliance.
    The code does what it should — now verify it is well-built.

    ## What Was Implemented
    {Paste the builder's completion report.
     Include file paths and a brief description of what was built.}

    ## Files to Review
    {List every file the builder created or modified, with full paths.}

    ## Project Patterns
    {Include relevant existing patterns from the codebase:
     - Import conventions
     - File naming conventions
     - Component structure patterns
     - Testing patterns
     - Error handling patterns}

    ## Your Job
    Review for:
    1. Clean, maintainable code — readable names, clear logic flow
    2. Single responsibility — each file has one clear purpose with well-defined interface
    3. Tests verify behavior — not just mock behavior, meaningful assertions
    4. Follows existing codebase patterns — conventions, naming, structure
    5. No unnecessary complexity — YAGNI, no premature abstraction
    6. No large files — no new files over ~300 lines, no significant growth of existing files
    7. No hardcoded values that should be configurable
    8. Error handling is present and meaningful
    9. TypeScript types are correct and specific (no `any` unless justified)

    ## Report Format
    Respond with EXACTLY one of:

    QUALITY_APPROVED: YES
    Strengths: [1-2 brief positives]
    Notes: [Optional minor suggestions that do NOT block approval]

    — OR —

    QUALITY_APPROVED: NO
    Issues:
    - [CRITICAL/IMPORTANT/MINOR]: [description] — [file:line reference]
    - ...
    Fixes needed:
    - [Specific action the builder must take]
    - ...

    Only CRITICAL and IMPORTANT issues block approval.
    MINOR issues are noted but do not require fixes before approval.
```

**On QUALITY_APPROVED: YES** -> Review complete. Director integrates, verifies build/tests, marks task completed.

**On QUALITY_APPROVED: NO** -> Enter fix loop (see Review Fix Loop below).

## Review Fix Loop

When either reviewer finds issues:

```
LOOP (max 3 iterations per stage):

  1. Collect issues from reviewer report
  2. Re-dispatch the SAME builder that wrote the code (preserves context)
     - Include the reviewer's issue list verbatim
     - Include the specific fixes needed
     - Prompt: "Fix these review issues. Do not change anything else."
  3. Builder fixes and reports status
  4. Handle builder status (same rules as above)
  5. Re-dispatch the SAME reviewer (spec or quality) to re-review
     - Include original requirements
     - Include fix history: "Iteration N — previously found: [issues]. Builder claims fixed."
  6. If reviewer approves -> exit loop, proceed to next stage (or complete)
  7. If reviewer finds issues -> increment iteration counter, go to step 1

  IF iteration counter > 3 for the same stage:
    - STOP the review loop
    - Surface warning to Director:
      "WARNING: Review loop exceeded 3 iterations on {STAGE_NAME} for Task {TASK_NUMBER}.
       Recurring issues: {list issues that keep failing}
       Recommendation: Director should inspect directly or escalate to human."
    - Do NOT auto-approve. Do NOT continue to next stage.
    - Director decides: fix directly, re-scope the task, or escalate to human.
```

### Fix Loop Builder Prompt Template

```
TASK: Fix review issues for {TASK_NAME}
TASK_ID: {TASK_ID}
REVIEW_STAGE: {Spec Compliance | Code Quality}
ITERATION: {N} of 3 max

## Issues Found by Reviewer
{Paste reviewer's issue list verbatim, including file:line references}

## Fixes Needed
{Paste reviewer's "Fixes needed" list verbatim}

## Rules
- Fix ONLY the listed issues. Do not refactor other code.
- Do not add features or change behavior beyond what the fix requires.
- Self-review your fixes before reporting back.
- Report status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
```

## Ordering Rules (STRICT)

1. Builder completes task -> handle builder status
2. Spec compliance review MUST run first
3. Spec compliance MUST pass (SPEC_COMPLIANT: YES) before code quality review starts
4. Code quality review runs second
5. Code quality MUST pass (QUALITY_APPROVED: YES) before task is marked completed
6. Never skip either review stage
7. Never start code quality while spec compliance is failing
8. Never mark a task completed without both stages passing

## Escalation Rules

| Condition | Action |
|-----------|--------|
| Spec compliance loop > 3 iterations | Pause. Surface warning. Director inspects or escalates to human |
| Code quality loop > 3 iterations | Pause. Surface warning. Director inspects or escalates to human |
| Builder returns BLOCKED during fix loop | Pause. Director assesses blocker |
| Builder returns NEEDS_CONTEXT during fix loop | Director provides context, re-dispatch builder |
| Same issue fails across multiple iterations | Flag as recurring in warning. Likely architectural problem |
| 2 builder failures on same task (across all loops) | Claude/Director takes over implementation directly |

## Communication Signals

Emit these signals during the review process so the user and logs can track progress:

```
"Spec review: dispatching for Task {N}..."
"Spec review: PASSED" or "Spec review: FAILED — {count} issues found"
"Spec review: fix loop iteration {N}/3"
"Spec review: PASSED after {N} fix iterations"

"Quality review: dispatching for Task {N}..."
"Quality review: APPROVED" or "Quality review: FAILED — {count} issues ({critical} critical, {important} important)"
"Quality review: fix loop iteration {N}/3"
"Quality review: APPROVED after {N} fix iterations"

"WARNING: Review loop exceeded 3 iterations on {stage} for Task {N}"
"Two-stage review: COMPLETE for Task {N} — both stages passed"
```

## Integration with Director/Builder Workflow

This skill plugs into step 4 of the Director/Builder build iteration:

```
1. Claude reads state
2. Claude creates builder prompt
3. Builder implements -> reports status
4. >>> TWO-STAGE REVIEW (this skill) <<<
   4a. Handle builder status
   4b. Spec compliance review (with fix loop if needed)
   4c. Code quality review (with fix loop if needed)
5. Claude integrates & verifies (build, typecheck, tests)
6. Claude marks task completed
7. Claude updates state
```

After this skill completes successfully (both stages passed), the Director proceeds to integration and verification. The task is NOT marked completed until the Director also confirms build/typecheck/tests pass.

## Quick Reference

```
Builder DONE/DONE_WITH_CONCERNS
        |
        v
  [Handle Status]
        |
        v
  [STAGE 1: Spec Compliance]
        |
    YES |          NO
        |    .-----------.
        |    | Fix Loop   |
        |    | (max 3)    |
        |    '-----------'
        |          |
        |     Still NO after 3?
        |          |
        |      ESCALATE
        v
  [STAGE 2: Code Quality]
        |
    YES |          NO
        |    .-----------.
        |    | Fix Loop   |
        |    | (max 3)    |
        |    '-----------'
        |          |
        |     Still NO after 3?
        |          |
        |      ESCALATE
        v
  [REVIEW COMPLETE]
        |
        v
  Director integrates & verifies
```
