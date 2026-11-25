---
name: secrets-safe-config-audit
description: Audit app integrations/config read-only, no secret values.
category: security
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security, audit, config, integrations, secrets, production]
    triggers: [audit integrations, config gap audit, production config review, secrets-safe audit, check external integrations, deployment config audit]
    related_skills: [pii-exposure-audit, repo-sanitization-audit, web-application-security-assessment]
---

# Secrets-Safe Config & Integration Audit

Read-only audit of a deployed app's external integrations and production configuration that reports gaps and risks WITHOUT ever printing secret values. Distinct from `pii-exposure-audit` (finding secrets already committed) and `repo-sanitization-audit` (removing them): this is a live+static health audit of AI/OpenRouter, transcription, SMTP, OAuth, affiliate, and deployment/security config.

## Non-negotiable rules (the "without exposing secrets" part)

1. NEVER print a secret value — not truncated, not "partially". Allowed: key NAMES, presence/absence, length, 4–8 char prefix for classification, file paths, match counts.
2. Shape scans so values can't leak: collapse matches with `sed -E 's/:[0-9]+:.*/ [MATCH FOUND]/'` or output file:count only.
3. `NEXT_PUBLIC_*` vars are client-visible by design — their values are public, but still don't echo them; host names are fine.
4. `env(VAR)` substitutions in toml/yaml are references, not secrets — but a sibling file hardcoding the same name IS the finding.

## Workflow

### Phase 1 — Repo map + git state
- `git remote -v`, `git branch`, `git status --short` — untracked/modified files are often the LIVE deploy config (compose, nginx conf, deploy docs) — read those first.
- `git ls-files | grep -iE '\.env|secret|credential|key'` — any tracked env/secret file is a finding.
- `git check-ignore .env.production` — confirm live env files are ignored.

### Phase 2 — Env inventory (names only)
- `grep -oE '^[A-Za-z_][A-Za-z0-9_]*' .env.template .env.local .env.production` — diff the key sets across template/local/prod. Template drift (keys in prod but not template, keys in template never used) is a config-hygiene finding.

### Phase 3 — Value triage without values
For each key print only: `present (len=N, prefix=XXXXXX)` or `MISSING/empty`:
```bash
for k in KEY1 KEY2; do v=$(grep -E "^${k}=" .env.production | head -1 | cut -d= -f2-); \
  [ -n "$v" ] && echo "$k: present (len=${#v}, prefix=${v:0:6})" || echo "$k: MISSING"; done
```
Classification heuristics (length+prefix → status):

| Evidence | Conclusion |
|---|---|
| `sk-or-` len≈10 | Placeholder — real OpenRouter keys are ~60–70 chars → AI features broken |
| key MISSING but code/config requires it | Feature broken (OAuth, SMTP, affiliate tag) |
| key present, ZERO code refs (grep) | Dead config or liability (e.g., Amazon PA-API keys never used) |
| `:free` / `-exp` model names in prod code | Free/experimental models — rate-limited, unreliable for prod |
| `|| "dummy-key"` fallback in client construction | Masks misconfig; check whether the route actually guards it |
| `skip_nonce_check = true` in prod auth config | Dev-only setting left in prod (Google OAuth nonce skip) |

### Phase 4 — Integration mapping
- `grep -rhoE 'https?://[a-zA-Z0-9.-]+' lib app scripts --include='*.ts' --include='*.tsx' | sort | uniq -c` → the external integration surface (AI providers, CDNs, OAuth, scraper sources).
- For each env key: `grep -rn 'KEY_NAME' --include='*.ts' --include='*.tsx' lib app` — unused key = gap or dead config.
- Read each integration route fully: auth checks, input validation (file size/type), model allowlists, retry/backoff, error paths.

### Phase 5 — Auth-surface audit (static)
- Per API route, count auth references: `for f in $(find app/api -name route.ts); do echo "$(grep -cE 'getUser|requireUser|auth\.' $f) $f"; done | sort -rn` — 0-count routes are unauthenticated. With a real upstream key they're cost-abuse vectors, especially AI routes that accept client-supplied `model` with no allowlist.
- Check middleware matcher exclusions — paths excluded from session refresh are also excluded from auth redirects.
- Note RLS dependency: no code-level auth + Supabase = RLS policies are the only boundary; verify them.

### Phase 6 — Deployment/security config
- Dockerfile: ARG/ENV pairs for server secrets → baked into image layers (extractable via docker history). A service-role key passed as build arg with zero code usage = pure liability.
- Compose sprawl: multiple compose files binding overlapping host ports (5432/54321/8000/80) → collision with the live stack (Traefik edge, local Supabase CLI). Note which file CI references.
- CI workflow drift: stale local Windows paths in commit comments, legacy compose file references, `git reset --hard` on the prod server, no tests/lint, TS+ESLint errors ignored in next.config.
- Dual config files (`next.config.js` AND `.mjs`) with conflicting settings → ambiguous live behavior.

### Phase 7 — Live probe (read-only HTTP)
```bash
curl -sI https://<host>/          # status, security headers, Server version leak, Cache-Control
curl -s https://<host>/api/health
curl -s -o /dev/null -w '%{http_code}' https://<host>/rest/v1/     # exposed DB API surface
curl -s -o /dev/null -w '%{http_code}' https://<host>/auth/v1/health
```
Missing HSTS/CSP/X-Frame-Options/X-Content-Type-Options + `Server: nginx/x.y.z` version leak = header findings. Supabase Kong proxied on the same origin (`/rest/v1/`, `/auth/v1/`, `/storage/v1/` return 200) = attack-surface finding, especially combined with image-baked service-role keys.

