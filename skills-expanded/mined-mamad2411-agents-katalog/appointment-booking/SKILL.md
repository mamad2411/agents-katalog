---
name: appointment-booking
description: When the user wants to build or improve a sales bot's ability to integrate with calendars and schedule meetings autonomously. Also use when the user mentions "booking meetings," "calendar integration," "scheduling calls," "appointment setting," or "automated booking."
---

# Appointment Booking for Sales Bots

You are an expert in building automated appointment booking systems for sales bots. Your goal is to help design systems that integrate with calendars to schedule meetings autonomously and efficiently.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What type of meetings are you booking?
   - Whose calendars are involved?
   - What channels initiate booking?

2. **Current State**
   - How are meetings booked today?
   - What calendar systems do you use?
   - What friction exists in the booking process?

3. **Goals**
   - What would automated booking help you achieve?
   - What does a successful booking flow look like?

---

## Core Principles

### 1. Reduce Friction to Zero
- Every click is a drop-off risk
- Minimize steps to booked
- Make it effortless

### 2. Respect Everyone's Time
- Don't offer unavailable slots
- Account for prep time
- Appropriate meeting lengths

### 3. Confirm and Remind
- Clear confirmation
- Timely reminders
- Easy rescheduling

### 4. Graceful Failures
- Always have fallback
- Manual option when automation fails
- Don't lose the lead

---

## Booking Flow Design

### Basic Flow

```
Qualification Complete
        ↓
"Would you like to schedule a call?"
        ↓
[Yes] → Show available times
        ↓
Select time → Confirm details → Book meeting
        ↓
Send confirmation → Add to calendars → Set reminders
```

### Conversation-Based Booking

**Step 1: Transition to booking**
"Based on what you've shared, it sounds like a quick call would help. Would you like to schedule 15 minutes with our team?"

**Step 2: Time preference**
"Great! Do you prefer morning or afternoon? And what time zone are you in?"

**Step 3: Offer options**
"I have these times available:
• Tuesday 10am
• Wednesday 2pm
• Thursday 11am
Which works best?"

**Step 4: Confirm**
"Perfect! I've got you down for Wednesday at 2pm ET with [Rep Name]. You'll get a calendar invite shortly. Looking forward to it!"

### Widget/Link-Based Booking

**When to use:**
- High volume
- Self-service preference
- Detailed availability needed

**Integration:**
"Here's a link to find a time that works: [Calendly/HubSpot/etc. link]"

---

## Calendar Integration

### Common Integrations

**Calendar platforms:**
- Google Calendar
- Microsoft Outlook/365
- Apple Calendar

**Scheduling tools:**
- Calendly
- HubSpot Meetings
- Chili Piper
- Cal.com

### API Integration Basics

**What to implement:**
- Availability checking
- Event creation
- Event updates
- Reminder scheduling

**Example flow:**
```
function getAvailableSlots(rep_id, date_range, duration) {
  // Get rep's calendar
  calendar = getCalendar(rep_id)

  // Get busy times
  busy = calendar.getBusyTimes(date_range)

  // Get working hours
  working_hours = rep.working_hours

  // Calculate available slots
  available = calculateAvailability(
    date_range,
    working_hours,
    busy,
    duration
  )

  // Apply buffer rules
  available = applyBuffers(available, rep.buffer_settings)

  return available
}
```

### Availability Rules

**Working hours:**
- Define per rep
- Account for time zones
- Exclude blocked time

**Buffer time:**
- Between meetings
- Before first meeting
- After last meeting

**Meeting limits:**
- Max per day
- Max per week
- Consecutive meeting limits

---

## Time Zone Handling

### Detection

**Methods:**
- Ask explicitly
- Infer from phone number
- Detect from browser
- Look up company location

**Best practice:**
Always confirm: "Just to confirm, you're in [detected timezone]?"

### Display

**Show times in their zone:**
"Here are times in Pacific Time (PT):
• Tuesday 10:00 AM PT
• Wednesday 2:00 PM PT"

**Include conversion if helpful:**
"That's 1:00 PM ET / 10:00 AM PT"

### Storage

**Store in UTC:**
- All times stored in UTC
- Convert for display
- Handle DST correctly

---

## Meeting Types

### Discovery Call

**Duration:** 15-30 minutes
**Purpose:** Initial qualification, needs discussion
**Attendees:** SDR + Prospect

**Booking prompt:**
"I'd love to learn more about your situation. Can we schedule a 15-minute call?"

### Demo

**Duration:** 30-60 minutes
**Purpose:** Product demonstration
**Attendees:** AE + Prospect (+ technical, if needed)

**Booking prompt:**
"Ready to see how this works? Let's schedule a 30-minute demo."

### Technical Discussion

**Duration:** 30-60 minutes
**Purpose:** Technical deep-dive
**Attendees:** SE + Technical buyer

**Booking prompt:**
"Let me connect you with our solutions engineer for a technical discussion."

### Executive Meeting

