---
name: proactive-suggestions
description: >-
  Generates and manages proactive code suggestions during EPCI workflow.
  Auto-invoke when: /epci reaches BP2 (post-Phase 2), or when code review
  findings need to be transformed into actionable suggestions.
  Do NOT load for: /epci-quick (no formal breakpoints), /epci-spike (exploration only),
  or when suggestions are explicitly disabled via learning preferences.
---

# Proactive Suggestions (F06)

## Overview

Transforms code review findings and pattern detection results into prioritized,
actionable suggestions that learn from user preferences.

## Integration Points

| Phase | Trigger | Suggestion Types |
|-------|---------|------------------|
| BP1 (Post-Plan) | Plan validated | Architecture patterns, documentation |
| BP2 (Post-Code) | Code reviewed | Security, performance, quality |

## Suggestion Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐
│  Findings   │────▶│  Suggestion  │────▶│   Breakpoint   │
│  (Sources)  │     │   Engine     │     │    Display     │
└─────────────┘     └──────────────┘     └────────────────┘
      │                    │                     │
      ▼                    ▼                     ▼
 @code-reviewer      Score & Filter        💡 Section
 @security-auditor   Learning prefs        [Actions]
 @qa-reviewer        Prioritize P1>P2>P3
 PatternDetector
```

## Priority Levels

| Priority | Icon | Category | Examples |
|----------|------|----------|----------|
| **P1** | 🔒 | Security | Input validation, SQL injection, XSS |
| **P2** | ⚡/🧹 | Performance/Quality | N+1 query, god class, long method |
| **P3** | 🧹 | Style/Optimization | Magic numbers, dead code |

## Pattern Catalog

### Security (P1) - Critical
- `input-not-validated` - User input without validation
- `sql-injection` - SQL string concatenation
- `xss-vulnerability` - Unescaped output
- `csrf-missing` - Form without CSRF token
- `auth-missing` - Endpoint without auth check

### Performance (P2) - Important
- `n-plus-one-query` - Query in loop
- `missing-index` - Query on non-indexed column
- `large-payload` - Response without pagination
- `no-cache` - Repeated query without cache

### Quality (P2-P3) - Normal/Minor
- `god-class` - Class > 500 LOC
- `long-method` - Method > 50 LOC
- `magic-numbers` - Hardcoded constants
- `dead-code` - Unreachable code
- `duplicate-code` - Similar blocks > 20 LOC

## Scoring Algorithm

```python
score = base_score * impact_multiplier * preference_multiplier

where:
  base_score = PRIORITY_WEIGHTS[priority] / 100  # P1=1.0, P2=0.7, P3=0.5
  impact_multiplier = SEVERITY_IMPACT[severity]  # critical=1.5, minor=0.7
  preference_multiplier = 0.5 + (learning_score * 0.5)  # Range: 0.5-1.0
```

Suggestions with score < 0.3 are filtered out.

## User Actions

| Action | Effect | Learning Impact |
|--------|--------|-----------------|
| **[Accepter]** | Apply suggestion (if auto-fixable) | +1 preference |
| **[Voir détails]** | Show full explanation | Neutral |
| **[Ignorer]** | Skip for this session | Neutral |
| **[Ne plus suggérer]** | Disable pattern permanently | -∞ (blocklist) |

## Breakpoint Display Format

### Full Format (default)

```
│ 💡 SUGGESTIONS PROACTIVES                                           │
│ ├── [P1] 🔒 Input non validé (path:line)                           │
│ │   └── Suggestion: Ajouter validation                             │
│ ├── [P2] ⚡ N+1 Query (path:line)                                   │
│ │   └── Suggestion: JOIN FETCH                                      │
│ └── [P3] 🧹 Magic number (path:line)                               │
│     └── Actions: [Accepter tout] [Voir détails] [Ignorer]          │
```

### Compact Format (token optimization)

```
💡 Suggestions: [P1] 🔒 Input validation | [P2] ⚡ N+1 query | [P3] 🧹 Magic num
```

## Learning Integration (F08)

Preferences stored in `.project-memory/learning/preferences.json`:

```json
{
  "suggestion_feedback": {
    "input-not-validated": {
      "accepted": 5,
      "rejected": 1,
      "acceptance_rate": 0.83
    }
  },
  "disabled_suggestions": ["magic-numbers"],
  "settings": {
    "suggestion_threshold": 0.3,
    "max_suggestions_per_breakpoint": 5
  }
}
```

## Hook Integration

The `post-phase-2-suggestions.py` hook automatically:
1. Collects findings from subagent reviews
2. Runs PatternDetector on changed files
3. Generates scored suggestions
4. Returns formatted output for breakpoint

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `suggestion_threshold` | 0.3 | Minimum score to display |
| `max_suggestions_per_breakpoint` | 5 | Max suggestions shown |
| `learning_enabled` | true | Enable preference learning |

## Usage Example

```python
from project_memory.suggestion_engine import SuggestionEngine, Finding

engine = SuggestionEngine(memory_dir=".project-memory")

findings = [
    Finding(
        pattern_id="input-not-validated",
        file_path="src/Controller/UserController.php",
        line_number=42,
        severity="critical",
    )
]

suggestions = engine.generate_suggestions(findings)
output = engine.format_for_breakpoint(suggestions)
print(output)
```

## Dependencies

- **F04 Project Memory** - Pattern and preference storage
- **F08 Continuous Learning** - Preference scoring and adaptation
- **F03 Enriched Breakpoints** - Display templates
