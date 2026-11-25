---
name: captcha-solver-service
description: Use when solving captchas or integrating with the self-hosted captcha-solver on the VPS. Covers the local HTTP API at :8877.
version: 1.0.0
license: MIT
platforms: [linux]
---

# Captcha Solver Service (self-hosted sidecar)

## Service facts
- **Endpoint:** `http://127.0.0.1:PORT_SOLVER` (FastAPI). Bearer token REQUIRED on ALL endpoints incl `/health` (liveness included deliberately — anonymous scanner learns existence otherwise). Token: `~/app` (plaintext, 600). `SOLVER_ALLOW_UNAUTHENTICATED=1` is the explicit opt-out.
- **Public endpoint:** `https://solver.gyukopo.dev` (verified live 2026-09-26) — Worker `domba-solver-proxy` fetches `http://178.83.181.248.sslip.io:8878` (sslip.io hostname beats CF raw-IP fetch block 1003) → Caddy Bearer auth (`cfsk_…` key in `/tmp/solver_apikey.txt`) → 8877. `/health` no auth. iptables: 8877 loopback-only, 8878 CF-CIDR-only. Worker src `/tmp/solver-proxy` (npx wrangler deploy). Worker fetch to cfargotunnel = 1102; raw IP = 1003; socket non-std port = cancelled — don't retry those paths.
- **Deployed at:** `/opt/captcha-solver/` (venv `./venv`, code from github captcha-solver (self-hosted) ⭐267,  — user often typos the org).
- **systemd:** `captcha-solver.service` — enabled, runs under `xvfb-run -a` (headed, 1920x1080), `BROWSER_HEADLESS=0`, `TURNSTILE_GEOIP=1`, `RECAPTCHA_GEOIP=1`, `PORT`, `SOLVER_API_TOKEN_SHA256=…`. Restart=always. Actual binary: `~/app/solver/.venv/bin/python3 server.py` (NOT /opt — old path stale; grep unit file before editing). Unit edits need `sudo` (root shell denied). File edits to `~/app/solver/web/*.py` need no sudo, then `sudo systemctl restart captcha-solver`.
- **11 types:** turnstile, recaptcha, hcaptcha, cloudflare, awswaf, botguard, datadome, perimeterx, akamai, aliyun, arkose.
- **Endpoints:** GET /health /status /logs /docs /redoc; POST /solve.
- **Docs file:** `/opt/captcha-solver/API_DOCS.md` — full request/response reference + curl/Python examples.
- Dependencies incl. `cloakbrowser[geoip]` (anti-detect Chromium) + playwright chromium + ONNX models (aliyun YOLO, recaptcha cls).

## Core API pattern
```bash
curl -X POST http://127.0.0.1:PORT_SOLVER/solve \
  -H "Authorization: Bearer $(cat ~/app)" \
  -H "Content-Type: application/json" \
  -d '{"type":"turnstile","sitekey":"0x4AAAAAAAhr9JGVDZbrZOo0","url":"https://accounts.x.ai"}'
```
- Success signal = `solved: true` (NOT token presence). Response also has: token, method, elapsed, error.
- Per-request proxy: `"proxy": "http://user:pass@host:port"` — honored by ALL types; clearance cookies are IP-bound → replay from same proxy IP.
- `timeout_s` default 60 → 408 on expiry. 400 = bad request/SSRF guard (private targets need `SOLVER_ALLOW_PRIVATE=1`).
- Verified live 2026-09-26: turnstile on accounts.x.ai solved in 8.9s via method "route".

## Gotchas
- Turnstile tokens are one-shot & expire in ~300s — use immediately.
- Don't parallelize same type >1-2 (shared browser serializes).
- grok-x-farm's Turnstile sitekey `0x4AAAAAAAhr9JGVDZbrZOo0` works with this solver (tested).
- Code updates: edit `~/app/solver` then `sudo systemctl restart captcha-solver`; scratch copy lives in profile cache.
- Solver failing diagnostics: `:8877 /health` OK ≠ solves working. `solved: true` is the only success signal. When solves all fail while daemon looks healthy, check EGRESS FIRST, not solver logic: `curl /proxy-check` (or `curl https://challenges.cloudflare.com/cdn-cgi/trace` direct), and confirm the proxy listener is up (`ss -tlnp | grep <port>`). A dead proxy (e.g. warp `socks5://127.0.0.1:1080` not listening, no process) makes every solve fail regardless of solver health — clearance cookies/tokens are IP-bound, so a broken egress path yields 100% failure with healthy uptime.
- Token hash is `sha256(token_string)` — the auth/lib hashes UTF-8 bytes of the token value, NOT the `openssl rand -hex | sha256sum` output (that hashes the hex text). Generate digest with `python -c "import hashlib; print(hashlib.sha256('$TOKEN'.encode()).hexdigest())"` and verify the curl works before trusting the unit edit. Wrong hash = silent persistent 401.
