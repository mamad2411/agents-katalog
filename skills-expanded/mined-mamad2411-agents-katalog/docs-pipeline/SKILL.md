---
name: docs-pipeline
description: "Genera y verifica un set completo de documentación de diseño: premise audit, decision register, 14 tipos de documento, trazabilidad y verificación con 3 scripts. Úsala con 'documenta este proyecto', 'documentación de diseño', 'traceability matrix' o para auditar un set existente."
---

# Docs Pipeline

Turns a project idea into a **complete, verified design documentation set** — and then checks it mechanically, because instructions are advisory and exit codes are not.

**The output is a document set that can be handed to an implementer or an AI agent with no further architectural decisions to make.**

---

## When to use this

| Situation | Enter at |
| :--- | :--- |
| A raw idea document exists and needs to become a design | Phase 0 |
| A document set exists and may be incomplete | Phase 5, then 7 |
| A document set exists and needs verification only | Phase 7 |
| The user asks "what else is missing?" | Phase 5 |

---

## The four ideas this pipeline is built on

1. **Audit the premises before generating anything.** An idea document assumes things it never states — that there is a client, a team, a budget, a deployment. If those premises are wrong, generating fourteen documents produces fourteen wrong documents, faster. This is the highest-value step and it must block.
2. **Separate assumptions from decisions, then order by blocking power.** A flat list of 40 questions is unusable. Deduplicated and tiered by what they block, it is 25 answerable questions, most with a defensible default.
3. **Complete is a checklist, not a feeling.** Fourteen document classes. A set can be well written and still missing the spine.
4. **Verify mechanically.** Three scripts, run before every commit. What they catch is what a human stops noticing after the second document.

---

## Phase 0 — Intake

Read the input. Identify, in one pass:

- **Domain** and what the system does
- **Actors** and which of them touch the system
- **Scale claims** (how many users, orders, branches)
- **The stack the idea proposes**, if any
- **What the document assumes but never states**

Write nothing yet.

---

## Phase 1 — Premise audit · BLOCKING

Read [`references/premise-audit.md`](references/premise-audit.md) and apply it.

The three premises that change everything:

| Premise | If false, what changes |
| :--- | :--- |
| **Who builds it** — a team, or one person | Scope, timeline, and whether the MVP is feasible at all |
| **Who it is for** — a client with requirements, or the author's portfolio | Every "requirement" is a design decision, not a client demand |
| **Where it runs** — on-premise, cloud, one host | The entire deployment and infrastructure section |

**Gate:** present the corrected framing and the questions it raises. **Do not generate a single document until the user confirms it.**

> Skipping this gate is the single most expensive mistake this pipeline can make. It happened: 38 documents were generated for a project that assumed a client, a three-developer team and an on-premise deployment. None of the three existed. Fifteen documents had to be archived.

---

## Phase 2 — Decision register · BLOCKING

Read [`references/decision-register.md`](references/decision-register.md).

1. **Collect** every assumption from the input plus every decision the design will require.
2. **Deduplicate.** Assumptions and decisions overlap heavily: "the stack is Next.js" is both. A 39-item list became 29 questions.
3. **Tier by blocking power**, not by topic. Tier 0 blocks everything; Tier 5 blocks nothing.
4. **Recommend** a value for every question, with the reason. Most questions should be answerable by approving a batch.
5. **Ask tier by tier**, in batches. Present the whole register so the user sees the shape, then ask about the tier that blocks.

**Gate:** the tier-0 questions must be answered before Phase 3. Everything else can be approved in a batch or corrected later.

> **Answer format that works:** a single table of question → recommendation → answer. The user replies "acepto todo salvo P04 y P11". Do not ask one question per turn across 30 turns.

---

## Phase 3 — Planning

Load and follow `planning-core`, `planning-roadmap`, `planning-risk`, `planning-stakeholders`, `planning-status` (el modo compacto de `planning-core` produce el charter en 1 página).

Produces: charter, roadmap, risks, stakeholders, status.

**Adapt to the real premise.** A solo portfolio project has no stakeholders and no RACI. A risk register for a team project is not a risk register for a solo one — abandonment and scope creep replace team rotation and client churn.

---

## Phase 4 — Design

Load and follow `design-core`, `design-data`, `design-api`, `design-adr` (el modo compacto de `design-core` produce las secciones agent-optimized).

Produces: architecture, schema, API contract, ADRs, technical spec.

**Rules that matter:**
- The **OpenAPI contract is the source of truth**. No endpoint is implemented before it is specified.
- Every significant decision gets an ADR with **alternatives considered and rejected**. An ADR without rejected alternatives is a note, not a decision record.
- Money, time and identifiers get explicit rules. `NUMERIC(19,4)`, `TIMESTAMPTZ`, UUIDv7.

---

## Phase 5 — Completeness layer

Read [`references/completeness.md`](references/completeness.md).

**This is the phase most often skipped, and it is where a design becomes verifiable.** Compare the set against the fourteen document classes and generate what is missing.

The four that are almost always missing, and why they matter:

