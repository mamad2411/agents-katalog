---
name: content-repurposer
description: |
  Transforms content from one format to another. Takes long-form content and creates
  social posts, emails, presentations, and more. Takes transcripts and creates multiple
  content pieces. Use this skill to maximize ROI from existing content by adapting it
  for different platforms and formats.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Content Repurposer Skill

> **QUICK REFERENCE**
> - **Output folders**: Multiple - depends on repurposed format:
>   - LinkedIn: `output/content/social/linkedin/`
>   - Twitter: `output/content/social/twitter/`
>   - Email: `output/content/emails/`
>   - Blog: `output/content/blogs/`
> - **File naming**: `YYYY-MM-DD_topic_[platform].md`
> - **Sample script**: `scripts/samples/sample_repurpose_content.py`
> - **Run with**: `.venv\Scripts\python.exe scripts/samples/sample_repurpose_content.py`
> - **Input sources**: Transcripts, blog posts, long-form content in `references/` or `input/`
> - **Python**: ALWAYS use `.venv\Scripts\python.exe` (never bare `python`)

Maximize content ROI by transforming one piece into many formats across platforms.

## Scope of This Skill

**This skill handles:**
- Long-form → Social posts
- Transcript → Multiple formats
- Blog → Email content
- Webinar → Blog + social + email
- Podcast → Written content
- Presentation → Articles + social
- Video script → Blog post
- Any format → Any other format

**NOT handled by this skill:**
- Creating from scratch → Use appropriate writer skills
- Audio/video editing → Creates written content only

## The COPE Strategy

**Create Once, Publish Everywhere**

```
                    ┌─→ LinkedIn Posts (5-10)
                    │
                    ├─→ Twitter Thread
                    │
Original Content ───┼─→ Email Newsletter
(Blog/Transcript)   │
                    ├─→ Carousel Script
                    │
                    ├─→ Short-form Video Scripts
                    │
                    └─→ Presentation Slides
```

## Transformation Paths

### From Transcript/Long-form Video

| Output | What to Extract |
|--------|-----------------|
| Blog Post | Main narrative + key points |
| LinkedIn Posts | Individual insights + stories |
| Twitter Thread | Sequential points |
| Email | Single theme + CTA |
| Carousel | Step-by-step or tips |
| Quotes | Memorable one-liners |
| Presentation | Key points + visuals |

### From Blog Post

| Output | What to Extract |
|--------|-----------------|
| LinkedIn Post | Main insight + CTA |
| Twitter Thread | H2s as tweet points |
| Email | Summary + link |
| Carousel | Tips/steps as slides |
| Video Script | Conversational rewrite |
| Infographic Text | Data + key points |
| Podcast Outline | Discussion points |

### From Webinar/Presentation

| Output | What to Extract |
|--------|-----------------|
| Blog Post | Full written version |
| LinkedIn Posts | Each slide = post |
| Email Series | Themes across emails |
| Video Clips | Key moments |
| Carousel | Slide highlights |
| Case Study | Success stories shared |

### From Podcast Episode

| Output | What to Extract |
|--------|-----------------|
| Blog Post | Show notes expanded |
| LinkedIn Posts | Guest quotes + insights |
| Audiograms | Best 60-sec clips |
| Email | Episode summary |
| Social Quotes | Memorable moments |

## Repurposing Framework

### Step 1: Content Audit

```bash
# Analyze source content
python scripts/content/audit_content.py \
  --input references/transcripts/webinar.txt \
  --output output/analysis/content_audit.json

# Output includes:
# - Word count / length
# - Key themes identified
# - Quotable moments
# - Data points / statistics
# - Stories / examples
# - Potential formats
```

### Step 2: Extract Components

| Component | Use For |
|-----------|---------|
| **Key insights** | Social posts, email |
| **Statistics** | Hooks, headlines |
| **Stories** | Long-form, presentations |
| **Quotes** | Social, carousels |
| **Steps/Process** | How-to content |
| **Examples** | Case studies, social proof |
| **Questions** | Engagement posts |

