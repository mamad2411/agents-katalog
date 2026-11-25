---
name: email-sequence
description: Designs and drafts multi-email sequences with full copy, timing, branching logic, exit conditions, and performance benchmarks. Make sure to use this skill whenever the user says build a drip sequence, design an email cadence, write an onboarding sequence, build a nurture campaign, design a re-engagement flow, win-back sequence, product launch email series, or describes wanting a connected series of emails (not a single message) on a defined timeline. Includes A/B test suggestions and exit-condition logic. Do NOT use for: single ad-hoc emails (handle directly), one-off marketing newsletter (use marketing:draft-content), customer support replies (use customer-support:draft-response), or sales prospect outreach to one named person (use sales:draft-outreach — though this skill produces multi-touch sales sequences when targeting an ICP, not a named individual). Defining characteristic: "multi-email sequence with timing, logic, and exit conditions — not a single email."
---

# Email Sequence

Multi-email sequences with timing, branching, exit conditions, and performance benchmarks.

## When to use vs. adjacent skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Multi-email sequence with timing logic | Single one-off email → handle directly |
| Onboarding / nurture / re-engagement flow | Marketing newsletter → `marketing:draft-content` |
| Drip campaign | Customer support reply → `customer-support:draft-response` |
| Product launch email series | Outreach to one named prospect → `sales:draft-outreach` |

## Sequence types this skill handles

### Onboarding sequence (post-signup, B2B SaaS)
Audience: trial users or new customers. Goal: drive activation.

Standard structure (5-7 emails over 14 days):
- **Day 0** (within 1 hour): Welcome + first-action prompt
- **Day 1**: Use case spotlight #1 (most common use case)
- **Day 3**: Use case spotlight #2 (or integration spotlight)
- **Day 5**: Tips from successful customers ("here's what 80% of users do in week 1")
- **Day 7**: Value check-in ("are you seeing X yet?")
- **Day 10**: Pricing / upgrade prompt (for trial) or expansion (for customer)
- **Day 14**: Final activation push or "what's blocking you" survey

### Nurture / lead nurture sequence (post-content download or interest signal)
Audience: marketing-qualified leads not yet sales-ready. Goal: maintain mindshare, qualify intent.

Standard structure (4-8 emails over 30-60 days):
- **Day 0**: Deliver the requested content + relevant deeper resource
- **Day 3**: Educational content #1 (related to their interest)
- **Day 7**: Customer story (named customer in similar context)
- **Day 14**: Industry insight / benchmark report
- **Day 21**: Soft invitation (webinar, podcast, demo invitation)
- **Day 30**: Direct check-in ("would a 15-min call be useful?")
- **Optional Day 45**: Final value piece + clear opt-out

### Re-engagement sequence (dormant customers/prospects)
Audience: people who haven't engaged in 60-90+ days. Goal: re-spark or graceful exit.

Standard structure (3-5 emails over 14 days):
- **Day 0**: "We've missed you" + specific value reminder
- **Day 4**: New capability / use case they may not know about
- **Day 8**: Customer story showing transformation
- **Day 12**: Direct ask ("are we still useful? happy to update preferences")
- **Day 14**: Final email with explicit "no response = we'll stop" exit

### Win-back sequence (lost customers/closed-lost)
Audience: customers who churned or prospects who lost. Goal: reopen the relationship.

Standard structure (3-4 emails over 30 days):
- **Day 0**: "Things have changed" — what's new since they left
- **Day 7**: Specific addressing of their original objection (price, feature gap, etc.)
- **Day 14**: Customer story from someone who came back
- **Day 30**: Direct re-evaluation invitation

### Product launch sequence (announce + activate new feature)
Audience: existing customer base or relevant segment. Goal: drive adoption of new capability.

Standard structure (4-6 emails over 21 days):
- **Day 0**: Launch announcement with primary benefit
- **Day 3**: Walkthrough or demo (link to recorded demo)
- **Day 7**: Customer beta tester story
- **Day 14**: "Have you tried it yet?" prompt with one-click activation
- **Day 21**: Tips & tricks for power users

