---
name: webinar-planner
description: "Plans webinars end-to-end with content outlines, slide structures, promotional email sequences, registration page copy, and post-webinar follow-up, with optional planning pages in Notion and promotional graphics in Canva. Use when a user is hosting a webinar, live workshop, or virtual event and needs the full content and promotional package."
allowed-tools: Read Write Glob mcp__claude_ai_Notion__notion-create-pages mcp__claude_ai_Notion__notion-search mcp__claude_ai_Canva__generate-design mcp__claude_ai_Canva__generate-design-structured mcp__claude_ai_Canva__list-brand-kits mcp__claude_ai_Canva__export-design mcp__claude_ai_Canva__get-export-formats mcp__claude_ai_Canva__get-design-thumbnail
metadata:
  author: Salah-XD
  version: "1.0"
---

# Webinar Planner

## When to Use This Skill

Use this skill when you need to:
- Plan a live webinar, virtual workshop, or online event from scratch
- Build a content outline with slide structure and speaker notes
- Write a registration page with headline, benefits, and CTA
- Create a promotional email sequence to fill seats before the event
- Write a post-webinar follow-up sequence for attendees and no-shows
- Optionally create a planning page in Notion and promotional graphics in Canva

**DO NOT** use this skill for pre-recorded courses (use course-outline), podcast planning (use podcast-show-notes), in-person event logistics, or standalone email sequences (use email-sequence).

---

## Core Principle

EVERY WEBINAR EXISTS TO DELIVER ONE TRANSFORMATIVE IDEA AND ONE CLEAR NEXT STEP — IF THE AUDIENCE CANNOT STATE BOTH IN ONE SENTENCE AFTER ATTENDING, THE WEBINAR FAILED.

---

## Webinar Type Reference

| Type | Price | Duration | Pitch | Primary Goal | Best For |
|------|-------|----------|-------|--------------|----------|
| **Lead Gen** | Free | 60 min | Yes (10 min) | Collect leads, pitch offer | Coaches, consultants, course creators |
| **Authority Builder** | Free | 45-60 min | No | Build credibility, grow audience | Thought leaders, agency owners |
| **Workshop** | $27-197 | 90 min | Optional upsell | Deliver hands-on outcome | Service providers, educators |
| **Product Demo** | Free | 30-45 min | Feature walkthrough | Drive sign-ups or trials | SaaS founders, e-commerce operators |

---

## Phase 1: Strategy

Gather all details before building content. Use defaults in parentheses when the user does not specify.

1. **Topic** — what the webinar teaches (ask, no default)
2. **Target audience** — who attends and their problem (ask, no default)
3. **Goal** — leads, sales, authority, or product adoption (ask, no default)
4. **Format** — teaching, demo, panel, or Q&A (teaching)
5. **Webinar type** — lead gen, authority builder, workshop, or product demo (lead gen)
6. **Duration** — 30, 45, 60, or 90 minutes (60 min)
7. **Offer or pitch** — what you sell at the end, if anything (ask for lead gen/workshop)
8. **Date and time** (ask, no default)
9. **Platform** — Zoom, WebinarJam, StreamYard, or other (Zoom)
10. **Speaker name and title** (ask, no default)

Present the strategy brief before writing anything:

```
## Webinar Strategy Brief

**Topic:** How to Land Your First 5 Coaching Clients Using LinkedIn
**Audience:** New coaches (0-3 clients) who struggle with lead generation
**Goal:** Lead generation — pitch group coaching program at end
**Format:** Teaching (slides + live examples)
**Type:** Lead Gen (free, 60 min, pitch at end)
**Offer:** "Client Magnet Accelerator" — 8-week group coaching ($997)
**Date/Time:** March 22 at 12:00 PM EST
**Platform:** Zoom
**Speaker:** Rachel Torres, Certified Business Coach
```

**GATE: Do not proceed to Phase 2 until the user confirms topic, audience, goal, and format.**

