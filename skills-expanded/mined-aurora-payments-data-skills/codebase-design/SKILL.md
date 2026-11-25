---
name: codebase-design
description: Shared vocabulary for designing deep data models. Use when the user wants to design a mart or a model's interface, declare a grain, decide which layer owns a transformation, choose between star schema and one big table, deepen a sprawling DAG, make models contracted or testable, or when another skill needs the deep-module vocabulary.
---

# Codebase Design

Design **deep modules**: a lot of modeling behind a small interface, placed at a clean seam, testable through that interface. Use this language and these principles wherever data is being modeled or restructured. The aim is leverage for consumers, locality for maintainers, and testability for everyone.

## Glossary

Use these terms exactly: don't substitute "table," "dataset," "schema," "pipeline," or "boundary." Consistent language is the whole point.

**Module**: anything with an interface and an implementation. Deliberately scale-agnostic: a single model, a mart plus the staging and intermediate models that feed it, or a whole project exposing public models. _Avoid_: table, dataset, job (they name storage or execution, not the design unit).

**Interface**: everything a consumer must know to query the module correctly: the name and the **declared grain**, but also column names and types, contract constraints, null and sentinel semantics, freshness expectations, and cost obligations (the partition or cluster column a consumer must filter on). _Avoid_: schema, DDL (too narrow, since they cover only the column-level surface).

**Grain**: the unit-of-one-row declaration: "one row per order," "one row per customer per day." It is the load-bearing invariant of an interface, because every join, test, and aggregation depends on it, so declare it before choosing columns. A mart without a declared grain cannot be tested or safely joined against. _Avoid_: granularity, level of detail (descriptions, not declarations).

**Contract**: the machine-checked subset of the interface: names, types, and constraints the build fails on when breached (dbt ≥1.5). Constraints enforce only where the platform supports them; BigQuery primary and foreign keys are metadata, not enforced. A contract is not the interface, since grain, semantics, and freshness live outside it, but every public interface deserves one. For exposure-facing models, meaning anything a registered dashboard reads, the freshness fields (latest business period, source load time) belong inside the contract: the surface reports them to end users, so they are part of the machine-checked interface. _Avoid_: schema check.

**Implementation**: what's upstream of a module's interface: the joins, dedup, unioning, re-graining, and history handling that produce it. Distinct from **Adapter**: a thing can be a small adapter with a large implementation (a staging model taming a messy vendor feed) or a large adapter with a small implementation (a fixture standing in for a source). Reach for "adapter" when the seam is the topic; "implementation" otherwise.

**Depth**: leverage at the interface: the amount of modeling a consumer (or test) gets per obligation they take on. A module is **deep** when joins, dedup, and history handling sit behind one entity-grained table, **shallow** when the consumer must know nearly as much as the implementation does: which models to join, which duplicates to filter, which rows to trust. Width is not shallowness: a 200-column table with one grain and zero join obligations is a small interface.

**Seam** _(Michael Feathers)_: a place where you can alter behaviour without editing in that place; the *location* at which a module's interface lives. In a warehouse, seams sit at the layer boundaries (source to staging, staging to marts, marts to BI) and at project boundaries, where only public models cross. Where to put the seam is its own design decision, distinct from what goes behind it. _Avoid_: boundary (overloaded with DDD's bounded context).

