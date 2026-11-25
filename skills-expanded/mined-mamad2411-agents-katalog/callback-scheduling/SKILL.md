---
name: callback-scheduling
description: When the user wants to build or improve a sales bot's ability to offer and confirm specific callback times when prospects say "call me later." Also use when the user mentions "scheduling callbacks," "call me back," "booking calls," "callback handling," or "follow-up scheduling."
---

# Callback Scheduling

You are an expert in building callback scheduling systems for sales bots. Your goal is to help developers create seamless experiences when prospects request to be called back.

## Detecting Callback Requests

### Explicit Requests
```
Direct:
- "Call me back tomorrow"
- "Can you call me at 2pm?"
- "I'll be free after 3"
- "Try me again next week"

With conditions:
- "Call me when you have pricing"
- "Reach out after I talk to my boss"
- "Get back to me once you have the info"
```

### Implicit Requests
```
Timing signals:
- "I'm in a meeting right now"
- "Not a good time"
- "Can't talk now"
- "I'm driving"

Interest + unavailability:
- "Sounds interesting but I'm swamped"
- "I'd like to hear more but I'm about to..."
```

## Response Framework

### Immediate Confirmation
```
Prospect: "Call me back tomorrow afternoon"

Bot: "Absolutely! I'll call you tomorrow afternoon.
Would 2pm or 3pm work better for you?"

Why this works:
- Confirms the request
- Offers specific times (easier to commit)
- Gets precise commitment
```

### Handling Vague Timing
```
Prospect: "Call me later"

❌ "Okay, I'll call you later"
❌ "When would be a good time?"

✓ "Happy to! Would later today work, or is tomorrow better?"
✓ "Of course! Are afternoons generally better for you?"
✓ "Sure thing. What time zone are you in? I'll find a time that works."
```

### Capturing Details
```
Essential information:
- Specific date
- Specific time (or window)
- Time zone
- Phone number to use
- Topic for the call

"Got it—I'll call you Thursday at 2pm Pacific.
Is [number on file] the best number, or is there a better one?"
```

## Scheduling Logic

### Availability Matching
```
Prospect preferred time + Rep availability = Scheduled call

If conflict:
"Thursday at 2pm is tough for me—could we do 2:30 instead?
Or if morning works better, I'm free at 10am."
```

### Time Zone Handling
```
Always:
1. Detect prospect's time zone (from area code, IP, explicit)
2. Confirm time zone in scheduling
3. Send confirmation in THEIR time zone
4. Convert internally for rep's calendar

"Just to confirm—that's 2pm Pacific Time, right?"
```

### Buffer Management
```
Between callbacks:
- Minimum 15-minute gap
- Account for overruns
- Consider travel time (if in-person)

Confirmation:
- Send immediately after scheduling
- Reminder 24 hours before
- Reminder 1 hour before (optional)
```

## Calendar Integration

### Creating the Event
```
Event details:
- Title: "Call with [Prospect Name] - [Company]"
- Duration: 15-30 minutes (based on context)
- Description: Context from conversation
- Attendees: Rep + prospect (if email available)
- Reminder: 15 minutes before
```

### Conflict Prevention
```
Before confirming:
1. Check rep's calendar
2. Check for double-bookings
3. Respect working hours
4. Account for existing commitments

If busy:
"I'm actually in another call at 2pm.
How about 2:30 or 3pm instead?"
```

### Two-Way Sync
```
If prospect reschedules:
- Update rep's calendar
- Update CRM
- Send confirmation

If rep reschedules:
- Notify prospect
- Offer alternatives
- Apologize appropriately
```

## Confirmation Flow

### Immediate Confirmation
```
SMS/Email immediately after scheduling:

"Confirmed: Call scheduled for Thursday, Jan 18 at 2:00 PM Pacific.

I'll call you at [phone number].

If you need to reschedule, just reply to this message.

Looking forward to connecting!
- [Rep Name]"
```

### Reminder Sequence
```
24 hours before:
"Quick reminder: We're scheduled to talk tomorrow at 2pm Pacific.
Looking forward to it! Reply if anything's changed."

1 hour before (optional):
"Talk in an hour! I'll call you at [number] at 2pm."

If no answer at scheduled time:
"Hey [Name], I just tried you for our 2pm call.
Let me know a better time—or I can try again in 15 min?"
```

## Handling Complications

### Prospect Doesn't Commit
```
Prospect: "Yeah, sometime next week"

Bot: "Works for me! Tuesday, Wednesday, or Thursday—
which is usually less hectic for you?"

[Narrow down iteratively]

Prospect: "Probably Wednesday"
Bot: "Morning or afternoon on Wednesday?"

Prospect: "Afternoon"
Bot: "How about 2pm? That way you're past lunch."

Prospect: "Sure"
Bot: "Perfect—Wednesday at 2pm it is. I'll send a confirmation."
```

### Conditional Callbacks
```
Prospect: "Call me after you get the pricing approved"

Bot: "Understood—I'll get that approval and reach back out.
Usually takes 1-2 business days. If I can get it done sooner,
would tomorrow afternoon work if I have the answer?"

Track:
- Condition: Pricing approval needed
- Tentative time: Tomorrow afternoon
- Status: Pending internal action
```

### Reschedule Requests
```
Prospect: "Actually, can we move it to Friday?"

Bot: "No problem at all. Same time, 2pm, on Friday?
Or would a different time work better?"

Update:
- Cancel original
- Create new event
- Send updated confirmation
- Note reschedule in CRM
```

### No-Shows
```
At scheduled time, no answer:

Attempt 1: Call at scheduled time
Wait 2-3 minutes
Attempt 2: Try again

If still no answer:
"Hi [Name], I tried you at 2pm as we scheduled.
No worries if something came up—would you like to
reschedule for later today or another time this week?"

Follow-up next day if no response:
"Following up on our missed call yesterday.
Happy to find a new time that works better—
just let me know."
```

## CRM Documentation

### Callback Record
```
Log in CRM:
- Scheduled date/time
- How it was scheduled (conversation context)
- Purpose of callback
- Prospect's preferred topics
- Any prep needed

Example note:
"Callback scheduled for 1/18 2pm PT.
Prospect interested in enterprise pricing.
Mentioned concerns about implementation timeline.
Wants to discuss integration with their current CRM."
```

### Status Tracking
```
Callback statuses:
- SCHEDULED: Confirmed, on calendar
- REMINDED: Reminder sent
- COMPLETED: Call happened
- NO_SHOW: Prospect didn't answer
- RESCHEDULED: Moved to new time
- CANCELLED: Prospect cancelled
```

## Optimization

### Best Practices
```
Scheduling callbacks:
- Offer 2-3 specific times
- Same week when possible
- Respect their stated preferences
- Confirm all details
- Send written confirmation

Timing:
- Schedule within 48-72 hours if possible
- Distant callbacks (1+ week) have higher no-show
- Morning calls have higher show rates
```

### Metrics to Track
```
- Show rate by time of day
- Show rate by day of week
- Show rate by lead time (days until call)
- Reschedule rate
- Conversion from callback to opportunity
```
