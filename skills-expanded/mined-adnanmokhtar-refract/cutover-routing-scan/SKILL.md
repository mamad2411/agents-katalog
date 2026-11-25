---
name: cutover-routing-scan
description: "Strangler cutover: façade routes, shared session, shadow isolation, one-step rollback — read-only."
kind: skill
pack: migration
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: cutover-routing-scan

## Premise

During a strangler cutover both halves serve traffic. A façade decides which half answers each route and method; a session crosses between them; a shadow copy of V2 receives mirrored traffic; V1 stays warm so a flag can send traffic back. Each of these is configuration, not application code, so no test of either app sees it.
- A `location = /api/tickets` sends every ticket sub-path back to a V1 that stopped receiving writes.
- A mirror with no method match replays order placements on a shadow wired to the production mail relay.
- A V1 worker scaled to 0 turns the rollback into an outage.

This skill owns the strangler classes **CO-1, CO-2, CO-3 and CO-5** (CR §1–§4). It reads the façade, mesh and ingress config, the session and CSRF settings of both halves, the shadow environments and the V1 runtime manifests, and judges each against the ledger: which feature is `V2-only`, `V2-canary`, `V2-shadow` or still V1, and who owns writes. The comparator class CO-4 is `parity-proof-scan` §5.

**Every finding cites the config line, the ledger state or flag it contradicts, and the V1 fact (the route, the cookie, the worker's job), with its oracle.** A shadow that can write is a **blocker** at any mirror percentage (precedent 17). "Routing is fine" is never printed without the class-coverage block (§ Output).

## The rule

A candidate becomes a finding only when all four hold:

1. **The rule is live.** The façade or manifest file is deployed (referenced by the deploy, the mesh namespace, or the runbook), not an example.
2. **The ledger says otherwise.** The feature's state (`ai/migration/ledger.md`) and write owner (the `<feature>.writes_owner` flag) disagree with where the rule sends a method. V1 still owns work the rule turns off, or both halves serve a route whose session does not cross (precedent 19).
3. **Nothing upstream or downstream corrects it.** Read the next matching rule, the mesh `VirtualService` order, a gateway in front, and V2's own handler for the method (precedent 28).
4. **No record makes it intentional.** There is no ADR or plan step that moves the boundary on purpose (precedents § 3).

## Boundaries

- The comparator, its tolerance and control-vs-control calibration (CO-4) → `parity-proof-scan` §5. Effects a V2 subscriber duplicates during dual run (SE §2) → `side-effect-parity-scan`. Data flips, fences and reverse paths (DM-11, DM-12) → `data-cutover-orchestrate` §10–§11. This skill owns the traffic flag and V1 kept warm (CO-5).
- Cookie flags as a security property (`Secure`, `HttpOnly`, `SameSite=None` on an auth cookie) → security, when the security pack is installed. This skill reports only the **V1≠V2 difference** that breaks identity across the halves. Without the security pack, the hardening row is out of scope here and the coverage block says so.
- Single-codebase router traps (a trailing slash, a prefix) inside V2 → backend `http-contract-scan` §11, when the backend pack is installed.
- A V1 route V2 never implemented (MG-RT-1) → `surface-parity-scan` §1. Here a route counts only when the façade sends it to the wrong half.

## Lanes

| Layer | Routing (§1) | Session / CSRF (§2) | Mirror and shadow (§3) | V1 kept warm (§4) | Tag |
|---|---|---|---|---|---|
| **nginx** | `location [= \| ^~ \| ~]`, the first match wins by type; `proxy_pass` to an upstream or a `map $request_method` | `proxy_cookie_domain`, `proxy_cookie_path` | `mirror /path;` + `mirror_request_body` (on by default: buffers the body on the primary path) | — | [V] port-pair |
| **Istio / Envoy** (1.31 / 1.38 docs) | `VirtualService` `http[].match` order; `uri: {exact \| prefix}`, `method:` | — | `mirror:` + `mirrorPercentage` (absent = 100%); Envoy `request_mirror_policies`; shadow requests carry a `-shadow` host suffix | — | [V] port-pair |
| **Gateway API / Ingress / ALB / YARP / Traefik** | `HTTPRoute` matches, `Ingress` `pathType: Exact \| Prefix`, ALB listener rules, YARP `Match.Path`, `IngressRoute` | — | `HTTPRoute` `RequestMirror` filter | — | [K?] |
| **Next.js / SPA hosts** | `rewrites()` (`beforeFiles`, `fallback`) | — | — | — | [K?] |
| **Laravel (V1)** | — | `config/session.php` (`cookie`, `domain`, `path`, `same_site`, `driver`, `serialization`), `XSRF-TOKEN` cookie + `X-XSRF-TOKEN` header by default, `APP_KEY` encryption | — | `php artisan queue:work`, `schedule:run` | [V] port-pair |
| **NestJS / Fastify / Express (V2)** | — | `@fastify/cookie` / `express-session` options, a CSRF hook's cookie and header names, JWT keys and claims | Scientist-style `try` blocks (tzientist 4.0.2) that write | — | [V] port-pair |
| **Rails / Django** | — | `session_store` `domain:` / `SESSION_COOKIE_DOMAIN`, `CSRF_COOKIE_NAME` | — | Sidekiq, Celery beat | [K?] |
| **Kubernetes / cloud** | — | — | shadow `Deployment` env, secrets | `replicas: 0`, `suspend: true`, an ASG `min_size = 0`, ECS `desired_count = 0` | [V] port-pair |

GoReplay 1.3.3 (`--output-http`) replays writes for real; its middleware is where a comparator plugs in. A replay 401 storm is usually expired session tokens, not a regression (research notes A1).

## Tool lane and ledger

Static only, offline. No request is sent to either half or to the façade. The oracles are a façade route probe (V383), a session crossing test (V384), a shadow effect journal (V371 with the mirror on) and a rollback rehearsal (V382). They run against a staging façade and are requested in the output. `paired-inventory` supplies the V1 route list (`I-ROUTES`), so a rule can be checked against every V1 sub-path it must cover. Read its ledger first.

## Pre-flight

Run as one script (bash 3.2-safe). `V2` is the V2 root (where the deploy config lives; point it at the infra repo if the façade lives there). `V1` is the V1 root, empty in solo mode. `MIG` holds `ledger.md`, `pair-map.tsv` and `v1-inventory/`. The script greps from **inside** V2. Every grep ends in `ck`: exit 2 is a blocked class, never zero hits.

```bash
PI="${PI:-.claude/skills/paired-inventory/scripts/pair-inventory.py}"; V2="${V2:-.}"; V1="${V1:-}"; MIG="${MIG:-$V2/ai/migration}"
abs() { (cd "$(dirname "$1")" 2>/dev/null && printf '%s/%s\n' "$(pwd)" "$(basename "$1")") || printf '%s\n' "$1"; }
PI=$(abs "$PI"); MIG=$(abs "$MIG"); [ -n "$V1" ] && V1=$(abs "$V1"); cd "$V2" || exit 2
OUT="$(mktemp -d "${TMPDIR:-/tmp}/cutover-routing.XXXXXX")"; export GIT_OPTIONAL_LOCKS=0; mkdir "$OUT/none"; : > "$OUT/stamp"
ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
if [ -n "$V1" ]; then SIDE=(--v1="$V1" ${LIVE:+--live-v1}); else SIDE=(--v1-inventory="$MIG/v1-inventory"); fi
python3 -I "$PI" "${SIDE[@]}" --v2=. --lanes=I-ROUTES --pair-map="$MIG/pair-map.tsv" --ledger="$MIG/ledger.md" --out="$OUT/run" > "$OUT/candidates.tsv" 2> "$OUT/ledger.txt"; RX=$?; echo "pair-inventory exit $RX (I-ROUTES: the V1 paths each façade rule must cover; 1 = candidates, 2/3/4 = BLOCKED, the ledger's last line says why)"; grep -q '^  I-ROUTES .*blocked' "$OUT/ledger.txt" && echo "CR1 N/A (I-ROUTES blocked: the V1 paths a façade must cover are unread — fix the join first)"
V1ROOTS=("${V1:-$OUT/none}")
X=(-g '!**/{node_modules,vendor,dist,build,coverage,.git}/**' -g '!**/{test,tests,spec,__tests__,__mocks__,fixtures,e2e}/**' -g '!**/*.{spec,test,e2e-spec,test-data,fixture,d}.*' -g '!**/*.md')
# 0. The routing surface: façade, mesh, ingress and framework rewrite files; the shadow environments; V1 runtime manifests.
rg -l --pcre2 '^\s*location\s|kind:\s*(?:VirtualService|HTTPRoute|Ingress|IngressRoute)\b|request_mirror_policies|"ReverseProxy"|\basync\s+rewrites\s*\(|aws_lb_listener_rule|\bmirror\s+/' -g '*.{conf,yaml,yml,json,js,mjs,ts,tf,toml}' "${X[@]}" . > "$OUT/facade.txt"; ck CR0a $?
rg --files -g '*shadow*' -g '*mirror*' -g '*dark*' "${X[@]}" . > "$OUT/shadow.txt"; ck CR0b $?
rg -l --pcre2 'php\s+artisan|\bartisan\b|bin/rails|manage\.py|\bv1[-_]|\blegacy[-_]' -g '*.{yaml,yml,json,tf}' "${X[@]}" . > "$OUT/v1infra.txt"; ck CR0c $?
rg -l -i --pcre2 'cookie|csrf|xsrf' -g '*.{ts,js,mjs}' "${X[@]}" . > "$OUT/cookie.txt"; ck CR0d $?
rg --files -g '*flag*.{yaml,yml}' -g '**/flags/**/*.{yaml,yml}' "${X[@]}" . > "$OUT/flags.txt"; ck CR0e $?
wc -l "$OUT/facade.txt" "$OUT/shadow.txt" "$OUT/v1infra.txt" | sed '$d'
# 2. Session and CSRF on both halves: cookie name, domain, path, SameSite, serialisation; the CSRF cookie and header names.
rg -n -H --pcre2 "[\x27\"](?:cookie|domain|path|same_site|driver|serialization|encrypt)[\x27\"]\s*=>" -g '**/config/session.php' "${V1ROOTS[@]}"; ck CR2a $?
rg -n -H --pcre2 'xsrf(?:Cookie|Header)Name|X-XSRF-TOKEN|XSRF-TOKEN|VerifyCsrfToken|validateCsrfTokens\(|csrf_token\(\)' -g '*.{js,ts,php}' -g '!**/{vendor,node_modules,public,storage}/**' "${V1ROOTS[@]}"; ck CR2b $?
rg -n -H --pcre2 '^\s*(?:name\s*:\s*[\x27"][\w-]*(?:sess|sid|token|auth)[\w-]*[\x27"]|(?:domain|sameSite)\s*:\s*[\x27"][^\x27"]+[\x27"])|\b(?:csrf|xsrf)\w*\s*[:=]\s*\{|cookie\s*:\s*[\x27"][\w-]+[\x27"]\s*,\s*header\s*:|\bJWT_(?:SECRET|PUBLIC_KEY)\b|\bAPP_KEY\b' -g '*.{ts,js,mjs}' "${X[@]}" .; ck CR2c $?
cat > "$OUT/cr.py" <<'PY'
import glob, os, re, sys
out, mig = sys.argv[1], sys.argv[2]
rd = lambda p: open(p, errors='replace').read() if os.path.exists(p) else ''
lines = lambda f: [l.strip() for l in open(os.path.join(out, f)) if l.strip()] if os.path.exists(os.path.join(out, f)) else []
led = rd(os.path.join(mig, 'ledger.md'))
state = dict(re.findall(r'feature:\s*([\w-]+)\s*\n\s*state:\s*([\w-]+)', led))
flags = ' '.join(rd(p) for p in lines('flags.txt'))
owner = {f: v for f, v in re.findall(r'([\w-]+)\.writes?_owner:\s*\n\s*value:\s*(\w+)', flags)}
v1r = [l.split('\t')[1] for l in rd(os.path.join(out, 'run', 'v1', 'I-ROUTES.tsv')).splitlines() if l.startswith('I-ROUTES\t')]
print('ledger: ' + ', '.join('%s=%s%s' % (f, s, '(writes %s)' % owner[f] if f in owner else '') for f, s in sorted(state.items())))
side = lambda s: 'v2' if re.search(r'v2|next|new', s) else 'v1' if re.search(r'v1|legacy|old|portal', s) else '?'
quiet = []
for p in lines('facade.txt'):                                   # 1. nginx: every location, its match type and the side per method
    s = rd(p)
    if not re.search(r'^\s*location\s', s, re.M): continue
    if not re.search(r'^\s*proxy_pass\s', s, re.M) or not re.search(r'v1|legacy|old|portal|supabase', ' '.join(re.findall(r'(?:upstream|proxy_pass)\s+\S+', s)), re.I):
        print('CR1 N/A %s: serves an app (try_files / local routes, no V1 upstream) — not a strangler façade' % p); continue
    ups = {n: side(n + b) for n, b in re.findall(r'upstream\s+(\w+)\s*\{([^}]*)\}', s)}
    maps = {}
    for var, body in re.findall(r'map\s+\$request_method\s+\$(\w+)\s*\{([^}]*)\}', s):
        maps[var] = {k: ups.get(v, side(v)) for k, v in re.findall(r'(\w+)\s+(\w+);', body)}
    for i, l in enumerate(s.splitlines(), 1):
        m = re.match(r'\s*location\s+(=|\^~|~\*?)?\s*(/\S*)\s*\{(.*)', l)
        if not m: continue
        rest = m.group(3) + ' '.join(s.splitlines()[i:i + 4])
        t = re.search(r'proxy_pass\s+https?://\$?(\w+)', rest)
        tgt = t.group(1) if t else ''
        how = ', '.join('%s→%s' % kv for kv in sorted(maps[tgt].items())) if tgt in maps else (ups.get(tgt) or side(tgt) if tgt else 'local')
        seg = (re.findall(r'^/api/([\w-]+)', m.group(2)) or re.findall(r'^/([\w-]+)', m.group(2)) or [''])[0]
        st = state.get(seg, '-')
        deeper = sorted({k for k in v1r if re.match(r'\w+ %s/\S' % re.escape(m.group(2).rstrip('/')), k)}) if m.group(1) == '=' else []
        warn = []
        if deeper: warn.append('EXACT match: %d V1 sub-paths fall through to the next location (%s)' % (len(deeper), '; '.join(deeper[:3])))
        if st in ('V2-canary', 'V2-shadow', 'In-progress') and owner.get(seg) != 'v2' and how == 'v2': warn.append('every method → V2 while the ledger keeps writes on V1 (state %s, writes %s)' % (st, owner.get(seg, 'unset')))
        if st == 'V2-only' and 'v1' in how: warn.append('V2-only in the ledger, yet some methods → V1')
        if st == '-' and not warn: quiet.append('%s:%d' % (p, i)); continue
        print('CR1 %s:%d location %s%s → %s · ledger %s%s' % (p, i, (m.group(1) + ' ') if m.group(1) else '', m.group(2), how, st, ('  ' + ' | '.join(warn)) if warn else ''))
print('CR1 %d façade rules name no ledger feature (catch-alls, assets, health): %s' % (len(quiet), ', '.join(quiet[:6])))
for p in sorted(set(lines('facade.txt') + lines('shadow.txt'))):            # 3. mirrors: the method each mirrored match admits
    s = rd(p).splitlines()
    for i, l in enumerate(s, 1):
        if re.match(r'\s*mirror\s*:', l) or re.search(r'request_mirror_policies|^\s*mirror\s+/', l):
            blk = '\n'.join(s[max(0, i - 12):i])
            mt = blk.rfind('match')
            meth = re.findall(r'method:\s*\{\s*(?:exact|regex):\s*"?([\w|^$]+)', blk[mt:] if mt >= 0 else blk)
            ln = i - 12 + blk[:mt].count('\n') + 2 if mt >= 0 else i
            ok = meth and all(re.fullmatch(r'\^?\(?(?:GET|HEAD)(?:\|(?:GET|HEAD))*\)?\$?', x) for x in meth)
            print('CR3 %s:%d mirror admits %s%s' % (p, max(ln, 1), ','.join(meth) or 'EVERY method', '' if ok else '  ← writes are mirrored: the shadow must be side-effect-isolated (blocker when not)'))
EFF = r'MAIL|SMTP|SMS|PSP|PAY|STRIPE|WEBHOOK|QUEUE|KAFKA|BROKER|AMQP|SQS|SNS|S3|BUCKET|SFTP|PUSH|FCM|APNS|SLACK|PARTNER'
SAFE = r'sandbox|mailpit|mailhog|wiremock|stub|mock|fake|shadow|localhost|127\.0\.0\.1|\bfalse\b|disabled|\bnull\b|\bnone\b|\btest\b|sink|blackhole|devnull'
for p in lines('shadow.txt'):                                  # 3. the shadow's outbound effects: production targets?
    for i, l in enumerate(rd(p).splitlines(), 1):
        m = re.match(r'\s*-?\s*(?:name:\s*)?([A-Z0-9_]*(?:%s)[A-Z0-9_]*)\s*[=:]\s*(?:value:\s*)?"?([^"\n]*)' % EFF, l)
        if m and not re.search(SAFE, m.group(2), re.I): print('CR3 %s:%d %s=%s  ← an outbound effect the shadow reaches for real' % (p, i, m.group(1), m.group(2)))
v1s = '\n'.join(rd(p) for p in [os.path.join(sys.argv[3], 'config', 'session.php')]) if sys.argv[3] else ''
v2c = {p: rd(p) for p in lines('cookie.txt')}
def v1cfg(k):
    m = re.search(r"'%s'\s*=>\s*(?:env\(\s*'\w+'\s*,\s*)?'([^']*)'" % k, v1s); return m.group(1) if m else None
for k, v2k in (('cookie', 'name'), ('domain', 'domain'), ('path', 'path'), ('same_site', 'sameSite')):   # 2. the shared session cookie
    a = v1cfg(k)
    for p, s in v2c.items():
        for i, l in enumerate(s.splitlines(), 1):
            m = re.match(r"\s*%s\s*:\s*'([^']*)'" % v2k, l)
            if a and m and re.search(r'(?i)session', s) and m.group(1).lower() != a.lower(): print('CR2 %s:%d %s %r vs V1 %r (config/session.php)  ← differ on the shared cookie' % (p, i, v2k, m.group(1), a))
v1js = '\n'.join(rd(p) for p in glob.glob(os.path.join(sys.argv[3], 'resources', '**', '*.js'), recursive=True)) if sys.argv[3] else ''
xc = (re.findall(r"xsrfCookieName\s*=\s*'([^']+)'", v1js) or ['XSRF-TOKEN'])[0]; xh = (re.findall(r"xsrfHeaderName\s*=\s*'([^']+)'", v1js) or ['X-XSRF-TOKEN'])[0]
for p, s in v2c.items():                                       # 2. CSRF cookie and header V2 expects vs what V1 clients send
    for i, l in enumerate(s.splitlines(), 1):
        m = re.search(r"cookie\s*:\s*'([^']+)'\s*,\s*header\s*:\s*'([^']+)'", l)
        if m and sys.argv[3] and (m.group(1) != xc or m.group(2).lower() != xh.lower()): print('CR2 %s:%d CSRF %s / %s vs V1 clients %s / %s  ← differ' % (p, i, m.group(1), m.group(2), xc, xh))
if not sys.argv[3]: print('CR2 V1 side blocked (no V1 tree): the session and CSRF rows are Unconfirmed-solo')
cold = [f for f, s in state.items() if s not in ('V2-only', 'deprecated', 'V1-deleted')]
for p in lines('v1infra.txt'):                                 # 4. V1 runtime scaled to 0 / suspended while V1 still owns features
    for i, l in enumerate(rd(p).splitlines(), 1):
        if re.match(r'\s*(?:replicas:\s*0\b|suspend:\s*true\b|min_?[Ss]ize\s*[:=]\s*0\b|desired_?[Cc]ount\s*[:=]\s*0\b)', l):
            print('CR4 %s:%d %s  ← V1 cold while V1 still owns: %s' % (p, i, l.strip(), ', '.join(sorted(cold)) or 'nothing'))
for f, a in re.findall(r'([\w-]+\.(?:read_from|writes?_owner)):[^\n]*\n(?:[^\n]*\n){0,2}?\s*allowed:\s*\[([^\]]*)\]', flags):
    if 'v1' not in a: print('CR4 flag %s allows [%s]: no one-step way back to V1' % (f, a))
PY
python3 -I "$OUT/cr.py" "$OUT" "$MIG" "$V1"
for R in "$V1" .; do [ -n "$R" ] && find "$R" -newer "$OUT/stamp" -type f -not -path '*/node_modules/*' | head -3; done; echo "write check done (empty = nothing written)"
```

`CR1`–`CR4` lines are the joins against the ledger and flags; plain lines are the raw session and CSRF settings to read side by side.

## Measured

Measured 2026-10-18 on this repo's fixtures, and 2026-10-19 on one real Supabase → Nest port (read-only).

- **A real Supabase → Nest port** (2026-10-19). Before: the V2 SPA's `nginx.conf` (`try_files … /index.html`, no proxy to a V1) was read as the façade and its 4 locations printed as rules naming no ledger feature. After: `CR1 N/A …: serves an app … not a strangler façade`; a file is a façade only with a `proxy_pass` and a V1 / legacy upstream, and an I-ROUTES lane that is blocked prints `CR1 N/A (I-ROUTES blocked …)`. `port-pair` unchanged.

- **`port-pair`, paired** (V1 read in place with `LIVE=1`, run both in a scratch copy and in place: same output, write check 0). The engine read 44 V1 routes. Façade files: 3; shadow and mirror files: 3; V1 runtime manifests: 7. Joins:
  - CR1: 3 ledger-feature rules, 2 with a warning, plus 4 rules naming no ledger feature;
  - CR2: 2 differences;
  - CR3: 2 mirrors (1 admits every method) and 1 production effect in the shadow environment;
  - CR4: 2 cold V1 workloads.

  All 8 CR seeds sit on a `CR*` line. The decoys stay quiet: the GET-only tickets mirror prints with no arrow, and the façade `auth_request` rule is in the no-feature list.
- **`port-pair`, solo** (V2 + `ai/` only). CR1, CR3 and CR4 are identical: the sub-path count comes from the recorded I-ROUTES. CR2 prints `V1 side blocked (no V1 tree)`.
- **Noise fixes.**
  - CR2c first matched every `name:` property (metric names, queue names, cart stores): 14 lines on `obs-defects`. Restricted to session-like names (`sess`, `sid`, `token`, `auth`) plus `domain` and `sameSite`, it prints 1 line on `vuln-fullstack` (`sameSite: 'none'`), 1 on `node-api` (`JWT_SECRET`) and 0 elsewhere.
  - CR1 printed every `location` of an unrelated nginx file (12 on `infra-ops`); rules that name no ledger feature now print as one summary line.
  - The cookie lookup first used a recursive glob that stalled on a large tree; it now reads the `rg --files` list.
- **V2-only fixtures:** 0 `CR*` warnings on all 21. `ci-defects`, `infra-ops` and `vuln-fullstack` print their nginx rules only in the summary line.

## The 3,000-row path

A large mesh is almost always one default rule and a few exceptions.

1. **Order the rules as the proxy does.** nginx: an exact `=` match wins; otherwise the longest prefix is remembered, and used at once if it is `^~`; otherwise the first regex in file order; otherwise that longest prefix. Istio: `http[]` top to bottom. The first rule that matches decides; print each ledger feature's winning rule per method.
2. **Group by ledger state.** Every `V2-only` feature must route all methods and all V1 sub-paths to V2. Every feature whose writes V1 owns must route non-GET methods to V1. One rule per state is usually the finding, with N routes.
3. **Read in this order:** mirrors on write routes (§3, blockers), write methods sent to the wrong half (§1), cold V1 workloads (§4), sessions (§2).
4. **Close a group with one checked reason** (`18 static asset rules: no ledger feature, V1 only`). A write route or a mirror is never bulk-closed.

## Scans for

| § | Class | Join / grep | Finding when | Default severity | Solo | Oracle |
|---|---|---|---|---|---|---|
| 1 | CO-1 façade routing gap | CR1 (+ I-ROUTES) | a method or V1 sub-path of a ledger feature lands on the half that does not own it | high; blocker when writes land on a half whose data is stale or not yet authoritative | Finding (V2 config + recorded routes) | V383 |
| 2 | CO-2 session / auth not shared | CR2, CR2a–c | a route both halves serve in the window gets a cookie, CSRF pair, serialisation or token the other half rejects | high | Unconfirmed-solo (V1 config unread) | V384 |
| 3 | CO-3 shadow not isolated | CR3 | a mirror, replay or `try` block sends writes to a candidate whose effects reach real downstreams | **blocker** | Finding | V371 (shadow) |
| 4 | CO-5 not reversible / V1 cold | CR4 | V1 workers, crons or capacity are gone while the ledger still gives V1 work, or a flag cannot go back to V1 in one step | high | Finding | V382 |

### 1. Façade routing gap (CO-1)

```
BAD:   location = /api/tickets { proxy_pass http://v2_api; }        (V2-only: /api/tickets/41, /reopen, /next fall to location /api/ → V1)
       location /api/invoices { proxy_pass http://v2_api; }          (reads-only canary: POST …/issue now runs on V2)
GOOD:  location /api/tickets { … }      ·   proxy_pass http://$invoices_upstream;   (map: GET/HEAD → V2, the rest → V1)
```
**Read the code.** For each ledger feature, which rule wins per method (exact beats prefix in nginx; the first `match` wins in Istio)? List the V1 sub-paths of the feature (CR1 counts them from I-ROUTES) and check that each one lands where the ledger says. Who owns writes (the `writes_owner` flag, the ledger notes, the plan)? A method map defined and not used is the usual shape. Does V2 even serve the method the rule sends it (SP §1)? **Finding when** a request lands on the half that does not own it now. **Proof:** V383, every ledger route per method through the façade, asserting the side (a response header or the access log).

### 2. Session or auth not shared (CO-2)

```
BAD:   V1 'domain' => '.norrow.example'           V2 domain: 'app.norrow.example'          (signed out on the portal host)
       V1 clients send XSRF-TOKEN / X-XSRF-TOKEN   V2 checks csrf_token / x-csrf-token      (every cookie write → 419)
GOOD:  domain: '.norrow.example'   ·   CSRF = { cookie: 'XSRF-TOKEN', header: 'x-xsrf-token' }
```
**Read the code.** Which routes do both halves serve during the window: the same host, the portal shell plus V2 API calls (precedent 19)? Compare the cookie name, domain, path and SameSite, and the session store and its encoding: PHP `serialize` vs JSON, a cookie encrypted or signed with an app key (Laravel `APP_KEY`, Rails `secret_key_base`, Django `SECRET_KEY`) that the other half cannot open. Compare the token keys and claims, and the CSRF cookie and header names that V1's clients actually send (the JS client, not only the framework default). A difference on a host only one half serves is Hardening. **Finding when** identity or CSRF established on one half fails on the other on a shared route. **Proof:** V384, a session from each half used on the other, a CSRF-protected write and a logout.

### 3. Shadow path not side-effect-isolated (CO-3)

```
BAD:   - match: [{ uri: { prefix: /api/orders } }]   mirror: { host: v2-api-shadow }      (POST/PATCH mirrored at 10%)
       MAIL_TRANSPORT=smtp://smtp.norrow.internal:587   in the shadow env                  (a customer gets a second e-mail)
GOOD:  method: { exact: GET } on the mirrored match   ·   MAIL_TRANSPORT=smtp://mailpit.shadow.svc:1025
```
**Read the code.** Which methods does each mirror admit: an Istio match with no `method`, an nginx `mirror` in a location that takes writes, a GoReplay `--output-http` with no method filter, or a Scientist `try` that writes? Mirrored responses are discarded, but mirrored writes are real (research notes A1). For every outbound effect variable in the shadow's environment (mail, SMS, payments, webhooks, queues, buckets, partner calls), is it a sink, a stub, a sandbox or disabled? A shadow database of its own is isolation for data, not for effects. **Finding when** a mirrored or replayed request can reach a real downstream. Severity is a blocker at any percentage (precedent 17). **Proof:** V371 with the mirror on: the candidate's external effects = 0 (Mailpit and WireMock journals).

### 4. Flag not reversible in one step; V1 cold (CO-5)

```
BAD:   v1-queue-worker  replicas: 0      while V1 still issues invoices and adjusts wallets
       v1-schedule-run  suspend: true    while two of its five jobs exist nowhere in V2
GOOD:  V1 workers and scheduler kept at capacity until every job they run has a V2 owner and the soak has ended
```
**Read the code.** Which jobs, queues and crons do the V1 workloads run (the command, `routes/console.php`, the queue names)? Which ledger features still give V1 that work (`CR4` lists the states that are not V2-only)? Can each traffic flag go back to `v1` with one change: an `allowed` list that includes `v1`, a flag rather than a deploy, and no V1 schema already dropped? **Finding when** a rollback would land on a V1 that cannot serve, or V1 work stops before V2 owns it. **Proof:** V382, flip back after N V2 writes and watch V1 serve them and drain its queue.

## Output

```
cutover-routing-scan — paired · façade nginx (deploy/nginx/front-proxy.conf) · mesh istio · ledger 10 features (1 V2-only, 2 V2-canary, 2 V2-shadow)

Findings: 8 · Unconfirmed: 0

1. v2/deploy/istio/api-mirror.yaml:9                                [report-with-fix]  blocker
   §3 the orders mirror matches a URI prefix with no method: 10% of POST/PATCH replayed on v2-api-shadow, whose env
   mails through the production relay (deploy/shadow/shadow-api.env:4). V1 mails on create (OrderMailObserver.php:13).
   Proof: V371 shadow on, candidate effects 1 ≠ 0. Fix: method: { exact: GET }.
2. v2/deploy/nginx/front-proxy.conf:41                              [report-with-fix]  high
   §1 tickets are V2-only (ledger F003) but `location = /api/tickets` matches the bare path only: 4 V1 sub-paths
   (GET /api/tickets/{}, PATCH, /reopen, /next) fall through to location /api/ → V1. Proof: V383. Fix: prefix location.

Verification: 11 candidates → 8 findings · 0 unconfirmed · 1 hardening · 0 pre-existing · 2 refuted

Class coverage:
  §1  façade routing         checked (3 ledger rules → 2; 4 rules name no feature)
  §2  session / CSRF         checked (2 differences → 2; shared routes: portal shell + ticket writes)
  §3  shadow isolation       checked (2 mirrors, 1 env → 2)
  §4  V1 warm / reversible   checked (2 cold workloads → 2; 5 flags all allow v1)
```

`[report-with-fix]`: the config line, the ledger fact and the V1 fact cited, and a local fix. `[report-flagged]`: one link unproven (the shared route, the deployed file), with the probe. Every run prints **all four** §s, each as `checked (k candidates → m)`, `N/A (<reason>)` (no façade: a big-bang cutover; no shadow), `blocked (<grep or lane>: <reason>)`, `→ <owner> (k)`, or `Unconfirmed-solo (k)`.

## Precedents

The verifier reads [`precedents/migration.md`](../../../../snippets/precedents/migration.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4:
- § 17: a shadow on a write route with no isolation is a blocker;
- § 18: the point of no return;
- § 19: a session difference matters only on routes both halves serve;
- § 21: solo mode;
- § 28: a counterpart outside the app is a counterpart once read.

The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Migration: V371, V382, V383 and V384.

## When to run

- On every whole-repo `/compare-v1`, printing all four §s.
- Before a façade, mesh or ingress change that moves a route, before mirror traffic is turned on or raised, and before any V1 workload is scaled down.
- When a ledger row changes state (`V2-shadow` → `V2-canary` → `V2-only`).

## Halt conditions

- Do not report a high or blocker row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/compare-v1` that is `@parity-auditor` in refute mode, plus `@verifier` on every BLOCKER and HIGH. Run standalone, apply the protocol as a separate second pass and tag those rows `self-verified`. Never drop them.
- **Solo mode never prints GO.** §1, §3 and §4 read V2-side config and the recorded routes and run in full. §2 needs V1's session and CSRF config: without the V1 tree it is `Unconfirmed-solo`, and the settling probe is "re-run with `--v1=<path>`" (precedent § 21).
- A ledger with no feature states makes §1 and §4 `blocked (no ledger)`, never `checked`. A façade that lives in another repository is `blocked (façade not in the roots: pass V2=<infra repo>)`.
- Halt on any finding without the config line, the ledger state or flag, and the V-number.
- **Never write into either tree and never send traffic.** Probes run against staging and are requested in the output.

## Related

- `paired-inventory` (this pack): the V1 route list. `data-cutover-orchestrate` covers data flips and reverse paths; `parity-proof-scan` §5 covers the comparator behind a shadow.
- `/compare-v1` runs this skill; `@parity-auditor` judges; `/find-and-fix --from-audit` closes each row from its V-number. A façade or mirror change gets the STOP-and-ask of a cutover flag.
- Security, when installed, for cookie flags as a security property. Backend `http-contract-scan`, when installed, for single-codebase router traps.
