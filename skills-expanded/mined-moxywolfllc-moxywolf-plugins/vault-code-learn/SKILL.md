---
name: vault-code-learn
description: This skill should be used when Dorian says "learn this code", "code-learn", "/code-learn", "read the repo", "extract code patterns", "study our code", "what's the code style here", or any request to inspect a MoxyWolf repo and durably persist what was learned into the MoxyWolf Vault's Code Patterns folder. Also triggered automatically by /session-start for the active project's GitHub repos. Reads source files in `~/GitHub/<repo>/`, extracts a durable pattern digest (tech stack, naming, error handling, tests, lint/type rules, file layout, frequent imports), and writes one digest per repo to `MoxyWolf Vault/_Shared Knowledge/Code Patterns/<repo>.md`. Incremental — only re-reads files modified since the digest's `last-learned:` frontmatter timestamp.
---

# vault-code-learn — Code Patterns Extraction into the MoxyWolf Vault

The MoxyWolf knowledge layer already captures decisions, research, insights, and meeting notes. What it does not yet capture is **how the team actually writes code**. This skill closes that gap. It reads a repo and writes a per-repo digest the team's future Claude sessions can consult before producing new code, so the suggestions match existing patterns instead of generic boilerplate.

The digest is small, opinionated, and human-readable. It is not a code dump.

---

## Step 0: Locate the vault and the GitHub root

Use the same resolution rules as `obsidian-update` and `session-start`:

1. `${VAULT}` — first directory under `/sessions/*/mnt/` containing `CLAUDE.md` with MoxyWolf Vault markers, or fall through to `/sessions/*/mnt/*MoxyWolf Vault/`, or to the Google Drive REST helper. Standard path on the user's Mac is `/Users/doriancougias/Library/CloudStorage/GoogleDrive-dorianc@moxywolf.com/Shared drives/MoxyWolf Shared Files/MoxyWolf Vault`.
2. `${GH_ROOT}` — `~/GitHub/` on the Mac. In sandboxed Cowork sessions, the `GitHub` root is mounted under `/sessions/*/mnt/GitHub/`.

Ensure `${VAULT}/_Shared Knowledge/Code Patterns/` exists; create it if missing. Read `${VAULT}/CLAUDE.md` once so the digest's frontmatter and tags conform to the vault's conventions.

---

## Step 1: Resolve which repo(s) to learn from

| Invocation | Repo set |
|---|---|
| `/code-learn <name>` | `${GH_ROOT}/<name>` only. If the folder doesn't exist, abort with the path checked. |
| `/code-learn --project <slug>` | Read `Taskade/<project>/00 – Project Hub/cowork-project-instructions.md` (or the vault mirror), parse the GitHub repos list, learn from each. |
| `/code-learn --all` | Every immediate subdirectory of `${GH_ROOT}` that contains a `.git` directory. Warn if more than 5 repos. |
| `/code-learn` (no args) | Auto-detect from the launch directory: if launched from `${GH_ROOT}/<repo>/...` use that one repo; else fall back to the most recently active project (same rule `/session-start` uses) and learn from its repos. |

Auto-invocation from `/session-start` passes the project slug and uses the `--project` path.

---

## Step 2: Compute the incremental file set

For each resolved repo:

