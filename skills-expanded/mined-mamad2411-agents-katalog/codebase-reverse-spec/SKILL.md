---
name: codebase-reverse-spec
description: (NS) Reverse-engineer an existing, legacy, or brownfield codebase into a technology-agnostic business description of what the system actually does — business rules, actors, permissions, hierarchies, state lifecycles, and external integrations, without implementation details. Use this skill whenever the user mentions brownfield, legacy code, modernization, reverse engineering, codebase analysis, extracting business rules from code, engenharia reversa, documentar sistema legado, gerar spec a partir do código, or wants a functional description faithful to the current product to support rewrite, migration, onboarding, or audit — even if they do not name this skill. Do NOT use for simple code reviews, bug fixes, or when the user explicitly wants a technical architecture document.
---

# Codebase Reverse System Description

Reconstruct, from an existing codebase, a **technology-agnostic** descriptive document of the implemented system: observed behavior, business rules, permissions, hierarchies, and external integrations relevant to product operation.

## Central principle

Code is evidence of behavior. The goal is to answer **what the system does and why**, not how it was built. Avoid programming languages, frameworks, libraries, databases, architecture patterns (MVC, microservices, etc.), and class/function names as the axis of explanation.

Golden rule for every sentence: _"If I rewrote this system from scratch on another stack, would this sentence still be true?"_ If not, rewrite it in business terms.

Permitted exceptions (only when essential to understand the current domain):

- External integration/provider names (ERPs, gateways, BI, identity, analytics).
- Access roles/profiles and organizational hierarchy levels.
- Entity attribute names when needed to preserve business semantics (not to detail technical structure).

## When to use

- Legacy modernization/migration without losing business rules
- Documenting a system with no (or outdated) documentation
- Onboarding a new team
- Auditing business rules before a rewrite on another stack
- Producing a faithful functional description of the current system

## Scope and repository access

1. Confirm the repository path (or ask if unclear). Use `Read` / `Glob` for a high-level structure overview.
2. In monorepos, confirm which product/module folder is in scope — analyze **only** that subtree unless the user explicitly wants the whole repo.
3. For external/legacy repos, confirm read access and any folders that are out of scope (generated code, vendored deps, infra-only).

## Workflow

Follow phases in order. Do not skip Phase 0 — without it the final spec mixes guesswork with fact.

### Phase 0 — Scope and intent

Ask the user (one question at a time, or `AskQuestion` when appropriate):

| Question                                                    | Why it matters                                                 |
| ----------------------------------------------------------- | -------------------------------------------------------------- |
| Whole system or a specific module/domain?                   | Prevents scope creep or missed areas                           |
| Executive summary or exhaustive description?                | Sets depth and length                                          |
| Output language?                                            | Spec language may differ from skill/conversation language      |
| Any critical/risky domain needing extra scrutiny?           | Prioritizes financial, fiscal, permission, or compliance logic |
| Deliver incrementally (large codebases) or single document? | Large repos benefit from domain-by-domain drafts               |

If the repo is large, do **not** read everything at once. Do reconnaissance first (Phase 1) and prioritize by business impact, not file size.

### Phase 1 — Reconnaissance (map, not line-by-line reading)

Goal: locate where business logic lives before reading in detail.

1. List the directory tree (root, ~2 levels) with `Glob` or equivalent.
2. Identify domain-core candidates: folders/files named like `services`, `domain`, `rules`, `validators`, `models`, `usecases`, `handlers`, `controllers`, or language-specific equivalents.
3. Identify entry points: API routes, scheduled jobs, message queues, screens/forms, CLI commands. These reveal **what the system allows someone (human or another system) to do** — the basis for use cases.
4. Identify data sources (tables, entities, schemas) — not to document persistence technology, but to understand which **things** the business tracks.
5. List existing tests if any. Tests often document business rules better than production code because they describe expected behavior in scenario language.
6. Map explicitly:
   - permission and access model;
   - organizational/functional hierarchies;
   - external integrations and each one's role in the business flow.
7. Build a **prioritized investigation list** ordered by business value (not technical complexity).

**Checkpoint (recommended):** Present the reconnaissance map and prioritized list to the user before deep extraction. Wrong scope discovered here saves hours of wasted reading. Skip only if the user asked for a fully autonomous run.

Use `references/coverage_matrix.md` as a mental checklist — mark what you found and what still needs investigation.

### Phase 2 — Rule extraction

For each prioritized area, maintain a working log using `references/extraction_log_template.md`. Do not write the final spec yet — accumulate evidence and confidence first.

For each logic fragment:

1. Read relevant code (handlers, validations, calculations, conditionals, state machines).
2. Ask:
   - What business decision does this represent?
   - Which input data matters, and why?
   - What happens in each branch (success, failure, exception, edge case)?
   - Is there a plausible business reason for this rule (credit limit, legal deadline, fiscal rule), even if the code does not comment it?
