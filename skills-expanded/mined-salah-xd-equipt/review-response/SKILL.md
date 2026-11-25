---
name: review-response
description: "Writes professional responses to positive and negative online reviews across Google, Yelp, and social platforms to build trust and reputation."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Review Response

## When to Use This Skill

Use this skill when you need to:
- Write professional responses to positive reviews to reinforce loyalty
- Craft diplomatic responses to negative reviews that protect your reputation
- Create a review response framework for consistent, timely replies
- Handle fake or unfair reviews with appropriate responses

**DO NOT** use this skill for soliciting reviews, managing review platforms, or crisis communication. This is for writing individual review responses.

---

## Core Principle

EVERY REVIEW RESPONSE IS WRITTEN FOR TWO AUDIENCES — THE REVIEWER AND EVERY FUTURE CUSTOMER WHO READS IT. YOUR RESPONSE REVEALS MORE ABOUT YOUR BUSINESS THAN THE REVIEW ITSELF.

---

## Phase 1: Review Context

Understand the review before crafting a response.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Platform** | "Where is the review? (Google, Yelp, Facebook, G2, Trustpilot, social media)" | Google |
| **Rating** | "What star rating or sentiment?" | No default |
| **Review text** | "Paste the full review text." | No default |
| **Customer known?** | "Do you know who this customer is? Any context on their experience?" | Unknown |
| **Legitimate?** | "Is this review from a real customer?" | Assumed real |
| **Business name** | "What is your business name?" | No default |

**GATE: Read the full review before drafting a response.**

---

## Phase 2: Draft Response

Write the response following platform-appropriate guidelines.

### Positive Review Response (4-5 stars)

```
## Response Template: Positive Review

Hi [Name],

[Specific acknowledgment of what they mentioned — do not be generic].

[Personal touch — reference their experience, the product they bought, or the result they got].

[Future invitation — "We look forward to..." or "Next time you visit..."].

Thank you for taking the time to share this!

[Your name], [Business Name]
```

**Rules for positive responses:**
- Respond within 48 hours
- Reference something specific from their review (proves you read it)
- Keep it to 3-5 sentences — warm but not excessive
- Do NOT ask for anything (no "tell your friends" or "come back soon")
- Use their name if provided

### Negative Review Response (1-3 stars)

```
## Response Template: Negative Review

Hi [Name],

Thank you for sharing your experience — I am sorry it did not meet your expectations.

[Acknowledge the specific issue they raised without being defensive].

[State what you are doing about it OR invite them to connect offline].

I would like to make this right. Please reach out to me directly at [email/phone] so I can help.

[Your name], [Business Name]
```

**Rules for negative responses:**
- Respond within 24 hours
- NEVER argue, blame, or get defensive in a public response
- Acknowledge the issue specifically — "We are sorry your order was late" not "We are sorry you had a bad experience"
- Move the conversation offline — provide a direct contact method
- Keep it under 5 sentences — long defensive responses look worse
- Do NOT offer compensation publicly (do it privately)

### Mixed Review Response (3 stars)

```
Hi [Name],

Thanks for the honest feedback. I am glad [positive element they mentioned] worked well for you.

Regarding [issue they raised] — that is helpful to know and something I am working to improve.

If you have any other suggestions, I would love to hear them at [contact].

[Your name], [Business Name]
```

### Fake/Unfair Review Response

```
Hi [Name],

I appreciate you taking the time to leave feedback. I was unable to find a record matching this experience in our system.

If you could reach out to me directly at [email], I would love to look into this and make it right.

[Your name], [Business Name]
```

Then flag the review for removal through the platform's dispute process.

**GATE: Present the draft response for approval before posting.**

---

## Phase 3: Polish

Refine the response and check for common pitfalls.

### Response Checklist

```
- [ ] Does the response address the specific points in the review?
- [ ] Is the tone professional and empathetic (not defensive)?
- [ ] Is it under 5 sentences? (Shorter is almost always better)
- [ ] Does it use the reviewer's name?
- [ ] Does it avoid disclosing private customer details?
- [ ] For negative reviews: is there an invitation to resolve offline?
- [ ] Would you be comfortable if this response went viral?
```

### Words to Avoid in Review Responses

- "Actually..." (sounds defensive)
- "Our policy states..." (sounds corporate and cold)
- "You should have..." (blames the customer)
- "Unfortunately..." (starts with negativity)
- "As I already explained..." (sounds dismissive)

---

## Phase 4: Review Management System

Set up an ongoing review monitoring and response process.

### Response Cadence

- **Negative reviews:** Respond within 24 hours
- **Positive reviews:** Respond within 48 hours
- **All reviews:** Check platforms every business day

### Review Tracking

```
## Review Log

| Date | Platform | Rating | Theme | Response Sent | Resolved? |
|------|----------|--------|-------|--------------|-----------|
| [Date] | [Platform] | [Stars] | [Issue/Praise] | [Date] | [Y/N] |
```

### Monthly Review Summary

1. Total reviews received this month
2. Average rating trend
3. Common themes (positive and negative)
4. Outstanding unresolved negative reviews

---

## Anti-Patterns

- **Copy-paste responses** — identical replies to every review look automated and uncaring. Personalize each one.
- **Arguing publicly** — you will never win a public argument with a reviewer. Even if you are right, you look petty.
- **Ignoring negative reviews** — silence reads as "we do not care." Always respond.
- **Over-explaining** — a paragraph of excuses makes you look worse. Acknowledge, apologize, offer to fix, done.
- **Delayed responses** — a response 3 weeks later looks like you do not monitor reviews.

---

## Recovery

- **Review contains false information:** Respond calmly, state the facts briefly, and invite offline resolution. Flag for platform removal.
- **Customer escalates after response:** Move to direct communication immediately. Do not continue the public thread.
- **User gets emotional reading negative reviews:** Write the response, wait 1 hour, then re-read before posting. Never respond in the moment.
- **Too many reviews to respond to individually:** Prioritize: all negative reviews, then positive reviews with specific detail. Skip one-word positive reviews if time is limited.
- **Competitor leaving fake reviews:** Document the pattern, report to the platform, and do NOT call it out publicly.
