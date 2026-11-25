---
name: memory
description: Remember durable facts across sessions and recall only the few relevant ones under a strict budget — never bulk-injected. Use when the user says "remember this", asks "what do you remember about…", wants a preference or decision saved, or when a stored fact would materially help the current task.
allowed-tools: Bash, Read, Write
---

# Durable memory

Resolve the plugin root before shelling out: use `${CLAUDE_PLUGIN_ROOT}` if it is set; otherwise
resolve `../..` relative to this SKILL.md to an ABSOLUTE path (bash cwd is not the skill dir).
Call that root `$ROOT` below.

## Recall (the default operation — pull, on demand)

Before relying on memory for a task, derive 5–15 salient keywords from the task at hand —
nouns, tool names, file names, error strings — never a whole prompt. Then run:

```bash
python3 "$ROOT/bin/memory_recall.py" --query "<keywords>"
```

Treat the returned block as advisory context, not ground truth. A fact whose header line is
flagged stale (the recall engine appends `— STALE, verify before relying`) must be re-checked
against the repo or reality before you act on it — do not treat a stale fact as current.

`no memory above the relevance gate for this query` is a SUCCESS, not a failure: proceed
without memory. Do not loosen or repeat the query with broader terms just to force a match —
an empty recall means nothing relevant and durable is stored, and that is the system working
correctly.

Useful flags: `--max-facts N` / `--budget-chars N` to tighten the cap further than the
defaults, `--include-expired` only for review-style flows (never for normal task recall),
`--json` for scripting, `--now YYYY-MM-DD` to pin date math.

## The effectiveness contract

Memory must never make answers worse. Never bulk-inject: do not paste `memory/index.md`,
the store directory, or uncapped fact sets into context — recall goes through
`bin/memory_recall.py` and its budget (at most 5 facts / 4000 chars by default), always.
Expired facts are withheld, stale facts arrive down-ranked and flagged, and an empty
recall is the system working as designed.

## Save

Worth remembering: durable user preferences, decisions plus their rationale, environment
facts, and corrections the user gave you. NOT worth remembering: anything the repo or
CLAUDE.md already records, secrets or credentials, and transient state that won't matter
next session.

```bash
python3 "$ROOT/bin/memory_store.py" add --name "..." --type <user|feedback|project|reference|decision> --description "..." --tags a,b --body "..."
```

Always set meaningful `--tags` — they are the retrieval hooks that rescue a fact from the
lexical ranker's blindness to synonyms and paraphrase. `--slug`, `--expires`
(`YYYY-MM-DD` or `never`), `--confidence` (`high|medium|low`), and `--source` are optional
but worth setting when known.

If `add` exits 2 with `duplicate of [<slug>] — update it instead (or pass --force)`, UPDATE
that fact instead of forcing a duplicate:

```bash
python3 "$ROOT/bin/memory_store.py" update <slug> --description "..." --body "..." --tags a,b
```

Update over duplicate, always — an update also bumps `last_verified`, so it doubles as a
freshness refresh. If the user says a stored fact is wrong, remove it immediately:

```bash
python3 "$ROOT/bin/memory_store.py" remove <slug>
```

## Review & prune

Periodically, or whenever the user asks "what do you remember" / "what have I told you to
remember":

```bash
python3 "$ROOT/bin/memory_store.py" review
```

This is a read-only staleness report grouped expired-then-stale. For each fact it surfaces,
either `verify <slug>` (still holds, just bump freshness), `update <slug> ...` (drifted —
rewrite the fields that changed), or `remove <slug>` (dead). `python3 "$ROOT/bin/memory_store.py" list`
shows every stored fact with its freshness state, for a full picture rather than just the
stale ones.

## Privacy

The store lives under the gitignored `memory/` directory at the plugin root — local-only,
never committed, and it holds only what the user chose to remember. Recalled text enters
the model's context because that is its purpose; nothing else in the store does.
