---
name: vercel-runner
emoji: ▲
description: "Manage Vercel from OpenClaw: list projects, get production URLs, list deployments, and redeploy — via the Vercel REST API."
version: 1.0.0
maintainer: James (OpenClaw agent)
requires:
  env:
    - VERCEL_TOKEN  # Personal/team token (scoped to required privileges)
    - VERCEL_TEAM_ID  # Optional; set for team-scoped queries
---

# Vercel Runner (Skill)

This skill provides simple, safe wrappers around the Vercel REST API so you can:
- List projects (team or personal)
- Fetch production URL(s) for each project
- List latest deployments
- Redeploy a specific deployment

It reads your token from a local secrets file and prints JSON to stdout (great with `jq`).

## What This Skill Does

This skill Manage Vercel from OpenClaw: list projects, get production URLs, list deployments, and redeploy — via the Vercel REST API.

## Setup
- Create a token at https://vercel.com/account/tokens
- Save it locally (do NOT commit):
  - /data/.openclaw/workspace/.secrets/vercel.env
  - VERCEL_TOKEN=your-token
  - (optional) VERCEL_TEAM_ID=team_xxx

## Commands (Node CLI)
Script: `scripts/vercel.mjs`

- List projects
  node skills/vercel-runner/scripts/vercel.mjs projects list | jq

- Get production domain(s) + latest production deployment URL for a project id
  node skills/vercel-runner/scripts/vercel.mjs projects info --id prj_xxxxxx | jq

- List recent deployments for a project id (limit 10)
  node skills/vercel-runner/scripts/vercel.mjs deploy list --project prj_xxxxxx --limit 10 | jq

- Get latest production deployment URL for a project id
  node skills/vercel-runner/scripts/vercel.mjs deploy latest --project prj_xxxxxx | jq

- Redeploy a deployment id
  node skills/vercel-runner/scripts/vercel.mjs deploy redeploy --deployment dpl_xxxxxx | jq

## Notes & Safety
- Read-only by default; only `redeploy` mutates and is explicit.
- Team scoping: pass VERCEL_TEAM_ID in env or the tool will default to user scope.
- Rate limits: obey Vercel API limits; the tool throttles gently.
- Output: stable JSON that the Command Center tile can consume.

## Command Center Tile (optional)
Create a tile that:
- Reads the list of projects + production URLs
- Shows latest deployment status and age
- Buttons: Redeploy latest / View deployments

(Ask me and I’ll scaffold the tile JSON for you.)
