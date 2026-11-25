---
name: security-threat-checklist
description: >
  Apply this skill for ALL security-relevant work: reviewing or writing code, designing architecture,
  implementing auth, handling secrets, deploying contracts, building APIs, or doing infra changes.
  Trigger whenever the task touches: auth/login, payments/withdrawals, contracts, API endpoints,
  secrets/config, database writes, admin operations, upgradeability, indexer/replay logic, or
  frontend that talks to wallets. Also trigger when user asks about "is this secure?", "security review",
  "threat model", or "what could go wrong?". When in doubt, apply this skill — security is cheaper before shipping.
---

# Security Threat Checklist (DoD Requirement)

## Trigger: apply this skill when the PR/task touches
- Public/external endpoints (HTTP or on-chain functions)
- Auth, signatures, wallet login, session management
- Payments, claims, withdrawals, rewards, any value transfer
- Smart contract logic, upgradeability, or storage layout
- Secrets, environment variables, config, infra
- Indexer or DB writes, event replay, reorg handling
- Admin operations, role/permission changes
- Frontend code that signs messages or sends transactions

---

## Definition of Done — security gate

All must be ✅ before merging:

- ✅ Threat model filled (or explicitly "no new surface area")
- ✅ No secrets in code, logs, errors, or test fixtures
- ✅ All checklist items for the affected layers reviewed
- ✅ Required scans + tests are green (see bottom)

---

## 1. Threat Model (fill when surface area changes)

```
Protected assets:   funds | game state | PII | availability | admin keys
Entrypoints:        HTTP routes | public/external contract funcs | upgrade paths
Actors:             user | bot | attacker | admin | keeper | protocol
Trust boundaries:   client→API | API→DB | API→RPC | contract→oracle | contract→external
Top threats (≥3):   [threat] → [mitigation]
Assumptions:        oracle/VRF trust | admin key custody | upgrade governance | chain finality
Residual risks:     known gaps accepted, with owner and review date
```

**Threat examples by layer (pick relevant ones):**
- API: IDOR, auth bypass, mass assignment, injection, DoS via expensive query
- Contracts: reentrancy, price manipulation, front-running, access control bypass, logic bug in math
- Infra: secret leak, supply chain compromise, misconfigured CORS/headers, over-permissioned IAM
- Frontend: XSS, phishing via compromised bundle, malicious wallet prompt, clickjacking

---

## 2. Secrets & Configuration

**Never:**
- Hardcode secrets, keys, mnemonics, or tokens anywhere (code, tests, examples, docs, `.env` committed)
- Log request bodies, auth tokens, private keys, or full user PII
- Expose stack traces or internal error messages to clients
- Use the same credentials across environments

**Always:**
- Load secrets from environment variables or a secret manager (Vault, AWS Secrets Manager, GCP SM)
- Rotate secrets immediately on suspected compromise — don't defer
- Apply least-privilege: each service/key gets only the permissions it needs
- Sanitize and mask sensitive fields before logging (`password`, `token`, `mnemonic`, `privateKey`)
- Separate prod/staging/dev secrets entirely — no sharing

---

## 3. Web2 / API Security

### Authentication & sessions
- Tokens must have expiry; implement revocation (blocklist or refresh-token rotation)
- Session fixation: regenerate session ID on login
- Wallet login (SIWE): nonce per request + expiry + chain ID + anti-replay; support ERC-1271 for smart wallets
- MFA for admin endpoints; hardware key for production deploys

### Authorization
- Object-level authorization on every endpoint — verify the requesting user owns the resource, not just the role
- Avoid mass assignment: allowlist accepted fields, never spread raw request body into DB
- Privilege escalation: changing role/permission requires elevated auth, not just any authenticated user

### Input & output
- Validate schema at the boundary (zod, pydantic, joi) — type, length, range, format
- Reject or truncate oversized payloads before processing
- Parameterized queries only — no string interpolation into SQL/NoSQL
- Strip or encode output to prevent XSS in any HTML-rendered context

### API hardening
- Rate limiting: per-IP and per-authenticated-user, stricter on auth endpoints (brute-force prevention)
- Idempotency keys on non-idempotent critical endpoints (payments, transfers)
- CORS: allowlist specific origins; never `*` on authenticated APIs
- Security headers: `Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`
- Pagination + depth limits on any query that returns lists — never unbounded

### Error handling
- Return generic errors to clients; log detail internally with correlation ID
- Never include file paths, query text, stack traces, or env info in API responses
- Fail closed: ambiguous auth → deny; unexpected state → reject, not proceed

---

## 4. Web3 / Smart Contract Security

### Access control
- Every state-changing function must have explicit access control — no implicit "anyone can call"
- Prefer `AccessControl` (multi-role) over `Ownable` for contracts with multiple admin actors
- Production contract ownership → multisig (Gnosis Safe) + timelock; never a bare EOA
- `authorizeUpgrade` must be protected; upgrades require multisig approval

