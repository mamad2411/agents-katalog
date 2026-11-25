---
name: channel-fallback-logic
description: When the user wants to build or improve a sales bot's ability to try alternative channels when one fails. Also use when the user mentions "channel fallback," "channel switching," "multi-channel retry," "delivery failure handling," or "channel redundancy."
---

# Channel Fallback Logic

You are an expert in building sales bots that intelligently switch channels when one fails. Your goal is to help developers create systems that maximize reach by falling back to alternative channels when primary channels don't work.

## Why Fallback Matters

### The Single-Channel Problem
```
Email-only outreach:
- Email bounces (bad address)
- Email goes to spam
- Prospect ignores email
- No other way to reach

Result: Lost opportunity
```

### With Channel Fallback
```
Smart multi-channel:
- Email bounces → Try SMS
- SMS not delivered → Try phone
- Phone no answer → Try LinkedIn

Result: Multiple paths to prospect
```

## Failure Detection

### Email Failures
```
Hard failures (don't retry):
- Hard bounce (invalid address)
- Spam complaint
- Unsubscribe
- "Address not found" error

Soft failures (may retry):
- Soft bounce (mailbox full)
- Temporary server error
- Rate limiting

Engagement failures (try other channel):
- Multiple sends, no opens
- Opens but no response (3+)
- Reply-to bounces
```

### SMS Failures
```
Hard failures:
- Invalid number
- Landline (can't SMS)
- Carrier block
- Opt-out recorded

Soft failures:
- Temporary delivery failure
- Carrier congestion
- Rate limiting

Engagement failures:
- Delivered but no response (3+)
- Read receipts but no reply
```

### Phone Failures
```
Hard failures:
- Number disconnected
- Wrong number
- "Do not call" list

Soft failures:
- Voicemail (consider success)
- Busy signal
- No answer

Engagement failures:
- Multiple VM, no callback
- Always goes to VM
- Repeatedly asks to call back but doesn't
```

## Fallback Logic

### Basic Fallback Rules
```python
FALLBACK_RULES = {
    "email_hard_bounce": {
        "fallback_to": ["sms", "phone", "linkedin"],
        "delay": timedelta(0),  # Immediate
        "message": "email_failed_sms_version"
    },
    "email_no_engagement": {
        "fallback_to": ["linkedin"],
        "delay": timedelta(days=3),
        "condition": "after_3_unopened_emails"
    },
    "sms_undeliverable": {
        "fallback_to": ["email", "phone"],
        "delay": timedelta(hours=4),
        "message": "sms_failed_email_version"
    },
    "phone_disconnected": {
        "fallback_to": ["email", "linkedin"],
        "delay": timedelta(0),
        "message": "phone_failed_email_version"
    }
}
```

### Intelligent Channel Selection
```python
def select_fallback_channel(prospect, failed_channel, failure_type):
    # Get available channels for this prospect
    available = get_available_channels(prospect)

    # Remove failed channel
    available.remove(failed_channel)

    if not available:
        return None

    # Prioritize by prospect preferences
    if prospect.preferred_channel in available:
        return prospect.preferred_channel

    # Prioritize by success probability
    channel_scores = {}
    for channel in available:
        score = calculate_channel_score(prospect, channel)
        channel_scores[channel] = score

    # Return highest scoring available channel
    return max(channel_scores, key=channel_scores.get)

def calculate_channel_score(prospect, channel):
    score = 50  # Baseline

    # Historical engagement
    if channel in prospect.engaged_channels:
        score += 30

    # Channel-specific factors
    if channel == "sms" and prospect.mobile_verified:
        score += 20
    if channel == "linkedin" and prospect.linkedin_active:
        score += 15
    if channel == "phone" and prospect.answered_before:
        score += 25

    return score
```

## Fallback Sequences

### Email → SMS → Phone
```
Day 1: Email #1
Day 3: Email #2 (if no open on #1)
Day 5: Email #3 (if no open on #1 or #2)

After Email #3 with no engagement:
→ Switch to SMS

Day 6: SMS #1
"Hi [Name], I've sent a few emails about [topic].
Not sure if they're getting through—is this a
better way to reach you?"

Day 9: SMS #2 (if no response)

After SMS #2 with no response:
→ Switch to Phone

Day 11: Phone attempt #1
Day 14: Phone attempt #2
```

### Immediate Hard Failure Fallback
```
Email sent → Hard bounce immediately

Fallback response (same day):
SMS: "Hi [Name], email bounced. Trying here
instead. Wanted to reach you about [topic].
Is this the right number?"

If SMS also fails:
LinkedIn: "[Name], having trouble reaching you
via email/text. Would love to connect here
about [topic]."
```

### Engagement-Based Fallback
```
Email opened 3x but no response:

Don't retry email—they're seeing but not
responding.

Switch approach:
LinkedIn: "Saw you've been checking out my
emails—figured I'd try a different channel.
[Shorter, different angle pitch]"

Or SMS:
"Hi [Name], emails might be getting lost.
Quick question: [single question]?"
```

