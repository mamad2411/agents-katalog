---
name: canva-content-generator
description: |
  Generate content ideas and text for Canva designs. Use this skill when user needs help
  with what to write, content suggestions, copy for designs, captions, headlines, or
  creative direction. Analyzes user's sample preferences from the samples folder to match
  their style. Does NOT directly edit Canva - provides content that other skills use.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Canva Content Generator Skill

> **QUICK REFERENCE**
> - **Scripts location**: `scripts/` (NOT `skills/canva-content-generator/scripts/` - those don't exist)
> - **Samples folder**: `samples/` (images, presentations, videos, brand-kits)
> - **Output**: `output/content/` (various subfolders)
> - **Sample script**: `scripts/samples/sample_canva_operations.py`
>
> **WARNING**: Commands below referencing `skills/canva-content-generator/scripts/*.py` are WRONG paths.
> This skill generates TEXT content - no API scripts needed. Save output to `output/content/`.

Generate creative content, copy, and ideas for Canva designs based on user preferences and samples.

## Scope of This Skill

**This skill handles:**
- Headline and title suggestions
- Body copy and descriptions
- Social media captions
- Call-to-action text
- Presentation outlines
- Content calendars
- Design brief creation
- Style analysis from samples

**NOT handled by this skill:**
- Actually editing Canva designs → Use `canva-image-editor`, etc.
- Exporting files → Use `canva-export`
- Managing folders → Use `canva-folder-organizer`

## How It Works

1. **Analyze User Samples** - Learn from samples folder
2. **Understand Request** - What content is needed
3. **Generate Options** - Multiple content variations
4. **Refine with User** - Get feedback and iterate
5. **Output for Use** - Ready for other skills to apply

## Using Sample References

The `samples/` folder contains user preferences:

```
samples/
├── images/
│   ├── social-media/      # Instagram, Facebook, etc.
│   ├── posters/           # Poster designs
│   ├── logos/             # Logo styles
│   └── banners/           # Banner designs
├── presentations/
│   ├── pitch-decks/       # Business presentations
│   ├── reports/           # Report styles
│   └── educational/       # Educational content
├── videos/
│   ├── reels/             # Short video styles
│   ├── ads/               # Advertisement videos
│   └── intros/            # Intro/outro styles
├── brand-kits/            # Brand guidelines
├── color-palettes/        # Preferred colors
└── fonts/                 # Font preferences
```

### Analyzing Samples

```python
# Analyze user's image style preferences
python skills/canva-content-generator/scripts/analyze_samples.py \
  --type images

# Get brand voice from presentations
python skills/canva-content-generator/scripts/analyze_samples.py \
  --type presentations

# Extract color preferences
python skills/canva-content-generator/scripts/extract_colors.py \
  --folder "samples/color-palettes"

# Analyze text style
python skills/canva-content-generator/scripts/analyze_text_style.py \
  --samples "samples/images/social-media"
```

## 3-Mode Workflow

### MODE 1: PLAN

1. **Understand the Need**
   ```
   - What type of content? (headline, caption, outline)
   - What design will it be used for? (Instagram, presentation)
   - What's the purpose? (promote, inform, entertain)
   - Target audience?
   ```

2. **Check Sample Preferences**
   ```python
   # Load user's style preferences
   python skills/canva-content-generator/scripts/analyze_samples.py \
     --type images/social-media
   ```

3. **Document Content Plan**
   ```
   ## Content Generation Plan

   ### Request
   - Need: Instagram post caption
   - Topic: New product launch
   - Tone: Exciting, modern

   ### User Preferences (from samples)
   - Style: Minimal, clean
   - Emoji usage: Moderate
   - Hashtag strategy: 10-15 relevant
   - CTA style: Direct

   ### Will Generate
   - 3 headline options
   - 3 caption variations
   - Hashtag suggestions
   ```

### MODE 2: CLARIFY

Content-specific questions:

1. **Tone and Voice**
   - "Should this be formal or casual?"
   - "Playful or professional?"

2. **Constraints**
   - "Any character limits?"
   - "Required keywords or hashtags?"

3. **Brand Alignment**
   - "Match your usual style or try something new?"
   - "Include emojis?"

4. **Purpose**
   - "Drive sales, build awareness, or engage?"
   - "What action should viewers take?"

### MODE 3: IMPLEMENT

Generate content and save to output:

```python
# Generate headlines
python skills/canva-content-generator/scripts/generate_headlines.py \
  --topic "Summer Sale" \
  --style "energetic" \
  --count 5 \
  --output "output/content/headlines.txt"

# Generate social captions
python skills/canva-content-generator/scripts/generate_caption.py \
  --platform instagram \
  --topic "Product Launch" \
  --tone "exciting" \
  --include-hashtags \
  --output "output/content/caption.txt"

# Generate presentation outline
python skills/canva-content-generator/scripts/generate_outline.py \
  --type "pitch-deck" \
  --topic "Q4 Business Review" \
  --slides 15 \
  --output "output/content/outline.json"
```

## Available Scripts

### Analysis Scripts
- `analyze_samples.py` - Learn from user's samples
- `extract_colors.py` - Get color preferences
- `analyze_text_style.py` - Understand writing style
- `detect_brand_voice.py` - Identify brand tone

### Generation Scripts
- `generate_headlines.py` - Create headline options
- `generate_caption.py` - Social media captions
- `generate_outline.py` - Presentation structure
- `generate_copy.py` - Body text and descriptions
- `generate_cta.py` - Call-to-action text
- `generate_hashtags.py` - Relevant hashtags

### Utility Scripts
- `save_content.py` - Save generated content
- `format_output.py` - Format for specific use

## Content Types

### Headlines
```
Input: Topic, tone, character limit
Output: Multiple headline options

Example:
Topic: Summer Sale
Tone: Urgent, exciting
Options:
1. "SUMMER SALE: 50% OFF EVERYTHING"
2. "Don't Miss Out - Summer Deals End Soon!"
3. "☀️ Hot Summer Savings Inside"
```

### Social Captions
```
Input: Platform, topic, tone, hashtag count
Output: Full caption with hashtags

Example:
Platform: Instagram
Topic: New product launch
Output:
"Introducing our game-changing new [Product] ✨

We've been working on this for months, and it's finally here!

🎁 First 100 orders get FREE shipping
⏰ Available now - link in bio

#NewProduct #Launch #Innovation #MustHave..."
```

### Presentation Outlines
```
Input: Type, topic, slide count
Output: Structured outline

Example:
Type: Pitch Deck
Topic: Startup Funding
Slides: 12
Output:
1. Title Slide
2. Problem Statement
3. Our Solution
4. Market Opportunity
5. Business Model
...
```

### Body Copy
```
Input: Purpose, length, tone
Output: Paragraph text

Example:
Purpose: Product description
Length: Medium (50-100 words)
Output: "Transform your workflow with..."
```

## Style Matching

When samples are provided, the generator matches:

1. **Vocabulary Level** - Simple vs. sophisticated
2. **Sentence Structure** - Short punchy vs. flowing
3. **Emoji Usage** - Heavy, moderate, none
4. **Tone** - Formal, casual, playful
5. **CTA Style** - Direct, subtle, urgent
6. **Hashtag Strategy** - Count, type, placement

## Brand Kit Integration

If brand kit exists in `samples/brand-kits/`:

```json
{
  "brand_name": "Acme Corp",
  "tagline": "Innovation Made Simple",
  "voice": "professional yet approachable",
  "values": ["innovation", "simplicity", "trust"],
  "avoid": ["complicated", "jargon", "corporate-speak"],
  "emoji_style": "minimal",
  "hashtags": ["#AcmeCorp", "#InnovationMadeSimple"]
}
```

Content will automatically align with brand guidelines.

## Example Interactions

### "I need captions for my Instagram posts"
```
[PLAN]
- Check samples/images/social-media for style
- Identify user's caption patterns
- Note emoji and hashtag usage

[CLARIFY]
- "What are the posts about?"
- "How many captions needed?"
- "Match your usual style?"

[IMPLEMENT]
- Generate captions matching user style
- Include appropriate hashtags
- Save to output/content/
```

### "Help me outline a pitch deck"
```
[PLAN]
- Check samples/presentations/pitch-decks
- Identify preferred structure
- Note typical slide count

[CLARIFY]
- "What's your company/product?"
- "Who's the audience? (investors, clients)"
- "How many slides?"

[IMPLEMENT]
- Generate structured outline
- Include speaker notes suggestions
- Save to output/content/outline.json
```

## Output Files

Generated content saved to:
- `output/content/headlines.txt` - Headlines
- `output/content/captions.txt` - Social captions
- `output/content/outlines/` - Presentation structures
- `output/content/copy/` - Body text
- `output/content/style_analysis.json` - Detected preferences

## Adding Your Samples

To teach the generator your style:

1. Add examples to appropriate folders in `samples/`
2. Include both images and their associated text
3. Create a `style_notes.txt` with preferences
4. Run analysis to update preferences

```
samples/images/social-media/
├── post_1.png
├── post_1_caption.txt
├── post_2.png
├── post_2_caption.txt
└── style_notes.txt
```

The more samples provided, the better the style matching.
