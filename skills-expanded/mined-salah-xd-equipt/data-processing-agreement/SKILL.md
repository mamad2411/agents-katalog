---
name: data-processing-agreement
description: "Drafts data processing agreements for GDPR compliance with processing details and security measures. Use when you process personal data on behalf of another business."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Data Processing Agreement

## When to Use This Skill

Use this skill when you need to:
- Draft a DPA between a data controller and data processor
- Document data processing activities for GDPR compliance
- Establish security measures and breach notification procedures
- Create sub-processor management provisions

**DO NOT** use this skill as a substitute for legal counsel. Data processing agreements have significant legal implications. Have an attorney review the final document.

---

## Core Principle

A DPA EXISTS TO PROTECT PERSONAL DATA BY CLEARLY DEFINING WHO DOES WHAT WITH IT, HOW IT IS SECURED, AND WHAT HAPPENS WHEN SOMETHING GOES WRONG.

---

## Phase 1: Processing Details

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Controller name** | "Who is the data controller (the business that owns the customer relationship)?" | No default — must be provided |
| **Processor name** | "Who is the data processor (the business processing data on behalf of the controller)?" | No default — must be provided |
| **Data types processed** | "What personal data is being processed? (names, emails, IPs, payment info)" | No default — must be provided |
| **Data subjects** | "Whose data? (customers, employees, website visitors, subscribers)" | Customers |
| **Processing purpose** | "Why is the data being processed? (email marketing, analytics, payment, support)" | No default — must be provided |
| **Processing location** | "Where is the data stored and processed? (US, EU, specific countries)" | United States |
| **Sub-processors** | "Do you use third-party services that also process this data?" | Yes — list them |

**GATE: Do not proceed without controller, processor, data types, and processing purpose.**

---

## Phase 2: Agreement Structure

```
## Data Processing Agreement

**Between:**
Controller: [Controller Legal Name] ("Controller")
Processor: [Processor Legal Name] ("Processor")

**Effective Date:** [Date]

### 1. Definitions
- "Personal Data" means any information relating to an identified or
  identifiable natural person as defined in GDPR Article 4(1).
- "Processing" means any operation performed on Personal Data as
  defined in GDPR Article 4(2).
- "Data Subject" means the identified or identifiable person to whom
  Personal Data relates.
- "Sub-processor" means any third party engaged by the Processor to
  process Personal Data on behalf of the Controller.

### 2. Scope and Purpose of Processing

| Detail | Description |
|--------|-------------|
| Subject matter | [Description of the service] |
| Duration | [Duration of the agreement] |
| Nature and purpose | [Why data is processed] |
| Types of Personal Data | [List: names, emails, IPs, etc.] |
| Categories of Data Subjects | [Customers, users, employees, etc.] |

### 3. Obligations of the Processor

The Processor shall:
a) Process Personal Data only on documented instructions from the
   Controller, unless required by law
b) Ensure persons authorized to process data are bound by
   confidentiality obligations
c) Implement appropriate technical and organizational security measures
d) Assist the Controller in responding to Data Subject requests
e) Assist the Controller in ensuring compliance with GDPR Articles
   32-36 (security, breach notification, impact assessments)
f) Delete or return all Personal Data at the end of the agreement,
   at the Controller's choice
g) Make available information necessary to demonstrate compliance
   and allow for audits

### 4. Sub-Processors

| Sub-Processor | Purpose | Data Processed | Location |
|--------------|---------|---------------|----------|
| [Name] | [Purpose] | [Data types] | [Country] |
| [Name] | [Purpose] | [Data types] | [Country] |

The Processor shall:
- Maintain an up-to-date list of sub-processors
- Notify the Controller [30] days before adding a new sub-processor
- Ensure sub-processors are bound by equivalent data protection obligations
- Remain liable for the acts of sub-processors

### 5. Security Measures

The Processor implements the following technical and organizational measures:

**Technical:**
- [ ] Encryption of data at rest and in transit
- [ ] Access controls and authentication
- [ ] Regular security testing and vulnerability assessments
- [ ] Backup and disaster recovery procedures
- [ ] Logging and monitoring of data access

**Organizational:**
- [ ] Staff training on data protection
- [ ] Confidentiality agreements with personnel
- [ ] Incident response procedures
- [ ] Regular review and update of security measures

### 6. Data Breach Notification

The Processor shall notify the Controller of any Personal Data breach
without undue delay and no later than [48/72] hours after becoming
aware of the breach. The notification shall include:

a) Nature of the breach, including categories and approximate number
   of Data Subjects affected
b) Name and contact details of the data protection contact
c) Likely consequences of the breach
d) Measures taken or proposed to address the breach

### 7. International Data Transfers

[If data is transferred outside the EEA:]
Data transfers to countries outside the EEA shall be conducted in
compliance with GDPR Chapter V, using [Standard Contractual Clauses /
adequacy decision / other approved mechanism].

### 8. Data Subject Rights

The Processor shall assist the Controller in fulfilling obligations
to respond to Data Subject requests for:
- Access to their data
- Rectification of inaccurate data
- Erasure of data ("right to be forgotten")
- Restriction of processing
- Data portability
- Objection to processing

### 9. Term and Termination

This DPA shall remain in effect for the duration of the underlying
service agreement. Upon termination, the Processor shall [delete /
return] all Personal Data within [30] days and certify deletion
in writing.

### 10. Governing Law

This DPA is governed by the laws of [jurisdiction].
```

---

## Phase 3: Review and Customize

- Remove sections that do not apply (e.g., international transfers if all processing is domestic)
- Customize security measures to reflect actual implemented controls
- Ensure sub-processor list is complete and accurate
- Align breach notification timeline with your actual capabilities

---

## Phase 4: Finalize

```
## DPA Checklist

- [ ] All processing activities accurately described
- [ ] Sub-processor list is complete
- [ ] Security measures reflect actual controls in place
- [ ] Breach notification timeline is achievable
- [ ] International transfer mechanisms identified (if applicable)
- [ ] Agreement reviewed by legal counsel
- [ ] Signed by authorized representatives of both parties
- [ ] Copy retained by both parties
```

---

## Example: SaaS Email Marketing Platform

**Controller:** E-commerce store (owns the customer list). **Processor:** Email platform (sends emails on store's behalf). **Data:** Customer names, email addresses, purchase history. **Sub-processors:** AWS (hosting), SendGrid (email delivery), Stripe (billing). **Breach notification:** 48 hours. **Data location:** US (AWS us-east-1).

---

## Anti-Patterns

- **Copy-pasting without customizing** — every DPA must reflect the actual processing activities. Generic DPAs miss critical details.
- **Forgetting sub-processors** — if your SaaS uses AWS, Stripe, or any third-party service, those are sub-processors and must be listed.
- **Unrealistic breach notification times** — promising 24-hour notification when you cannot detect breaches that fast sets you up for violations.
- **No audit provisions** — the controller must have the right to verify compliance. Include audit rights.
- **Skipping legal review** — DPAs create binding legal obligations. Always have an attorney review before signing.

---

## Recovery

- **No DPA in place and processing has started:** Draft and execute the DPA immediately. Better late than never for compliance.
- **Controller requests changes:** DPAs are negotiable. Focus on what you can actually comply with rather than agreeing to obligations you cannot meet.
- **Sub-processor changes:** Notify the controller per the agreed timeline. Update the sub-processor list in the DPA.
- **Data breach occurs:** Follow the notification procedure exactly. Document everything. Consult legal counsel immediately.
