---
name: handoff
description: Write a self-contained brief and dispatch one task to an agent under a hard time budget, or save a handover. Use when handing one task or half-finished work to an agent, writing its brief, restarting a stalled or timed-out run, sending findings back for a fix, or wrapping up to resume. Choosing agents is delegate.
user-invocable: true
argument-hint: "[--agent claude|codex|antigravity|zcode] [--model <id>] [--worktree] <task>"
---

# Handoff

The receiving agent starts with **zero context**: the brief is everything it knows. Write it so the agent could finish the task with no question back to you.

**User's arguments:** $ARGUMENTS

## Modes

- **Dispatch**: a task goes to another agent now. Everything below applies.
- **Resume**: the user is stopping or switching and wants the work continued later, by a new session or another agent. You write the handover and launch nothing; see "Resume".

Take Resume when the user is stopping or switching and asks to save the state, wrap up, continue later or hand over for later. A request to hand a task over now, with or without a named agent, is Dispatch: `delegate` picks the agent when none is named. When unsure whether the work starts now or later, ask in one line.

**Advisory (agent judgment):** Talk to the user in the language they are using, including questions and option labels; keep command names, flags, file paths, skill names and other technical names unchanged.

## Prerequisites

Dispatch only. Load the `delegate` skill and the host config it names. Requires the `delegate` skill installed beside this one. When it is missing, tell the user to add it (`npx skills add finolabs/vibecode --skill delegate`, or install the whole plugin) and stop. Grade and route the task there unless the arguments name an agent.

## Arguments

1. **Agent and model**: `--agent` and `--model`, or ones named in the text; otherwise the `delegate` routing.
2. **Isolation**: `--worktree`, or any parallel dispatch → a new git worktree on a short branch named after the task, cut from the integration branch tip (`commit-messages` "Branches").
3. **Task**: everything else.

## The brief

Read [references/brief-template.md](references/brief-template.md) in full before drafting; it owns the template, required environment constraint and lint command.

**Preserve task semantics.** Investigate-only → "Do not edit files." Fix → "implement the fix." Refactor → "refactor, not rewrite." Carry the user's exact intent and scope.

**Findings sent back.** While the run is still light, send the findings as a follow-up to the same run, one defect per item. Open a new run with a new brief, carrying what was tried, when the run has used about 60% of its context or the recorded rework limit (default two rounds) has not cleared the defects (`tidy` "Context pressure").

**Prose output.** Write the brief in English and name the output language and tone in the Task. When the result is social content or a document for readers, and the user's instructions give an editing pass for that language, the coordinator runs the pass at acceptance; the agent does not. A plain reply to a user needs no pass.

For Antigravity, write an edit-only brief when its commands fall outside both its allow-rules and what the user granted for this run (`delegate` "Route"), and paste the search results or excerpts it would otherwise fetch.

## Dispatch

1. Save the brief where `delegate` "Where files go" puts it, as `<slug>.md` (`tidy` titles): a local handoff brief in `.finolabs/briefs/`, a brief worth keeping as project documentation in the project's documentation folder.
2. Record the dispatch: `ledger.py start ...` (see `delegate`), keeping the id.
3. Launch the agent with the host config's command, under the hard cap, in the host's background mode (never `( … ) &` or `nohup`), with its log and final output in `.finolabs/logs/`.
4. Tell the user in one line: the run's name (`<runner>: <project> <scope> <activity>`, `tidy` "Titles"), agent, model, worktree, budget, check deadline, ledger id.

The completion notice brings you back. At the check deadline, judge liveness from artifacts as `delegate` describes, then accept and record the outcome there.

## Resume

Load `tidy` "Handover content" and follow its save-and-continue procedure. It is the one home for handover content, storage, read-back and continuation. This mode launches nothing. Requires `tidy`; when it is missing, tell the user to add it (`npx skills add finolabs/vibecode --skill tidy`, or install the whole plugin) and stop.
