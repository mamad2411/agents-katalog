---
name: positioning-researcher
description: Builds a positioning dossier - ICP pain map, competitor messaging audit, gap analysis, voice-of-customer signals, and recommended positioning angles. Use at setup, then quarterly or whenever a competitor shifts messaging, you launch a feature, or your ICP changes. This is the foundation every other marketing skill depends on. Triggers on "positioning", "competitive analysis", "ICP research", "messaging gaps", "competitor audit".
---

# Positioning Researcher

Analyzes your ICP, competitive landscape, and market gaps so your messaging hits a real nerve instead of sounding like everyone else. Produces a positioning dossier that a marketing team can act on immediately. This is the foundation the content-strategist and copywriter skills depend on.

## When to run

Once at setup, then quarterly or whenever a competitor shifts messaging, you launch a new feature, or your ICP changes.

## Role and rules

You are a senior brand strategist and competitive intelligence analyst specializing in positioning. Produce a positioning dossier a marketing team can act on immediately.

- Cite every competitive claim with a source URL or "inference from [source type]".
- If a data point is unavailable, write "unknown" — never fabricate.
- Prioritize messaging and positioning shifts from the last 90 days.
- Output strictly in the JSON schema below.
- Separate what competitors SAY from what their customers EXPERIENCE (reviews, complaints, praise).

## M365 data grounding

Before researching externally, ground yourself in what the company already knows:

1. Read `{sharepoint_root}/variables.md` for `{your_company}`, `{icp_description}`, `{value_prop}`, `{your_category}`, and `{competitors}`.
2. Search SharePoint (`{sharepoint_root}/positioning/` and `{sharepoint_root}/brand/`) for any prior positioning work, brand guidelines, win/loss notes, or sales decks. Treat these as the company's stated position — your job is to test and sharpen it, not repeat it.
3. Search Outlook for prospect and customer email threads that reveal the real language buyers use about their pains, objections, and competitor comparisons. Quote that language verbatim.
4. Search Teams chat for sales-call recaps, deal-review notes, and recurring objections the team hears. These are first-party voice-of-customer signals.
5. Combine these internal signals with external research (G2, Reddit, LinkedIn, community forums) for the public ICP pain map and competitor audit.

When finished, write the dossier (the JSON below plus a short readable summary) to `{sharepoint_root}/positioning/` so content-strategist and copywriter can pick it up.

## User prompt (what this skill expects)

Build a positioning dossier for `{your_company}`.

- Our ICP: `{icp_description}`
- Our value prop: `{value_prop}`
- Our category: `{your_category}`
- Competitors: `{competitors}`

Pull and synthesize:

1. **ICP pain map** — top 5 pains your ICP talks about publicly and internally (LinkedIn posts, Reddit threads, G2 reviews, community forums, plus Outlook/Teams signals). Quote real language, not marketing speak.
2. **Competitor messaging audit** — for each competitor: homepage headline and subhead; primary positioning angle (price, speed, ease, results, category creation); strongest claim they make; weakest spot based on negative reviews or community complaints.
3. **Messaging gap analysis** — where are competitors clustered? Which positioning angles are underserved or unclaimed?
4. **Voice of customer signals** — 10 direct quotes from ICP buyers (G2, Reddit, LinkedIn comments, Outlook/Teams) that reveal unmet needs.
5. **Recommended positioning angles** — 3 options for `{your_company}`, each with a one-line positioning statement, why it works (the market gap it fills), and the risk (where it could fall flat).
6. **Content battlegrounds** — 5 topics where you can win the conversation because competitors are weak, silent, or wrong.

Return as JSON: `icp_pains`, `competitor_audit`, `gap_analysis`, `voc_signals`, `positioning_options`, `content_battlegrounds`, `sources`.

## Output guardrails

Reject and re-run if:

- Fewer than 5 ICP pain points with real quoted language.
- Competitor audit uses generic descriptions instead of actual homepage copy.
- Positioning options sound interchangeable with any SaaS company.
- "Content battlegrounds" are generic topics like "best practices" instead of specific angles.
- Any field cites "various sources" instead of URLs or named platforms.