---

## Phase 2: Content

Build the webinar structure, slide outline, and speaker notes.

### Structure Template (60-Minute Default)

| Segment | Time | Duration | Purpose |
|---------|------|----------|---------|
| Welcome + housekeeping | 0:00-5:00 | 5 min | Greet, set expectations, explain Q&A |
| Hook + problem statement | 5:00-10:00 | 5 min | Name the pain, state the promise |
| Content block 1 | 10:00-25:00 | 15 min | First teaching point with examples |
| Content block 2 | 25:00-40:00 | 15 min | Second teaching point with examples |
| Content block 3 | 40:00-50:00 | 10 min | Third teaching point or live demo |
| Q&A or Pitch | 50:00-60:00 | 10 min | Questions (authority) or offer (lead gen) |

**Duration variants:** 45 min: compress Block 3 and Q&A to 5 min each. 90 min workshop: expand blocks to 20 min, add 10-min exercise after Block 2, extend Q&A to 15 min.

### Slide Outline

Default: 18-22 slides for 60 minutes. Create titles with purpose notes for each:

- **Slide 1** — Title slide (webinar name, speaker, date)
- **Slide 2** — About the speaker (credibility proof in one sentence)
- **Slide 3** — Housekeeping (recorded, chat Q&A, stay for bonus)
- **Slide 4** — The Problem (name their pain with a specific stat or scenario)
- **Slide 5** — The Promise (what they will walk away with)
- **Slides 6-9** — Content Block 1 (concept, framework, before/after example, action step)
- **Slides 10-13** — Content Block 2 (same structure: concept, framework, example, action)
- **Slides 14-16** — Content Block 3 (concept, live demo or case study, key takeaway)
- **Slide 17** — Recap (restate all 3 steps in one slide)
- **Slide 18** — The Offer (lead gen only: program details, price, enrollment link, attendee bonus)
- **Slide 19** — Q&A
- **Slide 20** — Thank you + next steps (replay info, free resource download, contact)

### Speaker Notes

Write notes for the hook, each block opener, the offer, and the close. 3-5 bullets per slide. Example:

```
SLIDE 4 (The Problem):
- Open with: "Raise your hand in chat if you've ever spent an entire week
  trying to figure out where to find clients instead of actually coaching."
- Pause for chat responses — acknowledge a few by name
- "That's exactly where I was 3 years ago. Great at coaching. Terrible
  at getting people to coach."

SLIDE 18 (The Offer):
- Transition: "Everything I taught today works on its own. But if you want
  me in your corner building this with you, here's how."
- Walk through the 3 biggest benefits (don't read every bullet)
- State the price once, clearly — don't apologize for it
```

**GATE: Present the full content outline to the user. Do not proceed to Phase 3 until approved.**

---

## Phase 3: Promote

Build the registration page, promo emails, social posts, and optional Canva/Notion assets.

### Registration Page Copy

Deliver these elements:

- **Headline:** Specific outcome + objection buster in parentheses. Example: "How to Land Your First 5 Coaching Clients Using LinkedIn (Without Cold DMs, Expensive Ads, or Begging for Referrals)"
- **Subheadline:** Free/paid label + date + time + speaker name
- **3-5 benefit bullets:** Each starts with "The exact..." or "A step-by-step..." — tangible, specific
- **Speaker bio:** 2-3 sentences with credibility proof (number of clients, specific result)
- **Event details:** Date, time, duration, platform, price, replay availability
- **CTA button:** "Save My Spot" (free) or "Reserve My Seat — $XX" (paid)
- **Below the fold:** "This is for you if..." (4 bullets) and "This is NOT for you if..." (3 bullets)

### Promotional Email Sequence (3 Emails)

**Email 1 — Announcement (7 days before):**
- Subject line: personal, lowercase (e.g., "I'm going live on March 22 — you're invited")
- Open with the question the webinar answers
- 3 bullet benefits matching the registration page
- CTA: registration link
- P.S.: replay available but live attendees get a bonus

