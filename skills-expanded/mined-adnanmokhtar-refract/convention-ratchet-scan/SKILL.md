---
name: convention-ratchet-scan
description: Convention-rule suppressions, ratchet growth, per-package lint drift and half-done declared migrations (AL-29–32).
kind: skill
pack: align
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: convention-ratchet-scan

## Premise

A convention that a lint rule enforces stays aligned only while three things hold: nobody silences the rule without a reason, the baseline of known violations only shrinks, and every package actually runs the rule. A fourth thing decides whether "aligned" is even reachable: when the project has declared a move from shape A to shape B, the old shape must keep shrinking. Each of these fails silently. CI stays green, the rule looks installed, and the convention erodes one disable, one rebaseline, one package config at a time.

This skill owns the four align classes about the **machinery** of a declared convention:

- **§ 1 AL-29** a suppression that dodges a declared **convention** rule (naming, layout, wrapper or import bans, tokens, design-system rules) with no reason, a reason that does not resolve, or a copy-pasted one;
- **§ 2 AL-30** a ratchet regression: a baseline file grew, or a convention rule was loosened, since the base;
- **§ 3 AL-31** per-package config drift: a package where the shared convention silently does not apply;
- **§ 4 AL-32** a half-finished declared migration: the oracle names the new shape and the old one survives, or grows.

**A tool that cannot run is `NOT RUN`, never zero.** A baseline with no base to compare against, a rule set the static parse could not resolve, a lint step CI never runs: each is a `blocked` or `NOT RUN` line in the coverage block, never a clean class ([`precedents/align.md`](../../../../snippets/precedents/align.md) § 20).

**Every finding cites the directive, baseline or config line `<file:line>` + the convention rule it concerns, with its oracle row from `oracle-map.py` + the count before and after (or the reason and whether it resolves) + the fix.** A grep hit is never a finding by itself, and "ratchets hold" is never printed without the class-coverage block (§ Output).

## The rule

A candidate is a finding when all four hold:

1. **The rule is a convention rule** the project declares at T1 or T2: one the `CONV` list in the pre-flight matches (`no-restricted-imports`, `boundaries/*`, `check-file/*`, `unicorn/filename-case`, `naming-convention`, `declaration-strict-value`, `tailwindcss/no-arbitrary-value`, `i18next/no-literal-string`, Ruff `TID251` and `N8xx`, depcruise `forbidden`, design-system plugin rules), or a `no-restricted-syntax` selector whose configured `message` names a wrapper, token or naming rule. Correctness rules (`eqeqeq`, `no-floating-promises`, `no-explicit-any`) and security rules are not: their suppressions belong to code-quality `suppression-scan` and security `sast-scan` § 10.
2. **No documented exception covers it** (§ 3): a reason citing an ADR that exists, a ticket matching the tracker's key pattern, a design-system exception prefix, an `allow` / `ignore_imports` / known-violation entry that did not grow.
3. **The comparison is real.** AL-30 and the dated part of AL-32 need a base: `git merge-base` with the default branch, an explicit `BASE`, or a `BASE_DIR` copy. With none, the row is `blocked (no base)`, never "no growth". A base that IS `HEAD` (a scan of the default branch itself, where the merge-base is HEAD) compares every count with itself: `AL-30: NOT RUN (BASE == HEAD)`.
4. **The convention is live for the site**: the scope is not frozen by an ADR whose date has not passed (§ 16), not a context split (§ 17), not generated code.

## Boundaries

- **Suppressions of correctness and project-local correctness rules**, blanket disables over files with no convention rule, and correctness rules turned off → code-quality `suppression-scan` §1–§3 (always installed). The two scans dedupe by `<file:line>`; a blanket disable over a file a convention rule covers is listed by both.
- **Suppressions of security rules** (`security/*`, `nosemgrep`, `# nosec`, Ruff `S`) → security `sast-scan` § 10 (always installed).
- **A convention rule that sits at `warn`, or whose whole scope no CI job lints** → `convention-oracle` § 3 (AL-03). A package left out **while its siblings are linted** (`ci=partial`), a package config that drops the shared one, or a rule `off` in one package is AL-31 here.
- **The violations the suppressions hide**, once revealed, are the site detectors' rows: `wrapper-adoption-scan` (AL-11/13/14/15/22), `naming-layout-scan` (AL-16–19), ui-ux `design-token-audit` (AL-05–10/12, when the ui-ux pack is installed; without it `N/A (owner pack ui-ux not installed)`).
- **Accrual of suppression debt over time** (counts per run, owner, delete-by date) → code-quality `debt-ledger`.
- **A V1→V2 port** of a framework or library → `/migrate`; **a version bump** → `/upgrade-dep`. AL-32 is the same-version convergence on a shape the project already declares.
- **A sweep that resolves one pattern two ways, or edits outside its hits** (AL-33/AL-34) → `align-sweep-gate.py` under `find-and-align`, on the sweep, not the tree.

## Adapt to the codebase — the ratchet lanes

Versions come from `$RUN/oracle/versions.tsv` and `gates.tsv`, never from memory. Tool facts are from the align research catalog (2026-10-18) unless dated otherwise.