| Missing class | What breaks without it |
| :--- | :--- |
| **Requirements with stable IDs** | Nothing else can reference anything. This is the spine |
| **Non-functional requirements with numbers** | A target that cannot be measured is a wish. "Fast" is not a requirement |
| **Traceability matrix** | Nothing proves the design is complete, or that no endpoint is scope creep |
| **Operations runbook** | No backup procedure, no incident response, no capacity model. An unrehearsed restore is not a backup |

---

## Phase 6 — Design system

Load and follow `agent-anti-slop-designer` (modo estándar o experimental — `references/experimental.md` para lo arriesgado/memorable).

**Derive the visual direction from the domain, not from a menu of art movements.** The best design system is made of the product's own artifacts. A restaurant system is made of thermal tickets, rubber stamps and heat lamps; a logistics system is made of manifests, barcodes and loading docks.

Then update `agent-docs/DESIGN.md` to a token sheet pointing at the full document. **A stale token sheet is worse than none**, because an agent will read it.

---

## Phase 7 — Verification · BLOCKING

Run all three scripts. Fix what fails, or declare it explicitly in the document.

```bash
python scripts/check-docs.py          <project-dir>
python scripts/check-traceability.py  <project-dir>
python scripts/check-consistency.py   <project-dir>
```

### Severity model

Not every check should gate. A check that fails on false positives gets ignored, which is worse than no check.

| Check | Severity | Why |
| :--- | :--- | :--- |
| Missing required document class | **GATE** | The set is incomplete by definition |
| Broken internal link | **GATE** | A navigational link that goes nowhere is a defect |
| Emoji in an English document | **GATE** | A stated convention |
| Mermaid in `agent-docs/` | **GATE** | Agent docs use text graphs |
| Requirement ID traced but undefined | **GATE** | A reference to something that does not exist |
| Requirement defined but untraced | **GATE** | The design does not cover it |
| Endpoint in the contract, untraced | **GATE** | Either scope creep or a missing requirement |
| NFR group untraced | **GATE** | No verification method |
| ADR referenced but absent | **GATE** | A dangling decision reference |
| Count conflicts | *Advisory* (`--strict` to gate) | Ambiguous nouns: "33 tables" and "24 tables" are not a contradiction when one means schema and the other means seed data |
| Endpoints traced but outside the contract | *Advisory* | Expected when the contract covers an earlier release than the matrix |
| Paths in prose not found | *Advisory* | Planned artifacts and conventions are legitimately not files yet |
| Duplicated table headers | *Advisory* | A summary in two documents is fine; it drifts when values change |

### Known false-positive classes

Documented so they are not "fixed" by weakening a real check:

| Symptom | Real cause | Fix |
| :--- | :--- | :--- |
| `NFR-1` reported as an undefined ID | The pattern reads `NFR-1.1` as `NFR-1` | Negative lookahead for `.digit`, plus an ignore-prefix list |
| Business rules (`RN-01`) reported as untraced requirements | A different ID namespace | Add the prefix to the ignore list |
| `/orders/{id}` vs `/orders/{orderId}` reported as different endpoints | Path parameter names are an implementation detail | Normalise `{...}` to `{}` on both sides |
| Narrative documents reported as contradicting themselves | A decision log and a changelog describe past states on purpose | Exclude them: they are records, not live documents |
| The raw idea document reported as full of undefined IDs | It is the input, not part of the set | Exclude `index.md` |
| Archived documents reported with broken links | Archive is a record; a link to something that moved is expected | Exclude `archive/` from every check |

---

## Phase 8 — Publish

Read [`references/publish.md`](references/publish.md).

Git hygiene that prevents problems later: `eol=lf` in `.gitattributes`, a minimal `.gitignore`, `main` as the branch, conventional commits.

**Archive, never delete.** A superseded document moves to `docs/archive/`. The question "why did this change?" has an answer six months later.

---

## Language split

Read [`references/language-split.md`](references/language-split.md).

Documents are written for a reader, and different readers need different languages. The portfolio surface goes in English; the working documents stay in the author's language. Translating a working document is effort with no benefit.

---

## What this skill does NOT do

- **Does not estimate in points or hours.** That is a separate concern. Effort ranges in weeks are fine; a Fibonacci estimate is not this skill's job.
- **Does not write code.** It produces the design and the scaffold order. The implementation is a separate pass.
- **Does not run the design system questionnaire.** It delegates that to the anti-slop skill.
- **Does not generate a document set before Phase 1 and 2 are confirmed.** This is the one hard rule.
- **Does not weaken a check to make it pass.** If a check fails, either the document is wrong or the check has a documented false-positive class. Fix the right one.

---

## Files

| File | Purpose |
| :--- | :--- |
| `references/premise-audit.md` | How to find the premises an idea document does not state |
| `references/decision-register.md` | Deduplication and tiering by blocking power |
| `references/completeness.md` | The fourteen document classes and the orphan analysis |
| `references/language-split.md` | Which documents go in which language, and why |
| `references/publish.md` | Git hygiene for a documentation repository |
| `scripts/check-docs.py` | Completeness, links, emoji, mermaid, count consistency |
| `scripts/check-traceability.py` | Requirement IDs, NFR groups, endpoint orphans |
| `scripts/check-consistency.py` | ADR references, ID references, paths, duplicated tables |
