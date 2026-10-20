# API Gateway Security

## Summary

**One-sentence:** Layered gateway security: TLS termination at the edge, authentication (API keys, JWT, OAuth 2), authorization, secure headers, and WAF integration.

**One-paragraph:** Defines the security controls every API gateway MUST enforce: TLS 1.2+ termination, mutual TLS for service-to-service, JWT verification with JWKS, per-route authorization, OWASP secure-headers pack, and a WAF in front for known attack signatures. Output is a gateway security config artefact plus a periodic posture audit.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'API gateway security' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф конфігу до того, як він потрапить у CI.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Gateway terminates TLS for external traffic.
- Backend services rely on the gateway for authentication or authorization.
- Regulatory regime (GDPR, HIPAA, PCI-DSS, SOC 2) applies to traffic crossing the gateway.

## Skip If (ANY kills it)

- Pure internal service mesh with mTLS already enforced; no external clients.
- Static-content gateway with no auth concerns.
- Dev-only deployment with no PII or regulated data.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| TLS certificate inventory | X.509 cert paths | platform team |
| Identity provider details (JWKS URL, issuer, audience) | config | identity team |
| Per-route auth matrix | table | service owners |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/api-gateway-patterns` | Selects the gateway pattern this config secures. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules + skip-this-methodology fallback | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the security config + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | deep | 6-step procedure: TLS → auth → authz → headers → WAF → posture audit | ~900 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-security-config` | sonnet | Template fill from auth matrix + cert inventory. |
| `design-authz-matrix` | sonnet | Per-route allow/deny synthesis. |
| `posture-audit` | opus | Cross-route policy synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/security.yaml` | Gateway security config: TLS, auth, authz, headers, WAF. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-gateway-security.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[api-gateway-patterns]]
- [[api-gateway-resilience]]
- [[api-gateway-observability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
