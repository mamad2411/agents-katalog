---
name: audit-secrets-crypto
description: Audit Joomla extensions for exposed secrets, weak or predictable security tokens, unsafe password handling, and cryptographic designs that do not provide their claimed property. Use when reviewing credentials, key material, token generation and comparison, or encryption in a Joomla extension, or when explicitly invoked for a secrets and cryptography audit.
---

# Audit Joomla secrets and cryptography

Audit distributed files and runtime flows for secret exposure, weak authentication tokens, unsafe
password handling, and cryptographic designs that do not provide the property they claim.

## Boundaries

This audit owns credentials and key material, random token generation, token comparison, password
storage, signing, encryption, and key lifecycle.

- Secrets exposed **specifically through** logs, errors, caches, exports, or response headers also
  belong to `audit-sensitive-output`. Cross-reference a shared root cause rather than duplicating it:
  a token that is predictable is this audit's, a correctly-generated token written to a log is
  theirs.
- Whether a webhook request is *authorised* belongs to `audit-authz`; whether its signature is
  *constructed and compared correctly* belongs here.

## What to inspect

- Committed passwords, API tokens, private keys, signing secrets, connection strings, and realistic
  production credentials in source, fixtures, SQL, manifests, build files, and packaged artifacts.
- Secrets embedded in URLs, browser-visible markup, JavaScript, client configuration, exception text,
  telemetry, or values readable by users who do not need them. In Joomla specifically: values reaching
  `$doc->addScriptOptions()` are in the page source for anyone who can load it.
- Tokens, nonces, reset links, API keys, and filenames generated from predictable values — time,
  counters, `rand()`, `mt_rand()`, `uniqid()`, hashes of public data, or too few random bytes. Use
  `random_bytes()` / Joomla's `UserHelper::genRandomPassword()`, not the above.
- Secret and token comparison that leaks timing or tolerates type juggling, truncation, case folding,
  or ambiguous encodings — `==` on two hashes, or a comparison that returns early. `hash_equals()` is
  the answer.
- Plaintext or reversibly encrypted passwords, obsolete password hashes, static IVs or nonces,
  unauthenticated encryption, reused nonces, hard-coded encryption keys, confused signing and
  encryption, and home-grown algorithms.
- Rotation, revocation, expiry, and key separation **where the extension's design claims those
  properties**. An extension that promises revocable API tokens and cannot revoke one is a finding.

### What is not a finding

Examples, obvious placeholders, public keys, hashes, and test-only fixtures provably excluded from
the release package. Joomla-generated secrets are not findings merely because they look like random
strings. Use entropy or format checks for discovery only, then verify the context.

**Never print a complete discovered secret.** Identify its location and type, and show at most a
minimal redacted fingerprint.

## Workflow

### Step 1 — Audit

Report findings ordered by severity:

- **CRITICAL** — a live or plausibly live privileged credential or private key in distributed or
  public material, or trivial forgery of a high-impact authentication token.
- **HIGH** — predictable reset, API, or session-equivalent tokens; plaintext password storage; or
  broken encryption/signature logic exposing protected data or authority.
- **MEDIUM** — secrets exposed to an unnecessarily broad authenticated audience, weak lifecycle
  controls, or exploitation requiring substantial samples or access.
- **LOW** — legacy or fragile cryptography with no demonstrated security impact in its current use.

For every finding state the intended security property, the material or operation involved, the
exposure or failure mode, the attacker's prerequisites, the impact, and a migration-safe mitigation —
with file and line references.

Recommend revocation or rotation where exposure may already have occurred, **without performing it**.

Report and await user feedback. Do not change code in this step.

### Step 2 — Feedback round

The user is a subject matter expert and may reclassify or overrule a finding after giving more
context.

### Step 3 — Plan fixes

Once the user is done giving feedback, check for remaining items to fix.

If none, say so and stop.

Otherwise break the fixes into smaller, individually implementable plans and write them to the
`.gitignore`'d `.plans` directory, clearing any existing files there first. Then propose running
those plans in parallel via subagents, on a cheaper/faster model — the planning work is already done.

---

*Adapted for this suite from the `audit-secrets-crypto` workflow in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. The MIT permission notice accompanies this adaptation;
full text at <https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*
