---
name: legal-compliance
description: |
  Guide founders through startup legal foundations and compliance. Use when a founder says "Should I incorporate as C-corp or LLC?", "Where should I incorporate?", "Help me create founder agreement", "What vesting schedule?", "Help with employee equity", "Generate terms of service", "Help with SAFE/convertible notes", "Help with cap table", or asks about incorporation, founder agreements, ESOP setup, legal documents, fundraising instruments, or cap table management.
---

# Legal & Compliance Skill

Guide founders through the legal foundations every startup needs—incorporation, founder agreements, employee equity, legal documents, fundraising instruments, and cap table management.

## Important Disclaimers

Always include when providing legal guidance:
- This is educational information, not legal advice
- Recommend consulting a qualified attorney for specific situations
- Laws vary by jurisdiction and change over time
- Complex situations require professional legal counsel

## Core Workflow

### 1. Assess Stage and Needs

Determine where the founder is:

| Stage | Primary Needs |
|-------|---------------|
| Pre-incorporation | Entity selection, jurisdiction, founder agreement |
| Just incorporated | ESOP setup, IP assignment, initial docs |
| Raising pre-seed/seed | SAFEs, convertible notes, cap table |
| Raising Series A+ | Cap table cleanup, governance, compliance |

### 2. Route to Appropriate Guidance

Based on the question, load the relevant reference:

- **Incorporation questions** → `references/incorporation-guide.md`
- **Founder agreement/vesting** → `references/founder-agreements.md`
- **Employee equity/ESOP** → `references/employee-equity.md`
- **Terms of service/privacy** → `references/legal-documents.md`
- **SAFEs/convertible notes** → `references/fundraising-instruments.md`
- **Cap table modeling** → `references/cap-table-guide.md`

## Decision Trees

### Entity Selection

```
Planning to raise VC?
├─ Yes → Delaware C-Corp
└─ No → Will you have outside investors?
         ├─ Yes → Delaware C-Corp (likely)
         └─ No → Consider LLC for tax flexibility
                 └─ But: Converting LLC→C-Corp later is expensive
```

### Founder Vesting

```
Multiple founders?
├─ Yes → 4-year vesting, 1-year cliff for ALL founders
│        └─ Credit prior work? Start vesting date earlier
└─ Solo founder → Still consider vesting (for future co-founders/investors)
```

### Equity Grant Sizing

```
Determine: Stage × Role × Seniority

Example: Series A hire, Senior Engineer
→ Load references/employee-equity.md
→ Find: 0.1-0.25% typical range
→ Adjust for: market conditions, candidate negotiation, competing offers
```

## Key Frameworks

### Incorporation Checklist
1. Choose entity (C-Corp for VC-track)
2. Choose jurisdiction (Delaware standard)
3. File incorporation documents
4. Adopt bylaws and initial resolutions
5. Issue founder shares with vesting
6. File 83(b) elections (within 30 days!)
7. Execute IP assignment agreements
8. Obtain EIN

### ESOP Pool Sizing
| Stage | Typical Pool |
|-------|-------------|
| Pre-seed | 10-15% |
| Seed | 10-12.5% |
| Series A | 10-12.5% |
| Series B+ | 10-15% |

### Standard Vesting Terms
- 4-year total vesting period
- 1-year cliff (25% vests at month 12)
- Monthly vesting thereafter
- Double-trigger acceleration on M&A

## Assets

### Cap Table Template
Location: `assets/cap-table-template.xlsx`

5-sheet workbook containing:
- **Current Cap Table**: Ownership summary
- **Option Grant Ledger**: Track all employee grants
- **Convertible Securities**: SAFEs and notes tracker
- **Pro Forma Cap Table**: Model funding scenarios
- **Instructions**: How to use each sheet

When founders ask about cap tables:
1. Explain the concepts from `references/cap-table-guide.md`
2. Offer the template for their use
3. Help them understand how to model scenarios

## Integration Points

### With Fundraising Skill
- SAFE/note terms affect cap table
- Pro forma modeling for pitch
- Investor-standard documents

### With Business Model Skill
- Compensation philosophy
- Equity vs cash tradeoffs
- Total comp benchmarking

## Common Questions

### "Should I use a SAFE or convertible note?"
→ Load `references/fundraising-instruments.md`
→ SAFEs: simpler, no interest, no maturity (YC standard)
→ Notes: debt structure, some investors prefer
→ Recommend: Post-money SAFE for most situations

### "How much equity should I give my first engineer?"
→ Load `references/employee-equity.md`
→ Seed stage engineer: 0.1-0.5% depending on seniority
→ Consider: full-time vs part-time, prior experience, market rate cash

### "Do I need a privacy policy?"
→ Load `references/legal-documents.md`
→ Yes, if collecting any user data
→ Required for: app stores, payment processing, EU users
→ Recommend: use generator as starting point, lawyer review for complex cases

### "What's a fair founder split?"
→ Load `references/founder-agreements.md`
→ Consider: contribution so far, going-forward commitment, skills/experience
→ Key principle: vesting matters more than initial split
→ Always: document the reasoning

## Output Formats

### For Guidance Questions
Provide clear, actionable advice with:
- Direct recommendation
- Key considerations
- When to consult a lawyer
- Relevant resources

### For Template Requests
1. Explain what the document should contain
2. Provide template or point to standard sources (YC, Clerky)
3. Emphasize need for legal review
4. Never provide as "final" legal document

### For Calculations
Use cap table template or provide formulas:
- Ownership percentages
- Dilution scenarios
- SAFE/note conversion math
- Option pool sizing

## Reference Quick-Lookup

| Topic | File | Key Sections |
|-------|------|--------------|
| C-Corp vs LLC | incorporation-guide.md | Entity Selection |
| Delaware pros/cons | incorporation-guide.md | Jurisdiction Selection |
| Founder vesting | founder-agreements.md | Vesting Schedules |
| Equity split | founder-agreements.md | Equity Split |
| Grant sizing by role | employee-equity.md | Grant Sizing tables |
| Strike price/409A | employee-equity.md | Strike Price section |
| SAFE vs note | fundraising-instruments.md | Comparison table |
| Conversion math | fundraising-instruments.md | Conversion Mechanics |
| ToS essentials | legal-documents.md | Essential Sections |
| Privacy requirements | legal-documents.md | Legal Requirements |
| Cap table modeling | cap-table-guide.md | Pro Forma Modeling |

## Resources to Recommend

**Incorporation:**
- [Stripe Atlas](https://stripe.com/atlas)
- [Clerky](https://clerky.com)

**Legal Documents:**
- [YC Standard Documents](https://www.ycombinator.com/documents)
- [Cooley GO](https://www.cooleygo.com/documents/)

**Equity:**
- [Carta Equity Education](https://carta.com/equity-education/)
- [Index Ventures Option Plan](https://www.indexventures.com/optionplan)

**Cap Table:**
- [Carta](https://carta.com)
- [Pulley](https://pulley.com)

---

*Adapted from [Linas Beliūnas's](https://linas.substack.com/p/onepersonunicorn) **The One-Person Unicorn** founder skill set.*
