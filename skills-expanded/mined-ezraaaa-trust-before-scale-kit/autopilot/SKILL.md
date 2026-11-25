---
name: autopilot
description: "Run or resume the autonomous work loop under the project's extension. Triggers: autopilot, work the backlog, overnight run, unattended run, continue the milestone."
---

Read the project extension first: `autopilot.extension` in `.agents/trust-before-scale.json` (else
`.claude/trust-before-scale.json`), default `.claude/skills/autopilot/SKILL.md`. A project autopilot skill
with no line pointing at `trust-before-scale:autopilot` is not yet an extension: follow it, under this
core's lane gate and supervision ladder.

# Autopilot core

The extension and the host instruction file (`AGENTS.md`, `GEMINI.md` or `CLAUDE.md`) win where they also
speak, except that neither can loosen the lane gate (the upper bound on parallel work, whatever ceiling
the extension names) or the supervision ladder below.
If the extension is missing, report it and establish the project instructions before implementing.
Quality bars, budgets, priorities, platform tools, release rules and git flow belong to the project.
Nothing here grants permission to release or deploy.

## Supervision by adoption level

Supervision lifts one step per adoption level (`level` in the config). A config without `level` counts as level 1, here and
in the scripts: projects opt in to more autonomy. A `level` that is not 1, 2, 3 or 4 counts as level 1 here;
the scripts reject that config until it is fixed. Owner decision, 19 Nov 2026, for
every project, replacing unattended runs at any level: "autopilot level one should only be supervised.
slowly lift off supervision to level 4". The level caps everything below; the extension and host
instructions may only be stricter. Only the owner changes the level. Owner decisions, 19 Nov 2026: a
missing level means level 1, and gate code and governance stay the owner's at every level, level 4 included:
ask the owner before changing them, not only before merging. Like the rest of the ladder, no extension or
host instruction can loosen this.

| Level | Who starts a run | Plans | Merges |
|---|---|---|---|
| 1 | the owner, by hand, every run | the owner approves each one | the owner approves each one |
| 2 | the owner, by hand | the owner approves each one | the agent merges a PR whose every file is docs or prose and none is gate code or governance, after routine and gates; the owner merges the rest |
| 3 | runs may be scheduled or looped | owner-approved priorities | the agent merges a PR with no gate-code or governance file, after routine, gates and `skill-eval --check`; the owner merges the rest |
| 4 | runs may be scheduled or looped | the extension's priority order | full loop within the lane gate for a PR with no gate-code or governance file; the owner merges the rest, and the stop-and-ask list needs the owner |

**Gate code** is every check that decides what passes: the project's gates, hooks, CI workflows and
`scripts/tbs/`. **Governance** is what decides what agents may do: the trust-before-scale config, the
autopilot and routine extensions, host instruction files, every file `routine.ruleSources` lists, the enforcer table, and
agent settings (`.agents/`, `.claude/`, `.codex/`, `.cursor/`). The extension may add paths, never remove
them. Check every file in a PR, not its label.

Below level 3, never schedule a run or re-arm a wake-up. If the owner asks in person for an unattended or
overnight run, say the level does not allow it and offer supervised work. If a timer, schedule or loop
started this run, report that the level does not allow it and stop without implementing anything. Report and stop when the
supervised work is done. A merge the level does not allow is parked for the owner with the PR, its head
and the evidence. The ladder is an instruction, not a hook: no check enforces it mechanically.

## Step 0: falsify the handoff

Read `autopilot.handoff` (default `HANDOFF.md`) as claims to check, not facts. Run the extension's
session-start check if it names one; resolve each failed section or report its owner and next action,
and rerun before ranking work on a partial picture. Then run:

```bash
node scripts/tbs/self-merge.mjs --owed
node scripts/tbs/skill-eval.mjs --check
```

Review owed self-merges and the listed hook skips, then run `node scripts/tbs/self-merge.mjs --ack-skips`.
Check every handoff claim you will act on against current git and issue state, and measure an issue's
proposed root cause before building on it.

Run `ListAgents`, confirm each session's project from its branch or worktree, and message sessions
touching the same files. Wait for a reply or an idle notice; silence is not agreement. Repeat this
before every merge, and check live branches and open PRs too. A worktree or branch a live session holds
is never yours to push, rebase, commit to or remove, even when listed as unpushed: message its holder,
and act only once no live session holds it.

