---
name: skill-stocktake
description: Use when auditing skills for quality. Reviews all skills against a quality checklist and provides Keep/Improve/Retire verdicts.
---

# Skill Stocktake

Audits all Gemini agent skills for quality, relevance, and currency.

## When to Activate

- Periodically reviewing skill quality (monthly recommended)
- After adding multiple new skills
- When skills seem outdated or overlapping
- Before a major project milestone

## Scope

Skills to audit:

| Path | Description |
|------|-------------|
| `system/agents/gemini/skills/` | All Gemini agent skills |

## Stocktake Workflow

### Phase 1 — Inventory

List all skills with their descriptions and last modified dates:

```bash
find system/agents/gemini/skills -name "SKILL.md" -exec sh -c '
  dir=$(dirname "{}")
  name=$(basename "$dir")
  mtime=$(stat -f "%Sm" -t "%Y-%m-%d" "{}" 2>/dev/null || stat -c "%y" "{}" 2>/dev/null | cut -d" " -f1)
  desc=$(head -5 "{}" | grep "description:" | sed "s/description: //")
  printf "| %-25s | %-12s | %s\n" "$name" "$mtime" "$desc"
' \;
```

### Phase 2 — Quality Evaluation

Evaluate each skill against this checklist:

```
- [ ] Content overlap with other skills checked
- [ ] Freshness of technical references verified
- [ ] Actionability: has code examples and concrete steps
- [ ] Scope fit: name, trigger, and content are aligned
```

### Verdict Criteria

| Verdict | Meaning |
|---------|---------|
| **Keep** | Useful, current, and unique |
| **Improve** | Worth keeping, but specific changes needed |
| **Update** | Referenced technology is outdated |
| **Retire** | Low quality, stale, or redundant |
| **Merge into [X]** | Substantial overlap with another skill |

### Evaluation Dimensions (Holistic AI Judgment)

- **Actionability**: Code examples, commands, or steps for immediate use
- **Scope fit**: Name, trigger, and content are aligned; not too broad or narrow
- **Uniqueness**: Value not replaceable by another skill or project rules
- **Currency**: Technical references are current and correct

### Reason Quality Requirements

The reason for each verdict must be self-contained and decision-enabling:

- **Retire**: State (1) what defect was found, (2) what covers the same need
  - Bad: `"Superseded"`
  - Good: `"Content fully covered by gin-patterns skill which has better examples and GORM integration. No unique content."`
- **Merge**: Name the target and describe what content to integrate
  - Bad: `"Overlaps with X"`
  - Good: `"40 lines of generic content; the 'validation patterns' section should be moved to security-review skill as a subsection."`
- **Improve**: Describe the specific change needed
  - Bad: `"Too long"`
  - Good: `"300 lines; Section 'Framework Comparison' duplicates coding-standards; delete it to reach ~180 lines."`
- **Keep**: Restate why it's valuable
  - Bad: `"Fine"`
  - Good: `"Comprehensive Go testing patterns with table-driven tests and GORM mocking; no overlap with other skills."`

### Phase 3 — Summary Table

| Skill | Verdict | Reason |
|-------|---------|--------|
| golang-patterns | Keep | Comprehensive Go idioms with concurrency and functional options patterns |
| ... | ... | ... |

### Phase 4 — Consolidation

1. **Retire/Merge**: Present justification, get user confirmation before acting
2. **Improve**: Present specific suggestions with rationale
3. **Update**: Present updated content with sources checked

## Best Practices

- Run stocktake quarterly or after adding 5+ skills
- Focus on overlap detection — skills should be orthogonal
- Check that examples still compile/work
- Ensure 80% of lines contain actionable content (not filler)

---

**Remember**: Skills should be lean, actionable, and non-overlapping. Quality over quantity.
