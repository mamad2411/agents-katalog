---
name: brand-voice-manager
description: |
  Maintains brand voice consistency across all content. Defines, documents, and enforces
  brand guidelines including tone, vocabulary, style, and messaging. Use this skill to
  create brand voice guides, check content alignment, or ensure consistency across
  content pieces.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Brand Voice Manager Skill

> **QUICK REFERENCE**
> - **Output folder**: `output/analysis/` (for voice analysis reports)
> - **Brand voice files**: `references/brand-voice/` (store brand guides here)
> - **Analysis script**: `.venv\Scripts\python.exe scripts/content/analyze_brand_voice.py`
> - **File naming**: `YYYY-MM-DD_brand_voice_guide.md`
> - **Key deliverables**: Voice guide, tone matrix, vocabulary lists, do/don't examples
> - **Python**: ALWAYS use `.venv\Scripts\python.exe` (never bare `python`)

Ensures consistent, authentic brand voice across all content types and platforms.

## Scope of This Skill

**This skill handles:**
- Brand voice definition and documentation
- Voice consistency checking
- Tone and style guidelines
- Messaging framework creation
- Vocabulary and language rules
- Brand personality articulation
- Voice training for content teams
- Content alignment audits

**NOT handled by this skill:**
- Visual branding → This is voice/copy only
- Creating content → Use appropriate writer skills
- Logo/design guidelines → Text/voice only

## Brand Voice Components

### 1. Brand Personality

Define your brand as a person:

```markdown
## Brand Personality

**If our brand were a person, they would be:**
- [Age range, appearance, lifestyle]
- [Profession or expertise area]
- [Personality traits - 3-5 words]
- [How they speak and communicate]
- [What they value most]

**Personality Traits:**
1. [Trait 1] - [How it shows up in content]
2. [Trait 2] - [How it shows up in content]
3. [Trait 3] - [How it shows up in content]
```

### 2. Tone Spectrum

Define tone across different contexts:

| Context | Tone | Example |
|---------|------|---------|
| Educational | [Helpful, expert, approachable] | "Here's what most people miss..." |
| Promotional | [Confident, exciting, direct] | "This is your moment to..." |
| Support | [Empathetic, patient, clear] | "We understand how frustrating..." |
| Social | [Friendly, engaging, authentic] | "Real talk: This changed everything..." |
| Formal | [Professional, authoritative, precise] | "Our analysis indicates..." |

### 3. Voice Attributes

Define 3-5 core voice attributes:

```markdown
## Voice Attributes

### 1. [Attribute Name] (e.g., "Confident")
**What it means:** [Definition]
**How it sounds:**
- DO: [Example phrase]
- DON'T: [Counter-example]

### 2. [Attribute Name] (e.g., "Approachable")
**What it means:** [Definition]
**How it sounds:**
- DO: [Example phrase]
- DON'T: [Counter-example]

### 3. [Attribute Name] (e.g., "Expert")
**What it means:** [Definition]
**How it sounds:**
- DO: [Example phrase]
- DON'T: [Counter-example]
```

### 4. Language Guidelines

#### Vocabulary

```markdown
## Vocabulary Guidelines

### Power Words (Use Frequently)
[List of brand-aligned power words]

### Words to Avoid
[List of off-brand words/phrases]

### Industry Jargon Policy
[When to use, when to explain, when to avoid]

### Competitor Words to Avoid
[Terms associated with competitors]
```

#### Grammar & Style

```markdown
## Grammar & Style

### Contractions
[Use: yes/no, when]

### Sentence Length
[Guidelines for sentence structure]

### Paragraph Length
[Max lines/sentences per paragraph]

### Point of View
[First person (we/I), second person (you), third person]

### Active vs Passive
[Preference and when to use each]

### Oxford Comma
[Yes/No]

### Capitalization
[Title case rules, brand name rules]
```

### 5. Messaging Framework

```markdown
## Core Messaging

### Tagline
[Primary brand tagline]

### Value Proposition
[One-sentence value statement]

### Elevator Pitch
[30-second version]

### Key Messages (3-5)
1. [Message 1]
2. [Message 2]
3. [Message 3]

### Proof Points
- [Proof point 1]
- [Proof point 2]
- [Proof point 3]

### Differentiation Statement
[How we're different from competitors]
```

## 3-Mode Workflow

### MODE 1: PLAN

1. **Understand Brand Context**
   ```
   - Existing brand guidelines?
   - Target audience(s)?
   - Competitive positioning?
   - Content examples to analyze?
   ```

2. **Audit Existing Content**
   ```bash
   # Analyze existing content for voice patterns
   python scripts/content/analyze_brand_voice.py \
     --folder references/examples/ \
     --output output/analysis/voice_audit.json
   ```

3. **Document Plan**
   ```markdown
   ## Brand Voice Plan

   ### Current State
   - Existing guidelines: [Yes/No]
   - Content consistency: [Low/Medium/High]
   - Key gaps: [List]

   ### Deliverables
   1. Brand personality definition
   2. Voice attributes (3-5)
   3. Tone spectrum
   4. Language guidelines
   5. Messaging framework
   ```

### MODE 2: CLARIFY

**Discovery Questions:**
- "Describe your brand as if it were a person - who are they?"
- "What 3 words should people use to describe your brand?"
- "What tone do competitors use that you want to avoid?"
- "Who is your target audience?"
- "What values does your brand stand for?"

**Style Questions:**
- "Formal or casual? How casual?"
- "Use humor? What kind?"
- "Use emojis in content?"
- "First person (we/I) or third person?"

**Differentiation Questions:**
- "What makes your brand voice unique?"
- "Any words/phrases competitors overuse?"
- "What's your 'anti-voice' - what you never want to sound like?"

