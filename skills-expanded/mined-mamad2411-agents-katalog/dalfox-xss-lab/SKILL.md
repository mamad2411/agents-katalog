---
name: dalfox-xss-lab
description: >
  Run Dalfox for authorized XSS discovery in labs, CTFs, and owned web apps:
  crawl/pipe modes, parameter mining, DOM/reflected checks, blind XSS callbacks
  on owned collectors, and triage of findings into real PoCs. Use only with
  written scope — not for unsolicited scanning of third-party sites.
---

# Dalfox XSS Lab

## Scope And Authorization

- **In scope:** Targets you own, legal CTF/lab apps, or systems under a written pentest authorization that names the hosts and rules of engagement.
- **Out of scope:** Internet-wide scanning; blind XSS probes against random sites; using findings to harm users.
- Prefer dedicated lab environments; throttle production-authorized tests.
- Redact real session cookies from command lines and tickets.
- Pair with `xss-cross-site-scripting` for methodology depth and CSP skills for defenses.

## When To Use

- Quick parameterized XSS hunting with Dalfox after recon.
- Piping URLs from `waybackurls`/`gau`/`katana` (owned scope lists only).
- Comparing Dalfox output to manual PoCs.
- Training engineers on XSS tooling in a safe lab.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full XSS methodology / fix patterns | `xss-cross-site-scripting` |
| Authenticated DAST broadly | `dast-authenticated-scans` |
| CSP rollout | `csp-report-only-rollout` |
| DOM-only deep review without scanner | manual DOM XSS techniques in XSS skill |
| Implementation quality baseline | `code-quality-standards` |

## Dalfox roles

| Mode | Use |
| --- | --- |
| URL / param scan | Single target with known params |
| Pipe mode | Mass URLs from scope file |
| Worker / remote | Controlled distributed lab only |
| Blind XSS | Callback to **your** collector |

## Workflow

### 1. Confirm authorization and scope file

1. Written scope hosts; exclude payment, prod destructive actions if required.
2. Rate limits and time windows.
3. Success: high-signal findings with manual PoC or justified false positive.

```bash
# scope.txt one host/URL pattern per line — owned only
```

### 2. Install and version

```bash
# Example install paths vary
dalfox version
```

Pin version in lab docs for reproducibility.

### 3. Single-target scan

```bash
dalfox url 'https://lab.example.local/search?q=test' \
  --output dalfox-out.json \
  --format json
```

Useful flags (check `dalfox --help` for your version):

- Custom headers / cookies for **test** sessions: `--cookie 'session=...'`
- Delay / worker limits to avoid DoS: follow RoE
- Mining: parameter discovery options when enabled in your version

### 4. Pipe mode on scoped URLs

```bash
cat scoped-urls.txt | dalfox pipe --output pipe-out.json --format json
```

Only URLs under authorized domains. Deduplicate before piping.

### 5. Blind XSS (owned collector only)

1. Deploy callback app you control (e.g. internal XSS hunter / interactsh-like for lab).
2. Configure Dalfox blind payload host to that collector.
3. Never point blind payloads at third-party infrastructure you do not own.

### 6. Triage findings

| Scanner claim | Next step |
| --- | --- |
| Reflected payload in HTML | Manual browser PoC; context (attr/html/js) |
| DOM finding | Confirm in DevTools sources; sink still active |
| WAF blocked | Note; try authorized lab without WAF if in scope |
| Stored XSS | Verify persistence + victim role (test accounts) |

```html
<!-- Manual PoC only on lab after confirmation -->
<script>document.documentElement.setAttribute('data-xss','1')</script>
```

Escalate to `xss-cross-site-scripting` skill for encoding fixes and CSP.

### 7. Report and clean up

1. Evidence: request/response, screenshot, redacted headers.
2. Remove test payloads from stored fields when done.
3. Do not leave blind XSS callbacks active past engagement without consent.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Named hosts + rate limit | `pipe` entire internet lists |
| Auth | Test account cookie | Stolen real user session |
| Blind | Own collector | Random public XSS hunter with client data |
| Output | Manual verified PoC | Dump scanner noise as critical |
| Prod | Throttled window | Aggressive workers causing outage |

## Output Checklist

- [ ] Authorization and scope recorded
- [ ] Dalfox version pinned
- [ ] Scoped URL list only
- [ ] Rate limits applied
- [ ] Findings triaged with manual checks
- [ ] False positives labeled
- [ ] PoCs redacted and stored safely
- [ ] Stored payloads cleaned
- [ ] Fix handoff to app team / XSS skill
- [ ] Residual untested surface noted

## Rules

- Authorization first; tooling second.
- Dalfox is a helper — verify before severity claims.
- Focus on **authorized Dalfox XSS lab usage**.
