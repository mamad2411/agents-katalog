---
name: content-analyzer
description: |
  Analyzes reference materials, transcripts, videos, and knowledge bases to extract insights
  for content creation. Use this skill when you need to understand existing content, extract
  key themes, find quotable moments, or build a knowledge foundation before creating new content.
  Works with transcripts, documents, examples, and any reference material in the references folder.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Content Analyzer Skill

> **QUICK REFERENCE**
> - **Output folder**: `output/analysis/`
> - **Scripts**: `scripts/content/analyze_transcript.py`, `scripts/content/extract_themes.py`, `scripts/content/find_quotes.py`
> - **Sample script**: `scripts/samples/sample_content_analysis.py`
> - **References to scan**: `references/transcripts/`, `references/examples/`, `references/brand-voice/`
> - **Python**: `.venv\Scripts\python.exe` (Windows) or `.venv/bin/python` (Mac/Linux)

Deep analysis of reference materials, transcripts, and knowledge bases to power intelligent content creation.

## Scope of This Skill

**This skill handles:**
- Transcript analysis (video, audio, meeting notes)
- Theme and topic extraction
- Finding quotable moments and key insights
- Brand voice pattern detection
- Content example analysis
- Knowledge base organization
- Competitor content analysis
- Performance pattern identification

**NOT handled by this skill:**
- Actually writing content → Use appropriate writer skills
- Creating presentations → Use `presentation-content`
- Editing local files → Use `local-file-manager`

## Reference Materials Structure

```
references/
├── transcripts/              # Primary knowledge source
│   ├── training/             # Training sessions, courses
│   │   ├── session1.txt
│   │   ├── session1_notes.md
│   │   └── ...
│   ├── interviews/           # Expert interviews
│   ├── webinars/             # Recorded webinars
│   ├── podcasts/             # Podcast transcripts
│   └── meetings/             # Meeting recordings
├── examples/                 # High-performing content
│   ├── emails/               # Best emails to learn from
│   │   ├── welcome_sequence/
│   │   ├── sales_emails/
│   │   └── newsletters/
│   ├── social/               # Top social posts
│   │   ├── linkedin/
│   │   ├── twitter/
│   │   └── instagram/
│   ├── presentations/        # Excellent PPTs
│   └── blogs/                # Top articles
├── brand-voice/              # Brand guidelines
│   ├── tone-guide.md
│   ├── messaging-framework.md
│   ├── keywords.txt
│   └── avoid-list.txt
└── competitors/              # Competitor analysis
    ├── [competitor1]/
    └── [competitor2]/
```

## Analysis Types

### 1. Transcript Analysis

Extract insights from video/audio transcripts:

```bash
# Full transcript analysis
python scripts/content/analyze_transcript.py \
  --input references/transcripts/training/session1.txt \
  --output output/analysis/session1_analysis.json

# Output includes:
# - Key themes and topics
# - Quotable moments
# - Main arguments/points
# - Statistics and data mentioned
# - Action items/takeaways
```

**What to Extract:**
- **Core Messages**: Main points being communicated
- **Stories**: Anecdotes, case studies, examples used
- **Data Points**: Statistics, research, proof points
- **Quotes**: Memorable, shareable statements
- **Frameworks**: Models, processes, methodologies
- **Pain Points**: Problems discussed
- **Solutions**: Recommendations given

### 2. Theme Extraction

Identify recurring themes across multiple sources:

```bash
# Extract themes from folder
python scripts/content/extract_themes.py \
  --folder references/transcripts/ \
  --output output/analysis/themes.json \
  --min-occurrences 3

# Compare themes across sources
python scripts/content/compare_themes.py \
  --source1 references/transcripts/training/ \
  --source2 references/transcripts/webinars/ \
  --output output/analysis/theme_comparison.md
```

### 3. Quote Mining

Find the best quotable moments:

```bash
# Extract quotes from transcript
python scripts/content/find_quotes.py \
  --input references/transcripts/interview.txt \
  --output output/analysis/quotes.txt \
  --min-length 10 \
  --max-length 280

# Categorize quotes by topic
python scripts/content/categorize_quotes.py \
  --input output/analysis/quotes.txt \
  --categories "motivation,strategy,tactics,mindset" \
  --output output/analysis/quotes_categorized.json
```

### 4. Brand Voice Analysis

Detect and document brand voice patterns:

```bash
# Analyze voice from examples
python scripts/content/analyze_brand_voice.py \
  --examples references/examples/ \
  --output references/brand-voice/detected_voice.json

# Output includes:
# - Tone characteristics (formal/casual, energetic/calm)
# - Vocabulary patterns (simple/sophisticated)
# - Sentence structure preferences
# - Emoji usage patterns
# - CTA styles
# - Hashtag strategies
```

### 5. Content Performance Analysis

Learn from high-performing content:

```bash
# Analyze what makes content work
python scripts/content/analyze_performance.py \
  --folder references/examples/social/linkedin/ \
  --metrics engagement \
  --output output/analysis/linkedin_patterns.json

# Compare high vs low performing
python scripts/content/compare_content.py \
  --high references/examples/emails/best/ \
  --low references/examples/emails/underperforming/ \
  --output output/analysis/email_insights.md
```

## 3-Mode Workflow

### MODE 1: PLAN

