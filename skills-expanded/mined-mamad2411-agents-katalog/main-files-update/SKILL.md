---
name: main-files-update
description: >
  Read all 10 main context files (docs/main-files.md index), then ask David
  1-2 broad discovery questions per file about the DOMAIN (not the file contents)
  to surface new reality. Update each file based on his answers.
  Use when David wants to sync/refresh his core context.
triggers:
  - David says "update main files", "context sync", "catch me up", "sync files"
  - Start of a new work block where context may be stale
  - David explicitly asks to update his life/business context files
---

# main-files-update

## Purpose

Quickly get up to date on David's life and business by reading all 10 main
context files, then reviewing each file one at a time. Default to TLDR review so
David sees the actual file state and stale content surfaces; use discovery
questions when David explicitly asks for that mode or when a file is too long to
TLDR usefully. The goal is to discover new reality, not confirm old text.

## Steps

1. **Read the index.** Read `docs/main-files.md` to get the current file list.

2. **Read all 10 files.** Use direct read_file calls to load every file. The
   current month's reminders file uses the pattern
   `brain/main-reminders/{Month}-2026.md` (e.g., `May-2026.md`).

3. **Open the active file in cmux when available.** Before asking about a file,
   if running inside cmux (`CMUX_WORKSPACE_ID` / `CMUX_SOCKET_PATH`), open it on
   the right so David can see it while answering. Use this exact procedure per
   file; do not improvise with `--surface` / `move-surface` reuse because moving
   a markdown viewer leaves it blank:
   1. Close the previous file's right surface first:
      `cmux list-panes --workspace "$CMUX_WORKSPACE_ID"`, find the prior right
      markdown surface, then `cmux close-surface --surface <prev>`.
   2. Open the new file fresh:
      `cmux markdown open <abs-path> --direction right --focus false`.
   Order matters: always close previous before open new. Net effect: exactly one
   right markdown pane, always showing the file currently under review.

