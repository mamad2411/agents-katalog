---
name: grovs-setup-project
description: Set up a new mobile app project in Grovs — create an instance, configure iOS Universal Links or Android App Links, and set redirect behavior so your tracking links work out of the box. Use when the user wants to create a new app, project, or start using Grovs.
---

# Grovs: Set Up a New Project

## Data model

```
Instance (instance_id = hash_id string)
├── Production project (project_id = production.hash_id string)
│   └── links, campaigns, redirects, analytics
└── Test project (project_id = test.hash_id string)
    └── links, campaigns, redirects, analytics
```

`create_project` creates all of this in one call.

## Required order

1. `get_status` — check for existing instances first. If a matching one exists, confirm with the user before creating a duplicate.
2. `create_project` — returns `instance.hash_id` + `production.hash_id` + `test.hash_id`. Save all three.
3. `configure_sdk` with the **instance_id** — platform identity (bundle ID, package name, etc.)
4. `configure_redirects` with the **production project_id** — where users land (App Store URL, fallback website). Skip if user didn't provide URLs.

**`configure_sdk` takes instance_id. `configure_redirects` takes project_id. These are different strings. Mixing them up will fail silently or error.**

## What to ask the user

Only what's not already in the conversation:
- App name
- At least one platform: iOS needs `bundle_id` + `team_id`. Android needs `package_name` + `sha256_fingerprints`.
- Fallback URL for desktop/web (optional)

## Example

User: "Set up Grovs for my app Foodies, it's iOS only, bundle is com.foodies.app, team ID is ABC123"

```
1. get_status()                              → no existing instances
2. create_project(name: "Foodies")           → instance_id: "x7k2", prod_id: "p_m9f", test_id: "t_q3r"
3. configure_sdk(instance_id: "x7k2", ios_bundle_id: "com.foodies.app", ios_team_id: "ABC123")
4. → Done. No redirects needed since user didn't provide URLs.
```

Present the production project_id (`p_m9f`) — the user will need it for every other tool.

## Checking usage and subscription

`get_usage` takes an **instance_id** and returns current MAU count, MAU limit, quota status, and subscription status. Use it when:
- The user asks about their plan, usage, limits, or billing
- `get_status` shows a usage warning (quota exceeded) — `get_usage` gives the full picture
- Before setting up a new project, to check if the user's instance has capacity

If the quota is exceeded and there's no subscription, deep links stop working. Tell the user to subscribe.

## If something fails

- `create_project` errors with "name taken" → the instance already exists. Run `get_status` and use the existing one.
- `configure_sdk` errors → most likely you passed project_id instead of instance_id. Check.

## All tool responses are pre-formatted

Every Grovs tool returns human-readable formatted text (tables, summaries). Don't reformat — just present the response and add your own context around it.
