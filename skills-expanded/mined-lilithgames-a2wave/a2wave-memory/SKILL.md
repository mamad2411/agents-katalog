---
name: a2wave-memory
description: Progressively recall and maintain a2wave cross-session memory through a compact startup catalog, bounded topics, and searchable history.
---

# a2wave Memory

> a2wave platform memory overrides native Cursor / Claude Code / Codex memory.
> Never write memory to `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, or CLI-native memory files.
> Use the exact commands injected in `<recall_strategy>`; never assume a skill directory.

## Fast Recall

`MEMORY.md` is a compact startup summary and topic catalog. Detailed knowledge lives in bounded topic files.

1. Use the injected catalog to form a focused query.
2. Run `<memory-recall-command> "query"` once. It selects and returns at most one active topic while enforcing the disclosure budget.
3. Answer from that topic when sufficient. Do not list topics or read the same topic again.
4. Only when no topic matches, the topic is incomplete, or exact chronology is required, read [references/history-and-maintenance.md](references/history-and-maintenance.md).

If the user limits the answer to saved topics and says not to guess or to report absence, a no-match result is conclusive: stop and report that no saved topic matched. Do not list other topics or search history unless the user separately asks for historical evidence.

Never bulk-read topics. Read another topic only for a concrete cross-topic dependency revealed by the first result.

## Explicit Memory Mutations

Direct writes require an imperative request to remember, save to memory, add to a memory topic, update memory, or forget. A durable statement alone is not write authorization. Requests to only acknowledge or understand, and negated requests such as "do not save this", never authorize a write. Ordinary durable statements remain eligible for post-Run automatic extraction unless the user opts out of memory persistence for that Run. Explicit interactive mutations are authoritative and bypass post-Run worklog and insight persistence, avoiding duplicate or fallback writes; the Run and audit trail remain available.

### Add One Durable Item

Run exactly one server-routed write. Do not list or read topics first. Include `topicId` only when the injected catalog has an unambiguous match; otherwise let the server select or create the stable topic.

```bash
printf '%s' '{"title":"Build workflow","scope":"Repository build and validation","description":"Stable build conventions","keywords":["build","validation"],"section":"Workflows","items":["Build the shared package before API typechecking."]}' | <memory-write-command> --remember
```

Allowed sections: `Durable Knowledge`, `Decisions and Conventions`, `Workflows`, `Failure Patterns`, `Evidence Pointers`.

A successful response is the server confirmation: it has routed and deduplicated the item, enforced topic limits, rebuilt the catalog, and returned the resulting topic metadata. Do not read the topic again to verify it. If the command fails, do not retry or claim success. If it reports `LEGACY_SINGLE_FILE`, follow the compatibility flow in [references/history-and-maintenance.md](references/history-and-maintenance.md).

### Update or Forget Existing Content

These operations require a read-modify-replace flow. Read [references/history-and-maintenance.md](references/history-and-maintenance.md) before acting.

## Runtime Command Map

The injected `<recall_strategy>` defines:

- `<memory-recall-command>`: bounded one-topic recall (`memory-search.mjs --recall`)
- `<memory-search-command>`: topic/history search
- `<memory-topics-command>`: topic metadata only
- `<memory-read-topic-command>`: exact topic read by stable ID
- `<memory-write-command>`: explicit server-routed writer

Replace placeholders in full, including inside pipelines.
