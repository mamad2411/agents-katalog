---
name: pystack-workflow
description: Main PyStack workflow for large-codebase feature delivery. Orchestrates PyStack Brainstorm, GStack-style review, OpenSpec change creation, Superpowers TDD, GStack QA, GStack ship, and OpenSpec archive.
---

# PyStack Workflow

Use this skill for substantial feature work in large codebases after native Superpowers, GStack, and OpenSpec are already installed and initialized.

PyStack is a workflow coordinator. It does not vendor or replace Superpowers, GStack, or OpenSpec.

## Preflight

Before running the workflow, confirm the native stack is ready:

- Superpowers is installed in the active agent/harness.
- GStack is installed and set up for the active agent.
- OpenSpec CLI is installed; `openspec --version` works.
- The current repository has been initialized with `openspec init`.
- PyStack skills were installed after those native tools.

If OpenSpec is missing, stop and ask the user to install and initialize it:

```bash
npm install -g @fission-ai/openspec@latest
openspec init
```

If Superpowers or GStack is missing, stop and ask the user to install the native tool first. Do not create `.pystack`, do not copy upstream repositories, and do not simulate the native installations.

## Default Flow

```text
pystack-brainstorm
-> pystack-review
-> pystack-openspec-change
-> pystack-tdd
-> pystack-qa
-> pystack-ship
-> pystack-archive
```

## Step 0: Decide Brainstorm

Ask whether brainstorm is needed only when the input is ambiguous.

Run brainstorm when:

- The user gives a rough feature idea.
- The feature affects multiple modules.
- Success criteria, risk, or boundaries are unclear.
- The user asks for ideation, design, or critique.

Skip brainstorm when:

- The user gives a mature document and says to start from it.
- There is already an approved OpenSpec change.
- The current task is continuing a previously approved plan.

If skipping brainstorm, record why in the workflow notes.

## Step 1: PyStack Brainstorm

Invoke `pystack-brainstorm`.

This wraps the installed native Superpowers Brainstorm capability:

```text
installed Superpowers brainstorming
```

Expected output:

```text
problem framing
scope boundary
acceptance intent
risk notes
```

## Step 2: PyStack Review

Invoke `pystack-review`.

This is a pre-OpenSpec review. It simulates the team saying whether the brainstorm output or mature document is ready to become an OpenSpec change.

The review should cover:

- Product value.
- Engineering boundaries.
- Missing risks.
- Over-complexity.
- Testability.
- Whether everyone is agreed enough to create the OpenSpec change.

## Step 3: PyStack OpenSpec Change

Invoke `pystack-openspec-change`.

Create the formal OpenSpec artifacts:

```text
openspec/changes/<change-id>/proposal.md
openspec/changes/<change-id>/design.md
openspec/changes/<change-id>/tasks.md
openspec/changes/<change-id>/specs/<capability>/spec.md
```

OpenSpec remains the only spec/change/archive source of truth.

## Step 4: PyStack TDD

Invoke `pystack-tdd`.

Use Superpowers TDD discipline for implementation:

```text
failing test
-> minimal implementation
-> passing test
-> refactor
```

## Step 5: PyStack QA

Invoke `pystack-qa`.

Use GStack-style QA. For frontend work, run browser verification. For backend or CLI work, run command-level acceptance checks.

## Step 6: PyStack Ship

Invoke `pystack-ship`.

Use GStack ship behavior for final release preparation.

## Step 7: PyStack Archive

Invoke `pystack-archive`.

Ship is not complete until OpenSpec archive is complete.

## Hard Rules

- Do not create a second source of truth.
- Do not invent Stack archive. Archive means OpenSpec archive.
- Do not create `.pystack` as a runtime bundle.
- Do not copy upstream Superpowers/OpenSpec/GStack into the project.
- PyStack wrappers coordinate native skills and commands; OpenSpec owns specs and archive.
