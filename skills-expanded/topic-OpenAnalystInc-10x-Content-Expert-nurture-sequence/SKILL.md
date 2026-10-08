---
name: nurture-sequence
description: |
  Creates email nurture sequences, drip campaigns, and automated email flows.
  Designs welcome sequences, lead nurturing, onboarding flows, and re-engagement
  campaigns. Use this skill when you need multi-email sequences with strategic
  timing and progressive engagement.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Nurture Sequence Skill

> **QUICK REFERENCE**
> - **Output folder**: `output/content/sequences/`
> - **File naming**: `YYYY-MM-DD_topic_nurture_sequence.md`
> - **Sample script**: `scripts/samples/sample_nurture_sequence.py`
> - **Run with**: `.venv\Scripts\python.exe scripts/samples/sample_nurture_sequence.py`
> - **Sequence types**: Welcome, Lead Nurture, Onboarding, Re-engagement, Launch, Webinar
> - **Frameworks**: PAS, AIDA, BAB (see `content-frameworks` skill)
> - **Python**: ALWAYS use `.venv\Scripts\python.exe` (never bare `python`)

Creates strategic email sequences that build relationships and drive conversions over time.

## Scope of This Skill

**This skill handles:**
- Welcome/onboarding sequences
- Lead nurture sequences
- Sales sequences
- Educational drip campaigns
- Re-engagement sequences
- Cart abandonment sequences
- Post-purchase sequences
- Event/launch sequences

**NOT handled by this skill:**
- Single standalone emails → Use `email-copywriter`
- Cold outreach emails → Use `email-copywriter`
- Newsletter content → Use `email-copywriter`

## Sequence Types & Structures

### 1. Welcome Sequence

**Purpose:** Introduce brand, deliver value, build trust, prime for purchase
**Duration:** 5-7 emails over 14-21 days

```
Email 1 (Immediate): Welcome + Quick Win
- Confirm subscription
- Deliver promised lead magnet
- Set expectations for what's coming
- One quick actionable tip

Email 2 (Day 2): Your Story
- Who you are and why you do this
- Relatable origin story
- Build connection and credibility
- Soft CTA to engage

Email 3 (Day 4): Core Value
- Your best content piece
- Educational, pure value
- Establish expertise
- No selling

Email 4 (Day 7): Social Proof
- Customer stories/testimonials
- Case study or results
- Build desire through proof
- Subtle product mention

Email 5 (Day 10): Common Problem
- Address biggest objection/pain
- Show you understand their struggle
- Introduce your solution
- Soft pitch

Email 6 (Day 14): The Offer
- Full pitch for product/service
- Benefits, features, proof
- Clear CTA
- Urgency if appropriate

Email 7 (Day 21): Final Nudge
- Last chance messaging
- Address remaining objections
- Testimonial + strong CTA
- Transition to regular newsletter
```

### 2. Lead Nurture Sequence

**Purpose:** Educate leads, build trust, guide to purchase decision
**Duration:** 6-10 emails over 3-6 weeks

```
Email 1: Problem Acknowledgment
- "I know you're struggling with [X]"
- Validate their situation
- Promise to help

Email 2: Quick Win
- Actionable tip they can implement today
- Easy victory to build trust
- Position you as helpful

Email 3: Education Part 1
- Foundational concept
- "Most people get this wrong"
- Challenge assumptions

Email 4: Education Part 2
- Build on previous email
- More depth
- Establish expertise

Email 5: Case Study
- Real results from real person
- Their situation → transformation
- Proof your approach works

Email 6: Common Objection
- "You might be thinking [objection]"
- Address it directly
- Overcome with logic + emotion

Email 7: Soft Pitch
- Introduce your solution
- Benefits focused
- Low-pressure CTA

Email 8: Hard Pitch
- Full offer details
- Urgency element
- Strong CTA

Email 9: FAQ
- Answer common questions
- Remove friction
- Build confidence

Email 10: Final Opportunity
- Last chance
- Summary of value
- Final CTA
```

### 3. Onboarding Sequence

**Purpose:** Activate new users, drive adoption, prevent churn
**Duration:** 5-7 emails over first 14 days

```
Email 1 (Immediate): Welcome + First Step
- Congratulations!
- Single most important first action
- Clear instructions

Email 2 (Day 1): Quick Win
- Easy early success
- Build confidence
- Show value fast

Email 3 (Day 3): Core Feature
- Most important feature
- How to use it
- Why it matters

Email 4 (Day 5): Pro Tips
- "Here's what power users do"
- Advanced but accessible tips
- Show depth of product

Email 5 (Day 7): Check-In
- "How's it going?"
- Offer help
- Ask for feedback

Email 6 (Day 10): Success Story
- Customer who achieved results
- Inspire and motivate
- Show what's possible

Email 7 (Day 14): Next Level
- Upgrade pitch or advanced features
- "Ready for more?"
- Growth path
```

