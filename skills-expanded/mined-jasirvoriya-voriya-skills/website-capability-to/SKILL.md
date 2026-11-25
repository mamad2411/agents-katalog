---
name: website-capability-to-skill
description: Convert website capabilities into a site-specific API-first skill from a target URL. Use when asked to transform a website's visible functions into callable API workflows, implement "learn by browser, execute by API", and keep auth in ~/.domain-slug-auth.yaml with automatic browser-based refresh on auth failure.
---

# Website capability to skill

## Overview

Convert website capabilities into a site-specific skill from a website URL. Use
Chrome DevTools only for capability discovery and auth recovery. Implement
final behavior with direct API calls.

## Non-negotiable rules

1. Use browser automation only for discovery and auth recovery.
2. Use API calls for all business actions in the generated skill.
3. Persist auth data in the user home directory as `~/.<site>-auth.yaml`.
4. Load auth data from file before every API session.
5. On auth failure or token expiry, recover auth from browser and rewrite the
   auth file.
6. Write auth files with `0600` permissions.

## Input contract

- Required: target website URL.
- Optional: capability scope; if not provided, cover key user workflows.

## Workflow

### 1) Discover capabilities with chrome-devtools

1. Open target URL with `new_page`.
2. Inspect menu and key workflows with `take_snapshot`.
3. Trigger real user actions and inspect traffic with
   `list_network_requests` and `get_network_request`.
4. Capture candidate endpoints, methods, request body/query, headers, and
   response schema.
5. Filter out static assets and analytics requests.

### 2) Build capability-to-API mapping

For each visible website capability, map:

- capability name
- UI path
- endpoint(s)
- request schema
- response schema
- auth requirement
- validation method

If no callable API exists, mark capability as `unsupported-via-api`.

### 3) Scaffold a site skill

Run:

```bash
python3 scripts/bootstrap_site_skill.py --url <target-url> --output-root <skills-root>
```

This creates a generated skill folder with:

- `SKILL.md`
- `agents/openai.yaml`
- `scripts/auth_cache.py`
- `references/capability-map.md`

Then fill the generated `references/capability-map.md` with actual endpoint
details from discovery.

### 4) Implement mandatory auth lifecycle

Use `scripts/auth_cache.py`:

1. Resolve cache file path:
   `python3 scripts/auth_cache.py path --url <target-url>`
2. Read cache:
   `python3 scripts/auth_cache.py read --url <target-url>`
3. Validate cache:
   `python3 scripts/auth_cache.py is-valid --url <target-url>`
4. If validation fails or API returns auth errors (`401`, `403`, expired token,
   invalid session):
   - Open website in browser and complete login.
   - Extract auth artifacts from network requests, cookies, local storage, and
     anti-CSRF request data.
   - Persist auth:
     `python3 scripts/auth_cache.py write --url <target-url> --auth-json '<json>' --source browser-recovery --ttl-hours <n>`
5. Retry API flow with refreshed auth.
6. If retry still fails, return blocked status with evidence.

### 5) Enforce generated skill behavior

The generated site skill must:

1. Read auth cache before API calls.
2. Use API for all capability execution.
3. Use browser only when auth recovery is required.
4. Rewrite auth cache after successful recovery.
5. Surface unsupported capabilities clearly.

## Output contract

Produce all of the following:

1. A generated site-specific skill folder.
2. A completed capability map file for that site.
3. Auth cache workflow wired through `scripts/auth_cache.py`.
4. A short verification report with tested and unsupported capabilities.

## Resources

- `scripts/auth_cache.py`: manage auto-generated `~/.<host-slug>-auth.yaml` files.
- `scripts/bootstrap_site_skill.py`: scaffold site-specific API-first skills.
- `references/generated-skill-template.md`: template for generated skill body.
- `references/capability-map-template.md`: capability mapping template.
