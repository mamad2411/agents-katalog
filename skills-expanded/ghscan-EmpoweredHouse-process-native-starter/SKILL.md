# Code Review Skill

Performs a structured 15-point code review against the project's engineering standards.

## Usage

```
/review [target]
```

Where `[target]` is a file path, directory, or PR reference.

## Process

1. Load project context from `AGENTS.md` and `.ai/lessons.md`
2. Review code against the checklist in `references/checklist.md`
3. Report findings grouped by category with severity ratings

## Categories

- **Architecture** — Bounded contexts, separation of concerns, dependency direction
- **Security** — Input validation, CSRF, authentication, data isolation
- **Backend** — Context patterns, error handling, migrations, query patterns
- **Frontend** — Component patterns, accessibility, performance, i18n
- **Quality** — Type specs, test coverage, linting, documentation

## Output Format

```markdown
## Review: [target]

### [Category]
- [severity] [finding description]
  - File: [path:line]
  - Fix: [suggested fix]

### Summary
- Critical: N
- Warning: N
- Info: N
```

## References

@references/checklist.md
