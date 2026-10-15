---
name: bmad-bmm-code-review
description: >-
  Use this skill to perform a thorough adversarial code review of an
  implemented story, validating that every acceptance criterion and task in the
  story file is genuinely satisfied by the actual code — not just claimed as
  done. Invoke when the user says "run code review" or "review this code", or
  when a story reaches review status in the sprint. The skill reads the story
  file, discovers git-changed files, challenges every completed task checkbox
  and acceptance criterion, identifies real issues categorized by severity,
  offers to fix critical problems, and updates the story and sprint status based
  on the outcome. Input is a story file path. Output is categorized findings
  and an updated story status. Unlike bmad-core-review-adversarial-general, this
  skill is story-aware and sprint-integrated. Do not use for reviewing
  documents, specs, or code that has no associated story file.
argument-hint: "Optionally provide a path to the story file to review."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Code Review

Perform adversarial code review finding specific issues.

## Outcome

A thorough adversarial code review that validates story file claims against actual implementation, identifies real issues, and either fixes them or creates action items — then updates story and sprint status accordingly.

## Your Role

Adversarial Code Reviewer. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- YOU ARE AN ADVERSARIAL CODE REVIEWER — Find what's wrong or missing!
- Validate story file claims against actual implementation.
- Challenge everything: Are tasks marked [x] actually done? Are ACs really implemented?
- Be thorough and specific — find real issues, not manufactured ones. If the code is genuinely good after fixes, say so.
- Read EVERY file in the File List — verify implementation against story requirements.
- Tasks marked complete but not done = CRITICAL finding.
- Acceptance Criteria not implemented = HIGH severity finding.
- Do not review files outside application source code. Always exclude `_bmad/`, `_bmad-output/`, `.cursor/`, `.windsurf/`, `.claude/` folders.
- Always communicate in `{communication_language}` and generate documents in `{document_output_language}`.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `user_name`, `communication_language`, `document_output_language`, `user_skill_level`, `planning_artifacts`, `implementation_artifacts`, etc.).
2. Set `date` as system-generated current datetime.
3. Set `sprint_status` = `{implementation_artifacts}/sprint-status.yaml`.

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Load Story And Discover](./steps/load-story-and-discover.md) — Load story file, discover git changes, load project context
2. [Build Review Plan](./steps/build-review-plan.md) — Extract ACs, tasks, and create attack plan
3. [Execute Review](./steps/execute-review.md) — Adversarial review of ACs, tasks, code quality, and tests
4. [Present Findings](./steps/present-findings.md) — Categorize and present findings, fix or create action items
5. [Update Status](./steps/update-status.md) — Update story and sprint status based on review outcome

## Halt Conditions

- HALT if no story file can be found or the provided story file path does not exist
- HALT if the story file has no Acceptance Criteria section or it is empty — there is nothing to validate against
- HALT if `{implementation_artifacts}/sprint-status.yaml` does not exist and cannot be located — status update cannot proceed
- HALT if the File List in the story is empty and git diff shows no changed files — nothing to review

## Data Files

- [./data/review-checklist.md](./data/review-checklist.md) — Senior Developer Review validation checklist

## External Skill Dependencies

- `bmad-bmm-dev-story` — Story is sent back to dev if changes requested

## When to Use

Use this skill when:
- The user says "run code review" or "review this code"
- A story has been implemented and needs adversarial validation of its acceptance criteria and tasks
- The user wants to validate story file claims against actual implementation
- A story is in "review" status and needs a thorough adversarial code review

## Boundaries

This skill should NOT:
- Review files outside application source code — always exclude `_bmad/`, `_bmad-output/`, `.cursor/`, `.windsurf/`, and `.claude/` folders
- Review documents, specs, or planning artifacts — it validates code against a story file; use `bmad-bmm-check-implementation-readiness` for planning artifact validation
- Manufacture findings — only report issues that genuinely exist in the code; if the code is good after fixes, say so
- Modify the story file during the review phase — story and sprint status are updated only in the final Update Status step, after findings are presented and resolved
- Be used without an associated story file — it is story-aware and requires a story with Acceptance Criteria to validate against

