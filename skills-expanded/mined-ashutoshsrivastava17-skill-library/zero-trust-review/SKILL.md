---
name: zero-trust-review
description: >
  Review zero trust architecture — identity verification, device trust, network segmentation, least privilege, and continuous validation.
  TRIGGER when: user says /zero-trust-review or asks about zero trust implementation.
argument-hint: "[relevant context]"
user-invocable: true
---

# zero trust review

## Process

### Step 1: Define Scope
Identify the boundaries of what to assess, who is involved, and what assets/processes are in scope.

### Step 2: Identify Risks/Requirements
| Risk/Requirement | Category | Severity | Likelihood |
|-----------------|----------|----------|-----------|
| [item] | [category] | H/M/L | H/M/L |

### Step 3: Assess Current Controls
| Control | Effectiveness | Gap |
|---------|-------------|-----|
| [control] | Strong/Adequate/Weak | [description] |

### Step 4: Prioritize Actions
| Action | Impact | Effort | Priority |
|--------|--------|--------|----------|
| [action] | H/M/L | H/M/L | P1/P2/P3 |

### Step 5: Develop Mitigation Plan
| Risk | Mitigation | Owner | Timeline |
|------|-----------|-------|----------|
| [risk] | [strategy] | [name] | [date] |

### Step 6: Monitor and Report
| Metric | Target | Frequency |
|--------|--------|-----------|
| [KRI/metric] | [threshold] | Weekly/Monthly/Quarterly |

## Output Format
```markdown
## zero trust review: [Scope]
### Risk Summary: [Key findings]
### Controls: [Current state assessment]
### Recommendations: [Prioritized actions]
### Monitoring: [KRIs and reporting cadence]
```

## Quality Checklist
- [ ] Scope clearly defined
- [ ] Risks identified systematically
- [ ] Current controls assessed for effectiveness
- [ ] Recommendations prioritized by risk level
- [ ] Monitoring plan established
- [ ] Stakeholders reviewed findings

## Edge Cases
- For rapidly changing environments, increase assessment frequency
- If data is limited, use qualitative assessment with expert judgment
- For cross-organizational risks, coordinate with all affected parties
- Adjust methodology based on regulatory requirements
