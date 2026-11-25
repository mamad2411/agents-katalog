---
name: tidy
description: Name and rename sessions, save handovers and write back decisions. Use at a session's first task, after a compaction, on a task or phase change or stale title, on a request to rename, wrap up, save, hand over or resume later, past 60% context, on a writer change, or to remember or recall decisions, lessons or state.
---

# Tidy: session hygiene

## Context pressure

**Advisory (agent judgment):** Talk to the user in the language they are using, including questions and option labels; keep command names, flags, file paths, skill names and other technical names unchanged.

When the compaction nudge fires, context passes about 60%, the host is about to compact, or work hands over to a fresh session or another writer, read [references/context-pressure.md](references/context-pressure.md) and follow it: the context check (`context_steward.py`), the handover before compaction (`handover_state.py`), when to compact or start fresh, and the writeback. The host owns its compaction threshold; the writeback is advisory (agent judgment). A rename alone does not need it.

## Remember or recall

Corrected-lesson example: on 2026-11-07 a delegated test assertion dumped the process environment into the run log and provider context; retain the rule to use synthetic environments and compare variable names only.

When the user asks to remember something or recall earlier decisions, lessons or project state, load [references/knowledge.md](references/knowledge.md). Use that procedure also when preserving a settled decision or lesson, or resolving a disagreement between notes and the repository. Load it only for this knowledge work; naming a session or preparing a handover with nothing new to remember does not need it.

## Handover content
Read [references/handover.md](references/handover.md) for saving and continuing a handover; `handoff` Resume points here.

## Titles

A title tells the user which session holds which work, without opening it: `<emoji> <project> <scope>: <activity>`.

- **emoji**: one emoji for the kind of work, from the fixed set in [references/titles.md](references/titles.md) (🐛 fix, 🔍 review); change it with the activity.
- **project**: the repository or product name the user knows, as short as stays unambiguous (`billing-api`).
- **scope**, optional: the feature, spec or ticket the work belongs to (`003 search`, `PAY-142`, `US4`, `T044–T046`). Leave it out for work that has none.
- **activity**: what the session is doing now, verb-led, a few words (`fix webhook retries`, `review PR 12`, `plan rate limits`). A review, advice or committee session says so.

Keep the title near 50 characters, the activity in English unless asked otherwise, technical names intact. Examples: `🐛 billing-api: fix webhook retries`, `✨ billing-api 003 search: T044–T046 rebuild CLI`, `🔍 docs-site: review PR 12`.

When to name: at entry, in the first turn whatever the task (a question or a chore too, not only coding; a title the host made from the first prompt does not count), on a resume whose title no longer matches the work, when the task or phase changes materially (a new story, planning to implementation to review), and when a spec, story or large pull request the session ran is done: a coordinator session that carries on renames to its next work (the merge notice reminds it after `gh pr merge`). Do not rename for every step. Check the title again after a compaction.
Advisory (agent judgment): where the host's rename tool needs this session's own id, a session can read its id from the "started by" entry of a child session it started itself; with no such child, say so in one line and ask the user to
rename, and do not guess ids or retry blind.

Sessions you start: a session you open for other work (on the Claude Code desktop app, the session-start tool's `title`) gets this same format at the moment you start it, emoji included (advisory, agent judgment).

Whose: rename only this session and sessions you started; a session someone else started keeps its name unless the user asks. A delegated run takes its title, or its log file name where the host has no titles, from its ledger project and task label (`delegate`).

**Background runs and agents.** Every background task or agent you start (a headless Codex, Antigravity or Claude run, a reviewer or other subagent) gets a name at the moment it starts that says who runs it and what it does: `<runner>: <project> <scope> <activity>`. The runner is the agent family and a short model name (`codex sol`, `agy flash`, `claude sonnet`) or, for a reviewer or other subagent, its role (`code review`, `sec review`). Examples: `codex sol: billing-api T044 rebuild CLI`, `code review: billing-api PR 12`. Put the same label in the host's name or
description field for the run (`ledger.py start` prints it), the log file names (as the slug form of `references/titles.md`) and the one line you tell the user at dispatch. The label is plain words you write yourself, never copied from an issue or pull request title, and it is passed to a command only as a quoted argument, never through a shell expansion. The enforcer is agent judgment, so this is advisory: no hook renames a tool call.

Titles carry no secrets, customer data or private history. Use the host's supported mechanism ([references/titles.md](references/titles.md)); where a host offers none, say so in one line and carry the name in the handover and log file names instead. Pin the active session and unpin retired ones only where the host supports it and the user allows it. Session stores and app databases are never edited by hand.

Before archiving a session, turn off its remote access where the host keeps a switch for it; the host steps are in [references/titles.md](references/titles.md) "Archiving". Advisory (agent judgment).

## Writers and checkouts

- One writer per scope, with an explicit handover between writers.
- Prefer a suitable existing checkout or worktree; stricter isolation rules win.
- Keep notes, briefs and logs in a durable local folder (`.finolabs/` at the main checkout's root, kept out of git, unless the host config names another); temporary directories and scratchpads are wiped on restart.
