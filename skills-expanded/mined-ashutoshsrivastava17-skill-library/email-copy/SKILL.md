---
name: email-copy
description: >
  Write marketing emails: subject lines, body copy, CTAs, personalization,
  A/B test variants, and compliance (CAN-SPAM/GDPR).
  TRIGGER when: user says /email-copy, "write an email", "email campaign", "marketing email", "newsletter copy", "drip sequence".
argument-hint: "[email purpose, e.g. 'product launch announcement' or 'abandoned cart recovery']"
user-invocable: true
---

# Email Copy

Write high-converting marketing emails with optimized subject lines, body copy, CTAs, personalization tokens, A/B test variants, and full regulatory compliance. Supports one-off sends, drip sequences, and triggered emails.

---

## Process

### Step 1 — Define Email Purpose and Context

Clarify the strategic context before writing a single word.

| Input | Question | Why It Matters |
|---|---|---|
| Email type | What kind of email? | Determines structure, tone, and length |
| Goal | What should the reader do? | Shapes the CTA and copy hierarchy |
| Audience | Who is receiving this? | Drives tone, personalization, and content |
| Sending context | Cold list, warm subscribers, triggered by action? | Affects open rate assumptions and copy approach |
| Brand voice | Formal, casual, playful, authoritative? | Ensures consistency |
| Key offer/message | What is the core value proposition? | Becomes the headline and hook |

Common email types and their characteristics:

| Email Type | Primary Goal | Typical Length | Tone |
|---|---|---|---|
| Welcome email | Onboard, set expectations | 150-250 words | Warm, helpful |
| Product launch | Drive awareness and action | 200-400 words | Excited, confident |
| Newsletter | Inform, engage, retain | 300-600 words | Conversational |
| Promotional / Sale | Drive purchases | 100-200 words | Urgent, benefit-focused |
| Abandoned cart | Recover lost conversion | 100-150 words | Helpful, low-pressure |
| Re-engagement | Win back inactive users | 100-200 words | Personal, curious |
| Event invitation | Drive registrations | 150-250 words | Professional, compelling |
| Case study / story | Build trust, nurture | 200-400 words | Narrative, proof-oriented |
| Transactional (receipt, confirm) | Inform, reduce support | 50-150 words | Clear, factual |

### Step 2 — Write Subject Lines

The subject line determines whether the email gets opened. Produce 5-8 variants across different psychological approaches.

| Approach | Example | When to Use |
|---|---|---|
| **Benefit-driven** | "Cut your onboarding time by 60%" | When you have a clear, quantifiable benefit |
| **Curiosity gap** | "The one metric most teams ignore" | Newsletters, thought leadership |
| **Urgency / scarcity** | "Last chance: early-bird pricing ends tonight" | Promotions, events with deadlines |
| **Personalized** | "{{first_name}}, your Q3 content plan is ready" | Triggered emails, high-value segments |
| **Question** | "Is your checkout flow losing you customers?" | Problem-aware audiences |
| **Social proof** | "Why 2,000+ teams switched this quarter" | Consideration-stage prospects |
| **How-to** | "How to write proposals that close in 3 days" | Educational content, lead nurture |
| **Announcement** | "Introducing: AI-powered campaign planner" | Product launches, feature releases |

Subject line rules:
- **Length**: 30-50 characters for mobile-first (6-10 words)
- **Preview text**: Write complementary preview text (40-90 characters) — it is NOT a repeat of the subject line
- **Avoid**: ALL CAPS, excessive punctuation (!!!), spam trigger words (free, guarantee, act now) unless contextually appropriate
- **Emoji**: Use sparingly (0-1) and only if it matches brand voice

### Step 3 — Write Body Copy

Structure the email body using this hierarchy:

```
1. Hook (first 1-2 sentences) — connect to a pain point, desire, or context
2. Value / Story (2-4 sentences) — deliver the core message or narrative
3. Proof (1-2 sentences) — data point, testimonial, or social proof
4. CTA (1 sentence + button) — clear, single action
5. PS line (optional) — secondary CTA or urgency reinforcement
```

Copy principles:

| Principle | Guideline |
|---|---|
| **One email = one goal** | Do not split attention across multiple CTAs unless it is a newsletter |
| **Write for scanners** | Short paragraphs (1-3 sentences), bold key phrases, use whitespace |
| **Second person** | "You" focused, not "We are excited to announce" |
| **Specific > vague** | "Save 4 hours/week" beats "Save time" |
| **Active voice** | "Download the guide" not "The guide can be downloaded" |
| **Mobile-first** | 600px max width, 14-16px body font, tappable CTA button (44x44px min) |
| **Plain text version** | Always provide a plain-text alternative for deliverability |

### Step 4 — Craft the CTA

| CTA Type | Button Text Examples | Best For |
|---|---|---|
| Direct action | "Start free trial", "Download the report" | Conversion-focused |
| Low commitment | "See how it works", "Learn more" | Awareness, top-of-funnel |
| Urgency | "Claim your spot", "Get early access" | Limited offers, events |
| Personal | "Build my plan", "Show me my results" | Personalized experiences |
| Social | "Join 5,000+ marketers", "See what others built" | Community, social proof |

CTA rules:
- One primary CTA per email (can repeat the same CTA 2-3 times in longer emails)
- Button text: 2-5 words, starts with a verb
- Place the primary CTA above the fold AND at the end
- Use contrasting button color
- Link the CTA to a dedicated landing page, not a homepage

### Step 5 — Add Personalization

