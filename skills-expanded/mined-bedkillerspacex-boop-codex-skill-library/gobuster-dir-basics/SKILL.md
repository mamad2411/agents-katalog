---
name: gobuster-dir-basics
description: >
  Authorized directory/vhost/DNS content discovery with Gobuster: dir mode,
  wordlists, extensions, status filtering, threads, and evidence capture. Use
  only on owned labs/CTFs or systems with written authorization — never random
  Internet targets.
---

# Gobuster Dir Basics

## Scope And Authorization

- **In scope:** Targets you own, deliberately vulnerable labs, CTFs, and engagements
  with **written authorization**.
- **Out of scope:** Unauthorized brute-force of third-party sites; DoS via extreme threads;
  using findings to access data outside ROE.
- Prefer staging/non-prod; rate-limit threads; stop on instability.
- Redact discovered admin paths if reports go external.
- Pair with `recon-and-methodology` for engagement planning.

## When To Use

- Finding hidden paths (`/admin`, `/backup`, `/api/v2`) on authorized web apps.
- Quick content discovery before heavier tools.
- DNS/vhost modes when those are in scope (this skill emphasizes **dir** mode).
- Teaching controlled brute-force enumeration.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full engagement methodology | `recon-and-methodology` |
| SQLi exploitation | `ghauri-sqli-lab` / `sqli-sql-injection` |
| HTTP smuggling | `request-smuggling` / `http2-specific-attacks` |
| Authenticated app mapping | Burp-centric API recon skills |
| Implementation quality for fixes | `code-quality-standards` |

## Concepts

| Mode | Purpose |
| --- | --- |
| `dir` | Path/file discovery |
| `dns` | Subdomain brute (authorized) |
| `vhost` | Virtual host discovery |
| `fuzz` | Custom FUZZ keyword (versions vary) |
| Wordlist | Candidate paths |
| Status filter | Include/exclude HTTP codes |
| Extensions | `.php`, `.bak`, `.git` etc. |

## Workflow

### 1. Authorization gate

1. Record target URL, owner, ROE, max rps/threads, blackout paths.
2. Success: list of interesting paths with status codes; no out-of-scope access.
3. If production: obtain change window / lower threads.

### 2. Install

```bash
# Go install
go install github.com/OJ/gobuster/v3@latest
gobuster version

# Or distro package / prebuilt release
```

### 3. Wordlists

```bash
# Common locations (SecLists)
# /usr/share/seclists/Discovery/Web-Content/common.txt
# raft-medium-directories.txt for deeper labs
```

Start small (`common.txt`); escalate only if needed and allowed.

### 4. Basic dir scan

```bash
gobuster dir \
  -u https://lab.example.local/ \
  -w /path/to/common.txt \
  -t 20 \
  -o gobuster-dir.txt
```

HTTPS labs with lab CA issues:

```bash
gobuster dir -u https://lab.example.local/ -w common.txt -k
```

### 5. Extensions and filters

```bash
gobuster dir \
  -u https://lab.example.local/ \
  -w common.txt \
  -x php,txt,bak,old,zip \
  -s "200,204,301,302,307,401,403" \
  -b "" \
  -t 20 \
  -o gobuster-ext.txt
```

Tune `-b` (blacklist status) vs `-s` (show) per Gobuster version help:

```bash
gobuster dir -h
```

### 6. Authenticated / header needs

```bash
gobuster dir \
  -u https://lab.example.local/ \
  -w common.txt \
  -H "Authorization: Bearer <lab-token>" \
  -H "Cookie: session=..."
```

Do not put real production tokens into shared logs; use lab tokens.

### 7. Interpret results

| Status | Typical meaning |
| --- | --- |
| 200 | Accessible resource — review sensitivity |
| 301/302 | Follow carefully; note Location |
| 401/403 | Exists but protected — still intel |
| 404 | Missing (or soft-404) |
| 500 | Maybe interesting; don’t hammer |

Soft-404s: baseline a known bad path size; filter false positives manually.

### 8. Evidence and next steps

1. Save command line + wordlist name + timestamp.
2. Screenshot or curl interesting hits.
3. Hand off to vulnerability testing skills **within ROE**.
4. Remediation guidance: remove dead paths, authZ, disable dir listing, WAF only as defense-in-depth.

```bash
curl -i https://lab.example.local/admin
```

### 9. Safety limits

| Control | Guidance |
| --- | --- |
| Threads `-t` | Start 10–20; raise only if stable |
| Wordlist size | Escalation path agreed |
| Delay | Use tool delay flags if available under load |
| Scope URLs | Single host/path prefix in ROE |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Written ROE lab | Random `.gov` scan |
| Threads | Conservative | 500 threads DoS |
| Wordlists | Start small | Entire rockyou as paths |
| Secrets | Lab tokens only | Prod session in public gist |
| Reporting | Paths + status + impact | Dump only with no analysis |

## Output Checklist

- [ ] Authorization/ROE recorded
- [ ] Target and rate limits set
- [ ] Gobuster version noted
- [ ] Wordlist documented
- [ ] dir results saved
- [ ] Interesting paths manually verified
- [ ] Soft-404 considered
- [ ] Findings filed with remediation
- [ ] Tokens redacted from reports

## Rules

- Authorized targets only — hard rule.
- Minimize load; stop if service degrades.
- Discovery ≠ exploitation without ROE.
- Prefer fix guidance over pure loot lists.
- Other Gobuster modes need same authorization bar.
