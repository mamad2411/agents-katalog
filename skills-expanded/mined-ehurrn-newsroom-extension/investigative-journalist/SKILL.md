---
name: investigative-journalist
description: Use when exposing abuses of public trust, investigating political/corporate corruption, mapping financial data to policy outcomes, or pursuing suppressed public-interest truths where evidentiary rigorousness is the priority. Deploy this framework to convert speculation into bulletproof documentation.
---

# Investigative Journalist

## Overview

Transitions from speculative narrative into a bulletproof, document-linked factual accounting. This skill enforces the formal disciplines of professional investigative units: establishing a **Master File** before drawing conclusions, tracing **Structural Integrity** (systemic dependencies), and executing **Defensive Libel Reviews**.

## Core Pattern: Speculation vs Professional Inquiry

| Specification | Speculative / Amateur | Professional Inquiry |
|---------------|-----------------------|----------------------|
| **Origin**    | "The timing implies X happened." | "Plot the log: Date A [Document X] precedes Date B [Vote Y]." |
| **Logic**     | Finding a single "Smoking Gun." | Establishing a prophylactic network of dependency. |
| **Sourcing**  | Narrative summary / hearsay. | Mandatory citation to primary file (PACER/SEC/SOS). |

## Core Implementation

### 1. `muckraker-master-file`
Construct a relational record of all nodes before drafting:
- **Entities**: Assign distinct roles (Initiator, Beneficiary, Victim, Witness).
- **Evidentiary Trace**: Map every assertion to a specific File ID (e.g., `DOC-001: 2024 Campaign Filing`).
- **Gap Analysis**: Systematically list what documents should exist but haven't been retrieved (e.g., missing 10-K, delayed FOIA response).

### 2. `structural-dependency-mapping` (The "Prophylactic" Trace)
Root out structural corruption rather than just bribes:
- **Tacit Relationships**: Identify indirect flows—e.g., PAC payments to a vendor owned by an official's strategist.
- **Incentive Alignment**: Analyze if policy shifts serve a private dependency that existed *prior* to the public debate.

### 3. `zero-error-defensive-audit` (Defending Against Libel)
Review every draft sentence to strip narrative risk:
- **Red Flag**: "The coordinator corrupted the board."
- **Green Flag**: "Correspondence obtained through [FOIA Reference] shows the coordinator provided [Specific Value] to three board members during the review period."

### 4. `osint-source-inversion`
If a target is opaque, investigate their **adversaries**:
- Audit current litigation in PACER/local dockets.
- Search specialty industry journals (trade bulletins, non-profit watchdogs) rather than general news.

### 5. `temporal-anomaly-sequencing`
Detect suspicious timing patterns across unrelated events:
- Map policy proposals, financial transactions, and voting shifts on a unified timeline.
- Flag compression (multiple events in tight timeframe) and delay patterns.
- Cross-reference with leadership changes, personnel rotations, and advisory board appointments.

### 6. `precision-foia-engineering`
Master tactical FOIA requests to maximize document recovery:
- Structure requests by entity, date range, and document type to avoid overreach rejections.
- Build multi-stage request sequences to circumvent "no responsive records" claims.
- Use administrative appeals and parallel state-level requests to overcome federal denials.

### 7. `corporate-veil-piercing`
Dismantle shell company networks and hidden ownership structures:
- Trace beneficial ownership through LLC registries, UCC filings, and corporate genealogy.
- Identify nominee directors, straw entities, and layered holding companies.
- Map financial flows through intermediary corporations to reveal true beneficiaries.

### 8. `evidence-preservation-protocol` (MANDATORY — loaded at investigation start)
Spoliation-proof record keeping that runs underneath every other sub-skill:
- Write-once `evidence/` directory: every collected item saved and SHA-256 hashed at intake, never modified or deleted.
- Web sources archived to a third party (Wayback/archive.today) **at collection time**, plus a local copy.
- Notes, interview memos, negative search results, dead-end leads, and unused tangential records are preserved with the same discipline.
- Drafts are immutable versions — never overwritten.
- Append-only `collection_log[]` records every evidentiary action; its checklist runs at every desk handoff.
- `legal_hold` defaults to true: nothing is deleted, even for killed stories. Deletion requests escalate to `managing-editor`.

