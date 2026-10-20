---
name: document-search
description: Search indexed personal documents via Linkly AI — progressive workflow from environment detection through find_paths, list, search, outline/grep, and paginated read. Use when the user asks to find files in their knowledge base, search notes/PDFs/docs, or read indexed content outside the repo.
---

# Document Search

Search the user's **indexed document library** (Linkly AI) with a progressive, token-efficient workflow. Never read whole documents upfront — narrow first, then paginate.

**Detailed references** (read when stuck):
- `references/cli-reference.md` — full CLI syntax
- `references/mcp-tools-reference.md` — MCP tool parameters
- `references/search-strategies.md` — query crafting, AND enforcement, time filters
- `references/troubleshooting.md` — connection, sandbox, version, cloud vs local

## Phase 0 — Environment Detection

Before any search, determine **how** you can reach the index:

| Signal | Mode | Action |
|--------|------|--------|
| MCP tools `search`, `find_paths`, `list_libraries` available | **MCP** | Use `GetDynamicTools` → `CallDynamicTool` on the Linkly namespace |
| `linkly status` succeeds in shell | **CLI** | Run `linkly` subcommands directly |
| CLI fails with localhost/LAN unreachable but MCP works | **Sandboxed CLI** | Prefer MCP; do not retry CLI without user approval for network sandbox |
| Neither available | **Blocked** | Ask user to start Linkly Desktop + enable MCP, or install CLI |

**Connection tier** (critical — wrong tier = false "not found"):

| Connection | Reaches |
|------------|---------|
| Local MCP / default CLI | All **local** indexed content |
| LAN (`--endpoint` + `--token`) | Same machine's local content only |
| Remote (`--remote` / cloud gateway) | Local (via tunnel, Pro) **+** linked `cloud://owner/slug` libraries |
| Cloud library explicit | `cloud://owner/slug` — works even when Desktop offline |

Run `list_libraries` (MCP) or `linkly list-libraries` early when the user mentions a named library or cloud content.

**Severity if misdetected:**

| Level | Symptom | Fix |
|-------|---------|-----|
| Blocker | Reporting "not found" without checking cloud tier | Re-run with `--remote` or `library="cloud://..."` |
| Major | CLI sandbox blocks localhost | Switch to MCP or request sandbox approval |
| Minor | Stale `doc_id` after re-index | Search again for fresh IDs |

## Phase 1 — Orient (explore / list_libraries)

When the request is broad ("what do I have about X?", "what's in my notes?"):

```bash
linkly list-libraries
linkly explore                          # local overview: types, dirs, keywords, recent activity
linkly explore --library my-research    # single library
```

MCP equivalents: `list_libraries`, `explore`.

Use output to pick keywords, libraries, and directories for Phase 2.

**Decision tree:**

```
User question
├── "What libraries do I have?"     → list_libraries
├── "What's in my knowledge base?"  → explore
├── "What's in folder X?"           → find_paths → list
├── "Find docs about topic Y"       → search (maybe after find_paths)
└── "Read note Z"                   → list --scope notes OR search --scope notes → read
```

## Phase 2 — Locate Container (find_paths / list)

**User names a folder/app, not a topic** ("in my WeChat", "Notion notes", "that reports folder"):

```bash
# Step 1: discover real path (OR-match patterns)
linkly find-paths --patterns WeChat,微信,wxid --limit 5

# Step 2a: topic inside container → search with path_glob
linkly search "receipt" --path-glob "*xinWeChat*" --limit 10

# Step 2b: enumerate container → list (not search)
linkly list --scope folder --path /Users/me/Documents/reports --type pdf
```

| User intent | Tool | Why |
|-------------|------|-----|
| Topic/content query | `search` | Ranked full-text retrieval |
| "What's in this folder?" | `list` | Complete enumeration, paginated |
| Browse notes by tag | `list --scope notes --tags project` | Notes are a separate container |
| Find note mentioning X | `search --scope notes` | Full-text over notes |

**Notes scope rules:** `--scope notes` ignores `--library` and `--path-glob`. Cloud libraries have no notes.

Copy `path_glob` from `find_paths` JSON **verbatim** when scoping a whole folder.

## Phase 3 — Search

Default: omit `--library` (searches all **local** content). Add `cloud://owner/slug` explicitly per cloud library.

