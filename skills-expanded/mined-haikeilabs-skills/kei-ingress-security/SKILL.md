---
name: kei-ingress-security
description: Fail-closed security invariants for a chat-bot ingress boundary in front of Kei-governed tools (for example a customer assistant that receives Microsoft Teams / Bot Framework activities). Use when building or reviewing the ingress service's feature flags, token verification, SSO or OBO exchange, principal derivation, enrollment allowlist, idempotency, pseudonymous audit, or a pinned policy-governor subprocess. Also use for pen-test or security-review findings about error bodies, 401 or 412 responses, unknown vs expired token errors, requests to add debug detail to deny responses or audit, JWT audience or issuer checks, a new environment feature flag, or importing a downstream token mint outside the composition root. Also use when someone says "dark by construction", "accept-any token", or "fails closed". Keep generic tool-call middleware guidance in agentware-sdk.
---

# Ingress security — fail-closed invariants

An ingress boundary authenticates inbound bot activities, derives a principal, gates it,
and either replies with a closed diagnostic or hands a verified grant to ONE composed tool
lane. A hardened boundary has no LLM, no generative seam, and no "accept anything" path.

Deny responses stay indistinguishable. Every token-verification failure returns the
same `401 {"error":"unauthorized"}`, whether the token is unknown or expired. The reason
goes only to the pseudonymous audit, as a closed code. Never enrich an error body or an
audit reason to help debugging: that breaks invariant 4 (closed verifier code set) and
invariant 5 (pseudonymous, closed-code audit), and it leaks gate internals.

Three more answers come up often:

- A new environment flag is strict-equality to the literal `"true"` (`"TRUE"`, `"1"` and
  `" true "` are off), and the disabled path is dark by non-construction (invariant 1).
- A verifier that accepts any valid JWT from a known issuer without checking the audience is an
  accept-any-token vulnerability (invariant 4): verification must enforce audience and issuer
  and fail with a typed verification error carrying a closed code.
- Tool lanes never import a downstream token mint. The composition root is the one production
  import site, enforced by a lint rule and a source-scan test (invariant 11).

Keep these answers short, but always name the invariant by number and say what it pins: for
an error-body or deny-reason question, cite invariant 4 (closed verifier code set) and
invariant 5 (pseudonymous audit); for an audience question, call it an accept-any-token
vulnerability and say the verifier fails with a typed error carrying a closed code.

Every change must preserve the invariants below. Back each one with a test; weakening one is
a security regression, never a test convenience.

## The invariants

1. **Master switches are strict-equality, fail closed.** A feature flag such as `BOT_ENABLED`
   is `true` ONLY for the literal `"true"`. `"TRUE"`, `"1"`, `" true "` are OFF. A disabled
   path must be **dark by non-construction**: its objects are never built, so they make zero
   token/process/network/filesystem calls. Do not replace non-construction with a runtime
   `if (enabled)` check that still builds the components.
2. **Tool lanes are mutually exclusive per process.** Two lane flags both true is a refused
   startup, never a precedence rule. There is exactly one verified-grant callback.
3. **Secrets are presence-only in config.** The config object records that a secret is
   configured (a boolean), never the value. The raw value flows env → composition root →
   the SDK credential factory, and is never stored, serialized, or logged.
4. **No accept-any-token implementation anywhere.** Verification throws a typed error with a
   closed code set; unknown codes map to `other`. The disabled path uses a deny-all verifier.
5. **Audit is pseudonymous and closed.** Attacker-influenced identifiers are pseudonymized
   (keyed hash) before audit; activity types and verifier codes go through closed sets.
   Audit `reason` strings are fixed constants — never reflect user text, token text, or
   upstream error text into audit.
6. **Every gate uses validated fields only.** Message *text is never authority*. "Addressed"
   comes from the audience class plus a verified bot mention, not from text. The tenant gate
   compares the declared tenant and the token's `tid` against the single trusted tenant from
   config. Origin requires a trusted Connector host suffix AND a matching `serviceurl` claim.
7. **Idempotency is scoped, not bare.** The key is scoped to (tenant id, conversation id,
   activity id) — never an attacker-chosen bare activity id. Reserve after
   sender/principal/enrollment validation; commit on success AND expected failure; release on
   throw so a corrected redelivery can retry. A duplicate is acknowledged with zero reprocessing.
8. **Enrollment gates a pilot.** An allowlist of approved directory object IDs admits users;
   the not-enrolled reply is generic and reveals nothing. This is distinct from Kei's
   claim-link enrollment for chat-platform users — see `kei-harness-setup` and `kei-api`.
9. **Outbound capability is object identity.** Claiming an outbound turn takes the verified
   identity object itself as the capability, so a copied or fixture identity cannot reach the
   Connector. With no outbound wired the pipeline is outbound-dark.
10. **A policy governor is pinned and binding.** Executable path, script path, cwd, and script
    SHA-256 are pinned inputs validated at startup; the child runs with isolated interpreter
    flags (for Python, `-I -B`), an EMPTY environment, bounded stdout, and a lifetime backstop,
    and the script bytes are re-hashed from a no-follow descriptor before every spawn.
    Decisions are bound to the exact request (request/proposal ids, actor and identity refs,
    canonical tuple, exact role list, version pins); anything that does not bind is a replay
    and collapses to `unavailable`.
11. **The composition root owns the mints.** Only the composition root imports the downstream
    token mints, enforced by a lint rule and a source-scan test. Tool lanes never import them.
12. **Startup is eager and fail-stops.** When enabled, every pin is validated in one pass and
    every component is constructed before any socket opens. A mis-deployed artifact or a
    missing variable refuses to start rather than degrade.

## The message pipeline order (do not reorder)

POST messaging endpoint → method must be POST → master switch → body size cap →
`Authorization: Bearer` present → strict JSON parse → token verification → activity parse →
tenant gate → type dispatch (`message`, or `invoke` only when an SSO gate is wired) →
trusted origin → mention gate (channel/group need a verified mention) → principal derivation →
enrollment → idempotency reserve → lane routing / SSO card / handoff / diagnostic → commit.

## Validation

- Run the repo's typecheck, lint, and full test suite; never skip the security slices.
- Each invariant above has at least one negative test (disabled flag makes zero calls, hostile
  origin denied, audit contains no raw identifiers, verifier failure is a closed code).
- `npm audit --omit=dev --audit-level=high` (or the language equivalent) passes.

## Realistic usage boundaries

- **Do not** loosen a gate to make a test pass. A failing test usually asserts a real
  invariant that the change broke.
- **Do not** add environment variables for things that are deliberately source constants
  (deadlines, scope allowlists, fixed selections, interpreter flags). A value an operator can
  set is a value a misconfiguration can widen.
- **Do not** store, echo, or log token values, bot passwords, relay tokens, or secret-store
  references that resolve to secrets.
- **Do not** implement fuzzy or LLM-driven routing inside the ingress. Message→selection
  stays a closed, deterministic parser (see `kei-tool-adapters`).
- **Do not** treat docs as authority over code; the code and its tests are the contract.
- When adding a gate: deny via a fixed outcome code, a closed audit `reason`, a bounded HTTP
  status, and no reflection of attacker input. Add a negative test and an audit-pseudonymity
  assertion.

## Related skills

- `kei-teams-ingress` — Microsoft Teams and Bot Framework mechanics.
- `kei-tool-adapters` — the protected tool-lane pattern a verified grant is delivered to.
- `agentware-sdk` — generic middleware policy/audit guidance for harnesses.
