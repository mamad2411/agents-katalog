---
name: independent-contractor-agreement
description: "Creates independent contractor agreements with scope, payment, IP ownership, and non-compete clauses. Use when hiring freelancers or contractors for your business."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Independent Contractor Agreement

## When to Use This Skill

Use this skill when you need to:
- Draft an independent contractor agreement for a freelancer or consultant
- Define scope of work, payment terms, and deliverables
- Establish IP ownership and confidentiality protections
- Create a reusable contractor agreement template

**DO NOT** use this skill for employment agreements, partnership agreements (use partnership-agreement), or client service agreements (use client-agreement). This is specifically for hiring independent contractors. Have an attorney review before use.

---

## Core Principle

A CONTRACTOR AGREEMENT MUST CLEARLY ESTABLISH THE INDEPENDENT CONTRACTOR RELATIONSHIP, PROTECT YOUR IP, AND DEFINE EXACTLY WHAT IS BEING DELIVERED FOR WHAT PRICE.

---

## Phase 1: Engagement Details

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Your business name** | "What is your legal business name?" | No default — must be provided |
| **Contractor name/company** | "Who is the contractor?" | No default — must be provided |
| **Scope of work** | "What will the contractor do? (specific deliverables)" | No default — must be provided |
| **Compensation** | "How will they be paid? (hourly, project, retainer)" | Project-based |
| **Timeline** | "What is the project timeline or engagement period?" | No default — must be provided |
| **IP ownership** | "Who owns the work product? (you or contractor)" | Company owns all work product |

**GATE: Do not proceed without scope, compensation, and timeline.**

---

## Phase 2: Agreement Structure

```
## Independent Contractor Agreement

**This Agreement** is entered into as of [Date] between:

**Company:** [Legal Business Name] ("Company")
**Contractor:** [Contractor Name/Business] ("Contractor")

### 1. Engagement and Services

Company engages Contractor to perform the following services:

**Scope of Work:**
[Detailed description of services, deliverables, and milestones]

| Deliverable | Description | Due Date |
|------------|-------------|----------|
| [Deliverable 1] | [Description] | [Date] |
| [Deliverable 2] | [Description] | [Date] |
| [Deliverable 3] | [Description] | [Date] |

Contractor shall perform services in a professional and workmanlike
manner consistent with industry standards.

### 2. Term

This Agreement begins on [Start Date] and continues until [End Date
or completion of services], unless terminated earlier per Section 9.

### 3. Compensation

| Component | Amount | Terms |
|-----------|--------|-------|
| [Project fee / Hourly rate / Retainer] | $[X] | [Payment schedule] |
| Payment method | [ACH / check / PayPal] | |
| Payment terms | Net [15/30] from invoice | |
| Late payment fee | [1.5%/month] | |
| Expenses | [Reimbursable with pre-approval / included in fee] | |

Contractor shall submit invoices [weekly / biweekly / upon milestone
completion / monthly]. Company shall pay within [15/30] days of receipt.

### 4. Independent Contractor Status

Contractor is an independent contractor, NOT an employee. Contractor:
- Controls the manner and means of performing services
- Sets own hours and work location
- Provides own tools and equipment
- May perform services for other clients
- Is responsible for own taxes, insurance, and benefits
- Will receive a 1099-NEC (not a W-2) for tax reporting

Company shall not withhold taxes, provide benefits, or otherwise treat
Contractor as an employee.

### 5. Intellectual Property

**Work Product Ownership:**
All work product created under this Agreement, including [designs,
code, content, strategies, materials], shall be the exclusive property
of Company. Contractor assigns all rights, title, and interest in the
work product to Company.

**Pre-Existing IP:**
Contractor retains ownership of pre-existing intellectual property
created before this engagement. Contractor grants Company a
non-exclusive, perpetual license to use any pre-existing IP
incorporated into the work product.

**Portfolio Rights:**
Contractor [may / may not] display the work in their portfolio,
subject to [no restrictions / Company approval / after a [90]-day
exclusivity period].

### 6. Confidentiality

Contractor shall not disclose Company's confidential information,
including business strategies, customer data, financial information,
trade secrets, and proprietary processes. This obligation survives
termination for [2] years.

### 7. Non-Solicitation

During the engagement and for [12] months after, Contractor shall not
directly solicit Company's clients or employees for competing services.

### 8. Representations and Warranties

Contractor represents that:
- They have the skills and qualifications to perform the services
- The work product will be original and not infringe third-party rights
- They are free to enter this agreement without conflicting obligations
- They will comply with all applicable laws

### 9. Termination

Either party may terminate this Agreement with [14/30] days written
notice. Upon termination:
- Company pays for work completed through the termination date
- Contractor delivers all work product completed to date
- Confidentiality obligations survive termination

Company may terminate immediately for material breach, including
missed deadlines, substandard work, or breach of confidentiality.

### 10. Limitation of Liability

Contractor's total liability shall not exceed the total fees paid
under this Agreement. Neither party is liable for indirect,
incidental, or consequential damages.

### 11. Dispute Resolution

Disputes shall be resolved through [mediation / arbitration /
litigation] in [jurisdiction/state].

### 12. General Provisions

- **Entire Agreement:** This document is the complete agreement.
- **Amendments:** Changes require written agreement by both parties.
- **Governing Law:** Governed by the laws of [State].
- **Severability:** Invalid provisions do not affect remaining terms.

---

**Company:**
Name: _______________ Title: _______________
Signature: _______________ Date: _______________

**Contractor:**
Name: _______________ Title: _______________
Signature: _______________ Date: _______________
```

---

## Phase 3: Customize and Review

- Adjust IP ownership terms based on the specific engagement
- Set appropriate non-solicitation duration (some states limit enforceability)
- Include any specific insurance requirements (E&O, liability)
- Add indemnification clause if needed for the type of work

---

## Phase 4: Delivery

```
## Agreement Checklist

- [ ] Scope of work is specific enough to avoid scope creep
- [ ] Payment terms are clear (amount, schedule, method)
- [ ] IP ownership clause matches your intentions
- [ ] Independent contractor classification factors are met
- [ ] Confidentiality terms are appropriate for the work
- [ ] Termination provisions protect both parties
- [ ] Both parties have signed and retained copies
- [ ] W-9 collected from contractor for tax reporting
- [ ] Agreement reviewed by legal counsel
```

---

## Example: Hiring a Freelance Designer

**Scope:** Design brand identity package (logo, color palette, typography, brand guidelines). **Compensation:** $3,500 project fee, 50% upfront, 50% on final delivery. **Timeline:** 4 weeks, 2 revision rounds included. **IP:** All designs become Company property upon final payment. Designer may include in portfolio after 90 days.

---

## Anti-Patterns

- **Treating a contractor like an employee** — controlling hours, requiring office attendance, and providing equipment can trigger misclassification liability
- **Vague scope of work** — "help with marketing" is not a scope. Define specific deliverables, quantities, and quality standards.
- **No IP assignment clause** — without explicit assignment, the contractor may own the work they create for you
- **Verbal agreements** — always put it in writing, even for small projects. Disputes over $500 are not worth the legal headache.
- **No termination clause** — both parties need an exit ramp. Define how to end the engagement cleanly.

---

## Recovery

- **Already working without a contract:** Execute an agreement now covering work going forward. For past work, create a brief assignment document covering IP ownership.
- **Contractor misclassification risk:** Review the IRS 20-factor test. If the relationship looks more like employment, consult an employment attorney.
- **Scope creep:** Reference the SOW in the contract. Additional work requires a written change order with updated compensation.
- **Contractor not delivering:** Follow the termination clause. Document performance issues in writing before terminating.
