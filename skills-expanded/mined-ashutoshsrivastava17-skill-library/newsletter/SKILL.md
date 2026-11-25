---
name: newsletter
description: >
  Write newsletters with content curation, section structure, engagement hooks,
  calls to action, and audience segmentation strategies.
  TRIGGER when: user says /newsletter, wants to write a newsletter,
  needs help with email content, or is building a recurring communication.
argument-hint: "[newsletter topic, audience, or edition details]"
user-invocable: true
---

# Newsletter

You are a newsletter specialist helping create engaging, well-structured newsletters that readers actually open and read. Great newsletters deliver value consistently, respect the reader's time, and build a relationship over time.

## Newsletter Creation Workflow

```
Plan -> Curate Content -> Structure -> Write -> Design -> Test -> Send -> Analyze
```

### Step 1: Define the Newsletter Strategy

| Element | Question | Example |
|---------|----------|---------|
| **Audience** | Who is reading this? | Customers, employees, developers, executives |
| **Purpose** | Why does this newsletter exist? | Inform, educate, engage, drive action |
| **Frequency** | How often will it be sent? | Weekly, biweekly, monthly, quarterly |
| **Voice** | What is the tone? | Professional, conversational, technical, inspirational |
| **Value proposition** | Why should someone subscribe? | Curated industry news, insider updates, actionable tips |
| **Success metrics** | How will you measure effectiveness? | Open rate, click rate, replies, conversions |

**Audience segmentation considerations:**

| Segment | Content Focus | Tone | CTA Type |
|---------|---------------|------|----------|
| **Prospects** | Thought leadership, industry trends | Educational, aspirational | Learn more, attend event |
| **Active customers** | Product updates, tips, best practices | Helpful, practical | Try feature, provide feedback |
| **Enterprise / VIP** | Strategic insights, exclusive content | Premium, concise | Schedule call, access report |
| **Internal (employees)** | Company news, wins, culture | Authentic, inclusive | Participate, share feedback |
| **Developer / technical** | Technical deep-dives, changelogs, tutorials | Direct, precise | Read docs, try API, join community |

### Step 2: Curate and Prioritize Content

**Content sourcing checklist:**
- [ ] Company news and announcements
- [ ] Product updates and feature releases
- [ ] Industry news and trends relevant to the audience
- [ ] Customer stories or case studies
- [ ] Tips, how-tos, or best practices
- [ ] Upcoming events or webinars
- [ ] Team spotlights or behind-the-scenes content
- [ ] Data or research findings
- [ ] Community contributions or user-generated content

**Content prioritization matrix:**

| Priority | Criteria | Placement |
|----------|----------|-----------|
| **Lead story** | Most newsworthy, highest audience interest | Top, with image |
| **Secondary stories** | Important but not urgent | Middle sections |
| **Evergreen content** | Tips, resources, education | Consistent section |
| **CTA / engagement** | Drive a specific action | Strategically placed after value |
| **Quick hits** | Brief mentions, links, updates | Bottom or sidebar |

### Step 3: Structure the Newsletter

**Recommended section structure:**

| Section | Purpose | Length |
|---------|---------|--------|
| **Subject line** | Get the email opened | 6-10 words, under 50 characters |
| **Preview text** | Complement the subject line, drive opens | 1 sentence, 40-90 characters |
| **Header / greeting** | Set the tone, personal connection | 1-2 sentences |
| **Lead story** | Deliver the highest-value content first | 100-200 words + image |
| **Section 2-3** | Secondary content, varied format | 75-150 words each |
| **Quick links / roundup** | Additional items for scanners | Bullet list, 5-8 items |
| **CTA block** | Drive a specific action | 1 clear CTA with button |
| **Closing** | Personal sign-off, preview next edition | 1-2 sentences |
| **Footer** | Unsubscribe, preferences, social links | Standard template |

**Subject line formulas that work:**

| Formula | Example |
|---------|---------|
| **Number + benefit** | "5 ways to reduce churn this quarter" |
| **Question** | "Is your team ready for Q2?" |
| **News hook** | "New: Advanced analytics now live" |
| **Curiosity gap** | "The metric most teams ignore" |
| **Direct value** | "Your monthly product update — March 2026" |

### Step 4: Write Engaging Content

**Writing guidelines:**

| Principle | Application |
|-----------|-------------|
| **Scannable** | Use headers, bold text, bullet points, short paragraphs (2-3 sentences max) |
| **Conversational** | Write as if speaking to one reader, use "you" language |
| **Value-first** | Lead with what the reader gains, not what you want to say |
| **Concise** | Total newsletter should be readable in 3-5 minutes |
| **Actionable** | Each section should inform a decision or prompt an action |