### Step 3: Adapt for Platform

Each platform needs specific adaptation:

**LinkedIn:**
- Hook in first 3 lines
- White space formatting
- Personal/professional tone
- 3-5 hashtags
- Engagement question at end

**Twitter:**
- 280 char limit
- Thread structure for depth
- No links in first tweet
- 1-2 hashtags max

**Email:**
- Personal subject line
- Story-driven opening
- Single CTA
- Mobile-friendly length

**Carousel:**
- One point per slide
- Visual-friendly text
- Strong title slide
- CTA on final slide

## 3-Mode Workflow

### MODE 1: PLAN

1. **Analyze Source Content**
   ```
   - What's the original format?
   - What's the main message?
   - What components can be extracted?
   - Word count / length?
   ```

2. **Identify Opportunities**
   ```bash
   # Analyze content for repurposing
   python scripts/content/analyze_repurpose.py \
     --input [source file] \
     --output output/analysis/repurpose_opportunities.json
   ```

3. **Map Transformations**
   ```markdown
   ## Repurposing Plan

   ### Source Content
   - Type: [Transcript/Blog/etc.]
   - Title: [Name]
   - Length: [Words/minutes]

   ### Extracted Components
   - Key insights: [count]
   - Stories: [count]
   - Quotes: [count]
   - Data points: [count]

   ### Planned Outputs
   | Format | Count | Platform |
   |--------|-------|----------|
   | LinkedIn posts | 5 | LinkedIn |
   | Twitter thread | 1 | Twitter |
   | Email | 1 | Email list |
   | Carousel | 1 | LinkedIn/IG |
   ```

### MODE 2: CLARIFY

**Questions:**
- "What's the source content to repurpose?"
- "Which platforms/formats do you want?"
- "Are all formats equally important or prioritize?"
- "Any specific insights to highlight?"
- "Timeline for this content?"

### MODE 3: IMPLEMENT

1. **Extract & Transform**
   ```bash
   python scripts/content/repurpose_content.py \
     --input references/transcripts/webinar.txt \
     --formats "linkedin,twitter,email,carousel" \
     --output output/content/repurposed/
   ```

2. **Optimize Each Format**
   - Adapt length for platform
   - Add platform-specific elements
   - Ensure standalone value

3. **Save Outputs**
   ```
   output/content/repurposed/
   ├── [date]_[source]/
   │   ├── source_analysis.md
   │   ├── linkedin/
   │   │   ├── post_1.md
   │   │   ├── post_2.md
   │   │   └── ...
   │   ├── twitter/
   │   │   └── thread.md
   │   ├── email/
   │   │   └── newsletter.md
   │   └── carousel/
   │       └── slides.md
   ```

## Output Templates

### Repurposing Report

```markdown
# Content Repurposing: [Source Title]

## Source Analysis
- **Original Format**: [Type]
- **Word Count**: [Count]
- **Main Theme**: [Theme]
- **Key Insights**: [Count]
- **Quotable Moments**: [Count]

## Extracted Content

### Key Insights
1. [Insight 1]
2. [Insight 2]
...

### Best Quotes
1. "[Quote 1]"
2. "[Quote 2]"
...

### Stories/Examples
1. [Story summary]
...

## Created Content

### LinkedIn Posts (X total)
- [Post 1 hook preview]
- [Post 2 hook preview]
...

### Twitter Thread
- [Thread hook]
- [X tweets total]

### Email
- Subject: [Subject line]
- Theme: [Main focus]

### Carousel
- Title: [Carousel title]
- Slides: [Count]

## Content Calendar Suggestion
| Day | Platform | Content |
|-----|----------|---------|
| Mon | LinkedIn | Post 1 |
| Tue | Twitter | Thread |
| Wed | Email | Newsletter |
| Thu | LinkedIn | Post 2 |
...
```

