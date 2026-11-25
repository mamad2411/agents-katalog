---
name: docs-components-design
description: Maintain technical design docs for services, components, workers, modules, and APIs. Use when implementation design, contracts, schema, integrations, runtime behavior, or operational concerns change.
---

# Docs Components Design

Maintain technical design docs for implementation units. Put contracts, state, runtime behavior, and operational detail here rather than in feature or architecture docs.

## Resource Map

- Use `assets/doc-starters/component-design-doc.md` when creating or substantially rewriting a doc in `docs/designs/`.
- Read `references/component-design-example.md` when you need a worked example of the expected technical depth.

## When to Use

- New service, worker, module, integration surface, or shared component
- Changes to interfaces, contracts, schema, queues, state machines, or external integrations
- Changes to concurrency, retries, failure handling, security boundaries, or operational behavior
- Technical design updates that should not live in feature docs

## Do Not Use

- System or domain topology docs that belong in `docs-architecture`
- User-facing feature behavior and goals that belong in `docs-feature-design`

## Workflow

1. Identify the implementation unit and current doc path.
- Default location is `docs/designs/`
- Reuse an existing design doc when one already exists

2. Capture the technical shape of the change.
- Problem and scope
- Interfaces and contracts
- Data model or state changes
- Runtime behavior, failure modes, and operations
- Security and ownership boundaries

3. Keep feature and architecture boundaries clean.
- Link to relevant feature docs instead of retelling the product story
- Link to architecture docs instead of restating system topology

4. Verify against the repo.
- Commands, migrations, contracts, and runtime behavior match the current code
- Design decisions still reflect the active implementation

5. Trim low-value detail.
- Avoid path dumps and copied code
- Keep only the technical detail needed to understand and maintain the component

## Writing Rules

- Technical detail belongs here
- Prefer concise summaries of contracts, schemas, and state over long pasted definitions
- If one component supports multiple features, describe the reusable implementation capability rather than a single feature narrative
- Make trade-offs, failure modes, and ownership explicit
- The Technical Design sub-sections (Interfaces, Data Model, Runtime, Security) are a baseline — add domain-specific sections (Processing Flow, Algorithm, Examples, Configuration) at the same level when they clarify the design better than generic sub-sections would

## Quality Checklist

- The doc clearly names the component or service scope
- Contracts, state, and runtime behavior are accurate
- Operational and security details are current
- Feature behavior is linked out rather than embedded
- Architecture context is referenced rather than duplicated
