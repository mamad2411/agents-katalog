---
name: butter-workflow-code-review
description: |-
  Trigger: docs/specs/{TASK-ID}/00-META.md exists with Status implemented or a recorded PR URL, and the user asks for that change to be reviewed ("review this PR", "check this diff"). Both conditions are required. Collects track-specific context (issue, plan, task, risk targets), reviews the diff and review comments, applies safe fixes, and escalates design or scope-changing feedback.
  Skip: no docs/specs/{TASK-ID}/00-META.md exists — this is not a Butter Workflow, so handle the review request directly rather than pulling in this stage. Also skip when the user only wants specific feedback applied — apply, verify, commit, and push it directly. Also skip when nothing is implemented yet — use `butter-workflow-implement` first.
---

# Butter Workflow Code Review

Review the implemented diff with context from the issue and workflow docs.

## Workflow

1. Read repository instructions first.
2. Read `~/.agents/preferences/preferences.md` when it exists and review against it. It is the only preference file.
3. Determine review target:
   - Prefer a PR URL supplied by the user or recorded in `00-META.md`.
   - Otherwise review the current branch diff against the base branch from `00-META.md`.
4. Collect context by track:
   - Track A: PR diff or branch diff, related issue, existing PR review comments, and `01-SPEC.md` as the requirement reference.
   - Track B: Track A context plus `02-PLAN.md` and relevant `03-TASK-*.md`.
   - Track C: Track B context plus `Risk Review Targets`.
5. Use MCP for PR and review comment access when available. If unavailable, use `gh` only for PR lookup, PR diff, and review comments when installed/authenticated.
6. Review in this order:
   - Requirement mismatch.
   - Bugs and behavioral regressions.
   - Side effects outside the planned scope.
   - Architecture boundary violations.
   - Security, authentication, authorization, privacy, and data integrity issues.
   - Missing tests or weak verification.
   - Conflicts with `preferences.md`.
7. For Track C, explicitly inspect every `Risk Review Targets` item and report whether the implementation satisfies its `review-focus`.
8. Classify findings:
   - Immediate fixes: clear bug or small stability/test fix, low scope, no plan/preference conflict.
   - User decision: design change, scope expansion, plan conflict, preference conflict, or trade-off with no obvious winner.
9. Apply immediate fixes when safe, run targeted verification, commit, and push.
10. Present user-decision items with the feedback, benefit, downside, recommendation, and why user input is needed.
11. Update PR body or comment with review/fix summary when a PR is available.
12. Update `00-META.md` to `Status: reviewed` only after review and required safe fixes are complete. `reviewed` is the terminal state: the workflow ends here, and preferences were already captured along the way by `## Preference Capture`.

## Follow-Up Requests

An active workflow does not make every later message a stage transition. Route
the next one:

- A specific fix requested after the review — apply it, run targeted
  verification, commit, and push. Do not re-run the full review for it.
- A request to review again after new commits — re-run this stage against the
  updated diff.
- Anything else — an ordinary request; carry it out directly. The workflow ends
  at `Status: reviewed`.

Routing is independent of `## Preference Capture`. Whichever branch a message
takes, it still goes to a capture agent. A request to apply review feedback is
the most common source of preferences, not an exception to capture.

## Preference Capture

Keep this section identical in `butter-workflow-start`,
`butter-workflow-implement`, and `butter-workflow-code-review`. When you change
one copy, change all three.

### What Counts

Record anything that would help you write a better plan, a better change, or a
better review next time. The bar is deliberately low. It is not limited to what
the user would call a "preference".

Most useful signals arrive attached to one specific thing. The user says "this
component is too complex, simplify it", not "I like simple code". **Extract the
general rule behind the request and record that rule.** Never skip a request
just because it names a file, a function, or a value.

- "Write the plan in Korean, not English" → plan documents are written in
  Korean from now on.
- "This component's logic is too complicated, unpack it" → favor simple, direct
  code; do not pile on defensive handling for unlikely cases.
- "Leave the tool credit out of the commit message" → commit messages carry the
  change description only.

When unsure, record it. A wrong entry costs the user one line to delete. A
missing entry is invisible to them and never gets corrected.

Skip only these:

- `preferences.md` already holds an entry that means the same thing.
- The project instruction files (`AGENTS.md`, `CLAUDE.md`, or equivalent)
  already state it. Project rules are not preferences.
- It is a pure one-off with no rule behind it: a single value, a rename, a
  scope tweak for this task alone.
- It carries no content: a bare approval, acknowledgement, or rejection.

Judge equivalence by meaning, not by string match. The same rule worded
differently is the same entry.

### Delegate The Judgement

Do not decide what is worth recording yourself. When a user message carries any
content at all — feedback, a request, a question, a correction — hand the
message to a separate capture agent and get on with the work the user asked
for. The two run in parallel.

The only call you make is whether the message has content, not whether it is
worth recording. A message that is nothing but "ok", "looks good", or "go
ahead" needs no agent. Everything else gets one.

This holds no matter how `## Follow-Up Requests` routes the message. A spec
edit, a code fix, a list of review replies — each still gets a capture agent.
Routing decides what work you do; it never decides whether capture happens.

Give the capture agent:

- The user's message, verbatim and unsummarized.
- The current stage name.
- The path `~/.agents/preferences/preferences.md` and the project instruction
  file paths.

Instruct it to:

1. Read `preferences.md`. When it is missing, create it with the eight
   category headings listed below, each holding `- None yet.`
2. Read the project instruction files.
3. Split the message into separate items. One message may carry dozens; judge
   each on its own.
4. Extract the general rule behind each item.
5. Record the rule when it could shape a future plan, change, or review. Record
   when unsure.
6. Skip items that hit a skip condition.
7. Replace the older entry when a new one contradicts it. Do not ask.
8. Delete an entry when the user asks for it to be dropped.
9. Write the file.
10. Return one line per entry recorded, replaced, or deleted. Return nothing
    otherwise.

Writing rules for the agent:

- Add, replace, or delete single entries only. Never rewrite or reformat the
  whole file.
- File each entry under one of `Planning`, `Architecture`, `Naming`, `Testing`,
  `Implementation`, `Review And PR`, `Working Style`, `Communication`. Add the
  heading when the file lacks it.
- Replace a section's `- None yet.` placeholder when adding its first real
  entry.
- Never ask for approval first.

When the tool has no subagent mechanism, do the same work inline at the end of
your response. Same criteria, same writing rules, same report. Only the place it
runs changes.

### Report

Collect the capture agent's result before ending the turn and append its lines
to your response, written in the language the user is working in:

- `Preference recorded: <one-line summary>`
- `Preference updated: <old entry> → <new entry>`
- `Preference removed: <deleted entry>`

Say nothing when nothing was recorded.

Recording is never a substitute for acting. Apply the request to the current
work as well.

## Review Output Format

Lead with findings ordered by severity. Use file and line references when possible.

For no findings, say that no blocking issues were found and list residual risk or unrun verification.

Avoid broad refactors unless they directly reduce risk identified by the review.
