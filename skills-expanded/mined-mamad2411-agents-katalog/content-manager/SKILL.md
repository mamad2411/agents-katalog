---
name: content-manager
description: |
  Master orchestrator for the 10X Content Expert system. Routes content requests to appropriate
  specialist skills based on content type and user needs. Use this skill when user wants to
  create any type of content (emails, social posts, presentations, blogs, etc.) or when
  unsure which specific skill to use. Analyzes references and maintains content quality.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - WebSearch
  - WebFetch
---

# Content Manager Skill

> **QUICK REFERENCE — ROUTING TABLE**
> | User wants... | Route to skill |
> |---|---|
> | Write an email | `email-copywriter` |
> | Write LinkedIn/Twitter post | `social-media-writer` |
> | Write a blog post | `blog-article-writer` |
> | Create hooks/headlines | `hook-generator` |
> | Create email sequence | `nurture-sequence` |
> | Create presentation content | `presentation-content` |
> | Repurpose content | `content-repurposer` |
> | Analyze references | `content-analyzer` |
> | Define brand voice | `brand-voice-manager` |
> | Choose a framework | `content-frameworks` |
>
> - **All outputs go to**: `output/` subfolders (see CLAUDE.md for full path table)
> - **Sample scripts**: `scripts/samples/` (copy and modify these)
> - **References**: ALWAYS check `references/` folder before creating content
> - **Python**: ALWAYS use `.venv\Scripts\python.exe` (never bare `python`)

Master orchestrator for the 10X Content Expert system. This skill routes requests to specialized content creation skills and ensures consistent, high-quality output aligned with brand voice and reference materials.

## Overview

The Content Manager is your central hub for all content creation needs:
- **Routing**: Directs requests to the right specialist skill
- **Analysis**: Understands context from references and transcripts
- **Quality**: Ensures brand consistency across all content
- **Coordination**: Manages multi-format content projects

## Skill Routing

Based on user request, route to the appropriate specialist:

| Request Type | Route To |
|-------------|----------|
| Email marketing, newsletters, campaigns | `email-copywriter` |
| LinkedIn, Twitter, Instagram, social posts | `social-media-writer` |
| PPT content, presentation outlines | `presentation-content` |
| Blog posts, articles, long-form | `blog-article-writer` |
| Headlines, hooks, CTAs | `hook-generator` |
| Email sequences, drip campaigns | `nurture-sequence` |
| Transform content across formats | `content-repurposer` |
| Analyze transcripts, references | `content-analyzer` |
| Brand voice, tone consistency | `brand-voice-manager` |
| Copywriting frameworks reference | `content-frameworks` |
| Edit local files (DOCX, PPTX, PDF) | `local-file-manager` |
| **Canva design creation (explicit request)** | `canva-manager` |
| Create images in Canva | `canva-image-editor` |
| Create presentations in Canva | `canva-presentation` |
| Export from Canva | `canva-export` |

## Canva Integration (Optional)

When user **explicitly** requests Canva design creation, route to Canva skills:

- Use `/canva` command for Canva operations
- Requires Canva API credentials in `.env`
- Run `python scripts/oauth_flow.py` for initial setup

**When to use Canva vs Local Files:**
| User Says | Use |
|-----------|-----|
| "Edit my presentation.pptx" | `local-file-manager` |
| "Create a presentation in Canva" | `canva-presentation` |
| "Modify this PDF" | `local-pdf-editor` |
| "Design social graphics in Canva" | `canva-image-editor` |

## Reference Materials Structure

The `references/` folder contains knowledge sources:

```
references/
├── transcripts/           # Video/audio transcripts
│   ├── training/          # Training session transcripts
│   ├── interviews/        # Interview transcripts
│   └── webinars/          # Webinar content
├── examples/              # Content examples to learn from
│   ├── emails/            # High-performing emails
│   ├── social/            # Viral/engaging social posts
│   ├── presentations/     # Excellent PPT examples
│   └── blogs/             # Top-performing articles
├── brand-voice/           # Brand guidelines
│   ├── tone-guide.md      # Voice and tone documentation
│   ├── keywords.txt       # Power words and phrases
│   └── avoid-list.txt     # Words/phrases to avoid
└── templates/             # Content templates
    ├── email/
    ├── social/
    ├── ppt/
    └── blog/
```

## 3-Mode Workflow

### MODE 1: PLAN

1. **Understand the Request**
   ```
   - What type of content is needed?
   - What's the purpose (awareness, conversion, engagement)?
   - Who is the target audience?
   - What format(s) are required?
   ```

2. **Analyze Available References**
   ```bash
   # Check what reference materials exist
   ls references/

   # Analyze transcripts for key insights
   python scripts/content/analyze_references.py --folder references/transcripts

   # Check brand voice guidelines
   cat references/brand-voice/tone-guide.md
   ```

3. **Route to Specialist**
   - Identify which skill(s) to invoke
   - Pass relevant context and references
   - Set quality expectations

