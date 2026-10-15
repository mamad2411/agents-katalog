# Create GitHub Issue

Standard process for creating well-structured GitHub issues. Use for bugs, feature requests, and tasks.

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| GitHub | Create and label issues |

## Bug report template

```markdown
## Problem

[Clear description of what's broken. Include steps to reproduce.]

1. Step one
2. Step two
3. Observe: [what happens]

## Expected behavior

[What should happen instead]

**Environment**: [browser, OS, version, relevant config]
```

## Feature request template

```markdown
## Problem

[What user problem does this solve? Who is affected?]

## Expected behavior

[What the feature should do, from the user's perspective]

## Notes

[Optional: technical considerations, related issues, mockups]
```

## Labels

| Label | When to use |
|-------|------------|
| `bug` | Something is broken |
| `feature` | New functionality request |
| `enhancement` | Improvement to existing feature |
| `docs` | Documentation change needed |
| `good first issue` | Simple, well-scoped, good for new contributors |
| `priority:high` | Blocks users or causes data issues |
| `priority:low` | Nice to have, no urgency |
| `needs-triage` | Needs review before prioritization |
| `customer-reported` | Came from customer feedback |

## Process

1. **Check for duplicates** - search existing issues before creating
2. **Use the right template** - bug report or feature request
3. **Add labels** - at least one type label and one priority label
4. **Link related issues** - reference with `#issue-number` if related
5. **Assign** - only if the assignee is clear; otherwise leave unassigned

## Title format

- Bug: `[component] Short description of what's broken`
- Feature: `[component] Short description of desired behavior`
- Docs: `docs: Short description of what needs updating`

Examples:
- `[API] Query timeout on large datasets`
- `[Dashboard] Add date range filter to usage chart`
- `docs: Update authentication setup guide`

## Guardrails

- **No PII** - scrub customer names, emails, and company names from all issue content
- **One issue per problem** - no omnibus issues covering multiple bugs
- **No Impact section** - keep body to Problem + Expected behavior only
- **No confidential data** - no API keys, credentials, or internal URLs in issues
- **Don't close issues** - only the CAO or the assignee closes issues

## Self-improvement

After the CAO reviews created issues:

1. If the CAO edits an issue title, body, or labels before posting, note the pattern
2. If her edits reveal a preference for how problems are framed, bug reports are structured, or priorities are assigned, update the Templates or Labels sections
3. Update `product/_insights.md` with patterns: which issue formats get the fastest triage, which label conventions the team actually uses
4. If an issue template works particularly well, save it to `product/_examples/` as a reference
