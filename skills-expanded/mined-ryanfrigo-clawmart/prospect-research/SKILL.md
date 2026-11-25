---
name: prospect-research
description: Enrich a lead from a domain, company, or name — what they do, who the person is, recent buying signals, and the single best angle to lead with.
metadata: { "openclaw": { "emoji": "🔎" } }
---

# Prospect Research

Turn a bare domain or name into a tight, decision-ready research card: what the company does, who the person is, what changed recently, and the one angle worth opening with. This is the fuel for every other skill in the pack.

## When to use (trigger phrases)

Use this skill when the user says:
- "research <company / domain>"
- "who is <name> at <company>?"
- "enrich this lead: <email / domain / name>"
- "should I reach out to <company>? give me the angle"
- "build a research card for <prospect>"

## How it works

1. **Normalize the input.** Accept a domain, a company name, a person's name + company, or an email (the domain after `@` is usually the company). Resolve to a canonical company domain before searching.
2. **Understand the company (the "what").** Search the company site (home, about, pricing, careers) and the open web. Capture: one-line description of what they actually sell, rough size/stage (headcount band, funded vs bootstrapped), industry, and business model (B2B/B2C, self-serve vs sales-led). Prefer the company's own words over a directory's stale summary.
3. **Find buying signals (the "why now").** These are the reason the timing is good. Hunt for, in rough priority order:
   - Funding rounds or acquisitions (new budget).
   - Relevant new hires or open roles (a new VP of Sales, three SDR reqs → they're scaling the thing you help with).
   - Product launches, market expansion, or a public pivot.
   - Public pain: reviews, support threads, a founder tweet complaining about a problem you solve.
   - Tech-stack changes (a new tool in a job description or their site's footer).
   Record each signal with its **source URL and date**. A signal you can't link to is a rumor, not a signal.
4. **Understand the person (the "who").** If a specific person is named: their role, likely scope, how long they've been there (new-in-seat people buy differently — they're looking to make a mark), and whether they're the economic buyer, a champion, or a blocker. If no person is named, identify the two most likely titles to target.
5. **Infer the likely pain.** Connect the company's stage + signals to a concrete problem they probably have right now. Be specific: not "they need more leads" but "they just hired two AEs with no SDR support, so those AEs are self-sourcing — expensive and slow."
6. **Pick the single best angle.** One trigger + one hypothesized pain + one reason you're credible on it. Everything else is backup. Note a second angle only as a fallback.
7. **Flag confidence.** Mark each claim as **verified** (you have a source), **inferred** (reasonable but unproven), or **unknown**. Downstream skills must not assert inferred claims as fact.

## Output

A compact research card the user (or `cold-open`) can act on immediately. Example:

```
RESEARCH CARD — Acme Analytics (acme.com)

What: Self-serve product analytics for mobile teams. Sales-led on
      enterprise. [verified: acme.com/pricing]
Stage: ~80 employees, Series A ($12M, Mar 2026). [verified: techcrunch link]
Person: Dana Ruiz — VP Sales, started ~2 months ago. New in seat,
        likely rebuilding the motion. [inferred from LinkedIn tenure]

Signals:
  1. Two open AE roles, zero SDR roles. (careers page, seen 2026-06-28)
  2. Series A closed 3 months ago — fresh GTM budget. (TechCrunch, Mar)
  3. Founder tweeted about "pipeline being the bottleneck." (x.com link)

Likely pain: Scaling AEs without top-of-funnel support; new AEs will
             burn ramp time self-sourcing. [inferred]

BEST ANGLE: hiring signal → ramp problem. Lead with the two AE reqs,
            hypothesize the SDR gap, offer to run research + first touch.
Fallback angle: fresh funding → "prove the GTM motion fast."

Confidence: company & funding verified; org gap and pain inferred.
```

Hand off to `cold-open` with "want me to draft the first touch?"

## Notes

- **You configure the search/browse tools.** This skill relies on OpenClaw having web search and page-fetch capability. Quality tracks the tools you give it — a good search backend beats none.
- **Enrichment APIs are optional.** If you've set up Apollo, Clearbit, or similar, the agent can use them for firmographics and verified emails; otherwise it works from public web results. Never scrape LinkedIn directly — it's against their terms; use only what's publicly searchable or a sanctioned API.
- **Do not fabricate.** If a signal, headcount, or funding figure can't be sourced, mark it **unknown** rather than guessing. A fabricated "recent Series B" that never happened is an instant credibility kill on the first email.
- **Freshness matters.** Prefer signals from the last 90 days. A two-year-old funding round is not a "why now."
- **PII hygiene.** Only collect what you'll use for outreach. Store the card via `pipeline-log`, not scattered across chat history.
