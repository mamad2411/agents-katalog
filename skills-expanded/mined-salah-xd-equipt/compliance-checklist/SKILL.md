---
name: compliance-checklist
description: "Creates industry-specific regulatory compliance checklists with documentation requirements and audit preparation. Use when ensuring your business meets regulatory obligations."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Compliance Checklist

## When to Use This Skill

Use this skill when you need to:
- Create a regulatory compliance checklist for your industry
- Identify compliance obligations for a new business or product launch
- Prepare for a compliance audit or review
- Document compliance procedures and responsible parties

**DO NOT** use this skill for legal advice or as a substitute for a compliance officer. This is a planning and tracking tool. Consult industry-specific legal counsel for complex compliance requirements.

---

## Core Principle

COMPLIANCE IS NOT OPTIONAL — IT IS THE COST OF DOING BUSINESS IN A REGULATED ENVIRONMENT. PROACTIVE COMPLIANCE IS CHEAPER THAN REACTIVE PENALTIES.

---

## Phase 1: Business and Industry Profile

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Industry** | "What industry are you in? (e-commerce, health, finance, education, food, SaaS)" | No default — must be provided |
| **Business model** | "What do you sell or provide?" | No default — must be provided |
| **Location** | "Where are you based and where do you sell? (states, countries)" | United States |
| **Customer type** | "Who are your customers? (consumers, businesses, minors, patients)" | Consumers (B2C) |
| **Data collected** | "What personal or sensitive data do you collect?" | Name, email, payment info |
| **Team size** | "How many employees or contractors?" | 1-10 |

**GATE: Do not proceed without industry, business model, and location.**

---

## Phase 2: Universal Compliance

These apply to nearly all businesses. Check all that apply and complete accordingly.

```
## Universal Business Compliance

### Business Formation and Registration
- [ ] Business entity properly formed (LLC, Corp, etc.)
- [ ] Registered with Secretary of State
- [ ] EIN obtained from IRS
- [ ] State tax registration completed
- [ ] Local business license obtained (if required)
- [ ] DBA ("doing business as") filed (if using a trade name)
- [ ] Annual report filings current

### Tax Compliance
- [ ] Federal tax obligations identified (income, self-employment)
- [ ] State tax obligations identified (income, sales, franchise)
- [ ] Sales tax collection set up (if selling taxable goods/services)
- [ ] Sales tax nexus states identified
- [ ] Quarterly estimated tax payments scheduled
- [ ] 1099-NEC filing for contractors paid $600+
- [ ] W-2 filing for employees
- [ ] Payroll tax compliance (if employees)

### Employment and Contractor
- [ ] Worker classification correct (employee vs. contractor)
- [ ] Employment agreements in place
- [ ] I-9 forms completed for employees
- [ ] Workers' compensation insurance (if required by state)
- [ ] Anti-discrimination policies in place
- [ ] OSHA compliance (if applicable)
- [ ] Minimum wage and overtime compliance

### Data Privacy and Security
- [ ] Privacy policy published on website
- [ ] Cookie consent mechanism implemented (if EU visitors)
- [ ] CCPA compliance (if California customers and revenue >$25M or data thresholds)
- [ ] GDPR compliance (if EU customers)
- [ ] Data breach response plan documented
- [ ] PCI compliance (if processing credit cards)
- [ ] SSL/TLS certificate on website

### Consumer Protection
- [ ] Refund/return policy clearly posted
- [ ] Terms of service published
- [ ] FTC advertising guidelines followed (truthful, not deceptive)
- [ ] Testimonial and endorsement disclosures (FTC guidelines)
- [ ] Affiliate disclosures on all affiliate content
- [ ] CAN-SPAM compliance for email marketing
- [ ] Unsubscribe mechanism in all marketing emails

### Insurance
- [ ] General liability insurance
- [ ] Professional liability / E&O insurance (if providing services)
- [ ] Cyber liability insurance (if handling sensitive data)
- [ ] Product liability insurance (if selling physical products)
```

---

## Phase 3: Industry-Specific Compliance

Select the applicable industry section and customize.

### E-Commerce

```
## E-Commerce Compliance

- [ ] Sales tax collection in nexus states
- [ ] Marketplace facilitator laws compliance (if selling on Amazon, etc.)
- [ ] Product safety regulations (CPSC for consumer products)
- [ ] FTC labeling requirements (textiles, care labels, country of origin)
- [ ] ADA website accessibility (WCAG 2.1 AA recommended)
- [ ] Shipping and delivery disclosures
- [ ] Subscription billing compliance (ROSCA / state auto-renewal laws)
- [ ] Import/export regulations (if international)
```