**Email 2 — Reminder (1 day before):**
- Subject line: urgency + topic (e.g., "tomorrow at noon — your LinkedIn client system")
- 3 prep steps (block calendar, open relevant tool, bring notebook)
- Include the Zoom/event link directly
- P.S.: mention the live-only bonus again

**Email 3 — Last Chance (day of, morning):**
- Subject line: time-based (e.g., "we're live in 3 hours")
- 3 bullet takeaways (not benefits — what they will leave with)
- Event link. Keep under 80 words total.

Write all emails with real copy matching the strategy brief — never use placeholder text.

### Social Media Promo Posts

One post per platform, each native to the format:

- **LinkedIn:** Professional, numbered list of what you will cover, CTA to comment or link in comments, no hashtags in first line
- **Instagram:** Hook in first line (shows before "more"), conversational, "link in bio," end with "save this post"
- **X/Twitter:** Under 280 characters, bold claim + 3 bullet takeaways + "link below"

### Optional: Canva Promotional Graphic

If the user requests a graphic:

1. Call `list-brand-kits` to load colors/fonts
2. Generate at 1080x1080 with webinar title, date/time, speaker name, and "Free Live Training" or price badge
3. Preview with `get-design-thumbnail`, get user approval
4. Export as PNG via `get-export-formats` and `export-design`

**IF NO BRAND KIT:** Ask for primary color, secondary color, font preference. **IF 3 ATTEMPTS FAIL:** Provide a design spec for manual creation.

### Optional: Notion Planning Page

If the user requests a planning page:

1. Call `notion-search` to locate the parent page
2. Call `notion-create-pages` with: strategy brief, slide titles, promo timeline with send dates, run-of-show, and pre/post-event task checklists

**IF SEARCH FAILS AFTER 3 ATTEMPTS:** Provide the planning page as markdown for manual paste.

**GATE: Present registration page and all promo materials. Do not proceed to Phase 4 until approved.**

---

## Phase 4: Execute

### Run-of-Show Document

Create a minute-by-minute timeline. Example for 60-minute lead gen webinar:

```
PRE-SHOW (11:30 AM - 12:00 PM)
  11:30  Open room, start recording, test screen share
  11:45  Load slides, open demo tabs
  11:50  Post "room is open" in chat
  11:55  Welcome early joiners
  11:58  Final mic/camera check
  12:00  START

LIVE SHOW
  12:00  Welcome + housekeeping (Slides 1-3)
  12:05  Hook + problem (Slides 4-5) — ENGAGEMENT: poll or chat question
  12:10  Content Block 1 (Slides 6-9) — ENGAGEMENT: "Type your [X] in chat"
  12:25  Content Block 2 (Slides 10-13) — ENGAGEMENT: "Which approach resonates?"
  12:40  Content Block 3 (Slides 14-16) — ENGAGEMENT: "Has anyone tried this?"
  12:50  Recap (Slide 17) — restate all 3 steps in 60 seconds
  12:51  Offer (Slide 18) — walk through program, state price, share link
  12:56  Q&A (Slide 19) — repeat each question before answering
  12:59  Close (Slide 20) — replay info, free resource, thank you
  13:00  END — stop recording
```

Include at least 3 engagement prompts (chat questions, polls, hand-raises) spaced every 10-15 minutes.

### Tech Checklist

