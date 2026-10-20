---
name: ffuf-fuzz-basics
description: >
  Use ffuf for authorized HTTP fuzzing and content discovery: FUZZ keyword placement,
  wordlists, matchers/filters (status, size, word, regex), rate limiting, multi-wordlist
  modes, and result triage. Use when enumerating paths, vhosts, parameters, or values
  on owned apps and scoped assessments—not for unbounded production DoS.
---

# Ffuf Fuzz Basics

## Scope And Authorization

- **In scope:** URLs and vhosts in written scope or owned labs/CTFs.
- **Out of scope:** unauthorized targets, credential stuffing third parties, or flood testing without approval.
- Cap threads and QPS; pause on 429/5xx storms.
- Redact cookies, tokens, and PII from `-o` exports before sharing.
- Pair wrapper scripts with `code-quality-standards`.

## When To Use

- Path, file extension, query parameter, header, or virtual-host fuzzing with **ffuf**.
- Fast filter/matcher iteration when soft-404s dominate.
- Comparing response clusters (size/words/lines) to find anomalies.
- Lightweight API value fuzzing with custom wordlists (authorized).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Recursive link-following discovery | `feroxbuster-basics` |
| Coverage-guided binary fuzzing | `fuzzing-libfuzzer-basics` |
| Engagement planning | `recon-and-methodology` |
| Injection exploitation after finding params | `injection-checking` / class skill |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Tool | `ffuf` |
| Core idea | Place `FUZZ` (or named keywords) in URL, headers, body, or Host |
| Match | `-mc` status match; default often non-filtered noise |
| Filter | `-fc`, `-fs`, `-fw`, `-fl`, `-fr` to drop boring responses |
| Rate | `-rate`, `-t`, delays; respect scope |
| Output | `-o` JSON/HTML/CSV; `-of` format |

## Essential flags

| Flag | Role |
| --- | --- |
| `-u` | URL with `FUZZ` |
| `-w` | Wordlist (`-w list:KEYWORD` for multi) |
| `-H` | Header (`Host: FUZZ` for vhost) |
| `-X` / `-d` | Method / body |
| `-mc` / `-fc` | Match / filter status codes |
| `-fs` / `-fw` / `-fl` | Filter size / words / lines |
| `-fr` | Filter response regex |
| `-t` / `-rate` | Threads / req per second |
| `-ac` | Auto-calibrate filters (when appropriate) |
| `-replay-proxy` | Send hits to Burp |
| `-b` | Cookie |

## Workflow

### 1. Confirm scope and success criteria

1. Scope hosts, paths, max rps, allowed methods, time box.
2. Success: small set of interesting responses with reproducible curl commands—not raw millions of lines.
3. Get auth material if authenticated fuzzing is approved.

### 2. Install and baseline

```bash
ffuf -V
curl -sS -o /dev/null -w "%{http_code} size=%{size_download}\n" \
  "https://app.example/this-path-should-404-zzq"
```

1. Measure baseline 404/soft-404 size and word count.
2. Pick wordlist proportional to time (start small).

### 3. Path discovery (typical)

```bash
ffuf -u "https://app.example/FUZZ" \
  -w wordlists/common.txt \
  -mc 200,204,301,302,307,401,403 \
  -fc 404 \
  -t 40 \
  -rate 50 \
  -H "User-Agent: authorized-ffuf/1.0" \
  -o ffuf-paths.json -of json
```

1. If all paths return 200 with same size, use `-fs <baseline_size>` or `-ac`.
2. Add extensions: `-e .php,.bak,.old` or second wordlist for extensions.
3. Authenticated: `-b "session=..."` or `-H "Authorization: Bearer ..."`.

### 4. Vhost and parameter patterns

```bash
# Vhost fuzz (owned DNS or lab hosts file)
ffuf -u "https://target.example/" \
  -H "Host: FUZZ.target.example" \
  -w wordlists/subdomains-top.txt \
  -fs 1234

# Query param values
ffuf -u "https://app.example/search?q=FUZZ" \
  -w wordlists/values.txt \
  -fw 10

# POST JSON value
ffuf -u "https://app.example/api/item" \
  -X POST -H "Content-Type: application/json" \
  -d '{"id":"FUZZ"}' \
  -w ids.txt -mc 200,500
```

### 5. Multi-wordlist and calibration

```bash
# Named keywords
ffuf -u "https://app.example/FUZZPATH" \
  -w paths.txt:FUZZPATH \
  -w ext.txt:FUZZEXT \
  # adjust URL to use both markers per ffuf docs for clusterbomb/pitchfork modes
```

1. Use pitchfork vs clusterbomb intentionally—clusterbomb multiplies traffic.
2. Recalibrate filters when content length shifts (deploy, A/B).

### 6. Triage and safety

1. Sort hits by status and size clusters; manually verify top findings.
2. On WAF block pages, tighten rate or change strategy—do not blindly raise threads.
3. Export only in-scope evidence; delete raw files with secrets after engagement.

```bash
# Example: summarize JSON (field names vary by ffuf version)
# jq '.results[] | {url:.url,status:.status,length:.length}' ffuf-paths.json | head
```

### 7. Hand off

1. Deliver commands, wordlist names, filter rationale, verified URLs.
2. Hand interesting params to injection skills; auth boundaries to IDOR/auth skills.
3. Note false positives (default vhost page, CDN).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Filters | Baseline size then `-fs`/`-ac` | Unfiltered 200 flood |
| Rate | Explicit `-rate` in prod-like | Unlimited threads “go faster” |
| Methods | GET discovery first | Recursive state-changing POST |
| Evidence | curl repro per hit | “ffuf found admin” without URL |
| Wordlists | Time-boxed growth | RockYou against paths |
| Scope | Host allowlist | Random CDN IPs |

## Output Checklist

- [ ] Authorization, rate limit, time box recorded
- [ ] Soft-404 baseline measured
- [ ] ffuf version and commands saved (secrets redacted)
- [ ] Match/filter strategy documented
- [ ] Hits triaged and manually verified
- [ ] Results archived with redaction
- [ ] Follow-up skills identified
- [ ] No out-of-scope hosts
- [ ] Scripts meet `code-quality-standards` if any

## Rules

- Authorized HTTP fuzzing only; ffuf is not permission.
- Prefer precise filters over noise; prefer rate limits over heroics.
- Do not confuse HTTP content discovery with libFuzzer-style binary fuzzing.
- Keep topic fidelity: FUZZ placement, matchers/filters, and triage—not generic SAST.
