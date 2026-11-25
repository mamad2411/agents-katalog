---
name: git-wiki
description: |
   Build and maintain a local code-project wiki under .wiki. Use this skill whenever the user mentions "wiki", "ingest", "refresh wiki", "update wiki", "lint wiki", "check wiki", "document the codebase", or asks a question that can be answered from wiki pages. Also use it when the user asks how something works in the project and a wiki page could capture the answer for future reference.
version: "1.3.1"
---

# Project Wiki

Maintain a local wiki for a code project under `.wiki`.

Source of truth is always the current git-tracked repository files at `HEAD`, including tracked documentation in `.docs/` and `docs/`, not the wiki.
The wiki files themselves may be untracked; read and update the live `.wiki/` contents from the working tree when present.

## Rules

* Operate only on git-tracked files and git history
* Ignore staged and unstaged uncommitted changes; ingest and query verification use committed content at `HEAD` only
* Exclude `.wiki/**` from git-based source selection
* Do not assume `.wiki/**` is git-tracked; use the current `.wiki/index.md` checkpoint when it exists
* Every wiki page must have YAML frontmatter
* `.wiki/index.md` must be updated on every ingest
* Do not ask the user before ingesting

## Wiki Layout

Required:

* `.wiki/index.md` — master catalog (tracks last ingest commit)

Optional (create as needed):

* `.wiki/features/` — one page per significant feature, module
* `.wiki/bug-fixes/` — one page per notable bug fix or patch
* `.wiki/concepts/` — cross-cutting ideas and patterns
* `.wiki/entities/` — data models, schemas, types
* `.wiki/flows/` — sequences, pipelines, request lifecycles
* `.wiki/notes/` — ad-hoc or open questions

## Page Conventions

### index.md frontmatter

`index.md` carries extra fields to track ingest state:

```yaml
---
title: "Project Wiki"
type: "index"
status: "active"
last_commit: "<full-sha>"
updated_at: "YYYY-MM-DD"
---
```

`last_commit` is the full git commit SHA at the time of the most recent full-repository ingest. This checkpoint lives in the current `.wiki/index.md` file whether or not `.wiki/` is git-tracked. On the next ingest, prefer this saved `last_commit` to find changed files with `git diff --name-status -M <last_commit> HEAD`.

If git metadata is unavailable, do not fall back to filesystem scanning. Ingest and lint are unavailable until git access works again.

### Other pages

```yaml
---
title: "Page Title"
type: "feature|bug-fix|concept|entity|flow|note"
status: "draft|active|stale"
source_paths: []
updated_at: "YYYY-MM-DD"
---
```

Use `status: "stale"` when the source file has changed significantly since the page was last updated, or when the page describes something that no longer exists. During ingest, pages whose `source_paths` changed since `last_commit` should be updated or marked stale. Do not delete stale pages automatically — mark them and note the drift so the user can decide.

### Page naming

* Use lowercase, hyphenated filenames: `auth-middleware.md`, `user-schema.md`
* Mirror the source path when making feature pages: `src/api/routes.ts` → `.wiki/features/src-api-routes.md`
* Use descriptive names for concepts and flows: `.wiki/concepts/request-lifecycle.md`

### Wiki links

Use `[[page-slug]]` links between pages whenever a page references something covered on another page. The target should match the destination filename without the `.md` extension. This makes the wiki navigable and lets lint resolve links deterministically.

## Ingest

Trigger on:

* `ingest`
* `ingest [file]`
* `ingest [folder]`
* `refresh wiki`
* `update wiki`

Workflow:

1. Read `.wiki/index.md` from the working tree if it exists, even when `.wiki/` is untracked — note `last_commit` from frontmatter
   * Missing `.wiki/index.md` or a missing `last_commit` means there is no prior ingest checkpoint
2. Run `git rev-parse HEAD` to get the current HEAD commit SHA
3. Detect changed files:
   * If `last_commit` is set: `git diff --name-status -M <last_commit> HEAD` and exclude `.wiki/**`
   * Use the saved `last_commit` even if the wiki is untracked; do not treat an untracked `.wiki/` as a fresh ingest from `HEAD`
   * Use the git status codes to distinguish added, modified, deleted, and renamed paths when updating wiki pages
   * If no prior ingest: build a broad ingest candidate set from `git ls-files` at `HEAD`, excluding `.wiki/**` (see Ingest Priorities below)
