---
name: outreach-planning
description: Plan a cold-outbound campaign from scratch — trigger-based ICP definition (not static firmographics), persona cards per buying-committee role, signal→pain map, outcome-framed offer, pre-flight data-connection check, company/people/intent-signal sourcing into a deduplicated CSV list, and full campaign architecture (angles, channel mix, cadence, exit conditions, GTM stress test). Use when starting any new outbound campaign, when reply rates are low and the targeting itself may be the problem, or when asked to define an ICP/persona/offer or build a contact list. Runs before `outreach-execution`.
---

# Outreach Planning

Consolidates: `outreach-strategy`, `outreach-data-connections`, `outreach-list-building`, `outreach-campaign-design`.

Cold outbound fails most often at targeting and planning, not copy — a perfectly written email to the wrong person with no clear campaign structure still gets ignored. This skill runs before `outreach-execution` and its output (ICP + personas + pain map + offer + verified tool inventory + contact list + campaign architecture) is what that skill consumes.

## 1. Trigger-based ICP, not static firmographics

"B2B SaaS, 50-500 employees" is a filter, not an ICP — it describes millions of companies with wildly different buying urgency. A trigger-based ICP instead names the **events** that predict someone is about to have the problem the product solves: a funding round, a leadership hire in a relevant function, a tech-stack change (new tool adopted, old one deprecated), rapid headcount growth in a specific team, a public complaint or review mentioning the problem. Firmographics narrow the *pool*; triggers tell you **when** someone in that pool is actually in-market. List-building (step 4) filters on both.

## 2. Persona cards, per role in the buying committee

One persona per distinct role that touches the decision — economic buyer, technical evaluator, day-to-day user, and often a blocker (security/procurement/IT). Each card: what they're measured on, what a bad outcome looks like for them personally, where they get information, and what objection is unique to their seat.

## 3. Signal → pain map

For each trigger, state the specific pain it implies — not the product's feature list. "Just raised a Series B" doesn't imply "needs software," it implies specific pressures (scaling a process that worked at 10x smaller, proving ROI to a new board). The map should be falsifiable: if the signal doesn't reliably predict that pain, drop it.

## 4. Offer definition: outcomes, not features

Write the offer as "[persona] gets [outcome] instead of [status quo pain]" — not a feature list. The feature list is objection-handling material, not the opening pitch.

## 5. Data-connection pre-flight

Before sourcing, confirm which tools are actually reachable versus need manual setup:

| Tool | Used for | Check method |
|---|---|---|
| Apollo / Clay / lemlist | Company + people sourcing | MCP connector, or manual export |
| Sales Navigator / LinkedIn | People sourcing, LinkedIn sequence | MCP or manual; note automation risk |
| G2 / Product Hunt | Intent/niche signal sourcing | Usually manual/API export |
| n8n | Automation (execution phase) | Self-hosted or cloud + API credentials |
| Tavus / HeyGen | Video outreach (execution phase) | API key + paid account |
| Email sending infra | Send step | Verify deliverability + domain warmup, not just API access |

Use the `mcp-integration-scout` agent to do the live check. Treat intermediate outputs (lists, enrichment data) as worth caching — outbound data sources rate-limit and charge per lookup. Re-verify time-sensitive trigger data (funding, hiring, tech changes) close to send time.

## 6. Company sourcing

Filter on the ICP's firmographics *and* triggers together (Apollo, Clay, lemlist-style enrichment all allow this combination). Pull more candidates than needed; let step 8's qualification bar cut the list down rather than under-filtering and inheriting noise.

## 7. People sourcing

Find the specific people matching each persona card — title-match loosely (titles vary by company size/industry) and verify against the persona's actual responsibility, not just the title string. Sales Navigator / LinkedIn boolean operators (title + seniority + function) are the standard tool. Pull multiple contacts per company across different buying-committee roles — B2B outbound rarely converts on a single touchpoint.

## 8. Intent/niche-signal sourcing

Review sites (G2, Capterra) and launch platforms (Product Hunt) surface **active intent** — a company leaving a competitor review or a persona commenting on a relevant Product Hunt launch is a stronger trigger than firmographic fit alone. Treat as a supplementary trigger layer on top of step 6, not a replacement.

## 9. List assembly: dedup, qualify, format

Dedupe on email domain + name (catches near-duplicates exact-match dedup misses), verify email deliverability where the source doesn't guarantee it, drop contacts that fail a basic ICP/persona sanity check. Output as a clean CSV: company, contact name, title, verified trigger, source. The trigger column is mandatory downstream — `outreach-execution` needs the specific signal to personalize the first touch, not just a company name.

## 10. Campaign angles: 3 per ICP

A single messaging angle run against an entire ICP produces uniform, easily-ignored copy and no learning signal. Generate at least 3 distinct angles per ICP — vary which pain/trigger leads (from step 3's signal→pain map), not just the wording of the same angle. Split the list across angles so results are comparable; treat the angle as the unit of experimentation.

## 11. Campaign architecture

Define before anything sends: channel mix and sequencing (e.g. email touch 1 → LinkedIn connection → email touch 2 → call → breakup email), cadence (days between touches), what triggers a contact's exit (reply, booked meeting, explicit opt-out, or reaching the final breakup message), and which steps are automated via `outreach-execution`'s n8n capability versus manual. A plan that specifies message copy but skips this structure is the most common reason outbound underperforms even with good copy.

## 12. GTM stress test

Deliberately try to break the plan before it ships:
- Does the ICP actually have budget authority, or does this campaign target the wrong seniority for the deal size?
- Does the volume in step 9 actually exist at the stated quality bar, or will hitting list-size targets require diluting the ICP?
- Does the cadence account for the sales cycle length, or does the sequence end before a realistic decision timeline?

This is a critique pass, not a confirmation pass. The value is finding the weak assumption before spend. Report findings even if unflattering — that's the point of running it.

## Output

A single `outreach-brief.md` deliverable: trigger-based ICP, persona cards, signal→pain map, offer statements, data-connection status, list-building spec (or list itself), campaign architecture with angles and channel/cadence/exit structure, and stress-test findings. This is the canonical brief `outreach-execution` consumes.

## Related skills in this repo

- **outreach-execution**: consumes this brief to write copy, execute channels, handle replies, and automate.
- **product-marketing-context**: foundational "who's the customer" doc — pull from it rather than re-deriving personas from scratch if it already exists.
- **competitor-profiling**: if the pain map includes "currently using a competitor," that skill's battle-card output sharpens objection-handling angle.
- **sales-enablement**: MEDDPICC/BANT qualification criteria overlap with the buying-committee persona cards here — reuse rather than duplicate.
- **business-decision-frameworks**: useful for prioritizing which angle/ICP combination to run first when resources don't allow testing everything at once.
- **mcp-integration-scout** (agent): does the live connector check described in step 5.
