---
name: fleet-project-pipeline
description: "Use when running a product through the fleet: stages, gates, kanban cards, briefs, legs, qa fix pairs, merges and the clean-up sweep."
version: 2.0.0
author: "coordinator role of hermes-fleet-apps (generic method distilled from the fleet's own run notes)"
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [fleet, pipeline, product, gates, kanban, worktrees, orchestration]
    related_skills: [fleet-agent-inspection, app-project-kickoff, hermes-agent-factory]
---

# Fleet project pipeline

How the coordinator runs one product through the fleet:
`product -> designer -> coder -> qa -> media -> docs`. Read the fleet map
(who does what) before every stage. The coordinator orchestrates, merges and
reports; it never builds the product itself.

The owner decides at two gates only: SPEC (after product) and DESIGN (after
designer). Everything else runs without asking.

## 0. Before the repo exists

- Search for existing FOSS apps and for the data sources (API, licence, rate limits).
  Report in three blocks: what exists, data sources, honest verdict.
- Propose a few names and verify each one with a search; mark each verified/unverified.
- Use trademark-safe wording from day one ("<Brand> data", never "the <Brand> app"): it
  spreads into every brief.
- Check the DATA licence apart from the code licence: open code often serves NC data, which
  rules out ads, paid tiers or donations. Tell the owner before the spec.
- Map every planned feature to a real endpoint of the data source. A feature with no
  endpoint is cut or needs a second source: the owner's call.
- Ask what distribution may cost (signing, stores, certificates) before the spec, not after.

## 1. Repo and identity

- If the owner publishes under more than one identity, git should sign by folder
  (`includeIf` in `~/.gitconfig`). Pick the folder, never set `user.email` by hand.
  After the first commit check `git log --format='%an <%ae>' -1`.
- Private repos: agents commit with `--author "<ROLE> <role@localhost>"`; repo default
  identity `unattributed`, so a missing `--author` shows. A repo headed for public release
  commits with the publishing identity and no agent names.

## 2. Skeleton (one commit, before any agent touches it)

```
.gitignore      private/, .env*, build/, jobs/*/scratch/, jobs/*/session-stdout.log
.gitattributes  * text=auto eol=lf (+ binary media): no CRLF churn from Windows agents
README.md       one paragraph + an "unofficial / trademark" line if needed
PROJECT.md      which folder each role writes, the standing rules
CHECKLIST.md    numbered stages with gates; the coordinator ticks it (chats lose state, files do not)
jobs/JOB-<nnn>-<role>-<topic>/BRIEF.md, REPORT.md
private/        local only, git-ignored
```

Output folders: `SPEC.md` + `tickets/` (product), `.design/` (designer), source +
`CHANGELOG` (coder), `QA-REPORT.md` (qa), `assets/` (media), README/store text (docs).

## 3. Stages and gates

- **Designer runs as two jobs.** Phase A: 2-3 named directions (the owner's count if
  given), throwaway mockups of the most telling surfaces, one review page with a
  recommendation; writes only its job folder. Gate 2: the owner picks. Phase B: `.design/`
  for the chosen direction, written so the coder needs no question. Copy the direction's
  listed risks into the Phase B brief as "solve with proof" and look at the proof yourself.
- **The owner brings a mockup or prototype**: it IS the direction, skip Phase A. Write
  `.design/reference/MOCKUP-NOTES.md`: Keep / Adapt (every clash with the SPEC, numbered) /
  Missing. Check the file's metadata for personal data before committing it.
- **UI rework of an existing tool**: skip product, keep the roles: shape in 4 bullets ->
  designer mockups -> gate -> coder builds (current page = what it does, mockup = how it
  looks) -> qa and designer review in parallel -> one coder fix pass.
- **Presenting a gate**: bullets (surfaces, limits, acceptance-test count, "Later"), facts
  that changed since the brief, open questions one line each with the recommended default,
  your opinion on the one default worth flipping. Show phone AND desktop for a design.
  Your overrides go in as "applied unless you say no".
