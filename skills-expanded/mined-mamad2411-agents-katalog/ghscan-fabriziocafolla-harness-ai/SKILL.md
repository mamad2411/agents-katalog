# wikictl - AI Memory System

wikictl is a file-based memory layer for AI agents. It manages a `wiki/` directory of Markdown files with YAML frontmatter metadata. No RAG, no vector DB, no embeddings — just files on disk that agents list, read, create, and edit through a CLI or, when a server is running, an MCP client.

This single skill covers all of it: when to use memory, reading/recalling, creating, editing, and the MCP alternative to the CLI.

## Core Concept: Metadata-First

The system uses metadata-first progressive disclosure to stay within context limits:

1. **Metadata level**: `wikictl list --json` or `wikictl search <query>` return only metadata (name, description, tags, timestamps) — no body content.
2. **Content level**: `wikictl read <name>` returns the full content of a specific entry.

Always start with `list` or `search` to understand what is available, then `read` only the entries you need. Never load all entries into context at once. See `references/progressive-disclosure.md` for the full rationale.

## When to Use Memory

| Intent | Operation | Section |
|--------|-----------|---------|
| Find, retrieve, recall information | Read | [Reading / Recalling](#reading--recalling) |
| Save, remember, persist new information | Create | [Creating](#creating) |
| Update, correct, append to existing information | Edit | [Editing](#editing) |
| An MCP client is connected and the wikictl server is running | MCP | [MCP Access](#mcp-access) |
| "forget X" / "delete the entry about Y" | Direct CLI | `wikictl delete <name> --force` — destruction, no workflow needed |

## Configuration

Wiki directory resolution (order of precedence):

1. `--wiki-dir <path>` CLI flag
2. `WIKICTL_DIR` environment variable
3. `./wiki/` relative to the current working directory (default)

## CLI Reference

| Command | Description |
|---------|-------------|
| `wikictl list` | List all entries (metadata only) |
| `wikictl list --json` | List as JSON array |
| `wikictl list --tag <tag>` | Filter entries by tag |
| `wikictl search <query>` | Text search over name and description (metadata only) |
| `wikictl search <query> --tag <tag>` | Combined text + tag filter |
| `wikictl tags` | List unique tags across all entries |
| `wikictl read <name>` | Read full content of one entry |
| `wikictl create -n <name> -d "<desc>" -t "<tags>" -b "<body>"` | Create a new entry |
| `wikictl edit <name> [-d desc] [-t tags] [-b body] [-s section]` | Edit an existing entry |
| `wikictl move <name> <folder>` | Move entry to a sub-folder |
| `wikictl delete <name> --force` | Delete an entry (requires `--force`) |
| `wikictl schema` | Print the entry metadata contract |
| `wikictl index` | Rebuild the `wiki/index.md` file |

## Reading / Recalling

1. **Scan**: `wikictl list --json` (or `wikictl list --json --tag <tag>` to narrow first). Returns `name`, `description`, `tags`, `created_at`, `updated_at` for every entry — no body content.
2. **Evaluate relevance** from name, description, and tag overlap with the current task. Select only entries that are likely relevant — do not read everything.
3. **Fetch**: `wikictl read <name>` for each relevant entry. Never guess a name; if it doesn't match what `list` returned, the read fails.
4. **Correlate** when multiple entries are relevant: look for connections via shared tags, note entries covering the same topic from different angles, and flag contradictions to the user instead of silently picking one.

A question spanning multiple topics (e.g. "how does our auth setup relate to our deployment process?") follows the same four steps: scan everything, identify entries from both domains, read both, synthesize — presenting both sides if they conflict.

## Creating

Create a memory entry for: decisions (architecture choices, technology selections), preferences (coding style, tool choices, naming conventions), context (domain terminology, team conventions), lessons (bugs and root causes, what worked/failed), procedures (setup, deployment, access).

Do NOT create entries for: ephemeral information, anything already documented in the codebase (README, CONTRIBUTING, inline docs), trivially retrievable information, or a duplicate of an existing entry (edit it instead, see [Editing](#editing)).

1. **Check for duplicates**: `wikictl list --json`. If a related entry exists, edit it instead of creating a new one.
2. **Choose a name**: kebab-case, specific (`react-state-management`, not `frontend-notes`), topic-based (never a date or session ID), 2-4 words.
3. **Write metadata**: a one-sentence `description` — the only text visible during `list`, so make it precise — and 2-4 `tags` from the shared [Tag Vocabulary](#tag-vocabulary).
4. **Create**:
   ```bash
   wikictl create \
     --name "descriptive-kebab-name" \
     --description "One sentence summary for progressive disclosure" \
     --tags "domain,tech,type" \
     --body "Full markdown content with all the details worth remembering"
   ```

Body guidelines: write Markdown, be concise but complete (include the reasoning, not just the conclusion). Decisions: state what was decided, why, and what alternatives were considered. Procedures: step-by-step with prerequisites. Preferences: the preference plus known exceptions. Lessons: problem, root cause, solution, how to avoid recurrence.

## Editing

Edit when new information supplements, corrects, or replaces an existing entry; create a new entry only when the topic genuinely has none yet. Rule of thumb: if `wikictl list --json` shows an entry on the topic, edit it.

`edit` is a partial update — only the flags you pass change:

| Flag | Behavior |
|------|----------|
| `--description` | Replaces the description |
| `--tags` | **Replaces the entire tag list** (not a merge) |
| `--body` | **Replaces the entire body** (not an append) |
| _(omitted)_ | Field remains unchanged |

`name` and `created_at` never change; `updated_at` is set automatically.

1. **Find**: `wikictl list --json`, identify the entry by name/description.
2. **Read first** if appending rather than replacing: `wikictl read <name>` to get the current body, so you can merge old and new content before writing `--body`.
3. **Apply**:
   ```bash
   wikictl edit <name> --description "New desc" --tags "a,b" --body "New content"
   ```

## MCP Access

When an MCP client is configured and the wikictl server is running, the same capabilities are available as MCP tools instead of CLI commands — same workflows (scan → evaluate → fetch/write), different transport.

Endpoint: `http://<host>:<port>/mcp` — default `http://127.0.0.1:9797/mcp` (local) or `http://localhost:9797/mcp` (Docker).

| Tool | Parameters | Returns |
|------|-----------|---------|
| `list_entries` | `tag?` (string) | Array of entry metadata |
| `read_entry` | `name` (required) | Entry metadata + body |
| `search_entries` | `q?`, `tag?` | Array of matching entry metadata |
| `list_tags` | _(none)_ | Sorted array of all unique tags |
| `create_entry` | `name`, `description` (required), `tags?`, `body?`, `section?` | Created entry metadata |
| `edit_entry` | `name` (required), `description?`, `tags?`, `body?`, `section?` | Updated entry metadata |
| `delete_entry` | `name` (required) | Confirmation object |

`edit_entry`'s `tags`/`body` replace rather than merge, exactly like the CLI. There is no confirmation prompt on `delete_entry` — it is permanent, and by default the server has no auth, so anyone who can reach it can CRUD the wiki.

## Tag Vocabulary

Use these categories to keep tags consistent across entries and operations. 2-4 tags per entry; avoid inventing one-off tags that will never be reused.

| Category | Example tags |
|----------|-------------|
| Domain | `architecture`, `security`, `performance`, `testing`, `observability` |
| Technology | `python`, `react`, `terraform`, `docker`, `postgresql` |
| Type | `decision`, `preference`, `procedure`, `lesson`, `convention` |
| Scope | `frontend`, `backend`, `infra`, `ci-cd`, `data` |

## Gotchas

- **Always list before read.** Never guess entry names — run `wikictl list --json` (or `search`) first, then `read`/`edit` by the exact name it returned.
- **Don't read everything.** Progressive disclosure exists to stay within context limits — evaluate metadata first, read only what's relevant.
- **Check for duplicates before creating.** A topic that already has an entry gets edited, not duplicated — duplicates fragment knowledge.
- **`--tags`/`--body` (CLI) and `tags`/`body` (MCP) replace, they don't merge or append.** To add to an existing body, `read` it first, combine old and new, then pass the full result.
- **Description is the only thing visible during `list`.** A vague one ("some notes") makes the entry invisible to future scans.
- **kebab-case names only.** Spaces, underscores, and camelCase cause issues.
- **`delete` requires `--force` on the CLI and has no confirmation over MCP.** Both are permanent.
- **Use `--json` for agent workflows.** Reliable to parse, unlike the human-readable table output.
- **If nothing relevant exists, say so.** Do not fabricate memories.
- **Conflicting information.** When memory conflicts with the user's current statement, present both and ask — don't silently prefer one.

## Examples

**"Remember that we chose PostgreSQL over MySQL for the auth service because of row-level security"**
```bash
wikictl list --json  # check for existing DB-related entries
wikictl create \
  --name "auth-service-db-choice" \
  --description "Decision to use PostgreSQL over MySQL for the auth service" \
  --tags "decision,architecture,postgresql" \
  --body "## Auth Service Database\n\nChose PostgreSQL over MySQL.\n\n**Reason**: PostgreSQL supports row-level security (RLS) natively, required for the multi-tenant auth model.\n\n**Alternatives considered**: MySQL (no native RLS), CockroachDB (too much operational complexity for team size)."
```

**"What do we know about our deployment process?"**
```bash
wikictl list --json --tag devops   # narrow by tag
wikictl read deploy-procedure      # read the relevant entry
```

**"Update the architecture entry — we switched from monolith to microservices"**
```bash
wikictl list --json
wikictl read project-architecture   # read current content first, since this is an append
wikictl edit project-architecture \
  --body "## Architecture\n\nMicroservices (previously monolith).\n\n**Update (2026-04-15)**: Migrated from a monolith to microservices for independent team deploys. Original monolith rationale no longer applies."
```

**Same read, over MCP:**
```
1. list_entries(tag="devops")
2. Evaluate results — "deploy-procedure" looks relevant
3. read_entry(name="deploy-procedure")
4. Present findings to the user
```
