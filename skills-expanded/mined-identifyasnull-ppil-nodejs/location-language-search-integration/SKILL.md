---
name: "location-language-search-integration"
description: "Use when implementing hierarchical location search or language-aware parsing, breadcrumbs, and pagination in JAL site search flows."
intent: >-
  Provide a site-local workflow for hierarchical location and multi-language search integration: add location criteria, preserve language in the state token, keep breadcrumb filtering stable, and validate ranking and pagination behavior end to end.
type: workflow
best_for:
  - "Adding hierarchical location criteria to search"
  - "Persisting language-aware search state through pagination"
  - "Updating breadcrumb labels and token payloads"
  - "Validating search ranking and location/language regression coverage"
scenarios:
  - "search needs Country -> State -> City -> Suburb hierarchy"
  - "lang must persist in the search state token"
  - "breadcrumb_criteria must stay pre-filtered at the search endpoint"
---

# Location and Language Search Integration

## Purpose

Use this skill when a JAL-authored site needs hierarchical location search, language-aware parsing, or state-token persistence for search results, breadcrumbs, and pagination.

## Core Rules

- Treat location as optional and rank-based unless the business rule explicitly says otherwise.
- Keep breadcrumb filtering at the search endpoint; do not rebuild or expand it later in listing code.
- Preserve the selected `lang` value in the state token so pagination and breadcrumb rendering stay consistent.
- Keep the 7-field state token contract stable unless the owning search system explicitly changes it.
- Validate search results against both ranking behavior and breadcrumb display behavior.

## Required Location Model

For hierarchical location support, model location as a 4-level path:

1. Country
2. State or Region
3. City
4. Suburb

The search system should treat each level as a parent of the next level and allow a selected lower-level location to match its ancestors and descendants according to the configured hierarchy.

## Language Model

Support language-aware search parsing with a stable `lang` field in the state token.

Recommended baseline set:

- `en`
- `es`
- `fr`
- `de`
- `pt`
- `zh`
- `ja`

Use language-aware parsing for query tokenization, breadcrumb presentation, and any voice or NLP inputs that need locale selection.

## Quick Start

1. Add or update location criteria in the search config.
2. Ensure each location criterion declares its hierarchy level and parent relationship.
3. Preserve `lang` in the search state token.
4. Filter `breadcrumb_criteria` once at the search endpoint.
5. Render breadcrumbs from the token payload during listing.
6. Run regression tests for location matching, language persistence, and pagination.

## Search Token Contract

Keep the state token aligned to the repo's search flow:

- `selector`
- `rawSelector`
- `queryDerivedSelector`
- `query`
- `breadcrumb_criteria`
- `queryDiagnostics`
- `lang`

If a payload field is missing, fix the search endpoint or token creation path first. Do not patch listing code to reconstruct missing token semantics.

## Workflow

1. Update search config with hierarchical location properties.
2. Update the parser or selector merge logic to respect language.
3. Confirm breadcrumb criteria is pre-filtered before token creation.
4. Ensure pagination reuses the token instead of rebuilding search context.
5. Verify ranking still treats location as an optional match dimension.
6. Add or update tests for state token round-trip, breadcrumb persistence, and language-specific parsing.

## Validation

- Location hierarchy selections return the expected result set.
- Matching ads rank higher when both location and other optional criteria match.
- Breadcrumbs render only the selected criteria from the token payload.
- Language persists through pagination and breadcrumb rendering.
- Tests cover state-token round-trip and location/language combinations.

## Anti-Patterns

- Rebuilding breadcrumbs in listing code.
- Treating location as an exclusive WHERE-clause filter when it should rank instead.
- Dropping `lang` during pagination.
- Hardcoding one language path and bypassing parser configuration.
- Expanding breadcrumb criteria after the search endpoint has already filtered it.

## References

- `memories/repo/location-language-implementation.md`
- `memories/repo/grpc-mtls-certs-and-encryption-process.md`
- `memories/repo/grpc-mtls-certs-quickstart.md`
