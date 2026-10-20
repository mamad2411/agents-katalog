---
name: content-security-policy-bypass
description: >
  Authorized Content-Security-Policy (CSP) review and bypass research: parse policy
  directives, assess nonce/hash/'strict-dynamic' posture, source expressions, and XSS
  impact under CSP. Use when responses or meta tags set CSP, inline script is blocked,
  or a confirmed XSS still needs a realistic execution path under the deployed policy.
---

# Content-Security-Policy Bypass (Authorized)

## Scope And Authorization

- **In scope:** owned apps, labs, authorized pentests/bug bounty in-scope assets.
- **Out of scope:** exploiting CSP gaps on third-party sites without permission.
- Prefer non-destructive script alerts / cooperators you control for XSS proof.
- Pair design fixes with `content-security-policy-design` and XSS with `xss-cross-site-scripting`.

## When To Use

- Evaluating whether XSS is mitigated or still exploitable under CSP.
- Policy has `script-src`, nonces, `'unsafe-inline'`, wildcards, or JSONP hosts.
- Tokens: CSP bypass, strict-dynamic, nonce reuse, script-src, base-uri, object-src.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Deploying strong CSP | `content-security-policy-design` |
| Finding XSS sinks | `xss-cross-site-scripting` |
| Clickjacking frames | `clickjacking` / frame-ancestors |
| COOP/COEP | `coop-coep-isolation` |

## Parse Policy First

```bash
curl -sI https://app.example.com/ | rg -i "content-security-policy"
# Also HTML: <meta http-equiv="Content-Security-Policy"
```

| Directive | Bypass relevance |
| --- | --- |
| `script-src` | Primary for XSS execution |
| `'unsafe-inline'` / `'unsafe-eval'` | Often full XSS still works |
| nonces / hashes | Strong if consistently applied |
| `'strict-dynamic'` | Trust propagates from nonce/hash scripts |
| host allowlists | JSONP/CDN gadgets on allowed hosts |
| `object-src` / `base-uri` / `frame-src` | Secondary vectors |
| report-only | Does not block — note separately |

## Common Weaknesses → Attack Ideas (authorized)

| Weakness | Research direction |
| --- | --- |
| `'unsafe-inline'` without nonce | Classic reflected/stored XSS |
| Wildcard `*.cloudfront.net` etc. | Find JSONP or upload XSS on that host |
| `cdnjs` / old Angular allowlisted | Library gadgets / angular expression |
| Nonce present but also `'unsafe-inline'` | Inline still executes |
| Nonce leaked into attacker-controlled HTML | Reuse nonce on injected script |
| Missing `base-uri` | Base tag injection shifts relative script URLs |
| Missing `object-src` | Plugin vectors (legacy) |
| CSP only on some paths | XSS on path without CSP |
| Meta CSP weaker than header | Inconsistent enforcement |

**Note:** Modern browsers + good nonce CSP make many classic bypasses fail — report residual accurately.

## Workflow

### 1. Confirm scope and success

1. Target pages, XSS primitives already found (if any), ROE.
2. Success: working XSS under CSP **or** evidence CSP blocks realistic exploitation.
3. Use cooperative payload host you control when exfil needed.

### 2. Inventory all policies

1. Headers vs meta; multiple CSPs combine (intersection semantics matter — document browser behavior carefully).
2. Per-route differences (app vs static vs error pages).
3. `Content-Security-Policy-Report-Only` vs enforcing.

### 3. Map XSS capability

1. Where can you inject? HTML, attr, JS string, URL?
2. Can you inject `<script>`? Event handlers? `javascript:`? markup for `base`?

### 4. Attempt realistic bypasses only as needed

1. If `'unsafe-inline'` → standard XSS proof.
2. If host allowlist → search gadgets on allowed origins (authorized knowledge / public research).
3. If nonce → check predictability, reuse in page, injection into server-rendered nonce contexts.
4. If `'strict-dynamic'` → need trusted script to load attacker script; look for DOM sinks in trusted code (`createElement('script')` + user URL).

### 5. Document impact

1. Policy string, page, payload, browser version.
2. Whether session theft / action possible under cookie flags (HttpOnly still matters).
3. Fix: tighten CSP (`content-security-policy-design`) **and** remove XSS sink.

### 6. Verify defenses after fix

1. Old payload blocked (console CSP error).
2. App still functions (nonces applied to legitimate scripts).

### 7. Hand off

1. Engineering ticket with policy diff suggestion.
2. Do not claim “CSP bypass” if only report-only was present.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Method | Parse then targeted | Spray XSS polyglots only |
| Proof | Works in modern browser | Theoretical 2015 gadget only |
| Scope | In-scope hosts | Attacking random CDNs off-scope |
| Fix | CSP + fix sink | CSP theater with unsafe-inline |
| Honesty | “Blocked by CSP” when true | Inflate severity |

## Output Checklist

- [ ] All CSP variants collected
- [ ] Directives analyzed for script execution
- [ ] XSS primitive characterized
- [ ] Bypass attempted with evidence or blocked evidence
- [ ] Browser/version noted
- [ ] Remediation to design skill + XSS fix
- [ ] Residual risks (JSONP hosts, path gaps) listed

## Rules

- Authorized testing only.
- Prefer accurate residual risk over hype.
- CSP is defense-in-depth; still fix XSS.
- Offense/review skill; deployment design is the sibling skill.
