---
name: ask-yak
description: Tells the user where their work is in the YesYak process and what comes next. It reads the branch, the progress file, specs, plans, reports, handoffs and pull requests, shows a map of the whole process with the current position marked, names the next skill and the rest of the way to the pull request, and waits. It never writes and never starts a skill alone. Use it whenever the user asks "what now", "what next", "where am I", "where are we", "which skill do I use", "what is left", is new to the skills, or seems lost between phases.
---

# Ask Yak

A person who is new to the skills must find the next step with one question. Read the state, answer, and wait.

## Rules

- Read only. Run only commands that read: `git status`, `git log`, `git branch`, `git diff --name-only`, `gh pr view <branch>` or `glab mr view` (or the environment's tools), `python3` with `scripts/check_yesyak.py`, and file reads. Do not change any file.
- Do not start the next skill. End with one question.
- Answer in the user's language. Keep skill names, file paths and commands as they are.
- The process map, the state signals, the entry points and one card per skill are in `references/process.md`. Read it first.

## 1. Find the slug

Follow "State signals" in `references/process.md`: the branch name first, then the docs in the branch diff, then `.scratchpad/`.

## 2. Find the position

Check the state signals of `references/process.md`, strongest first. The strongest signal found sets the position. Name the other signals you found, but do not use them. Then check the conflict table.

If git is missing or `gh` fails, say which signals you could not read, and answer from the others.

If nothing is found, show the entry points table and ask one question: feature, bug, resume, one task, or customize?

## 3. Read the adjustments

Run `python3` with the `scripts/check_yesyak.py` of this skill, from the project root. Its `active:` lines are the adjustments that apply: extra instructions (`add`), a replaced section (`replace`) or a skill switched off (`off`). If it reports problems or cannot run, say so. No adjustment applies until they are fixed.

## 4. Answer

Use three parts:

```text
You are here: 3 Make it work, step 3 of 7 (progress.md)

 0 Starter kit ✔ ── 1 Grill & sketch ✔ ── 2 Write the contract ✔ ── 3 Make it work ● ── 4 Break it ── 5 Sign your work ── 6 Retrospective

Next: execute-plan-loop, step 3 "Edit an order" of docs/orders-plan.md
Then: steps 4–7 → verify-against-spec → (browser-acceptance-testing) → red-team-review
      → triage-findings-list → execute-plan-loop (change-list mode) → write-visual-pr
      → pr-reviewer-guide → (feature-walkthrough) → session-retrospective-rules
Adjusted: verify-against-spec (add, project)
```

- Draw the map from the process map. Mark the current phase with ● and every phase before it with ✔. For Resume, the current phase is the phase of the step the handoff names. On the fix route, draw the fix route line instead.
- In "Then", list every later step in order, up to `session-retrospective-rules`. Put optional steps in brackets. Add "(adjusted)" after a skill with an `add` or `replace` entry. Leave out a skill with an `off` entry.
- In "Adjusted", name each adjusted skill, its mode and its scope, from the `active:` lines.
- Say which signal set the position, in brackets.

End with one question: start the next step now?
