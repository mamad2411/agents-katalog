---
name: feature-delivery-pipeline
description: Orchestrates the full feature workflow from a vague request to a reviewed pull request, with a checkpoint for the user after every phase. The phases are interview, acceptance spec, walking-skeleton plan, optional work items, step-by-step implementation, verification, optional browser testing, red team, triage and fixes, visual PR, reviewer guide and retrospective. yak-pilot starts it for a feature request after the user approves the plan, and says which checkpoints are gates. Use it directly only when the user names it, asks for "the full process with a checkpoint after every phase", or yak-pilot is not installed.
---

# Feature delivery pipeline

This skill runs the other skills in order. Each phase ends at a checkpoint: a short summary in the user's language, the artifact path, the defaults you took and one clear question. Then wait. Do not start the next phase in the same message, unless `unattended-run` is active. The user often changes direction at a checkpoint; that is the point of it.

## Conventions for the whole pipeline

Load these first and keep them active: `simplified-technical-language`, `scratchpad-working-files`, `git-commit-organizer`, `no-slop-code`, `decision-record-log`, `traffic-light-findings`, `plain-visual-docs`.

If the user asks you to run without them ("do not ask me", "take the decisions yourself"), also load `unattended-run`. It turns every checkpoint below into a logged decision and a status line, and it says which actions still need the user. When `yak-pilot` started the run, its plan says which checkpoints are gates; the others become logged decisions of `unattended-run`.

## Phases

Invoke every phase skill with the skill tool, not by reading its file. If a project skill is not listed, read the project `SKILL.md` directly and tell the user. Do the same if the base directory that the tool prints is neither in this repository's skills folder (for example `.claude/skills/` or `.agents/skills/`) nor the target of a symlink there. A user skill with the same name shadows it.

```text
0 Starter kit         branch → slug → .scratchpad/<slug>/ → progress.md → does it fit in one iteration?
1 Grill & sketch      on-the-spot → (prototype-options) → domain-language
2 Write the contract  write-acceptance-spec → (red-team-review: devil's advocate on the spec)
                      → write-acceptance-spec (refine) → walking-skeleton-plan → (work-items-breakdown)
3 Make it work        execute-plan-loop
4 Break it            verify-against-spec → (browser-acceptance-testing) → red-team-review → (agent-hook-guard)
5 Sign your work      triage-findings-list → execute-plan-loop (change-list mode)
                      → write-visual-pr → pr-reviewer-guide → (feature-walkthrough)
6 Retrospective       session-retrospective-rules → (handoff-and-resume, when the work pauses or changes hands)
7 Later               production-readiness-review, when the user prepares a deploy
```

A bug report enters through `bug-intake` instead of phase 1. It reproduces the bug, finds its contract and runs the short fix route, which ends with `write-visual-pr` (short) and `session-retrospective-rules`.

The map of the whole process is in `ask-yak/references/process.md`. This block lists the same skills per phase.

Steps in parentheses are optional. Offer them; do not run them by default.

| Phase | Checkpoint question |
| --- | --- |
| 0 Starter kit | Branch name confirmed? Does it fit in one iteration, or which delivery first? Write the working rules from the chat to AGENTS.md? |
| 1 Grill & sketch | Decisions complete? Prototype chosen? Terms agreed? |
| 2 Write the contract | Spec approved? Challenge findings to apply? Plan approved? Work items needed? |
| 3 Make it work | Loop finished, or where it stopped |
| 4 Break it | Browser testing wanted? Red team missions? |
| 5 Sign your work | Which changes from the list to apply now? Create the PR? Post the guide as a comment? |
| 6 Retrospective | Which guards to apply? |

## Phase 0: Starter kit

1. If AGENTS.md has no YesYak block, or the block says YesYak is not set up, say it in one line and offer `customize-yak` first. Go on without it if the user says no. Ask for the branch name if the user did not give one; derive the slug. If the branch name is fixed and not descriptive, choose the slug separately (`git-commit-organizer`).
2. Create the branch from the default branch, or from the base branch the user names. Record the base branch in `progress.md`, because the pull request targets it. If the project has a git host, check now that the branch can reach it (a remote, signed-in tools), not at the end.
3. Make sure `.scratchpad/` is ignored; create `.scratchpad/<slug>/progress.md` with the phase table.
4. If the user gives working rules in the chat (language, branch names, commit style), propose to write them in AGENTS.md, outside the YesYak block (`customize-yak` rewrites that block). A rule that stays only in the chat is lost in the next session.
5. Fix obvious inconsistencies you find in AGENTS.md only if the user agrees.

### Does it fit in one iteration?

Before the interview, read the request and the code it touches and give one verdict:

| Verdict | When | Next |
| --- | --- | --- |
| Fits | One spec and one plan can cover it, and one pull request can deliver it | Phase 1 |
| Split | It holds more than one result that a user can check on its own | Propose the deliveries; the user chooses the first one |
| Information missing | You cannot size it | Phase 1 starts with the questions that size it |

Split by deliveries, not by technical layers. Each delivery is complete and can be verified on its own. Order the deliveries by dependency. Use the smallest number of deliveries. The other deliveries go to the out-of-scope section of the spec, so they are not lost.

## Keeping state

Update `progress.md` at every checkpoint: phase, status, artifacts, commits. If the session stops, a new session reads it and resumes at the right phase and step.
