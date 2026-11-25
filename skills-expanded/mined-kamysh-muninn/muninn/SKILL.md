---
name: muninn
description: Search indexed code and repository knowledge with Muninn, or configure its file selection through the JSON CLI. Use for code discovery, relationships, worktree searches, and indexing configuration.
---

# Muninn

Muninn saves exploration by finding relevant code and recorded repository
knowledge. Use it when the location is unknown, a question spans files, or code
relationships help. Read the returned source ranges and judge their relevance.
Direct reads and `rg` are useful when the file/target is known, for literal text,
or when index results are missing or stale. Explain consequential index misses.
A reminder invites this judgment; it does not enforce a tool call or a
hook-generated rating, require writeback on every task, or authorize
configuration changes.

## Explain retrieval to the user

After a Muninn retrieval, tell the user how useful the result was for the
current task: give a 0–5 score, one short reason, and what you will do with
the information. Use 0 when nothing usable was found and 5 when the result
directly resolves the question. This is your assessment of task usefulness,
not a search rank or relevance percentage. When several retrievals answer
one question, a single assessment of the combined findings is enough.
Explain in plain language; do not repeat raw JSON unless the user asks for
it. For example: "Muninn usefulness: 4/5 — this points to the relevant
implementation; I’ll read that source range before changing code."

## Search the intended checkout

For code searches, pass `repo` as the absolute path of the checkout you are
working in, including a linked worktree. Alternatively, `cwd` can be a directory
inside that checkout or registered directory. `repo` takes precedence. Supplying
neither is an error; the MCP process does not infer your shell's directory.
Git and database registration resolve the target.

| Question | Tool |
| --- | --- |
| Behavior or concept, symbol unknown | `search_hybrid` (semantic + full-text) |
| Keywords or identifier terms | `search_fulltext` (tokenized, not literal grep) |
| Semantic similarity alone | `search_semantic` |
| Callers/callees, definitions, other recorded relationships | `search_structural` |
| Previously curated repository notes | `search_knowledge` |

The first three accept `query`, `repo` or `cwd`, and optional `limit` (default 10).
Structural search accepts `symbol`, `repo` or `cwd`, and `relation`: `callers`,
`callees`, `defines`, `imports`, `inheritors`, or `inherits`.
Scores rank results; they are not relevance percentages.

Structural results are name-based candidates, not compiler-verified bindings.
For Git checkouts, call resolution prefers matches in the caller's file, keeps
all local ties, and otherwise keeps all checkout-wide matches. Check paths and source before
relying on an edge. Missing edges do not prove an absence of calls. Git checkout
reconciliation rebuilds cross-file relationships after relevant changes;
database-managed directory families also run repository reconciliation. Inspect
the actual state and source before requesting an expensive reindex.

## Worktrees and freshness

An enabled repository family discovers its Git worktrees automatically. New
worktrees inherit the family policy and index without separate configuration.
Search selects that checkout's completed view; unchanged file chunks/vectors
are shared. Updating the main checkout preserves other worktrees' indexed
content until those worktrees are reconciled with their own files.

During merge/rebase or an unmerged index, Muninn retains the last completed
index. It does not index conflict contents. A failed reconciliation also retains
the previous index. A new checkout without a completed index may be temporarily
unavailable. Check `muninn status`, `muninn config PATH --json`, daemon logs and
Git state when freshness matters; `status PATH` only accepts the registered
locator, and search results currently have no freshness field. Use direct source
inspection while the index is catching up.

## Configure with JSON

Connections and credentials come from `~/.config/muninn/config.toml` and the
existing credential setup. Family policies are in PostgreSQL. Configure them
through the CLI rather than editing SQL directly. A policy change affects
the repository's whole worktree family; preflight inventories only the selected
checkout. `muninn add PATH` and `muninn config PATH` open the human TUI.
Agents should use the JSON forms below.

Set `ROOT` to the intended absolute checkout path. Use these read-only operations
for a registered family:

```sh
muninn config "$ROOT" --json
muninn preflight "$ROOT" --json
```

For an unregistered directory, begin with `preflight PATH --json`; it returns
creation policy/defaults without registering. `config PATH --json` reports
`not_registered` until registration exists.

Inspect `.data.policy`, `.data.effective_policy`, `.data.defaults`,
`.data.capabilities`, and `.data.preflight`. Preflight reports file counts,
bytes, costly directories, limits and advice; it does not parse or embed files
and cannot guarantee indexing cost. This metadata preflight does not apply Git ignore files. Runtime indexing does,
with explicit Muninn inclusion overrides. Selection maintenance temporarily refuses
family searches; inspect status/configuration for pending targets and errors. Choose
exclusions based on what the task needs and the actual inventory, including
build outputs, dependencies and generated bundles. Review incomplete inventory
and warnings before deciding to start. `index.exclude` drops files;
`index.vendor` retains text search and defers embeddings. The Git worktree
search path currently does not lazily warm those deferred vectors or apply the
legacy vendor ranking penalty; do not assume equivalent semantic coverage.
Family rules extend frozen defaults; last match wins, exclusion precedes vendor classification,
and a pruned parent must be re-included before its children can be included.

For an existing family, construct a complete candidate from a fresh inspect
response, preserving fields you do not intend to change:

```sh
muninn config "$ROOT" --json > view.json
jq '.data | {api_version:1, expected_family_id:.family_id,
  expected_revision:.revision, policy:.policy}' view.json > candidate.json
# Edit candidate.json for the intended policy; this is a request, not stored config.
muninn config "$ROOT" --json --check - < candidate.json
muninn config "$ROOT" --json --apply - < candidate.json
```

A new-family request has `{ "api_version": 1, "policy": ... }`, using the
complete policy returned by preflight for that unregistered directory and any intended
changes. New-family defaults snapshot the global provider/model, request size,
watcher delay and global file rules. Existing saved policy/defaults remain stable
when global settings change.
For local embeddings set `policy.embeddings.backend` to `"local"` and
`policy.embeddings.model` to `null` before registration. Check it with
`config PATH --json --check -`, then register with
`muninn add "$ROOT" --json --input - < initial.json`.
`add PATH --json` without input uses creation defaults and is idempotent for an
existing family. Registration and saving do not start a new family's indexing.

When indexing is wanted, inspect/preflight the saved policy again and explicitly
start it. Use the returned family ID/revision to guard the decision:

```sh
muninn preflight "$ROOT" --json > ready.json
jq '.data | {api_version:1, expected_family_id:.family_id,
  expected_revision:.revision}' ready.json > start.json
muninn start "$ROOT" --json --input - < start.json
```

Start records authorization and performs indexing; the daemon can resume an
interrupted authorized run. A policy change for an already enabled family can
trigger reconciliation. JSON responses have `api_version`, `ok`, and `data` or
`error`; check exit status and error codes. On a revision/identity conflict,
re-read and review the change before retrying. Respect reported capabilities:
changing an existing embedding profile is currently unsupported. Normal
startup/preparation applies schema migrations automatically; read-only
inspect/check/preflight do not. Users do not need a separate migration script.

## Durable knowledge

Record stable, non-obvious repository facts that save future exploration using
`record_knowledge`; retrieve them with `search_knowledge` or `list_knowledge`.
Knowledge tools currently use an exact `repo` path string, not worktree/family
resolution. Use the established repository key (usually the main checkout path)
for shared notes, and explicitly describe any branch-specific applicability.
Do not silently create a separate note collection for each temporary worktree.
Mimir is useful for durable lessons about approaches and prior decisions.
