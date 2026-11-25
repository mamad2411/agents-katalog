---
name: data-cutover-orchestrate
description: "V1→V2 data cutover: backfill, reconcile, load casts, ids, fenced flip, reverse path — read-only."
kind: skill
pack: migration
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: data-cutover-orchestrate

## Premise

A port moves the data as well as the code: a V1 store fills a **different** V2 store (another engine, schema or service), and reads, then writes, follow it. Three failures dominate. Reads flip before the backfill is complete and verified, and users see missing or stale rows. Dual writes run with no reconciliation, or with one that masks the drift it exists to find, and the two stores diverge silently. Writes flip with no fence and no way back, so a rollback after the flip loses every V2 write. The successful public cutovers kept every part of the shape: a bulk copy, change replication, a check before the read flip, a fenced write flip measured in seconds, and a reverse path (Stripe 2024-06-06, Figma 2023-04-04, Notion 2021-10-06; research notes B, C3).

This skill owns the cross-store data classes **DM-1…DM-9 and DM-11…DM-13** (DC §1–§12). It reads backfill, sync, reconcile, loader, flag and plan code, and both schemas through `paired-inventory`. It also keeps the orchestration contract below: the 7-step cutover sequence and a **readiness verdict** the read-flip gate consults.

**Every finding cites the V2 line (backfill, reconcile query, loader rule, flag, runbook step), the V1 fact it breaks (the schema row, the route, the zone, the writer), and the oracle that proves it.** "The data is migrated" is not evidence. A readiness verdict without the reconcile result **and** the checkpoint is BLOCK. No `CLEAR` is ever printed without the class-coverage block (§ Output).

## The rule

A candidate becomes a finding only when all four hold:

1. **The data path is real.** The file runs in the cutover: `run.ts`, a runbook step, a CI job or the flag system names it. A script nothing calls is Hardening.
2. **V1 holds the data or the writer the step breaks.** It is the V1 column, constraint, zone, id or live writer, read from the schema row (`I-SCHEMA`, `I-SCOPE`, `I-CONF`) or from V1 code. A recorded row counts in solo mode (§ Halt conditions).
3. **Nothing else in the window covers it.** Read the shared runner, the target library, the loader defaults, the CDC config, the flag system, the runbook and the ADRs (precedents § 1, § 12–§ 14, § 28).
4. **No record makes it intentional.** There is no ADR plus `changes_baseline` (precedents § 3), and no declared, bounded lag with a matching threshold (precedents § 13).

## Boundaries

- **Single-store** schema evolution (expand-contract, an in-table batched backfill, online DDL) → database `migration-safety`, when the database pack is installed. Without it, this skill names the class and leaves it ungraded. One store means hand off.
- **Dual-write, CDC and outbox mechanics** (lost events, ordering, at-least-once) → distributed-systems `dual-write-scan`, when that pack is installed. This skill keeps the reconcile and flip gates. A CDC consumer's own upsert is that pack's row.
- **Output equivalence** → `parity-test-generate` and `parity-proof-scan`. A green parity suite over an empty V2 store still fails at the read flip; you need both.
- Effects duplicated in the dual-run window (SE §2) and DB triggers that maintained a column (SE §5) → `side-effect-parity-scan`. A dropped soft-delete **filter on reads** is §7 here. A lost tenant scope is SP §5.
- Façade routing, session crossing, shadow isolation and V1 kept warm → `cutover-routing-scan`.

## The cutover sequence (the orchestration contract)

Run these steps in order. Each step leaves an artifact that the next step, and the gate, read.

1. **Source of truth for the window.** One store is authoritative per feature (`source_of_truth: v1` in the plan). Ambiguity is how both end up half-right.
2. **Dual write or CDC through one mapper.** The backfill and the live path call the same function (§4). An unreconciled dual write is two stores drifting on a timer.
3. **Resumable, checkpointed, idempotent, throttled backfill** (§1–§2). Batches by key range, a durable cursor, an upsert keyed on the V1 id with a version guard, and a pause or lag check between batches.
4. **Preload anomalies decided per class** (§8), loader casts and zones declared (§6), ids kept or mapped (§5), sequences reset (§9), live-row semantics kept (§7).
5. **Reconcile with a stated mask list** (§3). The checks run in order: counts per range, money aggregates, row comparison on exact fields, then repeat after CDC catch-up. A reconciler is trusted only after it reports seeded drift (V375).
6. **Read flip, gated** on checkpoint-complete **and** reconcile-green (§10). It is behind a flag that is reversible in one step.
7. **Fenced write flip, reverse path, point of no return** (§10–§11). Pause and revoke the V1 writers, then flip. The reverse sync then replays V2 writes into V1. V1 objects are dropped only at a named, signed step after the soak, never in the release that flips writes.

A mapping change after the checkpoint started invalidates every key already ported (§12).

## Lanes

The V1 side comes from `paired-inventory` (`I-SCHEMA` constraints and views, `I-SCOPE` soft delete, `I-CONF` timezone). The data path is mostly V2 code and deploy files, read by the greps below. Tool facts come from the research notes B (C6), dated there; never from memory.

| Stack / tool | Backfill and sync (§1, §2, §4, §5, §9) | Reconcile (§3) | Load and CDC (§6, §9) | Flags and plan (§10–§12) | Tag |
|---|---|---|---|---|---|
| **Node / TS scripts** (V2) | chunked loops with a checkpoint key and a sleep; `.insert(` / `.upsert(` helpers; raw `INSERT … ON CONFLICT … DO UPDATE`; a mapper spread and overridden | DVT `data-validation validate column \| row` | pgloader `.load` files; Debezium connector YAML | flag YAML with `requires:`; a release-train YAML; runbooks | [V] port-pair |
| **Laravel** (V1 writers) | `chunkById`, `upsert(`, `insertOrIgnore(`; `$casts`, mutators (`Attribute::make(set:)`) the backfill must reproduce | — | `config/app.php` timezone (naive `DATETIME` wall clock) | — | [V] port-pair |
| **Rails / Django / Spring / Go** | `find_in_batches` + `upsert_all`; `bulk_create(ignore_conflicts=…)`; Spring Batch readers and writers; hand-written loops | the same tools | the same loaders | LaunchDarkly, Unleash, OpenFeature flags in code | [K?] |
| **DVT 8.10.0** | — | row hash applies RTRIM; `-cim` adds UPPER(); wildcard aggregates skip string length and timestamps unless `--wildcard-include-string-len` / `--wildcard-include-timestamp`; timestamps aggregate as unix seconds; `--comparison-fields` compares exact values | — | — | [R] |
| **pt-table-checksum 3.7.1** | — | MySQL → MySQL replicas only; needs `--trim` and `--float-precision` | — | — | [R] |
| **AWS DMS validation** | — | stops after 10,000 failures; rows updated continuously cannot validate; a Postgres PK collation other than "C" fails against Oracle | full load + CDC | — | [R] |
| **pgloader 3.6.9** | — | — | defaults: `tinyint(1)` → boolean, zero dates → NULL with NOT NULL dropped, `datetime` → `timestamptz` read in the **session** zone; `reset sequences` on by default | — | [R] |

