---
skill_id: spec_driven_spec_edit
name: spec-driven-spec-edit
description: Create or modify individual main spec files under .spec-driven/specs/ directly, without going through the change workflow. For quick corrections, typo fixes, and adding missing spec entries.
author: auto-spec-driven
type: agent_skill
version: 1.0.0
---

You are helping the user create or modify main spec files under
`.spec-driven/specs/` directly, without going through the change workflow.
This is for lightweight corrections — fixing typos, correcting inaccurate
requirements, or adding missing spec entries.

## Prerequisites

The `.spec-driven/` directory must exist at the **project root**. Before
proceeding, verify:
```
ls .spec-driven/
```
If this fails, the project is not initialized. Run `/spec-driven-init` first.

## Steps

1. **Read spec context first** — before making any changes, read:
   - `.spec-driven/config.yaml`
   - `.spec-driven/specs/INDEX.md`
   - any existing main spec files relevant to the user's request

2. **Understand the request** — identify whether the user wants to:
   - add a new spec file or category
   - add new requirements to an existing spec file
   - modify an existing requirement
   - remove one or more existing requirements

3. **Choose the target** — use `INDEX.md` to determine where the content
   belongs:
   - If one or more existing spec files cover the behavior, use those
   - Only create a new spec file if no existing file fits
   - Only create a new category if no existing category fits

4. **Prepare the changes** — draft the exact modifications:
   - For additions: write the new `### Requirement:` heading and body
   - For modifications: show the before and after content
   - For removals: identify the exact `### Requirement:` heading(s) to remove
   - Describe observable behavior only, not implementation details

5. **Present and confirm** — show the user:
   - which file or files will be changed
   - the exact content that will be added, modified, or removed
   - whether `INDEX.md` needs updating

   **Wait for explicit user confirmation before writing anything.**

6. **Apply the changes** — after confirmation:
   - Edit the target spec file(s) under `.spec-driven/specs/`
   - If a new file or category was created, update `.spec-driven/specs/INDEX.md`
   - For removals, delete the exact `### Requirement:` heading(s) cleanly — do
     not leave orphaned headings or vague remnants

7. **Validate the result** — after editing, verify:
   - Each edited file still follows the standard `### Requirement:` heading
     format
   - `INDEX.md` correctly reflects all spec files under `.spec-driven/specs/`
   - If format issues are found, fix them immediately

8. **Summarize** — tell the user:
   - which file(s) were changed
   - what was added, modified, or removed
   - whether INDEX.md was updated

## Rules

- Always read existing specs before editing — never edit blind
- Present changes and wait for confirmation before writing
- Prefer existing categories and files unless the content clearly requires a
  new path
- Describe observable behavior only, not implementation details
- Do not implement product code — this skill edits planning artifacts only
- Do not create or interact with `.spec-driven/changes/`
