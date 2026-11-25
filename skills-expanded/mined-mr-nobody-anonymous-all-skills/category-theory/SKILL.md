---
name: category-theory
description: "Categories, functors, natural transformations, limits, colimits, adjunctions, monads, and yoneda lemma"
category: mathematics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mathematics/category-theory/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Category Theory

## Scope
Category theory formalizes mathematical structure and systems of relationships, unifying concepts across algebra, topology, geometry, and computer science.

## Core Concepts
- **Category $\mathcal{C}$**: Objects $\operatorname{Ob}(\mathcal{C})$ and Morphisms $\operatorname{Hom}(A, B)$ satisfying composition and identity laws.
- **Functor $F: \mathcal{C} \to \mathcal{D}$**: Maps objects and morphisms preserving identities and composition.
- **Natural Transformation $\alpha: F \implies G$**: Family of morphisms $\alpha_A$ making diagram commute.
- **Yoneda Lemma**: Natural transformations $\operatorname{Nat}(\operatorname{Hom}(A, -), F) \cong F(A)$.
- **Adjunctions & Monads**: $F \dashv G$; Monad $T = G \circ F$ with unit $\eta$ and multiplication $\mu$.

## Tools & References
- **Canonical References**: Mac Lane — *Categories for the Working Mathematician*; Awodey — *Category Theory*.
