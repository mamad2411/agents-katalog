---
name: pr-description
description: "Generate PR description from commits and diff. Args: [<base-branch>]"
argument-hint: "[<base-branch>]"
---

<!-- Note: $ARGUMENTS is substituted by Claude commands only. In Copilot,
     the user must include their argument inline in the prompt; the skill
     body sees the literal text "$ARGUMENTS" unsubstituted. -->

## Arguments

`[<base-branch>]`

- Optional. The branch to diff against; defaults to `main`.
- **Examples**: `/pr-description`, `/pr-description develop`

> Copilot CLI note: `$ARGUMENTS` does not substitute in skills; include the argument inline in your prompt.

Generate a pull request description for the current branch.

Base branch from $ARGUMENTS (default: "main").

Steps:
1. Get branch name: `git branch --show-current`
2. Get commit list: `git log <base-branch>..HEAD --pretty=format:"- %s" --no-merges`
3. Get changed files: `git diff <base-branch>..HEAD --name-status`
4. Get diff summary: `git diff <base-branch>..HEAD --stat`

Format output as:

---
## Summary
<1-2 sentence description of what this PR does and why>

## Changes
<bullet list from commits, grouped by area if possible>

## Files Changed
<list from diff --name-status, grouped by type: Added / Modified / Deleted>

## How to test
1. <step 1>
2. <step 2>

## Notes
<any breaking changes, dependencies, or deploy considerations>
---

Infer testing steps using this routing table: first match wins, list the matching steps in `## How to test`:

| Changed file shape | Test step to include |
|---|---|
| `*.test.*` / `*.spec.*` / `tests/**` only | "Run `<project test command>`: added/updated tests cover the change." |
| API route file (e.g., `routes/`, `controllers/`, `*Controller.*`, `app.py` Flask routes) | "Hit the endpoint with curl/Postman: `curl <method> <url>`: expect `<status>` and `<body shape>`." |
| Database migration | "Run the migration on a dev DB, then run the reverse, then re-run forward. Confirm schema matches `<file>`." |
| UI component (`.vue`, `.tsx`, `.jsx`) | "Open the affected view in the running app (`<dev command>`), exercise the changed interaction, confirm `<expected visible result>`." |
| Config / build / CI file | "Re-run the affected pipeline locally (e.g., `npm run build`, `./scripts/check.sh`): confirm no new warnings or failures." |
| Docs-only (`.md`, `.rst`, `docs/**`) | "Read for clarity; no functional test needed." |
| Mix of the above | List one step per category, in the order above. |

If no step applies, write "Manual smoke-test recommended: exercise the changed area in the running app." rather than fabricating a procedure.

**Exclude from `## Files Changed`:**
- Lockfiles (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, `poetry.lock`, `Gemfile.lock`, `go.sum`), unless the PR stated purpose is a dependency upgrade.
- Generated files matching `dist/`, `build/`, `*.min.*`, `coverage/`.
- The auto-generated `CHANGELOG.md` if the PR uses semantic-release or similar.

If excluded files are >5% of the diff line count, note in `## Notes`: "Lockfile/generated delta: N files, ~M lines: excluded from review surface."

Do not narrate steps. Output only the formatted PR description.
