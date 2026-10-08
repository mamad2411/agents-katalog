---
name: timezone-awareness
description: When the user wants to build or improve a sales bot's ability to respect prospect time zones for outreach. Also use when the user mentions "timezone," "local time," "send time optimization," "time-based outreach," or "international outreach."
---

# Timezone Awareness

You are an expert in building sales bots that respect prospect time zones and optimize send times. Your goal is to help developers create systems that reach prospects at the right moment, regardless of where they are in the world.

## Why Timezone Matters

### The Wrong Time Problem
```
Your bot is in EST. Prospect is in Sydney.
You send at 9am EST = 1am Sydney.

Result:
- Message buried by morning
- Lower open rates
- Appears tone-deaf
- Damages brand perception

"Why are they emailing me at 1am?"
```

### The Right Time Advantage
```
Same scenario, timezone-aware:
You send at 9am Sydney time.

Result:
- Top of inbox
- Higher open rates
- Appears professional
- Feels personalized

"They actually know what time it is here."
```

## Timezone Detection

### From Phone Number
```
Phone number: +61 2 9999 9999
+61 = Australia
02 = Sydney/NSW area code
Timezone: Australia/Sydney (AEST/AEDT)

Phone number: +1 415 555 1234
+1 = USA/Canada
415 = San Francisco area code
Timezone: America/Los_Angeles (PST/PDT)

Mapping:
- Extract country code
- For large countries (US, CA, AU), use area code
- Map to IANA timezone identifier
```

### From Email Domain
```
Email: john@company.com.au
TLD: .com.au = Australia
Default: Australia/Sydney

Email: contact@company.de
TLD: .de = Germany
Default: Europe/Berlin

Email: john@company.com
→ Need additional signals (IP, phone, address)
```

### From Company Data
```
Company headquarters: San Francisco, CA
→ America/Los_Angeles

Company website shows UK address
→ Europe/London

LinkedIn shows "Based in Singapore"
→ Asia/Singapore

Priority:
1. Explicit timezone in data
2. Phone area code
3. Company headquarters
4. Email TLD
5. IP geolocation (least reliable)
```

### From Explicit Input
```
Always allow prospect to state preference:

"When's a good time to chat?"
"Mornings work best, I'm in Chicago."
→ Parse and store: America/Chicago, morning preference

Forms:
[Select your timezone ▼]
→ Store as provided
```

## Optimal Send Windows

### Universal Best Times
```
General guidelines (in prospect's local time):

Email:
- Best: Tuesday-Thursday, 9-11am, 2-4pm
- Good: Monday 10am+, Friday before 2pm
- Avoid: Monday before 10am, Friday after 2pm
- Never: Saturday-Sunday (most industries)

SMS:
- Best: Tuesday-Thursday, 10am-12pm, 2-5pm
- Avoid: Before 9am, after 8pm
- Never: Before 8am, after 9pm (compliance)

Phone:
- Best: Tuesday-Thursday, 10-11:30am, 2-4pm
- Good: Right after lunch (1-2pm)
- Avoid: Monday morning, Friday afternoon
```

### Industry Adjustments
```
B2B Enterprise:
- Email: 8-10am (catch before meetings)
- Calls: 7:30-8:30am (executives available early)

Retail/E-commerce:
- Avoid holiday seasons
- Weekend outreach may work

Healthcare:
- Early morning or after 6pm (practitioners)
- Avoid clinic hours

Startups/Tech:
- Later mornings (10am+)
- Avoid very early (culture tends late)

Finance:
- Very early (6-8am) can work
- Avoid month/quarter end
```

### Personal Patterns
```
Learn individual preferences:

Track:
- When do they open emails?
- When do they respond?
- When are calls answered?

Adapt:
- Opens emails at 7am? Send at 6:45am.
- Responds at night? Send EOD.
- Answers calls at lunch? Call at 12:30.

"Send when THEY engage, not when you assume."
```

## Implementation

### Storing Timezone Data
```json
{
  "prospect_id": "12345",
  "timezone": {
    "iana": "America/New_York",
    "offset_hours": -5,
    "observes_dst": true,
    "current_offset": -5,
    "detection_method": "phone_area_code",
    "confidence": "high"
  },
  "preferences": {
    "preferred_time": "morning",
    "avoid_days": ["Friday"],
    "stated_by_prospect": true
  },
  "engagement_patterns": {
    "typical_open_hour": 9,
    "typical_response_hour": 14,
    "most_active_day": "Tuesday"
  }
}
```

### Send Time Calculation
```python
def calculate_send_time(prospect, message_type):
    tz = get_prospect_timezone(prospect)

    # Get optimal window for message type
    if message_type == "email":
        windows = [(9, 11), (14, 16)]  # 9-11am, 2-4pm
    elif message_type == "sms":
        windows = [(10, 12), (14, 17)]  # 10am-12pm, 2-5pm
    else:
        windows = [(10, 11.5), (14, 16)]  # Phone

    # Apply individual patterns if available
    if prospect.engagement_patterns:
        preferred_hour = prospect.engagement_patterns.typical_open_hour
        windows = [(preferred_hour, preferred_hour + 1)] + windows

    # Find next available window
    now_local = now_in_timezone(tz)

    for window_start, window_end in windows:
        send_time = next_occurrence(now_local, window_start)
        if is_valid_day(send_time, message_type):
            return send_time

    # Default: next business day, first window
    return next_business_day(now_local, windows[0][0])
```

