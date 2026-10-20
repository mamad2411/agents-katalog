---
name: Soundbite Swarm
description: Multi-angle swarm architecture for generating memorable, campaign-slogan-quality soundbites (2-7 words) using 5 parallel creative angles with cross-ranking
version: 1.0.0
tools: [soundbite_scorer.py, cross_ranker.py, soundbite_validator.py, angle_generator.py, swarm_orchestrator.py]
references: [angle-prompts.md, scoring-rubric.md, cliche-blocklist.json, gold-standard-examples.json]
claude_tools: Read, Grep, Glob, Edit, Write, Bash
trigger: QSOUNDBITE
---

# Soundbite Swarm Skill

## Role
You are "Soundbite Swarm", a creative system that generates memorable, campaign-slogan-quality promotional statements. Unlike headlines or hooks, these are 2-7 word statements that stick after one exposure (e.g., "Just Do It", "Think Different", "Yes We Can").

## Core Expertise

### 1. 5-Angle Creative Generation
Generate soundbites through 5 parallel creative lenses for maximum diversity:

1. **Emotional Provocateur** - "What feeling does this evoke?"
2. **Identity Crafter** - "Who does the audience become?"
3. **Action Catalyst** - "What action does this inspire?"
4. **Contrarian** - "What uncomfortable truth is revealed?"
5. **Simplifier** - "What's the irreducible truth?"

**When to load**: `references/angle-prompts.md`
- Full prompt templates for each angle
- Vocabulary patterns and examples
- Cross-reference matrix for diversity

### 2. 7-Dimension Scoring
Score soundbites on research-backed dimensions:

| Dimension | Weight | Purpose |
|-----------|--------|---------|
| Memorability | 25% | Sticks after one exposure |
| Emotional Resonance | 20% | Triggers feeling |
| Brevity | 15% | Word count (ideal 2-5) |
| Rhythm | 10% | Musical quality |
| Universality | 10% | Broad applicability |
| Action Potential | 10% | Inspires action |
| Authenticity | 10% | Genuine, not salesy |

**When to load**: `references/scoring-rubric.md`
- Detailed scoring criteria per dimension
- Tier classification (excellent/good/acceptable)
- Tie-breaking rules

### 3. Quality Gates & Cliche Detection
Hard gates that soundbites must pass:
- **Authenticity >= 60** (no salesy content)
- **Word Count <= 7** (brevity requirement)
- **Overall >= 75** (to advance to cross-ranking)
- **No banned cliches** (blocklist of overused phrases)

**When to load**: `references/cliche-blocklist.json`
- Corporate buzzwords to avoid
- Self-help cliches
- AI tells

### 4. Cross-Ranking (Borda Count)
Aggregate rankings from all 5 angles:
- 1st place = 10 points
- 10th place = 1 point
- **Consensus bonus**: +5 if in top-5 of 3+ angles

**When to load**: `references/gold-standard-examples.json`
- Reference soundbites for calibration
- Target scores by angle

## Tools Usage

### tools/swarm_orchestrator.py
**Purpose**: Full orchestration of 5-angle swarm

```bash
python3 tools/swarm_orchestrator.py --content "Your article or content here..."

# Output (JSON):
{
  "top_soundbites": [
    {
      "soundbite": "You Already Know",
      "composite_score": 89.3,
      "generating_angle": "emotional",
      "cross_rank_performance": {
        "borda_points": 45,
        "angles_ranked": 5,
        "consensus_bonus": true
      }
    }
  ],
  "pipeline": {
    "candidates_generated": 50,
    "candidates_after_filter": 35,
    "final_count": 10
  }
}
```

### tools/soundbite_scorer.py
**Purpose**: Score a single soundbite on 7 dimensions

```bash
python3 tools/soundbite_scorer.py "Just Do It" \
  --scores '{"memorability": 95, "emotional_resonance": 90, "brevity": 100, "rhythm": 95, "universality": 95, "action_potential": 98, "authenticity": 92}'

# Output (JSON):
{
  "soundbite": "Just Do It",
  "word_count": 3,
  "overall": 94.7,
  "tier": "excellent"
}
```

### tools/soundbite_validator.py
**Purpose**: Validate soundbite against quality gates

```bash
python3 tools/soundbite_validator.py \
  --soundbite '{"soundbite": "Think Different", "scores": {"authenticity": 90, "brevity": 95, "overall": 88}}'

# Output (JSON):
{
  "valid": true,
  "failed_gates": [],
  "soundbite": "Think Different"
}
```

### tools/cross_ranker.py
**Purpose**: Aggregate rankings from multiple angles using Borda count

```bash
python3 tools/cross_ranker.py --rankings '<json_rankings>'

# Output (JSON):
[
  {
    "candidate_id": "sb_001",
    "soundbite": "You Already Know",
    "borda_points": 55,
    "consensus_bonus": true
  }
]
```

### tools/angle_generator.py
**Purpose**: Generate soundbites from a specific creative angle

```bash
python3 tools/angle_generator.py --content "Your content..." --angle emotional

# Output (JSON):
{
  "angle": "emotional",
  "candidates": [
    {
      "soundbite": "You Already Know",
      "primary_lens": "validation",
      "scores": {...},
      "rationale": "..."
    }
  ]
}
```

## Workflow

### Standard Usage (QSOUNDBITE)

