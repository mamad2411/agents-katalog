---
name: event-run-of-show
description: "Creates detailed run-of-show documents with minute-by-minute timing, cues, transitions, and contingency plans."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Event Run-of-Show

## When to Use This Skill

Use this skill when you need to:
- Create a minute-by-minute run-of-show for a live or virtual event
- Define cues, transitions, and responsibilities for every event moment
- Build contingency plans for technical failures, speaker no-shows, and schedule changes
- Produce a production document that keeps the entire event team synchronized

**DO NOT** use this skill for event planning, marketing, or budgeting. This is the operational document used during the event to ensure everything runs on time and on cue.

---

## Core Principle

A RUN-OF-SHOW IS THE SINGLE DOCUMENT EVERY TEAM MEMBER LOOKS AT DURING THE EVENT — IF IT IS NOT IN THE RUN-OF-SHOW, IT DOES NOT HAPPEN.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Event agenda** | "What is the full session schedule with times?" | No default — must be provided |
| **Team roles** | "Who is on the production team and what are their roles?" | No default — must be provided |
| **Venue/platform details** | "Where is this happening and what tech is available?" | No default — must be provided |
| **Speaker list** | "All speakers with session titles and time slots?" | No default — must be provided |
| **Special moments** | "Any announcements, awards, sponsor mentions, or surprises?" | None |

**GATE: Confirm all details before building the run-of-show.**

---

## Phase 2: Structure

### Run-of-Show Format

```
| Time | Duration | What Happens | Who | Cues/Notes |
|------|----------|-------------|-----|-----------|
| 8:00 AM | 60 min | Doors open / registration | Registration team | Music playing, signage up |
| 9:00 AM | 5 min | Welcome + housekeeping | Host | Slides: welcome deck |
| 9:05 AM | 45 min | Keynote: [Title] | [Speaker] | Lapel mic, slides pre-loaded |
| 9:50 AM | 5 min | Transition + sponsor mention | Host | Slide: sponsor logo |
| 9:55 AM | 5 min | Break | — | Music, timer on screen |
```

### Role Assignments

```
## Production Team

| Role | Person | Responsibilities |
|------|--------|-----------------|
| Stage manager | [Name] | Timing, cues, transitions |
| AV tech | [Name] | Sound, slides, streaming |
| Host/MC | [Name] | Introductions, transitions, energy |
| Speaker liaison | [Name] | Backstage prep, mic check, timing signals |
| Chat/audience moderator | [Name] | Q&A, polls, chat management |
| Registration | [Name] | Check-in, badges, troubleshooting |
```

**GATE: Present the structure and role assignments for approval.**

---

## Phase 3: Build

### Detailed Run-of-Show

For every moment of the event:

```
---
### 9:00 AM — Welcome and Housekeeping (5 min)
**Who:** [Host name]
**Audio:** Lapel mic — channel 1
**Visuals:** Welcome slides (deck loaded on laptop A)
**Script notes:**
- Welcome attendees
- Housekeeping: bathrooms, wifi password, emergency exits
- Thank sponsors: [Sponsor A] and [Sponsor B] — show logo slides
- Introduce first speaker

**Transition to next:** "Please welcome [Speaker Name]!" → stage manager cues speaker from backstage
---

### 9:05 AM — Keynote: [Title] (45 min)
**Who:** [Speaker name]
**Audio:** Lapel mic — channel 2 (switched from channel 1)
**Visuals:** Speaker's slides (deck loaded on laptop B)
**Cues:**
- 5-min warning: [Speaker liaison] holds up "5 MIN" card from front row
- Wrap signal: [Speaker liaison] holds up "WRAP" card
**Q&A:** 10 min included in the 45 (speaker manages)
**Backup:** If speaker is late, host does 5-min audience icebreaker

**Transition to next:** Speaker exits → host takes stage → sponsor mention (30 sec) → announce break
---
```

### Transition Scripts

For every transition between sessions:

```
## Transition Template (30-60 seconds)

"Thank you, [Speaker Name] — [one-sentence recap of their key point].

[Sponsor mention if scheduled: "This next session is brought to you by [Sponsor]"]

Up next, we have [Next Speaker Name], who is going to [one-sentence preview].

[If break: "We'll take a 10-minute break. Be back at [Time]."]
[If no break: "Please welcome [Name]!"]"
```

### Contingency Plans