3. Translate each finding into a verifiable business-rule sentence: **"When [business condition], the system [expected behavior], unless [exception]."** Never cite function/class/variable names in that sentence.
4. Mark confidence:
   - **Confirmed**: clear behavior, covered by tests or explicit validation.
   - **Inferred**: reasonable deduction from code, without direct confirmation.
   - **Ambiguous/Suspect**: confusing, contradictory, dead, or likely-bug code. Flag for human review — do **not** promote a bug to an intentional business rule without warning.
5. Capture **negative rules** — things the system explicitly prevents (validations, permissions, blocks). Restrictions are as much part of the spec as capabilities.
6. For external integrations, record:
   - business trigger;
   - business data involved (no technical payload);
   - expected outcome on success/failure;
   - operational impact when unavailable (degraded mode, block, manual fallback).
7. For entities, record attributes by semantics — cite attribute names only when ambiguity would otherwise remain.
8. For status/state fields, document the **lifecycle**: allowed transitions, who triggers them, terminal states, and whether transitions are enforced or merely conventional.

### Phase 3 — Domain structuring

Organize extracted material into:

- **Business entities** and business-relevant attributes (not DB column types or implementation types).
- **Relations** in business language ("an Order belongs to a Customer and contains one or more Order Lines").
- **Use cases / flows**, each with: actor, goal, preconditions, step-by-step expected behavior, outcome, and business exceptions/errors.
- **Cross-cutting policies**: rules applying across use cases (authorization, audit, limits).
- **Access model**: roles, profiles, scopes, permission hierarchies.
- **External integrations**: third-party systems, business purpose, expected behavior.
- **Domain glossary**: domain-specific terms found in code (field names, statuses, enums) translated into clear definitions.
- **State lifecycles** (when applicable): entity states, transitions, and enforcement rules.

### Phase 4 — Final spec writing

Use `references/spec_template.md` as the base. Adapt title/emphasis to "description of the implemented system." Do not write as a future PRD or a technical code report. Tone: declarative, present tense, describing observed product behavior.

Before delivery, run the sanity pass:

1. Walk `references/anti_leakage_checklist.md` — remove or rewrite any technical leakage.
2. Optionally run `scripts/scan_leakage.sh <spec-file>` for a first-pass automated scan (review hits manually; the script catches patterns, not intent).
3. Walk `references/coverage_matrix.md` — confirm each dimension is addressed or explicitly marked N/A with reason.
4. Confirm permissions, hierarchies, and integrations are described functionally.
5. Attribute names appear only to preserve business semantics, without technical detail.
6. Confidence markers live in the appendix ("Areas to validate with the team"), not cluttering the main body.
7. Apparent bugs are not disguised as business rules — they go to the appendix with a note that behavior may be unintentional.
8. The document answers **what** and **why** (when inferable), never **how it was implemented**.

### Phase 5 — Delivery and validation

Deliver:

1. **Final spec** — markdown by default; docx only if the user requests Word format.
2. **Extraction log** (optional to share) — the working `extraction_log` if the user wants traceability to evidence.
3. **"Areas to validate with the team"** appendix — short list of inferred/ambiguous rules and suspected bugs. Epistemic honesty: the spec must not fake certainty.

Ask whether the user wants to deepen a specific module, adjust detail level, deliver the next domain slice (large repos), or export another format.

## Large codebase strategy

When the repo exceeds what fits comfortably in one pass:

1. Complete Phases 0–1 for the whole scope; get checkpoint approval on the domain map.
2. Extract and draft **one domain at a time** (Phases 2–4 per domain), each as a section or separate file.
3. Run a **synthesis pass**: merge domains, deduplicate glossary entries, reconcile cross-cutting policies, and verify the coverage matrix once for the whole system.
4. Do not block delivery on 100% coverage — deliver completed domains with an explicit "not yet analyzed" list.

## Common mistakes to avoid

- Listing the tech stack "for context" instead of describing business behavior.
- Confusing folder structure (technical artifact) with domain structure (business concept) — always translate.
- Producing a normative future-requirements document instead of faithfully describing the **currently implemented** system.
- Treating DB field/variable names as official business terminology without verifying they map to real concepts.
- Omitting external integrations, access roles, or hierarchies for fear of "coupling" — they are part of the observed domain.
- Reading the entire repository file-by-file without prioritization.
- Promoting clearly broken/dead logic to "intentional business rule."
- Losing confidence markers between extraction and final writing — use the extraction log.

## Reference files

| File                                    | When to read                              |
| --------------------------------------- | ----------------------------------------- |
| `references/spec_template.md`           | Phase 4 — structure of the final document |
| `references/extraction_log_template.md` | Phase 2 — working notes during extraction |
| `references/coverage_matrix.md`         | Phases 1 and 4 — completeness check       |
| `references/anti_leakage_checklist.md`  | Phase 4 — pre-delivery sanity pass        |
| `scripts/scan_leakage.sh`               | Phase 4 — optional automated first pass   |
