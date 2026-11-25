---
name: timing-optimization
description: When the user wants to build or improve a sales bot's ability to send messages or make calls when prospects are most likely to engage. Also use when the user mentions "best time to send," "send time optimization," "engagement timing," "when to call," or "optimal contact times."
---

# Timing Optimization for Sales Bots

You are an expert in optimizing outreach timing for automated sales systems. Your goal is to help design systems that contact prospects when they're most likely to engage.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What channels are you optimizing for?
   - What's your prospect demographic?
   - What time zones do you operate across?

2. **Current State**
   - How do you currently schedule outreach?
   - What response rates are you seeing?
   - Do you have historical engagement data?

3. **Goals**
   - What would better timing help you achieve?
   - What engagement lift are you targeting?

---

## Core Principles

### 1. Timing Can Make or Break Response
- Same message, different time = different results
- Optimal windows exist
- But they vary by segment

### 2. Data Beats Assumptions
- Test, don't assume
- What works for others may not work for you
- Your prospects are unique

### 3. Individual > Segment > Global
- Personal patterns beat averages
- But use averages when no personal data
- Build toward personalization

### 4. Respect Boundaries
- Don't contact at inappropriate times
- Compliance requirements exist
- Late night ≠ "higher engagement"

---

## General Timing Benchmarks

### Email

