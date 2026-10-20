---
name: flash-crossdomain-legacy
description: >
  Assess legacy Adobe Flash cross-domain policy risks (crossdomain.xml, clientaccesspolicy.xml):
  overly permissive allow-access-from, HTTPS/HTTP mismatches, and residual endpoints that still
  serve policies for old clients or other runtimes. Use on owned apps and authorized assessments
  when hunting historical misconfigurations, not for attacking third parties.
---

# Flash Crossdomain Legacy

## Scope And Authorization

- **In scope:** web origins you own or are authorized to test; historical policy files still deployed.
- **Out of scope:** abusing third-party `crossdomain.xml` for unauthorized data access.
- Flash Player is end-of-life—focus on residual risk and cleanup, not new Flash features.
- Redact session tokens found during testing.
- Pair config fixes with `code-quality-standards`.

## When To Use

- Discovering **`/crossdomain.xml`** or **`/clientaccesspolicy.xml`** on live hosts.
- Reviewing `allow-access-from domain="*"` and insecure header/meta policies.
- Migrations that removed Flash UI but left policies enabling other stack components.
- Silverlight `clientaccesspolicy.xml` adjacent reviews on same hosts.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Modern CORS | CORS skill in catalog |
| CSRF / Fetch Metadata | `fetch-metadata-isolation` / `fetch-metadata-sec-headers` |
| General recon | `recon-and-methodology` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| File | Runtime historically |
| --- | --- |
| `/crossdomain.xml` | Adobe Flash socket/HTTP cross-domain |
| `/clientaccesspolicy.xml` | Microsoft Silverlight |
| Risk today | Misconfig residual; some non-Flash tools historically abused patterns; signals poor hygiene |

## Policy anti-patterns

| Pattern | Risk |
| --- | --- |
| `allow-access-from domain="*"` | Any site could read responses via Flash-era model |
| `secure="false"` on HTTPS origins | HTTP SWF access to HTTPS content (historical) |
| Wildcard to parent `*.com` style mistakes | Overbroad trust |
| Policies on cookie-auth APIs origins | Cross-domain data theft when plugin existed |
| Still deployed with `*` | Indicates forgotten attack surface / compliance fail |

## Workflow

### 1. Confirm scope and success criteria

1. Host list in scope; whether any legacy Flash/Silverlight still required (almost never).
2. Success: inventory of policy URLs; permissive policies removed or tightened; monitoring for reintroduction.
3. Note CDN/path variants (`/foo/crossdomain.xml`).

### 2. Inventory

```bash
for h in app.example api.example; do
  for p in /crossdomain.xml /clientaccesspolicy.xml; do
    code=$(curl -sS -o /tmp/pol -w "%{http_code}" "https://$h$p")
    echo "$h$p $code"
    head -c 400 /tmp/pol 2>/dev/null; echo
  done
done
```

1. Search repos and object storage for committed policies.
2. Check load balancers returning default policies.

### 3. Evaluate content

```xml
<!-- Bad historical example -->
<cross-domain-policy>
  <allow-access-from domain="*" secure="false"/>
  <allow-http-request-headers-from domain="*" headers="*"/>
</cross-domain-policy>
```

```xml
<!-- Less bad if truly required for a controlled legacy peer -->
<cross-domain-policy>
  <allow-access-from domain="trusted-legacy.example.com"/>
</cross-domain-policy>
```

1. Any `domain="*"` on authenticated origins → high priority remove.
2. Prefer **delete file** and return 404 if no legitimate consumer.

### 4. Remediate

1. Remove policies from production origins serving APIs or user data.
2. If a rare internal tool still needs a policy, allowlist exact domains; force `secure="true"` on HTTPS; document owner/expiry.
3. Ensure modern clients use CORS intentionally—not Flash policies.
4. Block path at WAF/edge if accidental republish risk.

### 5. Verify with evidence

```bash
curl -sS -o /dev/null -w "%{http_code}\n" "https://app.example/crossdomain.xml"
# Expect 404 after cleanup
```

1. Repo search clean; IaC does not recreate `*`.
2. Regression test in CI grepping for `allow-access-from domain="*"`.

### 6. Observe and harden

1. Periodic crawl of inventory hosts for policy paths.
2. Alert if 200 returns with wildcard content.

### 7. Hand off

1. Findings with policy snippets (redacted) and remediation PR.
2. Note Flash EOL; discourage any reintroduction.
3. Apply `code-quality-standards` if automation added.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Default | No policy file (404) | `domain="*"` forever |
| Exception | Exact domain + owner + expiry | “Marketing might need Flash” |
| HTTPS | secure true / delete | secure false on HTTPS site |
| Detection | Scheduled curl inventory | One-time manual 2015 review |
| Modern equiv | Explicit CORS | Rely on crossdomain for JS SPA |

## Output Checklist

- [ ] Hosts checked for both policy filenames
- [ ] Permissive policies documented with severity
- [ ] Removed or tightly allowlisted
- [ ] Repo/IaC cleaned
- [ ] Regression grep or crawl in place
- [ ] No business justification left unreviewed
- [ ] `code-quality-standards` applied if code shipped

## Rules

- Authorized hosts only.
- Prefer deletion over clever legacy support.
- Do not treat Flash policy review as a substitute for CORS/CSRF modern controls.
- No assistance bypassing third-party cross-domain protections.
