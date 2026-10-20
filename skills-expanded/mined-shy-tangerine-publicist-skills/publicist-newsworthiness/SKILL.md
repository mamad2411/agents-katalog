---
name: publicist-newsworthiness
description: Score a news event, announcement, or source pitch before pitch work starts. Use to decide whether a story merits outreach or whether the user has enough standing to respond to a current event.
license: MIT
metadata:
  version: "0.1.0"
  author: "shy-tangerine"
---

# Publicist newsworthiness gate

Most things are not news, and most company updates are not worth pitching. This gate exists to stop inflation before it turns into spam. An honest low score protects the user's relationships with journalists; a flattering high score burns them. Run it before angle development, before a newsjacking handoff from publicist-monitor, and whenever a draft brief assumes its own importance.

## Modes

Pick exactly one unless the user asks for both:

- **Event.** Is this public news event worth riding for a user with standing?
- **Announcement.** Is the user's own announcement, angle, or source pitch genuinely newsworthy to journalists?

If an event plus a planned angle arrives together, judge the event first. Only judge the angle if the event clears.

## Hard stops

Return `KILL` immediately, with the reason, when the premise involves:

- riding a tragedy, disaster, death, or someone else's crisis for visibility
- a claimed connection to the story that does not exist
- proof, data, customers, or market position the user does not actually have
- generic thought leadership with no news peg
- an embargo or off-the-record constraint the pitch would violate

No score rescues a `KILL`. If the user pushes, restate the cost in one sentence and hold.

## Evidence rules

Judge only from dated, attributable evidence: the event's canonical coverage, the user's approved facts and proof assets, and the recent output of the target journalists. Never score from the user's enthusiasm, a press release's adjectives, or your own memory of what "usually" gets coverage. Missing evidence lowers the score; it never gets assumed away.

## Scoring

Score 1-10 with anchors, then assign a verdict:

- **1-3** `NOT_NEWS`: a company milestone, minor feature, award nobody independent conferred, or an event with no stakes beyond the user's own interests.
- **4-5** `WEAK`: a real peg but thin. The scale is small, the story is crowded, the timing is weak, or the standing needs work. Pitch only if a specific journalist's recent coverage makes the fit obvious; otherwise hold.
- **6-7** `NEWSWORTHY`: independent stakes, clear timing, and something the coverage lacks, such as data, a contrarian credential, or a concrete case.
- **8-10** `NEWSWORTHY` and rare: the story is moving now and the user is one of the few credible voices. Act the same day or drop it.

Anti-inflation rules: most honest scores land at 3-6. An 8+ requires naming the specific evidence that carries it. Never round up because the user likes the story.

## Output

- mode, score, verdict (`KILL`, `NOT_NEWS`, `WEAK`, `NEWSWORTHY`)
- the two or three reasons that set the score, each tied to evidence
- what evidence would raise the score, or state that none realistically exists
- for a pass: the suggested next step (which market skill, which standing the pitch leans on)
- for a fail: what the user could do instead that is not pitching this

A score without evidence-tied reasons is incomplete. This gate never drafts, selects journalists, or contacts anyone.
