---
name: map-the-surface
description: Reconnaissance pass over an unfamiliar or vibe-coded codebase that produces SURFACE.md, an inventory of data models, every entry point, where data lives, the tenant model, third-party services, and where money moves. Use at the very start of a deslop / security audit / takeover, whenever you need to understand an inherited or AI-generated app before changing it, or when the user asks "what does this app actually do / expose". Run before plug-the-holes and launch-gate; they both consume SURFACE.md.
---

# Map The Surface

Build the map before you walk the territory. **You cannot audit a surface you haven't mapped**, and generated codebases reliably hide entry points the author no longer remembers: a debug route, a webhook from a half-finished payments experiment, a second database from when they switched ORMs mid-vibe.

The output is one artifact: `SURFACE.md`. It feeds `/plug-the-holes` (what to attack) and `/launch-gate` (what to verify). Keep it factual; this is reconnaissance, not judgement. Findings come later.

See [../deslop/GLOSSARY.md](../deslop/GLOSSARY.md) for **Surface**, **Tenant isolation**, and the other terms used here.

**Speak the project's language.** If the repo already has a `CONTEXT.md` (the domain glossary used by the architecture/grilling skills), read it first and name things in `SURFACE.md` using its terms ("the Order intake function", not "the FooHandler"). If the codebase is vibe-coded and has no `CONTEXT.md`, and recon forces you to coin a durable name for a core concept (the tenant, a central module), write that term into `CONTEXT.md` (create it lazily) rather than inventing a private synonym. That keeps recon, the audit, and Phase 2 all speaking one domain vocabulary; see the "Vocabulary layers" note in the glossary.

## Process

### 1. Orient

Read the README, `package.json`/manifest, and any config. Answer in one paragraph: what does this app do, for whom, and who are its tenants (orgs? users? both?). If you can't answer "who is a tenant", that gap is itself the first thing to flag. Multi-tenancy you can't describe is multi-tenancy you can't isolate.

### 2. Walk it organically

Explore the codebase (use a subagent to explore if available). Don't grade anything yet. Capture six things:

- **Data models**: every table/collection/schema, and which field ties a row to its tenant (`orgId`, `userId`, `accountId`…). Note any model with **no** tenant key; that's a future Hole waiting.
- **The surface**: every entry point untrusted input can reach:
  - HTTP routes / API handlers
  - Public backend functions / RPC endpoints (whatever `STACK.md` names as your surface unit; mark which are meant to be internal-only)
  - Webhooks and callback URLs
  - File uploads
  - Cron / queue / background consumers
  - Anything the client bundle can call directly
- **Data stores**: every database, bucket, cache, external store. Flag if there's more than one doing the same job (mixed-stack slop) or no backups.
- **Third-party services**: auth provider, payment processor, email, LLM/AI APIs, anything with a key. Note which cost money per call.
- **Money & identity flows**: where authentication happens, where authorisation is *supposed* to happen, and every code path that charges, refunds, or grants entitlement.
- **Secrets**: where config/keys live (`.env`, dashboard, hardcoded?). Don't print secret values into `SURFACE.md`; record *locations* only.

### 3. Write SURFACE.md

Structure it so the audit can be driven straight off it:

```markdown
# SURFACE - <app name>

## What it is
<one paragraph: purpose, users, tenant definition>

## Tenant model
- Tenant = <org | user | …>, keyed by `<field>`
- Models WITHOUT a tenant key: <list - these are pre-flagged>

## Data models
| Model | Tenant key | Holds PII? | Notes |
|-------|-----------|------------|-------|

## Surface (entry points)
| Entry point | Type | Auth expected? | Tenant-scoped? | Touches money? | Notes |
|-------------|------|----------------|----------------|----------------|-------|
<one row per route / public function / webhook / upload / consumer>

## Data stores
| Store | Purpose | Backed up? | Notes |

## Third-party services
| Service | Used for | Key location | Costs per call? |

## Money & identity flows
- Authn: <where/how>
- Authz: <where it's meant to live>
- Charging / entitlement paths: <list>

## Unknowns
<anything you couldn't determine - these get resolved during the audit, not guessed>
```

The **"Auth expected?" / "Tenant-scoped?"** columns are deliberately *claims to test*, not facts; `/plug-the-holes` turns each suspicious row into an exploit test. An honest "Unknowns" section is worth more than confident guesses. A vibe-coded app will have unknowns, and pretending otherwise is how Holes survive the audit.

### 4. Hand off

`SURFACE.md` done → proceed to `/plug-the-holes`. If recon surfaced something obviously catastrophic (a literal API key in the client bundle, an admin route with no auth), note it as **Suspected** and carry it straight into the audit. Don't fix mid-recon, you'll lose the map.
