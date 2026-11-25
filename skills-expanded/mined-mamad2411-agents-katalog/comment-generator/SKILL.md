# QCOMMENT Skill

Generate authentic, human-sounding comments for Substack articles based on Travis's real experiences.

## Purpose

Review comment drafts created by the comment-generator pipeline and produce publication-ready comments that:
1. Sound authentically human (not AI-generated)
2. Add genuine value to the conversation
3. Are grounded in Travis's real stories and frameworks
4. Maintain diversity across comment styles

## Usage

```bash
# Review all pending drafts
QCOMMENT

# Review specific draft
QCOMMENT --draft draft-20260129-120000-a1b2

# Batch approve/reject with reasons
QCOMMENT --batch
```

## Pipeline Context

This skill operates on comment jobs created by the comment-generator cron job (CRON-016).

**Input**: `/content/n8n/outbox/*.json` (jobs with `status: "draft"` and `type: "substack_comment"`)
**Output**: Updated job with filled `comment` field and `status: "ready"`

## Draft Structure

Each draft contains:
```json
{
  "id": "draft-YYYYMMDD-HHMMSS-xxxx",
  "status": "pending_review",
  "request": {
    "article": { "title", "author", "content_excerpt" }
  },
  "match": {
    "quality": "strong|good|weak",
    "matched_stories": [...],
    "matched_frameworks": [...]
  },
  "selected_approach": {
    "approach": "experience-matcher|question-first|...",
    "reason": "..."
  },
  "generation_context": {
    "primary_story": { "name", "summary", "specifics" },
    "suggested_angle": "...",
    "word_count_target": { "min": 80, "max": 150 },
    "phrases_to_avoid": [...]
  }
}
```

## Approach Guidelines

### 1. Experience-Matcher (Primary)
Share a specific story with concrete details.

**Pattern**:
```
[Specific hook to article] + [Your story with numbers/timeframes] + [Outcome or lesson]
```

**Example**:
> The GSK story hit home. We had the exact same fear when our automated testing caught a false positive that would've halted a $2M batch. Took us 3 weeks to build the confidence to trust the system. What changed it: we started with 'advisory mode' - alerts but no auto-holds. 47 correct catches later, the team asked us to turn on auto-hold.

**Must include**:
- Specific numbers (dollar amounts, timeframes, percentages)
- Real outcomes (including negative aspects)
- Connection to article topic

### 2. Question-First (Fallback)
Lead with genuine curiosity.

**Pattern**:
```
[Question you actually want answered] + [Brief context for why you're curious]
```

**Example**:
> Curious about the timeline here - did the resistance happen before or after people saw the first results? In my experience the skeptics convert faster when they witness a win, but I'm wondering if your team had a different pattern.

**Must include**:
- Non-rhetorical question
- Reason for curiosity
- Optional: brief relevant context

### 3. Relationship-Builder
Focus on connection with known authors.

**Pattern**:
```
[Reference to shared context] + [Personal connection] + [Forward-looking element]
```

**Example**:
> This builds perfectly on what you said about permission structures last month. I've been thinking about your "trust radius" concept since then - finally tested it with our compliance team. Would love to compare notes on what worked.

### 4. Contrarian-Additive (High Risk)
Extend or thoughtfully challenge the idea.

**Pattern**:
```
[Acknowledge the point] + [Add nuance or edge case] + [Question or insight]
```

**Example**:
> The three-tier model makes sense for established teams, but I'm wondering about the bootstrap phase. When you're still building trust, jumping to tier 2 too fast can backfire. We found a "tier 1.5" worked better - demonstrate value in low-stakes areas first before asking for real autonomy.

**Caution**: Only use when you have genuine expertise and the addition adds real value.

### 5. Minimalist
Short, punchy reaction.

**Pattern**:
```
[One specific insight or reaction]
```

**Example**:
> "Advisory mode before auto-mode" - stealing this for our next rollout.

**Must be**: Specific, not generic praise.

## Phrases to AVOID (AI Tells)

Never use these phrases - they're dead giveaways:
- "This really resonated with me"
- "Great article"
- "In my experience" (overused)
- "I love how you..."
- "Thanks for sharing"
- "You make such a great point"
- "This is so true"
- "Couldn't agree more"
- "Well said"
- "Spot on"
- "Love this"

## Signals to PRESERVE (Human Tells)

These make comments feel human:
- Specific numbers and names
- Real outcomes including failures
- Emotional honesty
- Incomplete resolutions ("still figuring this out")
- Vulnerability
- Tangential but genuine connections

## Quality Checklist

Before approving a comment:

1. **Specificity**: Does it include concrete details?
2. **Authenticity**: Could only Travis have written this?
3. **Value-add**: Does it contribute to the conversation?
4. **Non-generic**: Avoids AI-tell phrases?
5. **Length**: Within word count target?
6. **Approach-fit**: Matches selected approach style?

## Workflow

1. **Load draft**: Read draft JSON from comment-drafts/
2. **Review context**: Understand article, match quality, selected approach
3. **Generate comment**: Following approach guidelines
4. **Self-check**: Run quality checklist
5. **Update draft**: Set status to 'approved' or 'needs_edit'
6. **Save**: Write updated draft back

## Tools

### tools/draft-reviewer.py
Review and score a draft comment.

```bash
python tools/draft-reviewer.py draft-id

# Output:
{
  "scores": {
    "specificity": 85,
    "authenticity": 90,
    "value_add": 80,
    "phrase_check": 100,
    "length_check": true
  },
  "issues": [],
  "recommendation": "approve"
}
```

### tools/batch-status.py
Show status of all drafts.

```bash
python tools/batch-status.py

# Output:
Pending: 5
Approved: 12
Rejected: 3
Edited: 2
```

## Integration

After approval, comments can be:
1. Posted manually via Substack web interface
2. Queued for posting via browser automation
3. Archived with metadata for learning

## Metrics

Track weekly:
- Comments generated vs posted
- Approval rate (target: >70%)
- Skip rate from pipeline (target: 60-70%)
- Approach diversity (no >40% single approach)
- Author response rate (target: >20%)