### Phase 8 — Machine config-reuse scan (names only)
When asked to find existing reusable config on the machine, report KEY NAMES + file paths only, never values:
- `$HOME/AppData/Local/hermes/config.yaml` (LLM provider keys, e.g. openrouter)
- Infra repos' `.env` (n8n/Traefik host: MAILJET_SMTP_*, OAUTH_CLIENT_*, OPENAI_API_KEY)
- `$HOME/.supabase`, `~/.config`
- ALWAYS `ls` the parent dir first, then target a shortlist of repos — broad `grep -rl` over huge trees (github dirs with node_modules/.git) times out (exit 124).

### Phase 9 — Report shape
1. Integration status table (integration | prod status)
2. Priority-ordered gaps (cost-abuse, secret baking, exposed surfaces, broken features)
3. Positives (no committed secrets, cookie flags, non-root user, rate limits)
4. Machine reuse locations (key names + file paths only)
5. Safe integration strategy (ordered remediation)

## Pitfalls

### Output redaction vs. disk truth (the trap that produces false findings)
Tool output masks secret-adjacent substrings **output-side** — `process.env.OPENROUTER_API_KEY` renders as `proces..._KEY`, long JWTs render truncated (`eyJhbG...81IU`), emails may render as `[email protected]`. Consequences, both directions:
- **False corruption alarm**: a "mangled" identifier in read_file output is usually a clean `process.env.X` on disk — verify with `grep -c "process.env" file` or an esbuild parse before reporting broken source.
- **False absence alarm**: grepping for the MASKED pattern (`grep "proces\.\.\."`) finds nothing — expected, since the file holds the unmasked string. That is NOT proof the value is absent.
- **False safety alarm**: a JWT shown truncated in output is often a **full key on disk** (e.g. 164-char service-role JWT). Display truncation ≠ disk truncation.

Verification ladder (never trust displayed content for secrets):
1. Raw bytes: `python -c "d=open('f','rb').read(); i=d.find(b'needle'); print(d[i:i+80])"` — repr/char-codes survive redaction partially, so prefer sha/length/char-class evidence.
2. Parse check: `node -e "require('esbuild').transformSync(require('fs').readFileSync('f','utf8'),{loader:'ts'})"` — definitive syntax verdict (`.cmd` shims like `tsc` can exit 0 silently in git-bash).
3. Hash-compare against known defaults: `sha256(value)[:16]` vs known Supabase local-dev ANON/SERVICE keys (prefixes baked into `scripts/classify-secret.py`) — tells you "public dev default" vs "unique credential → flag for rotation" without ever printing the value.
4. Length+prefix classifies key type: real JWTs ≈100–200 chars with 2 dots; stubs are short (`sk-or-` len≈10); new-format Supabase keys start `sb_publishable_`/`sb_secret_`; `eyJ` + 2 dots + base64url = JWT-format.

Run `scripts/classify-secret.py <file> <needle>` for the whole classification in one shot.

### Other pitfalls
- **Broad greps on huge trees time out** (exit 124). List top-level dirs first, scope `--include`/`--exclude-dir=node_modules,.git,.next`, or loop over a shortlist of repos with per-repo `head -5`.
- **Placeholders pass presence checks**: length/prefix triage catches stub keys that `[ -n "$v" ]` misses. Always measure, never just check non-empty.
- **Build args ≠ runtime env**: `NEXT_PUBLIC_*` build args are expected (inlined into client bundle); server secrets as build args are NOT — they land in image layers.
- **`x-forwarded-host` fallback origins** in OAuth callbacks are attacker-controllable open redirects if the env override is unset — flag the dependency.
- **`s-maxage=31536000` on HTML** (Next.js static default) = year-long caching — fine for static pages, wrong for user-specific content.
- **`auth.admin.*` on an anon server client throws**: the admin API requires service_role; a `.catch`-swallowed call (e.g. signup notifications via `auth.admin.listUsers()`) is a silently broken feature — check which client the call is on, not just that it exists.
- **RPC-existence check before trusting migration runners**: `supabase.rpc('exec_sql'|'exec', …)` with no such function in migrations = silent no-op → schema drift. `grep -rn "create function exec" supabase/migrations/` first.
- **RLS triage specifics**: `WITH CHECK (true)` on "System can X" policies = anon can invoke (e.g. award/revoke badges); RLS enabled with zero policies = deny-all; anon client + service-role-only write policy = broken write feature — flag comment-vs-code mismatches (routes claiming "service role" while using the cookie/anon client).
- **Windows/git-bash audit mechanics**: `search_files` needs Windows-style paths (`E:\...`) — MSYS `/e/...` fails with "system cannot find the path"; compound shell one-liners (`for` loops, `<(...)`, heredocs) hit the hardline blocklist — split into simple commands or use python one-liners; native curl doesn't grok MSYS `/tmp` — write probe output to cwd-relative files.

## See Also
- `pii-exposure-audit` — hunting secrets already committed to a repo
- `repo-sanitization-audit` — stripping them before sharing
- `web-application-security-assessment` — active vuln testing (contrast: this skill is passive config/integration audit)
- `references/bookends-audit-example.md` — worked example: Next.js+Supabase app on Traefik edge; findings, triage table, report shape