Vitess VDiff and reladiff 0.6.0 are reconcilers too. The archived `data-diff` is not recommended (2024-05-17).

## Tool lane and ledger

Static only, offline. Nothing connects to either database. The dynamic oracles are a kill-and-resume run, a seeded-drift reconcile, the first insert after load, a flip under load and a rollback rehearsal (V374–V382). They run against **scratch copies** and are requested in the output, never run against the stores the audit reads. The engine ledger on stderr comes first: a `blocked` I-SCHEMA or I-SCOPE lane turns §5–§8 to `blocked`, never `checked`.

## Pre-flight

Run as one script (bash 3.2-safe; shell state does not survive between tool calls). Set `V2` to the V2 root and `V1` to the V1 root; leave `V1` empty in solo mode. `MIG` holds `pair-map.tsv`, `ledger.md` and `v1-inventory/`. `RB` holds the runbooks (default `$MIG/../runbooks`). `LIVE=1` reads an uncommitted V1 in place (ceiling GO-UNVERIFIED). The script greps from **inside** V2, because rg globs also match the root path you pass. Here `scripts/`, `deploy/` and migrations are **in scope** on purpose. Every grep ends in `ck`: exit 2 is a blocked class, never zero hits.

```bash
PI="${PI:-.claude/skills/paired-inventory/scripts/pair-inventory.py}"; V2="${V2:-.}"; V1="${V1:-}"; MIG="${MIG:-$V2/ai/migration}"
abs() { (cd "$(dirname "$1")" 2>/dev/null && printf '%s/%s\n' "$(pwd)" "$(basename "$1")") || printf '%s\n' "$1"; }
PI=$(abs "$PI"); MIG=$(abs "$MIG"); RB="${RB:-$(dirname "$MIG")/runbooks}"; [ -n "$V1" ] && V1=$(abs "$V1"); cd "$V2" || exit 2
OUT="$(mktemp -d "${TMPDIR:-/tmp}/data-cutover.XXXXXX")"; export GIT_OPTIONAL_LOCKS=0; mkdir "$OUT/none"; : > "$OUT/stamp"
ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
if [ -n "$V1" ]; then SIDE=(--v1="$V1" ${LIVE:+--live-v1}); else SIDE=(--v1-inventory="$MIG/v1-inventory"); fi
python3 -I "$PI" "${SIDE[@]}" --v2=. --lanes=I-SCOPE,I-SCHEMA,I-CONF --pair-map="$MIG/pair-map.tsv" --ledger="$MIG/ledger.md" --out="$OUT/run" > "$OUT/candidates.tsv" 2> "$OUT/ledger.txt"; echo "pair-inventory exit $? — 0 ran clean · 1 candidates (not a failure) · 2/3/4 BLOCKED: read $OUT/ledger.txt (its last line prints the reason) before any row"
awk -F'\t' '$1=="CANDIDATE" && $2=="I-SCOPE" && $5=="soft_delete"' "$OUT/candidates.tsv"            # §7 rows: V1 soft-deletes, V2 does not
V1TZ=$(awk -F'\t' '$2=="timezone"{sub(/.*value=/, "", $3); print $3; exit}' "$OUT"/run/v1/I-CONF.tsv 2>/dev/null); echo "V1 timezone (I-CONF): ${V1TZ:-unread}"   # §6 compares every loader session zone with it
# The data path: backfill, sync, reconcile, loader, flag and plan files. scripts/, deploy/ and migrations/ are IN scope here.
X=(-g '!**/{node_modules,vendor,dist,build,coverage,.git}/**' -g '!**/{test,tests,spec,__tests__,__mocks__,fixtures,e2e}/**' -g '!**/*.{spec,test,e2e-spec,test-data,fixture,d}.*')
# Loader shapes anywhere; the words backfill / reconcile / cutover / checkpoint only in script, deploy and ops trees (an app
# use case named `reconcileAll`, a seed script and a schema snapshot are not the data path). Snapshots and seeds are out.
DX=(-g '!**/*snapshot*.json' -g '!**/.snapshot*' -g '!**/{seed,seeds,seeders}/**' -g '!**/seed*.{ts,js,py,sql}')
rg -l -i --pcre2 'dual[-_ ]?write|\bread_from\b|\bwrites?_owner\b|\bpgloader\b|LOAD DATABASE|data-validation\s+validate|pt-table-checksum|debezium' -g '*.{ts,js,mjs,py,rb,go,java,kt,php,sql,sh,yaml,yml,json,load,toml,conf}' "${X[@]}" "${DX[@]}" . > "$OUT/dp0.txt"; ck DP $?
rg -l -i --pcre2 'backfill|reconcil|\bcutover\b|\bcheckpoint' -g '**/{scripts,bin,deploy,ops,tools,etl,cdc,migration,migrations}/**/*.{ts,js,mjs,py,rb,go,sql,sh,yaml,yml,load,toml,conf}' "${X[@]}" "${DX[@]}" . >> "$OUT/dp0.txt"; ck DPw $?
rg --files -g '**/{backfill,backfills,reconcile,reconciliation,cutover,sync,etl,cdc,pgloader,dms}/**' -g '**/*{backfill,reconcil,cutover}*' "${X[@]}" "${DX[@]}" . >> "$OUT/dp0.txt"; sort -u "$OUT/dp0.txt" > "$OUT/dp.txt"; rg --files -g '*checkpoint*.json' "${X[@]}" . > "$OUT/cp.txt"
DPROOTS=(); while IFS= read -r f; do DPROOTS+=("$f"); done < "$OUT/dp.txt"; [ ${#DPROOTS[@]} -gt 0 ] || DPROOTS=("$OUT/none"); echo "data-path files: $(wc -l < "$OUT/dp.txt")"
RBS=("$OUT/none"); [ -d "$RB" ] && RBS=("$RB"); [ -d docs/runbooks ] && RBS+=(docs/runbooks)
# 1. Not resumable / not idempotent / not throttled: a null checkpoint or zero pause; a plain INSERT; a full-table fetch.
rg -n -H --pcre2 '\bcheckpoint\w*\s*[:=]\s*(?:null|None|nil|false|undefined)\b|\b(?:sleep|pause|throttle|delay)\w*\s*[:=]\s*(?:0|false)\b' "${DPROOTS[@]}"; ck DC1a $?
rg -n -H -U --pcre2 '\.(?:insert|bulkCreate|insertMany|insert_many|bulk_create|executemany)\(\s*[\x27"]?\w|\bINSERT\s+INTO\b(?![^`;]{0,400}\bON\s+(?:CONFLICT|DUPLICATE\s+KEY)\b)' -g '!**/*.{yaml,yml,json,load}' "${DPROOTS[@]}"; ck DC1b $?
rg -n -H -i --pcre2 '\bSELECT\s+\*\s+FROM\s+\W?\w+\W?\s*(?:[`\x27";)]|$)|\.(?:findAll|find)\(\s*(?:\{\s*\})?\s*\)' "${DPROOTS[@]}"; ck DC1c $?
# 2. Overwrites newer: an upsert with no version / updated_at guard.
rg -n -H -U --pcre2 'ON\s+CONFLICT\b[^;`]{0,200}DO\s+UPDATE\s+SET\b(?!\s*\$\{)(?![^;`]{0,600}\bWHERE\b)|ON\s+DUPLICATE\s+KEY\s+UPDATE\b|\.upsert\((?![^;\n]*\b(?:onlyIfOlder|ifOlder|version|updated_?[aA]t|where)\b)[^;\n]*\)\s*;' "${DPROOTS[@]}"; ck DC2 $?
# 3. Reconcile: every validator call, then the masking flags and count-only checks (precedent 15).
rg -n -H --pcre2 'data-validation\s+validate|pt-table-checksum\s+--?\w|\bvdiff\s+\w|reladiff\s+\w|EnableValidation' "${DPROOTS[@]}"; ck DC3a $?
rg -n -H --pcre2 '\s-cim\b|--case-insensitive-match|--hash\s+[\x27"]?\*|validate\s+column\b(?![^\n]*--(?:sum|min|max|avg|std))|--(?:sum|min|max)\s+[\x27"]?\*(?![^\n]*--wildcard-include)|pt-table-checksum\s+--?\w(?![^\n]*--float-precision)' "${DPROOTS[@]}"; ck DC3b $?
# 4. Two transforms for one row: a sync / dual-write path that spreads the mapper and then overrides a field.
rg -n -H --pcre2 '\{\s*\.\.\.\s*(?:\w+\.)?map[A-Z]\w*\([^)]*\)\s*,\s*\w+\s*:|\*\*\s*map_\w+\([^)]*\)\s*,\s*[\x27"]\w+[\x27"]\s*:' "${DPROOTS[@]}"; ck DC4 $?
rg -n -H --pcre2 '^\s*(?:export\s+)?(?:async\s+)?(?:function|def|const)\s+(map_?[A-Z]?\w+)\b' "${DPROOTS[@]}" | sed -E 's/.*(function|def|const)[[:space:]]+([A-Za-z_]+).*/\2/' | sort | uniq -d | sed 's/^/DC4b two definitions of mapper: /'
# 5. Ids: fresh ids at load (keep the V1 id as legacy_id?) and regenerated business numbers.
rg -n -H --pcre2 '\bid\s*:\s*(?:randomUUID|uuid\w*|ulid|nanoid|cuid\w*|uuid4)\(|\b(?:number|code|reference|ref|slug|external_?id)\s*:\s*[^,\n]*\b(?:format|generate|build|make|next)\w*\(' "${DPROOTS[@]}"; ck DC5 $?
# 6. Loader casts and session zones (pgloader, DMS); compare each zone with the V1 timezone above.
rg -n -H -i --pcre2 'type\s+tinyint\s+to\s+boolean(?![^\n]*when\s*\(\s*=\s*1\s+precision)|\btimezone\s+to\s+\x27[^\x27]+\x27|zero-dates-to-null|"rule-action"\s*:\s*"change-data-type"' -g '*.{load,json,yaml,yml,sql}' "${DPROOTS[@]}"; ck DC6 $?
# 7. Live-rows uniqueness: V1 rules or indexes over live rows only; V2 unique keys on a soft-deleted table.
rg -n -H --pcre2 'unique\([^\n]*whereNull\(\s*[\x27"]deleted_at|->unique\(\)->where|whereNull\(\s*[\x27"]deleted_at[\x27"]\s*\)\s*\]' -g '*.php' -g '!**/{vendor,node_modules,storage}/**' "${V1:-$OUT/none}"; ck DC7v1 $?
rg -l --pcre2 'SoftDeletable|@Filter\([^)]*deleted|@DeleteDateColumn|\bparanoid\b' -g '*.{ts,js}' "${X[@]}" . | while read -r f; do rg -n -H --pcre2 '@Unique\((?![^\n]*(?:deleted|where))|@Index\([^)\n]*unique:\s*true(?![^\n]*where)' "$f" | sed 's/^/DC7c /'; done
# 9. Explicit ids loaded with no sequence reset in the same file; a loader that turns its reset off.
rg -n -H -i --pcre2 'reset\s+no\s+sequences' "${DPROOTS[@]}"; ck DC9a $?
rg -l --pcre2 '^\s*id\s*:\s*row\.id\b|INSERT\s+INTO\s+\w+\s*\(\s*id\b' "${DPROOTS[@]}" | while read -r f; do case "$f" in *queries*|*-wire.*|*.mapper.*|*/web/*|*/frontend/*) continue;; esac; rg -q --pcre2 'INSERT\s+INTO|\.(?:insert|upsert|insertMany|nativeInsert)\(|\bCOPY\s+\w+' "$f" || continue   # a read projection (`id: row.id` in a mapper) loads nothing
  rg -q --pcre2 'resetSequence|setval\(|RESTART\s+WITH|reset\s+sequences' "$f" && continue; N=$(rg -n --pcre2 '\.(?:insert|upsert|exec)\(|INSERT\s+INTO' "$f" | tail -1 | cut -d: -f1); L=$(awk -v s="${N:-0}" 'NR>s && /^[[:space:]]*\}\)?;?[[:space:]]*$/ {f=1; next} f && NF {print NR; exit}' "$f"); echo "DC9b $f:${L:-$N}: explicit ids loaded (last write at :$N), no sequence reset in this file — it belongs after the load"; done
# 10. Flips: write-owner flags set with a bare set (no fence); ungated read flags are read in the flag table below.
rg -n -H --pcre2 '\.(?:set|update|enable|put)\(\s*[\x27"][\w.:-]*(?:write|writes|writer|owner|primary)\w*[\x27"]' "${DPROOTS[@]}"; ck DC10 $?
cat > "$OUT/dc.py" <<'PY'
import glob, json, os, re, sys
out, v1tz, rb = sys.argv[1], sys.argv[2], sys.argv[3:]
dp = [l.strip() for l in open(os.path.join(out, 'dp.txt')) if l.strip()]
txt = lambda p: open(p, errors='replace').read()
def rows(side, lane):
    p = os.path.join(out, 'run', side, lane + '.tsv')
    return {f[1]: f for f in (l.rstrip('\n').split('\t') for l in (open(p) if os.path.exists(p) else []) if l.startswith(lane + '\t'))}
v1, v2 = rows('v1', 'I-SCHEMA'), rows('v2', 'I-SCHEMA')
sd = {k.split(':', 1)[1] for k, f in rows('v2', 'I-SCOPE').items() if 'soft_delete=yes' in f[2]}
names = lambda t: {t, t + 's', t + 'es', re.sub(r'y$', 'ies', t)}
def sites(table, words):   # a handling line names the table within 5 lines of it, not merely somewhere in the file
    out = []
    for f in dp:
        if f.endswith('.json'): continue
        ls = txt(f).splitlines()
        for i, l in enumerate(ls, 1):
            if re.search(words, l, re.I) and not re.match(r'\s*(?:import|from|require|#|//|\*)', l) and \
               any(re.search(r'\b%s\b' % n, '\n'.join(ls[max(0, i - 6):i + 5])) for n in names(table)):
                out.append('%s:%d %s' % (f, i, l.strip()[:60]))
    return out
orph = ['%s:%d' % (f, i) for f in dp for i, l in enumerate(txt(f).splitlines(), 1) if re.search(r'[Oo]rphan\w*\(|LEFT\s+JOIN\b.*\bIS\s+NULL', l)]
for k in sorted(set(v2) - set(v1)):                                   # 7/8: constraints V2 enforces that V1 never did
    m = re.match(r'(fk|unique):(\w+)\(([^)]*)\)', k)
    if not m or 'legacy_id' in m.group(3): continue
    t, at = m.group(2), v2[k][3]
    if m.group(1) == 'fk':
        h = [s for s in sites(t, r'orphan|LEFT\s+JOIN|IS\s+NULL') if s.split(':')[0] in {o.split(':')[0] for o in orph}]
        print('DC8a %s (%s): V1 had no FK; orphan check on this table: %s · checks that exist: %s' % (k, at, '; '.join(h) or 'NONE', ', '.join(orph) or 'none'))
    else:
        h = sites(t, r'duplicat|HAVING\s+count|dedupe|uniqBy|DISTINCT\s+ON|DO\s+NOTHING|INSERT\s+IGNORE|drop_duplicates')
        print('DC8b %s (%s): V1 had no unique key; handling: %s' % (k, at, '; '.join(h) or 'NONE'))
        if t in sd and not re.search(r'where=\S', v2[k][2]): print('DC7b %s (%s): unique over ALL rows of a soft-deleted table; V1 checked live rows? (DC7v1)' % (k, at))
for f in dp:                                                          # 6: loader session zone vs the V1 zone
    for i, l in enumerate(txt(f).splitlines(), 1):
        m = re.search(r"\btimezone\s+to\s+'([^']+)'", l, re.I)
        if m and v1tz and m.group(1) != v1tz: print('DC6b %s:%d loader session zone %s, V1 wall clock %s: naive datetimes shift' % (f, i, m.group(1), v1tz))
loaded = {m for f in dp for m in re.findall(r"(?:table:\s*|\.(?:insert|upsert)\(\s*)['\"](\w+)['\"]|TABLE NAMES MATCHING\s+'(\w+)'", txt(f)) for m in m if m}
recon = {m for f in dp for m in re.findall(r'-tbls\s+\w+\.(\w+)=|table\.include\.list:\s*\w+\.(\w+)|COUNT\(\*\)[^\n]*FROM\s+(\w+)', txt(f)) for m in m if m}
print('DC3c loaded with no reconcile artifact naming the table: %s' % (', '.join(sorted(loaded - recon)) or 'none'))
for p in [f for f in dp if re.search(r'flag|cutover', f) and f.endswith(('.yaml', '.yml', '.json'))]:   # 10: flags and their gates
    blocks = []
    for i, l in enumerate(txt(p).splitlines(), 1):
        m = re.match(r'^\s{2}([\w.-]+):\s*$', l)
        if m: blocks.append([m.group(1), i, []])
        elif blocks: blocks[-1][2].append((i, l))
    for name, ln, body in blocks:
        if not re.search(r'read|write|owner', name): continue
        req = [b for b in body if re.search(r'requires|^\s*-\s', b[1])]
        joined = ' '.join(b[1] for b in req)
        miss = [w for w in (['checkpoint', 'reconcil'] if 'read' in name else ['fence']) if w not in joined]
        at = next((i for i, b in req if 'requires' in b), ln)
        print('DC10 %s:%d %s requires [%s]%s' % (p, at, name, ', '.join(b[1].strip(' -') for b in req if 'requires' not in b[1]), ('  MISSING: ' + ', '.join(miss)) if miss else ''))
for p in [f for f in dp if f.endswith(('.yaml', '.yml'))]:            # 11: a drop step shipped with a write flip
    rel = {}
    for i, l in enumerate(txt(p).splitlines(), 1):
        m = re.search(r'step:\s*([\w-]+).*release:\s*"?([\w.]+)', l)
        if m: rel.setdefault(m.group(2), []).append((m.group(1), i))
    for r, steps in rel.items():
        for n, i in steps:
            if re.search(r'write', ' '.join(s for s, _ in steps)) and re.search(r'drop|delete|decommission|truncate', n): print('DC11b %s:%d %s ships in %s with a write flip' % (p, i, n, r))
for d in rb:                                                          # 11: rollback with no reverse path / point of no return
    for p in sorted(glob.glob(os.path.join(d, '**', '*.md'), recursive=True)):
        s = txt(p); low = s.lower()
        ln = next((i for i, l in enumerate(s.splitlines(), 1) if re.search(r'roll ?back', l, re.I)), 0)
        if ln: print('DC11a %s:%d rollback · reverse path %s · point of no return %s' % (p, ln, 'yes' if re.search(r'reverse|replay\w* into v1|bidirectional', low) else 'NO', 'yes' if 'point of no return' in low else 'NO'))
for p in [l.strip() for l in open(os.path.join(out, 'cp.txt')) if l.strip()]:   # 12: mapping version at the checkpoint vs now
    try: c = json.loads(txt(p))
    except ValueError: continue
    key = os.path.basename(p).split('.')[0]
    src = [f for f in dp if re.search(r'checkpoint_?[Kk]ey\s*[:=]\s*[\'"]%s[\'"]' % re.escape(key), txt(f))]
    now = [int(n) for f in src for t in re.findall(r'MAPPING_VERSION\s*=\s*(\d+)|mapping_?[Vv]ersion\s*[:=]\s*(\d+)', txt(f)) for n in t if n]
    cur = max(now) if now else 1
    if c.get('last_id') and c.get('mapping_version', 1) != cur:
        print('DC12 %s:1 checkpoint at mapping v%s, last_id %s, started %s; %s is at v%s: resumes without a re-backfill?' % (p, c.get('mapping_version'), c['last_id'], c.get('started_at'), ', '.join(src), cur))
PY
python3 -I "$OUT/dc.py" "$OUT" "$V1TZ" "${RBS[@]}"
for R in "$V1" .; do [ -n "$R" ] && find "$R" -newer "$OUT/stamp" -type f -not -path '*/node_modules/*' | head -3; done; echo "write check done (empty = nothing written)"
```

The labelled lines (`DC8a`, `DC10`, …) are the joins the script computed; plain `file:line` lines are grep hits to read. `pair-inventory exit 4` means a lane is blocked: read the ledger first.

## Measured

Measured 2026-10-18 on this repo's fixtures, and 2026-10-19 on one real Supabase → Nest port (read-only).

- **A real Supabase → Nest port** (2026-10-19). Before: 287 data-path files (any file naming `reconcile`, `backfill` or `checkpoint`: app use cases, a seed script, the schema snapshot), 182 of 184 `DC8b` rows citing a "handling" line that never named the table, and 7 `DC9b` rows on read projections (`id: row.id` in query mappers). After: loader shapes anywhere, the weak words only in script / deploy / ops trees, snapshots and seeds out → 136 files; a handling line must name the table within 5 lines → 16 of 184; `DC9b` needs a write in the file → 0. `port-pair` unchanged (32 data-path files, was 34; every DC line identical).

- **`port-pair`, paired** (V1 read in place with `LIVE=1`; the fixture root committed in a scratch copy, `change/` overlaid). Engine: 0 rg exit-2, 0 unparsed, write check 0, calibration 0 rows. It found 26 data-path files, then 34 once path names were added: `preflight.ts` mentions no data-path word and was missed by content alone. Grep lines: DC1a 1 · DC1b 3 · DC2 3 · DC3a 5 · DC3b 2 · DC4 2 · DC5 2 · DC6 5 · DC7v1 1 · DC9a 1 · DC10 1. Joins: DC6b 1 · DC7b 1 · DC7c 1 · DC8a 1 · DC8b 2 · DC9b 1 · DC10 5 flags (1 MISSING) · DC11a 2 runbooks · DC11b 1 · DC12 2 · DC3c none. Every one of the 24 DC seeds sits on a printed line or within two lines of one (DM-7a: the I-SCOPE row cites the class line, the seed its decorator). The decoys stay quiet as findings: the append-only ledger load, the declared CDC lag, the tickets soft-delete filter with its ADR, the gated orders read flag and the orders runbook. The first measurement also printed two unseeded lines (the invoices backfill upsert with no version guard beside the invoice sync, DC2; three loaded tables no reconcile named, DC3c); the fixture's clean pair was fixed instead (guarded upserts, reconcile checks added), so DC2 now prints the two seeds plus `stock` (no concurrent writer, refuted at read) and DC3c prints none. On the clean pair DC2 prints `stock` only. Report each one or refute it with a reason.
- **`port-pair`, solo** (V2 + `ai/` only, the inventory re-recorded at the pin). The same joins appear. The order soft-delete row is tagged `solo` (DM-7 is a guarantee class: Finding). The V1 timezone comes from the recorded I-CONF row, and DC7v1 reads nothing (no V1 tree).
- **Noise fixes.** DC1b first matched the target library's own `INSERT … ON CONFLICT`, because a quote inside the template string stopped the look-ahead; the look-ahead now stops only at a backtick or `;`. DC2 skips `DO UPDATE SET ${set}` (a helper whose guard is a variable). DC3 ignored a `pt-table-checksum` mention in a comment; the tool must be followed by a flag. The DC12 checkpoint search first used a recursive glob that stalled on a large tree; it now uses `rg --files`.
- **V2-only fixtures** (no V1): `ds-defects` DC1b 1 · DC2 3 · DC9b 1 (CDC consumers' upserts, distributed-systems' class, refuted here with that reason); `node-api` DC1b 1 (an audit-log insert, not a data path); the other 19 fixtures print 0 lines.

## The 3,000-row path

A large data path is almost always one runner and one target library used by every table.

1. **Read the shared pieces first.** The chunk runner (checkpoint, throttle, version check), the target's `insert` / `upsert` (conflict key, guard), the reconcile script and the loader files. A defect there is **one finding with N tables** (precedents § 27).
2. **Group per table** by the joins: `DC8a`, `DC8b`, `DC7b`, `DC9b`, `DC12`, then the per-call grep lines. A table whose call differs from its siblings (`checkpointKey: null` where the others pass a key, `insert` where they `upsert`) is the candidate; the siblings are the control.
3. **Read in this order:** money tables (wallets, invoices, ledgers), §10–§11 flips and reverse paths, §3 reconcile masks, §2 overwrite guards, then the rest.
4. **Close a group with one checked reason** (`7 lookup tables loaded once: append-only, counts + sums verified (verifyX)`). A money table, a flip or a reconcile row is never bulk-closed by name.
5. **Ledger the rest** as `Live, unreviewed (k tables)` with the command that continues; never `checked`.

## Scans for

| § | Class | Grep / join | Finding when | Default severity | Solo | Oracle |
|---|---|---|---|---|---|---|
| 1 | DM-1 not resumable / idempotent / throttled | DC1a, DC1b, DC1c | a real backfill restarts from 0, duplicates on a re-run, or runs unthrottled against a live replica | high | Finding (V2 code) | V374 |
| 2 | DM-2 overwrites newer rows | DC2 | a live writer (sync, CDC, V2 itself) updates the table during the backfill, and the upsert has no version / `updated_at` guard | high; **blocker** on money | Finding | V374 |
| 3 | DM-3 no or masking reconcile | DC3a, DC3b, DC3c | a loaded table has no cross-store check, or its check masks a drift class the table has (case, trailing space, money only counted) | high | Finding | V375 |
| 4 | DM-4 two transforms | DC4, DC4b | the backfill and the live path produce different values for one source row | high | Finding | V376 |
| 5 | DM-5 id mapping lost | DC5 | a V1 id or business number that leaves the system (link, provider, document) does not resolve on V2 | high | Unconfirmed-solo unless the recorded V1 route is fresh | V377 |
| 6 | DM-6 load cast drift | DC6, DC6b | a loader cast or session zone changes a value a V1 column holds | high | Finding when `I-SCHEMA` / `I-CONF` is fresh | V375 |
| 7 | DM-7 soft-delete lost | I-SCOPE `soft_delete` CHANGED · DC7b, DC7c, DC7v1 | soft-deleted V1 rows are loaded and V2 reads, counts, exports or unique checks include them where V1 did not | high; medium for a unique-check-only change | **Finding** (guarantee class) | V378 |
| 8 | DM-8 orphans / duplicates | DC8a, DC8b | V2 adds an FK or a unique key V1 never had, and the load drops or rejects rows with no counted, per-class decision | high; medium when the count is known and small | Finding when `I-SCHEMA` is fresh | V379 |
| 9 | DM-9 sequence not reset | DC9a, DC9b | rows loaded with explicit ids and nothing moves the sequence past `max(id)` | high (an outage at the first V2 insert) | Finding | V380 |
| 10 | DM-11 flip not gated / not fenced | DC10 (flag table), DC10 (bare set) | a read flag that does not require checkpoint-complete **and** reconcile-green; a write flip with no pause / revoke / version fence | high; **blocker** when the flag already reads `v2` | Finding | V381 |
| 11 | DM-12 no reverse path / point of no return | DC11a, DC11b | a write flip with no replay of V2 writes into V1, or V1 objects dropped in the release that flips writes | high; **blocker** for money | Finding | V382 |
| 12 | DM-13 mapping changed mid-window | DC12 | the checkpoint's mapping version is older than the code's, `last_id > 0`, and nothing re-backfills from 0 | medium; high when the changed field is money or an id | Finding | V376 |

Severity rises one step when the table's read flag already serves V2 (the defect is live), and falls one step for a table nothing reads yet. A static fact with both ends cited (a missing checkpoint key, `reset no sequences`, an ungated flag) passes gate 6. A behaviour row (overwrite, cast drift, two mappers) needs its oracle on a scratch copy (precedents § 5).

### 1. Backfill not resumable, idempotent or throttled (DM-1)

```
BAD:   runChunked(source, { table: 'tickets', checkpointKey: null, batch: 5000, sleepMs: 0 }, rows => target.insert('tickets', rows.map(mapTicket)))
GOOD:  runChunked(source, { table: 'tickets', checkpointKey: 'tickets', batch: 1000, sleepMs: 200 }, rows => target.upsert('tickets', rows.map(mapTicket), ['legacy_id']))
```
**Read the code.** What does the runner do when the key is null: does it start from 0 on every run? Does the batch write upsert on a key the source row carries (the V1 id), or does it insert rows with fresh ids, so that a restart duplicates them? What happens between the batch write and the checkpoint write? Is there a pause or lag check (pt-table-checksum's shape: `--max-lag`, adaptive chunks)? A full-table `SELECT *` with no key range dies at scale. **Finding when** a crash or a second run duplicates or skips rows, or the run is unthrottled against the replica V1 reads. **Proof:** V374, kill at 50% and resume, then run twice.

### 2. Backfill overwrites newer rows (DM-2)

```
BAD:   ON CONFLICT (legacy_id) DO UPDATE SET balance_minor = EXCLUDED.balance_minor, …, updated_at = EXCLUDED.updated_at
GOOD:  … DO UPDATE SET … WHERE wallets.updated_at < EXCLUDED.updated_at      ·   target.upsert(t, rows, ['legacy_id'], { onlyIfOlder: 'updated_at' })
```
**Read the code.** Who else writes this V2 table during the backfill: a sync, CDC, or V2 itself after a write flip? The backfill reads a snapshot, so a row updated after its batch was read is older than what the live path wrote. Does the mapped row carry `updated_at` (or a version), so a guard can compare? A table with no concurrent writer cannot be overwritten: refute it with the writer search written out. **Finding when** a live writer and an unguarded upsert meet on one table. **Proof:** V374, a live update between the snapshot read and the batch write.

### 3. No reconcile, or one that masks the class (DM-3)

```
BAD:   data-validation validate column -tbls norrow.invoices=public.invoices --count '*'        (money never compared)
       data-validation validate row -tbls norrow.users=public.users -pk email --hash '*' -cim     (UPPER + RTRIM mask case and spaces)
GOOD:  … --count '*' --sum subtotal_amount,tax_amount,total_amount --min total_amount --max total_amount
       … -pk email --comparison-fields email,name
```
**Read the code.** Which tables does the load touch (DC3c), and which check names each one? For each check, which drift classes does the table have — e-mail case (a lower-casing mutator), trailing spaces (V1 trimmed), money, zones — and does the tool's option mask them (precedent 15)? Is a sample stated with its rate and confidence (precedent 14)? Is a CDC lag declared with a matching window (precedent 13; that is the control)? **Finding when** a loaded table has no check, or its check cannot see a drift class it has. **Proof:** V375, seed one row per class into scratch copies and run the reconciler **as configured**; each unreported class is masked.

### 4. Backfill transform differs from the live transform (DM-4)

```
BAD:   const doc = { ...invoiceToDoc(row), issued_at: row.issued_at };    (the sync overrides the mapper's zone conversion)
GOOD:  const doc = invoiceToDoc(row);
```
**Read the code.** Do the backfill and the sync, CDC sink or dual write call the **same** mapper? If one spreads the mapper and overrides a field, what does the override lose: a zone conversion, lower-casing, an enum map? Two mappers with one name (DC4b) are two transforms. **Finding when** one source row yields two different V2 rows depending on the path. **Proof:** V376, the same row through both paths compared structurally.

### 5. Id mapping lost (DM-5)

```
BAD:   id: randomUUID(),                    (no legacy_id: every e-mailed /tickets/123 link 404s)
       number: buildInvoiceNo(row.id, row.issued_at)         (the legal number printed on issued invoices changes)
GOOD:  id: randomUUID(), legacy_id: row.id,   ·   number: row.number
```
**Read the code.** Where do V1 ids and business numbers leave the system: V1 routes with `{ticket}` (read the V1 route file), e-mails, PDFs, a payment provider, partner files? Does V2 resolve the old form (a unique `legacy_id` and a lookup; an ADR that keeps old links)? Is a business number regenerated from the row id rather than copied? **Finding when** an id or number a client already holds no longer resolves, or changes. **Proof:** V377, every old id form through V2.

### 6. Load cast and zone drift (DM-6)

```
BAD:   CAST type tinyint to boolean using tinyint-to-boolean,        (tax_category 1–3 collapses to true/false)
       SET PostgreSQL PARAMETERS timezone to 'UTC'                    (V1 wrote naive Asia/Riyadh wall clock)
GOOD:  CAST type tinyint when (= 1 precision) to boolean …   ·   timezone to 'Asia/Riyadh'
```
**Read the code.** For each cast rule, which V1 columns match it (I-SCHEMA type and values)? A default or custom cast is a finding on every column it touches unless the V2 schema says the change is intended (precedent 16). For `datetime → timestamptz`, which zone did V1 write in (`DC6b` compares the loader session zone with the I-CONF timezone)? Are zero dates on NOT NULL columns turned into NULL? **Finding when** a loaded value differs from the V1 value. **Proof:** V375, seed `tinyint` 2, a zone-naive timestamp and a zero date.

### 7. Soft-delete semantics lost (DM-7)

```
BAD:   V1 Order uses SoftDeletes; V2 Order has deletedAt and no live-rows filter → deleted orders return in lists, counts, exports
       V1 Rule::unique('stock_items','sku')->whereNull('deleted_at'); V2 @Unique({ properties: ['account', 'sku'] }) on all rows
GOOD:  @scoped.SoftDeletable() on Order   ·   a partial unique index … where deleted_at is null
```
**Read the code.** Does the backfill load soft-deleted rows, or filter them at the source with a reason (ADR-0010 shape; that is the control)? For each V1 `SoftDeletes` model, which V2 read paths reach the table: an ORM filter (on by default?), raw SQL, exports, counts? For unique keys, did V1 check only live rows (DC7v1), and is the V2 index partial (`DC7b` from the schema, `DC7c` on the entity)? **Finding when** a soft-deleted V1 row is visible, counted or blocks a re-create on V2. **Proof:** V378, a list, count, export and unique check with soft-deleted rows present.

### 8. Orphans and duplicates V1 tolerated (DM-8)

```
BAD:   preflight checks orphans on invoice_lines, ticket_messages, wallet_transactions — not order_lines, the one V1 left without an FK
       const rows = checks.uniqBy(batch, r => r.email.toLowerCase());        (the second account's user silently disappears)
GOOD:  requireNoOrphans(source, 'order_lines', 'order_id', 'orders')   ·   failOnDuplicates(batch, …, 'users.email')
```
**Read the code.** Which constraints does V2 add that V1 never enforced (`DC8a`, `DC8b` from the two schema rows)? For each one, is there a counted pre-load check with a decision per class: repair, map, drop with a record? Or does the load drop rows silently (`uniqBy`, `ON CONFLICT DO NOTHING` on a natural key, `INSERT IGNORE`, an `INSERT … SELECT` that inserts nothing for an orphan)? `DO NOTHING` on the row's own V1 id is idempotence, not a drop. **Finding when** V1 rows that violate the new constraint are lost or rejected with no count and no decision. **Proof:** V379, orphans per FK and duplicates per natural key (also under `lower()`), counted before the load.

### 9. Sequence or identity not reset (DM-9)

```
BAD:   rows loaded with id: row.id, no resetSequence      ·   pgloader WITH … reset no sequences
GOOD:  await target.resetSequence('invoices', 'id')       ·   WITH … reset sequences
```
**Read the code.** Which tables keep V1 ids (`DC9b`)? Does anything (`setval`, `ALTER … RESTART WITH`, the loader's default reset) move the sequence past `max(id)` after the load **and** after the tail replay? A UUID key has no sequence: refute it. **Finding when** the first V2 insert into a loaded table collides. **Proof:** V380, the first insert per table after the load.

### 10. Read flip not gated; write flip not fenced (DM-11)

```
BAD:   invoices.read_from: { value: v2, requires: [] }        ·   await flags.set('orders.writes_owner', 'v2')
GOOD:  requires: [backfill.invoices.checkpoint_complete, reconcile.invoices.green]   ·   flags.setFenced(…, { pauseV1Pool, revokeGrants })
```
**Read the code.** For each read flag, does its gate require **both** checkpoint-complete and reconcile-green, and does a check actually produce that signal (§3)? For each write flip, is there a fence: version-token fencing (Stripe), a pool pause plus a grant revoke with drain (Figma), or a maintenance window? Does the runbook's fence match the script that runs? **Finding when** a read flag can open without both signals, or V1 can still commit after V2 owns the rows. **Proof:** V381, a flip under a write generator, lost = 0 and duplicated = 0.

### 11. No reverse path; no point of no return (DM-12)

```
BAD:   "5. Rollback: flip wallets.read_from and wallets.writes_owner back to v1."     (V2's writes are lost)
       - { step: drop-v1-order-tables, release: "2.4.0", after: orders-writes-flip }
GOOD:  reverse-sync replays every V2 write into V1 until the point of no return, a named step signed by owners after the soak
```
**Read the code.** After the write flip, how do V2's writes reach V1 for a rollback: reverse replication, a reverse audit log, a replay script? Which step switches it off, and is that the named point of no return, signed and after a soak? Does any release drop, rename or truncate V1 objects together with the write flip (`DC11b`)? **Finding when** a rollback after the flip would lose V2 writes, or the way back is removed in the flip's own release. **Proof:** V382, a rollback after N V2 writes (a new enum value, a new required column).

### 12. Mapping changed mid-window (DM-13)

```
BAD:   orders.checkpoint.json { "last_id": 48211, "mapping_version": 2 }  while ORDERS_MAPPING_VERSION = 3
GOOD:  the checkpoint reset to 0 under v3 (or the runner refuses to resume across versions)
```
**Read the code.** Does the runner compare the stored mapping version with the code's before resuming? Which field changed (read the mapper comment or the diff), and are rows `1…last_id` re-mapped by anything, such as a targeted re-backfill or a migration? **Finding when** rows before the checkpoint keep the old mapping and rows after get the new one. **Proof:** V376 across the version change.

## Output

```
data-cutover-orchestrate — paired · laravel 11.31.0 → nest 11.0.6 · mysql → postgres · snapshot=live · data-path files 34

Readiness: orders BLOCK (§12 re-backfill, §10 write fence) · invoices BLOCK (§10 ungated read, §3 count-only) ·
           wallets BLOCK (§11 no reverse path, §2 guard) · tickets BLOCK (§1, §5) · stock BLOCK (§12)
Findings: 24 (4 shown) · Unconfirmed: 1

1. v2/deploy/flags/read-switch.yaml:28                             [report-with-fix]  blocker
   §10 invoices.read_from = v2 with requires: [] — no checkpoint, no reconcile; the only invoices check is count-only
   (scripts/reconcile/compare-counts.sh:14). V1 still owns invoice writes (v1/routes/api.php:30). Proof: V381.
   Fix: requires backfill.invoices.checkpoint_complete + reconcile.invoices.green.
2. v2/scripts/backfill/wallet-balances.ts:20                        [report-with-fix]  blocker
   §2 ON CONFLICT … DO UPDATE SET balance_minor … with no WHERE guard; CDC applies V1 balances during the run
   (deploy/cdc/wallet-stream.yaml:5). Money. Proof: V374 live update between read and write. Fix: WHERE wallets.updated_at < EXCLUDED.updated_at.
3. ai/runbooks/cutover-wallets.md:10                                [report-with-fix]  blocker
   §11 rollback = flip back; no reverse path, no point of no return; the orders runbook has both (cutover-orders.md:12,16).
4. v2/deploy/pgloader/journal.load:9                                [report-flagged]   high
   §6 session zone UTC; V1 writes naive Asia/Riyadh (v1/config/app.php:11). Unproven link: no seeded-drift run.
   Settling probe: V375 with one posted_at row on a scratch copy.

Verification: 31 candidates → 24 findings · 1 unconfirmed · 2 hardening · 0 pre-existing · 4 refuted
Oracles requested (scratch copies only): V374 tickets, users, orders, wallets · V375 users, invoices, ledger · V380 invoices, wallet_transactions

Class coverage:
  §1  not resumable          checked (DC1a 1, DC1b 3 → 2)
  §2  overwrites newer       checked (DC2 3 → 2; stock: no concurrent writer)
  §3  reconcile masks        checked (DC3a 5, DC3b 2 → 2; DC3c none)
  …
  §12 mapping mid-window     checked (DC12 2 → 2)
```

`[report-with-fix]`: both ends cited, the writer or reader search written out, and a local fix. `[report-flagged]`: one link unproven; the row names it and the probe that settles it. Every run prints **all twelve** §s, each as `checked (k candidates → m)`, `N/A (<reason>)` (no data path, a single store), `blocked (<lane or grep>: <reason>)`, `→ <owner> (k)`, or `Unconfirmed-solo (k)`.

**Readiness verdict per feature** (the contract `@parity-auditor` and the read-flip gate consult):
- `BLOCK <feature> (§n …)` is the default.
- `CLEAR-UNVERIFIED` means no finding, but a V-number oracle has not run, or the run is solo or `snapshot=live`.
- `CLEAR` needs the checkpoint artifact (cursor past `max(id)`) **and** the reconcile result, both cited, plus every §'s oracle run on a scratch copy.

The closure verbs are `BLOCK cutover`, `CLEAR cutover`, `RE-BACKFILL <range>` (§12, §2), `RECONCILE` (§3 missing or masked) and `FENCE` (§10). Each verb names the artifact that clears it. The runbook draft (source of truth, checkpoint, reconcile query and result, gate status, reverse path, point of no return) is written to the run folder (`$OUT/cutover-<feature>.md`). The caller (`/port-feature`, `/migration-phase`) moves it into `ai/runbooks/` as its own ledger write.

## Precedents

The verifier reads [`precedents/migration.md`](../../../../snippets/precedents/migration.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- § 1 the counterpart search, § 3 ADR plus `changes_baseline`, § 5 a parity claim needs execution;
- § 12 an append-only dataset needs counts, not a dual write; § 13 a declared lag; § 14 sampling;
- § 15 a masking reconciler; § 16 loader casts; § 18 the point of no return; § 21 solo mode; § 27 one wiring row.

The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Migration, V374–V382.

## When to run

- On every whole-repo `/compare-v1`, printing all twelve §s.
- Before any read flip or write flip, and before the point-of-no-return step: the readiness verdict for that feature.
- On a diff that touches a backfill, a sync or CDC config, a reconcile script, a loader file, a cutover flag, a release plan or a runbook; and when a mapper's version constant changes.

## Halt conditions

- Do not report a high or blocker row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/compare-v1` that verifier is `@parity-auditor` in refute mode, plus `@verifier` on every BLOCKER and HIGH. Run standalone, apply the protocol as a separate second pass and tag those rows `self-verified`. Keep the rest Unconfirmed, Hardening or Refuted; never drop them.
- **No `CLEAR` without the reconciler's seeded-drift self-check** (V375): a reconciler nobody has seen fail proves nothing (precedent 15). No `CLEAR` without the checkpoint artifact and the reconcile result, both cited.
- **Solo mode never prints `CLEAR` or GO.** Solo mode means a recorded V1 inventory and no V1 tree.
  - §1–§4 and §9–§12 read V2 code and run in full.
  - §7 is a guarantee class and may become a Finding from the recorded I-SCOPE row.
  - §5, §6 and §8 need a fresh recorded row (`I-SCHEMA`, `I-CONF`, a route); with a stale one they are `Unconfirmed-solo`, with "re-run with `--v1=<path>`" as the settling probe (precedents § 21, § 24).
- Do not read a row from a `blocked` lane: calibration, rg exit 2, `schema-map` NOT-RUN, or an extractor that changed. Its §s print `blocked`.
- Halt on any finding that lacks the V2 line, the V1 fact or the V-number.
- **Never write into either tree, and never connect to either store.** The audit does not run a backfill, a reconcile, a loader or a flag change. Every oracle runs on scratch copies and is requested, not performed, here. The runbook draft goes to the run folder.
- One store → hand off to database `migration-safety`; do not double-own an in-table backfill.

## Related

- `paired-inventory` (this pack): the engine. `surface-parity-scan`, `semantics-parity-scan`, `side-effect-parity-scan`, `cutover-routing-scan` and `parity-proof-scan` are the sibling detectors.
- `/compare-v1` runs this skill and folds its coverage into the 48-class ledger. `@parity-auditor` judges the rows and reads the readiness verdict. `/find-and-fix --from-audit` closes each row failing-first from its V-number.
- `parity-test-generate` (this pack) compares outputs; this skill moves and reconciles the stores.
- When their packs are installed: database `migration-safety` and `index-coverage-scan/scripts/schema-map.py`; distributed-systems `dual-write-scan`.
