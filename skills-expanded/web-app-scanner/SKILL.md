---
name: web-app-scanner
description: "Authorized web application testing from the CLI, including local pre-deploy source/config audits, subdomain enumeration, passive recon, non-destructive active vulnerability checks, and guarded SQL injection testing. Use for reviewing deploy secrets, frontend build artifacts and source maps, admin defaults, static XSS sinks, or an authorized live web estate."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Web App Scanner

> CLI web application assessment for authorized targets. Includes a read-only local pre-deploy audit for secrets, frontend builds, source maps, admin defaults, and static XSS sinks, plus subdomain mapping, passive recon, non-destructive active checks, optional nuclei/ffuf, and guarded SQL injection testing.

> **Language rule**: All skill instructions use English.
> **Final summary presented to the user must be in Vietnamese.**

> **Fastest path — whole system.** For "scan the entire system / all subdomains", run the orchestrator: it enumerates subdomains, keeps the web-alive ones, and runs passive recon + active vuln checks on each, then aggregates one report.
>
> ```powershell
> python web-app-scanner\scripts\scan_all.py example.com --active --crawl 1 --authorized --out output\scan
> ```
>
> Read `output\scan\FINDINGS_ALL.md`. Steps 1–5 below are the individual stages if you want to run them one at a time.

---

## 0. Authorization & Routing

Operates under [MASTER_POLICY.md](../MASTER_POLICY.md) §1-§2.

**Scope gate — required.** Test only web apps you **own or are explicitly authorized to assess** (written engagement, bug-bounty scope in-scope asset, CTF, or your own lab). Passive recon and passive subdomain sources (crt.sh/subfinder) are low-impact; **anything that sends probes to the target — active vuln checks (`web_recon.py --active`), link crawling, DNS brute (`subdomain_enum.py --brute`), and SQLi testing (`sqli_test.py`) — is intrusive** and requires the explicit `--authorized` flag. If scope is unclear, ask one concise question first. Never point these at third-party sites without authorization.

| Sibling skill | When |
|---|---|
| [network-scanner](../network-scanner/SKILL.md) | Find which hosts/ports serve the web app |
| [network-interceptor](../network-interceptor/SKILL.md) | Capture the app's API/auth traffic |
| [pentest-script-generator](../antigravity-kit/pentest-script-generator/SKILL.md) | Turn a confirmed finding into a PoC/verify script |
| [container-cloud-auditor](../container-cloud-auditor/SKILL.md) | Audit the hosting config behind the app |

---

## Step 0 — Environment check

```powershell
python web-app-scanner\scripts\scan_all.py --check
python web-app-scanner\scripts\deploy_audit.py --check
python web-app-scanner\scripts\brain_python_library.py --check
python web-app-scanner\scripts\subdomain_enum.py --check
python web-app-scanner\scripts\web_recon.py --check
python web-app-scanner\scripts\sqli_test.py --check
```

Native recon + subdomain enum + active checks need only Python. Optional tools:
- **subfinder** — https://github.com/projectdiscovery/subfinder (extra passive subdomain sources)
- **nuclei** — https://github.com/projectdiscovery/nuclei (single binary in PATH)
- **ffuf** — https://github.com/ffuf/ffuf (single binary in PATH)
- **sqlmap** — `pip install sqlmap` (or clone the repo)

---

## Pre-deploy source audit (local, read-only)

Run this against the application source tree before deploying:

```powershell
python web-app-scanner\scripts\deploy_audit.py C:\path\to\project --out output\deploy-audit --fail-on high
```

The audit writes `FINDINGS.md` and `findings.json` and checks:
- Deploy `.env*` values for empty/default/example secrets, values shorter than 32 characters, repeating or sequential patterns, low estimated randomness, and weak or empty credentials embedded in common database/service URLs. Reports include only the key name, component, length, and reason; secret values are never emitted.
- Frontend projects for a missing or empty production build (`dist`, `build`, `.next`, or `out`), emitted `.map` files, `sourceMappingURL` references, and production-effective Vite/Webpack/Next/Vue/Angular/CRA settings that enable source maps, including hidden/inline and Angular object forms. Development-only settings are ignored.
- Admin credentials in env and seed/config files for common defaults, password=username, short passwords, and weak character variety. Hashes and runtime secret references are not treated as plaintext passwords.
- Client-side XSS risk sinks such as `dangerouslySetInnerHTML`, `innerHTML=`, `v-html`, `document.write`, Angular sanitizer bypasses, dynamic `eval`, and unescaped template output.

