---
name: moss-wallet-security-review
description: "Reviews an existing MOSS wallet integration for security and correctness before launch on MegaETH. Use when auditing partner code rather than building it: produces findings grouped as Critical, Risky defaults, and Recommendations with concrete remediations. Checks for frontend-owned trust decisions, missing backend SIWE/JWT verification, over-broad or long-lived permission grants, to-only call matching, unguarded silent: true usage, sponsor endpoints that do not decode signed calls or enforce policy/budgets/rate limits, unhandled cancelled/error results, insecure-context passkey failures, and persisted session-key material in frontend storage."
---

# MOSS Wallet Security Review

Audit an existing MOSS integration for security and correctness before launch. This skill **reviews, it does not build** — it inspects partner code (any `@megaeth-labs/wallet-*` package) and emits findings grouped as **Critical / Risky defaults / Recommendations**, each with `file:line`, the risk, and a concrete remediation.

When `moss-wallet-sdk` is also installed, its
`references/behavioral-rules.md` file is the canonical source for
cross-cutting wallet semantics. This review skill remains self-contained for
single-skill installs; enforce the local rules below even if the SDK skill is
not installed.

## Golden rules (what the audit enforces)

1. **The wallet host holds keys, the app never does.** Any code that reads, writes, exports, imports, derives, or persists a private key, seed phrase, or "Recovery Code" is an automatic Critical finding. MOSS is a hosted wallet at `https://account.megaeth.com`.
2. **Trust decisions belong on the backend.** Auth, account linking, sponsorship, and permission escalation must be verified server-side. A frontend that grants access based only on `useStatus().address` (no signature/JWT check) is Critical.
3. **Permission grants are least-privilege.** Every `calls[]` entry needs **both** `to` and `signature`. Short expiry, small spend caps, scoped contracts. `to`-only matching is not the documented model.
4. **`silent: true` requires a matching unexpired grant.** Otherwise it errors unless `silentUIApproveFallback: true`. Unguarded silent calls break or surprise users.
5. **The sponsor endpoint is attacker-reachable.** It must decode the signed
   operation and enforce every inner call. Trusting a separate client-supplied
   target, or omitting call policy, budget caps, or rate limits, is drainable.
   Critical. `sponsorMode: 'everything'` is testing-only.
6. **Methods resolve, they don't throw on cancel.** Every transacting call must branch on `result.status` (`approved`/`cancelled`/`error`). `cancelled` is neutral — never an error toast.

## Audit workflow

1. **Map the integration.** Grep for the package(s) and entrypoints:
   ```bash
   grep -rn "@megaeth-labs/wallet" --include=*.ts --include=*.tsx --include=*.js .
   grep -rn "mega\.\|MegaProvider\|useStatus\|grantPermissions\|sponsorUrl\|silent" src
   ```
   Identify: core SDK vs React vs wagmi connector, whether `wallet-server-verify` is used, and where `initialise`/`MegaProvider config` lives.
2. **Locate the trust boundary.** Find every place the app decides "this user is allowed to X." Confirm each is backed by a server-side `verifySignature` (SIWE) or partner-auth JWT verify call — not by a frontend address read.
3. **Inspect permission grants.** For each `grantPermissions`, check expiry length, `calls[]` shape, spend limits, and whether a revoke path exists.
4. **Inspect sponsorship.** Find `sponsorUrl`/`sponsorMode`/`sponsorToken` and the sponsor endpoint handler. Verify it decodes the signed operation, checks every inner target/selector/value/argument plus sender and chain, and enforces budgets and rate limits.
5. **Inspect result handling.** Every `transfer`/`callContract`/`send`/`swap`/`signMessage`/`signData`/`authenticate`/`grantPermissions` result must branch on `status`.
6. **Inspect storage & context.** Grep `localStorage`/`sessionStorage`/`indexedDB`/cookies for session-key or delegated-signing material. Confirm passkey flows account for secure-context requirements.
7. **Pin versions.** Confirm `@megaeth-labs/wallet-*` deps are pinned to tested versions, not `latest`/`^`-floating across a major.
8. **Emit findings** using the rubric below. Tick the copy-paste checklist.

## Findings rubric

Grep hints are starting points; confirm by reading the surrounding code before flagging.

### Critical — block launch

