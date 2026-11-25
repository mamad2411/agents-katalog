---
name: employment-offer-drafting
description: Draft an offer letter with comp details and terms. Use when a candidate is ready for an offer, assembling a total comp package (base, equity, signing bonus), writing the offer letter text itself, or prepping negotiation guidance for the hiring manager.
argument-hint: <role and level>
license: Apache-2.0
metadata:
  author: Anthropic
  source: anthropics/knowledge-work-plugins/human-resources/skills/draft-offer
  source_url: https://github.com/anthropics/knowledge-work-plugins/blob/8f8779a1681ea2f8dc697a6b3063d5e3e7f7460c/human-resources/skills/draft-offer/SKILL.md
  upstream-commit: 8f8779a1681ea2f8dc697a6b3063d5e3e7f7460c
  original-name: draft-offer
  packaged-by: AutoGPT
  packaged-on: '2026-09-25'
---

> Packaging adaptation by AutoGPT, 2026-09-25. Original authorship and licence are retained. Changes are limited to the recorded name, metadata and local references; see ATTRIBUTION.md in this package.


# /draft-offer

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](references/CONNECTORS.md).

Draft a complete offer letter for a new hire.

## Usage

```
/draft-offer $ARGUMENTS
```

## What I Need From You

- **Role and title**: What position?
- **Level**: Junior, Mid, Senior, Staff, etc.
- **Location**: Where will they be based? (affects comp and benefits)
- **Compensation**: Base salary, equity, signing bonus (if applicable)
- **Start date**: When should they start?
- **Hiring manager**: Who will they report to?

If you don't have all details, I'll help you think through them.

## Output

```markdown
## Offer Letter Draft: [Role] — [Level]

### Compensation Package
| Component | Details |
|-----------|---------|
| **Base Salary** | $[X]/year |
| **Equity** | [X shares/units], [vesting schedule] |
| **Signing Bonus** | $[X] (if applicable) |
| **Target Bonus** | [X]% of base (if applicable) |
| **Total First-Year Comp** | $[X] |

### Terms
- **Start Date**: [Date]
- **Reports To**: [Manager]
- **Location**: [Office / Remote / Hybrid]
- **Employment Type**: [Full-time, Exempt]

### Benefits Summary
[Key benefits highlights relevant to the candidate]

### Offer Letter Text

Dear [Candidate Name],

We are pleased to offer you the position of [Title] at [Company]...

[Complete offer letter text]

### Notes for Hiring Manager
- [Negotiation guidance if needed]
- [Comp band context]
- [Any flags or considerations]
```

## If Connectors Available

If **~~HRIS** is connected:
- Pull comp band data for the level/role
- Verify headcount approval
- Auto-populate benefits details

If **~~ATS** is connected:
- Pull candidate details from the application
- Update offer status in the pipeline

## Tips

1. **Include total comp** — Candidates compare total compensation, not just base.
2. **Be specific about equity** — Share count, current valuation method, vesting schedule.
3. **Personalize** — Reference something from the interview process to make it warm.
