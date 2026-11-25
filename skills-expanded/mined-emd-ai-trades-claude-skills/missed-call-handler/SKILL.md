---
name: missed-call-handler
description: Use this skill when you've missed a call from a potential or existing customer and need to respond immediately. Triggers on phrases like "missed a call from", "just saw a missed call", "someone called and I couldn't answer", or when you paste a phone number with no context. Generates an immediate SMS response and a callback script. Speed is everything — use within 5 minutes of seeing the missed call.
---

# Missed Call Handler

## Pre-configured business data

This skill is configured for **{{OWNER_NAME}}** at **{{BUSINESS_NAME}}**.
- Trade: {{PRIMARY_SERVICES}}
- Emergency call-outs: {{EMERGENCY_CALLOUTS}}
- Tone: Write all outputs in a {{TONE_INSTRUCTION}} style.

**Important:** Emergency call-outs are **{{EMERGENCY_CALLOUTS}}** for this business. If emergency call-outs are "no", respond to after-hours calls by setting expectations about next-morning availability only — do not offer emergency service.

**The rule:** A homeowner who calls three companies books with whoever responds first. This skill makes sure that's you — even when you couldn't pick up.

Respond within 5 minutes of a missed call and you recover 80%+ of those leads. Wait an hour and most of them have already booked someone else.

## What you need to tell me

- **The number or name** (if you know who it is)
- **Time of the missed call** (morning, afternoon, evening — affects tone)
- **Any context** (did they leave a voicemail? Did you recognise the number? Existing customer?)

If you have zero context — just a missed call from an unknown number — that's fine. I'll produce a generic but personalised-sounding recovery message.

## What I'll produce

### 1. Immediate SMS (send within 5 minutes)

For unknown caller:
> "Hi, this is {{OWNER_NAME}} from {{BUSINESS_NAME}}. Sorry I missed your call just now — I was on a job. What can I help you with? Happy to call you back in [X] minutes or answer any questions over text."

For known customer:
> "Hi [Name], sorry I missed your call — just finishing up a job. Is everything okay with the [previous job type]? Call me back anytime or text me here. — {{OWNER_NAME}}, {{BUSINESS_NAME}}"

For after-hours missed call:
> "Hi, {{OWNER_NAME}} from {{BUSINESS_NAME}} here. Saw your missed call this evening — sorry I missed you! I'm available from 8am tomorrow but happy to text now if it's urgent. What can I help with?"

### 2. Callback Script (30 seconds, for when you call back)

```
When they pick up:
"Hi, is this [name if known / otherwise:] the person who called {{BUSINESS_NAME}} earlier?
This is {{OWNER_NAME}} — really sorry I missed your call, I was on a job.
How can I help you?"

Then: LISTEN. Don't pitch. Let them tell you the problem.
After they explain:
"Got it. [Repeat the problem back in one sentence.]
I can [get someone out / give you a quote / take a look] —
what does your schedule look like?"
```

### 3. If They Don't Respond to Your SMS (24 hours later)

> "Hi again — {{OWNER_NAME}} from {{BUSINESS_NAME}}. Just checking in on my message yesterday. If you've sorted the [issue/job] already, no worries at all. If you still need a hand, I'm available this week. — {{OWNER_NAME}}"

After this second message: move on. You've made two attempts. That's professional.

## After-hours missed calls — special handling

Calls between 6pm–8am often signal urgency (broken AC in a heatwave, burst pipe, no heat in winter). For these:

**Immediate response:**
> "Hi, {{BUSINESS_NAME}} here. Saw your call — is this an emergency? Text me what's going on and I'll get back to you right away. We handle after-hours calls."

If they confirm it's urgent, produce a callback script specific to emergency call-outs.

## Track your recovery rate

Keep a note of missed calls you respond to via this skill and whether they converted to a booked job. Most trades businesses who do this discover they were losing 20–40% of their inbound leads to unanswered calls. This skill closes most of that gap.
