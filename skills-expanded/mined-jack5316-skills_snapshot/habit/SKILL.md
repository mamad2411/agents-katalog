---
name: habit
description: Log and analyze behavioral patterns (habits). Use when user asks to track habits, log habits, habit check-in, analyze behavior patterns, /habit, or review habit compliance.
---

# Habit — Log and Analyze Behavioral Patterns

Track recurring behaviors and analyze patterns over time. Habits live in `Habits/`; analysis cross-references with Daily/Weekly Synthesis for cross-domain insights.

## Usage

```bash
# Create new habit
python3 _scripts/habit_track.py create "Habit Name" [--desc "Brief description"]

# List active habits
python3 _scripts/habit_track.py list [--all]

# Log check-in for today
python3 _scripts/habit_track.py log "Habit Name" [optional note]

# Analyze behavioral patterns
python3 _scripts/habit_track.py analyze [--days N] [--no-synthesis] [--no-save]
```

- **create**: Creates a habit note. AI fleshes out What It Is, Why Track It, When/How.
- **list**: Lists habits in `Habits/` with check-in counts. Use `--all` to include inactive.
- **log**: Records a check-in for today. Partial habit name match. Optional note (e.g., "Felt focused").
- **analyze**: Cross-references habit check-ins with Daily/Weekly Synthesis. AI produces streaks, trends, patterns, and cross-domain insights. Saves to `Sources/Habit Analysis - YYYY-MM-DD.md` unless `--no-save`. Use `--no-synthesis` to skip synthesis cross-reference.

## Output

- **Habits**: `Habits/{Habit Name}.md` — Definition + Check-ins (dated log)
- **Analysis**: `Sources/Habit Analysis - YYYY-MM-DD.md` — Streaks, trends, patterns, synthesis cross-reference

Uses `[[wikilinks]]` for Obsidian interconnection. YAML frontmatter: `status`, `tags`.

## Agent workflow

When user says "/habit" or "track habits" or "log habit" or "analyze my habits":

1. **Create**: Run `create` with habit name and optional description
2. **List**: Run `list` to show active habits
3. **Log**: Run `log` with habit name (and optional note) to record today's check-in
4. **Analyze**: Run `analyze` to generate pattern report (use `--days 30` for a month of data)
