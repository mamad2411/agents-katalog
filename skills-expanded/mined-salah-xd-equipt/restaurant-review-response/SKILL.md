---
name: restaurant-review-response
description: "Writes professional restaurant review responses for positive, negative, and mixed reviews across platforms. Use when managing online reputation for a food business."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Restaurant Review Response

## When to Use This Skill

Use this skill when you need to:
- Write professional responses to Google, Yelp, or TripAdvisor reviews
- Handle negative reviews with grace and damage control
- Thank positive reviewers in a way that encourages return visits
- Create response templates for common review types

**DO NOT** use this skill for review solicitation strategies, reputation marketing campaigns, or social media comment management. This is for review platform responses only.

---

## Core Principle

EVERY REVIEW RESPONSE IS A PUBLIC CONVERSATION — YOU ARE NOT JUST RESPONDING TO THE REVIEWER, YOU ARE SHOWING EVERY FUTURE CUSTOMER HOW YOU HANDLE FEEDBACK.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Restaurant name** | "What is the restaurant name?" | No default — must be provided |
| **Review text** | "Paste the review you need to respond to." | No default — must be provided |
| **Star rating** | "What rating did they give? 1-5 stars." | No default — must be provided |
| **Platform** | "Where was this posted? Google, Yelp, TripAdvisor?" | Google |
| **Context** | "Do you know what happened? Was the complaint valid?" | Unknown — respond diplomatically |
| **Tone preference** | "Should the tone be warm, professional, or apologetic?" | Warm and professional |

**GATE: Confirm the review and context before writing the response.**

---

## Phase 2: Classify the Review

### Review Types

| Type | Star Range | Approach |
|------|-----------|----------|
| **Glowing** | 5 stars | Thank, personalize, invite back |
| **Positive** | 4 stars | Thank, acknowledge what they loved, address minor note |
| **Mixed** | 3 stars | Thank, acknowledge positive, address concern, invite back |
| **Negative** | 1-2 stars | Acknowledge, empathize, offer resolution, take offline |
| **Unfair/Fake** | Any | Respond professionally, flag to platform if policy violation |

### Response Priority

- **Negative reviews:** Respond within 24 hours (damage control)
- **Mixed reviews:** Respond within 48 hours
- **Positive reviews:** Respond within 1 week
- **All reviews:** Never leave a review without a response

**GATE: Classify the review type and confirm the approach before writing.**

---

## Phase 3: Write

### Response Framework by Type

**Glowing Review (5 stars):**
1. Thank them by name
2. Reference something specific they mentioned
3. Share a brief personal touch (the chef is thrilled, we are glad you loved X)
4. Invite them back with a specific suggestion

**Positive Review (4 stars):**
1. Thank them warmly
2. Acknowledge what they enjoyed
3. Briefly address any constructive note
4. Invite them to try something specific next time

**Mixed Review (3 stars):**
1. Thank them for honest feedback
2. Acknowledge the positive elements first
3. Address the concern directly (no excuses, no deflecting)
4. Explain what you are doing about it (if applicable)
5. Invite them to give you another chance

**Negative Review (1-2 stars):**
1. Apologize sincerely (not "sorry you feel that way")
2. Acknowledge the specific issue
3. Do not make excuses or argue
4. Explain corrective action (briefly)
5. Offer to make it right (take the conversation offline)
6. Provide contact info (email or phone)

**Unfair or Fake Review:**
1. Respond calmly and factually
2. State your version without being defensive
3. Invite them to contact you directly
4. Report to the platform if it violates review policies

### Response Templates

**5-Star Template:**
"[Name], thank you so much for the kind words! We are thrilled you enjoyed the [specific dish or experience they mentioned]. [Personal touch — e.g., "Our chef puts a lot of love into that dish"]. Next time you visit, ask about our [seasonal item or special] — I think you would love it. See you soon!"

