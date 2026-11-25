---
name: ralph-converter
description: >-
  Converts EPCI specifications (markdown) to Ralph Wiggum format (prd.json).
  Generates ralph.sh script and PROMPT.md customized for the detected stack.
  Use when: /epci:decompose generates Ralph-compatible outputs (automatic since v5.1.2).
  Not for: Direct invocation, use /epci:decompose instead.
---

# Ralph Converter Skill

## Overview

This skill transforms EPCI specification files into Ralph Wiggum format:
- Markdown specs → prd.json (user stories)
- Stack detection → PROMPT.md (customized commands)
- Project setup → ralph.sh (executable script)

## prd.json Schema (v2)

**Version**: 2.0 — Enhanced structure for granular tracking

```json
{
  "$schema": "https://epci.dev/schemas/prd-v2.json",
  "version": "2.0",
  "branchName": "feature/my-feature",
  "projectName": "My Project",
  "generatedAt": "2025-01-14T10:00:00Z",
  "generatedBy": "EPCI /epci:decompose v5.2",
  "config": {
    "max_iterations": 50,
    "test_command": "npm test",
    "lint_command": "npm run lint",
    "granularity": "small"
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "Story title",
      "category": "backend",
      "type": "Logic",
      "complexity": "M",
      "priority": 1,
      "status": "pending",
      "passes": false,

      "acceptanceCriteria": [
        {"id": "AC1", "description": "Criterion description", "done": false},
        {"id": "AC2", "description": "Another criterion", "done": false}
      ],

      "tasks": [
        {"id": "T1", "description": "Task description", "done": false},
        {"id": "T2", "description": "Another task", "done": false}
      ],

      "dependencies": {
        "depends_on": [],
        "blocks": ["US-002"]
      },

      "execution": {
        "attempts": 0,
        "last_error": null,
        "files_modified": [],
        "completed_at": null,
        "iteration": null
      },

      "testing": {
        "test_files": [],
        "requires_e2e": false,
        "coverage_target": null
      },

      "context": {
        "parent_spec": "S01-core.md",
        "parent_brief": "docs/briefs/my-feature/brief.md",
        "estimated_minutes": 60
      }
    }
  ]
}
```

### Schema Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | string | Yes | Schema version ("2.0") |
| `id` | string | Yes | Unique story ID (US-001, US-002...) |
| `title` | string | Yes | Story title |
| `category` | string | Yes | backend, frontend, fullstack, infra, test, docs |
| `type` | string | Yes | Script, Logic, API, UI, Test, Task |
| `complexity` | string | Yes | S (Small), M (Medium), L (Large) |
| `priority` | number | Yes | 1 (Must), 2 (Should), 3 (Could) |
| `status` | string | Yes | pending, in_progress, completed, failed, blocked |
| `passes` | boolean | Yes | True if story passes (implies status=completed) |
| `acceptanceCriteria` | array | Yes | Array of {id, description, done} |
| `tasks` | array | Yes | Array of {id, description, done} |
| `dependencies` | object | Yes | {depends_on: [], blocks: []} |
| `execution` | object | Yes | Runtime tracking fields |
| `testing` | object | Yes | Test-related metadata |
| `context` | object | Yes | Traceability fields |

### Business Rules

- **RM1**: `passes = true` implies `status = "completed"` automatically
- **RM2**: `complexity` inferred from estimated time: S (<45min), M (45-90min), L (>90min)
- **RM3**: `estimated_minutes` calculated from complexity: S=30, M=60, L=120
- **RM4**: IDs are local per story: AC1, AC2, T1, T2 (not global)
- **RM5**: `blocks[]` is inverse-calculated from other stories' `depends_on[]`

## Conversion Rules

### From INDEX.md

```markdown
| ID | Title | Effort | Priority | Dependencies | Status |
|----|-------|--------|----------|--------------|--------|
| S01 | Core Models | 2j | 1 | - | Pending |
```

Maps to:
- Each spec becomes multiple stories based on effort
- 1 day ≈ 4 stories (15-30 min each)
- Priority preserved from INDEX

### From SXX-*.md Specs

Each spec file is parsed for:
- `## Tasks` section → individual stories
- `## Acceptance Criteria` → story AC
- Estimated effort → story count

### Granularity Settings

| Flag | Story Size | Stories/Day |
|------|------------|-------------|
| `--granularity micro` | 15-30 min | 8-12 |
| `--granularity small` | 30-60 min | 4-8 |
| `--granularity standard` | 1-2 hours | 2-4 |

---

## Inference Rules (v2)

### Type Inference

Infer `type` from title keywords (case-insensitive):

