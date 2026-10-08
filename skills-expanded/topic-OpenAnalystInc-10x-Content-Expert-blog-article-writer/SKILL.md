---
name: blog-article-writer
description: |
  Creates long-form content including blog posts, articles, guides, and thought leadership pieces.
  Uses SEO best practices, storytelling frameworks, and learns from reference materials.
  Use this skill for blog posts, articles, how-to guides, listicles, case studies, and
  any long-form written content.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - WebSearch
---

# Blog & Article Writer Skill

> **QUICK REFERENCE**
> - **Output folder**: `output/content/blogs/`
> - **File naming**: `YYYY-MM-DD_topic_blog.md`
> - **Sample script**: `scripts/samples/sample_blog_content.py`
> - **Run with**: `.venv\Scripts\python.exe scripts/samples/sample_blog_content.py`
> - **References**: Check `references/` folder for brand voice and examples before writing
> - **Frameworks**: AIDA, PAS, Hook-Story-Offer (see `content-frameworks` skill)
> - **Python**: ALWAYS use `.venv\Scripts\python.exe` (never bare `python`)

Creates compelling long-form content that ranks, engages, and converts.

## Scope of This Skill

**This skill handles:**
- Blog posts
- How-to guides
- Listicles
- Thought leadership articles
- Case studies
- Ultimate guides
- Comparison posts
- News/trend articles
- Guest posts
- Pillar content

**NOT handled by this skill:**
- Short social posts → Use `social-media-writer`
- Email copy → Use `email-copywriter`
- Visual content → Creates written content only

## Article Types & Structures

### 1. How-To Guide

```markdown
# How to [Achieve Result] in [Timeframe]

**Hook**: [Why this matters now]

**Introduction**:
- Problem statement
- What you'll learn
- Why trust this guide

## What You'll Need / Prerequisites
- [Requirement 1]
- [Requirement 2]

## Step 1: [Action Verb + Outcome]
[Detailed instructions]
[Pro tip or warning]

## Step 2: [Action Verb + Outcome]
...

## Common Mistakes to Avoid
1. [Mistake + how to fix]
2. [Mistake + how to fix]

## Conclusion
- Summary of steps
- Next action to take
- CTA

## FAQ
[Address common questions]
```

### 2. Listicle

```markdown
# [Number] [Adjective] [Things] for [Audience] in [Year]

**Hook**: [Pattern interrupt or stat]

**Introduction**:
- Why this list matters
- How it was curated
- Quick preview

## 1. [Item Name]
[Why it's on the list]
[Key benefit]
[How to use/apply]

## 2. [Item Name]
...

## Bonus: [Extra Item]

## How to Choose the Right One
[Comparison or decision framework]

## Conclusion + CTA
```

### 3. Thought Leadership

```markdown
# [Bold Claim] : Why [Common Belief] Is Wrong

**Hook**: [Contrarian opening]

**Introduction**:
- The conventional wisdom
- Why it's outdated/wrong
- Your alternative view

## The Problem with [Conventional Approach]
[Evidence and examples]

## A Better Way: [Your Framework]
[Your methodology]

## Evidence This Works
[Case studies, data, testimonials]

## How to Implement
[Actionable steps]

## Conclusion
- Key shift in thinking
- Call to action
```

### 4. Case Study

```markdown
# How [Client] [Achieved Result] in [Timeframe]

**Quick Stats**:
- [Key metric 1]: [Result]
- [Key metric 2]: [Result]
- [Key metric 3]: [Result]

## The Challenge
[Client's situation and problems]

## The Solution
[What was implemented]

## The Process
### Phase 1: [Name]
### Phase 2: [Name]
### Phase 3: [Name]

## The Results
[Detailed outcomes with data]

## Key Takeaways
[What readers can apply]

## Ready to [Achieve Similar Results]?
[CTA]
```

### 5. Ultimate Guide

```markdown
# The Ultimate Guide to [Topic] in [Year]

**Table of Contents**
[Linked sections]

## Introduction: What is [Topic] and Why Does It Matter?

## Part 1: [Foundation/Basics]
### Chapter 1.1
### Chapter 1.2

## Part 2: [Intermediate/Strategy]
### Chapter 2.1
### Chapter 2.2

## Part 3: [Advanced/Tactics]
### Chapter 3.1
### Chapter 3.2

## Part 4: [Tools & Resources]

## Conclusion: Your [Topic] Action Plan

## FAQ
```

## SEO Best Practices

### On-Page Elements

| Element | Best Practice |
|---------|--------------|
| Title | 55-60 chars, keyword near front |
| Meta Description | 150-160 chars, include CTA |
| H1 | One per page, includes keyword |
| H2/H3 | Include secondary keywords |
| URL | Short, includes primary keyword |
| First 100 Words | Include primary keyword naturally |
| Images | Alt text with keywords |
| Internal Links | 2-5 to relevant content |
| External Links | 1-3 to authoritative sources |

### Keyword Integration

- **Primary keyword**: In title, H1, first paragraph, conclusion
- **Secondary keywords**: In H2s, throughout body
- **LSI keywords**: Related terms, synonyms
- **Natural density**: Write for humans first

### Content Length Guidelines

| Article Type | Optimal Length |
|-------------|---------------|
| News/Updates | 300-500 words |
| Standard Blog | 1,000-1,500 words |
| How-To Guide | 1,500-2,500 words |
| Ultimate Guide | 3,000-7,000 words |
| Pillar Content | 5,000-10,000 words |

## 3-Mode Workflow

### MODE 1: PLAN

1. **Understand Content Goals**
   ```
   - Topic and angle
   - Target audience
   - SEO keywords (if any)
   - Content type/format
   - Desired length
   - Publication context
   ```

