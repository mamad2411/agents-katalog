---
name: event-planner
description: "Plans virtual and in-person events with detailed checklists, timelines, run-of-show documents, promotional copy, and attendee communications, with optional planning pages in Notion. Use when a user is organizing a workshop, conference, meetup, launch party, networking event, or any event that needs structured planning and communication materials."
allowed-tools: Read Write Glob mcp__claude_ai_Notion__notion-create-pages mcp__claude_ai_Notion__notion-search mcp__claude_ai_Notion__notion-create-database
metadata:
  author: Salah-XD
  version: "1.0"
---

# Event Planner

## When to Use This Skill

Use this skill when you need to:
- Plan a workshop, conference, meetup, launch party, or networking event from scratch
- Build a master checklist with timeline milestones for any event type
- Create a run-of-show document with minute-by-minute scheduling
- Write promotional copy including registration pages, email sequences, and social posts
- Draft attendee communications (welcome messages, reminders, follow-ups)
- Optionally save the planning checklist and run-of-show to Notion

**DO NOT** use this skill for:
- Webinars or virtual presentations with slide decks (use webinar-planner instead)
- Pre-recorded course content (use course-outline instead)
- Ongoing content scheduling without an event anchor (use content-calendar instead)
- Email sequences unrelated to an event (use email-sequence instead)

---

## Core Principle

EVERY EVENT EXISTS TO ACHIEVE ONE MEASURABLE GOAL FOR THE HOST AND ONE CLEAR OUTCOME FOR THE ATTENDEE — IF YOU CANNOT STATE BOTH IN ONE SENTENCE, THE EVENT IS NOT READY TO PLAN.

---

## Event Type Reference

| Type | Typical Duration | Format | Key Logistics | Default Goal |
|------|-----------------|--------|---------------|-------------|
| **Workshop** | 2-4 hours | In-person or virtual | Hands-on materials, breakout space, AV | Education |
| **Conference** | Full day+ | In-person or hybrid | Multiple rooms, speakers, catering, signage | Authority |
| **Meetup** | 1-2 hours | In-person | Casual venue, name tags, light refreshments | Community |
| **Launch Party** | 2-3 hours | In-person or virtual | Product demo area, branded decor, photographer | Buzz |
| **Networking Event** | 1.5-3 hours | In-person | Open floor plan, conversation starters, name tags | Lead gen |

---

## Phase 1: Brief

Gather all event details before building any materials.

1. **Event name** — what the event is called (ask, no default)
2. **Event type** — workshop, conference, meetup, launch party, or networking (ask, no default)
3. **Format** — in-person, virtual, or hybrid (ask, no default)
4. **Date and time** — when the event takes place (ask, no default)
5. **Goal** — leads, sales, community, education, or brand awareness (ask, no default)
6. **Expected attendance** — how many people (50 by default)
7. **Venue or platform** — physical location or virtual platform (Zoom by default for virtual)
8. **Budget range** — total event budget (proceed without if user declines)
9. **Speakers or hosts** — names and titles of anyone presenting (host only by default)
10. **Target audience** — who should attend and what problem it solves for them (ask, no default)

### Event Brief Template

```
## Event Brief

**Event:** Content Creator Kickoff — Q2 Networking Night
**Type:** Networking event
**Format:** In-person
**Date/Time:** April 18, 2026 at 6:00 PM PST
**Goal:** Generate 15 warm leads for coaching program
**Expected Attendance:** 40 people
**Venue:** The Hive Coworking, Portland OR — Main event space
**Budget:** $500
**Speakers/Hosts:** Jamie Lawson, Business Coach
**Target Audience:** Local content creators and solopreneurs who want to grow their network
```

**GATE: Do not proceed to Phase 2 until the user confirms event type, format, date, and goal. Attendance, venue, budget, and speakers can use defaults or be left TBD.**

---

## Phase 2: Plan

Build the master planning checklist, run-of-show document, and budget tracker.