```bash
linkly search "API authentication design" --limit 10
linkly search "quarterly report" --type pdf --modified-after 2024-07-01
linkly search "standup" --scope notes --tags work
linkly search "design tokens" --remote --library "cloud://owner/design-system"
```

**Document type filter** — use `--type` / `doc_types`, not path globs:

| Type | Value | Notes |
|------|-------|-------|
| PDF | `pdf` | No outline — grep then read |
| Markdown | `md` | Outline supported |
| Word | `docx` | Outline supported |
| Slides | `pptx` | Slide-level outline |
| Images | `image` | OCR text indexed |
| Audio/video | `audio`, `video` | Transcript indexed; check Desktop indexing settings |

**Query strategy** (see `references/search-strategies.md`):
- Precise terms → BM25 keyword match
- Natural language → vector semantic match
- Synonyms in one query → OR logic, multi-match ranks higher
- Require ALL terms → chain `search` → `grep` per doc_id

Read `[meta] now=<iso>` or `_meta.now` for relative dates — never guess today's date.

**Pass `doc_id` verbatim** to downstream tools (`local://…` or `cloud://…`). Never fabricate IDs.

## Phase 4 — Narrow (outline / grep)

Before reading, pick the smallest surface:

```bash
# Structure available
linkly outline 1044 --expand 2,3.1

# Exact text / no outline
linkly grep "useState" 1044 -C 3
linkly grep "TODO|FIXME" 1044 --mode count
```

| Situation | Tool |
|-----------|------|
| Long doc, need sections | `outline` → note line ranges `[L30-50]` |
| Known term, name, regex | `grep` → note line numbers |
| `has_outline=false` (PDF, txt) | `grep` first, then `read` |

MCP `grep` accepts one `doc_id` per call; CLI accepts batch via stdin (`-`).

## Phase 5 — Read (paginated)

```bash
linkly read 1044 --offset 30 --limit 21    # section from outline [L30-50]
linkly read 1044 --image-text full         # OCR for embedded images
```

- Max 500 lines per call; paginate until sufficient
- `ocr_pending: true` → background OCR/transcription still running; retry later
- `skip_reason` on list items → **terminal** — do not retry read

## Security Boundary

- **Read-only by default** — only `note_save` writes; use only when user explicitly asks to create/edit a note
- **Never** echo API keys, LAN tokens, or `~/.linkly/credentials.json` contents
- **Do not** disable sandbox globally — request approval for the specific blocked command
- **Do not** exfiltrate document content beyond what the user task requires
- Notes content whitelist: no headings, code blocks, links, images in `note_save` — see MCP reference
- Tag policy: add tags only when user explicitly requests them

## Output Template

```markdown
## Document Search — {query}

**Mode:** MCP | CLI ({local|remote}) | **Libraries searched:** {list}
**Connection note:** {e.g. cloud library only, tunnel required}

### Results ({n} documents)
| Title | Type | Relevance | doc_id |
|-------|------|-----------|--------|
| ... | pdf | 0.82 | local://1044 |

### Key findings
- {bullet from snippets/outline/grep — cite doc title + line range}

### Sources read
- `{title}` — lines {from}-{to} via `read`

### Not searched / limitations
- {e.g. cloud libraries not reachable on local connection}
```

## Anti-Patterns

- Reading entire 200-page PDFs without outline/grep first
- Guessing `path_glob` instead of running `find_paths`
- Using `search` when user asked "list everything in folder" — use `list`
- Mixing `local://` and `cloud://` doc_ids in one MCP `outline` call
- Reporting "content not found" from local-only search when user has cloud libraries
- Retrying `read` on `skip_reason` / cloud-placeholder documents
- Piping cloud doc_ids through `xargs` (paths contain spaces — use stdin `-`)
- Inventing tags or writing notes without explicit user request

## Diagnostics

```bash
linkly doctor              # first step for any connection failure
linkly status              # index state, versions
linkly doctor --remote     # remote/tunnel checks
```

See `references/troubleshooting.md` for sandbox, Pro/Free gating, version mismatches, and gateway error codes.

## Cross-References

- Repo codebase search → use workspace `Grep`/`Glob`, not this skill
- Convert downloaded PDFs to Markdown → `markdown-convert`
- GitHub-hosted docs → `github-workflow` or `web-search`
