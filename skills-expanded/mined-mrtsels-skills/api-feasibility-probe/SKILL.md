---
name: api-feasibility-probe
description: Probe a third-party API transport before building a client.
metadata:
  imported_from: hermes
---

# API Transport Feasibility Probe

Verify that a third-party HTTP API is actually reachable and client-friendly BEFORE writing a CLI/wrapper against it. Produces a structured, evidence-based report (each finding = command + real output). Do not fabricate results — run real commands.

## When to use
- Building a zero-dependency CLI/wrapper (urllib, curl, etc.) against an external API
- The API docs say one thing but requests behave unexpectedly (redirects, 404s, empty bodies)
- Any "does this API actually work from THIS machine" question

## Steps (in order)

1. **Confirm the base URL actually serves the API.** `curl -s -D - -o /dev/null <base>/<endpoint>`. If you get a 302/301, capture `location:` — a redirect to a docs/help page (`/help/index.html`, Swagger UI, Apifox site) usually means **the API moved hosts**. Recover the real host:
   - `curl -sL <base>/` and scan the served HTML/JS for URLs: regex `https?://[a-zA-Z0-9._/-]*<vendor>[a-zA-Z0-9._/-]*`
   - Test the discovered host immediately with one V1/simple endpoint.
2. **Check for per-version host separation (V1 vs V2).** A docs site may document V1 and V2 endpoints that live on **different domains**. Don't assume one host serves both: probe a V2 path on the V1 host — 404 there does NOT mean V2 is dead. Two reliable recovery sources when docs have `servers: []`:
   - The docs site's own HTML/JS (embedded config tokens often contain every live host).
   - **The official client source code on GitHub** (search `<vendor> <client> repo` → `config`/`ApiUrls`/`Endpoints` files, e.g. RailGo's `DefaultApiUrls.cs` maps each API name to its real URL). This is the ground truth for "which host serves which endpoint".
3. **Environment inventory** (context for the report): `python3 --version && which python3` (check the specific version the target code needs, e.g. 3.10+ for `dict | None`); check alternate interpreters (`python3.11/3.12/3.13`); `git status` in the target dir; proxy env vars `echo $HTTP_PROXY $HTTPS_PROXY $ALL_PROXY`.
4. **Latency**: 3 GETs per endpoint with `curl -s -o /dev/null -w "code=%{http_code} total=%{time_total}s dns=%{time_namelookup}s connect=%{time_connect}s tls=%{time_appconnect}s size=%{size_download}B"`, report min/avg/max. Include DNS/connect/TLS breakdown — it distinguishes CDN/WAF latency from app latency.
5. **UA sensitivity**: default curl UA, explicit `-A "curl/8.0"`, empty `-A ""`, and one full browser UA. Identical results = UA-insensitive (safe for urllib).
6. **gzip behavior**: request once WITH `-H 'Accept-Encoding: gzip'` and once WITHOUT; compare `content-encoding` / `content-length` / `vary`. Key fact: `urllib.request` sends NO `Accept-Encoding` and does NOT auto-decompress. If the server only gzips when asked, urllib is safe with zero extra handling; if you add the header you MUST decompress yourself.
7. **Encoding**: fetch a Chinese/unicode-bearing endpoint, pipe through `python3 -c "import json,sys; print(json.load(sys.stdin))"` (or a script file). Watch for `\uXXXX` escapes — they're valid JSON and decode fine.
8. **Response size**: fetch a known-large endpoint, report byte size.
9. **Headers audit**: `curl -sI` / `-D -` — look for rate-limit headers (`x-ratelimit-*`, `ratelimit`), cache headers (`age`, `eo-cache-status`), WAF/CDN fingerprints (`server: openresty/nginx`, `x-waf-*`, `eo-log-uuid` = Tencent EdgeOne).

## Pitfalls
- **302-to-docs-page = API moved.** Do NOT keep hammering the documented path. The docs site usually embeds the real API host in its HTML/JS — extract it.
- **404 on one host ≠ endpoint dead.** V1/V2 may be split across domains (RailGo: V1=`data.railgo.zenglingkun.cn`, V2=`rg-api.zenglingkun.cn`). Probe the other host before concluding an endpoint is gone.
- **Verify subagent/parallel-probe reports yourself.** A probe subagent that never discovers the alternate host will confidently report "all endpoints fail" (happened for RailGo V2). Spot-check the top-2 most important claims with your own curl before acting on them.
- **Hermes terminal blocks shell commands whose payload contains `<`** (e.g. `grep -oE "<title>..."` gets hardline-blocked with "command parser limit"). Workaround: use `search_files` for greps, or `write_file` a small `.py` script and run it — don't retry inline.
- **fake-ip DNS = TUN proxy is active even with empty env vars.** If `dig` returns `198.18.0.0/15` addresses, a Clash/Surge-class TUN proxy is intercepting; `scutil --proxy` will show the local proxy port. `urllib` won't see env-var proxies (empty), but TUN still forces traffic through the tunnel — latency and egress IP reflect that.
- **Distinguish "docs site serves the host" from "API serves the host".** `curl -L <base>/` returning a 100KB+ Apifox/Swagger page while `/api/*` 404s or redirects means the host is docs-only now.
- Set generous timeouts in the client (5s+) when observed latency is 0.3–0.6s per request; CDN/WAF hops add ~0.2s TLS time alone.
- **Docs may be wrong about param names.** RailGo's `getCoachPic`/`mapLine` use `train`, not `trainNum`. Missing-param error messages (`Missing required param 'train'.`) reveal the true name — read them.

## Report format
Numbered findings in the user's language, each with the exact command run and its real output; lead with the single most important conclusion (e.g. "the documented base URL is dead, the real one is X").

## Support files
- `references/railgo-api.md` — RailGo API transport facts (real base URL, V1/V2 host split, this Mac's env) as of 2026-08.
- `references/python-cli-argparse-pitfalls.md` — dual-position global flags (`--pretty` after subcommand) via `parents=[common]` + `default=argparse.SUPPRESS`.
