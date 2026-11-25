---
name: semantics-parity-scan
description: "V1→V2 semantics parity: rounding, integer division, strings, look-alikes, order, nulls, zones — read-only."
kind: skill
pack: migration
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: semantics-parity-scan

## Premise

"It is the same code in TypeScript" is the claim, not the proof. A port keeps V1's **semantics** only when the same input gives the same number, string, order, presence and instant on both sides, and the languages disagree in exactly the places a line-by-line port does not look: PHP `round(-2.5)` is −3 and JS `Math.round(-2.5)` is −2; `intdiv` truncates and `Math.floor` floors; `explode` with a limit keeps the rest and `split` with a limit drops it; `array_search` returns `false` and `indexOf` returns `-1`; a Laravel `max:60` or a Rails `length` validator counts characters and `Buffer.byteLength` counts bytes; MySQL hands back primary-key order nobody asked for and Postgres does not.

This skill pairs **call sites on the same money, string, date or list path** across the two trees, using the look-alike table below, and owns the V1≠V2 delta for MG-MN-1/2, MG-NUM-1, MG-STR-1, PP-4, MG-ORD-1, MG-NULL-1 and MG-TZ-1 (SM §1, §2, §4–§8). §3 (precision), §9 (plurals) and §10 (transactions) are routed to their single-codebase owners with the V1 inventory they need.

**Every finding cites the V1 call `file:line`, the V2 call `file:line`, the look-alike pair that differs, the path that stores, charges, reports or returns the value, and the oracle (V363–V368) that proves it.** Static reading alone gives `[report-flagged]` for these behaviour classes ([precedents § 5](../../../../snippets/precedents/migration.md)); `[report-with-fix]` needs the property or replay to fail on the pre-fix V2.

## The rule

A pair becomes a finding only when all four hold:

