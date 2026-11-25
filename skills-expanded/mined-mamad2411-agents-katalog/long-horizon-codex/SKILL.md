---
name: long-horizon-codex
description: Structure and run multi-hour Codex work with four control-plane documents.
---

# Long Horizon Codex

## Overview

Use a persistent set of working documents to keep large Codex tasks coherent across long runtimes, context compaction, and handoff. Treat the four files as the operating surface for the task, not as optional notes.

## Quick Start

1. Check whether `prompt.md`, `plans.md`, `implement.md`, and `documentation.md` already exist in the target repo.
2. If they do not exist, or are clearly stale, scaffold them with:

```bash
python /path/to/long-horizon-codex/scripts/bootstrap_long_horizon_docs.py \
  --output-dir /path/to/repo \
  --project-name "Project Name" \
  --objective "What Codex must deliver"
```

3. Fill the files before major implementation begins. `plans.md` must exist and be coherent before broad coding work starts.
4. Execute milestone by milestone from `plans.md`.
5. Keep `plans.md` and `documentation.md` current as reality changes.

## File Contract

### `prompt.md`

Write the initial mission brief here. This file should push Codex into the right operating mode.

- Define the role Codex should take.
- State the core goals and hard requirements.
- Define the deliverable clearly.
- Include the concrete product or implementation spec.
- End with an explicit process directive that says planning comes before coding.

Use an ambitious, concrete, and procedural tone. Use direct imperatives such as `Start now.` and `Do NOT start coding until plans.md exists and is coherent.`

### `plans.md`

Treat this as the source of truth for execution.

- Include a verification checklist that stays current.
- Break the work into milestones with:
  - scope
  - key files or modules
  - acceptance criteria
  - verification commands
- Add a risk register with mitigations.
- Add a demo or acceptance flow if the work is user-facing.
- Add an architecture or approach overview when design choices matter.
- Append implementation notes and decisions as the project evolves.

Prefer more milestones than you think you need. The point is to create durable checkpoints and validation gates.

### `implement.md`

Use this as the execution contract. It should remove hesitation and define how Codex proceeds.

- State that Codex should not stop after each milestone to ask for confirmation.
- State that `plans.md` is authoritative.
- Require validation after every milestone.
- Require failing tests before bug fixes when practical.
- Require documentation updates as the implementation becomes real.
- Define concrete completion criteria.

This file is where you put the "keep going until the whole thing is actually done" wording.

### `documentation.md`

Use this as the operator-facing runbook. Keep it concise and factual.

- Explain what the project is.
- Provide local setup and one-command start instructions.
- List verification commands.
- Record demo recipes.
- Summarize repo structure.
- Describe the high-level file or data format when relevant.
- Keep a troubleshooting section current.

Update it continuously so it matches the current state of the repo rather than the intended state.

## Operating Rules

### Before implementation

- Write or refresh the four files first.
- Make sure `plans.md` is specific enough that another agent could resume from it.
- Record assumptions and tradeoffs up front if they will shape the implementation.

### During implementation

- Work from `plans.md`, not from memory.
- Update the verification checklist every time a meaningful milestone is completed.
- Record decisions in `plans.md` as they are made, especially when reality differs from the original plan.
- Keep `documentation.md` aligned with shipped behavior.
- If the task spans multiple sessions, re-read the four files before resuming work.

### After implementation

- Make sure all milestone boxes reflect reality.
- Run the final validation sweep listed in `plans.md`.
- Tighten `documentation.md` so a human operator can run, verify, and demo the project without reading the whole codebase.

## Resources

- Read [references/pattern.md](references/pattern.md) for the operating pattern and the rationale for each file.
- Use the templates in `assets/templates/` when you want the GitHub example shape without copying a specific product spec.
- Use `scripts/bootstrap_long_horizon_docs.py` to materialize the four files into a target repo quickly.
