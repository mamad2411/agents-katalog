---
name: re-engagement-sequencing
description: When the user wants to build or improve a sales bot's ability to nurture cold leads back into active conversations. Also use when the user mentions "re-engaging leads," "nurture sequences," "cold lead reactivation," "win-back campaigns," or "dormant lead outreach."
---

# Re-Engagement Sequencing for Sales Bots

You are an expert in building re-engagement systems for automated sales. Your goal is to help design sequences that nurture cold leads back into active conversations effectively.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - How do leads go cold in your process?
   - How large is your cold lead pool?
   - What caused leads to disengage?

2. **Current State**
   - Do you have re-engagement efforts today?
   - What happens to leads that don't convert?
   - What's your reactivation success rate?

3. **Goals**
   - What would better re-engagement help you achieve?
   - What does a reactivated lead look like?

---

## Core Principles

### 1. Timing and Triggers Matter
- Not all cold leads are ready at the same time
- Watch for buying signals
- Right message, right moment

### 2. Value First, Always
- They went cold for a reason
- Don't just "check in"
- Give them a reason to re-engage

### 3. Respect Their Choice
- Some leads won't come back
- Don't harass
- Know when to stop

### 4. Learn from History
- What worked before?
- Why did they engage initially?
- What changed?

---

## Lead Lifecycle

### How Leads Go Cold

**No response:**
- Initial outreach ignored
- Sequence completed, no reply
- Stopped responding mid-conversation

**Timing issues:**
- Not ready to buy
- Other priorities
- Budget cycle

**Lost interest:**
- Chose competitor
- Solved problem differently
- Priority changed

**Bad experience:**
- Poor sales interaction
- Technical issues
- Unmet expectations

### Cold Lead Categories

| Category | Definition | Re-engagement Approach |
|----------|------------|------------------------|
| Unresponsive | Never responded to outreach | New angle, different channel |
| Stalled | Engaged then stopped | Address likely cause |
| Lost | Chose competitor | Monitor for dissatisfaction |
| Timing | Said "not now" | Wait and watch for triggers |
| Disqualified | Didn't meet criteria | May re-qualify over time |

---

## Re-Engagement Triggers

### Time-Based Triggers

**Standard intervals:**
- 30 days after going cold
- 60 days
- 90 days
- Quarterly thereafter

**Calendar triggers:**
- New quarter
- New year
- Budget cycles
- Renewal periods

### Signal-Based Triggers

**Engagement signals:**
- Visited website
- Opened old email
- Engaged on social
- Clicked content

**Business signals:**
- Funding announcement
- Leadership change
- Company growth
- New job title

**Intent signals:**
- Searched relevant terms
- Visited competitor
- Downloaded content
- Attended webinar

### Combination Triggers

```
TRIGGER re_engagement_sequence
WHEN:
  - lead.status = "cold"
  - lead.days_since_last_contact > 60
  AND
  - lead.visited_website_recently = true
  OR
  - lead.company.recent_funding = true
  OR
  - lead.engagement_score increased
```

---

## Re-Engagement Sequences

### The Standard Re-Engagement

**Day 1: Value-first email**
"Hey [Name], I came across [relevant content/insight] and thought of our previous conversation about [topic]. [Brief value point]. Worth revisiting?"

**Day 7: Different angle**
"[Name], just published a case study about [company like theirs]. Thought you might find it interesting: [link]"

**Day 14: Direct check-in**
"Quick question: Is [challenge you discussed] still a priority for [Company]?"

**Day 21: New trigger or breakup**
"[If new info available]: Noticed [Company] just [trigger event]..."
"[If no new info]: Closing the loop for now—let me know if things change."

### The Trigger-Based Re-Engagement

**When trigger detected:**

**Immediate (same day):**
"Hi [Name], saw the news about [trigger]. Congrats! [Relevant connection to your value]. Worth a quick chat?"

**Day 3 (if no response):**
"Following up on my note about [trigger]. Many companies in your situation find [specific challenge]. Still relevant?"

**Day 7 (if no response):**
"Last thought: Given [trigger], [company like them] saw [result] from [your solution]. Happy to share how if useful."

### The Value Drip

**For very cold leads:**

**Month 1:** Valuable content (no pitch)
**Month 2:** Different valuable content
**Month 3:** Industry insight
**Month 4:** Case study (relevant)
**Month 5:** Soft check-in
**Month 6:** Direct offer

---

## Message Templates

### Pattern Interrupts

**The "saw this, thought of you":**
"[Name], saw this article on [relevant topic] and thought of our conversation about [their challenge]. [Link]. Still dealing with that?"

**The industry insight:**
"[Name], we're seeing a trend with [industry] companies around [challenge]. Is that on your radar at [Company]?"

**The results share:**
"[Name], just helped [similar company] achieve [specific result]. Given what you shared about [their situation], thought you'd find this interesting."

### Direct Re-Engagements

**The honest check-in:**
"[Name], it's been a while since we talked about [topic]. Wanted to check: still a priority, or has the situation changed?"

