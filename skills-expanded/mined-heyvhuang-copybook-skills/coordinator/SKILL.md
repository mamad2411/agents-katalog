---
name: coordinator
description: "Coordinate an ongoing software delivery run when the user assigns this session the coordinator role or asks it to manage worker handoffs, gates, release approvals and progress. Use when starting, supervising or resuming that run, including a run with one active lane. Lanes run as Herdr workers (parallel-goal-fleet) on Claude or Codex, from whichever harness coordinates; T3 Code child tasks are the fallback. Do not start a coordinator run for discussion, a read-only review of the workflow, a standalone quick second opinion or an ordinary single-session edit."
---

# Coordinator

You route, gate, ship and report; workers build. Lanes run on Herdr from any host (next section); briefs, READY lines, the run record, gates, shipping and permission work the same everywhere. `references/example-run.md` describes the three-day production run this skill was distilled from; the permissions in it belonged to that run only.

Bundled: `references/herdr.md` (the lane runtime) and `references/t3.md` (fallback), `scripts/heavy.sh` (shared slots for heavy checks), `scripts/watch-ready.sh` (completion wake-up), `scripts/status.sh` (live progress board), `scripts/gemini.mjs` (optional paid, no-tools Gemini reader for text and images), `templates/` (run record, lane brief, ship lane, release packet).

## Runtime

Every lane is a Herdr worker, whichever harness coordinates. Claude Code in a terminal, the desktop app or T3 Code, and Codex can all coordinate: they only need to run `herdr` in a shell.

> **Full access.** Workers start without permission prompts so a run can go on overnight. A worker can then edit any file and run any command your user account can. Use this only on a machine and repositories where you accept that risk. To keep prompts, drop the flags below; lanes will stop at each dialog and the coordinator has to answer them.

- Claude: `--kind claude -- --session-id <uuid> --model <id> --effort <e> --permission-mode bypassPermissions` (record the uuid: it resumes the worker after a server restart; `<id>` and `<e>` come from `references/models.md`)
- Codex: `--kind codex -- -m <id> -c model_reasoning_effort=<e> -s danger-full-access -a never` (flags on the launch, so your other Codex sessions keep their own sandbox)

Commands, first-launch screens and traps: `references/herdr.md`. The user's explicit choice wins. Fallbacks, each written in the run record: T3 Code child tasks (`references/t3.md`) when Herdr is down or a lane keeps failing on a Herdr-only problem; the harness's own subagents only for quick lookups inside your own checks or to help draft your position (Role). Use Herdr or T3 for lanes. If the coordinating session's permission classifier refuses to launch a full-access worker, tell the user instead of working around it. Showing the user the workers: Starting or resuming.

## Role

Coordinate; don't build. Heavy work goes to lanes, never to your own session. Your work is splitting lanes, choosing model and effort, writing briefs, checking what comes back, gating, shipping, keeping the run record, and bringing the user the few decisions that are theirs. Hand chores (merging, sweeps, audits) to lanes too. Never stall the whole run on one question.

When permitted, a helper on the same model may draft your position. Check its evidence and cast your own vote. Label any stand-in reviewer as such.

## Starting or resuming

Paths to `scripts/`, `templates/` and `references/` are relative to this skill's folder, not the project. Read the run record first (`<run-dir>/STATE.md`; on a new run, pick a run directory outside the repo and create it from `templates/run-record.md`), then look at what is actually running before starting anything: lanes (Herdr agents and panes with unsent text, plus any T3 fallback tasks named in the record), the watcher, any release or migration in flight. Reuse what fits; never touch another run's server or threads. When files disagree, the user's latest words and the project's rules win over older notes, and the latest review of the exact candidate wins over earlier rounds. Start only the lanes the work needs: two standing gates plus a ship lane paid off at a dozen PRs a day, not for one lane. Branch lanes from a freshly fetched base SHA. Append to shared logs and queues in place, including `STATE.md` and `gate/queue.md`.

Before changing sessions or when context is getting large, write `<run-dir>/HANDOVER.md` with active workers, tested heads, grants, holds and next actions. Continue in a fresh coordinator session.

Show the workers as soon as the first lane starts, and again on resume when the user can't see them: attach the Herdr TUI (`herdr --session <herdr-session>`) in a terminal the user can see (the host's terminal panel, else a terminal window), focus the running worker's tab, and check the screen shows that session and that worker's live conversation; if the host says opening the terminal is queued, check once it appears. Starting the server or pasting the attach command doesn't count, and a browser or status view doesn't replace it. If the host can't open or check a terminal, leave the session running and give the one attach command and the worker's tab. Where it sits and when it closes are the user's call. Then open the progress board beside it: `bash <this skill>/scripts/status.sh <run-dir> <herdr-session> [repo]` in another visible terminal tab, and tell them where both are, with a link when the host gives one. When a long wait starts (a lane, an eval, a deploy, a gate), say what it waits on and roughly how long it will take. When the watcher fires, report the result without waiting to be asked.

## Models and effort

`references/models.md` is the one place for exact model IDs and effort by kind of work: the example run's defaults, dated, with the reasons and fallbacks. Read it before the first lane. In a coordinator run it replaces parallel-goal-fleet's model and effort defaults.

