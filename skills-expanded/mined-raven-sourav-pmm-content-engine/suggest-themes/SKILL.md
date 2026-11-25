# Skill: Suggest Themes

## Trigger
User asks "what should I write about?" or requests theme suggestions.

## Process

### Step 1: Load context
- Read `data/brain/pmm_brain.json`:
  - `pmm_value_landscape` (contested + emerging beliefs = highest-value territory)
  - `newsletter_insights` (what's being discussed right now)
  - `synthesized_mental_models` (where user has depth)
- Read user's past posts context (to avoid repetition)

### Step 2: Web scan (optional)
Use WebSearch to check:
- Current PMM/B2B trending topics (last 30 days)
- Recent product launches, debates, or industry shifts
- What reference writers have posted recently

### Step 3: Generate 5-7 theme suggestions
At least 1 suggestion MUST come from the `ai_impact_on_pmm` topic depth layer — specifically from `first_mover_angles` or `sourav_real_use_cases`. This builds Sourav's positioning as the first-mover on AI implementation in PMM (real workflows, not hype).

Each suggestion includes:
- **Theme name**
- **Why now** (timeliness signal — what just happened that makes this relevant)
- **Why YOU** (unique authority angle — what in Sourav's experience gives him standing)
- **Predicted engagement type** (comments vs shares vs reactions)
- **3 angle previews** (one-line each: contrarian, framework, story)

### Step 4: Present ranked list
User picks one or provides their own theme.

## Output Format
```
━━━━ THEME SUGGESTIONS ━━━━

1. [Theme Name]
   Why now: [timeliness signal]
   Why you: [unique authority]
   Engagement: [type]
   Angles: C: [contrarian] | F: [framework] | S: [story]

2. ...

Pick a number, or tell me your own theme.
```