| Type | Keywords | Examples |
|------|----------|----------|
| Script | script, hook, bash, shell, automation, cron | "Add deployment script" |
| Logic | entity, model, service, function, business, handler | "Create User entity" |
| API | endpoint, route, controller, REST, GraphQL, api | "Add login endpoint" |
| UI | component, form, view, page, modal, button, ui | "Create login form" |
| Test | test, spec, coverage, e2e, unit, integration | "Write unit tests" |
| Task | (default if no match) | "Update dependencies" |

**Algorithm:**
```
FOR each keyword_set in TYPE_KEYWORDS:
    IF any keyword in title.lower():
        RETURN type
RETURN "Task"  # default
```

### Category Inference

Infer `category` from file patterns and content:

| Category | Patterns | File indicators |
|----------|----------|-----------------|
| backend | Entity, Repository, Service, Controller, Model | `src/Entity/`, `app/Models/`, `services/` |
| frontend | Component, View, CSS, React, Vue, Angular | `components/`, `views/`, `*.tsx`, `*.vue` |
| fullstack | Mix of backend + frontend in same story | Both patterns detected |
| infra | Docker, CI, deploy, config, nginx, k8s | `Dockerfile`, `.github/`, `deploy/` |
| test | Test files only | `tests/`, `__tests__/`, `*Test.php` |
| docs | Documentation, README, changelog | `docs/`, `*.md`, `README` |

**Algorithm:**
```
backend_score = count_matches(BACKEND_PATTERNS, title + files)
frontend_score = count_matches(FRONTEND_PATTERNS, title + files)

IF backend_score > 0 AND frontend_score > 0:
    RETURN "fullstack"
ELIF backend_score > frontend_score:
    RETURN "backend"
ELIF frontend_score > backend_score:
    RETURN "frontend"
ELSE:
    RETURN infer_from_file_paths(files)
```

### Complexity Inference

Infer `complexity` from estimated minutes:

| Complexity | Minutes | Criteria |
|------------|---------|----------|
| S (Small) | 30 | < 45 minutes |
| M (Medium) | 60 | 45-90 minutes |
| L (Large) | 120 | > 90 minutes |

**Reverse calculation** (if minutes not specified):
- Count tasks: 1-2 tasks → S, 3-4 tasks → M, 5+ tasks → L
- Count AC: 1-2 AC → S, 3-4 AC → M, 5+ AC → L

---

## Extraction Rules (v2)

### Acceptance Criteria Extraction

Extract `acceptanceCriteria[]` from spec files:

**Source patterns:**
1. `## Acceptance Criteria` section with bullet points
2. `| ID | Criterion |` table format
3. `- [ ] Given... When... Then...` checklist

**Algorithm:**
```
FOR each spec_file:
    IF has_section("## Acceptance Criteria"):
        PARSE bullets or table
        FOR each item:
            CREATE {id: "AC{n}", description: item, done: false}
    ELIF has_checklist("- [ ]"):
        PARSE checklist items
    ELSE:
        CREATE generic AC: "Story implemented and tested"
```

### Tasks Extraction

Extract `tasks[]` from spec files:

**Source patterns:**
1. `## Tasks` section with checklist `- [ ]`
2. `## 3. Tasks` numbered section
3. Infer from AC if no explicit tasks

**Algorithm:**
```
FOR each spec_file:
    IF has_section("## Tasks"):
        PARSE checklist items
        FOR each item:
            CREATE {id: "T{n}", description: item, done: false}
    ELSE:
        # Infer tasks from AC
        FOR each ac in acceptanceCriteria:
            CREATE task from AC description
```

### Dependencies Extraction

Calculate `dependencies` from specs and INDEX:

**Source patterns:**
1. Explicit: "depends on S01", "requires S02", "after S03"
2. INDEX.md Dependencies column
3. ForeignKey references (Django/Doctrine)
4. Import statements

**Algorithm:**
```
FOR each story:
    depends_on = []

    # Check explicit dependencies
    IF spec mentions "depends on {ID}":
        depends_on.append(ID)

    # Check INDEX dependencies column
    IF INDEX has dependencies for this spec:
        depends_on.extend(parse_dependencies(INDEX))

    # Calculate blocks (inverse)
    FOR each other_story:
        IF this_story.id in other_story.depends_on:
            blocks.append(other_story.id)
```

---

## Stack Detection

Detect project stack to customize PROMPT.md:

| File | Stack | Commands |
|------|-------|----------|
| `package.json` | Node.js | npm test, npm run lint |
| `composer.json` | PHP | composer test, php-cs-fixer |
| `requirements.txt` | Python | pytest, flake8 |
| `Cargo.toml` | Rust | cargo test, cargo clippy |
| `go.mod` | Go | go test, golint |
| `pom.xml` | Java | mvn test, mvn checkstyle |

