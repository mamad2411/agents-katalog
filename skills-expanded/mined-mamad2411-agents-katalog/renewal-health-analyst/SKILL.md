---
name: renewal-health-analyst
description: Your per-renewal analyst. Connect a CRM plus a product-analytics tool (and optionally a meeting tool) and turn any "will this renewal happen?" question into a per-deal verdict: renew yes/no, value, and conditions, a champion-stability check, an adoption story for the pitch, a commercial-lever inventory, and save-play prerequisites. Built for per-renewal depth, not portfolio rollups. Trigger on "will {account} renew?", "renewal verdict on {account}", "is {customer}'s renewal real?", "prep for {account} renewal", "what should I offer {account}?", "save play for {account}", "commercial levers on {customer}", "champion check on {account}", or any single-renewal question.
---

# Renewal-Health Analyst

## What this does
This skill reads one customer and returns a renewal verdict you can act on. It combines product adoption, champion stability, support sentiment, and any competitive signals into a single per-deal call: will this renew, at what value, and under what conditions. It then hands you the pitch material: the adoption story, the commercial levers you can pull, and the checklist of things that must happen before the renewal call. It is built for depth on one renewal at a time, not portfolio rollups.

## What you'll need
You do not need to connect anything to start. Bring your renewals and the skill runs today. Connect the tools below and it pulls the data automatically and adds usage signals you cannot paste by hand.

- Works today with: your upcoming renewals (account, renewal date, value, contract terms, the champion and key contacts), plus whatever usage notes you have. Paste or upload.
- More powerful connected to a CRM: accounts, renewal dates and value, contacts, and the renewal opportunity, live.
- More powerful connected to a product-analytics tool: which features the customer actually uses and how often, the signal that predicts a renewal best and is hardest to paste by hand.
- Sharper with a meeting tool (champion-conversation depth) and a support tool (support-sentiment pulse).

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a number it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste or upload what you have (a CSV or an export). The skill runs the full analysis today on your real numbers. No connection required.
- **Connect your tools**: the same skill pulls the data automatically and adds signals you cannot paste by hand (live activity, product usage, history). Same output, less effort, sharper.
- **Just exploring**: no data yet? Get the framework, the exact fields it reads, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a field to add or a tool to connect.
## Customize this for yourself
| Set this | What it is | Default / Example |
| --- | --- | --- |
| CRM | The system of record for the account and the renewal | A CRM with account, contact, opportunity objects |
| Renewal date field | The field holding the renewal close or period-end date | A "renewal end date" field |
| Renewal value field | The current ARR up for renewal | An "open renewal ARR" field |
| Product-usage signal | The adoption read per feature or capability | A per-feature usage tier from your analytics tool |
| Champion field | The contact marked as the primary relationship owner | A "primary champion" field |
| Renew threshold | Confidence floor above which you call it a likely renewal | 70% |
| Champion-stale threshold | Days of champion silence that downgrade the verdict | 90 days |
| Engagement-floor threshold | Active weeks below which the relationship reads thin | Customer median |

Your product-usage signal is the part most worth mapping carefully. Decide how your analytics tool expresses adoption per feature, and name the features the way your customers would recognize them.

## The method
- Per-renewal verdict. Combine product adoption, champion stability, support sentiment, and competitive intel into a verdict and a confidence number: renew yes/no, a predicted value (flat, upsell, downgrade), and the conditions attached.
- Champion-stability check. Confirm the named champion is still active: record valid, title still a buyer, recent engagement. Flag single-thread risk when the only real relationship runs through one person.
- Adoption story for the pitch. Group product usage by depth: deeply used, established, emerging, untouched. State it in features the customer recognizes. The untouched group becomes the expansion narrative.
- Commercial-lever inventory. Term length, discount headroom, expansion add-ons, multi-year incentives, prepay. Attach a number to each and mark the strongest.
- Save-play prerequisites. A sequenced checklist of what must happen before the renewal call, with branch logic for responds, ghosts, and rejects.

## Quality gates
- No renewal verdict without a champion check. If the champion left or has not engaged within the stale threshold, the verdict downgrades automatically.
- The adoption story is named-capability, not "good usage."
- Save plays are sequenced (Day 0 / Day 7 / Day 14) with branch logic for responds, ghosts, rejects.

## Output (example)
```
EXAMPLE CO RENEWAL  ·  Closes 2026-08-15

VERDICT: RENEW + EXPANSION POSSIBLE  ·  Confidence 78%

Champion stability:
  - Champion still at the company (profile verified this month)
  - Engaged 6 of the last 12 weeks (above customer median)
  - Second-thread contact left in March, single-thread risk

Adoption story (for the pitch):
  Deeply used: Sequencing, Smart Send
  Established: Templates, Meeting Recording
  Emerging:    AI Compose
  Untouched:   Calendar features, Auto Follow-ups
  Story: "Core outreach is fully adopted. Calendar is your next step."

Commercial levers:
  - Multi-year at flat rate (strongest)
  - Add calendar bundle (expansion)

Save-play prerequisites:
  [ ] Re-thread to a second champion
  [ ] Run a calendar-feature demo
  [ ] Pre-position the multi-year offer 30 days out
```

## Where the numbers come from
The thresholds are defaults, not laws. The renew threshold (70%) is the confidence floor for calling a renewal likely. The champion-stale threshold (90 days) is the silence window that downgrades a verdict. The engagement floor defaults to your own customer median, so it self-calibrates once you have enough accounts. Re-tune all three after you watch a few renewals land against the verdicts the skill gave you.

## Example chat

**You:** Will Example Co renew? Closes August 15th. Here's what I know about their usage and the champion situation.

**Claude:** Read it. Renew, with a real expansion angle, but there's a single-thread risk you should close first.
```
EXAMPLE CO RENEWAL  ·  Closes 2026-08-15
VERDICT: RENEW + EXPANSION POSSIBLE  ·  Confidence 78%

Champion stability:
  - Champion still at the company, engaged 6 of last 12 weeks
  - Second-thread contact left in March, single-thread risk

Adoption story (for the pitch):
  Deeply used: Sequencing, Smart Send
  Untouched:   Calendar features, Auto Follow-ups
```
The gate that mattered here: I don't hand back a renewal verdict without checking the champion first. If they'd gone quiet past 90 days I'd have downgraded the confidence automatically instead of letting the usage numbers carry the call.

**You:** What's the save-play checklist look like given the single-thread risk?

**Claude:** Re-thread to a second champion first, then run the calendar demo, then pre-position the multi-year offer 30 days out, in that order. Sharpener: connect your product-analytics tool and I'll pull the real weekly usage instead of working off the notes you pasted, so the adoption story is exact.

## Go further
The single-account read proves the model works. Here is the version that runs it on every renewal.

- **Run this the day a renewal enters the window.** Schedule a Claude task off your CRM's renewal-date field so every account gets a verdict 90 days out automatically, not when a CSM remembers to ask.
- **Watch champion silence live.** Connect Gong or your email tool so a champion going quiet past 90 days downgrades the verdict the moment it happens.
- **Push the save-play checklist to the CSM's task list.** Wire the sequenced prerequisites into Salesforce tasks so "re-thread to a second champion" shows up as an assigned to-do, not a line in a doc.

The verdict stops being a snapshot and starts updating itself as the signals move.

## Make it yours
Map the roles to your stack, set your thresholds, and name your features the way your customers do. Built by an operator. Customize it, break it, make it better.
