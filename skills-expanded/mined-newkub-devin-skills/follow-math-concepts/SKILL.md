---
name: follow-math-concepts
description: Mathematics handbook for software development
argument-hint: "[topic]"
related:
  - deep-research
  - report-math-equation
  - explain
  - learn
  - follow-lib-fast-check
  - ask-me
  - deep-debug
  - deep-review-codebase
  - follow-context-engineering
  - follow-best-practice
  - report-slides
---

## Goal

Help the user understand and apply mathematics in software development

## Scope

Use for general concepts: logic, sets, boolean algebra, combinatorics, graphs, algorithm complexity, discrete math, calculus, probability, statistics, markov chains, queueing theory, reliability, automata/formal languages, order/lattice, category theory, game theory, information theory, linear algebra, optimization, numerical methods, cryptography, proofs — each topic lives in `references/<topic>.md`

## Execute

### 1. Select Topic

> Goal: know which area of math to use

1. Take the `topic` from the argument or context
2. If not specified, look at the topics table below and ask the user with `/ask-me`
3. Pick and read the matching `references/<topic>.md`, then follow its `## Execute`
4. For overall sources and references, see [references/math-resources.md](references/math-resources.md)

| No. | Topic | Reference |
|-----|-------|-----------|
| 1 | propositional-logic | [references/propositional-logic.md](references/propositional-logic.md) |
| 2 | predicate-logic | [references/predicate-logic.md](references/predicate-logic.md) |
| 3 | set-theory | [references/set-theory.md](references/set-theory.md) |
| 4 | boolean-algebra | [references/boolean-algebra.md](references/boolean-algebra.md) |
| 5 | combinatorics | [references/combinatorics.md](references/combinatorics.md) |
| 6 | graph-theory | [references/graph-theory.md](references/graph-theory.md) |
| 7 | algorithm-complexity | [references/algorithm-complexity.md](references/algorithm-complexity.md) |
| 8 | discrete-math | [references/discrete-math.md](references/discrete-math.md) |
| 9 | category-theory | [references/category-theory.md](references/category-theory.md) |
| 10 | game-theory | [references/game-theory.md](references/game-theory.md) |
| 11 | information-theory | [references/information-theory.md](references/information-theory.md) |
| 12 | linear-algebra | [references/linear-algebra.md](references/linear-algebra.md) |
| 13 | optimization | [references/optimization.md](references/optimization.md) |
| 14 | numerical-methods | [references/numerical-methods.md](references/numerical-methods.md) |
| 15 | cryptography | [references/cryptography.md](references/cryptography.md) |
| 16 | probability | [references/probability.md](references/probability.md) |
| 17 | statistics | [references/statistics.md](references/statistics.md) |
| 18 | proofs | [references/proofs.md](references/proofs.md) |
| 19 | calculus | [references/calculus.md](references/calculus.md) |
| 20 | automata-formal-languages | [references/automata-formal-languages.md](references/automata-formal-languages.md) |
| 21 | markov-chains | [references/markov-chains.md](references/markov-chains.md) |
| 22 | queueing-theory | [references/queueing-theory.md](references/queueing-theory.md) |
| 23 | reliability-math | [references/reliability-math.md](references/reliability-math.md) |
| 24 | order-lattice-theory | [references/order-lattice-theory.md](references/order-lattice-theory.md) |

### 2. Apply Mathematics

> Goal: apply math to the problem

1. Identify the domain to solve for, then pick suitable concepts from `references/<topic>.md`
2. Build an example or model per the concepts and test its correctness, following `/follow-best-practice`
3. Cite trustworthy sources and use `/deep-review-codebase` to check the result when needed
4. If more sources are needed → use `/deep-research` or `/learn`

## Rules

- Use English for explanations
- Give clear, practically usable examples
- Cite trustworthy sources
- Keep the content current with the latest versions
- Use `/follow-context-engineering` for long-horizon tasks
- Follow `/follow-best-practice` when needed
- Apply math in triage: use probability/Bayes to rank root causes alongside `/deep-debug` `### 3. Triage Incident`

### 5. Cross Skills

- Use `/report-math-equation`, `/explain`, `/follow-lib-fast-check`, `/report-slides` per the problem's context

## Expected Outcome

- Understand discrete mathematics for algorithms
- Able to use linear algebra in ML and graphics
- Able to apply information theory
- Able to analyze algorithm complexity
