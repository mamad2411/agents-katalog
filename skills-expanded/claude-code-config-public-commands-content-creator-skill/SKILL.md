---
name: content-creator
description: Create SEO-optimized marketing content with consistent brand voice. Includes brand voice analysis, SEO optimization, research assistance, citation management, content frameworks, and social media templates. Use when writing blog posts, articles, newsletters, tutorials, creating social media content, analyzing brand voice, optimizing SEO, planning content calendars, or when user mentions content creation, brand voice, SEO optimization, content research, citations, or content strategy.
license: MIT
metadata:
  version: 2.0.0
  author: Alireza Rezvani
  category: marketing
  domain: content-marketing
  updated: 2025-01-31
  python-tools: brand_voice_analyzer.py, seo_optimizer.py
  tech-stack: SEO, social-media-platforms
---

# Content Creator

Professional-grade content creation suite combining brand voice analysis, SEO optimization, research assistance, and platform-specific content frameworks.

## Keywords
content creation, blog posts, SEO, brand voice, social media, content calendar, marketing content, content strategy, content marketing, brand consistency, content optimization, social media marketing, content planning, blog writing, content frameworks, brand guidelines, social media strategy, research, citations, writing partner

## Core Capabilities

### 1. Brand Voice Analysis
- Analyze existing content to establish baseline
- Select voice attributes and archetypes
- Ensure consistency across all content

### 2. SEO Optimization
- Keyword research and density analysis
- Structure assessment and meta tag suggestions
- Actionable optimization recommendations

### 3. Research & Citations
- Conduct research and find credible sources
- Add and format citations properly
- Manage references in multiple formats

### 4. Content Frameworks
- Blog post templates with proven structures
- Social media content optimization
- Content repurposing matrices

## Quick Start

### For Brand Voice Development
1. Run `scripts/brand_voice_analyzer.py` on existing content to establish baseline
2. Review `references/brand_guidelines.md` to select voice attributes
3. Apply chosen voice consistently across all content

### For Blog Content Creation
1. Create outline collaboratively (see Research Workflow below)
2. Research keywords for topic
3. Write content following template structure from `references/content_frameworks.md`
4. Run `scripts/seo_optimizer.py [file] [primary-keyword]` to optimize
5. Apply recommendations before publishing

### For Research-Backed Writing
1. Start with an outline: "Help me create an outline for an article about [topic]"
2. Research and add citations: "Research [specific topic] and add citations"
3. Write sections with feedback: "Review this section and give feedback"
4. Polish: "Review the full draft for flow, clarity, and consistency"

### For Social Media Content
1. Review platform best practices in `references/social_media_optimization.md`
2. Use appropriate template from `references/content_frameworks.md`
3. Optimize based on platform-specific guidelines
4. Schedule using `assets/content_calendar_template.md`

## Research Workflow

### Collaborative Outlining

When creating content, start with a structured outline:

```markdown
# Article Outline: [Title]

## Hook
- [Opening line/story/statistic]
- [Why reader should care]

## Introduction
- Context and background
- Problem statement
- What this article covers

## Main Sections

### Section 1: [Title]
- Key point A
- Key point B
- [Research needed: specific topic]

### Section 2: [Title]
- Key point C
- Data/citation needed

## Conclusion
- Summary of main points
- Call to action

## Research To-Do
- [ ] Find data on [topic]
- [ ] Get examples of [concept]
- [ ] Source citation for [claim]
```

### Research and Citations

When conducting research:
- Search for relevant information
- Find credible sources
- Extract key facts, quotes, and data
- Add citations in requested format

**Citation Formats:**

Inline Citations:
```markdown
Studies show 40% productivity improvement (McKinsey, 2024).
```

Numbered References:
```markdown
Studies show 40% productivity improvement [1].

[1] McKinsey Global Institute. (2024)...
```

### Section-by-Section Feedback

As you write each section, get feedback for:
- **Clarity**: Clear and understandable?
- **Flow**: Logical transitions?
- **Evidence**: Claims supported?
- **Style**: Consistent voice?

### Hook Improvement

For introductions, analyze and strengthen:
- What works well
- What could be stronger
- Alternative approaches (data-driven, question, story)

## Key Scripts

### brand_voice_analyzer.py
Analyzes text content for voice characteristics, readability, and consistency.

**Usage**: `python scripts/brand_voice_analyzer.py <file> [json|text]`

**Returns**:
- Voice profile (formality, tone, perspective)
- Readability score
- Sentence structure analysis
- Improvement recommendations

### seo_optimizer.py
Analyzes content for SEO optimization and provides actionable recommendations.

**Usage**: `python scripts/seo_optimizer.py <file> [primary_keyword] [secondary_keywords]`

**Returns**:
- SEO score (0-100)
- Keyword density analysis
- Structure assessment
- Meta tag suggestions
- Specific optimization recommendations

## Reference Guides

### When to Use Each Reference

**references/brand_guidelines.md**
- Setting up new brand voice
- Ensuring consistency across content
- Training new team members

**references/content_frameworks.md**
- Starting any new content piece
- Structuring different content types
- Planning content repurposing

**references/social_media_optimization.md**
- Platform-specific optimization
- Hashtag strategy development
- Understanding algorithm factors

## Content Types Supported

### Blog Posts & Articles
- SEO-optimized long-form content
- Thought leadership pieces
- Educational tutorials
- Case studies

### Newsletters
- Quick outline format
- Clarity and link optimization
- Quick polish workflow

### Technical Tutorials
- Step-by-step structure
- Code examples with explanations
- Troubleshooting sections

### Social Media
- Platform-specific optimization
- Content repurposing from blog posts
- Hashtag and timing strategies

## Best Practices

### Content Creation Process
1. Always start with audience need/pain point
2. Research before writing
3. Create outline using templates
4. Write first draft without editing
5. Get section-by-section feedback
6. Optimize for SEO
7. Edit for brand voice
8. Proofread and fact-check
9. Optimize for platform
10. Schedule strategically

### Voice Preservation
- Learn the writer's style from samples
- Suggest, don't replace
- Match tone appropriately
- Ask: "Does this sound like you?"

### Quality Indicators
- SEO score above 75/100
- Readability appropriate for audience
- Consistent brand voice throughout
- Clear value proposition
- Actionable takeaways
- Proper citations and sources

### Common Pitfalls to Avoid
- Writing before researching keywords
- Ignoring platform-specific requirements
- Inconsistent brand voice
- Over-optimizing for SEO (keyword stuffing)
- Missing clear CTAs
- Unsubstantiated claims

## File Organization

Recommended structure for writing projects:

```
~/writing/article-name/
├── outline.md          # Your outline
├── research.md         # All research and citations
├── draft-v1.md         # First draft
├── draft-v2.md         # Revised draft
├── final.md            # Publication-ready
├── feedback.md         # Collected feedback
└── sources/            # Reference materials
```

## Performance Metrics

### Content Metrics
- Organic traffic growth
- Average time on page
- Bounce rate
- Social shares
- Backlinks earned

### Engagement Metrics
- Comments and discussions
- Email click-through rates
- Social media engagement rate
- Content downloads

## Quick Commands

```bash
# Analyze brand voice
python scripts/brand_voice_analyzer.py content.txt

# Optimize for SEO
python scripts/seo_optimizer.py article.md "main keyword"

# Create monthly calendar
cp assets/content_calendar_template.md this_month_calendar.md
```