### Individual Outputs

Each repurposed piece saved with:
- Full content ready to publish
- Platform-specific formatting
- Hashtags/CTAs included
- Link back to source (if needed)

## Repurposing Examples

### Blog Post → Social Content

**Source**: 2000-word blog on "Email Marketing Mistakes"

**Output**:
```
LinkedIn Posts:
1. Hook from intro + main insight
2. Mistake #1 expanded as story
3. Mistake #2 with tip
4. Data point + contrarian take
5. Conclusion as advice post

Twitter Thread:
1/ Hook: "I've sent 10M+ emails..."
2/ Context
3-7/ Each mistake (one per tweet)
8/ Summary
9/ CTA

Email:
- Subject: "Are you making these email mistakes?"
- Body: Best 3 insights + link to full post

Carousel:
- Slide 1: "5 Email Mistakes Costing You Opens"
- Slides 2-6: One mistake each
- Slide 7: What to do instead
- Slide 8: CTA
```

### Webinar → Multi-format

**Source**: 60-minute webinar on "Content Strategy"

**Output**:
```
Blog Post:
- Full written summary (2500 words)
- Includes quotes, examples, framework

LinkedIn Posts (10):
- Each major point = separate post
- Stories shared = story posts
- Q&A highlights

Email Series (3):
- Email 1: Main framework + replay link
- Email 2: Top 3 takeaways
- Email 3: Implementation guide

Presentation:
- Cleaned up slides for SlideShare
- Added context slides

Short Video Scripts (5):
- Key moments for Reels/Shorts
- 60-second scripts each
```

## Best Practices

### Maintain Context
- Each piece should stand alone
- Don't assume prior knowledge
- Add necessary context

### Platform Native
- Don't just copy-paste
- Adapt tone and format
- Use platform features

### Link Strategically
- Not every piece needs a link
- Native content often performs better
- Link when there's clear value

### Schedule Strategically
- Space out repurposed content
- Mix with other content types
- Don't flood same audience

## Example Interactions

### "Turn my webinar transcript into social content"
```
[PLAN]
- Analyze transcript for content
- Identify key insights, quotes, stories
- Map to social platforms

[CLARIFY]
- "Which platforms - LinkedIn, Twitter, both?"
- "How many posts do you want?"
- "Any key moments to prioritize?"
- "Include link to replay?"

[IMPLEMENT]
- Extract all usable content
- Create 10 LinkedIn posts
- Create Twitter thread
- Create 1 email summary
- Provide content calendar
```

### "I have a blog post, maximize its reach"
```
[PLAN]
- Read and analyze blog post
- Extract components
- Create multi-platform plan

[CLARIFY]
- "Which platforms are you active on?"
- "Want carousel content too?"
- "Should everything link back to blog?"

[IMPLEMENT]
- Create 5 LinkedIn posts
- Create Twitter thread
- Create newsletter excerpt
- Create carousel script
- Provide posting schedule
```

### "Repurpose my podcast episode"
```
[PLAN]
- Analyze transcript
- Find quotable moments
- Identify shareable insights

[CLARIFY]
- "Want to highlight guest or topic?"
- "Video available for clips?"
- "Full show notes or just social?"

[IMPLEMENT]
- Create blog show notes
- Create social posts with quotes
- Create email announcement
- Suggest audiogram moments
```

## Output Files

Repurposed content saved to:
- `output/content/repurposed/[project]/` - All formats
- `output/content/repurposed/[project]/calendar.md` - Posting schedule
- `output/content/repurposed/[project]/analysis.md` - Source breakdown

## Quality Checklist

- [ ] Each piece stands alone
- [ ] Platform-appropriate format
- [ ] Consistent message across formats
- [ ] Proper attribution if needed
- [ ] Hashtags/CTAs included
- [ ] Links where appropriate
- [ ] Posting schedule provided
