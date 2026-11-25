---
name: game-theory
description: "Nash equilibrium, strategic and extensive form games, zero-sum games, cooperative games, Shapley value, and mechanism design"
category: mathematics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mathematics/game-theory/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Game Theory

## Scope
Game theory mathematically models strategic interaction among rational agents, finding equilibria in cooperative and non-cooperative contexts.

## Core Formulations
- **Nash Equilibrium**: Strategy profile $(s_1^*, \dots, s_n^*)$ such that no player can unilaterally deviate to increase their payoff:
  $$u_i(s_i^*, s_{-i}^*) \ge u_i(s_i, s_{-i}^*) \quad \forall s_i \in S_i$$
- **Minimax Theorem (von Neumann)**: In zero-sum games, $\max_{x} \min_{y} x^T A y = \min_{y} \max_{x} x^T A y$.
- **Shapley Value (Cooperative)**: Fair distribution of surplus among players based on marginal contributions.

## Tools & References
- **Software**: Gambit, Axelrod (Python).
- **Canonical References**: Gibbons — *Game Theory for Applied Economists*; Osborne & Rubinstein — *A Course in Game Theory*.
