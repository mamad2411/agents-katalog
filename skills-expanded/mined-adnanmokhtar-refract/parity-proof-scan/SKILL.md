---
name: parity-proof-scan
description: "Was parity proven: V1-pinned tests kept, V1 branches reached, gated suites run, comparator blind spots."
kind: skill
pack: migration
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: parity-proof-scan

## Premise

"Parity is green" is a claim about evidence: a suite pinned to V1, a corpus that reaches V1's branches, a comparator that can see a difference, run in CI where V1 is present. Each part can be emptied without a red build:
- a port PR skips the one V1 case it would fail, or re-records the golden to V2's answer;
- the corpus never takes V1's credit-line branch;
- the parity job never sets `V1_REPO_PATH`, so `describeV1` skips every suite and the job passes;
- the tolerance file ignores `total`.

The agent evidence is direct. Dropping MigrationBench's test-integrity checks raised the reported success from 71.67% to 97.67%. FreshBrew found line-coverage drops above 5 points were consistently reward hacking, and many hacks fell under 5. LLM judges told false success from real success at no better than 0.65 AUROC (research notes A, B4/B5; arXiv 2505.09569 v3, 2510.04852, 2606.09863).

This skill owns the proof classes **PP-1, PP-2, PP-3 and CO-4** (PF §1–§3, §5). It consumes **PP-5** (§4), which the testing pack owns. It grades the **evidence**, never the code under test: a defect the parity suite should have caught belongs to the detector of its class.

**Every finding cites the test, golden, corpus, contract, CI step or tolerance line, the V1 fact it weakens (the pinned case, the V1 branch, the V1 behaviour), and the oracle that proves it.** A parity claim that rests on a NOT-RUN suite is never PASS (precedent 25). "Parity is proven" is never printed without the class-coverage block (§ Output).

## The rule

A candidate becomes a finding only when all four hold:

1. **The evidence backs a claim.** The test, golden, corpus or tolerance is cited by a ledger row (`parity_tests:`), `test-map.tsv`, a contract, or the CI job that gates the merge.
2. **It is V1-pinned or V1-derived.** It was recorded from V1 at the pin, drives V1 (`describeV1`, `V1_REPO_PATH`), or names a V1 entry (`v1_entry`, `recorded_from`).
3. **The weakening is real.** For a diff it comes from the port PR itself (§1). For a corpus, the V1 branch exists in the pinned V1 (§2). For a comparator, the hidden field is not V1-vs-V1 noise (§5).
4. **No record makes it intentional.** A case changed in its **own** earlier PR with an ADR and `changes_baseline`, or a test moved 1:1 with a `test-map.tsv` row, is the control (precedents § 3, § 20).

## Boundaries

- **PP-5, the V1-gated suite skipped,** → testing `suite-execution-scan` §2 (2c), when the testing pack is installed. That skill writes `gated-suites.tsv` (`GATES_TSV`), owns the class and grades it. Here §4 reads the TSV, works out per CI **job** whether the job that runs each gated suite sets the variable, and marks every dependent parity claim `NOT-RUN`. Without the testing pack, §4 runs its own helper grep and reports the row tagged `testing-class (owner pack testing not installed)`.
- Generic test weakening outside the V1-pinned set (`new-skip`, `fewer-assertions` on V2-only tests) → the testing pack and the repo-baseline `test-integrity.py` gate. §1 reads the same script and keeps the rows on the pinned set.
- Mutation testing of the corpus (V1 mutants) → testing `mutation-probe`, when installed; without it §2 stays at branch reach.
- The behaviour the hidden field carries (a wrong `total`) → the class detector (`semantics-parity-scan`, backend `wire-format-scan`). §5 reports only that the comparator cannot see it.

## Lanes

