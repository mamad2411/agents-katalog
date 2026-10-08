---
name: response-length-calibration
description: When the user wants to build or improve a sales bot's ability to match message length to channel and prospect behavior. Also use when the user mentions "message length," "response calibration," "message sizing," "brevity," or "message formatting."
---

# Response Length Calibration

You are an expert in building sales bots that match message length to channel norms and prospect behavior. Your goal is to help developers create systems that send appropriately-sized messages based on context.

## Why Length Matters

### The Too-Long Problem
```
SMS message (400 characters):
"Hi John, I wanted to follow up on our previous
conversation about your marketing needs. We have
several solutions that could help you achieve your
goals this quarter, including our analytics suite,
automation platform, and reporting tools. Would you
be available for a call this week to discuss further?"

Prospect reaction:
- Wall of text on small screen
- Skimmed, key point missed
- Feels like spam
- Lower response rate
```

### The Right Length
```
Same message, calibrated for SMS (100 characters):
"Hi John, quick follow-up on marketing tools.
Worth a 15-min call this week?"

Prospect reaction:
- Easy to read quickly
- Clear ask
- Feels personal
- Higher response rate
```

## Channel-Specific Norms

### SMS Norms
```
Optimal: 50-160 characters (1 SMS segment)
Maximum: 320 characters (2 segments)
Never: 500+ characters

Format:
- Single clear ask
- No paragraphs
- Direct language
- Easy response

Example:
"Hi [Name], any questions after the demo?
Happy to clarify anything."
```

### Email Norms
```
Cold outreach:
- Optimal: 50-125 words
- Maximum: 200 words
- Format: 3-4 short paragraphs max

Warm follow-up:
- Optimal: 75-150 words
- Can go longer if substantive

Proposal/detailed:
- Varies by complexity
- Use bullets and formatting
- Summary up front

Subject line:
- Optimal: 30-50 characters
- Mobile preview: 30-40 visible
```

### LinkedIn Norms
```
Connection request:
- Maximum: 300 characters
- Optimal: 100-200 characters

InMail:
- Optimal: 100-200 words
- Maximum: 400 words
- Format: Brief, personal

Regular message:
- Conversational length
- Match prospect's response length
```

### Chat/Live Messaging
```
Real-time chat:
- 1-2 sentences per message
- Break long responses into multiple
- Match prospect's pace
- Don't dump walls of text

Example:
Message 1: "Good question!"
Message 2: "Here's how that works:"
Message 3: "[Explanation]"
Message 4: "Does that help?"
```

## Prospect Behavior Calibration

### Matching Prospect Length
```python
def calibrate_to_prospect(prospect, base_response):
    # Get prospect's average message length
    avg_length = calculate_avg_message_length(
        prospect.message_history
    )

    if avg_length < 50:
        # Very brief responder
        return shorten_response(base_response, target=50)
    elif avg_length < 100:
        # Brief responder
        return shorten_response(base_response, target=100)
    elif avg_length < 200:
        # Moderate responder
        return base_response  # Standard length
    else:
        # Detailed responder
        return expand_response(base_response, target=300)
```

### Engagement-Based Calibration
```
High engagement (opens, clicks, responses):
→ Can be slightly longer
→ They're reading carefully
→ More detail acceptable

Low engagement (rarely opens):
→ Shorter, punchier
→ Get to point immediately
→ Strong subject lines

No engagement:
→ Very short, pattern-breaking
→ Different approach entirely
```

### Conversation Stage Calibration
```
First touch:
- Shorter (earn attention)
- 50-100 words email
- Clear single ask

Middle of sequence:
- Moderate length
- Can add more value
- 100-150 words

Negotiation/detail:
- Longer acceptable
- Thorough answers needed
- But still concise
```

## Length Reduction Techniques

### Eliminate Filler
```
Before:
"I hope this email finds you well. I wanted
to reach out to you today because I thought
you might be interested in..."

After:
"Reaching out because [specific reason]..."

Remove:
- "I hope this finds you well"
- "I wanted to reach out"
- "I just thought I'd"
- "I'm writing to"
- "As per our conversation"
```

### Consolidate Points
```
Before:
"We offer analytics. We also have reporting.
Additionally, we provide insights. Plus,
we have dashboards."

After:
"We offer analytics, reporting, and custom
dashboards."
```

### Remove Redundancy
```
Before:
"Schedule a meeting call to discuss and
talk about potential opportunities."

After:
"Schedule a call to discuss opportunities."
```

### Strengthen CTAs
```
Before:
"If you have some time available this week
or next, and it would be convenient for you,
maybe we could potentially set up a call?"

After:
"Free for 15 minutes this week?"
```

## Implementation

