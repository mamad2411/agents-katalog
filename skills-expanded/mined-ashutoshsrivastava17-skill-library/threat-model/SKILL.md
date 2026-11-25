---
name: threat-model
description: >
  Build a structured threat model for a system, feature, or change.
  Identifies assets, threat actors, attack surfaces, and mitigations using STRIDE.
  TRIGGER when: user says /threat-model, asks about threats to a system,
  wants to identify attack vectors, or needs a security risk assessment for a feature.
argument-hint: "[system, feature, or change to model]"
user-invocable: true
---

# Threat Modeling

You are a security engineer conducting a structured threat model. Produce a clear, actionable threat model tailored to the system or change under review.

## Process

### Step 1: Understand the Scope

Gather context:
- What system, feature, or change is being modeled?
- What are the trust boundaries?
- What data flows exist (user input, APIs, databases, third-party services)?
- Who are the users and what are their privilege levels?
- What is the deployment environment?

### Step 2: Identify Assets

List what an attacker would target:
- Sensitive data (PII, credentials, tokens, financial data)
- System resources (compute, storage, network)
- Business logic (payment flows, auth, authorization)
- Availability (uptime, SLAs)

### Step 3: STRIDE Analysis

For each component or data flow, analyze threats using STRIDE:

| Threat | Description | Example |
|--------|-------------|---------|
| **S**poofing | Pretending to be someone else | Forged auth tokens, session hijacking |
| **T**ampering | Modifying data or code | SQL injection, parameter manipulation |
| **R**epudiation | Denying an action occurred | Missing audit logs, unsigned transactions |
| **I**nformation Disclosure | Exposing data to unauthorized parties | Verbose errors, insecure storage, SSRF |
| **D**enial of Service | Making a system unavailable | Resource exhaustion, algorithmic complexity |
| **E**levation of Privilege | Gaining unauthorized access | IDOR, broken access control, privilege escalation |

### Step 4: Risk Assessment

For each identified threat:

| Threat | Likelihood | Impact | Risk Level | Mitigation |
|--------|-----------|--------|------------|------------|
| *description* | Low/Med/High | Low/Med/High | Low/Med/High/Critical | *specific countermeasure* |

### Step 5: Recommendations

Prioritize mitigations by:
1. **Critical** — Must fix before shipping
2. **High** — Should fix before shipping, accept risk if timeline-constrained
3. **Medium** — Fix in next iteration
4. **Low** — Track and address opportunistically

## Output Format

Present findings as a structured document with:
- Scope and assumptions
- Data flow diagram (text-based)
- STRIDE threat table
- Risk assessment matrix
- Prioritized recommendations

## Edge Cases

- For API changes: focus on authentication, authorization, input validation, and rate limiting
- For infrastructure changes: focus on network segmentation, secrets management, and access control
- For third-party integrations: focus on supply chain risk, data sharing, and trust boundaries
- For client-side changes: focus on XSS, CSRF, and sensitive data exposure

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
