---
name: relay
description: "Use when work should continue in a fresh session: the user says \"handoff\", \"hand off\", \"relay\", \"fresh session\", \"new session\", \"context is getting full\", \"give me a prompt for a new session\", or wants the work picked up in a different repo; when they paste a relay doc path to resume from; and to offer a scoped relay, unprompted, once context passes ~70%."
---

# Relay

A steerable replacement for `/compact`. Relay writes a short doc capturing what the current work *is* and where it's headed. A fresh session reads that doc and derives everything else itself.

Compaction keeps the whole conversation, lossily, and the user has no say in what survives. A relay keeps only what a new session cannot recompute, and the user says what matters.

## The one rule

**A relay doc carries narrative and pointers. Never status.**

Status is branch state, what's deployed, what's committed, which tasks are open, whether tests pass. All of it is derivable in seconds, and all of it goes stale between writing the doc and reading it. Narrative is why this approach, what was tried and abandoned and why, what the user decided, what is out of scope. None of that is recoverable from the repo.

| Write this | Not this |
|---|---|
| "work is on `feat/character-chat`" | "`feat/character-chat` is 3 commits ahead, uncommitted" |
| "the retry logic lives in `worker/queue.ts`" | "queue.ts is done and tested" |
| "tried polling first; it deadlocked under concurrent writes, so we moved to the listener" | "polling didn't work" |

## Offering a relay

When context passes ~70%, or the session has drifted across several topics, offer once, in one line, scoped to what is next: "Context is ~70%. Want a relay scoped to the migration so a fresh session picks it up?" Don't write it until the user says yes. Don't repeat the offer.

## Mode 1: write (`/relay <steering note>`)

The argument steers what carries forward ("focus on the webhook path"). Weight the doc toward it. With no argument, ask what the next session is for (one question), then write.

1. Slug: `basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"`. Timestamp: `date +%m%d-%H%M`.
2. Write to `~/.claude/relays/<slug>-<timestamp>.md` (`mkdir -p` first). Under 40 lines; longer means it's carrying status.
3. End with the closing block (below).

```markdown
# Relay: <slug>, <YYYY-MM-DD HH:MM>

**For the arriving agent:** this doc is narrative only. Derive current state yourself (git, tasks, tests) before you act on anything here. Then state your plan and wait for a go-ahead.

## What we're doing
<2-4 sentences. The goal and why it matters. Not a task list.>

## Where it stands
<Narrative only. "The listener is wired but nothing calls it yet.">

## Tried and ruled out
<Approach, and the specific reason it failed. The highest-value section.>

## Decisions made
<User rulings, with the reasoning. Binding on the next session.>

## Next
<What the user steered toward, first. Then anything else queued.>

## Pointers
- repo: <absolute path>
- branch: <name>
- files: <paths>
- tasks: <IDs>
- docs: <paths or URLs to specs, plans, reviews>

## Out of scope
<Things deliberately not being done, so the next session doesn't drift in.>
```

**Sanitize.** No API keys, tokens, passwords, connection strings, or personal data. Name them (`ANTHROPIC_API_KEY is set locally`), never their values.

## Closing block (every write ends with this)

The last lines of the reply, nothing after them:

1. The doc's absolute path (expand `~`).
2. The directory to open: the repo the next session runs in.
3. A fenced block, ready to paste, starting with the `cd`:

```
cd /Users/me/prj/my-app && claude "/relay /Users/me/.claude/relays/my-app-1031-1420.md"
```

Use the slash command, not "read this file": it loads this skill and its resume discipline in the fresh session.

## Mode 2: resume (`/relay <path>`)

If the argument resolves to a readable file, this is resume mode.

1. Read the doc.
2. **Derive current state before trusting anything.** Branch, dirty files, recent commits, whether the named files exist and what they contain now, open tasks. Cross-repo: read this repo's CLAUDE.md first.
3. Report anything that contradicts the doc. Drift is the signal that matters.
4. State the plan in a few lines and **wait**. Do not start work. The user ended the last session deliberately; they get to aim this one.

## Mode 3: cross-repo (`/relay --to <repo path> <steering note>`)

Use when the next piece of work happens in a different repo: this session found what another repo must change, or built the half that another repo consumes. The doc is a brief for a session that has never seen this repo.

- Slug is the **target** repo's basename; the directory to open is the target repo.
- Add a `## From <source repo>` section: what this repo did or needs, the contract between the two (endpoint, payload shape, function signature, env var names), and absolute paths to the source files that define it. Quote the contract itself if it is short; the arriving session should not have to open the source repo to start.
- Pointers name target-repo paths where you know them. Mark guesses as guesses.
- Tell the arriving agent to read the target repo's own CLAUDE.md first and to leave the source repo untouched unless the user says otherwise.

## Housekeeping

Relays are disposable. When writing one, if `~/.claude/relays/` holds files older than 30 days, mention the count and offer to delete. Don't delete unprompted.

## Common mistakes

- **Writing status because it feels helpful.** It is the one thing guaranteed to be wrong on arrival.
- **Restating what's in the repo.** If it's greppable, point to it.
- **A checklist instead of a narrative.** Task lists live in the tracker.
- **A `~` path or no `cd` in the closing block.** The user pastes it into a fresh terminal; it has to work as is.
- **The arriving session acting immediately.** A relay is a briefing, not an instruction.
