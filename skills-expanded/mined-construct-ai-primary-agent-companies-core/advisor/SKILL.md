---
name: advisor
description: >
  Use when: mapping new features or requirements across 50+ engineering/construction disciplines, assessing discipline-specific workflow impacts, identifying gaps in discipline coverage, or aligning features with discipline standards.
  Don't use when: implementing technical code changes (use architect), testing features (use validator), or resolving cross-discipline conflicts (use liaison).
allowed-tools:
  - Read
  - Grep
  - Write
  - Glob
  - Bash
metadata:
  paperclip:
    tags:
      - discipline-operations
      - strategy
      - workflow-mapping
---

# Discipline Strategy Skill

## Purpose

This skill maps new features to the appropriate discipline workflows across 50+ engineering and construction disciplines, ensuring that every feature correctly serves the relevant discipline needs.

## When to Use

- During feature planning and design phases
- When new discipline workflows are added
- As part of the requirements gathering process
- During sprint planning for discipline-specific work

## Steps

### 1. Feature Analysis

Analyze the new feature to understand:
- What problem does it solve?
- Which users will use it?
- What workflows does it support?
- What data does it process?

### 2. Discipline Mapping

Map the feature to relevant disciplines:

```bash
# Find discipline documentation
find ../docs-construct-ai/disciplines -name "*.md" -type f

# Search for relevant workflows
grep -r "workflow" ../docs-construct-ai/disciplines --include="*.md"
```

**Discipline Categories:**
- **Engineering**: Civil, Structural, Geotechnical, Electrical, Mechanical, Chemical
- **Construction**: Construction Management, Safety, Quality Control
- **Commercial**: Procurement, Finance, Contracts, Legal
- **Operations**: Logistics, Document Control, Project Controls
- **Governance**: Ethics, Environmental, HSE

### 3. Workflow Impact Analysis

For each mapped discipline:
- Identify which workflows are affected
- Assess the impact on existing processes
- Determine if new workflow steps are needed
- Check for cross-discipline dependencies

### 4. Standards Alignment

Verify alignment with discipline standards:
- Review discipline-specific requirements
- Check regulatory compliance needs
- Ensure industry best practices are followed
- Validate against discipline checklists

### 5. Gap Identification

Identify gaps where:
- Discipline needs are not addressed
- Workflows are incomplete
- Standards are not met
- Cross-discipline coordination is needed

## Output

```markdown
# Discipline Strategy: [Feature Name]

## Mapped Disciplines
| Discipline | Tag | Impact Level |
|------------|-----|--------------|
| [Discipline] | [tag] | High/Medium/Low |

## Affected Workflows
- [Discipline]: [Workflow name] — [Impact description]

## Standards Compliance
- [ ] [Standard 1]
- [ ] [Standard 2]

## Identified Gaps
1. [Gap description]
2. [Gap description]

## Recommendations
1. [Recommendation]
2. [Recommendation]
```

## Error Handling

- If discipline mapping is unclear, flag for manual review
- If cross-discipline conflicts detected, escalate to liaison skill
- If standards are unclear, consult discipline documentation

## Related Skills

- `liaison` — Handles multi-discipline conflicts
- `coordinator` — Ensures existing workflows aren't broken
- `analyst` — Applies sector-specific rules
- `validator` — Creates tests for discipline workflows