1. **Same path.** The V1 and V2 calls compute the same field for the same entry point (the I-MONEY `area:` key, a port comment, the ledger's file map, or the route that returns it). Two rounding calls in different features are not a pair.
2. **The pair diverges on an input that reaches it.** Negative halves on a refund, `x.xx5` on a discounted line, a negative SLA, a multibyte name, a tie in a sort key, an untagged ticket, a non-UTC server. The look-alike table says which input; gate 2 asks whether it occurs.
3. **Someone observes it.** A stored, charged or reported amount (any size is high, [precedents § 11](../../../../snippets/precedents/migration.md)); a list a consumer pages or takes "the first" of (§ 7); a typed consumer that branches on presence (§ 8). Display-only rounding of an already-rounded string is Hardening.
4. **No record makes it intentional** (ADR plus `changes_baseline`, § 3), and both sides do not call one decimal library with one explicit mode (§ 33).

## Boundaries

- **Precision and type on the wire (MG-MN-3)** → backend `wire-format-scan` §1/§2, when the backend pack is installed; SM §3 hands it the V1 `decimal:N` casts. Without it, §3 prints `N/A (owner pack backend not installed)` with the cast list.
- **Plural and format drift (MG-I18N-1)** → frontend `i18n-scan` §3 with `catalog-parity.py --v1=<laravel-root>`, when the frontend pack is installed; else `N/A (owner pack frontend not installed)`.
- **Transaction and isolation drift (MG-TX-1)** → database `transaction-scan` (§7 write skew, §8 lost update), when the database pack is installed; SM §10 hands it the V1 implicit-transaction and lock inventory. Without it, `N/A (owner pack database not installed)`.
- The single-codebase defect that exists whatever V1 did (float money, an unordered paginated query in a fresh app, a zone-less `Date`) belongs to backend and database detectors; this skill reports only what changed against V1.
- Input-rule drift (`max:60` vs a schema `max`) → `surface-parity-scan` §7; §5 here owns *how* the length is counted.

## Lanes

`paired-inventory` supplies I-MONEY (`area:<noun>` with rounding `modes`), I-CONF (`timezone`, `locale`, `currency`, `per_page`) and the I-RULES `max` rows; the greps below find the call sites the lanes do not key. Read the PHP platform version (`composer.json` / `composer.lock`) and the JS libraries (`decimal.js`, `big.js`, `dayjs`) from the lockfiles: PHP 8.4 changed `round()` pre-rounding (§ 33).

| Stack pair | Money / integers (§1–§4) | Strings (§5) | Order, nulls (§6–§7) | Time (§8) | Tag |
|---|---|---|---|---|---|
| **Laravel → NestJS** | PHP `round` half away from zero; `intdiv` truncates; `bc*` truncate at scale ↔ `Math.round` (ties toward +∞), `toFixed` on a binary float, decimal.js `ROUND_HALF_UP` (= away from zero) | `mb_*` count characters, `strlen`/`substr` bytes ↔ `.length`/`substring` UTF-16 units, `Buffer.byteLength` bytes | MySQL InnoDB → Postgres order; `->values()`, `?->` always emit ↔ `undefined` dropped by `JSON.stringify` | Carbon parses in the app zone ↔ `dayjs(x)` in the process zone, `dayjs.tz(x, zone)` in the given one | [V] port-pair |
| **Rails → Node** | `round(half: :even)` options, `BigDecimal` | `String#length` characters | `.order` absent on MySQL; `as_json` `nil` | `Time.zone` | [K?] |
| **Django / Python → any** | `round()` is half-even; `//` and `%` floor | `len` code points | `exclude_none` | `USE_TZ`, `zoneinfo` | [K?] |
| **Java / Spring → any** | `BigDecimal` `RoundingMode`, integer `/` truncates | `length()` UTF-16 units; default-locale case mapping (Turkish İ) | JPA order | `ZoneId.systemDefault()` | [K?] |
| **Go → any** | `math.Round` away from zero; integer `/` truncates | `len` bytes | `omitempty` drops zero values | `time.Local` | [K?] |

### The look-alike table (V1 → V2, known divergences)

Sources: PHP and MDN manuals fetched 2026-10-18 (MDN `split`, `indexOf`, `Math.floor`/`trunc` modified 2025-07-10; `length` 2026-09-02; `JSON.stringify` 2026-08-28), Day.js docs (fetched 2026-10-18), Laravel 12.x validation docs, and the research notes (the Rails, Django, Spring and Go rows stay [K?]) behind [precedents § 33, § 37](../../../../snippets/precedents/migration.md).

| V1 (PHP) | V2 (JS / TS) | Diverges on | § |
|---|---|---|---|
| `round($x, 2)` (half away from zero) | `Math.round(x * 100) / 100` (ties toward +∞) | negative halves: `round(-1.125, 2)` = −1.13, the JS form gives −1.12 | 1 |
| `round($x, 2)` (PHP < 8.4 pre-rounds) | `Number(x.toFixed(2))` (rounds the binary value) | `1.005`, `2.675`: V1 1.01 / 2.68, V2 1.00 / 2.67 | 1 |
| `round` per line, then `+=` | one rounding of the subtotal | multi-line sums differ by cents | 2 |
| `Money::allocate` (remainder to the first parts) | `round(total / n)` repeated | 100.00 / 3 sums to 99.99 | 2 |
| `intdiv($a, $b)` (toward zero; `intdiv(-3, 2)` = −1) | `Math.floor(a / b)` / `Math.round(a / b)` | negative dividends (floor), any remainder ≥ half (round) | 4 |
| `max:N` on a string (characters) / `mb_strlen` | `Buffer.byteLength(s) > N` / `s.length` (UTF-16 units) | Arabic (2 bytes), emoji (2 units) | 5 |
| `mb_substr($s, 0, N)` | `s.substring(0, N)` / `slice(0, N)` | a surrogate pair cut at N leaves a lone surrogate | 5 |
| `array_search(...) === false` (0 is a hit) | `!arr.indexOf(x)` (−1 is truthy, 0 is falsy) | the first element reads as "absent" | 5 |
| `explode(',', $s, 2)` (last part keeps the rest) | `s.split(',', 2)` (the rest is dropped) | any field holding the delimiter | 5 |
| `strtolower` / `strtoupper` (byte-wise ASCII) | `toLowerCase()` / `toLocaleLowerCase(tr)` | Turkish İ/ı, non-ASCII | 5 |
| query with no `orderBy` on MySQL (PK order in practice) | the same on Postgres (unspecified) | pagination duplicates and skips; `->first()` picks another row | 6 |
| `->orderByDesc('priority')->first()` (ties by PK) | `findOne(…, { orderBy: { priority } })` with UUID ids | which tie wins | 6 |
| `'tags' => $x->pluck()->values()` (always `[]`) | `cond ? list : undefined` (key dropped) | empty collections | 7 |
| `'shipped_at' => $x?->iso()` (key with `null`) | `...(x && { shipped_at })` (key absent) | unset values | 7 |
| `json_encode([])` = `[]`; `12.0` → `12` | `{}` / `12` / `12.0` per serializer | empty maps, whole decimals (§ 37) | 7 |
| `Carbon::parse($in)` (app zone) | `dayjs(in)` (process zone) vs `dayjs.tz(in, zone)` | a server `TZ` ≠ the business zone | 8 |
| `trans_choice` pipes and ranges | i18next CLDR categories | Arabic counts 0, 2, 3–10, 11–99 (§ 38) | 9 → frontend |

## Tool lane and ledger

Static only: the greps list call sites and the lanes key the money areas. The proof runs V1 as the model (fast-check or Hypothesis calling V1 over HTTP or `php -r` on the snapshot; `proof-oracles.md` § Harnesses (migration)). No PHP is run by this skill. The engine ledger comes first: an I-MONEY lane tagged `partial` prints `checked · partial`.

## Pre-flight

Run as one script (bash 3.2-safe). Inputs and the inside-V2 rule are those of `surface-parity-scan` § Pre-flight: `V2`, `V1` (empty = solo), `MIG`, `LIVE=1` for an uncommitted V1. Every grep ends in `ck`: exit 2 is a blocked class. V1 greps run through `v1g` by V1 stack (`surface-parity-scan` § Pre-flight): a Supabase V1 is read in its SQL (migrations included) and edge functions, a Rails, Django or Spring V1 prints N/A.

```bash
PI="${PI:-.claude/skills/paired-inventory/scripts/pair-inventory.py}"; V2="${V2:-.}"; V1="${V1:-}"; MIG="${MIG:-$V2/ai/migration}"
abs() { (cd "$(dirname "$1")" 2>/dev/null && printf '%s/%s\n' "$(pwd)" "$(basename "$1")") || printf '%s\n' "$1"; }
PI=$(abs "$PI"); MIG=$(abs "$MIG"); [ -n "$V1" ] && V1=$(abs "$V1"); cd "$V2" || exit 2   # grep from inside V2: rg globs also match the root path given
OUT="$(mktemp -d "${TMPDIR:-/tmp}/semantics-parity.XXXXXX")"; export GIT_OPTIONAL_LOCKS=0; mkdir "$OUT/no-v1"; : > "$OUT/stamp"
ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
if [ -n "$V1" ]; then SIDE=(--v1="$V1" ${LIVE:+--live-v1}); else SIDE=(--v1-inventory="$MIG/v1-inventory"); echo "solo: V1 greps search an empty dir (blocked, no V1 tree)"; fi
python3 -I "$PI" "${SIDE[@]}" --v2=. --lanes=I-MONEY,I-CONF,I-RULES --pair-map="$MIG/pair-map.tsv" --ledger="$MIG/ledger.md" --out="$OUT/run" > "$OUT/candidates.tsv" 2> "$OUT/ledger.txt"; echo "pair-inventory exit $? — 0 ran clean · 1 candidates (not a failure) · 2/3/4 BLOCKED: read $OUT/ledger.txt (its last line prints the reason) before any row"
S1=$(ls -d "$OUT"/run/run.*/v1 2>/dev/null | head -1); V1ROOTS=("${S1:-${V1:-$OUT/no-v1}}"); V2ROOTS=(.)
case "/${V1ROOTS[0]}/" in */fixtures/*|*/test/*|*/tests/*|*/spec/*|*/e2e/*|*/docs/*|*/lang/*|*/vendor/*) echo "BLOCKED: the V1 root path holds an excluded segment, so every V1 grep reads 0 files — copy V1 out or use the snapshot";; esac
X=(-g '!**/{node_modules,vendor,dist,build,coverage,storage,bootstrap/cache,migrations}/**' -g '!**/{test,tests,spec,__tests__,__mocks__,fixtures,e2e}/**'
   -g '!**/*.{spec,test,e2e-spec,test-data,fixture,fixtures,d,stories}.*' -g '!**/{lang,locales,i18n,docs}/**' -g '!**/database/{seeders,factories}/**' -g '!**/*.{md,lock,map,snap,json}')
V1STACK=none; [ -f "${V1ROOTS[0]}/composer.json" ] && V1STACK=laravel; [ -d "${V1ROOTS[0]}/supabase/migrations" ] && V1STACK=supabase; echo "V1 stack: $V1STACK (V1 greps read its files: PHP for laravel, SQL + edge functions for supabase, else N/A — never 0 files silently)"
v1g() { local id="$1" php="$2" sb="$3"; shift 3; case "$V1STACK" in laravel) rg -n --pcre2 "$@" "$php" -g '*.php' "${X[@]}" "${V1ROOTS[@]}"; ck "$id" $?;; supabase) if [ "$sb" = - ]; then echo "$id N/A (V1 stack supabase: no grep for this shape; the lane rows carry it)"; else rg -n -i --pcre2 "$sb" -g '*.{sql,ts,toml}' -g '!**/{node_modules,tests,__tests__}/**' -g '!**/*.{test,spec}.ts' "${V1ROOTS[0]}/supabase"; ck "$id" $?; fi;; *) echo "$id N/A (V1 stack $V1STACK: this grep reads Laravel PHP or Supabase SQL; a Rails, Django or Spring V1 prints N/A)";; esac; }
awk -F'\t' '$1=="CANDIDATE" && ($4 ~ /^area:|^(timezone|locale|currency|per_page)$/ || $5 ~ /^(max|clamp_max)$/)' "$OUT/candidates.tsv" | cut -f2-9
# 0. Engines, runtimes, libraries and process zones on both sides (gates 3 and 7 for every class below).
rg -n --pcre2 '^\s*DB_CONNECTION=|"php"\s*:\s*"[^"]+"|"(?:pg|mysql2|@mikro-orm/(?:postgresql|mysql)|decimal\.js|big\.js|dayjs|luxon|date-fns-tz|i18next)"\s*:|^\s*(?:ENV\s+)?TZ[=\s]|\b(?:APP_TIMEZONE|TZ)\b\s*(?::|=)' -g '*.{json,yaml,yml,example,php}' -g 'Dockerfile*' -g '!**/{node_modules,vendor}/**' -g '!**/*lock*' "${V1ROOTS[@]}" "${V2ROOTS[@]}"; ck SM0 $?
# 1. Rounding calls: V2 (JS/TS, Python) and V1 (PHP). A cents shape `Math.round(x * 100) / 100` is the negative-half pair.
rg -n --pcre2 'Math\.round\(|\.toFixed\(|\btoDecimalPlaces\(|\bROUND_(?:HALF_\w+|UP|DOWN|CEIL|FLOOR)\b|\bRoundingMode\.\w+|\bquantize\(|(?<![\w.])round\(' -g '*.{ts,tsx,js,py}' "${X[@]}" "${V2ROOTS[@]}"; ck SM1a $?
v1g SM1b '(?<![\w>:$])round\(|\bnumber_format\(|\bbc(?:add|sub|mul|div|mod|pow)\(|\bPHP_ROUND_\w+|RoundingMode::\w+' '\bround\s*\(|\btrunc\s*\(|::\s*numeric\s*\(\s*\d+\s*,\s*\d+|\.toFixed\(|Math\.round\('
# 2. Order and allocation: V2 rounds an aggregate or splits by a count; V1 rounds per line and sums, or allocates a remainder.
rg -n --pcre2 '[Rr]ound\w*\(\s*[\w.]*(?:[Ss]ub)?[Tt]otal\w*\s*[*/]|[Rr]ound\w*\([^()\n]*/\s*[\w.]*(?:count|length|parts|n)\b|\.toFixed\([^()\n]*\)\s*\*\s*\w*(?:count|length)\b' -g '*.{ts,tsx,js,py}' "${X[@]}" "${V2ROOTS[@]}"; ck SM2a $?
v1g SM2b '\+=\s*round\(|\bfunction\s+allocate\w*\(|\$remainder\b' '\bround\s*\(\s*[\w.]+\s*\*\s*[\w.]+|\bround\s*\([^;]*\)\s*\*\s*\w+|\bsum\s*\(\s*round\s*\('
# 4. Integer division: V2 floor / round / ceil of a quotient, `| 0`, Python `//`; V1 intdiv, (int) casts, fmod.
rg -n --pcre2 'Math\.(?:floor|round|ceil)\(\s*[^()\n]*?[\w)]\s*/\s*[\w(]|\bparseInt\([^()\n]*/|[\w)]\s*/\s*[\w.]+\s*\|\s*0\b|\w\s*//\s*\w' -g '*.{ts,tsx,js,py}' "${X[@]}" "${V2ROOTS[@]}"; ck SM4a $?
v1g SM4b '\bintdiv\(|\(int\)\s*\(\s*\$[\w>-]+\s*/|\bfmod\(|\bfloor\(\s*\$[\w>-]+\s*/' '\bdiv\s*\(|::\s*(?:int|integer|bigint)\s*/\s*\w+|\w+\s*/\s*\w+\s*\)?\s*::\s*(?:int|integer|bigint)\b|Math\.(?:floor|trunc)\(\s*[\w.]+\s*/'
# 5. Strings and look-alikes: byte vs character lengths, code-unit slicing, split limits, indexOf truthiness.
rg -n -U --pcre2 'Buffer\.byteLength\(|\.substring\(\s*0\s*,|\.substr\(|\.split\([^()\n]*,\s*\d+\s*\)|(\w+)\s*=\s*[^;\n]*\.(?:indexOf|findIndex|search)\([^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*(?:\(\s*!\s*\1\s*[)&|]|\1\s*==\s*(?:false|null)\b)' -g '*.{ts,tsx,js}' "${X[@]}" "${V2ROOTS[@]}"; ck SM5a $?
v1g SM5b '\bmb_(?:substr|strlen|str_split|strtolower|strtoupper|strimwidth)\(|(?<!mb_)\b(?:substr|strlen|strtolower|strtoupper|ucfirst)\(|\bexplode\([^()\n]*,[^()\n]*,\s*-?\d+\s*\)|\barray_search\(|\bstrpos\(' '\bsplit_part\s*\(|\b(?:left|right|substr|substring)\s*\(|\.(?:slice|substring|substr)\(|\binitcap\s*\('
# 6. Ordering: V2 paged reads with no orderBy, and findOne ordered by one non-id key (ties); V1 single-key orderBy and latest().
rg -n -U --pcre2 '\.(?:find|findAndCount|findAll|findMany)\(\s*\w+\s*,(?:(?!\borderBy\b)[^;])*?\b(?:limit|offset|take|skip)\b(?:(?!\borderBy\b)[^;])*?\)\s*;|\.(?:findOne\w*|findFirst\w*)\(\s*\w+\s*,[^;]*?\borderBy\s*:\s*\{\s*(?!id\b|uuid\b)\w+\s*:\s*[\w.\x27"]+\s*,?\s*\}' -g '*.{ts,js}' "${X[@]}" "${V2ROOTS[@]}"; ck SM6a $?
v1g SM6b '(?:->orderBy(?:Desc)?\(\s*\x27\w+\x27\s*\)\s*(?:->(?:first|get|paginate|simplePaginate|take|limit)\(|$)|->(?:latest|oldest)\(\))' '\border\s+by\s+[\w.]+(?:\s+(?:asc|desc))?\s*(?:limit\b|\)|;)'
# 7. Null / empty / missing: V2 branches to `undefined` or spreads a key in only when set; V1 forces lists and nulls.
rg -n --pcre2 '\?\s*[^:;\n]+:\s*undefined\b|\.\.\.\(\s*[^()\n]*?&&\s*\{|\bjson:"\w+,omitempty"|\bexclude_(?:none|unset)\s*=\s*True' -g '*.{ts,tsx,js,go,py}' "${X[@]}" "${V2ROOTS[@]}"; ck SM7a $?
v1g SM7b '(?:->values\(\))|=>\s*\$this->\w+\?->|\bjson_encode\(|\barray_filter\((?![^\n]*array_values)|JSON_(?:PRESERVE_ZERO_FRACTION|FORCE_OBJECT)' '\bjsonb?_strip_nulls\s*\(|\bnullif\s*\(\s*[\w.]+\s*,\s*\x27\x27\s*\)|\bcoalesce\s*\(\s*[\w.]+\s*,\s*\x27\x27\s*\)'
# 8. Time zones: V2 parses dates with no zone; V1 parses in the app zone (Carbon). The config pair is the I-CONF row above.
rg -n --pcre2 '\bdayjs\(\s*[\w.]+\s*\)(?!\s*\.tz)|\bmoment\(\s*[\w.]+\s*\)(?!\s*\.tz)|\bnew Date\(\s*\w*(?:Raw|Str|String|query|body|params|input|from|to)\w*\s*\)|\bDate\.parse\(|\bdatetime\.(?:now|fromisoformat|strptime)\((?![^)\n]*tz)' -g '*.{ts,tsx,js,py}' "${X[@]}" "${V2ROOTS[@]}"; ck SM8a $?
v1g SM8b 'Carbon::(?:parse|createFromFormat)\(|\bstrtotime\(|->(?:timezone|setTimezone)\(|\bdate_default_timezone_set\(|->(?:startOfDay|endOfDay|addMonths?|subMonths?)\(' '\bat\s+time\s+zone\b|\bdate_trunc\s*\(|::\s*date\b|\bcurrent_date\b|\btimezone\s*\('
# 3 / 9 / 10 — routed: the V1 inventory each owner needs (decimal casts, plural calls, implicit transactions and locks).
v1g SM-routed '\x27decimal:\d+\x27|\btrans_choice\(|@choice\(|\bDB::transaction\(|->(?:lockForUpdate|sharedLock)\(\)' '::\s*numeric\s*\(|\bfor\s+update\b|\bpg_advisory\w*lock\b|\bisolation\s+level\b'
for R in "$V1" .; do [ -n "$R" ] && find "$R" -newer "$OUT/stamp" -type f -not -path '*/node_modules/*' | head -3; done; echo "write check done (empty = nothing written)"
```

Pair the V2 lines with the V1 lines by path: the I-MONEY `area:` key, a `// Port of V1 …` comment, the same route, or the same function name. A V2 call with no V1 twin is not a semantics row (it may be new code); a V1 call with no V2 twin is a `surface-parity-scan` or `side-effect-parity-scan` question.

## Measured

Measured 2026-10-18 on this repo's fixtures, and 2026-10-19 on one real Supabase → Nest port (read-only).

- **A real Supabase → Nest port** (2026-10-19). Before: every SM V1 grep read `*.php` (0 V1 lines). After: SM1b 484 · SM2b 273 · SM4b 2 · SM5b 504 · SM6b 525 · SM7b 1,252 (narrowed from 12,940: only `coalesce(x, '')`, `nullif(x, '')`, `json_strip_nulls`) · SM8b 369 · SM-routed 376. The I-MONEY lane pairs 5 V1 areas (was 1) once pagination rounding is dropped (precedent § 49). `port-pair` unchanged.

- **`port-pair`, paired** (`--live-v1`; the port PR in `change/` overlaid). Engine rows (the build whose candidate rows carry a `lane` column): I-MONEY 5 / 6 rows → 1 V2-ONLY, 4 CHANGED — the PR's credit-note module pairs by name with the V1 pricing service as `area:pricing half-away → half-away,half-up`, and `area:order` carries the `float-tofixed` line net; I-CONF `timezone` Asia/Riyadh → UTC and `per_page` 25 → 20. Grep lines: SM0 9 · SM1a 9 · SM1b 12 · SM2a 2 · SM2b 4 · SM4a 2 · SM4b 3 · SM5a 6 · SM5b 8 · SM6a 7 (3 sites) · SM6b 8 · SM7a 2 · SM7b 8 · SM8a 1 · SM8b 6 · routed 16. Each of the 16 migration-owned SM seeds sits on a grep line or a lane row, the **negative-half credit-note seed** on SM1a (`Math.round(Number(net) * ratio * -1 * 100) / 100`) paired with SM1b `round((float) $net * $ratio * -1, 2)`; the three routed seeds sit on the routed line (casts, `lockForUpdate`) or their owner's input (`lang/ar`). Decoys on a line, refuted on reading: half-even by ADR (SM1a), decimal.js `ROUND_HALF_UP` (SM1a), the tag suggester whose contract says the order is unspecified (SM6a). The display-only `Intl.NumberFormat` decoy is on no line.
- **Noise fix.** SM6a first also listed every single-key `orderBy`: 14 lines on `slow-marketplace`. Restricted to paged reads with no `orderBy` and `findOne` ordered by one non-id key, it prints 1 there and keeps both seeds.
- **V2-only fixtures** (no V1): `slow-marketplace` SM1a 7 · SM7a 3 · SM8a 4; `quality-mix` SM1a 7 · SM4a 3; `backend-defects` SM1a 4; others ≤ 3 per grep.
- **Solo** (re-recorded inventory): the V1 greps read an empty directory; every SM row stays `Unconfirmed-solo` with the recorded I-MONEY / I-CONF line as the only V1 evidence.

## The 3,000-row path

1. **Key by area first.** `cut -f4 "$OUT/candidates.tsv" | sort | uniq -c` on the `area:` rows (I-MONEY pairs on the outermost money method). One shared V2 helper that differs from V1 (a `roundMoney` written as `Math.round`) is **one finding with N call sites**; a V2 helper that matches V1 (decimal.js with an explicit mode) clears every call that goes through it.
2. **Read money paths first** (stored, charged, reported), then integer division on stock and SLA paths, then strings on validated or sent fields, then list order on paged and "first" reads, then presence on typed consumers, then dates on report boundaries.
3. **Close a group with one checked reason** (`22 Math.round calls in apps/web: display only, inputs are V1-rounded strings`). Money paths are never bulk-closed by name.
4. **Ledger the rest** as `Live, unreviewed (k groups / n lines)`, never `checked`.

## Scans for

| § | Class | Finding when | Default severity | Solo | Oracle |
|---|---|---|---|---|---|
| 1 | MG-MN-1 rounding mode | a V1/V2 rounding pair on one money path differs in mode or pre-rounding | high on stored, charged or reported amounts (§ 11); Hardening when display only | Unconfirmed-solo | V363 |
| 2 | MG-MN-2 rounding order / allocation | per-line vs per-total, or a split whose parts do not sum to the total | high | Unconfirmed-solo | V363 |
| 3 | MG-MN-3 precision / type | — | → backend `wire-format-scan` | → backend | V339 / V363 |
| 4 | MG-NUM-1 integer division | the quotient or remainder differs for an input the path receives | medium; high on stock, money or quota | Unconfirmed-solo | V364 |
| 5 | MG-STR-1 + PP-4 strings and look-alikes | a length, slice, split, search or case pair differs on input the field accepts | medium; high when it rejects valid input or corrupts stored text | Unconfirmed-solo | V365 |
| 6 | MG-ORD-1 ordering | a paged or first-match read whose order V1 fixed (PK order, a tiebreak) and V2 does not | high with pagination or first-match; Hardening with no consumer (§ 7) | Unconfirmed-solo | V366 |
| 7 | MG-NULL-1 null / empty / missing | a field's presence or shape differs and a consumer is typed or branches on it | medium | Unconfirmed-solo | V367 |
| 8 | MG-TZ-1 time zone / parse | the zone a date is parsed, grouped or bounded in differs | high on report or due-date boundaries; medium otherwise | Unconfirmed-solo | V368 |
| 9 | MG-I18N-1 plurals | — | → frontend `i18n-scan` §3 | → frontend | V369 |
| 10 | MG-TX-1 transactions | — | → database `transaction-scan` | → database | V370 |

### 1. Rounding mode (MG-MN-1)

```
BAD:   V1  $refund = round((float) $net * $ratio * -1, 2);           V2  Math.round(Number(net) * ratio * -1 * 100) / 100
       V1  round((float) $unitPrice * $quantity * (1 - $discount), 2) V2  Number((unitPrice * quantity * (1 - discount)).toFixed(2))
GOOD:  V2  money.roundMoney(x, 2)      (decimal.js toDecimalPlaces(2, ROUND_HALF_UP): ties away from zero, as PHP)
```
**Read both ends.** Which PHP version (pre-rounding before 8.4)? Can the value be negative (credits, refunds, returns, discounts) or land on a half cent? Does a shared V2 helper already match V1, so the finding is the call that bypasses it? Is the result stored, charged or summed into a report? **Finding when** some reachable input rounds differently on a stored, charged or reported amount. **Proof:** V363 — property with V1 as the model at x.5 ties, negatives and `1.005`.

### 2. Rounding order and allocation (MG-MN-2)

```
BAD:   V1  foreach (lines) { $tax += round($net * $rate, 2); }          V2  roundMoney(subtotal * taxRate, 2)
       V1  Money::allocate($total, $count)  (remainder cents first)    V2  Array.from({ length: n }, () => round(total / n, 2))
GOOD:  V2  per-line tax then sum  ·  money.allocateCents(total, n)
```
**Read both ends.** Where does V1 round — per line, per tax group, per total? Does V2 round at the same step? For a split: do the parts sum to the total on both sides? A faithful port often sits unused beside the call (an `allocateCents` nobody calls). **Finding when** a multi-line sum or a split differs on any input. **Proof:** V363 — many-line carts and 100.00 three ways; parts sum to the total.

### 4. Integer division (MG-NUM-1)

```
BAD:   V1  $hours = intdiv($minutesLeft, 60);      V2  Math.floor(minutesLeft / 60)    (−90 → −1 vs −2)
       V1  intdiv($free, $item->pack_size);         V2  Math.round(free / row.pack_size)  (11/4 → 2 vs 3)
GOOD:  V2  Math.trunc(a / b)
```
**Read both ends.** Can the dividend be negative (overdue, refunds, balances)? Is the result a count of whole units someone can order or a threshold someone is escalated on? Python `//` floors where JS, Java, Go and PHP `intdiv` truncate. **Finding when** a reachable input gives another quotient or remainder. **Proof:** V364 — negative dividends and remainders ≥ half.

### 5. Strings and look-alike APIs (MG-STR-1, PP-4)

```
BAD:   V1  'company_name' => ['max:60']            V2  if (Buffer.byteLength(name, 'utf8') > 60) reject     (Arabic: 2 bytes a letter)
       V1  mb_substr($subject, 0, 50)              V2  subject.substring(0, 50)                            (emoji split)
       V1  if ($pos === false)                     V2  if (!pos)          after indexOf                     (index 0 is "absent")
       V1  explode(',', $line, 2)                  V2  raw.split(',', 2)                                    (description loses text)
GOOD:  V2  Array.from(s).length  ·  Array.from(s).slice(0, n).join('')  ·  pos === -1  ·  split at the first index only
```
**Read both ends.** What does the field hold in production (Arabic names, emoji subjects, commas in CSV descriptions)? Which unit does each side count? Is the result validated, stored or sent to a gateway that rejects malformed text? Look up the pair in the look-alike table; a pair not in it is read from both manuals before it is reported. **Finding when** valid input is rejected, cut or misread on V2. **Proof:** V365 — multibyte, emoji at the limit, delimiter in the last field, the first element of a list.

### 6. Ordering (MG-ORD-1)

```
BAD:   V1  Order::query()->paginate($perPage)   (MySQL InnoDB: PK order in practice)
       V2  em.findAndCount(Order, where, { limit, offset })   (Postgres: unspecified, changes after updates)
       V1  ->orderByDesc('priority')->first()   (ties by PK: oldest first)   V2  findOne(…, { orderBy: { priority: DESC } })  (UUID ids)
GOOD:  V2  orderBy: { id: 'asc' }  ·  orderBy: { priority: DESC, createdAt: ASC }
```
**Read both ends.** Which engine does each side run (SM0)? Does a consumer page through the list, take the first row, or diff it? A contract that says "order unspecified" with a consumer that sorts client-side is the control (§ 7). **Finding when** a paged or first-match read can return another row or skip one on V2. **Proof:** V366 — ties on the sort key, updates between pages.

### 7. Null, empty and missing (MG-NULL-1)

```
BAD:   V1  'tags' => $this->tags->pluck('name')->values()   (always an array)
       V2  tags: cond ? list : undefined                      (JSON.stringify drops the key)
       V1  'shipped_at' => $this->shipped_at?->toIso8601String()   (null)     V2  ...(o.shippedAt && { shipped_at: … })   (absent)
GOOD:  V2  tags: list ?? []  ·  shipped_at: o.shippedAt ? o.shippedAt.toISOString() : null
```
**Read both ends.** What does the contract say (`.nullable()` vs `.optional()`)? Does a typed consumer (a mobile decoder, `=== null` checks) branch on presence? Does a cast (`as Dto`) hide the gap from the type checker? **Finding when** a consumer sees `undefined` where V1 sent `[]` or `null`, or the reverse. **Proof:** V367 — empty list, unset value, `json_encode([])`.

### 8. Time zones and parsing (MG-TZ-1)

```
BAD:   V1  'timezone' => env('APP_TIMEZONE', 'Asia/Riyadh')    V2  timezone: process.env.APP_TIMEZONE ?? 'UTC'  (and the API deployment sets no APP_TIMEZONE)
       V1  Carbon::parse($from)->startOfDay()   (app zone)      V2  dayjs(fromRaw).startOf('day')   (process zone; the next line uses dayjs.tz)
GOOD:  V2  the V1 zone as default and in the deployment  ·  dayjs.tz(fromRaw, appConfig.timezone).startOf('day')
```
**Read both ends.** Which zone does each process run in (SM0: Dockerfile `TZ`, manifest env)? Which zone parses request dates, groups report days and computes due dates? Are both ends of a range parsed the same way? **Finding when** an instant or a calendar day differs for a non-UTC business zone. **Proof:** V368 — server `TZ` ≠ business zone, DST and month boundaries.

### 3, 9, 10. Routed

- **§3 precision** — the routed line lists V1 `decimal:N` casts; hand each cast field to `wire-format-scan` §1 (a V2 `Number(amount)` on a `decimal:2` field). Print `→ backend (k)`.
- **§9 plurals** — run frontend `catalog-parity.py --v1=<V1 root>` and hand its rows to `i18n-scan` §3. Print `→ frontend (k)`.
- **§10 transactions** — the routed line lists `DB::transaction` and `lockForUpdate` sites; hand each with its V2 counterpart to `transaction-scan`. Print `→ database (k)`.

## Output

```
semantics-parity-scan — paired · php ^8.3 → node (decimal.js 10.4.3, dayjs 1.11.13) · mysql → postgresql · I-MONEY partial

Findings: 1 · Unconfirmed: 3 · routed: backend 1 · frontend 1 · database 1

1. v2/apps/api/src/invoices/credit-memo.ts:5                      [report-with-fix]  high
   §1 rounding mode — Math.round(Number(net) * ratio * -1 * 100) / 100 vs V1 round((float) $net * $ratio * -1, 2)
   (v1/app/Services/RefundCalculator.php:21). Credit notes are stored and refunded. Proof: V363 net 1.125, ratio 1:
   V1 −1.13, V2 −1.12 (fails). Fix: money.roundMoney(…, 2), the helper the other money paths use.
2. v2/apps/api/src/tickets/escalation.ts:21                       [report-flagged]   medium
   §5 look-alike — `if (!pos)` after indexOf vs V1 `$pos === false` (EscalationService.php:27): tier1 (index 0) reads as
   unknown. Unproven link: no property run. Settling test: V365 nextTier('tier1') → 'tier2' on both.

Verification: 19 candidates → 1 finding · 13 unconfirmed · 2 hardening · 0 pre-existing · 3 refuted

Class coverage:
  §1  rounding mode          checked (SM1a 9 / SM1b 12 → 2; half-even by ADR-0012, decimal.js HALF_UP = V1)
  §2  order / allocation     checked (SM2a 2 → 2)
  §3  precision              → backend (1)
  §4  integer division       checked (SM4a 2 → 2)
  §5  strings, look-alikes   checked (SM5a 4 sites → 4)
  §6  ordering               checked (SM6a 3 sites → 2; tag suggester: contract says unspecified)
  §7  null / missing         checked (SM7a 2 → 2)
  §8  time zones             checked (I-CONF timezone, SM8a 1 → 2)
  §9  plurals                → frontend (1)
  §10 transactions           → database (1)
```

`[report-with-fix]`: the pair is cited on both sides, the property or replay failed on the pre-fix V2, and the fix is local. `[report-flagged]`: the static pair is read and the oracle has not run; the row names the settling test. Every run prints all ten §s as `checked (k candidates → m)`, `N/A (<reason>)`, `blocked (<reason>)`, `→ <owner> (k)` or `Unconfirmed-solo (k)`.

## Precedents

The verifier reads [`precedents/migration.md`](../../../../snippets/precedents/migration.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4: § 3 intentional breaks, § 4 single-codebase owners, § 5 behaviour classes need execution, § 6 versions from lockfiles, § 7 order needs a consumer, § 8 presence needs a typed consumer, § 11 money, § 21 solo, § 33 negative halves and PHP 8.4, § 34 MySQL → Postgres order, § 35 `_ci` keys, § 37 PHP JSON shapes, § 38 plurals. Oracles: [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Migration, V363–V370.

## When to run

- On every whole-repo `/compare-v1`, printing all ten §s.
- On a diff that ports a service holding arithmetic, string handling, list queries, serializers or date code; on any change to `common/money`-style helpers.
- Before a money, report or SLA path moves to V2 at the façade.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/compare-v1` that is `@parity-auditor` in refute mode plus `@verifier` on every HIGH. Run standalone, apply the protocol as a separate second pass, tag rows `self-verified`, and keep the rest Unconfirmed, Hardening or Refuted. Never drop them.
- **Solo mode never prints GO**, and every SM class is a behaviour class: in solo mode each row is `Unconfirmed-solo` with "re-run with `--v1=<path>`" (precedents § 21).
- Do not mark a behaviour row `[report-with-fix]` from reading. It needs V363–V368 to fail on the pre-fix V2 with V1 as the model.
- Do not pair calls from different paths, and do not report a V2-only computation as drift.
- Do not report a mechanism one side's runtime does not have (precedent 2 of `refute-before-report.md` § 4); read the versions in SM0 first.
- Do not print "semantics hold" without the class-coverage block; a blocked grep or lane is `blocked`, never `checked`.

## Related

- `paired-inventory` (I-MONEY, I-CONF lanes), `surface-parity-scan`, `side-effect-parity-scan` (this pack); `/compare-v1`, `@parity-auditor`, `/find-and-fix --from-audit`; `parity-test-generate` writes the property tests.
- Backend `wire-format-scan`, frontend `i18n-scan` with `catalog-parity.py --v1`, database `transaction-scan` — each when its pack is installed.
