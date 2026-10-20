---
name: dex-oidc-connector
description: >
  Configure Dex (dexidp) as an OIDC identity provider with upstream connectors (LDAP, SAML,
  GitHub, Google, OIDC, OAuth2), static clients, redirect URIs, connectors for Kubernetes
  login (kubectl oidc), and claim mapping/groups. Use when Dex config.yaml connectors,
  dex OIDC issuer, kubernetes OIDC authn, Gangway/kubelogin, GitHub org connector, or owned
  cluster SSO via Dex — hand generic JWT abuse tests to api-auth-and-jwt-abuse and SAML
  specifics to saml-sso-basics.
---

# Dex OIDC Connector

## Scope And Authorization

- **In scope:** Dex deployments, clusters, and identity backends you own or administer.
- **Out of scope:** Pointing Dex at third-party IdPs or scraping org directories without authorization; weakening redirect URI validation.
- Prefer staging Dex issuer before production cluster API server cutover.
- Redact client secrets, LDAP bind passwords, and connector tokens from git and tickets.
- Pair with `secrets-management-hygiene`, `saml-sso-basics` (SAML connector), `api-auth-and-jwt-abuse`, and `code-quality-standards`.

## When To Use

- Standing up Dex as OIDC issuer for Kubernetes API, internal apps, or CI.
- Adding/configuring connectors: LDAP, SAML, GitHub, Google, OIDC proxy, etc.
- Mapping upstream groups to Kubernetes `ClusterRoleBinding` subjects.
- Debugging `redirect_uri` mismatch, issuer URL, or group claim missing in tokens.
- Rotating static client secrets and connector credentials.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| SAML protocol deep assessment | `saml-sso-basics` |
| JWT/OIDC client validation bugs | `api-auth-and-jwt-abuse` |
| Generic K8s RBAC design | Kubernetes RBAC skills |
| Passwordless WebAuthn primary | WebAuthn skills |
| Secrets inventory | `secrets-management-hygiene` |
| Code quality baseline | `code-quality-standards` |

## Architecture (mental model)

```text
User → Dex (issuer) → Upstream connector (GitHub/LDAP/SAML/OIDC)
                     ↘ issues ID/access tokens to OIDC client
kubectl / app (client_id) ⇄ Dex token endpoint
K8s API server oidc-issuer-url = Dex issuer
```

| Component | Role |
| --- | --- |
| Issuer URL | Stable HTTPS URL in tokens (`iss`); must match API server config |
| Connector | Authenticates user upstream; returns identity + groups |
| Static client | OIDC `client_id`/`secret`, redirect URIs |
| Storage | Crds/sqlite/postgres/kubernetes for sessions/refresh (HA needs shared storage) |
| Claims | `email`, `groups`, `name`, username claim for K8s |

## Workflow

### 1. Confirm scope and success criteria

1. Environments (dev/stage/prod), Dex version, HA needs, upstream IdP owners.
2. Success: users log in via connector; tokens have expected `iss`/`aud`/groups; kubectl works; no public client secret leakage.
3. Rollback: previous issuer flags on API server documented.

### 2. Inventory current auth path

```bash
# Cluster (authorized)
kubectl -n auth get deploy,svc,ingress -l app=dex 2>/dev/null
kubectl get cm -n auth dex -o yaml 2>/dev/null | head
# API server OIDC flags (managed clusters: check docs/console)
```

1. Note existing IdP, group naming, and who can bind `cluster-admin`.
2. List apps relying on Dex clients.

### 3. Minimal secure Dex config skeleton

```yaml
# config.yaml (illustrative — secrets from env/mounted secret)
issuer: https://dex.example.com/dex
storage:
  type: kubernetes
  config:
    inCluster: true
web:
  http: 0.0.0.0:5556
  # terminate TLS at ingress with trusted cert
telemetry:
  http: 0.0.0.0:5558
staticClients:
  - id: kubectl
    redirectURIs:
      - http://localhost:8000
      - http://localhost:18000/callback
    name: kubectl
    secret: $KUBECTL_CLIENT_SECRET
connectors:
  - type: github
    id: github
    name: GitHub
    config:
      clientID: $GITHUB_CLIENT_ID
      clientSecret: $GITHUB_CLIENT_SECRET
      redirectURI: https://dex.example.com/dex/callback
      orgs:
        - name: your-org
          teams:
            - platform-admins
            - developers
oauth2:
  skipApprovalScreen: true   # only for trusted first-party; understand UX/security tradeoff
enablePasswordDB: false      # prefer upstream IdP; static passwords rarely needed
```

