---
name: surface-parity-scan
description: "V1→V2 surface parity: routes, guards, tenant scope, enums, rules, errors, defaults — read-only."
kind: skill
pack: migration
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: surface-parity-scan

## Premise

A port keeps V1's **surface** when every live V1 route still answers on V2, with the same guard decision, the same tenant scope, the same value vocabulary, the same input rules, the same error status and code, and the same defaults for what the client leaves out. None of these show in V2 alone. A Nest controller with no `@Permissions` looks finished; it is a widening only because V1 had `permission:wallets.adjust` on that route. A `z.string().max(64)` looks reasonable; it is drift only because V1 said `max:30` and the column is `varchar(30)`.

This skill owns the **V1≠V2 delta** on the request surface, classes MG-RT-1/2, MG-AZ-1/2/3, MG-VO-1, MG-VA-1, MG-ER-1 and MG-SD-1 (SP §1–§9). "Is it RFC-correct" stays with backend; "is it what V1 did" is answered here.

**Every finding cites the V1 line and the V2 line (or "no counterpart" after the written search), the lane row that raised it, and the oracle that proves it.** A lane row is a candidate, never a finding. "Surface parity holds" is never printed without the class-coverage block (§ Output).

## The rule

A candidate becomes a finding only when all four hold:

1. **The pair is real.** The row comes from a calibrated lane with the keys joined (no prefix-sanity halt), and V1 was read at the pin (paired) or from a fresh record (solo) — `paired-inventory` § The rule.
2. **V1 does it on a live path.** The V1 route, guard, rule or default is reached on halt 11's six axes (app source, tests, cron, route, infra, telemetry). Dead V1 is not a drop ([precedents § 2](../../../../snippets/precedents/migration.md)).
3. **V2 does not, anywhere that runs on that route.** The counterpart search is written out: global guards, pipes and filters, base classes, the ORM filter, the gateway or façade, the SPA router, `pair-map.tsv` with a reason (precedents § 1, § 26, § 28).
4. **No record makes it intentional.** No ADR plus `changes_baseline` for the difference (precedents § 3).

## Boundaries

- **MG-AZ-1 widening and MG-AZ-3 tenant scope** → the security pack, when installed: `@api-security-reviewer` grades AZ-1 and `@tenant-isolation-reviewer` grades AZ-3, both in refute mode, and the row is listed here as `→ security (k)` with the paired evidence handed over. Without the security pack, the row is reported here, tagged `security-class (owner pack security not installed)`, and never graded as security would grade it.
- Single-codebase HTTP correctness → backend `http-contract-scan` (§7 pagination, §11 router traps), `validation-boundary-scan` (§4 coercion, §6 unknown keys) and `edge-error-scan` (envelope), when the backend pack is installed; without it the V2-only defect is out of scope here and the coverage block says so.
- Effects behind a route (mail, audit, jobs) → `side-effect-parity-scan`. Rounding, strings, order and time on the path → `semantics-parity-scan`. Soft-delete on reads (I-SCOPE `soft_delete`) → `data-cutover-orchestrate` §7.
- UI pages and nav leaves a `web.php` route served in V1 (MG-UI-1/2) → `@parity-auditor` Section 0; SP §1 refutes those routes when the SPA router has the path.

## Lanes

The rows come from `paired-inventory` (I-ROUTES, I-AUTHZ, I-RULES, I-ENUM, I-ERR, I-SCOPE, I-CONF); the one-sided greps add what the lanes cannot see. Read the framework **and its version** from both lockfiles before using a default below.

| Stack | Routes, shapes (§1–§2) | Guards, scope (§3–§5) | Enums, rules, errors (§6–§8) | Defaults (§9) | Tag |
|---|---|---|---|---|---|
| **Laravel (V1)** | `routes/*.php` chains, `apiResource`, `fallback`; paginator is 1-based; `(array) $request->input()` reads `a[]=` | route / group middleware, `can:<ability>,<model>` policies (owner checks inside), spatie `role:` / `permission:`, `#[ScopedBy]`, `addGlobalScope` | backed enums, FormRequest `rules()`, global `TrimStrings` + `ConvertEmptyStringsToNull` (on by default from 11 unless removed), 422 with every field, `withExceptions` renderers | `$attributes`, `$request->input('x', d)`, `paginate()` 15 | [V] port-pair |
| **NestJS (V2)** | `dto-types.py --routes` (prefix + `exclude`, versioning); Fastify or Express adapter options | `APP_GUARD` + `@Public()`, class + method decorators; a metadata guard that returns `true` with no metadata is default-allow; MikroORM `@Filter` (never applied to raw SQL) | TS enums (implicit = 0-based), zod / class-validator chains, `ValidationPipe` 400 `message[]`, `HttpException` subclasses | entity initialisers, zod `.default()` | [V] port-pair |
| **Express 5 / Fastify** | Express 5's default query parser is `"simple"`: `a[b]=c` is no longer an object (research B, Express 5 guide, 2026-10-09). Fastify 5.12 docs (fetched 2026-10-18): the default `querystringParser` is a fork of Node's `querystring`, and `routerOptions.ignoreTrailingSlash` defaults to `false`; how it reads `a[]=` is not documented [K?] | per-router middleware only | hand-written validators | handler literals | [K?] |
| **Rails** | `config/routes.rb`, `resources`; `ids[]=` arrays | `before_action`, Pundit, `default_scope` | integer-mapped `enum` (stored ints) | column defaults, `per_page` | [K?] partial lane |
| **Django / DRF** | `urls.py`, `APPEND_SLASH` | `permission_classes`, manager filters | `TextChoices`, serializers | `PAGE_SIZE` | [K?] partial lane |
| **Spring** | `@RequestMapping` | `@PreAuthorize`, Hibernate filters | `@Enumerated(ORDINAL)` stores positions | `@PageableDefault` | [K?] partial lane |
| **FastAPI / Go** | `APIRouter`, `redirect_slashes`; gin / chi / echo routes | dependencies; middleware | Pydantic v2 (`Optional` without default is required) | model defaults | [K?] partial lane |

