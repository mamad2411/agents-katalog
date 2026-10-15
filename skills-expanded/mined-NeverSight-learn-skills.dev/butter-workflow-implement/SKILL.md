---
name: butter-workflow-implement
description: |-
  Trigger: docs/specs/{TASK-ID}/00-META.md exists with Status planned, and the user approves that spec or asks for it to be built ("implement this", "build the approved plan", "continue the implementation"). Both conditions are required. Reads workflow state, applies the approved track scope, runs verification, commits task-sized changes, pushes, and creates or updates a PR.
  Skip: no docs/specs/{TASK-ID}/00-META.md exists — the user never started a Butter Workflow, so do the requested work directly rather than pulling in this stage. Also skip for spec-file edits and single follow-up fixes inside an active workflow — apply those directly. Also skip once a PR already exists and is awaiting review — use `butter-workflow-code-review` instead.
---

# Butter Workflow Implement

Implement the approved spec while preserving the docs as the handoff surface.

## Workflow

1. Read repository instructions first.
2. Read `~/.agents/preferences/preferences.md` when it exists and follow it while implementing. It is the only preference file.
3. Find the active task docs:
   - Prefer the task id or path supplied by the user.
   - Otherwise inspect `docs/specs/*/00-META.md` and choose the one whose status is `planned` or whose working branch matches the current branch.
   - Ask the user only when multiple plausible active specs exist.
4. Read the spec for the task's track:
   - Always: `00-META.md` and `01-SPEC.md`.
   - Track B/C also: `02-PLAN.md` and relevant `03-TASK-*.md`.
   - Track C also: `02-PLAN.md` `Risk Review Targets`.
   - Track A implements from `00-META.md` and `01-SPEC.md` only.
5. Prepare the working branch from `00-META.md` before implementing. Ask first when the working tree is dirty or any branch create/switch operation would be risky:
   - If the `Working branch` does not exist, create it from the `Base branch` with `git switch -c <working-branch> <base-branch>`.
   - If it already exists, switch to it.
6. Implement only the current task scope. Do not expand beyond the spec without updating it or asking the user when scope/risk changes.
7. Run targeted verification after each meaningful task:
   - Use repo-native commands from package scripts, build files, test config, or existing documentation.
   - Prefer focused tests first, then broader checks if shared behavior changed.
8. Commit task-sized changes:
   - Follow the repository's existing commit style.
   - Use `git` for status, diff, add, commit, and push.
   - It is acceptable to skip a commit for investigation-only tasks with no file changes.
9. After all tasks are complete:
   - Push the working branch.
   - Create a PR with MCP when available. If unavailable, use `gh` only for PR work when installed/authenticated.
   - Use the repository PR template when present.
   - Include background, summary, verification, related issue, and any user decisions needed.
10. Update `00-META.md`:
    - Set `Status: implemented`.
    - Fill `PR URL` when known.
    - Commit the metadata update if it is part of the implementation branch.
11. Recommend the `butter-workflow-code-review` skill. It is the last stage of the workflow.

## Follow-Up Requests

This stage is done once the PR exists. An active workflow does not make every
later message a stage transition. Route the next one:

- A specific code fix, or a list of feedback to apply — apply it, run targeted
  verification, commit, and push to the working branch. Do not run
  `butter-workflow-code-review` for it.
- A request to review the change — hand off to `butter-workflow-code-review`.
- A spec change — update the spec file, then make the matching code change.

Routing is independent of `## Preference Capture`. Whichever branch a message
takes, it still goes to a capture agent. A request to apply feedback is the
most common source of preferences, not an exception to capture.

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

## Constraints

- Do not perform code review as a separate critique during implementation. Defer full diff review to the code-review stage.
- Keep verification output out of files unless the repository already has a convention for test artifacts.
- If the implementation materially differs from the spec (`01-SPEC.md`, or `02-PLAN.md` for Track B/C), update it before or with the code change.