```
Audio:
  [ ] Microphone connected and selected in platform settings
  [ ] Test recording — play back 10 seconds to confirm clarity
  [ ] Notification sounds silenced on all apps and phone

Camera:
  [ ] Positioned at eye level, lighting on face (not behind)
  [ ] Background clean or simple virtual background
  [ ] Preview checked in platform settings

Screen Share:
  [ ] Slide deck on Slide 1, demo tabs open separately
  [ ] All unrelated tabs and apps closed
  [ ] Test share — confirm attendees see slides, not desktop

Recording:
  [ ] Cloud or local recording enabled and tested
  [ ] Backup recording via OBS or QuickTime

Backup Plan:
  [ ] Backup event link ready to email if platform crashes
  [ ] Mobile hotspot as secondary internet connection
  [ ] PDF version of slides if screen share fails
  [ ] Phone dial-in as backup audio

Platform Settings:
  [ ] Attendees muted on entry
  [ ] Chat enabled for all participants
  [ ] Waiting room disabled for direct join
  [ ] Co-host assigned if using a moderator
```

---

## Phase 5: Follow-Up

### Attendee Emails (3 Emails)

**Email 1 — Replay Link (day after):** Subject: "your [topic] replay." Deliver the replay link (available 48 hours), recap the 3 key steps with slide numbers, link to free resource/checklist.

**Email 2 — Value Recap + Nudge (day 3):** Subject: "did you try the [highest-impact tactic]?" Highlight the single most actionable step from the webinar, re-explain it briefly, invite them to reply with their result. P.S. with soft offer mention.

**Email 3 — Offer Deadline (day 5):** Subject: "enrollment closes [day]." State what is included, the price, the attendee bonus, and the deadline. Close with "if now isn't the right time, no worries" to reduce unsubscribes.

### No-Show Emails (2 Emails)

**Email 1 — Replay for No-Shows (day after):** Subject: "you missed it — here's the replay." No guilt. Deliver replay link with timestamps for key sections so they can skip to what matters.

**Email 2 — Final Nudge (day 3):** Subject: "quick recap from the training." Summarize the core takeaway in 3 sentences, restate the 3 steps, note replay expiration, mention the offer link.

**IMPORTANT:** Write separate emails for attendees and no-shows. Never send the same email to both segments.

Write all follow-up emails with real copy matching the webinar content — never use placeholder text.

---

## Example 1: Free Lead-Gen Webinar for a Business Coach

**User request:** "I'm a business coach hosting a free webinar called '3 Steps to Land Premium Clients.' Audience is coaches charging under $2,000/project. Pitching my $4,500 group coaching program. April 10 at 2 PM EST on Zoom."

**Execution:**

1. **Strategy:** Lead gen webinar, 60 min, pitch at end. Brief confirmed.
2. **Content:** 3 blocks — positioning as premium, the value conversation, the proposal that closes. 20-slide deck. Speaker notes for hook ("What if the problem isn't your skills — it's your price tag?") and offer.
3. **Promote:** Registration page with headline "Stop Trading Hours for Dollars." 3 promo emails with real copy. LinkedIn/Instagram/X posts, each platform-native.
4. **Execute:** Minute-by-minute run-of-show with engagement prompts. Zoom tech checklist.
5. **Follow-up:** Attendee sequence — replay with value conversation recap, "try raising your next proposal by 30%" nudge, enrollment deadline. No-show sequence — replay with timestamps, final recap with offer link.

**Delivered:** 20-slide outline, 8 emails, registration page, 3 social posts, run-of-show, tech checklist.

---

## Example 2: Paid Workshop for a Designer

**User request:** "I'm running a $97 workshop: 'Build Your Brand Identity in 90 Minutes.' Audience is solopreneurs who can't afford a designer. They leave with a mood board, color palette, and font pairing. March 29 at 10 AM PST on StreamYard. Want a Canva promo graphic and Notion planning page under 'Workshops.'"

**Execution:**