### 4. Re-Engagement Sequence

**Purpose:** Win back inactive subscribers/users
**Duration:** 3-4 emails over 7-14 days

```
Email 1: "We Miss You"
- Acknowledge absence
- What they're missing
- Easy re-engagement action

Email 2: Best Content
- Your top performing content
- "In case you missed this"
- Pure value, no pitch

Email 3: Special Offer
- Exclusive comeback offer
- Time-limited
- Clear CTA

Email 4: Final Goodbye
- "Should we part ways?"
- Unsubscribe option
- Last chance to stay
- Clean your list
```

### 5. Cart Abandonment Sequence

**Purpose:** Recover abandoned purchases
**Duration:** 2-3 emails within 72 hours

```
Email 1 (1 hour): "Did something go wrong?"
- Remind what's in cart
- Offer help
- Link back to checkout

Email 2 (24 hours): "Still thinking about it?"
- Social proof / review
- Benefits reminder
- Address common objections

Email 3 (72 hours): "Last chance"
- Urgency (stock, price, etc.)
- Small incentive if possible
- Final CTA
```

## Email Timing Best Practices

| Sequence Type | Email Spacing | Total Duration |
|--------------|---------------|----------------|
| Welcome | Days 0, 2, 4, 7, 10, 14, 21 | 3 weeks |
| Lead Nurture | Every 3-5 days | 4-8 weeks |
| Onboarding | Days 0, 1, 3, 5, 7, 10, 14 | 2 weeks |
| Re-engagement | Days 0, 3, 7, 14 | 2 weeks |
| Cart Abandon | 1hr, 24hr, 72hr | 72 hours |
| Launch | Daily or every other day | 5-10 days |

## Sequence Writing Principles

### The 80/20 Rule
- 80% value / education
- 20% promotion
- Build trust before asking

### Progressive Disclosure
- Start broad, get specific
- Educate before selling
- Build on previous emails

### One Email = One Goal
- Single clear CTA per email
- Don't confuse with options
- Guide one next step

### Behavioral Triggers
Consider branching based on:
- Email opens (interested vs. cold)
- Link clicks (specific interests)
- Website visits
- Purchase behavior
- Time since signup

## 3-Mode Workflow

### MODE 1: PLAN

1. **Understand Sequence Goals**
   ```
   - Purpose: Welcome, nurture, onboard, re-engage?
   - Audience: New leads, customers, inactive?
   - End goal: Purchase, activation, retention?
   - Duration: How long?
   - Email count: How many?
   ```

2. **Map Customer Journey**
   ```markdown
   Start: [Where they are]
   ↓
   Step 1: [First email goal]
   ↓
   Step 2: [Second email goal]
   ↓
   ...
   ↓
   End: [Desired outcome]
   ```

3. **Check References**
   ```bash
   # Check email examples
   ls references/examples/emails/

   # Analyze existing sequences
   python scripts/content/analyze_sequences.py \
     --folder references/examples/emails/sequences/ \
     --output output/analysis/sequence_patterns.json
   ```

4. **Document Plan**
   ```markdown
   ## Sequence Plan

   ### Overview
   - Type: [Welcome/Nurture/Onboard/etc.]
   - Emails: [Count]
   - Duration: [Days/Weeks]
   - Goal: [Desired outcome]

   ### Email Flow
   1. [Email 1 purpose] - Day [X]
   2. [Email 2 purpose] - Day [X]
   ...

   ### Key Messages
   - [Message 1]
   - [Message 2]
   - [Message 3]
   ```

### MODE 2: CLARIFY

**Essential Questions:**
- "What type of sequence - welcome, nurture, onboarding?"
- "What's the end goal - purchase, activation, engagement?"
- "How many emails and over what time period?"
- "What product/service are you eventually pitching?"

**Context Questions:**
- "Who is the audience and where are they in their journey?"
- "What lead magnet or entry point triggers this sequence?"
- "Any specific content or stories to include?"

**Brand Questions:**
- "Formal or casual tone?"
- "How personal should these be?"
- "Any specific offers or discounts to include?"

### MODE 3: IMPLEMENT