- **Audit the defaults product guessed** before the SPEC gate: owners of each stage against
  the fleet map; credentials least-privilege (a refreshing token over a permanent one);
  perceptual defaults (voice, music, motion) get a blind bake-off before code depends on
  them. Settle anything a command can answer yourself; only real choices go to the owner.
- **Applying an approval is your edit, not a new product job**: SPEC status line
  (`APPROVED <date>. Decisions: Q1 A, Q2 C`), the decision tick, the text and acceptance
  criterion the option changes, the ticket that builds it. Grep the tickets for the old
  default; do multi-file renames as one scripted replace that asserts each old string
  exists. Then dispatch wave 1 in the same turn.
- **An approval given in chat is recorded nowhere**: apply it, commit, complete the card.
- **Keep the kanban review lane manual** (check the dispatcher's review setting on the
  profile that launches the gateway): an automatic review run lets an agent approve its
  own work past the owner's gate.
- **Browser review pages** (e.g. the Lavish skill): keep one poll alive as a background
  process for the whole review, copy every asset into the page's own folder, strip remote
  fonts, look at 2-3 shots yourself before sending the link. A chat answer always counts.
- **Expert questions go to the expert.** Map each part of a request to its owner (look and
  style = designer, script/voice/edit = media, copy = docs, code = coder) before planning.
  The coordinator's own part is gates, merges, live checks and relaying.

## 4. Kanban cards and briefs

- **Dispatch = a kanban card**, one system for the whole fleet. Commit
  `jobs/JOB-<nnn>-.../BRIEF.md` first; the card body points at it. Chain stages with
  `--parent` so the next one starts by itself. Workers finish with `kanban_complete`.
  Subscribe the owner's chat to every card (`scripts/kanban-card.sh`).
- Write the card body with a file tool, not a heredoc; pass native absolute paths
  (`C:/...` on Windows), never `$PWD` from git-bash. Parse the id from `--json` and
  subscribe only when it is non-empty.
- A card with no parent starts at once, in parallel. A card that must wait for your step
  (a merge, a live check) is created only after that step. `link` refuses a running child.
- Every card says: "do not create kanban cards; follow-ups go in REPORT".

Brief content, every stage:
- Name each skill at the step it applies, not as a list up front.
- Paste established facts: the owner's decisions "not negotiable", your own research
  "verify, do not take on faith" (quick pre-vetting gets licences and versions wrong).
- Name every external thing exactly (package + version, model id, endpoint), checked to
  be the newest first, as "candidate set, pin newer if one appears".
- "Research online before you build": current docs, reuse proven libraries, cite links.
- Questions go into the artifact as decision forms with a default, never a blocking stop.
- Stop only for credentials, publishing, foreign changes in the worker's paths.
- Name every off-limits path AND the allowed alternative; a bare ban gets worked around.
- Secrets: only the app reads them at runtime; the agent never opens, greps or prints the
  file; tests use a fake; check presence with a boolean, never the value.
- One-off writes to the owner's real data are the coordinator's step: the brief says
  "build the command + dry run; the coordinator runs the write".
- Live runs set a scratch data home inline in every command, background ones included.
- Native paths for native tools, `PYTHONDONTWRITEBYTECODE=1`, commit after each unit with
  a pathspec, never push, delete scratch and list it in REPORT.
- Long downloads/builds run in the background and resume from cache.
- The product itself is English (names, CLI, messages, SPEC); check it at the SPEC gate.
- 3+ parallel jobs: shared rules once in `COMMON-RULES.md`; each brief holds only its items.

After every card:
- Read REPORT AND the artifact; check `git log` for the commit. Uncommitted work: commit it
  with the worker's `--author` and say "committed by the coordinator".
- Brief changed mid-run: commit it, comment the card, check REPORT against the new rule.
- A late notification: compare its timestamp with the card's latest events before acting.

