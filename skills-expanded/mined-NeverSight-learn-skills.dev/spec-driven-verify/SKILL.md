---
name: spec-driven-verify
description: Verify a spec-driven change is complete and correctly implemented. Checks task completion, implementation evidence, and spec alignment.
version: 0.1.0
---

You are helping the user verify a spec-driven change before archiving.

## Steps

1. **Select the change** — run `node {{SKILL_DIR}}/scripts/spec-driven.js modify` to list active changes. Ask which change to verify. If already specified, use it.

2. **Format check** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js verify <name>
   ```
   Report any errors (blocking) or warnings (non-blocking).

3. **Task completion check** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js apply <name>
   ```
   If `remaining > 0`, list the incomplete tasks. These are CRITICAL issues.
   If the script warns about a missing `## Testing` section, this is also a CRITICAL — every change must include test tasks.

4. **Open questions check** — read `.spec-driven/changes/<name>/questions.md` and scan for `- [ ] Q:` entries:
   - Any open (unanswered) question is a CRITICAL — implementation cannot be verified with unresolved ambiguity
   - The script also reports these as errors; treat them as CRITICALs here

6. **Implementation evidence check** — for each completed task in tasks.md:
   - Identify what code or files the task should have changed
   - Verify the change actually exists (read relevant files)
   - Note any tasks with no visible evidence as WARNINGs

7. **Spec alignment check** — read `.spec-driven/specs/`, `.spec-driven/config.yaml`, `.spec-driven/changes/<name>/proposal.md`, and all files in `.spec-driven/changes/<name>/specs/`:
   - Does the implementation match what was proposed?
   - Do the delta files in `changes/<name>/specs/` accurately describe what was implemented? Empty `specs/` with real behavior changes is a CRITICAL.
   - Does each delta file mirror its corresponding main spec file path? Mismatched paths mean the merge will fail.
   - Do the delta files use the standard format (`### Requirement: <name>`, RFC 2119 keywords, `#### Scenario:` blocks)? Non-conforming format is a CRITICAL — the spec format is mandatory.
   - If config.yaml has a `rules` field (including any `fileMatch` entries), check whether the implementation and artifacts comply — violations are WARNINGs
   - If proposal.md has an **Unchanged Behavior** section with content, verify the implementation has not violated any listed behaviors — violations are CRITICALs
   - Flag misalignments as WARNINGs or CRITICALs

8. **Output a tiered report**:
   ```
   CRITICAL (blocks archive):
     - [list or "none"]

   WARNING (should address):
     - [list or "none"]

   SUGGESTION (optional improvements):
     - [list or "none"]
   ```

9. **Recommend next step**:
   - If CRITICAL issues: address them before archiving
   - If only WARNINGs: ask user if they want to address them or proceed
   - If clean: suggest `/spec-driven-review <name>`

## Rules
- Be honest — don't pass a change just because tasks are checked off
- CRITICALs are things that would make the change incorrect or incomplete
- WARNINGs are things that reduce confidence but don't necessarily block
- SUGGESTIONs are optional quality improvements