1. **Strategy:** Paid workshop, 90 min, hands-on. Optional upsell: full brand package ($2,500). Brief confirmed.
2. **Content:** 3 hands-on blocks with 5-min exercises — mood board, color palette, font pairing. 24-slide deck with before/after brand examples. Soft upsell at close (no hard pitch).
3. **Promote:** Registration page with headline "Stop Looking DIY. Start Looking Pro." Promo emails emphasize tangible deliverables. Social posts highlight "walk away with a real brand."
4. **Canva:** Loaded brand kit, generated 1080x1080 promo graphic with title/date/price/"Hands-On Workshop" badge. Exported PNG after approval.
5. **Notion:** Found "Workshops" page via search. Created planning page with brief, content outline, promo timeline, run-of-show, and checklists.
6. **Execute:** Run-of-show with exercise pause notes. StreamYard tech checklist.
7. **Follow-up:** Attendee emails — materials recap, "show me your brand board" engagement, soft upsell. No-show emails — recording with timestamps, final recap.

**Delivered:** 24-slide outline, 8 emails, registration page, 3 social posts, run-of-show, tech checklist, Canva graphic, Notion page.

---

## Pre-Delivery Checklist

Run this before delivering. **DO NOT SKIP ANY ITEM.**

```
  [ ] Strategy brief confirmed before content was written
  [ ] Structure matches confirmed duration (30/45/60/90 min)
  [ ] Slide outline has hook, 3 content blocks, and closing
  [ ] Speaker notes for hook, block openers, and offer slide
  [ ] Registration page has headline, benefits, bio, CTA
  [ ] 3 promo emails with correct timing (7 days, 1 day, day of)
  [ ] Social posts are platform-native (not copy-pasted)
  [ ] Run-of-show has minute-by-minute timestamps
  [ ] Tech checklist covers audio, camera, share, recording, backup
  [ ] Separate follow-up emails for attendees and no-shows
  [ ] Offer details consistent across all materials
  [ ] No placeholder text — all examples use real content
  [ ] All links labeled clearly (registration, event, replay, offer)
```

---

## Anti-Patterns

- **DO NOT create webinars longer than 90 minutes** — attention drops sharply after 60. Workshops are the only exception, and only with hands-on exercises.
- **DO NOT pitch before delivering value** — offers in the first 40 minutes of a 60-minute webinar cause mass drop-off.
- **DO NOT skip the follow-up sequence** — 40-60% of registrants no-show. Without follow-up, you lose the majority of your leads.
- **DO NOT send the same email to attendees and no-shows** — attendees need a recap, no-shows need timestamps and the replay link.
- **DO NOT overload slides with text** — maximum 6 lines per slide. Slides support the speaker, not replace them.
- **DO NOT skip engagement prompts** — webinars without chat interaction every 10-15 minutes become lectures with high drop-off.
- **DO NOT make registration pages longer than needed** — headline, subheadline, 3-5 bullets, bio, CTA. Save long-form for paid workshops.
- **DO NOT skip the tech rehearsal** — audio failures, screen share issues, and recording problems are all preventable.
- **DO NOT send the replay immediately** — send it the next day. Instant replays train people to skip your future live events.

---

## Recovery

- **User cannot define a topic:** Ask "What question do your clients ask you most often?" That question is the webinar. If still stuck, have them name 3 things they help with — pick the one with broadest appeal.

- **User wants to cover too many topics:** Enforce one idea. Ask: "If attendees remember one thing, what should it be?" Cut everything else. Offer to turn extras into future webinars.

- **User has no audience to promote to:** Extend the promo timeline from 7 days to 14-21 days. Recommend organic social promotion and joint webinars with someone who has an audience.

- **User has never presented live:** Add near-scripts to speaker notes for the hook and transitions. Recommend two full rehearsals. Add a "practice run" task to the run-of-show 48 hours before the event.

- **Notion or Canva integration unavailable:** Deliver all content as markdown files with exact specs (dimensions, colors, text). Never block the workflow because an optional integration fails.

- **User wants a panel format:** Replace solo content blocks with moderated discussion blocks. Add panelist intros (5 min), talking points per panelist, and directed Q&A in the run-of-show.

- **If 3 revision rounds produce no approval:** Stop and reassess. Ask the user to share a webinar they loved as a reference for structure and tone.