### Handling Edge Cases
```python
def validate_send_time(send_time, prospect, message_type):
    local_time = to_local(send_time, prospect.timezone)

    # Hard limits (legal/compliance)
    if message_type == "sms":
        if local_time.hour < 8 or local_time.hour >= 21:
            return defer_to_next_valid_time(local_time)

    # Soft limits (best practice)
    if local_time.hour < 7 or local_time.hour >= 20:
        return defer_to_next_valid_time(local_time)

    # Weekend handling
    if local_time.weekday() >= 5:  # Saturday or Sunday
        if not prospect.industry_allows_weekend:
            return defer_to_monday(local_time)

    # Holiday handling
    if is_holiday(local_time.date(), prospect.country):
        return defer_to_next_business_day(local_time)

    return send_time
```

## Multi-Timezone Campaigns

### Batch Scheduling
```
Campaign to 1000 prospects across 10 timezones:

Wrong approach:
→ Send all at once at 9am your time
→ Some get it at 6am, others at midnight

Right approach:
→ Group by timezone
→ Schedule each group for 9am local
→ Sends roll out over 24 hours

Implementation:
1. Group prospects by timezone
2. Calculate send time per group
3. Schedule batches
4. Stagger to avoid delivery issues
```

### Real-Time Messaging
```
For synchronous channels (chat, SMS responses):

If prospect messages at 2am your time:
→ Is it business hours for them?
→ Yes: Respond (bot or human handoff)
→ No: They're night owl, respond anyway

For scheduled messages:
→ Always use their timezone
→ Queue until appropriate window
```

### Global Team Coordination
```
Sales team across timezones:

Prospect in Tokyo, Rep in New York:
→ Bot handles initial outreach at Tokyo optimal time
→ Bot manages async conversation
→ Schedules call for overlap window
→ Hands off to rep with context

Finding overlap:
- Tokyo: 9am-6pm JST
- New York: 9am-6pm EST
- Overlap: 10pm-12am JST = 8-10am EST
→ Schedule calls in overlap window
```

## Daylight Saving Time

### DST Handling
```
Critical: Use IANA timezone IDs, not offsets.

Wrong: Store "UTC-5"
→ Half the year it's UTC-4 (DST)

Right: Store "America/New_York"
→ System handles DST automatically

DST transition handling:
- Check if DST change is upcoming
- Recalculate scheduled sends
- Avoid scheduling exactly at transition hour
```

### DST-Affected Regions
```
Observes DST:
- USA (most), Canada (most)
- Europe
- Australia (some states)
- New Zealand
- Parts of South America

Does NOT observe DST:
- Most of Asia
- Most of Africa
- Arizona, Hawaii (USA)
- Queensland (Australia)

Always check current rules—they change.
```

## Compliance Considerations

### TCPA (USA)
```
SMS/Voice calls:
- Not before 8am local time
- Not after 9pm local time
- Applies to recipient's timezone
- Document timezone determination

Penalties: $500-$1500 per violation
```

### ACMA (Australia)
```
Telemarketing:
- Weekdays: 9am-8pm local
- Saturdays: 9am-5pm local
- Sundays/holidays: Prohibited

SMS similar restrictions apply.
```

### GDPR (Europe)
```
No specific time restrictions, but:
- Consent still required
- Reasonable expectations apply
- 3am emails look suspicious
- Best practice: 8am-8pm local
```

### General Best Practice
```
Regardless of legal requirements:

Safe window:
- 9am-6pm local time
- Monday-Friday
- Avoid local holidays

Extended window (if needed):
- 8am-8pm local time
- Include Saturday cautiously

Never:
- Before 8am local
- After 9pm local
- On local major holidays
```

## User Experience

### Communicating Timezone Awareness
```
Show the prospect you know their timezone:

"Good morning from Sydney!"
(When it's morning there)

"I know it's late in London, so no rush—
whenever you have a moment."
(When sending EOD their time)

"Happy to chat—I'm flexible since I know
we're 12 hours apart. What works for you?"
(Acknowledging the gap)
```

### Letting Prospects Choose
```
Always provide escape valve:

"I'll follow up Thursday at 10am your time.
If that doesn't work, let me know what's better."

Calendar links:
→ Auto-detect timezone
→ Show times in their local zone
→ Let them pick

Preference capture:
"For future reference, is morning or afternoon
better for you?"
```

## Testing & Monitoring

### Timezone Testing
```
Test cases:
- Prospect in your timezone (same day)
- Prospect 12 hours ahead (different day)
- Prospect in DST transition
- Prospect in non-DST region
- Unknown timezone prospect

Verify:
- Send time correct in all cases
- No messages outside safe window
- Holiday handling works
- DST transitions handled
```

### Monitoring Metrics
```
Track by timezone:
- Open rates
- Response rates
- Opt-out rates
- Spam complaints

Look for:
- Timezone with poor metrics (wrong detection?)
- Patterns by send hour
- Weekend vs weekday performance

Optimize:
- Adjust send windows per timezone
- Identify timezone-specific preferences
- Fix detection issues
```

### Error Handling
```
When timezone unknown:

Default strategy:
1. Use company headquarters timezone
2. Or: Assume business hours in most likely region
3. Send at safe middle time (2pm UTC = safe for Americas/Europe)

Flag for enrichment:
- Mark "timezone_confidence: low"
- Attempt to enrich from other sources
- Watch engagement patterns for hints
```

