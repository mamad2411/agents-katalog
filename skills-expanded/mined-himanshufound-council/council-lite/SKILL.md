---
name: council-lite
description: >
  Run one request through several approaches or skills one at a time, keeping
  each pass as independent as possible, then merge the answers or pick the best
  one. The claude.ai-compatible version of Council. Use when the user says
  things like "try this a few different ways and compare", "run this through
  several of my skills", "which approach answers this best", or "give me a few
  takes on this and combine them". Do NOT trigger on vague requests; when
  inferring intent from natural language, confirm first before running the
  whole flow.
---

# Council Lite — Multi-Approach Orchestrator (claude.ai)

Run one request through several skills or approaches, then aggregate: one
merged answer, or the single best. This is the claude.ai version of Council.

**How it differs from the full Claude Code skill — say this plainly if it
matters to the user:** claude.ai runs everything in a single conversation with
no subagents, no shell, and no way to auto-discover your other installed
skills. So Council Lite cannot give each skill a truly separate, walled-off
run. Instead it does the best a single context allows: each pass is produced as
independently as possible, deliberately not leaning on the earlier passes. If
the user needs real isolation (each skill blind to the others), point them to
the full Council skill in Claude Code. Do not overstate the isolation here.

## When to run

- The user invokes `/council` / `/council-lite`, or
- asks in plain language to compare approaches / run several skills / get
  multiple takes and combine them. In the natural-language case, confirm once
  ("Want me to run this through a few approaches and combine them?") before
  starting — don't silently produce six drafts.

If the request itself isn't stated yet, ask for it before running.

## Step 1 — Choose what to run it through

There is no filesystem discovery here, so ask the user directly. Offer two
ways, as a short conversational prompt (no special picker UI exists — use a
plain numbered list and let them reply in text):

- **Named skills** — if the user has other skills uploaded to claude.ai, they
  name the ones to include (e.g. "run it through my minimalist-ui and
  web-design-guidelines skills"). For each named skill, apply that skill's own
  instructions during its pass.
- **Ad-hoc lenses** — if they don't have matching skills, have them name
  distinct approaches/personas/lenses instead (e.g. "a security reviewer, a
  performance reviewer, and a plain-English explainer"). Each becomes one pass.

Confirm the resolved list in one line before running. There is no persistent
skillset store in this version — selections are per-conversation. If the user
wants saved, reusable skillsets, that's a full-Council (Claude Code) feature;
say so rather than pretending to save one.

## Step 2 — Choose the mode

Ask, in plain text:

1. **Combined** — merge the distinct strengths of every pass into one coherent
   answer.
2. **Best** — silently judge which single pass is strongest and present it.

## Step 3 — Run the passes sequentially

For each chosen skill/lens, in turn:

1. Announce nothing to the user mid-run — do the passes internally.
2. Produce a complete answer to the user's original request using **only** that
   skill's instructions (or that lens's perspective). Treat each pass as a
   fresh attempt: do not summarize, critique, or build on the previous passes —
   the point is to get genuinely different takes, not a conversation that
   converges after the first answer.
3. Keep each pass's full text; you'll need it for aggregation and for the
   reveal-on-request behavior.

If a named skill can't be applied (not actually available, or the user named
something you have no instructions for), don't abort — skip it, keep the rest,
and note the omission in the final answer.

## Step 4 — Aggregate (you do this, with all passes in view)

- **Combined**: merge the distinct, non-redundant strengths of the passes into
  ONE coherent answer — a real synthesis, not "approach A said… approach B
  said…".
- **Best**: pick the strongest pass for this request and present it directly
  and completely. Don't narrate the judging.

## Step 5 — Output

- Show only the final aggregated answer.
- If any pass was skipped, add one short line, e.g. *"Note: I couldn't apply
  the `xlsx` skill, so it isn't reflected above."*
- Do not dump the individual passes by default.

## Reveal on request

If the user then asks "show me each one" / "what did each approach say",
present the individual passes, each labeled, from what's already in context.
Don't re-run them.
