---
name: release-safety
description: Use before cutting or deploying a backend release (or reviewing release readiness) — backward compatibility with the current production app, testing the current app against the new backend, rollback plan, config/data readiness, feature flags & observability, and the code-comment policy for transition logic.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Release safety

Core principle: **a backend release is valid only if the current production app keeps working after
it deploys.** Any change that breaks the current app version is an invalid release — regardless of
whether a force update is planned.

## 1. Backend backward compatibility
Every backend release MUST work with BOTH the current production app and the new app — there's always
a gap between backend deploy and app rollout.

**Database changes:**
- Only additive migrations per release (add columns, add tables).
- NEVER rename or drop columns in the same release as the feature using them.
- Sequence: add column → update reads/writes → remove old column in a later release.

**API changes:**
- Preserve existing API contracts (fields, response shapes, endpoints).
- Don't remove/break old fields or endpoints until the old app version is fully deprecated.

**Code requirement:** when introducing backward-compatible logic, add a comment explaining why it's
needed, which app versions are affected, and when the old logic/fields can be removed.

## 2. Test current app against new backend
Before every release — including force-update releases — verify the current production app version
works against the new backend. Run all critical user flows with the current app pointed at the new
backend. If any critical flow fails: block the release, fix the backend, re-test. No exceptions.

## 3. Rollback plan
Every release requires a documented rollback plan before it ships, answering:
- Can the previous backend version be redeployed safely?
- If not, what's the forward-fix strategy?
- Who is the rollback owner (authority to trigger it)?
- What are the rollback conditions (error-rate threshold, critical failure types)?

Do not release if any of the above is undefined.

## 4. Config & data readiness
- NEVER assume staging DB, config, or seed data matches production — verify explicitly.
- Validate all critical config at startup; fail fast if missing/invalid — no silent fallbacks.
- Treat code readiness, DB migration readiness, and config readiness as three separate checks.
- Explicitly verify partner settings, category mappings, plan settings, and other business config.
- Keep a golden staging/UAT dataset covering critical flows and known edge cases.
- Don't rely on staging-only assumptions or seed data in production code paths.

## 5. Feature flags & observability
- Use feature flags for high-risk business-logic changes — do not gate on `NODE_ENV`.
- Add logs and alerts on every critical rule branch, fallback path, missing config, unexpected behavior.
- Post-release verification is mandatory for critical flows — smoke-test before AND after release.

## 6. Code comment policy (transition logic)
Add code comments only when needed for: backward compatibility (affected versions + when removable),
migration safety (what state the DB must be in), release safety (deploy-order requirement), or
temporary transition logic (`TODO: remove after <version>`).