```
## If This Happens → Do This

**Speaker is late (5+ min):**
→ Host runs an audience Q&A or icebreaker until speaker arrives
→ If 15+ min late, move to next session and slot the late speaker later

**Tech failure (slides won't load):**
→ Speaker presents without slides (they should be prepared for this)
→ AV tech troubleshoots on backup laptop during the session

**Audio fails:**
→ Switch to backup mic immediately (always have 2 ready)
→ If all audio fails, take a 5-min "tech break" while AV resolves

**Session runs long:**
→ Speaker liaison gives "WRAP NOW" signal
→ Host takes stage at the scheduled end time regardless
→ Shorten next break by the overage amount

**Fire alarm / emergency:**
→ Host directs attendees to exits calmly
→ Stage manager coordinates with venue staff
→ Resume event when cleared, adjust schedule as needed
```

---

## Phase 4: Polish

### 1. Pre-Event Distribution

```
## Who Gets the Run-of-Show
- Stage manager: Full document
- AV tech: Full document + AV-specific notes highlighted
- Host/MC: Full document + transition scripts printed separately
- Speaker liaison: Full document + speaker-specific pages
- Speakers: Their session block only + arrival time + tech check time
- Volunteers: Simplified timeline with their specific assignments
```

### 2. Final Checks

```
## Day-Before Checklist
- [ ] Run-of-show printed for all team members
- [ ] Every speaker confirmed for their time slot
- [ ] All slides and decks loaded and tested
- [ ] Backup mic and laptop available and tested
- [ ] Timing cards printed (15 MIN, 10 MIN, 5 MIN, 2 MIN, WRAP)
- [ ] Contingency plans reviewed with the full team
- [ ] Emergency contact list distributed
- [ ] Venue walkthrough completed
```

### 3. Post-Event Notes

Add a notes column to capture real-time adjustments during the event. These become the foundation for the next event's run-of-show.

---

## Example 1: Full-Day Conference Run-of-Show (Excerpt)

```
| Time | Dur | What | Who | Cues |
|------|-----|------|-----|------|
| 8:00 | 60m | Doors + registration | Reg team | Ambient music |
| 9:00 | 5m | Welcome | MC | Welcome slides |
| 9:05 | 45m | Keynote | Sarah J. | Lapel mic, channel 2 |
| 9:50 | 5m | Sponsor mention + break intro | MC | Sponsor slide |
| 9:55 | 15m | Break | — | Timer on screen |
| 10:10 | 30m | Session A: Email Marketing | Mike R. | Room A, headset mic |
| 10:10 | 30m | Session B: SEO Basics | Lisa T. | Room B, lapel mic |
```

## Example 2: Virtual Event Run-of-Show (Excerpt)

```
| Time | Dur | What | Who | Cues |
|------|-----|------|-----|------|
| 11:55 | 5m | Speakers join backstage | Producer | Confirm audio/video |
| 12:00 | 3m | Welcome + housekeeping | Host | Share screen: welcome slide |
| 12:03 | 25m | Session 1: [Title] | [Speaker] | Spotlight speaker, enable slides |
| 12:28 | 7m | Q&A | Host + Speaker | Read curated questions from chat |
| 12:35 | 5m | Break | — | BRB slide + music |
```

---

## Anti-Patterns

- **No timing signals for speakers** — speakers will always run long without warning cards. Assign someone to signal.
- **Missing transitions** — dead air between sessions feels unprofessional. Script every transition.
- **No contingency plans** — something always goes wrong. If the plan does not cover it, the team improvises poorly.
- **Too much detail for volunteers** — give volunteers a simplified version with only their tasks. The full document overwhelms them.
- **Not distributing in advance** — the team needs the run-of-show at least 48 hours before the event to prepare.
- **Ignoring buffer time** — transitions take longer than you think. Build 5-minute buffers between sessions.

---

## Recovery

- **Event is tomorrow and no run-of-show exists:** Build a simplified version — time, what happens, who. Skip transition scripts and use verbal briefing instead.
- **Schedule changes day-of:** Update the digital version and announce changes to the team verbally. Printed copies get hand-annotated.
- **Speaker cancels last minute:** Execute the contingency — extend the previous session Q&A, do an audience activity, or move up the next speaker.
- **Team has never used a run-of-show:** Walk through it together in the pre-event briefing. Assign one person as the "timekeeper" who calls out the next item 2 minutes before each transition.
