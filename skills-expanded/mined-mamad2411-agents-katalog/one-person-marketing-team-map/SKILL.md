---
name: one-person-marketing-team-map
description: Map of the ReStructure AI demo "The One-Person Marketing Team" (four AI teammates Bella, Max, Vic and Cody running research, content, ads and reporting for a car dealership, with human take-over and spend approval) to the draft-only agents and approval gate already in this repo. Use when the user asks how to build or run a small AI marketing team, or what the demo shows. Source @restructureai 87-second video (Batch 103). Summarised from video frames; the narration was not available, so role names and flows are read from on-screen text only.
---

# The One-Person Marketing Team (demo summary)

On screen: a diagram of agents and tools, a "Reese" box (a small Mac-mini-style device shown as the local host), and a chat window "Reese - Summit Auto" with four agents who "have control" and a "Take over" button for the human.

| Agent on screen | What the frames show | Closest here |
|---|---|---|
| Bella (research) | Trend scout, competitor watch, hook analyst, question miner, keyword finder, audience profiler, idea bank, content planner; Google Trends and Semrush views; "who are we up against?" | `os-market`, `os-seo`, `os-pain-point`; Semrush and Ahrefs connectors are available here |
| Max (content) | Designs a "Can you trade in a car you still owe on?" post in Canva, fills a content library, schedules to Instagram, TikTok, Facebook, LinkedIn | `content-pipeline` command, `brand-reviewer` agent, `content-designer`, `content-publisher` (publish only after approval) |
| Vic (ads) | Builds campaigns on Meta and Google, "Don't spend more than $1,500 a week" prompt, "Locked at $1,500. Nothing spends until you say yes." with Yes / Not yet buttons | `os-ads` plus `os-approval`, and the `max_spend_per_approval_eur` limit in `limits.json` |
| Cody (reporting) | Morning brief, call log, Stripe payments, lead and revenue tables, "what did we learn?" | `os-business-analyst`, `/os-morning-page` |

## What to copy and what not to
- Copy the control pattern: a spend cap the human sets, a hard stop until the human says yes, a take-over button, and a morning brief. These are the same ideas as this repo's draft-only tier, approval cards and morning page.
- Do not copy autonomy: in the demo the agents connect to Meta, Google, Stripe and a call-tracking tool. Here `os-*` agents have no network or connector access by design; a human sends. Do not promote any agent before you have read 20+ of its drafts.
- The demo is a polished product video for ReStructure's blueprint; it does not show failures, costs or approval latency. Treat it as a design reference, not evidence that it works unattended.
- Related: `ai-entrepreneur-os`, `governed-marketing-team`, `agentic-marketing-levels` (this demo is Level 3 "Orchestrate").
