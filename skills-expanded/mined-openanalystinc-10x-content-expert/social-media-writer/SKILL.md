---
name: social-media-writer
description: |
  Creates engaging social media content for LinkedIn, Twitter/X, Instagram, and other platforms.
  Uses proven hook formulas, platform-specific best practices, and learns from reference examples.
  Generates posts, carousels content, thread scripts, and engagement content. Use this skill
  for any social media content creation needs.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Social Media Writer Skill

> **QUICK REFERENCE**
> - **LinkedIn output**: `output/content/social/linkedin/`
> - **Twitter output**: `output/content/social/twitter/`
> - **Instagram output**: `output/content/social/instagram/`
> - **Naming**: `YYYY-MM-DD_topic_platform.md`
> - **Sample script**: `scripts/samples/sample_social_content.py`
> - **Check references first**: `references/examples/social/`

Expert social media content creation for engagement and growth across platforms.

## Scope of This Skill

**This skill handles:**
- LinkedIn posts and articles
- Twitter/X posts and threads
- Instagram captions
- Facebook posts
- Carousel content (text for slides)
- Thread scripts
- Hashtag strategies
- Engagement content
- Repurposed content for social

**NOT handled by this skill:**
- Creating visual designs → Use `local-pptx-editor` or design tools
- Scheduling posts → Creates content only
- Analytics → Creates content only

## Platform Specifications

### LinkedIn

**Optimal Post Structure:**
```
[HOOK - First 3 lines visible before "see more"]

[VALUE - Main content, insights, story]

[CTA - Engagement question or action]

[HASHTAGS - 3-5 relevant]
```

**Best Practices:**
- Character limit: 3,000 (optimal: 1,200-1,500)
- First 3 lines are critical (before "see more")
- White space increases readability (+25% engagement)
- Carousels/PDFs get highest dwell time
- Best times: Tue-Thu, 8-11 AM
- Comments > Likes (15x more valuable)

### Twitter/X

**Optimal Structure:**
```
[HOOK - Pattern interrupt or bold statement]

[BODY - Value or insight]

[CTA - Engage or follow action]
```

**Thread Structure:**
```
1/ [Hook that earns the click]

2/ [Context or background]

3-8/ [Main points, one per tweet]

9/ [Summary or key takeaway]

10/ [CTA + thread link]
```

**Best Practices:**
- Single tweet: 280 characters (optimal: 100-150)
- Threads: 5-12 tweets optimal
- No links in first tweet (kills reach)
- Hashtags: 1-2 maximum
- Best times: 8-10 AM, 12-1 PM

### Instagram

**Caption Structure:**
```
[HOOK - Stop the scroll]

[BODY - Story or value]

[CTA - Engagement action]

.
.
.

[HASHTAGS - 5-15 in separate block]
```

**Best Practices:**
- Character limit: 2,200 (optimal: 150-300)
- First line must hook
- Emojis: Yes, but strategic
- Hashtags: Mix popular + niche
- CTA: Ask questions, save prompts

## Hook Formulas

### Opening Hook Types

| Type | Formula | Example |
|------|---------|---------|
| Curiosity | "What nobody tells you about [X]" | "What nobody tells you about growing on LinkedIn" |
| Contrarian | "Unpopular opinion: [statement]" | "Unpopular opinion: followers don't matter" |
| Story | "Last [time], I [experience]" | "Last week, I lost a $50K deal" |
| Question | "What if I told you [possibility]?" | "What if I told you posting daily hurts growth?" |
| Number | "[X] [things] I wish I knew about [Y]" | "5 things I wish I knew about content creation" |
| Mistake | "I made a [X] mistake" | "I made a $10,000 mistake with my first launch" |
| Bold claim | "[X] is [surprising adjective]" | "Your content strategy is backwards" |
| Social proof | "[X] people [result]" | "10,000 people asked me this question" |

### The Hook-Value-CTA Framework

