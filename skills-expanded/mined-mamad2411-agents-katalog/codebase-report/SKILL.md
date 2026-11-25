---
name: codebase-report
description: Structured codebase reporting skill. Combines outputs from codebase-analyzer and codebase-learner agents into a unified report covering architecture, data flow, coding patterns, gotchas, confidence ratings, and recommended study paths. Used when onboarding new developers or auditing an unfamiliar codebase.
origin: AI Dev Kit
---

# Codebase Report

Combine architecture analysis and codebase learning into a unified, structured report.

## When to Use

- Onboarding a new developer (human or AI agent) to an unfamiliar codebase
- Auditing a codebase before making significant changes
- Preparing documentation for external contributors
- Evaluating a codebase for acquisition or integration

## Report Structure

The report combines the architectural view from `codebase-analyzer` with the practical understanding from `codebase-learner`:

```markdown
# Codebase Report: <project-name>

---

## Executive Summary
<3-5 sentences: what this project is, its health, and the overall assessment>

---

## Project Overview
- **Purpose**: What the project does in one sentence
- **Tech Stack**: Languages, frameworks, databases, build tools
- **Size**: File count, line count, test count, coverage percentage
- **Maturity**: Age, release frequency, active maintenance

---

## Architecture

### System Diagram
<ASCII diagram of the system architecture>

### Layer Map
- Presentation layer: what handles incoming requests
- Business logic: where the domain logic lives
- Data layer: storage, caching, external APIs
- Infrastructure: config, middleware, deployment

### Module Boundaries
<How the codebase is organized, which directories are independent>

### Dependency Graph
<Which modules depend on which others, highlighting circular deps and god modules>

---

## Data Flow

### Key Feature Walkthroughs
<Trace 2-3 representative features from entry to storage and back>

### State Management
<How state is stored and transformed across the system>

### Error Handling
<How errors are caught, logged, and surfaced to users>

---

## Coding Conventions

### Style Guide (Inferred from Code)
| Convention | Pattern | Example |
|---|---|---|
| Variable naming | | |
| File naming | | |
| Error handling | | |
| Test structure | | |
| Import ordering | | |

### Common Idioms
<Patterns that appear repeatedly — factory functions, dependency injection, etc.>

### Anti-Patterns Detected
<Patterns that violate best practices — God files, circular deps, hardcoded values>

---

## Structural Health

### Code Smells
| Issue | Severity | Location |
|---|---|---|
| | high/medium/low | |

### Technical Debt
- TODO/FIXME/HACK count and age distribution
- Duplicated code instances
- Untested files
- Deprecated dependencies

### Architectural Violations
| Violation | Impact | Recommendation |
|---|---|---|
| | | |

---

## Gotchas

<Non-obvious things that will trip up new developers>

| Gotcha | Impact | Workaround |
|---|---|---|
| Must run migration before first start | Crash on startup | `npm run db:migrate` |
| God file with side effects on import | Unpredictable behavior | Import specific functions only |

---

## Confidence Map

<Rate confidence level in each area after analysis>

| Area | Confidence | Notes |
|---|---|---|
| | high/medium/low | |

---

## Recommended Study Path

<Ordered list for learning the codebase effectively>

1. Start with: <easiest to understand>
2. Then: <depends on understanding from step 1>
3. Then: <depends on step 2>
4. Finally: <most complex areas>

---

## Open Questions

<Things that need human input or further investigation>

1. <Question 1>
2. <Question 2>

---

## Dependencies Health

| Package | Version | Last Updated | CVEs | Status |
|---|---|---|---|---|
| | | | | ✓/⚠/✗ |

---

## Appendix

### File Inventory
<Complete file list with line counts>

### Test Coverage Detail
<Per-file coverage breakdown>

### Git Activity
<Most-edited files, recent changes, contributor summary>
```

## How to Generate

1. Run `codebase-analyzer` agent for architecture, data flow, dependency analysis
2. Run `codebase-learner` agent for pattern learning, gotcha hunting, confidence mapping
3. Combine both outputs into the unified report format above
4. Save to `.workflow/codebase-report/report-<date>.md`
5. Highlight critical findings (security issues, architectural violations) for immediate attention

## Integration with Multi-Agent Workflow

This skill is triggered as part of the `multi-agent-git-workflow` research wave:

```
[Repo Scanner] → maps surfaces
       ↓
[Codebase Analyzer] → architecture, data flow, patterns
       ↓
[Codebase Learner] → studies conventions, finds gotchas
       ↓
[Codebase Report] → unified report combining both analyses
```

The report is then used by the Micro-Task Decomposer to make informed task breakdowns that respect existing conventions and avoid known pitfalls.