**Duration:** 30-45 minutes
**Purpose:** Strategic discussion
**Attendees:** Executive + Executive

**Booking prompt:**
"Would it be valuable to connect [your exec] with [their exec] to discuss [strategic topic]?"

---

## Lead Routing for Booking

### Round Robin

**How it works:**
- Distribute evenly among reps
- Rotate through available reps
- Skip unavailable reps

```
function getNextRep(team_id, meeting_type) {
  team = getTeam(team_id)
  reps = team.reps.filter(r => r.handles(meeting_type))

  // Get rep with least recent booking
  reps.sort(by_last_booking_date)

  for (rep in reps) {
    if (rep.hasAvailability()) {
      return rep
    }
  }

  return null // No availability, fallback
}
```

### Territory-Based

**Route by:**
- Geography
- Company size
- Industry
- Named accounts

### Skill-Based

**Route by:**
- Meeting type
- Technical requirements
- Language
- Specialization

---

## Confirmation and Reminders

### Immediate Confirmation

**Include:**
- Date and time (with timezone)
- Meeting link or location
- Who they're meeting with
- Brief agenda or purpose
- How to reschedule

**Example:**
```
Subject: Confirmed: Call with [Rep] on [Date]

Hi [Name],

Your meeting is confirmed!

📅 [Day, Date] at [Time] [Timezone]
👤 Meeting with: [Rep Name], [Title]
🔗 Join link: [video link]

We'll be discussing [purpose].

Need to reschedule? Click here: [link]

See you soon!
```

### Reminder Sequence

**24 hours before:**
"Reminder: Your call with [Rep] is tomorrow at [Time]."

**1 hour before:**
"Starting in 1 hour: Your call with [Rep] at [Time]. Join here: [link]"

**At meeting time (if no-show):**
Wait 5 minutes, then: "We're ready for you! Join when you can: [link]"

---

## Handling Edge Cases

### No Availability

**Response:**
"I don't have any times that work in the next few days. Can I have [Rep] reach out to find a time that works?"

**Fallback:**
- Capture contact info
- Queue for manual outreach
- Offer callback

### Conflicting Time Zones

**Clarify:**
"Just to double-check—when you said 2pm, did you mean 2pm your time (Pacific) or 2pm Eastern?"

### Rescheduling

**Make it easy:**
"No problem! Here are some alternative times: [options]. Or let me know what works better for you."

### Cancellation

**Be gracious:**
"Understood—things come up. Would you like to reschedule for another time?"

---

## No-Show Handling

### Prevention

- Send reminders
- Make joining easy
- Confirm day before
- Send meeting link separately

### When They Don't Show

**5 minutes after:**
"Hi [Name], we're ready for our call. Having trouble joining? Here's the link: [link]"

**15 minutes after:**
"Looks like we missed each other! Want to reschedule? Here are some times: [options]"

**Follow-up email:**
"Sorry we missed you today. Let me know if you'd like to reschedule."

### Tracking No-Shows

- Record no-show rate
- By rep, by lead source, by time
- Identify patterns
- Adjust confirmation/reminder strategy

---

## Implementation Checklist

### Phase 1: Basic Booking
- [ ] Calendar integration (read availability)
- [ ] Offer time slots in conversation
- [ ] Create calendar events
- [ ] Send confirmation emails

### Phase 2: Smart Booking
- [ ] Time zone detection
- [ ] Lead routing logic
- [ ] Reminder sequences
- [ ] Rescheduling flow

### Phase 3: Optimized Booking
- [ ] No-show handling
- [ ] Multi-rep coordination
- [ ] Analytics and reporting
- [ ] A/B testing booking flows

---

## Measuring Booking Performance

### Key Metrics

**Conversion:**
- Booking rate (offered → booked)
- Show rate (booked → attended)
- Conversion to next stage

**Efficiency:**
- Time to book
- Touches to book
- Rescheduling rate

**Quality:**
- Meeting quality scores
- Follow-up actions taken
- Pipeline generated

---

## Common Mistakes

### 1. Too Many Steps
**Problem:** Long booking flow loses people
**Fix:** Minimize clicks, conversational booking

### 2. Stale Availability
**Problem:** Offered time no longer available
**Fix:** Real-time calendar sync

### 3. No Timezone Handling
**Problem:** Wrong time bookings
**Fix:** Always clarify timezone

### 4. No Reminders
**Problem:** High no-show rate
**Fix:** Automated reminder sequence

### 5. No Fallback
**Problem:** Automation fails, lead lost
**Fix:** Always have manual backup

---

## Questions to Ask

If you need more context:
1. What calendar system do you use?
2. What types of meetings do you need to book?
3. How many reps need to be routed to?
4. What's your current no-show rate?
5. What booking tools do you currently use?

---

## Related Skills

- **lead-qualification-logic**: Qualifying before booking
- **conversational-flow-management**: Booking conversation design
- **timing-optimization**: Best times to suggest
- **multi-channel-coordination**: Booking across channels
