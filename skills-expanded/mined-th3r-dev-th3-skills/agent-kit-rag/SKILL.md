---
name: agent-kit-rag
description: Give agents project memory without breaking the prompt cache. Keeps a local, Obsidian-compatible vault (claude-obsidian layout - hot, index, log, one note per decision, session or source) out of git, indexes it with stdlib BM25, and puts the retrieved notes into agent briefs after the cached prefix. Migrates a single progress or state file and a prompt log into vault notes. Use WHENEVER the work is "RAG", "retrieval", "project memory", "knowledge base", "Obsidian vault", "second brain", "move progress.md into notes", "agents keep forgetting decisions", "search past decisions", "claude-obsidian", "ความจำของโปรเจกต์", "ย้าย progress เป็น obsidian".
---

# RAG for agents, cache-safe

Tool: `uv run --script ${CLAUDE_SKILL_DIR}/scripts/vault.py <cmd> --vault DIR`. Stdlib only, and
nothing leaves the machine: chunks get a "title · type" prefix, with no LLM call and no embeddings.

The layout matches [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) (MIT), so its
plugin and Obsidian itself can open the same vault. Neither is required:

```
<vault>/
  .claude-obsidian.json   marks the vault
  inbox/                  raw sources waiting to be filed
  wiki/hot.md             what is happening now (replaced each pass)
  wiki/index.md           queue + links to every decision
  wiki/log.md             one line per change
  wiki/overview.md
  wiki/decisions/ sessions/ sources/ concepts/   one note each, frontmatter type/date/tags, [[links]]
  .vault-meta/bm25.json   derived; delete any time
```

| Command | Does |
|---|---|
| `init` | creates the layout; prints the `.git/info/exclude` line that keeps it local |
| `migrate --progress FILE [--prompts FILE]` | a single state file → notes: `## Now` → hot, `## Next` → index queue, each `## Decisions` table row → a decision note, each `## <stamp>` prompt-log entry → a source note. Re-running keeps existing notes (`--force` rewrites) |
| `note --type decision\|session\|concept --title --body` | the one write path while working; also appends to log (and index for decisions) |
| `hot --body` | replace hot.md |
| `index [--extra 'design/*.md' …]` | BM25 over `wiki/` plus repo docs; re-chunks only changed files |
| `query "<question>" [--top 5] [--json]` | the best passage per page: path, score, text |

## Rules

1. **Local only.** A vault inside a repo goes in `.git/info/exclude`, not `.gitignore`: nothing is
   committed, so it can't be pushed by accident. Check with `git check-ignore -v <vault>/wiki/hot.md`.
2. **One writer.** Only the main session (the lead in an agent team, `../team`) writes the
   vault. Worktree agents don't even see ignored files, so they get vault knowledge through their
   brief and report back; the lead files it.
3. **Retrieved text goes after the cached prefix.** `pcache.py brief "<task>" --rag <vault>` builds:
   outline → rules → hot.md → retrieved notes → role → task. The outline and rules are byte-stable
   across every agent; hot.md is the same for all agents of one pass; only the retrieved notes and
   the task differ. Put retrieval at the front and no two prompts share a prefix, so the cache
   never hits (`../prompt-cache`).
4. **Retrieval is a pointer, not proof.** A passage says where to look; the agent opens the note or
   file before relying on it.
5. **Re-index after writing** (`index` takes milliseconds on unchanged files) so the next brief sees new notes.

## Check

`uv run --script scripts/vault.py --selftest` covers migration parsing, decision and prompt notes,
BM25 ranking, an idempotent re-run, and incremental re-chunking. `../prompt-cache`'s self-test checks
that two RAG briefs are identical up to the retrieved notes.
