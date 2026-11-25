---
name: refactoring-expert
description: Expert skill for Clean Code, Refactoring, and Design Patterns. Combines Refactoring Guru's deep patterns with Supercent's rigorous operational metrics and validation workflows.
version: 1.1.0
keywords: [clean-code, refactoring, design-patterns, solid, code-smells, software-architecture, metrics, validation]
---

# refactoring-expert 🛠

> Keyword: refactoring | Platforms: gemini,claude,codex

High-Performance Refactoring Expert Skill - A fusion of **Refactoring Guru's** architectural patterns and **Supercent's** rigorous operational discipline.

## 🎯 Core Mandates (Strict Constraints)

- **Test-First:** Mandatory to verify or write tests *before* any code transformation. No tests = No refactor.
- **Behavior Preservation:** Absolute prohibition on functional changes. Same input → same output.
- **Atomic Steps:** One transformation at a time (e.g., Extract Method only). Do not mix refactoring with feature additions or bug fixes.
- **Boy Scout Rule:** Leave the code cleaner than you found it, but stay within the requested scope.
- **Quantitative Constraints:**
    - **Methods:** Max 20 lines of code.
    - **Parameters:** Max 3 parameters per method.
    - **Nesting:** Max 2 levels of indentation (if/for/while).
    - **Complexity:** Proactively simplify "Arrow Code."

---

## 🛠 Refactoring & Design Domains

### 1. Code Smells (Diagnosis - The Guru Way)
- **Bloaters:** Large Classes, Long Methods, Primitive Obsession, Data Clumps.
- **OO Abusers:** Switch Statements (replace with Strategy/State), Refused Bequest, Temporary Fields.
- **Change Preventers:** Divergent Change, Shotgun Surgery.
- **Dispensables:** Dead Code, Duplicate Code, Speculative Generality.

### 2. Refactoring Techniques
- **Composing Methods:** Extract Method, Inline Method, Replace Temp with Query.
- **Moving Features:** Move Method, Move Field, Extract Class, Hide Delegate.
- **Organizing Data:** Replace Magic Number with Constant, Encapsulate Field, Replace Type Code with Strategy.
- **Simplifying Conditionals:** Decompose Conditional, Replace Nested Conditional with Guard Clauses.

### 3. Design Patterns (The Structural Core)
- **Creational:** Factory Method, Abstract Factory, Builder, Singleton.
- **Structural:** Adapter, Bridge, Composite, Decorator, Facade, Proxy.
- **Behavioral:** Command, Observer, State, Strategy, Template Method, Visitor.

---

## 🔄 Operational Workflow (The Supercent Way)

### Phase A: Understand & Map
1.  **Analyze Behavior:** Document inputs, outputs, invariants, and dependencies.
2.  **Verify Tests:** Ensure current tests are green. Create a reproduction test if logic is complex.

### Phase B: Validate & Execute
1.  **Transform:** Apply atomic changes.
2.  **Verify Shell:** Run build/test commands (e.g., `mvn test`, `bazel test`).
3.  **Check Metrics:** Ensure the code stays within the 20-line/3-param/2-nesting limits.

### Phase C: Standardized Output (The Summary)
After every refactoring task, provide a summary using this format:

```markdown
### 🛠 Refactoring Summary
- **Pattern Applied:** [e.g., Strategy Pattern]
- **Smell Removed:** [e.g., Long Switch Statement]
- **Metrics Improved:** [e.g., Method lines: 45 -> 12, Nesting: 4 -> 1]
- **Verification:** [e.g., All 15 tests passed, checkstyle clear]
```

---

## 🌐 Knowledge Sources & Deep Dives

> **Directive:** If you encounter a complex smell or need a specific pattern implementation, use `web_fetch` on these sources.

- **Refactoring Guru:** [Techniques & Patterns](https://refactoring.guru/refactoring) - The primary catalog.
- **SOLID Principles:** [Design Patterns Foundation](https://refactoring.guru/design-patterns/solid) - S.O.L.I.D. rules.
- **Coding Standards:** [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) - Formatting rules.
- **Advanced Strategy:** [Supercent Refactoring Template](https://github.com/supercent-io/skills-template/blob/main/.agent-skills/code-refactoring/SKILL.md) - Operational guidelines.

## Skill Interoperability

The **refactoring-expert** 🛠 skill provides the quality gate for:
- **java-expert** ☕: Enforces Clean Code and Style on Java primitives.
- **quarkus-expert** ⚡: Refactors CDI and Reactive patterns (Mutiny).
- **rules-quarkus** 🔧: Modularizes build logic and macros.
