---
name: aws-apigateway-http-api
description: >
  Amazon API Gateway HTTP API (v2) for owned AWS accounts: JWT authorizers, IAM/Lambda
  authorizers, routes/stages, CORS, access logging, throttling, and least-privilege
  integrations. Use when building or reviewing HTTP APIs on API Gateway — not for
  attacking third-party APIs.
---

# AWS API Gateway HTTP API

## Scope And Authorization

- **In scope:** API Gateway HTTP APIs, authorizers, and integrations in AWS accounts you own or assess with authorization.
- **Out of scope:** Unauthorized scanning or credential abuse against third-party APIs.
- JWT misconfiguration can expose backends — treat authorizer reviews as security-critical.
- Prefer private integrations (VPC Link) when APIs must not be public.
- Pair IaC with `code-quality-standards`; deep JWT attack patterns with authorized API auth skills.

## When To Use

- Creating HTTP APIs (not REST API v1) with JWT (Cognito/Auth0/OIDC) authorizers.
- Migrating from REST API to HTTP API for cost/latency.
- Configuring CORS, stages, throttling, access logs to CloudWatch.
- Least-privilege Lambda/AWS service permissions for integrations.
- Debugging 401/403 from JWT claim routes (`$request.context.authorizer.claims`).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| REST API (v1) API keys/usage plans deep dive | REST API Gateway skill if present |
| Lambda least privilege broadly | `aws-lambda-least-privilege` |
| Cognito/Auth0 IdP config | IdP skills |
| WAF rules broadly | WAF skill |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Feature | HTTP API note |
| --- | --- |
| Authorizers | JWT built-in; Lambda authorizer supported; no native AWS_IAM same as REST in all cases — check current feature matrix |
| JWT | Issuer, audience, identity source (`$request.header.Authorization`) |
| Integrations | Lambda proxy, HTTP proxy, private ALB/NLB via VPC Link |
| Stages | `$default` auto-deploy optional; stage variables limited vs REST |
| CORS | Configurable on API; preflight handling |
| Logging | Access logs JSON to CloudWatch |

## JWT Authorizer Essentials

| Setting | Guidance |
| --- | --- |
| Issuer | Exact issuer URL (trailing slash consistency) |
| Audience | Client ID / API identifier — required check |
| Scopes | Route-level authorization scopes when using OAuth |
| Identity source | Prefer Authorization header bearer |
| Claims | Do not authorize only on presence of any JWT |

## Workflow

### 1. Confirm scope and success criteria

1. Record account, region, API ID, auth IdP, backend type, public vs private.
2. Success: unauthenticated requests 401; wrong audience 401; valid token reaches Lambda; access logs present; throttles set.
3. Note break-glass admin routes protection.

### 2. Inventory HTTP APIs

```bash
aws apigatewayv2 get-apis
API_ID=...
aws apigatewayv2 get-routes --api-id "$API_ID"
aws apigatewayv2 get-authorizers --api-id "$API_ID"
aws apigatewayv2 get-stages --api-id "$API_ID"
aws apigatewayv2 get-integrations --api-id "$API_ID"
```

1. Flag routes with `AuthorizationType=NONE` that should be protected.
2. List CORS configuration and allowed origins.
3. Check resource policies / VPC endpoints if private.

### 3. Baseline

1. Export OpenAPI or IaC definition of the API.
2. Capture sample JWT (lab) claims set (redact).
3. Baseline 4xx/5xx metrics in CloudWatch.

### 4. Apply secure configuration

**JWT authorizer (CLI sketch):**

```bash
aws apigatewayv2 create-authorizer \
  --api-id "$API_ID" \
  --authorizer-type JWT \
  --identity-source '$request.header.Authorization' \
  --name jwt-auth \
  --jwt-configuration Audience=api://my-api,Issuer=https://issuer.example.com/
```

**Attach to route:**

```bash
aws apigatewayv2 update-route \
  --api-id "$API_ID" \
  --route-id "$ROUTE_ID" \
  --authorization-type JWT \
  --authorizer-id "$AUTH_ID"
  # --authorization-scopes scope1 scope2   # when applicable
```

**Access logging:**

```bash
aws apigatewayv2 update-stage \
  --api-id "$API_ID" \
  --stage-name '$default' \
  --access-log-settings DestinationArn=arn:aws:logs:REGION:ACCT:log-group:apigw-access,Format='$context.requestId $context.identity.sourceIp $context.routeKey $context.status $context.authorizer.error'
```

**CORS:** explicit origins/methods/headers — avoid `*` with credentials.

**Lambda permission:**

```bash
aws lambda add-permission \
  --function-name order-api \
  --statement-id apigw-invoke \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:REGION:ACCT:API_ID/*/*"
```

1. Prefer narrow `source-arn` (stage/route) when possible.
2. Backend authorizes on claims/sub still — gateway is necessary but not always sufficient for multi-tenant.
3. Throttle default route limits; set burst/rate for abuse control.
4. Disable execute-api endpoint if using custom domain + private only patterns as designed.

### 5. Verify with evidence

```bash
# No token
curl -i "https://$API_ID.execute-api.$REGION.amazonaws.com/orders"
# Expect 401
# Valid token
curl -i -H "Authorization: Bearer $JWT" "https://$API_ID.execute-api.$REGION.amazonaws.com/orders"
# Wrong aud token → 401
aws logs filter-log-events --log-group-name apigw-access --limit 20
```

1. Confirm Lambda never invoked for failed JWT (authorizer reject).
2. CORS: browser preflight from allowed origin OK; evil origin fails.
3. IaC drift: re-read authorizer issuer/audience after deploy.

### 6. Observe and harden

1. Alarms on 4XX/5XX spikes and authorizer failures.
2. WAF association if Internet-facing and org requires.
3. Rotate IdP keys/JWKS monitoring; cache behavior understood.

### 7. Hand off

1. Document routes → auth → integration map.
2. Runbook for JWT 401 debugging (iss/aud/exp/clock skew).
3. CODEOWNERS for API IaC.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Auth | JWT + aud/iss validated | NONE on sensitive routes |
| Scopes | route-level OAuth scopes | any signed JWT accepted |
| CORS | explicit origins | `*` with cookies |
| Logs | access logs on | no logging |
| Invoke | narrow source-arn | `*` permission for all APIs |
| Backend | still checks tenant | trusts gateway alone blindly for all data |

## Output Checklist

- [ ] Account, API, routes, IdP recorded
- [ ] Authorizers inventory; NONE routes justified
- [ ] JWT issuer/audience/scopes correct
- [ ] CORS tightened
- [ ] Access logging + throttles enabled
- [ ] Lambda/invoke permissions least privilege
- [ ] 401/200 evidence captured
- [ ] Alarms/WAF considered
- [ ] `code-quality-standards` applied to IaC

## Rules

- Owned accounts only.
- Always validate audience and issuer for JWT authorizers.
- Do not leave sensitive routes open for “temporary” demos without expiry.
- Gateway auth ≠ complete application authorization for multi-tenant data.
- Focus on HTTP API (v2); REST-specific features and deep JWT offense elsewhere.
