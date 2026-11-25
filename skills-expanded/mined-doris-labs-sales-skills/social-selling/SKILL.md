---
name: social-selling
description: "Run LinkedIn outreach that earns the reply — warm a prospect through their profile and posts before you pitch, then send a connection note and first-message sequence built on real context. Use when reaching out cold on LinkedIn or planning a social-selling cadence. Triggers on: LinkedIn outreach, social selling, connection request, comment strategy, LinkedIn message."
---

# Social Selling

## Purpose
Turn a cold LinkedIn profile into a warm conversation: engage with the prospect's
world first, send a connection note they accept, and open with a first message that
references something real — not a templated pitch they've seen a hundred times.

## Inputs
- The prospect (LinkedIn URL, name + company, or profile text)
- Why you're reaching out (the trigger: their post, a role change, a mutual, an account play)
- The account context (existing deal, prior touchpoints, who else you know there)

## Method

### 1. Profile-led engagement — warm before you pitch
Never let the connection request be the first time they've heard your name. Read the
profile for hooks and engage on their terms first:
- **Recent activity** — posts, comments, reposts in the last 2–4 weeks. This is the
  highest-signal hook; it's what they care about *right now*.
- **Role + tenure** — new in role (<6 months) = openness to change; long tenure = owns the status quo.
- **Career path / shared ground** — past companies, schools, regions, mutual connections.
- **About section + featured** — the problems they self-identify with, in their words.

**Warm-before-pitch rule:** earn one to three touchpoints (a thoughtful comment, a
relevant reaction) *before* the connection request. The request then lands as
"the person who said that smart thing," not a stranger.

### 2. Content-comment cadence — engage before reaching out
Run this over 5–10 business days, not all at once:

| Day | Action |
|-----|--------|
| 1   | Follow (not connect). Like 1 recent post. |
| 2–3 | Leave one substantive comment on a recent post — add a point, don't praise. |
| 4–5 | React to a second post; reply if they answer your comment. |
| 6   | Send the connection request with a note (formula below). |
| 8–10| If accepted and quiet, send first message. If ignored, keep commenting; retry the request in 3–4 weeks. |

**Comment quality bar:** a good comment teaches, disagrees respectfully, or adds a
concrete example. "Great post!" is invisible. "We saw the opposite with X — curious if
Y was a factor for you?" gets a profile click.

### 3. Connection-note formula
Keep it under 300 characters. Structure: **context → relevance → low-friction reason →
no ask.**
```
<specific hook about them> + <why you, in one clause> + <soft reason to connect>.
```
Do **not** pitch, book a meeting, or "hop on a call" in the connection note. The only
goal of the note is acceptance.

### 4. Identify warm-intro paths
Before going cold, check for a shorter route — a warm intro beats any cold note:
- **Mutual connections** — sort by who actually knows them (former colleagues > random 1st-degrees).
- **Existing relationships at the account** — a current champion, a past buyer, a stakeholder already in a deal.
- **Internal paths** — your exec, an investor, a customer who'll vouch.
Ask the mutual for a soft intro or permission to name-drop ("Mind if I mention we both
know you?"). Use cold outreach only when no warm path exists.

### 5. Sample connection note + first-message sequence

**Connection note (post-comment):**
```
Hi <name> — enjoyed your take on <topic from their post>, especially <specific point>.
I work with <peer role/company type> on <the problem space>. Would be good to connect.
```

**First message (Day 1 after accept) — no pitch, one open question:**
```
Thanks for connecting, <name>. Your post on <topic> stuck with me — <one-line genuine
reaction>. Out of curiosity, how are you thinking about <related problem> heading into
<quarter/initiative>?
```

**Message 2 (Day 4–5 if engaged) — offer value, still no ask:**
```
That tracks with what I'm hearing from <similar role/company>. We put together
<relevant resource / short teardown> on exactly that — happy to send it over, no strings.
```

**Message 3 (Day 8–10 if warm) — the soft meeting ask:**
```
Given <thing they said>, it might be worth 15 min to compare notes on how <peers> are
handling <problem>. Worst case you get a couple of ideas. Open to a quick chat next week?
```
Then break the thread — keep commenting on their content and re-engage in 3–4 weeks
rather than sending a fourth chase.

## Tool binding
This skill works from a profile URL or pasted profile text alone. It gets sharper when
connected to your stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, pull relationship context so the
outreach reflects real history instead of guessing:
- `ontology_resolve("person", id, expand=["company","deals","meetings"])` — use the
  prospect's company, any deals they're attached to, and prior meeting touchpoints to
  ground the hook in real context (e.g. reference a live deal at their account or a past
  conversation) and to avoid cold-pitching someone you already have a relationship with.
- `ontology_search` to find the person record by name/company before resolving.
This tells you whether this is truly cold or already warm — and surfaces the warm-intro
paths and prior touchpoints that should change the message.

### With a CRM / CI / email MCP
- LinkedIn MCP / Sales Navigator export → source the profile, recent activity, and mutuals.
- CRM MCP (Salesforce/HubSpot) → check existing relationship history, account owner, and
  prior contact so you don't cold-pitch a known contact.

### With nothing connected
Ask the user for the profile URL or paste of the profile (headline, about, recent
posts, mutuals). From that, produce: the warm-intro check, a 5–10 day comment cadence,
a connection note, and the three-message sequence — all populated with the specific
hooks from the profile. The user pastes them into LinkedIn manually.

## Works without Doris
Fully functional from a profile URL or pasted profile text — Doris only removes the
lookup step and tells you whether the prospect is already warm via existing deals and
meetings.

## Common mistakes
- Pitching in the connection note — the note's only job is acceptance.
- Reaching out cold when a warm-intro path existed and went unchecked.
- "Great post!" comments that add nothing and get ignored.
- Sending all messages on a timer regardless of whether they engaged.
- Templated first messages with no reference to anything specific about them.
