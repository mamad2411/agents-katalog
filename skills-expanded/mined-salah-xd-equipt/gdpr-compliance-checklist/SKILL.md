---
name: gdpr-compliance-checklist
description: "Creates GDPR compliance checklists with data mapping, consent mechanisms, and breach response procedures. Use when ensuring your business complies with GDPR requirements."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# GDPR Compliance Checklist

## When to Use This Skill

Use this skill when you need to:
- Assess GDPR compliance for a business that serves EU customers
- Create a data mapping inventory of personal data processing activities
- Establish consent mechanisms, data subject rights procedures, and breach response plans
- Build a compliance checklist to track your GDPR readiness

**DO NOT** use this skill as a substitute for legal counsel or a Data Protection Officer. This is a compliance planning tool. Consult a GDPR specialist for complex data processing scenarios.

---

## Core Principle

GDPR COMPLIANCE IS NOT A ONE-TIME PROJECT — IT IS AN ONGOING COMMITMENT TO TRANSPARENCY, DATA MINIMIZATION, AND RESPECT FOR INDIVIDUAL PRIVACY RIGHTS.

---

## Phase 1: Business Assessment

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business location** | "Where is your business based?" | No default — must be provided |
| **EU customers** | "Do you have customers or website visitors from the EU?" | Yes |
| **Personal data collected** | "What personal data do you collect? (names, emails, IPs, payment info)" | No default — must be provided |
| **Processing activities** | "How do you use this data? (marketing, analytics, service delivery)" | No default — must be provided |
| **Third-party tools** | "What third-party services process your data? (email, analytics, payments)" | No default — list all |
| **Team size** | "How many people access personal data?" | 1-5 |

**GATE: Do not proceed without personal data inventory and processing activities.**

---

## Phase 2: Data Mapping

```
## Data Processing Inventory

### Personal Data Map
| Data Category | Specific Data | Source | Purpose | Legal Basis | Storage Location | Retention |
|--------------|--------------|--------|---------|-------------|-----------------|-----------|
| Contact info | Name, email | Signup form | Service delivery | Contract | [Cloud provider] | Account lifetime + [X] months |
| Payment | Card details | Checkout | Payment processing | Contract | [Stripe/processor] | As required by law |
| Analytics | IP, device, pages | Website | Site improvement | Legitimate interest | [Analytics tool] | [26] months |
| Marketing | Email, name | Opt-in form | Email marketing | Consent | [Email platform] | Until unsubscribe |

### Third-Party Processors
| Processor | Data Shared | Purpose | DPA in Place? | Location |
|-----------|-----------|---------|--------------|----------|
| [Email platform] | Name, email | Email marketing | [Yes/No] | [Country] |
| [Analytics] | IP, behavior | Website analytics | [Yes/No] | [Country] |
| [Payment processor] | Payment data | Transactions | [Yes/No] | [Country] |
| [Cloud hosting] | All stored data | Infrastructure | [Yes/No] | [Country] |
```

---

## Phase 3: Compliance Checklist

