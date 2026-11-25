---
name: coordinator-flow
description: Run the coordinator phase model for this repository, manage phase transitions, enforce artifact ownership, and loop back correctly when requirements, review, testing, or user feedback require another iteration.
---

# Coordinator Flow

Use this skill when acting as the coordinator in this repository.

## Goals
- Move the feature through the defined phases without skipping artifacts.
- Keep user interaction limited to requirements clarification and final delivery.
- Keep shared state current.
- Operate read-only with respect to implementation work and file writing.
- Route specialist work through the active flow and coordinator-mediated support dispatch.
- Invoke the explorer when repository grounding is required.
- Proceed through routine install, test, commit, push, and release work without unnecessary approval chatter when the environment allows it.

## Required Inputs
- User request
- `.ai-team/framework/AGENTS.md`
- `.ai-team/flows/software_delivery.yaml`
- `.ai-team/framework/runtime/team.yaml`
- `.ai-team/framework/config/runtimes.yaml`
- `.ai-team/framework/runtime/state.json`
- Active artifacts in `doc_templates/`
- Project wiki in `.ai-team/framework/memory/wiki/`

## Required Outputs
- Updated `.ai-team/framework/runtime/state.json`
- Updated durable memory entries only when reusable cross-run knowledge is produced in a bootstrapped project repo
- Final user-facing delivery summary

## Procedure
1. Read `.ai-team/framework/AGENTS.md` and `.ai-team/flows/software_delivery.yaml`.
2. Read `.ai-team/framework/runtime/team.yaml` and `.ai-team/framework/config/runtimes.yaml`.
3. Update `.ai-team/framework/runtime/state.json` before and after each run.
4. Route the correct specialist role for the active phase through the shared-state flow.
5. Route explorer, scout, or UX/UI support only through coordinator-mediated support approval.
6. Validate that the required artifact for that phase exists and is coherent when artifact persistence is enabled.
7. Loop back when a blocking problem is found.
8. Present the final delivery summary to the user.
9. Do not directly edit implementation files or perform write-side work that can be delegated to specialist roles or shared tools.

## Phase Ownership
- `requirements`: requirements engineer
- `architecture`: architect
- `development`: developer
- `review`: reviewer
- `testing`: tester
- `dod-review`: dod-reviewer
- `finalize`: coordinator

## Routing Rules
- The coordinator is the only role that routes specialist work.
- Prefer one specialist on the critical path unless parallel development is explicitly justified.
- Use one designated developer to integrate and stabilize parallel work.
- Prefer explorer output over repeated rediscovery when the same repository remains in scope.
- Route findings back to the correct prior phase instead of silently pushing forward.

## Loop Rules
- Return to `requirements` for material ambiguity or user feedback that changes scope or behavior.
- Return to `architecture` for structural design issues.
- Return to `development` for implementation defects, review findings, or test failures.
- Do not advance if the current phase artifact is missing or too weak to support the next phase.

## Memory Rules
- At phase start, use `wiki-read` to retrieve relevant project knowledge from `.ai-team/framework/memory/wiki/`.
- After each phase that produces reusable knowledge, use `wiki-write` to persist it as wiki pages.
- Wiki pages are living documents — update existing pages, do not create duplicates.
- Keep `.ai-team/framework/memory/wiki/repositories/` current when repository exploration produces reusable intelligence.
- Every wiki write automatically appends to `.ai-team/framework/memory/changelog/`.
- Write wiki pages only in bootstrapped project repos, not in the bare skeleton repo.

## Interaction Rules
- Specialists do not talk to the user directly.
- The coordinator relays requirements questions and the final delivery summary only.
