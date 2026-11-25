---
name: orc-coder
description: "Implement features or behavior-preserving refactors with the smallest complete change; route reported defects to orc-bugfix."
---

# Development playbooks

Use the shared orc-worker-base lifecycle. Select one playbook from the task; users
do not need a separate flow for each kind of development.

## Feature

1. Read affected code and callers. State the user-visible result, acceptance criteria,
   authoritative data shape and trust boundaries before introducing new logic.
2. For nontrivial work, record a short implementation plan in the task. Resolve
   observable questions by inspecting or running code; ask for genuine product choices.
3. Reuse the project's existing components, services and patterns. Implement in small
   verifiable units, including affected callers, exports, fixtures and stored data.
4. Test observable behavior and exercise the real interface when applicable. Verify
   error paths and security boundaries, not merely compilation or a green proxy check.

## Refactor

Identify behavior that must stay unchanged and its callers. Establish baseline checks,
then change structure in small units. Migrate affected callers in the same change;
avoid speculative compatibility layers. Prove behavior is preserved with the relevant
checks and disclose any untested paths.

## Bug fix

Load orc-bugfix. Reproduce, establish root cause, fix it once at the correct owner,
and verify a regression check fails before the fix and passes after it.

## Delivery

Follow the shared verification, knowledge review and outcome contract. Do not duplicate
status changes or Git publishing instructions here. A plan or typecheck alone does
not establish that the task is complete.