The owner changes course:
- Reverses a decision: never build a substitute on your own. Apply the reversal in ONE
  commit everywhere (SPEC, strings, tickets cancelled in place, CHECKLIST, running cards).
- Reports a problem: sort it. BUG -> reproduce it yourself first, then a fix + recheck
  pair. NEW FEATURE -> one-line proposal, wait for yes (a plain request is a yes). BY
  DESIGN -> only after reproducing it.
- Live feedback session: one coder card at a time, each chained on the last; one qa card
  collects a numbered check per job.
- New capability mid-build: check the out-of-scope list, answer now, recommend "after v1",
  log it in `BACKLOG.md` (private notes if the repo will be public).

## 5. Worker budget and legs

- A run has an iteration cap and a context limit. Cap a leg at ~3 deliverables, one area
  per leg (engine OR UI OR docs), and put REPORT in its own small leg.
- Every brief: "commit after EACH unit, first commit within your first 10-15 turns; grep
  big files, read only the regions you edit". Review cards too: qa max 3 areas, write
  the report after each.
- Size big jobs as legs up front: a UI port = one leg per 2-3 screens, then a strings +
  browser-check + REPORT leg. Before splitting, give every AC of the ticket a leg row in
  `SPLIT.md`: an item no row names is never built.
- First block on context (HANDOFF written): unblock once with the narrowed scope.
  Second block on the same card = too big: split into legs chained with `--parent`.
- A leg that blocks with nothing: unblock with an explicit read list, a do-not-open list of
  the big files, any open choice decided, "save each file as soon as it exists".
- A worker that gave up with work uncommitted: commit it as "WIP, unverified", run the
  suite yourself, unblock with the done list by commit hash and the one item left.
- A timed-out card is retried: before the retry claims it, comment a resume note (commits
  made, own uncommitted paths, one-off steps already run "do NOT run again", what is left).
- A worker's scratch is pruned: copy logs and data into the job folder before a respawn.
- Deadline run with several coder lines: first ONE small foundation card (pinned stack,
  stubs, a fake of the external engine, `docs/ARCHITECTURE.md` as the frozen contract,
  written right after research), then the line cards as its children.

## 6. qa and fix pairs

- qa reviews a frozen copy (`git worktree add --detach <repo>-qa <commit>`) so the next
  coder leg runs in parallel; remove the worktree after the verdict.
- A FAIL becomes two chained cards: coder fix (findings as must-do / if-cheap) + qa recheck
  that reruns the old mutants. Completing a qa card releases its children even on FAIL:
  re-hang the later stage on the recheck (`unlink` + `link`).
- Recheck PASS with only LOW findings: merge, fold the LOWs into the next polish leg.
- One-line remaining finding: fix it yourself with a test that fails without it, full
  suite, "fixed by the coordinator, not re-shot". Surviving mutants only: write the test,
  apply the mutant by hand (test must fail), restore, suite green.
- qa and designer reviewed the same stage: one fix brief with both lists, one recheck.
- The same heuristic fails a second recheck: switch to a strict allow-list with right AND
  wrong cases as tests. A third time on one sub-case: cut the sub-case.
- Fix tests go through the real user path, not a hand-built fixture.
- Bad data already stored: an `audit` command, then mark invalid (never delete), backup
  first, counts before/after. Unsure enrichment stores nothing.
- Any check or approval is bound to what it checked (text excerpt or file hash); the gate
  fails when the file changed. Re-hash right before publishing.
- Every one-way action and every failure state needs a way back in the UI; a message names
  only actions the UI has. A pass that found nothing must not say "done".
- UI qa drives the interface at each breakpoint (click every control, scroll every area);
  screenshots alone pass dead buttons. Designer signs off ported screens against `.design/`.
- Two views disagree on a count: decide the counting unit per surface in the fix brief.
- Measure, do not guess: quality over 3+ seeds, resource estimates never below the measured
  peak, a measured fix becomes a card the same turn.
