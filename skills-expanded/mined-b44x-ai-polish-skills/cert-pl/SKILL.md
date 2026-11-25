---
name: cert-pl
display_name: CERT Polska — podejrzane linki
version: 1.0.0
description: >-
  Check a domain or HTTP(S) URL against the active CERT Polska warning list, including matching subdomains. Use for "sprawdź link", "podejrzany SMS", "dopłata do paczki", "czy domena jest na liście CERT". Does not visit the submitted URL or certify that an unlisted site is safe.
category: utilities
language: pl
country: PL
license: MIT
author: Michell Hoduń (https://github.com/b44x)
repository: https://github.com/b44x/ai-polish-skills
network: true
authentication: none
source: CERT Polska (NASK-PIB)
source_type: official_api
official: true
homepage: https://cert.pl/lista-ostrzezen/
documentation: https://cert.pl/lista-ostrzezen/
rate_limit: "Local cache: 5 minutes; no published request quota"
last_verified: 2026-11-04
tags:
  - cert
  - phishing
  - oszustwa
  - podejrzane-linki
  - sms
  - bezpieczenstwo
compatibility: Python 3.8+ (standard library only); internet access required.
---

# CERT Polska domain checks

## Running the script

Run from this skill's directory:

| OS | Command |
|---|---|
| Linux / macOS | `python3 scripts/cert_pl.py check <domain-or-url>` |
| Windows | `py scripts/cert_pl.py check <domain-or-url>` |

Example: `python3 scripts/cert_pl.py check https://cert.pl/`.

## Interpreting results

- Accept a domain or a full HTTP(S) URL. The script extracts the hostname locally, normalizes IDNs and checks the CERT list. It does not visit the submitted URL, follow its redirects or expand shortened links.
- `listed: true` means the domain or a parent domain appears on the active list. Cite `matched_domain` and `list_fetched_at`.
- `listed: false` means only that no entry was found. State that this does not establish the site's safety: the list is not a complete inventory of threats.
- Do not accept IP addresses, URL credentials or other protocols. Do not send SMS contents to external services.
- The cache is in `$XDG_CACHE_HOME/ai-polish-skills/cert-pl/` or `~/.cache/ai-polish-skills/cert-pl/`. Entries are valid for up to 5 minutes. A failed refresh returns an error rather than an old list. Failure to write the cache does not prevent an online lookup.

## Output and exit codes

Success, including an unlisted domain: JSON on stdout, exit `0`. Errors: JSON on stderr with `error` and `type`, exit `64` for input errors or `69` for source/network errors. `--help` and `-h` return `0`.

Read [references/output.md](references/output.md) for fields and an example.
Source and reuse terms: [CERT Polska](https://cert.pl/lista-ostrzezen/).