### Master Checklist by Timeline

**4+ Weeks Before:**
- [ ] Confirm venue or platform — sign contract, pay deposit, get floor plan or virtual room link
- [ ] Confirm speakers or panelists — send confirmation emails with expectations
- [ ] Draft the event agenda — time blocks, session titles, break periods
- [ ] Set up registration page — Eventbrite, Lu.ma, Google Forms, or landing page
- [ ] Create event budget tracker — venue, catering, marketing, materials, contingency
- [ ] Order branded materials — name tags, signage, banners, printed agendas

**2-3 Weeks Before:**
- [ ] Launch promotional push — announcement email, social media, partner outreach
- [ ] Contact sponsors if applicable — send sponsorship one-sheet
- [ ] Prepare presentation materials — slides, handouts, worksheets, demo equipment
- [ ] Arrange catering or refreshments — confirm headcount, finalize menu
- [ ] Assign day-of roles — registration desk, AV, speaker liaison, photography

**1 Week Before:**
- [ ] Send attendee reminder email — date, time, venue/link, parking, what to bring
- [ ] Conduct tech check for virtual/hybrid — platform, screen sharing, recording, backup
- [ ] Finalize run-of-show — minute-by-minute with owner for each segment
- [ ] Confirm all vendors — catering, AV rental, photographer, venue contact
- [ ] Print attendee list and name tags (in-person)

**Day of Event:**
- [ ] Arrive early — 90 min before for in-person, 30 min for virtual
- [ ] Run final tech check — microphones, projector, WiFi, recording
- [ ] Brief all volunteers — review run-of-show, assign stations
- [ ] Set up registration/check-in area
- [ ] Test backup plan — hotspot, backup slides on USB, venue contact phone number

**After the Event:**
- [ ] Send thank-you email within 24 hours
- [ ] Send feedback survey within 48 hours (3-5 questions)
- [ ] Compile event metrics — attendance rate, feedback scores, leads collected
- [ ] Repurpose event content — recap blog post, social photos, highlight reel
- [ ] Follow up with new contacts — personalized emails within 72 hours

### Run-of-Show Template

Create a minute-by-minute schedule with owner, tech cues, and notes for each segment. Every run-of-show must include pre-event setup, live event segments, and post-event tasks.

```
## Run-of-Show: Content Creator Kickoff
## April 18, 2026 | 6:00 PM PST | The Hive Coworking

PRE-EVENT (4:30 - 6:00 PM)
  4:30  Arrive, confirm room layout          Owner: Jamie
  5:00  Test AV, set up registration table   Owner: Alex
  5:30  Volunteer walkthrough of run-of-show Owner: Jamie
  5:45  Open doors, background music on      Owner: Alex

LIVE EVENT (6:00 - 8:30 PM)
  6:00  Doors open — registration, free networking
        Tech: Music playlist, welcome slide on projector
  6:15  Welcome + housekeeping (10 min)       Owner: Jamie
        Cover: Wi-Fi, restrooms, hashtag, evening format
  6:25  Icebreaker — structured intros (20 min) Owner: Jamie
        Split into groups of 10. Each person: name, what they
        create, one thing they need help with.
  6:45  Featured talk (15 min)                Owner: Jamie
        "3 Collaboration Models That Actually Work for Creators"
  7:00  Networking round 1 — "Find Your Match" (20 min)
        Each person has a card: their "offer" and their "need."
  7:20  Break — refreshments, open conversation (15 min)
  7:35  Networking round 2 — "Lightning Intros" (30 min)
        Groups of 5, 2 min each, rotate twice.
  8:05  Closing remarks + next steps (10 min) Owner: Jamie
        QR code for feedback survey and email list
  8:15  Open networking until close
  8:30  Event ends — cleanup

POST-EVENT
  8:30  Collect sign-in sheet, debrief with volunteers (10 min)
  Next day: Thank-you email + feedback survey
  Within 72 hours: Lead follow-up emails
```