## Lane count

Run `node scripts/tbs/lanes.mjs` at session start and before every launch, and never run more
implementation lanes than it allows. Launch scripts can use `--require <n>`; `--json` gives the count and
reasons as data. When it caps at one, clear the printed reasons first; lane one stays available to repair
trust. Scaling requires `skill-eval --check --fresh` (records also recent, normally within seven days);
an unavailable check caps at one.

## Lanes and review

Every lane gets its own worktree, branch and committed brief. Before delegating, check its allowed files
are disjoint from running lanes, lanes awaiting review and open PRs. The project owns the mechanics
(for example `scripts/codex-lanes.sh`, `scripts/codex-implement.sh`, `scripts/session-start.mjs`); take
the actual commands from its extension.

Stop launching while one finished lane awaits review. Review and merge one at a time with the project's
gates and review ritual on the exact head, merging with `--match-head-commit <verified-sha>`. If the base
moved, merge it into the lane, rerun required gates and reviews, and push before merging. After each
merge, merge the base into every other lane, coordinating with running writers rather than editing under
them, and reverify affected work. Let project tooling perform these steps.

## Finish to merge

Push after every commit. Open a PR when the feature is built and ready for the project's review ritual, never a draft or a
PR for a brief alone; resolve findings and finish one feature to merge. Work that cannot finish gets no
PR: keep its branch pushed, comment on its issue with the branch, head and what is owed, and close any
existing PR for it with the same status.

## Autonomy

Follow the extension's priority order (at level 3, only owner-approved items). A blocked item is parked, never a reason to stop: add it to the
handoff's owner list with context and a recommendation, leave one issue comment, and pick the next
unblocked item free of file overlap. Under `/loop` (level 3 and up), keep going until a usage limit or the owner says stop.
If everything is parked, refresh the handoff and re-arm an idle wake-up to check issues and owner
answers; report if the session cannot schedule one. A parked list alone does not end the loop.

## Owner check-ins

If `autopilot.checkIns` is set, use its `timeZone` and `times`. At the first round boundary after each
time, batch unanswered parked questions, most blocking first; once per local day, never interrupting an
edit, gate or review, and skipped when there are no questions. Ask in simple words, recommended option
first, with a reason the owner can assess. An answer the owner did not type or select is absent:
defaults, elapsed time and plausible machine answers authorize nothing. Keep unanswered questions parked
and work elsewhere. Save real answers that round in the project's decision record or issue, update the
handoff owner list, and return unblocked items to the queue.

## A new owner decision

A changed rule is not landed until every live copy agrees. Use the extension's recording locations and
decision workflow:

1. Ask one scope question if the ruling's reach is unclear. Do not invent broader permission.
2. Record the owner's words, date, scope and the rule replaced where the extension says.
3. Sweep every live copy of the old rule, including instructions, handoff, briefs and priorities.
4. Create or update the tracking issue with the affected locations and an audit of the sweep.
5. Open a prose PR for the rule change and its audit, following the project's review ritual.

## Milestones

Keep membership current without asking: read milestone descriptions, place each candidate before starting
it, and move issues when the work shows they belong elsewhere, following project priorities. Milestone
meaning, dates and creation need the owner's typed instruction. Never rename or rewrite a milestone to
reconcile conflicting records; name the conflict and park that decision.

## Stop and ask

First search existing decisions and run checks that can answer the question. Park unanswered questions
for the owner and continue independent work when a change would:

- Alter data models, authentication or security.
- Delete or rewrite work outside the current slice.
- Overturn a recorded decision or a “do not fix back” instruction.
- Add a new dependency.
- Change gate code or governance (defined under "Supervision by adoption level"), at any level.

The extension adds project-specific triggers. Routine work within the authorized slice continues.

## On a limit or end of session

Refresh `autopilot.continuation` (default `docs/codex-continuation.md`) as a self-contained cold-start
brief: objective, current branches and heads, allowed files, completed checks, remaining steps, parked
decisions and the next exact action. Push all branches you own, then run the project's handoff skill;
report any push that cannot complete. After a run that overlapped a usage limit, inspect errors and the
checks that actually completed before trusting its results: a reported success does not prove its agents
or gates ran.
