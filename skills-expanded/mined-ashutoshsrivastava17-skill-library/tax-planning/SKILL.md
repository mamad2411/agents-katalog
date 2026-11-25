---
name: tax-planning
description: >
  Plan tax strategy — entity structure, deductions, credits, jurisdiction
  analysis, compliance calendar, and estimated liability.
  TRIGGER when: user says /tax-planning, needs tax planning guidance,
  or asks about tax optimization strategies.
argument-hint: "[entity or tax situation to plan for]"
user-invocable: true
---

# Tax Planning

> **Disclaimer:** This is not tax advice. Consult a qualified tax professional.

## Process

### Step 1: Assess Current Tax Position
| Element | Details |
|---------|---------|
| Entity type | Sole proprietor, LLC, S-Corp, C-Corp, Partnership |
| Jurisdictions | Federal, state(s), international |
| Revenue | Annual revenue and growth trajectory |
| Effective rate | Actual tax paid / taxable income |

### Step 2: Identify Optimization Opportunities
| Strategy | Applicability | Estimated Impact |
|----------|-------------|-----------------|
| Entity restructuring | Growth stage changes | Variable |
| R&D tax credits | Development activity | 6-8% of qualifying expenses |
| Depreciation acceleration | Capital-intensive | Timing benefit |
| Retirement contributions | All entities | Deduction up to limits |
| State tax planning | Multi-state | Rate differential savings |

### Step 3: Build Compliance Calendar
| Date | Filing | Jurisdiction |
|------|--------|-------------|
| Jan 15 | Q4 estimated payment | Federal |
| Mar 15 | Partnership/S-Corp returns | Federal |
| Apr 15 | Individual/C-Corp, Q1 estimated | Federal |
| Jun 15 | Q2 estimated | Federal |
| Sep 15 | Q3 estimated | Federal |

### Step 4: Estimate Liability
| Component | Current Year | Next Year |
|-----------|-------------|-----------|
| Revenue | $X | $X |
| Deductions | $X | $X |
| Taxable income | $X | $X |
| Estimated liability | $X | $X |

## Output Format
```markdown
## Tax Plan: [Entity]
### Current Position: [rate, key facts]
### Opportunities: [prioritized strategies]
### Calendar: [key dates]
### Estimated Impact: [projected savings]
```

## Quality Checklist
- [ ] Current position accurately assessed
- [ ] Opportunities aligned with business structure
- [ ] Compliance calendar includes all jurisdictions
- [ ] Professional review recommended for implementation

## Edge Cases
- For international operations, consider transfer pricing and tax treaties
- For startups, focus on R&D credits and NOL carryforward
- For crypto assets, track cost basis meticulously
