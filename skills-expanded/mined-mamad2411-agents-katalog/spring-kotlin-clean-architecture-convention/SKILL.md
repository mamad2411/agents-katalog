---
name: spring-kotlin-clean-architecture-convention
description: >
  Guides writing and structuring Spring + Kotlin code following Hexagonal Architecture principles.
  ALWAYS activate when the user uses any of these phrases:
  "hexagonal", "clean architecture", "port", "adapter", "use case", "dependency rule",
  "클린 아키텍처", "헥사고날", "포트", "어댑터", "유스케이스", "의존성 방향", "레이어 구조",
  "도메인 분리", "아키텍처 맞게", "패키지 구조".
  Covers package structure, dependency rules, domain purity, use case pattern, and adapter conventions.
  Works alongside spring-kotlin-clean-code-convention (which handles code-level rules).
---

# Spring Kotlin Clean Architecture Convention

Apply Hexagonal Architecture principles when writing or structuring Spring + Kotlin code.
Load the relevant reference files and follow their guidelines.

## Package Structure

```
adapter/
  in/              ← Driving adapters (Controllers)
  out/
    infra/         ← Driven adapters (JPA persistence)
    api/           ← Driven adapters (External API clients)
application/
  service/         ← Use case implementations
  util/
domain/
  model/           ← Entities, Value Objects
  port/
    in/            ← Input port interfaces (use cases)
    out/           ← Output port interfaces (repositories, clients)
```

## Dependency Rule

```
adapter → application → domain
```

Dependencies point **inward only**. Domain knows nothing about adapters or Spring.

## Principles

| # | Area | Reference |
|---|------|-----------|
| 1 | Package structure & dependency rules | `references/package-structure.md` |
| 2 | Domain layer (purity, Entity, VO) | `references/domain-layer.md` |
| 3 | Application layer (UseCase, Ports) | `references/application-layer.md` |
| 4 | Adapter layer (In/Out, naming) | `references/adapter-layer.md` |

Load all 4 reference files when writing or structuring from scratch.
Load only the relevant one for targeted questions (e.g., "도메인 어떻게 짜?" → `references/domain-layer.md`).