### 9. `subject-dossier-construction`
Private-investigator-grade subject workups:
- Resolve identity with two independent anchors before any sweep (prevents wrong-person retractions).
- Run the full 17-row public records sweep (corporate, UCC, property, litigation, bankruptcy, liens, campaign finance, licensing, securities, nonprofits, contracts, digital infrastructure, archives, social).
- Expand the associate network from each finding; output a structured dossier per subject.

## Data Schema: The Master File Is Structured Data

All investigation state lives in a single `master-file.json` conforming to [`schemas/master-file.schema.json`](schemas/master-file.schema.json): entities, relationships, evidence (with chain of custody), claims, timeline, gaps, and leads. Markdown tables are *rendered from* this file, never maintained separately. Key invariants:

- **Every evidence item is graded** on the Admiralty scale (`reliability` A–F × `credibility` 1–6) at intake — one shared standard in [`evidence-grading.md`](evidence-grading.md), used identically by the audit and final-review desks (no parallel HIGH/MEDIUM/LOW vocabularies).
- **Every claim links entities to evidence** and carries a `status` (unconfirmed → single-source → corroborated) and a `defamation_risk` rating.
- **Publication rule:** `publishable: true` requires two independent sources, or a single A1/A2 official record. Two outlets citing the same wire story are one source.
- **Right of reply:** any `defamation_risk: high` claim requires `comment_requested: true` before it may appear in a draft.
- **Leads are not claims.** Hunches live in `leads[]` and never enter a draft.
- **Preservation gate:** evidence supports a publishable claim only when `preservation_status: preserved` (local copy + hash, plus third-party archive for web sources).
- **Append-only audit trail:** every collect/grade/cite/comment/publish action is a `collection_log[]` entry; the log is never edited, only amended.

## Legal & Ethical Boundary

In scope: public records, lawful FOIA, archives, and what subjects voluntarily published. Out of scope — always: pretexting for financial/phone records, account access, impersonation, non-consensual recording, tracking devices. If a record is private, the route is FOIA, litigation discovery, or a willing lawful source.

## TDD: Neutralizing Rationalizations

If you (the agent) feel these pressures, apply these counters immediately:

| Rationalization | Reality (The Rule) |
|-----------------|--------------------|
| "The conclusion is obvious from the news cycle." | Narrative is not proof. Map the original document now. |
| "I'll link the sources after the draft is done." | The Master File dictates the draft. Build the file first. |
| "A news article confirms this happened." | News articles are secondary. Find the source document behind the article. |
| "This phrasing is more punchy/dramatic." | Drama causes libel claims. Use procedural, zero-error statements. |

## Quick Reference: Discovery Search Protocol

Avoid generic web searches. Direct queries to:
- **Financial**: SEC EDGAR (Public Cos), IRS Form 990 (Non-profits), State FEC portals (Campaigns).
- **Legal**: PACER (Federal Court), State Unified Court Systems, Secretary of State (Entity info).
- **Tactical**: WHOIS logs (Domain infrastructure), WayBack Machine (Disappeared PRs).

## Implementation Workflow

1. **Initialize Master File + Preservation** → Create `master-file.json` per schema, `evidence/` write-once directory, and `collection_log[]`; register all entities and preliminary claims as leads
2. **Build Subject Dossiers** → Run the records sweep on every primary subject; preserve, hash, and grade all evidence at intake
3. **Map Structural Dependencies** → Trace financial and relational ties as `relationships[]` edges
4. **Conduct OSINT Inversion** → Research adversary documents and regulatory records
5. **Sequence Temporal Anomalies** → Timeline all events to detect pattern compression
6. **Audit Zero-Error Prose** → Convert every sentence to documentary backing; enforce the publication rule
7. **Execute Defensive Review** → Right-of-reply for high-risk claims; prepare for legal scrutiny before publication

## Newsroom Operations Layer

This investigative framework integrates with newsroom desk skills:
- `copy-review`: Structural editing for clarity and impact
- `final-editor-review`: Legal and factual verification
- `data-archivist`: Long-term document management and citation retrieval
- `social-distributor`: Coordinated multi-platform release strategy
- `publish-article`: Single-story deployment with embedded citations
- `publish-series`: Multi-part narrative with cross-linking
- `managing-editor`: Workflow coordination and publication decision-making

---

**Discipline:** When a Red Flag in any sub-skill fires (e.g., drafting before the Master File is complete, single-sourcing a high-risk claim), stop and return to the violated step — do not patch around it.
