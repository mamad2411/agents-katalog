---
name: review-responder
description: Use this skill when you need to respond to a Google review (positive, negative, or neutral). Triggers on phrases like "respond to this review", "write a reply to", "how should I respond to this", or when you paste a review text directly. Generates a response that sounds human, references the job, includes local keywords naturally, and is under 150 words. Do NOT generate fake or generic responses — always base the reply on what the customer actually said.
---

# Review Responder

## Pre-configured business data

This skill is configured for **{{BUSINESS_NAME}}** in **{{CITY}}**, serving {{SERVICE_AREA}}.
- Phone: {{PHONE}} (used in negative review responses for offline resolution)
- Tone: Write all outputs in a {{TONE_INSTRUCTION}} style.

Turns every Google review into a response that improves your local ranking and builds trust with the next customer reading it.

**Why this matters:** Google's algorithm counts review responses as a signal of business activity. An unanswered review — especially a negative one — actively hurts your ranking. Every response you post is indexed.

## What you need to tell me

Just paste the review. That's it. If you have additional context (what the job was, who the tech was, what went wrong), add it — but the review text alone is enough to start.

## What I'll produce

A response under 150 words that:
- Thanks the customer by name (if they gave it)
- References the specific job or service naturally
- Includes {{CITY}} naturally in the response (local SEO signal)
- Sounds like a human wrote it — not a template
- For negative reviews: acknowledges the issue, offers a path to resolution via {{PHONE}}, does NOT argue or make excuses

## Positive review example

**Customer wrote:**
> "Jake was on time, professional, and fixed our AC in under an hour. Very fairly priced. Definitely using again."

**Response:**
> Thank you so much — we really appreciate you taking the time to share this! Really glad Jake could get your AC sorted quickly, especially in this heat. That's exactly what we aim for every job in {{CITY}}. If you ever need anything down the road, we're always a call away. Thanks again for choosing {{BUSINESS_NAME}}!

---

## Neutral/mixed review example

**Customer wrote:**
> "Good work overall. Took a bit longer than expected but the job was done right."

**Response:**
> Thanks for the honest feedback, and really glad the job came out right — that's what matters most to us. You're right that this one took longer than we'd like, and we appreciate your patience. We're always working to be more accurate with our time estimates. Hope we get the chance to make it up to you on the next one. Thanks for choosing {{BUSINESS_NAME}} in {{CITY}}!

---

## Negative review example

**Customer wrote:**
> "They didn't show up for the first appointment and didn't call to cancel. Had to take a day off work for nothing."

**Response:**
> We're genuinely sorry about this — a missed appointment with no call is not acceptable, and we completely understand your frustration. This isn't the standard we hold ourselves to. If you're open to it, please reach out to us directly at {{PHONE}} so we can make this right. We'd like the chance to earn back your trust. Thank you for letting us know.

**Note:** Do not offer a discount publicly in the response — this incentivises fake negative reviews. Resolve privately.

---

## Volume tip

If you have a backlog of unanswered reviews, paste them all at once labelled 1, 2, 3 — I'll respond to all of them in one go. Start with the negative ones — those hurt most sitting unanswered.
