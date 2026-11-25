---
name: hook-generator
description: |
  Generates powerful hooks, headlines, CTAs, and attention-grabbing opening lines.
  Uses proven formulas and psychological triggers. Use this skill when you need
  subject lines, social media hooks, ad headlines, CTAs, or any content that must
  capture attention instantly.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Hook Generator Skill

> **QUICK REFERENCE**
> - **Output folder**: `output/content/hooks/`
> - **File naming**: `YYYY-MM-DD_topic_hooks.md`
> - **Sample script**: `scripts/samples/sample_hook_generation.py`
> - **Run with**: `.venv\Scripts\python.exe scripts/samples/sample_hook_generation.py`
> - **8 hook formulas**: Question, Stat, Bold Claim, Story, How-To, Contrarian, Social Proof, Urgency
> - **Python**: ALWAYS use `.venv\Scripts\python.exe` (never bare `python`)

Creates attention-grabbing hooks, headlines, and CTAs that stop the scroll and drive action.

## Scope of This Skill

**This skill handles:**
- Email subject lines
- Social media hooks (first 3 lines)
- Ad headlines
- Blog/article titles
- Video titles and thumbnails text
- Call-to-action copy
- Landing page headlines
- Webinar/event titles
- Slide headlines

**NOT handled by this skill:**
- Full email body → Use `email-copywriter`
- Full social posts → Use `social-media-writer`
- Full articles → Use `blog-article-writer`

## The Psychology of Hooks

### Emotional Triggers

| Trigger | Why It Works | Example |
|---------|--------------|---------|
| **Curiosity** | Information gap creates tension | "The one thing top creators never tell you" |
| **Fear** | Loss aversion is powerful | "The mistake that's killing your growth" |
| **Urgency** | Scarcity drives action | "24 hours left to change your career" |
| **Surprise** | Pattern interrupt grabs attention | "Why I stopped posting on LinkedIn" |
| **Specificity** | Concrete beats vague | "How I grew from 0 to 10K in 47 days" |
| **Controversy** | Disagree = engagement | "Unpopular opinion: Daily posting is a scam" |
| **Social Proof** | Validation reduces risk | "Why 50,000+ marketers read this daily" |
| **Identity** | People want to belong | "What elite performers do differently" |

### Power Words

**Curiosity Words:**
secret, hidden, revealed, discover, uncover, truth, mystery, insider, little-known

**Urgency Words:**
now, today, limited, deadline, expires, final, last chance, immediately

**Exclusivity Words:**
exclusive, members-only, invitation, private, elite, premium, VIP

**Transformation Words:**
transform, revolutionize, breakthrough, unlock, master, dominate, supercharge

**Trust Words:**
proven, research-backed, data-driven, guaranteed, tested, verified, authentic

**Negative Words (high engagement):**
mistake, wrong, fail, avoid, stop, never, warning, problem, crisis

## Hook Formulas

### Universal Formulas

1. **The Curiosity Gap**
   ```
   "What [authority/group] know about [topic] that you don't"
   "The [adjective] truth about [topic]"
   "What nobody tells you about [topic]"
   ```

2. **The Contrarian**
   ```
   "Why [common advice] is wrong"
   "Unpopular opinion: [statement]"
   "Stop [common action]. Do this instead."
   ```

3. **The Number**
   ```
   "[Number] [things] to [achieve result]"
   "I spent [time/money] learning [topic]. Here's [what I learned]"
   "[Number] mistakes [killing/hurting] your [goal]"
   ```

4. **The Story**
   ```
   "I [failed/succeeded] at [thing]. Here's what I learned."
   "[Time] ago, I was [bad state]. Now I'm [good state]."
   "This [event] changed everything about how I [do thing]"
   ```

5. **The Question**
   ```
   "What if [possibility]?"
   "Why do [successful people] always [do thing]?"
   "Are you making these [topic] mistakes?"
   ```

6. **The Direct Benefit**
   ```
   "How to [achieve result] in [timeframe]"
   "Get [result] without [pain point]"
   "The fastest way to [achieve goal]"
   ```

