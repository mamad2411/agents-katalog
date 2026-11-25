---
name: logic
description: "Propositional logic, first-order predicate calculus, completeness, compactness, Gödel's incompleteness theorems, and model theory"
category: mathematics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mathematics/logic/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Logic

## Scope
Mathematical logic investigates formal systems, deductive reasoning, valid inference, truth values, and the expressive limits of formal languages.

## Formulations & Metatheory
- **Propositional & First-Order Logic (FOL)**: Syntax (terms, formulas, quantifiers $\forall, \exists$), semantics (models, valuations, satisfaction $\models$).
- **Gödel's Completeness Theorem**: In FOL, syntactic provability coincides with semantic truth: $\Gamma \vdash \phi \iff \Gamma \models \phi$.
- **Gödel's Incompleteness Theorems**:
  1. Any consistent formal system capable of arithmetic is incomplete (contains true but unprovable statements).
  2. Such a system cannot prove its own consistency.

## Tools & References
- **Software**: Z3 (SMT solver), Coq, Lean, Isabelle.
- **Canonical References**: Enderton — *A Mathematical Introduction to Logic*; Mendelson — *Introduction to Mathematical Logic*.
