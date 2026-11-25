---
name: meeting-prep-kit
description: Personal meeting prep tool. Given a meeting (attendees, topic, desired outcome), generates a tight prep packet — 3-bullet pre-read, time-boxed agenda, your top 3 talking points, and the top 3 objections you'll face with rebuttals. Use before any meeting where you're driving an outcome — exec reviews, stakeholder pitches, scope negotiations, manager 1:1s with an ask, vendor calls.
---

# Meeting Prep Kit

Personal prep tool for meetings where *you* are driving an outcome. Not a meeting note-taker. Not a generic agenda builder. The output is for you, the person walking into the room.

---

## Design choices (why this skill is opinionated)

- **For you, not the team.** Output assumes you already know the context. No "as you know" preambles.
- **Outcome-first.** Every section ladders back to one thing: what you want when you walk out.
- **Top 3, not all 12.** Talking points capped at 3. Objections capped at 3. If you can't pick 3, you don't know your ask yet.
- **Speakable, not slidable.** Talking points are how you'd actually say it out loud — not bullet-point soup.

---

## Inputs the skill needs (interview if missing)

1. **Who's in the room?** Names + roles. Power dynamics matter.
2. **Meeting length** (15 / 30 / 60 min)
3. **Topic** (one sentence)
4. **The outcome you want.** Specific. "Get Sarah to approve $50K budget" — not "discuss budget."
5. **What they care about** (their KPIs, recent context, stated priorities)
6. **What you have** (data, alternatives, asks already discussed offline)

If any of these are missing, ask before drafting. Vague inputs = generic output.

---

## Output format

### Pre-read (3 bullets, ≤30 words each)
The minimum context anyone in the room needs before you open your mouth. Three things, no more.

### Time-boxed agenda

| Time | Section | Owner |
|------|---------|-------|
| 0:00 | What this is + the outcome we need | You |
| 0:03 | Context (data, ≤2 min) | You |
| ... | ... | ... |
| Final 5 min | Decision + next steps | You |

Total adds up to meeting length. Decision time is always reserved at the end.

### Your talking points (top 3, in order)
1. **Lead with the strongest** — the one fact or framing they can't argue with.
2. **Address the elephant** — name the obvious objection yourself, before they do.
3. **Make the ask** — the one specific yes/no thing you want.

Each in plain spoken language. No corporate-speak, no buzzwords.

### Anticipated objections (top 3, with rebuttals)

| Objection | Who'd raise it | Your rebuttal (1 line) |
|-----------|----------------|------------------------|
| "We tried this in 2023 and it didn't work" | Sarah | "Different context — Q1 data shows X is now true" |
| ... | ... | ... |

---

## Process

1. **Confirm inputs** (interview if anything's missing).
2. **Reverse-engineer from the outcome.** What would have to be true for them to say yes?
3. **Draft pre-read → agenda → talking points** in that order.
4. **Brainstorm objections by role.** What would each person in the room push back on?
5. **Cut everything that doesn't ladder to the outcome.** If a bullet doesn't serve the ask, drop it.

---

## Worked example

**Input**
- Who: Mark (VP Eng), Priya (PM lead)
- Length: 30 min
- Topic: Pushing v2 launch from 5/15 to 6/1
- Outcome: Both approve the slip by end of meeting
- They care about: Mark = team burnout, Priya = GTM commits to design partners
- I have: 400-hr capacity gap, 2 design partners' rescheduling status, Q1 burnout survey (4/10 NPS)

**Output**

### Pre-read
- v2 scope = 1,800 hrs estimated; team capacity = 1,400 hrs (400-hr gap).
- Cutting AI-tagging closes the gap but breaks the GTM commit to 4 design partners.
- Slip to 6/1 = 17 days, keeps full scope, gives the team room (NPS hit 4/10 in Q1).

### Agenda
| Time | Section | Owner |
|------|---------|-------|
| 0:00 | Why we're here + the ask | You |
| 0:03 | The capacity gap (data) | You |
| 0:08 | Two paths: cut vs. slip | You |
| 0:15 | Discussion | Mark, Priya |
| 0:25 | Decision + next steps | All |

### Talking points
1. We're 400 hrs over and the team's already at 4/10 NPS. If we ship 5/15, we either cut quality or burn the team for two more weeks. That's the actual choice.
2. I know GTM committed 5/15 — I've already drafted the design-partner email and confirmed they can absorb a 17-day slip without losing the pilot.
3. I'm asking for the slip to 6/1, full scope intact. Yes/no by EOD so I can lock the comms.

### Objections
| Objection | Who | Rebuttal |
|-----------|-----|----------|
| "Why didn't you flag this 2 weeks ago?" | Mark | I underestimated the AI-tagging integration. Baking better estimation into the next planning cycle. |
| "Can't we just cut AI-tagging?" | Priya | We could — but it's the #1 ask from 3 of 4 design partners. Slipping costs less than cutting. |
| "What does this do to Q3?" | Mark | Q3 plan already assumed 6/1 — buffer was built in. No downstream slip. |

---

## When to use
- Exec reviews where you're presenting
- Stakeholder pitches that need a yes
- Scope or timeline negotiations
- 1:1s with your manager where you're making an ask (raise, role change, project shift)
- Vendor calls where you're closing or evaluating

## When NOT to use
- Status updates (no outcome to drive)
- Brainstorms (no ask)
- 1:1 catchups (no agenda needed)
- Recurring standups

---

## Pairs well with
- **Decision Memo Builder** — if the meeting is to approve a memo, draft the memo first, prep the meeting around it
- **McKinsey Critic** — run your talking points through the critic before walking in