## Template Variables

For PROMPT.md generation:

| Variable | Source |
|----------|--------|
| `{PROJECT_NAME}` | package.json name or folder |
| `{TEST_COMMAND}` | Detected from stack |
| `{LINT_COMMAND}` | Detected from stack |
| `{BUILD_COMMAND}` | Detected from stack |
| `{STACK_RULES}` | Stack-specific best practices |

## Stack Rules Templates

### Node.js/TypeScript

```markdown
## Stack-Specific Rules

- Use TypeScript strict mode
- Run `npm run type-check` before committing
- Follow ESLint configuration
- Use Jest for testing
- Prefer async/await over callbacks
```

### Python

```markdown
## Stack-Specific Rules

- Follow PEP 8 style guide
- Use type hints (Python 3.9+)
- Run pytest with coverage
- Use black for formatting
- Prefer dataclasses over dicts
```

### PHP/Symfony

```markdown
## Stack-Specific Rules

- Follow PSR-12 coding standard
- Use PHP 8.1+ features
- Run PHPUnit for tests
- Use php-cs-fixer for formatting
- Follow Symfony best practices
```

## Generated Files

### ralph.sh

```bash
#!/bin/bash
# Generated by EPCI /epci:decompose
# Project: {PROJECT_NAME}
# Date: {DATE}

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Source utilities
source lib/circuit_breaker.sh
source lib/response_analyzer.sh
source lib/date_utils.sh

# Configuration
MAX_ITERATIONS=${MAX_ITERATIONS:-50}
PRD_FILE="prd.json"
PROGRESS_FILE="progress.txt"
PROMPT_FILE="PROMPT.md"

# Initialize
init_circuit_breaker

echo "🚀 Starting Ralph Loop — $(date)"
echo "   Max iterations: $MAX_ITERATIONS"
echo ""

for ((i=1; i<=MAX_ITERATIONS; i++)); do
    echo "═══════════════════════════════════════════"
    echo "🔄 Iteration $i of $MAX_ITERATIONS"
    echo "═══════════════════════════════════════════"

    # Check circuit breaker
    if should_halt_execution; then
        exit 1
    fi

    # Check rate limit
    if ! check_rate_limit; then
        echo "⏳ Waiting for rate limit reset..."
        sleep 60
        continue
    fi

    # Run Claude with context
    OUTPUT=$(claude --print \
        -f "$PROMPT_FILE" \
        -f "$PRD_FILE" \
        -f "$PROGRESS_FILE" \
        2>&1)

    echo "$OUTPUT"

    # Analyze response
    EXIT_DECISION=$(analyze_response "$OUTPUT" "$i")

    case "$EXIT_DECISION" in
        project_complete)
            echo "✅ Project complete!"
            exit 0
            ;;
        blocked)
            echo "🚫 Blocked — manual intervention required"
            exit 2
            ;;
        max_iterations)
            echo "⚠️ Max iterations reached"
            exit 1
            ;;
    esac

    # Update circuit breaker with progress
    FILES_CHANGED=$(git diff --name-only 2>/dev/null | wc -l || echo 0)
    HAS_ERRORS=$(echo "$OUTPUT" | grep -qi "error\|failed" && echo true || echo false)
    record_loop_result "$i" "$FILES_CHANGED" "$HAS_ERRORS"

    echo ""
done

echo "⚠️ Loop ended without completion"
exit 1
```

### fix_plan.md Template

```markdown
# Fix Plan — {PROJECT_NAME}

> Auto-generated by EPCI Ralph Converter

## Current Status

- [ ] Story US-001: {title}
- [ ] Story US-002: {title}
...

## Discovered Issues

(Claude will update this section with blockers)

## Learnings

(Claude will update with patterns discovered)
```

## Error Handling

| Error | Action |
|-------|--------|
| No specs found | Abort with message |
| Invalid INDEX.md | Suggest format fix |
| Unknown stack | Use generic PROMPT.md |
| Empty acceptance criteria | Warn, continue |

## Usage

This skill is invoked internally by `/epci:decompose` (automatic since v5.1.2):

```
/epci:decompose my-prd.md --granularity small
```

Outputs:
```
docs/specs/my-feature/
├── INDEX.md
├── S01-core.md
├── S02-api.md
├── prd.json        ← Ralph format
├── ralph.sh        ← Executable script
├── PROMPT.md       ← Customized prompt
├── progress.txt    ← Empty, for logging
└── lib/            ← Symlink to scripts/lib/
```
