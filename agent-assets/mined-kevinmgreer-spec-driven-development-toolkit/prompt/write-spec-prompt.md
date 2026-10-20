---
description: "Generate a change folder — proposal, delta feature, delta rules, and tasks — from requirements or a user story. Creates specs/changes/<name>/ describing what changes relative to the capability."
agent: agent
tools: [read, edit, search]
argument-hint: "Describe the feature or paste requirements / user story"
---

Write a complete change spec for the following feature or requirement:

${input}

Use the **spec-writer** subagent if available; otherwise follow the steps below directly.

A change never edits a capability file directly. It writes a **delta** describing what changes;
Phase 7 merges that delta into the capability once the work is done and verified.

## Steps

1. **Read `docs/project-profile.md` — mandatory.** Note the public API style, error format,
   naming conventions, and domain vocabulary. If the profile does not exist, **stop** and run
   `/analyze-project` first — specs that don't match repo vocabulary cause drift.

2. **Identify the capability.** List `specs/capabilities/` and pick the domain this change
   modifies.
   - If it modifies more than one, that is usually two changes — split them unless they
     genuinely must ship together.
   - If none fits, this change **creates** a capability. Say so in `proposal.md`; every delta
     scenario will be `@added`.

3. **Read the capability in full** — `specs/capabilities/<domain>/behavior.feature` and
   `rules.md`. You cannot write a correct `@modified:` or `@removed:` tag without knowing the
   exact scenario names that exist. Skip only when creating a new capability.

4. Search the codebase for relevant domain terms, existing entities, and naming conventions.

5. **Create the change folder** `specs/changes/<kebab-case-name>/` containing:

   **`proposal.md`** — why, what changes, in scope, out of scope, capability impact.
   Template: `docs/atdd/templates/proposal.template.md`.

   **`delta.feature`** — only the scenarios this change touches, each carrying exactly one delta
   tag. Grammar and rules: `docs/atdd/gherkin.md` § Delta Tags. Template:
   `docs/atdd/templates/delta.template.feature`.

   Two rules that block the archive if broken, so get them right here:
   - A `@modified:` must carry **every `Then` step the capability already has** for that scenario.
     Dropping one removes a guarantee — that is a `@removed:`, and needs the user's explicit
     agreement before you propose it.
   - `@smoke` is capped at **one per capability**. If the capability already has one, do not add
     another.

   **`delta-rules.md`** — only the rules this change adds, alters, or removes, grouped under
   ADDED / MODIFIED / REMOVED, keeping the capability's existing numbering. A rule that accepts
   more than before is a relaxation: put it under REMOVED, not MODIFIED.
   Template: `docs/atdd/templates/delta-rules.template.md`.

   **`tasks.md`** — the implementation checklist.
   Template: `docs/atdd/templates/tasks.template.md`.

Follow `docs/atdd/gherkin.md` § Delta Tags and `docs/atdd/spec-writing.md`.

## Approval

After creating the change folder, present it to the user and ask:
_"Does this delta look correct? Any changes before I proceed?"_

Show the delta scenarios grouped by operation so the reviewer sees the shape of the change at a
glance — what is being added, what is being altered, and anything being removed.

**Do not generate tests or implementation code.** The delta must be explicitly approved before
the next phase begins. If the user requests changes, update and re-present until approved.

Report: change folder path, capability targeted (or "new capability"), scenario count by delta
operation and by priority tag, rule deltas by operation, and any assumptions made.
