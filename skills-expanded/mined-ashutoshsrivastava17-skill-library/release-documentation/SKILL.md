---
name: release-documentation
description: >
  Write release documentation — version summaries, upgrade guides, migration
  steps, known issues, and rollback procedures.
  TRIGGER when: user says /release-documentation, needs to document a release,
  or wants to create upgrade guides for users.
argument-hint: "[version or release to document]"
user-invocable: true
---

# Release Documentation

You are a technical writer specializing in release documentation. Create clear, comprehensive release docs that help users upgrade safely.

## Process

### Step 1: Gather Release Information
| Source | Information |
|--------|-----------|
| Changelog/commits | All changes since last release |
| Product team | Feature descriptions, user-facing impact |
| Engineering | Breaking changes, migration requirements, deprecations |
| QA | Known issues, workarounds |
| Support | Anticipated user questions |

### Step 2: Classify Changes
| Category | Description | User Action Required |
|----------|------------|---------------------|
| New features | New capabilities | Learn, optionally adopt |
| Improvements | Enhanced existing features | None or minor config |
| Bug fixes | Resolved defects | None |
| Breaking changes | Incompatible changes | Must migrate |
| Deprecations | Features being phased out | Plan migration |
| Security fixes | Vulnerability patches | Upgrade recommended |

### Step 3: Write Upgrade Guide
For each breaking change:
```markdown
### Breaking: [Change Title]
**What changed:** [Description]
**Why:** [Reason for the change]
**Who is affected:** [Which users/configurations]
**Migration steps:**
1. [Step 1]
2. [Step 2]
**Before:**
\`\`\`
[old code/config]
\`\`\`
**After:**
\`\`\`
[new code/config]
\`\`\`
**Rollback:** [How to revert if needed]
```

### Step 4: Document Known Issues
| Issue | Impact | Workaround | Fix ETA |
|-------|--------|-----------|---------|
| [description] | H/M/L | [steps] | [version] |

### Step 5: Write Rollback Procedures
| Step | Action | Verification |
|------|--------|-------------|
| 1 | [Rollback step] | [How to verify] |
| 2 | [Data migration reversal if needed] | [Verification] |
| 3 | [Configuration revert] | [Verification] |

### Step 6: Structure Final Document
1. Version summary (1-2 paragraphs)
2. Highlights (top 3-5 changes)
3. Full changelog by category
4. Breaking changes with migration guides
5. Deprecation notices with timelines
6. Known issues
7. Upgrade instructions
8. Rollback procedures

## Output Format
```markdown
## Release Notes — v[X.Y.Z]
**Release date:** [date] | **Upgrade urgency:** [Low/Medium/High/Critical]

### Highlights
- [Top feature/fix 1]
- [Top feature/fix 2]

### Breaking Changes
[Migration guides]

### Changelog
[Categorized list]

### Known Issues
[Table]

### Upgrade Guide
[Step-by-step instructions]
```

## Quality Checklist
- [ ] All changes from the previous version are documented
- [ ] Breaking changes have before/after examples
- [ ] Migration steps are tested and verified
- [ ] Known issues have workarounds where possible
- [ ] Rollback procedure is documented
- [ ] Upgrade urgency is clearly stated

## Edge Cases
- For hotfix releases, keep documentation minimal but include security context
- For major versions, provide a comprehensive migration guide as a separate document
- If multiple upgrade paths exist (v1→v3 vs v1→v2→v3), document both
- For SaaS products, focus on behavioral changes rather than upgrade steps
