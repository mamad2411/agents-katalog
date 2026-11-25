---
name: "jpa"
description: "JPA/Hibernate persistence: entity mapping, fetch strategy, transactions, repositories, and avoiding N+1 and proxy pitfalls."
version: 1
created: "2026-06-09T03:34:24+05:30"
updated: "2026-06-26"
---
## When to Use
Use when tsa.technology.database.access = JPA/Hibernate (typically with Spring Data JPA). Activate for ORM-based relational persistence.

## Procedure
1. Map entities with explicit @Id strategy; keep @Column nullability aligned to DB constraints.
2. Default all relationships to FetchType.LAZY; use explicit fetch joins/entity graphs where needed.
3. Use Spring Data repositories per aggregate root; write @Query only when derived queries are insufficient.
4. Annotate read methods @Transactional(readOnly=true) and writes @Transactional.
5. Never expose entities in API responses - map to DTOs (MapStruct).
6. Avoid @Data on entities; implement equals/hashCode on the business key, not the generated id.
7. Detect and fix N+1 with fetch joins, @EntityGraph, or batch fetching.

## Patterns
- LAZY by default + explicit fetch joins
- Repository per aggregate root
- DTO projection (no entities in responses)
- Read-only transactions for queries
- Batch size / entity graph to kill N+1

## Anti-Patterns
- FetchType.EAGER everywhere
- @Data/@ToString on entities (proxy + recursion issues)
- Returning entities from controllers
- Open-session-in-view masking lazy issues
- N+1 queries left unaddressed

## Tool Selection
- Generic: read_file, write_file, command_line, skills
- Intended (roadmap): jpa_mapping_validator, n_plus_one_detector

## Validation Rules
- All relationships LAZY unless justified
- No entity leaks past the service layer
- Read methods are readOnly transactions
- No detectable N+1 on core flows

## RAG Sources
- jakarta-persistence-spec
- hibernate-user-guide
- spring-data-jpa-docs
