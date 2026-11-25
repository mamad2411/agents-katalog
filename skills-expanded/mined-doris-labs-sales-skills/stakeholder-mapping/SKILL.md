---
name: stakeholder-mapping
description: "Map the buying committee on a deal — who holds power, who's on your side, and which roles you haven't reached yet — then build a plan to close the gaps. Use when a deal feels single-threaded, before a big meeting, or when forecasting risk. Triggers on: map stakeholders, buying committee, who else, power map, stakeholder map."
---

# Stakeholder Mapping

## Purpose
Turn a deal's contact list into a power map: who matters, how much influence each
person carries, whether they're for you or against you, and — most importantly —
which decision-making roles you have *not* yet reached. Output a coverage gap list
and a concrete plan to access the missing players before they sink the deal.

## Inputs
- The list of people you've engaged on the deal (names + titles)
- What each person has said or done (transcripts, emails, your recollection)
- The deal's stage, size, and what you're trying to advance
- Your read on the org chart (reporting lines, who answers to whom)

## Method
1. **List every known contact** with title and the last time you interacted.
2. **Score each person on three axes** and place them in the grid below.
3. **Classify each as champion / blocker / neutral / coach** using the rules.
4. **Run the coverage check**: mark which buying roles are filled vs. empty.
5. **Build the access plan** to reach the empty roles.
6. **Emit the power map** in the output format.

**Three axes (score each person 1–5):**
- **Role power** — formal authority over the decision and budget.
- **Influence** — informal sway over the outcome, regardless of title.
- **Sentiment** — how they feel about you/your solution: −2 (against) to +2 (for).

**Power-map grid (role power × influence):**
```
                 HIGH INFLUENCE          LOW INFLUENCE
              +----------------------+----------------------+
  HIGH POWER  | KEY PLAYERS          | DORMANT AUTHORITY    |
              | (must win — econ     | (has the title, not  |
              |  buyer, exec sponsor)| engaged — wake them)  |
              +----------------------+----------------------+
  LOW  POWER  | HIDDEN INFLUENCERS   | LOW PRIORITY         |
              | (no title, big sway —| (keep warm, don't    |
              |  coach, gatekeeper)  |  over-invest)        |
              +----------------------+----------------------+
```
Plot each contact into one quadrant. Annotate each name with sentiment
(`+2 … −2`). The top-left quadrant is where deals are won or lost.

**Classification rules:**
- **Champion** — high influence, sentiment +2, *and* actively sells for you when
  you're not in the room. Influence without action is just a fan, not a champion.
- **Blocker** — sentiment −1 or worse with the power to stall or kill. Name the
  reason (incumbent loyalty, competing priority, threatened by the change).
- **Coach** — gives you intel and guidance but lacks authority. Invaluable for
  navigating, never a substitute for a champion.
- **Neutral** — engaged but undecided; a conversion target.

**Coverage gap check — the buying committee roles:**
| Role | Question to answer | Filled? |
|------|--------------------|---------|
| Economic buyer | Who controls the budget / signs? | |
| Technical buyer | Who vets feasibility / security / integration? | |
| User buyer(s) | Who lives with this day to day? | |
| Champion | Who sells internally for you? | |
| Coach | Who feeds you intel? | |
| Blocker (known) | Who could stop this — do you know them? | |

Any empty row is a **gap**. A deal where you've only met the user buyer is
single-threaded and high-risk — flag it loudly.

**Access plan (one row per gap):**
`gap role → who can introduce you → the ask → the angle that earns the meeting`
- Prefer warm intros through a champion or coach over cold outreach.
- Give the introducer a reason the new stakeholder benefits from the meeting,
  not just a reason *you* want it.
- Tie each access move to deal advancement (mutual action plan, exec-to-exec, ROI
  review for the economic buyer, security review for the technical buyer).

## Tool binding
This skill works from a contact list alone. It gets sharper when connected to your
stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, pull the committee directly
instead of asking the user to reconstruct it from memory:
- `ontology_resolve("deal", id, expand=["stakeholders","emails","activity"])` —
  use the transcript- and email-derived stakeholder roster, who's actually been
  engaged (and how recently, via `activity`), and email threads to read sentiment
  from real language rather than guesswork.
- For each stakeholder, drill in with
  `ontology_resolve("person", id, expand=["deals","meetings","emails","company"])`
  — see every meeting they attended, their email footprint, other deals they touch,
  and their company role to calibrate role power and influence.
Doris already extracts stakeholders and engagement per call — prefer those signals
over re-deriving from raw text, and use them to detect roles that appear in
transcripts/emails but were never formally engaged (the dormant-authority quadrant).

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot) → pull the contact roster and contact roles for the
  deal as the starting committee list.
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) → see who actually spoke on
  calls and gauge sentiment from what they said.
- Email MCP → read thread participation to spot engaged-but-unlogged stakeholders.

### With nothing connected
Ask the user to list the contacts they've engaged, with title and last interaction.
Then:
1. Score each on role power, influence, and sentiment from the user's account.
2. Plot the power-map grid and classify each as champion/blocker/neutral/coach.
3. Run the coverage check against the six buying roles; mark empty rows as gaps.
4. Produce the access plan for each gap.
Output the full power map, the gap list, and the access plan as copy-paste text.

## Works without Doris
Fully functional from a hand-listed contact roster — Doris only removes the
reconstruction step and supplies evidence-backed engagement, role, and sentiment
signals so the map reflects what actually happened, not memory.

## Common mistakes
- Confusing title with power — the named decision-maker often defers to a hidden
  influencer; score influence separately from role power.
- Calling someone a champion because they're friendly; a champion sells for you
  when you're not in the room.
- Declaring full coverage when you've only met user buyers — the economic and
  technical buyers are the ones who kill deals late.
- Mapping once and never updating it; committees shift, sponsors leave, blockers
  emerge. Re-map on every major meeting.
- Building an access plan of cold outreach instead of routing through a coach or
  champion who can open the door warm.
