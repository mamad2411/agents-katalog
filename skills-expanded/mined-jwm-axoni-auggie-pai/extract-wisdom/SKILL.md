---
name: extract-wisdom
description: Extract the most valuable ideas, insights, and recommendations from any content including articles, videos, podcasts, and documents. USE WHEN extract wisdom, key takeaways, what's interesting, extract insights, analyze video, analyze podcast, content analysis.
---

# Extract Wisdom -- Content Analysis Skill

Extract the most valuable ideas, insights, and recommendations from any content.
Works with articles, videos, podcasts, transcripts, documents, and any other source material.

## When to Use

- Analyzing YouTube videos, podcasts, interviews, articles, or documents
- User says "extract wisdom," "key takeaways," "what's interesting," or "extract insights"
- Processing any content where you want to capture the most valuable parts
- When standard summaries miss the real gems

## Depth Levels

| Level | Sections | Bullets/Section | Closing Sections | When |
|-------|----------|----------------|-----------------|------|
| **Instant** | 1 | 8 | None | Quick hit, one killer section |
| **Fast** | 3 | 3 | None | Skim in 30 seconds |
| **Basic** | 3 | 5 | One-Sentence Takeaway only | Solid overview |
| **Full** | 5-12 | 3-15 | All three | Default. Complete extraction |
| **Comprehensive** | 10-15 | 8-15 | All three + Themes & Connections | Maximum depth |

Default is **Full** if no level is specified.

## Process

### Phase 1: Content Scan
Read the full content. Identify what DOMAINS of wisdom are present -- not topics discussed,
but TYPES of insight being delivered. Examples:
- Programming Philosophy, Developer Workflow, Business/Money Philosophy
- Human Psychology, Technology Predictions, Life Philosophy
- Contrarian Takes, First-Time Revelations, Technical Architecture
- Leadership & Team Dynamics, Creative Process, Security Thinking

### Phase 2: Section Selection
Pick sections based on depth level. Requirements:
- Each section needs at least 3 strong bullets to justify existing
- Always include "Quotes That Hit Different" if the content has good ones
- Always include "First-Time Revelations" if there are genuinely new ideas
- Section names should be conversational, not academic
- Sections must be SPECIFIC to this content. Generic sections are a failure
- Name sections like headlines: "The Death of 80% of Apps" not "Technology Predictions"

### Phase 3: Extraction
For each section, extract 3-15 bullets depending on density. Rules:
1. Write like you'd say it. Read each bullet aloud -- it should sound natural
2. Target 8-16 words per sentence. Mix short with medium and longer
3. Use periods between thoughts, not em-dashes. Let ideas breathe
4. Include the actual detail, not vague references
5. Use the speaker's words when they said something perfectly
6. No hedging language -- not "it was suggested that," just say the thing
7. Every bullet should be something worth telling someone about
8. Vary your openers. No more than 3 bullets starting with the speaker's name
9. Capture human moments -- doubt, burnout, things that moved them
10. Insight over inventory. Go deeper on WHY, not just WHAT
11. Specificity is everything. Details make bullets memorable
12. Surface contradictions and reversals -- the gap IS the wisdom

### Phase 4: Closing Sections
Include closing sections based on depth level:
- **One-Sentence Takeaway** (Basic+): The single most important point in 15-20 words
- **If You Only Have 2 Minutes** (Full+): The 5-7 absolute must-know points
- **References & Rabbit Holes** (Full+): People, projects, tools worth following up on
- **Themes & Connections** (Comprehensive only): 3-5 throughlines connecting multiple sections

## Output Format

```markdown
# EXTRACT WISDOM: {Content Title}
> {One-line description of what this is and who's talking}

---

## {Dynamic Section 1 Name}

- {bullet}
- {bullet}
- {bullet}

## {Dynamic Section 2 Name}

- {bullet}
- {bullet}

[... more dynamic sections ...]

---

## One-Sentence Takeaway

{15-20 word sentence}

## If You Only Have 2 Minutes

- {essential point 1}
- {essential point 2}
- {essential point 3}
- {essential point 4}
- {essential point 5}

## References & Rabbit Holes

- **{Name/Project}** -- {one-line context of why it's worth looking into}
```

## Quality Check

Before delivering output, verify:
- [ ] Sections are specific to THIS content, not generic
- [ ] Every bullet has a specific detail, quote, or insight -- not vague summaries
- [ ] Section names are conversational and headline-worthy
- [ ] Section count matches depth level
- [ ] Closing sections match depth level
- [ ] No bullet starts with "The speaker" or "It was noted that"
- [ ] No bullet exceeds 25 words
- [ ] Reading the output makes you want to consume the original content

## Customization

User-specific preferences can be placed in:
`~/.augment/USER/SKILLCUSTOMIZATIONS/ExtractWisdom/`

If that directory exists, load and apply any PREFERENCES.md or configurations found there.
These override default behavior. If the directory does not exist, use skill defaults.