1. Look for `${VAULT}/_Shared Knowledge/Code Patterns/<repo>.md`.
2. If present, read its frontmatter `last-learned:` timestamp (ISO 8601) and `learned-from-commits:` list. **Idempotence guard:** if `last-learned` is less than 2 hours ago, log "digest fresh, skipping" and move to the next repo (unless `--force` was passed).
3. The file set in scope is every tracked file under the repo where `git log -1 --format=%ct -- <file>` is greater than the `last-learned` epoch. If no prior digest exists, the whole tracked tree is in scope.
4. Always exclude: `node_modules/`, `dist/`, `build/`, `.next/`, `vendor/`, `__pycache__/`, `.venv/`, lock files (`package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, `Cargo.lock`, `yarn.lock`), binary assets (images, fonts, model weights), and anything matched by `.gitignore` or a `.codepatternsignore` at the repo root.
5. Cap the file set at 300 files; if more, sort by recency and keep the most-recent 300, noting the truncation in the digest.

Use `git -C <repo>` for every git invocation — never `cd`.

---

## Step 3: Extract the signal dimensions

Read the file set and synthesize answers to the dimensions below. Do not paste source code into the digest — answer in concise English with one or two illustrative examples per dimension where helpful.

### Required dimensions

1. **Tech stack signature.** Language(s) with version pinning, package manager (pnpm/npm/yarn/poetry/uv/pip/cargo), framework(s), database(s), deploy target. Read the manifest files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.) plus `Dockerfile` / `fly.toml` / `vercel.json` / `.github/workflows/*.yml`. Capture exact versions where pinned.
2. **Build & test commands.** From the manifest's scripts section and CI config — the exact one-liners to install, build, test, lint, type-check. Use these in future suggestions instead of guessing.
3. **Naming conventions.** Files (kebab-case vs snake_case vs PascalCase, per directory), functions, variables, components, tests. One representative example each.
4. **Error handling.** Throw-vs-return-Result, exception class hierarchy, error logging library, retry/backoff patterns. Cite one canonical example file path.
5. **Test patterns.** Framework (vitest/jest/pytest/etc.), file naming (`*.test.ts` vs `__tests__/` vs `tests/`), fixture and mocking style, snapshot usage, integration-test split.
6. **Type & lint rules.** TypeScript strictness flags, eslint config, ruff/mypy/pyright config, the rules the codebase actually relies on (not just what's in the config). Note any `// @ts-expect-error` or `# type: ignore` hot spots.
7. **File layout idioms.** Where do feature code, shared utilities, types, schemas, tests, and infra live? One-line per top-level directory.
8. **Frequent imports.** The 10 most-imported internal modules and the 10 most-imported third-party packages.
9. **Recurring helpers.** Utility functions, decorators, or hooks that show up in 3+ places. Name them and cite paths.
10. **What this repo intentionally does NOT use.** If `useReducer` is rare, if class components are absent, if there's no ORM and queries are hand-written — call it out. Negative signals stop future-Claude from proposing tools the team already rejected.

### Optional dimensions (include only when the repo has them)

- **API surface** (OpenAPI / tRPC / GraphQL schema location, conventions for new endpoints).
- **Database migrations** (tool, directory, naming).
- **Feature flag pattern** (library, config location).
- **Observability** (logger lib, log shape, telemetry exporter).
- **Release process** (changesets, semver tooling, tag format).

---

## Step 4: Write the digest

Write `${VAULT}/_Shared Knowledge/Code Patterns/<repo>.md` (overwriting any existing file). Use this exact frontmatter and section order:

```markdown
---
title: "Code Patterns — <repo>"
type: code-patterns
repo: <repo>
repo-root: ~/GitHub/<repo>
last-learned: <ISO 8601 timestamp in America/Los_Angeles>
learned-from-commits:
  - <SHA-1 of HEAD at extraction time>
  - <SHA-1 of HEAD at previous extraction, if any>
files-in-scope: <count>
files-truncated: <true | false>
tags:
  - code-patterns
  - <repo>
  - <primary-language>
---

# Code Patterns — <repo>

> One-sentence "what this codebase is" line.

## Tech stack signature
- Language: ...
- Package manager: ...
- Framework(s): ...
- Database: ...
- Deploy: ...

## Build & test commands
```bash
<install one-liner>
<build one-liner>
<test one-liner>
<lint one-liner>
<typecheck one-liner>
```

## Naming conventions
- Files: ...
- Functions: ...
- Components: ...
- Tests: ...

## Error handling
...
Canonical example: [[<relative-path-in-repo>]]

## Test patterns
...

## Type & lint rules
...

## File layout
- `src/`: ...
- `tests/`: ...
- `scripts/`: ...

## Frequent imports
**Internal**
1. ...

**Third-party**
1. ...

## Recurring helpers
- `<name>` at `<path>` — what it does, when to use.

## What this repo intentionally does NOT use
- ...

## Optional dimensions
<only the ones present in this repo>

## Change log
- <YYYY-MM-DD HH:MM PT>: full extraction, <N> files in scope, HEAD <SHA>.
- <YYYY-MM-DD HH:MM PT>: incremental, <M> files changed, HEAD <SHA>.
```

**Append, don't replace, the change-log section.** Every run adds one new bullet.

**Cross-link.** At the bottom add `Related: [[<project-hub-file>]]` if a matching project hub exists in `Projects/`.

---

## Step 5: Surface the result and trigger downstream

1. Print a one-line summary per repo learned: `Learned N new patterns from <repo>; updated digest at <vault-relative-path>.`
2. If invoked from `/session-start`, the briefing now adds a row: **Code Patterns digest:** ✓ fresh as of <timestamp> (or ⚠ stale >14 days — re-run /code-learn).
3. If `obsidian-update` runs later in the same session and writes a Decision Record that touches code style, architecture, or tooling, that DR should include `Related: [[Code Patterns/<repo>]]` automatically.

---

## Idempotence and cost

- Default is incremental — second-and-later runs in the same day touch only changed files.
- Hard cap: 300 files per repo per run. Above that the digest carries `files-truncated: true` and the change log notes the cap.
- The skill never writes to the repo, never opens PRs, never modifies code. It only reads code and writes one Markdown digest in the vault.

---

## Edge cases

- **Repo not at `${GH_ROOT}/<name>`.** Abort with the exact path checked. Don't search elsewhere — the vault expects one canonical location per repo.
- **Repo with no manifest** (raw scripts, dotfiles). Skip the manifest-driven sections, capture file-layout and naming-convention sections, note the limitation in the digest's header.
- **First run on a very large repo** (>300 files). Truncate to the 300 most-recent files, set `files-truncated: true`, note the cap. Next run will pick up where this one left off because `last-learned` advances.
- **Repo deleted but digest still exists.** Don't touch the digest; surface a warning in the next `/code-learn --all` run that the repo path is gone.
- **Repo on a feature branch with very different patterns than `main`.** Always learn from the currently checked-out HEAD and record the SHA in `learned-from-commits`. Don't try to reconcile across branches.
- **Submodules.** Skip them by default; submodules have their own repo and their own digest.
- **Monorepos** (Turborepo / Nx / pnpm workspaces). Learn from each workspace as a separate sub-section under the same `<repo>.md` digest — don't fragment into many files. Use `### <workspace-name>` subheaders inside each dimension.

---

## Notes

- This skill is the missing piece from Chase's seven-levels framework — the team is at Levels 5–6 (vault, raw→wiki, MCP-ready) on the knowledge axis but had no code-axis learning loop. The digest is the code-axis equivalent of an Insight note.
- The digest is meant to be read by Claude, but it is also a useful onboarding document for any human joining a repo.
- If you need to force a full re-learn, pass `--force` to `/code-learn` or delete the existing digest file.
