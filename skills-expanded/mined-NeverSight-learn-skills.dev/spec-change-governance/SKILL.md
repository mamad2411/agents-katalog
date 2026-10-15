---
name: spec-change-governance
description: Govern spec amendments without losing history, completed work, or review context. Use when the user wants to change requirements, amend a plan, update a spec in place, mark superseded items, rerun clarification or planning, or prevent spec drift during rework.
license: Apache-2.0
metadata:
  author: Mike Willbanks
  repository: https://github.com/mwillbanks/agent-skills
  homepage: https://github.com/mwillbanks/agent-skills
  bugs: https://github.com/mwillbanks/agent-skills/issues
  purpose: Amend specs in place while preserving history and forcing downstream consistency
---

# Spec Change Governance

Use this skill when a living spec needs to change without erasing the record of what already happened.

This skill exists to keep amendments honest, visible, and traceable across spec, plan, tasks, validation, and review artifacts.

## When to use

Use this skill for prompts like:

- "Update the spec without losing history"
- "Amend the plan and keep the completed tasks visible"
- "Mark the old requirement as superseded"
- "Rerun the spec workflow after a requirement change"
- "Prevent drift when the scope changes"

Use it whenever an in-flight spec changes in a way that could invalidate earlier artifacts.

## Required workflow

1. Identify the authoritative source artifacts and the exact requirements being changed.
2. Preserve the original requirement text or completed state before introducing the amendment.
3. Mark what is superseded, replaced, narrowed, or deferred instead of deleting it.
4. Carry the change through clarification, plan, tasks, validation, and review as needed.
5. Update the downstream artifacts that depend on the changed requirement.
6. Record any new assumptions or constraints created by the amendment.
7. Keep completed work visible unless the user explicitly asks to restart from scratch.

## Non-negotiable rules

- Do not silently replace the old spec with a new one.
- Do not erase completed tasks just because requirements moved.
- Do not hide a requirement change behind a casual wording tweak.
- Do not skip downstream consistency checks after an amendment.
- Do not leave contradictory artifacts in place without calling them out.
- Do not pretend the original history does not exist.

## Change discipline

- Prefer in-place amendment over replacement.
- Preserve a clear before/after record for each changed requirement.
- Treat requirement changes as triggers for revalidation.
- Surface any ambiguity introduced by the amendment instead of guessing it away.
- If the change invalidates prior artifacts, say which artifacts must be rerun or rewritten.

## Definition of done

This skill is complete only when all of the following are true:

- the changed requirement is explicit
- the superseded requirement remains visible
- downstream artifacts are updated or marked stale
- the change path is traceable and honest
- unresolved inconsistencies are called out

## Final output contract

Report all of the following:

- what changed
- what was preserved
- what was superseded
- which downstream artifacts were updated
- which artifacts still need rerun or review
- any unresolved contradictions or assumptions

If the spec cannot be amended cleanly, say what makes it unsafe to proceed.