1. **redirectURIs** must be exact allowlist—no wildcards in production.
2. Issuer URL path (`/dex`) must match how Ingress routes and what clients use.
3. Prefer `enablePasswordDB: false` unless lab-only local users.

### 4. Connector patterns

| Connector | Hardening notes |
| --- | --- |
| GitHub/GitLab | Restrict orgs/teams; least-scope OAuth app; secret rotation |
| LDAP | Bind DN least privilege; LDAPS; group search filters tight |
| SAML | Validate certs/ACS; see `saml-sso-basics` |
| OIDC | Upstream issuer pin; reject `alg=none`; proper `aud` |
| Google | Hosted domain restriction when applicable |

1. Map upstream groups to stable strings; document them for RBAC authors.
2. Avoid connectors that allow arbitrary public users if cluster is private.

### 5. Kubernetes API server trust

```text
# API server flags (values must match Dex)
--oidc-issuer-url=https://dex.example.com/dex
--oidc-client-id=kubernetes
--oidc-username-claim=email
--oidc-groups-claim=groups
# optional: --oidc-ca-file for private CA
```

```yaml
# Example binding — owned cluster
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: platform-admins
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: Group
    name: your-org:platform-admins
    apiGroup: rbac.authorization.k8s.io
```

1. Prefer group-based bindings over personal users for ops teams.
2. Use kubelogin/oidc-login plugins with the static client; never embed client secrets in shared world-readable configs if using confidential clients—prefer public + PKCE where supported.

### 6. Verify OIDC surfaces

```bash
# Discovery
curl -sS https://dex.example.com/dex/.well-known/openid-configuration | jq .
# JWKS
curl -sS https://dex.example.com/dex/keys | jq .
# Login smoke: device/browser flow via kubectl oidc-login or gangway
```

1. Decode ID token (lab): confirm `iss`, `aud`, `email`, `groups`, `exp`.
2. Negative tests: wrong redirect URI rejected; user outside org denied; expired token rejected by API server.
3. HA: kill one Dex pod; login still works with shared storage.

### 7. Operate and hand off

1. Alerts: Dex 5xx, connector latency, login failure spikes.
2. Rotate GitHub/LDAP secrets on schedule; restart/reload per Dex version practices.
3. Document break-glass cluster admin certs outside Dex.
4. Apply `code-quality-standards` to any custom connectors or Helm values templates.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Issuer | Stable HTTPS + matching API flags | HTTP issuer in prod |
| Redirects | Exact localhost + known apps | `*` redirect |
| Groups | Org-restricted connector | Any GitHub user is admin |
| Secrets | K8s Secret / external vault | Plain secret in git |
| Storage | HA shared storage | sqlite on single ephemeral pod for prod |
| RBAC | Groups → least privilege | Everyone `cluster-admin` |

## Output Checklist

- [ ] Issuer URL, TLS, and DNS stable and documented
- [ ] Connectors restricted to intended orgs/directories
- [ ] Static clients with minimal redirect URIs
- [ ] Secrets externalized and rotatable
- [ ] API server OIDC flags match Dex claims
- [ ] Group → RBAC mappings least privilege
- [ ] Discovery/JWKS and login smoke pass
- [ ] Negative redirect/org tests pass
- [ ] HA/storage and break-glass documented
- [ ] Monitoring and rotation runbook updated

## Rules

- Dex is a critical auth component—treat config changes as security changes.
- Never broaden redirect URIs or org filters to “make it work” without review.
- Fail closed: unknown users get no cluster groups.
- Keep SAML/JWT deep dives in neighbor skills.
- Authorized clusters and IdPs only; redact secrets always.