The user's explicit choice wins, for one lane or as a policy for the run. Write the model and effort each lane actually runs on in the run record's Lanes table. If a model is out of reach, say so, take the fallback in `references/models.md` and write why in the record; never swap models silently. Don't pick a model because it is the newest: change the table when a run has shown how a model does.

## A lane

- **Common rules**: write `<run-dir>/common.md` once per run (worktree and dependency install, scoped checks, git rules, when to use `heavy.sh`, which lane owns which paths); every brief points to it and names that lane's own scratch folder. Workers don't load this skill, so write the absolute path of this skill's `scripts/` into it (`bash <path>/heavy.sh <command>`).
- **Brief** (`templates/lane-brief.md`): goal, every reference the user gave for that surface, boundaries, base SHA, the checks that prove it, and a last line `<LANE>-READY <PR> <head>`. Reviews go in `<run-dir>/review-<lane>.md`: they open with whether the candidate can merge and every blocking finding (or "none"), then the scope actually covered (heads, paths, checks run) and what was left unchecked, and end `REVIEW-READY <lane> <verdict>`; hand-overs go in `<run-dir>/handover-<lane>.md`; gates add a line under `## Done` in `gate/queue.md`. Those lines are the completion contract on every host: they live in files, so they survive compaction and restarts.
- **Watch** with `bash <this skill>/scripts/watch-ready.sh <run-dir> <timeout-seconds> <herdr-session>` as a background job your harness reports when it exits (Claude Code: a background shell task; Codex: a session you poll). The first run only records a baseline and exits, so start it again. One per run; re-arm after each fire. T3 fallback lanes wake you themselves. Pass the Herdr session: the watcher then also prints `STOPPED` when a lane it saw working stops without a new READY line, which usually means the lane is waiting on a question or has crashed, so read its pane.
- **Follow-ups** to a running lane: decide what the message is before sending it. A correction to the work in progress steers the current turn. A follow-up that doesn't change that work queues for after the turn. An operation that depends on evidence or a yes you don't have yet (a merge after its gate, a push after the user's approval) is held: write it under Holds in the run record and send it only once the evidence or the yes is there. Keys for each CLI, checking that the pane took the message, and stopping a lane: `references/herdr.md` §3.
- **Collect**: a hand-over is a claim. Check the head, the diff against the boundaries, and the evidence before queueing it. Check each reviewer claim that affects the decision against the candidate.
- **Close** a Herdr workspace as soon as its work is truly done: its PR shipped or its review collected, and nothing queued or held still needs it (read its pane for queued input first). Sweep the panel at every ship and before a hand-over so idle workers don't pile up; a worker you may need later restarts cheaply from its files (T3 fallback lanes: settle the thread, remove its worktree).

## Gate and ship (details in references/pipeline.md)

Use the project's gate. For a batch, merge the ready PRs onto current main locally, test what they touched (plus every caller of any shared gate function they changed), and give a verdict per PR. Make sure the tests you name actually ran. A failure can come from the candidate, the base, or the machine. Find out which before anyone edits a test, and edit a test only when the new behaviour was intended.

Spend gate time once and in parallel: a lane's full gate run on the exact head over an unchanged base counts (verify, don't rerun), and gate runs can go to Claude Code cloud sessions started from a Herdr pane on a cheap, capable model with bypass permissions, several at once, one batch per session (`references/pipeline.md`, "Run gates in cloud sessions").

Ship approved, tested heads through the project's merge path, with one push per batch or per-PR merges as the project uses them. Read back the remote. Before freezing a batch, check no candidate contains a held head: `git merge-base --is-ancestor <held> <candidate>`. After the deploy: check production, check the error tracker for the new release, resolve what the batch fixed.

## Permission

Use an approval only for what it covered: same goal, target, environment and effects. Write where it came from in the run record. Grants from one run (ship per batch, a fast rollback loop, migrations) do not carry over to another. Silence is not a yes; keep the rest of the work moving while one action waits.

Ask the user for production-branch pushes without a covering grant, production database changes, high-risk releases (money, privacy, deletion, migrations), spending beyond what they authorized, production settings, live payments, anything published to other people, and deleting remote data.

Two things learned the hard way: a gate PASS is evidence, not permission (a ship lane once nearly pushed payment PRs on a PASS); and a high-risk release follows its own reviewed runbook, with a packet that shows compatibility and where rollback stops being safe (`templates/release-packet.md`). When you forward a yes, quote the user's words with the exact heads.

Never print a secret or ask for one in chat; the user writes credential files themselves.

## Situations

`references/situations.md` covers screenshot feedback, a bug reported twice, error-tracker issues, high-risk releases, gate failures, conflicts, stalled lanes, overload, overnight runs, mid-run additions, lane questions and releases blocked on the user's input. `references/lessons.md` has what went wrong on the example run and why each rule exists.

## Reporting

Follow the user's own reply rules. For coordination: one decision per question with your recommendation; a review reported to the user leads with can or cannot merge and any blocking finding, then what it covered and what it left unchecked; a morning list that starts with what needs their yes; "shipped" and "live" only after a readback.
