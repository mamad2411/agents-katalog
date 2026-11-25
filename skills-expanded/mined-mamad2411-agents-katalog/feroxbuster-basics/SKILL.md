---
name: feroxbuster-basics
description: >
  Use feroxbuster for authorized recursive content discovery: wordlists, status/size
  filtering, rate limits, recursion depth, extensions, and output triage. Use when
  enumerating paths on owned web apps, labs, or scoped pentests; tuning feroxbuster
  to reduce noise; comparing with ffuf/gobuster; or documenting hidden admin, backup,
  and API routes without reckless scanning.
---

# Feroxbuster Basics

## Scope And Authorization

- **In scope:** hosts and vhosts explicitly owned or listed in written engagement scope.
- **Out of scope:** Internet-wide scanning, third-party assets, or DoS via unbounded threads/recursion.
- Start low rate; respect robots only when policy says so—authorization still governs.
- Redact discovered credentials, session tokens, and personal data from exports.
- Pair any automation scripts with `code-quality-standards`.

## When To Use

- Recursive **directory/file discovery** with auto-collected links (`feroxbuster`).
- Mapping large apps where recursion and smart filtering beat one-shot fuzzers.
- Extracting endpoints from responses while walking trees.
- Producing machine-readable findings for later manual review.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| ffuf filter/fuzz craft | `ffuf-fuzz-basics` |
| Broader recon methodology | `recon-and-methodology` |
| Injection class testing after path found | `injection-checking` or class skill |
| Nuclei template scanning | matching vuln-scan skill / catalog |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Tool | `feroxbuster` (Rust recursive content discovery) |
| Inputs | base URL, wordlist, extensions, headers/cookies, proxy |
| Controls | `-t` threads, `--rate-limit`, `-d` depth, status/size/line filters, `--dont-recurse` |
| Outputs | stdout, JSON (`-o` / `--json`), silent mode for pipelines |
| Pitfalls | recursive explosion; 429 bans; false 200 catch-alls; scanning prod without rate cap |

## Core flags cheat sheet

| Flag | Purpose |
| --- | --- |
| `-u URL` | Target base URL |
| `-w wordlist` | Path wordlist |
| `-x php,aspx,bak` | Extensions |
| `-d N` | Recursion depth |
| `-t N` | Threads |
| `--rate-limit N` | Cap requests/sec |
| `-H "Name: value"` | Custom header (auth, Host) |
| `-C 404,403` | Hide status codes |
| `-S size` / `-N lines` | Filter by size/lines |
| `--auto-tune` / `--auto-bail` | Adaptive behavior when supported |
| `-k` | Insecure TLS (lab only; note risk) |
| `--methods GET,POST` | Methods when needed |
| `-o out` / `--json` | Save results |

## Workflow

### 1. Confirm scope and success criteria

1. Written scope: domains, paths allow/deny, max rps, time box, contact for WAF false positive.
2. Success: high-signal path list with evidence (status, size, redirect), not “scanned forever.”
3. Identify out-of-scope subdomains and third-party CDNs.

### 2. Prepare environment

1. Install known feroxbuster version; record `feroxbuster --version`.
2. Choose wordlist sized to time box (e.g. medium dir list first, then targeted).
3. Collect auth: cookie or Bearer for authenticated discovery if authorized.
4. Optional: Burp/ZAP upstream proxy for traffic review.

```bash
feroxbuster --version
# Wordlist examples (paths vary by distro)
ls /usr/share/seclists/Discovery/Web-Content/ 2>/dev/null || true
```

### 3. Baseline target behavior

1. Manual request for known 404 vs soft-404 (same size body for all unknown paths).
2. Note WAF headers, rate limits, and required Host/SNI for vhosts.
3. Seed with a few known paths to validate filters.

```bash
curl -sS -o /dev/null -w "%{http_code} %{size_download}\n" "https://app.example/does-not-exist-zzq"
curl -sS -o /dev/null -w "%{http_code} %{size_download}\n" "https://app.example/"
```

### 4. Run feroxbuster with safe defaults

```bash
# Owned/lab example — tune host, wordlist, rate
feroxbuster \
  -u "https://app.example/" \
  -w wordlists/common-dirs.txt \
  -x php,html,js,json,bak,old \
  -d 2 \
  -t 20 \
  --rate-limit 50 \
  -C 404 \
  -H "User-Agent: authorized-recon/1.0" \
  -H "Cookie: session=${SESSION}" \
  --json \
  -o ferox-app.json
```

1. Start shallow (`-d 1` or `2`); deepen only on interesting branches.
2. Filter soft-404 by size/words if needed (`-S`, `-W`, or response similarity features).
3. For APIs, add relevant extensions and methods carefully; avoid state-changing methods unless allowed.
4. Use `--dont-extract-links` if link extraction floods scope; use extraction when HTML apps hide routes.

### 5. Triage results

1. Prioritize: admin, backup, `.git`, debug, swagger, internal API, upload, actuator-style paths.
2. Deduplicate redirects and parameterized clones.
3. Re-request high-value hits manually; confirm authorization boundaries (IDOR next, not more blasting).

```bash
# Quick triage from JSON lines (shape depends on version)
# Inspect status != 404 and interesting keywords
grep -E 'admin|backup|swagger|debug|internal|\.git' ferox-app.json | head
```

### 6. Observe and reduce harm

1. If 429/503 spike: lower `--rate-limit`, threads, or pause.
2. Document WAF blocks vs real denials.
3. Do not auto-recurse into logout, password-reset, or payment confirm URLs.

### 7. Hand off

1. Deliver scoped path list, commands used (redacted secrets), false-positive notes.
2. Route findings: auth issues → relevant auth skills; injections → injection skills.
3. Archive wordlist name/version for reproducibility.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Named hosts + rate cap | Whole ASN “just to see” |
| Recursion | Depth limits + review | Unlimited depth on large CMS |
| Filtering | Soft-404 baseline first | 50k fake 200s unfiltered |
| Auth | Explicit cookie for app area | Unauth scan then claim full coverage |
| Methods | GET/HEAD default | Blind POST/PUT recursion |
| Evidence | Status+size+URL saved | Screenshot-only claim |

## Output Checklist

- [ ] Authorization and rate limits recorded
- [ ] Target baseline (404/soft-404) captured
- [ ] feroxbuster command and version documented
- [ ] Results saved (JSON/text) with redactions
- [ ] High-value paths manually verified
- [ ] Recursion and filters justified
- [ ] No out-of-scope hosts hit
- [ ] Follow-up skills identified for findings
- [ ] `code-quality-standards` if custom scripts shipped

## Rules

- Authorized targets only; treat aggressive recursion as potential DoS.
- Prefer feroxbuster-specific controls (depth, extract-links, filters) over generic “run fuzzer.”
- Never put production session tokens in shared tickets unredacted.
- Compare with `ffuf-fuzz-basics` when you need flexible multi-position fuzzing more than recursion.
- Evidence-driven triage beats raw hit counts.
