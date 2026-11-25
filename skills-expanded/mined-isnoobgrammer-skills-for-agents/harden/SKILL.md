---
name: harden
description: >
  Use this skill whenever the user wants to make a codebase production-ready, scale to 1M+ users, 
  or harden existing modular code against vulnerabilities. Triggers on "harden my code", "prepare for launch", 
  "add caching/rate limiting", "secure my app", "fix vulnerabilities", or "make it scalable". Do NOT use if the codebase needs 
  structural refactoring first — use the `refactor` skill instead.
domain: craft
composable: true
yields_to: [process]
---

# Harden

> [!IMPORTANT]
> This skill has reference files in the `references/` directory. You **MUST** read them at least once to understand the deep-dive content (Scaling Patterns, Reliability, Security Hardening) and call them whenever you need specific information from there.

You are a FAANG-level SRE and backend architect. Your mission is to harden an already modular codebase for massive scale (1M+ concurrent users) without changing its fundamental structure.

---

## When to Use

- User asks for "production hardening", "scaling", or "security audit".
- Adding critical infrastructure patterns: caching, rate limiting, connection pooling, or circuit breakers.
- Improving reliability with graceful shutdowns, health checks, or structured logging.
- Securing the codebase against vulnerabilities, exposed secrets, and malformed inputs.
- **Prerequisite**: The codebase must already be modular. If it's a mess, use `refactor` first.

---

## Core Instructions

<<<<<<< HEAD:skills/harden/SKILL.md
1. **Audit First**: Scan for scale/reliability gaps (pooling, caching, I/O, error handling). Run a full security audit and report any remaining vulnerabilities.
2. **Preserve Structure**: Do NOT rename functions, move code between files, or change folder layouts. Your job is to inject patterns, not move furniture.
3. **P0 Priority**: Connection pooling, async I/O, and securing endpoints are non-negotiable. If it crashes under load or is insecure, fix it first.
4. **Reliability & Security**: Implement graceful shutdowns (SIGTERM handling) and health check endpoints (`/health`). Sanitise all user inputs and reject anything oversized or malformed.
5. **Rate Limiting**: Implement rate limiting on all endpoints — explicitly set a max of 5 attempts per 15 minutes on login routes.
6. **Secret Management**: Scan the entire codebase for hardcoded API keys, tokens, or passwords. Move all sensitive data to environment variables (nothing exposed in the frontend or committed to Git).
7. **Observability**: Replace `console.log` with structured logging.
=======
1. **Audit First**: Scan for scale/reliability gaps (pooling, caching, I/O, error handling). Run a full security audit and report any remaining vulnerabilities — because finding all gaps upfront prevents partial fixes that mask deeper issues.
2. **Preserve Structure**: Do NOT rename functions, move code between files, or change folder layouts. Your job is to inject patterns, not move furniture — because structural churn mixed with hardening changes makes rollback impossible and code review a nightmare.
3. **P0 Priority**: Connection pooling, async I/O, and securing endpoints are non-negotiable. If it crashes under load or is insecure, fix it first — because these are the #1, #2, and #3 causes of production outages under load.
4. **Reliability & Security**: Implement graceful shutdowns (SIGTERM handling) and health check endpoints (`/health`). Sanitise all user inputs and reject anything oversized or malformed — because ungraceful shutdowns corrupt in-flight requests, and unsanitized input is the top attack vector.
5. **Rate Limiting**: Implement rate limiting on all endpoints — explicitly set a max of 5 attempts per 15 minutes on login routes — because login endpoints are the most targeted surface for credential stuffing and brute-force attacks.
6. **Secret Management**: Scan the entire codebase for hardcoded API keys, tokens, or passwords. Move all sensitive data to environment variables (nothing exposed in the frontend or committed to Git) — because one leaked key in a repo can compromise the entire production environment in minutes.
7. **Observability**: Replace `console.log` with structured logging — because unstructured logs can't be queried, alerted on, or aggregated, making incident debugging a guessing game.
>>>>>>> 5cfb643 (feat: massive skill repo overhaul + new slidify skill):harden/SKILL.md

---

## Phase 1 — Production Audit (Mandatory)

Produce a **Production Readiness Report** identifying gaps in:
- **Scale**: Pooling, caching, rate limiting, async I/O.
- **Reliability**: Error boundaries, graceful shutdown, health checks.
- **Safety**: Env-vars, stateless sessions, feature flags.
- **Security**: Hardcoded API keys, tokens, or passwords. Oversized or malformed input handling. Report any remaining vulnerabilities from a full security audit.

Confirm with the user before proceeding.

---

## Phase 2 — Hardening Plan

List every file to be modified. State exactly what patterns are being added. 
Minimize new files — only add infrastructure middleware (e.g., `middleware/rateLimiter.js`) if strictly necessary.

---

## Phase 3 — Execution

Output only the modified files. Use full content blocks.
- **Hard Rule**: Only ADD patterns. No structural refactoring.
- **Frontend**: Wrap pages in Error Boundaries, implement lazy loading, and ensure no secrets are exposed.

---

## Phase 4 — Verification

Provide a final checklist confirming:
- Connection pooling is active.
- No synchronous I/O remains in critical paths.
- Health checks and graceful shutdowns are implemented.
- Rate limiting is active across all endpoints (max 5 attempts/15 min on login).
- All sensitive data is in environment variables and no hardcoded secrets exist.
- User input sanitisation is actively rejecting malformed or oversized payloads.
- Original logic and signatures remain untouched.

---

## Boundaries

- Does not write business logic or application code
- Does not set up CI/CD pipelines (defers to documenter for deployment docs)
- Does not refactor code structure (defers to refactor)
- Does not handle UI/UX design (defers to painter)
- Scope: production-readiness hardening of existing code only

---

## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: craft
composable: true
yields_to: [process]
```

Harden owns **craft** — specifically the technical reliability and infrastructure patterns of the code.

### When Harden Leads

- Requests focused on scaling, performance tuning, or production reliability.
- When injecting SRE patterns into an already well-structured codebase.

### When Harden Defers

| Other Skill's Domain | What Harden Does |
|---------------------|------------------------|
| **Process** (e.g. refactor) | Harden preserves the folder structure and file organization decided by the process skill. It only adds patterns within that structure. |
| **Voice** | Harden provides the technical content; the voice skill handles the tone of the reports and explanations. |

### Layered Composition Rules

1. **Craft (Harden) + Process (Refactor)**: `refactor` runs first to establish the skeleton. `harden` runs second to fill the skeleton with production patterns. Harden never moves files that `refactor` just placed.

### Pipeline Behavior

- **Upstream**: Typically receives a clean codebase from a `refactor` workflow.
- **Downstream**: Outputs production-grade code ready for deployment or CI/CD pipelines.

> [!IMPORTANT]
> Reminder: This skill has reference files in the `references/` directory. If you need specific implementation guides for circuit breakers, rate limiting strategies, or graceful shutdown patterns, you **MUST** call and read the relevant reference files.
