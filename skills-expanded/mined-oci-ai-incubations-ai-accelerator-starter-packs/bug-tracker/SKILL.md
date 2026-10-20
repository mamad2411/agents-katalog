---
name: bug-tracker
description: This skill should be used when a bug is discovered, when a bug is fixed, when the user says "log this bug", "track this bug", "add to BUGS.md", "update BUGS.md", "mark bug as fixed", "bug resolved", or when investigating a bug and wanting to check if it's been seen before.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Bash
argument-hint: [log|fix|list] [description]
---

# Bug Tracker

Track bugs discovered during development and testing in `BUGS.md` at the repo root. Maintain an ongoing list of issues found, their symptoms, root causes, and resolutions.

## Usage

- `/bug-tracker log <description>` — Log a new bug
- `/bug-tracker fix <bug-id>` — Mark a bug as fixed with resolution details
- `/bug-tracker list` — List all open bugs
- `/bug-tracker` — No args: check if the current issue matches a known bug

## File Location

`BUGS.md` at the repository root (`/Users/grantneuman/workspace/ai-accelerator-starter-packs/BUGS.md`).

## Logging a New Bug

When a bug is discovered, append an entry to `BUGS.md` using this format:

```markdown
### BUG-NNN: Short title

**Status:** Open
**Date found:** YYYY-MM-DD
**Found by:** [name or context, e.g., "Grant during integration testing"]
**Severity:** Critical | High | Medium | Low

**Symptoms:**
[What the user observed — error messages, wrong UI behavior, unexpected output]

**Root cause:**
[Technical explanation of why the bug occurs. Include file paths and line numbers.]

**Affected files:**
- `path/to/file.tf:123` — description of what's wrong

**Workaround:**
[If any temporary workaround exists, document it here. Otherwise "None".]

**Resolution:**
Pending.
```

Assign the next sequential BUG-NNN ID by reading the last entry in BUGS.md.

## Marking a Bug as Fixed

When a bug is resolved, update the existing entry:

1. Change `**Status:** Open` to `**Status:** Fixed`
2. Add `**Date fixed:** YYYY-MM-DD`
3. Update `**Resolution:**` with:
   - What was changed (with file paths and line numbers)
   - PR number if applicable (e.g., `#93`)
   - Commit hash if applicable
   - How to verify the fix

Example resolution:

```markdown
**Resolution:**
Added `cuopt_frontend_admin_username`, `cuopt_frontend_admin_password`, and `google_maps_api_key`
to `common_schema.yaml` with `visible: false`. This prevents ORM from displaying them as raw
fields in non-cuOpt categories. Fixed in PR #93, commit `e67bb3c`.

**Verification:** Regenerate schemas (`python3 create_final_schema.py --all`), check that
`grep cuopt_frontend_admin schemas/generated/enterprise_rag_aiq_schema.yaml` shows `visible: false`.
```

## Listing Open Bugs

Read `BUGS.md` and list all entries with `**Status:** Open`, showing their ID, title, severity, and date.

## Checking for Known Bugs

When investigating an issue, search `BUGS.md` for matching symptoms or affected files before logging a new entry. Avoid duplicates.

## Initializing BUGS.md

If `BUGS.md` does not exist, create it with this header:

```markdown
# Known Bugs

Ongoing list of bugs discovered during development and testing. Each entry tracks symptoms, root cause, and resolution.

| Status | ID | Title | Severity | Date |
|--------|---------|-------|----------|------|

---

```

Then add the first bug entry below the separator.

## Updating the Summary Table

After adding or updating a bug entry, update the summary table at the top of `BUGS.md` to reflect the current state. Each row:

```markdown
| Open/Fixed | BUG-NNN | Short title | Severity | YYYY-MM-DD |
```

## Severity Guide

- **Critical** — Blocks deployment or causes data loss
- **High** — Broken functionality, no workaround
- **Medium** — Broken functionality with workaround, or cosmetic issue in production-facing UI
- **Low** — Minor issue, cosmetic, or edge case
