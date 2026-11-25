---
name: claude-desktop-babysitting
description: Use when supervising Claude Desktop/Claude Code/Fable sessions through Hermes Computer Use for long-running local work. Covers logs-first monitoring, GUI verification, continuation prompts, context lifecycle management, blocked-state handling, and end-of-window reporting.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [claude-code, computer-use, supervision, local-workflows, agent-ops, handoffs]
    related_skills: [agent-session-progress]
---

# Claude Desktop Babysitting

## Overview

Use Hermes as a supervisor for Claude Desktop / Claude Code / Fable-style sessions. Hermes reads session logs first, uses Computer Use only for action/verification, and keeps local/reversible agent lanes moving without giving those lanes ownership of public release credentials.

## When to Use

Use this when:

- a Claude Desktop or Claude Code session is doing long local work;
- multiple agent lanes need monitoring;
- you want Hermes to restart idle sessions with direct continuation prompts;
- you need context-window lifecycle management and handoffs;
- you want an end-of-window report with git/tests verification.

Do not use this for:

- typing secrets, passwords, 2FA, API keys, or payment details;
- clicking permission dialogs without explicit approval;
- public posting, pushing, purchasing, or sending messages from a worker lane;
- one-shot CLI tasks that Hermes can do directly.

## Key Principle

The orange Claude logo is not proof that work is running.

Reliable running signals:

- latest prompt appears as a posted user bubble;
- sidebar/title says `Running`;
- stop-square or spinner is visible;
- elapsed runtime/tokens are visible;
- assistant/tool activity is actively expanding;
- transcript has fresh assistant/tool activity.

Idle/not-submitted signals:

- prompt text remains in the input box;
- normal submit arrow is visible instead of stop-square;
- sidebar says Ready/Awaiting input/Idle;
- latest assistant message is a final summary;
- no transcript activity after a fresh user prompt.

## Workflow

1. Run read-only session-log discovery.
2. Map target sessions by exact title/cwd/session id.
3. Classify each lane from logs.
4. Use Computer Use only for lanes that are idle/unknown/blocked or need action.
5. If idle and safe, submit a direct continuation prompt.
6. Verify the prompt posted and the session became running.
7. If the Desktop UI accepts a prompt but no assistant/tool activity starts, use same-session CLI resume as a fallback only when safe.
8. Periodically verify changed repos with git status and tests.
9. Produce a compact report.

## Continuation Prompt Shape

```text
Continue from the current state; do not use /loop. Use existing context and do a quick continuation scan of git status, current diff, recent tests, and relevant docs.

Act as a high-agency local build partner. Finish the current milestone. If it is complete and context is healthy, choose the next highest-leverage adjacent local/reversible improvement and build it. Run focused tests. Avoid secrets, public/external actions, and permission dialogs; create local stubs/runbooks instead.

Final response should lead with what now works, files changed, tests/reports run, rollback/demo path, blockers, and next highest-leverage step.
```

## Context Lifecycle

For Fable-style 1M-context sessions, use approximate context percentage as a heuristic, not a hard truth:

- <50%: continuing same session is usually fine;
- 50-70%: finish the current unit and prepare a handoff;
- >70%: closeout/handoff only; do new implementation in a fresh session;
- >85%: emergency closeout only.

Closeout is a transition, not a loop. Once a lane has produced a handoff, start a fresh lane or pause.

## Common Pitfalls

1. Mistaking text in the input box for a submitted prompt.
2. Treating the orange logo/spinner as proof of work.
3. Over-trusting a log classifier when latest text is a final summary.
4. Prompting old history sessions instead of the current exact target lane.
5. Reusing stale Computer Use element indices after sidebar rows reorder.
6. Repeatedly pressing Return on a stale Desktop prompt overlay instead of falling back safely.
7. Publishing raw transcripts or private repo details.
8. Letting worker lanes push publicly under the wrong account.

## Verification Checklist

- [ ] Correct target session selected by exact title/cwd/session id.
- [ ] Prompt posted as a user bubble.
- [ ] Running indicator visible or fresh assistant/tool activity appears in logs.
- [ ] No permission/secret/public-action dialog was clicked.
- [ ] Git status and relevant tests checked independently when reporting results.
- [ ] Context lifecycle decision recorded when a session approaches handoff range.
