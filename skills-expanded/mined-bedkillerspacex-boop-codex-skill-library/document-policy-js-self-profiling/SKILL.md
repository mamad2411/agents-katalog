---
name: document-policy-js-self-profiling
description: >
  Use Document-Policy (and related HTTP policies) for JS self-profiling controls on owned
  sites: enable/disable self-profiling APIs, understand privacy/performance tradeoffs,
  header syntax, feature detection, and safe production rollout. Use when Document-Policy
  js-profiling, JS self-profiling API, performance profiler in page, or controlling
  profiling capability via HTTP headers — not for fingerprinting users without basis.
---

# Document-Policy JS Self-Profiling

## Scope And Authorization

- **In scope:** Web applications and headers you control.
- **Out of scope:** Enabling invasive profiling on third-party sites; using profiler data for covert tracking (`device-fingerprint-ethics`).
- Prefer staging validation across target browsers; API support varies.
- Redact profiling samples that may include URLs with tokens.
- Pair with performance/observability skills, security header skills, and `code-quality-standards`.

## When To Use

- Using or evaluating the JavaScript Self-Profiling API in production/RUM.
- Setting `Document-Policy` to allow or deny `js-profiling`.
- Debugging why profiler construction fails in some browsers.
- Privacy review of continuous profiling in first-party pages.
- Coordinating CSP/Document-Policy/Permissions-Policy headers.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General security headers (CSP, HSTS) | `nginx-security-headers` / platform header skills |
| Device fingerprint ethics | `device-fingerprint-ethics` |
| Backend tracing/metrics | `observability-metrics-tracing` |
| Frontend React patterns | `react-component-patterns` |
| Code quality baseline | `code-quality-standards` |

## Concepts

| Term | Role |
| --- | --- |
| Document-Policy | HTTP response header configuring document features |
| `js-profiling` | Policy token related to JS Self-Profiling API capability |
| Self-Profiling API | Sample JS stacks/timestamps in-page for performance |
| Privacy | Stacks may reveal code paths and URL state |
| Support | Chromium-family primarily; check current MDN/Can I Use |

**Note:** Exact header tokens and defaults evolve—verify against current specs/MDN for your browser targets before production.

## Workflow

### 1. Confirm scope and success criteria

1. Why profile (lab only vs RUM)? Data retention? Who accesses traces?
2. Success: policy header deployed intentionally; profiler works only where allowed; privacy review signed; no token leakage in samples.
3. Browser matrix documented.

### 2. Inventory current headers and profiling code

```bash
rg -n "Document-Policy|js-profiling|Profiler|Self-Profiling" -g '*.{js,ts,tsx,html,go,py,nginx,conf}'
curl -sI https://www.example.com | rg -i "document-policy|permissions-policy|content-security"
```

1. Find RUM agents that may enable profilers.
2. Note conflicting policies from CDN/edge.

### 3. Decide allow vs deny

| Mode | When |
| --- | --- |
| Deny / omit enable | Default for most pages; privacy-sensitive apps |
| Allow on sample | Performance debugging, canary % traffic |
| Allow broad RUM | Only with privacy review, aggregation, short retention |

1. Prefer **sampling** and **session consent** where legal/product requires.
2. Never send raw profiles to untrusted third parties without DPA.

### 4. Configure Document-Policy (illustrative)

```http
# Illustrative — confirm token syntax for your browser version
Document-Policy: js-profiling
```

```nginx
# Edge sketch
add_header Document-Policy "js-profiling" always;
```

1. Combine carefully with CSP; headers are independent but all must pass review.
2. Staging: verify header present only on intended routes (admin vs public).

### 5. Application usage pattern

```javascript
// Feature-detect; fail soft
async function maybeProfile() {
  if (typeof Profiler === "undefined") return;
  try {
    const profiler = new Profiler({ sampleInterval: 10, maxBufferSize: 1000 });
    // ... run workload ...
    const trace = await profiler.stop();
    // Send to first-party endpoint after scrubbing
    await fetch("/rum/profile", {
      method: "POST",
      credentials: "same-origin",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(scrub(trace)),
    });
  } catch (e) {
    // Policy blocked or unsupported
  }
}
```

1. **Scrub** query tokens, auth fragments, PII from stack/resources before storage.
2. Rate-limit profile uploads; authenticate RUM endpoint.
3. Disable in browsers/modes where policy denies—do not hammer errors.

### 6. Privacy and security review

1. Data class of profiles; retention (e.g. 7–30 days).
2. Access control on RUM store; no public buckets.
3. Threat: profiles leaking proprietary logic or user identifiers in URLs.
4. Align with `device-fingerprint-ethics` if combining with fingerprint SDKs.

### 7. Verify and hand off

```bash
curl -sI https://staging.example.com/app | rg -i document-policy
# Manual: Chromium devtools / feature detect Profiler
```

1. Canary metrics: profile accept rate, error rate, payload size.
2. Document how to disable instantly via edge config.
3. Apply `code-quality-standards` to RUM client code.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Default | Off / sampled | Always-on full stacks prod-wide |
| Header | Intentional Document-Policy | Unknown vendor enable silent |
| Data | Scrubbed first-party | Raw traces to random SaaS |
| Fail | Soft detect | Break app if Profiler missing |
| Privacy | Review + retention | Infinite storage of URLs+stacks |
| Scope | Owned site | Inject into third-party pages |

## Output Checklist

- [ ] Purpose and browser support documented
- [ ] Allow/deny decision recorded
- [ ] Document-Policy configured on correct routes
- [ ] Client feature-detects and scrubs
- [ ] RUM endpoint authenticated and rate-limited
- [ ] Retention and access control set
- [ ] Privacy review complete as required
- [ ] Kill switch via edge/header
- [ ] Staging verification evidence
- [ ] `code-quality-standards` applied

## Rules

- Profiling data is sensitive performance telemetry—protect it.
- Verify current platform syntax; do not rely solely on outdated blog posts.
- Prefer sampling and scrubbing over bulk raw capture.
- Owned sites only; no covert cross-site profiling.
- Focus on Document-Policy + JS self-profiling controls.