| Finding | How to detect | Remediation |
| --- | --- | --- |
| Private-key / seed-phrase / Recovery-Code handling | any read/write/export of key/mnemonic/`privateKey`/`seedPhrase`/`recovery` | Remove entirely. MOSS holds keys in the hosted wallet; the app only requests actions. |
| Missing backend verification | login/link gated on `useStatus().address` or `connect()` result with no server call | Add `wallet-server-verify`: server `getMessageToSign` → client `mega.signMessage` → server `verifySignature`. Or JWT: `mega.authenticate()` → backend verify at the partner-auth endpoint. |
| Frontend-owned trust decision | entitlements/roles/balances-of-trust computed client-side from wallet state | Move the decision server-side; treat the frontend address as a claim, not proof. |
| Unrestricted sponsor endpoint | handler trusts a separate `target`, cannot decode batches, or lacks exact call policy / budget cap / rate limit | Decode the signed operation; enforce every inner target, selector, value, relevant argument, sender, and chain plus atomic budgets and rate limits before signing. |
| `sponsorMode: 'everything'` in production | `sponsorMode: 'everything'` in prod `initialise`/`megaWallet`/`MegaProvider` config | Use `app-only` (default) or `explicit`; `everything` is testing-only. |

### Risky defaults — fix before scaling

| Finding | How to detect | Remediation |
| --- | --- | --- |
| Long or variable expiry | `expiry` far in the future, or no upper bound | 24h for active sessions, 7 days max for background agents. Compute `Math.floor(Date.now()/1000) + ttl`. |
| `to`-only call matching | `calls: [{ to }]` missing `signature` | Add the exact `signature` for every entry; never grant `to`-only. |
| Broad spend limits | large `limit`, long `period`, native+token unscoped | Smallest tolerable `limit`; tighten `period`; scope by `token` where possible. |
| Unguarded `silent: true` | `silent: true` with no matching grant and no `silentUIApproveFallback` | Ensure a matching unexpired `{ to, signature }` grant exists, or set `silentUIApproveFallback: true` and handle `silentHasUsedFallback`. |
| Persisted session-key material | session-key / delegated-signing creds in `localStorage`/`sessionStorage`/`indexedDB`/cookie | Do not persist delegated signing material in frontend storage. |

### Recommendations — hardening

| Finding | Remediation |
| --- | --- |
| No revoke path | Expose `mega.revokePermissions()` (revokes ALL grants) in the UI; note users can also revoke per-app in wallet settings. |
| Not subscribed to status | Call `mega.events.onStatusChange(cb)` once (single handler) to keep UI in sync with out-of-app changes. React: gate UI on `useStatus().initialised`. |
| `cancelled`/`error` not handled distinctly | Branch all three: `approved` → success, `cancelled` → reset UI (no toast), `error` → show `result.error`. |
| No secure-context preflight | Passkey/WebAuthn needs a secure context (`http://localhost` OK; trusted https OK; `https://localhost` self-signed and http LAN IPs are refused). Preflight and message the user. |
| Unpinned SDK versions | Pin `@megaeth-labs/wallet-*` to tested versions; verify network (`mainnet` chainId 4326 / `testnet` 6343) matches the deployment. |

## Output format

Produce one section per severity. For each finding:

```
[Critical] Login trusts frontend address with no server verification
  src/auth/login.ts:42
  Risk: Any client can spoof `address` in the request body; backend grants a session
        without proving wallet ownership.
  Fix:  Add wallet-server-verify — server getMessageToSign → client mega.signMessage →
        server verifySignature (single-use, expiring nonce stored server-side).
```

When reviewing code, always include `file:line`. When reviewing a design/PR description with no code, state the assumption and flag the area to inspect.

## Copy-paste audit checklist

