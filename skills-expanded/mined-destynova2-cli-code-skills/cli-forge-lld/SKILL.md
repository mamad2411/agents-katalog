---
name: cli-forge-lld
metadata:
  author: clement
description: "Generate a Low-Level Design (LLD) document for a software component or service. Use when the user mentions 'LLD', 'low-level design', 'detailed design', 'class diagram', 'sequence diagram', 'API spec', 'database schema', 'component design', 'module design', 'STRIDE', 'threat model', or asks for detailed technical design of a specific service/component. Produces C4 L3-L4 diagrams, class/sequence/state diagrams, API contracts, DB schemas, error handling, and testability design. Do NOT use for system-level architecture — use cli-forge-hld instead."
argument-hint: "[component-or-service-name]"
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

# Forge LLD — Low-Level / Detailed Design

Translate an HLD's "what" into the "how" — detailed enough that a developer can implement without ambiguity. *(Robert C. Martin, Clean Architecture)*

## Core Principles

1. **Mitosis** — the document grows only the sections the component actually needs. A stateless function doesn't need a state machine. A read-only service doesn't need a migration plan. Kill empty sections, don't fill them with boilerplate
2. **Implementable precision** — every included section must be specific enough to code from. No hand-waving
3. **Contract-first** — define API contracts and interfaces before internals
4. **SOLID by default** — design visible in class diagrams must respect SOLID; flag violations explicitly
5. **Patterns justified** — only document a pattern when its use is non-obvious from reading the code
6. **KISS** — one clear diagram beats two pages of prose. One code example beats three paragraphs of explanation. Readers are developers — they scan for interfaces, schemas, and contracts
7. **Gotchas** — read `../gotchas.md` before producing output to avoid known mistakes

---

## Workflow

### Step 1 — Identify scope

| Signal | Output |
|--------|--------|
| "LLD", "low-level design", "detailed design" | Full LLD for a component/service |
| "class diagram", "module design" | Class/module design section only |
| "API spec", "contract", "OpenAPI" | API contract section only |
| "DB schema", "database design", "ER diagram" | Database schema section only |
| "sequence diagram", "flow" | Sequence diagram for a specific flow |
| "STRIDE", "threat model" | Security design section only |
| "state machine", "lifecycle" | State machine section only |

### Step 2 — Locate the HLD anchor

The LLD must reference its parent HLD:
1. Check if an HLD exists in the project (`docs/*hld*`, `docs/*architecture*`, `docs/*design*`)
2. If yes: identify which HLD container(s) this LLD covers
3. If no: note that this LLD is standalone and may need an HLD later

### Step 3 — Gather implementation context

Read existing code if available:
- **Source files** for the component (understand current structure)
- **Cargo.toml / package.json** (dependencies, features)
- **Config files** (understand runtime configuration)
- **Existing tests** (understand testing approach)
- **CI pipeline** (understand deployment constraints)

### Step 4 — Size the document (Mitosis)

Determine the component's complexity tier. The tier decides which sections to include.

**Detect the tier from signals:**

| Signal | Tier |
|--------|------|
| Pure function, utility module, single-file component | **S** |
| Single service with DB, one domain concept | **M** |
| Service with external deps, multiple domain concepts, async flows | **L** |
| Complex service: multi-aggregate, saga, high concurrency, regulated | **XL** |

**Section inclusion matrix:**

| # | Section | S | M | L | XL |
|---|---------|---|---|---|-----|
| 1 | Overview & HLD Anchor | Yes | Yes | Yes | Yes |
| 2 | Component Architecture (C4 L3) | — | Yes | Yes | Yes |
| 3 | Tactical Domain Model | — | If DDD | Yes | Yes |
| 4 | Class/Module Design | Key interfaces | Yes | Yes | Yes |
| 5 | API Contracts | If API exists | Yes | Yes | Yes |
| 6 | Database Schema | If persistence | Yes | Yes | Yes |
| 7 | Sequence Diagrams | Main flow only | Happy + error | All critical | All |
| 8 | State Machines | — | If >2 states | Yes | Yes |
| 9 | Error Handling & Resilience | Error codes only | Yes | Yes | Yes |
| 10 | Concurrency Design | — | — | If shared state | Yes |
| 11 | Caching Strategy | — | If cache exists | Yes | Yes |
| 12 | Component-Level Security (STRIDE) | — | Input validation | Yes | Yes |
| 13 | Testability Design | — | DI points only | Yes | Yes |
| 14 | Configuration & Feature Flags | — | If non-trivial | Yes | Yes |
| 15 | Micro-ADRs | — | If non-obvious | Yes | Yes |
| 16 | Migration Plan | — | — | If brownfield | If brownfield |

**Target document size:**

| Tier | Pages | Sections | Diagrams |
|------|-------|----------|----------|
| S | 1-3 | 3-5 | 1-2 |
| M | 4-8 | 7-10 | 3-5 |
| L | 8-15 | 12-14 | 5-8 |
| XL | 12-20 | All 16 | 8+ |