### Budget Tracker Template

If the user provides a budget, create a tracker. Skip if no budget.

```
| Category | Item | Estimated | Actual | Notes |
|----------|------|-----------|--------|-------|
| Venue | The Hive — 4-hour rental | $150 | — | Includes tables, chairs, projector |
| Catering | Appetizers + drinks (40 ppl) | $200 | — | Ordered 2 weeks out |
| Materials | Name tags, signage | $40 | — | Vistaprint |
| Marketing | Eventbrite promoted listing | $50 | — | Optional |
| Contingency | Unexpected costs (12%) | $60 | — | Reserve fund |
| **Total** | | **$500** | — | |
```

### Optional: Save to Notion

1. Call `mcp__claude_ai_Notion__notion-search` to find the parent page
2. Call `mcp__claude_ai_Notion__notion-create-pages` with event brief, checklist (to-do blocks), run-of-show, and budget tracker
3. Confirm publication to the user

**IF NOTION FAILS AFTER 3 ATTEMPTS:** Deliver as local markdown files.

**GATE: Present the master checklist, run-of-show, and budget tracker. Do not proceed to Phase 3 until the user approves.**

---

## Phase 3: Promote

Build registration page copy, 3-email promotional sequence, and social media posts.

### Registration Page Copy

Include these sections: headline + subheadline, 3-5 benefit bullets, host bio, event details (date, time with timezone, address or link, parking/login, price, capacity), CTA button text, "This is for you if..." and "This is NOT for you if..." qualifiers.

```
HEADLINE: Content Creator Kickoff — Q2 Networking Night
Meet the Creators Who Will Make Your Next Quarter Count

SUBHEADLINE: April 18 at 6:00 PM PST | The Hive Coworking, Portland OR | Free

BENEFITS:
- Meet 40+ local creators and solopreneurs in one room
- Walk away with at least 3 connections matched to your skills and goals
- Learn 3 proven collaboration models from Jamie Lawson's featured talk
- Structured networking that skips the small talk
- Light appetizers and drinks included

CTA: Reserve My Spot
```

### 3-Email Promo Sequence

**Email 1: Announcement (2-3 weeks before)**

```
Subject: you're invited — content creator meetup on April 18

Hey [FIRST_NAME],

I'm hosting a networking night for content creators and solopreneurs
in Portland on April 18 at 6:00 PM.

The goal: connect you with 3+ people who can help your next quarter
be better than your last one.

- Structured networking rounds (no awkward milling around)
- A 15-minute talk on 3 collaboration models that actually work
- Light appetizers and drinks at The Hive Coworking

40 spots. Free to attend. Reserve your spot: [REGISTRATION LINK]

See you on the 18th,
Jamie

P.S. Last quarter's event filled up 10 days early.
```

**Email 2: Social Proof (1 week before)** — Share registration numbers, highlight the mix of attendees already signed up (roles and industries), restate logistics and registration link.

**Email 3: Last Chance (day before or morning of)** — Spots remaining, quick logistics (address, parking, time), short reminder of the format, final CTA.

### Social Media Posts

Write one platform-native post per channel. LinkedIn: professional detail with hashtags at bottom. Instagram: hook in first line, concise benefits, CTA to link in bio. X/Twitter: punchy, under 280 characters per tweet, direct register link.

```
LinkedIn example:
I'm hosting a free networking night for content creators in Portland on April 18.

40 creators. Structured networking. A short talk on collaboration
models that generate revenue. Food and drinks.

Last quarter's event connected a podcast host with a newsletter writer
who now cross-promote weekly. That's the outcome I'm designing for.

April 18 | 6 PM | Free | 40 spots | Link in comments.

#ContentCreators #PortlandNetworking #Solopreneur
```

**GATE: Present all promotional materials. Do not proceed to Phase 4 until the user approves.**

---

## Phase 4: Execute

