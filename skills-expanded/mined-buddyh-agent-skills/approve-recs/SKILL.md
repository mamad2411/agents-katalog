---
name: approve-recs
description: >-
  Turn an agent's recommendations into one-click approvals using the host's
  question tool (AskUserQuestion in Claude Code, request_user_input in Codex,
  or the equivalent), then carry out whatever the user approves. Each
  recommendation becomes a question whose first option is the recommended
  action, so the user can approve the whole batch without typing. Use this
  whenever the user says "/approve-recs", "give me the approvals", "let me
  approve these", "ask me with the question tool", "queue these up for
  approval", "what do you need me to sign off on", or "walk me through the
  calls". It works on any list of calls from this conversation (PR review
  MERGE/FIX/REBASE/CLOSE calls, punch list next steps, cleanup candidates,
  triage results), or on a report file the user names. Also use it unprompted
  at the end of a report or review turn that leaves the user several
  decisions, instead of listing them as text.
---

# Approve recommendations

People often read reports on a phone or between other work. Typing out "yes merge 46 and 49, rebase 132, skip the rest" is friction. The goal here is to turn each recommendation into a question with the recommended answer already first. That way approving everything takes a few taps, and changing one call is a single different choice.

## 1. Collect the recommendations

Use the most recent set of calls in the conversation. If the user names a file (for example a PR review report), read it and take the calls from its table and details. If the last report came from a scheduled run, it is still valid input. The user is here now, so this is the live approval step that the scheduled run couldn't do.

Write each recommendation as a concrete action that you can carry out exactly as worded:
- **Good:** "Merge https://github.com/acme/webapp/pull/46 with a merge commit (no deploy)."
- **Bad:** "Handle webapp#46."

If an action has a precondition or a side effect, put it in the option description. Examples: "mark ready first", "rebase, then request a review", "set the database credentials before the next run".

Leave out items that need nothing from the user, such as WAIT items blocked on something external. Ask about a WAIT item only when the user has a real choice to make, for example whether to close a stale draft.

## 2. Ask with the question tool

Use whatever structured question tool your host gives you: `AskUserQuestion` in Claude Code, `request_user_input` in Codex, or the equivalent elsewhere. The field names and limits below are Claude Code's. On another host, keep the same shape and adapt to that tool's fields and limits.

If you have no question tool, list the recommendations as numbered text in the same wording, recommended action first, and tell the user how to reply, for example "approve all", "approve 1, 3", or "2: fix first".

**Shape of each question:**
- Give each recommendation its own question.
- `header` is short (12 characters or fewer in Claude Code) and names the target, for example `webapp#46` or `api#10`.
- `question` says what will happen, in one sentence that ends with "?".
- Options, 2 to 4 of them:
  1. The recommended action, with " (Recommended)" at the end of the label. The description is the one-line reason.
  2. One realistic alternative, if there is one. For example, the recommendation is MERGE and the alternative is "Fix first", or the recommendation is CLOSE and the alternative is "Keep open".
  3. "Skip for now": do nothing this round.
- If the tool already offers a free-text "Other" choice, as Claude Code's does, don't add your own.

**Batching:**
- Claude Code's tool takes at most 4 questions per call. Ask in rounds of that size, in report order (MERGE first), and keep going until every item has been asked.
- Before the first round, say in one line how many decisions there are and how many rounds that makes.
- When there are more than 8 items of the same kind (for example 8 FIX items that all mean "start a fix session"), group them. Use one multi-select question (`multiSelect: true` in Claude Code) that lists up to 4 targets per question, so the user can tick the ones to approve.
- Don't ask about the same item twice in one session.

**Ordering hint:** put the decisions that unblock other work early. For example, ask about merging #132 before #134, because #134 is stacked on it.

## 3. Act on the answers

An approval through this tool counts as the user's explicit go-ahead for exactly the action written in the option you showed. It doesn't cover anything more. A merge approval doesn't cover a deploy, and "start a fix session" doesn't cover a merge. If carrying out an approved action turns up a step you didn't name, stop on that item and ask about it separately. One example is a new conflict. Another is a deploy the merge triggers.

- **Order:** carry out approved items in dependency order. Merge the base PR before the stacked one. Rebase before you request a review.
- **Long work:** fan independent long jobs, like fix sessions on separate repos, out to background agents rather than doing them one at a time inline.
- **"Other" answers:** treat the typed text as the user's instruction for that item. If the text is ambiguous, ask once more about that item only.
- **Skipped items:** do nothing.
- **Hard limits:** the user's standing rules (CLAUDE.md, project instructions) and the safety rules still apply, such as no force pushes or no unapproved deploys. An approval here can't override them. If the recommended action would break one of those rules, it shouldn't be the first option in the first place.

## 4. Report back

Finish with a short table: item, the decision, what actually happened (commit SHA, PR state, session started, error). Mark failures plainly.

If the recommendations came from a report file, append a dated section to that file called "Approvals (YYYY-MM-DD HH:MM)" with the same table, so the next run can see what was decided. If an item is tracked in an issue tracker or task list, add a note there with the decision too.

## When the user isn't there

Scheduled and unattended runs can't ask questions, so don't call the question tool in them. Instead, end the report with a section named "Ready for approval". List each recommendation in it in the same wording you'd use for the question: the target, the recommended action, the alternative. The user can then run `/approve-recs` on that report later and get the one-tap version.
