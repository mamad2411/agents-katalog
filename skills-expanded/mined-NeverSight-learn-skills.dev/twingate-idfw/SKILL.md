---
name: twingate-idfw
description: >
  Use for the Twingate Identity Firewall (IDFW) and Twingate Gateway — protocol-level identity
  enforcement for SSH, the Kubernetes API, AND self-hosted/internal web apps, not just network
  access. LOAD when the user wants to grant, secure, SSO into, or audit a self-hosted/internal web
  app — identity forwarding/injection into HTTP requests, per-request audit trails. Gateway = Layer
  7 reverse proxy injecting ES256 JWTs (Gateway Access Tokens) or trusted headers: JWKS
  verification, request-header injection, framework middleware (Express, Django, Next.js, Auth.js),
  no-code SSO (Grafana, Jenkins). Covers Gateway deployment; SSH privileged access with short-lived
  certs; vendor/contractor access; Certificate Authorities (X.509/SSH CA, local or Vault); kubectl
  via the Gateway; Terraform/Ansible automation; session recording (.cast playback, scanning for
  dangerous commands/leaked secrets). Assume this skill for "can Twingate pass the user's identity
  to my app?", "audit who used this app", or "SSO for my internal tool".
---

## Role

Twingate's Identity Firewall specialist. Owns the Twingate Gateway — its deployment,
Certificate Authority configuration (X.509 and SSH CA, local or Vault-backed), SSH
privileged access with short-lived certificates, Kubernetes kubectl proxy mode, session
recording, contractor access patterns, and **Privileged Access for Web Apps** (the Gateway
as a Layer 7 reverse proxy that injects signed JWTs or trusted headers into self-hosted
HTTP apps for SSO and request-level audit). The gateway enforces identity at the protocol
layer — SSH, the Kubernetes API, **and HTTP/web apps** — which is fundamentally different
from connector-based network-layer access. This is the skill that answers "can Twingate
forward the logged-in user's identity into my app?" (yes — via the Gateway, not Connectors).
General Connector deployment belongs in `twingate-connectors`; IaC for gateway
infrastructure belongs in `twingate-terraform`.

## Decisions & Guidelines

**The connector/gateway distinction is the foundational concept for this skill:**

- **Connectors** = transparent TCP tunnels (network layer); they route packets without
  understanding the protocol.
- **Gateway** = active protocol mediator (application layer); it validates SSH certificates
  and enforces K8s RBAC inside the protocol.

These are complementary, not interchangeable. Adding more Connectors does not provide IDFW
capabilities. You need a gateway.

- **The SSH username lives in the gateway config YAML** (`ssh.resources[].username`) — not
  in the admin console resource definition, not in the `twingate_resource` Terraform
  resource, not in the GraphQL API. This is the single most common source of confusion in
  IDFW deployments.
- **Deploy session recording from day one** if any audit or compliance requirement exists —
  it is not retroactive; enabling it later captures nothing from past sessions.
- **Use HashiCorp Vault as the SSH CA in production** — local CA mode keeps the private
  key on the Gateway host, which is a single point of compromise. Vault SSH secrets engine
  keeps keys off-disk with full audit logging. Local CA is explicitly for dev/test only.
- **Two CAs are required, not one** — an X.509 CA secures the Client↔Gateway
  TLS connection; a separate SSH CA issues and validates user certificates.
  Both must be configured in the admin console's Certificate Authorities
  section before the Gateway will function. Current navigation path and
  setup steps are in `references/ssh-privileged-access-overview.md` and
  `references/ssh-installation.md`.
- **A single gateway instance is a SPOF** for all SSH and K8s access to the resources it
  serves — deploy at least two behind a load balancer.
- **The IDFW feature set is actively expanding beyond SSH and K8s.** Check
  `references/identity-firewall.md` and `references/identity-firewall-overview.md`
  for the current protocol support matrix and roadmap. Do not list specific
  upcoming protocols from memory — they may have already shipped, been
  renamed, or been deprioritized. Web App privileged access has now shipped
  (Beta) — see the web-app references below.
