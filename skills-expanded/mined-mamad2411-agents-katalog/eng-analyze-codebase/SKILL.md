---
name: eng-analyze-codebase
description: Analyze codebase architecture, directory topology, design patterns, and dependency graphs. Use when onboarding, planning refactorings, auditing architecture, or evaluating project structure.
---

# Analyze Codebase

Perform multi-angle architectural and code pattern inspection across a codebase. Supports both quick structural scans and deep dependency audits.

## Analysis Modes

- **Quick Scan (`quick`)**: Directory hierarchy, framework identification, layering patterns (MVC, Clean Architecture, etc.), and key module responsibilities.
- **Deep Audit (`deep`)**: Module dependency graph, circular dependency detection, internal design patterns, anti-pattern scan, and dead code indicators.

---

## Process

### 1. Topology & Manifest Discovery
1. Map directory structure up to depth 3, ignoring build outputs (`node_modules`, `dist`, `target`, `__pycache__`, `.git`).
2. Read project manifests (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `pom.xml`).
3. Identify language versions, major frameworks, and package dependencies.

### 2. Architecture & Layering Inspection
1. Determine architecture style (Modular Monolith, Clean/Hexagonal, Layered MVC, Microservices/Multi-package).
2. Trace request/data flow through entry points (controllers $\rightarrow$ services $\rightarrow$ data access).
3. Check boundary enforcement and cross-cutting concerns (auth, logging, error handling).

### 3. Deep Code Patterns & Dependency Health
1. Search for recurring design patterns across services, models, and repositories.
2. Detect circular dependencies or tight coupling between modules.
3. Identify anti-patterns (e.g. monolithic utility files, hidden global state, duplicate abstractions).

---

## Output Report Structure

```markdown
# Codebase Analysis Report

## 1. Executive Summary
- **Primary Tech Stack**: <Languages, Frameworks, Runtimes>
- **Architecture Paradigm**: <e.g. Clean Architecture / Modular Monolith>
- **Health Score**: #/10

## 2. Directory & Module Breakdown
| Directory / Package | Responsibility | Key Technologies |
|---|---|---|
| `src/core` | Core business models & rules | Pure TypeScript |
| `src/api` | REST/GraphQL controllers | Express / NestJS |

## 3. Dependency Graph & Coupling
- **Layer Flow**: `api` $\rightarrow$ `services` $\rightarrow$ `database`
- **Coupling Issues**: <Circular dependencies or leaky abstractions if found>

## 4. Observed Conventions & Patterns
- **Naming Conventions**: PascalCase types, camelCase functions
- **Error Handling Strategy**: Result pattern / Custom domain exceptions
- **Testing Approach**: Co-located unit tests + dedicated integration tests

## 5. Architectural Recommendations
1. Actionable improvement 1
2. Actionable improvement 2
```

---

## Checkable Completion Criteria

- [ ] Directory topology mapped to depth 3 with build outputs excluded.
- [ ] Architecture paradigm, tech stack, and health score stated in the report.
- [ ] Dependency graph traced with circular dependencies and coupling issues flagged.
- [ ] Recommendations are actionable improvements tied to observed evidence, not generic advice.
