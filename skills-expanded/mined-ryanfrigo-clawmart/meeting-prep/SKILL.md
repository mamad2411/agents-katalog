---
name: meeting-prep
description: Before each meeting, a one-pager — who's in the room, why, where the last thread left off, and your goal.
metadata: { "openclaw": { "emoji": "📋" } }
---

# Meeting Prep

Walk into every meeting already briefed. This skill takes an upcoming calendar event and builds a tight one-pager: who the attendees are, the last time you talked to them and where it left off, what you want out of the meeting, and the two or three things to actually say.

## When to use (trigger phrases)

Use this skill when the user says:

- "prep me for my next meeting" / "who am I meeting with at 2?"
- "brief me on the [Acme] call"
- "what do I need to know before this?"
- Or run it automatically ~20 min before each external or important meeting.

## How it works

1. **Resolve the meeting.** Take the named meeting, or default to the next one on the calendar tool (`gcalcli agenda`, `icalBuddy`, Google Calendar). Read title, time, attendees, description, attached docs/links, and the join link/location.
2. **Identify the attendees.** Split internal vs external.
   - **External** — enrich from what's actually available: prior email/message history with them, the email signature/domain, any notes in the CRM or notes tool if connected. State role + company + why they're relevant. If a paid enrichment tool is configured, use it; otherwise work from your own history.
   - **Internal** — pull recent context: what you last worked on together, open threads, anything you owe them.
3. **Find the last interaction.** Search email and messages (`himalaya` / Gmail search, `slack` / `imsg` search) for the most recent thread with these people and summarize where things stand — decisions made, promises outstanding, the open question.
4. **Establish the goal.** Infer the meeting's purpose from title + context (decision, sale, status update, relationship, interview). If it's unclear and the meeting matters, ask the user one line: "What's the win here?"
5. **Assemble the one-pager** (below). Keep it to a screen.
6. **Suggest talking points and watch-outs** — 3-5 points that move toward the goal, plus any sensitivities (a stalled deal, an unhappy customer, an unresolved ask).
7. **Surface prep tasks** — docs to skim, anything to send beforehand — and hand them to `task-capture` if action is needed.
8. **Deliver** ~15-30 min before start (via `cron`) or on demand.

## Output

Example one-pager:

```
📋 4:00 PM — Investor intro: Dana Lee (Sequoia)  ·  Zoom (link)

WHO
  • Dana Lee — Partner, Sequoia. Leads seed/A infra deals. Warm intro via Marcus.
  • You + Dana only (30 min).

YOUR GOAL
  Get to a second meeting with the full partnership. Not raising yet — planting.

CONTEXT (last touch)
  Marcus introduced you by email 6 days ago; Dana replied "loved the demo, let's
  talk." No prior direct thread. She's invested in 2 adjacent infra tools.

TALKING POINTS
  1. The wedge: why self-hosted assistants beat SaaS for your ICP (your strongest story).
  2. Traction shape — real numbers only; don't over-claim.
  3. Ask her what she's seeing in the space (she'll respect the curiosity).

WATCH-OUTS
  • Don't commit to a raise timeline you can't hit.
  • She'll probe retention — have the honest churn answer ready.

PREP (15 min)
  • Skim your metrics one-pager.
  • Send Dana the deck beforehand? [capture as task]
```

## Notes

- **Requires calendar + search access.** Quality of the "who" and "last touch" sections depends entirely on the history your email/message tools can search. Thin history → thinner brief.
- **Never fabricates facts about people.** If it can't find prior context or can't confirm who someone is, it says "no prior context found" rather than inventing a bio, a company, or a shared history.
- **No paid data enrichment unless you configured it.** By default it works from your own inbox and messages, not third-party people-lookup services.
- **Schedule it** with OpenClaw `cron` to fire before external/important meetings; running it on *every* internal standup is usually noise — gate on `externalOnly` or a `prepThresholdMinutes` if you like.
- **Privacy.** One-pagers can contain sensitive deal and personnel info; deliver only to the user's private channel.