4. **Pick a mode per file.** Two valid modes. At the start of each file, ask
   David which one he wants if unclear; default to TLDR if he does not specify.

   **MODE A - TLDR REVIEW (default, recommended).** Give David a concise
   bulleted TLDR of what is currently in the file (~10-20 bullets, every section
   represented). Then proactively flag the items that look most
   outdated/wrong/stale, cross-referencing other main files already loaded. David
   reads the TLDR plus flagged staleness, then directs edits ("delete X",
   "update Y to Z", "add this"). This keeps David's eyes on the actual file
   state; discovery-only mode can let stale/wrong content silently accumulate.
   Do not ask "should I show you the TLDR?" - just show it.

   **MODE B - DISCOVERY QUESTION.** Ask 1-2 broad, open-ended questions about
   the DOMAIN the file covers, not what the file currently says. Use this only
   when David explicitly asks for it, or when the file is too long to TLDR
   usefully. Question rules:
   - Domain-level, not detail-level ("What's the biggest business priority
     right now?" not "Is X still true?")
   - Designed to surface things the file does not mention yet
   - Forget the file contents; ask as if you know nothing about the topic
   - One file at a time; never batch multiple files in one message
   - Single-faceted; each question asks one thing
   - Concrete and grounded, not abstract life-coach framings

5. **Update files.** After David answers, patch each file with the new info.
   Patch after each answer before asking the next question. Use surgical edits;
   do not rewrite entire files.

6. **Log word counts.** Run
   `bash .agents/skills/main-files-update/log-wordcount.sh` once at the end. It
   appends one row per file (datetime, file, words) to
   `docs/data/main-files-wordcount.csv` so file-length evolution is tracked.

7. **Log the run + bump per-file timestamps.** This is mandatory at end of every
   run.
   - For each file changed during the run, patch its
     `**Last updated:** DD-MM-YYYY` line to today's date (DD-MM-YYYY, CET). If
     the line is missing, add it right after the H1.
   - Append one row to `docs/main-files-runs.csv`:
     `YYYY-MM-DD HH:MM,<files_updated_count>,<short notes>`.
   - Files not changed during the run: do not bump their date.

8. **Confirm.** After all 10 are done, give a one-line summary of what changed.

## Questioning Style

- **Write clear, direct, very concise, pointed questions.** No padding, no "given everything you said...", no setup clauses, no soft framing. Ask the thing directly in one short sentence. David hates verbose or roundabout questions.
- Broad and open-ended in discovery mode; concrete and grounded in TLDR mode.
- The goal is to pull new context out of David, not verify old text.
- After David answers, compare his answer to the file and update accordingly:
  remove outdated entries, append new info, or rewrite stale sections.
- If a file's domain has nothing new, David will say so. Move on.

## File Order

Process in the order listed in `docs/main-files.md` (top 3 first, then 4-10).

## Single-Source-of-Truth Principle (DO NOT scatter numeric facts)

Numeric or fast-changing facts (current weight, daily calorie target, current
MRR, exact page in current book, etc.) live in one dedicated file: their source
of truth. Other main files should reference that file, not duplicate the number.
When you spot the same number in two main files, that is a bug.

Rule:
- `personal/health.md` owns weight, kcal target, training, sleep numbers.
- `docs/context.md` owns current revenue split, team structure status, location.
- `docs/goals/reviews/Q*-*.md` owns goal-progress numbers.
- Apply the same principle to any other recurring number you find duplicated.

When David gives a new number, update only the source-of-truth file. Strip the
duplicate from satellite files and replace it with a pointer to the owner file.

## READ-ONLY FILES (never edit during this skill)

Some main files are reference-only snapshots. Load them for context, but do not
modify them during routine main-files-update runs.

- `docs/goals/reviews/Q1-2026.md` - quarterly review. Created/documented once
  per quarter, then frozen. Q2 goals live here as source of truth, but routine
  updates must not patch the file or bump its date.

For any read-only file: read it, use it for context, skip directly to the next
file. Do not TLDR-review it for staleness, propose edits, or bump its date.

## Swapping a File In/Out of the Top 10

1. Read `docs/main-files.md` first.
2. Never suggest files that are already in the top 10 as replacements.
3. Propose 3-5 candidates, each with a one-line reason tied to a real coverage
   gap in the current top 10.
4. After David picks, update `docs/main-files.md` by replacing the slot line.
5. After swapping, scan root `AGENTS.md` for references to the removed file's
   domain. Ask before deleting routing rules.
6. The removed file still exists and can still be loaded on demand; say this.

## Promoting a New File Into the Top 10

1. Pick the path with David.
2. Create the file with a clear `**Last updated:** DD-MM-YYYY` line.
3. Fill it from what you already know across the repo first.
4. Ask single-faceted follow-ups for gaps. One question at a time.
5. After the file is populated, swap it into `docs/main-files.md`.

## Pitfalls

- **MODE A pitfall: a TLDR is not a summary of section headers.** It must surface
  concrete facts in each section so David can tell what is stale.
- **Keep TLDRs short.** Default flag format: one wrong/outdated item and one
  unsure/clarifying question. Long flag lists create friction.
- **After the TLDR, surface the most-likely-stale item + one open question.**
  End with a concise prompt for David's attention.
- **Do not ask "should I show TLDR?"** Once TLDR mode is active, show it.
- **Never ask "Is X still true?" or "File says X - still accurate?"** This is
  confirmation mode. Ask what is happening in the domain.
- **Never ask identifying-only trivia.** Names, dates of birth, IDs, etc. are not
  operational context. Ask what changes how you should help.
- **When proposing replacements, verify every candidate is not already top-10.**
- **When doing Q&A on a single file, update the file after each answer.**
- **Drop irrelevant entries on request without arguing.** Do not move them to a
  parking lot if David says they are unimportant.
- **If David says "not sure, ask me a specific question", narrow immediately.**
- **If David says "remove all mentions of X", remove literal occurrences of X.**
  Replacement text must not contain the string.
- **Discovery questions must be concrete and grounded in the actual file.** Avoid
  abstract framings like "what is moving forward vs dying."
- **If David says skip or signals a file is annoying/weird, move on.**
- **When David asks to stage & push between files, do it and then re-ask the same
  question.**
- **Do not ask "should I show the next file?"** Proceed mechanically.
- **If David says "run all 10 together", do not present a batch option.** State
  "one file at a time per the skill" and start with file 1.
- **When flagging stale items in the TLDR, highlight contradictions across
  files.**
- **When a file is clearly in bad shape, stop and ask 2-4 concise clarifying
  questions before moving to the next file.**
- **When TLDR-ing file N reveals stale content in file M, fix M before
  proceeding.**
- **When David asks to scrub a term from the 10 files, grep all 10 immediately
  and verify zero hits before declaring done.**
- The month in `brain/main-reminders/` changes; resolve it dynamically.
- Q1-2026.md contains Q2 goals in Section 4; do not confuse Q1 review with Q2
  goals.
- Todoist IDs go stale; flag any file references to Todoist IDs for re-fetch.
- Do not ask David to repeat info he already gave in the same session.
- When David says "skip" or lacks data, mark the stale section visibly, e.g.
  `**Needs recalculation - last computed DD-MM**`.
- Active initiative files should not contain specific daily tasks. Delete those.
- When checking "when was this last run?", do at least two session searches with
  different queries and sort by date. Trust David's recency if he pushes back.