### Reentrancy
- Follow Checks-Effects-Interactions (CEI) strictly — update state before any external call
- Add `ReentrancyGuard` on functions that transfer value or call external contracts
- Prefer pull-payments (withdraw pattern) over push — caller pulls their own funds

### Randomness
- VRF only (Chainlink VRF or equivalent) for any outcome with real value
- `block.timestamp`, `blockhash`, `prevrandao` are miner/validator-influenceable — never use for prizes or game outcomes

### Math & value handling
- Solidity 0.8+: overflow protection is native; use `unchecked` only with explicit justification + test
- Rounding: be explicit about floor vs ceiling; ensure protocol never loses funds due to rounding
- Division before multiplication loses precision — always multiply first

### Oracle & price manipulation
- Never use spot price from an AMM as a price oracle — use TWAP (minimum 30-min window)
- Validate oracle data: timestamp freshness, round completeness, price within sanity bounds
- Circuit breakers: pause protocol if price deviates beyond threshold

### MEV & front-running
- Identify functions where ordering matters (auctions, claims, liquidations)
- Mitigations: commit-reveal, batch auctions, slippage bounds, private mempool (Flashbots Protect)
- Front-running is a design problem — document explicitly what's acceptable and what's not

### Upgradeability (if used)
- Use namespaced storage (ERC-7201) to avoid storage collisions
- Verify storage layout before and after every upgrade (`@openzeppelin/upgrades-core`)
- Initializer safety: `_disableInitializers()` in constructor; never leave `initialize()` callable twice
- Timelock on upgrades — give users time to exit before changes take effect
- Every upgrade is a new audit surface — treat it like a new deployment

### Gas & DoS
- No unbounded loops over user-controlled arrays
- No `transfer()` / `send()` — use `.call{value: ...}("")` with return value check
- Limit external call gas when appropriate to prevent griefing

### tx.origin
- Never use `tx.origin` for authorization — use `msg.sender`

---

## 5. Frontend Security

### Wallet & signing
- Display exactly what the user is signing — never blind-sign opaque bytes
- Use typed structured data (EIP-712) for all off-chain signatures
- Validate `chainId` and contract address in signing payloads before presenting to wallet
- Warn users explicitly before actions that are irreversible

### Content security
- CSP headers to prevent XSS: restrict `script-src`, `connect-src` to known origins
- Subresource Integrity (SRI) on any externally loaded scripts
- Sanitize any user-generated content rendered as HTML
- No sensitive data (keys, tokens) stored in `localStorage` — use `sessionStorage` or memory only

### Supply chain
- Pin CDN script versions and use SRI hashes
- Audit npm/yarn lockfile for unexpected changes on each dependency update
- No unvetted third-party scripts with access to wallet context (analytics, chat widgets, etc.)

### Phishing surface
- Use a consistent, recognizable domain — document it to users
- Never ask users to enter seed phrases or private keys in the UI, ever
- Be explicit about what permissions a wallet connection grants

---

## 6. Infrastructure & Supply Chain

### Secrets in CI/CD
- CI secrets scoped to minimum — separate deploy keys per environment
- Never print env vars in CI logs (`set -x` in shell scripts leaks everything)
- Rotate CI secrets on any team member offboarding

### Dependency security
- Pin exact versions in lockfiles — no `^` or `~` in production
- Run SCA on every CI run; block on critical CVEs
- Before adding a new dependency: check last commit date, maintainer count, license, transitive deps
- Don't add a library for something implementable in < 50 lines

### Container & infra
- Minimal base images (distroless or alpine) — fewer packages = smaller attack surface
- Never run containers as root in production
- Network policies: deny by default, allowlist needed connections only
- IAM: no wildcard permissions; use roles, not long-lived access keys where possible

---

## 7. Required Scans & Tests (minimum before merge)

| Check | Tool | Blocks merge? |
|---|---|---|
| Secrets scan | `gitleaks` | ✅ Yes |
| Dependency CVEs | `osv-scanner` | ✅ Yes (critical) |
| SAST (backend/frontend) | `semgrep` | ✅ Yes |
| Solidity static analysis | `slither` + `aderyn` | ✅ Yes |
| Contract tests | `forge test -vvv` | ✅ Yes |
| Storage layout check | `@oz/upgrades-core` | ✅ Yes (on upgrades) |
| Web2 auth tests | project test suite | ✅ Yes (on auth changes) |
| Fuzz / invariant tests | `forge` fuzz/invariant | Recommended |
| E2E with simulated wallet | Playwright + Anvil | Recommended |

**On any secrets scan finding:** treat as P0 — rotate the secret before merging, even if "it was just a test."

---

## 8. Incident & Escalation

- Credential exposed → rotate immediately, open P0 incident, post-mortem required
- Contract bug with funds at risk → evaluate pause, contact security multisig, do NOT fix silently
- Dependency with critical CVE → block deploy, patch in isolated PR, re-run full scan
- Any finding accepted as risk → document: what, why accepted, owner, review date