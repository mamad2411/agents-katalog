---
name: bentoml-service-auth
description: >
  Authentication and authorization for owned BentoML model services: API tokens,
  OAuth/OIDC at the edge, network policies, TLS, secrets for model artifacts, and
  avoiding open inference endpoints. Use when hardening BentoML/Yatai deployments —
  not for attacking exposed model APIs without authorization.
---

# BentoML Service Auth

## Scope And Authorization

- **In scope:** BentoML services and deployment platforms you own (local, K8s, cloud).
- **Out of scope:** Unauthorized probing of third-party inference APIs; model theft.
- Open inference endpoints can leak data and burn GPU budget — default deny anonymous.
- Use `code-quality-standards` for service code; K8s identity skills when on AKS/EKS.

## When To Use

- Exposing a BentoML service beyond localhost.
- Adding API key/JWT auth or putting service behind API gateway/mesh.
- Reviewing runners for missing authn/z and TLS.
- Securing model download credentials and artifact stores.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic BFF cookie sessions | `bff-cookie-session-pattern` |
| AKS workload identity | `azure-aks-workload-identity` |
| Rate limiting methodology | `rate-limit-bypass-testing` (authorized) |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Layer | Control |
| --- | --- |
| Edge | API gateway, Ingress auth, mTLS mesh |
| App | BentoML runners/APIs validate bearer/API key |
| Network | Private service, NetworkPolicy, no public LB if internal |
| Artifacts | Private registry; pull secrets / MI |
| Tooling | `bentoml`, Docker/K8s manifests, OPA/gateway, TLS certs |

## Workflow

### 1. Confirm scope and success criteria

1. Service name, deployment target, clients, data sensitivity, authorization.
2. Success: unauthenticated requests denied; authorized client infers successfully; TLS on.
3. Budget: rate limits prevent GPU exhaustion.

### 2. Inventory exposure

```bash
bentoml list
# K8s
kubectl get svc,ingress -n "$NS" | rg -i bento
curl -sI http://localhost:3000/ 2>/dev/null | head
```

1. Find public LoadBalancer/Ingress without auth.
2. List env vars for tokens; ensure not default/docs keys.
3. Model store permissions and cloud credentials on the pod.

### 3. Baseline threat model

| Threat | Mitigation |
| --- | --- |
| Anonymous inference | Authn required |
| Model exfil via API | Authz + rate limit + monitoring |
| Prompt/data leakage in logs | Redact payloads |
| SSRF via URL features | Disable or allowlist |
| Dependency CVE | Image scan |

### 4. Apply auth controls

**Prefer edge auth + private network; add app verification defense-in-depth.**

```python
# Conceptual ASGI/BentoML API middleware sketch
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import os, hmac

API_KEY = os.environ["BENTO_API_KEY"]  # from secret store, not image

class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        key = request.headers.get("x-api-key", "")
        if not hmac.compare_digest(key, API_KEY):
            return JSONResponse({"error": "unauthorized"}, status_code=401)
        return await call_next(request)
```

1. Store `BENTO_API_KEY` in K8s Secret / cloud secret manager; mount as env; rotate.
2. For user-facing apps: OIDC JWT validation (issuer, audience, exp) instead of long-lived static keys.
3. Ingress: TLS mandatory; optional IP allowlist for partner APIs.
4. Disable debug endpoints in prod; lock metrics if sensitive.
5. Resource quotas + max concurrency to mitigate auth-bypass DoS on GPU.
6. Separate auth for admin/push model vs inference.

### 5. Verify with evidence

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://bento.example/predict
# expect 401
curl -s -o /dev/null -w "%{http_code}\n" -H "x-api-key: $KEY" \
  -H "content-type: application/json" \
  -d @sample.json https://bento.example/predict
# expect 200
```

1. Expired JWT fails; wrong audience fails.
2. Logs show auth failures without printing full API keys.
3. NetworkPolicy: pod cannot be reached from random namespaces if required.

### 6. Observe and harden

1. Metrics: 401/403 rates, latency, GPU util, request sizes.
2. Alerts on anonymous traffic spikes and auth failure bursts.
3. Regular key rotation and image rebuilds.

### 7. Hand off

1. Client onboarding: how to get tokens.
2. Runbook for rotation and revoke.
3. Architecture diagram: edge vs app auth.

## Auth Options

| Option | Pros | Cons |
| --- | --- | --- |
| Edge only (gateway) | Central policy | Direct pod IP bypass risk |
| App API key | Simple service-to-service | Key distribution |
| OIDC JWT | User/workload federation | JWKS/clock skew ops |
| mTLS mesh | Strong service identity | Complexity |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Default | Deny anonymous | Open `/predict` on Internet |
| Secrets | Mounted from vault | Key in Dockerfile ENV |
| TLS | Required | Plain HTTP public |
| Authz | Per-model permissions | One key for all admin+infer |
| Logs | Metadata only | Full prompts with PII/secrets |

## Output Checklist

- [ ] Exposure inventoried (svc/ingress)
- [ ] Authn mechanism chosen and implemented
- [ ] Secrets not in images/git
- [ ] TLS enabled on external path
- [ ] Negative auth tests evidenced
- [ ] Rate/concurrency limits considered
- [ ] Monitoring for 401 and abuse
- [ ] Rotation runbook written
- [ ] `code-quality-standards` applied

## Rules

- Authorized services only.
- Never leave production inference open without auth.
- Protect model artifacts and credentials.
- Redact sensitive inputs in logs.
- Defense in depth: network + edge + app.