```
## GDPR Compliance Checklist

### Lawful Basis for Processing
- [ ] Identified a lawful basis for each processing activity (consent, contract, legitimate interest, legal obligation, vital interest, public task)
- [ ] Documented the lawful basis in the data processing inventory
- [ ] Where consent is the basis, consent is freely given, specific, informed, and unambiguous
- [ ] Consent records are stored (who, when, what they consented to)
- [ ] Legitimate interest assessments documented where applicable

### Privacy Notice / Policy
- [ ] Privacy policy published and easily accessible on website
- [ ] Policy explains: what data is collected, why, how long it is kept, who it is shared with
- [ ] Policy written in clear, plain language (not legal jargon)
- [ ] Policy lists all third-party processors and their purposes
- [ ] Policy explains data subject rights and how to exercise them
- [ ] Policy includes contact information for data protection inquiries
- [ ] Policy updated when processing activities change

### Consent Management
- [ ] Cookie consent banner implemented (opt-in, not pre-checked)
- [ ] Marketing email consent is separate from terms acceptance
- [ ] Consent can be withdrawn as easily as it was given
- [ ] Records of consent are maintained
- [ ] Double opt-in used for email marketing (recommended, not required)

### Data Subject Rights
- [ ] Process exists to handle access requests (Article 15) within 30 days
- [ ] Process exists to handle rectification requests (Article 16)
- [ ] Process exists to handle erasure requests (Article 17) — "right to be forgotten"
- [ ] Process exists to handle data portability requests (Article 20)
- [ ] Process exists to handle objection to processing (Article 21)
- [ ] Process exists to handle restriction of processing (Article 18)
- [ ] Identity verification procedure before fulfilling requests
- [ ] Response templates created for each request type

### Data Security
- [ ] Data encrypted at rest and in transit
- [ ] Access controls implemented (least privilege principle)
- [ ] Strong passwords and multi-factor authentication enforced
- [ ] Regular security assessments conducted
- [ ] Employee/contractor access to personal data is logged
- [ ] Data processing agreements (DPAs) signed with all processors

### Data Breach Response
- [ ] Breach detection and reporting procedures documented
- [ ] Supervisory authority notification process (within 72 hours)
- [ ] Data subject notification process (without undue delay for high-risk breaches)
- [ ] Breach response team identified
- [ ] Breach log maintained

### Data Minimization and Retention
- [ ] Only necessary data is collected (no "just in case" data)
- [ ] Retention periods defined for each data category
- [ ] Automated deletion or anonymization after retention period
- [ ] Regular review of stored data for necessity

### International Transfers
- [ ] Data transfers outside EEA identified
- [ ] Appropriate safeguards in place (Standard Contractual Clauses, adequacy decisions)
- [ ] Transfer impact assessments conducted where required

### Organizational Measures
- [ ] Staff trained on GDPR obligations and data handling
- [ ] Data Protection Officer appointed (if required — 250+ employees or large-scale sensitive data processing)
- [ ] Regular compliance reviews scheduled (at least annually)
- [ ] Privacy by design considered in new products and features
```

---

## Phase 4: Breach Response Plan

```
## Data Breach Response Plan

### Step 1: Detection and Assessment (0-24 hours)
- Identify the breach (unauthorized access, data loss, disclosure)
- Assess scope: what data, how many people, what risk
- Contain the breach (revoke access, patch vulnerability)

### Step 2: Documentation (0-72 hours)
- Record: nature of breach, data affected, number of subjects, likely consequences, measures taken
- Maintain in breach log regardless of severity

### Step 3: Authority Notification (within 72 hours)
If the breach is likely to result in risk to individuals:
- Notify the relevant supervisory authority within 72 hours
- Include: description of breach, categories and number of subjects, likely consequences, measures taken

### Step 4: Data Subject Notification (without undue delay)
If the breach is likely to result in HIGH risk to individuals:
- Notify affected individuals directly
- Include: description in plain language, likely consequences, measures taken, recommendations for protection

### Step 5: Review and Improve
- Conduct post-incident review
- Update security measures to prevent recurrence
- Document lessons learned
```

---

## Example: SaaS Startup with EU Customers

**Data collected:** Name, email, IP, usage data, payment via Stripe. **Processors:** AWS (hosting, US), Stripe (payments, US), Mailchimp (email, US), Google Analytics (analytics, US). **Actions:** Signed DPAs with all processors, implemented cookie consent with opt-in, published privacy policy listing all processors, created data export feature for portability requests, set 26-month retention on analytics data, enabled data deletion on account closure.

---

## Anti-Patterns

- **Treating GDPR as a checkbox exercise** — compliance is ongoing. Revisit when you add new tools, features, or data collection.
- **Relying on consent for everything** — consent is one of six legal bases. Contract performance and legitimate interest are often more appropriate and simpler.
- **Privacy policy nobody can understand** — GDPR requires clear, plain language. If a user cannot understand your policy, it does not comply.
- **No DPAs with processors** — if your email platform processes EU personal data and you do not have a DPA, you are both non-compliant
- **Ignoring the 72-hour breach notification rule** — this is a strict deadline. Have your response plan ready before a breach occurs.

---

## Recovery

- **Not currently GDPR compliant:** Prioritize: 1) Privacy policy, 2) Cookie consent, 3) DPAs with processors, 4) Data subject rights processes. Address highest-risk gaps first.
- **Received a data subject access request:** Respond within 30 days. Verify identity, compile all personal data held, provide in a portable format.
- **Data breach occurred:** Follow the response plan. Document everything. Notify the authority within 72 hours if risk to individuals exists.
- **Using US-only tools without DPAs:** Most major SaaS tools (Stripe, AWS, Mailchimp) offer DPAs. Request and execute them immediately.
