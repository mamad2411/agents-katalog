---
name: lead-research-dossier
description: Build a structured one-page prospect dossier (company facts, ICP fit, buying signals, contacts, personalization hooks) from live web research. Use when the user asks to "research this lead", "build a dossier", "who is this company", "prep me for this sales call", "qualify this prospect", or names a company they want to sell to. Don't use for writing the outreach itself — hand the finished dossier to cold-outreach-sequencer.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Business Ops, Sales, Research, Prospecting]
    related_skills: [cold-outreach-sequencer, pipeline-tracker, competitor-pricing-scan]
    requires_toolsets: [web]
---

# Lead Research Dossier

Produces a one-page, evidence-backed prospect dossier an SDR could act on in five minutes. Every claim carries a source URL; anything unverifiable is marked "unconfirmed" rather than guessed. The dossier feeds directly into `cold-outreach-sequencer`.

## When to Use

- User names a company (or a person + company) they want to sell to, partner with, or pitch.
- User asks for call prep, account research, or "is this company a fit for us?"
- User has a list of leads and wants dossiers one at a time.
- **Not for:** writing the outreach itself — hand the finished dossier to `cold-outreach-sequencer`. Not for competitor analysis — use `competitor-pricing-scan`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Company site sweep | `web_extract` on homepage, /about, /pricing, /careers, /blog |
| Recent signals | web search: `"<company>" (funding OR hiring OR launch OR partnership) 2026` |
| Team + contacts | web search: `"<company>" (founder OR "head of" OR VP) site:linkedin.com` |
| Tech/scale hints | careers page job posts (stack, team size), press releases |
| ICP fit scoring | Compare findings against the user's ICP criteria (ask if not given) |

## Procedure

1. **Precheck** — confirm web tools are available and you have: company name or domain, and the user's ICP criteria (target size, industry, problem you solve, who buys). If ICP criteria are missing, ask for them or pull from prior context — fit scoring is meaningless without them.
2. **Firmographics** — extract homepage + about page: what they do, for whom, HQ, rough headcount, business model. Success: you can state their one-liner in your own words with a source URL.
3. **Signals sweep** — search for events in the last ~12 months: funding, leadership changes, product launches, hiring spikes, expansion. Each signal gets a date and URL. Old news labeled as old.
4. **Contacts** — identify 1–3 likely buyer-persona people (name, role, public profile URL). Public professional info only — no personal emails, no scraped private data. If no contact is findable, say so; never invent names.
5. **Hooks** — from their blog, job posts, founder posts, or product pages, pull 2–3 specific, recent, non-generic personalization hooks ("they just opened a Singapore office", not "I love your website").
6. **Score fit** — rate ICP fit High / Medium / Low against each of the user's criteria, one line of evidence per criterion.
7. **Deliver** — fill the template completely. Mark any empty section "none found" — a visible gap beats silent omission.

## Output Template

```
# Dossier: <Company> — <date>
**One-liner:** what they do, for whom. [source]
**Firmographics:** HQ | ~headcount | model (B2B SaaS / services / ...) | est. stage/revenue (unconfirmed if inferred)

## ICP Fit: High / Medium / Low
| Criterion | Verdict | Evidence |
|---|---|---|

## Signals (last 12 months)
- <date> — <signal> [source]

## Contacts
- <Name> — <Role> — <public profile URL>

## Personalization Hooks
1. <specific, recent, sourced>
2. ...

## Open Questions / Risks
- <what we couldn't verify>
```

## Pitfalls

- **Confidently wrong facts (stale or hallucinated)** — headcount, funding, and even the product change fast. Recovery: only state what a fetched page actually says, attach the URL, and date every signal. If two sources disagree, show both.
- **Wrong company (name collision)** — "Mercury" the bank vs. Mercury Marine. Recovery: lock onto the exact domain early; verify industry + HQ match the user's intent before deep research.
- **Generic hooks** — "congrats on your growth" gets deleted on sight. Recovery: a hook must pass the test "could this sentence apply to any other company?" If yes, dig into their blog/job posts until you find one that couldn't.
- **Empty contacts section treated as blocker** — some companies expose no people publicly. Recovery: deliver the dossier anyway with contacts marked "none found publicly" and suggest the role title to target instead.

## Verification

- [ ] Every factual claim has a source URL; inferences are labeled "unconfirmed"
- [ ] All signals dated and from the last 12 months (or flagged as older)
- [ ] Hooks are specific enough that they couldn't apply to another company
- [ ] ICP fit scored against the user's actual criteria, not generic ones
- [ ] No private/personal contact data included — public professional info only
- [ ] Output matches the template with no silently omitted sections
