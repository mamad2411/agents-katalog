---
name: wiki-sync
description: Session-close routine that writes durable knowledge into a markdown knowledge base - a log entry in a fixed format, updated pages, a refreshed index. Use at the end of any session that produced real work, so the next session starts informed instead of re-deriving what this one learned.
---

# Wiki Sync

A session that is not logged did not happen, as far as the next session is concerned.

This is the close-out routine: decide what is durable, write it where the next session will
actually read it, and flag honestly what is still open.

## The knowledge base

Any directory of markdown files works — an Obsidian vault, a `docs/` folder, a wiki. What
matters is the shape:

```
log.md                chronological, newest first. The entry point
index.md              table of contents and current status
entities/             people, organisations, standing facts
projects/<name>/      one directory per project
concepts/             frameworks and reusable thinking
```

**One canonical location.** A second mirrored copy will drift, and then no session knows which
one is true. If a mirror exists, delete it.

## Load first

1. `log.md` — your entry goes at the **top**
2. `index.md` — update if pages were created or a status changed
3. The specific pages this session touched

## Steps

### 1. Decide what is durable

The knowledge base records:

- What shipped
- What was decided, **and why**
- What is still open
- Which files are canonical

It does **not** record what other tools already know: code structure, git history, one-off chat.
Duplicating those is how a knowledge base becomes noise nobody reads.

### 2. Update the pages first

Edit the existing page rather than creating a near-duplicate beside it. Only create a new page
for a genuinely new project or concept — and then add it to `index.md` in the same pass, or it
is invisible.

*The failure this prevents:* when a project's positioning changed, the fix was editing the
existing entity page in place. Writing a new note beside the stale one would have left two
contradictory answers with no way to tell which was current.

### 3. Write the log entry

At the top of `log.md`, in a fixed format:

```markdown
## [YYYY-MM-DD HH:MM] type | title → pages touched

- **Bold the key phrase**, then the concrete detail. File paths, counts, versions, hashes
- One bullet per real thing that happened. Three to six total
- Flag anything incomplete as **UNRESOLVED, needs user** — never round a partial fix up to done

**Pages updated:** path/one.md, path/two.md
**Pages created:** path/three.md
```

Types in use: `build` · `feature` · `fix` · `maintenance` · `analysis` · `decision` ·
`ingest` · `github` · `design` · `project-setup`.

### 4. Refresh the index

New page links, status changes, and the "last updated" date at the top.

### 5. Convert relative dates to absolute

"Yesterday" → the actual date. "Last week" → the actual week. Relative dates are worthless the
moment the session ends, and actively misleading six months later.

## What a good entry looks like

```markdown
## [2026-07-01 21:26] fix | Tracker found frozen since April; 3 missing records recovered

- **Audited the tracker and its merge pipeline** — found it **frozen at 2026-04-20 with only 4
  entries**, despite three records having actually been created since, traced via output files
- **Recovered and filed the missing three**, with matching reports 005, 006, 007
- **Added a lane classification** so category fit can be read at a glance
- Tracker now: **7 tracked** (4 active, 3 evaluated-not-sent). Scheduled scan still
  **UNRESOLVED** — the OS blocks the scheduler from reading that directory, needs a GUI
  permission change only the user can make

**Pages updated:** entities/profile.md, log.md
```

Note the shape: specific numbers, real file references, an honest failure, and one thing
explicitly flagged as needing the user.

## Mistakes that have actually happened

- **Skipping the sync is how a tracker froze for ten weeks.** Three records were created without
  being logged, and nothing noticed until an audit. If the session changed something, sync it.
- **Do not summarise vaguely.** "Fixed the scanner" is wrong. "2 dead endpoints → 6 live, 514
  results found" is right. Specificity is the entire value.
- **Flag the unresolved.** An entry that says "UNRESOLVED, needs user" saves the next session
  from confidently building on a broken foundation.
- **Update, do not duplicate.** Two pages disagreeing is worse than one page being out of date,
  because at least the stale page is honestly stale.
