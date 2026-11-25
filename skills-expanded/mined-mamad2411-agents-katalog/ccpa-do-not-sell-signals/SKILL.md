---
name: ccpa-do-not-sell-signals
description: >
  Honor CCPA/CPRA “Do Not Sell or Share” and Global Privacy Control (GPC) signals on
  owned sites: detect Sec-GPC / GPC, map to sale/share suppression, cookies/ads vendors,
  preference storage, and audit evidence. Use when CCPA DNSMPI, GPC, do not sell link,
  or California privacy signal compliance engineering — not legal advice.
---

# Ccpa Do Not Sell Signals

## Scope And Authorization

- **In scope:** Websites/apps you operate that may “sell” or “share” personal information under California privacy law definitions (as interpreted by your counsel).
- **Out of scope:** Providing legal advice; guaranteeing compliance; processing signals for systems you do not control.
- Partner with privacy counsel/DPO — this skill is **engineering implementation**.
- Redact real user preference records in tickets.
- Pair with consent management, cookie skills, and `code-quality-standards`.

## When To Use

- Implementing or verifying GPC (`Sec-GPC: 1`) handling.
- Wiring “Do Not Sell or Share My Personal Information” links and UIs (CPRA).
- Propagating opt-out to ad tags, data brokers, analytics configs.
- Building preference centers and audit logs for regulators/customers.
- Fixing gaps where UI opt-out does not stop pixels.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full privacy program / DPIA | privacy program / counsel |
| Cookie banner UX only | consent management skills |
| Generic frontend a11y | `accessibility-a11y-checklist` |
| Security headers | `nginx-security-headers` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Signal / control | Engineering meaning |
| --- | --- |
| GPC / `Sec-GPC` | Browser signal; treat as opt-out of sale/share where policy says |
| DNSMPI link | User-facing opt-out mechanism |
| Sale / Share | Adtech cross-context behavioral advertising often in scope — confirm with counsel |
| Preference store | Server-side record tied to user/device |
| Vendors | Suppress or switch to non-sale mode |
| Evidence | Logs of signal received + actions taken |

## Workflow

### 1. Confirm scope with privacy stakeholders

1. Jurisdictions, definitions of sell/share for **your** data flows, known ad/analytics vendors.
2. Success: GPC and explicit opt-out both suppress sale/share processing; preference persists; vendor tags respect state; audit trail exists.
3. Document legal interpretation owner (counsel) — engineering implements their decision.

### 2. Inventory data flows and tags

```bash
# Find marketing/ad tags in owned frontends
rg -n "gtag|googletagmanager|facebook|fbq|tiktok|ads|segment|amplitude|hotjar" -g '*.{js,ts,tsx,html}'
```

1. List each vendor: personal data sent, whether classified as sale/share.
2. Map server-side events (CAPI, webhooks) too — not only browser pixels.
3. Identify login vs anonymous identity graph.

### 3. Detect signals

**GPC:**

```text
Request header: Sec-GPC: 1
# Also navigator.globalPrivacyControl in some browsers (readable by JS)
```

```js
function gpcEnabled(req, navigatorGpc) {
  return req.headers['sec-gpc'] === '1' || navigatorGpc === true;
}
```

**Explicit opt-out:**

1. Privacy preference center toggle.
2. “Do Not Sell or Share” link flow.
3. Authenticated account preference.

1. Treat GPC as opt-out when counsel policy says so (common expectation for participating businesses).
2. Do not require account creation solely to honor GPC if policy forbids friction.

### 4. Propagate suppression

```text
Edge/app detects GPC or stored preference
  → set internal privacy context (sale_share=false)
  → CMP / tag manager consent mode
  → suppress sale/share vendors
  → server-side pipelines honor flag
  → share opt-out with vendors via their APIs if used
```

| Channel | Action when DNS/GPC |
| --- | --- |
| Browser tags | Do not load sale/share pixels; or limited mode |
| Server CAPI | Stop sending events used for cross-context ads if classified as share/sale |
| Cookies | Delete/avoid ad IDs where required |
| Partners | Call vendor opt-out / privacy API |
| Data lake activations | Exclude from audience export jobs |

1. Prefer **server-enforced** flags so client bypass does not re-enable sale pipelines.
2. Cache preference on first-party cookie/local profile **and** server if identified.

### 5. Store preferences and evidence

```text
preference record:
  subject_id or device_pseudonym
  source: gpc | ui | call_center
  sale_share_opt_out: true
  timestamp, user_agent hash, region if needed
  version of policy
```

1. Retention per legal schedule.
2. Provide user-readable status in privacy center.
3. Log signal application for audits (access-controlled).

### 6. Verify

| Test | Expected |
| --- | --- |
| `Sec-GPC: 1` anonymous visit | Sale/share tags not fired |
| UI opt-out | Same + preference persists new session |
| Logged-in opt-out | Server pipelines stop exports |
| GPC off after opt-out UI | Still opted out until user opts in (policy) |
| Network panel | No unexpected ad IDs set |

```bash
curl -sI -H "Sec-GPC: 1" https://www.example.com/ | rg -i "set-cookie|gpc|privacy"
# Browser automation: assert tag manager data layer consent flags
```

1. Periodic crawl of pages for accidental tag regressions.
2. Vendor contract/config review annually.

### 7. Hand off

1. Runbook for new marketing tags: privacy review gate.
2. Metrics: % sessions with GPC; opt-out rates; tag load violations.
3. Coordinate with counsel on notices (privacy policy text is legal-owned).
4. Apply `code-quality-standards` to preference services.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| GPC | Honored as opt-out per policy | Ignored header |
| Enforcement | Server + tag manager | Only hide link text |
| Vendors | Inventory + suppress | “Banner covers us” |
| Persistence | Stored preference | Only for one page view |
| Evidence | Audit logs | No records when asked |
| Legal | Counsel-defined scope | Engineers invent legal theory alone |

## Output Checklist

- [ ] Counsel-approved interpretation documented
- [ ] Vendor/data-flow inventory complete
- [ ] GPC detection implemented
- [ ] UI DNSMPI / preference center wired
- [ ] Suppression across browser + server paths
- [ ] Preference storage + audit logs
- [ ] Verification tests for GPC and UI
- [ ] Marketing tag change control
- [ ] `code-quality-standards` applied

## Rules

- Not legal advice — implement counsel’s requirements.
- Prefer server-side enforcement over cosmetic UI.
- New adtech requires privacy review.
- Protect preference data as sensitive configuration of user rights.
- Security vuln testing of privacy endpoints still needs authorization.