4. **Document the Plan**
   ```markdown
   ## Content Creation Plan

   ### Request Summary
   - Content Type: [email/social/ppt/blog/etc.]
   - Purpose: [awareness/conversion/engagement]
   - Audience: [target description]

   ### Reference Analysis
   - Key themes from transcripts: [list]
   - Brand voice notes: [summary]
   - Relevant examples: [list]

   ### Skills to Invoke
   1. [skill-name] - for [purpose]
   2. [skill-name] - for [purpose]

   ### Expected Output
   - [deliverable 1]
   - [deliverable 2]
   ```

### MODE 2: CLARIFY

Ask targeted questions based on content type:

**General Questions:**
- "Who is the target audience for this content?"
- "What's the primary goal - awareness, engagement, or conversion?"
- "Any specific topics or references I should prioritize?"

**Format-Specific Questions:**
- Email: "Is this a cold email, nurture email, or promotional?"
- Social: "Which platform(s)? LinkedIn, Twitter, Instagram?"
- PPT: "How many slides? What's the presentation context?"
- Blog: "Target word count? SEO keywords to include?"

**Brand Questions:**
- "Should I match your established brand voice or try something different?"
- "Any specific phrases or CTAs you want included?"

### MODE 3: IMPLEMENT

1. **Invoke Specialist Skills**
   - Pass full context and references
   - Request specific outputs
   - Coordinate multi-skill workflows

2. **Quality Check**
   - Verify brand voice alignment
   - Check for consistency across outputs
   - Validate against reference standards

3. **Save Outputs**
   ```
   output/
   ├── content/
   │   ├── [date]_[project]/
   │   │   ├── email/
   │   │   ├── social/
   │   │   ├── ppt/
   │   │   └── blog/
   ```

## Multi-Format Content Projects

For projects requiring multiple content types:

### Example: Product Launch Campaign

```markdown
## Campaign: New Product Launch

### Content Required:
1. Email sequence (3 emails) → email-copywriter, nurture-sequence
2. LinkedIn posts (5 posts) → social-media-writer
3. Sales presentation (15 slides) → presentation-content
4. Blog announcement → blog-article-writer
5. All hooks and CTAs → hook-generator

### Workflow:
1. Analyze product references and brand voice
2. Generate core messaging and hooks
3. Branch to specialist skills for each format
4. Quality check all outputs for consistency
5. Package deliverables
```

## Working with References

### Analyzing Transcripts

```bash
# Extract key themes from transcript
python scripts/content/extract_themes.py \
  --input references/transcripts/training/session1.txt \
  --output output/analysis/themes.json

# Find quotable moments
python scripts/content/find_quotes.py \
  --input references/transcripts/ \
  --output output/analysis/quotes.txt

# Generate content ideas from transcript
python scripts/content/generate_ideas.py \
  --transcript references/transcripts/webinar.txt \
  --format all \
  --output output/ideas/
```

### Loading Brand Voice

```bash
# Analyze brand voice from examples
python scripts/content/analyze_brand_voice.py \
  --examples references/examples/ \
  --output references/brand-voice/detected_voice.json

# Check content against brand guidelines
python scripts/content/check_brand_alignment.py \
  --content output/content/draft.txt \
  --guidelines references/brand-voice/
```

## Example Interactions

### "I need content for my product launch"
```
[PLAN]
- Identify content types needed
- Analyze product references
- Map to specialist skills

[CLARIFY]
- "Which formats do you need: email, social, PPT, blog?"
- "What's the launch timeline?"
- "Who's the target audience?"

[IMPLEMENT]
- Coordinate multiple skills
- Generate cohesive content package
- Quality check and deliver
```

### "Create social posts from my training video transcript"
```
[PLAN]
- Read and analyze transcript
- Extract key insights
- Route to social-media-writer

[CLARIFY]
- "Which platforms: LinkedIn, Twitter, both?"
- "How many posts?"
- "Educational or promotional tone?"

[IMPLEMENT]
- Extract quotable insights
- Generate platform-specific posts
- Save to output folder
```

### "I need emails for my nurture sequence"
```
[PLAN]
- Check email examples in references
- Understand nurture goals
- Route to nurture-sequence skill

[CLARIFY]
- "How many emails in the sequence?"
- "What's the conversion goal?"
- "Time between emails?"

[IMPLEMENT]
- Generate email sequence
- Create subject line variants
- Include CTAs and timing notes
```

## Output Structure

All content saved to:
```
output/
├── content/
│   ├── emails/
│   ├── social/
│   ├── presentations/
│   ├── blogs/
│   └── campaigns/
├── analysis/
│   ├── themes/
│   ├── brand-voice/
│   └── reference-notes/
└── logs/
    └── [timestamp]_session.log
```

## Quality Standards

All content must:
1. Align with brand voice guidelines
2. Use insights from reference materials
3. Include appropriate CTAs
4. Follow platform-specific best practices
5. Be original and non-plagiarized

## Todo List Tracking (REQUIRED)

**ALWAYS use TodoWrite** for content projects:

```json
[
  {"content": "Analyze reference materials", "status": "in_progress", "activeForm": "Analyzing references"},
  {"content": "Generate email content", "status": "pending", "activeForm": "Generating emails"},
  {"content": "Create social posts", "status": "pending", "activeForm": "Creating social posts"},
  {"content": "Quality check outputs", "status": "pending", "activeForm": "Quality checking"}
]
```
