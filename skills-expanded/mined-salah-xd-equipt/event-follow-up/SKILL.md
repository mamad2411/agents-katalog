---
name: event-follow-up
description: "Creates post-event follow-up sequences with thank-you emails, survey distribution, content delivery, and nurture paths."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Event Follow-Up

## When to Use This Skill

Use this skill when you need to:
- Create a post-event follow-up email sequence for attendees
- Design survey distribution and feedback collection processes
- Build content delivery systems for recordings, slides, and resources
- Plan nurture paths that convert attendees into customers or community members

**DO NOT** use this skill for pre-event marketing or event-day communications. This is for everything that happens after the event ends.

---

## Core Principle

THE EVENT IS NOT OVER WHEN THE LAST SESSION ENDS — IT IS OVER WHEN EVERY ATTENDEE HAS BEEN THANKED, SURVEYED, GIVEN ACCESS TO RECORDINGS, AND OFFERED A CLEAR NEXT STEP.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Event name and date** | "What event just happened?" | No default — must be provided |
| **Attendee count** | "How many people attended?" | No default — must be provided |
| **Content to deliver** | "Do you have recordings, slides, or resources to share?" | Recordings + slide decks |
| **Next offer** | "What do you want attendees to do next? (buy, join, subscribe, attend next event)" | Join a paid program or community |
| **Survey goals** | "What feedback do you need?" | Overall satisfaction + improvement suggestions |
| **Follow-up timeline** | "How long should the follow-up sequence run?" | 14 days |

**GATE: Confirm the brief before building the sequence.**

---

## Phase 2: Plan

### Follow-Up Timeline

```
## Post-Event Sequence

**Day 0 (event ends):** Thank-you email + key takeaways
**Day 1:** Feedback survey email
**Day 3:** Recording/resource delivery email
**Day 5:** Highlight reel — best moments, quotes, photos
**Day 7:** Survey reminder (if not completed)
**Day 10:** Nurture email — "Here's how to implement what you learned"
**Day 14:** Next step offer — "The next level is [paid program/next event/community]"
```

### Audience Segmentation

```
| Segment | Criteria | Follow-Up Focus |
|---------|----------|----------------|
| Attended live | Showed up for sessions | Full sequence + VIP treatment |
| Registered but absent | Signed up, did not attend | Recording access + "you missed it" framing |
| VIP/premium | Paid for higher tier | Personal follow-up + exclusive bonus |
| Speakers/sponsors | Partners | Thank-you + results data + renewal conversation |
```

**GATE: Present the timeline and segments for approval.**

---

## Phase 3: Write

### Email 1: Thank-You (Day 0)

```
Subject: You showed up — here's what's next

[Personal thank-you from the host]
[Top 3 takeaways or moments from the event]
[What to expect in the coming days (recordings, resources, survey)]
[One immediate action item: "The #1 thing to do this week based on what you learned"]
```

### Email 2: Survey (Day 1)

```
Subject: Quick favor — 2 minutes to make the next event even better

[Acknowledge their time and input]
[Link to survey — keep it under 5 minutes]
[What you'll do with the feedback]
[Optional: incentive for completing (raffle entry, bonus resource)]
```

### Email 3: Content Delivery (Day 3)

```
Subject: Your [Event Name] recordings and resources are ready

[Access link to recordings]
[Slide decks or downloadable resources]
[Recommended watching order or "start here" guide]
[Access expiration if applicable]
```

### Email 4: Highlight Reel (Day 5)

```
Subject: The best moments from [Event Name]

[Photos, quotes, and key stats from the event]
[Social sharing prompt — encourage attendees to share their experience]
[Community link if applicable]
```

### Email 5: Implementation (Day 10)

```
Subject: How to actually use what you learned at [Event Name]

[Pick one key framework or tactic from the event]
[Break it into 3 implementation steps]
[Offer help: resource, template, or community support]
```

### Email 6: Next Step Offer (Day 14)

```
Subject: Ready for the next level?

[Connect the event experience to the next offer]
[What the offer is and who it's for]
[Specific benefit — what they'll achieve]
[CTA with deadline or incentive for event attendees]
[Attendee-exclusive pricing or bonus if applicable]
```

---

## Phase 4: Polish

### 1. Survey Design

```
## Post-Event Survey (5 minutes)

1. Overall, how would you rate the event? (1-10)
2. What was the most valuable session or takeaway? (Open)
3. What would you improve for next time? (Open)
4. How likely are you to attend again? (1-10 NPS)
5. How likely are you to recommend this event to a colleague? (1-10 NPS)
6. May we use your feedback as a testimonial? (Yes/No)
7. What topics would you like to see at future events? (Open)
```

### 2. Content Delivery Checklist

```
- [ ] Recordings are edited (remove dead air, tech issues)
- [ ] Slide decks are collected from all speakers
- [ ] Resources are organized in a single access point (Notion, Google Drive, or member area)
- [ ] Access links are tested and working
- [ ] Expiration dates are set and communicated (if applicable)
- [ ] Speaker attribution is included on all shared materials
```

### 3. Metrics to Track

```
## Follow-Up Performance
- Thank-you email open rate (target: 60%+)
- Survey completion rate (target: 30%+)
- Recording access rate (target: 50%+)
- Nurture email click rate (target: 5%+)
- Next-step offer conversion rate (track against event attendee count)
- NPS score from survey (target: 50+)
```

---

## Example 1: Business Conference Follow-Up

```
Day 0: "Thank you for making Scale Summit unforgettable" — top 3 moments + next steps
Day 1: Survey with raffle for free ticket to next event
Day 3: All 12 session recordings + speaker slides
Day 7: "The #1 framework from Scale Summit — how to implement it this week"
Day 14: "Scale Summit alumni get 20% off our 12-week growth program"
```

## Example 2: Virtual Summit Follow-Up

```
Day 0: "The summit is a wrap — here are your top takeaways"
Day 1: 3-question survey (keep it ultra-short for virtual)
Day 2: VIP pass offer — "Get lifetime access to all recordings for $47"
Day 5: Highlight reel + speaker social tags
Day 10: Free resource related to the summit theme
Day 14: Community membership offer
```

---

## Anti-Patterns

- **No follow-up at all** — the most common mistake. Silence after an event wastes all the goodwill you built.
- **Waiting too long** — the thank-you email must go out within hours, not days. Momentum fades fast.
- **Immediate hard sell** — pitching your paid program 2 hours after the event feels extractive. Thank first, sell later.
- **No survey** — you cannot improve what you do not measure. Always collect feedback.
- **Generic emails** — "Dear attendee" is lazy. Use their name and segment by attendance type.
- **Recordings never delivered** — if you promised recordings, deliver them within 72 hours or lose trust.

---

## Recovery

- **Recordings are not ready:** Send a "coming soon" email with a specific delivery date. Do not wait for recordings to send the thank-you.
- **Survey response rate is low:** Send one reminder, then accept the data you have. Offering a small incentive (raffle, bonus resource) helps.
- **Attendees are unresponsive to nurture:** Shorten the sequence. If they are not engaging by email 3, they may not convert this cycle. Add them to your regular list.
- **User did not collect attendee emails:** If this was an in-person event, use the registration list. For future events, make email capture mandatory at check-in.
