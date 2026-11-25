---
name: knowledge-management
description: >
  Design IT knowledge management — article templates, review workflows,
  KCS practices, metrics, and retirement policies.
  TRIGGER when: user says /knowledge-management, needs to improve IT knowledge
  sharing, or asks about KCS or knowledge base practices.
argument-hint: "[IT knowledge domain or team]"
user-invocable: true
---

# IT Knowledge Management

## Process
### Step 1: Assess Current State
| Dimension | Questions |
|-----------|----------|
| Content volume | How many articles exist? |
| Quality | What % are current and accurate? |
| Usage | How often are articles accessed? |
| Coverage | What % of incidents have KB matches? |
| Process | Who creates/reviews/retires content? |

### Step 2: Implement KCS (Knowledge-Centered Service)
| KCS Practice | Implementation |
|-------------|---------------|
| Capture | Create/update articles as part of incident resolution |
| Structure | Consistent templates with problem-cause-resolution |
| Reuse | Search before creating, link articles to tickets |
| Improve | Flag inaccurate content, track usage metrics |

### Step 3: Design Article Templates
**Incident resolution template:**
```markdown
# [Problem Title]
## Symptoms: [What the user sees]
## Environment: [Affected systems/versions]
## Cause: [Root cause]
## Resolution: [Step-by-step fix]
## Workaround: [Temporary solution if applicable]
## Related: [Links to related articles]
```

### Step 4: Define Review Workflow
| Stage | Owner | Action |
|-------|-------|--------|
| Draft | Resolver | Created during incident |
| Review | SME | Technical accuracy check |
| Published | KB Manager | Approved for self-service |
| Retired | KB Manager | Archived when obsolete |

### Step 5: Track Metrics
| Metric | Target |
|--------|--------|
| Articles linked to incidents | > 60% |
| Self-service resolution rate | > 40% |
| Article accuracy rating | > 90% |
| Average article age | < 12 months |
| Zero-match incident rate | < 20% |

## Output Format
```markdown
## KM Plan: [Scope]
### Current State: [metrics]
### KCS Implementation: [phased plan]
### Templates: [article types]
### Metrics: [targets]
```

## Quality Checklist
- [ ] KCS practices aligned with incident workflow
- [ ] Article templates are standardized
- [ ] Review process has clear ownership
- [ ] Metrics track usage and quality
- [ ] Retirement policy prevents stale content

## Edge Cases
- For new KB, seed with top-50 most common incident resolutions
- If KCS adoption is low, start with one team as a pilot
- For vendor-specific knowledge, link to vendor docs rather than duplicating
