---
name: project-memory-loader
description: >-
  Loads and applies Project Memory context at the start of EPCI workflows.
  Auto-invoke when any EPCI command starts (/epci-brief, /epci, /epci-quick,
  /epci-spike, /epci-decompose). Provides conventions, patterns, settings,
  and historical context for consistent code generation.
allowed-tools: [Read, Glob]
---

# Project Memory Loader

## Purpose

This skill loads the Project Memory context at the beginning of each EPCI workflow.
It ensures that all code generation follows project conventions, uses established
patterns, and benefits from historical learning.

## When to Load

**Always load at the start of:**
- `/epci-brief` — Before exploration
- `/epci` — Before each phase
- `/epci-quick` — Before implementation
- `/epci-spike` — Before exploration
- `/epci-decompose` — Before analysis

## Loading Process

### Step 1: Check for Project Memory

```
Check if `.project-memory/` directory exists in project root.
```

**If not found:** Continue without context. At workflow end, suggest:
```
💡 No Project Memory detected. Run `/epci-memory init` to enable
   learning, conventions, and velocity tracking.
```

### Step 2: Load Required Files

Load the following files in order. Each file serves a specific purpose.

#### 2.1 Context — `.project-memory/context.json`

**Extract:**
```json
{
  "project.name": "Project identifier",
  "project.stack": "Tech stack (e.g., 'python-django', 'php-symfony')",
  "project.framework_version": "Framework version",
  "team.code_style": "Code style preference"
}
```

**Usage:**
- Auto-detect appropriate stack skill
- Set framework-specific defaults
- Apply code style preferences

#### 2.2 Conventions — `.project-memory/conventions.json`

**Extract:**
```json
{
  "naming": {
    "files": "kebab-case | snake_case | PascalCase",
    "classes": "PascalCase",
    "functions": "camelCase | snake_case",
    "variables": "camelCase | snake_case",
    "constants": "UPPER_SNAKE_CASE"
  },
  "structure": {
    "source_dir": "src/",
    "tests_dir": "tests/",
    "docs_dir": "docs/"
  },
  "code_style": {
    "max_line_length": 120,
    "indent": "spaces | tabs",
    "indent_size": 4
  }
}
```

**Usage:**
- Apply naming conventions to all generated code
- Place files in correct directories
- Format code according to style rules

#### 2.3 Settings — `.project-memory/settings.json`

**Extract:**
```json
{
  "flags": {
    "default_thinking": "think | think-hard | ultrathink",
    "auto_safe_for_sensitive": true
  },
  "hooks": {
    "enabled": true,
    "fail_on_error": false
  },
  "breakpoints": {
    "require_confirmation": true
  }
}
```

**Usage:**
- Apply default flags if not explicitly set
- Configure hook behavior
- Set breakpoint behavior

#### 2.4 Patterns — `.project-memory/patterns/detected.json`

**Extract:**
```json
{
  "patterns": [
    {
      "id": "repository-pattern",
      "confidence": 0.95,
      "files": ["src/Repository/*.php"]
    },
    {
      "id": "command-pattern",
      "confidence": 0.88,
      "files": ["src/commands/*.md"]
    }
  ]
}
```

**Usage:**
- Suggest consistent architectural patterns
- Guide file placement decisions
- Inform refactoring strategies

### Step 3: Load Optional Files (if exist)

These files enhance context but are not required.

#### 3.1 Velocity — `.project-memory/metrics/velocity.json`

**Extract:**
```json
{
  "summary": {
    "total_features": 15,
    "avg_completion_time": "2h 30m"
  },
  "trend": {
    "velocity_trend": "improving | stable | declining"
  },
  "by_complexity": {
    "TINY": {"count": 5, "avg_time": "10m"},
    "SMALL": {"count": 6, "avg_time": "45m"},
    "STANDARD": {"count": 3, "avg_time": "3h"},
    "LARGE": {"count": 1, "avg_time": "8h"}
  }
}
```

**Usage:**
- Calibrate time estimates
- Identify complexity patterns
- Track improvement trends

#### 3.2 Feature History — `.project-memory/history/features/*.json`

**Scan for:** Similar features by keywords

**Extract:**
```json
{
  "slug": "user-authentication",
  "complexity": "STANDARD",
  "patterns_used": ["repository-pattern", "service-pattern"],
  "files_created": ["src/Auth/*.php"],
  "lessons_learned": ["Use JWT for API tokens"]
}
```

**Usage:**
- Suggest reuse of patterns from similar features
- Avoid repeating past mistakes
- Leverage proven solutions

#### 3.3 Learning Preferences — `.project-memory/learning/preferences.json`

**Extract:**
```json
{
  "disabled_patterns": ["singleton"],
  "preferred_approaches": {
    "testing": "TDD",
    "documentation": "inline"
  }
}
```

**Usage:**
- Avoid suggesting disabled patterns
- Follow user's preferred approaches
- Respect past decisions

## Context Application Matrix

| Loaded Data | Where Applied |
|-------------|---------------|
| `conventions.naming` | All generated code, file names |
| `conventions.structure` | File placement, imports |
| `conventions.code_style` | Code formatting |
| `patterns.detected` | Architecture suggestions |
| `settings.flags` | Default flag values |
| `velocity.by_complexity` | Time estimates |
| `history.similar` | "Similar feature X used Y" suggestions |
| `learning.disabled` | Filter out rejected patterns |

## Memory Status Display

At workflow start, display loaded context summary:

```
📚 PROJECT MEMORY LOADED
├── Project: {project.name} ({project.stack})
├── Conventions: {naming.files} files, {naming.functions} functions
├── Patterns: {patterns.count} detected
├── History: {features.count} features completed
└── Velocity: {trend} trend, avg {avg_time} per feature
```

## Error Handling

| Condition | Action |
|-----------|--------|
| File missing | Skip with debug log, continue |
| Invalid JSON | Warn user, skip file, continue |
| Empty directory | Suggest `/epci-memory init` |
| Partial data | Use available data, log gaps |

## Integration with Hooks

This skill complements the hook system:
- **Reading** context → `project-memory-loader` skill (this)
- **Writing** context → `post-phase-3-memory-update.py` hook
- **Breakpoint context** → `on-breakpoint-memory-context.py` hook

## Performance Notes

- Load only required files for the current phase
- Cache loaded context for duration of workflow
- Avoid re-reading unchanged files within same session
