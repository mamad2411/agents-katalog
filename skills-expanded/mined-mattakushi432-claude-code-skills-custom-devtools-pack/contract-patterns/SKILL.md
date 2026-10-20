---
name: contract-patterns
description: "When to activate: MSA, SOW, NDA, contract negotiation, redlines, contract lifecycle management, approval workflows, key contract clauses, legal review process"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: business-ops
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Contract Patterns

## Contract Types Reference

| Contract | Purpose | Who signs |
|----------|---------|-----------|
| NDA (Mutual) | Protects confidential information during evaluation | Both parties before sharing sensitive info |
| MSA (Master Services Agreement) | Governs entire commercial relationship | Both parties once, referenced by all SOWs |
| SOW (Statement of Work) | Defines specific project scope, deliverables, timeline | Both parties per project / engagement |
| Order Form | Captures commercial terms for a specific purchase | Both parties per transaction |
| DPA (Data Processing Agreement) | GDPR/CCPA compliance for data handling | Both parties when processing personal data |
| SLA (Service Level Agreement) | Defines service standards and remedies | Often an exhibit to MSA |
| BAA (Business Associate Agreement) | HIPAA compliance for health data | Both parties when handling PHI |

---

## MSA Key Clauses

### Intellectual Property
```
Preferred (vendor-friendly):
  All IP developed by Vendor remains with Vendor.
  Customer receives a license to use deliverables.
  
Alternative (customer-friendly):
  All work product developed specifically for Customer under this 
  agreement is work-for-hire and owned by Customer.

Negotiation note:
  For SaaS: Vendor always retains platform IP.
  For custom development: negotiate based on leverage.
```

### Liability Cap
```
Standard cap: "Aggregate liability shall not exceed the greater of 
(a) fees paid in the 12 months preceding the claim or (b) $[X]."

Watch out for:
  - Uncapped liability for: IP infringement, gross negligence, 
    willful misconduct, indemnification obligations, data breaches
  - "Uncapped" clauses can expose vendor to existential risk
  
Customer push: "Remove the cap for data breaches."
Vendor counter: "Cap applies to all claims including data breaches, 
  but we carry cyber insurance of $[X]M."
```

### Indemnification
```
Mutual indemnification covers:
  - Each party's IP infringement claims
  - Each party's gross negligence / willful misconduct
  - Vendor: indemnifies customer if third party claims product infringes their IP
  - Customer: indemnifies vendor for customer's data and content

Red flag: one-sided indemnification with unlimited scope.
```

### Termination
```
Termination for cause:
  Either party may terminate if material breach not cured within 30 days notice.

Termination for convenience:
  Customer: 30–90 days written notice (negotiate based on contract value)
  Vendor: typically not allowed to terminate for convenience in B2B SaaS

Effect of termination:
  - Customer data returned or deleted within 30 days
  - Fees paid not refunded for current period (pro-rated annual is negotiable)
  - Outstanding invoices payable
```

### Governing Law and Dispute Resolution
```
Vendor preference: Vendor's home state / country
Customer preference: Customer's home state / country
Compromise: neutral jurisdiction or "each party's home jurisdiction for claims against them"

Dispute resolution order:
  1. Executive escalation (30 days)
  2. Mediation (60 days)
  3. Arbitration (AAA / JAMS rules) or litigation
```

---

## SOW Structure

