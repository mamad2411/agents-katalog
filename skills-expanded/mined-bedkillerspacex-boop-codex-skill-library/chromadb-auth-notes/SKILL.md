---
name: chromadb-auth-notes
description: >
  ChromaDB authentication and exposure notes for owned deployments: server authn
  config, multi-tenancy pitfalls, network binding, API token/basic auth patterns,
  and securing vector collections used by RAG. Use when Chroma auth, chroma server
  security, or locking down vector DB endpoints — not for attacking open Chromas.
---

# Chromadb Auth Notes

## Scope And Authorization

- **In scope:** ChromaDB instances and clients you operate (dev/stage/prod).
- **Out of scope:** Scanning the Internet for open Chroma/vector DBs; data theft.
- Vector stores often hold sensitive embeddings of private documents — treat as confidential data stores.
- Pair with `chunking-strategies-rag`, RAG security, `secrets-management-hygiene`, `code-quality-standards`.

## When To Use

- Deploying Chroma server beyond localhost.
- Adding auth tokens / reversing “open by default” lab configs for shared environments.
- Reviewing multi-user RAG apps for cross-tenant collection access.
- Hardening docker-compose Chroma for team use.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Chunking/RAG quality | `chunking-strategies-rag` |
| General LLM prompt injection | `llm-prompt-injection` |
| Postgres/Redis hardening | DB-specific skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Topic | Guidance |
| --- | --- |
| Binding | Prefer private network; never public `:8000` without auth + TLS |
| Auth | Enable server auth per current Chroma version docs (token/basic evolve) |
| Tenancy | Collection naming ≠ authorization; enforce in app |
| Data | Embeddings can leak content via nearest-neighbor attacks — access control matters |
| Clients | Secrets in env; not in browser for privileged admin APIs |

**Note:** Chroma auth features change across versions — always verify against the version you run.

## Workflow

### 1. Confirm scope and success criteria

1. Chroma version, deploy mode (embedded library vs server), data classification.
2. Success: unauthenticated remote access denied; TLS or mesh; app enforces per-user filters; backups protected.
3. Inventory who needs admin vs read.

### 2. Inventory exposure

```bash
# Process / compose
rg -n "chromadb|chroma" docker-compose*.yml *.env || true
ss -lntp | rg 8000 || netstat -an | rg 8000
curl -sS http://127.0.0.1:8000/api/v1/heartbeat || true
```

1. Cloud SG: is 8000 world-open?
2. Is auth env set (`CHROMA_SERVER_AUTH*` style vars — names vary by version)?
3. Are collections holding prod data on a shared dev server?

### 3. Enable authentication (version-specific)

```bash
# Illustrative — confirm exact env keys for your Chroma version docs
export CHROMA_SERVER_AUTHN_PROVIDER="chromadb.auth.token_authn.TokenAuthenticationServerProvider"
export CHROMA_SERVER_AUTHN_CREDENTIALS="generate-long-random-token"
# Server start via docker/k8s with those envs
```

```python
# Client must send auth
import chromadb
from chromadb.config import Settings
client = chromadb.HttpClient(
    host="chroma.internal",
    port=8000,
    headers={"Authorization": f"Bearer {token}"},  # header form may vary
)
```

1. Store token in secret manager; rotate on staff changes.
2. Terminate TLS at ingress/service mesh; avoid cleartext tokens on shared networks.
3. Separate credentials per environment.

### 4. Network and deployment hardening

| Control | Practice |
| --- | --- |
| Listen | Internal only / NetworkPolicy |
| Ingress | Auth + TLS; no public admin |
| Docker | Non-root; read-only where possible; no privileged |
| Persistence | Encrypt volumes; backup access controlled |
| Resource | Limits to avoid noisy neighbor DoS |

```yaml
# k8s sketch
spec:
  containers:
    - name: chroma
      ports: [{ containerPort: 8000 }]
      envFrom: [{ secretRef: { name: chroma-auth } }]
---
# NetworkPolicy: only app pods as clients
```

### 5. Application-level authorization (mandatory for multi-tenant)

Chroma auth often proves **caller is a trusted app**, not **end-user isolation**.

```python
# Always scope queries by tenant metadata you control server-side
results = collection.query(
    query_embeddings=[emb],
    n_results=5,
    where={"tenant_id": current_user.tenant_id},  # enforce; never trust client-alone
)
```

1. Do not let browsers talk to Chroma with a powerful token.
2. Prevent collection name guessing (`tenant_a_docs` vs `tenant_b_docs`) as sole security.
3. Review delete/reset APIs — disable in prod or super-admin only.

### 6. Verify

```bash
# No token → fail
curl -sS https://chroma.internal:8000/api/v1/collections
# With token → success
curl -sS -H "Authorization: Bearer $TOKEN" https://chroma.internal:8000/api/v1/heartbeat
# Cross-tenant test in app: user A cannot query user B metadata filter
```

1. Port scan from outside VPC should not show Chroma.
2. Confirm tokens not in client bundles or git.
3. Backup restore test with auth still enforced.

### 7. Hand off

1. Document version + auth provider config.
2. Rotate procedure; on-call access path.
3. Link RAG pipeline security (prompt injection + data access).
4. Apply `code-quality-standards` to wrappers.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Exposure | Private + auth + TLS | Public Docker port no auth |
| Token | Secret manager, rotated | Token in GitHub issue |
| Tenancy | Server-side metadata filters | Trust collection name from client |
| Client | Backend BFF only | Browser → Chroma admin token |
| Reset APIs | Disabled/protected | Open `/reset` in prod |
| Version | Pin + read auth changelog | Assume auth defaults safe |

## Output Checklist

- [ ] Version and mode documented
- [ ] Network exposure inventoried and locked down
- [ ] Auth enabled and verified (deny without creds)
- [ ] TLS or equivalent in transit
- [ ] App-level tenant isolation tested
- [ ] Admin/reset endpoints restricted
- [ ] Secrets not in git/browser
- [ ] Backups protected
- [ ] Runbook for rotation
- [ ] RAG/chunking skills linked as needed

## Rules

- Treat embeddings as sensitive content.
- Network isolation + auth + app authz are complementary.
- Never expose unauthenticated Chroma to the Internet.
- Verify config against **your** Chroma version docs (APIs evolve).
- Authorized deployments only.
