---
name: bazel-remote-cache-auth
description: >
  Authenticated Bazel remote cache for owned CI/developer fleets: remote cache URL,
  credential helpers, mTLS or token auth, read/write separation, and poisoning
  prevention. Use when enabling --remote_cache securely — not for unauthorized
  access to others’ build caches.
---

# Bazel Remote Cache Authentication

## Scope And Authorization

- **In scope:** Remote cache services and Bazel clients you operate (BuildBuddy, bazel-remote, GCS/S3 gateways, etc.).
- **Out of scope:** Reading or writing to third-party caches without authorization; cache poisoning attacks.
- A writable cache is a supply-chain surface — protect upload credentials tightly.
- Pair Java rules with `bazel-java-rules`; use `code-quality-standards` for helper scripts.

## When To Use

- Enabling remote cache for CI to speed builds.
- Separating CI write credentials from developer read-only.
- Configuring mTLS, Google credentials, or Authorization headers for cache.
- Investigating cache misses due to auth failures or ACLs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Java target authoring | `bazel-java-rules` |
| Generic secrets hygiene | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concern | Guidance |
| --- | --- |
| `--remote_cache` | HTTPS endpoint only |
| Auth | mTLS, OAuth, static bearer via credential helper — not world-readable flags in logs |
| ACLs | CI: read+write; devs: read-only if policy requires |
| Poisoning | Only trusted builders upload; verify instance names/namespaces |
| Tooling | Bazelisk, credential helpers, cache server admin, SIEM on upload |

## Workflow

### 1. Confirm scope and success criteria

1. Cache product, network path, trust model (who may upload), authorization.
2. Success: authenticated clients hit cache; anonymous denied; CI writes; unauthorized write fails.
3. Rollback: disable remote flags without breaking local builds.

### 2. Inventory current remote settings

```bash
rg -n "remote_cache|remote_header|google_default_credentials|tls_client" ~/.bazelrc .bazelrc .bazelrc.* 2>/dev/null
bazel info 2>/dev/null | head
```

1. Find credentials in CI secret stores vs checked-in rc files (bad).
2. List service accounts with cache write.
3. Note disk vs remote cache combination.

### 3. Baseline security model

| Principal | Cache access |
| --- | --- |
| Prod CI | Read/write to prod instance |
| PR CI from forks | Read-only or no remote write |
| Developers | Read-only or personal namespace |
| Public | Deny |

### 4. Configure authenticated cache

**`.bazelrc` patterns (secrets via env/helper, not plaintext tokens in git):**

```text
build:ci --remote_cache=https://cache.example.internal/bazel
build:ci --remote_header=Authorization=Bearer PLACEHOLDER
# Prefer credential helper that injects header without printing secret
build:ci --google_default_credentials  # when using GCP REAPI/cache compatible setups
```

**Credential helper sketch:**

```bash
# helper reads from secret store / env and prints flags
#!/usr/bin/env bash
echo "build --remote_header=Authorization=Bearer ${BAZEL_CACHE_TOKEN}"
```

1. Enable TLS; pin CA if private PKI.
2. mTLS: `--tls_client_certificate` / key paths mounted from secret store on CI agents.
3. Separate cache instances or prefixes per trust zone (prod vs OSS PR).
4. Server side: authn required; rate limit; audit logs for puts.
5. Never log full remote headers in verbose CI output.

### 5. Verify with evidence

```bash
# Authorized CI
bazel build //... --config=ci
# Expect remote cache hits/writes in profile or logs without dumping secrets

# Unauthorized
bazel build //... --remote_cache=https://cache.example.internal/bazel
# Expect 401/403
```

1. Confirm fork PR pipelines cannot upload to prod cache.
2. Rotate token and confirm old token fails.
3. Spot-check cache object ACLs not public.

### 6. Observe and harden

1. Metrics: auth failures, upload volume, unusual put spikes.
2. Alerts on anonymous access attempts.
3. Periodic credential rotation and access review.

### 7. Hand off

1. Document configs per environment (`ci`, `dev`).
2. Secret locations and rotation owners.
3. Incident: revoke token, wipe poisoned entries if write was compromised.

## Trust Boundaries

| Boundary | Control |
| --- | --- |
| Fork PRs | No write credentials |
| Dev laptops | Read-only token optional |
| Release CI | Write + signed provenance if available |
| Cache admin | Break-glass only |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Secrets | Helper + CI secret store | `--remote_header` token committed |
| Writes | Trusted builders only | Every developer can poison |
| Transport | HTTPS/mTLS | HTTP cache on corp wifi |
| Forks | Isolated cache or no remote | Same write token as main |
| Logs | Redacted | Bearer token in build logs |

## Output Checklist

- [ ] Cache endpoint and trust model documented
- [ ] Auth mechanism configured (token/mTLS/OAuth)
- [ ] Read/write separation enforced
- [ ] No credentials in git
- [ ] Unauthorized access denied evidenced
- [ ] Fork/PR policy enforced
- [ ] Monitoring/rotation planned
- [ ] Incident revoke path documented
- [ ] `code-quality-standards` applied to helpers

## Rules

- Authorized cache infrastructure only.
- Treat write access as supply-chain critical.
- Never commit cache credentials.
- Prefer least privilege tokens with rotation.
- Do not poison or probe third-party caches.
