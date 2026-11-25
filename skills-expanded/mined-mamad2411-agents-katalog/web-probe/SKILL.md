---
name: web-probe
description: Use when probing a declared web application or API for vulnerabilities under an engagement contract (OWASP-style checks, injection, auth, fuzzing, templated scans). Routes to extensions/offsec-tools/wrapper.py tools: zap-baseline, sqlmap, nuclei, ffuf. Passive-first; active scanning requires confirmation.
triggers: [user, model]
---

# Web Probe

Web/API offensive testing under contract, via
`extensions/offsec-tools/wrapper.py` (domain `web`).

## Contract (mandatory)

`--target` (URL), `--window`, `--roe`. ROE should state allowed methods,
rate limits, and out-of-scope paths.

## Tools

| Tool | Mode | Use |
|---|---|---|
| `zap-baseline` | active | OWASP ZAP baseline container scan |
| `nuclei` | active | templated CVE/misconfig scan |
| `sqlmap` | active | SQLi detection on a parameterized endpoint |
| `ffuf` | active | content/param/vhost fuzzing with wordlist |

## Commands

```bash
W=extensions/offsec-tools/wrapper.py

python $W doctor                         # tool availability by backend
python $W run --tool nuclei --target https://t.example \
  --window "..." --roe "..." --confirm -- -u https://t.example -severity high
python $W run --tool zap-baseline --target https://t.example \
  --window "..." --roe "..." --confirm --backend docker \
  -- -t https://t.example
python $W run --tool sqlmap --target "https://t.example/i?id=1" \
  --window "..." --roe "..." --confirm -- -u "https://t.example/i?id=1" --batch
```

All four are `mode: active` -- `--confirm` required per run. Methodology:
OWASP WSTG as checklist; passive review (headers, TLS via `testssl.sh`
in `net-probe`) before any active probe.

## Evidence

Per finding: request/response pair, tool version, template/rule id,
confidence, and false-positive notes. Reproduce before reporting as
`confirmed`; otherwise `likely`.

## Boundaries

- No auth bypass against third-party IdPs; declared scope only.
- Rate limits and denied paths from ROE are hard stops, not hints.
- No credential stuffing or account harvesting.