### MODE 3: IMPLEMENT

1. **Create Voice Guide**
   ```bash
   python scripts/content/generate_voice_guide.py \
     --brand "Brand Name" \
     --output references/brand-voice/
   ```

2. **Document All Components**
   - Brand personality
   - Voice attributes
   - Tone guidelines
   - Language rules
   - Messaging framework

3. **Save Files**
   ```
   references/brand-voice/
   ├── brand-voice-guide.md       # Full guide
   ├── tone-guide.md              # Tone spectrum
   ├── messaging-framework.md     # Core messages
   ├── vocabulary.md              # Word lists
   ├── do-dont-examples.md        # Examples
   └── quick-reference.md         # One-page summary
   ```

## Voice Consistency Check

### Checking Content Against Brand

```bash
# Check content for brand alignment
python scripts/content/check_brand_alignment.py \
  --content output/content/draft.md \
  --guidelines references/brand-voice/ \
  --output output/analysis/alignment_report.md
```

### Alignment Report Format

```markdown
# Brand Voice Alignment Report

## Content Analyzed
[File/content identifier]

## Overall Score: [X/10]

## Voice Attribute Alignment
| Attribute | Score | Notes |
|-----------|-------|-------|
| [Attribute 1] | X/10 | [Notes] |
| [Attribute 2] | X/10 | [Notes] |
...

## Issues Found

### Tone Issues
- Line [X]: "[Quote]" - [Issue description]
  - Suggested: "[Rewrite]"

### Vocabulary Issues
- "[Word used]" → Suggest: "[Brand-appropriate word]"

### Style Issues
- [Issue and recommendation]

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
...
```

## Brand Voice Guide Template

```markdown
# [Brand Name] Brand Voice Guide

## Our Brand Personality

[Paragraph describing brand as a person]

**If [Brand] were a person, they would be:**
- [Description]

**Personality Traits:**
- [Trait 1]: [Description]
- [Trait 2]: [Description]
- [Trait 3]: [Description]

---

## Voice Attributes

### 1. [Attribute] - [Tagline]
**Definition:** [What this means]
**In practice:**
- ✅ DO: "[Example]"
- ❌ DON'T: "[Counter-example]"

### 2. [Attribute] - [Tagline]
...

---

## Tone by Context

| Situation | Tone | Example |
|-----------|------|---------|
| Social media | [Tone] | "[Example]" |
| Email marketing | [Tone] | "[Example]" |
| Support | [Tone] | "[Example]" |
| Sales | [Tone] | "[Example]" |

---

## Language Guidelines

### We Say / We Don't Say
| Instead of... | We say... |
|---------------|-----------|
| [Off-brand] | [On-brand] |
| [Off-brand] | [On-brand] |

### Power Words
[List of brand-aligned power words]

### Words to Avoid
[List of off-brand words]

---

## Writing Style

- **Contractions:** [Yes/No]
- **Point of view:** [First/Second/Third person]
- **Sentence length:** [Short/Medium/Varied]
- **Emoji usage:** [Never/Sometimes/Often]
- **Humor:** [Never/Subtle/Frequent]

---

## Core Messages

### Our Promise
[Value proposition statement]

### Key Messages
1. [Message 1]
2. [Message 2]
3. [Message 3]

### Elevator Pitch
[30-second pitch]

---

## Examples in Action

### Social Post
**On-brand:**
> [Example post]

**Off-brand:**
> [Counter-example]

### Email
**On-brand:**
> [Example email excerpt]

**Off-brand:**
> [Counter-example]

---

## Quick Reference Card

**Remember:** [Brand] is [Trait 1], [Trait 2], and [Trait 3].

**Our voice is:** [One-sentence summary]

**When in doubt:** [Quick rule]
```

## Example Interactions

### "Create a brand voice guide for my business"
```
[PLAN]
- Need full brand voice documentation
- Will create comprehensive guide
- Requires discovery questions

[CLARIFY]
- "Describe your brand personality"
- "Who is your target audience?"
- "What tone do competitors use?"
- "Share examples of content you love"
- "What should your brand NEVER sound like?"

[IMPLEMENT]
- Create full voice guide
- Document all components
- Include examples
- Provide quick reference card
```

### "Check if this content matches our brand voice"
```
[PLAN]
- Content alignment check
- Need existing brand guidelines
- Will provide detailed report

[CLARIFY]
- "Where are your brand voice guidelines?"
- "What specific aspects to check?"
- "Any known problem areas?"

[IMPLEMENT]
- Analyze content against guidelines
- Score alignment by attribute
- Flag specific issues
- Provide rewrite suggestions
```

### "Make our content more consistent"
```
[PLAN]
- Analyze current content
- Identify inconsistencies
- Create standards

[CLARIFY]
- "Sample content from different team members?"
- "Which pieces represent ideal voice?"
- "Any specific inconsistencies noticed?"

[IMPLEMENT]
- Audit content samples
- Identify variation patterns
- Create/update voice guide
- Provide alignment checklist
```

## Output Files

Brand voice documents saved to:
- `references/brand-voice/brand-voice-guide.md` - Full guide
- `references/brand-voice/tone-guide.md` - Tone spectrum
- `references/brand-voice/messaging-framework.md` - Messages
- `references/brand-voice/vocabulary.md` - Word lists
- `references/brand-voice/quick-reference.md` - One-page summary
- `output/analysis/voice_audit.md` - Content alignment reports

## Quality Checklist

For brand voice guides:
- [ ] Personality clearly defined
- [ ] 3-5 voice attributes with examples
- [ ] Tone spectrum for different contexts
- [ ] Specific vocabulary guidance
- [ ] Clear do/don't examples
- [ ] Messaging framework complete
- [ ] Quick reference available
- [ ] Practical and usable for team
