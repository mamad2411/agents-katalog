---
name: discover-artifacts
version: 1.0.0
description: Discover and read artifacts published by other agents
uses: []
requires:
  tools: []
  env: []
security:
  risk_level: read
  capabilities:
    - artifact:read
  requires_approval: false
---

# Discover Artifacts

Find and read work products published by other agents. Artifacts are the primary way agents share results — reviews, analyses, reports, and decisions.

## Execution Model

This is a **builtin skill** (`handler: type: builtin`). When `list_artifacts` is invoked, the executor scans artifact directories (`.os/memory/{type}/`) and returns metadata and paths. The tool schema in tool.yaml defines the external contract; the executor handles the directory listing and frontmatter parsing directly.

## When to Use

- Finding work products from other agents (reviews, analyses, reports)
- Checking if someone has already analyzed a topic
- Getting the latest review or report on a subject
- Reacting to new artifacts published on the bus
- Building on previous work rather than starting from scratch

## Methodology

### 1. Determine What You Need

Before searching, clarify:
- **Artifact type**: What kind of artifact? (review, analysis, report, summary, decision)
- **Subject**: What topic or entity? (e.g., PR #23, module X)
- **Recency**: Do you need the latest, or historical?

### 2. Search by Type

Artifacts are organized by type in directories:

| Type | Location | Contains |
|------|----------|----------|
| `review` | `.os/memory/review/` | Code review feedback, PR comments |
| `analysis` | `.os/memory/analysis/` | Investigation results, research findings |
| `report` | `.os/memory/report/` | Status reports, progress summaries |
| `summary` | `.os/memory/summary/` | Condensed information, digests |
| `decision` | `.os/memory/decision/` | Architectural decisions, ADRs |

### 3. Read Artifact Metadata

Each artifact has YAML frontmatter with:
- `type` — artifact type
- `subject` — what it's about
- `created_by` — which agent created it
- `created_at` — when it was created
- `related_to` — related artifacts (optional)

### 4. Use the Artifact

After reading, integrate the artifact into your work:
- Don't duplicate work that's already been done
- Reference the artifact in your own output
- Note if the artifact is stale (check `created_at`)

## Output Format

```
## Artifact Discovery

### Search
- Type filter: [type or all]
- Creator filter: [agent or all]
- Results found: [count]

### Artifacts
| # | Type | Subject | Creator | Created | Path |
|---|------|---------|---------|---------|------|
| 1 | [type] | [subject] | [agent] | [date] | [path] |

### Selected
- Path: [full path]
- Summary: [first few lines of content]
```

## Quality Criteria

- Search is scoped appropriately (not too broad, not too narrow)
- Artifact metadata is parsed correctly from frontmatter
- Results are sorted by relevance or recency
- Stale artifacts are identified (check creation date)
- Artifacts are read and used, not just discovered
- Previous work is referenced rather than duplicated

## Common Mistakes

- **Not checking for existing artifacts**: Starting work from scratch when someone already did the analysis. Always check for artifacts before beginning.
- **Ignoring artifact age**: Using a week-old review summary when the code has changed since. Check `created_at` and compare to recent commits.
- **Wrong directory**: Looking in `.os/memory/review/` for a decision record. Use the type taxonomy to find the right directory.
- **Duplicating work**: Redoing an analysis that another agent already completed and published. Discover first, then build on it.
- **Not parsing frontmatter**: Skipping the YAML frontmatter and missing important metadata (creator, date, related artifacts).

## Completion

Artifact discovery is complete when:
- The correct artifact type and scope are identified
- Available artifacts are found and listed
- Relevant artifacts are read and their content understood
- Artifact metadata (age, creator, relevance) is assessed
