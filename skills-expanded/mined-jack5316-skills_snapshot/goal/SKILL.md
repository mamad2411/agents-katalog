---
name: goal
description: Track goals and review them against daily/weekly synthesis logs. Use when user asks to track goals, review goals, goal alignment, /goal, or check progress against logs.
---

# Goal Tracking Skill

Creates and tracks personal goals in `Goals/`. Reviews goal alignment against Daily Synthesis and Weekly Synthesis notes — what you actually did vs. what you want to achieve.

## Usage

```bash
# Create new goal
python3 _scripts/goal_track.py create "Goal Name" [--desc "Brief description"] [--target "Q2 2026"]

# List active goals
python3 _scripts/goal_track.py list [--all]

# Log progress to existing goal
python3 _scripts/goal_track.py log "Goal Name" "What you did"

# Review goals against daily/weekly synthesis
python3 _scripts/goal_track.py review [--days N] [--no-save]
```

- **create**: Creates a goal note. AI fleshes out Desired Outcome, Why This Matters, Target, Success Criteria.
- **list**: Lists goals in `Goals/`. Use `--all` to include inactive.
- **log**: Appends a dated log entry to an existing goal (partial name match).
- **review**: Cross-references active goals with Daily/Weekly Synthesis notes from Sources/. AI assesses alignment, gaps, surprises, and recommendations. Saves to `Sources/Goal Review - YYYY-MM-DD.md` unless `--no-save`.

## Output

- **Goals**: `Goals/{Goal Name}.md` — Desired Outcome, Why, Target, Success Criteria, Log
- **Review**: `Sources/Goal Review - YYYY-MM-DD.md` — Alignment, Gaps, Surprises, Recommendations

Uses `[[wikilinks]]` for Obsidian interconnection. YAML frontmatter: `status`, `target`, `tags`.

## Prerequisites for Review

The `review` command needs Daily Synthesis and Weekly Synthesis notes in `Sources/`. Run:
- `python3 _scripts/daily_synthesis.py` (after daily curation)
- `python3 _scripts/weekly_synthesis.py` (weekly)

## Agent workflow

When user says "/goal" or "track goals" or "review goals against my logs":

1. **Create**: Run `create` with goal name and optional description/target
2. **List**: Run `list` to show active goals
3. **Log**: Run `log` with goal name and progress note
4. **Review**: Run `review` to generate alignment report (use `--days 14` for 2 weeks of synthesis)