1. **Understand Analysis Goals**
   ```
   - What insights are needed?
   - Which reference materials are available?
   - What will the insights be used for?
   ```

2. **Inventory References**
   ```bash
   # List available references
   find references/ -type f -name "*.txt" -o -name "*.md"

   # Count materials by type
   ls references/transcripts/ | wc -l
   ls references/examples/ | wc -l
   ```

3. **Create Analysis Plan**
   ```markdown
   ## Analysis Plan

   ### Goal
   [What insights are needed]

   ### Available Materials
   - Transcripts: X files
   - Examples: Y files
   - Brand guidelines: [yes/no]

   ### Analysis Steps
   1. [Step 1]
   2. [Step 2]

   ### Expected Outputs
   - [Output 1]
   - [Output 2]
   ```

### MODE 2: CLARIFY

Ask to understand analysis scope:

- "Which transcripts should I prioritize?"
- "What specific themes are you looking for?"
- "Should I focus on quotes for social or for presentations?"
- "Any particular competitor content to analyze?"
- "What format should the analysis output be?"

### MODE 3: IMPLEMENT

1. **Run Analysis**
   - Execute appropriate analysis scripts
   - Process all relevant reference materials
   - Generate structured outputs

2. **Synthesize Findings**
   - Combine insights from multiple analyses
   - Create actionable summaries
   - Highlight key patterns

3. **Save Results**
   ```
   output/analysis/
   ├── [date]_[project]/
   │   ├── themes.json
   │   ├── quotes.txt
   │   ├── brand_voice.json
   │   ├── insights_summary.md
   │   └── content_recommendations.md
   ```

## Analysis Output Formats

### Themes Analysis
```json
{
  "themes": [
    {
      "name": "Customer Success",
      "occurrences": 15,
      "sources": ["training1.txt", "webinar2.txt"],
      "key_points": [
        "Always measure outcomes",
        "Regular check-ins are crucial"
      ],
      "related_quotes": ["..."]
    }
  ]
}
```

### Quote Mining Output
```json
{
  "quotes": [
    {
      "text": "The best content comes from understanding, not guessing.",
      "source": "training_session_3.txt",
      "timestamp": "12:34",
      "category": "strategy",
      "suggested_use": ["linkedin", "presentation"],
      "character_count": 58
    }
  ]
}
```

### Brand Voice Profile
```json
{
  "voice_profile": {
    "tone": {
      "formality": "professional-casual",
      "energy": "confident",
      "warmth": "approachable"
    },
    "vocabulary": {
      "level": "accessible",
      "jargon_usage": "minimal",
      "power_words": ["transform", "accelerate", "proven"]
    },
    "structure": {
      "sentence_length": "varied, mostly short",
      "paragraph_style": "short, scannable",
      "formatting": "bullets, headers, white space"
    },
    "personality": {
      "emoji_usage": "moderate",
      "humor": "occasional, professional",
      "storytelling": "frequent"
    }
  }
}
```

## Example Interactions

### "Analyze my training transcripts"
```
[PLAN]
- Count available transcripts
- Plan comprehensive analysis
- Define output structure

[CLARIFY]
- "Which aspects to focus on: themes, quotes, or both?"
- "Any specific topics you want me to look for?"
- "Should I create a content calendar from the insights?"

[IMPLEMENT]
- Process all transcripts
- Extract themes and patterns
- Mine quotable moments
- Generate actionable summary
```

### "What content can I create from this webinar?"
```
[PLAN]
- Read and analyze webinar transcript
- Identify content opportunities
- Map to appropriate formats

[CLARIFY]
- "Which formats are you most interested in?"
- "What's your posting frequency goal?"

[IMPLEMENT]
- Full transcript analysis
- Generate content ideas by format
- Prioritize by potential impact
- Save recommendations
```

### "Learn my brand voice from these examples"
```
[PLAN]
- Inventory all example content
- Plan voice analysis approach
- Define output format

[CLARIFY]
- "Are all these examples representative of your ideal voice?"
- "Any examples that are NOT your preferred style?"

[IMPLEMENT]
- Analyze all examples
- Detect patterns and characteristics
- Create brand voice profile
- Save to references/brand-voice/
```

## Best Practices

1. **Quality Over Quantity**: Better to deeply analyze few excellent references than superficially scan many
2. **Source Attribution**: Always track where insights came from
3. **Regular Updates**: Re-analyze when new reference materials are added
4. **Cross-Reference**: Look for patterns across multiple sources
5. **Actionable Output**: Analysis should directly inform content creation

## Adding New References

When adding new reference materials:

1. **Place in correct folder** based on type
2. **Use consistent naming** (date_topic_source.txt)
3. **Include metadata** if available (speaker, date, context)
4. **Run initial analysis** to integrate into knowledge base

```bash
# After adding new transcript
python scripts/content/analyze_transcript.py \
  --input references/transcripts/new_transcript.txt \
  --update-themes \
  --output output/analysis/
```

## Output Files

Analysis saved to:
- `output/analysis/themes/` - Theme extraction results
- `output/analysis/quotes/` - Mined quotes
- `output/analysis/voice/` - Brand voice profiles
- `output/analysis/insights/` - Synthesized insights
- `references/brand-voice/` - Brand guidelines (updated)
