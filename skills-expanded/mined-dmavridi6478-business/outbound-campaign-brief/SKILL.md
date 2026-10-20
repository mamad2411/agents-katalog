---
name: outbound-campaign-brief
description: Turn a one-line, plain-English brief (e.g. "find 50 managing directors of B2B marketing agencies and reach them across email and LinkedIn") into a structured outbound/lead-gen campaign — derived target filters, drafted outreach copy, and an explicit human-approval gate with a send cap before anything actually goes out. Use whenever the user wants to build a B2B outbound/prospecting campaign, describes a target audience in plain language and wants it turned into concrete filters, or wants outreach that stays human-approved rather than fully autonomous. This is the campaign-construction shape specifically — for the general autonomy/approval-boundary discipline behind the send-gate, see night-shift-workflow; for the actual message copy, see copywriting.
---

# Outbound Campaign Brief

Source: a promotional carousel for a commercial SaaS product ("Velox AI," veloxhouse.co.uk) demonstrating a one-line-brief → auto-targeted → drafted → approved-before-send outbound campaign pattern. This skill generalizes the workflow shape as reusable guidance — it is not affiliated with or endorsing that product, and no vendor-specific detail from the ad is treated as fact.

## The pattern: one line is all it takes

Take a brief the way you'd brief a colleague, in plain language — who to target, and across which channels — rather than making the user fill out a structured form up front:

> "Find 50 managing directors of B2B marketing agencies and reach them across email and LinkedIn."

From one sentence like this, derive the concrete campaign parameters explicitly, rather than leaving them implicit:

| Element | Derived from the brief above |
|---|---|
| Target filters | Founders & MDs at B2B marketing agencies |
| Industry | Marketing & advertising |
| Company size | Small-to-mid (infer a reasonable band; confirm with the user rather than guessing a number that matters to the outcome) |
| Seniority | Founder, executive |
| Geography | Ask if not stated — don't default to a region silently |
| Channels | Email and LinkedIn, as named |

State the derived filters back to the user before building a list against them — a one-line brief is fast to give and easy to misread; confirming the derived interpretation costs one message and prevents building a campaign against the wrong audience.

## Building the actual target list: use real data, never fabricate it

Once filters are confirmed, the list itself must come from a real, queryable source — never invented names, companies, or contact counts presented as if real. Check what's actually available in this environment before promising a list:

- **Vibe Prospecting** (`mcp__Vibe_Prospecting__*`) — company/contact lookup, enrichment, and export by firmographic filters (industry, size, role) directly matching this skill's derived-filter shape.
- **OpenFunnel Agent Primitives** (`mcp__OpenFunnel_Agent_Primitives__*`) — company lookup, tech-stack search, and lookalike search for building a target company list from criteria.

If neither is connected, say so explicitly and ask the user how they want to source the list (their own CRM export, a manual list, connecting one of these tools) rather than approximating a list from general knowledge.

## Drafting the outreach

Once the list exists, draft outreach copy per channel:

- Use `copywriting`'s Problem → Promise → Proof → CTA framework for the actual message structure.
- Use `marketing-psychology` to pick one deliberate persuasive lever (social proof, specificity, etc.) rather than writing generic cold outreach.
- Channel-specific adjustments: email allows more length and a clear CTA link; LinkedIn messages should be shorter and read as a real message from a person, not a copy-pasted pitch.
- Run `humanizer` on the draft before it's shown for approval.

## The approval gate: nothing sends until a human says so

Building the list and drafting the messages can happen autonomously. **Sending cannot** — this is the same Claude-may/human-approval-required boundary as `night-shift-workflow`, applied to outbound specifically:

| Claude may do unattended | Requires explicit human approval |
|---|---|
| Derive and confirm target filters from the brief | Actually sending any message |
| Query connected prospecting sources for a candidate list | Committing to a send volume/cadence |
| Draft outreach copy per channel | Approving copy that names specific claims about the recipient's company |

- **State a daily/per-run send cap explicitly** before the first send (the source pattern's "daily cap 10" is a reasonable illustrative default, not a fixed rule — the actual number should come from the user, calibrated to their own deliverability/reputation tolerance).
- **Present the plan for approval, not the fact of having already sent** — list size, message draft, channel, and cap — and wait for an explicit approve before anything goes out.
- If the user says "not now" or doesn't respond, the campaign stays in draft state — don't send partial batches while waiting for approval on the rest.

## Output conventions when using this skill

- Always restate the derived target filters and get confirmation before building a list against them.
- Never present a fabricated lead count, company name, or contact as if it came from a real query — if no real source is connected, say so.
- Present drafted copy and the send plan together for approval — don't ask for approval on the concept and then draft/send without a second checkpoint.

## Related skills in this repo

- **night-shift-workflow**: Supplies the general Claude-may/human-approval-required discipline this skill's send-gate is an instance of — read that skill for the full autonomy-boundary reasoning.
- **copywriting**: Writes the actual outreach message using its Problem→Promise→Proof→CTA framework.
- **marketing-psychology**: Picks the persuasive principle the outreach copy leans on.
- **humanizer**: Run on drafted outreach before it goes to approval.
- **sales-enablement**: Once a reply comes in, that skill's buyer-persona-card and objection-handling material carries the conversation forward from cold outreach into an active deal.
- **product-marketing-context**: The source of truth for who the *real* ICP is — use it to sanity-check a one-line brief's target filters rather than taking the brief at face value if it contradicts documented positioning.
- **the-leverage-stack-auditor**: If outbound campaigns become a recurring, mostly-manual weekly task, check whether it's actually leveraged (a repeatable system) or a labor trap dressed up as automation.

## Notes

Source: an 8-slide promotional carousel for "Velox AI" (veloxhouse.co.uk, @veloxhousetiktok) — a paid, hosted SaaS product. This skill captures the general *workflow shape* it demonstrates (one-line brief → derived targeting → drafted outreach → human approval with a send cap), not the product itself; no feature, pricing, or claim from the ad is treated as verified fact, and nothing here should be read as an endorsement of that specific product.