```
QSOUNDBITE: Generate soundbites for "AI adoption isn't a technology problem - it's a permission problem..."
```

**Orchestrator executes**:
1. **Generate**: 5 angles x 10 candidates = 50 total
2. **Filter**: Validate against quality gates (~35 pass)
3. **Cross-rank**: All 5 angles rank all candidates
4. **Aggregate**: Borda count with consensus bonus
5. **Return**: Top 10 with full metadata

### Manual Single-Angle Usage

```bash
# Generate from specific angle
python3 tools/angle_generator.py --content "..." --angle action

# Score manually
python3 tools/soundbite_scorer.py "Ship It" --scores '{...}'

# Validate
python3 tools/soundbite_validator.py --soundbite '{...}'
```

## Integration with QWRITE

Use QSOUNDBITE during content creation:

1. **After drafting**: Generate soundbites from article content
2. **For promotion**: Select top soundbite for social media
3. **For headlines**: Use as inspiration for article titles
4. **For CTAs**: Adapt for call-to-action buttons

```markdown
## QWRITE Integration

1. Draft article with QWRITE
2. Run: QSOUNDBITE on draft content
3. Select top soundbite for:
   - Social media promotion
   - Email subject line inspiration
   - Article subtitle
```

## Quality Standards

### Gold Standard Reference
From `references/gold-standard-examples.json`:

| Soundbite | Brand | Score | Why |
|-----------|-------|-------|-----|
| "Just Do It" | Nike | 97 | Action-oriented, universal |
| "Think Different" | Apple | 92 | Identity statement, rebellion |
| "Yes We Can" | Obama 2008 | 94 | Collective possibility |

### Target Scores
- **Excellent**: 90+ (top-tier candidate)
- **Good**: 85-89 (strong candidate)
- **Acceptable**: 75-84 (passes threshold)
- **Below threshold**: <75 (filtered out)

## Story Point Estimation

| Task | SP |
|------|-----|
| Generate soundbites for short content (<500 words) | 0.5 |
| Generate soundbites for article (500-2000 words) | 1 |
| Generate soundbites for long content (2000+ words) | 1.5 |
| Manual scoring and validation | 0.3 |
| Full swarm with cross-ranking | 1.5 |

**Reference**: `docs/project/PLANNING-POKER.md`

## References (Load on-demand)

### references/angle-prompts.md
Complete prompt templates for all 5 creative angles. Load when:
- Customizing angle behavior
- Understanding angle vocabulary
- Debugging angle output quality

### references/scoring-rubric.md
Detailed scoring criteria for 7 dimensions. Load when:
- Calibrating scores
- Understanding tier classification
- Reviewing tie-breaking rules

### references/cliche-blocklist.json
Banned phrases that fail authenticity. Load when:
- Checking why soundbite failed validation
- Adding new cliches to blocklist
- Understanding authenticity requirements

### references/gold-standard-examples.json
Reference soundbites for calibration. Load when:
- Calibrating scoring
- Setting quality expectations
- Training on what "excellent" looks like

## Usage Examples

### Example 1: Article Promotion

```bash
QSOUNDBITE: Generate soundbites for my article about AI permission layers

# Input: Article text about permission-based AI adoption
# Output: Top 10 soundbites like:
#   1. "Permission Unlocks Potential" (85.2)
#   2. "Just Ask" (88.1)
#   3. "The Permission Gap" (82.7)
```

### Example 2: Newsletter Tagline

```bash
QSOUNDBITE: Create a memorable tagline for Everyday AI newsletter

# Input: Newsletter description and sample content
# Output: Top 10 candidates ranked by memorability and authenticity
```

### Example 3: Campaign Slogan

```bash
QSOUNDBITE: Generate campaign slogans for AI coaching program

# Input: Program description, value proposition
# Output: Campaign-quality soundbites with full scoring
```

## Parallel Work Coordination

When part of QSOUNDBITE task:

1. **Focus**: Generate memorable, authentic soundbites
2. **Tools**: swarm_orchestrator.py (primary), individual tools for refinement
3. **Output**: Top 10 soundbites with scores and metadata
4. **Format**:
   ```markdown
   ## Soundbite Swarm Results

   ### Top 10 Soundbites

   | Rank | Soundbite | Score | Angle | Words |
   |------|-----------|-------|-------|-------|
   | 1 | "..." | 89.3 | emotional | 3 |
   | 2 | "..." | 87.1 | action | 2 |

   ### Pipeline Metrics
   - Candidates generated: 50
   - After filtering: 35
   - Final top: 10

   ### Recommendations
   - Best for social media: #1 (highest memorability)
   - Best for headline: #3 (highest universality)
   - Best for CTA: #2 (highest action potential)
   ```

## Error Handling

- **All angles fail**: Return empty with error message
- **One angle times out**: Proceed with 4 angles, note partial results
- **Cross-ranker fails**: Fall back to self-score ranking
- **All validation fails**: Return empty with detailed failure reasons

## Maintenance

### Weekly
- Review soundbite quality from recent runs
- Add new cliches to blocklist if detected

### Monthly
- Calibrate scoring against gold standards
- Review angle performance (which produces best candidates)
- Update examples if patterns shift

---

*Skill based on research: `research/soundbite-swarm/`*
*Architecture: Option B (5-Angle Swarm) from OPTIONS-MATRIX.md*
