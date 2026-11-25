---
name: session-handoff
description: >-
  Write a handoff document at the end of a long agent session so a fresh session with no memory can
  resume correctly: human rulings in force (dated, including what was explicitly NOT approved),
  verified per-repo state (commit, branch, remote, pushed or not, dirty files), what the session did,
  ordered next steps marked by which need an explicit human go, recipes that worked, lessons that cost
  time, and exact start-up steps. Every state claim is checked with a command before it is written and
  labelled done / verified / assumed; older handoffs are superseded explicitly and an entry file points
  at the new one. Use when the user says "write a handoff", "hand this off", "wrap up the session",
  "leave notes for the next session", "pick this up tomorrow", "we're running low on context", "end of
  session", or before a context reset on multi-step work. Also use at the start of a session to resume
  from an existing handoff.
---

# Session Handoff

A handoff is the only memory the next session has. Its one job: a fresh agent, reading it cold, makes
the right next move without re-deriving what is known and without undoing a human decision.

Paths like `scripts/repo_state.py` and `references/template.md` are relative to this skill's folder
(typically `.claude/skills/session-handoff/`); run the script from the repo you are handing off, e.g.
`python .claude/skills/session-handoff/scripts/repo_state.py . <other repo paths>`.

It exists to prevent four specific failures, each of which is expensive:

1. **Acting on permission that was never given.** The next session sees "next: push to the new remote"
   and pushes. The human had said "not yet". Outward-facing and irreversible steps need the human's
   words, not the previous agent's plan.
2. **Trusting stale or invented state.** "Everything is committed and pushed" written from memory, when
   the push failed or a file was left out. The next session builds on a false floor.
3. **Redoing finished work or re-opening settled questions.** Without a clear "done" list and the
   rulings behind it, a fresh agent re-litigates.
4. **Re-paying for lessons.** A tool quirk that cost the last session an hour costs the next one an hour
   too, unless it is written down in one line.

## When to use

- At the end of any session that leaves work in flight: uncommitted changes, pending human decisions,
  a multi-step plan partly done, several repos touched.
- Before a context reset or compaction on long work, or when the human steps away mid-plan.
- At the **start** of a session, when a handoff exists: see "Resuming from a handoff" below.