7. **The Social Proof**
   ```
   "How [person/company] [achieved result]"
   "[Number] [people] are already [doing thing]"
   "[Authority] recommends this [approach]"
   ```

8. **The Challenge**
   ```
   "Most people can't [do thing]. Can you?"
   "Only [percentage] of [people] know this"
   "The [topic] test that stumps [most people]"
   ```

## Platform-Specific Hooks

### Email Subject Lines (28-39 chars optimal)

**Formulas:**
- `Quick question about [their thing]`
- `[Name], [curiosity hook]`
- `re: [topic they care about]`
- `[Number] [things] for [result]`
- `Did you see this?`
- `I noticed [observation]`
- `Bad news about [topic]...`
- `You're invited: [exclusive thing]`

**Examples:**
```
Quick question about your content
3 things killing your email opens
Did you see this LinkedIn post?
You're doing [topic] wrong
I have a confession...
This changed my business
```

### Social Media (First 3 Lines)

**LinkedIn/Facebook:**
```
[Bold statement or question]

↓

[Promise of what's coming]
```

**Twitter:**
```
[Pattern interrupt or bold claim]:
```

**Examples:**
```
I fired my best client yesterday.

Here's why it was the best decision I ever made:
---
Stop creating content.

Start creating conversations.

Here's the difference:
---
$0 to $100K in 12 months.

No paid ads. No big following. No luck.

Just this system:
```

### Video Titles (60 chars max)

**Formulas:**
- `How I [achieved result] in [timeframe]`
- `I Tried [thing] for [time]. Here's What Happened`
- `[Number] [Topic] Mistakes You're Making Right Now`
- `Why [Common Thing] Doesn't Work (And What Does)`
- `The [Topic] They Don't Want You to Know`

### Ad Headlines

**Formulas:**
- `[Result] in [timeframe] or your money back`
- `Finally, a [product] that actually [works]`
- `[Number]+ [people] can't be wrong`
- `Tired of [pain point]? Try this.`
- `What [authority] uses for [result]`

### Landing Page Headlines

**Formulas:**
- `[Big result] without [big pain]`
- `The [solution] for [specific audience]`
- `[Result] guaranteed, or [safety net]`
- `Join [number] [people] who [achieved result]`
- `[Action verb] your [thing] in [timeframe]`

## CTA Writing

### CTA Formulas

| Type | Formula | Example |
|------|---------|---------|
| **Action** | [Verb] + [Benefit] | "Start Growing Today" |
| **Urgency** | [Verb] + [Time] | "Claim Your Spot Now" |
| **Value** | Get + [Outcome] | "Get Instant Access" |
| **Risk-Free** | [Action] + Risk Reversal | "Try Free for 14 Days" |
| **Exclusive** | [Action] + Scarcity | "Join 500 Members" |
| **Personal** | [Verb] + My + [Thing] | "Build My Strategy" |

### CTA Power Words
- Start, Begin, Launch
- Get, Claim, Grab, Unlock
- Join, Become, Enter
- Download, Access, Try
- Discover, Learn, Master
- Save, Boost, Grow

### Platform-Specific CTAs

**Email:**
- "Reply with [word] to get started"
- "Click here to [get benefit]"
- "Schedule your [thing] now"

**Social Media:**
- "Save this for later"
- "Drop a [emoji] if you agree"
- "Follow for more [topic] tips"
- "Comment [word] and I'll send you [thing]"

**Landing Page:**
- "Start Free Trial"
- "Get [Benefit] Now"
- "Claim Your [Thing]"
- "Join [Number]+ [People]"

## 3-Mode Workflow

### MODE 1: PLAN

1. **Understand Context**
   ```
   - Where will this hook be used?
   - What's the content about?
   - Who's the audience?
   - What action do we want?
   ```

2. **Select Approach**
   - Choose emotional trigger(s)
   - Pick appropriate formula(s)
   - Note any constraints (character limits)

3. **Document Plan**
   ```markdown
   ## Hook Plan

   ### Context
   - Platform: [where]
   - Topic: [what]
   - Audience: [who]
   - Goal: [action]

   ### Approach
   - Trigger: [curiosity/fear/etc.]
   - Formula: [which one]
   - Constraints: [limits]

   ### Will Generate
   - [Number] variants
   ```

