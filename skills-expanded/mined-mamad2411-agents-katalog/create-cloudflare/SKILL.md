---
name: create-cloudflare
description: Create Cloudflare resources — worker, deploy button, API token via create-cloudflare-* skills
argument-hint: "[domain]"
related:
  - follow-service-cloudflare
  - deploy-to-cloudflare
  - use-wrangler
  - follow-secret-manager
  - ask-me

---

## Goal

Dispatch to the skill for the Cloudflare resource that needs to be created — the parent only routes.

## Scope

- The argument is the domain; if omitted → `/ask-me` to pick a domain.

## Execute

### Create Cloudflare Skills

| Domain | Skill |
|---|---|
| `worker` | `/create-cloudflare-worker` — scaffold a new Worker |
| `deploy-button` | `/create-cloudflare-deploy-button` — create a deploy-to-Cloudflare button |
| `token` | `/create-cloudflare-token` — create an API token with the right scope |

1. Determine the domain from the argument (e.g. `/create-cloudflare worker`)
2. If the domain is supported → invoke the matching skill from the table and follow its flow
3. If no domain is given or it is unrecognized → `/ask-me` to pick a domain

## Rules

- The parent only dispatches — never duplicate the target skill's workflow
- New credentials/tokens must go through `/follow-secret-manager` — never commit them

- Use /follow-service-cloudflare when needed
- Use /deploy-to-cloudflare when needed
- Use /use-wrangler when needed

## Expected Outcome

- The caller is dispatched to the skill matching the domain and creates the resource via its flow
