---
name: jal-seo-generation-integration
description: JAL Site Agent playbook for SEO generation and integration across compute flows, ad view rendering, seoPermalink ownership, gateway lookup mappings, and regression validation.
intent: >-
  Use this skill when implementing or reviewing SEO behavior for JAL-authored sites, including phase-1 SEO generation, ad-view SEO metadata mapping, permalink ownership separation, and gateway operational routing.
type: workflow
best_for:
  - "Implementing generatePageSEO and generateIndexSEO workflows"
  - "Injecting language-specific SEO metadata into ad/profile view routes"
  - "Managing SEO-owned permalink documents and gateway lookup contracts"
  - "Designing regression tests for config, task, and rendering contracts"
scenarios:
  - "search.seo payloads are missing fields or include deprecated permalink fragments"
  - "SEO profile URLs must resolve to ad_view via document lookup"
  - "Need deterministic permalink regeneration with ownership and stale cleanup"
---

# JAL SEO Generation and Integration

## Required Subskills

Run these subskills in order for full implementation:

1. `phase-1-generation`
2. `ad-view-integration`
3. `permalink-ownership-gateway`
4. `validation-regression`
5. `grpc-mtls-cert-bootstrap` when the site needs local gRPC cert generation or rotation before startup
6. `location-language-search-integration` when the site needs hierarchical location search or language-aware parsing

## Implementation Rules

- Keep `_gen.*` files read-only; edit source templates/config/tasks only.
- Prefer site-local changes under `sites/<site>/...`.
- Treat shared-lib as read-only unless the defect is systemic and approval is explicit.
- Keep permalink ownership out of `search.seo.<lang>` once `seoPermalink` is active.
- Use `grpc-mtls-cert-bootstrap` before launching sites whose gRPC services fail on missing local TLS files.
- Use `location-language-search-integration` before changing search token, breadcrumb, or language behavior.

## Output Expectations

- SEO generation behavior documented.
- Route/template mapping verified.
- Gateway mappings and document lookup contract validated.
- Regression tests added or updated for all changed SEO contracts.