Not needed when nothing is pending: a one-line note in the entry file ("2026-09-28: X done, nothing
open") is enough. A handoff is not a changelog, a commit message, or a status report for stakeholders.

## Rules (binding)

1. **Absolute dates only.** `2026-09-28`, never "today", "yesterday", "last session", "this week".
   Check the date with a command before writing (`date` in a POSIX shell, `Get-Date` in PowerShell,
   or `python -c "import datetime; print(datetime.datetime.now().astimezone())"` anywhere; in Windows
   `cmd.exe`, `date` prompts to *set* the date, so don't use it there). Long sessions cross midnight,
   and a handoff stamped with the wrong day misleads every later reader.
2. **Verify before you write.** Every state claim (commit, branch, remote, pushed, dirty, test result,
   count) comes from a command run *now*, not from memory of running it earlier. Run
   `python scripts/repo_state.py <repo> [<repo> ...]` for the repo table; see
   `references/verification.md` for the claim-to-command list.
3. **Label confidence.** Each claim is one of: **done** (the action happened), **verified** (checked,
   with the command and the date), **assumed** (not checked; say why). Never let "assumed" read as
   "done". Claims made by other agents or models are *assumed* until you check them yourself.
4. **Rulings are the human's words, dated, including the negatives.** "Keep everything local", "not
   yet", "not approved", "ask me again after X" are rulings too, and the most important ones to carry.
   Never infer permission from silence, and never extend a go given for one step to the next step.
5. **Flag every step that needs an explicit go.** Anything outward-facing or hard to reverse (push,
   publish, deploy, delete, send, change a remote, spend money, touch shared infrastructure) is marked
   *needs the human's go* even when it is the obvious next step. Deleting a *remote* branch is a push.
   A conditional approval ("delete the old branch once the new one works") is still *needs go* until
   the condition is met; record who judges the condition.
6. **Short enough to read first.** Aim for 60-120 lines. Link to details (commit messages, logs,
   receipts, plans) instead of inlining them. If it does not fit, it is a report, not a handoff.
7. **Supersede explicitly.** The new handoff names the one it replaces. The old one gets a one-line
   forward pointer at its top and is kept for history, never deleted. Exactly one handoff is current.
8. **Point the entry file at it.** Whatever a fresh session reads first (see "Where it lives") gets a
   line at the top: `NEXT SESSION: read <path> first`.
9. **Record losses and unknowns plainly.** Something deleted by mistake, a check that could not run, a
   feature never exercised against the real service: write it down with what is and isn't known.
10. **Recompute numbers; don't copy them forward.** Counts carried from an older handoff drift. Re-run
    the command or mark the number *assumed (from the <date> handoff)*.
11. **No secrets.** Say where a credential lives or that it is missing; never paste its value.

## Workflow

### 1. Gather (read-only)

- The date, from a command (see rule 1), and the timezone if the work spans people or servers.
- `python scripts/repo_state.py` over every repo or folder the session touched, including ones that are
  not git repos (the script says so, and "not a git repo" is itself state worth recording). It also
  lists every local branch with its upstream, whether its tip is on a remote, and whether it is merged
  into HEAD: branches the rulings mention (to delete, to keep) belong in the handoff.
- The rulings: scan the conversation for every decision the human made, with its date and exact scope.
  Include refusals and deferrals. If a ruling from an older handoff was not revisited, carry it and say
  so ("unchanged since 2026-09-26").
- What was done: from `git log` since the session started, not from recollection.
- Open items: pending human decisions, known gaps, untested paths, anything flagged but not fixed.
- The previous handoff: follow the entry file's pointer, or search the repo for existing handoffs
  (`handoff` in file names under `docs/`, `notes/`, or similar).

### 2. Draft from the template

Copy `references/template.md` and fill it section by section. The section order is deliberate: rulings
come before state because a fresh agent must know what it may *not* do before it reads what it could do.

### 3. Verify pass

Re-read the draft line by line. For every state claim, name the command behind it; if you cannot, run
one or relabel the claim *assumed*. Walk the checklist at the end of `references/verification.md`.

### 4. Supersede and point

- Old handoff: add at its top `> Superseded on <date> by <new path>. Kept for history.` If some of its
  items are still open, say which ones moved into the new handoff.
- Entry file: add or replace the `NEXT SESSION:` line.
- Writing the handoff and the pointer changed the working tree after step 1 ran. Add both paths to the
  state table's working-tree owners (or re-run `repo_state.py` now), or the next session will see
  them as unexplained drift.

### 5. Commit only if asked

If the human wants the handoff committed, note the self-reference trap: a handoff cannot contain the
hash of the commit that adds it. Write "the commit that adds this file" and, after committing, check it
with `git log -1 --format=%h -- <handoff path>`. Never leave a placeholder like "this session's final
commit" in a state table without that note.

### 6. Tell the human

One short message: the handoff path, what needs their decision, and anything that only they can do
(remove a lock file, approve a push, answer an open question).

## Where it lives

- **Follow the repo's existing convention** if one exists (search before creating).
- Otherwise: `docs/handoffs/YYYY-MM-DD-<slug>.md`, where the slug names the point you are handing off
  from (`after-auth-migration`, `mid-batch-3`), not the session number alone.
- Several repos: put it in the one the human works from or the one that coordinates the others, and
  list every repo in the state table.
- **Entry file**: the file a fresh agent session actually reads first, in this order:
  1. an instructions file the agent tool loads automatically (`CLAUDE.md`, `AGENTS.md`, or your tool's
     equivalent);
  2. a working-notes or memory file that the project already tells agents to read;
  3. `README.md` only if the project already uses it that way. A README is usually public-facing, so a
     `NEXT SESSION:` line there can get committed and published.
  If none fits, ask the human before creating one; do not invent a new convention silently.

## Section guide

Full template with guidance: `references/template.md`. In brief:

| Section | What proved its worth |
|---|---|
| Header | Written date + session name, what it supersedes, what to read first |
| Human rulings in force | Dated, near-verbatim, scoped; explicit "NOT approved / not yet" lines; open questions only the human can answer |
| State you inherit | One row per repo: last commit, branch, remote and where it points, pushed or not, dirty paths with an owner for each; plus non-repo state (lock files, flags, running processes) |
| What this session did | One line per item, newest meaning last; link commits or logs for detail |
| Next, in order | Numbered; each marked *needs go* or *safe to do*; a recommendation where there is a choice; finished items struck through in place with the date |
| Method | Recipes that worked, as exact commands or file pointers: "reuse, do not reinvent" |
| Operational lessons | Only things that cost real time; one line each: symptom, cause, workaround |
| Still open | Unresolved decisions, known gaps, never-exercised paths, losses |
| How to start next session | 2-4 steps: a health check with its expected result, then the question to ask the human, then the first concrete step |

## Resuming from a handoff

The other half of the protocol, for the session that reads it:

1. **Find the current one**: the entry file's pointer, then check the file is not itself marked
   superseded (follow the chain to the newest).
2. **Run its start-up steps**, then re-run `scripts/repo_state.py` on the listed repos. State may have
   changed since it was written: the human may have committed, pushed, or deleted things. Where the
   command and the handoff disagree, trust the command and tell the human what moved.
3. **Re-read the rulings before acting.** A "Next" list is a plan, not approval. For any step marked
   *needs go*, confirm with the human in one line first ("Handoff says step 2 is next and needs your go:
   proceed?").
4. **Keep it live while you work.** When you finish an item, mark it in place:
   `~~2. Rotate the API key~~ **DONE 2026-09-28**: new key in the vault, old one revoked (verified).`
   When you end the session, write the next handoff and supersede this one.

## Anti-patterns

- A narrative diary of the session instead of state + next steps.
- "All committed" or "pushed" without `git status` / an upstream comparison behind it. A push that was
  *attempted* is not a push that *landed*.
- Relative dates, or a date copied from the previous handoff after the day rolled over.
- Rulings copied forward without checking they still hold, or rulings without dates.
- A "Next" list with no order and no *needs go* markers, or the marker buried in prose.
- Operational lessons that are general advice ("be careful with X") rather than a specific symptom and
  workaround.
- Deleting the old handoff instead of superseding it; two handoffs that both claim to be current.
- A 300-line handoff. The next session will skim it and miss the one ruling that mattered.

## Files

- `references/template.md`: the fill-in template, with guidance per section and a short worked example.
- `references/verification.md`: claim-to-command table, the done / verified / assumed labels, traps
  (self-referencing hashes, date rollover, stale fetch), and the pre-save checklist.
- `scripts/repo_state.py`: prints a verified per-repo state table (branch, last commit, remotes, pushed
  or not, staged / modified / untracked, stashes) plus every local branch (upstream, ahead/behind, on a
  remote or not, merged into HEAD or not). Handles plain folders and bare repos. Python 3 stdlib +
  `git`. `--fetch` refreshes remote refs first so "pushed?" is current; `--self-test` checks the parser
  against a throwaway repo (run it once after copying the skill).
