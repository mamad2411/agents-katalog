---
name: biswodip-security-review
description: Server-authoritative security review of a codebase: secrets, authentication, authorization, database, money, webhooks, API, files, abuse, errors, logging, supply chain, privacy and AI-feature security, each with an evidence-backed status. Use when asked to review, harden or audit security, check authorization, or find vulnerabilities in code.
license: Apache-2.0
metadata:
  author: Biswodip Goj
  version: 2.2.0
  homepage: https://github.com/Biswadipgoj
---
# Security review — server-authoritative, with a status per control

Phase 8. Review every applicable control before attacking it. Each one gets a status and evidence, never a shrug.

## Non-negotiable

**The client is untrusted.** Never authoritative from the client: `userId` `accountId` `tenantId` `role` `permissions` `isAdmin` `isOwner` `isVerified` `price` `amount` `currency` `fee` `discount` `balance` `paymentStatus` `ownerId` `status`. Client validation is UX; server validation is security. Deny by default, fail closed, re-authorize every request.

Pattern: authenticate → load the object → authorize against server state → compute from server data → validate → act in a transaction → audit.

## Checklist

**Secrets** — nothing in source, bundles, source maps, logs, errors, images, CI output, git history. Watch `NEXT_PUBLIC_*`, `VITE_*`, `REACT_APP_*`, `EXPO_PUBLIC_*`. Found one: stop treating it as safe, identify exposure, rotate, remove, prevent, verify. Never print it.

**Authentication** — opaque server-side sessions, never JWTs in Local/Session Storage, IndexedDB, URLs or readable cookies. `HttpOnly` `Secure` `SameSite`, narrow path, `__Host-` where possible. Rotate on login and privilege change; revoke on logout, password change, MFA change, recovery. Test replay, fixation, reset-token reuse, enumeration, MFA bypass, OAuth `state`/PKCE/redirect allowlist.

**Authorization** — write the matrix (`reports/AUTHORIZATION-MATRIX-TEMPLATE.md`). Test horizontal, vertical, property-level (mass assignment), function-level and tenant isolation, with two identities per role and two tenants. Cover exports, downloads, jobs, admin APIs, GraphQL resolvers, websockets. Kill stale decisions after a downgrade. → `security/AUTHORIZATION.md`

**Database** — parameterised queries, constraints for invariants, transactions for multi-step changes, least-privilege credentials, RLS where available (never *instead of* application checks).

**Money** — integer minor units or exact decimals, never floats. Server-owned state machine, idempotency keys with a unique constraint, row locks for balances, append-only ledger, reconciliation. `HTTP 200` is not a payment. → `security/FINANCIAL-SYSTEMS.md`

**Webhooks** — signature over the raw body, constant-time compare, timestamp window, event-id replay protection, schema and size limits, idempotent processing, out-of-order handling. Reaching your endpoint proves nothing. → `security/WEBHOOKS.md`

**API** — schema validation rejecting unknown fields, body/page size limits, rate limits, CORS (never reflected origin with credentials), CSRF for cookie auth, SSRF defence, no stack traces in production.

**Files** — magic bytes not extensions, size and count limits, randomized names, non-executable storage, authorized downloads, signed URLs with expiry, traversal and zip-slip and decompression-bomb defences, SVG and image-processing risks.

**Abuse** — meaningful rate limits keyed on the right identity, shared store when scaled, not bypassable by header, route, casing or API version. Bound every expensive path with timeouts and concurrency limits.

**Errors and logging** — help the user without helping the attacker; correlation ids; security events auditable and tamper-resistant; never log secrets or unnecessary personal data.

**Supply chain** — committed lockfile, audit output recorded, reviewed install scripts, CI actions pinned by SHA, least-privilege workflow permissions, pinned base images.

**Privacy** — data inventory, minimisation, retention, deletion and export, encryption, tested restore. → `security/DATA-PROTECTION.md`

**AI features** — model output is untrusted input; assume prompt injection from every ingested document; tools get least privilege and act as the end user; confirm irreversible actions outside the model; filter retrieval by tenant in the query; budget tokens and cost. → `references/07-extended-hardening.md` §1

## Automated support

```bash
node bin/biswodip.mjs gates --root . --project-checks --fail-on high
```
Secret candidates are findings to confirm. Risk hints are `UNVERIFIED` pointers, not verdicts. A clean scan proves nothing — it is one input to the evidence matrix.

## Exit gate

- [ ] Every applicable area has a status, with file:line evidence for findings.
- [ ] Nothing marked `VERIFIED` without a procedure and an actual result.
- [ ] Areas that do not apply are `N/A` with a written reason.
- [ ] Gate output saved under `.biswodip/evidence/`.

Deep dives: `security/`. Full sections: `references/MASTER-PROMPT.md` §6–§17, §28, §41. Procedure: `lifecycle/08-security.md`.