A stack the engine tags `partial` prints `checked · partial` in the coverage block, never plain `checked`.

## Tool lane and ledger

Static only, offline. The opt-in cross-checks (`php artisan route:list --json -vv --except-vendor`, spatie `permission:show` against a restored copy) run on the engine's snapshot, never on the audited trees (`paired-inventory` § Tool lane). The engine ledger on stderr comes first: a `blocked` lane, a prefix-sanity halt or a write-check hit is settled before any row is read. Rows a `pair-map` row closes (a rename, a V2-only acknowledgement, an ADR-backed attribute acceptance) are listed there under `pair-map:`; each counts as checked with that reason, and its file is still read when the reason is `moved-to-…` (precedents § 28). Candidate rows are `CANDIDATE · lane · diff · key · attr · v1 · v2 · v1_at · v2_at · tags · excerpt`.

## Pre-flight

Run as one script (bash 3.2-safe; shell state does not survive between tool calls). `V2` is the V2 root; `V1` is empty in solo mode; `MIG` holds `pair-map.tsv`, `ledger.md` and `v1-inventory/`. `LIVE=1` reads an uncommitted V1 in place (verdict ceiling GO-UNVERIFIED). The script greps from **inside** V2, because rg globs also match the root path you pass (a root under `…/fixtures/` or `…/tests/` reads 0 files); a V1 path that holds such a segment prints `BLOCKED`. Every grep ends in `ck`: exit 2 is a blocked class, never zero hits. Each V1 grep runs through `v1g` by the V1 stack the script detects: Laravel PHP, Supabase SQL and edge functions (`supabase/`, migrations included, every superseded definition too — read the live one on the lane row), else (a Rails, Django or Spring V1) `N/A (V1 stack <x>)` — never 0 files silently. `pair-inventory exit 1` is candidates, not a failure; `2`/`3`/`4` is BLOCKED, and the ledger's last line prints why.

