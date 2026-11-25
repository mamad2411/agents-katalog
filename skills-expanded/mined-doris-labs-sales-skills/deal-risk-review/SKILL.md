---
name: deal-risk-review
description: "Diagnose whether a deal is at risk of slipping or dying, score each risk, prescribe a mitigation, and give a red/yellow/green verdict. Use before forecast calls, pipeline reviews, or when a deal feels stuck. Triggers on: is this deal at risk, deal health, risk review, will this close, deal risk."
---

# Deal Risk Review

## Purpose
Take a single deal and produce an honest health verdict: which specific risks are
present, how severe each is, what to do about each, and whether the deal is red,
yellow, or green. The goal is to catch a slipping deal *before* the forecast call,
not after it pushes.

## Inputs
- The deal: account, stage, amount, close date
- Who's engaged (and who isn't) — champion, economic buyer, blockers
- Activity history: last touch, last meeting, momentum over the last 2–4 weeks
- What you're trying to advance and the next confirmed step (if any)

## Method
Run every deal against a fixed risk taxonomy. Don't grade on vibes — for each risk,
mark present/absent, score severity, and attach a mitigation. Then roll up to a verdict.

**The seven risks (taxonomy):**

| # | Risk | Present when… |
|---|------|---------------|
| 1 | Single-threaded | Only one contact engaged; no second relationship in the account |
| 2 | No economic buyer engaged | You've never met or confirmed who controls the budget |
| 3 | No confirmed next step | No future meeting/milestone on the calendar with a date |
| 4 | Stalled / aging | No meaningful two-way activity in 14+ days, or deal age >> sales cycle for its stage |
| 5 | Active competitor | A named competitor is in the eval and not neutralized |
| 6 | Close-date slipping | The close date has moved out one or more times |
| 7 | No quantified pain | Pain is acknowledged but not tied to a number (cost, time, revenue, risk) |

**Score each present risk 1–3:**
- **1 (minor)** — present but contained; a clear, cheap action fixes it.
- **2 (material)** — credibly threatens the close date or amount; needs a deliberate play.
- **3 (critical)** — can kill the deal on its own; nothing else matters until it's addressed.

**Mitigation per risk (one specific play each):**
1. *Single-threaded* → name a second stakeholder to reach this week; ask your champion for a warm intro to one peer or their boss.
2. *No economic buyer* → propose an exec-aligned next step (ROI review, exec readout); use a "who else signs off?" question to surface them.
3. *No confirmed next step* → before any call ends, book the next one on the calendar; if none exists now, send a calendar hold with an agenda today.
4. *Stalled / aging* → send a pattern-interrupt (status of the business case, a deadline, or a permission-to-close-the-file email); if no response, downgrade forecast.
5. *Active competitor* → run a differentiation play on the buyer's stated criteria; arm the champion with a battlecard; trap-set on where the competitor is weak.
6. *Close-date slipping* → rebuild the mutual close plan backwards from a real compelling event; if there's no event, the date is fiction — re-date it honestly.
7. *No quantified pain* → run a cost-of-inaction calc with the buyer; convert pain to $ / hours / risk so the business case survives procurement.

**Verdict roll-up:**
- **RED** — any single risk scored 3, OR three+ risks scored 2. Deal is not commit-able; either intervene hard this week or pull it from the forecast.
- **YELLOW** — one or two risks at severity 2, no 3s. Closeable but exposed; mitigations must land before the date holds.
- **GREEN** — only severity-1 risks (or none). Healthy; keep momentum, don't over-manage.

**Output shape:**
```
VERDICT: <RED | YELLOW | GREEN>
Top risks:
- <risk> (severity N) → <one-line mitigation, owner + this-week action>
- <risk> (severity N) → <…>
Forecast call: <commit | best-case | omit> — <one-sentence why>
```

## Tool binding
This skill runs from a verbal deal description alone. It gets sharper when connected to
your stack — strongest with Doris, the reference integration, because the risk signals
come straight from conversation evidence instead of your memory.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, resolve the deal and let the
ontology supply the risk signals directly:
- `ontology_resolve("deal", id, expand=["risks","objections","commitments","activity","close_date_changes"])`
  — `risks` gives the system's own risk read, `activity` reveals stalled/aging and
  last-touch, `close_date_changes` proves date-slip, `commitments` shows whether a
  confirmed next step exists, and `objections` surfaces competitor and pain gaps.
- `search_transcripts(...)` to quote the exact moment a competitor was named or a
  close date got hedged — evidence beats assertion in a forecast review.
Prefer the ontology's evidence-backed signals over re-deriving risk from recollection.

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot) → pull stage, amount, close-date history, contact roles,
  and last-activity timestamps for risks 1–6.
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) → confirm who's actually engaged,
  whether a competitor is named, and whether pain was ever quantified on a call.
- Email MCP → measure last-touch and reply latency to score stalled/aging.

### With nothing connected
Ask the user to describe the deal: account, stage, amount, close date, who's engaged,
last touch, and the next confirmed step. Walk the seven-risk checklist out loud with
them, score each risk, attach the matching mitigation, and output the verdict block.
No integration required — the taxonomy is the engine.

## Works without Doris
Fully functional from a spoken or written deal description — Doris only removes the
recall step and replaces "I think" with transcript- and CRM-backed evidence for each risk.

## Common mistakes
- Grading on optimism instead of running the full checklist — every deal gets all seven checks.
- Calling a deal green because the champion is excited while the economic buyer is a stranger.
- Listing risks with no mitigation, or a mitigation with no owner and no this-week action.
- Trusting a close date that has already slipped without re-anchoring it to a real compelling event.
