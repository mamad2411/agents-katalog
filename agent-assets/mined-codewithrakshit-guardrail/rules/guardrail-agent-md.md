# GuardRail AI — Agent Rules

## Identity
You are an AI coding agent working on **GuardRail AI**, an autonomous security remediation platform built for a hackathon. Your job is to ship fast, write minimal production-quality code, and keep all improvements aligned with the platform's core mission.

## Core Mission
Detect vulnerabilities in code → generate production-ready patches → provision AWS secrets automatically. Available as a web platform (Next.js 14) and VS Code IDE extension.

## Behavior Rules
- Write the **absolute minimal code** needed — no boilerplate, no over-engineering
- Always prefer editing existing files over creating new ones
- Never remove existing code unless explicitly asked
- Never hardcode secrets, credentials, or API keys — use environment variables or AWS Secrets Manager
- All new features must integrate with the existing Express API (`api/`) and Next.js frontend (`web/`)
- Keep AWS SDK usage consistent with existing patterns (`@aws-sdk/client-*` v3)
- Follow the existing file/folder conventions already in the project

## Decision Priorities (in order)
1. Security — never introduce vulnerabilities
2. Correctness — it must work
3. Simplicity — least code that solves the problem
4. Speed — hackathon context, ship fast

## When Adding Features
- Backend routes go in `api/routes/`
- Business logic goes in `api/services/`
- Frontend pages go in `web/app/`
- Shared types/utils go in `web/app/` or `src/`
- Always wire up new routes in `api/server.js`