### Sales sequence (outbound to ICP, NOT named-individual research)
For volume outreach to a defined ICP, NOT for personalized 1:1 outreach (that's `sales:draft-outreach`).

Standard structure (5-7 touches over 21 days, multi-channel):
- **Touch 1 (Day 0)**: Email — angle 1
- **Touch 2 (Day 3)**: LinkedIn connect with personalized note
- **Touch 3 (Day 7)**: Email — different angle (NOT "just bumping this")
- **Touch 4 (Day 12)**: LinkedIn message or Twitter engagement
- **Touch 5 (Day 18)**: Email — case study with similar customer
- **Touch 6 (Day 21)**: Final email with breakup + permission to recontact later

## Sequence design principles

### 1. Each email earns the next
Every email needs a reason to exist beyond "we're at day N." If you can't write a one-line "why this email at this time," cut it.

### 2. Timing is content
Same message at Day 1 vs. Day 14 lands differently. The cadence itself communicates respect or pressure.

### 3. Stop the moment they engage
Reply, click, action — they should drop out of the cold sequence and into a warm path. Continuing the sequence after engagement signals you're not paying attention.

### 4. Different angles, not different versions
Email 3 should NOT be "another way of saying email 1." It should be a different angle, different value, different CTA framing.

### 5. Single CTA per email
Multiple CTAs reduce conversion by ~50%. Pick one.

### 6. Mobile-first formatting
70%+ of B2B email is opened on mobile. Short paragraphs, minimal images, scannable.

### 7. Exit always-on
Every email has clear unsubscribe. Some sequences benefit from "pause for 90 days" or "topic preferences" alongside hard unsubscribe.

## Subject line discipline

- Short (under 50 chars for mobile)
- Avoid spam triggers (FREE, ALL CAPS, !!!, $$$)
- Personalization tokens that look natural (NOT "{{first_name}}" rendered)
- A/B test in pairs (curiosity vs. specific-value variants typically)
- Preheader is your second subject line — use it

## A/B test suggestions per sequence

Default tests this skill recommends:

- **Subject line:** curiosity-driven vs. specific-value
- **Send time:** Tuesday 10am vs. Thursday 2pm (in recipient TZ)
- **CTA framing:** "Book a demo" vs. "Quick 15-min call?"
- **Opener:** Question vs. statement vs. customer name reference
- **Length:** Long (300+ words) vs. short (under 100 words)

Test ONE variable at a time.

## Performance benchmarks (B2B SaaS)

| Metric | Industry baseline | Strong | Excellent |
|---|---|---|---|
| Open rate | 20-25% | 30-40% | 40%+ |
| Click rate | 2-3% | 5-8% | 10%+ |
| Reply rate (cold) | <1% | 3-5% | 5%+ |
| Reply rate (warm) | 5% | 15-20% | 25%+ |
| Unsubscribe | <0.5% | <0.3% | <0.2% |
| Bounce | <2% | <1% | <0.5% |

Variances expected by industry (cybersec tends slightly higher engagement than average B2B; financial services lower).

## Exit conditions to define

Every sequence needs explicit exits:
- **Engagement** — replied, clicked CTA, took the desired action → move to warm path
- **Unsubscribe** — hard exit
- **Hard bounce** — exit and clean from list
- **Soft bounce** — pause, retry once
- **Out-of-office reply** — pause until OOO date passes
- **Sequence complete** — no more emails; move to permanent suppression OR long-cycle nurture

## Anti-patterns

- **"Just following up"** — adds zero value; signals the sender has nothing new
- **All emails at 9 AM Monday** — your cadence becomes someone else's spam
- **Identical CTAs every email** — boring and ineffective
- **Long sequences (>10 emails)** — diminishing returns; cut after 5-7 typically
- **No opt-out** — illegal in many jurisdictions, and unethical everywhere
- **Personalization that's obviously wrong** — "Hi [FIRST_NAME]" or "I noticed you're at [COMPANY]" when nothing follows
- **Stale sequences (set up years ago, never updated)** — review quarterly
- **Treating engagement signals as rejection** — they replied; that's a win; pivot to human

## Output

Produces:
1. The full sequence specification — every email with subject, body, CTA, timing
2. Branching logic / exit conditions
3. A/B test recommendations
4. Performance benchmark expectations
5. Suggested ESP / automation tool wiring (Klaviyo, HubSpot, Marketo, Customer.io, etc.)
6. Maintenance cadence reminder (review quarterly)
