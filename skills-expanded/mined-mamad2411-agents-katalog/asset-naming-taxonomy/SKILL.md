---
name: asset-naming-taxonomy
description: Use when defining or enforcing consistent naming taxonomy and conventions across governance reports, customizations, documentation, and code artifacts.
---

# Taxonomy

## Specialization

Define and enforce the workspace naming taxonomy so every artifact is classified, consistently named, and discoverable across its full lifecycle context.

The taxonomy has four classification layers. A name is only fully correct when all four layers are aligned:

1. **Type** — what structural form the artifact takes.
2. **Lane** — which lifecycle phase it primarily serves.
3. **Domain** — what subject area it operates on.
4. **Function** — what action it performs, expressed through vocabulary choice.

## Classification Model

### Layer 1: Asset Type

Each asset type has a fixed structural identity determined by path and file extension.

| Type | Path | Extension | Role |
|---|---|---|---|
| Agent | `.github/agents/` | `*.agent.md` | Specialist persona with routing role |
| Instruction | `.github/instructions/` | `*.instructions.md` | Policy constraint applied by `applyTo` scope |
| Prompt | `.github/prompts/` | `*.prompt.md` | Workflow entry point with output contract |
| Skill | `.github/skills/<name>/` | `SKILL.md` | Reusable procedure invoked by agents or prompts |

### Layer 2: Lane

Every asset has exactly one primary lane and optionally one secondary lane. Lane assignment is authoritative in:
- [skills-discovery-index.md](../../catalogs/skills-discovery-index.md) for skills
- [agents-discovery-index.md](../../catalogs/agents-discovery-index.md) for agents
- Prompt and instruction lifecycle catalogs

For canonical lane definitions, clarification prompts, synonyms, and known vocabulary exceptions use **[lane-intent.md](./references/lane-intent.md)**. Keep lane guidance centralized there to avoid drift.

### Layer 3: Domain

Every asset belongs to one primary domain category. Domain is inferred from the noun part of the name.

| Domain | Keywords | Example Assets |
|---|---|---|
| Governance | governance, lifecycle, cadence, naming, taxonomy, audit, health | Use the workspace catalogs to map governance assets deterministically. |
| Engineering | dotnet, csharp, syrx, resilience, refactor, test, tdd, scaffold | Use keyword-to-lane matching and verify with catalog metadata. |
| Mobile | maui, mobile, ux, ui, prototype, usability | Use mobile-focused keywords and confirm ownership in catalogs. |
| Data | sql, dba, database, schema | Use data-domain keywords and validate lane/type in catalogs. |
| DevOps | docker, powershell, cicd, scripts, scripting, branch, editorconfig | Use automation/tooling keywords and resolve via catalog entries. |
| Documentation | docs, readme, adr, technical, corpus, index, librarian, plan, prd | Use docs-oriented keywords and confirm artifact type and lane. |
| Meta-workflow | task, route, executing, skill, agent, prompt, critical, learn, refine, ideas | Use workflow keywords and classify via lane-intent and catalogs. |

### Layer 4: Function Vocabulary

The verb or lead noun in a name should reflect the lane the asset belongs to. This is a guidance rule: the catalog is authoritative for lane assignment; vocabulary conformance is a quality signal and a drift detector.

Use **[function-vocabulary.md](./references/function-vocabulary.md)** as the canonical source for lane vocabulary, noun-form patterns, drift detection, and the naming formula.

A name whose leading verb does not align with its lane is a vocabulary drift signal. It is not automatically a violation but must be justified by a clear disambiguation note in the catalog, then recorded in [lane-intent.md](./references/lane-intent.md).

## Lightweight Ontology

The four layers have a defined relationship. This ontology is not encoded in file names; it is a classification framework for authoring and audit decisions.

```
Asset ──belongs-to──▶ Lane (Planning | Execution | Review)
Asset ──operates-on──▶ Domain (Governance | Engineering | Mobile | Data | DevOps | Documentation | Meta-workflow)
Asset ──artifact-type-is──▶ Type (Agent | Instruction | Prompt | Skill)
Name-part ──signals──▶ [Lane-via-vocabulary, Domain-via-noun]
```

Practical uses of the ontology:
- **Authoring**: pick a verb from the target lane's vocabulary; pick a noun from the target domain's keywords.
- **Drift detection**: if a skill's name uses a Review verb but its catalog lane is Execution, that is a signal to investigate.
- **Discovery**: a new team member can find assets by knowing lane + domain without reading catalog tables.

## Trigger Conditions

Invoke this skill when any of the following is true:

- A new asset must be named and the right lane + domain is not obvious.
- Naming inconsistency, vocabulary drift, or lane mismatch is detected.
- A workspace rename/migration requires deterministic naming convergence.
- New naming standards must be introduced with backward-compatible migration guidance.
- Governance checks need explicit naming policy references.

## Inputs

- Workspace root path.
- Scope (`all`, `governance`, `customizations`, `docs`, `code`).
- Optional override profile in `./references/naming-conventions.json`.
- Optional migration mode (`report-only` or `apply` when authorized).

## Required Outputs

- Naming taxonomy assessment grid with pass/fail/advisory per scope (Type, Lane, Domain, Function columns).
- Canonical naming map (`legacy → canonical`) for each detected inconsistency.
- Vocabulary drift signals table for lane/function mismatches.
- Policy alignment notes mapped to:
  - `.github/instructions/governance-naming-conventions.instructions.md`
  - `.github/instructions/governance-lifecycle.instructions.md`
  - `.github/instructions/technical-docs.instructions.md`
- Ranked remediation grid with deterministic next actions.

## Workflow

1. Load workspace naming policy and lifecycle governance instructions.
2. Load configurable patterns and domain categories from `./references/naming-conventions.json`.
3. Load lane clarification prompts and synonyms from `./references/lane-intent.md`.
4. Load function vocabulary and drift-detection guidance from `./references/function-vocabulary.md`.
5. For each asset in scope: classify by Type, Lane, Domain, and Function.
6. Detect pattern-level drift (regex non-conformance) and vocabulary-level drift (lane/verb mismatch).
7. When lane or domain is unclear, use the clarification prompts from `lane-intent.md` before proceeding.
8. Build canonical rename map and identify reference rewrites.
9. Produce report-first output with all four classification layers represented.
10. Only apply changes when explicitly authorized (`apply` mode).
11. After apply-mode migrations: run naming, link integrity, and catalog checks.
12. Record catalog updates and add new vocabulary exceptions to `lane-intent.md`.

## References

- [naming-conventions.json](./references/naming-conventions.json) — Configurable patterns, lane vocabulary, domain categories, ontology, and report name mappings.
- [lane-intent.md](./references/lane-intent.md) — Lane definitions, clarification prompts, synonyms, and known vocabulary exceptions.
- [function-vocabulary.md](./references/function-vocabulary.md) — Full verb/noun vocabulary per lane, drift detection guide, and naming formula.
- [README.md](./references/README.md)

## Done Criteria

- All four classification layers (Type, Lane, Domain, Function) are assessed for the requested scope.
- Pattern-level and vocabulary-level drift are both reported.
- A single canonical naming scheme is active with all legacy alternatives explicitly mapped.
- Policy alignment and governance checks are explicitly mapped.
- Migration guidance is complete and deterministic.

## Execution Context

### Input Context

- Request objective and scope boundary.
- Applicable constraints and required outputs.

### Process Context

- Follow this skill's deterministic workflow from intake to closure.
- Record ownership and decisions for required outputs.

### Output Context

- Deliverables with explicit completion status.
- Residual risks and next actions.
