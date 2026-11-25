---
name: saas-agreement
description: "Drafts SaaS subscription agreements with service levels, data ownership, and termination provisions. Use when creating terms for a software-as-a-service product."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# SaaS Agreement

## When to Use This Skill

Use this skill when you need to:
- Draft a SaaS subscription agreement for your software product
- Define service levels, uptime commitments, and support terms
- Establish data ownership, security, and privacy provisions
- Create subscription, renewal, and termination terms

**DO NOT** use this skill for terms of service (general website), mobile app terms (use terms-of-use-app), or marketplace agreements. This is for SaaS-specific subscription agreements. Have an attorney review before use.

---

## Core Principle

A SAAS AGREEMENT MUST BALANCE PROTECTING YOUR BUSINESS WITH BUILDING CUSTOMER TRUST — UNFAIR TERMS LOSE CUSTOMERS, MISSING TERMS EXPOSE YOU TO LIABILITY.

---

## Phase 1: Product and Service Details

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Product name** | "What is your SaaS product called?" | No default — must be provided |
| **Product description** | "What does it do in 1-2 sentences?" | No default — must be provided |
| **Pricing model** | "How do you charge? (monthly, annual, per-seat, usage-based)" | Monthly subscription |
| **Free trial** | "Do you offer a free trial?" | Yes — 14 days |
| **Target customer** | "B2B or B2C? SMB or enterprise?" | B2B SMB |
| **Data handling** | "What customer data does your product process?" | Business data, no personal health/financial data |
| **Uptime commitment** | "What uptime SLA do you commit to?" | 99.9% |

**GATE: Do not proceed without product name, pricing model, and data handling details.**

---

## Phase 2: Agreement Structure

```
## [Product Name] SaaS Subscription Agreement

**Last Updated:** [Date]

### 1. Definitions

- "Service" means the [Product Name] software application and related
  services provided by [Company Name].
- "Customer" means the entity or individual subscribing to the Service.
- "Customer Data" means all data uploaded, stored, or processed by
  Customer through the Service.
- "Subscription Term" means the period of the Customer's paid subscription.
- "Users" means individuals authorized by Customer to access the Service.

### 2. Access and Use

**2.1 License Grant.** Subject to this Agreement, [Company] grants
Customer a non-exclusive, non-transferable right to access and use
the Service during the Subscription Term.

**2.2 Usage Limits.** Customer's use is limited to [number of users /
usage volume / features] specified in the applicable subscription plan.

**2.3 Acceptable Use.** Customer shall not:
- Reverse engineer, decompile, or attempt to extract source code
- Use the Service for illegal purposes
- Interfere with Service operations or security
- Resell, sublicense, or provide access to unauthorized third parties
- Upload malicious code or attempt to gain unauthorized access
- Exceed documented API rate limits

### 3. Subscription and Billing

**3.1 Subscription Plans.**
| Plan | Price | Includes |
|------|-------|----------|
| [Starter] | $[X]/month | [Features/limits] |
| [Pro] | $[X]/month | [Features/limits] |
| [Enterprise] | Custom | [Features/limits] |

**3.2 Billing.** Fees are billed [monthly / annually] in advance.
All fees are non-refundable except as stated in this Agreement.

**3.3 Payment.** Payment is due upon invoice. Late payments incur
[1.5%] monthly interest. [Company] may suspend access for accounts
[30+] days past due.

**3.4 Price Changes.** [Company] may adjust pricing with [30] days
notice before the next renewal period.

### 4. Free Trial

[If applicable:]
The free trial lasts [14] days. No payment information is required.
At the end of the trial, Customer must subscribe to continue access.
Trial data [will / will not] be preserved if Customer subscribes
within [7] days of trial expiration.

### 5. Service Level Agreement

**5.1 Uptime Commitment.** [Company] commits to [99.9%] monthly
uptime, excluding scheduled maintenance and force majeure events.

**5.2 Scheduled Maintenance.** [Company] will provide [48] hours
notice for planned maintenance and schedule during off-peak hours.

**5.3 Service Credits.** If uptime falls below the commitment:
| Monthly Uptime | Service Credit |
|---------------|---------------|
| 99.0% - 99.9% | 10% of monthly fee |
| 95.0% - 99.0% | 25% of monthly fee |
| Below 95.0% | 50% of monthly fee |

Service credits must be requested within [30] days and are applied
to future invoices, not refunded.

### 6. Customer Data

**6.1 Ownership.** Customer retains all rights to Customer Data.
[Company] acquires no ownership rights in Customer Data.

**6.2 Use of Data.** [Company] may access Customer Data only to
provide the Service, troubleshoot issues, or as directed by Customer.

**6.3 Data Security.** [Company] implements industry-standard
security measures including encryption at rest and in transit,
access controls, and regular security assessments.

**6.4 Data Portability.** Customer may export their data at any
time through [export feature / API / support request]. Upon
termination, [Company] will make data available for export for
[30] days.

**6.5 Data Deletion.** Following the data export period after
termination, [Company] will delete Customer Data within [30] days.

### 7. Intellectual Property

The Service, including all software, documentation, and improvements,
remains the exclusive property of [Company]. Customer's feedback or
suggestions may be used by [Company] without obligation.

### 8. Confidentiality

Each party agrees to protect the other's confidential information
with at least the same degree of care used for its own confidential
information, and in no event less than reasonable care.

### 9. Warranties and Disclaimers

**9.1** [Company] warrants the Service will materially conform to
its documentation during the Subscription Term.

**9.2** EXCEPT AS STATED ABOVE, THE SERVICE IS PROVIDED "AS IS."
[COMPANY] DISCLAIMS ALL OTHER WARRANTIES, EXPRESS OR IMPLIED,
INCLUDING MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

### 10. Limitation of Liability

[COMPANY]'S TOTAL LIABILITY SHALL NOT EXCEED THE FEES PAID BY
CUSTOMER IN THE [12] MONTHS PRECEDING THE CLAIM. NEITHER PARTY
IS LIABLE FOR INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES.

### 11. Term and Termination

**11.1 Term.** The Subscription Term is [monthly / annual] and
automatically renews unless either party provides [30] days notice
before renewal.

**11.2 Termination for Cause.** Either party may terminate if the
other materially breaches and fails to cure within [30] days of notice.

**11.3 Effect of Termination.** Upon termination, Customer's access
ceases. Data export rights per Section 6.4 apply.

### 12. Governing Law and Disputes

This Agreement is governed by the laws of [State]. Disputes shall
be resolved through [binding arbitration / litigation] in [jurisdiction].
```

