---
name: arena
description: Multi-candidate exploration and trait-grafting protocol (/arena). Generates 2-3 genuinely distinct designs or prototypes, scores them on an explicit rubric, and grafts winning traits cleanly.
---

# Arena: Parallel Candidate Exploration & Grafting (`/arena`)

> **Role**: Principal Design & Algorithm Evaluator  
> **Philosophy**: *Never settle for your first plausible draft on a hard problem. Exhaust the design space with competing shapes, score with evidence, and graft only what earns its place.*

This skill implements `Exhaust the Design Space` for high-stakes UI compositions, tricky algorithms, data pipelines, and architectural refactors.

---

## 1. Quick Navigation & References

| Resource | Purpose |
| :--- | :--- |
| [references/candidate-scoring-and-grafting.md](references/candidate-scoring-and-grafting.md) | Weighted evaluation rubrics, prototype isolation rules, and anti-Frankenstein grafting checks. |

---

## 2. When to Invoke `/arena`
- **No Clear Precedent**: Novel interaction, mascot choreography, or layout grammar where generic defaults risk AI slop.
- **Competing Trade-Offs**: Memory vs throughput, IndexedDB vs OPFS, SSR vs client worker, state machine vs reducer.
- **High Blast Radius**: Core API or schema refactor affecting 5+ modules.
- *Do NOT invoke* for routine CRUD, obvious bug fixes, or single-line edits (`Laziness Protocol`).

---

## 3. The 4-Step Arena Protocol

1. **Define Orthogonal Axes**: Create 2–3 genuinely distinct candidates (different data structures, layout hierarchies, or execution models — never superficial variable renames).
2. **Prototype or Sketch Independently**:
   - For algorithm/runtime forks: write isolated 20–50 line probes in `scratch/` and benchmark on identical inputs.
   - For architecture/UI forks: emit compact shape specs (types + layout tree + failure modes).
3. **Score on Explicit Weighted Rubric**:
   - **Correctness & Edge-Case Safety** (30%)
   - **Simplicity & Reader Load** (25%)
   - **Performance / Token / Frame Budget** (25%)
   - **Reversibility & Blast Radius** (20%)
4. **Select Winner & Graft**:
   - Pick the single cleanest base architecture.
   - Graft at most 1–2 specific superior mechanisms from runner-ups only if they integrate naturally without extra wrapper layers.
   - Delete losing probe files before committing.
