---
name: siyuan-upstream-debug
description: "Inspect SiYuan kernel source (github.com/siyuan-note/siyuan) without cloning, when debugging siyuan-cli behavior against the upstream kernel: API registration, request/response shape, SQL semantics, asset paths, guards. Use when a question can only be settled by reading upstream Go code."
metadata:
  version: "0.1.0"
---

# SiYuan Upstream Debug

Read upstream source on demand: cached tree → targeted raw fetches → static entry table. Never `git clone` the full repo (heavy `app/` frontend). Never browse the web UI for structural questions.

## Layer 0 — Static entry table (try first)

Question type → file under `kernel/` (paths stable across versions; verify against tree if unsure):

| Question | File(s) |
|---|---|
| Which endpoints exist, auth level, handler name | `kernel/api/router.go` — one `ginServer.Handle(...)` per line: path + `CheckAuth`/`CheckAdminRole`/`CheckReadonly` + handler |
| Exact request fields, response = JSON or raw bytes, error codes | `kernel/api/<domain>.go` (`block.go` `attr.go` `file.go` `asset.go` `filetree.go` `export.go` `history.go` `notebook.go` `system.go`). `c.JSON(...)` = JSON; `c.Data(200, mime, data)` = raw bytes |
| `blocks` table schema, SQL query semantics (e.g. TEXT vs numeric compare) | `kernel/sql/database.go` `block.go` `block_query.go` `block_ref.go` |
| Block model, blocktree/ial, id/attr semantics | `kernel/treenode/blocktree.go`; markdown parse/`dataType` lives in external lib `88250/lute` (entry: `kernel/util/lute.go`) |
| Asset path resolution (`data/assets`, S3, custom dirs) | `kernel/model/asset_path_resolver_windows.go` / `asset_path_resolver_other.go`, `kernel/model/assets.go` |
| Behavior semantics (e.g. does child update bump doc `updated`) | `kernel/model/*.go` (`block_update.go`, `refer.go`, ...) |
| Path guards / refused reads (conf, keys, encrypted boxes) | `kernel/util/file.go` (`GetAbsPathInWorkspace`), `refuseToAccess` in `kernel/api/file.go` |
| Config structs, i18n error messages | `kernel/conf/*.go` (`api.go` token/auth, `lang.go`) |
| WebSocket broadcast event payloads | `kernel/api/broadcast.go` + `Push*` calls in `kernel/model/` |
| What the official side wraps as agent tools (naming/validation reference) | `kernel/mcp/tools/*.go` |
| SiYuan native CLI surface (command-name competition) | `kernel/cli/cmd/*.go` |

## Layer 1 — Tree inventory (when location unknown)

```bash
REF=v3.8.2   # or master; see Version pinning
mkdir -p tmp && echo '*' > tmp/.gitignore
curl -s "https://api.github.com/repos/siyuan-note/siyuan/git/trees/${REF}?recursive=1" -o tmp/sy-tree.json
```

Flat manifest of every path: `{path, mode, type(blob|tree), sha, size, url}`.

- **Cache per session**; reuse the file for all "where is X / does X exist / did X change" questions. The trees call counts against the **60/h unauthenticated core-API limit**, so caching is load-bearing, not cosmetic.
- Check the `truncated` flag. If `true`, the listing is partial — never conclude "file does not exist"; fetch sub-trees instead: `git/trees/${REF}:kernel/api?recursive=1`.
- Blob `sha` = content hash: compare across refs to detect whether a file changed between versions.

## Layer 2 — Content fetch (main workhorse)

```bash
curl -sL "https://raw.githubusercontent.com/siyuan-note/siyuan/${REF}/kernel/api/router.go" -o tmp/router.go
```

- `raw.githubusercontent.com` is a separate CDN; it does **not** consume the core-API limit. Fetch freely.
- Then grep/read locally: filter `router.go` for candidate routes, read only the matching handler functions.
- Handler function name = last route segment, files split by domain → path lookup is deterministic once you know the endpoint.

## `gh` / code search — only for content search

Use `gh search code --repo siyuan-note/siyuan "<literal>"` (needs auth; separate rate limit) only when a string is known to exist but its file cannot be located from Layer 0/1. Everything else (locate + read) works without `gh`.

## Version pinning (correctness, not hygiene)

1. Resolve the user's kernel version first: `pnpm run siyuan api system.getVersion` (or ask).
2. Set `REF=v<version>` (e.g. `v3.8.2`); raw and trees both accept tag names directly.
3. Use `master` only when the behavior is known stable across versions or the question is about future upstream state; say which ref a conclusion came from.
4. Guards/auth logic change often between releases; never cite master findings as the user's runtime behavior without a version check.

## Typical loop

```text
symptom in CLI → Layer 0 table → raw-fetch the file → grep handler →
read function (request binding, c.JSON vs c.Data, error codes, middleware) →
compare with src/api/endpoints/<id>.ts in this repo → conclude + cite ref
```

## Gotchas

- `git/trees` needs the **branch/tag/sha**, not `HEAD` alias for some endpoints; tag names work (`v3.8.2`).
- Some kernel logic lives outside the repo (`88250/lute` for markdown/blocks). Layer 0 notes where.
- SiYuan repo layout shifts occasionally (e.g. old `kernel/block/` no longer exists; block logic moved to `kernel/model/`, `kernel/treenode/`, `kernel/sql/`). If a Layer 0 path 404s on an older tag, fall back to Layer 1 tree lookup for that ref.