```bash
PI="${PI:-.claude/skills/paired-inventory/scripts/pair-inventory.py}"; V2="${V2:-.}"; V1="${V1:-}"; MIG="${MIG:-$V2/ai/migration}"
abs() { (cd "$(dirname "$1")" 2>/dev/null && printf '%s/%s\n' "$(pwd)" "$(basename "$1")") || printf '%s\n' "$1"; }
PI=$(abs "$PI"); MIG=$(abs "$MIG"); [ -n "$V1" ] && V1=$(abs "$V1"); cd "$V2" || exit 2   # grep from inside V2: rg globs also match the root path given
OUT="$(mktemp -d "${TMPDIR:-/tmp}/surface-parity.XXXXXX")"; export GIT_OPTIONAL_LOCKS=0; mkdir "$OUT/no-v1"; : > "$OUT/stamp"
ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
if [ -n "$V1" ]; then SIDE=(--v1="$V1" ${LIVE:+--live-v1}); else SIDE=(--v1-inventory="$MIG/v1-inventory"); echo "solo: V1 greps search an empty dir (blocked, no V1 tree)"; fi
python3 -I "$PI" "${SIDE[@]}" --v2=. --lanes=I-ROUTES,I-AUTHZ,I-RULES,I-ENUM,I-ERR,I-SCOPE,I-CONF --pair-map="$MIG/pair-map.tsv" --ledger="$MIG/ledger.md" --out="$OUT/run" > "$OUT/candidates.tsv" 2> "$OUT/ledger.txt"; echo "pair-inventory exit $? — 0 ran clean · 1 candidates (not a failure) · 2/3/4 BLOCKED: read $OUT/ledger.txt (its last line prints the reason) before any row"
S1=$(ls -d "$OUT"/run/run.*/v1 2>/dev/null | head -1); V1ROOTS=("${S1:-${V1:-$OUT/no-v1}}"); V2ROOTS=(.)
case "/${V1ROOTS[0]}/" in */fixtures/*|*/test/*|*/tests/*|*/spec/*|*/e2e/*|*/docs/*|*/lang/*|*/vendor/*) echo "BLOCKED: the V1 root path holds an excluded segment, so every V1 grep reads 0 files — copy V1 out or use the snapshot";; esac
X=(-g '!**/{node_modules,vendor,dist,build,coverage,storage,bootstrap/cache}/**' -g '!**/{test,tests,spec,__tests__,__mocks__,fixtures,e2e}/**'
   -g '!**/*.{spec,test,e2e-spec,test-data,fixture,fixtures,d}.*' -g '!**/{lang,locales,i18n,docs}/**' -g '!**/database/{seeders,factories}/**' -g '!**/*.{md,lock,map,snap}')
V1STACK=none; [ -f "${V1ROOTS[0]}/composer.json" ] && V1STACK=laravel; [ -d "${V1ROOTS[0]}/supabase/migrations" ] && V1STACK=supabase; echo "V1 stack: $V1STACK (V1 greps read its files: PHP for laravel, SQL + edge functions for supabase, else N/A — never 0 files silently)"
v1g() { local id="$1" php="$2" sb="$3"; shift 3; case "$V1STACK" in laravel) rg -n --pcre2 "$@" "$php" -g '*.php' "${X[@]}" "${V1ROOTS[@]}"; ck "$id" $?;; supabase) if [ "$sb" = - ]; then echo "$id N/A (V1 stack supabase: no grep for this shape; the lane rows carry it)"; else rg -n -i --pcre2 "$sb" -g '*.{sql,ts,toml}' -g '!**/{node_modules,tests,__tests__}/**' -g '!**/*.{test,spec}.ts' "${V1ROOTS[0]}/supabase"; ck "$id" $?; fi;; *) echo "$id N/A (V1 stack $V1STACK: this grep reads Laravel PHP or Supabase SQL; a Rails, Django or Spring V1 prints N/A)";; esac; }
cut -f2,3,4 "$OUT/candidates.tsv" | sort | uniq -c | sort -rn | head -12   # lane · diff · key
# 0. Wiring that moves verdicts: V2 global prefix, guards, pipes, filters, adapter; V1 global middleware and exception renderers.
rg -n --pcre2 'setGlobalPrefix\(|useGlobal(?:Guards|Pipes|Filters|Interceptors)\(|\bAPP_(?:GUARD|PIPE|FILTER)\b|@Public\(\)|new (?:Fastify|Express)Adapter\(|querystringParser|ignoreTrailingSlash|["\x27]query parser["\x27]' -g '*.{ts,js}' "${X[@]}" "${V2ROOTS[@]}"; ck SP0a $?
v1g SP0b 'withMiddleware|trimStrings|TrimStrings|ConvertEmptyStringsToNull|->remove\(|->(?:render|renderable)\(\s*function|shouldRenderJsonWhen|protected \$middleware(?:Groups|Aliases)?\b' 'verify_jwt\s*=\s*false|export\s+(?:async\s+)?function\s+(?:with|require|enforce|ensure|verify)\w*\s*\(|\balter\s+default\s+privileges\b'
# 1. Counterpart search for each V1-ONLY route: its last static segment anywhere in V2 code, the SPA router and deploy/.
awk -F'\t' '$3=="V1-ONLY" && $4 ~ /^[A-Z]+ \//{print $4}' "$OUT/candidates.tsv" | sort -u | while read -r M P; do W=$(printf '%s' "$P" | tr '/' '\n' | grep -v '^{' | tail -1); [ -n "$W" ] || W=root; printf '%-44s %s\n' "$M $P" "$(rg -c -F -w -- "$W" -g '!**/node_modules/**' "${V2ROOTS[@]}" 2>/dev/null | head -4 | tr '\n' ' ')"; done
# 2. Path / query shape: page→offset with no `- 1`; bracket arrays V1 parsed; the paginator V1 used.
rg -n --pcre2 '(?<!-\s1\)\s\*\s)\bpage\w*\s*\*\s*(?:this\.|query\.|dto\.)?\w*(?:per_?[Pp]age|[Ll]imit|[Ss]ize|[Tt]ake)\b|\bskip\s*:\s*\w*\.?page\s*\*' -g '*.{ts,js,py,go,java,kt,rb}' "${X[@]}" "${V2ROOTS[@]}"; ck SP2a $?
v1g SP2b '\(array\)\s*\$request->(?:input|query|get)\(|\$request->(?:input|query)\(\s*\x27[^\x27]+\x27\s*,\s*\[\s*\]|->(?:paginate|simplePaginate)\(' '\.range\(\s*\w+|\.limit\(\s*\w+|\bmax_rows\s*=|\boffset\s+\(?\s*\w+\s*-\s*1\)?\s*\*|\blimit\s+\w+\s+offset\b'
# 3/4. Authz: guards that pass a handler with no metadata (default-allow); V1 policies whose ability carries an owner/tenant check.
rg -n -U --pcre2 'if\s*\(\s*!\s*\w*(?:required|[Pp]ermissions?|[Rr]oles?|meta\w*)\w*(?:\?\.length)?\s*\)\s*\{?\s*return\s+true' -g '*.{ts,js}' "${X[@]}" "${V2ROOTS[@]}"; ck SP3a $?
v1g SP3b 'function\s+\w+\(\s*User\s+\$\w+\s*,\s*\w+\s+\$\w+|\$\w+->(?:account_id|tenant_id|team_id|user_id|owner_id)\s*===' '\bauth\.uid\(\)\s*=\s*\w+|\b\w*(?:owner|user|workspace|tenant|account)_id\s*=\s*auth\.uid\(\)|\bhas_\w*permission\s*\(' -g '**/Policies/**'
# 5. Tenant scope: raw SQL on a table V1 scoped (I-SCOPE tenant=yes) with no tenant column — an ORM filter never sees raw SQL.
TT=$(awk -F'\t' '$1=="I-SCOPE" && $3 ~ /tenant=yes/ {sub(/^table:/, "", $2); printf "%s%s", (n++ ? "|" : ""), $2}' "$OUT"/run/v1/I-SCOPE.tsv 2>/dev/null); echo "V1 tenant-scoped tables: ${TT:-none (SP5 grep N/A)}"
rg -n -U --pcre2 '\.(?:execute|raw|query|\$queryRaw(?:Unsafe)?|\$executeRaw(?:Unsafe)?)\s*(?:<[^>\n]*>)?\(\s*[\x27"`](?![^\x27"`]*\b(?:account|tenant|org(?:anization)?|team|company|workspace)_?id\b)[^\x27"`]*\b(?:from|join|update|into)\s+"?(?:'"${TT:-__none__}"')(?:e?s)?\b' -g '*.{ts,js}' "${X[@]}" "${V2ROOTS[@]}"; ck SP5 $?
# 6. Vocabulary: numeric enums with implicit values (0-based); V1 backed enums.
rg -n --pcre2 '\benum\s+\w+\s*\{\s*[A-Z]\w*\s*(?:,\s*[A-Z]\w*\s*)*,?\s*\}' -g '*.{ts,js}' "${X[@]}" "${V2ROOTS[@]}"; ck SP6a $?
v1g SP6b '^\s*enum\s+\w+\s*:\s*(?:int|string)\b' '\bcreate\s+type\s+[\w."]+\s+as\s+enum\b|\balter\s+type\s+[\w."]+\s+(?:add|rename)\s+value\b|\bcheck\s*\(\s*\(?\s*\w+\s*\)?(?:::\w+)?\s*(?:in\s*\(|=\s*any\s*\()'
# 7. Rules: where V2 registers (or only defines) global input normalisation, and per-controller opt-ins.
rg -n --pcre2 'useGlobalPipes\(|\bAPP_PIPE\b|@UsePipes\(|\b(?:whitelist|forbidNonWhitelisted|transform)\s*:|function\s+\w*(?:[Nn]ormali[sz]|[Tt]rim)\w*\s*\(' -g '*.{ts,js}' "${X[@]}" "${V2ROOTS[@]}"; ck SP7 $?
# 8. Errors: statuses V2 throws by number, first-error-only validation; V1 renderers, abort codes, error codes.
rg -n --pcre2 'new\s+\w*(?:Error|Exception)\(\s*[45]\d\d\b|\bissues\.slice\(\s*0\s*,\s*1\s*\)|\.(?:issues|errors)\[0\]|\bstopAtFirstError\b|\bexceptionFactory\b|\berrorHttpStatusCode\b' -g '*.{ts,js}' "${X[@]}" "${V2ROOTS[@]}"; ck SP8a $?
v1g SP8b '\babort\(\s*[45]\d\d\b|[\x27"]code[\x27"]\s*=>|\bstopOnFirstFailure\b|\bbail\b|response\(\)->json\([^\n]*,\s*[45]\d\d\)' '\braise\s+exception\s+\x27[A-Za-z][\w.]*\x27|\berrcode\s*=\s*\x27|\bstatus\s*:\s*[45]\d\d\b'
# 9. Silent defaults: V1 model $attributes and request-input defaults; V2 entity initialisers and zod / DTO defaults.
v1g SP9a 'protected\s+\$attributes\s*=\s*\[[^\]]*\]|\$request->(?:input|query|integer|string)\(\s*\x27\w+\x27\s*,\s*[^)\s]+\)|->default\([^)\n]+\)' '\balter\s+column\s+\w+\s+set\s+default\b|\b\w+\s*\?\?\s*(?:\x27[^\x27]*\x27|-?\d+|true|false)\b' -U -g '!**/database/migrations/**'
rg -n --pcre2 '^\s*\w+[!?]?\s*:\s*[\w.<>| ]+=\s*(?:[\x27"][^\x27"]*[\x27"]|-?\d+(?:\.\d+)?|true|false)\s*;|\.default\(\s*[^)\n]+\)|\bdefault\s*:\s*(?:[\x27"][^\x27"]*[\x27"]|-?\d+)' -g '*.{ts,js}' "${X[@]}" "${V2ROOTS[@]}"; ck SP9b $?
for R in "$V1" .; do [ -n "$R" ] && find "$R" -newer "$OUT/stamp" -type f -not -path '*/node_modules/*' | head -3; done; echo "write check done (empty = nothing written)"
```

`pair-inventory exit 4` means a requested lane is blocked: its §s print `blocked (<lane>: <reason>)`. In solo mode the V1 greps read an empty directory on purpose; the recorded row (`v1_at`) is the only V1 evidence.

## Measured

Measured 2026-10-18 on this repo's fixtures, and 2026-10-19 on one real Supabase → Nest port (read-only).

- **A real Supabase → Nest port** (2026-10-19, V1 read in place, V2 read-only, an audit's 466-row route map). Before: every V1 grep read `*.php` and printed nothing (793 lines, all V2-side); I-ROUTES/AUTHZ/RULES halted. After: `V1 stack: supabase`, SP0b 117 · SP2b 310 · SP3b 1,308 (policy predicates) · SP6b 157 · SP8b 969 (RAISE sites) · SP9a 172 (after narrowing from 2,710 to `alter column … set default` and edge `??` defaults); the route lanes route-join the 466 mapped routes. On `port-pair` every line is unchanged (`V1 stack: laravel`).

- **`port-pair`, paired** (`--live-v1`: V1 is uncommitted there; `change/` overlaid as the port PR). Engine (the build whose candidate rows carry a `lane` column): 0 rg exit-2, 0 unparsed, write check 0, built-in calibration 0 rows. Candidates: I-ROUTES 44 / 34 rows → 9 V1-ONLY, 1 V2-ONLY; I-AUTHZ 9 / 1 / 9 CHANGED; I-RULES 2 / 0 / 12; I-ENUM 6 CHANGED; I-ERR 1 V1-ONLY; I-SCOPE 3 CHANGED; I-CONF 2 CHANGED. Grep lines: SP0a 12 · SP0b 14 · SP2a 1 · SP2b 7 · SP3a 4 · SP3b 8 · SP5 1 · SP6a 1 · SP6b 4 · SP7 4 · SP8a 2 · SP8b 2 · SP9a 14 · SP9b 22. All 18 SP seeds sit on a lane row or a grep line (table in § Output); the restored twins (wallet credit-limit, the invoice account filter, the low-stock raw query, the invoice status set, the update-body `po_number` rule) print no row.
- **`port-pair`, solo** (V2 + a V1 inventory re-recorded at the pin, then faulted: `I-ENUM` with a foreign `sha`, `I-SCHED` with an old extractor hash). The same rows, every one tagged `solo`; the three enum rows carry `stale-v1-inventory`; the engine exits 4 for the blocked lane. The fixture's own `v1-inventory/` still carries a placeholder extractor hash, so every lane read from it is `blocked (extractor changed since record)` until it is re-recorded.
- **Noise fixes.** SP5 first matched any raw SQL with no tenant column: 39 lines on `backend-defects`, 34 on `slow-marketplace`, 5 on `port-pair`. Restricted to tables V1 scoped (I-SCOPE `tenant=yes`), it prints 0, 0 and 1 (the seeded `findBySku`), and the low-stock decoy stays out. Every grep first returned 0 lines on every other fixture because the root path itself held `fixtures/` and rg matched the exclusion against it; the pre-flight now greps from inside V2.
- **V2-only fixtures** (V1 absent, so V1 greps read nothing): `backend-defects` SP0a 9 · SP6a 1 · SP7 5 · SP8a 1 · SP9b 8; `slow-marketplace` SP0a 3 · SP7 1 · SP9b 13; `ds-defects`, `obs-defects`, `vuln-fullstack`, `node-api`, `quality-mix` ≤ 3 per grep.

## The 3,000-row path

A large diff is almost always one root cause.

1. **Prefix sanity first.** More than half the V1 keys V1-ONLY *and* half the V2 keys V2-ONLY is the normaliser, not the port: add the `prefix:` row the ledger suggests, or re-run with the `--routes` build of `dto-types.py` (precedents § 23). Nothing is triaged before that.
2. **Group by wiring row.** `cut -f2,3,4,5 "$OUT/candidates.tsv" | sort | uniq -c` (lane · diff · key · attr), then by V1 controller or route group, then by attr. One V1 global middleware or group missing in V2 is **one finding with N sites** (precedents § 27): `GLOBAL trim_strings on yes→no` covers every string field; a `role:admin` group covers every route in it; a vocabulary rename (`view.order` ↔ `orders:view`) is one `pair-map` question, not N rows.
3. **Read in this order:** I-AUTHZ and I-SCOPE (guarantee classes), the `GLOBAL` rule rows, enum stored values, then write routes in I-ROUTES, then I-ERR, I-CONF and the rest.
4. **Close a group with one checked reason** (`6 V1-ONLY web.php pages: each path is in apps/web/src/app-routes.tsx — UI class, parity-auditor Section 0`). Write routes, guards and tenant rows are never bulk-closed by name.
5. **Ledger the rest** as `Live, unreviewed (k groups / n rows)` with the command that continues it; never `checked`.

## Scans for

| § | Class | Lane / grep | Finding when (after the counterpart search) | Default severity | Solo | Oracle |
|---|---|---|---|---|---|---|
| 1 | MG-RT-1 route or method dropped | I-ROUTES V1-ONLY · SP1 | a live V1 key with no V2 key, no counterpart, no `pair-map` row | high; medium for an HTML-form `_method` route | Unconfirmed-solo | V358 |
| 2 | MG-RT-2 path / query shape | I-ROUTES `constraint` · SP0a, SP2a/b | the same key parses or pages differently | medium; high when a filter is dropped or a page is unreachable | Unconfirmed-solo | V358 |
| 3 | MG-AZ-1 permission widening | I-AUTHZ CHANGED (V2 ⊂ V1) · SP3a/b | V1 authz attrs ⊄ V2 attrs on the route, and nothing global or upstream restores them | **blocker** on data-bearing or money routes, else high → security | **Finding** | V359 |
| 4 | MG-AZ-2 permission narrowing | I-AUTHZ CHANGED (V1 ⊂ V2) | a role or ability V1 allowed is refused, with no ADR | medium | Unconfirmed-solo | V359 |
| 5 | MG-AZ-3 tenant / owner scope lost | I-SCOPE `tenant` · SP3b, SP5 | a V1-scoped table read on a V2 path with no filter, base-repository predicate or SQL predicate | **blocker** → security | **Finding** | V359 |
| 6 | MG-VO-1 enum / vocabulary drift | I-ENUM · SP6a/b | a V1 wire or stored value set ≠ V2's | high; low for a label-only change | Unconfirmed-solo | V360 |
| 7 | MG-VA-1 validation drift | I-RULES (incl. `GLOBAL`) · SP0b, SP7 | a per-field token differs, or V1's global trim / empty→null has no registered V2 counterpart (one finding, N fields) | high if V2 accepts more; medium if less | **Finding** for the `GLOBAL` rows; per-field Unconfirmed-solo | V361 |
| 8 | MG-ER-1 error status / code / envelope | I-ERR · SP8a/b | a V1 exception→status/code mapping V2 answers differently, or all-errors → first-error | high when a client branches on it; else medium | Unconfirmed-solo | V362 |
| 9 | MG-SD-1 silent defaults | I-CONF · SP9a/b | a default for an omitted field differs (page size, sort, currency, entity default) | medium; high on money or stored values | Unconfirmed-solo | V358 |

Severity rises one step on a route the façade already sends to V2 (it is live now) and falls one step behind a flag nothing can turn on. A static-fact row (a dropped guard, a lost scope) passes gate 6 with both ends cited; a behaviour row needs its oracle to fire ([precedents § 5](../../../../snippets/precedents/migration.md)).

### 1. Route or method dropped (MG-RT-1)

```
BAD:   V1  Route::post('/{order}/duplicate', 'duplicate')->middleware('can:orders.create');
       V2  OrdersService.duplicate() is ported; OrdersController has create, update, cancel — no handler
GOOD:  V2  @Post(':id/duplicate') @Permissions('orders:create') duplicate(...)   · or a pair-map row: rename / ADR-NNN
```
**Read both ends.** Is the V1 route live (an access-log hit, a mobile or partner client, a link in an e-mail template), or dead with an ADR (precedents § 2)? What does the SP1 line show for its last segment: a V2 service method only (ported, not exposed — the common shape), the SPA router (a `web.php` page now served by the client: refute, route the nav question to `@parity-auditor`), a façade or gateway rule (read it: precedents § 28), or a catch-all filter for `Route::fallback`? Does the façade already send the path to V2 (then it 404s today)? **Finding when** the V1 key is live, no V2 key answers, and the search above is empty. **Proof:** V358 — replay the V1 route list against V2: not 404, the same status class.

### 2. Path and query shape (MG-RT-2)

```
BAD:   V1  ->paginate($perPage)            (page=1 is the first page)      V2  return page * perPage;     (page=1 skips a page)
       V1  (array) $request->input('status', [])  with clients sending status[]=placed
       V2  new FastifyAdapter(fastifyOptions)  with no querystringParser — `status[]` arrives as a literal key and is stripped
GOOD:  V2  return (page - 1) * perPage;   ·   querystringParser: parseBracketQuery   ·   a lost whereNumber() restored as ParseIntPipe
```
**Read both ends.** Which paginator does V1 use (Laravel's is 1-based), and what does V2's offset helper do with `page=1`? Which array syntax do V1's clients send, and which query parser does V2's adapter run (Express 5's default is `"simple"`; Fastify's default is a fork of Node's `querystring` unless `querystringParser` names another — read what the V2 test or a one-line probe gives for `status[]=a&status[]=b`)? Did V1 constrain a param (`whereNumber`, `<int:id>`) that V2 now passes to the database as text? Trailing slash: does V1 redirect or match both, while Fastify matches neither by default (`ignoreTrailingSlash: false`)? **Finding when** the same request yields different rows, filters or status on the two sides. **Proof:** V358 — page 0/1/last+1, both array syntaxes, trailing slash on and off.

### 3. Permission widening (MG-AZ-1)

```
BAD:   V1  Route::post('/{wallet}/adjust', 'adjust')->middleware('permission:wallets.adjust');
       V2  @Post(':id/adjust') with no @Permissions, under a PermissionsGuard that returns true when no metadata is set
GOOD:  V2  @Post(':id/adjust') @Permissions('wallets:adjust')     (the sibling credit-limit handler already has it)
```
**Read both ends.** Where does V1 enforce it — route, group (`role:admin` around a prefix), controller constructor, `authorize()`, a policy, a FormRequest `authorize()`? What does every V2 guard do on this handler: is a global `APP_GUARD` metadata-driven and default-allow (SP3a), is there a class-level decorator, a gateway `auth_request` (read the façade file)? A route moved out of an admin group into a new controller loses the group's role: compare the CHANGED `roles` attr, not just abilities. Vocabulary: `can:view,order` is a **policy** — its body (SP3b) may carry the owner or tenant check that V2 moves to an ORM filter; compare after reading both, never by name. **Finding when** a role or caller V1 refused is allowed on V2. **Proof:** V359 — the matrix cell for that role on that route: V1 403, V2 2xx. Owner: security, when installed.

### 4. Permission narrowing (MG-AZ-2)

```
BAD:   V1  ->middleware('can:orders.view')  on GET /orders/export      V2  @Permissions('orders:export'), seeded for managers only
       V1  role:agent|admin                                            V2  @Roles('admin')
GOOD:  V2  @Permissions('orders:view')  ·  @Roles('agent', 'admin')  ·  or an ADR plus the seed change
```
**Read both ends.** Who held the V1 ability (the spatie seed or the roles table), who holds the V2 one (its permissions seed)? Is there an ADR? **Finding when** a role that succeeded on V1 gets 403 on V2 with no record. **Proof:** V359, V1 ⊆ V2 per cell.

### 5. Tenant or owner scope lost (MG-AZ-3)

```
BAD:   V1  #[ScopedBy([AccountScope::class])] class Ticket          V2  @Entity tickets with no @OwnerScoped filter
       V1  StockItem booted() addGlobalScope('account', …)          V2  execute('select … from stock_items where sku = ?')   (raw SQL: no filter applies)
GOOD:  V2  @scoped.OwnerScoped() on the entity  ·  where account_id = ? and sku = ?  on every raw statement
```
**Read both ends.** Which V1 tables carry a tenant or owner scope (the I-SCOPE rows, SP3b policy bodies)? On V2, which read paths reach that table — the ORM (does the filter default on, and is it enabled for this request?), a base repository, **raw SQL** (SP5 lists the statements with no tenant column), a report or export job (where V1 also bypassed it with `withoutGlobalScopes()` on purpose)? **Finding when** a V2 path returns or changes another tenant's row. **Proof:** V359 — the cross-tenant cell: V1 404, V2 200. Owner: security, when installed.

### 6. Enum and vocabulary drift (MG-VO-1)

```
BAD:   V1  case Cancelled = 'cancelled';        V2  ['draft', …, 'canceled', …] as const
       V1  enum TicketPriority: int { case Low = 1; … }     V2  export enum TicketPriority { Low, Normal, High, Urgent }   (0–3)
GOOD:  V2  'cancelled'   ·   enum TicketPriority { Low = 1, Normal = 2, High = 3, Urgent = 4 }
```
**Read both ends.** Which form differs — the **wire** value, the **stored** value or only the **label**? Do backfilled rows keep V1's spelling while V2 writes the new one? Does any V1 consumer (mobile app, partner webhook) read the value? Values in `*.test-data.*` or fixtures are inputs, not the vocabulary. A V2-only value with an ADR and tolerant consumers is the control. **Finding when** a V1 value fails to round-trip on V2 or a V2 value reaches a V1 consumer that rejects it. **Proof:** V360.

### 7. Validation drift (MG-VA-1)

```
BAD:   V1  framework-global TrimStrings + ConvertEmptyStringsToNull (except passwords)
       V2  registerInputNormalization() defined, never called; only TicketsController has @UsePipes(new NormalizeInputPipe(...))
       V1  'po_number' => ['nullable','string','max:30','regex:/^[A-Z0-9-]+$/']     V2  z.string().max(64).nullable().optional()
GOOD:  V2  the global pipe registered at bootstrap   ·   z.string().max(30).regex(/^[A-Z0-9-]+$/)
```
**Read both ends.** For a `GLOBAL` row: does V1 remove either middleware (`->remove(`, `except`), and on V2 is the pipe **registered** on the app (the engine notes a registration function nothing calls) or opted into per controller (that module is the control; the rest are the finding)? For a field row: which side accepts more, and what is the column (a 64-character PO into `varchar(30)` is a 500, not a 422)? **Finding when** an input V1 rejected, trimmed or nulled is accepted or stored differently on V2. **Proof:** V361 — empty, whitespace-only, `""` vs `null`, max ±1, the pattern; compare accept/reject **and** the stored value.

### 8. Error status, code and envelope (MG-ER-1)

```
BAD:   V1  OrderNotEditableException → 409 { message, code: 'order_not_editable' }     V2  new DomainError(400, 'Order is not editable')
       V1  422 lists every failing field                                               V2  result.error.issues.slice(0, 1)
GOOD:  V2  new DomainError(409, 'Order is not editable', 'order_not_editable')   ·   every issue mapped   ·   or ADR + changes_baseline
```
**Read both ends.** Which V1 renderer or default produces the status and `code`, and which V2 throw or filter does? Does a client branch on the status or `code` (offer "duplicate instead" on 409)? Message text is tolerated (precedents § 9); status, `code` and field keys are not. A declared 422 → 400 with ADR and `changes_baseline` is the control (precedents § 31). **Finding when** a contract error path answers with another status, `code` or field set. **Proof:** V362.

### 9. Silent defaults (MG-SD-1)

```
BAD:   V1  $request->input('per_page', 25)         V2  per_page: z.coerce.number()…default(20)
       V1  protected $attributes = ['currency' => 'SAR']    V2  currency: string = 'USD';
GOOD:  V2  .default(25)   ·   currency: string = 'SAR';
```
**Read both ends.** For each V1 default (model `$attributes`, request-input defaults, column defaults, config), find the V2 value the same omitted field gets: entity initialiser, zod or DTO default, service code that sets it only when present. Do clients compute from it (a 25-row page as the "more" signal)? A money or stored default is high. **Finding when** an omitted field yields a different stored or returned value. **Proof:** V358 with every optional parameter and body field omitted.

## Output

```
surface-parity-scan — paired · laravel 11.31.0 → nest 11.0.6 (fastify) · calibrated: built-in laravel→nest 0 rows · snapshot=live

Findings: 3 · Unconfirmed: 1 · routed → security: 2

1. v2/apps/api/src/credits/credits.controller.ts:31                [report-with-fix]  blocker → security
   §3 widening — POST /api/credits/{}/adjust: V1 permission:credits.adjust (v1/routes/api.php:40); V2 handler has no
   @Permissions and PermissionsGuard returns true without metadata (common/permissions.guard.ts:11). No gateway rule.
   Proof: V359 clerk 403 → 201. Fix: @Permissions('credits:adjust').
2. v2/apps/api/src/app-setup.ts:7                                  [report-with-fix]  high
   §7 GLOBAL trim_strings / empty_to_null yes→no — v1/bootstrap/app.php:20; registerInputNormalization() (common/
   boot-pipes.ts:13) is never called; tickets opt in (the control). One finding, every string field outside tickets.
   Proof: V361 "  PO-1 " stored untrimmed, "" stored for a nullable. Fix: call it in configureApp.
3. v2/apps/api/src/orders/orders.controller.ts:45                  [report-flagged]   high
   §1 POST /api/orders/{}/duplicate dropped — v1/routes/api.php:27; OrdersService.duplicate exists, no handler.
   Unproven link: V1 liveness (no access log read). Settling probe: V358 replay of the V1 route list.

Verification: 41 candidates → 3 findings · 1 unconfirmed · 4 hardening · 0 pre-existing · 33 refuted

Class coverage:
  §1  route dropped          checked (9 V1-ONLY → 2; 6 web.php pages in the SPA router, 1 fallback ↔ catch-all filter)
  §2  path / query shape     checked (SP2a 1, SP2b 3 → 2)
  §3  widening               → security (2)
  §4  narrowing              checked (2 CHANGED → 2)
  §5  tenant scope           → security (2)
  §6  enum drift             checked (6 CHANGED → 2; merged ADR-0008, label-only rename)
  §7  validation drift       checked (12 CHANGED → 2)
  §8  error contract         checked (I-ERR 1, SP8a 2 → 2)
  §9  silent defaults        checked (I-CONF 3, SP9 → 2)
```

`[report-with-fix]`: both ends cited, the counterpart search written out, the oracle fired (or the static fact is two-ended), and the fix is local. `[report-flagged]`: one link unproven; the row names it and the probe that settles it. Every run prints **all nine** §s, each as `checked (k candidates → m)`, `N/A (<reason>)`, `blocked (<lane or grep>: <reason>)`, `→ security (k)`, or `Unconfirmed-solo (k)`. A `checked · partial` lane says so.

## Precedents

The verifier reads [`precedents/migration.md`](../../../../snippets/precedents/migration.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most: § 1 counterpart search, § 2 dead V1, § 3 ADR plus `changes_baseline`, § 9 message text tolerated, § 21 solo mode, § 23 prefix sanity, § 26 pair-map reasons, § 27 one wiring row, § 28 counterparts outside the app, § 29 global trim, § 30 open-by-default routes, § 31 422 → 400. The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Migration, V358–V362.

## When to run

- On every whole-repo `/compare-v1`, printing all nine §s.
- On a diff that adds or moves a V2 controller, guard, pipe, filter, entity filter, enum, zod or DTO schema, or an entity default; and on any V1 change `/migration-sync` pulls in.
- Before a façade change sends another route prefix to V2.

## Halt conditions

- Do not report a high or blocker row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (security rows through the security protocol, when that pack is installed). Under `/compare-v1` that is `@parity-auditor` in refute mode plus `@verifier` on every BLOCKER and HIGH. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and keep the rest Unconfirmed, Hardening or Refuted. Never drop them.
- **Solo mode never prints GO.** Guarantee rows (§3, §5, the §7 `GLOBAL` rows) may become Findings from the recorded line plus the full V2 search; every other § stays `Unconfirmed-solo` with "re-run with `--v1=<path>`" (precedents § 21). A lane tagged `stale-v1-inventory` gives Unconfirmed rows only.
- Do not read a row from a lane that is `blocked` (calibration, prefix sanity, rg exit 2, `dto-types` NOT-RUN, extractor changed). Its §s print `blocked`, never `checked`.
- Halt on any finding without the V1 line, the V2 line or the written counterpart search, and the V-number.
- Do not add a `pair-map` row, a role to a seed, or `@Public()` to make a row quiet; the audit writes nothing into either tree.
- Do not print "surface parity holds" without the class-coverage block.

## Related

- `paired-inventory` (this pack) — the engine and its lanes; `semantics-parity-scan` and `side-effect-parity-scan` — the other two paired detectors.
- `/compare-v1` runs this skill and folds its coverage into the 48-class ledger; `@parity-auditor` judges the rows; `/find-and-fix --from-audit` closes them failing-first from the V-number.
- Security `@api-security-reviewer` and `@tenant-isolation-reviewer`, when the security pack is installed; backend `http-contract-scan`, `validation-boundary-scan`, `edge-error-scan` and `validation-boundary-scan/scripts/dto-types.py`, when the backend pack is installed.