| Personalization Level | Example | Data Required |
|---|---|---|
| **Basic** | "Hi {{first_name}}," | First name |
| **Contextual** | "Since you downloaded our SEO guide..." | Behavioral data |
| **Segment-based** | Different copy blocks for different industries | Segment tags |
| **Dynamic content** | Product recommendations based on browsing history | Product/behavioral data |
| **Send-time optimization** | Deliver at each recipient's optimal open time | Engagement history |

Always include fallback values: `{{first_name | "there"}}` so emails don't render as "Hi ," for contacts with missing data.

### Step 6 — Create A/B Test Variants

Produce at least two testable variants. Only test one variable at a time.

| Test Variable | Variant A | Variant B | Minimum Sample Size |
|---|---|---|---|
| Subject line | Benefit-driven | Curiosity-driven | 1,000+ per variant |
| CTA text | "Start free trial" | "See it in action" | 1,000+ per variant |
| Email length | Short (100 words) | Long (300 words) | 1,000+ per variant |
| Personalization | With first name | Without first name | 1,000+ per variant |
| Send time | Tuesday 10am | Thursday 2pm | 1,000+ per variant |
| Sender name | Company name | Person's name | 1,000+ per variant |

Recommend the user test subject lines first (highest impact on open rate), then CTAs (highest impact on click rate).

### Step 7 — Ensure Compliance

Every marketing email must comply with applicable regulations.

| Requirement | CAN-SPAM (US) | GDPR (EU) | CASL (Canada) |
|---|---|---|---|
| **Consent** | Opt-out (can send without prior consent) | Opt-in required (explicit consent) | Opt-in required (express or implied) |
| **Unsubscribe** | Must include, honor within 10 business days | Must include, honor without delay | Must include, honor within 10 business days |
| **Sender identity** | Accurate "From" name and reply address | Identify the data controller | Identify the sender |
| **Physical address** | Must include valid postal address | Not explicitly required but recommended | Must include valid postal address |
| **Subject line** | Must not be deceptive | Must not be deceptive | Must not be deceptive |
| **Data rights** | N/A | Right to access, rectify, delete, port data | Right to withdraw consent |

Compliance checklist for every email:
- [ ] Unsubscribe link is visible and functional
- [ ] Physical mailing address is included in the footer
- [ ] "From" name and email are accurate and recognizable
- [ ] Subject line accurately represents the email content
- [ ] Consent was obtained appropriately for the audience's jurisdiction
- [ ] Privacy policy is linked in the footer

---

## Output Format

Deliver the email copy as follows:

```
EMAIL: [Email name / campaign name]
TYPE: [Welcome / Promotional / Newsletter / etc.]
AUDIENCE: [Segment description]
GOAL: [Primary action desired]

SUBJECT LINE OPTIONS:
1. [Subject line] | Preview: [preview text]
2. [Subject line] | Preview: [preview text]
3. [Subject line] | Preview: [preview text]
4. [Subject line] | Preview: [preview text]
5. [Subject line] | Preview: [preview text]

A/B TEST RECOMMENDATION: Test subjects #X vs #Y — [rationale]

---

FROM: [Sender name] <[email]>
SUBJECT: [Recommended subject]
PREVIEW: [Preview text]

[Full HTML-ready body copy with formatting notes]

---

CTA: [Button text] → [Landing page URL or description]

PERSONALIZATION TOKENS USED:
- {{first_name}} — fallback: "there"
- [any others]

COMPLIANCE FOOTER:
[Unsubscribe link, postal address, privacy policy link]

PLAIN TEXT VERSION:
[Full plain-text alternative]

A/B VARIANT:
[Variant B copy with the tested variable changed]
```

---

## Quality Checklist

- [ ] Subject line is under 50 characters and not misleading
- [ ] Preview text complements (not repeats) the subject line
- [ ] Hook in the first sentence connects to reader's situation
- [ ] Body copy follows the Hook → Value → Proof → CTA structure
- [ ] Only one primary CTA per email
- [ ] CTA button text starts with a verb and is 2-5 words
- [ ] Personalization tokens have fallback values
- [ ] Email reads well on mobile (short paragraphs, clear hierarchy)
- [ ] A/B test variant changes only one variable
- [ ] Unsubscribe link, physical address, and sender identity are included
- [ ] Plain text version is provided
- [ ] No spam trigger words used unnecessarily
- [ ] Tone matches the stated brand voice

---

## Edge Cases

- **Cold outreach** (not marketing email): Note that cold emails have different legal requirements. CAN-SPAM still applies, but GDPR requires legitimate interest basis. Recommend keeping cold emails very short (50-100 words) and highly personalized.
- **Drip sequence** (multi-email): Produce all emails in the sequence with clear trigger conditions, wait times between sends, and exit conditions. Ensure the narrative progresses across emails.
- **Re-engagement to inactive list**: Warn that sending to a cold list risks deliverability. Recommend a small test batch first. Use a "We miss you" or "Should we remove you?" angle to get an explicit signal.
- **No brand voice defined**: Default to professional and conversational. Flag the assumption and recommend the user establish brand voice guidelines.
- **Multiple CTAs required** (e.g., newsletter): Use a clear visual hierarchy — one primary CTA, others as text links. Do not make every section equal weight.
- **Highly regulated product** (financial services, healthcare): Add a disclaimer review step. Flag that specific claims may need legal review. Avoid guarantees or specific outcome promises.
- **Very small list** (< 500 contacts): A/B testing is not statistically reliable. Recommend sending the best single version and testing subject lines when the list grows.
- **Transactional email that includes marketing**: Note that mixing transactional and marketing content may change the regulatory classification. Keep marketing content minimal and clearly separated.
