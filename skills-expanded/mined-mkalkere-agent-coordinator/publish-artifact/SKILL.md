---
name: publish-artifact
version: 1.0.0
description: Publish work products to shared memory and notify via bus
uses:
  - core/bus
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - artifact:write
    - bus:write
  requires_approval: false
---

# Publish Artifact

Publish work products to shared memory so other agents can discover and use them. Artifacts are the primary way agents share durable results — reviews, analyses, reports, and decisions.

## Execution Model

This is a **builtin skill** (`handler: type: builtin`). When `publish_artifact` is invoked, the executor writes the artifact file to `.os/memory/{type}/{subject-slug}.md` with frontmatter, then publishes a notification to the bus. The tool schema in tool.yaml defines the external contract; the executor handles the file write and bus notification directly.

## When to Use

- After completing a code review — publish the review summary
- After finishing an analysis — publish findings for others to use
- After generating a report — make it discoverable
- When making an architectural decision — record it as a decision artifact
- Any time you produce a result that other agents should know about

## Methodology

### 1. Determine Artifact Type

| Type | Use For | Example |
|------|---------|---------|
| `review` | Code review results, PR feedback | Review of PR #23 with issues found |
| `analysis` | Investigation results, research | Root cause analysis of performance bug |
| `report` | Status reports, summaries | Sprint progress report |
| `summary` | Condensed information, digests | Summary of 3 related PRs |
| `decision` | Architectural decisions, ADRs | Decision to use PostgreSQL over MySQL |

### 2. Create the Artifact

Write the artifact with proper frontmatter:

```markdown
---
type: [artifact_type]
subject: [what it's about]
created_by: [your agent ID]
created_at: [ISO timestamp]
related_to: [optional list of related artifacts]
---

# [Title]

[Content in markdown]
```

### 3. Generate Subject Slug

Convert the subject to a filename-safe slug:
- Lowercase
- Replace spaces with hyphens
- Remove special characters except hyphens
- Examples: `PR #23` → `pr-23`, `Sprint Review 2026-02` → `sprint-review-2026-02`

### 4. Write and Notify

1. Write artifact to `.os/memory/{type}/{slug}.md`
2. Publish notification to the `work` bus channel
3. Verify the file was written and notification sent

## Output Format

```
## Artifact Published

- Type: [artifact type]
- Subject: [subject]
- Path: [file path]
- Notification: [channel and message ID]
- Size: [content size]
```

## Quality Criteria

- Artifact has complete frontmatter (type, subject, created_by, created_at)
- Content is well-structured markdown
- Subject slug follows naming conventions
- Bus notification is sent after writing
- Artifact is discoverable via discover-artifacts skill
- Content is self-contained (reader shouldn't need external context)

## Common Mistakes

- **Missing frontmatter**: Artifacts without frontmatter can't be parsed by discover-artifacts. Always include type, subject, created_by, and created_at.
- **Ambiguous subject**: Using generic subjects like "review" instead of "PR #23". Be specific so artifacts are findable.
- **Not notifying**: Writing the artifact file but forgetting to publish the bus notification. Other agents won't know it exists.
- **Wrong type**: Using `report` for a code review or `summary` for a decision. Use the right type so artifacts are categorized correctly.
- **Non-self-contained content**: Artifacts that reference "the thing we discussed" without specifying what. Include enough context for any reader.
- **Overwriting without versioning**: Publishing a new artifact with the same slug overwrites the previous one. If both versions matter, use different slugs or append dates.

## Completion

Artifact publishing is complete when:
- Artifact file is written with proper frontmatter and content
- File is in the correct type directory
- Bus notification is published to the `work` channel
- File can be discovered and read by other agents
