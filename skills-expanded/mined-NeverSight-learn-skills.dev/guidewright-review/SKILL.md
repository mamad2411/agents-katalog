---
name: guidewright-review
description: >-
  Review a documentation page or guide for user-experience quality by reading it,
  walking the path it describes in the live product with Chrome DevTools MCP, and
  returning prioritized, specific, expert feedback on how to make it clearer and
  more usable. Use whenever the user wants a docs review, a UX review of a guide,
  a "is this doc any good / how do I improve it" check, wants to find where docs
  drifted from the actual UI, or wants their documentation held to the standard of
  the best technical-writing and docs-UX experts. Trigger even when the user just
  says "review this doc", "critique this guide", "does this how-to make sense",
  "audit our docs", or "the docs feel off" without naming this skill.
---

# Guidewright Review

Audit a documentation page the way a senior docs-UX expert would: read it, **walk
the path it describes in the live product**, and report what works, what breaks a
reader, and exactly how to fix it. The walk is the differentiator. Most doc
reviews only read the text; this one checks the text against reality, so it catches
stale screenshots, renamed buttons, missing steps, and dead ends that a
read-only review never sees.

This is the companion to **guidewright-capture** (the doc *authoring* skill), which creates
annotated walkthroughs, this one holds them to a standard. It works on any
product's documentation — substitute the app and docs you're reviewing wherever
this skill refers to "the product" or "your docs."

## What you produce

A **prioritized review report** (markdown), not a vague impression. Every finding
is specific, points at a location, says why it hurts the reader, and proposes the
fix. Lead with what matters most. End with the rewrite suggestions a writer can
paste in.

## Workflow

1. **Scope it.** Identify the exact page(s) under review (a path in the docs repo,
   a PR, or pasted text). If the user is vague, confirm which page in one question.
2. **Read the doc** and form a model of the reader: who are they, what do they
   already know, what are they trying to accomplish on this page?
3. **Walk the documented path in the live UI** (Chrome DevTools MCP) when the doc
   describes a UI flow. Follow it literally, step by step, as a first-timer would.
   Note every place where:
   - a step's button/label/menu no longer matches the UI,
   - a screenshot is stale or shows a different screen,
   - a step is missing (the doc jumps; the user would get stuck),
   - there's a dead end, an error, or a precondition the doc never mentioned,
   - the doc's path is not the path a real user would actually take (a more
     obvious route exists).
   If the doc is conceptual (no UI flow), skip the walk and review against the
   lenses only.
4. **Score against the lenses** in `references/lenses.md` (Diátaxis type-fit,
   task orientation, findability/standalone-ness, progressive disclosure,
   minimalism, scannability, plain language, accessibility, accuracy). Read that
   file — it is the rubric and the source of the expert standard.
5. **Write the report** using the structure below. Be honest and direct; flattery
   helps no one, but call out what genuinely works so it is preserved.

## Report structure

ALWAYS use this template:

```
# Docs UX Review: <page title>

## Verdict
<2-3 sentences: overall state, who it serves well, the single biggest problem.>

## What works (keep this)
- <specific strengths worth preserving>

## Findings (most important first)
### [Blocker|Major|Minor] <short title>
- **Where:** <heading / step / line / screenshot>
- **Reader impact:** <what happens to the reader because of this>
- **Fix:** <concrete change; include the rewritten text/step when useful>

## Drift from the live UI
<Only if you walked it. Per mismatched step: doc says X, UI now shows Y.>
If you did not walk the UI, say so and why.

## Suggested rewrites
<Paste-ready replacements for the worst passages.>
```

## Severity

- **Blocker** — a reader following the doc gets stuck, lost, or misled (wrong/missing step, dead end, broken precondition). Fix first.
- **Major** — the reader can get through but with friction or confusion (wrong doc type for the job, buried key info, unexplained jargon, stale screenshot).
- **Minor** — polish (wording, scannability, consistency, alt text).

Don't pad the list. A short report of real blockers beats a long one of nitpicks.
Rank by reader impact, not by how easy the fix is.

## Running the live UI safely (read before driving Chrome)

The live walk needs the **Chrome DevTools MCP** (tools named
`mcp__...chrome-devtools__*`). Confirm those are available before walking; if they
aren't, strongly suggest the user enable the `chrome-devtools-mcp` server — or fall
back to a read-only review of the text/screenshots and **say clearly that you
couldn't verify against the live UI** (the live walk is what makes this review
catch drift, so flag what you couldn't check).

The browser profile may also be **shared** with other agents, and a dev stack can
be resource-sensitive:

- **Confirm with the user before starting the app/dev stack and driving the UI.**
- **Reuse the open browser page**; don't kill or relaunch the profile.
- **One driver at a time** — don't fan out agents onto the same shared profile.
- Get login credentials and the environment URL from the user; **never read `.env`
  or other secret files** to obtain them.

## Checklist

1. Scope the page(s); confirm if ambiguous.
2. Read; model the reader and their goal.
3. Walk the documented path live (if it's a UI flow); log every drift and gap.
4. Score against `references/lenses.md`.
5. Write the prioritized report, most-impactful first, with paste-ready rewrites.
