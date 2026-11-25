---
name: health
description: Comprehensive health check of the knowledge base — coverage, freshness, consistency, structure
---

# Health — Knowledge Base Health Check

Perform a comprehensive health check of the entire knowledge base.

## Checks

### 1. Coverage
- List all knowledge files and their `status` (skeleton / draft / active / stale / archived)
- Calculate: X of Y files are active
- Identify areas with only skeleton files or no content
- Flag knowledge areas critical for the partner's situation that are underdeveloped

### 2. Freshness
- Check `last_updated` dates on all files
- Flag anything not updated in 30+ days as potentially stale
- Flag files with `status: draft` older than 14 days
- Assess whether stale content is still likely accurate based on other files

### 3. Consistency
- Dispatch the **Librarian** sub-agent for thorough contradiction detection
- Verify `knowledge/decisions/` entries are consistent with current state
- Check that `ops/action-items.md` doesn't reference completed or abandoned work
- Verify `[[wiki links]]` resolve to existing files

### 4. Completeness
- For each knowledge area, assess depth relative to what the partner's situation needs
- Flag critical gaps (e.g., for a startup: no financial projections while fundraising; for a researcher: no source notes while writing a paper; for a creative project: no character work while drafting)

### 5. Structure
- Verify all files have valid YAML frontmatter with required fields
- Check naming conventions are followed
- Scan for potential sensitive data that shouldn't be in committed files
- Verify every knowledge subfolder has a `README.md` with a `## Current Contents` section that matches reality (dispatch the **Librarian** for the detailed sync check)

### 6. Inbox Health
- Count files in `ops/inbox/` (excluding `README.md` and any `processed/` subfolder)
- Check the age of the oldest unprocessed item
- Apply these thresholds:
  - **Healthy**: fewer than 10 items AND oldest is less than 14 days old
  - **Warning**: 10-25 items OR oldest is 14-30 days old → recommend running `/process-inbox` soon
  - **Critical**: more than 25 items OR oldest is over 30 days old → the inbox is becoming a graveyard, process now
- Also check `sources/` for files that have **never been ingested** (no entries in `ops/changelog.md` referencing them) — flag these as "captured but not digested"

## Output

```
# Health Report — [Date]

## Overall Health: [Excellent / Good / Needs Attention / Critical]

## Coverage: X/Y files active and current

## Issues

### Critical (act now)
[Issues that could cause problems if not addressed]

### Warning (act soon)
[Issues that are degrading knowledge quality]

### Info (nice to fix)
[Minor structural or completeness issues]

## Recommendations
[Prioritized list of what to fix, grouped by effort level]
```

## After Health Check

- Save report to `ops/reviews/YYYY-MM-DD-health-report.md`
- Offer to fix issues that can be addressed immediately
- Add remaining fixes to `ops/action-items.md` with appropriate priority