```
HOOK (First 3 lines):
- Pattern interrupt OR
- Curiosity gap OR
- Bold/contrarian statement OR
- Relatable story opening

VALUE (Body):
- 3-5 key insights OR
- Story with lesson OR
- Framework/process OR
- Practical tips

CTA (Closing):
- Question for comments OR
- Follow for more OR
- Save/share prompt OR
- Link in bio/comments
```

## 3-Mode Workflow

### MODE 1: PLAN

1. **Understand Content Goals**
   ```
   - Platform(s): LinkedIn, Twitter, Instagram?
   - Purpose: Awareness, engagement, conversion?
   - Topic: What message/value to share?
   - Format: Single post, carousel, thread?
   ```

2. **Check References**
   ```bash
   # Check social media examples
   ls references/examples/social/

   # Analyze top-performing posts
   python scripts/content/analyze_social.py \
     --folder references/examples/social/linkedin/ \
     --output output/analysis/linkedin_patterns.json
   ```

3. **Select Hook Strategy**
   - Match hook type to content
   - Consider audience awareness level
   - Plan CTA approach

4. **Document Plan**
   ```markdown
   ## Social Content Plan

   ### Platform: [LinkedIn/Twitter/Instagram]
   ### Format: [Post/Thread/Carousel]
   ### Goal: [Engagement/Awareness/Conversion]

   ### Topic
   [Main message]

   ### Hook Approach
   [Hook type and angle]

   ### Key Points
   1. [Point 1]
   2. [Point 2]
   3. [Point 3]

   ### CTA
   [Engagement action]
   ```

### MODE 2: CLARIFY

**Essential Questions:**
- "Which platform(s) is this for?"
- "What's the main message or insight?"
- "Is this educational, promotional, or personal?"
- "Any specific CTA you want?"

**Style Questions:**
- "What tone - professional, casual, provocative?"
- "Use emojis?"
- "How personal/vulnerable should it be?"

**Format Questions:**
- "Single post or carousel/thread?"
- "Should I create variants for A/B testing?"

### MODE 3: IMPLEMENT

1. **Write Content**
   ```bash
   # Generate social post
   python scripts/content/write_social.py \
     --platform linkedin \
     --topic "Content creation tips" \
     --hook-type curiosity \
     --output output/content/social/
   ```

2. **Create Variants**
   - Write 3 hook variations
   - Different CTA options
   - A/B testing versions

3. **Add Hashtags**
   - Platform-appropriate count
   - Mix of popular + niche

4. **Save Output**
   ```
   output/content/social/
   ├── linkedin/
   │   ├── [date]_[topic]_post.md
   │   └── [date]_[topic]_variants.md
   └── twitter/
       └── [date]_[topic]_thread.md
   ```

## Content Templates

### LinkedIn Post Template
```markdown
[HOOK - 3 lines max]
[Bold claim, question, or story opening]

[Empty line for visual break]

Here's what I learned:

↳ [Point 1 with context]
↳ [Point 2 with context]
↳ [Point 3 with context]
↳ [Point 4 with context]
↳ [Point 5 with context]

[Synthesis or lesson]

[CTA - Question to spark comments]

---

#hashtag1 #hashtag2 #hashtag3
```

### LinkedIn Carousel Script
```markdown
Slide 1: [Hook headline - pattern interrupt]
Slide 2: [Problem statement or context]
Slide 3-8: [One tip/point per slide]
Slide 9: [Summary/recap]
Slide 10: [CTA - Follow, save, comment]

CAPTION:
[Summary of carousel value]
[CTA to view all slides]
```

### Twitter Thread Template
```markdown
1/ [HOOK - Bold statement or promise]

2/ [Context - Why this matters]

3/ [Point 1]
↳ [Supporting detail]

4/ [Point 2]
↳ [Supporting detail]

5/ [Point 3]
↳ [Supporting detail]

6/ [Point 4]
↳ [Supporting detail]

7/ [Point 5]
↳ [Supporting detail]

8/ [Summary + Key takeaway]

9/ [CTA]
If you found this valuable:
• Like/RT the first tweet
• Follow for more [topic]

[Repost of first tweet]
```

