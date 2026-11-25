---
name: ask-data-skills
description: Ask which data-engineering skill or flow fits your situation. A router over this suite, the data fork of the stock engineering skills.
disable-model-invocation: true
---

# Ask Data Skills

You don't remember every skill, so ask. This suite reworks the stock engineering skills for data work and extends them to the dashboard. If you also have the stock suite installed: stock routes software repos, this suite routes data repos, and the same-name inner-loop forks (`tdd`, `implement`, `diagnosing-bugs`, `prototype`, `codebase-design`, `improve-codebase-architecture`) ship as project-scoped copies inside your data repo, so software repos keep stock behavior. `/ask-matt` still routes the stock suite; this file routes this one.

## The main flow: idea → shipped data product

1. **`/grill-with-docs`** (stock): sharpen the idea by interview. It's stateful, retaining what it learns in `CONTEXT.md` and ADRs. No repo? `/grill-me`.
2. **Branch: does a question need a runnable answer?** (does this grain hold, what should the mart expose, what does the surface look like) → detour through **`/prototype`** (fork): materialize → inspect rows → amend fixture → re-run, in a scratch schema, bridged by `/handoff` in both directions. Throwaway from day one: keep the answer, delete the models.
3. **Branch: multi-session build?**
   - **Yes** → **`/to-pipeline-spec`**, where the checkpoint pins grain, oracle, and tolerance per seam, and the spec carries a source-to-target mapping. Then **`/to-tickets`** (stock, with the data-slicing layer: a vertical slice is one thin source→mart flow; backfill tickets are first-class; blocking edges follow the DAG). Then **`/implement`** per ticket, clearing context between.
   - **No** → **`/implement`** right here.

   `/implement` drives **`/tdd`** internally across two planes (mock-input unit tests drive red-green; data tests audit live data and never drive the loop), produces the **data diff** against production (row counts, schema, values, freshness columns), and closes with **`/data-review`** on three axes: Standards, Spec, and **Impact** (blast radius, contract breaks, destructive writes, cost, the data diff).
4. **The last mile, when the mart feeds people and not just queries:**
   - **`/to-dashboard-spec`**: the checkpoint pins the dashboard contract: audience and type, metric map (each metric's named source of truth), freshness SLA, control map, logic placement.
   - **`/dashboard-build`**: contract gate first (the feeding models must carry grain, source-anchored freshness columns, and dimension-parity assertions; gaps file upstream, never patched in the BI tool), then a thin build, then a mandatory review handoff.
   - **`/dashboard-review`**: rubric review plus source tie-out; ship only on an approving verdict.

## On-ramps

- **Data incidents piling up** → **`/triage`** (stock, with the data-incident layer: data/code/ops classification, blast-radius severity, pinned-evidence verification before anything is banked).
- **Someone reports a wrong number** → **`/data-qa`**. Reproduce and pin first: the pinned query (time travel / snapshot, as-of timestamp) IS the repro; then file.
- **Something's broken and resists a first glance** → **`/diagnosing-bugs`** (fork). Pin the evidence before reasoning from it (production mutates mid-diagnosis), walk lineage to the most-upstream exhibiting node, fix at the seam, then **backfill down**.

## Codebase health

- **`/improve-codebase-architecture`** (fork-lite): walk the DAG, not the directory tree; surfaces deepening candidates (pass-through stacks, grain-mixing models, source-seam leaks). Picking one generates an idea for the main flow.

## Vocabulary underneath

- **`/codebase-design`** (fork): the deep-module vocabulary, data edition: an interface is a name plus a **declared grain**, column contract, null and sentinel semantics, freshness expectations, and cost obligations.
- **`/domain-modeling`** (stock, with the data layer): glossary entries carry grain; metrics are first-class terms; two dashboards disagreeing on "revenue" is a glossary failure before it is a pipeline failure.
- **Layer canons**: docs, not skills, wired via your repo's `## Agent skills` block: data-slicing, data-incident-triage, data-domain-modeling, data-interface-canon (the five-paradigm design menu), warehouse-architecture-canon, warehouse-guardrails.

## Crossing sessions

Same as stock: `/handoff` forks to a fresh session via a markdown bridge; `/compact` continues in place. The data twist: after any gap, re-pin before resuming a diagnosis, because the tables moved while you were away.

## Standalone

- **`/design-an-interface`** (shipped by this suite, plus the data-interface canon): five modeling paradigms explored in parallel: one big table, dimensional star, snapshot, semantic layer, consumer-defined contract. Grain first, always. Upstream retired this skill in v1.2.0; the suite vendored it, so it installs from here.
- **`/setup-pre-commit-data`**: static-only commit gates for SQL repos: lint, config hygiene, a destructive-SQL tripwire. Tests belong in CI, not the commit hook.

## Precondition

**`/setup-data-skills`**: run before the first flow in a data repo. It scaffolds the config the suite reads: issue tracker, triage labels, domain docs, warehouse write-safety rails, data-quality registry, and the dashboards config (including an optional pointer to your org's dashboard guidance: rubric, style guide, brand palette). The skills resolve their org specifics through those files; without them the abstract verbs dangle.