### Length Checker
```python
def check_message_length(message, channel):
    length = len(message)
    word_count = len(message.split())

    limits = {
        "sms": {"char_max": 160, "warn_at": 140},
        "email": {"word_max": 200, "warn_at": 150},
        "linkedin_connect": {"char_max": 300, "warn_at": 250},
        "linkedin_inmail": {"word_max": 400, "warn_at": 300},
        "chat": {"char_max": 280, "warn_at": 200}
    }

    channel_limits = limits.get(channel, limits["email"])

    if channel in ["sms", "linkedin_connect", "chat"]:
        current = length
        max_val = channel_limits["char_max"]
        warn_val = channel_limits["warn_at"]
    else:
        current = word_count
        max_val = channel_limits["word_max"]
        warn_val = channel_limits["warn_at"]

    return {
        "current": current,
        "max": max_val,
        "warn": warn_val,
        "status": "ok" if current <= warn_val else "warning" if current <= max_val else "too_long"
    }
```

### Auto-Shorten Function
```python
def auto_shorten(message, target_length, channel):
    # Remove common filler phrases
    fillers = [
        "I hope this email finds you well",
        "I wanted to reach out",
        "I just wanted to",
        "As a follow up",
        "I thought you might be interested"
    ]
    for filler in fillers:
        message = message.replace(filler, "")

    # Remove redundant phrases
    message = remove_redundancy(message)

    # If still too long, truncate with ellipsis handling
    if len(message) > target_length:
        if channel == "sms":
            message = smart_truncate(message, target_length)
        else:
            message = condense_paragraphs(message, target_length)

    return message.strip()

def smart_truncate(message, target):
    # Find good break point
    if len(message) <= target:
        return message

    # Try to break at sentence
    truncated = message[:target]
    last_sentence = truncated.rfind('.')

    if last_sentence > target * 0.7:
        return message[:last_sentence + 1]

    # Break at word
    last_space = truncated.rfind(' ')
    return message[:last_space] + "..."
```

### Dynamic Template Selection
```python
def select_template(intent, channel, prospect):
    # Get prospect's response pattern
    brevity_preference = assess_brevity_preference(prospect)

    template_versions = {
        "brief": get_brief_template(intent),
        "standard": get_standard_template(intent),
        "detailed": get_detailed_template(intent)
    }

    # Channel constraints
    if channel == "sms":
        return template_versions["brief"]

    if channel == "chat":
        return template_versions["brief"]

    # Prospect preference
    if brevity_preference == "very_brief":
        return template_versions["brief"]
    elif brevity_preference == "detailed":
        return template_versions["detailed"]
    else:
        return template_versions["standard"]
```

## Format Optimization

### Mobile-First Formatting
```
Consider mobile reading:

- Short paragraphs (2-3 sentences max)
- Plenty of white space
- Bullets for lists
- Bold for key points
- Clear hierarchy

Don't:
- Dense paragraphs
- Walls of text
- Tiny font expectations
- Complex formatting
```

### Channel-Specific Formatting
```
Email:
- Subject line: [Key point]
- Greeting
- 1-2 short paragraphs
- Bullet points if needed
- Single clear CTA
- Signature

SMS:
- Direct opening
- One main point
- One question or CTA
- No signature (they know who you are)

LinkedIn:
- Personal opening
- Brief context
- Question to engage
- No formal signature
```

## Testing and Optimization

### A/B Test Length
```
Test:
- Same message, different lengths
- Short vs standard vs detailed
- Channel-specific variations

Measure:
- Open rate (email)
- Response rate
- Click rate
- Conversion rate

Find optimal length per:
- Channel
- Audience segment
- Message type
```

### Length Analytics
```
Track:
- Average message length sent
- Response rate by length
- Engagement by length
- Optimal length by segment

"Messages under 100 words have 23% higher
response rate for cold email."
```

## Examples by Channel

### SMS Examples
```
Cold outreach (78 chars):
"Hi [Name], [Company] might help with [problem].
Worth a quick chat?"

Follow-up (92 chars):
"Following up on [topic]. Still interested?
Happy to answer questions."

Meeting reminder (67 chars):
"Reminder: Our call is tomorrow at 2pm.
See you then!"
```

### Email Examples
```
Cold email (89 words):
Subject: Quick question about [topic]

Hi [Name],

Noticed [observation about their company].
We help companies like yours [benefit].

[One sentence about relevant result]

Worth 15 minutes to see if we can help?

[Name]

---

Follow-up (52 words):
Subject: Re: [Original subject]

Hi [Name],

Following up on my note last week. If [topic]
is a priority, happy to share how we've helped
[similar companies].

If not, no worries—just wanted to check.

[Name]
```

### LinkedIn Examples
```
Connection request (147 chars):
"Hi [Name], saw your work on [topic].
We share interest in [area]. Would love to
connect and share insights."

InMail (67 words):
Hi [Name],

Your post about [topic] resonated with me.
We work with [similar companies] on exactly
that challenge.

Not pitching—just curious if you'd be open
to exchanging ideas sometime?

[Name]
```

