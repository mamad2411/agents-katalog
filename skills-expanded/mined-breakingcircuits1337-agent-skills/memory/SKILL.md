# Memory Skill

Use this skill to remember and recall information across conversations.

## Triggers

- `/remember`
- `/recall`
- `/forget`
- `/memory`
- "remember that"
- "don't forget"
- "I need to remember"

## Usage

### Add to Playbook

```
/remember Use python3 -m venv for virtual environments
```

Categories: strategies, errors, preferences, commands

```
/remember --category errors TypeError means something is None
/remember --category preferences Sarah prefers concise responses
```

### Search Playbook

```
/recall python
/recall azure
/recall
```

### Remove Entry

```
/forget str-00001
/forget python
```

### Vote on Entry

```
/vote str-00001 helpful   # Mark as helpful
/vote str-00001 harmful  # Mark as not helpful
```

### View Stats

```
/memory stats
/memory status
```

### Export/Import

```
/memory export ~/playbook.md
/memory import ~/playbook.md
```

## Auto-Learn (Phase 3)

### Learn from Error

Automatically extract insights from error messages:

```
memory learn error "TypeError: 'NoneType' object is not subscriptable"
# Learns: "Check if object exists before indexing"
```

### Learn from Feedback

Learn from user corrections:

```
memory learn feedback "That was wrong, use black instead"
# Learns: "Correction noted: That was wrong, use black instead"
```

### Review Playbook

Get suggestions for improving the playbook:

```
memory review
# Shows entries with low helpful/harmful ratio
```

### Configuration

```
memory config                    # Show all settings
memory config learn_from_errors true   # Enable/disable
memory config learn_from_feedback true
```

## ACE Framework (Phase 4)

Full ACE (Agentic Context Engineering) integration for self-improving playbooks.

### ACE Status

Show ACE system status:

```
memory ace status
# Output:
# {
#   "ace_enabled": true,
#   "total_entries": 15,
#   "quality_distribution": {"high_value": 3, "neutral": 10, "low_quality": 2}
# }
```

### ACE Run

Run ACE cycle to generate insights:

```
memory ace run coding "Python debugging session"
memory ace run debugging "Error in traceback"
memory ace run general "Any context here"
```

This:
1. **Generator** - Creates insights based on context
2. **Reflector** - Analyzes for lessons
3. **Curator** - Adds to playbook (with deduplication)

### ACE Enable/Disable

```
memory ace enable
memory ace disable
```

### ACE Deduplicate

Find and merge duplicate entries:

```
memory ace deduplicate
```

## Files

- Script: `scripts/memory.py`
- Playbook: `~/.config/opencode/memory/playbook.md`
- Data: `~/.config/opencode/memory/memory.json`
- Config: `~/.config/opencode/memory/config.json`

## Examples

```
> memory ace run coding "working on Python function"
{
  "generated": ["Use type hints for better code clarity"],
  "lessons": [],
  "added": ["[str-00001]"],
  "total_entries": 16
}

> memory ace status
{
  "ace_enabled": true,
  "total_entries": 16,
  "quality_distribution": {"high_value": 3, "neutral": 11, "low_quality": 2}
}

> memory ace deduplicate
Deduplicated. Added: [...]
```
