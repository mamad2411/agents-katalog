---
name: email-copywriter
description: |
  Expert email copywriter for all types of email marketing content. Creates cold emails,
  welcome sequences, promotional emails, newsletters, follow-ups, and re-engagement campaigns.
  Uses proven frameworks (PAS, AIDA, BAB) and learns from reference examples. Use this skill
  for any email writing needs.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Email Copywriter Skill

> **QUICK REFERENCE**
> - **Output folder**: `output/content/emails/`
> - **Naming**: `YYYY-MM-DD_topic_email.md`
> - **Sample script**: `scripts/samples/sample_email_content.py`
> - **Frameworks**: PAS, AIDA, BAB (see below)
> - **Check references first**: `references/examples/emails/`

Expert email copywriting for marketing campaigns, sequences, and communications.

## Scope of This Skill

**This skill handles:**
- Cold outreach emails
- Welcome email sequences
- Promotional/sales emails
- Newsletter content
- Follow-up emails
- Re-engagement campaigns
- Transactional email copy
- Subject line creation
- Preview text optimization
- CTA writing

**NOT handled by this skill:**
- Multi-email drip sequences → Use `nurture-sequence`
- Sending emails → This creates copy only
- Email design/HTML → Creates text content

## Email Types & Frameworks

### 1. Cold Emails

**Framework: AIDA (Attention-Interest-Desire-Action)**

```
SUBJECT: [Pattern interrupt or curiosity hook]

[ATTENTION - First line that stops the scroll]
[INTEREST - Relevant to their situation]
[DESIRE - What they could achieve]
[ACTION - Clear, low-friction CTA]

[Signature]
```

**Best Practices:**
- Subject: 28-39 characters for mobile
- First line: Personalized or pattern-interrupt
- Body: Under 150 words
- CTA: Single, clear action
- No attachments in first email

### 2. Welcome Emails

**Framework: Value-First**

```
SUBJECT: Welcome! Here's what you need to know

Hi [Name],

[Warm welcome + confirmation of what they signed up for]

[Immediate value - what they get right now]

[What to expect next - set expectations]

[One clear next step]

[Signature with personal touch]
```

### 3. Promotional Emails

**Framework: PAS (Problem-Agitate-Solution)**

```
SUBJECT: [Problem-aware or solution-focused hook]

[PROBLEM - State the pain point they experience]

[AGITATE - Amplify the consequences/frustration]

[SOLUTION - Your offer as the answer]

[PROOF - Testimonial or result]

[CTA - Clear action with urgency if appropriate]
```

### 4. Newsletter Emails

**Framework: Value-Packed**

```
SUBJECT: [This week/month's main insight]

[Personal opening - current event, observation]

[Main content piece - valuable insight/story]

[Secondary content - quick tips, links]

[Community element - question, highlight]

[CTA - soft, engagement-focused]
```

### 5. Follow-Up Emails

**Framework: BAB (Before-After-Bridge)**

```
SUBJECT: Quick follow-up on [topic]

[BEFORE - Reference previous email/situation]

[AFTER - Paint the outcome they want]

[BRIDGE - Simple path to get there]

[Soft CTA]
```

## Subject Line Formulas

### High-Converting Patterns

| Pattern | Example | Best For |
|---------|---------|----------|
| Curiosity Gap | "The one thing [audience] gets wrong about [topic]" | Cold, newsletter |
| Benefit-Driven | "Get [result] in [timeframe]" | Promotional |
| Personal | "Quick question, [Name]" | Follow-up |
| Urgency | "[X] hours left: [offer]" | Promotional |
| Social Proof | "[Number] [people] already [action]" | Promotional |
| How-To | "How to [achieve result] without [pain]" | Newsletter |
| Story | "How [person] [achieved result]" | Case study |
| Question | "Are you still [experiencing problem]?" | Re-engagement |

### Subject Line Best Practices

- **Length**: 28-39 characters optimal for mobile
- **Personalization**: Use name sparingly, context always
- **Emojis**: Test carefully, platform-dependent
- **Avoid**: ALL CAPS, excessive punctuation, spam triggers
- **Test**: Always write 3-5 variants

## 3-Mode Workflow

### MODE 1: PLAN

1. **Understand Email Context**
   ```
   - Email type (cold, welcome, promo, etc.)
   - Target audience
   - Goal (click, reply, purchase, etc.)
   - Where in funnel/sequence
   ```

2. **Check References**
   ```bash
   # Check example emails
   ls references/examples/emails/

   # Analyze successful emails
   python scripts/content/analyze_emails.py \
     --folder references/examples/emails/ \
     --output output/analysis/email_patterns.json
   ```

3. **Select Framework**
   - Match framework to email purpose
   - Note any brand voice requirements
   - Plan subject line variants

4. **Document Plan**
   ```markdown
   ## Email Plan

   ### Email Type: [type]
   ### Framework: [AIDA/PAS/BAB/etc.]
   ### Goal: [click/reply/purchase]

   ### Audience
   - Who: [description]
   - Pain points: [list]
   - Desires: [list]

   ### Key Elements
   - Hook: [concept]
   - Value prop: [main benefit]
   - CTA: [action]
   ```

