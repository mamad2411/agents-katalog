---
description: Co-edit a paper or concept page in place — action inline review comments, follow chat instructions, or build on the user's own edits — grounded in the page's cited sources, preserving frontmatter and wikilinks
argument-hint: <path to a paper, concept, or course module page> (e.g. "papers/react.md", "concepts/rlhf.md", "course/flow-matching/modules/2-flow-matching-objective.md")
allowed-tools: Read, Edit, Glob, Write(course/*/.session_reminded), Write(course/*/.edit_count), Bash(date:*)
---

Co-edit a knowledge-base page with the user, editing it in place. This is the
collaborative refinement step for a `papers/` or `concepts/` page: the user drives
and you make the changes. Any **factual** content must come **only from the
sources the page was synthesised from** — if the sources don't cover what's asked,
point out the gap instead of inventing it.

The user works in three (combinable) modes:
- **Inline comments** — they mark requests addressed to you inline in the file,
  e.g. `@claude: phrase this more precisely and less bombastically.`
- **Chat** — they tell you in conversation what to change ("tighten the overview",
  "add a limitations paragraph from the InstructGPT source").
- **Direct edits** — they've already edited the page themselves; re-read it so your
  changes build on their current text, and never revert their wording.

If **$ARGUMENTS** is empty, ask the user which page to work on, then continue.

## Steps

1. **Read the page.** `Read` the file at **$ARGUMENTS** (always re-read so you see
   the user's latest direct edits).

2. **Load its sources.** Read the page's `sources:` frontmatter list — these are the
   files it was synthesised from. Resolve each entry relative to the page; if that
   path doesn't exist, locate the file by its basename with `Glob` (e.g.
   `sources/**/<name>.md`, `notes/**/<name>.md`). `Read` every resolved source.
   These are the **only** admissible basis for new or changed factual content.

3. **Gather the requests.** Collect both the `@claude: ...` comments in the
   page (inline or on their own line; each refers to the text around it unless it
   says otherwise) and any instructions the user gave in chat. Comments **without**
   the `@claude:` marker are the user's private notes — leave them untouched. If
   there are no comments and no chat instructions, ask the user what they'd like
   changed and stop.

4. **Action each request** in document order, with a surgical `Edit` to the passage
   it refers to. For an actioned `@claude:` comment, **remove that comment** in
   the same edit. Follow the **Editing rules** below.
   - If a request needs information **not present in the sources**, do not invent
     it. Leave any related comment in place (so it stays outstanding) and note the
     gap for the wrap-up — e.g. "the cited sources don't state X". Make only the
     part of the change the sources do support.
   - If a request is ambiguous, ask the user instead of guessing.

5. **Confirm completion.** Report what you changed (one line each) and, separately,
   any **gaps** — requests left unactioned because the sources don't cover them — so
   the user can add a source or revise.

6. **Tutor re-test reminder.** After confirming, check whether the edited page belongs
   to a learning course and, if so, respect the user's chosen cadence (see **Tutor
   prompt trigger** below). Skip entirely if no course covers the page.

## Editing rules

- **Ground edits in the sources only.** New or revised factual claims must be
  supported by the page's cited sources (step 2). Match the page's existing citation
  style (inline relative links to `../sources/...` / `../notes/...`). Pure
  wording/tone edits that add no new facts are always fine.
- **Preserve Obsidian/Markdown syntax exactly.** Treat these as literal content —
  never reformat, normalise, or rewrite them unless a request explicitly asks:
  - **YAML frontmatter** (the `---` block): keep every key, value, and ordering
    as-is unless asked to change a specific field.
  - `[[wikilinks]]`, `[[link|alias]]`, embeds `![[...]]`, block refs `^block-id`,
    heading links `[[note#heading]]`, `#tags`, and callouts (`> [!note]`).
  - **LaTeX math** (`$ ... $`, `$$ ... $$`) — leave existing math untouched unless a
    request targets it.
- **Write math in LaTeX.** When a request adds or revises math, use LaTeX (inline
  `$ ... $`, display `$$ ... $$`, which render in Obsidian and VS Code) — never plain
  text or Unicode. If asked to make something more precise or rigorous, describe it
  mathematically and include the critical equations/derivations, grounded in the
  page's sources.
- **Only change what's asked.** Edit the specific passage and nothing else. Leave
  other text, spacing, and line breaks untouched. Don't restructure headings or
  rewrap paragraphs unless asked.
- **Edit in place.** Change the original file at **$ARGUMENTS** — never create a new
  file, add a suffix, or change the location.

## Tutor prompt trigger — re-test reminder

After a successful edit, check whether the page is covered by a learning course and
remind the user to re-test at their chosen cadence:

1. Glob `course/*/goal.md`. For each, check whether the edited page's slug/title
   appears in that course's Knowledge Audit, or the page lives under the course's own
   `modules/`. If no course matches, do nothing.

2. For a matching course `<slug>`, read its `tutor_prompt_mode` (from `goal.md`):

   - **`session-end`** — at the very end of the wrap-up (once per session, even if
     several pages in the course are edited), append:
     > *Course `<slug>` covers this page — remember to run `/tutor <slug>` this session.*
     Track with a flag file `course/<slug>/.session_reminded` (treated as created on the
     first reminder this session); don't repeat the line if it already exists.

   - **`after-3-edits`** — read the integer in `course/<slug>/.edit_count` (0 if absent),
     increment, write it back. When it reaches 3, prompt
     > *You've edited 3 pages covered by course `<slug>` this session — run `/tutor <slug>`?*
     and reset `.edit_count` to 0.

   - **`never`** or **`unset`** — no prompt.

These flag files are gitignored runtime state, not knowledge-base content.

## Notes

- Works from the page and its sources — no API key. The user iterates by adding more
  `@claude: ...` comments, chatting, or editing directly, and re-running the
  skill; each run actions the outstanding requests (leaving only those blocked by a
  source gap).