| Stack | Skips and edits (§1) | Goldens re-recorded (§1) | Branch reach (§2) | Gated suites and CI (§4) | Comparator (§5) | Tag |
|---|---|---|---|---|---|---|
| **Vitest / Jest (V2)** | `it.skip`, `xit`, `describe.skip`, `test.todo`, `.only`; config `exclude`, `testPathIgnorePatterns`, `--passWithNoTests` | `-u`, `--update-snapshots`, `__snapshots__/`, `__golden__/` with `recorded_from` | — | `HAS_V1 ? describe : describe.skip`, `describe.skipIf(` | `behavior-diff.py` tolerance keys | [V] port-pair |
| **PHPUnit / Pest (V1)** | `markTestSkipped(`, `markTestIncomplete(` | approval files | Xdebug or pcov branch coverage on the pinned V1 [K?: not measured here] | — | — | [V] V1 side read |
| **pytest** | `pytest.mark.skip(if)`, `xfail` non-strict, `-k "not …"`, `--deselect` | `--snapshot-update`, syrupy / approvaltests | coverage.py `--branch` | `skipif(not os.environ…V1…)` | — | [K?] |
| **JUnit / Maven / Gradle** | `@Disabled`, `assumeTrue(getenv…)`, Surefire `<exclude>`, `-DskipTests` | — | JaCoCo 0.8.9 (FreshBrew's tool) | `@EnabledIfEnvironmentVariable` | — | [K?] |
| **Go / RSpec** | `t.Skip(`, build tags; `xit`, `pending` | `-update` flags | `go test -cover` | `os.Getenv` + `t.Skip` | — | [K?] |
| **CI** | a test step removed, `\|\| true`, `continue-on-error` | — | — | GitHub Actions job and step `env:`, GitLab `variables:`, CircleCI `environment:` | — | [V] port-pair (GitHub Actions) |

## Tool lane and ledger

Static, offline, with two read-only helpers.
- **`test-integrity.py`** (repo-baseline, installed at `.claude/scripts/`) reads the diff `BASE..worktree` and prints `new-skip`, `undeclared-baseline-rewrite`, `deleted-test-case`, `fewer-assertions` and `removed-ci-test-step`. Its exit codes are 0 (none), 1 (rows) and 2 (usage).
- **`git diff -U0`** gives every changed line of the pinned set.

Nothing is executed. Coverage, branch reach, the V1-gated run count and the comparator self-check come from **evidence** (`EVID=<dir>`: CI logs, JUnit XML, coverage summaries) or are requested. A summary written by an agent is not evidence (precedent 20).

## Pre-flight

Run as one script (bash 3.2-safe):
- `V2` is the V2 root inside a git work tree, and `BASE` is the port PR's base (default: the merge-base with `origin/HEAD`, `origin/main` or `main`).
- `V1` is the pinned V1 root, empty in solo mode. `MIG` holds `ledger.md`, `test-map.tsv` and the contracts.
- `TI` is `test-integrity.py`.
- `GATES_TSV` is the testing pack's `gated-suites.tsv`, when that pack ran.
- `EVID` is a directory of CI logs and coverage evidence.

Test trees **are** in scope here. Every grep ends in `ck`: exit 2 is a blocked class, never zero hits.

```bash
V2="${V2:-.}"; V1="${V1:-}"; MIG="${MIG:-$V2/ai/migration}"; TI="${TI:-$V2/.claude/scripts/test-integrity.py}"; EVID="${EVID:-}"
abs() { (cd "$(dirname "$1")" 2>/dev/null && printf '%s/%s\n' "$(pwd)" "$(basename "$1")") || printf '%s\n' "$1"; }
MIG=$(abs "$MIG"); TI=$(abs "$TI"); [ -n "$V1" ] && V1=$(abs "$V1"); [ -n "$EVID" ] && EVID=$(abs "$EVID"); [ -n "$GATES_TSV" ] && GATES_TSV=$(abs "$GATES_TSV"); cd "$V2" || exit 2
OUT="$(mktemp -d "${TMPDIR:-/tmp}/parity-proof.XXXXXX")"; export GIT_OPTIONAL_LOCKS=0; mkdir "$OUT/none"; : > "$OUT/stamp"
ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
TOP=$(git rev-parse --show-toplevel 2>/dev/null); BASE="${BASE:-$(git merge-base HEAD origin/HEAD 2>/dev/null || git merge-base HEAD origin/main 2>/dev/null || git merge-base HEAD main 2>/dev/null)}"
[ -n "$BASE" ] && [ "$(git rev-parse "$BASE" 2>/dev/null)" = "$(git rev-parse HEAD 2>/dev/null)" ] && BASEHEAD=1   # the merge-base of a checkout of main is HEAD
echo "git: ${TOP:-none} · base: ${BASE:-none (PF1 blocked: pass BASE=<ref>)}${BASEHEAD:+ (= HEAD)} · V1: ${V1:-none (solo)} · evidence: ${EVID:-none} · TI: $TI"
# Test trees ARE the subject here: no test/spec exclusion; dependencies and build output only.
X=(-g '!**/{node_modules,vendor,dist,build,coverage,.git}/**')
# 0. The V1-pinned set: test-map.tsv rows, files that drive V1 (describeV1, V1_REPO_PATH, "V1-pinned"), goldens recorded from V1.
rg -l --pcre2 '\bdescribeV1\b|\bV1_REPO_PATH\b|\bHAS_V1\b|V1-pinned|"recorded_from"\s*:' -g '*.{ts,tsx,js,mjs,py,rb,php,go,java,kt,json}' "${X[@]}" . > "$OUT/pinned.txt"; ck PF0 $?
: > "$OUT/mapped.txt"; [ -f "$MIG/test-map.tsv" ] && awk -F'\t' 'NR>1 && $3 != "-" {sub(/::.*/, "", $3); print $3}' "$MIG/test-map.tsv" | while read -r p; do [ -n "$TOP" ] && [ -f "$TOP/$p" ] && (cd "$TOP" && printf '%s\n' "$p"); done > "$OUT/mapped.txt"
echo "V1-pinned files: $(wc -l < "$OUT/pinned.txt") by marker, $(wc -l < "$OUT/mapped.txt" 2>/dev/null || echo 0) by test-map.tsv"
# 1. The port diff against the pinned set: test-integrity.py rows, every changed line, build-config skips, coverage evidence.
PRE=$(git rev-parse --show-prefix 2>/dev/null); { sed "s#^\./#$PRE#" "$OUT/pinned.txt"; cat "$OUT/mapped.txt" 2>/dev/null; } | sort -u > "$OUT/pinned.rel"
if [ -z "$TOP" ] || [ -z "$BASE" ]; then echo "PF1 blocked (no git base: pass BASE=<ref>)"
elif [ -n "$BASEHEAD" ]; then echo "PF1 N/A (BASE = HEAD: no port diff to read — pass BASE=<the port PR's base>)"
elif [ ! -f "$TI" ]; then echo "PF1 blocked (test-integrity.py not found at $TI: pass TI=<path>)"
elif [ ! -s "$OUT/pinned.rel" ]; then echo "PF1 N/A (no V1-pinned test or golden found)"
else
  python3 -I "$TI" --base="$BASE" --repo="$TOP" > "$OUT/ti.txt"; echo "test-integrity exit $? (0 none · 1 rows · 2 error); rows on the V1-pinned set:"
  rg -F -f "$OUT/pinned.rel" "$OUT/ti.txt"; ck PF1a $?
  (cd "$TOP" && git diff -U0 "$BASE" -- $(cat "$OUT/pinned.rel")) | awk '/^\+\+\+ /{f=substr($2,3)} /^@@/{split($3,a,/[+,]/); n=a[2]} /^\+[^+]/{print "PF1 " f ":" n ": " substr($0,1,110); n++}'
  (cd "$TOP" && git diff -U0 "$BASE" -- '*vitest.config*' '*jest.config*' '*playwright.config*' 'pom.xml' '*build.gradle*' 'pytest.ini' 'pyproject.toml' 'phpunit.xml*' '*package.json' '.github/workflows/*') | rg -n --pcre2 '^\+.*(?:exclude|testPathIgnore|--passWithNoTests|skipTests|maven\.test\.skip|-k\s+["\x27]not|--deselect|\|\|\s*true|continue-on-error)' -; ck PF1c $?
fi
for E in "$EVID" coverage; do [ -d "$E" ] && rg -n -H -i --pcre2 'line coverage|coverage[^\n]{0,40}(?:→|->|drop)|\b\d+\s+skipped\b|executed|new skip' "$E"; done
# 2. Corpus reach: each corpus that names its V1 entry, the V1 conditions in that function, and whether any case takes each branch.
rg --files -g '**/corpus/**/*.json' -g '*.corpus.json' "${X[@]}" . > "$OUT/corpus.txt"; ck PF2 $?
# 3. Recorded V1 bugs: contracts whose Known V1 bugs say none; V1 quirk shapes on those features; V2 shapes that "fix" them.
if [ -d "$MIG" ]; then rg -n -H -A2 --pcre2 '^#+\s*Known V1 bugs' -g '*.md' "$MIG"; ck PF3a $?; else echo "PF3 N/A (no $MIG: no contracts to read)"; fi
P3V1=none; [ -n "$V1" ] && { [ -f "$V1/composer.json" ] && P3V1=laravel; [ -d "$V1/supabase/migrations" ] && P3V1=supabase; }   # V1 quirk shapes by V1 stack, never 0 files silently
case "$P3V1" in
  laravel) rg -n -H --pcre2 'array_filter\((?![^;\n]*array_values)|[\x27"]like[\x27"]\s*,\s*[\x27"]%[\x27"]\s*\.\s*\$|\bjson_encode\(\s*\$\w+\s*\)(?![^;\n]*JSON_)|==\s*(?:null|0|[\x27"]{2})\b' -g '*.php' -g '!**/{vendor,tests,database,lang,docs}/**' "$V1"; ck PF3b $?;;
  supabase) rg -n -H -i --pcre2 '\bi?like\s+\x27%\x27\s*\|\||\.i?like\(\s*[\x27"][\w.]+[\x27"]\s*,\s*`%\$\{|\bnullif\(\s*\w+\s*,\s*\x27\x27\s*\)|\bjsonb?_strip_nulls\(' -g '*.{sql,ts}' -g '!**/{node_modules,tests,docs}/**' "$V1/supabase"; ck PF3b $?;;
  *) echo "PF3b N/A (V1 stack $P3V1: reads Laravel PHP or Supabase SQL and edge functions; a Rails, Django or Spring V1 prints N/A)";;
esac
rg -n -H --pcre2 '\bescape_?[Ll]ike\b|replace\(\s*/\[[^\]]*%[^\]]*\]/' -g '*.{ts,js}' -g '!**/{node_modules,test,tests,__tests__}/**' .; ck PF3c $?
# 4. V1-gated suites (testing suite-execution-scan §2c gated-suites.tsv when that pack ran; else the built-in helper grep).
if [ -n "$GATES_TSV" ] && [ -f "$GATES_TSV" ]; then awk -F'\t' '$1=="v1"' "$GATES_TSV" > "$OUT/gates.tsv"; echo "gates from $GATES_TSV: $(wc -l < "$OUT/gates.tsv") v1 rows"
else rg -n -H --pcre2 '(?:const|let|var)\s+(\w+)\s*(?::[^=\n]+)?=\s*[^;\n?]*V1[^;\n?]*\?\s*(?:describe|it|test)\s*:\s*(?:describe|it|test)\.skip\b|\b(?:describe|it|test)\.skipIf\([^)\n]*V1|skipif\([^)\n]*V1' -g '*.{ts,tsx,js,mjs,py}' "${X[@]}" . > "$OUT/gates.txt"; ck PF4 $?; cat "$OUT/gates.txt"; fi
rg --files -g '.github/workflows/*.y*ml' -g '.gitlab-ci*.yml' -g '.circleci/*.yml' -g 'azure-pipelines*.yml' -g 'bitbucket-pipelines.yml' --hidden . > "$OUT/ci.txt"; ck PF4ci $?
# 5. Comparator: tolerance files and comparator code (both-raise, status-only); committed loosening since the base.
rg --files -g '*tolerance*.{json,yaml,yml}' "${X[@]}" . > "$OUT/tol.txt"; ck PF5 $?
rg --files -g 'package.json' "${X[@]}" . > "$OUT/pkg.txt"; ck PF4pkg $?
rg -n -H --pcre2 'control[- ]vs[- ]control|calibrat\w*|primary\W+secondary|v1\W+vs\W+v1' -i -g '*.{ts,js,py,json,md}' "${X[@]}" . > "$OUT/cal.txt"; ck PF5cal $?; head -5 "$OUT/cal.txt"; [ -s "$OUT/cal.txt" ] || echo "PF5 no control-vs-control (V1-vs-V1) run found: every ignore key is uncalibrated"
[ -n "$BASE" ] && [ -s "$OUT/tol.txt" ] && git log --format='%h %s' "$BASE"..HEAD -- $(sed 's#^\./##' "$OUT/tol.txt") | sed 's/^/PF5 committed tolerance change: /'
cat > "$OUT/pf.py" <<'PY'
import json, os, re, sys
out, v1, gtsv = sys.argv[1], sys.argv[2], sys.argv[3]
rd = lambda p: open(p, errors='replace').read() if p and os.path.exists(p) else ''
ls = lambda f: [l.strip() for l in rd(os.path.join(out, f)).splitlines() if l.strip()]
floor = (re.findall(r'(?i)v1_?[Bb]ranch_?[Ff]loor\W+([\d.]+)', ' '.join(rd(p) for p in ls('corpus.txt') + [os.path.join(os.path.dirname(os.path.dirname(c)), 'parity.config.ts') for c in ls('corpus.txt')])) or ['undeclared'])[0]
snake = lambda n: re.sub(r'(?<!^)([A-Z])', r'_\1', n).lower()
for c in ls('corpus.txt'):                                         # 2. V1 branches the corpus never takes
    try: d = json.loads(rd(c))
    except ValueError: continue
    ent, cases = d.get('v1_entry', ''), d.get('cases', [])
    ln = next((i for i, l in enumerate(rd(c).splitlines(), 1) if '"cases"' in l), 1)
    if '::' not in ent: print('PF2 %s:%d %d cases, no v1_entry: V1 branch reach unknown (floor %s)' % (c, ln, len(cases), floor)); continue
    if not v1: print('PF2 %s:%d %s: V1 tree absent — Unconfirmed-solo' % (c, ln, ent)); continue
    f, fn = ent.split('::'); src = rd(os.path.join(v1, f))
    m = re.search(r'function\s+%s\s*\([^)]*\)[^{]*\{' % re.escape(fn), src)
    if not m: print('PF2 %s:%d %s: function not found in V1' % (c, ln, ent)); continue
    body, depth, i = '', 1, m.end()
    while depth and i < len(src): depth += {'{': 1, '}': -1}.get(src[i], 0); body += src[i]; i += 1
    for var, op, num in re.findall(r'if\s*\(\s*\$(\w+)\s*(<=|>=|<|>|===|==|!==|!=)\s*(-?\d+(?:\.\d+)?)\s*\)', body):
        key = next((k for k in (cases[0] if cases else {}) if k in (var, snake(var))), None)
        if key is None: print('PF2 %s:%d %s if ($%s %s %s): no corpus field maps to $%s' % (c, ln, ent, var, op, num, var)); continue
        test = lambda x: eval('%r %s %s' % (float(x), {'===': '==', '!==': '!='}.get(op, op), num))
        vals = [k[key] for k in cases if isinstance(k.get(key), (int, float))]
        t, fl = sum(map(test, vals)), len(vals) - sum(map(test, vals))
        miss = [b for b, n in (('true', t), ('false', fl)) if not n]
        print('PF2 %s:%d %s if ($%s %s %s): %d cases take true, %d false%s · floor %s' % (c, ln, ent, var, op, num, t, fl, ('  ← branch never reached: ' + ', '.join(miss)) if miss else '', floor))
gates = []                                                       # 4. which CI job runs each gated suite, and does it set the variable
if gtsv:
    for l in ls('gates.tsv'):
        f = l.split('\t'); env = [e for e in f[4].split(',') if e != '-']
        env = env or sorted(set(re.findall(r'process\.env\.(\w*V1\w*)', rd(f[1].rsplit(':', 1)[0])))) or ['V1_REPO_PATH']
        gates.append((f[1], f[2], sorted(set(env)), f[7].split(',')))
else:
    for l in ls('gates.txt'):
        m = re.match(r'(.+?):(\d+):(.*)', l); hm = re.search(r'(?:const|let|var)\s+(\w+)', m.group(3))
        src = rd(m.group(1)); env = sorted(set(re.findall(r'process\.env\.(\w*V1\w*)|environ(?:\.get)?\(?\[?\s*[\'"](\w*V1\w*)', src)) - {''}) or ['V1_REPO_PATH']
        env = sorted({e for t in env for e in (t if isinstance(t, tuple) else (t,)) if e})
        h = hm.group(1) if hm else 'inline'
        users = [u for u in ls('pinned.txt') if h != 'inline' and re.search(r'\b%s\b' % h, rd(u)) and u != m.group(1)]
        gates.append(('%s:%s' % (m.group(1), m.group(2)), h, env, users))
pk = {}
for p in ls('pkg.txt'):
    try: [pk.setdefault(k, []).append((os.path.dirname(p), v)) for k, v in json.loads(rd(p)).get('scripts', {}).items()]
    except ValueError: pass
for ci in ls('ci.txt'):
    s = rd(ci).splitlines(); jobs = []
    for i, l in enumerate(s, 1):
        m = re.match(r'^  ([\w-]+):\s*$', l)
        if m and any(re.match(r'^jobs:', x) for x in s[:i]): jobs.append([m.group(1), i, []])
        elif jobs: jobs[-1][2].append((i, l))
    for at, h, env, users in gates:
        dirs = sorted({os.path.dirname(u) for u in users}) or [os.path.dirname(at.split(':')[0])]
        for name, ln, body in jobs:
            runs = [(i, l.split('run:', 1)[1].strip()) for i, l in body if 'run:' in l]
            hit = []
            for i, cmd in runs:
                for tok in re.findall(r'[\w:.-]+', cmd):
                    paths = [os.path.normpath(os.path.join(b, x)) for b, sc in pk.get(tok, []) for x in re.findall(r'[\w.-]*/[\w./-]+', sc)] + re.findall(r'[\w.-]+/[\w./-]+', cmd)
                    if any(os.path.normpath(d).startswith(os.path.normpath(x)) for d in dirs for x in paths if x): hit.append(i)
            if not hit: continue
            sets = [e for e in env if any(re.search(r'\b%s\s*[:=]' % e, l) for _, l in body)]
            state = 'RUN (%s set by the job)' % ','.join(sets) if sets else 'NOT-RUN'
            print('PF4 %s:%d job %s runs the suite gated at %s (%s, %d specs) at %s:%d — %s%s' % (ci, ln, name, at, h, len(users), ci, hit[0], state, '' if sets else ': %s never set in this job; every parity claim on these specs is NOT-RUN' % '/'.join(env)))
        for name, ln, body in jobs:
            if any(re.search(r'\b%s\s*:' % e, l) for e in env for _, l in body): print('PF4 %s:%d job %s sets %s (for the suites it runs)' % (ci, ln, name, '/'.join(env)))
NOISE = r'(?i)(?:request_?id|trace_?id|correlation|_at$|timestamp|date|etag|nonce|host)$'
for t in ls('tol.txt'):                                          # 5. tolerance keys: what each one hides
    s = rd(t); lines = s.splitlines()
    at = lambda x: next((i for i, l in enumerate(lines, 1) if x in l), 1)
    try: d = json.loads(s)
    except ValueError: d = None
    if not isinstance(d, dict): print('PF5 %s: not JSON — read its ignore / structural / compare keys by hand' % t); continue
    flat = lambda v: [x for k in (v.values() if isinstance(v, dict) else v if isinstance(v, list) else [v]) for x in (flat(k) if isinstance(k, (dict, list)) else [k])]
    for path in flat(d.get('ignore', [])):
        leaf = re.split(r'[.\[\]]+', str(path).strip('$.'))[-1]
        print('PF5 %s:%d ignore %s — %s' % (t, at('"%s"' % path), path, 'noise only if a V1-vs-V1 run shows it (precedent 10)' if re.search(NOISE, leaf) else 'a business field: no calibration can make it noise'))
    for path in flat(d.get('structural', [])): print('PF5 %s:%d structural %s — presence (null vs absent vs []) is hidden (precedent 8)' % (t, at('"%s"' % path), path))
    for k, v in (d.get('compare') or {}).items():
        if str(v).lower() in ('status', 'status-only', 'code'): print('PF5 %s:%d %s compares %s only — body, presence and values are never compared' % (t, at('"%s"' % k), k, v))
PY
python3 -I "$OUT/pf.py" "$OUT" "$V1" "${GATES_TSV:+1}"
for R in "$V1" .; do [ -n "$R" ] && find "$R" -newer "$OUT/stamp" -type f -not -path '*/node_modules/*' | head -3; done; echo "write check done (empty = nothing written)"
```

`PF1` lines are changed lines of the pinned set. `PF2` lines are per-branch counts over the corpus. `PF4` lines are the per-job verdict. `PF5` lines are each tolerance key and what it hides. Plain lines are raw hits to read.

## Measured

Measured 2026-10-18 on this repo's fixtures, and 2026-10-19 on one real Supabase → Nest port (read-only).

- **A real Supabase → Nest port** (2026-10-19, V2 checked out at its main branch). Before: `BASE` resolved to HEAD and PF1 ran test-integrity over an empty diff, `mapped.txt` was never created (a `wc` error), the default `TI` resolved against the caller's directory, and PF3b read `*.php` (0 lines). After: `PF1 N/A (BASE = HEAD …)`, `TI` defaults under `$V2`, PF3b reads the Supabase SQL and edge functions (222 lines), docs excluded. `port-pair` unchanged.

- **`port-pair`, paired.** The fixture root was committed in a scratch git repository and `change/` laid over it as the uncommitted port PR (`BASE=HEAD`, `EVID=.refract-fixture/runtime`).
  - The V1-pinned set is 7 files by marker and 3 by `test-map.tsv`.
  - `test-integrity.py` exit 1, with 2 rows on the pinned set (`new-skip`, `undeclared-baseline-rewrite`). PF1 changed lines: 2. The script cites the golden at line 1; the diff gives line 4.
  - PF2: 4 corpora, 2 with `v1_entry`, each with a V1 branch never reached (`$quantity < 0`, `$minutesLeft < 0`; floor 0.8).
  - PF3: 3 contracts, 2 with "none recorded"; V1 quirk lines 2; V2 "fix" lines 3.
  - PF4: one gate (`describeV1`, 4 specs). Job `parity` runs it at `ci.yml:60` → **NOT-RUN**; job `contract` sets the variable for its own suite.
  - PF5: 3 ignore keys (1 business field) and 1 status-only compare, with no calibration run found.
  - All 8 PF seeds sit on a `PF*` line and PP-5 is printed NOT-RUN with the suite named. The decoys stay quiet: the 1:1 moved wallet test is not in the diff; the orders contract has a recorded KB-1 with its ADR; the `contract` job prints as setting the variable, with no finding.
- **`port-pair`, solo** (V2 + `ai/` committed, no PR overlay). The two `v1_entry` corpora print `V1 tree absent — Unconfirmed-solo`; PF4 and PF5 are identical.
- **`GATES_TSV`.** The testing pack's 2c script on the same V2 wrote one `v1` row with env `-`: it resolves one constant hop, and here `HAS_V1 = Boolean(V1_REPO_PATH)` is two. §4 then reads the variable from the helper file, and the verdict is unchanged.
- **Noise fixes.**
  - PF1 first diffed the whole work tree when the pinned set was empty (a pathspec of nothing is everything): measured on a fixture inside this repository. It now prints `N/A` instead.
  - PF5 first read every `$.path` in a tolerance file as an ignore key: 7 rows on `regression-baseline`, whose keys are all `exact`. It now reads only `ignore`, non-empty `structural` and `compare` (0 rows).
  - PF3c dropped `Object.values(` (3 fixtures, unrelated).
- **V2-only fixtures** (no git base, no V1): 0 lines on all 21.

## The 3,000-row path

A large proof surface is almost always one harness, one config and one CI job.

1. **§4 first.** If the job that runs the pinned suites never sets the variable, every parity claim is NOT-RUN. Report that once, then still grade §1, §2 and §5: they decide what the suite proves once it runs.
2. **§1 on the diff only.** Group `test-integrity.py` rows and `PF1` lines by file. One re-recorded golden directory is one finding with N cases.
3. **§5 per tolerance file.** Group the ignore keys by leaf name: one `$..total` hides every money body.
4. **§2 per corpus,** then **§3 per contract** (read the contract's paths against the other detectors' rows).
5. **Close a group with one checked reason** (`12 snapshot files added, none existed at base: new, not rewritten`). A pinned test or a money key is never bulk-closed.

## Scans for

| § | Class | Grep / join | Finding when | Default severity | Solo | Oracle |
|---|---|---|---|---|---|---|
| 1 | PP-1 tests modified / skipped / re-recorded | test-integrity rows on the pinned set · PF1 · PF1c · coverage evidence | the port diff edits, skips or re-records a V1-pinned test or golden, changes the build config to skip it, or line coverage drops > 5 points | **critical** for a pinned skip or a re-recorded golden; high for a coverage drop alone | Finding (V2 diff) | V386 |
| 2 | PP-2 corpus misses V1 branches | PF2 | V1 branch reach under the corpus is below the declared floor, or a V1 branch on a contract path is never taken | high on money or state paths; medium else | Unconfirmed-solo | V387 |
| 3 | PP-3 V1 bug fixed or ported unrecorded | PF3a–c + the other detectors' rows | V2 differs from V1 on a contract path, "Known V1 bugs" is empty and no ADR + `changes_baseline` covers it | medium; high when a client depends on the V1 shape | Unconfirmed-solo | V362 / V358 + ledger |
| 4 | PP-5 V1-gated suite skipped (→ testing) | GATES_TSV or the helper grep · PF4 | the CI job that runs a gated suite never sets the variable, or evidence shows 0 executed | high → testing; every dependent parity claim NOT-RUN | Finding (V2 CI) | V388 |
| 5 | CO-4 comparator blind spots | PF5, PF5cal, the committed-change log | an ignore key on a business field; an uncalibrated noise key; status-only comparison; `structural` hiding presence; both-raise counted as a match; a loosening committed without an ADR | high when the hidden field is money, status or an id; medium else | Finding | V385 |

### 1. Tests modified, skipped or goldens re-recorded (PP-1)

```
BAD:   - it('matches V1 credit amounts for negative halves', …)  + it.skip('matches V1 credit amounts …', …)      (in the port PR)
       __golden__/invoice-sums.json    "tax": "13.08" → "13.09"   (recorded_from: v1/tests/Feature/InvoiceSumsTest.php)
GOOD:  the case unchanged and the rounding fixed   ·   a separate earlier PR with an ADR and changes_baseline, if V1 was wrong
```
**Read the code.** Is the file in the pinned set (a `test-map.tsv` row, `describeV1`, `recorded_from`, an ADR such as "V1-pinned tests are immutable")? Did this diff introduce the skip, the edit or the new golden value, or did an earlier PR with an ADR and `changes_baseline` do it first? Was the golden re-recorded to V2's output (compare the new value with the V1 test's assertion)? Did a config change exclude the file? Does the coverage evidence show a drop above 5 points, or fewer executed tests (MigrationBench r4: the executed count must not fall)? A test moved 1:1 with a mapping row is the control. **Finding when** the port PR weakens the evidence it is judged by. **Proof:** V386, the pinned set from the base run unmodified against the PR's V2, with no new skips and a coverage drop of at most 5 points.

### 2. Corpus does not reach V1 branches (PP-2)

```
BAD:   pricing.corpus.json  8 cases, quantity 1…12 — V1 lineNet has `if ($quantity < 0)` (credit lines: no discount re-applied)
GOOD:  cases with quantity -1 and -3 (and a discount), so the credit branch runs on both sides
```
**Read the code.** Which V1 function does the corpus drive (`v1_entry`, or the route for an HTTP corpus)? Which conditions does it hold (PF2 reads numeric comparisons; read the rest: string matches, `null` checks, enum switches)? Does any case take each side? What floor does the config declare (`v1BranchFloor`), and does the floor count V1 branches or only inputs (halt 2's 30 inputs is a count, not reach)? An HTTP corpus with no `v1_entry` has unknown reach: request V1 coverage. **Finding when** a V1 branch on a contract path is never taken, or measured reach is below the floor. **Proof:** V387, V1 branch coverage under the corpus (Xdebug or pcov on the pinned snapshot), with the unreached branches and a witness input for each.

### 3. A V1 bug fixed, or ported, with no record (PP-3)

```
BAD:   V1 Invoice::toApi  'lines' => array_filter($lines, …)   (keys kept: a zero-quantity line makes `lines` an object)
       V2 returns a list.   Contract "Known V1 bugs: none recorded", no ADR, no changes_baseline.
GOOD:  contract KB-1 + ADR-NNN + changes_baseline: invoices.lines-shape   (the orders contract's KB-1 is the shape)
```
**Read the code.** On each contract path, where does V2 behave differently from V1 (this skill's PF3b/PF3c quirk lines, and the rows other detectors refuted as "V2 is better")? Is the difference a fix (`escapeLike`, a list instead of an object) or a faithful port of a bug? Either way, is it recorded: a contract entry, an ADR and the ledger's `changes_baseline`? Does a client depend on the V1 shape (a mobile decoder, a partner)? **Finding when** V2 differs on a contract path and nothing records it. **Proof:** V362 (or V358) shows the difference, and the ledger and contract show no record.

### 4. V1-gated parity suite skipped in CI (PP-5 → testing)

```
BAD:   export const describeV1 = HAS_V1 ? describe : describe.skip;    job `parity`: checks V1 out, runs test:parity, never sets V1_REPO_PATH
GOOD:  - run: pnpm --filter @norrow/api test:parity   env: { V1_REPO_PATH: ${{ github.workspace }}/v1-snapshot }
```
**Read the code.** Which helper gates the suites, and which variable does it read (follow `HAS_V1 = Boolean(V1_REPO_PATH)` through every hop)? Which CI job runs those spec files? Map the step's script (`test:parity` → `vitest run test/parity`) to the paths. Does **that** job set the variable, at job or step level? A job that sets it for another suite is the decoy, and textual "CI sets it somewhere" is not enough. Does the run evidence show k > 0 executed? **Finding when** no job that runs the gated suite sets the variable, or the evidence shows 0 executed. The row is graded by testing when that pack is installed; here it is printed as `PP-5 NOT-RUN <suite> (<helper>, <job>:<line>)` and every parity claim on those specs is NOT-RUN. **Proof:** V388, the CI log of the job backing the claim shows k > 0 V1-gated tests executed.

### 5. Comparator blind spots (CO-4)

```
BAD:   "ignore": ["$..request_id", "$..total", "$..updated_at"]     ·   "compare": { "tickets": "status" }
GOOD:  "$..total" removed; request_id / updated_at kept only after a V1-vs-V1 run shows they differ; "tickets": "status+body"
```
**Read the code.** For each ignore key: is it a field two V1 runs disagree on (timestamps, generated ids, host names: precedent 10), and is there a calibration run? A business field (money, status, ids, counts) is never noise. Which endpoints compare status only, and what does the body carry there (presence, enum values, scoping)? Does `structural` hide `null` vs absent vs `[]` (precedent 8)? Does the comparator count both sides raising as a match? Was any key added in a commit after the base without an ADR (the PF5 commit log; uncommitted changes are §1's)? **Finding when** a difference a client observes cannot be reported by the comparator as configured. **Proof:** V385, one seeded mismatch per tolerance key through `behavior-diff.py` (or the project's comparator); each one not reported is a blind spot.

## Output

```
parity-proof-scan — paired · base 185b7e5..worktree · V1 pinned 61cb5c9 · gates from testing (1 v1 row) · evidence .refract-fixture/runtime

Parity claims: NOT-RUN — 4 specs under apps/api/test/parity (describeV1) never execute in CI job `parity`
Findings: 8 (3 shown) · routed → testing: 1

1. change: v2/apps/api/test/parity/credit-notes.parity.spec.ts:26    [report-with-fix]  critical
   §1 the port PR turns the V1-pinned case "matches V1 credit amounts for negative halves" into it.skip
   (test-map.tsv invoice-credits; ADR-0003). Evidence: 7 → 6 executed. Proof: V386. Fix: revert the skip, fix creditFor.
2. v2/.github/workflows/ci.yml:60                                    [report-with-fix]  high → testing
   §4 PP-5 NOT-RUN: job parity (ci.yml:38) runs test:parity → apps/api/test/parity, gated by describeV1
   (test/parity/support/v1.ts:8), and never sets V1_REPO_PATH. Evidence: 0 passed, 7 skipped. Proof: V388.
3. v2/apps/api/test/parity/ignore-paths.json:4                       [report-with-fix]  high
   §5 ignore $..total hides every money field in orders, invoices and wallets bodies; no V1-vs-V1 run exists.
   Proof: V385 seeded total mismatch not reported. Fix: remove the key.

Verification: 11 candidates → 8 findings · 0 unconfirmed · 2 hardening · 0 pre-existing · 0 refuted (+1 routed)

Class coverage:
  §1  pinned tests kept     checked (2 test-integrity rows, 2 PF1 lines → 2)
  §2  V1 branch reach       checked (4 corpora: 2 with v1_entry → 2; 2 HTTP corpora reach unknown)
  §3  V1 bugs recorded      checked (2 contracts "none recorded", 2 quirks → 2)
  §4  gated suites ran      → testing (1) · parity claims NOT-RUN
  §5  comparator            checked (3 ignore keys, 1 status-only → 2; 2 uncalibrated noise keys → hardening)
```

`[report-with-fix]`: the evidence line, the V1 fact and the oracle are cited. `[report-flagged]`: one link unproven (no CI log, no coverage run), with the probe that settles it. Every run prints **all five** §s, each as `checked (k candidates → m)`, `N/A (<reason>)`, `blocked (<reason>)`, `→ testing (k)`, or `Unconfirmed-solo (k)`. When any parity claim is NOT-RUN, it prints the `Parity claims: NOT-RUN` line first, naming the gated suite.

## Precedents

The verifier reads [`precedents/migration.md`](../../../../snippets/precedents/migration.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4:
- § 3: an intentional break needs an ADR plus `changes_baseline`;
- § 5: a parity claim needs execution;
- § 8: presence;
- § 10: noise is only what two V1 runs disagree on;
- § 20: a port PR that modifies, skips or re-records V1-pinned tests is Refuted as evidence; FreshBrew's 5 points;
- § 21: solo mode;
- § 25: a skipped V1-gated suite is NOT-RUN.

The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Migration: V362, V385, V386, V387 and V388.

## When to run

- On every whole-repo `/compare-v1`, printing all five §s.
- On every port PR (`/find-and-fix`, `/port-feature`, `/migrate`) before it claims parity: §1 on its diff, and §4 on the CI it will merge through.
- When a tolerance file, a corpus, a parity harness or a CI test job changes.

## Halt conditions

- Do not report a high or critical row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/compare-v1` that verifier is `@parity-auditor` in refute mode, plus `@verifier` on every BLOCKER and HIGH. Run standalone, apply the protocol as a separate second pass and tag those rows `self-verified`. Never drop them.
- **Any NOT-RUN parity claim caps the verdict at GO-UNVERIFIED** (precedent 25). A summary from an agent ("the parity suite passed") is never the evidence: the CI log, JUnit XML or the runner's own summary is.
- **Solo mode never prints GO.** §1, §4 and §5 read V2 and its CI and run in full. §2 and §3 need the V1 tree: without it they are `Unconfirmed-solo`, and the settling probe is "re-run with `--v1=<path>`" (precedent 21).
- No git base means §1 is `blocked (no base)`, never `checked`. A test-integrity exit 2 means §1 is `blocked`.
- Halt on any finding without the evidence line, the V1 fact and the V-number.
- **Never write into either tree.** No test is edited, re-recorded or un-skipped here. No CI is triggered and nothing is executed. Oracles are requested.

## Related

- `parity-test-generate` (this pack) builds the corpus, the goldens and the tolerance file this skill grades. The other detectors in this pack supply the rows §3 reads.
- `/compare-v1` runs this skill, and its production bar *PARITY WAS RUN* needs §1 and §4 at 0. `@parity-auditor` judges, and `/find-and-fix --from-audit` refuses fix diffs that touch pinned tests (its reward-hack grep).
- Testing `suite-execution-scan` (§2c, `gated-suites.tsv`) and `mutation-probe`, when the testing pack is installed. The repo-baseline `test-integrity.py` and `behavior-diff.py` are the mechanisms.
