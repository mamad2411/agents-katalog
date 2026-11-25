---
name: searching-apple-notes
description: Search, recall, and create Apple Notes via semantic vector search powered by Qwen3-Embedding-0.6B and ChromaDB. Use when the user asks to find notes, search memos, recall what they previously wrote, needs note content as context for an answer, or wants to save an insight from the current conversation into Apple Notes. Triggers on phrases like "find in my notes", "search my notes", "what did I write about", "recall my note on", "do I have notes about", "save this to notes", "save this insight", "查我的笔记", "找一下我写过的", "存到备忘录".
---

# Apple Notes Semantic Search & Capture

This skill gives Claude semantic search over the user's Apple Notes archive and the ability to write new notes back. It uses Qwen3-Embedding-0.6B embeddings (1024-dim, multilingual, strong on Chinese-English mixed content) and ChromaDB. Searches understand meaning and synonyms — searching for "burnout" finds notes about "exhaustion" and "压力" even when neither word literally appears.

## Path resolution

The skill's helper scripts live next to this SKILL.md, in the `scripts/` subfolder. They figure out the parent repo's location automatically — there is nothing for the user or for Claude to configure. In the commands below, replace `SKILL_DIR` with the absolute path of this skill folder, which is wherever the user copied it (typically `~/.claude/skills/searching-apple-notes/` or `<project>/.claude/skills/searching-apple-notes/`).

## Prerequisite check

Before the first search of a session, verify the index exists by running:

```bash
python3.12 SKILL_DIR/scripts/vector_search.py --stats
```

If this returns an error about ChromaDB not being found, the user has not completed the setup steps in the parent repository. Tell them to follow the install instructions in the repo README and then come back. Do not proceed.

## Searching

```bash
# Default: full-corpus semantic search, 10 results
python3.12 SKILL_DIR/scripts/vector_search.py "query text"

# Specify result count
python3.12 SKILL_DIR/scripts/vector_search.py "query text" -n 20

# Filter by Apple Notes hashtag
python3.12 SKILL_DIR/scripts/vector_search.py "query text" --tag TagName

# Filter by Notes folder name
python3.12 SKILL_DIR/scripts/vector_search.py "query text" --folder FolderName

# Date range filter
python3.12 SKILL_DIR/scripts/vector_search.py "query text" --after 2025-01-01
python3.12 SKILL_DIR/scripts/vector_search.py "query text" --before 2025-12-31

# Combine filters
python3.12 SKILL_DIR/scripts/vector_search.py "query text" --tag Ideas --after 2025-06-01

# Index health snapshot
python3.12 SKILL_DIR/scripts/vector_search.py --stats
```

The script returns a JSON array. Each result has: `rank`, `title`, `score`, `snippet` (first 500 chars), `updated`, `folder`, `tags`, `id`.

## When to search

Reach for `vector_search.py` whenever the user:

- Asks "what did I write about X" / "find my notes on X" / "do I have notes about X"
- References past thinking ("remember when I noted...", "I wrote something about this before")
- Needs to recall a fact, quote, or idea they previously captured
- Is researching a topic where their personal prior thinking is relevant context

## When NOT to search

- General knowledge questions unrelated to personal notes ("what is the capital of France")
- Live information that obviously would not be in personal notes (current news, code in the active repo, etc.)
- The user is dictating new content to be saved — use `create_note.py` instead

## Search strategy

1. **Default fetch size**: start with `-n 5`. Bump to 10 or 20 only if the user asks for "more" or the first batch is clearly insufficient.
2. **Phrase queries the way the note would be written.** Semantic search rewards specific concrete terms. "ideas about onboarding friction in B2B SaaS" works better than "onboarding stuff".
3. **Iterate if the first search misses.** If the top results are off-topic, try a different phrasing or a synonym before giving up. Two attempts is usually enough.
4. **Mix languages freely.** Qwen3-Embedding-0.6B handles Chinese-English mixed queries natively. If the user writes "find my notes about 心流 and flow state," send the query as-is.
5. **Use `--tag` only when the user explicitly mentions a tag they use.** Otherwise full-corpus search is broader and usually better. If a tag-scoped search returns nothing, retry without the tag.
6. **Use `--folder` only when the user explicitly mentions a Notes folder by name.**
7. **Use `--after` / `--before` when the user mentions a time window** ("last month", "since January", "before the trip").

## How to interpret and present results

The `snippet` field is preview-only — first 500 characters of the note body. For most questions the snippet contains enough context to answer.

If the user explicitly asks for the *full content* of a specific note from the result list, fetch it:

```bash
# Single note by Notes.app index
python3 SKILL_DIR/scripts/get_note.py --index 5

# Multiple notes
python3 SKILL_DIR/scripts/get_note.py --indices 1,5,12
```

**Always cite which note(s) the answer came from by title.** Do not synthesize an answer that pretends to come from "the notes" without naming which ones. If two notes contradict each other, surface both rather than picking one silently.

## Index freshness

If the user mentions they just added a note and search does not find it, run a sync first:

```bash
python3.12 SKILL_DIR/scripts/sync_index.py
```

This re-exports from Notes.app, bridges native hashtags, and incrementally updates the vector index. Only notes modified since the last sync get re-embedded — usually finishes in seconds.

If `--stats` shows fewer indexed notes than the user reports having, suggest running `sync_index.py`.

## Saving insights to Apple Notes

When the user discusses a topic in conversation (an article, a piece of news, a brainstorm) and asks to save the conversation as a note, use `create_note.py`:

```bash
# Inline body
python3 SKILL_DIR/scripts/create_note.py "Note title" "Body content with #Tag1 #Tag2"

# Specific folder
python3 SKILL_DIR/scripts/create_note.py "Note title" "Body" --folder "Notes"

# Pipe a longer body via stdin
echo "long body content" | python3 SKILL_DIR/scripts/create_note.py "Note title" --stdin
```

Hashtags written as `#TagName` in the body become real Apple Notes hashtags automatically — no escaping needed.

### Workflow: dialogue → insight → note

1. The user discusses a topic (article, news, brainstorm)
2. The user says something like "save this to notes" or "save this insight" — they may or may not specify a tag
3. Claude condenses the dialogue into a tight insight (2-3 sentences of the key takeaway, plus the supporting context)
4. Claude calls `create_note.py` with the user's specified tag(s) embedded as `#Tag` in the body
5. Claude confirms the new note ID

### Note format convention

Use this structure unless the user asks for something different:

```
# [Insight title]

[2-3 sentence summary of the key insight]

## Context
- Source: [URL or conversation topic]
- Date: [YYYY-MM-DD]

## Key takeaways
- [Bullet point]
- [Bullet point]

#Tag1 #Tag2
```

## Notes on Python versions

- **Searching, syncing, and stats** require `python3.12` because `chromadb` and `sentence-transformers` (Qwen3-Embedding-0.6B) are pinned to that version in the parent repo.
- **Creating notes and fetching note content** only need `python3` — they just call AppleScript via `osascript` and have no Python dependencies.
- The first search of a session takes ~10 seconds because Qwen3-Embedding-0.6B has to load. After that, queries are sub-second.
