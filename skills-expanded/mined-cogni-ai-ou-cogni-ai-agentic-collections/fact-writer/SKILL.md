---
name: fact-writer
description: >-
  Strict guidelines for creating, writing, and maintaining verifiable project
  fact files (e.g., FACTS.md or FACTS.mmd) without contradictions, ensuring
  state compression and lexical ordering.
  You MUST load this skill when managing canonical project fact files.
license: MIT
---
<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->
# Fact Writer

Guidance for structuring and maintaining verifiable project fact files. Use this skill when managing `FACTS.md`,
`FACTS.mmd`, or similar canonical stores.

## WHEN TO USE

- Creating or updating canonical fact stores (e.g., `FACTS.md`, `FACTS.mmd`).
- Documenting verifiable ecosystem properties, constraints, or architectural decisions.
- Resolving state conflicts or contradictions within documentation limits.

## WHEN NOT TO USE

- For writing conversational READMEs or unstructured tutorial documentation (use `docs-writer` instead).
- When recording temporal, ephemeral state like "Build 45 failed" (fact stores are for persistent architectural truths).
- For writing executable code or scripts.

## Common Pitfalls

- **Violating Lexical Order**: Appending a new fact at the bottom of the list instead of inserting it in strict alphabetical order, breaking the state compression logic.
- **Silent Contradictions**: Adding a fact that explicitly contradicts an existing node without explicitly removing or updating the old node.
- **Prose Injection**: Writing long paragraphs of explanation instead of dense, structured nodes.

## Core Process

1. **Verify State**:
    Read existing fact files entirely before proposing updates; never infer missing state.
2. **Contradiction Transparency**:
    Surface conflicts immediately; reject silent overwrites when a proposed fact contradicts an existing `A ≠ ¬A` state.
    Replace, do not append.
3. **Verifiable Facts Only**:
    Record objective facts grounded in repository configuration, code, and explicit documentation. Zero subjective prose.
4. **Structured Format**:
    Enforce rigid hierarchical structures (e.g., Mermaid `mindmap` or perfectly nested Markdown lists). Group by logical
    domains like `Architecture`, `Context`, `Ecosystem`.
5. **Lexical Sorting**:
    Insert new facts in strict alphabetical order within their domain/level.
    - **Case**: Case-insensitive (e.g., `A` and `a` share same priority; `App` before `apple`).
    - **Numbers**: Natural sort (e.g., `v2` < `v10`).
    - **Special Characters**: Sort symbols (e.g., `@`, `_`) before alphanumeric characters.
6. **Reversibility Focus**:
    Offload history, diffs, and rollback logic entirely to Git. Eradicate historical changelogs, sequence IDs, and
    obsolete states from the fact file itself.

## Diagnostics and Revisions

- **Contradiction Sweep**: Pre-commit self-review to guarantee zero logical conflicts.
- **Orphan Pruning**: Seamlessly drop redundant, outdated, or superseded facts (e.g., deprecated libraries) to
  maintain high-density state compression.

## What to Avoid

- **NEVER** insert nodes or lists out of alphabetical order.
- **NEVER** include conversational prose, narratives, or explanations in fact structures.
- **NEVER** hallucinate project details. If unsupported by repo state, reject ingestion.
- **NEVER** preserve historical states when superseded. Replace with the new fact.

## Related Skills

- **mermaid**:
  You MUST load this skill when creating or maintaining Mermaid.js diagrams.
- **mermaid-beta**:
  You MUST load this skill when working with experimental Mermaid.js beta diagrams.
