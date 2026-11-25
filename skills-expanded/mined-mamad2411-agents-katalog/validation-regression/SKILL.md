---
name: validation-regression
description: Regression validation strategy for SEO generation/integration and gateway permalink contracts.
intent: >-
  Use when adding tests that generalize SEO behavior checks across task logic, config contracts, and route helper behavior.
type: workflow
---

# Validation and Regression

## Test Layers

1. Helper unit tests:
- SEO payload shape
- permalink normalization/deduplication
- deterministic seoPermalink doc generation
- language fallback and canonical URL normalization

2. Config contract tests:
- ads-memory-tree exclusive write includes `seoPermalink`
- gateway SEO mappings count and lookup contract

3. Source contract tests:
- `generatePageSEO` sync path includes independent seoPermalink synchronization

## Runtime Validation

1. Launch services.
2. Run compute flow.
3. Verify seoPermalink documents exist.
4. Verify search.seo payload does not carry `permalinks` field.
5. Verify SEO profile route resolves to ad view.

## Failure Triage

- Empty datasets after regen: repopulate compute/search first.
- Mapping exists but route fails: inspect lookup documentType and param mapping.
- Metadata missing in HTML: trace route model -> template conditions.