**1-2 Star Template:**
"[Name], I am sorry your experience did not meet your expectations. [Acknowledge specific issue]. That is not the standard we hold ourselves to, and I want to make this right. I have shared your feedback with our team, and we [specific corrective action if applicable]. Please reach out to me directly at [email] — I would love the opportunity to turn this around for you. — [Name, Title]"

### Response Rules

- **Always use their name** (if available)
- **Never argue publicly** — even when the review is wrong
- **Never offer compensation in a public response** — take it offline
- **Never copy-paste the same response** — personalize every reply
- **Keep it concise** — 3-5 sentences for positive, 5-7 for negative
- **Sign with your name and title** — personal accountability matters
- **Never say "sorry you feel that way"** — this is dismissive, not an apology

---

## Phase 4: Polish

### 1. Response Tone Guide

| Tone | When to Use | Example Phrase |
|------|-------------|---------------|
| **Warm** | Positive reviews | "We are so glad you had a great time!" |
| **Grateful** | All reviews | "Thank you for taking the time to share this." |
| **Empathetic** | Negative reviews | "I understand how frustrating that must have been." |
| **Action-oriented** | Negative reviews | "We have addressed this with our team." |
| **Inviting** | All reviews | "We would love to welcome you back." |

### 2. Escalation Protocol

For reviews that require offline follow-up:
1. Respond publicly with empathy and an invitation to connect
2. Reach out privately within 24 hours
3. Offer a specific resolution (comp, replacement visit, refund)
4. Document the resolution
5. If the reviewer updates their rating, thank them publicly

### 3. Quality Checklist

```
## Review Response Checklist

- [ ] Response addresses the reviewer by name
- [ ] Specific details from their review are referenced
- [ ] Positive elements are acknowledged (even in negative reviews)
- [ ] Concerns are addressed without excuses or arguing
- [ ] Negative reviews include an apology and corrective action
- [ ] Contact information provided for offline resolution (negative reviews)
- [ ] Response is signed with name and title
- [ ] Tone is appropriate to the review type
- [ ] Response is concise (3-7 sentences)
- [ ] No compensation offered in public responses
```

---

## Example

**Review (2 stars):** "Food was decent but we waited 45 minutes for our entrees. Server seemed overwhelmed and never checked on us. Will not be back."

**Response:**
"Sarah, thank you for your honest feedback — and I sincerely apologize for the long wait and lack of attention during your visit. A 45-minute wait for entrees is not acceptable, and you deserved better service. I have spoken with our team about staffing during peak hours, and we are making changes to prevent this from happening again. I would love the chance to give you the experience you should have had. Please email me at [email] — dinner is on us next time. — Marco, General Manager"

**Review (5 stars):** "Best pasta I have had outside of Italy! The cacio e pepe was perfect and the tiramisu was to die for. Our server Anna was wonderful."

**Response:**
"James, you just made our chef's day! The cacio e pepe is his pride and joy — he actually spent two weeks in Rome perfecting that recipe. And Anna is a gem, we will make sure she sees your kind words. Next time you are in, ask about our housemade limoncello — it pairs perfectly with the tiramisu. We cannot wait to have you back!"

---

## Anti-Patterns

- **Copy-paste responses** — "Thank you for your review! We hope to see you again!" on every review looks automated and careless.
- **Arguing with the reviewer** — even if they are wrong, a public argument makes you look bad. Take it offline.
- **Ignoring negative reviews** — silence looks like you do not care. Always respond to negative reviews first.
- **Over-explaining** — "Our dishwasher broke and two servers called in sick" is an excuse, not a solution.
- **Offering freebies publicly** — "Come back for a free meal" trains customers to leave bad reviews for free food. Offer resolution privately.

---

## Recovery

- **Review is factually wrong:** Politely state your perspective without calling them a liar. "We looked into this and our records show [X]. We would love to discuss further."
- **Reviewer will not respond to offline outreach:** You have done your part. The public response shows future customers you tried.
- **Multiple negative reviews about the same issue:** Fix the root cause. Respond to each review individually, but mention the systemic fix.
- **Suspected fake review:** Respond professionally, then flag the review to the platform with evidence (no record of the visit, competitors, etc.).