### Instagram Caption Template
```markdown
[Hook - First line must stop scroll]

[Story or valuable content - 2-3 paragraphs]

[Lesson or takeaway]

💡 Key insight: [One-liner summary]

[CTA - Double tap, save, comment]

.
.
.

#hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5
```

## Content Ideas by Type

### Educational Posts
- "X things I wish I knew about [topic]"
- "The [X] framework for [result]"
- "How to [achieve result] in [timeframe]"
- "Common [topic] mistakes and how to fix them"
- "[Myth] vs [Reality] in [topic]"

### Story Posts
- "X years ago, I [starting point]. Now I [result]."
- "I just made a [X] mistake. Here's what I learned."
- "A client asked me [question]. Here's my answer."
- "Behind the scenes of [achievement]"

### Engagement Posts
- "Agree or disagree: [statement]"
- "Which do you prefer: [A] or [B]?"
- "Fill in the blank: [topic] is ___"
- "What's your biggest [topic] challenge?"

### Social Proof Posts
- "Client spotlight: [result achieved]"
- "[Number] people have [achieved result]"
- "This feedback made my day: [testimonial]"

## Example Interactions

### "Write a LinkedIn post about productivity"
```
[PLAN]
- LinkedIn single post
- Educational content
- Hook: Contrarian or insight

[CLARIFY]
- "What specific productivity insight do you want to share?"
- "Personal experience or general tips?"
- "Target audience - entrepreneurs, employees, creators?"

[IMPLEMENT]
- Write post with hook-value-CTA
- Create 3 hook variants
- Add appropriate hashtags
```

### "Create a Twitter thread about content creation"
```
[PLAN]
- Twitter thread format
- 8-10 tweets optimal
- Value-packed insights

[CLARIFY]
- "What aspect - strategy, tactics, mindset?"
- "Based on personal experience?"
- "Any specific results to highlight?"

[IMPLEMENT]
- Write thread with strong hook
- One point per tweet
- End with clear CTA
```

### "Turn my blog post into social content"
```
[PLAN]
- Repurpose long-form to social
- Extract key insights
- Create platform-specific versions

[CLARIFY]
- "Which platforms do you want?"
- "Single posts or series?"
- "Direct blog link or native content?"

[IMPLEMENT]
- Extract 5-10 key points
- Create LinkedIn post
- Create Twitter thread
- Optimize for each platform
```

## Hashtag Strategy

### LinkedIn Hashtags
- Use 3-5 hashtags
- Mix: 1 broad + 2-3 niche + 1 branded
- Place at end of post
- Research trending hashtags in your niche

### Twitter Hashtags
- Use 1-2 hashtags maximum
- Only if trending/relevant
- Can place inline or at end
- Less is more

### Instagram Hashtags
- Use 5-15 hashtags
- Mix: Popular (100K+) + Mid (10K-100K) + Niche (<10K)
- Place after caption break
- Save hashtag groups for efficiency

## Output Files

Social content saved to:
- `output/content/social/linkedin/` - LinkedIn posts
- `output/content/social/twitter/` - Twitter posts/threads
- `output/content/social/instagram/` - Instagram captions
- `output/content/social/carousel_scripts/` - Carousel text
- `output/content/social/hashtags.txt` - Hashtag collections

## Quality Checklist

Before posting:
- [ ] Hook earns the "see more" click
- [ ] White space for readability
- [ ] Single clear message
- [ ] Value before ask
- [ ] Platform-appropriate length
- [ ] CTA for engagement
- [ ] Hashtags appropriate for platform
- [ ] No links in first tweet (Twitter)
- [ ] Brand voice consistent
