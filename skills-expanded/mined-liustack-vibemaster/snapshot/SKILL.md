---
name: snapshot
description: Task-state snapshots for session handoff. Write a resumable snapshot when wrapping up, restore from it when picking the work back up, trusting its decisions and re-checking its facts. Use when the user says 打个快照 / 交接 / 收尾下次接着做 / 换个会话继续 / 上次做到哪了 / 快没上下文了先记下进度 / snapshot this task / handoff / wrap up this session / pick up where we left off. Do not trigger for jest/vitest test snapshots, VM/database/filesystem snapshots, compressing the current conversation (that is /compact), remembering long-term preferences (that is platform memory), or deliverables addressed to humans (design docs, onboarding docs).
---

# snapshot: task-state snapshots

Iron rule: **the reader is a new session that knows nothing.** There's exactly one bar to clear: reading only this snapshot, they can carry on without re-asking, re-checking, or re-litigating decisions that are already settled. A memo written for yourself doesn't clear it.

## Writing a snapshot (wrapping up)

Save it to the workspace draft directory at `.issues/<YYYY-MM-DD-topic>/snapshot.md`. If the task already has a directory, write into it. When the same task wraps up again later, update that same file (it's a living document, not a log). Before writing to disk, make sure the draft directory is ignored: if `git check-ignore .issues` fails, append `.issues/` to `.git/info/exclude` (a local ignore, leaving the shared `.gitignore` untouched) and let the user know. In a non-git environment there's no commit risk, so write directly.

**Where the handoff lands decides what must travel.** `.issues/` is machine-local (gitignored), and uncommitted changes exist only here, which is exactly right when the reader is this machine's next session. When the work moves to another machine or someone else's agent, a local snapshot hands over nothing: push the work to a WIP branch, carry the snapshot's content in something that travels with the repo (the commit message, the PR description, or a file the user chooses to commit), and say out loud which parts stay machine-local.

Five sections, ordered by what the new session needs, not by chronology:

1. **Goal and current state**: one line on what the task is and how far along it is overall.
2. **Decisions already made (questions not to reopen)**: each one with its reasoning. The biggest waste in a new session is re-litigating something already settled: write the reasoning in full, this section never gets to summarize.
3. **Verified state**: which files changed, and the actual results of tests and lint (pass or fail, and what command ran them). Anything unverified gets written as "unverified," never "should be fine."
4. **Next steps and blockers**: an ordered to-do list, each item with enough context to act on. Blockers get their own list: questions waiting on the user's call stay exactly as open questions, don't decide for them.
5. **State pointers**: branch, uncommitted changes, commands that need rerunning, key file paths, rollback point, and what has to be running for the work to continue (dev server, containers, required environment variables).

Content discipline:

- Write state, not narrative. The compression standard is "what the new session needs," not "what happened in this session."
- One screen is the budget. Past roughly 40 lines, the snapshot is either narrating or copying content a pointer could reference.
- Risk splits into two kinds: **an accepted cost** (flagged as not to be reopened) and **an open problem** (goes into blockers). Don't mix the two.
- When a specialized workflow already has its own file on disk (a diagnosis log, a spec, ideation output), don't copy its content, just point to it and add one line on its current state.

## Restoring (picking work back up)

1. **Find the snapshot**: the one the user names. Otherwise scan the task directories under `.issues/`: one clear recent candidate, take it. Several plausible ones, show them one line each and let the user claim theirs. Newest is a tiebreaker, not a verdict.
2. **Trust the decisions, verify the facts.** Inherit settled decisions directly, without reopening them. Check reality fast (branch, `git status`, the files and test results the snapshot points at): reality may have drifted, reality wins, and any drift found gets written back into the snapshot.
3. **Report before resuming.** "Where were we" is a question, so answer it first: goal and progress, what's verified, the next step, the blockers, in a few lines, drift included. Act after the user nods. Only when the request itself already says continue does the work start without the pause, and blockers still get surfaced first.
4. **Route the work where it belongs**: implementation continues through coding's loop, an unknown-cause anomaly goes to dig, a requirement that turned out unsettled goes back to shaping.

## Division of labor with the platform

Compressing the current session belongs to the harness's /compact. Long-term project knowledge belongs to platform memory. Replaying a session verbatim belongs to resume. This skill does only what those three don't: **a deliberately structured, distilled task snapshot meant to be read by any downstream consumer** (a new session, another tool, someone else's agent). When publishing externally (an Issue/PR), never paste the snapshot verbatim, distill it into a publish-ready final draft first.

## Silent exit

A request this skill does not fit (a test snapshot, a VM image, compressing the current conversation) gets completed directly. Zero ceremony, no mention of this skill. When it cannot be told whether this applies, it does not.

## Red flags: stop the moment these thoughts show up

| Thought | Reality |
|---|---|
| "Summarizing the chat log counts as a snapshot" | The reader needs state, not narrative. A compressed narrative is still a narrative |
| "Just write the decision's conclusion, no need for the reasoning" | A decision with no reasoning attached is guaranteed to get re-litigated by the new session. The call you made was for nothing |
| "The tests should all be passing" | Verified state only counts actual runs: if it wasn't run, write that it wasn't run |
| "Let whoever picks this up figure out the next step" | Right now, at wrap-up, you're the person who understands the situation best. That understanding disappears the moment it isn't written down |
| "The snapshot is on disk, so the handoff is done" | A gitignored file and uncommitted changes don't follow the work to another machine or someone else's agent. See where the handoff lands |
| "Restore means start working immediately" | The user asked where things stand. Report first, resume on the nod |
