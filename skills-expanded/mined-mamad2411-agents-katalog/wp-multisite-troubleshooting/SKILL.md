---
name: wp-multisite-troubleshooting
description: Diagnoses WordPress Multisite routing, authentication, uploads, domains, rewrites, plugins, themes, cron, cache, database upgrades, and network incidents. Use when failures affect one or many sites.
---

# WordPress Multisite Troubleshooting

Use this skill when a Multisite network has login loops, domain errors, missing media, routing failures, broken Network Admin, inconsistent plugins/themes, cron failures, cache leakage, failed upgrades, or site-specific outages.

## Diagnostic Order

1. Define blast radius: one site, a site class, mapped domains, admin only, or the whole network.
2. Capture exact URL, site ID, timestamp, user role, request path, status code, and recent changes.
3. Verify DNS, TLS, proxy host headers, redirects, cookies, and rewrite behavior.
4. Verify network constants and site records without editing.
5. Compare a failing site with a working site.
6. Check must-use, network-active, and site-active plugins separately.
7. Check active theme and network availability separately.
8. Inspect logs, cron, cache, uploads, and database version state.
9. Reproduce in staging before changing production.
10. Apply the smallest reversible fix and validate the entire affected scope.

## Workflow

Use `workflows/multisite-incident-triage-workflow.md`.

## Resource

Use `resources/multisite-troubleshooting-matrix.md`.

## Example

Use `examples/reauth-loop-investigation.md`.
