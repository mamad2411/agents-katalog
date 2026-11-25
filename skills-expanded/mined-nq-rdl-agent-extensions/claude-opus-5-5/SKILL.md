---
license: MIT
description: >-
  Prompting and harness guidance specific to Claude Opus 5.5 (claude-opus-5-5).
  Use when writing or tuning a system prompt, agent loop, or Messages API
  request for Opus 5.5, or when migrating prompts from Claude Opus 5. Also use
  when choosing an effort level, when a request with thinking disabled returns
  400, when an unattended agent stops after reporting progress, when long
  agentic turns look silent, when a response has stop_reason "refusal", or when
  chat replies start slowly.
compatibility: >-
  Claude Opus 5.5 (claude-opus-5-5) on the Claude API. Verified 2026-09-28
  against Anthropic's "Prompting Claude Opus 5.5" guide, the Opus 5.5 migration
  guide and the effort docs. Beta header names are as of that date.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Prompting Claude Opus 5.5

This skill covers only what changed from Claude Opus 5. For general prompt
engineering, use `/prompting:engineer`.

**Verify first.** Beta headers, defaults and effort behaviour change between
releases. Where a wrong answer would mislead, check the canonical sources:
the [prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5),
the [migration guide](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide#migrating-from-claude-opus-5)
and the [effort docs](https://platform.claude.com/docs/en/build-with-claude/effort).
The four breaking request changes (thinking cannot be disabled, forced
`tool_choice` returns 400, preserved thinking, the computer-use toolset) are
covered in the migration guide. This skill covers only their prompting side.

## One rule behind several fixes

Set every system-prompt addition and every tool **from the first request of the
session**. On Opus 5.5, editing `system`, `tools` or earlier messages mid-session
invalidates the conversation's earlier thinking blocks. The error is a 400 for
accounts created on or after 2026-08-31. Add mid-session instructions as
appended messages and never delete them afterwards.

## Find the symptom

**Turns run long, or cost more than on Opus 5.**
- The API default effort is `medium`; Opus 5 defaults to `high`. Set `effort`
  explicitly. Level names do not map across models: Opus 5.5 at `medium` matches
  or beats Opus 5 at `high`, and `low` comes close on several coding evals.
  Carrying over the Opus 5 value gives longer turns and more output tokens. Opus
  5.5 thinks more per turn at a given level, especially at `xhigh` and `max`.
- Start at `medium`, sweep the neighbouring levels on your own evals, and keep
  `xhigh` and `max` for measured gains.
- To reduce thinking, **lower effort before adding "think less" prompts**.
- Thinking counts toward `max_tokens`, even when it is not returned. Size the
  limit for thinking plus the reply. Anthropic reports that 128,000 works for
  long agentic coding turns.
- Changing top-level `effort` between requests invalidates the prompt cache. Use
  a per-message effort change instead (beta
  `mid-conversation-output-config-2026-07-01`).

**400 on `thinking: {"type": "disabled"}`, or the Opus 5 route ran thinking-off.**
Thinking is always on. Omit `thinking` and start at `low`. If time to first
token still matters, measure the line "Answer directly without deliberating."
Delete prompt lines that asked the model to write its reasoning in the reply.
Read `display: "summarized"` thinking blocks instead. The old lines can now
trigger a `reasoning_extraction` refusal. Delete any "don't think" rule as well.
Re-test the Opus 5 thinking-disabled mitigation instruction. Read content blocks
by `type`, not position.

**An unattended agent stops after reporting progress.** Progress updates can end a
turn with `stop_reason: "end_turn"` while work remains. The harness should treat
a text-only end of turn as a report, not as completion:
- Track the task's parts in a checklist the model updates, such as a to-do tool
  or a file. If items are open and no blocker is stated, send a user message
  naming them. Alternatively, have a smaller model check the completion
  condition and return its reason as the next message.
- Allow at most two or three automatic continuations per task, then stop for
  review.
- If a background command or subagent is still running, wait for it and return
  its output as the next user message.
- For fully unattended agents only, add the "named early stops" system-prompt
  paragraph from the first request. Keep your own confirmation step for risky
  actions.

**Long agentic turns look silent.** Text written between tool calls now arrives as
progress-update `thinking` blocks, not `text` blocks. They are empty unless you
set `thinking.display: "updates"` (beta `thinking-display-updates-2026-08-18`).
Then render non-empty thinking blocks before the `tool_use` they precede. If the
model must hand over verbatim content mid-turn, such as code or an exact value,
give it a send-message tool from the first request. State the update cadence
you want in the system prompt. If turns still go quiet, the harness can count
consecutive tool steps with no readable text. After about five, append the
"quiet stretch" reminder as a turn-scoped system message (`clear_at:
"next_user_message"`, beta `mid-conversation-system-clear-at-2026-08-21`).
Send at most two or three reminders, and never delete earlier copies.

**`stop_reason: "refusal"`.** Check `stop_reason` before reading `content`.
`stop_details.category` is informational, for example `cyber`, `bio` (new
relative to Opus 5) or `reasoning_extraction` (also new). Opt into refusal
fallbacks. Server-side fallback returns `reasoning_extraction` declines instead
of retrying them, so fix the prompt as described above. A fallback model runs
without Opus 5.5's thinking blocks. Finding vulnerabilities in source code is
allowed. For life-sciences work that the biology classifier blocks, apply to the
Life Sciences Verification Program.

**Situational fixes.** Each of these has a snippet in the reference below.
- *Multi-app agent misses context the task did not name:* add the
  "explore broadly first" line. Keep untrusted content out of the searched
  records, because the line tells the model to act on what it finds.
- *Multi-agent team is slow:* append `elapsed 340s / 1200s` (elapsed time
  against the budget, in seconds) to each message the harness sends. Set the
  budget above your target. It is advisory, so keep a hard timeout. Without a
  budget, show elapsed time alone and add the "time matters" line.
- *Chat replies start slowly:* remove "think carefully before answering" lines.
  Effort is the control. Add "treat earlier answers as settled" only where the
  model should not revisit its earlier work. It can also stop the model from
  pointing out its own earlier mistakes.
- *The model obeys instructions inside pasted text:* wrap each pasted block in
  `<pasted_content id="…">` tags. Each tag goes on its own line, and a random ID
  repeats on the closing tag. Add the system note. The tags can be imitated, so
  keep other injection defences.
- *Dense charts, diagrams or screenshots are misread:* first re-test whether the
  scaffolding you built for older models is still needed. For the densest
  inputs, use higher-resolution images and a crop tool, or a container with
  PIL or OpenCV. The model uses those tools better at higher effort.
- *Frontend output looks generic:* "avoid a generic AI look" only swaps one
  default for another. Name the specific patterns to avoid, then extend the list
  after each iteration.

Verbatim snippets, with placement rules and caveats:
[references/system-prompt-snippets.rst](references/system-prompt-snippets.rst).