Finalize day-of materials: day-of checklist, finalized run-of-show, attendee welcome message, and tech backup plan.

### Attendee Welcome Message (24 hours before)

```
Subject: see you tomorrow — here's everything you need

Hey [FIRST_NAME],

The Content Creator Kickoff is tomorrow at 6 PM.

WHERE: The Hive Coworking, 1234 SE Division St, Portland OR 97202
WHEN: Doors at 6:00 PM, program at 6:15 PM
PARKING: Free street parking after 6 PM
BRING: Business cards or phone with LinkedIn/Instagram ready

Tip: Think about one thing you need help with and one thing you
can offer. That's your intro for the icebreaker.

See you there,
Jamie
```

### Tech Backup Plan

Address at least these scenarios:

- **Mic fails:** Project voice from center of room; ask venue for backup mic
- **Projector fails:** Deliver talk without slides; announce survey URL verbally
- **WiFi fails:** Use mobile hotspot; switch to printed check-in list; collect emails on paper
- **Catering no-show:** Send volunteer for basic refreshments using contingency fund
- **Speaker cancels day-of:** Extend networking rounds; host delivers shorter informal talk

---

## Phase 5: Follow-Up

### Thank-You Email (Within 24 Hours)

```
Subject: thanks for showing up last night

Hey [FIRST_NAME],

Thanks for being part of the Content Creator Kickoff.

3 things to do this week:
1. Follow up with your new connections — send a quick "great meeting
   you" message to the 2-3 people you clicked with
2. Tag us with #ContentCreatorKickoff and I'll reshare the best posts
3. Fill out the 2-minute feedback survey: [SURVEY LINK]

I'm already planning the Q3 event. Reply "I'm in" for priority access.

Jamie

P.S. Photos from last night: [PHOTO ALBUM LINK]
```

### Feedback Survey (3-5 Questions)

1. Overall rating (1-5 stars)
2. Most valuable part (structured networking / featured talk / open networking / other)
3. Did you make at least one meaningful connection? (Yes / No)
4. What would you improve? (open text)
5. Would you attend again? (Definitely / Probably / Unlikely)

### Recap Content

- **Blog post outline:** Why we hosted it, how the format worked, key takeaways from the talk, results and feedback highlights, next event announcement
- **Social recap post:** Attendance stat, 2-3 specific outcomes (collaborations formed, connections made), invitation to next event

### Lead Nurture (Within 72 Hours)

Personalized email to warm leads collected at the event. Reference a specific detail from the conversation. Include: next event invitation, newsletter opt-in, booking link for 1-on-1 chat.

---

## Example 1: Virtual Workshop for a Coach

**User request:** "I'm a productivity coach running 'Build Your Content System in 90 Minutes' on Zoom. 50 attendees, free, need the full plan."

**Execution:**

1. **Brief:** Workshop, virtual, 50 attendees, Zoom, $0, goal: education + lead gen.
2. **Plan:** Checklist adapted for virtual (no venue/catering tasks). Run-of-show: 10 min welcome, 25 min teaching block 1, 25 min teaching block 2, 15 min hands-on exercise, 10 min Q&A, 5 min closing. Tech backup: backup Zoom link, phone dial-in.
3. **Promote:** Registration page for content creators. 3 promo emails. Social posts for LinkedIn, Instagram, X.
4. **Execute:** Virtual day-of checklist (tech check 30 min before, slides loaded, chat moderator assigned). Welcome message with Zoom link.
5. **Follow-up:** Thank-you with replay link, feedback survey, recap social post, lead nurture email.

**Result:** Run-of-show, 8 emails, registration page, 3 social posts, zero budget.

---

## Example 2: In-Person Networking Meetup

**User request:** "I run a local entrepreneur community. 30 people, rented venue, $500 budget."

**Execution:**

