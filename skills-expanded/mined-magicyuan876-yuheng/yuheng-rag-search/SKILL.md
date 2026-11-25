---
name: yuheng-rag-search
description: Use when retrieving from or asking questions against a Yuheng knowledge base via the `yuheng` CLI — and especially when unsure whether to use `chat` or `search chunks` for a given goal.
metadata:
  tested_against: v0.10
---

# Yuheng — retrieval & RAG queries

**REQUIRED BACKGROUND:** read the `yuheng-shared` skill first (auth, `--kb`
resolution, the JSON envelope, exit codes, streaming/NDJSON output).

Yuheng gives you several ways to "ask about a knowledge base." Picking the wrong
one wastes turns or returns the wrong shape. Use the decision table.

## Pick the command by your goal

| Your goal | Command | LLM synthesis? | Returns |
|---|---|---|---|
| Natural-language **answer** grounded in a KB | `chat "<q>" --kb <kb>` | yes | bounded answer events; `--reference` adds citations; `--verbose` adds execution detail |
| **Raw context chunks** to reason over yourself (no answer) | `search chunks "<q>" --kb <kb>` | no | ranked chunk list |
| Which **documents** match a keyword (title/filename) | `search docs "<q>" --kb <kb>` | no | document list |
| Find a **knowledge base** by name | `search kb "<q>"` | no | KB list |
| Find a past **session** by title | `search sessions "<q>"` | no | session list |

### The decisions that matter

1. **Answer vs raw context.** Want a written answer → `chat`. Want chunks to
   feed into your *own* reasoning (e.g. you'll synthesize across sources) →
   `search chunks`. Don't call `chat` just to read source text.
2. **One-shot vs multi-turn.** `chat` returns a `data.session_id` in default
   JSON output. Pass `--session <id>` on the next call to continue the
   conversation. In NDJSON mode, read it from `init`.

## Safety / Gotchas

- `chat`, `search chunks`, `search docs` need a KB: pass `--kb <id-or-name>`, or
  set `YUHENG_KB_ID`, or `yuheng link` the directory (resolved in that order).
  If none resolves it's exit 1 (`local.kb_id_required`); a bad name is exit 1
  (`local.kb_not_found`). Resolve names with `yuheng kb list` / `search kb`.
  (`search kb` / `search sessions` are tenant-wide and take no `--kb`.)
- `chat` returns one buffered JSON envelope with answer events by default. Add
  `--reference` for indexed citations and `--verbose` for execution detail; use
  `--format ndjson` for raw events or `--format text` for the live
  human-readable projection.
- A stalled stream is not stopped by Ctrl-C (that just drops your local
  connection; the server keeps generating + billing). Stop it server-side:
  `yuheng session stop <session-id> --message <message-id>` (session_id from
  `data.session_id`, or from `init` under `--format ndjson`).
  Re-attach to a stream with `yuheng session resume <session-id>
  --message <message-id>`.
- `search chunks --limit` defaults to **8** (tuned for an LLM context window);
  the `search docs/kb/sessions` lists default to 30. Tune retrieval with
  `--vector-threshold` / `--keyword-threshold`, or `--no-vector`/`--no-keyword`
  to disable a channel. Details: `references/search-chunks.md`.

## Quick examples

```bash
# raw retrieval to reason over
yuheng search chunks "retry backoff policy" --kb engineering --limit 12

# grounded answer (human transcript)
yuheng chat "How do we handle retries?" --kb engineering --format text

# continue the conversation (session id from data.session_id above)
yuheng chat "And the max attempts?" --kb engineering --session sess_abc
```