2. **Research & References**
   ```bash
   # Check existing content on topic
   ls references/examples/blogs/

   # Analyze successful articles
   python scripts/content/analyze_articles.py \
     --folder references/examples/blogs/ \
     --output output/analysis/article_patterns.json

   # Web research for current info
   # Use WebSearch tool for latest data
   ```

3. **Create Outline**
   ```bash
   python scripts/content/generate_blog_outline.py \
     --topic "Content Marketing" \
     --type how-to \
     --keywords "content marketing, strategy, ROI" \
     --output output/content/blogs/
   ```

4. **Document Plan**
   ```markdown
   ## Article Plan

   ### Topic
   [Main subject]

   ### Angle
   [Unique perspective/hook]

   ### Type
   [How-to/Listicle/Thought Leadership/etc.]

   ### Target Keywords
   - Primary: [keyword]
   - Secondary: [keywords]

   ### Outline
   [H2 structure]

   ### Target Length
   [Word count]

   ### References
   [Sources to cite]
   ```

### MODE 2: CLARIFY

**Essential Questions:**
- "What's the main topic and angle?"
- "Who is the target reader?"
- "Are there specific keywords to target?"
- "What's the desired word count?"

**Context Questions:**
- "Is this for SEO, thought leadership, or both?"
- "Any specific points you want to cover?"
- "Sources or references to include?"

**Style Questions:**
- "Formal or conversational tone?"
- "First person or third person?"
- "Technical or accessible language?"

### MODE 3: IMPLEMENT

1. **Write Article**
   ```bash
   python scripts/content/write_article.py \
     --outline output/content/blogs/outline.md \
     --tone conversational \
     --length 2000 \
     --output output/content/blogs/
   ```

2. **Optimize for SEO**
   - Check keyword placement
   - Write meta description
   - Add internal/external links

3. **Save Output**
   ```
   output/content/blogs/
   ├── [date]_[topic]/
   │   ├── outline.md
   │   ├── draft.md
   │   ├── meta.json
   │   └── images_needed.txt
   ```

## Writing Guidelines

### Opening Hooks

| Type | Example |
|------|---------|
| Stat | "73% of B2B marketers say content marketing increases engagement." |
| Question | "What if everything you knew about [topic] was wrong?" |
| Story | "Last year, I made a $50,000 mistake with my content strategy." |
| Bold Claim | "Most content marketing advice is dead wrong. Here's why." |
| Problem | "You're creating content. You're posting consistently. But nothing's working." |

### Paragraph Guidelines

- **Short paragraphs**: 2-4 sentences max
- **One idea per paragraph**
- **Transition sentences** between sections
- **White space** for readability
- **Subheadings** every 200-300 words

### Bullet Point Guidelines

- Use for lists of 3+ items
- Start each with action verb or parallel structure
- Keep to one line when possible
- Don't overuse - save for scannable info

### Conclusion Best Practices

1. **Summarize** key points (not repeat verbatim)
2. **Reinforce** the main takeaway
3. **Call to action** - what should they do next?
4. **Optional**: Question to spark comments

## Example Interactions

### "Write a blog post about email marketing"
```
[PLAN]
- Topic: Email marketing
- Determine angle and type
- Research current best practices

[CLARIFY]
- "What specific aspect - strategy, copy, automation?"
- "Target audience - beginners or advanced?"
- "Any keywords to target?"
- "Desired word count?"

[IMPLEMENT]
- Create comprehensive outline
- Write full article
- Optimize for SEO
- Add meta description
```

### "Create a how-to guide for LinkedIn growth"
```
[PLAN]
- How-to format
- Step-by-step structure
- Practical, actionable content

[CLARIFY]
- "What audience - job seekers, founders, creators?"
- "Any specific strategies you want included?"
- "Case studies or examples to reference?"

[IMPLEMENT]
- Detailed step-by-step guide
- Include pro tips and common mistakes
- Add FAQ section
- Optimize for search
```

### "Write a thought leadership piece about AI in marketing"
```
[PLAN]
- Thought leadership format
- Need unique angle/perspective
- Research current discourse

[CLARIFY]
- "What's your unique take on AI in marketing?"
- "Contrarian view or forward-looking?"
- "Any original data or experience to share?"

[IMPLEMENT]
- Bold opening hook
- Build argument with evidence
- Practical implications
- Strong conclusion with POV
```

## Editing Checklist

### Structure
- [ ] Compelling headline with keyword
- [ ] Hook in first 100 words
- [ ] Clear H2 structure
- [ ] Logical flow between sections
- [ ] Strong conclusion with CTA

### Content
- [ ] Delivers on headline promise
- [ ] Provides unique value
- [ ] Supported by evidence/examples
- [ ] Actionable takeaways

### Style
- [ ] Appropriate tone for audience
- [ ] Short paragraphs (2-4 sentences)
- [ ] Active voice primarily
- [ ] Jargon-free (or explained)
- [ ] Scannable with subheads/bullets

### SEO
- [ ] Primary keyword in title, H1, first 100 words
- [ ] Secondary keywords in H2s
- [ ] Meta description (150-160 chars)
- [ ] Internal links added
- [ ] External links to authority sources

### Readability
- [ ] Grade level appropriate
- [ ] No walls of text
- [ ] Transition sentences
- [ ] Formatting aids scanning

## Output Files

Blog content saved to:
- `output/content/blogs/[topic]/draft.md` - Full article
- `output/content/blogs/[topic]/outline.md` - Structure
- `output/content/blogs/[topic]/meta.json` - SEO metadata
- `output/content/blogs/swipe_file.md` - Best examples

## Word Count Guidelines

When given a target, aim for:
- Within 10% of target for standard articles
- Can go over for comprehensive guides
- Better to be thorough than padded
- Every word should earn its place