**The assumption test:**
"[Name], guessing [challenge] either got solved or pushed to the back burner. Either way, [new value point]. Worth revisiting?"

**The new development:**
"[Name], since we last spoke, we've [new feature/capability/customer]. Changes the conversation around [their challenge]. Worth 10 minutes?"

### Trigger-Based Messages

**Funding:**
"Congrats on the Series [X]! As you scale, [common challenge] often comes up. Happy to share what we've seen work."

**New role:**
"Congrats on the new role at [Company]! If [relevant challenge] is on your list, I'd love to share what's worked for others in your position."

**Company growth:**
"Saw [Company] is growing fast—congrats! Companies at this stage often face [challenge]. Sound familiar?"

---

## Channel Strategy

### Email Re-Engagement

**Best for:**
- Initial re-engagement
- Content sharing
- Longer messages

**Tips:**
- New subject line (not reply to old thread)
- Short and value-focused
- Clear CTA

### SMS Re-Engagement

**Best for:**
- Quick check-ins
- Trigger responses
- After email engagement

**Tips:**
- Very short
- Conversational
- Only if previously communicated via SMS

### LinkedIn Re-Engagement

**Best for:**
- Job change triggers
- Professional content sharing
- Staying visible

**Tips:**
- Engage with their content first
- Soft DM approach
- Reference shared connection

### Phone Re-Engagement

**Best for:**
- High-value leads
- Post-trigger outreach
- After other channels fail

**Tips:**
- Have clear reason for calling
- Reference previous relationship
- Brief voicemail if no answer

---

## Segmentation for Re-Engagement

### By Cold Reason

| Reason | Approach |
|--------|----------|
| No response | New angle, different channel |
| Said "not now" | Wait for trigger, check in at interval |
| Chose competitor | Monitor, re-engage if dissatisfied |
| Budget issues | Wait for new fiscal period |
| Lost champion | Find new contact |

### By Lead Quality

**High-value cold leads:**
- More touches
- Multi-channel
- Personalized content
- Manual review

**Medium-value cold leads:**
- Standard sequence
- Automated personalization
- Periodic review

**Low-value cold leads:**
- Minimal effort
- Batch campaigns
- Marketing nurture

### By Engagement Level

**Previously highly engaged:**
- Something changed—investigate why
- Personal outreach
- Address potential issues

**Minimal previous engagement:**
- May never have been right fit
- New angle needed
- Lower investment

---

## Automation Rules

### Entry Criteria

```
lead.status changes to "cold"
AND lead.days_in_pipeline > 30
AND lead.opt_out = false
AND lead.last_sequence_completed > 14 days ago

→ Enroll in re_engagement_sequence
```

### Exit Criteria

```
lead responds → Exit, route to rep
lead opts out → Exit, mark as opted out
lead converts → Exit, mark as converted
lead disqualified → Exit, mark reason
sequence completed → Exit, move to long-term nurture
```

### Trigger Listeners

```
ON lead.website_visit
IF lead.status = "cold"
AND lead.days_since_last_contact > 30
→ Send triggered re-engagement

ON lead.company.funding_announcement
IF lead.status = "cold"
→ Send funding-triggered outreach

ON lead.contact.job_change
IF lead.status = "cold"
→ Send new role congratulations
```

---

## Measuring Re-Engagement

### Key Metrics

**Volume:**
- Cold leads in pool
- Leads in re-engagement sequences
- Re-engagement attempts per lead

**Effectiveness:**
- Re-engagement response rate
- Reactivation rate (cold → active)
- Conversion rate (reactivated → customer)

**Efficiency:**
- Touches to reactivation
- Time to reactivation
- Cost per reactivated lead

### Benchmarks

| Metric | Poor | Okay | Good |
|--------|------|------|------|
| Re-engagement response rate | <2% | 2-5% | >5% |
| Reactivation rate | <5% | 5-10% | >10% |
| Conversion (reactivated) | <10% | 10-20% | >20% |

---

## Common Mistakes

### 1. Just "Checking In"
**Problem:** No value, easy to ignore
**Fix:** Always lead with value or reason

### 2. Too Aggressive
**Problem:** Harassing cold leads
**Fix:** Reasonable frequency, respect opt-out

### 3. Same Message Every Time
**Problem:** If it didn't work before...
**Fix:** New angles, new value, new triggers

### 4. No Trigger Monitoring
**Problem:** Missing buying signals
**Fix:** Set up signal detection

### 5. Treating All Cold Leads Same
**Problem:** One-size doesn't fit all
**Fix:** Segment by reason, quality, history

---

## Questions to Ask

If you need more context:
1. How do leads go cold in your process?
2. What's the size of your cold lead pool?
3. Do you have insight into why leads went cold?
4. What trigger data do you have access to?
5. What re-engagement are you doing today?

---

## Related Skills

- **timing-optimization**: When to re-engage
- **personalization-at-scale**: Customizing re-engagement
- **multi-channel-coordination**: Cross-channel re-engagement
- **intent-detection**: Detecting buying signals