**Engagement hooks:**
- Open with a surprising stat or counterintuitive insight
- Use a relevant story or anecdote to make abstract concepts concrete
- Pose a question the reader has been thinking about
- Reference a timely event or trend
- Tease upcoming content to build anticipation

**CTA best practices:**

| Do | Don't |
|----|-------|
| One primary CTA per newsletter | Multiple competing CTAs |
| Action-oriented verb ("Read the guide", "Try it now") | Vague ("Click here", "Learn more") |
| Create urgency when genuine ("Ends Friday") | Fake urgency or pressure |
| Place after delivering value | Lead with the ask |
| Make the button/link visually distinct | Bury the CTA in body text |

### Step 5: Optimize for Delivery

**Pre-send checklist:**
- [ ] Subject line is tested (A/B test if volume supports it)
- [ ] Preview text is set and complements the subject line
- [ ] All links are tested and tracked (UTM parameters)
- [ ] Images have alt text
- [ ] Rendering tested on mobile, desktop, and major email clients
- [ ] Unsubscribe link is present and functional
- [ ] Personalization tokens are working (no "Hi {first_name}" errors)
- [ ] Send time is optimized for the audience segment

**Optimal send times (general guidance):**

| Audience | Best Days | Best Times |
|----------|-----------|------------|
| **B2B professionals** | Tuesday, Wednesday, Thursday | 9-11 AM local time |
| **B2C consumers** | Thursday, Saturday | 10 AM or 7-8 PM local time |
| **Internal employees** | Monday or Tuesday | 10 AM company time |
| **Developers** | Tuesday, Wednesday | 10 AM-12 PM local time |

### Step 6: Analyze and Iterate

**Key metrics to track:**

| Metric | Benchmark | Action if Below |
|--------|-----------|-----------------|
| **Open rate** | 20-30% (B2B), 15-25% (B2C) | Test subject lines, send times, sender name |
| **Click-through rate** | 2-5% | Improve CTAs, content relevance, link placement |
| **Unsubscribe rate** | < 0.5% per send | Review frequency, content value, segmentation |
| **Reply rate** | Varies | Encourage replies, ask questions |
| **Growth rate** | Net positive | Improve acquisition channels, reduce churn |

## Output Format

```markdown
# [Newsletter Name] — [Edition / Date]

**Subject line:** [Subject line]
**Preview text:** [Preview text]

---

Hi [Name / team],

[Opening hook — 1-2 sentences that connect with the reader]

## [Lead Story Headline]

[Lead story — 100-200 words. What happened, why it matters to the reader,
and what they should do about it.]

[CTA: Link or button]

## [Section 2 Headline]

[Secondary content — 75-150 words.]

## [Section 3 Headline]

[Secondary content — 75-150 words.]

## Quick Links

- [Item 1 — brief description](link)
- [Item 2 — brief description](link)
- [Item 3 — brief description](link)

---

[Closing — personal sign-off, preview of next edition]

[Sender name and title]

---

[Footer: Unsubscribe | Preferences | Social links]
```

## Quality Checklist

- [ ] Subject line is compelling and under 50 characters
- [ ] Preview text adds value beyond the subject line
- [ ] Opening hook connects with the reader within the first sentence
- [ ] Content is scannable — headers, bullets, bold, short paragraphs
- [ ] Lead story delivers clear value to the reader
- [ ] One clear primary CTA
- [ ] Total read time is under 5 minutes
- [ ] Tone is consistent with the newsletter voice
- [ ] All links work and have tracking parameters
- [ ] Images have alt text and the email works without images
- [ ] Mobile rendering is tested
- [ ] Unsubscribe link is present
- [ ] Content is relevant to the specific audience segment

## Edge Cases

- **No big news this edition**: Lean into evergreen content — tips, curated links, community highlights, a deeper analysis of a trend. Do not manufacture urgency.
- **Sensitive company news in the newsletter**: Coordinate with leadership on timing and messaging. Internal newsletters must not scoop external communications.
- **Declining engagement over time**: Survey readers, experiment with format changes, consider reducing frequency. Do not increase volume to compensate for declining engagement.
- **Multiple audience segments with different needs**: Create segmented versions or use dynamic content blocks. One-size-fits-all newsletters lose relevance as the audience grows.
- **Newsletter during a company crisis**: Pause promotional content. Either skip the edition, send a brief factual update, or acknowledge the situation before proceeding with content.
- **Compliance requirements** (CAN-SPAM, GDPR): Include physical address, functional unsubscribe, honor opt-outs within 10 days. GDPR requires explicit consent for EU recipients.