**Generally optimal:**
- Tuesday-Thursday
- 9-11am, 2-4pm (recipient's time zone)
- Avoid Monday morning, Friday afternoon

**B2B patterns:**
- Early morning (7-9am): Executives
- Mid-morning (10am-12pm): Managers
- Afternoon (2-4pm): General

### SMS

**Generally optimal:**
- Tuesday-Thursday
- 10am-12pm, 2-5pm
- Avoid early morning, late evening

**Critical:**
- Respect TCPA/ACMA quiet hours
- Generally 8am-9pm local time only

### Phone

**Generally optimal:**
- Wednesday-Thursday
- 8-9am, 4-5pm
- Late morning and early afternoon are harder

**Connect rates:**
- Early morning: Catch before meetings
- End of day: Catch wrapping up

### Chat

**Timing = real-time:**
- Respond immediately when initiated
- Proactive chat based on behavior
- Consider page engagement time

---

## Time Zone Management

### Challenges

- Prospect TZ may be unknown
- Database TZ may be wrong
- Daylight saving complexities
- Global prospects = always "business hours" somewhere

### Solutions

**Identify time zone:**
- Phone number area code
- Company HQ location
- IP address (for web)
- Explicit data (CRM)

**Handle unknown:**
- Assume based on country
- Use safest window (overlapping business hours)
- Ask and record preference

**Multi-TZ campaigns:**
- Schedule per time zone
- Dynamic send time adjustment
- 24-hour coverage with global teams

---

## Building Timing Intelligence

### Data Collection

**Track for each contact:**
- When messages were sent
- When they were opened/clicked
- When they responded
- Device/platform used

**Aggregate patterns:**
- Best times by segment
- Best days by segment
- Seasonal variations
- Industry differences

### Individual Optimization

**Learning loop:**
1. Send at segment-optimal time
2. Track individual engagement
3. Adjust based on their pattern
4. Continue refining

**Example model:**
```
Contact: Sarah
Open history:
  - Sent 9am → Opened 9:15am
  - Sent 2pm → Opened 6pm
  - Sent 9:30am → Opened 9:45am

Pattern: Morning opener
Optimal send time: 9am
```

### Segment-Level Optimization

**Segmentation factors:**
- Industry
- Role/seniority
- Company size
- Geography
- Past engagement

**Example segments:**
- C-suite: Early morning (6-8am)
- Sales roles: Lunch and end of day
- Tech roles: Mid-morning
- East coast vs. West coast

---

## Implementation Approaches

### Approach 1: Rule-Based

**Simple rules:**
```
if (recipient_tz == "America/New_York") {
  send_at = "10:00 AM ET"
} else if (recipient_tz == "America/Los_Angeles") {
  send_at = "10:00 AM PT"
}
```

**Segment rules:**
```
if (role == "executive") {
  optimal_hours = [7, 8, 17, 18]
} else if (industry == "healthcare") {
  optimal_hours = [10, 11, 14, 15]
}
```

### Approach 2: Statistical

**Send time distribution:**
- Spread sends across optimal window
- A/B test different times
- Measure and shift distribution

**Example:**
- Week 1: 30% at 9am, 30% at 11am, 30% at 2pm
- Analyze: 11am had highest engagement
- Week 2: 50% at 10-11am, 25% at 9am, 25% at 2pm
- Continue refining

### Approach 3: ML-Based

**Predictive model:**
- Features: segment data, past engagement, day of week, time of year
- Output: Predicted optimal send time
- Continuous learning from results

**Providers:**
- SendGrid Send Time Optimization
- HubSpot Smart Send
- Custom ML models

---

## Channel-Specific Optimization

### Email Timing

**Factors:**
- When they typically open
- Inbox competition
- Subject relevance to time

**Techniques:**
- Morning send for "start of day" reads
- Pre-meeting times
- Avoid peak inbox times (9am Monday)

### SMS Timing

**Factors:**
- Much more intrusive
- Real-time expectation
- Compliance windows critical

**Techniques:**
- Trigger-based (after action)
- Appointment reminders (appropriate lead time)
- Follow-up after business hours email

### Phone Timing

**Factors:**
- Much more intrusive than SMS
- Connect rate varies dramatically
- Voicemail strategy needed

**Techniques:**
- Early morning (before meetings)
- End of day (wrapping up)
- Post-email follow-up
- Callback at their preferred time

---

## Triggered vs. Scheduled

### Triggered Timing

**Send immediately when:**
- Form submission
- Chat initiation
- Hand-raised intent
- Support request

**Speed matters:**
- Response within 5 minutes = 21x more likely to qualify
- First responder advantage
- Intent decays quickly

### Scheduled Timing

**Schedule for optimal time when:**
- Cold outreach
- Nurture sequences
- Non-urgent follow-up
- Batch campaigns

**Balance:**
- Optimal time vs. freshness
- Don't wait too long for "perfect" time
- Same day often better than next day optimal

### Hybrid Approach

**Example:**
1. Lead comes in at 11pm
2. Send immediate acknowledgment
3. Schedule substantive follow-up for next morning optimal time

---

## Respecting Boundaries

### Compliance Requirements

**TCPA (US SMS):**
- 8am-9pm local time
- Document consent
- Immediate opt-out

**ACMA (Australia):**
- 9am-8pm weekdays
- 9am-5pm Saturday
- No Sunday/public holidays

**General best practice:**
- 8am-8pm recipient local time
- Respect stated preferences
- Err on conservative side

### Personal Boundaries

**Monitor for signals:**
- "Stop contacting me"
- "This is a bad time"
- Consistent non-response

**Respect preferences:**
- "Call me after 3pm"
- "Email only"
- "Best time is Tuesday"

---

## Measuring Timing Impact

### Key Metrics

**By time sent:**
- Open rate
- Response rate
- Connect rate (phone)
- Conversion rate

**By segment:**
- Best performing times per segment
- Variance in response patterns
- Seasonal shifts

### A/B Testing

**Test structure:**
- Control: Current send time
- Variant: Proposed optimal time
- Hold out: Random time (calibration)

**Statistical significance:**
- Enough volume per cell
- Account for day-of-week effects
- Long enough window for patterns

### Continuous Optimization

**Regular review:**
- Monthly timing analysis
- Seasonal adjustments
- Segment-specific tuning

**Automation:**
- Automated time shifting based on results
- Alert when patterns change
- Machine learning optimization

---

## Questions to Ask

If you need more context:
1. What channels are you trying to optimize?
2. What time zones do your prospects span?
3. What engagement data do you have access to?
4. What are your current response/open rates?
5. What compliance requirements apply to you?

---

## Related Skills

- **multi-channel-coordination**: Timing across channels
- **re-engagement-sequencing**: Timing for cold leads
- **response-latency-management**: Real-time response speed
- **compliance-handling**: Regulatory timing requirements
