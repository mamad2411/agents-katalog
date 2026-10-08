---
name: hips-install
description: Install or update hips hybrid code search and configure it for a coding agent, preferring MCP in a sandbox and the CLI otherwise, including optional macOS Codex sandbox cache access. Use for hips installation and setup requests, not routine code searches.
---

# Install hips

Install the semantic build from a local hips checkout when developing hips:

```sh
cargo install --path . --features semantic
```

Otherwise use the upstream source:

```sh
cargo install --git https://github.com/jasonthird/high-performance-search-engine --features semantic
```

Check `command -v hips` and `hips --version` so verification uses the intended
binary. Preserve the user's existing MCP, plugin, and search-skill setup;
installing the binary alone does not configure those integrations.

## Configure routing for the execution environment

Use this routing rule: **sandboxed shell → prefer MCP; no shell sandbox →
prefer CLI**. Preserve an existing hips MCP registration. Otherwise register a stdio server
running `hips mcp --root /absolute/path/to/repository` in the client's MCP
configuration, or use the hips plugin's existing registration. Without
`--root`, the server resolves the git work tree enclosing its startup directory.
Check the reported root; an existing server does not follow shell `cd`.

For Codex, merge this with the existing config (do not duplicate the table):

```toml
[mcp_servers.hips]
command = "/absolute/path/to/hips"
args = ["mcp", "--root", "/absolute/path/to/repository"]
```

Resolve the binary with `command -v hips`. Install/update the sibling `hips` search skill too, so it chooses MCP for
sandboxed shell execution and the CLI otherwise.
The canonical skill sources are `skills/hips/SKILL.md` and
`skills/hips-install/SKILL.md`; plugin mirrors live under `plugin/hips/skills/`.
Update the user's existing skill location; avoid creating competing copies.

After a binary update, reconnect/restart the MCP server and refresh its tool
schema. The running process retains its old code. Check that `tools/list`
advertises `verbose` for `search_code` and `index_status`.

MCP builds a missing index on first search and watches for changes. First
semantic use downloads the 274 MB CodeRankEmbed GGUF into
`~/.cache/csearch/models/` (`HIPS_MODEL_PATH` points at a local copy,
`HIPS_MODEL_OFFLINE=1` forbids downloads). Use prepopulated model and grammar
caches offline. CoreML also needs separately compiled CodeRankEmbed shapes;
installing the semantic binary supplies the ggml engine, not those CoreML
models. Keep the CLI available for terminals and repositories
that the connected MCP server does not serve.

## Optional Codex setup on macOS

If E5RT cannot write under `~/Library/Caches/hips`, Codex supports adding
that directory to the writable roots while retaining `workspace-write`.
Check the current [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
and the user's active configuration before changing it.

Treat a persistent sandbox permission grant as opt-in. If the user already
requested this configuration, proceed within that authorization. Otherwise
show the concrete proposed change and obtain their choice before applying it.
Merge the entry with existing writable roots and preserve unrelated settings;
do not overwrite the config or add a duplicate TOML table.

```toml
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
writable_roots = ["/Users/your-user/Library/Caches/hips"]
```

Resolve the user's actual absolute path; TOML does not expand `$HOME`. Apply
this to the selected config scope (normally `~/.codex/config.toml`) and
verify in a new Codex session, since an existing process retains its sandbox.
Grant only the directories the requested workflow needs, not the whole home
or Library tree. Index-building and first-time downloads may separately need
writable `CSEARCH_CACHE_DIR` (indexes and the model) locations.

Alternatively, with a hips version supporting the override, relocate the
CoreML cache for one invocation into an already writable directory:

```sh
HIPS_COREML_CACHE_DIR="$PWD/.hips-coreml-cache" \
  hips search --root <repository> --query "permission validation" -v
```

Keep this directory out of the repository index. The override changes the
hips process's Foundation home using `CFFIXED_USER_HOME`; runtime files are
under `<override>/Library/Caches/hips/com.apple.e5rt.e5bundlecache/`. It does
not move hips indexes or the model file. This mechanism is not a public
CoreML configuration property and needs verification on the target macOS.

Neither writable roots nor relocation grants GPU, ANE, or IOSurface service
access. If those remain denied, hips retries with ggml, choosing Metal
when a GPU is accessible and CPU otherwise. Do not claim that adding a cache
permission enables CoreML, disable the sandbox, require routine escalation,
or permanently change the user to lexical search.

## Verify the installed result

Run MCP `search_code` with a representative query, `mode: "semantic"`,
`verbose: true`, and `expected_root` set to the indexed repository root.
Require `isError: false`, finite scores, and relevant paths. Inspect
`structuredContent.diagnostics.encoder` for the actual backend, validated
warmup, and fallback reasons. Repeat the query to verify query-cache reuse.
`index_status` with `verbose: true` inspects the resident runtime without
triggering inference; a not-loaded encoder or a hybrid-capable index alone
does not prove semantic execution works.

CoreML's allowed compute units do not prove ANE/GPU execution. Report
`execution_device: not_observed` honestly. The client's MCP launch context
may differ from its shell sandbox; verify the actual connected server and
avoid assuming all MCP hosts grant the same hardware access. No broader
shell permissions are needed just to use the registered MCP tool.

For the CLI path, run a representative query with `-v` in the target sandbox.
Capture stderr separately and validate JSONL stdout. A `using lexical BM25`
note means lexical degradation; a ggml retry can still be successful hybrid
execution. Report the backend that worked and any remaining restriction.

`--root` prefers the index for that directory, then its nearest indexed
ancestor. Ancestor reuse searches the entire indexed repository and rebases
paths (so `../` results are valid); it does not filter to the subtree.

MCP checks for invalid or missing live document embeddings before semantic
search and rebuilds affected files, even if their text is unchanged. Debug
status reports `invalid_live_embeddings`; search reports
`repaired_embeddings`. A failed repair is an error, not a successful hybrid
result. For CLI repair, run `hips index-repo --root <repository>` and retry.
