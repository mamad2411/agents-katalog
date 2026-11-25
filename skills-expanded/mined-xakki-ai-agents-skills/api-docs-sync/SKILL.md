---
name: api-docs-sync
description: 'Reconcile API documentation, OpenAPI artifacts, documentation UIs and public capability catalogs (llms.txt, indexes) with the shipped implementation. Use when API docs may have drifted from routes or schemas. RU: документация API, openapi, llms.txt.'
disable-model-invocation: true
---

# API documentation

Use implementation, route and schema declarations as evidence for public claims. Identify the canonical source, generated artifacts, public surfaces, supported tools and authorized scope before editing. Preserve unrelated work and follow the project's conventions.

Reconcile documentation with shipped routes, request and response shapes, authorization, entitlements and limitations. Change canonical inputs first, then regenerate only affected derived artifacts with the project's supported commands. Verify source and generated output for drift and stale claims; never assume a specific build target exists or hand-edit generated output as a substitute for fixing its source. Runtime-generated specifications need runtime verification.

For public API indexes, `llms.txt`, sitemaps and similar capability catalogs, use the [public capability catalog checklist](references/public-capability-catalogs.md): verify claims against the implementation, reconcile counts and localized entries and boundaries against evidence, and document the actual protocol, authentication and freshness limits. A catalog-only change does not by itself require OpenAPI generation, container builds or a commit.

For self-hosted documentation UIs, use the [UI asset checklist](references/self-hosted-docs-ui.md). A page with no third-party startup requests, a build that does not download UI assets, and an entirely offline rebuild are separate claims.

For operation-level authentication metadata or a generator that cannot write to its default output, use [schema verification](references/schema-verification.md). Run proportionate project checks for the changed contract, including relevant authentication behavior and documentation drift. Report commands, actual outcomes and skipped checks, and distinguish unchanged artifacts from regenerated changes. Preserve existing staged work and commit only when authorized under the project policy.
