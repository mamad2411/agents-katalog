---
name: workflows
description: When and how to use the repoindex plugin surface (MCP tools, agents, slash commands) for collection queries, release prep, activity summaries, and tag discipline. Use when users ask repoindex questions, mention their repo catalog, or want to know which repoindex tool fits their task.
---

# repoindex: which tool for which task

The plugin exposes three layers. Pick the smallest one that answers the question.

| Layer | Use when |
|-------|----------|
| MCP tool calls (`run_sql`, `get_manifest`) | Single question, clear query, one answer. |
| Slash commands (`/repo-week`, `/repo-status`, `/repo-audit`, `/repo-sprint`, `/repo-mirror`) | Named recurring task with a fixed shape. |
| Agents (`repo-polish`, `repo-explorer`) | Multi-step reasoning, prose synthesis, or file writing. |

## Picking the layer

### Use raw MCP when the user asks one question

"Show me my Python repos" is one `run_sql`. Do not invoke an agent. Do not reach for a slash command.

```sql
SELECT name, path FROM repos WHERE language = 'Python' ORDER BY name
```

Same for "how many repos do I have", "which repos are on PyPI", "what are my most starred repos". Direct SQL wins.

### Use a slash command for recurring shaped queries

These have a known output format and the user invokes them by name:

- `/repo-week [window]`: activity rollup via `repoindex digest`. Top churn, releases, totals.
- `/repo-status [name]`: collection overview or single-repo detail card.
- `/repo-audit [filters]`: read-only per-check summary of `ops audit` findings.
- `/repo-sprint`: the triage entry point. "What needs attention / what's open?" (dirty, unpushed, active, release candidates, audit gaps, stale, unpublished).
- `/repo-mirror [flags]`: dry-run-first wrapper around `ops mirror` for redundancy pushes.

Slash commands never write files on their own (mirror is the one exception, and only with `--force-real`).

### Use an agent for multi-step or prose work

- `repo-polish`: single-repo release prep. Audits, generates citation/license/codemeta, writes README improvements, syncs GitHub metadata. Writes files.
- `repo-explorer`: open-ended analysis. Custom SQL across multiple tables with narrative synthesis.

## Common patterns

### Language-filtered audit

```
/repo-audit --language python --severity critical
```

Summary first. If the user wants to fix a specific repo, hand off to `repo-polish`.

### Release prep flow

1. `/repo-status <name>` to confirm state.
2. `repo-polish` agent for the full audit-fix-improve cycle.
3. `/repo-audit --language <lang>` after the release to confirm nothing regressed collection-wide.

### Cross-platform status

```sql
SELECT r.name, p.registry, p.package_name, p.current_version, p.published, p.downloads_30d
FROM repos r JOIN publications p ON p.repo_id = r.id
WHERE p.published = 1
ORDER BY p.downloads_30d DESC NULLS LAST
```

Direct SQL. No agent needed. Join `tags` if filtering by classification.

### Weekly standup for myself

```
/repo-week 7d
```

Or `30d` for a monthly rollup.

## Tag strategy

Tags live in the `tags` table. The `source` column says where a tag came from: `user` for tags assigned via `mcp__repoindex__tag`, everything else derived during refresh (repo state, forge topics, project keywords, registries). Query the current set rather than assuming it:

```sql
SELECT source, COUNT(*) FROM tags GROUP BY source
```

Naming conventions for user tags:

- `work/<area>` for work-in-progress groupings: `work/active`, `work/paused`, `work/release-queue`.
- Do not reuse the `prefix:` namespaces that derived tags occupy (`lang:`, `topic:`, `keyword:`, `has:`, `published:`; check with `SELECT DISTINCT substr(tag, 1, instr(tag, ':')) FROM tags WHERE instr(tag, ':') > 0`).
- Project-domain tags: short nouns like `ml`, `cli`, `dsl`, `paper`, `plugin`.

Use `mcp__repoindex__tag` to add/remove user tags. Filter by tag with the `--tag` flag (accepted by `copy`, `link`, `ops` subcommands, and `export`; supports `*` wildcards, for example `--tag 'work/*'`), or from `run_sql` with the `EXISTS (SELECT 1 FROM tags t WHERE t.repo_id = r.id AND t.tag = '...')` pattern.

## Anti-patterns to avoid

- Do not invoke `repo-explorer` for a question that is one `run_sql` call.
- Do not run `/repo-sprint` for single-repo questions. That is `/repo-status` or `repo-polish`.
- Do not run `repoindex ops` commands without `--dry-run` on the first pass. `/repo-mirror` enforces this; other ops commands rely on the user choosing.
- Do not bypass MCP. The CLI and the MCP server share a database, but MCP is the canonical read path inside Claude Code sessions.

## Quick reference

```
Single question        → run_sql
Weekly rollup          → /repo-week
Glanceable status      → /repo-status
Read-only audit        → /repo-audit
Triage / kickoff       → /repo-sprint
Redundancy push        → /repo-mirror
Release prep (writes)  → repo-polish agent
Ad-hoc deep analysis   → repo-explorer agent
```