## Channel-Specific Considerations

### Email Fallback Considerations
```
When falling back TO email:

- Use different subject line
- Acknowledge channel switch
- Shorter format (they were avoiding long emails)
- Different angle on pitch

Example:
"Hi [Name], tried reaching you on [other channel].
Thought email might be better. Quick question:
[single question]?"
```

### SMS Fallback Considerations
```
When falling back TO SMS:

- Much shorter message
- Direct question format
- Easy response options
- Acknowledge it's different channel

Example:
"Hi [Name], this is [Your name] from [Company].
Email not getting through—is this better?
Happy to chat if [topic] is relevant."
```

### Phone Fallback Considerations
```
When falling back TO phone:

- Consider time zone
- Have voicemail script ready
- Reference other attempts briefly
- Clear reason for call

VM Script:
"Hi [Name], this is [Your name] from [Company].
I've been trying to reach you about [topic]—
wanted to try calling since email didn't connect.
Feel free to call back at [number] or just
reply to my email. Talk soon."
```

### LinkedIn Fallback Considerations
```
When falling back TO LinkedIn:

- Check if they're active on LinkedIn
- Keep message professional
- Don't sound desperate about other channels
- New value proposition

Example:
"Hi [Name], reaching out here as LinkedIn seems
to be where you're active. [Brief pitch].
Worth a quick conversation?"
```

## Fallback Messaging

### Acknowledging Channel Switch
```
Transparent approach:

"Trying a different channel—not sure if my
emails are getting through."

"Wanted to reach you another way since I
haven't heard back via email."

"Email not the best way? Happy to connect
here instead."

Don't pretend the other attempts didn't happen.
```

### Not Acknowledging (Fresh Start)
```
Sometimes better to start fresh:

"Hi [Name], [New pitch angle completely
different from email sequence]"

When to use:
- Email sequence was very different tone
- Want to test new message
- Been a long time since email attempts
```

## Implementation

### Fallback State Machine
```python
class ChannelFallback:
    def __init__(self, prospect_id):
        self.prospect_id = prospect_id
        self.attempts = {}
        self.current_channel = None

    def record_attempt(self, channel, result):
        if channel not in self.attempts:
            self.attempts[channel] = []
        self.attempts[channel].append({
            "timestamp": datetime.now(),
            "result": result
        })

    def should_fallback(self, channel):
        if channel not in self.attempts:
            return False

        attempts = self.attempts[channel]

        # Hard failure? Immediate fallback
        if attempts[-1]["result"] in ["hard_bounce", "invalid", "blocked"]:
            return True

        # Soft failure pattern? Count
        soft_failures = [a for a in attempts if a["result"] in ["no_response", "no_open"]]
        if len(soft_failures) >= 3:
            return True

        return False

    def get_next_channel(self):
        prospect = get_prospect(self.prospect_id)

        for channel in ["email", "sms", "phone", "linkedin"]:
            if channel == self.current_channel:
                continue
            if channel not in self.attempts or not self.should_exhaust(channel):
                if is_channel_available(prospect, channel):
                    return channel

        return None  # All channels exhausted
```

### Fallback Event Handling
```python
def handle_channel_event(event):
    fallback = ChannelFallback(event.prospect_id)

    # Record the attempt
    fallback.record_attempt(event.channel, event.result)

    # Check if we should fallback
    if fallback.should_fallback(event.channel):
        next_channel = fallback.get_next_channel()

        if next_channel:
            # Schedule fallback message
            schedule_fallback(
                prospect_id=event.prospect_id,
                channel=next_channel,
                delay=get_fallback_delay(event.result),
                message_type=get_fallback_message_type(event.channel, next_channel)
            )
        else:
            # All channels exhausted
            mark_prospect_unreachable(event.prospect_id)
```

## Metrics

### Fallback Effectiveness
```
Track:
- Fallback trigger rate by channel
- Fallback success rate (engagement after switch)
- Conversion rate post-fallback
- Optimal fallback paths

Optimize:
- Which fallback sequences work best?
- How long to wait before fallback?
- Which messages work for fallback?
```

### Channel Reliability
```
Track per channel:
- Delivery rate
- Engagement rate
- Failure reasons
- Time to failure detection

Use to improve channel selection.
```

## Edge Cases

### All Channels Failed
```
When every channel has failed:

Options:
1. Mark as unreachable (temporary)
2. Add to long-term reactivation list
3. Try data enrichment (find new contact info)
4. Try different contact at company

"All contact methods exhausted. Adding to
quarterly reactivation list."
```

### Prospect Uses Different Channels
```
Prospect responds on unexpected channel:

Email sequence running, prospect responds via LinkedIn:

→ Pause email sequence
→ Continue on LinkedIn
→ Don't multi-channel simultaneously
```

### Channel Preferences Stated
```
Prospect says "Email me" or "Text is better":

→ Override fallback logic
→ Honor their preference
→ Only fallback if that channel hard fails
```

