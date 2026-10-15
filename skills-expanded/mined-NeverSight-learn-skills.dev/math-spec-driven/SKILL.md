---
name: math-spec-driven
description: Produces rigorous, unambiguous mathematical specifications using sets, functions, relations, invariants, and explicit edge-case handling. Use when requirements are ambiguous, systems have interacting constraints, or behavior/contracts must be precise and falsifiable.
metadata:
  version: "1.0.0"
---

# Math Spec-Driven Skill

## Purpose

Use this skill whenever a task requires **rigorous, unambiguous specification** of a system, process, relationship, or transformation. Mathematical specification is a methodology — not a subject. It applies whenever precision, completeness, and falsifiability matter more than narrative approximation.

This skill teaches Claude to think in **mathematical structures**: sets, functions, relations, invariants, and formal constraints. It is domain-agnostic. The formalism is the tool; the domain is whatever the user brings.

---

## Core Philosophy

Mathematics is simultaneously:
- A **system** (self-consistent, closed under its own rules)
- A **language** (capable of expressing any precisely definable concept)
- A **specification method** (the most unambiguous way to define what something IS and what it must DO)

When applied as a specification methodology, mathematics forces three things:
1. **Explicitness** — every assumption must be stated
2. **Composability** — every component can be independently verified then combined
3. **Falsifiability** — every claim is either provable or disprovable within the system

---

## When to Apply This Skill

Trigger this skill when you encounter:
- Ambiguous requirements that need precise boundaries
- Systems with many interacting parts that must remain consistent
- Transformations where the input/output relationship must be guaranteed
- Constraints that must hold under all conditions (invariants)
- Decisions that need justification beyond intuition or convention
- Any domain where "it depends" is not an acceptable specification

---

## The Math Spec Method

### Step 1 — Model the Domain

Map the real-world problem onto mathematical primitives:

| Real World | Mathematical Primitive |
|---|---|
| A collection of things | Set `S` |
| A thing with properties | Tuple or Record `(a, b, c)` |
| A process or transformation | Function `f: A → B` |
| A relationship between things | Relation `R ⊆ A × B` |
| A constraint that must always hold | Invariant / Predicate `P(x): Bool` |
| A sequence of states | Trace `[s₀, s₁, …, sₙ]` |
| A measurement | Metric `d: S × S → ℝ≥0` |

**Task:** Before writing any specification, identify which primitives apply. Name them explicitly.

---

### Step 2 — Define the Universe of Discourse

Before specifying behavior, define what EXISTS in the system:
```
Let U = the universe of all valid entities in this domain
Let S ⊆ U = the subset currently under consideration
Let ∅ = the empty/null case (always handle this explicitly)
```

Ask:
- What are the atomic elements? (Cannot be decomposed further)
- What are the compound elements? (Defined in terms of atoms)
- What is explicitly excluded?

---

### Step 3 — Specify Functions and Transformations

Every transformation has a **signature** and a **contract**:
```
f: A → B

Precondition:  P(a) must hold before f is applied
Postcondition: Q(f(a)) must hold after f is applied
Invariant:     I(a) = I(f(a))  [what must NOT change]
```

Write specs in this form even in prose-heavy domains. Example:
```
classify: Document → Category

Pre:  Document is non-empty, language is detected
Post: Category ∈ {defined_taxonomy}
Inv:  Document content is unchanged by classification
```

---

### Step 4 — State Invariants Explicitly

Invariants are properties that must hold at ALL times, not just at some steps.

For each invariant, state:
- **What it asserts** (the property)
- **When it must hold** (always / at boundaries / after each operation)
- **What violates it** (the failure mode)

Pattern:
```
∀ x ∈ S: P(x)           — Universal invariant
∃ x ∈ S: P(x)           — Existence guarantee
P(x) ⟹ Q(f(x))          — Conditional guarantee
¬(P(x) ∧ Q(x))          — Mutual exclusion
```

---

### Step 5 — Handle Edge Cases as First-Class Concerns

Mathematical completeness requires handling the boundary:
- The empty set (`S = ∅`)
- The singleton (`|S| = 1`)
- The degenerate input (zero, negative, infinite, null)
- The identity case (`f(x) = x`)
- The composition case (`f(g(x))` — does order matter?)

Never specify only the "happy path." A spec is incomplete if it omits boundary behavior.

---

### Step 6 — Compose and Verify