- Security audit: findings are hypotheses (confirm each in code), split into lines by file,
  each fix with a red-proven test, a guard test that scans for every instance, runtime
  proof only in an isolated data dir, each attack paired with the legitimate action.

## 7. Parallel worktrees

- While anything waits (a gate, the GPU, one card), dispatch the lanes that do not depend
  on it, each on its own worktree branch. Max 3 lines per repo (main + 2).
- Parallel briefs: "add, don't reshuffle" (new modules, only registration lines in shared
  files), name the hot files, freeze any contract another line imports, list shared-file
  edits in REPORT.
- Two roles in one tree: each stages only its own paths, and the brief names the other's
  uncommitted files as expected.
- A line needing another line's unmerged work branches from that line, never merges itself.
- Setup, inserting jobs, side effects and merge recipes: `references/parallel-worktree-jobs.md`.

## 8. Merge gate

- The commit depends on green tests:
  `set -o pipefail; git merge --no-ff --no-commit <b> && pytest && ruff check . && git commit`.
  Never `;`, never pipe the suite into `tail`/`grep` in that chain. Red = `git merge --abort`.
- Run a line's suite 3-4 times before merging; one red run in four = flaky, fix the cause.
- Hold a merge while any card works in the target tree.
- After merging parallel lines, run the full suite on the merged tree; the count must equal
  base + each line's added tests.
- CHANGELOG conflicts: keep both. Code and docs on the same behaviour: merge code first,
  resolve docs to what the merged code does.
- During a merge, finish with `git add <files> && git commit` (no pathspec). Untracking
  (`git rm --cached`) is committed without a pathspec too.
- Before reporting "merged": restart the owner's running server on the new code and check it.

## 9. Clean-up sweep (after every card, not only at the end)

- Worker scratch folders: delete leftovers of finished jobs (nothing newer than an hour, no
  running card points there).
- `jobs/*/scratch/` (git-ignored, so `git status` hides it), empty scratch dirs, test
  videos, build output.
- Servers and processes left running (listening ports, GPU processes, orphan runtimes).
  Briefs that start a server allow stopping that pid; workers that cannot delete list
  leftovers in REPORT's first lines.
- SQLite backup side files (`-shm`, `-wal`), stray files in `git status`.
- The owner's real data untouched (row counts, `git status` on data folders).
- Finished worktrees removed (`git worktree remove`, `prune`, `branch -d`).
- Superseded blocked cards: comment "superseded by <ids>", archive.
- Stopping a running agent: kill the agent process, not its shell wrapper; confirm the
  process count dropped. Cancelling a card: reclaim, archive its children, wait for the
  diff to stop changing, `git checkout -- <its paths>`.

Remove, then tell the owner what was removed in one line.

## 10. Release and after

- Release candidate: one clean rebuild of every package, then the owner hand-tests once;
  findings go in a committed findings file; one fix batch after.
- Before any build the owner or a video will see: check every icon surface against
  `.design/` (placeholders survive every test).
- Installers: per-user, and the uninstaller never deletes the user's own outputs. An install
  test that fails midway must clean up after itself (try/finally).
- Renaming a product means zero traces of the old name, incl. a fresh history before the
  first push.
- Every media cut gets a qa review before the owner sees it.
- Recurring reports: the product prints the final text; a no-agent scheduled script sends it.
- When the product replaces a tool another agent runs daily: draft that agent's skill in
  the repo, cutover is the owner's gate, retire every old skill with an overlapping trigger.

## 11. Reporting to the owner

- Chat in the language the owner writes in; every file in English.
- One line when a stage starts, one short report when it ends, gate questions only at gates.
- "Do I have to do something?": yes/no first, a 3-line status, the one next thing.
- Owner away: an "Unattended run" section in CHECKLIST, one scheduled report; FAILs get
  fix pairs without asking. Report: What's new / Verified / To know / Cleanup / Left.
- Say plainly when your own check missed something or a worker broke a rule.
