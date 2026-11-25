---
name: work-notes
description: The per-worktree work-notes format for the desktop-terminal work dashboard — where the note lives (one Obsidian vault note per branch, under ~/Developer/Work/Notes/Worktrees/), how to write it (title, Type, Status token + text, Recap, Plan, TODO), and how it gets archived. Use whenever you create, draft, refresh, or edit a worktree's notes, or need the notes convention. Pairs with start-work, resume-work, promote-work, and archive-work.
---

# Work Notes — one vault note per worktree

The per-worktree memory the desktop-terminal work dashboard reads. One note per
branch, living in the Obsidian vault. This skill is the single source of truth
for both **where** it lives and **what shape** it has — start-work, resume-work,
promote-work, archive-work and the dashboard's create/draft prompts all defer
here.

## Where the note lives

```
~/Developer/Work/Notes/Worktrees/<branch>.md
```

Filename = the branch with every character outside `[A-Za-z0-9._]` collapsed
to `-`:

| branch | note |
|--------|------|
| `LAKE-9970` | `Worktrees/LAKE-9970.md` |
| `tim/stroke-profiling-rig` | `Worktrees/tim-stroke-profiling-rig.md` |
| `release/4.31.0` (main checkout) | `Worktrees/release-4.31.0.md` |

- **Not in the worktree.** `.work/` inside a checkout is scratch space (logs,
  artifacts) and is git-ignored; notes are no longer kept there. A repo *outside*
  `~/Developer/Work/` still falls back to `<worktree>/.work/notes.md` — same
  format, different location.
- **Never rename a live note.** Three places derive that filename from the
  branch independently — `notes_slug` in the dashboard's `work.lua`, worktrunk's
  `post-start` hook, and you. Renaming (Obsidian's rename included) orphans the
  note: the dashboard looks for the branch-derived name, finds nothing, and a
  fresh empty scaffold takes its place. Rename only when archiving.
- **One note per branch, not per checkout.** Re-adding a worktree for a branch
  picks its existing notes back up.
- **It outlives the worktree** — that's the point of the move. `wt remove` no
  longer takes the notes with it; see **Archiving**.
- **It's a vault note**, so `[[wikilinks]]` to other notes work (link the plan
  note, a term, a recap) — but keep them out of `Status:` and `## Recap`
  (see Formatting rules).
- **The vault documents its own conventions** in `~/Developer/Work/Notes/Home.md`
  — folders, what a term note is versus a finding, how notes are written. Read it
  rather than trusting a folder list copied into a skill; this skill owns only the
  worktree note's format.

## One note, one thing

**Notes stay small and focused.** A worktree note answers "what is this, where
does it stand, what's next" — nothing more. When an idea wants room to breathe,
it becomes **its own note, linked**, not another section here:

- A design/approach that outgrows a few bullets → a note in `Plans/`, referenced
  by a `Plan: [[note name]]` line (the dashboard keeps that line off the card).
- A measurement run, a root-cause write-up, a ruled-out list, a decision record →
  its own note in `Findings/`, linked from `## Plan` with a one-line summary of
  what it concluded.
- Durable engine/app knowledge → the in-repo docs, linked the same way.

The test: if a section of the note would still be worth reading after this branch
is gone, it belongs in its own note. Splitting also keeps the card honest — the
dashboard only surfaces the top of this file, so buried depth is invisible anyway.

**Link in prose, never as a metadata field.** When the work belongs to a subject
the vault already has a **term note** for (`Replay`, `Strokerec`, `App Clip size
budget` — aliases resolve `[[Timelapse]]`, `[[strokerec]]`), use the term inside
the sentence that states the relation — "the replay path behind `[[Replay]]`" —
because that sentence is what shows in the term's backlinks. Don't add a
`Part of:`/`Hub:` line: it
flattens every relation into membership, implies a single parent for notes that
sit in two threads, and gives the backlink nothing to display.

## Write tight

These notes are a scratchpad to reload context fast — signal, not a report.
Default to **short, concise, and packed with information**. Every line earns its
place:

- **Lead with the fact, cut the windup.** "resumeQuery fix; awaiting Lazar QA" —
  not "We have now pivoted to an approach where…".