---

## Phase 3: Review and Customize

- Adjust SLA terms based on actual infrastructure capabilities
- Customize data handling for industry compliance (HIPAA, SOC 2, etc.)
- Add DPA reference if serving EU customers
- Include acceptable use specifics for your product type

---

## Phase 4: Delivery

```
## SaaS Agreement Checklist

- [ ] Service description accurately reflects the product
- [ ] Pricing and billing terms match current plans
- [ ] SLA commitments are achievable with current infrastructure
- [ ] Data ownership clearly belongs to the customer
- [ ] Data export and deletion procedures are implementable
- [ ] Limitation of liability is reasonable and enforceable
- [ ] Auto-renewal and cancellation terms are clear
- [ ] Agreement reviewed by legal counsel
- [ ] Published on website and linked from signup flow
```

---

## Example: Project Management SaaS

**Plans:** Starter $29/mo (5 users), Pro $79/mo (25 users), Enterprise custom. **SLA:** 99.9% uptime. **Data:** Customer retains ownership, encrypted at rest (AES-256) and in transit (TLS 1.2+), 30-day export period after cancellation. **Trial:** 14 days, no credit card required.

---

## Anti-Patterns

- **Claiming ownership of customer data** — this destroys trust and may violate regulations. Customer always owns their data.
- **No data export provision** — data lock-in is a competitive tactic that breeds resentment. Provide clean export options.
- **Unrealistic SLA** — do not promise 99.99% uptime if your infrastructure cannot deliver it. Set achievable targets.
- **No termination clause** — customers need a clear way out. Make cancellation easy and transparent.
- **Auto-renewal without notice** — always notify before renewal, especially for annual plans.

---

## Recovery

- **Customer disputes data ownership:** Your agreement should explicitly state customer data ownership. If it does not, amend it immediately.
- **SLA breach:** Apply service credits proactively. Communicate the incident, root cause, and prevention measures.
- **Need to change terms:** Provide advance notice (30+ days), allow customers to cancel if they disagree, and grandfather existing customers when possible.
- **Enterprise customer requires custom terms:** Be prepared to negotiate specific clauses. Common requests: higher liability caps, custom SLA, specific security provisions.
