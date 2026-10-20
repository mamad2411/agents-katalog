---
name: follow-create-product-deploy-mvp
description: Deploy product MVP — pick platform, env, deploy, verify live URL
argument-hint: "[platform]"
related:
  - follow-create-product
  - follow-deploy
  - deploy-to-cloudflare
  - implement-to-production
  - ask-me
---

## Goal

Deploy the MVP to live — platform per the techstack catalog, env vars complete, verify on the real URL

## Scope

- Use after scaffold + features are ready — focused on MVP deploy, not full production hardening
- Full production gate → `/implement-to-production`

## Execute

### 1. Select Platform

> Goal: platform matching the stack and cost

1. Pick the platform per the `/deep-review-codebase` catalog (default: Cloudflare)
2. If requirements don't match the default → `/ask-me` so the user chooses

### 2. Configure And Deploy

> Goal: successful deploy

1. env vars/secrets complete — via `/follow-secret-manager`, never committed
2. Run `/follow-deploy` or `deploy-to-<platform>` per the target
3. preview/staging before production if the platform supports it

### 3. Verify Live

> Goal: the MVP actually works on the public URL

1. smoke test the critical path on the live URL
2. Record the URL + version in the report

## Rules

- MVP deploy never skips secrets/verify — only non-critical hardening may be skipped
- Destructive config must be confirmed first

## Expected Outcome

- MVP live on a real URL with version and verification results
