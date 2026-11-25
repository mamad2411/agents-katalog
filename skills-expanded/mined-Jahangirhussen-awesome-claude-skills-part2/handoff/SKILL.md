---
name: handoff
description: Compact the current conversation into a handoff document so a fresh agent can continue. Use when the user wants to end a session and resume elsewhere. Not for launching a background agent directly (use claude-handoff).
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---
Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

## Purpose
Produce a concise, secret-free handoff document for the next agent.

## When to use
The user asks for a handoff, to continue in a new session, or to pass the work on.

## When NOT to use
- The user wants a background agent started immediately -> claude-handoff.
- Work is finished and needs no continuation.

## Inputs
The conversation, referenced artifacts (specs, plans, ADRs, issues, commits), and optional user text describing the next session.

## Core workflow
1. Summarise state: goal, done, remaining, decisions, blockers.
2. Reference existing artifacts by path/URL instead of copying them.
3. Add a "suggested skills" section naming skills the next agent should call.
4. Tailor to the user's argument about the next session.
5. Save the document to the OS temp directory, not the workspace.

## Edge cases and failure handling
- Sensitive values appear in context -> redact keys, passwords, personal data.
- No clear next step -> state open questions explicitly.

## Validation
- No secrets in the file; every referenced path/URL exists; a new agent could start from it without the chat.

## Output requirements
Path of the handoff file and a one-paragraph summary.

## Example
```text
Handoff: Goal, Done (3 tickets), Remaining (ticket 4), Decisions (ADR-007), Suggested skills: tdd, code-review.
```

## Related skills
claude-handoff, ce-handoff
