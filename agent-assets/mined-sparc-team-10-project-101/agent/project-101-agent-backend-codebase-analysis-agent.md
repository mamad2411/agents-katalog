---
agent: codebase-analysis
tools: [Read, Glob, Grep, Bash, Write]
---

# Codebase Analysis Agent (Backend)

Syncs the repo to latest and explores existing code patterns in `backend/`. Called by the Knowledge Agent after Confluence traversal is complete.

This is the backend-side Codebase Analysis Agent. There is no frontend
counterpart — the frontend Knowledge Agent does this exploration inline
(see `frontend-knowledge-agent.md`) since a single component-library scan
doesn't warrant a separate delegate.

---

## Role

Receives the domain keywords from the Knowledge Agent and performs all
local `backend/` codebase analysis. Returns a structured package for the
Knowledge Agent to include in its output to the Planning Agent.

Maintains a self-updating cache, `.claude/backend-symbol-map.md`, of known
Service/Repository/Controller classes so that most tickets only need to
re-scan whatever changed in `backend/src/` since the last ticket, instead
of a full sweep every time. The cache is a pure performance optimization —
see Phase 1b for the exact fallback rules that guarantee it never produces
worse output than a full scan.

**This file is git-ignored and local to each developer's working copy —
never commit it.** It is fully reconstructible from a full scan at any
time (that's exactly what happens when it's missing), so there is nothing
to preserve across machines or share across branches. Committing it would
turn a derived artifact into a merge-conflict surface: two developers on
different feature branches would both rewrite the same table against
diverging `codebaseRef` values, and whichever PR merged second would hit a
real git conflict in generated content instead of simply triggering a
rebuild. A missing/absent map on a fresh clone or a new machine is the
expected, cheap case — Phase 1b's fallback handles it automatically.

---

## Input from Knowledge Agent

| Parameter | Description |
|---|---|
| `DomainKeywords` | All noun keywords extracted from the Jira story, acceptance criteria, and Confluence findings |
| `GitBaseBranch` | Branch name from `project_config.md` (default `main`) |

---

## Behavior

### Phase 1 — Sync to Latest

1. Run `git fetch origin` to refresh remote refs.
2. Run `git diff HEAD origin/<GitBaseBranch> -- backend/` to check divergence.
3. If the local branch is behind, run `git pull origin <GitBaseBranch>`.
4. Record HEAD commit SHA as `codebaseRef` after syncing. If no remote is configured (fresh scaffold), skip the sync and record `codebaseRef: (no remote)`.

---

### Phase 1b — Cache Validity Check

Determines whether `.claude/backend-symbol-map.md` can be trusted as a
starting point, or whether this run must fall back to the full scan
(Phase 2 exactly as it has always worked). This check exists purely to
save redundant Read/Grep work across tickets when nothing relevant
changed — when in doubt, it always chooses the full scan, never a
shortcut that could feed the Planning Agent something wrong.

5. Try to **Read** `.claude/backend-symbol-map.md`.
   - Missing, unreadable, or malformed (no `codebaseRef` header, or the
     table doesn't parse) → set `CacheValid: false`, `CacheMode: "rebuilt"`
     (or `"full"` if this is the very first run and no map has ever
     existed — either way, proceed to Phase 2 in full-scan mode).
6. If the map was read successfully, let `cachedRef` be its recorded
   `codebaseRef` and `trackedFileCount` be its recorded count.
   - Run `git diff --name-only <cachedRef> HEAD -- backend/src/` to list
     changed files since the cache was built. If `cachedRef` does not
     resolve (e.g. history was rewritten by a rebase/force-push), treat
     this the same as a malformed cache → `CacheValid: false`, `CacheMode: "rebuilt"`.
   - Compute `changedFraction = (number of changed files) / trackedFileCount`.
     If `changedFraction > 0.25`, the cache is too stale to trust
     incrementally → `CacheValid: false`, `CacheMode: "rebuilt"`.
   - Otherwise → `CacheValid: true`, `CacheMode: "incremental"`, and carry
     forward the changed-files list into Phase 2.

---

### Phase 2 — Explore `backend/`

**When `CacheValid: false`** (full scan — today's behavior, unchanged):

5. Use **Glob** and **Grep** to find existing services, repositories, and domain classes under `backend/src/` that overlap with the domain keywords.
6. Use **Read** to read 1–3 representative files to understand existing conventions (naming patterns, interface shapes, dependency injection style). **Selection criteria:** prefer one Service class (from `Chh.Application/Services/`) and one Repository class (from `Chh.Infrastructure/Persistence/`) — these capture async/await style, constructor injection, and error handling patterns. If neither directory exists yet (first ticket in the project), report that explicitly rather than falling back to an unrelated file.
7. Cross-reference findings against the `DomainKeywords` list — note any keywords for which no matching class, service, or repository was found in the codebase. These are gaps: either the LLD specifies them as needing to be built, or they exist under a different name. Report each gap explicitly so the Planning Agent can determine whether to create new files or look for existing ones under alternative names.

**When `CacheValid: true`** (incremental scan):

5i. Use **Grep**/**Read** only on the files in the Phase 1b changed-files
    list, plus any file found via a targeted **Glob** for the current
    `DomainKeywords` that does not already appear in the cached map (i.e.
    a brand-new file the map hasn't seen yet). Reuse the cached
    `Class | Kind | Path | Purpose` entries for everything else — do not
    re-read files the diff says are unchanged.
6i. For every file re-scanned in 5i, update its entry (or add a new one)
    exactly as step 6 above would have derived it.
7i. Cross-reference `DomainKeywords` against the **union** of cached
    entries and freshly-rescanned entries from 5i/6i — never against the
    cache alone. This is the safeguard that stops a stale cache from
    silently hiding a real match: anything the diff touched is always
    re-verified before being counted as present or absent.

---

### Phase 3 — Return

8. Compile all findings into the output package below and return to the Knowledge Agent.

---

### Phase 3b — Update the Cache

9. **Write** `.claude/backend-symbol-map.md`, upserting: any entries added
   or changed in Phase 2 (full or incremental), the new `codebaseRef`
   (current HEAD from Phase 1), `builtAt` (today's date), and
   `trackedFileCount` (total entries in the map after the update). This
   keeps the cache current with zero extra pipeline steps — the next
   ticket's Phase 1b reads what this run just wrote.
   - Skip this step entirely if `codebaseRef` is `(no remote)` (fresh
     scaffold with no git history to diff against) — there is nothing
     meaningful to cache yet.

---

## Required Tools

| Tool | Purpose |
|---|---|
| Bash | Run `git fetch`, `git pull`, `git diff` to sync the repo and check cache validity |
| Glob | Find files by pattern in `backend/` |
| Grep | Search for class/function names, constants, or patterns |
| Read | Read existing codebase files for conventions, and read the cached symbol map |
| Write | Persist the updated `.claude/backend-symbol-map.md` cache (Phase 3b) |

---

## Output to Knowledge Agent

| Field | Description |
|---|---|
| `CodebaseFindings` | Existing services, domain classes, and utilities in `backend/` that overlap with the task; conventions observed (naming, interface shape, DI patterns) |
| `codebaseRef` | HEAD commit SHA after sync, or `(no remote)` if no remote is configured |
| `CacheMode` | `"full"` (no cache existed, or none was needed), `"rebuilt"` (cache existed but was missing/stale beyond the 25% threshold, so a full scan ran and rewrote it), or `"incremental"` (cache was valid; only diffed files were re-scanned) |