`--fail-on high` returns exit code 1 after writing reports when a high or critical finding exists, which is suitable for a deployment gate. Omit it for report-only mode.

Static XSS findings are marked `review-required`: trace whether untrusted data reaches the sink. Confirm runtime reflected XSS separately with the authorized active checks below.

---

## Reusable Python library

Before writing a one-off Python helper, search the in-project archive:

```powershell
python web-app-scanner\scripts\brain_python_library.py search "source map"
python web-app-scanner\scripts\brain_python_library.py search xss --json
python web-app-scanner\scripts\brain_python_library.py search admin --status all
python web-app-scanner\scripts\brain_python_library.py verify
```

The bundled catalog is `python-library\index.json`; copied source is under `python-library\files\`. Search results include a generated purpose description, categories, imports, public symbols, safety signals, and one of these reuse levels:

- `direct` — has a CLI/main guard and no detected target-specific settings.
- `adapt` — useful code that needs paths, arguments, or integration adjusted.
- `reference-only` — contains active networking or destructive capabilities; inspect and extract logic rather than running it unchanged.
- `do-not-run` — metadata only; the source was not copied because static analysis found a hardcoded sensitive value, invalid syntax, or a module-scope call outside the conservative pure-data allowlist.

Never execute a result solely because it appears in the catalog. Read the file, confirm authorization for any target interaction, and prefer extracting a function over launching a historical scratch script. To refresh the bundled archive from the local Antigravity brain:

```powershell
python web-app-scanner\scripts\brain_python_library.py sync
```

The sync parser never imports source files. Run `verify` after a refresh to validate the schema, file set, and every copied SHA-256. See [references/brain_python_library.md](references/brain_python_library.md) for schema and safety rules.

---

## Step 1 — Subdomain enumeration (map the estate)

Discover subdomains and which of them serve a live web app:

```powershell
python web-app-scanner\scripts\subdomain_enum.py example.com --out output\subs
```

- Passive by default: **crt.sh** Certificate Transparency + **subfinder** (if installed). Low-impact, but note crt.sh receives the target domain name.
- Add `--takeover` to flag **dangling-CNAME subdomain takeover** — CNAME points to a decommissioned service (GitHub Pages, S3, Heroku, Azure, Fastly, Shopify, CloudFront, Vercel, Netlify, Tumblr, WordPress, Tilda, Help Scout, …) with an unclaimed-resource fingerprint; also reports stale DNS verification tokens (`_github-pages-challenge`, `asuid`, `_dnsauth`, …).
- Add DNS brute force (active — sends DNS queries to the target zone, needs `--authorized`):

```powershell
python web-app-scanner\scripts\subdomain_enum.py example.com --brute wordlist.txt --authorized --out output\subs
```

Writes `SUBDOMAINS.md` + `subdomains.json` (host, IP, live URL, status). Feed the web-alive URLs into Step 2/3.

---

## Step 2 — Passive recon (no install)

```powershell
python web-app-scanner\scripts\web_recon.py https://app.local --out output\web
```

Checks and reports:
- Missing security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy.
- Cookie flags: Secure / HttpOnly / SameSite.
- TLS protocol version + certificate summary (flags TLS < 1.2).
- CORS reflection (echoed Origin, `*` + credentials).
- Tech disclosure via Server / X-Powered-By.

---

## Step 3 — Active vulnerability checks (non-destructive, authorized only)

Detection-only probes for real app-layer bugs — exposed `.git`/`.env`/backups & `security.txt`, reflected XSS, open redirect, path traversal (LFI), header injection (CRLF), **SSTI** (`{{a*b}}` evaluated server-side), **SSRF** (url-param fetching `169.254.169.254` cloud metadata), directory listing. Advanced CORS bypass tests (null origin, arbitrary-subdomain / prefix / suffix trust) run in Step 2's passive recon. Add `--crawl` to walk same-host links and test every discovered endpoint:

```powershell
python web-app-scanner\scripts\web_recon.py https://app.local --active --crawl 1 --authorized --out output\web
```

- Requires `--authorized` (sends probes to the target). Every check is detection-only: benign markers, no data dumped, no state changed.
- **SSRF** probes AWS IMDSv1 plus decimal/hex/IPv6-mapped encodings (defeat naive IP filters), Azure/GCP metadata, and `file://`. For blind SSRF, add `--ssrf-callback https://<your-oast>/` to fire an out-of-band probe you then verify on your collaborator.
- `--crawl DEPTH` discovers URLs (params-first); `--max-pages` caps the crawl.
- Run one URL directly with `vuln_checks.py "<url>" --authorized` for a quick single-endpoint check.