1. **Write Full Sequence**
   ```bash
   python scripts/content/generate_sequence.py \
     --type welcome \
     --emails 7 \
     --duration 21 \
     --output output/content/sequences/
   ```

2. **Create Email Components**
   - Subject lines (3 variants each)
   - Preview text
   - Body copy
   - CTAs
   - Timing notes

3. **Save Output**
   ```
   output/content/sequences/
   ├── [date]_[type]_sequence/
   │   ├── overview.md
   │   ├── email_1.md
   │   ├── email_2.md
   │   ├── ...
   │   └── implementation_notes.md
   ```

## Output Format

### Sequence Overview Document

```markdown
# [Sequence Name] Email Sequence

## Overview
- **Type**: [Welcome/Nurture/etc.]
- **Emails**: [Count]
- **Duration**: [Days]
- **Goal**: [Outcome]

## Flow Diagram
```
[Entry Point]
    ↓
Email 1 (Day 0): [Purpose]
    ↓
Email 2 (Day X): [Purpose]
    ↓
...
    ↓
[Exit to Regular Newsletter/Next Sequence]
```

## Sequence Summary
| Email | Day | Subject | Goal | CTA |
|-------|-----|---------|------|-----|
| 1 | 0 | [Subject] | [Goal] | [CTA] |
| 2 | 3 | [Subject] | [Goal] | [CTA] |
...

## Trigger/Automation Notes
[How to set this up in email platform]
```

### Individual Email Document

```markdown
# Email [Number]: [Name]

## Metadata
- **Send Day**: Day [X]
- **Time**: [Recommended time]
- **Goal**: [What this email achieves]
- **CTA**: [Primary action]

## Subject Lines (Test These)
1. [Option 1] ← Recommended
2. [Option 2]
3. [Option 3]

## Preview Text
[Preview text that complements subject]

## Email Body

[Full email copy]

---

## Implementation Notes
- **Trigger**: [What triggers this email]
- **Wait condition**: [Time since previous]
- **Branch options**: [If any behavioral branches]
```

## Example Interactions

### "Create a welcome sequence for my course"
```
[PLAN]
- Welcome sequence type
- 7 emails over 3 weeks
- Goal: Course purchase

[CLARIFY]
- "What's the lead magnet that starts this sequence?"
- "What's the course about and price point?"
- "Any testimonials or case studies to include?"
- "What's the deadline/urgency element?"

[IMPLEMENT]
- Full 7-email sequence
- Subject line variants for each
- Timing recommendations
- Automation setup notes
```

### "I need an onboarding sequence for my SaaS"
```
[PLAN]
- Onboarding sequence type
- 5-7 emails over 2 weeks
- Goal: User activation

[CLARIFY]
- "What's the #1 action new users should take?"
- "What features should we highlight?"
- "Any upgrade/upsell at the end?"
- "What does 'activated' look like?"

[IMPLEMENT]
- Activation-focused sequence
- Quick wins early
- Feature education
- Check-in emails
- Success story inspiration
```

### "Create a re-engagement campaign"
```
[PLAN]
- Re-engagement sequence
- 3-4 emails over 2 weeks
- Goal: Win back or clean list

[CLARIFY]
- "How long have they been inactive?"
- "Any special offer for returning?"
- "What's your best content to share?"
- "Are you willing to let them go?"

[IMPLEMENT]
- "We miss you" opener
- Best content / value reminder
- Special comeback offer
- Final goodbye with unsubscribe option
```

## Performance Benchmarks

| Metric | Good | Great | Excellent |
|--------|------|-------|-----------|
| Open Rate | 20%+ | 30%+ | 40%+ |
| Click Rate | 2%+ | 4%+ | 6%+ |
| Sequence Completion | 40%+ | 60%+ | 75%+ |
| Conversion Rate | 2%+ | 5%+ | 10%+ |

## Output Files

Sequences saved to:
- `output/content/sequences/[type]/overview.md` - Full sequence plan
- `output/content/sequences/[type]/email_[N].md` - Individual emails
- `output/content/sequences/[type]/subjects.txt` - All subject lines
- `output/content/sequences/[type]/implementation.md` - Tech setup notes

## Quality Checklist

Before finalizing sequence:
- [ ] Clear entry trigger defined
- [ ] Logical progression between emails
- [ ] Value before pitch (80/20 rule)
- [ ] One CTA per email
- [ ] Subject line variants for testing
- [ ] Timing makes sense for audience
- [ ] Exit point/next step defined
- [ ] Behavioral branches considered
- [ ] Brand voice consistent throughout
