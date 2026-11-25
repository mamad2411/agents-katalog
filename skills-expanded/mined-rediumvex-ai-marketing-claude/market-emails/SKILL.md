---
name: market-emails
description: Generate email sequences (welcome, nurture, launch, cold outreach, cart abandon, re-engagement, onboarding) with subject line variants, cadence, and metrics benchmarks. Invoke whenever the user says "email sequence", "welcome series", "nurture", "cold outreach", "win-back", or runs `/market emails <type>`. Matches BRAND-VOICE.md if present.
---

# Market Emails — Sequence Writer

Produce full, send-ready email sequences. Every email has a purpose, every sequence has a goal, every send has a metric target.

## Sequence Types

| Type | Goal | Length | Cadence |
|---|---|---|---|
| **Welcome** | Activate new signups | 5–7 emails | Day 0, 1, 3, 5, 7, (10, 14) |
| **Nurture** | Convert warm leads to buyers | 6–8 emails | Every 2–3 days |
| **Launch** | Drive sales for a new product | 5–7 emails | 14 days: tease → reveal → proof → urgency → cart close |
| **Cold outreach** | Start B2B conversations | 4–6 touches | Day 0, 3, 7, 14, 21, 30 |
| **Cart abandon** | Recover lost revenue | 3 emails | 1h, 24h, 72h |
| **Re-engagement** | Wake inactive subscribers | 3–4 emails | Every 3–4 days |
| **Onboarding** | Drive product activation | 5–6 emails | Triggered on signup + milestones |

## Benchmarks (2024+)

| Metric | B2B | B2C | E-com |
|---|---|---|---|
| Open rate | 25–35% | 20–30% | 18–25% |
| Click rate | 2–5% | 2–4% | 2–5% |
| Reply rate (cold) | 3–10% | — | — |
| Unsubscribe | <0.5% | <0.5% | <0.5% |
| Cart recovery | — | — | 10–25% |

Subject line failure = open rate < benchmark. CTA failure = click rate < benchmark. Offer failure = conversion below expected.

## Subject Line Formulas

| Formula | Pattern | Example |
|---|---|---|
| **Curiosity** | Tease without revealing | "The reporting mistake we all made" |
| **Specificity** | Number + outcome | "How Jamie cut reports from 8h to 20min" |
| **Personal** | First name + context | "{{first_name}}, a quick question" |
| **Contrarian** | Challenge common belief | "Stop A/B testing your headlines" |
| **Question** | Prompt self-reflection | "Is your funnel actually a funnel?" |
| **Urgency** | Real deadline | "Last day for the 2025 rate" |
| **Social proof** | Show outcome | "5,000 teams use this now" |
| **Fear of missing out** | What others know | "What growth teams are doing in Q2" |
| **Pattern interrupt** | Unexpected framing | "Ignore this if you're already ranking" |
| **Plain text-style** | No marketing gloss | "quick question about acme" |

**Always ship 3 subject line variants per email** so the client can A/B test.

## Pre-flight

1. Load `BRAND-VOICE.md` if present; match tone.
2. Confirm the goal, audience, and product/offer.
3. Confirm cadence and sending platform (affects formatting — Mailchimp vs SendGrid vs HubSpot all render differently).
4. Ask for a "from" name and reply-to — it matters more than people think.

## Email Anatomy

Every email includes:
- **From name** (real human preferred over "Acme Team")
- **Subject line** (3 variants)
- **Preview text** (40–90 chars, complements subject)
- **Body** (plain-text-friendly when possible)
- **Primary CTA** (1 per email; secondary only in nurture/launch)
- **PS** (often the second most-read line in the email)

## Body structures

| Position | Function |
|---|---|
| Opening line | Hook — curiosity, relevance, story start. Never "Hi {{name}}, I hope this email finds you well." |
| Setup | Context — why this matters to them, what they'll get |
| Payoff | The actual value — insight, offer, story, proof |
| CTA | Clear next step, value-driven, linked once or twice max |
| Signature | Real name, human |
| PS | Restate value, add urgency, or surface a secondary offer |

## Compliance (do not skip)

- **CAN-SPAM (US):** physical address, unsubscribe link, truthful headers, honor unsubs in 10 days
- **GDPR (EU):** explicit consent, unsubscribe, data purpose disclosed
- **CASL (Canada):** express consent for cold outreach; implied consent only in narrow cases
- **Cold outreach specifically:** include why you're reaching out, who you are, and an easy opt-out

Every sequence output must include a compliance note stating which regions it's cleared for.

## Output Format

```markdown
## [Sequence Type] Email Sequence — [Brand]

**Goal:** [activation / conversion / recovery / etc]
**Audience:** [describe]
**Cadence:** [days between sends]
**Expected metrics:** [open / click / convert targets]
**Compliance:** [CAN-SPAM / GDPR / CASL cleared]

---

### Email 1: [Purpose] — Send: [Day X]
**From:** [Name]
**Subject A:** "[subject]"
**Subject B:** "[subject]"
**Subject C:** "[subject]"
**Preview:** "[40–90 char preview text]"

[Full body]

[Sign-off]
[Name]

PS: [PS line]

**Why this email:** [1-sentence rationale]

---

### Email 2: ...
```

## Cold Outreach (special case)

Cold emails need extra care. Use this structure for every touch:

- **Touch 1 (Day 0):** Personal observation + specific problem + light CTA ("worth a quick chat?")
- **Touch 2 (Day 3):** Value drop — share an insight or resource, no ask
- **Touch 3 (Day 7):** Social proof — similar company outcome
- **Touch 4 (Day 14):** Direct ask with clear offer
- **Touch 5 (Day 21):** Breakup — "should I close the loop?"
- **Touch 6 (Day 30, optional):** New hook, different angle

Never send a 500-word first email. Cold outreach above 120 words dies.

## Quality Bar

- Read every email aloud. If it sounds like a template, rewrite.
- Personalization tokens are not personalization. A real observation is.
- Never promise a discount you can't deliver. Never fake scarcity.
- If the user can't point to a real outcome or proof, the sequence will fail no matter how good the copy is — say so.
