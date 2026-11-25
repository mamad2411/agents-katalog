---
name: compliance-programme
description: >
  HK competition law compliance programme design — risk assessment, training,
  reporting, audit, leniency preparation, Competition Commission investigation
  readiness.
---

# Compliance Programme (HK Competition Law)

## Overview

An effective competition law compliance programme reduces the risk of infringement, enables early detection, facilitates leniency applications, and may mitigate penalties in the event of a breach.

## Core Components

### 1. Risk Assessment

Identify areas of the business most exposed to competition law risk:

- **Sales and pricing teams**: Price fixing, bid rigging, market sharing
- **Trade associations**: Information exchange, collective boycotts
- **Distribution**: Resale price maintenance, exclusive dealing, tying
- **Procurement**: Bid rigging, information exchange with competitors
- **M&A activity**: Gun-jumping, information sharing during due diligence
- **Dominant firms**: Abuse of substantial market power (s.21)

**Output**: Risk register with likelihood × impact scoring

### 2. Policy and Procedures

Create clear written policies:

- Competition Law Compliance Policy (board-approved)
- Competition Law Handbook (practical guidance for staff)
- Code of Conduct covering interactions with competitors
- Pricing policy and discount guidelines
- Trade association participation guidelines
- Information exchange protocols
- Merger control protocol (pre-notification assessment)

### 3. Training Programme

| Level | Audience | Frequency | Content |
|-------|----------|-----------|---------|
| Basic | All staff | Annual | Overview, key rules, reporting |
| Intermediate | Sales, pricing, procurement | Biannual | Sector-specific risks, case studies |
| Advanced | Senior management, legal | Annual | Director liability, leniency, investigations |
| Specialised | M&A team | Ad hoc | Merger control, information sharing |

### 4. Monitoring and Audit

- Periodic compliance audits (internal or external)
- Transaction surveillance (pricing, bidding patterns)
- Email and communications monitoring (within legal limits)
- Compliance KPIs integrated into performance reviews

### 5. Reporting Mechanisms

- Confidential whistleblower hotline
- Designated compliance officer
- Non-retaliation policy for good faith reporting
- Anonymous reporting options

### 6. Leniency Preparation

Being ready to apply for leniency:

- Pre-prepared internal investigation protocol
- Document preservation procedures (legal hold)
- Model board resolution for leniency application
- Pre-identified legal counsel for competition matters
- Crisis communication plan

## Investigation Readiness

### Dawn Raid Response Plan

1. **Reception**: Escort officials to meeting room, verify identity and warrant
2. **Legal counsel**: Immediate notification; no substantive responses until legal arrives
3. **Document preservation**: Do not destroy or delete documents
4. **IT support**: Facilitate forensic imaging where required
5. **Employee interviews**: Cooperate, but request legal presence
6. **Designated contact**: Single point of contact for the investigation

### Commitment Agreements (s.66)

The Commission may accept commitments from investigated parties as an alternative to enforcement action. A compliance programme is often a key component of acceptable commitments.

## Penalty Mitigation

A credible compliance programme may:
- Reduce the base penalty by up to 20%
- Demonstrate good corporate governance
- Serve as evidence of no intentional breach

## Director Liability

Directors may be liable for:
- Authorising or participating in the breach
- Failing to take reasonable steps to prevent the breach
- Director disqualification orders (up to 5 years)

**Compliance programme as defence**: Evidence of a robust programme demonstrates directors took reasonable steps.

## Implementation Roadmap

| Phase | Timeline | Activities |
|-------|----------|------------|
| 1. Assessment | Month 1 | Risk assessment, gap analysis |
| 2. Design | Months 2–3 | Policy drafting, training materials |
| 3. Implementation | Months 4–6 | Training roll-out, processes |
| 4. Monitoring | Ongoing | Audits, updates, refreshers |


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