**Rules:**
- **Never include an empty section.** Omit entirely — don't write "N/A" or "Not applicable"
- **Merge small sections** for tier S. Class Design + API Contract + DB Schema can be one "Implementation" section
- **State the tier** at the top so readers calibrate their expectations
- **Diagram > prose.** If the class diagram already shows the relationships, don't re-explain them in text
- Ask: "Would a developer make a wrong implementation choice without this section?" If no, cut it

### Step 5 — Write the LLD

**Only include sections selected by the mitosis matrix in Step 4.** For tier S, merge related sections freely.

Read `references/sections.md` for full section templates with Mermaid examples. Only include sections selected by the mitosis matrix.

---

## LLD Document Structure

```
# [Component/Service Name] — Low-Level Design

## 1. Overview & HLD Anchor
## 2. Component Architecture (C4 Level 3)
## 3. Tactical Domain Model
## 4. Class/Module Design
## 5. API Contracts
## 6. Database Schema
## 7. Sequence Diagrams (Critical Flows)
## 8. State Machines
## 9. Error Handling & Resilience
## 10. Concurrency Design
## 11. Caching Strategy
## 12. Component-Level Security (STRIDE)
## 13. Testability Design
## 14. Configuration & Feature Flags
## 15. Micro-ADRs
## 16. Migration Plan
```

---

## HLD vs LLD Boundary

| In LLD | NOT in LLD (→ HLD) |
|--------|---------------------|
| C4 Level 3-4 diagrams | C4 Level 1-2 diagrams |
| Full API contracts (OpenAPI) | API surface list |
| Table schemas with indexes | Entity-relationship sketch |
| Class diagrams with methods, SOLID | Container diagram |
| Circuit breaker config values | "We use circuit breakers" |
| Component-level STRIDE (SQLi, IDOR, input validation) | System-level trust boundaries, security policies |
| Retry/backoff configuration | Failure mode categories |
| Migration scripts / phases | "We'll migrate data" |
| Tactical DDD (aggregates, entities, value objects) | Strategic DDD (bounded contexts, context maps) |
| Concurrency design (locks, channels, race conditions) | Scalability strategy (horizontal, sharding) |
| Testability design (DI points, mock boundaries) | Test strategy overview |
| Cache TTLs, invalidation patterns | "We need caching for hot data" |

If you're drawing system context or estimating capacity, you've drifted into HLD territory. Stop and suggest the user invoke `/cli-forge-hld`.

---

## Quality Scoring

Read `references/scoring.md` for the full DCI-LLD formula, 12 checklist items with weights, thresholds, and derived metrics.

## Anti-Patterns

Read `references/anti-patterns.md` for the 9 anti-patterns table with descriptions and fixes.

---

## Review Checklist

**All tiers:** Tier stated | HLD referenced | Interfaces defined | Mermaid syntax | No empty sections | No HLD-level content

**M+:** C4 L3 | API contracts (schemas + errors) | DB schema (ER + indexes) | Sequence diagrams (happy + error) | Error taxonomy

**L+:** Class diagram (SOLID) | State machines | STRIDE | Testability (DI + mocks) | Micro-ADRs

**XL:** Concurrency | Tactical DDD | Migration plan (if brownfield)

**Size:** S: 1-3p | M: 4-8p | L: 8-15p | XL: 12-20p — no section exists just because it's in the template

---

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|-------------------|-----------|-----|
| LLD reveals security threats (STRIDE) | `/cli-audit-code` on affected components | C9 security check |
| API contracts defined | `/cli-audit-drift` | Bootstrap CONTRACTS.md from the LLD |
| Component has complex state machine | `/cli-forge-schema` | Generate state diagram |
| PostgreSQL/SQLx schema, transactions, or brownfield migration carry business invariants | `/cli-forge-data` | Produce the database decision, concurrency proof, and safe migration plan |

**Rule:** Recommend, don't auto-execute.

## Integration with other cli-* skills

| Skill | Relationship |
|-------|-------------|
| `cli-forge-hld` | Provides the container architecture that LLD zooms into |
| `cli-forge-schema` | Can generate the Mermaid diagrams used in the LLD |
| `cli-audit-code` | Validates the implementation matches the LLD design |
| `cli-audit-test` | Validates test coverage matches the testability design |
| `cli-cycle` | Calls cli-forge-lld as part of full project review |
| `cli-forge-data` | Deepens sections 6, 8, 10, and 16 for PostgreSQL/SQLx persistence |

---

## Reference Sources

**Books:** Clean Architecture (Martin), DDD (Evans), IDDD (Vernon), Learning DDD (Khononov), PEAA (Fowler), Design Patterns (GoF), Release It! (Nygard), Domain Modeling Made Functional (Wlaschin), Working with Legacy Code (Feathers)

**Templates:** [C4 Model](https://c4model.com/), [arc42](https://arc42.org/overview), [MADR](https://adr.github.io/madr/), [French DAT](https://github.com/bflorat/modele-da), [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design), [STRIDE](https://owasp.org/www-community/Threat_Modeling_Process)
