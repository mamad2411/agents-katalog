---
name: follow-deploy-deploy-railway
description: Deploy to Railway by delegating to the /deploy-to-railway skill
argument-hint: "[target]"
related:
  - deploy-to-railway
  - follow-secret-manager
  - ask-me
  - resolve-errors
---

## Goal

Map the generic `/follow-deploy` flow to Railway by delegating all platform-specific work to `/deploy-to-railway`

## Scope

- Use when the parent `/follow-deploy` selects Railway as the target platform
- This workflow is a dispatch layer only — the real workflow lives in `/deploy-to-railway`
- Suits full-stack applications that need a database or long-running services

## Execute

### 1. Confirm Target

> Goal: confirm the target is Railway and the project is ready

1. Check project type — full-stack app, Dockerfile, or a service Railway supports (`railway.json` if present)
2. If unclear → `/ask-me`
3. Check prerequisites: env vars/secrets complete via `/follow-secret-manager` — set them with `railway variables set KEY=value` or the Railway dashboard

### 2. Map Generic Requirements

> Goal: map the parent flow's concepts to Railway equivalents

1. env vars/secrets → `railway variables set KEY=value` or the Railway dashboard via `/follow-secret-manager`
2. staging environment → a separate Railway environment in the same project
3. deployment URL → `*.up.railway.app` or the attached custom domain
4. version id → Railway deployment id from the deploy command output

### 3. Delegate To Platform Skill

> Goal: use the platform-specific skill instead of the generic flow

1. Follow the whole `/deploy-to-railway` flow — link project, deploy, post-deploy verify
2. If unsure about Railway CLI commands/flags → check the official docs instead of guessing

### 4. Report

> Goal: report deploy results per the parent's generic contract

1. report deployment URL, service/deployment id, and post-deploy verify results
2. if fail → `/resolve-errors` max 3 rounds, then stop and report

## Rules

### 1. Delegate Only

- never duplicate platform logic in this workflow — always delegate to `/deploy-to-railway`
- if unsure about a Railway feature → check the official docs instead of guessing

### 2. Safety

- staging environment before production per the parent's rules
- secrets only via `/follow-secret-manager` — never hardcode

## Expected Outcome

- deploy via `/deploy-to-railway` succeeds with URL + deployment id
- results reported back to the parent flow of `/follow-deploy`
