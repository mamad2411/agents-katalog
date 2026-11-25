---
name: conference-planner
description: "Plans multi-day conferences with tracks, speaker management, logistics, sponsorship, and attendee experience design."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Conference Planner

## When to Use This Skill

Use this skill when you need to:
- Plan a multi-day conference with multiple tracks and speakers
- Manage logistics including venue, catering, AV, and attendee flow
- Create speaker management processes and content curation systems
- Design the full attendee experience from registration to post-event follow-up

**DO NOT** use this skill for single workshops, webinars, or small meetups. This is for conferences with 100+ attendees, multiple sessions, and complex logistics.

---

## Core Principle

A CONFERENCE IS NOT A COLLECTION OF TALKS — IT IS A CURATED EXPERIENCE WHERE CONTENT, NETWORKING, AND LOGISTICS WORK TOGETHER TO CREATE VALUE THAT CANNOT BE REPLICATED BY WATCHING RECORDINGS.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Conference theme** | "What is the conference about?" | No default — must be provided |
| **Duration** | "How many days?" | 2 days |
| **Expected attendance** | "How many attendees?" | 200-300 |
| **Format** | "In-person, virtual, or hybrid?" | In-person |
| **Budget** | "What is the total budget?" | $50,000 |
| **Revenue model** | "Ticket sales, sponsorships, or both?" | Both |
| **Date range** | "When is the event?" | No default — must be provided |

**GATE: Confirm the brief before proceeding.**

---

## Phase 2: Architecture

### Conference Structure

```
## Day 1
**Morning:** Opening keynote (60 min) → Breakout sessions Track A/B (2 x 45 min)
**Lunch:** Sponsored lunch + networking (90 min)
**Afternoon:** Breakout sessions Track A/B (2 x 45 min) → Panel discussion (60 min)
**Evening:** Networking reception (2 hours)

## Day 2
**Morning:** Keynote (60 min) → Breakout sessions Track A/B (2 x 45 min)
**Lunch:** Roundtable discussions (90 min)
**Afternoon:** Workshop sessions (90 min) → Closing keynote (45 min)
**Close:** Wrap-up + next steps (15 min)
```

### Track Design

```
| Track | Focus | Audience | Sessions |
|-------|-------|----------|----------|
| Track A | [Topic] | [Beginner/Intermediate] | [X sessions] |
| Track B | [Topic] | [Intermediate/Advanced] | [X sessions] |
```

### Speaker Plan

```
## Speaker Targets
- Keynotes: [2-3 names or profile descriptions]
- Breakout speakers: [8-12 speakers needed]
- Panelists: [4-6 per panel]
- Workshop facilitators: [2-4]

## Speaker Package
- Compensation: [Fee, travel, hotel, free ticket]
- Requirements: [Slide deadline, bio, headshot, AV needs]
- Communication timeline: [Outreach → confirm → prep → event]
```

**GATE: Present the conference architecture for approval.**

---

## Phase 3: Build

### Master Planning Document

**1. Venue and Logistics**
```
## Venue Requirements
- Main stage: [capacity, AV needs]
- Breakout rooms: [number, capacity each]
- Networking area: [space requirements]
- Sponsor area: [booth/table space]
- Registration area: [check-in stations]
- Catering: [meals, breaks, dietary accommodations]
```

**2. Timeline (Working Backward)**
```
6 months out: Venue booked, theme finalized, speaker outreach begins
4 months out: Speakers confirmed, sponsorship sales open, early bird tickets launch
3 months out: Schedule published, marketing ramp-up
2 months out: Sponsor materials due, AV confirmed, volunteers recruited
1 month out: Final schedule, attendee communications, run-of-show draft
2 weeks out: Final logistics confirm, speaker prep calls
1 week out: Print materials, signage, swag bags prepared
Day before: Venue walkthrough, tech check, team briefing
```

**3. Budget Template**
```
| Category | Estimated | Actual | Notes |
|----------|----------|--------|-------|
| Venue | $[X] | | |
| Catering | $[X] | | |
| AV/Tech | $[X] | | |
| Speaker fees/travel | $[X] | | |
| Marketing | $[X] | | |
| Printing/signage | $[X] | | |
| Swag/materials | $[X] | | |
| Staff/volunteers | $[X] | | |
| Contingency (10%) | $[X] | | |
| **Total** | **$[X]** | | |
```

**4. Attendee Experience Map**
```
Registration → Welcome email → Event app download → Day 1 check-in →
Welcome session → Content tracks → Networking activities → Day 2 content →
Closing session → Thank-you email → Recording access → Feedback survey →
Next year early bird offer
```

---

## Phase 4: Polish

### 1. Pre-Event Checklist

```
## 1 Week Out
- [ ] All speakers confirmed and prepped
- [ ] AV tested at venue
- [ ] Volunteer team briefed and assigned
- [ ] Attendee communications sent (schedule, logistics, parking)
- [ ] Signage and materials printed
- [ ] Emergency plan in place (medical, weather, tech failure)
- [ ] Run-of-show document finalized and distributed
```

### 2. Day-Of Operations

```
## Day-Of Team Assignments
- Registration: [X people]
- Stage management: [X people]
- Speaker liaison: [1 person per track]
- AV tech: [1-2 people]
- Sponsor support: [1 person]
- Attendee support: [X people]
- Photography/social: [1-2 people]
```

### 3. Post-Event Plan

```
## Post-Event Timeline
Day 1: Thank-you email to all attendees
Day 3: Speaker thank-you + payment processing
Day 5: Attendee survey distribution
Week 2: Recording editing and distribution
Week 3: Sponsor impact reports delivered
Week 4: Team debrief and lessons learned
Month 2: Early bird announcement for next year
```

---

## Example 1: 200-Person Business Conference (2 Days)

```
Theme: "Scale Without a Team" — tools and strategies for solopreneurs
Tracks: Systems & Automation, Marketing & Sales
Keynotes: 2 (opening and closing each day)
Breakouts: 8 sessions across 2 tracks
Budget: $45,000 (offset by $20K sponsorship + $30K ticket sales)
```

## Example 2: 500-Person Industry Summit (3 Days)

```
Theme: "The Future of [Industry]" — trends, technology, and transformation
Tracks: Strategy, Technology, Leadership
Keynotes: 3 (one per day)
Breakouts: 18 sessions, 3 workshops, 2 panels
Budget: $120,000 (sponsored heavily, premium ticket pricing)
```

---

## Anti-Patterns

- **Too many sessions** — quality over quantity. Attendees cannot attend everything, so curate ruthlessly.
- **No networking time** — back-to-back sessions without breaks prevent the connections that make conferences valuable.
- **Ignoring the attendee journey** — if someone cannot figure out where to go, what to attend, or how to connect, the experience fails.
- **Underbudgeting AV** — bad audio ruins every session. Invest in professional AV or do not do in-person.
- **No contingency budget** — something will go wrong. Budget 10-15% for surprises.
- **Starting planning too late** — a 200-person conference needs 4-6 months minimum lead time.

---

## Recovery

- **Budget is too small for the vision:** Scale back attendance, reduce to 1 day, or increase sponsorship targets. Do fewer things well.
- **Cannot fill speaker slots:** Open a CFP (call for proposals) to your community. Peer speakers are often more relatable than celebrities.
- **Ticket sales are slow:** Add urgency (early bird deadline), increase promotion, offer group discounts, or give existing registrants a referral incentive.
- **Venue falls through:** Have a backup venue identified from the start. For emergencies, pivot to virtual with 30+ days notice.
