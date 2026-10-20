---
name: insight-to-deck-flow
description: Turn marketing results into on-brand presentations and feed them back into the next cycle, in five steps - (1) content marketing and (2) growth marketing produce winning insights, (3) Claude turns those insights into polished decks from your own templates via a presentation MCP, (4) personalised decks are generated at scale from templates and CRM/campaign variables, (5) results feed back into audience research, winning messages, customer insights and performance data. Uses the presentation connectors actually available (Gamma, Canva, Adobe Express, or local pptx) since the source's Pitch MCP is not connected here. Use when asked to turn campaign results or customer-call notes into a deck, build personalised sales/client decks at scale, or close the loop between marketing learning and sales material.
---

# Insight-to-Deck Flow

Source: uploaded infographic "5 Steps with Pitch MCP and API: Modern
Marketing Flow" (Madhav Mistry). It is a Pitch (pitch.com) promotion; the
flow is tool-agnostic. **[Certain]** Pitch MCP is not connected in this
account; the substitutes below are.

## The five steps

| # | Step | Source content | How here |
|---|---|---|---|
| 1 | Content marketing | Build trust and demand with useful content: audience problems, expert content, channel distribution, audience engagement, content insights | `content-strategy`, `claude-marketing-jobs` (Content) |
| 2 | Growth marketing | Find what works through testing: message testing, offer testing, campaign experiments, conversion tracking, growth insights | `claude-marketing-jobs` (Paid, Analytics), `marketing-adaptability-score` |
| — | **Winning insights** | Where steps 1 and 2 meet | One insights file per cycle (template below) |
| 3 | Insights → decks (MCP) | Bring research and campaign context from other tools; add notes from customer calls and performance insights; ask Claude to turn it into a deck from your own templates; share with tracked links | Gamma `generate_from_template` (your Gamma templates), Canva `create-design-from-brand-template`, or `pptx` skill with your .pptx master |
| 4 | Personalised decks at scale (API) | Trigger deck updates when data arrives or sales stages change; fill templates with customer, date and campaign variables; personalised decks per client; keep every deck on-brand | Loop step 3 over a CSV/CRM export (HubSpot `search_crm_objects`); for scheduled triggers use `n8n-agent-builder` |
| 5 | Feed results back | Use performance to improve the next cycle: content → growth → automation → back to content | Update `docs/marketing-context/` (proof rows, last-quarter.md) |

## Winning-insights file (input to step 3)

```
Cycle: [month/quarter]
Audience: [segment]
Insight 1: [what we learned] — evidence: [test / metric / call quote + date] — proof row: [ID]
Insight 2: ...
Winning message: [exact line] — result: [metric vs control]
Customer quotes (verbatim, with permission status): ...
What we stop: ...
Deck purpose: [sales pitch / QBR / board update / client report]  Audience: [who]  Length: [n slides]
```

## Deck prompt (step 3)
```
Build a [n]-slide [deck purpose] for [audience] from the insights file below, using our template [template id/name].
One idea per slide; slide titles are full-sentence takeaways. Every number cites the insight it came from. No claim without a proof row.
Structure: context → what we tested → what won (with numbers) → what it means for [audience] → recommendation → next step.
Insights file: [paste]
```

## Personalisation at scale (step 4) — rules
- Variables allowed: customer name, logo, date, segment, the 1–2 insights relevant to that segment, owner. Never generate customer-specific numbers that are not in the CRM export.
- Test the template on 3 records, check them by eye, then run the batch.
- Track which deck version each account received (CRM note), so step 5 can attribute outcomes.

## Honest limits
- "Decks on autopilot" is only safe for internal or low-stakes decks. Client- and board-facing decks go through `brand-reviewer` and a human.
- Tracked links (step 3) are a Pitch feature; Gamma has viewer analytics (`get_gamma_viewer_analytics`); Canva and pptx have none.
