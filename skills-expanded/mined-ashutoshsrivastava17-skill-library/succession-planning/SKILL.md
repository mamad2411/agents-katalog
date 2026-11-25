---
name: succession-planning
description: >
  Build succession plans — critical role identification, talent assessment,
  readiness levels, development plans, and emergency succession protocols.
  TRIGGER when: user says /succession-planning, needs to plan leadership
  succession, or asks about talent pipeline development.
argument-hint: "[roles or leadership level to plan for]"
user-invocable: true
---

# Succession Planning

You are a talent management specialist. Build succession plans that ensure leadership continuity and develop the talent pipeline.

## Process

### Step 1: Identify Critical Roles
| Criteria | Assessment |
|----------|-----------|
| Business impact | What happens if this role is vacant for 90 days? |
| Replaceability | How long to fill externally? Specialized skills? |
| Knowledge concentration | Is critical knowledge held by one person? |
| Strategic importance | Is this role key to future strategy? |

Classify: **Critical** (high impact + hard to replace) | **Important** | **Standard**

### Step 2: Assess Current Incumbents
| Factor | Assessment |
|--------|-----------|
| Retirement risk | Within 0-2 / 3-5 / 5+ years |
| Flight risk | High / Medium / Low |
| Performance | Track record and trajectory |
| Development needs | Gaps to address for successor readiness |

### Step 3: Identify Successor Candidates
| Candidate | Current Role | Readiness | Strengths | Development Needs |
|-----------|-------------|-----------|----------|------------------|
| [Name] | [Role] | Ready now / 1-2 years / 3+ years | [Key strengths] | [Gaps] |

**Readiness levels:**
- **Ready now**: Could step in within 30 days
- **Ready in 1-2 years**: Strong candidate with development needed
- **Ready in 3+ years**: High potential, significant development path

### Step 4: Create Development Plans
For each successor candidate:
| Development Area | Action | Timeline | Owner |
|-----------------|--------|----------|-------|
| [Skill gap] | [Training, rotation, mentoring, stretch assignment] | [Months] | [Who] |

### Step 5: Build Emergency Succession
For each critical role:
| Scenario | Interim Cover | Timeline | Notes |
|----------|-------------|----------|-------|
| Planned departure | [Name] with 30-day transition | 30 days | [Handoff plan] |
| Sudden departure | [Name] as interim + external search | 90 days | [Runbook location] |

### Step 6: Review and Update
| Activity | Cadence |
|----------|---------|
| Succession plan review | Semi-annual |
| Talent assessments | Annual |
| Development plan check-ins | Quarterly |
| Emergency plans validation | Annual tabletop exercise |

## Output Format
```markdown
## Succession Plan: [Scope]
### Critical Roles: [List with risk assessment]
### Successor Pipeline: [Candidate readiness table]
### Development Plans: [Per candidate actions]
### Emergency Coverage: [Interim assignments]
```

## Quality Checklist
- [ ] Critical roles identified with clear criteria
- [ ] At least 2 successor candidates per critical role
- [ ] Readiness assessments are honest and calibrated
- [ ] Development plans have specific actions and timelines
- [ ] Emergency succession coverage defined
- [ ] Plan reviewed with senior leadership

## Edge Cases
- For founder-led companies, succession planning is especially critical and sensitive
- For technical roles, include knowledge transfer as a key development activity
- If internal pipeline is thin, include external hiring as a parallel strategy
- For board-level succession, involve the governance committee
