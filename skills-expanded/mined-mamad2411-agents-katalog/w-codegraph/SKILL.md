---
description: Code-intelligence helper for w-task and w-fix — detects a CodeGraph index (.codegraph/), keeps it in sync, and answers context / impact / affected-test queries from the graph instead of grepping the tree. Degrades silently to git-grep when CodeGraph is unavailable.
argument-hint: <detect|ensure|sync|context|impact|affected|query> [args]
allowed-tools: Bash, Read
---

# w-codegraph

Single entry point every workflow phase uses to talk to [CodeGraph](https://github.com/) —
the on-disk code knowledge graph stored in `.codegraph/`.

Why it exists: Phase 0b, 2 and 4 all need "which files matter for this change".
Doing that with `git grep` costs a large number of file reads per phase. A synced
graph answers the same questions with one command and a bounded payload, so the
same phases run faster and the context window carries symbols instead of file dumps.

**This skill never fails a phase.** Every subcommand exits 0 with a
`CODEGRAPH: unavailable` line when the graph or the binary is missing — the caller
then uses its own fallback path.

Reads `.claude/workflow.yaml`:
- `project.codegraph.enabled` — `auto` (default) | `true` | `false`
- `project.codegraph.auto_index` — `true` (default) | `false`
- `project.codegraph.sync_phases` — phases that run `sync` before their work

---

## Resolution order (every subcommand starts here)

```
enabled: false                        → CODEGRAPH: disabled     (exit 0)
binary missing (command -v codegraph) → CODEGRAPH: unavailable  (exit 0)
.codegraph/ missing:
    enabled: true  + auto_index: true → run `ensure` (may index)
    enabled: auto                     → CODEGRAPH: not-indexed  (exit 0)
.codegraph/ present                   → proceed
```

Detect with:

```bash
command -v codegraph >/dev/null 2>&1 && test -d .codegraph && echo present
```

In a multi-repo project (`repos[]`), each repo has its own `.codegraph/`. Pass
`-p <repo-path>` — or run inside that repo — and never assume the superproject's
index covers a submodule.

---

## `detect`

Report whether the graph is usable, without changing anything. Used by the w-task
setup check to write `codegraph:` into `state.yaml`.

```bash
codegraph status --json 2>/dev/null
```

Emit exactly one line for the caller to store:

| Condition | Output |
|---|---|
| binary + index + fresh | `CODEGRAPH: ready (<N> files, <M> symbols)` |
| binary + index + stale | `CODEGRAPH: stale (<N> files changed since last index)` |
| binary, no index | `CODEGRAPH: not-indexed` |
| no binary | `CODEGRAPH: unavailable` |
| `enabled: false` | `CODEGRAPH: disabled` |

---

## `ensure`

Bring the project to a usable index. Only ever called when the binary exists.

1. **Index present** → run `sync` and return.
2. **Index missing, `auto_index: false`** → return `CODEGRAPH: not-indexed`.
3. **Index missing, `auto_index: true`** → indexing a large repo takes minutes and
   writes a new directory, so **ask once** before the first index:

   ```
   CodeGraph binary found but this project has no index.
   Building one makes context load, impact analysis and test targeting
   noticeably cheaper for every task from now on.

     codegraph init .        (writes .codegraph/, one-time, minutes on a large repo)

   Index now? [Y]es / [n]o, use git-grep this task / [never] — set codegraph.enabled: false
   ```

   - **Y** → `codegraph init .`, then add `.codegraph/` to `.gitignore` when absent
     (the index is a local build artefact — never commit it).
   - **n** → return `CODEGRAPH: not-indexed`, caller falls back for this task only.
   - **never** → set `project.codegraph.enabled: false` in `.claude/workflow.yaml`,
     return `CODEGRAPH: disabled`.

Do not re-ask within a task once answered — the answer is recorded in
`state.yaml.codegraph`.

---

## `sync`

Cheap incremental refresh. Run it before any read subcommand, and after every
commit a phase makes, so later phases query a graph that matches the tree.

```bash
codegraph sync -q 2>/dev/null || true
```

Never let a sync failure stop a phase — the graph being behind is a performance
issue, not a correctness one.

---

## `context <task-description>`

Phase 0b's primary context source.

```bash
codegraph context "<task title + one-line description>" --max-nodes 60 --max-code 12
```

Returns markdown: the relevant symbols, their files, and the code blocks that
matter. Feed it into `context.md § Relevant Files` and `§ Patterns Observed`
verbatim-ish — do **not** re-read those files with `Read` afterwards unless the
task needs a section the graph did not surface.

Fallback when unavailable: `git ls-files` + per-keyword `git grep -l`.

---

## `impact <symbol> [--depth N]`

Phase 2's blast-radius source.

```bash
codegraph impact "<symbol>" --depth 2 --json
codegraph callers "<symbol>" --json     # who breaks if the signature changes
codegraph callees "<symbol>" --json     # what this change depends on
```

Run one `impact` per symbol the plan says will change. Merge the results into
`impact.md § Affected Files` and `§ Dependencies`, keeping the graph's file list
as the authoritative set — it catches indirect callers that a grep for the symbol
name misses.

Fallback: the analyzer's existing grep-driven heuristics.

---

## `affected <file> [<file>…]`

Phase 4's test-targeting source — which test files cover the code being changed.

```bash
git diff --name-only | codegraph affected --stdin --quiet
codegraph affected <files from impact.md> --depth 5 --quiet
```

Use it two ways:
- **Before writing stubs** — an existing covering test must be extended, never
  duplicated by a new stub file.
- **After GREEN** — run the affected set first for a fast confirmation, then the
  full suite before the gate. The affected set never replaces the full run.

Fallback: the layer-glob conventions in `w-test-stubs`.

---

## `query <search> [--kind function|class|…]`

Ad-hoc symbol lookup, for any phase that would otherwise grep for a definition.

```bash
codegraph query "<symbol or partial name>" --limit 10 --json
```

---

## Cost note

Prefer `--json` + `--quiet` and a `--limit` on every read. The point of the graph
is a bounded answer; dumping an unbounded node list back into context spends more
than the grep it replaced.
