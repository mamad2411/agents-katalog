---
name: aws-cloudfront-functions
description: >
  CloudFront Functions for owned distributions: viewer-request/viewer-response
  handlers, JavaScript runtime limits, key-value store, vs Lambda@Edge, header
  manipulation, and security pitfalls (authz, open redirects). Use when implementing
  lightweight edge logic at CloudFront — not for abusing third-party distributions.
---

# AWS CloudFront Functions

## Scope And Authorization

- **In scope:** CloudFront distributions and Functions in AWS accounts you own or manage with authorization.
- **Out of scope:** Tampering with third-party CDN configurations or cache poisoning attacks without authorization.
- Edge code runs on every matching request — bugs have global blast radius; test on staging distributions.
- Do not put long-lived secrets in Function code; prefer CloudFront KeyValueStore or origin auth.
- Pair with `code-quality-standards`; general S3 origin hardening via `aws-s3-bucket-hardening`.

## When To Use

- Lightweight header rewrites, URL normalization, simple A/B cookie routing, JWT **format** checks (not full crypto-heavy auth unless within limits).
- Choosing CloudFront Functions vs Lambda@Edge (viewer/origin triggers, libraries, timeout).
- Debugging Function execution errors and test events in console/CLI.
- Using CloudFront KeyValueStore for config flags at the edge.
- Enforcing HSTS or security headers at viewer-response.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full origin request auth with heavy deps | Lambda@Edge / origin auth patterns |
| S3 bucket public access hardening | `aws-s3-bucket-hardening` |
| WAF bot/rules | WAF skill |
| API Gateway JWT | `aws-apigateway-http-api` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Constraint | CloudFront Functions (typical) |
| --- | --- |
| Triggers | viewer-request, viewer-response only |
| Runtime | Constrained JavaScript (no network in classic model; check current feature set for KVS) |
| Time/CPU | Very short — keep logic tiny |
| Package size | Small; no heavy node_modules |
| vs Lambda@Edge | Edge supports origin-request/response, longer limits, VPC not applicable same way |

## Functions vs Lambda@Edge

| Need | Prefer |
| --- | --- |
| Simple header/URL tweaks at viewer | CloudFront Functions (cheaper, faster scale) |
| Call external API / heavy JWT verify libs | Lambda@Edge or origin |
| Origin-request signing (SigV4 complex) | Lambda@Edge / dedicated origin shield patterns |
| Per-request sub-ms overhead | Functions |

## Workflow

### 1. Confirm scope and success criteria

1. Record distribution ID, behaviors, origins, whether OAC to S3, staging alias.
2. Success: Function publishes; associate to behavior; unit tests pass; no open redirect; headers as designed; p99 within budget.
3. Rollback: detach Function association quickly.

### 2. Inventory

```bash
aws cloudfront list-distributions --query "DistributionList.Items[].{Id:Id,Domain:DomainName}"
aws cloudfront list-functions
aws cloudfront describe-function --name "$FN_NAME" --stage DEVELOPMENT
```

1. List cache behaviors and existing Function/Lambda associations.
2. Note path patterns that skip the Function (static assets).

### 3. Baseline

1. Capture sample viewer requests (method, URI, headers) from access logs.
2. Current response headers (CSP, HSTS) inventory.
3. Error rate metrics before attach.

### 4. Implement Function safely

**Viewer-request URI normalize (sketch):**

```js
function handler(event) {
  var req = event.request;
  var uri = req.uri;
  // Normalize duplicate slashes carefully; avoid open redirects
  if (uri.indexOf('//') === 0) {
    return {
      statusCode: 400,
      statusDescription: 'Bad Request',
      headers: { 'content-type': { value: 'text/plain' } },
      body: 'Bad path'
    };
  }
  if (uri.endsWith('/')) {
    req.uri = uri + 'index.html';
  }
  return req;
}
```

**Viewer-response security headers (sketch):**

```js
function handler(event) {
  var res = event.response;
  res.headers['strict-transport-security'] = { value: 'max-age=31536000; includeSubDomains' };
  res.headers['x-content-type-options'] = { value: 'nosniff' };
  return res;
}
```

**Security rules for edge code**

1. Never reflect untrusted input into `Location` without allowlist (open redirect).
2. Do not implement “auth” by only checking cookie presence.
3. Keep allowlists for host/path rewrites.
4. Use KVS for flags rather than redeploying code for every toggle when available.
5. Test both HTTP methods and large header sets within documented limits.

```bash
aws cloudfront create-function --name "$FN_NAME" --function-config Comment=v1,Runtime=cloudfront-js-2.0 --function-code fileb://function.js
aws cloudfront test-function --name "$FN_NAME" --if-match "$ETAG" --event-object file://test-event.json
aws cloudfront publish-function --name "$FN_NAME" --if-match "$ETAG"
# Associate via distribution config update (behavior FunctionAssociations)
```

### 5. Verify with evidence

```bash
curl -sSI "https://$DIST_DOMAIN/app/"
# Expect headers / rewrite behavior
aws cloudfront get-monitoring-subscription --distribution-id "$DIST_ID" 2>/dev/null || true
```

1. Negative: crafted `//evil` or `/@evil` paths do not redirect off-site.
2. Cache: understand whether viewer-request changes affect cache key (query/headers).
3. Rollback drill: remove association, invalidation if needed.

### 6. Observe and harden

1. CloudWatch metrics for Function invocations/errors/throttles (per monitoring setup).
2. Alert on error rate > threshold.
3. Review Functions quarterly for dead code and secret leakage.

### 7. Hand off

1. Document trigger, behavior path pattern, and owners.
2. Store source in Git; CI publish to DEVELOPMENT then canary distribution.
3. Link WAF/S3 origin skills for layered controls.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Logic size | tiny pure transforms | mini-framework at edge |
| Redirects | allowlisted hosts | user-controlled Location |
| Secrets | KVS/origin auth | API keys in Function source |
| Choice | Functions for simple viewer | Functions for heavy crypto/network |
| Test | test-function + staging | edit prod only |
| Cache | intentional cache key design | accidental uncacheable all traffic |

## Output Checklist

- [ ] Distribution/behaviors/authorization recorded
- [ ] Functions vs Lambda@Edge decision documented
- [ ] Code reviewed for redirect/header injection
- [ ] test-function evidence on sample events
- [ ] Published and associated to correct behavior
- [ ] Security headers / URI rules verified via curl
- [ ] Monitoring/alerts considered
- [ ] Rollback path documented
- [ ] `code-quality-standards` applied

## Rules

- Owned distributions only; edge bugs are global.
- No secrets in Function source.
- Prefer allowlists over string concatenation for redirects.
- Keep runtime within CloudFront Functions limits; escalate to Lambda@Edge when needed.
- Focus on Functions; origin bucket and WAF hardening elsewhere.