1. **Brief:** Networking event, in-person, 30 attendees, $500, goal: community + warm leads.
2. **Plan:** Full in-person checklist. Run-of-show for 2 hours: arrival, icebreaker, two structured networking rounds, break, closing. Budget tracker: venue $150, catering $180, materials $35, contingency $65.
3. **Promote:** Eventbrite registration. 3 emails to community list. LinkedIn and Instagram posts.
4. **Execute:** Day-of checklist with venue setup, registration desk, AV, volunteer briefing. Welcome message with parking details. Tech backup for in-person contingencies.
5. **Follow-up:** Thank-you with photos, feedback survey, recap post, personalized lead nurture to top 10 contacts.

**Result:** Run-of-show, budget tracker, 7 emails, registration page, 2 social posts, $500 allocated.

---

## Anti-Patterns

- **DO NOT plan without a measurable goal.** "Build community" is not measurable. "Collect 15 warm leads" is. Without a goal, there is no way to evaluate success.
- **DO NOT skip the tech backup plan for virtual events.** Every virtual event needs a backup meeting link, phone dial-in, and a plan for host internet failure.
- **DO NOT send follow-ups more than 48 hours after the event.** Thank-you within 24 hours. Survey within 48. Leads go cold after 72.
- **DO NOT create agendas without buffer time.** Minimum 5-minute buffer between segments. No buffer guarantees running late by segment three.
- **DO NOT overprogram networking events.** At least 30% of total time must be unstructured. Over-scheduling kills organic conversations.
- **DO NOT skip the day-of checklist.** Memory fails under pressure. The checklist prevents forgotten name tags, untested microphones, and missing signage.
- **DO NOT copy-paste the same promo post across platforms.** LinkedIn is professional. Instagram is concise and visual. X is punchy. Each must feel native.
- **DO NOT skip logistics on the registration page.** Every page needs: date, time with timezone, address or link, parking or login instructions. Missing logistics create inbox floods.
- **DO NOT plan in-person events without a venue walkthrough.** Floor plans lie. Visit the space. Confirm AV, capacity, layout, and restroom access.
- **DO NOT ignore no-shows.** 30-50% of registrants will not attend. Send them a recap and invite to the next event. They are still warm leads.

---

## Recovery

- **User cannot define the goal:** Ask "What do you want to be true 1 week after this event that is not true today?" Translate their answer into a measurable outcome.
- **Budget too small:** Scale down. Remove catering (suggest BYOB). Switch to a free venue (library, partner's office). Use digital name tags. A $0 event with 15 people can still hit the goal.
- **Venue falls through last minute:** (1) Find backup coworking space, (2) ask an attendee or partner to host, (3) pivot to virtual as last resort. Email registrants with updated details immediately.
- **Speaker cancels day-of:** Extend networking rounds by 15 minutes. Host delivers a shorter informal talk. Announce at welcome without over-apologizing.
- **Notion integration fails:** Deliver checklist, run-of-show, and budget tracker as local markdown files with clear formatting for manual paste.
- **Low registrations 1 week before:** (1) Re-share registration link on all channels, (2) rewrite promo copy with sharper benefits, (3) ask 3-5 target attendees what is stopping them. If still low, shrink the event rather than canceling.
- **Event runs over time:** Cut from the next break or open networking, never from closing remarks. The closing collects survey sign-ups and announces the next event.

---

## Pre-Delivery Checklist

```
  [ ] Event brief confirmed before planning began
  [ ] Checklist covers all 5 timeline phases
  [ ] Run-of-show has timestamps with owners for every segment
  [ ] Buffer time (min 5 min) between major segments
  [ ] Registration page includes headline, benefits, host bio, logistics, CTA
  [ ] 3 promo emails with appropriate send dates
  [ ] Social posts are platform-native
  [ ] Tech backup plan covers at least 3 failure scenarios
  [ ] Follow-up includes thank-you, survey, and lead nurture
  [ ] Budget tracker includes contingency (if budget provided)
  [ ] No placeholder text — all examples use real content from the brief
  [ ] All times include timezone
```
