---
name: jquery-source-curation
description: Use when jQuery guidance needs evidence from api.jquery.com, jQuery Migrate, and release notes with explicit deprecation, plugin-compatibility, and legacy-browser freshness controls.
---

# jQuery Source Curation

## Specialization

Track jQuery source evidence around long-lived API behavior, Migrate warning coverage, plugin survivability, and browser-era compatibility constraints that matter in legacy estates.

This specialization starts with `api.jquery.com`, `jquery-migrate`, and release notes, then turns those inputs into keep-vs-modernize guidance for teams maintaining older frontend code.

This skill governs source selection and skill grounding only. It does not implement jQuery code or configure projects.

## Objective

Produce a jQuery maintenance evidence pack that clarifies deprecated APIs, migration blockers, plugin risk, and version-specific behavior changes for downstream jQuery skills.

## Trigger Conditions

- A new jQuery skill or policy needs source grounding.
- Existing jQuery skill references may be stale after a jQuery version release.
- A quality gate or implementation workflow needs refreshed source evidence before proceeding.
- The `jquery-core`, `jquery-events`, `jquery-ajax`, `jquery-plugins`, `jquery-performance`, `jquery-migration`, `jquery-testing`, `jquery-security`, or `jquery-quality-gate` skills require a source-freshness check.
- A project is adopting a new jQuery major version or migrating from jQuery to native APIs.

## Scope Boundaries

In scope:

- Source selection, authority classification, and freshness checks for jQuery and its immediate ecosystem.
- Mapping source content into actionable guidance deltas for downstream jQuery skills.
- Rejected-source recording with explicit reason codes.
- Version-aware curation for jQuery core changes, deprecated API removals, and plugin compatibility shifts.

Out of scope:

- Direct implementation of jQuery code or configuration files.
- Framework-specific integration patterns beyond what official docs cover.
- Non-jQuery frontend tooling unless it directly gates a jQuery capability phase.

## Inputs

- Target jQuery topics and expected output artifacts.
- Evaluation date in ISO format (`YYYY-MM-DD`).
- Freshness threshold in days (default: 30).
- Current jQuery version in the project (if applicable).
- Existing source inventory if available (`./references/source-catalog.md`).

## Required Outputs

- Updated source catalog (`./references/source-catalog.md`) with authority, freshness, relevance, and actionability fields.
- Topic-to-source coverage matrix across: core API, events, AJAX, plugins, performance, migration, security, and testing.
- Rejected-source table with deterministic reason codes.
- Prioritized guidance deltas grouped by: API changes, deprecated removals, plugin compatibility, performance recommendations, and security advisories.
- Version-impact note describing any jQuery behavior changes relevant to existing skills.

## Authoritative Source Registry

| Source | Authority | Domain | URL |
|---|---|---|---|
| jQuery API Documentation | Primary | Full API reference — selectors, DOM, events, AJAX, effects, utilities | https://api.jquery.com |
| jQuery Learn Center | Primary | Structured tutorials — core concepts, AJAX, events, plugins | https://learn.jquery.com |
| jQuery GitHub Repository | Primary | Source code, changelogs, issue tracker, version history | https://github.com/jquery/jquery |
| jQuery Blog | Primary | Release notes, deprecation announcements, security advisories | https://blog.jquery.com |
| jQuery Migrate Plugin | Primary | v1→v3 migration guidance, deprecation shims, compat testing | https://github.com/jquery/jquery-migrate |
| jQuery UI Docs | First-party | Interaction widgets, effects, theming — official jQuery UI surface | https://jqueryui.com/demos/ |
| jQuery Validation Docs | First-party | Client-side form validation plugin — official jQuery Validation | https://jqueryvalidation.org |
| MDN Web Docs (DOM/Events) | Supporting | Native DOM, Fetch, Event API context situating jQuery vs. native decisions | https://developer.mozilla.org |
| OWASP XSS Prevention Cheat Sheet | Standard | Security baseline for `.html()` vs `.text()`, `$.parseHTML()` safety | https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html |
| OWASP CSRF Prevention Cheat Sheet | Standard | CSRF token patterns in AJAX requests | https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html |
| Can I Use | Supporting | Browser compatibility signals for jQuery-adjacent DOM/CSS features | https://caniuse.com |
| QUnit Docs | First-party | jQuery's own test framework — preferred for jQuery plugin testing | https://qunitjs.com |

## Source Decision Rules

- `accept`: authoritative source, freshness within threshold, directly actionable.
- `accept-with-watch`: authoritative and relevant but partial, stale, or pending update.
- `reject`: not authoritative, too stale, redundant, or non-actionable.

## Rejected Source Reasons

- `R1`: Not authoritative for jQuery behavior.
- `R2`: Stale beyond freshness threshold with no mitigation.
- `R3`: Redundant — a higher-authority source already covers the same content.
- `R4`: Community content with unverified accuracy for production guidance.

## Workflow

1. Record evaluation date and freshness threshold.
2. Load existing source catalog from `./references/source-catalog.md` if present.
3. Fetch each authoritative source and classify: `accept`, `accept-with-watch`, or `reject` with a reason code.
4. Map each accepted source to the downstream skill phase it informs.
5. Identify guidance deltas since last evaluation: API removals, deprecation notices, jQuery version upgrades, plugin compatibility updates, security advisories.
6. Record rejected sources with reason codes.
7. Produce coverage matrix and confirm every downstream skill topic has at least one accepted source.
8. Emit the version-impact note for any behavior change that affects existing skill recommendations.
9. Write updated `./references/source-catalog.md`.

## Pragmatic Stop Rule

Stop when every downstream skill topic in the coverage matrix maps to at least one `accept` or `accept-with-watch` source and all guidance deltas are recorded. A bounded exception record is required for any topic with only `accept-with-watch` sources.
