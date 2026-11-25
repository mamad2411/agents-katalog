---
name: meeting-confirmation-reminder-logic
description: When the user wants to build or improve a sales bot's ability to confirm meetings and reduce no-shows. Also use when the user mentions "meeting confirmation," "calendar reminders," "no-show reduction," "appointment reminders," or "meeting attendance."
---

# Meeting Confirmation and Reminder Logic

You are an expert in building sales bots that reduce no-shows through smart confirmation and reminder sequences. Your goal is to help developers create systems that ensure prospects attend scheduled meetings.

## Why This Matters

### The No-Show Problem
```
Average no-show rates:
- Sales demos: 20-30%
- Discovery calls: 25-35%
- Free consultations: 30-50%

Cost of no-shows:
- Wasted rep time
- Lost pipeline momentum
- Scheduling chaos
- Opportunity cost
```

### With Smart Reminders
```
Optimized confirmation flow:
- Initial confirmation: +10% attendance
- 24-hour reminder: +15% attendance
- Same-day reminder: +10% attendance

Result: 50-70% reduction in no-shows
```

## Confirmation Sequence

### Immediate Confirmation
```
Right after booking:

"Great—you're confirmed for [Day, Date] at [Time]!

Here's what we'll cover:
• [Agenda item 1]
• [Agenda item 2]
• [Agenda item 3]

Meeting link: [link]
Calendar invite sent to: [email]

See you then!"

Why it works:
- Confirms details
- Sets expectations
- Provides access info
- Creates commitment
```

### 24-Hour Reminder
```
Day before meeting:

"Just a reminder: we're meeting tomorrow
at [Time] to discuss [topic].

Is that still good for you?

Reply 'Yes' to confirm, or let me know
if you need to reschedule."

Why it works:
- Gets active confirmation
- Catches conflicts early
- Creates psychological commitment
- Allows reschedule vs no-show
```

### Same-Day Reminder
```
2-3 hours before:

"Looking forward to our call in [X] hours!

Quick prep: [Optional—brief context or question]

Here's your meeting link: [link]

See you at [Time]!"

Why it works:
- Top of mind
- Easy access to link
- Last chance to reschedule
```

### 15-Minute Reminder
```
Just before meeting:

"We're starting in 15 minutes!
Click here to join: [link]"

Brief and action-focused.
```

## Confirmation Responses

### Confirmed Response
```
Prospect: "Yes, confirmed!"

Response:
"Great—see you tomorrow at [Time]! I'll send
a quick reminder in the morning."

Then: Proceed with normal reminder sequence.
```

### Reschedule Request
```
Prospect: "I need to reschedule"

Response:
"No problem! Here are some alternative times:
• [Option 1]
• [Option 2]
• [Option 3]

Or reply with what works better for you."

Then: Send new confirmation sequence.
```

### No Response to Confirmation
```
If no response to 24-hour reminder:

Add a follow-up 4 hours later:
"Hey [Name], just want to make sure our meeting
tomorrow at [Time] is still on your calendar.
Let me know if anything's changed!"

Still no response? Send same-day reminder as usual,
but flag for potential no-show.
```

### Cancellation Request
```
Prospect: "I need to cancel"

Response:
"Understood. Would you like to reschedule for
a better time, or should I follow up in a few
weeks when things settle down?"

Don't: Guilt them or push hard.
Do: Make it easy to reschedule.
```

## Smart Reminder Timing

### Time Zone Awareness
```
Send reminders in prospect's timezone:

24-hour reminder: 9-10am their time
Same-day reminder: 2-3 hours before
15-minute reminder: Exactly 15 min before

Never send outside business hours.
```

### Day-of-Week Adjustments
```
Monday meetings:
- Friday reminder (in case of weekend)
- Monday morning reminder

Friday meetings:
- Thursday afternoon reminder
- Friday morning reminder

Account for weekend gaps.
```

### Meeting Time Adjustments
```
Early morning meetings (before 9am):
- Previous day evening reminder
- Morning-of reminder earlier

Late afternoon meetings (after 4pm):
- Same-day morning reminder
- 2-hour before reminder

End-of-day meetings often forgotten.
```

## Multi-Channel Reminders

### Email + SMS Strategy
```
High-stakes meeting:

24 hours before: Email confirmation request
4 hours before: SMS reminder if no email reply
15 minutes before: SMS with meeting link

SMS gets immediate attention.
```

### Channel Selection Logic
```python
def select_reminder_channel(prospect, timing):
    # 24-hour reminder: Start with email
    if timing == "24_hours":
        return "email"

    # Same-day: Use SMS if available and no email response
    if timing == "same_day":
        if prospect.sms_opted_in and not confirmed_via_email:
            return "sms"
        return "email"

    # 15-minute: SMS preferred
    if timing == "15_minutes":
        if prospect.sms_opted_in:
            return "sms"
        return "email"
```

