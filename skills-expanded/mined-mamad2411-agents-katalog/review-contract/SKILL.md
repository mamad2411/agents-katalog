---
name: review-contract
description: Review a contract against standard negotiation positions - flag deviations, generate redlines, provide business impact analysis. Use when reviewing vendor or customer agreements, when you need clause-by-clause analysis, or when preparing a negotiation strategy.
argument-hint: "<contract file or text>"
---

# /review-contract - Contract Review

## MCP connectors

None required. This skill operates on local repo files only.

Review a contract against standard positions. Analyze each clause, flag deviations, generate redline suggestions, and provide business impact analysis.

**Important**: This assists with legal workflows but does not provide legal advice. All analysis should be reviewed by qualified legal professionals before being relied upon.

## Invocation

```
/review-contract <contract file or URL>
```

## Workflow

### Step 1: Accept the Contract

Accept in any format: PDF, DOCX, pasted text, or file path.
If no contract is provided, prompt the user.

### Step 2: Gather Context

Ask:
1. **Which side are you on?** (vendor/supplier, customer/buyer, licensor, licensee, partner)
2. **Deadline**: When does this need to be finalized?
3. **Focus areas**: Any specific concerns?
4. **Deal context**: Deal size, strategic importance, existing relationship?

Proceed with partial context if needed, noting assumptions.

### Step 3: Load Standard Positions

Load standard contract positions from `legal/templates/enterprise-service-agreement.md`.

If no template exists, proceed with generic review using widely-accepted SaaS commercial standards as baseline. Note clearly.

### Step 4: Clause-by-Clause Analysis

1. Identify the contract type (SaaS, services, license, partnership, procurement)
2. Determine the user's side
3. Read the entire contract before flagging issues - clauses interact
4. Analyze each material clause against standard positions
5. Consider the contract holistically

Cover at minimum:

| Clause Category | Key Review Points |
|----------------|-------------------|
| **Limitation of Liability** | Cap amount, carveouts, mutual vs. unilateral, consequential damages |
| **Indemnification** | Scope, mutual vs. unilateral, cap, IP infringement, data breach |
| **IP Ownership** | Pre-existing IP, developed IP, open source, license grants |
| **Data Protection** | DPA, processing terms, self-hosted vs. cloud, sub-processors, breach notification |
| **Confidentiality** | Scope, term, carveouts, return/destruction |
| **Warranties** | Scope, disclaimers, survival period |
| **Term & Termination** | Duration, renewal, termination for convenience/cause, wind-down |
| **Governing Law** | Jurisdiction, venue, arbitration vs. litigation |
| **Payment Terms** | Net terms, late fees, taxes, price escalation |
| **SLA & Support** | Uptime, response times, support channels |

### Step 5: Flag Deviations

#### GREEN - Acceptable
Aligns with or better than standard position. No action needed.

#### YELLOW - Negotiate
Outside standard position but within negotiable range. Generate redlines.

#### RED - Escalate
Outside acceptable range, poses material risk. Requires escalation.

### Step 6: Generate Redlines

For each YELLOW and RED deviation:

```
**Clause**: [Section reference]
**Current language**: "[quote]"
**Proposed redline**: "[alternative language]"
**Rationale**: [1-2 sentences, suitable for external sharing]
**Priority**: [Must-have / Should-have / Nice-to-have]
**Fallback**: [Alternative position if rejected]
```

### Step 7: Business Impact Summary

- **Overall risk assessment**: High-level view
- **Top 3 issues**: Most important items to address
- **Negotiation strategy**: Which issues to lead with, what to concede
- **Timeline considerations**: Urgency factors

## Notes

- For non-English contracts, ask if the user wants translation or review in the original language
- For long contracts (50+ pages), focus on material sections first
- Always remind that analysis should be reviewed by qualified legal counsel

## Self-improvement

After the CAO (or legal counsel) reviews the contract analysis:

1. If they override a risk assessment (e.g. marked something RED that should have been YELLOW, or vice versa), update the risk calibration in this skill
2. If they flag a clause type or risk pattern not covered in the Clause-by-Clause table, add it
3. Update `legal/_insights.md` with the correction and the reasoning
4. If new standard positions emerge from negotiations (e.g. "we now accept mutual liability caps at 2x annual fees"), update `legal/templates/enterprise-service-agreement.md`
5. If a review format or negotiation strategy worked well, save it to `legal/_examples/` as a reference
