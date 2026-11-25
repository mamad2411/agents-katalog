---
name: cli-forge-hld
metadata:
  author: clement
description: "Generate a High-Level Design (HLD) document for a software system. Use when the user mentions 'HLD', 'system design', 'architecture document', 'design doc', 'ADR', 'C4 diagram', 'back-of-envelope', 'capacity planning', 'ATAM', 'arc42', 'design proposal', 'Gate review', or says 'design X', 'architect Y'. Produces C4 L1-L2 diagrams, capacity estimations, ADRs, tradeoff analysis, and deployment architecture. Do NOT use for low-level/detailed design (class diagrams, DB schemas, API specs) — use cli-forge-lld instead."
argument-hint: "[system-name-or-description]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - WebSearch
  - WebFetch
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are written in English. When generating user-facing output, detect the project's primary language (from README, comments, docs, commit messages) and produce the document in that language. If the project is bilingual, ask the user which language to use before proceeding.

> **Diacritics rule:** When the chosen output language uses diacritics (French, Spanish, Portuguese, etc.), render them correctly — including on capitals (É, À, Ç, Ô…). Never strip accents to ASCII: write "sécurité" not "securite", "Rôle" not "Role". ASCII-flattened French is a defect, not a style.

> **Writing style:** Favor clarity — short sentences, one idea per sentence, plain words. A metaphor only when it clarifies. Keep one consistent register (impersonal/infinitive for operational docs). Separate narrative prose, meant to make the reader understand, from telegraphic content (tables, commands, checklists) which stays terse for action.

> **No fabricated output:** Never invent command output, console captures, API responses, metrics, or logs. When real output is needed, emit a clearly-marked placeholder (🚧 "replace with a real capture"), never plausible-but-fake text presented as real.

# Forge HLD — High-Level System Design

> "Everything is a trade-off. Why is more important than how." — Neal Ford & Mark Richards

## Core Principles

1. **Mitosis** — the document grows only the sections the project actually needs. A CLI tool doesn't need a deployment diagram. A single-service app doesn't need a context map. Kill empty sections, don't fill them with boilerplate
2. **Numbers before architecture** — always estimate capacity before designing. The numbers determine whether you need 1 server or 100
3. **Every decision needs a "why"** — no technology choice without justification via ADR
4. **Tradeoffs are explicit** — use ATAM-style reasoning: "We chose X over Y because [quality attribute] matters more than [other attribute] in this context"
5. **Diagrams are mandatory** — use Mermaid for all visuals (C4, sequence, deployment)
6. **Non-goals are as important as goals** — they prevent scope creep (Google design doc tradition)
7. **KISS** — if a section can be one table instead of three paragraphs, use the table. If a diagram replaces a page of text, use the diagram. Readers scan, they don't read
8. **Gotchas** — read `../gotchas.md` before producing output to avoid known mistakes

---

## Workflow

### Step 1 — Identify scope

| Signal | Output |
|--------|--------|
| "HLD", "architecture", "system design", "high-level" | Full HLD document |
| "ADR", "decision record" | ADR section only (MADR format) |
| "estimate", "capacity", "back-of-envelope", "sizing" | Capacity estimation section only |
| "design doc", "tech spec", "Gate review", "proposal" | Full HLD with executive summary |
| "tradeoff", "compare options" | ATAM tradeoff analysis only |

### Step 2 — Gather requirements

Extract or ask for **functional requirements** (use cases, actors, critical journeys) and **non-functional requirements** using ISO 25010:2023 as checklist:

| Quality Attribute | Questions to ask |
|-------------------|-----------------|
| Performance | Latency targets? Throughput (RPS)? Response time SLOs? |
| Reliability | Availability target (99.9%? 99.99%)? RTO/RPO? |
| Scalability | Expected users now? In 1 year? Growth rate? Peak events? |
| Security | Auth model? Encryption? Compliance (ANSSI, DISA STIG, PCI-DSS, RGPD)? |
| Maintainability | Team size? Deployment frequency? |
| Portability | Multi-cloud? On-prem? Air-gapped? |
| Data | Retention? Backup? Sovereignty? Volume? |

