---
name: continuous-learning
description: Automatically extract reusable patterns from sessions and save them as learned skills for future use.
---

# Continuous Learning Skill

Automatically evaluates sessions to extract reusable patterns that can be saved as learned skills.

## How It Works

This skill evaluates sessions to:

1. **Session Evaluation**: Checks if session has enough messages (default: 10+)
2. **Pattern Detection**: Identifies extractable patterns from the session
3. **Skill Extraction**: Saves useful patterns to learned skills

## Pattern Types

| Pattern | Description |
|---------|-------------|
| `error_resolution` | How specific errors were resolved |
| `user_corrections` | Patterns from user corrections |
| `workarounds` | Solutions to framework/library quirks |
| `debugging_techniques` | Effective debugging approaches |
| `project_specific` | Project-specific conventions |

## Configuration

```json
{
  "min_session_length": 10,
  "extraction_threshold": "medium",
  "auto_approve": false,
  "patterns_to_detect": [
    "error_resolution",
    "user_corrections",
    "workarounds",
    "debugging_techniques",
    "project_specific"
  ],
  "ignore_patterns": [
    "simple_typos",
    "one_time_fixes",
    "external_api_issues"
  ]
}
```

## What Gets Extracted

**Good candidates for learning:**
- Error patterns that took multiple attempts to solve
- User corrections that improved output
- Workarounds for specific libraries/frameworks
- Debugging techniques that worked

**Filtered out:**
- Simple typo fixes
- One-time issues (API outages, etc.)
- External factors beyond control

## Manual Extraction

Use `/learn` command to manually extract patterns mid-session:

```
/learn "Discovered that Redis requires specific timeout handling for long-running searches"
```

## Best Practices

1. **Quality over quantity** - Only extract genuinely reusable patterns
2. **Be specific** - Include context about when the pattern applies
3. **Update regularly** - Review and prune learned skills periodically
4. **Share patterns** - Export useful patterns for team use