### Health and Wellness

```
## Health/Wellness Compliance

- [ ] FDA regulations (supplements, health claims, labeling)
- [ ] FTC health claim restrictions (no unsubstantiated claims)
- [ ] HIPAA compliance (if handling protected health information)
- [ ] State licensing requirements (if providing health services)
- [ ] Disclaimer that content is not medical advice
- [ ] Informed consent procedures (if providing services)
```

### Financial Services

```
## Financial Compliance

- [ ] State money transmitter licenses (if handling payments)
- [ ] SEC/FINRA registration (if providing investment advice)
- [ ] Anti-money laundering (AML) procedures
- [ ] Know Your Customer (KYC) procedures
- [ ] Financial disclaimer (not financial advice)
- [ ] State lending/usury laws (if offering financing)
```

### SaaS / Technology

```
## SaaS/Technology Compliance

- [ ] SOC 2 Type I or II (if handling customer data)
- [ ] GDPR compliance (DPA, data subject rights, breach notification)
- [ ] CCPA compliance
- [ ] COPPA compliance (if under-13 users)
- [ ] App store compliance (Apple/Google requirements)
- [ ] Open source license compliance
- [ ] Accessibility (Section 508 / WCAG)
- [ ] Data residency requirements
```

### Education / Courses

```
## Education/Course Compliance

- [ ] FTC earnings claims guidelines
- [ ] Refund policy (state requirements vary)
- [ ] ADA/accessibility for course content
- [ ] COPPA (if under-13 students)
- [ ] FERPA (if handling student educational records)
- [ ] State education provider registration (some states require)
- [ ] Testimonial/results disclaimers
```

---

## Phase 4: Compliance Management

```
## Compliance Tracking

### Compliance Calendar
| Obligation | Frequency | Due Date | Owner | Status |
|-----------|-----------|----------|-------|--------|
| [Annual report filing] | Annual | [Date] | [Who] | [Done/Pending] |
| [Sales tax filing] | [Monthly/Quarterly] | [Date] | [Who] | |
| [Privacy policy review] | Annual | [Date] | [Who] | |
| [Insurance renewal] | Annual | [Date] | [Who] | |
| [Tax return filing] | Annual | [Date] | [Who] | |

### Audit Preparation
- [ ] All compliance documentation organized and accessible
- [ ] Policies and procedures are current and dated
- [ ] Training records maintained
- [ ] Incident/complaint log up to date
- [ ] Third-party compliance certifications current

### Review Schedule
- Monthly: Tax filings, payroll compliance
- Quarterly: Privacy policy, advertising compliance, contractor classifications
- Annually: Full compliance audit, insurance review, license renewals
```

---

## Example: Online Course Business

**Key compliance areas:** Business registration (LLC in Texas), sales tax (economic nexus in 5 states), FTC earnings claims compliance (uses income examples in marketing), CAN-SPAM for email list, privacy policy + cookie consent for website, CCPA compliance (California customers), refund policy posted, affiliate disclosures on recommended tools, testimonial disclaimers.

**Gaps identified:** No earnings disclaimer on sales pages, no CCPA "Do Not Sell" link, sales tax not collected in 2 nexus states.

---

## Anti-Patterns

- **Assuming compliance is a one-time task** — regulations change. Review compliance at least annually.
- **Copying a competitor's policies** — their compliance obligations may differ from yours. Build from your specific situation.
- **Ignoring state-level requirements** — many compliance obligations vary by state (sales tax, employment law, licensing). Do not assume federal compliance is enough.
- **No documentation** — if you cannot prove compliance, you are not compliant in the eyes of an auditor.
- **Waiting until you get caught** — fines and penalties far exceed the cost of proactive compliance.

---

## Recovery

- **Discovered a compliance gap:** Address it immediately. Document the gap, the remediation steps, and the completion date. Proactive remediation is viewed favorably.
- **Received a regulatory notice:** Consult an attorney immediately. Respond within the specified timeframe. Do not ignore it.
- **Operating without required licenses:** Apply immediately. Most regulatory bodies prefer voluntary compliance over enforcement.
- **No compliance documentation:** Start documenting now. Create a compliance folder and begin building records going forward.