4. Resolve scope:
   * If a file or folder is specified, prioritize it — limit the tracked candidate set to that scope
   * For a scoped ingest, do not advance `.wiki/index.md:last_commit` unless the scoped ingest also covers every file changed since `last_commit`
   * Otherwise ingest changed files first, then fill in missing coverage
5. Read relevant tracked repository files — understand their role
6. Update or create wiki pages under `.wiki/`
7. Mark pages for deleted source files as `status: "stale"` with a note in the page body, and update moved or renamed pages based on rename information from git
8. Update `.wiki/index.md`:
   * Always set `updated_at` to today
   * Set `last_commit` to the current HEAD SHA only after a full ingest or after processing the complete changed-file set from the previous `last_commit`
   * If a broad ingest stops early after partial coverage, leave `last_commit` unchanged and note in `index.md` that bootstrap coverage is still partial
   * Never discard an existing saved `last_commit` merely because `.wiki/` is untracked

Ingest is automatic. Do not ask the user for confirmation.

If git commands fail, report that the wiki skill cannot ingest until git access is restored. Do not substitute directory walking.

### Ingest Priorities

When doing a broad ingest from git-tracked files, work in this order and stop when you have good coverage (typically 10–20 pages for a medium project):

1. Root readme and tracked documentation under `.docs/` and `docs/`
2. Package/build/workspace config (`package.json`, `pyproject.toml`, `Cargo.toml`, etc.)
3. Entry points (`main.ts`, `index.ts`, `app.py`, `cmd/`, etc.)
4. Core features and shared utilities → `.wiki/features/`
5. API definitions, schemas, and persistence layers → `.wiki/features/` or `.wiki/entities/`
6. Notable bug fixes visible in git history → `.wiki/bug-fixes/`
7. Jobs, queues, background workers → `.wiki/features/`
8. UI structure (if present) → `.wiki/features/`
9. Tests (summarize patterns, don't document every test file)
10. Cross-cutting concepts, entities, and flows worth capturing

For large repos (100+ files), focus on depth over breadth: deeply document the 10 most important modules rather than shallowly touching 50.

## Query

When asked a project question:

1. Read `.wiki/index.md` if it exists
2. Read relevant wiki pages if they exist
3. If the wiki is missing, the relevant page is missing, or a page is marked stale, verify directly against git-tracked repository source before answering
4. Prefer tracked documentation in `.docs/` and `docs/` when it is relevant to the question, then confirm against code or config when needed
5. Verify against git-tracked repository source when the answer involves specific values (counts, names, configs)
6. Answer with a concise explanation and `[[wiki-link]]` citations when relevant wiki pages exist
7. If you created new understanding not yet in the wiki, mention it — the user can ask you to save it

## Lint

Trigger on:

* `lint`
* `lint wiki`
* `check wiki`

Checks:

* Contradictions between pages (two pages making conflicting claims)
* Orphan pages with no inbound `[[links]]`
* Concepts mentioned across multiple pages but lacking their own page
* Stale pages (`status: "stale"`) that may have drifted from current source
* Missing coverage for major changed modules (files changed since `last_commit` with no wiki page)
* Broken `[[wiki-links]]` where the target page doesn't exist

### Lint Output Format

```
## Wiki Lint Report — YYYY-MM-DD

### Errors
- [page] description of contradiction or broken link

### Warnings
- [page] description of potential issue

### Suggestions
- description of missing coverage or improvement

### Next Questions
- open questions worth investigating
```

Do not auto-fix unless explicitly asked.

## Writing Guidance

* Summarize; do not reproduce large code blocks — a few lines of example code is fine, but explain patterns rather than paste implementations
* Use concrete file paths as anchors (`src/api/routes.ts:42`)
* Separate facts (directly read from source) from inferences (your interpretation)
* Cross-link related pages with `[[wiki-links]]`
* Keep pages under ~500 words; create additional pages rather than growing one page long
* Prefer useful coverage over exhaustive coverage — a good wiki is navigable, not encyclopedic

## Quality Bar

The wiki succeeds when:

* `.wiki/index.md` helps a new reader navigate the project in under 2 minutes
* Answers can start from wiki pages and be verified in code
* Ingest detects changed files automatically using the saved `last_commit`
* Lint catches drift before the wiki becomes misleading