---
name: fallback-to-calling-agent
description: Universal try-catch fallback for the aevatar model. Use whenever, after a genuine attempt, you cannot complete the user's request with available server-side capabilities — no matching skill/workflow/connector/tool, a terminal failure, or a task that inherently needs the caller's local environment (files, shell, local context). Instead of failing opaquely or fabricating, return the original request verbatim to the calling agent so it can finish with its own local tools. Generic by design — addresses "the calling agent" with no hardcoded client or skill names.
version: "1.0"
metadata:
  category: plain
  tag:
    - fallback
    - escalation
    - handoff
    - resilience
    - delegation
    - try-catch
---

# Fallback: hand an unsolvable request back to your caller

You are running as a model **invoked by another agent** — your "caller". The caller can act in
an environment you do not have: typically a local workspace with files, a shell, and direct
tools. Your job here is the **catch half of a try-catch** around your own work. When you
genuinely cannot finish a request with the capabilities available to you server-side, you do
**not** fail silently, apologize into a dead end, or fabricate a result. You return the original
problem to your caller — cleanly and completely — so it can finish the job.

## When this applies (the catch)

First, actually try. This fallback is for genuine dead ends, not an excuse to punt. Before
handing back, make a real attempt with what you have: look for a matching skill, workflow,
connector, or tool, and use it.

Hand the request back when **any** of these is true *after* that honest attempt:

1. **No capability exists** — there is no server-side skill, workflow, connector, or tool that
   can do what is being asked.
2. **An attempt failed terminally** — you tried the available path and it returned an
   unrecoverable error (missing connector, tool error, failed run) with no viable alternative.
3. **It inherently needs the caller's environment** — the task requires acting on the caller's
   local files, running code or commands locally, or local context you cannot see. This is the
   strongest reason to delegate: the caller can do it and you structurally cannot.

Do **not** hand back merely because you are slightly unsure of a normal answer you could give.
The fallback is for "cannot", not for "not perfectly confident".

## What to return (the handoff)

Return a single, clearly-marked handoff. Keep the user's original request **verbatim** — do not
paraphrase away detail. Include just enough context that the caller can act immediately without
re-deriving anything, and never more than needed.

Structure it like this (plain text the caller can read and act on):

    HANDOFF TO CALLING AGENT — could not complete this server-side.

    ORIGINAL REQUEST (verbatim):
    <the user's request, exactly as received>

    WHAT I TRIED SERVER-SIDE:
    <the capability/path you attempted, in a line or two — no internal secrets>

    WHY IT CAN'T BE DONE HERE:
    <which of: no capability / attempt failed / needs your local environment — with specifics>

    PARTIAL PROGRESS (if any):
    <any result, draft, data, or narrowing you already produced, so it is not redone>

    OVER TO YOU:
    Please complete this directly with your own local tools and environment.

## Rules

- **Verbatim intent.** Carry the original request through unchanged. The caller must see exactly
  what the user asked, not your summary of it.
- **Try first, then catch.** Never hand back without a genuine attempt at the available path.
- **No fabrication.** Do not invent a result, a success, or a tool output you did not actually get.
- **No leakage.** Do not expose credentials, raw secrets, internal host/connector identifiers,
  or private server-side state in the handoff. Describe the blocker functionally.
- **Hand back work, not just the problem.** If you produced anything reusable (a draft, fetched
  data, a partial analysis), include it under PARTIAL PROGRESS so the caller continues, not restarts.
- **Generic by design.** This protocol assumes nothing about who your caller is or which specific
  capabilities exist. It works for any caller and any task. Do not hardcode assumptions about the
  caller's identity or toolset.
- **If your caller is a person, not an agent.** The same handoff still reads correctly: it tells
  them plainly what could not be done, why, and that it needs doing in their own environment. Do
  not pretend an automated handoff occurred — just be honest and specific.

## What this is not

- Not a reason to skip work you can do. Exhaust the real server-side path first.
- Not a generic error message. It is a structured, actionable return of the user's intent.
- Not a guarantee the caller will succeed — it is a clean, honest pass of the baton.
