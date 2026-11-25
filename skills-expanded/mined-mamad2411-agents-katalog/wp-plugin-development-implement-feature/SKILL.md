---
name: wp-plugin-development-implement-feature
description: Implements a bounded WordPress plugin feature using appropriate core APIs, explicit authorization, owned data, safe migrations, tests, and compatibility checks. Use when adding or changing plugin behavior.
---

# WordPress Plugin Feature Implementation

Use this skill after the plugin boundary and compatibility contract are known.

## Inputs to collect

- Existing plugin architecture and public contracts.
- Exact feature behavior and non-goals.
- Entry points and users or systems that can invoke them.
- WordPress/PHP minimums and required dependencies.
- Data shape, ownership, scale, query patterns, privacy, retention, and uninstall behavior.
- Upgrade path from existing versions.
- Acceptance tests and operational failure behavior.

## Method

1. Inspect the current bootstrap, hooks, services, storage, migrations, tests, and release conventions.
2. Select the narrowest suitable WordPress APIs with the [WordPress API selection matrix](resources/wordpress-api-selection-matrix.md).
3. Define authorization, request intent, validation, sanitization, output escaping, and error behavior for each entry point.
4. Apply the [data lifecycle and migration checklist](resources/data-lifecycle-and-migration-checklist.md).
5. Implement the smallest cohesive change using existing namespaces, prefixes, dependency injection, and file layout.
6. Keep migrations and background work restartable and idempotent.
7. Add positive, negative, compatibility, upgrade, and failure-path tests before broad refactoring.
8. Run the [feature implementation workflow](workflows/implement-plugin-feature-workflow.md).
9. Report changed contracts, migrations, compatibility impact, tests, and unresolved risks.

## Decision rules

- Use settings/options for site configuration, not for high-volume event or relational data.
- Use metadata only when the data belongs to the corresponding WordPress object and its query needs are supported.
- Use a custom post type when editorial lifecycle, permissions, revisions, REST exposure, or admin management genuinely fit the content.
- Use a custom table only for access patterns, volume, integrity, or indexing that core storage cannot meet cleanly.
- Use Transients or object cache only for disposable derived data; correctness must not depend on cache persistence.
- Use WP-Cron for deferred WordPress work, not precise scheduling guarantees.
- Use admin-post or REST for explicit actions; do not overload page rendering with mutations.
- Keep advanced block, headless REST, WP-CLI, and product-specific implementation in their dedicated plugins.

## Required output

Return:

- requirement-to-code mapping
- selected WordPress APIs and rejected alternatives
- entry-point authorization/input/output map
- storage and migration impact
- changed public hooks/routes/options/schema
- test evidence across supported versions
- performance, privacy, and rollback notes