### MODE 2: CLARIFY

**Essential Questions:**
- "What's the primary goal of this email?"
- "Who specifically is receiving this?"
- "What action should they take?"
- "Any specific offer or deadline?"

**Context Questions:**
- "Is this part of a sequence or standalone?"
- "What have they received before?"
- "What's their relationship with your brand?"

**Style Questions:**
- "Formal or casual tone?"
- "Use emojis?"
- "Long-form or brief?"

### MODE 3: IMPLEMENT

1. **Write Email**
   ```bash
   # Generate email with framework
   python scripts/content/write_email.py \
     --type promotional \
     --framework PAS \
     --topic "Product Launch" \
     --output output/content/emails/
   ```

2. **Create Subject Variants**
   - Write 5 subject line options
   - Mix different formulas
   - Include preview text

3. **Save Output**
   ```
   output/content/emails/
   ├── [date]_[type]_email.md
   └── [date]_[type]_subject_variants.txt
   ```

## Email Templates

### Cold Email Template
```markdown
SUBJECT: [Curiosity hook / Pattern interrupt]
PREVIEW: [Extend subject / Add intrigue]

Hi [Name],

[Opening that shows you've done research - NOT "I hope this finds you well"]

[One sentence about their problem/goal]

[How you can help - brief, specific value]

[Proof point - one line of credibility]

[Simple CTA - reply, not a meeting request]

[Short signature]

P.S. [Secondary hook or value add]
```

### Promotional Email Template
```markdown
SUBJECT: [Benefit-driven or urgency hook]
PREVIEW: [Extend value prop]

[Hook that addresses pain point or desire]

Here's the thing about [problem]:
[Agitate with consequences or missed opportunities]

That's why we created [solution].

With [Product/Service], you get:
• [Benefit 1 - most important]
• [Benefit 2]
• [Benefit 3]

[Social proof - testimonial or result]

[CTA button text: Action-oriented, benefit-focused]

[Urgency or scarcity if real]

[Signature]
```

### Newsletter Template
```markdown
SUBJECT: [This issue's main insight]
PREVIEW: [Tease additional value]

Hey [Name],

[Personal, timely opening - 2 sentences max]

---

## [Main Content Headline]

[Key insight or story - 150-300 words]

[Actionable takeaway]

---

## Quick Hits

• [Tip 1]
• [Tip 2]
• [Link to resource]

---

[Engagement question or community highlight]

[Soft CTA]

[Signature]
```

## Personalization Variables

Common merge fields to use:
- `{{first_name}}` - Recipient's first name
- `{{company}}` - Their company name
- `{{industry}}` - Their industry
- `{{pain_point}}` - Specific to their situation
- `{{previous_action}}` - What they did before
- `{{custom_1}}` - Campaign-specific

## Example Interactions

### "Write a cold email for B2B SaaS"
```
[PLAN]
- Cold outreach to business prospects
- AIDA framework best fit
- Goal: Get reply or meeting

[CLARIFY]
- "What's your product/service?"
- "Who's the ideal prospect (title, company size)?"
- "What problem do you solve?"
- "Any social proof to include?"

[IMPLEMENT]
- Write email with AIDA structure
- Create 5 subject line variants
- Include personalization notes
```

### "Create a promotional email for my course"
```
[PLAN]
- Promotional email for product
- PAS framework (problem-solution)
- Goal: Click to sales page

[CLARIFY]
- "What's the course about?"
- "Who is it for?"
- "Any launch deadline or bonus?"
- "Testimonials to include?"

[IMPLEMENT]
- Write email with PAS structure
- Emphasize transformation
- Strong CTA with urgency
```

### "Write a re-engagement email"
```
[PLAN]
- Re-engage inactive subscribers
- Emotional + value approach
- Goal: Reactivate or clean list

[CLARIFY]
- "How long have they been inactive?"
- "What did they originally sign up for?"
- "Any incentive to offer?"

[IMPLEMENT]
- Write empathetic email
- Remind of value
- Clear stay-or-go CTA
```

## Spam Avoidance

**Avoid these triggers:**
- ALL CAPS in subject
- Excessive exclamation marks!!!
- "Free" as first word
- "Act now" / "Limited time"
- "Click here" as CTA text
- Too many links
- Image-heavy / text-light ratio

**Maintain deliverability:**
- Balance text to image ratio
- Include plain text version
- Use proper sender authentication
- Consistent sending patterns

## Output Files

Email content saved to:
- `output/content/emails/[type]/` - Organized by email type
- `output/content/emails/subjects.txt` - Subject line collection
- `output/content/emails/swipe_file.md` - Best examples

## Quality Checklist

Before finalizing any email:
- [ ] Subject line under 40 characters
- [ ] Preview text complements subject
- [ ] Opening line earns attention
- [ ] Single clear CTA
- [ ] Mobile-friendly length
- [ ] Personalization where appropriate
- [ ] Brand voice consistent
- [ ] No spam triggers
- [ ] Value before ask