Once individual components are specified, compose them:
```
h = f ∘ g   (h(x) = f(g(x)))

Verify:
  - Codomain of g matches domain of f
  - Preconditions of f are implied by postconditions of g
  - Invariants of both f and g are preserved by h
```

If composition breaks: the specification has a gap. Find and fill it.

---

### Step 7 — Express Uncertainty with Precision

Where things are probabilistic or unknown, apply the right formalism:
```
P(outcome | evidence)     — conditional probability
E[X]                      — expected value
Var(X)                    — variance / spread
argmax_{x} f(x)           — best choice under a criterion
```

Uncertainty does not mean imprecision — it means quantified imprecision.

---

## Output Format

When producing a mathematical specification, always structure output as:
```
## Specification: [Name]

### 1. Domain Model
[Named sets, types, and primitives]

### 2. Functions / Operations
[Signatures, preconditions, postconditions, invariants]

### 3. Invariants
[Formal or semi-formal statements of what must always hold]

### 4. Edge Cases
[Explicit boundary conditions and their specified behavior]

### 5. Composition / Interaction
[How components combine; verification that composition is sound]

### 6. Open Questions
[What is explicitly left unspecified and why]
```

---

## Notation Guide (Use Consistently)

| Symbol | Meaning |
|---|---|
| `∀` | For all |
| `∃` | There exists |
| `∈` | Is a member of |
| `⊆` | Is a subset of |
| `∅` | Empty set |
| `→` | Function mapping (A → B) |
| `⟹` | Logical implication |
| `⟺` | If and only if |
| `∧` | Logical AND |
| `∨` | Logical OR |
| `¬` | Logical NOT |
| `∘` | Function composition |
| `≜` | Defined as |
| `|S|` | Cardinality of set S |
| `⊥` | Undefined / bottom (error state) |

Always define any non-standard notation locally.

---

## Example (Illustrative — Domain is Arbitrary)

**Task:** Specify a content routing system.
*(Domain could be emails, support tickets, API calls, documents — the structure is what matters.)*
```
## Specification: Content Router

### 1. Domain Model
Let M = set of all incoming messages (finite, non-empty)
Let C = {c₁, c₂, …, cₙ} = finite set of destination categories
Let R = set of routing rules, where each r ∈ R is a predicate r: M → Bool
Let priority: R → ℕ = total ordering on rules (lower = higher priority)

### 2. Functions / Operations

route: M → C ∪ {⊥}

Pre:  m ∈ M, |R| ≥ 1
Post: 
  If ∃ r ∈ R such that r(m) = true:
    route(m) = category associated with highest-priority matching r
  Else:
    route(m) = ⊥  [unrouted — must trigger fallback handler]
Inv:  m is not modified by route(m)

### 3. Invariants
∀ m ∈ M: route(m) is deterministic (same input → same output)
∀ m ∈ M: at most one category is assigned (no split routing)
If route(m) = ⊥, an alert must be emitted

### 4. Edge Cases
M = ∅        → route is never called; system is idle (valid state)
R = ∅        → route(m) = ⊥ for all m (all messages unrouted)
|C| = 1      → route(m) = c₁ for all matched m (trivial routing)
Two rules match → highest priority(r) wins; tie-break by rule index

### 5. Composition
filter ∘ route:
  filter: M → M' removes malformed messages before routing
  Pre of route is satisfied by Post of filter
  Composition valid iff filter guarantees m' ∈ M for all outputs

### 6. Open Questions
- How are rules added/removed at runtime? (Mutation spec not defined here)
- What is the SLA on route latency? (Performance spec out of scope)
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|---|---|---|
| "It should handle all cases" | Not falsifiable — not a spec | List every case explicitly |
| "Usually returns X" | Probabilistic without quantification | State P(returns X) or define when it doesn't |
| Defining only the happy path | Collapses on edge cases | Always specify ∅, ⊥, and boundary inputs |
| Natural language for constraints | Ambiguous, multi-interpretable | Restate as predicate logic or structured form |
| Composing without domain/codomain check | Silent type errors at system boundaries | Verify f ∘ g explicitly before combining |

---

## Quality Checklist

Before delivering any math-spec-driven output, verify:

- [ ] Every set is named and defined
- [ ] Every function has a signature (domain → codomain)
- [ ] Every function has preconditions and postconditions
- [ ] At least one invariant is stated
- [ ] Edge cases (∅, ⊥, boundary) are explicitly handled
- [ ] Compositions are verified for domain/codomain alignment
- [ ] Open questions are listed — not silently omitted
- [ ] Notation is consistent throughout