| Lane | Inline suppression (§ 1) | Baseline / ratchet file (§ 2) | Per-package config (§ 3) | Version traps |
|---|---|---|---|---|
| **JS / TS** — React, Vue, Svelte, Angular, Node | `// eslint-disable-next-line <rule> -- reason`, `/* eslint-disable */`; `biome-ignore <rule>: reason`; `// ast-grep-ignore` | a project's own ratchets: `*-baseline.json`, `*ratchet*.json` (every numeric leaf), and ceilings kept IN a test (`const CEILING = 130`, `'domain -> domain': 40` maps; `specs.tsv` ratchet rows and the test files a doc's ratchet table lists); ESLint bulk suppressions `eslint-suppressions.json` `{file: {rule: {count}}}` (core since 9.24.0; `error` rules only; an unpruned entry fails the run unless `--pass-on-unpruned-suppressions`; read in ESLint's source 2026-10-18); `eslint.seatbelt.tsv` (file, rule, max count); `@rushstack/eslint-bulk` `.eslint-bulk-suppressions.json`; `.dependency-cruiser-known-violations.json` | `eslint.config.*` per package; a spread of the shared config; `ignores`; `files` globs | **ESLint 10.0.0 (2026-02-06) removed eslintrc**: an `.eslintrc*` beside a flat config is dead config. **boundaries v6** renamed `element-types` → `dependencies`; **v7** renamed `no-unknown` / `no-ignored` → `*-dependencies` and the option `rules` → `policies`, so old disable comments become unused-directive errors. **unicorn ≥ 65** `filename-case` also checks directories. A count jump right after either bump is a rebaseline, not new drift |
| **CSS** | `/* stylelint-disable <rule> -- reason */` | none built in: a shrink-only counter (`rg -c` per rule per file, stored in the run) | `.stylelintrc*` per package; `ignoreFiles` | `reportDescriptionlessDisables`, `reportNeedlessDisables` exist but are off unless configured |
| **Python** | `# noqa: TID251`, `# noqa: N802` | Ruff `--add-noqa=<reason>` stamps (count `# noqa` per code); import-linter `ignore_imports` entries | `pyproject.toml` / `ruff.toml` per package: `extend-ignore`, `per-file-ignores` | Ruff `RUF100` flags unused `noqa`; import-linter 2.12+ reports unmatched ignores |
| **Go** | `//nolint:depguard // reason` | `--new-from-merge-base` hides old issues (a moved file shows all as new) | `.golangci.yml` per module | golangci-lint and depguard are GPL-3.0: run them, never vendor them |
| **Java / Kotlin** | `@SuppressWarnings`, `@Suppress` | ArchUnit `FreezingArchRule` store (`archunit_store/`); detekt `baseline.xml` | per-module Checkstyle / detekt configs | detekt 2.x cannot read a 1.x baseline |
| **.NET** | `#pragma warning disable IDE1006` | `GlobalSuppressions.cs` | `.editorconfig` per project | only the IDE1006 diagnostic severity is enforced at build |
| **Ruby / PHP** | `# rubocop:disable Naming/…`; `@phpstan-ignore` | packwerk `package_todo.yml` (`strict` refuses additions); `.rubocop_todo.yml`; `phpstan-baseline.neon`, `psalm-baseline.xml` | per-package `package.yml`, `.rubocop.yml` | `update-todo` overuse is the anti-pattern |
| **API specs** | Spectral `overrides` | `.redocly.lint-ignore.yaml` | per-spec ruleset | — |

Run only project-local binaries; never `npx -y`. A missing tool prints `blocked (<tool> not installed)`. Before any CLI: `DO_NOT_TRACK=1 CI=true`. Never pass `--fix`, `--suppress-all` or `--prune-suppressions` in a scan: they write into the repo.

## Pre-flight

Run as **one** bash script from the repo root. Step **N** feeds detector **§N**. Every `rg` names its path; any `rg` exit 2 is a failed search, never zero hits. `BASE` defaults to the merge-base with the default branch; set `BASE_DIR=<dir>` to compare against a copy when there is no history (a fixture's `.refract-fixture/align-base/`, a downloaded release). For § 4, set `OLD` (and optionally `NEW` and `SINCE`) to the patterns and date the ADR names.

```bash
[ -n "${BASH_VERSION:-}" ] || { echo "pre-flight: run it with bash (save it, then bash <file>): PIPESTATUS and arrays are bash-only, and under zsh every exit prints blank"; exit 2; }
ROOTS=(.)   # code roots; in a monorepo name them: ROOTS=(apps/web apps/api packages)
CO="${CO:-.claude/skills/convention-oracle/scripts}"; RUN="${RUN:-$(mktemp -d "${TMPDIR:-/tmp}/align.XXXXXX")}"; mkdir -p "$RUN"; echo "RUN=$RUN"
export GIT_OPTIONAL_LOCKS=0 DO_NOT_TRACK=1 CI=true
BASE="${BASE:-$(git merge-base HEAD origin/HEAD 2>/dev/null || git merge-base HEAD origin/main 2>/dev/null || git rev-parse -q --verify HEAD~1)}"; echo "BASE=${BASE:-none} BASE_DIR=${BASE_DIR:-none}"
NOBASE="no base: history-blind, no BASE_DIR"   # on the default branch the merge-base IS HEAD: every count compares with itself
if [ -n "$BASE" ] && [ -z "${BASE_DIR:-}" ] && [ "$(git rev-parse -q --verify "$BASE^{commit}" 2>/dev/null)" = "$(git rev-parse -q --verify HEAD 2>/dev/null)" ]; then
  echo "AL-30: NOT RUN (BASE == HEAD $(git rev-parse --short HEAD): set BASE=<an older commit or release tag> or BASE_DIR)"; NOBASE="BASE == HEAD"; BASE=; fi
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/third_party/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**'
   -g '!**/.venv/**' -g '!**/__generated__/**' -g '!**/*.gen.*' -g '!**/*.min.*' -g '!**/*.{md,lock,map,snap}')
# The convention rules: naming, layout, imports and wrappers, tokens, i18n literals, design-system rules. Correctness and
# security rules are NOT here: their suppressions belong to code-quality suppression-scan and security sast-scan § 10.
CONV='^(?:no-restricted-(?:imports|syntax|globals|properties)|boundaries/.+|import-x?/no-(?:internal-modules|restricted-paths|relative-packages)|check-file/.+|unicorn/filename-case|@typescript-eslint/naming-convention|camelcase|id-match|react/forbid-(?:elements|component-props|dom-props)|vue/no-restricted-.+|@nx/enforce-module-boundaries|i18next/no-literal-string|lingui/no-unlocalized-strings|tailwindcss/no-(?:arbitrary-value|custom-classname)|better-tailwindcss/.+|scale-unlimited/declaration-strict-value|color-no-hex|color-named|declaration-property-value-(?:allowed|disallowed)-list|unit-(?:allowed|disallowed)-list|custom-property-pattern|selector-class-pattern|function-disallowed-list|declaration-no-important|@atlaskit/design-system/.+|polaris/.+|primer/.+|primer-react/.+|carbon/.+|TID25[1-3]|N8\d\d|N999|ICN00\d|depguard|forbidden:.+)$'

# 0. The oracle map (convention-oracle § 0): rules.tsv, exceptions.tsv (every inline disable, its reason kind and cluster), gates.tsv.
[ -s "$RUN/oracle/rules.tsv" ] || { python3 -I "$CO/oracle-map.py" . --out="$RUN/oracle" --age-buckets; echo "oracle-map exit $?"; }

# 1. AL-29: every inline suppression (the count), then the ones that silence a convention rule or are blanket in a file a
#    convention rule at error covers. exceptions.tsv: site tool rules scope reason_kind resolves in_oracle cluster reason.
rg -n --pcre2 '(?:eslint-disable(?:-next-line|-line)?|stylelint-disable(?:-next-line|-line)?|#\s*noqa|//\s*nolint|ast-grep-ignore|biome-ignore|@SuppressWarnings|#pragma\s+warning\s+disable|rubocop:disable|@phpstan-ignore)\b' "${X[@]}" "${ROOTS[@]}" > "$RUN/supp.txt"; echo "rg 1 exit $? ($(wc -l < "$RUN/supp.txt" | tr -d ' ') directives)"
python3 -I - "$RUN/oracle" "$CONV" <<'PY'
import sys, re, os
d, conv = sys.argv[1], re.compile(sys.argv[2])
rd = lambda n: [dict(zip(ls[0][2:].split('\t'), l.split('\t'))) for ls in [open(os.path.join(d, n)).read().rstrip('\n').split('\n')] for l in ls[1:] if l and not l.startswith('#')]
rules = rd('rules.tsv')
err = [r for r in rules if r['severity'] == 'error' and conv.search(r['rule'])]
for r in rules:   # § 3 input: a convention rule switched off in some scope (AL-31 when the root or a sibling has it at error)
    if r['severity'] == 'off' and conv.search(r['rule']):
        print('AL-31?\toff\t%s\t%s\t%s' % (r['rule'], r['scope'], r['source']))
ex = rd('exceptions.tsv'); n = 0
for e in ex:
    ids = e['rules'].split(',')
    same = [r for r in err if r['tool'] == e['tool']]          # a blanket eslint-disable cannot silence a depcruise rule
    hit = [r for r in ids if conv.search(r)] or (ids == ['*'] and same and ['* (blanket over %d %s convention rules at error)' % (len(same), e['tool'])])
    if not hit:
        continue
    n += 1
    why = 'reasonless' if e['reason_kind'] == 'none' else 'adr unresolved' if e['resolves'] == 'no' else 'cluster %s (P-26)' % e['cluster'] if int(e['cluster'] or 0) > 5 else 'reasoned (%s) - verify' % e['reason_kind']
    print('AL-29\t%s\t%s\t%s\t%s\t%s' % (e['site'], ','.join(hit), e['scope'], why, e['reason'][:60]))
print('AL-29: %d of %d directives silence a convention rule (the rest: suppression-scan / sast-scan)' % (n, len(ex)))
PY

# 2. AL-30: every baseline file present, then per-(file, rule) counts head vs base. --hidden: some live in dot-directories.
#    BASE_DIR's own copies are the base, never a baseline at head: a BASE_DIR inside the tree is excluded (the last matching
#    rg glob wins, so the exclusion comes after the file-name globs).
BDX="${BASE_DIR:-.no-base-dir}"; BDX="${BDX#./}"; BDX="${BDX%/}"
#    A project's own ratchet files count too (`*-baseline.json`, `*ratchet*.json`: any numeric leaf that rose, or a new key).
rg --files --hidden -g '{eslint-suppressions.json,eslint.seatbelt.tsv,.dependency-cruiser-known-violations.json,package_todo.yml,phpstan-baseline.neon,psalm-baseline.xml,detekt-baseline.xml,baseline.xml,.redocly.lint-ignore.yaml,.importlinter,.eslint-bulk-suppressions.json,.betterer.results}' -g '*{-,.,_}baseline.json' -g '*ratchet*.json' -g 'archunit_store/**' -g '!.git/**' -g '!**/node_modules/**' -g '!**/{fixtures,__fixtures__,testdata}/**' -g "!$BDX/**" . > "$RUN/baselines.txt"; echo "rg 2 exit $? ($(wc -l < "$RUN/baselines.txt" | tr -d ' ') baseline files)"
while read -r f; do f="${f#./}"; mkdir -p "$RUN/base/$(dirname "$f")"
  if [ -n "${BASE_DIR:-}" ]; then cp "$BASE_DIR/$f" "$RUN/base/$f" 2>/dev/null || : > "$RUN/base/$f"
  elif [ -n "$BASE" ]; then git show "$BASE:$f" > "$RUN/base/$f" 2>/dev/null || : > "$RUN/base/$f"; git diff --numstat "$BASE" -- "$f"
  else echo "AL-30 $f: blocked ($NOBASE)"; continue; fi
  python3 -I - "$RUN/base/$f" "$f" <<'PY'
import sys, json, re
def counts(p):
    t = open(p, encoding='utf-8', errors='replace').read()
    if not t.strip(): return {}
    if p.endswith('eslint-suppressions.json') or p.endswith('.eslint-bulk-suppressions.json'):
        j = json.loads(t)
        if isinstance(j, dict) and 'suppressions' in j:   # @rushstack/eslint-bulk: a list of {file, scopeId, rule}
            c = {}
            for s in j['suppressions']: c[(s.get('file'), s.get('rule'))] = c.get((s.get('file'), s.get('rule')), 0) + 1
            return c
        return {(f, r): v.get('count', 0) for f, rs in j.items() for r, v in rs.items()}   # core: {file: {rule: {count}}}
    if p.endswith('known-violations.json'):
        c = {}
        for v in json.loads(t):
            k = (v.get('from'), v.get('rule', {}).get('name')); c[k] = c.get(k, 0) + 1
        return c
    if p.endswith('.tsv'):
        return {tuple(l.split('\t')[:2]): int(l.split('\t')[2]) for l in t.splitlines() if l.count('\t') >= 2 and l.split('\t')[2].strip().isdigit()}
    if p.endswith('.importlinter'):   # ignore_imports entries are `a -> b`; a new contract is coverage, not growth
        return {('ignore_imports', '*'): len([l for l in t.splitlines() if '->' in l and not l.lstrip().startswith(('#', ';'))])}
    if p.endswith('.json'):   # a project's own ratchet: every numeric leaf by its key path; a list of numbers by position
        c = {}
        def walk(v, k):
            if isinstance(v, bool): return
            if isinstance(v, (int, float)): c[(k, '')] = v
            elif isinstance(v, dict): [walk(x, k + '/' + str(n)) for n, x in v.items()]
            elif isinstance(v, list) and all(isinstance(x, (int, float)) for x in v): [walk(x, '%s[%d]' % (k, n)) for n, x in enumerate(v)]
            elif isinstance(v, list): c[(k, 'entries')] = len(v)
        walk(json.loads(t), ''); return c
    return {('lines', '*'): len([l for l in t.splitlines() if l.strip() and not l.lstrip().startswith(('#', ';'))])}
b, h = counts(sys.argv[1]), counts(sys.argv[2])
grew = [(k, b.get(k, 0), v) for k, v in h.items() if v > b.get(k, 0)]
for k, was, now in grew: print('AL-30\t%s\t%s\t%d -> %d' % (sys.argv[2], ' '.join(map(str, k)), was, now))
print('%s: %d keys, %d grew, total %d -> %d' % (sys.argv[2], len(h), len(grew), sum(b.values()), sum(h.values())))
PY
done < "$RUN/baselines.txt"
awk -F'\t' '$1 ~ /^(boundaries-rename|boundaries-major|unicorn-dirs)$/' "$RUN/oracle/gates.tsv"   # a count jump after these bumps is a rebaseline
#    2c. Ratchets that live IN a test: specs.tsv `ratchet` rows, plus the test files a doc's ratchet table lists (CONTRIBUTING
#        `### Ratchets`). Each `CEILING`-style const and each `'a -> b': N` map entry, head vs base (nth occurrence of a key).
{ awk -F'\t' '$2=="ratchet" {print $1}' "$RUN/oracle/specs.tsv" 2>/dev/null
  awk -F'\t' 'tolower($5) ~ /ratchet/ {print $8}' "$RUN/oracle/docs.tsv" | grep -oE '`[^`]+\.(spec|test)\.[cm]?[jt]sx?`' | tr -d '`'; } | sort -u > "$RUN/ratchet-tests.txt"
echo "2c: $(wc -l < "$RUN/ratchet-tests.txt" | tr -d ' ') ratchet tests"
while read -r f; do [ -f "$f" ] || continue; mkdir -p "$RUN/base/$(dirname "$f")"
  if [ -n "${BASE_DIR:-}" ]; then cp "$BASE_DIR/$f" "$RUN/base/$f" 2>/dev/null || : > "$RUN/base/$f"
  elif [ -n "$BASE" ]; then git show "$BASE:$f" > "$RUN/base/$f" 2>/dev/null || : > "$RUN/base/$f"
  else echo "AL-30 $f: blocked ($NOBASE)"; continue; fi
  python3 -I - "$RUN/base/$f" "$f" <<'PY'
import re, sys
CONST = re.compile(r'\b(?:const|let|var|final|static)\s+([A-Z][A-Z0-9_]*(?:CEILING|BASELINE|BUDGET|MAX|LIMIT|ALLOWED)[A-Z0-9_]*)\b[^=\n]*=\s*([\d_]+)\b')
ENTRY = re.compile(r'^\s*[\'"]([^\'"\n]{1,120})[\'"]\s*:\s*([\d_]+)\s*,?\s*(?://.*)?$')
def pts(p):
    out, seen = {}, {}
    for n, l in enumerate(open(p, encoding='utf-8', errors='replace').read().split('\n'), 1):
        for m in [CONST.search(l), ENTRY.match(l)]:
            if m:
                k = m.group(1); seen[k] = seen.get(k, 0) + 1; out[(k, seen[k])] = (int(m.group(2).replace('_', '')), n)
    return out
b, h = pts(sys.argv[1]), pts(sys.argv[2])
grew = [(k, b.get(k, (0, 0))[0], v) for k, v in h.items() if v[0] > b.get(k, (0, 0))[0] and (k in b or not b == {})]
for k, was, (now, ln) in grew: print('AL-30\t%s:%d\t%s\t%d -> %d%s' % (sys.argv[2], ln, k[0], was, now, '' if k in b else ' (new key)'))
print('%s: %d ratchet points, %d grew%s' % (sys.argv[2], len(h), len(grew), ' (absent at base)' if not b else ''))
PY
done < "$RUN/ratchet-tests.txt"
#    2b. A rule loosened since the base: the base revision's config files only, re-mapped, severities compared per (tool, rule, scope).
if [ -n "$BASE" ] && [ -z "${BASE_DIR:-}" ]; then mkdir -p "$RUN/base-tree"
  for p in $(cut -f12 "$RUN/oracle/rules.tsv" | sed 1d | cut -d: -f1 | sort -u) package.json; do   # one archive per file: a file absent at BASE fails only itself
    git archive "$BASE" -- "$p" 2>/dev/null | tar -x -C "$RUN/base-tree" 2>/dev/null; done; echo "base configs: $(find "$RUN/base-tree" -type f | wc -l | tr -d ' ') present at $BASE"; fi
BT="${BASE_DIR:-$RUN/base-tree}"; NB=0
[ -d "$BT" ] && python3 -I "$CO/oracle-map.py" "$BT" --out="$RUN/oracle-base" > /dev/null && NB=$(sed 1d "$RUN/oracle-base/rules.tsv" | wc -l | tr -d ' ')
if [ "$NB" -eq 0 ]; then echo "2b: NOT RUN (the base at ${BASE_DIR:-${BASE:-none}} holds 0 config rules: no loosening can be compared)"; else echo "2b: base holds $NB config rules"
python3 -I - "$RUN/oracle-base/rules.tsv" "$RUN/oracle/rules.tsv" <<'PY'
import sys
rank = {'error': 2, 'warn': 1, 'off': 0}
rd = lambda p: {(r[1], r[2], r[6]): r[3] for r in (l.split('\t') for l in open(p).read().splitlines()[1:]) if len(r) > 6}
b, h = rd(sys.argv[1]), rd(sys.argv[2])
for k, sev in sorted(b.items()):
    if rank.get(h.get(k, 'off'), 0) < rank.get(sev, 0): print('AL-30\tloosened\t%s %s (%s)\t%s -> %s' % (k[0], k[1], k[2], sev, h.get(k, 'removed')))
PY
fi

# 3. AL-31: per-package drift — dead or shadowed eslintrc, boundaries v7 option, convention rules turned off, CI coverage,
#    package configs that do not spread the shared one, Ruff ignores of a banned-api or naming code.
awk -F'\t' '$1 ~ /^(eslintrc-dead|eslintrc-shadowed|boundaries-option)$/' "$RUN/oracle/gates.tsv"
awk -F'\t' '$10=="partial" {print "ci="$10"\t"$2"\t"$3"\t"$7"\t"$12}' "$RUN/oracle/rules.tsv"
rg --files -g '**/eslint.config.{js,mjs,cjs,ts,mts}' "${X[@]}" . | rg -v '^\./eslint\.config\.' > "$RUN/pkg-configs.txt"
[ -s "$RUN/pkg-configs.txt" ] && xargs rg --files-without-match --pcre2 'from\s+["\x27](?:(?:\.\./)+eslint\.config|@[\w.-]+/eslint-config|eslint-config-[\w.-]+)|\.\.\.(?:base|root|shared)\w*' < "$RUN/pkg-configs.txt"; echo "package configs: $(wc -l < "$RUN/pkg-configs.txt" | tr -d ' ') (above: ones that import no shared config)"
rg -n --pcre2 '^\s*(?:extend-)?ignore\s*=\s*\[[^\]]*"(?:TID25\d|N8\d\d|N999|ICN\d+)"|^\s*"[^"]+"\s*=\s*\[[^\]]*"(?:TID25\d|N8\d\d)"' -g '{pyproject.toml,ruff.toml,.ruff.toml}' "${X[@]}" .; echo "rg 3e exit $? (1 = no ignore of a convention code)"

# 4. AL-32: the declared direction — ADR decisions, then written doc bullets that retire a shape (a conventions line such as
#    "`connect()` is retired" is a direction with no ADR), bans that name an old shape, and @deprecated exports.
#    "migrat" alone matched every database migration (measured 2026-10-18: 44 noise lines on a real monorepo). Only the VERB
#    counts ("Migrated the five raw selects", "a file that mixes the two is migrated"), and never inside a name or a path
#    (`foo-migrate`, `dist/database/migrate.cli.js`, `db:migrate`); the noun "migration" counts only as "migration to/from/away".
M='(^|[^-:./a-z_])migrat(e|es|ed|ing)([^a-z._]|$)|migration (to|from|away|off) '
awk -F'\t' -v M="$M" '($4=="adr-decision" && (tolower($8) ~ /instead of|replace|new code|no longer|deprecat|over |frozen/ || tolower($8) ~ M)) || ($3=="T2" && $4!="adr-decision" && (tolower($8) ~ /retired|instead of|replaced by|no longer|deprecat|being removed|is removed/ || tolower($8) ~ M)) {print $7"\t"$5"\t"substr($8,1,120)}' "$RUN/oracle/docs.tsv"
cut -f1,2,5 "$RUN/oracle/wrappers.tsv" | sed 1d
rg -n --pcre2 '@deprecated\b' -g '*.{ts,tsx,js,mjs,vue,py,kt,java,cs}' -g '!**/*.d.ts' "${X[@]}" "${ROOTS[@]}"; echo "rg 4c exit $?"
#    4d. Per old shape 4a or 4b names: OLD holds one pcre2 per line (one line per declared migration, OLD=$'<adr shape>\n<bullet
#        shape>'); NEW and SINCE, when set, pair with OLD line by line (an empty line skips). Files now, mixed vs uniform, adds after the date.
if [ -z "${OLD:-}" ]; then echo "4d: not run — set OLD=<pcre2 per line, one per old shape 4a / 4b names>"; else i=0
  while IFS= read -r o; do i=$((i+1)); [ -n "$o" ] || continue
    nw=$(printf '%s\n' "${NEW:-}" | sed -n "${i}p"); sn=$(printf '%s\n' "${SINCE:-}" | sed -n "${i}p")
    rg -c --pcre2 "$o" "${X[@]}" "${ROOTS[@]}" > "$RUN/old-$i.txt" < /dev/null; echo "rg 4d[$i] exit $? ($(wc -l < "$RUN/old-$i.txt" | tr -d ' ') files) OLD=$o"
    [ -n "$nw" ] && rg -l --pcre2 "$nw" "${X[@]}" "${ROOTS[@]}" < /dev/null | rg -F -x -f - <(cut -d: -f1 "$RUN/old-$i.txt") | sed "s/^/mixed (P-25 finding) [$i]: /"
    [ -n "$sn" ] && git log --since="$sn" --diff-filter=A --name-only --format= -- . < /dev/null | sort -u | rg -F -x -f - <(cut -d: -f1 "$RUN/old-$i.txt" | sed 's#^\./##') | sed "s/^/added since $sn [$i]: /"
    [ -z "$nw" ] && rg -n --pcre2 "$o" "${X[@]}" "${ROOTS[@]}" < /dev/null | head -50 | sed "s/^/old shape [$i]: /"   # no NEW: every site, to read
  done <<< "$OLD"; fi
```

`exceptions.tsv` (from `oracle-map.py`) classifies each directive's reason as `adr` (and whether the ADR file exists), `ticket`, `text` or `none`, and counts how many disables of one rule share one exact reason (`cluster`). The script prints only directives that touch a convention rule; everything else is listed by `suppression-scan`.

**Measured** (2026-10-18), whole script per fixture root:

- `quality-mix`: grep 1 found 4 directives: a file-level `/* eslint-disable */`, two `eslint-disable-next-line` for `no-floating-promises` / `no-require-imports` and one for `no-explicit-any` with a ticket reason. **0 are AL-29**: the only ESLint rules at `error` are `eqeqeq` and `no-floating-promises`, both correctness rules, so all four route to `suppression-scan`, which the answer key also names (QM-SUP-01, QM-SUP-03). A first draft counted the blanket disable as AL-29 because two depcruise `forbidden` rules are at `error`. An `eslint-disable` cannot silence depcruise, so the blanket test now counts only convention rules of the **same tool**. § 2: 0 baseline files. § 3: no package config, no Ruff ignore of a convention code, no `ci=partial` row (the depcruise rules are `ci=no` over their whole scope, which is AL-03, `convention-oracle` §3). § 4: the five depcruise bans of ADR 0002 are listed as the declared direction; no `@deprecated`, no migration ADR → `N/A (no declared migration)`.
- `convention-drift` (staged copy, one commit, `BASE_DIR=.refract-fixture/align-base`, `OLD=$'\bstyled\.\w+\n\bconnect\('` with `NEW='\.module\.css' SINCE=2026-03-01` on the first line only, from ADR-0011 and the `connect()` bullet; re-run 2026-10-18 after the fixes): **10 of 10 seeds** — a reasonless disable and a file-scope disable in a CSS module (CD-AL29-a/b), `cluster 6 (P-26) legacy` (CD-AL29-c), `<file> no-restricted-imports 1 -> 3` (CD-AL30-a), the new known violation `0 -> 1` (CD-AL30-b), the `off` rows for admin's import ban and for `TID251` (CD-AL31-a/b), gate `eslintrc-dead` (CD-AL31-c), a component mixing both shapes (CD-AL32-a), and `old shape [2]: <file>:<line>` (CD-AL32-b): 4a now lists written doc bullets that retire a shape, so `ai/conventions.md:33` ("`connect()` is retired") is offered beside the ADR, and `OLD` takes one pattern per line. Fixed: the baseline search listed `BASE_DIR`'s own two copies as baselines and printed two false `0 -> 1` AL-30 rows (the exclusion glob must come after the file-name globs: the last matching `rg` glob wins), now 3 baseline files and 0 false rows; 2b, against a base holding 0 configs, said nothing and now prints `2b: NOT RUN (the base … holds 0 config rules …)`. `added since` still means nothing on a one-commit copy. Decoys printed and dropped only at the read: CD-DECOY-21 (a generated route tree, P-16), DECOY-17 (ticket reason), DECOY-01 (ADR reason, the disable in the PDF helper), DECOY-13 (frozen until 2027-03-31, ADR-0009). Re-run after the real-repo fixes (2026-10-18): the same 10 seed rows, `2c: 0 ratchet tests`.
- A real NestJS + React monorepo (read-only, re-measured 2026-10-18 after the fold-back fixes; before → after): the default `BASE` was the merge-base with `origin/HEAD`, i.e. HEAD itself, and § 2 compared every count with itself, silently → `AL-30: NOT RUN (BASE == HEAD …)` and every baseline `blocked (BASE == HEAD)`. With `BASE=<an older commit>`: 0 baseline files read → 3 (`function-size-baseline.json`, `exhaustive-deps-baseline.json`, `validation-ratchet.json`: 4 new keys, total 24 → 24, a moved key) and 25 ratchet tests from `specs.tsv` and the CONTRIBUTING ratchet table: the six cross-module ceiling rises the audit had read by hand (`'domain -> domain'` 38 → 40 at `:73` … `'infrastructure -> application'` 35 → 38 at `:1160`) plus `FACTORY_ENTITY_CEILING` 144 → 237 and `ANY_ENTITY_CEILING` 1,076 → 1,143. § 1: 138 of 187 directives → 418 of 486 (the CI-linted test trees now count; no config prose). § 3: 0 → 24 `ci=partial` rows (CI lints `src/` and `test/` per package, not `scripts/`). 4a: 61 → 39 lines, the 22 dropped all database-migration prose; `convention-drift` 5 → 5.
- `web-dashboard`, `a11y-states`, `frontend-correctness`: 0 directives, 0 baseline files, 0 package configs, 0 migration signals: §1–§4 `N/A` with those reasons.
- Inside a fixture, `BASE` resolves to the host repository's merge-base, where the fixture does not exist yet: 2b printed `base configs: 0 present`, so nothing could be compared. A fixture run therefore needs `BASE_DIR`.
- A scratch git tree seeded with one case per class (2026-10-18) printed every expected row and nothing else: a reasonless and a `legacy`-reasoned `no-restricted-imports` disable; `eslint-suppressions.json` 1 → 3 for one (file, rule); `no-restricted-imports` loosened `error -> warn` since `BASE`; a dead `.eslintrc.json` beside the flat config on ESLint 10; a package config that turns the rule `off` without importing the shared one; `extend-ignore = ["TID251"]`; an ADR "New code uses CSS Modules instead of styled-components", with `OLD='\bstyled\.\w+'` and `NEW='\.module\.css'` finding one mixed file.

## The 3,000-hit path

A repo that has lived with lint rules for years can carry thousands of disables and a baseline with thousands of entries. Triage in this order and record every step in the coverage block:

1. **Intersect with the oracle.** Keep directives whose rule is a convention rule at T1/T2 (`CONV`, the same-tool blanket test). Hand the rest to `suppression-scan` in one line with the count.
2. **Group** by (rule, reason string). The same reason on more than 5 disables of one rule is one P-26 cluster for a human (§ 26), not N rows. Baselines group by (rule, file).
3. **Rank** by growth first (a baseline key that grew since `BASE`, a disable in a file added after the rule was enabled), then newest files, then churn.
4. **Read** the top 30 groups fully: the directive, the rule's message, the reason, and the site with the disable removed.
5. **Ratchet the rest.** Where the rule runs at `error`, the existing bulk-suppression file **is** the ratchet: report `Live, ratcheted (k groups / n hits — eslint-suppressions.json)`. Otherwise `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

| § | Class | Severity | Proof |
|---|---|---|---|
| 1 | AL-29 suppression dodging a declared convention rule | Low; Medium for a file-level or blanket disable; High only when the silenced rule guards a permission, tenant or auth wrapper | V406 |
| 2 | AL-30 ratchet regression (a baseline grew, a rule loosened) | Medium | V395 |
| 3 | AL-31 per-package config drift | Medium | V390 |
| 4 | AL-32 half-finished declared migration | Low; Medium for old-shape sites in files added after the ADR date | V395 (+ V391 on close) |

Convention classes are never Critical.

### 1. Suppression dodging a convention rule (AL-29)

```
BAD:   import ky from 'ky'; // eslint-disable-line no-restricted-imports              (no reason)
       /* stylelint-disable scale-unlimited/declaration-strict-value */                    (file-level)
       // eslint-disable-next-line boundaries/dependencies -- legacy                       (same reason on 6 disables: § 26)
GOOD:  // eslint-disable-next-line no-restricted-imports -- ADR-0007: raw ky streams the PDF export     (docs/adr/0007-… exists)
       // eslint-disable-next-line boundaries/dependencies -- ORD-412 vendor widget shim   (tracker key pattern)
```
**Read the code:** Is the rule a convention rule, or a correctness rule that only looks local (a `no-restricted-syntax` whose message names a correctness lesson belongs to `suppression-scan` §2)? Does the reason resolve: the ADR file exists and says this, the ticket matches the tracker's key and is open? Does the disable still suppress anything? Re-run with it removed in a scratch copy (`eslint --no-inline-config -f json <file>`, `ruff check --ignore-noqa --no-cache <file>`): no diagnostic means it is stale, and `reportUnusedDisableDirectives` would have caught it. Was a boundaries v7 or unicorn v65 bump in the same change? Then a renamed-rule disable is a rebaseline. **Finding when** a convention rule is silenced with no reason, an unresolved reason, a § 26 cluster reason, or file-wide. **Proof:** V406 — the reason resolves, or with the disable removed the rule fires at the site (that site then becomes the owning detector's row) or the disable is stale.

### 2. Ratchet regression (AL-30)

```
BAD:   eslint-suppressions.json  "apps/web/src/features/orders/api.ts": { "no-restricted-imports": { "count": 1 → 3 } }
       .dependency-cruiser-known-violations.json  +1 entry; .importlinter ignore_imports +1 line
       eslint.config.mjs  "no-restricted-imports": "error" → "warn"  since BASE
GOOD:  every (file, rule) count at head ≤ base, and no convention rule loosened; a rebaseline lands in the same commit as the
       boundaries v7 / unicorn v65 bump, with an ADR line naming it
```
**Read the code:** Is the base real and older than HEAD (`AL-30: NOT RUN (BASE == HEAD)` on the default branch: pass `BASE=<the last release tag>`)? Did a ceiling rise carry its own reason in the file (`// +1: <why>`)? The oracle decides whether a reasoned raise is the declared path (an ADR that says "a new pair is a decision recorded here") or erosion: report it Unconfirmed with that question, never silently accept it. Did the count grow because new violations were absorbed (someone re-ran `--suppress-all` or `--baseline`) or because a file was renamed (the key moved; the total did not grow)? Compare the totals line too. Is the base real (`base configs: k present`, a `numstat` line)? With 0 present the class is `blocked (no base)`. Is there a version bump of eslint-plugin-boundaries or eslint-plugin-unicorn in the same range (the gates rows)? Then it is the § 3 rebaseline exception **only** if an ADR or the commit names it. **Finding when** any key grew or any convention rule's severity fell since `BASE`. **Proof:** V395 — counts at head ≤ base for every baseline file, and no rule downgraded.

### 3. Per-package config drift (AL-31)

```
BAD:   apps/admin/eslint.config.mjs  imports no shared config and sets "no-restricted-imports": "off"
       services/reports-py/pyproject.toml  extend-ignore = ["TID251"]            (no reason)
       .eslintrc.json beside eslint.config.mjs on ESLint 10                       (dead config: the team edits a file nothing reads)
       eslint-plugin-boundaries 7 with `rules:` instead of `policies:`
GOOD:  every package config spreads the shared one; a different runtime (a Node CLI beside the web app) with its documented reason (§ 17)
```
**Read the code:** Does the package really run on a different runtime with a reason written down (P-17 exempt)? Is the convention rule `off` in that package while the root or a sibling has it at `error` (the `AL-31?` rows)? Does the CI job lint this package while its siblings are linted (`ci=partial`)? For the stale `.eslintrc*`: does anyone still edit it believing it applies (`git log -1 -- <file>`)? When ESLint is installed, `eslint --print-config <file in the package>` is the resolved truth; without it, the static parse is a candidate and every `static!=resolved` gate stays open. **Finding when** a convention rule declared for the repo does not apply in a package with no documented reason, or a config file the installed tool does not read is present. **Proof:** V390 — the rule at `error` over that package from a scratch config, counted; for dead config, the resolved config shows the file is not read.

### 4. Half-finished declared migration (AL-32)

```
BAD:   docs/adr/0011 (2026-03-01) "New code uses CSS Modules instead of styled-components"
       apps/web/src/features/cart/CartRow.tsx  styled.div  beside  CartRow.module.css     (mixed file: § 25 finding)
       apps/web/src/features/returns/ReturnForm.tsx  added 2026-06-12, uses styled.div       (after the ADR date: counts double)
GOOD:  packages/legacy-reports/** styled-components, ADR-0009 frozen until 2027-03-31  (§ 16)
       a module uniformly in the old shape that the oracle has not scheduled            (§ 25: ratchet it, not IMPORTANT)
```
**Read the code:** Does a T1/T2 oracle name the direction (an accepted ADR, a "use X" ban message, a `@deprecated` tag with its replacement)? An observed trend alone is a proposal for `convention-oracle` § 2. Is the old shape in a frozen package whose date has not passed (`frozen-until=` in `docs.tsv`)? Is the file mixed, or uniformly old? Is the old-shape count falling month on month (`git log -S'<old>' --since=<ADR date>` bounded to that range)? Without history the trend is `blocked (history-blind)` and only the current count stands. **Finding when** the declared new shape exists and the old one survives in a mixed file, or appears in a file added after the ADR date; otherwise it is ratcheted residue. **Proof:** V395 — a shrink-only counter for the old shape that only falls, and V391 re-detect zero at each closed site.

## Proof

Oracles and variant lists: [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Align. **V406** (suppression reason resolves) for §1, **V395** (ratchet shrink-only) for §2 and §4, **V390** (rule at error count) for §3, **V391** (re-detect zero) before any row closes, and **V399** (non-vacuous: the rule matched N > 0 files) for every rule the class leans on. The class's lint config is read-only during a fix (V408): loosening a rule, or regenerating a baseline after new violations, is the regression this skill reports, never a fix.

## Output

```
convention-ratchet-scan — lanes: eslint 10.13 (flat), boundaries 7.2, ruff 0.17; BASE=main@3f1c2a9 (merge-base)
Gates: boundaries-major v7 (policies) · eslintrc-dead .eslintrc.json

1. apps/web/src/features/orders/api.ts:4                                     [report-with-fix]   low
   §1 AL-29 — `eslint-disable-next-line no-restricted-imports` with no reason; rule at error (eslint.config.mjs:12,
   message "use @acme/http"). Removed in a scratch copy: the rule fires (raw `ky` import → wrapper-adoption-scan §1).
2. eslint-suppressions.json                                                  [report-with-fix]   medium
   §2 AL-30 — apps/web/src/features/orders/api.ts no-restricted-imports 1 → 3 since BASE; no plugin bump in range.
   Fix: revert the two absorbed entries; fix the sites. Proof: counts at head ≤ base (V395).
3. apps/admin/eslint.config.mjs:1                                            [report-flagged]    medium
   §3 AL-31 — imports no shared config; no-restricted-imports off. Same Vue runtime as apps/web: no P-17 reason found.
   Settling probe: node_modules/.bin/eslint --print-config apps/admin/src/main.ts.
4. ADR-0011 CSS Modules (2026-03-01)                                         [report-flagged]    low
   §4 AL-32 — styled.* in 14 files: 2 mixed, 1 added after 2026-03-01; trend blocked (history-blind).

Verification: 9 candidates → 2 findings · 2 unconfirmed · 3 hardening · 0 pre-existing · 2 refuted

Class coverage:
  §1  AL-29 suppressions       checked (212 directives → 9 convention → 1 finding; 203 to suppression-scan)
  §2  AL-30 ratchet growth     checked (2 baseline files, BASE present → 1 finding)
  §3  AL-31 package drift      checked (4 package configs, 1 ruff config → 1 unconfirmed)
  §4  AL-32 migration residue  checked (1 migration ADR → 1 unconfirmed) · trend blocked (history-blind)
```

`[report-with-fix]`: the convention rule, its oracle row and the before/after count or reason check are all in hand. `[report-flagged]`: a link is open (no base, a tool not installed, a resolved config not read, a trend history cannot date). The coverage block lists **all four** classes on every run: `checked (k → m)` only when the step ran; `N/A (<reason>)` only when the surface is absent (no directive, no baseline file, no package config, no declared migration); `blocked (<reason>)` when a base, a tool or a script was missing; `Live, unreviewed` / `Live, ratcheted` for a partial review.

## False positives / precedents

The verifier reads [`precedents/align.md`](../../../../snippets/precedents/align.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10 (maintainability / conventions column; gate 3 there carries the ESLint 10, TS 7, boundaries v7 and unicorn v65 facts). The ones this skill meets most:

- **§ 3 A reasoned exception is not a finding**: an ADR or ticket reason that resolves, an `allow` / `ignore_imports` / known-violation entry that did not grow; reported only if it grew.
- **§ 26 Copy-pasted boilerplate reasons do not count**: more than 5 disables of one rule with one reason is a cluster for review.
- **§ 16 Frozen packages** are out of scope until their date passes; **§ 25** a uniformly old module is ratcheted residue, a mixed file is a finding.
- **§ 17 Context splits**: a package on a different runtime with a written reason may differ.
- **§ 2** a rule at `warn` is AL-03, not a suppression question; **§ 20** a class with no base or no tool is `blocked`, never clean.
- **§ 34** a base that is HEAD is no base; **§ 35** a ceiling kept in a test is a baseline; **§ 36** a `-- see above` reason is the comment above it, and a cluster groups the resolved reason.

## When to run

- On any diff that adds or edits a disable comment, a baseline file (`eslint-suppressions.json`, a known-violations file, `package_todo.yml`, an ArchUnit store), a lint or Ruff config at any level, or an ADR that declares a migration: the `align-detect` dispatch signal.
- On every whole-repo `/align-scan`, reporting all four classes, and on every `/align` close: L11 of the fix ladder regenerates the baseline only **after** the fixes, and this skill's § 2 checks it only shrank.
- After a bump of ESLint, eslint-plugin-boundaries or eslint-plugin-unicorn: counts move for reasons that are not new drift.

## Halt conditions

- Do not report a row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§ 10). Under `/align-scan` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any row without its `<file:line>`, the convention rule and its oracle row, and the count or reason evidence.
- Never run `--fix`, `--suppress-all`, `--suppress-rule`, `--prune-suppressions`, `depcruise --baseline` or `ruff --add-noqa` during a scan: each writes into the repo.
- Never report "no growth" without a base: no `BASE`, no history and no `BASE_DIR` is `blocked (no base)`.
- Never print "ratchets hold" without the coverage block. A tool that cannot run is `NOT RUN` / `blocked`, never zero; a rule that matched 0 files is `NOT RUN (vacuous)`.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `convention-oracle` builds the oracle map this skill reads (`rules.tsv`, `exceptions.tsv`, `gates.tsv`, `docs.tsv`, `ages.tsv`) and owns AL-03. `wrapper-adoption-scan` and `naming-layout-scan` own the sites a removed suppression reveals. `align-detect` dispatches this skill; `/align-scan` folds its coverage block into the class ledger; `find-and-align` closes rows (`remove` + fix the site, ratchet enablement at L11, V395).
- `suppression-scan` and `debt-ledger` (code-quality) own correctness suppressions and their accrual; `sast-scan` § 10 (security) owns security suppressions.
- [`precedents/align.md`](../../../../snippets/precedents/align.md) § 2–3, § 16–17, § 20, § 25–26; [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Align V390, V391, V395, V399, V406, V408.