- **No marketing lingo, no hedging.** Drop "clean", "robust", "beautiful",
  "comprehensive", "successfully". State what is, what's decided, what's next.
- **Don't restate what git/PR/Jira already shows** (commit messages, diffs, PR
  status, ticket fields). Capture only what those *can't* tell a future reader.
- **Keep the top short.** Title + `Type:` + `Status:` + Recap are the high-traffic
  lines — a few words over and they stop being skimmable. Push detail downward.
- **Bullets over prose** for anything past a sentence or two; one fact per line.

If a line wouldn't help you in a week, delete it.

## The shape

```markdown
# <KEY> — <short title>          ← or `# tim/<slug>` for an exploration

Type: Bug                        ← ONLY for a Jira Bug; omit otherwise
Status: <token> — <one line on where this stands right now>

## Recap
<1–2 sentences: what this worktree is about. Only this first paragraph shows
on the dashboard, so keep it tight.>

## Plan
<approach + next steps as terse bullets — off the card, but still dense, no narrative>

## TODO
- [ ] <first concrete step>
- [x] <done step>
```

## Field by field

- **Title** `# <KEY> — <title>` (real ticket) or `# tim/<slug>` (exploration).
- **`Type: Bug`** — add this line *only* when the linked Jira issue is a Bug. It
  makes a red bug glyph (󰃤) appear in the worktree's header. Omit it for
  non-bugs and explorations (no glyph for other types — that's intentional).
- **`Status: <token> — <text>`** — the live "where this stands" the dashboard
  can't derive from git/PR signals. The widget colour-codes the `<token>`; the
  free text is markdown-styled (bold/`code`/links handled) and wraps to ~2 lines.
  A bare `Status: <token>` (no text) is fine. Tokens:

  | token     | colour | use when…                                     |
  |-----------|--------|-----------------------------------------------|
  | `blocked` | red    | waiting on someone/something external         |
  | `qa`      | accent | out for QA / awaiting on-device verification  |
  | `review`  | accent | PR is up, awaiting review                     |
  | `wip`     | accent | actively coding (a new exploration starts here)|
  | `ready`   | green  | done locally, ready to open/merge the PR      |
  | `done`    | merged | merged / shipped                              |

  Aliases resolve too (e.g. "Ready for QA" → `qa`, "in progress" → `wip`), but
  prefer a bare token. Example:
  `Status: qa — build out to Lazar via Firebase, verifying on iPad 8th Gen`.
- **`## Recap`** — *what this is*, 1–2 sentences, max. Keep it distinct from
  Status: Recap = what, Status = where it stands. They render as separate lines.
- **`## Plan`** — approach + next steps. Off the card, so length isn't *rendered*,
  but still write it tight: terse bullets of decisions/facts, not a narrative of
  how you got here. Dense beats long.
- **`## TODO`** — a checklist. One item per line, `- [ ]` for open and `- [x]`
  for done (a capital `- [X]` also counts). The done/total tally drives the
  progress bar, so keep boxes ticked as you go.

## Formatting rules

- **Markdown, standard.** Sections are `##` headings; the title is a single `#`.
- **One paragraph = one line — do NOT hard-wrap prose at 80 columns.** The Recap
  and the `Status:` text are each a single logical line; the dashboard wraps them
  to the card width itself. A manual newline mid-paragraph breaks the wrap (and a
  wrapped `Status:` line loses its tail). Let lines run long. *(Lists are the
  exception: one item per line.)*
- **Lists:** TODO items are checkboxes (`- [ ]` / `- [x]`); other bullets use
  `-` or `*`. The Recap may be prose *or* a short bullet list — either is shown.
- **Inline styling is fine** in the Recap and Status text: `**bold**`, `` `code` ``,
  and `[links](url)` all render (markers are dropped, code is highlighted). Don't
  rely on it for meaning, though — it's flattened to ~plain text on the card.
- **`[[wikilinks]]` only from `## Plan` downward.** The dashboard flattens
  markdown links but prints `[[…]]` verbatim, so a wikilink in `Status:` or
  `## Recap` shows its brackets on the card. In `## Plan` (or a `Plan:` metadata
  line, which the dashboard keeps off the card) they're the right way to point at
  a vault plan: `Plan: [[LAKE-9926-multiview-stage4-background-blur]]`.
- **Top of file, in order:** title → optional `Type:` → `Status:` → `## Recap`.
  Keep these first; put long-form detail under `## Plan` or extra sections below.
- **Don't dump a metadata table at the top** (Priority/Assignee/Reporter/etc.) —
  it's noise on the card. Title + `Type:` + `Status:` carry what's surfaced; the
  Jira link covers the rest.

## How the dashboard parses it (so you know what shows)

- **Recap** = the first paragraph of the `## Recap` section (or, lacking that
  heading, the first prose paragraph). Metadata lines and pure Jira-link lines
  are skipped, so they never leak into the recap.
- **Status** = the `Status:` line (token + text). If the line has only a token,
  the text is backfilled from a `## Status` / `## Current status` section.
- **bug glyph** = presence of a `Type: Bug` line.
- **TODO bar** = checkbox tally across the whole file.
- **Jira link** = the first `LAKE-####` key found anywhere (line or branch name).

## Keeping it current

- Refresh `## Recap` and tick `## TODO` as you work — a recap older than the tip
  commit raises a "notes stale" nudge on the dashboard.
- **Flip the Status token as the work moves:** `wip` → `review` (PR up) → `qa`
  (out for QA) → `blocked` (waiting on someone) → `ready`/`done` (it lands).
- If you re-read the linked Jira issue's **comments** (QA posts pass/fail there),
  reflect what changed in both the token and the Status text.
- **Rewrite, don't append.** Edit lines in place as reality changes; superseded
  notes are noise. The file should stay roughly the same size, not grow each pass.
- Editing the note in Obsidian is equivalent to editing it here — same file, and
  saving it clears the stale nudge either way.

## Archiving

`Worktrees/` should list only **live** work. When a branch is done (shipped,
merged, abandoned) its note gets a closing recap and moves to
`Worktrees/Archive/<YYYY-MM-DD> <descriptive name>.md` — the rename is safe
*there*, because nothing derives that name from the branch any more. The
**archive-work** skill owns that flow; use it rather than moving files by hand.

Two things do it for you, imperfectly:

- The dashboard's `x` (remove worktree) moves the note to
  `Archive/<YYYY-MM-DD> <branch-slug>.md` with **no recap** — a floor against
  loss, not a substitute for archive-work. Run archive-work *before* `x` and the
  removal finds the note already filed.
- Nothing at all happens on a plain `wt remove` from the CLI. The note stays in
  `Worktrees/` looking live. **A note whose worktree no longer exists is a
  leftover** — archive it.

## Updating an existing note

When asked to bring an existing note up to this format:

1. **Set the top block.** Ensure the first lines are `# <KEY> — <title>`, then a
   `Type: Bug` line *only* if it's a bug, then one `Status:` line. If the file
   has an old `**Type:** · **Status:** · …` metadata block, collapse it: keep
   `Type: Bug` (drop it for non-bugs), turn its status into a `Status: <token> —
   <text>` line (map the Jira status — e.g. "Ready for QA" → `qa`), and delete
   the Priority/Assignee/Reporter/Branch/etc. clutter (the Jira link covers it).
2. **Ensure a `## Recap`** holding *what this is* (1–2 sentences). If the only
   real summary lived in a `## Current status` section, split it: the durable
   "what" goes in Recap, the "where it stands now" goes in the `Status:` line.
3. **Keep the *valuable* depth, prune the rest.** Hold onto root-cause findings,
   test matrices, references, and live plans — under `## Plan` or their own
   sections — but drop stale, superseded, or now-obvious content as you go.
   Compress, don't copy: the reshape is a chance to cut, not just relocate.
4. **Pick the token** that matches reality right now (see the table above), and
   make the Status text a single tight line.

Pass a branch or worktree path (or "all worktrees") and migrate each note in
place. If a worktree still has a `.work/notes.md` from before the vault move,
that's the content to reshape — write the result to the vault path and delete
the old file (keep the rest of `.work/`, it's scratch).

## Compatibility

The dashboard still parses the older shapes (a `**Type:** · **Status:** · …`
metadata block, a `## Current status` section), so nothing breaks before you
migrate — but write **new** notes in the lean shape above.