If the user already provided context, use that instead of asking redundant questions.

### Step 3 — Size the document (Mitosis)

S/M/L/XL semantics are canonical in `../shared/tiering.md` — the tables below specialize them to system complexity and the arc42 section inclusion matrix.

**Detect the tier from signals:**

| Signal | Tier |
|--------|------|
| CLI tool, library, single-purpose utility | **S** |
| Single service/app, 1 team, 1 DB | **M** |
| Multi-service, multi-team, or regulated | **L** |
| Distributed system, multi-region, compliance-heavy | **XL** |

**Section inclusion matrix:**

| # | Section | S | M | L | XL |
|---|---------|---|---|---|-----|
| 1 | Executive Summary | — | — | Yes | Yes |
| 2 | Goals and Non-Goals | Yes | Yes | Yes | Yes |
| 3 | Stakeholders & Constraints | — | Yes | Yes | Yes |
| 4 | System Context (C4 L1) | Yes | Yes | Yes | Yes |
| 5 | Solution Strategy | Yes | Yes | Yes | Yes |
| 6 | Container Architecture (C4 L2) | — | Yes | Yes | Yes |
| 7 | Capacity Estimations | — | If >1K users | Yes | Yes |
| 8 | Domain Boundaries (Strategic DDD) | — | — | If multi-context | Yes |
| 9 | Data Architecture | If persistence | Yes | Yes | Yes |
| 10 | API Design (High-Level) | If API exists | Yes | Yes | Yes |
| 11 | Security & Trust Boundaries | Minimal | Yes | Yes | Yes |
| 12 | Deployment Architecture | — | If non-trivial | Yes | Yes |
| 13 | Observability & SLOs | — | — | Yes | Yes |
| 14 | Failure Modes | — | Top 3 only | Yes | Yes |
| 15 | ADRs | 1-2 key ones | 3-5 | All major | All |
| 16 | Tradeoff Analysis | — | — | If contested | Yes |
| 17 | Risks and Open Questions | If any | Yes | Yes | Yes |
| 18 | Glossary | — | If domain-heavy | Yes | Yes |

**Target document size:**

| Tier | Pages | Sections | ADRs |
|------|-------|----------|------|
| S | 2-4 | 4-6 | 1-2 |
| M | 5-10 | 8-12 | 3-5 |
| L | 10-18 | 14-16 | 5-8 |
| XL | 15-25 | All 18 | 8+ |

**Rules:**
- **Never include an empty section.** If a section doesn't apply, omit it entirely — don't write "N/A"
- **Merge small sections** when possible. For tier S, Security + Data + API can be one "Technical Decisions" section
- **State the tier** at the top of the document so readers know the level of detail to expect
- If in doubt about whether a section is needed, ask: "Would removing this section cause someone to make a wrong decision?" If no, cut it

### Step 4 — Run back-of-envelope estimations (if tier M+ or >1K users)

Read `references/estimation-cheatsheet.md` for formulas, unit conversions, latency numbers, and scalability laws. Compute traffic, storage, bandwidth, cache, and server estimates. Present results in a clear table — these numbers drive every subsequent design decision.

### Step 5 — Write the HLD

Read `references/sections.md` for full section templates with Mermaid diagrams, tables, and examples. Only include sections selected by the mitosis matrix in Step 3. For tier S, merge related sections freely.

## HLD Document Structure