```
STATEMENT OF WORK
Reference: MSA dated [Date] between [Vendor] and [Customer]
SOW #: [NNN]
Effective date: [Date]

1. SERVICES
   [Specific description of what will be delivered]
   
   Inclusions: [Explicit list of what is in scope]
   Exclusions: [Explicit list of what is NOT in scope — prevents scope creep]

2. DELIVERABLES
   | Deliverable | Description | Acceptance criteria | Due date |
   |-------------|-------------|--------------------|----- ----|
   | [Name] | [What it is] | [How customer accepts] | [Date] |

3. TIMELINE
   | Milestone | Description | Date |
   |-----------|-------------|------|
   | Kickoff | Project kickoff meeting | [Date] |
   | [Phase 1] | [Deliverables] | [Date] |
   | Final delivery | All deliverables accepted | [Date] |

4. FEES AND PAYMENT
   Total fee: $[X]
   Payment schedule:
     [X]% upon signing: $[Y]
     [X]% upon [milestone]: $[Y]
     [X]% upon final acceptance: $[Y]
   
   Expenses: [reimbursable / included / capped at $X]
   Change orders: any scope change requires written change order signed by both parties

5. CUSTOMER OBLIGATIONS
   [List what customer must provide: access, data, stakeholder availability, review turnarounds]
   
   Customer delay clause: if customer delays by > [N] days, timeline adjusted accordingly

6. ACCEPTANCE PROCEDURE
   Customer has [N] business days to accept or reject each deliverable.
   If no response within [N] days, deliverable is deemed accepted.
   Rejected deliverables: vendor has [N] days to revise; customer has [N] days to re-review.

7. PROJECT CONTACTS
   Vendor: [Name, email, role]
   Customer: [Name, email, role]
```

---

## NDA Essentials

### Key Provisions
```
Definition of Confidential Information:
  - Include: technical, business, financial, customer, product information
  - Exclude: publicly available, independently developed, received from third party

Obligations:
  - Use only for evaluation/business purpose
  - Limit disclosure to employees with need to know
  - Same protection as own confidential information (not less than reasonable care)

Term:
  - Mutual NDA: 2–3 years standard
  - Confidentiality obligations often survive termination by 2–5 years

Exceptions:
  - Compelled disclosure by law (notify before disclosing if legally permitted)
  - Information recipient can independently prove was not derived from disclosing party
```

### Red Flags in Incoming NDAs
- One-sided (only protects discloser's information)
- No carve-outs for publicly available information
- Overly broad definition of confidential (includes "all information shared verbally")
- Perpetual term with no sunset
- Automatic assignment of IP developed using confidential information

---

## Redline Process

### Redline Workflow
1. Receive contract → send to legal (or contract manager) within 24h
2. Legal marks up in track changes with comments explaining each change
3. Internal approval of redline before sending (sales + legal sign-off)
4. Send redline with cover email explaining major positions
5. Counterparty returns counter-redline → repeat
6. Issues list: for complex deals, move to issues list to track open points
7. Signature: collect via DocuSign / e-signature tool

### Negotiation Tiers
| Clause | Position | Flexibility |
|--------|----------|------------|
| Liability cap | 12 months fees paid | May go to 24 months for high-value deals |
| IP ownership | Vendor retains all | Non-negotiable for platform IP |
| Data return | 30 days post-termination | May extend to 60 days |
| Governing law | Vendor's home state | May accept neutral jurisdiction |
| Payment terms | Net 30 | May accept Net 45 for enterprise |
| Auto-renewal | 60-day opt-out window | May reduce to 90 days |

---

## Contract Lifecycle Management

### CLM Stages
1. **Request**: contract need identified (new customer, vendor, partnership)
2. **Drafting**: use template; customize for specific deal
3. **Review**: legal review; stakeholder approval per authorization matrix
4. **Negotiation**: redline exchange; issues resolution
5. **Approval**: final version approved per signing authority matrix
6. **Execution**: electronic signature; countersignature
7. **Repository**: filed in CLM system with metadata
8. **Obligation tracking**: renewal dates, SLA reviews, reporting requirements
9. **Renewal / amendment**: proactive outreach 90 days before expiration

### Signing Authority Matrix
| Contract value | Signing authority |
|---------------|-----------------|
| < $10K / year | Department head |
| $10K–$50K / year | VP + Finance |
| $50K–$250K / year | CFO |
| > $250K / year | CEO |
| Any contract with IP assignment | General Counsel |
| Any contract with unlimited liability | General Counsel + CEO |

### Contract Repository Metadata (capture for every contract)
- Counterparty name and entity
- Contract type (MSA / SOW / NDA / Order Form)
- Effective date
- Expiration / renewal date
- Auto-renewal: yes/no; opt-out notice period
- Contract value (annual + total)
- Governing law
- Notice provision (how to send formal notices)
- Owner (internal relationship owner)
- Location (CLM system link)