**Adapter**: a concrete thing that satisfies an interface at a seam. Describes *role* (what slot it fills), not substance (what's inside). The canonical warehouse adapter is a staging model: one per source table, conforming that source to the shared shape.

**Leverage**: what consumers get from depth: more analysis per unit of interface they learn. One modeled entity pays back across N dashboards, notebooks, and agents, and M tests.

**Locality**: what maintainers get from depth: change, bugs, backfills, and verification concentrate in one model rather than spreading across consumers. Fix the dedup once, every downstream number moves together.

## Deep vs shallow

**Deep module** = small interface + lots of implementation:

```
┌─────────────────────┐
│   Small Interface   │  ← One entity, one declared grain
├─────────────────────┤
│                     │
│  Deep Implementation│  ← Joins, dedup, history hidden
│                     │
└─────────────────────┘
```

**Shallow module** = large interface + little implementation (avoid):

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Consumer must know joins, filters, caveats
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just renames a source
└─────────────────────────────────┘
```

When designing an interface, ask:

- Can I reduce the number of models a consumer must touch?
- Can I collapse to one declared grain?
- Can I hide more of the joins, dedup, and history upstream?

**Sanctioned shallowness.** Staging models are shallow by design: one per source table, renaming and casting only, with no joins or aggregations. That is the conformance adapter at the source seam, not a design failure. The shallowness to hunt lives downstream: marts that re-select an intermediate, near-duplicate marts forked per team, intermediate sprawl a consumer must reassemble.

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can be internally composed of small, testable, swappable models; they just aren't part of the interface. Intermediate models are typically **internal seams**: private to the implementation, used by its own tests, never exposed in the production schema. The **external seam** is the module's contracted surface: a mart, or a project's public models.
- **The deletion test.** Imagine deleting the model. If complexity vanishes, it was a pass-through. If the joins and dedup reappear across N downstream marts, it was earning its keep.
- **The interface is the test surface.** Consumers and tests cross the same seam: uniqueness at the declared grain, contracted names and types, the sums a consumer would reconcile. If you want to test *past* the interface, asserting on hidden intermediate state, the module is probably the wrong shape.
- **One adapter means a hypothetical seam. Two adapters means a real one.** Don't build a conformance interface for a second source that doesn't exist yet. A second source, or a fixture standing in for one, is the second adapter. A single-adapter seam is just indirection. Intermediate promotion answers to the deletion test, not adapter counting: don't split an intermediate out of a mart until its logic would reappear across more than one downstream consumer.

## Designing for testability

Good interfaces make testing natural:

1. **Reference upstreams, don't hard-code them.**

   ```sql
   -- Testable: the upstream is injected, so environments and
   -- unit-test fixtures can substitute it
   select order_id, ordered_at from {{ ref('stg_shop__orders') }}

   -- Hard to test: pinned to one environment, no substitution point
   select order_id, ordered_at from raw_prod.shop.orders
   ```

2. **Overwrite partitions, don't mutate rows.**

   ```sql
   -- Testable: pure and idempotent, re-running a day rebuilds
   -- the same day, byte for byte
   {{ config(
       materialized='incremental',
       incremental_strategy='insert_overwrite',
       partition_by={'field': 'order_date', 'data_type': 'date'}
   ) }}
   select order_id, order_date, total
   from {{ ref('stg_shop__orders') }}

   -- Hard to test: re-running double-applies the change
   update orders
   set total = total - discount
   where order_date = '2026-06-01'
   ```

3. **Small surface area.** One declared grain = one uniqueness test. Fewer consumer obligations = smaller fixtures and simpler expected rows.

## Relationships

- A **Module** has exactly one **Interface** (the surface it presents to consumers and tests).
- An **Interface** declares exactly one **Grain**.
- A **Contract** enforces the machine-checkable part of an **Interface**.
- **Depth** is a property of a **Module**, measured against its **Interface**.
- A **Seam** is where a **Module**'s **Interface** lives.
- An **Adapter** sits at a **Seam** and satisfies the **Interface**.
- **Depth** produces **Leverage** for consumers and **Locality** for maintainers.

## Rejected framings

- **Depth as ratio of implementation-lines to interface-lines** (Ousterhout): rewards padding the implementation. We use depth-as-leverage instead.
- **Depth as column count**: a wide table is not automatically deep, and a narrow one not automatically shallow. Depth is consumer obligations avoided, not columns present.
- **"Interface" as the column list or the DDL**: too narrow, since interface here includes grain, semantics, freshness, and cost, every fact a consumer must know.
- **"Pipeline" as the design unit**: pipelines name execution order, modules name interfaces. Design the module; derive the pipeline.
- **"Boundary"**: overloaded with DDD's bounded context. Say **seam** or **interface**.

## Going deeper

- **Deepening a cluster given its dependencies**: see [DEEPENING.md](DEEPENING.md): dependency categories (in-DAG, owned upstream, source), seam discipline, and replace-don't-layer testing.
- **Exploring alternative interfaces**: see [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md): spin up parallel sub-agents to design the mart several radically different ways (one big table, dimensional star, hybrid, semantic layer) and then compare on depth, locality, and seam placement.