```
CRITICAL
[ ] No private-key / seed-phrase / Recovery-Code read, write, export, or persist anywhere
[ ] Auth / account-linking verified server-side (wallet-server-verify SIWE OR authenticate() JWT)
[ ] No trust/entitlement decision computed purely from frontend wallet state
[ ] Sponsor endpoint decodes signed calls and enforces call policy + budget cap + rate limit
[ ] sponsorMode is 'app-only' or 'explicit' in production (never 'everything')

RISKY DEFAULTS
[ ] grantPermissions expiry is short (<=24h active, <=7d agent), never open-ended
[ ] Every calls[] entry has BOTH to AND signature (no to-only)
[ ] Spend limits are minimal, period tight, scoped by token where possible
[ ] silent:true has a matching unexpired grant OR silentUIApproveFallback:true (+ fallback handled)
[ ] No session-key / delegated-signing material in localStorage/sessionStorage/indexedDB/cookies

RECOMMENDATIONS
[ ] A revoke path is exposed (mega.revokePermissions())
[ ] onStatusChange subscribed once; React UI gated on initialised
[ ] result.status branched for approved / cancelled (neutral) / error on every transacting call
[ ] Secure-context preflight before passkey/WebAuthn account creation
[ ] @megaeth-labs/wallet-* versions pinned; network/chainId matches deployment
```

## Method / config surface the audit relies on

| Concern | Authoritative API to check against |
| --- | --- |
| Backend verify (SIWE) | `getMessageToSign(config, address)`, `verifySignature(config, messageToConfirm)`, `Errors.DIFFERENT_MESSAGE` / `Errors.INVALID_SIGNATURE` (`@megaeth-labs/wallet-server-verify`) |
| Backend verify (JWT) | `mega.authenticate()` → `{ jwt }`; backend hits the partner-auth verify endpoint with `origin` + `jwt` |
| Permission grant shape | `mega.grantPermissions({ permissions: { expiry, permissions: { calls:[{to,signature}], spend:[{limit,period,token?}] } } })` |
| Revoke / read grants | `mega.revokePermissions()` (revokes ALL), `mega.getPermissions(address?)` |
| Silent execution | `mega.callContract({ ..., silent, silentUIApproveFallback })`; result `silentHasUsedFallback` |
| Result handling | `TransactionResult.status` = `approved` / `cancelled` / `error` |
| Status sync | `mega.events.onStatusChange(cb)`; React `useStatus().initialised` |
| Sponsorship config | `initialise`/`megaWallet`/`MegaProvider` config: `sponsorUrl`, `sponsorMode` (`app-only`/`explicit`/`everything`), `sponsorToken` |

## References

Cite these as the authoritative basis for each finding:

- [security-model.md](references/security-model.md) — hosted-iframe trust boundary, MOSS UI as the approval surface, partner best practices.
- [best-practices.md](references/best-practices.md) — initialise-early, status subscription, result handling, narrow permissions, sponsor + server-verify hardening.
- [smart-approvals.md](references/smart-approvals.md) — exact permission model, `{ to, signature }` canonical matching, silent-execution rules, security defaults.
- [integration-checklist.md](references/integration-checklist.md) — pre-launch checklist across UX, permissions, gas, security, rollout.
- [audits.md](references/audits.md) — independent audits of the on-chain Normal Account contract (SlowMist, BlockSec, Codex) for the "is the account contract reviewed?" question.

## Scripts

This skill bundles no scripts — it is a review workflow. Drive it with the grep commands above and the checklist.

## When To Switch Skills

- General MegaETH/protocol development review not involving MOSS wallet flows:
  use `megaeth-developer-skills`.
- Building or fixing SDK, React, Smart Approval, paymaster, backend auth, or
  Privy migration code rather than auditing it: use `moss-wallet-sdk`.
- CLI delegated-key operation or protocol execution through `mega moss`: use
  `moss-wallet-cli`.

## Old patterns

<details>
<summary>Stale assumptions to flag during review</summary>

- Treating the app as key-custodial (key/seed/Recovery-Code in app code or storage). MOSS is a hosted wallet; the app never holds keys.
- Trusting `connect()` / `useStatus().address` as proof of identity without a server-side signature or JWT check.
- `to`-only permission entries, or treating loose matching as the default — canonical matching is `{ to, signature }`.
- Calling `silent: true` and assuming it always skips UI — it errors without a matching unexpired grant unless `silentUIApproveFallback: true`.
- Showing an error toast on `status: 'cancelled'` — cancellation is neutral.
- Running an unrestricted sponsor endpoint, or shipping `sponsorMode: 'everything'` to production.
- Saying "seed phrase" — use "Recovery Code".
- Adding a second `QueryClientProvider` under `MegaProvider` (it owns its own) — flag as a correctness bug if seen.
- Floating `@megaeth-labs/wallet-*` on `latest`/wide `^` ranges instead of pinning tested versions.
</details>