```
# [System Name] — High-Level Design

## 1. Executive Summary
## 2. Goals and Non-Goals
## 3. Stakeholders & Constraints
## 4. System Context (C4 Level 1)
## 5. Solution Strategy
## 6. Container Architecture (C4 Level 2)
## 7. Capacity Estimations
## 8. Domain Boundaries (Strategic DDD)
## 9. Data Architecture
## 10. API Design (High-Level)
## 11. Security Architecture & Trust Boundaries
## 12. Deployment Architecture
## 13. Observability & SLOs
## 14. Failure Modes and Mitigation
## 15. Architecture Decision Records (ADRs)
## 16. Tradeoff Analysis
## 17. Risks and Open Questions
## 18. Glossary
```

## HLD vs LLD Boundary

| In HLD | NOT in HLD (→ LLD) |
|--------|---------------------|
| "We use PostgreSQL" | Table schemas with columns and indexes |
| C4 Level 1-2 diagrams | C4 Level 3-4 diagrams |
| "REST API with JWT auth" | Full OpenAPI spec with request/response schemas |
| Entity-relationship sketch | Column types, constraints, migration scripts |
| "Circuit breaker on external calls" | Retry config values, DLQ policy |
| Architecture style decision | Class/module structure, SOLID |
| Deployment topology | Dockerfile, Helm values |
| SLOs and error budgets | Alerting rules, runbook procedures |
| Bounded contexts + context map (strategic DDD) | Aggregates, entities, value objects (tactical DDD) |
| Trust boundaries + security policies (STRIDE system) | Component-level threats (STRIDE per class/module) |
| "We need caching for hot data" | Cache TTLs, invalidation patterns, Redis config |

If you're writing column-level detail or class diagrams, you've crossed into LLD territory. Stop and suggest the user invoke `/cli-forge-lld` for that component.

## Quality Scoring

After writing, score the HLD using the Architecture Completeness Index (ACI). Read `references/scoring.md` for the full formula, 12-item checklist with weights, thresholds, and derived metrics.

## Anti-Patterns

Before delivering, verify the HLD avoids common traps. Read `references/anti-patterns.md` for the 10 anti-patterns table.

## Review Checklist

**All tiers:** Tier stated | Goals + Non-Goals | C4 L1 | Solution strategy with rationale | 1+ ADR per decision | Arrows labeled | No empty sections
**M+:** C4 L2 | NFRs addressed | Tech justified | Security model | Data flow (write + read path)
**L+:** Capacity with formulas | Deployment architecture | Failure modes | SLIs/SLOs
**XL:** Context map | ATAM tradeoff | Glossary
**Size:** S: 2-4p | M: 5-10p | L: 10-18p | XL: 15-25p — no section exists just because it's in the template

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|-------------------|-----------|-----|
| HLD reveals components needing detailed design | `/cli-forge-lld` | Generate LLD |
| Deployment architecture needs infrastructure | `/cli-forge-infra` | Ops integration |
| Architecture needs visual diagrams | `/cli-forge-schema` | Generate C4 Mermaid |

**Rule:** Recommend, don't auto-execute.

## Integration with other cli-* skills

| Skill | Relationship |
|-------|-------------|
| `cli-forge-lld` | Takes the HLD and zooms into component/code level for each container |
| `cli-forge-schema` | Can generate the Mermaid diagrams used in the HLD |
| `cli-forge-infra` | Helps implement the deployment architecture section |
| `cli-audit-test` | Validates the testing strategy implied by the architecture |
| `cli-cycle` | Calls cli-forge-hld as part of full project review |

## Reference Sources

- Kleppmann — *Designing Data-Intensive Applications* | Bass, Clements, Kazman — *Software Architecture in Practice* | Ford, Richards — *Fundamentals of Software Architecture* | Brown — *The C4 Model* | Evans — *Domain-Driven Design*
- [arc42](https://arc42.org/overview) | [C4 Model](https://c4model.com/) | [MADR](https://adr.github.io/madr/) | [Google Design Docs](https://www.industrialempathy.com/posts/design-docs-at-google/) | [French DAT](https://github.com/bflorat/modele-da) | [ISO 25010:2023](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010)
- ByteByteGo | Software Engineering Radio | InfoQ | Software Engineering Daily