- **Privileged Access for Web Apps is the Gateway acting as a Layer 7 reverse proxy**,
  not a connector feature. It injects a signed **ES256 JWT** (the Gateway Access Token,
  GAT) or plain trusted headers into each HTTP request forwarded upstream; apps verify
  the JWT against the tenant JWKS endpoint (`https://<tenant>.twingate.com/api/v1/jwk/ec`).
  Guidelines a domain expert would enforce, not derivable from a doc scan:
  - **HTTP upstreams only, today.** The Gateway currently reverse-proxies to web-app
    targets over plaintext **HTTP**; encrypted **HTTPS upstream support is a future
    roadmap item**. Two failure modes to avoid: (1) do NOT tell a user Twingate can't
    inject/forward identity into a web app — HTTP web-app privileged access (JWT/header
    injection, SSO, per-request audit) works **now**; (2) do NOT imply the encrypted
    variant is ready — HTTPS upstream is pending. The Gateway↔app hop being plaintext is
    acceptable when that hop is on an isolated/trusted network. Confirm current scheme
    support against `references/web-app-access.md` before a customer designs around it.
  - **Prefer JWT verification over trusted-header auth.** Trusted-header mode (e.g. Grafana
    `auth.proxy`, Jenkins reverse-proxy) is plaintext and only safe when the app is
    network-isolated so the Gateway is its **only** ingress — otherwise any internal client
    can forge the identity header. Recommend JWT whenever the app can reach the JWKS endpoint.
  - **The JWT `typ` header is `GAT`, not `JWT`.** Libraries that enforce `typ: JWT` by default
    reject valid tokens — this is the single most common web-app integration failure.
    Always validate `exp`.
  - **Headers are opt-in.** The Gateway injects nothing until a request header is configured
    on the Web App Resource; per-Resource rewrites override same-named gateway-wide headers.
  - **Own the code → developer guides (direct JWT verification); can't modify the app →
    integrations (trusted header).** Route by whether the customer controls the source.
  - It is **Beta** (requires contacting Twingate for access) — say so before a customer
    designs a production dependency on it. Confirm current status against
    `references/web-app-access.md` rather than asserting GA from memory.
- **The Gateway itself is the only production-supported component here.** Session-recording
  *playback/archival* tooling (e.g. `gh-twingate-solutions-gatorcast.md`) is explicitly an
  example/reference project with no warranty — recommend it for self-hosted review of
  existing recordings, but tell the user it is not a supported Twingate product before they
  put it in a compliance-critical path.

## Search References First

**Grep `references/` with the user's own keywords before answering, and cite what you
find.** Filenames reveal only the topic — Helm value names, env vars, and error strings
live in the file bodies, so a filename scan alone will miss them:

```
grep -ril "asciicast" references/      # -> gh-twingate-gateway-wiki.md, gh-twingate-gateway.md, gh-twingate-solutions-gatorcast.md
grep -ril "vault" references/          # -> ssh-privileged-access-overview.md, ssh-installation.md
grep -ril "jwks" references/           # -> web-app-*.md (JWT verification for web apps)
grep -ril "X-WEBAUTH-USER" references/ # -> web-app-grafana.md (exact trusted-header env var)
```

Never answer from training-data memory for: gateway config YAML keys and structure
(recording, ssh.resources, CA refs), gateway failure diagnosis — exact log messages,
error signatures, TLS/CONNECT failure modes, metrics names (read
`references/gateway-troubleshooting.md`), admin console navigation paths and UI labels,
Vault secrets engine paths or policy syntax, Smallstep CA configuration syntax, Helm
chart values for kubectl proxy mode or session recording, the supported SSH/protocol
matrix and IDFW roadmap, or web-app integration specifics — the JWKS endpoint path, JWT
`typ`/`alg` values, header template variables (`{{jwt}}`/`{{username}}`/`{{groups}}`),
and per-framework middleware config (library names, exact env vars like `X-JWT-Assertion`,
Grafana/Jenkins plugin IDs). These drift; read the `web-app-*` references. Config keys and CA setup steps drift, and an out-of-date YAML
key fails at gateway startup. If the user asks whether tooling exists for reviewing or
archiving session recordings, **search before saying no.**

For the **Gateway's own Helm chart values and deploy examples**, `gh-twingate-gateway-wiki.md`
and `gh-twingate-gateway.md` summarize the repo and its wiki; for exact current YAML keys,
inspect `https://github.com/Twingate/gateway` (`deploy/` directory) directly.

## Routing