Optional external tools — template scan + content discovery when installed:

```powershell
python web-app-scanner\scripts\web_recon.py https://app.local --nuclei --ffuf wordlist.txt --out output\web
```

Tool output is saved under `output\web\` and referenced from `FINDINGS.md`.

---

## Step 4 — SQL injection testing (guarded, authorized only)

Detection with safe defaults (`--level 1 --risk 1 --batch`):

```powershell
python web-app-scanner\scripts\sqli_test.py "https://app.local/item?id=1" --authorized --out output\sqli
```

From a saved Burp request:

```powershell
python web-app-scanner\scripts\sqli_test.py --request req.txt --authorized --out output\sqli
```

Guardrails:
- Refuses to run without `--authorized`.
- Blocks data-dump / OS-takeover switches (`--dump*`, `--os-shell`, `--file-read`, `--sql-shell`, ...) unless `--allow-exploit` is set — for documented, authorized engagements only. This skill's purpose is **confirming and fixing** SQLi, not exfiltrating data.

Raise depth when needed: `--level 3 --risk 2`.

---

## Step 5 — Report & remediate

`scan_all.py` writes `output\scan\FINDINGS_ALL.md` + `findings_all.json` — a severity-ranked, per-host roll-up across the whole estate (plus per-host `FINDINGS.md` under `output\scan\hosts\`). A single-host `web_recon.py` run writes `FINDINGS.md` + `findings.json`. For SQLi, review sqlmap's session output for injectable parameters, DBMS, and technique.

The local pre-deploy audit writes `output\deploy-audit\FINDINGS.md` + `findings.json`. Treat static source findings as review leads and build-artifact findings as deploy blockers according to the selected `--fail-on` threshold.

Add to the defensive fixes below:
- **Exposed `.git`/`.env`/backups** → remove from web root; rotate any leaked secrets; block dotfiles at the web server.
- **Reflected XSS** → contextual output encoding + CSP.
- **Open redirect** → allow-list redirect targets; never reflect a raw URL param into `Location`.
- **Path traversal / LFI** → canonicalize and allow-list file paths; never pass user input to file APIs.
- **Header injection / CRLF** → strip/reject CR & LF in any user input reflected into headers; use the framework's header API.
- **SSTI** → never render user input as a template; use logic-less templates / strict sandboxing and pass data as context, not source.
- **SSRF** → allow-list outbound hosts, block link-local/metadata ranges (169.254.0.0/16, RFC1918), enforce IMDSv2, resolve-then-validate.
- **Subdomain takeover** → remove dangling DNS records for decommissioned services; claim or delete the CNAME target.
- **CORS** → reflect only an explicit allow-list of origins; never combine reflected/`null` origin with `Access-Control-Allow-Credentials: true`.

Defensive fixes to recommend:
- **SQLi** → parameterized queries / prepared statements, ORM binding, least-privilege DB accounts, input allow-listing.
- **Headers/cookies** → add the missing headers; set Secure/HttpOnly/SameSite.
- **TLS** → enforce ≥ 1.2, valid cert, HSTS.
- **CORS** → explicit trusted origins; never `*`/reflected origin with credentials.

See [references/web_checklist.md](references/web_checklist.md) for the full checklist.