### MODE 2: CLARIFY

**Questions:**
- "What's this hook for - email, social, ad, landing page?"
- "What's the main topic or offer?"
- "Who's the target audience?"
- "Any specific angle you want?"
- "Character or word limits?"

### MODE 3: IMPLEMENT

1. **Generate Options**
   - Create 5-10 variants
   - Use different formulas
   - Mix emotional triggers

2. **Evaluate & Rank**
   - Check against best practices
   - Verify character limits
   - Rank by likely performance

3. **Save Output**
   ```
   output/content/hooks/
   ├── [date]_[type]_hooks.md
   ```

## Output Format

```markdown
# [Topic] Hooks

## Context
- Platform: [platform]
- Topic: [topic]
- Character Limit: [limit]

## Top Recommendations

### Option 1 (Recommended)
`[Hook text]`
- Formula: [formula used]
- Trigger: [emotional trigger]
- Character count: [number]

### Option 2
`[Hook text]`
...

## Additional Variants

1. `[Hook]`
2. `[Hook]`
3. `[Hook]`
...

## A/B Testing Suggestion
Test: [Option 1] vs [Option 2]
Hypothesis: [why these differ]
```

## Example Interactions

### "I need subject lines for a product launch email"
```
[PLAN]
- Email subject lines
- Product launch = urgency + benefit
- 28-39 character target

[CLARIFY]
- "What's the product?"
- "Any launch deadline or discount?"
- "Target audience?"

[IMPLEMENT]
10 subject line variants:
1. "It's finally here: [Product]"
2. "[Name], you're getting first access"
3. "Launching today (24hr early access)"
4. "The wait is over"
5. "We built this for you"
...
```

### "Create hooks for LinkedIn posts about productivity"
```
[PLAN]
- LinkedIn first 3 lines
- Productivity topic
- Pattern interrupt hooks

[CLARIFY]
- "What aspect of productivity?"
- "Personal experience or general tips?"
- "Controversial or inspirational?"

[IMPLEMENT]
5 hook options:
1. "I deleted all my productivity apps.
    My output doubled.
    Here's why:"

2. "The most productive people I know
    don't have morning routines.
    They have this instead:"
...
```

### "Write CTAs for a coaching program landing page"
```
[PLAN]
- Landing page CTAs
- Coaching program = transformation
- Mix of action + benefit

[CLARIFY]
- "What transformation do they get?"
- "Price point (affects CTA style)?"
- "Any guarantee to mention?"

[IMPLEMENT]
Primary CTA options:
1. "Start Your Transformation"
2. "Apply Now (Limited Spots)"
3. "Get Your Strategy Session"
4. "Join 500+ Successful [People]"

Secondary CTA options:
1. "See Success Stories"
2. "Download Free Guide First"
...
```

## Testing & Iteration

### A/B Testing Guidelines

- Test ONE element at a time
- Run for statistical significance
- Document learnings

### What to Test
- Curiosity vs. direct benefit
- Question vs. statement
- Numbers vs. no numbers
- Urgency vs. no urgency
- Personal ("you") vs. general

### Tracking Metrics

| Platform | Primary Metric |
|----------|---------------|
| Email | Open rate |
| Social | Engagement rate |
| Ads | CTR |
| Landing page | Conversion rate |
| Video | Click-through rate |

## Output Files

Hooks saved to:
- `output/content/hooks/subjects/` - Email subject lines
- `output/content/hooks/social/` - Social media hooks
- `output/content/hooks/ctas/` - CTAs
- `output/content/hooks/headlines/` - Landing page headlines
- `output/content/hooks/swipe_file.md` - Best performing hooks

## Quality Checklist

- [ ] Creates curiosity or urgency
- [ ] Specific, not vague
- [ ] Benefit or outcome clear
- [ ] Within character limits
- [ ] No spam trigger words
- [ ] Matches audience language
- [ ] Delivers on promise (no clickbait)