### Calendar Integration
```
Leverage calendar systems:

1. Send calendar invite immediately
2. Include meeting link in invite
3. Enable calendar reminders (15m, 1h)
4. Add reschedule link in invite

Calendar + custom reminders = best results.
```

## Value-Add Reminders

### Pre-Meeting Content
```
Include useful info in reminders:

"For our call tomorrow, I've prepared:
- Analysis of your current [situation]
- 3 options to consider
- Case study from [similar company]

Any specific questions you want me to address?"

Adds value, increases commitment.
```

### Agenda Reinforcement
```
Remind them why the meeting matters:

"Looking forward to discussing how we can
help you [achieve their goal] tomorrow.

I'll have some ideas based on what you
mentioned about [their challenge]."

Connect to their motivation.
```

### Easy Access Information
```
Remove friction:

"Quick info for our meeting:

📅 Tomorrow at 2pm PT
📞 [Click here to join]
⏱️ 30 minutes
📋 Agenda: [topic]

Questions before we meet?"

One click to join.
```

## No-Show Handling

### Immediate Follow-Up
```
If prospect doesn't join within 5 minutes:

SMS/Email:
"I'm in the meeting room—are you still able
to join? Here's the link: [link]

If something came up, no worries—just let
me know and we'll reschedule."

Wait 10 more minutes. If no response:
End meeting, send follow-up.
```

### Post No-Show Message
```
30 minutes after no-show:

"Looks like we missed each other today.
No problem—these things happen.

Would one of these times work instead?
• [Option 1]
• [Option 2]
• [Option 3]

Let me know what's better for you."

No guilt. Make rescheduling easy.
```

### Repeated No-Shows
```
Second no-show:

"We've had trouble connecting the last couple
of times. I want to make sure I'm not
wasting your time if the timing isn't right.

Should we try once more, or would you
prefer I follow up in a month or two?"

Set boundaries while respecting them.
```

## Reminder Personalization

### By Meeting Type
```
Discovery call:
"Tomorrow we'll explore your challenges with
[topic] and see if there's a fit."

Demo:
"I'll be showing you [specific features] based
on what you mentioned about [their need]."

Proposal review:
"Ready to walk through the proposal and
answer any questions on pricing and scope."

Match reminder to meeting purpose.
```

### By Prospect Engagement
```
High engagement prospect:
Brief, assumes they'll attend.

Low engagement prospect:
More persuasive, reinforces value.

Previous no-show:
Emphasizes confirmation, offers reschedule.
```

## Implementation

### Reminder State Machine
```python
class MeetingReminderFlow:
    def __init__(self, meeting):
        self.meeting = meeting
        self.state = "scheduled"
        self.confirmations = []
        self.reminders_sent = []

    def process_confirmation_response(self, response):
        if is_confirmed(response):
            self.state = "confirmed"
            self.confirmations.append({
                "at": now(),
                "response": response
            })
        elif is_reschedule_request(response):
            self.state = "reschedule_requested"
            return self.generate_reschedule_options()
        elif is_cancellation(response):
            self.state = "cancelled"
            return self.handle_cancellation()

    def get_next_reminder(self):
        time_until_meeting = self.meeting.start_time - now()

        if time_until_meeting <= timedelta(hours=24):
            if "24_hour" not in self.reminders_sent:
                return self.create_reminder("24_hour")

        if time_until_meeting <= timedelta(hours=3):
            if "same_day" not in self.reminders_sent:
                return self.create_reminder("same_day")

        if time_until_meeting <= timedelta(minutes=15):
            if "15_minute" not in self.reminders_sent:
                return self.create_reminder("15_minute")

        return None
```

### Meeting Data Model
```json
{
  "meeting_id": "12345",
  "prospect_id": "67890",
  "scheduled_time": "2024-01-20T14:00:00-08:00",
  "meeting_type": "discovery_call",
  "meeting_link": "https://...",
  "status": "confirmed",
  "reminders": {
    "24_hour": {
      "sent_at": "2024-01-19T10:00:00-08:00",
      "channel": "email",
      "confirmed": true
    },
    "same_day": {
      "sent_at": "2024-01-20T11:00:00-08:00",
      "channel": "sms"
    },
    "15_minute": {
      "scheduled_for": "2024-01-20T13:45:00-08:00"
    }
  },
  "no_show_history": 0
}
```

## Metrics

### Reminder Effectiveness
```
Track:
- Confirmation response rate
- No-show rate by reminder sequence
- Reschedule vs cancel ratio
- Channel effectiveness

Benchmarks:
- Confirmation response rate: >60%
- No-show rate: <20%
- Reschedule vs cancel: 3:1
```

### Optimization Opportunities
```
Analyze:
- Which reminder timing works best?
- Which channels get responses?
- What content increases confirmation?
- When do no-shows happen most?

Use data to refine sequence.
```

