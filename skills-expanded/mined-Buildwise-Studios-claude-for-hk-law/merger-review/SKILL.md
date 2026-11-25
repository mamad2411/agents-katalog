---
name: merger-review
description: >
  Review merger implications under Cap 619 — mandatory for telecom mergers
  (s.12-17), voluntary for others, substantive test (SLC), Competition
  Commission clearance.
---

# Merger Review (s.12–17, Cap 619)

## Overview

Hong Kong's merger control regime under the Competition Ordinance distinguishes between **telecommunications mergers** (mandatory notification) and **non-telecommunications mergers** (voluntary notification to seek clearance).

## Scope

### Telecommunications Mergers (s.12(2), Schedule 7)
- **Mandatory**: Carrier licence holders under the Telecommunications Ordinance (Cap 106)
- Must notify the Competition Commission of a "merger" before completion
- Commission has 30 working days to decide or issue a notice of consideration

### Non-Telecommunications Mergers
- **Voluntary regime**: Parties may apply to the Commission for a decision
- No mandatory pre-merger notification requirement
- Parties may seek informal guidance or a formal clearance decision

## Definition of Merger (s.12)

A merger occurs when:
- Two or more undertakings cease to be distinct
- One undertaking acquires control of another
- One undertaking acquires assets of another

### Joint Ventures
- Full-function joint ventures may constitute mergers
- Partial-function JVs assessed under the first conduct rule

## Substantive Test — SLC

**Substantial Lessening of Competition (SLC)**

The Commission will prohibit a merger that has resulted, or may be expected to result, in an SLC in a market in Hong Kong.

**Analytical Framework:**
1. Define relevant market(s)
2. Assess counterfactual (with vs. without merger)
3. Assess competitive effects:
   - Unilateral effects (single firm market power)
   - Coordinated effects (increased likelihood of coordination)
   - Vertical effects (foreclosure, access to inputs)
4. Consider entry and expansion barriers
5. Assess efficiency gains (merger-specific, pass-on to consumers)
6. Assess failing firm defence

## Commission Procedures

### Informal Guidance
- Confidential
- Non-binding
- Typically within 20 working days

### Formal Clearance Decision
- Public
- Binding (subject to appeal)
- Commission aims to decide within 40 working days

### Variation/Revocation
- Commission may vary or revoke a clearance decision if:
  - Based on false/misleading information
  - There has been a material change in circumstances

## Remedies

- **Structural**: Divestiture of business/assets
- **Behavioural**: Supply obligations, non-discrimination commitments
- **Commitments**: Accepted by Commission during review

## Timeframes

| Step | Days |
|------|------|
| Informal guidance | ~20 working days |
| Formal clearance (Phase 1) | ~40 working days |
| Notice of consideration (Phase 2) | Additional time, no statutory limit |

## Appeals

- Competition Tribunal
- Appeal on merits
- Commission's decision stayed pending appeal (unless Tribunal orders otherwise)

## Penalties

- Directions to remedy
- Pecuniary penalties for failure to comply with directions
- Notifiable telecom mergers completed without notification: up to 10% of Hong Kong turnover


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