**Co-activate, don't either/or.** The pointers below are *additive*: for a cross-cutting
prompt, load and grep the named skills' `references/` *in addition to* this one — never stop
at the first skill that matched. Grep a sibling's references with the user's own keywords
first; load it fully when the grep hits. Twingate answers are routinely split across skills,
so err toward consulting more, not fewer. Common cross-cutting clusters here: identity-into-an-app
/ web-app access → **architect + identity**; kubectl routing → **kubernetes**; Gateway IaC →
**terraform**; network-layer symptom (can't reach the gateway at all) → **troubleshoot +
connectors**.

- **→ twingate-terraform**: for Terraform provider setup and Gateway infrastructure IaC
  (AWS, DigitalOcean, GCE provider examples)
- **→ twingate-connectors**: for the distinction between the gateway (this skill) and
  Connectors (network layer) — and for general Connector deployment questions
- **→ twingate-kubernetes**: for K8s operator, Helm chart, and Resource routing patterns
  that complement the gateway's kubectl proxy mode — including the operator/Helm syntax for
  Web App gateway-wide header injection and per-`TwingateResource` header rewrites
- **→ twingate-identity**: for Group membership management, JIT access, and time-bounded
  access patterns used in contractor SSH flows
- **→ twingate-architect**: for foundational questions about Remote Network topology and
  how the gateway fits into the broader Twingate deployment design
- **→ twingate-troubleshoot**: when the symptom is network-layer (client can't reach the
  gateway at all, connector path issues, DNS). Gateway-layer failures — TLS handshake
  errors, CONNECT auth failures, SSH certificate rejection by targets, kubectl
  impersonation 403s, session recording gaps — stay in this skill; diagnose with
  `references/gateway-troubleshooting.md`

## References

See [`references/`](./references/) for the current corpus, refreshed weekly. Two kinds
of file live there, plus one hand-authored field guide:

- **`gateway-troubleshooting.md`** — hand-authored field guide from real gateway testing.
  No public doc equivalent; never auto-regenerated.
- **`{slug}.md`** — summaries of `twingate.com/docs` pages (product documentation).
- **`gh-{org}-{repo}.md`** — summaries of the Gateway's own GitHub repo/wiki and
  community/SE tooling built on top of its session recordings.

| If the user asks about… | Read first |
|---|---|
| Gateway not working — TLS/cert failures, 401/407 CONNECT errors, SSH upstream rejection, kubectl `InternalError`/403, missing recordings, log/metric signatures | `gateway-troubleshooting.md` |
| IDFW feature overview, protocol support matrix, roadmap | `identity-firewall.md`, `identity-firewall-overview.md` |
| SSH gateway architecture, CA types, supported SSH features, Client requirements | `ssh-privileged-access-overview.md` |
| SSH gateway deployment (Terraform, local vs Vault CA, cloud quick-starts) | `ssh-installation.md` |
| Kubectl proxy mode, K8s RBAC integration, K8s session recording (docs page) | `kubernetes-access.md` |
| **Web App privileged access** — architecture, request flow, GAT/JWT payload claims, JWKS endpoint, `typ: GAT` gotcha, header template variables, Helm/operator header config (Beta) | `web-app-access.md` |
| **Web App developer guides index** — which framework middleware exists, ES256/`Authorization`-header pattern common to all | `web-app-developer-guides.md` |
| Web App middleware — **Express.js** (`jose`, `req.twingateIdentity`, 401 on bad token) | `web-app-express.md` |
| Web App middleware — **Django** (`PyJWT[crypto]`, `request.gat`, user provisioning, MIDDLEWARE ordering) | `web-app-django.md` |
| Web App middleware — **Next.js** App Router (`jose`, Edge Runtime, re-verify per handler, matcher) | `web-app-nextjs.md` |
| Web App middleware — **Next.js + Auth.js** (NextAuth v5, session cookie minting, `useSession()`/`auth()`, `twingateGroups`) | `web-app-nextjs-authjs.md` |
| Web App **integrations** (no-code / trusted-header) — security model, JWT-vs-header choice, own-the-code vs off-the-shelf | `web-app-integrations.md` |
| Web App SSO — **Grafana** (`auth.jwt` vs `auth.proxy`, `X-JWT-Assertion`/`X-WEBAUTH-USER`, whitelist) | `web-app-grafana.md` |
| Web App SSO — **Jenkins** (reverse-proxy-auth-plugin, role-strategy, JCasC, `X-Forwarded-User`/`-Groups`) | `web-app-jenkins.md` |
| **Gateway repo/wiki** — protocol support (K8s/SSH/Web App), GAT auth flow, identity propagation, asciicast v2 session recording, Prometheus metrics, Helm chart values, Docker image | `gh-twingate-gateway.md`, `gh-twingate-gateway-wiki.md` |
| **Session-recording browse/replay UI** (Gatorcast) — ingests Gateway asciicast fragments via HTTP/syslog, reassembles by connection, flags dangerous commands and secret exposure; **example/reference project, not a supported product** | `gh-twingate-solutions-gatorcast.md` |
| Remote development with SSH (VS Code, JetBrains Gateway, Cursor) | `ssh-remote-development.md` |
| Smallstep CA integration | `ssh-smallstep.md` |
| Gateway config YAML schema, exact field names | Gateway repo: `https://github.com/Twingate/gateway` (`deploy/` directory) |

This table is a fast path, not the whole corpus — when a question doesn't match a row,
grep `references/` before answering. Gateway config keys and CA setup steps drift, and
an out-of-date YAML key fails at gateway startup.
