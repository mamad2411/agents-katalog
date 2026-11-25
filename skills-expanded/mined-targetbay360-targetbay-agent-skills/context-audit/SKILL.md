---
name: context-audit
description: Use when onboarding a store nobody has assessed yet and the first question is what this store actually is — what TargetBay knows about it, what it already has configured across all three products, and which of those facts are measured rather than assumed. Reads the derived store context and reports what is derived, what is provisional, what is simply absent, and which questions only the store owner can answer. Produces no plan; establishes what a plan could honestly be built from.
license: MIT
metadata:
  targetbay.display_name: Store Context Audit
  targetbay.version: "0.2.0"
  targetbay.category: audit
  targetbay.requires: onboarding.store_context
  targetbay.risk_level: analysis
  targetbay.execution_mode: analyze_only
  targetbay.status: foundation
---

# Store Context Audit

## Purpose

Establish what is actually known about a store before anything is decided for it.

Onboarding fails in a specific way: the operator does not know this store, so they build what they built
last time. The defence is not more planning, it is knowing precisely which facts about this store are
measured, which are borrowed from a vertical, and which do not exist at all. This skill produces that
partition and stops there.

## When to Use

- Onboarding a store for the first time, before any plan exists
- A store has just signed up, migrated, or connected a new TargetBay product
- Before running [onboarding-blueprint](../onboarding-blueprint/SKILL.md), which depends on this partition
- Re-checking a blueprint's assumptions after the store has accumulated history

## When Not to Use

- The store has an established programme and the question is what to improve. Use the product audit
  skills — for example
  [opportunity-discovery](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/opportunity-discovery/SKILL.md)
  or
  [personalization-audit](../personalization-audit/SKILL.md).
- A specific product's configuration is in question rather than the whole store.
- The answer needed is a plan. This skill deliberately produces none; see
  [onboarding-blueprint](../onboarding-blueprint/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| The derived store context for this store | The entire input to the audit | Blocked |
| Capability readiness across all three products | Determines what any later skill can do at all | Blocked |
| Existing coverage per product | A migrated store is rarely empty (G5) | Partial; treat coverage as unknown, never as empty |
| When the context was computed | A decision made on stale evidence is a different decision | Partial; warn |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `onboarding.store_context` | The Store Context Pack and its per-capability readiness matrix |

## Decision Process

```
1. Read capability readiness      ← what is reachable for this store at all
2. Read the store context pack    ← identity, vertical, catalogue, customers, brand, coverage
3. Partition every value by basis ← derived / provisional / stated / absent
4. Read coverage                  ← what already exists, per product
5. Map readiness onto skills      ← which skills are blocked, and by what
6. List what only the store knows ← the intake gaps
7. Report. Decide nothing.
```

Step 3 is the skill. Everything downstream depends on nobody being able to confuse a measurement with a
default, and this is the only place that distinction gets made explicit.

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md),
[../../knowledge/evidence-and-provenance.md](../../knowledge/evidence-and-provenance.md).

- **Report the basis with every value** (G3, G14). A number without one is indistinguishable from a guess.
- **A provisional value is reported with what would replace it** (G14).
- **An absent value is reported as absent.** Never as a range, never as "roughly", never as a vertical
  default quietly promoted (G3).
- **An empty read is not a measurement** (S12).
- Cite `computed_at` alongside any value reported from the pack.
- Report existing coverage before anything else about the store's future. A migrated store's existing
  automation is a fact, not an obstacle (G5).
- Do not recommend, rank or sequence. That is [onboarding-blueprint](../onboarding-blueprint/SKILL.md)'s
  work, and doing it here removes the reviewer's chance to disagree with the facts before the plan is
  built on them.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read capability readiness and the store context pack | `read_only` |
| ANALYZE | Partition by basis; map readiness onto blocked skills; list intake gaps | `analysis` |
| REPORT | Present the four lists, the coverage inventory and the readiness matrix | `analysis` |

No PLAN, no APPROVE, no EXECUTE phase. This skill cannot change anything.

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) at `risk_level: analysis` containing: four lists
partitioning every pack value into derived, provisional, stated and absent; the existing-coverage
inventory per product; the capability readiness matrix with the skills each gap blocks; the list of
questions only the store owner can answer; and `computed_at` for the pack the report was built from.
Every absent value carries the observation that would make it derivable.

## Validation

- [ ] Every reported value carries its basis (G3, G14)
- [ ] Every provisional and absent value carries its `replaced_by`
- [ ] No absent value was given a substitute, a range or an approximation
- [ ] Existing coverage reported per product, including "unknown" where it could not be read (G5)
- [ ] Readiness matrix complete across all three namespaces
- [ ] `computed_at` stated, and staleness flagged if beyond the pack's TTL
- [ ] No recommendation, ranking or sequencing appears anywhere in the output

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read context and readiness | `read_only` | None |
| Report the partition | `analysis` | None |

Needing no approval is why this skill is safe to run first on every store.

## Examples

**"What do we actually know about this store?"**
A six-year-old store with 40,000 orders. Most boundaries come back derived with sample sizes in the
thousands; brand is derived from 120 templates; loyalty coverage is absent because the product was never
configured. The report says so, names the two capabilities that returned `unavailable`, and lists the
four intake questions the platform cannot answer — margin posture, capacity, brand policy and blackout
dates.

**"We just signed up — what can you tell us?"**
A store live for nine days with three orders. Nearly every derived value returns absent. The audit
reports that plainly, states the catalogue-shape facts that are visible without any order history, and
lists what each absent value is waiting for — "200 customers with a second purchase" rather than a date.
No thresholds are offered, because none can be derived and offering a default here would be the failure
this skill exists to prevent.

## Failure Handling

| Situation | Response |
|---|---|
| Store context unavailable | **Blocked.** There is nothing to audit; record it in `unmet_requirements` |
| Pack older than its TTL | **Partial.** Report it, cite `computed_at`, and recommend a refresh before planning |
| A pack section unavailable | **Partial.** That section is absent, never defaulted from another store or a vertical |
| Readiness matrix unavailable | **Partial.** Report capability status as unknown; do not infer availability from a successful read elsewhere |
| Coverage unreadable | **Partial.** Coverage is unknown, which is not the same as empty (S12) |
| A read returns an empty set | Report as "read succeeded, zero rows" or "read unavailable" — never as a measured zero unless the platform distinguished them |

Degraded outcomes set `status` and populate `unmet_requirements`. This skill fails loudly rather than
filling gaps with defaults.
