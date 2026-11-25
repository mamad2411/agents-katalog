---
name: wrapper-adoption-scan
description: "Find live code that bypasses a declared wrapper: raw or banned imports, copies of a named helper, deep imports, a missing required prop or gate."
kind: skill
pack: align
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: wrapper-adoption-scan

## Premise

A project wraps a raw primitive for a reason: the HTTP client attaches auth, the base URL and error mapping; the `Button` carries the tokens and the focus ring; `<Can>` hides an action from a role that may not take it; `formatMoney` rounds one way. A file that imports the raw primitive, re-implements the helper, reaches past a package's public entry, or renders the wrapper without its required prop skips that reason silently. Every test still passes, because the test was written against the call site, not against the invariant the wrapper adds.

This skill replaces `align-detect`'s old Detector 3 ("grep the fingerprint, each hit is a finding") with five runnable classes. It owns **AL-11, AL-13, AL-14, AL-15 and AL-22** of the align class catalog (eval batch 6 § 2). It reads the oracle that `convention-oracle` § 0 builds with `oracle-map.py`, and it never decides which wrapper the project *should* have: a wrapper no T1 or T2 oracle names produces no row.

Below, a spaced `§ n` (as in § 8) is [`precedents/align.md`](../../../../snippets/precedents/align.md) § n; an unspaced `§N` is a detector in this skill.

**Every finding cites the site `<file:line>` + the oracle row that declares the wrapper or the ban (rule id and config path, or a doc `path:line` with its quote) + the wrapper's own path + the proof that would close it + the closure verb.** A grep hit is never a finding by itself. "All wrappers adopted" is never printed without the class-coverage block (§ Output).

## The rule

A candidate is a finding when all four hold ([`precedents/align.md`](../../../../snippets/precedents/align.md), the claim restated):

1. **The oracle is declared.** A T1 rule at `error` in the resolved config of that file (`no-restricted-imports` with a "use X" message, a depcruise `forbidden` rule, Ruff `banned-api`), or a T2 line written by a human (`ai/conventions.md` outside the `refine-enriched` markers, an ADR, CONTRIBUTING, design-system docs). A T2g line (generated, `[inferred:]`, `.claude/codebase-profile.md`) makes the row **Unconfirmed** behind one ratification probe per rule (§ 28). A majority of call sites that happen to use the wrapper is not an oracle (§ 1).
2. **The site is live** and inside the rule's scope: the eslint `files` / `ignores` globs, the depcruise `from.path`, the Ruff config's directory. A rule scoped to client code does not reach a server module (§ 17).
3. **No documented exception covers it**: the wrapper's own implementation, its stories, tests and adapters, and the integration layer the oracle names (§ 8); a type-only import (§ 12); a reasoned suppression or an ADR exception (§ 3); a capability the wrapper does not expose, which is a wrapper gap for `/unify-surfaces`, not drift (§ 9).
4. **The proof holds**: the oracle quote resolves (V389), and the row carries the oracle that will close it (§ Proof).

## Boundaries

- **A native element where a DS component exists** (`<button>` beside the DS `Button`, a hand-rolled `div role="dialog"`): AL-12, ui-ux `design-token-audit` §6, when the ui-ux pack is installed. Without it the class prints `N/A (owner pack ui-ux not installed)`. Align never grades it in the owner's place. Every instance of one surface type behind one wrapper is `/unify-surfaces`.
- **A layer contract**: a module importing across a declared layer map, including a ban whose `from` scope is a layer (depcruise "domain imports no framework"). That is AL-20/AL-21, code-quality `architectural-diagnosis` §1–§2. Code-quality is always installed, so the row prints `owner: code-quality` and is listed here as corroboration only, deduped by `file:line`. Align closes it only as a mechanical re-route through a public surface the oracle names. Rework goes to `/optimize`.
- **A copy that diverged from the named helper**: code-quality `duplication-scan` §1, closed by `/quality-fix` with its divergence test. Align takes only the copy that agrees with the helper (`dedupe` after V403).
- **A dropped a11y convention** (an icon button with no accessible name): frontend `a11y-code-scan` §2, when the frontend pack is installed. Align closes it only in the AL-15 form, when the wrapper itself has the required label prop (§4 below). Without the frontend pack, the native-element case is `N/A (owner pack frontend not installed)`.
- **A raw HTTP call with no error path**: the missing failure handling is code-quality `error-handling-scan` §3–§4. This skill reports only that the call bypassed the declared client.
- **Introducing a wrapper** that does not exist yet, or a new prop on one: `/polish` or `/unify-surfaces`. **A V1→V2 library port**: `/migrate`. **A version bump**: `/upgrade-dep`. **Suppressions of these rules** are AL-29, `convention-ratchet-scan` §1.

## Adapt to the codebase — the oracle tables and the lanes

Build the oracle once per run: `python3 -I <align>/skills/convention-oracle/scripts/oracle-map.py <root> --out=$RUN/oracle`. Its `wrappers.tsv` holds the T1 rows (`raw wrapper kind source message import_names except type_imports`; kind `path`, `pattern`, `regex`, `ban`, `banned-api`; ESLint's narrowing travels with each row: `importNames` / `importNamePattern` and their `allow` forms, the group's `!` re-includes, `allowTypeImports`), `rules.tsv` the scope of each rule, and `exports.tsv` each workspace package's public entries. The agent then writes this skill's own tables into `$RUN/wa/`, never beside oracle-map's files (that folder already holds a `gates.tsv` of version gates). Every row quotes its `docs.tsv` source:

| File | Columns | Filled from |
|---|---|---|
| `wrappers-t2.tsv` | raw · wrapper (empty for a ban) · kind (`module` or `global`) · source · quote · scope · ignores (optional globs, when the line names them: "in `apps/admin`") | T2 rows of `docs.tsv` that reserve a module or a global for one wrapper ("`src/lib/api-client.ts` is the only module permitted to construct an HTTP request"); `_extracted-idioms.md § Wrappers` entries the user confirmed |
| `helpers.tsv` | name · canonical relpath · source | the helper inventory a T2 line names (`_extracted-idioms.md`, "tax lives once in `billing/tax.ts`") |
| `props.tsv` | Tag · prop · source | a declared required prop ("every `DataTable` on a read-only page passes `canDelete={false}`") |
| `gates.tsv` | trigger regex · GateTag · source | a declared gate ("destructive actions are never rendered ungated: wrap in `<Can action>`") |

| Lane | T1 oracle that may exist | Run it (offline, project-local binary only) | Version gate (from the lockfile) | Fallback |
|---|---|---|---|---|
| **JS / TS** (React, Vue, Svelte, Angular, Node) | ESLint core `no-restricted-imports` (`paths`, `patterns`, `message`, `allowTypeImports`); eslint-plugin-boundaries entry points; Nx `enforce-module-boundaries`; depcruise `forbidden` | `node_modules/.bin/eslint -f json` with no `--cache`; `depcruise --output-type json` with no cache | ESLint ≥ 10 reads flat config only, and an `.eslintrc*` beside it is dead config; `@typescript-eslint/no-restricted-imports` is deprecated in favour of core; boundaries v6/v7 renamed its rules (a count jump is a rebaseline, § 3) | greps 1a–1c, 1e, 2, 3, 4 |
| **Python** | Ruff `TID251` `banned-api` (`msg` names the wrapper); import-linter `forbidden` | `ruff check --select TID251 --no-cache --output-format json` | Ruff 0.17 | grep 1d |
| **Go** | golangci-lint `depguard` | the user's own `golangci-lint run` (GPL-3.0: run it, never vendor it) | v2 config schema | grep 1d |
| **Java / Kotlin** (Spring Boot, Ktor) | ArchUnit 1.5, Konsist 0.18 rules in the test tree | the project's test task | — | grep 1d |
| **.NET** (ASP.NET, workers) | BannedApiAnalyzers (`BannedSymbols.txt`) | `dotnet build` | — | grep 1d |
| **Ruby** | packwerk 3.3 privacy and dependency checks | `bin/packwerk check` | `enforce_dependencies: strict` refuses `package_todo.yml` growth | grep 1d |
| **PHP** | deptrac 4.7 | `vendor/bin/deptrac` | the `qossmic/deptrac` package is frozen; read which one is installed | grep 1d |

A tool lane that is installed and runs is the oracle's own verdict: take its JSON and skip the matching grep. A tool that is absent prints `blocked (<tool> not installed)` for its lane, and the greps still run. `--online` installs only into `$RUN/tools` (`npm --prefix`, `NPM_CONFIG_CACHE=$RUN/npm-cache`). Before any CLI: `DO_NOT_TRACK=1 CI=true`. Never `npx -y`.

## Pre-flight greps

Run as **one** script from the audited repo's root (shell state does not survive between tool calls), with `OM=$RUN/oracle WA=$RUN/wa`. Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`.`, run inside each root): given none, `rg` reads stdin under an agent's shell and reports a silent zero. Any `rg` exit 2 prints `blocked`, never zero hits.

```bash
[ -n "${BASH_VERSION:-}" ] || { echo "pre-flight: run it with bash (save it, then bash <file>): PIPESTATUS and arrays are bash-only, and under zsh every exit prints blank"; exit 2; }
OM=${OM:?oracle-map out dir}; WA=${WA:?$RUN/wa}; mkdir -p "$WA"; ROOTS=("$@"); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,.next,.nuxt,.output,.svelte-kit,coverage,storybook-static,vendor,third_party,generated,__generated__}/**'
   -g '!**/*.{min.js,map,lock,snap,md,mdx,json,yml,yaml,svg}' -g '!ai/**' -g '!docs/**')
T=(-g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,stories,.storybook}/**'
   -g '!**/*.{test,spec,e2e,stories,story,mock,test-data,fixture,fixtures,doc}.*' -g '!**/{conftest,*_test,test_*}.*')
J=(-g '*.{js,jsx,ts,tsx,mjs,cjs,mts,cts,vue,svelte,astro}'); TB='(?:[^>{]|\{(?:[^{}]|\{[^{}]*\})*\})*'   # JSX-aware tag body
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#(?!\{)|\{/\*|<!--)')                       # drops comment-only lines
# rg runs INSIDE each root on `.`: -g globs match the path as rg prints it, so `!**/fixtures/**` run from above a root that
# sits under a fixtures/ directory excludes the whole root (measured: 3 files -> 0).
G() { local r o; for r in "${ROOTS[@]}"; do o=$(cd "$r" && rg -n --no-heading --pcre2 "$@" .); [ $? -eq 2 ] && echo "blocked (rg exit 2) in $r" >&2
  [ -n "$o" ] && printf '%s\n' "$o" | sed "s#^\./#${r%/}/#; s#^\./##"; done; return 0; }
# 0a. The module table: wrappers.tsv + wrappers-t2.tsv, one alternation file per 300 modules (a larger generated pattern failed
#     PCRE2 compile in ui-state-scan with exit 2, which a careless reader takes for 0 hits). 0b: Vue global registration to read.
python3 -I - "$OM" "$WA" <<'PY'
import os, re, sys
om, wa = sys.argv[1:3]; mods = {'wrap': set(), 'ban': set(), 'global': set()}
for p in (os.path.join(om, 'wrappers.tsv'), os.path.join(wa, 'wrappers-t2.tsv')):
    for ln in (open(p, encoding='utf-8') if os.path.exists(p) else []):
        c = ln.rstrip('\n').split('\t') + ['', '']
        if ln.startswith('#') or not c[0]: continue
        mods['global' if c[2] == 'global' else 'wrap' if c[1] else 'ban'].add(re.escape(c[0]).replace(r'\*', '[^\'"]*'))
for k, v in mods.items():
    v = sorted(v)
    for i in range(0, len(v), 300): open(os.path.join(wa, 'mods-%s.%02d' % (k, i // 300)), 'w').write('(?:' + '|'.join(v[i:i + 300]) + ')')
PY
G '\b(?:app|createApp\([^)]*\))\.component\(\s*["\x27][\w-]+["\x27]' -g '*.{js,ts,vue}' "${X[@]}" "${T[@]}"
# 1 / 5. Raw or banned module, every import form: 1a value import; 1b the closing line of a multi-line import; 1c require, dynamic
#    import(), re-export; 1d Python, Go, .NET / Java / Kotlin, Ruby, PHP; 1e a reserved global (fetch, XMLHttpRequest, WebSocket).
for f in "$WA"/mods-wrap.* "$WA"/mods-ban.*; do [ -f "$f" ] || continue; M=$(cat "$f")
  G '^\s*import\s+(?!type\b)(?:[^;\n]*?\bfrom\s+)?["\x27]'"$M"'(?:/[^"\x27]*)?["\x27]' "${J[@]}" "${X[@]}" "${T[@]}" \
    | rg -v --pcre2 'import\s+\{\s*(?:type\s+[\w$]+(?:\s+as\s+[\w$]+)?\s*(?:,\s*|(?=\})))+\}' | "${NC[@]}"
  G '^\s*\}\s*from\s+["\x27]'"$M"'(?:/[^"\x27]*)?["\x27]' "${J[@]}" "${X[@]}" "${T[@]}"
  G '\b(?:require|import)\(\s*["\x27]'"$M"'(?:/[^"\x27]*)?["\x27]\s*\)|^\s*export\s+(?!type\b)(?:\*|\{[^}]*\})\s+from\s+["\x27]'"$M"'(?:/[^"\x27]*)?["\x27]' "${J[@]}" "${X[@]}" "${T[@]}" | "${NC[@]}"
  G '^\s*(?:from\s+'"$M"'(?:\.\w+)*\s+import\b|import\s+'"$M"'(?:\.\w+)*\b)' -t py "${X[@]}" "${T[@]}"
  G '^\s*(?:import\s+)?(?:[\w.]+\s+)?"'"$M"'(?:/[^"]*)?"\s*$' -t go "${X[@]}" -g '!**/*_test.go'
  G '^\s*(?:using\s+(?:static\s+)?|import\s+(?:static\s+)?|use\s+)'"$M"'(?:[.\\][\w*]+)*\s*;?\s*$|^\s*require(?:_relative)?\s+["\x27]'"$M"'(?:/[^"\x27]*)?["\x27]' -g '*.{cs,java,kt,php,rb}' "${X[@]}" "${T[@]}"
done > "$WA/hits.raw"
for f in "$WA"/mods-global.*; do [ -f "$f" ] || continue; M=$(cat "$f")
  G '(?<![\w$.])(?:(?:window|globalThis|self)\.)?'"$M"'\s*\(|\bnew\s+'"$M"'\s*\(' "${J[@]}" "${X[@]}" "${T[@]}" | "${NC[@]}"
done >> "$WA/hits.raw"
#    Scope filter: a hit counts only for a rule whose module it imports AND whose scope holds the file (eslint `files`/`ignores`
#    globs; a depcruise `from.path` regex, relative to its config's directory; a T2 row: its optional `scope` / `ignores`
#    columns, else the whole tree), and only where no config of the same tool turns that rule `off` for the file (a package
#    config's `off` is AL-31, `convention-ratchet-scan` §3: the T1 row is not cited there). The wrapper's own file, or its
#    package directory from exports.tsv, is § 8. One row per site: the class is AL-14 when the rule bans a deep subpath, else
#    AL-22 when any matching rule bans the module outright, else AL-11; every matching oracle is joined into the one row.
#    A row narrows as ESLint does: an ESLint `paths` name matches that exact specifier only; a group's `!x` (the `except`
#    column) re-includes x; `import_names` bans only those names (a namespace import binds all of them; `import()` none).
#    Prints: path:line TAB AL-11|AL-14|AL-22 TAB sources TAB text [TAB note]; the rows also land in $WA/rows.tsv.
python3 -I - "$OM" "$WA" <<'PY' | tee "$WA/rows.tsv"
import fnmatch, os, re, sys
om, wa = sys.argv[1:3]
def tsv(p, cols=('raw', 'wrapper', 'kind', 'source', 'quote', 'scope', 'ignores')):
    if not os.path.exists(p): return []
    rows = [l.rstrip('\n').split('\t') for l in open(p, encoding='utf-8')]
    head = [h.lstrip('# ') for h in rows[0]] if rows and rows[0][0].startswith('#') else list(cols)
    return [dict(zip(head, r)) for r in rows if r and r[0] and not r[0].startswith('#')]
cfg = tsv(os.path.join(om, 'rules.tsv')); scope = {r['source']: r for r in cfg}
own = {r['package']: os.path.dirname(r['source']) for r in tsv(os.path.join(om, 'exports.tsv')) if r.get('kind') != 'alias'}
rules = tsv(os.path.join(om, 'wrappers.tsv')) + tsv(os.path.join(wa, 'wrappers-t2.tsv'))
DEEP = re.compile(r'/(?:src|dist|lib|internal|esm|cjs|build)(?:/|\*|$)')
def braces(g):
    m = re.search(r'\{([^{}]*)\}', g)
    return [x for alt in m.group(1).split(',') for x in braces(g[:m.start()] + alt + g[m.end():])] if m else [g]
def glob_rx(g): return re.compile('|'.join(fnmatch.translate(b.replace('**/', '\0').replace('**', '*')).replace('\0', '(?:.*/)?') for b in braces(g)))
def split(s): return [x for x in re.split(r',(?![^{]*\})', s or '') if x]
def holds(r, src, path):   # r: a rules.tsv row, or a T2 row with its own scope / ignores columns
    if not r or not r.get('scope'): return True
    base, ok = os.path.dirname(src.rsplit(':', 1)[0]), False
    for s in split(r['scope']):
        ok |= bool(re.search(s, os.path.relpath(path, base or '.'))) if s.startswith('^') or '(?' in s else bool(glob_rx(s).match(path))
    return ok and not any(glob_rx(i).match(path) for i in split(r.get('ignores')))
STMT = {}
def names_of(path, line):   # the names an import statement binds: default, * (namespace / export *), {a, b as c}; type-only dropped
    if path not in STMT: STMT[path] = open(path, encoding='utf-8', errors='replace').read().split('\n') if os.path.isfile(path) else []
    L, k = STMT[path], line - 1
    while k > 0 and k > line - 40 and not re.match(r'\s*(?:import|export)\b', L[k] if k < len(L) else ''): k -= 1
    st = ' '.join(L[k:line]); out = set()
    if re.search(r'\*\s+as\b|export\s+\*', st): out.add('*')   # a namespace binds every name; import() / require bind none the rule reads
    if re.match(r'\s*import\s+(?!type\b)[\w$]+\s*(?:,|from\b)', st): out.add('default')
    for b in re.findall(r'\{([^}]*)\}', st):
        for sp in b.split(','):
            sp = sp.strip()
            if sp and not sp.startswith('type '): out.add(re.split(r'\s+as\s+', sp)[0].strip())
    return out
def name_hit(spec, names):  # wrappers.tsv import_names: a,b (banned) · /re/ · !a,b (only these allowed) · !/re/
    if not spec: return True
    if '*' in names: return True
    neg = spec.startswith('!'); spec = spec[1:] if neg else spec
    m = (lambda n: re.search(spec[1:-1], n)) if spec.startswith('/') else (lambda n: n in spec.split(','))
    return any((not m(n)) if neg else m(n) for n in names)
def switched_off(rule, path):   # the same tool's rule set `off` by a config whose scope holds the file
    t1 = scope.get(rule['source'])
    if not t1: return ''
    name = t1['rule']
    for r in cfg:
        if r['tool'] == t1['tool'] and r['severity'] == 'off' and r['source'] != rule['source'] and \
           (r['rule'] == name or name.startswith(r['rule'] + ':') or r['rule'] == name.split(':')[0]) and holds(r, r['source'], path):
            return r['source']
    return ''
sites = {}
for hit in sorted(set(open(os.path.join(wa, 'hits.raw'), encoding='utf-8'))):   # a module in both lists greps twice
    path, line, text = hit.rstrip('\n').split(':', 2)
    m = (re.search(r'["\']((?:@[\w.-]+/)?[\w.-][\w./-]*)["\']', text) or
         re.match(r'\s*(?:from|import|using|use)\s+(?:static\s+)?([\w.\\]+)', text)); spec = m.group(1).replace('\\', '.') if m else ''
    for rule in rules:
        raw, wrapper = rule.get('raw', ''), rule.get('wrapper', '')
        hit_mod = (re.search(r'(?<![\w$.])' + re.escape(raw) + r'\s*\(', text) if rule.get('kind') == 'global' else
                   spec == raw if rule.get('kind') == 'path' and re.match(r'(?:.*/)?(?:eslint\.config|\.eslintrc)', rule.get('source', '')) else   # ESLint `paths`: exact
                   fnmatch.fnmatch(spec, raw) or spec == raw or spec.startswith(raw.rstrip('*') + '/') or spec.replace('/', '.').startswith(raw + '.'))
        if not hit_mod or not holds(scope.get(rule['source']) or rule, rule['source'], path) or \
           (wrapper and (path == wrapper or path.startswith(own.get(wrapper, '\0') + '/'))): continue
        if any(fnmatch.fnmatch(spec, x) or spec == x or spec.startswith(x + '/') for x in split(rule.get('except'))): continue   # `!x` in the group
        if rule.get('import_names') and not name_hit(rule['import_names'], names_of(path, int(line))): continue   # importNames / importNamePattern
        s = sites.setdefault((path, int(line)), {'cls': set(), 'src': [], 'off': [], 'text': text.strip()[:110]})
        off = switched_off(rule, path)
        if off: s['off'].append('%s off here (%s)' % (rule['source'], off)); continue
        s['cls'].add('AL-14' if not wrapper and DEEP.search(raw) else 'AL-11' if wrapper else 'AL-22')
        if rule['source'] not in s['src']: s['src'].append(rule['source'])
n_off = 0
for k, s in sites.items():
    if not s['cls']: n_off += 1; continue   # every oracle for the site is switched off: AL-31 input, not a site row
    cls = next(c for c in ('AL-14', 'AL-22', 'AL-11') if c in s['cls'])
    note = '; '.join(sorted(set(s['off'])) + (['also ' + '/'.join(sorted(s['cls'] - {cls}))] if len(s['cls']) > 1 else []))
    print('%s:%d\t%s\t%s\t%s%s' % (k[0], k[1], cls, ' + '.join(s['src']), s['text'], '\t' + note if note else ''))
print('scope filter: %d sites in scope · %d with every oracle switched off (convention-ratchet-scan §3)' % (len(sites) - n_off, n_off), file=sys.stderr)
PY
# 2. A definition of a named helper outside its canonical file.
if [ -s "$WA/helpers.tsv" ]; then H=$(rg -v '^#' "$WA/helpers.tsv" | cut -f1 | paste -sd'|' -)
  G '(?:^|[\s;])(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s*\*?\s*(?:'"$H"')\b|\b(?:const|let|var)\s+(?:'"$H"')\s*(?::[^=\n]+)?=\s*(?:async\s*)?(?:\(|function\b|[\w$]+\s*=>)|^\s*(?:async\s+)?def\s+(?:'"$H"')\s*\(|^func\s+(?:\([^)]*\)\s*)?(?:'"$H"')\s*\(' "${X[@]}" "${T[@]}" \
    | "${NC[@]}" | rg -v -F -f <(rg -v '^#' "$WA/helpers.tsv" | cut -f2 | sed 's/$/:/') | sed 's/^/AL-13\t/'
fi
# 3. A deep import past a public entry of a WORKSPACE package (exports.tsv names them; a third-party deep import such as
#    `@nestjs/schedule/dist/…` is the dependency's business, /upgrade-dep's, never align's), or a relative hop into another
#    package's src. Each is checked against exports.tsv: an exported subpath is not a finding.
WS=$(awk -F'\t' 'NR>1 && $4!="alias" && $1!="" {print $1}' "$OM/exports.tsv" | sort -u | python3 -I -c 'import re,sys; print("|".join(re.escape(l.strip()) for l in sys.stdin if l.strip()) or "(?!)")')
G '\bfrom\s+["\x27](?:'"$WS"')/(?:src|dist|lib|internal|esm|cjs|build)(?:/[^"\x27]*)?["\x27]|\b(?:require|import)\(\s*["\x27](?:'"$WS"')/(?:src|dist|lib|internal|esm|cjs)/|\bfrom\s+["\x27](?:\.\./)+(?:packages|libs|modules)/[\w.-]+/(?:src|lib|internal)/' "${J[@]}" "${X[@]}" "${T[@]}" | "${NC[@]}" \
  | rg -v -F -f <(awk -F'\t' '$2=="AL-14" {print $1":"}' "$WA/rows.tsv") | sed 's/^/AL-14\t/'   # a site the scope filter printed as AL-14 prints once
# 4. A wrapper tag without its required prop (a spread is read, not trusted), and a trigger outside its gate: the gate check
#    counts unclosed <Gate> elements above the hit in the same file.
if [ -s "$WA/props.tsv" ]; then rg -v '^#' "$WA/props.tsv" | while IFS=$'\t' read -r W P _; do
  G -U '<'"$W"'\b(?!'"$TB"'(?:\b'"$P"'\s*=|\{\s*\.\.\.))'"$TB"'/?>' -g '*.{jsx,tsx,vue,svelte,astro}' "${X[@]}" "${T[@]}" | rg --pcre2 '^[^:]+:\d+:' | sed "s/^/AL-15 $W.$P\t/"; done; fi
if [ -s "$WA/gates.tsv" ]; then rg -v '^#' "$WA/gates.tsv" | while IFS=$'\t' read -r TR GT _; do
  G "$TR" -g '*.{jsx,tsx,vue,svelte,astro}' "${X[@]}" "${T[@]}" | python3 -I -c '
import re, sys
gt = sys.argv[1]
for hit in sys.stdin:
    p, n = hit.split(":", 2)[:2]
    pre = "".join(open(p, encoding="utf-8", errors="replace").readlines()[: int(n) - 1])
    if len(re.findall(r"<%s\b(?![^>]*/>)" % gt, pre)) <= len(re.findall(r"</%s\s*>" % gt, pre)): sys.stdout.write("AL-15 ungated " + gt + "\t" + hit)' "$GT"; done; fi
```

A gate row's trigger is written from the oracle's own words. For "destructive actions are never rendered ungated" with no list of destructive verbs, the default trigger is `<(?:Button|IconButton|button)\b(?=TB(?:\bvariant=["'](?:danger|destructive)["']|\bonClick=\{[^}]*\b(?:delete|remove|refund|destroy|revoke|purge)\w*))` (with `TB` written out). Three blind spots are structural, so work around them rather than trust a quiet grep:
- **A wrapper reached through a barrel** (`export * from 'ky'` in `src/lib/index.ts`) moves the raw import one hop. Grep 1c lists re-exports, so read the barrel's consumers.
- **A raw call through an alias** (`const http = axios.create()` in a feature file) shows as one import line. The import is the finding; the alias's call sites are its evidence.
- **A gate applied by a higher-order wrapper** (`withPermission(Component)`, a route guard) is invisible to the tag count. Read the route before calling a hit ungated.

**Measured** 2026-10-18 on `benchmarks/fixtures`:
- `web-dashboard`: no lint config, so `wrappers.tsv` has 0 rows. The T2 rows come from `docs.tsv`: `ai/conventions.md:19` reserves HTTP for `src/lib/api-client.ts`, and `:49` declares the `<Can>` gate.
  - Grep 1e (`fetch`) gives 4 raw lines → 1 after the scope and own-file filter: the seeded raw `fetch` in a detail panel (WEB-IMPORT-01). The 3 others are inside the client itself (§ 8).
  - Grep 4 (the gate) gives 2 lines: the seeded ungated action (WEB-PERM-01) and its icon-button twin three lines above.
  - §2, §3 and §5: `N/A` (no helper inventory, no workspace exports, no ban).
- `quality-mix`: depcruise `domain-is-framework-free` (T1-noci: no CI job runs depcruise) bans 5 modules from `^src/domain`.
  - Grep 1/5 gives 54 raw import lines → 1 after the scope filter: `api/src/domain/pricing.ts:1`, `@prisma/client` (seed QM-AR-03). A layer contract, so it is routed to `architectural-diagnosis` §1.
  - §2 with the two helpers `ai/architecture.md:24` names (`computeTax`, `prorate`): 4 definitions → 2 outside the canonical files, one in the web checkout and one in the billing worker. Both diverged (QM-DU-02, QM-DU-01), so both go to code-quality.
- `a11y-states`, `frontend-correctness`: no wrapper oracle (0 wrapper rows; 0 and 1 T2g doc rows), so every class is `N/A (no declared wrapper)`.
- `convention-drift` (staged copy, re-run 2026-10-18 after the scope-filter fix; the agent-filled tables written from `ai/conventions.md`: 11 wrapper / ban rows, the admin store-library bans scoped to `apps/admin/**` and `fetch` scoped away from `apps/web/src/server/**` by the doc's own words, 3 helpers, 2 required props, the `<Can>` gate): **13 of 13 seeds** (CD-AL11-a…e, AL13-a/b, AL14-a/b, AL15-a/b, AL22-a/b). 30 raw import lines (29 distinct: `moment` sits in both lists) → **21 rows at 21 sites**, one per site (17 AL-11, 2 AL-14, 2 AL-22), against 41 lines before the fix. Fixed: a T1 + T2 pair now prints one row citing both; the admin sites and `export.py` cite only the doc, with `eslint.config.mjs:29 off here (apps/admin/eslint.config.mjs:12)` and `pyproject.toml:5 off here (:12)` as the note; the date helper's import prints once as AL-22; the two deep imports print once as AL-14 (grep 3 drops a site the scope filter already printed). CD-AL22-b depends on the table naming the store library the admin allowlist line excludes, since that line names no library. CD-DECOY-01 (the PDF helper, ADR-0007) prints and only the § 1 read drops it; DECOY-02 and DECOY-16 are dropped by the own-package and scope filters. The 9 other in-scope sites carry an inline disable or a baseline entry (`convention-ratchet-scan` § 1–2 owns those). Owner hits printed, not credited: a hook (CD-HO-CQ-b, code-quality) and a cart row component (CD-HO-FE-c, frontend).
- A synthetic tree (ESLint flat `no-restricted-imports` with a path and a `@radix-ui/*` pattern scoped to `apps/web/**/*.{ts,tsx}`, Ruff `banned-api` for `requests`): all 5 seeded value imports were found (default, multi-line aliased, dynamic `import()`, `import requests`, `from requests.adapters import`). Not reported: 2 type-only imports, 1 commented import, `requests_toolbelt`, and the wrapper package's own `ky` import. One deep import into `@acme/ui/src/internal/` was found.
- A real NestJS + React monorepo (read-only, re-measured 2026-10-18 after the fold-back fixes, the same agent-filled `wrappers-t2.tsv` / `helpers.tsv`): **3,147 rows → 386**. The 2,740 AL-22 rows of the pages wall's `fetch*` rule (`importNamePattern: '^fetch[A-Z]'` on `@/**`, `./**`, `../**`, read before as "every import") → 0: no View imports a `fetch*` name (a dynamic `import()` binds no name the rule reads). The 21 imports of the contracts package's vocabulary subpath, which the domain and application walls re-include with `!…/vocab` → 0 (the bare-name `paths` row matched every subpath). Grep 3: 2 third-party deep imports (`<framework>/dist/…`, no oracle) → 0. The 386 left are the T2 table rows (376 toast-library imports a doc routes through a wrapper — an AL-04 doc question, 8 raw `fetch`, 2 `Intl`). `convention-drift` with the T1 tables only: 17 in-scope sites → 16, the dropped one `dayjs/plugin/relativeTime` (an ESLint `paths` name is exact; the doc's T2 `dayjs` row still reaches it when the tables are filled); seed CD-AL11-d (`import('dayjs')`) still prints.
- Three silent failures were found and fixed while measuring:
  - Grep 3 first took `..` for a package name and listed every `../lib/api` import as a deep import: 3, 5, 15 and 17 false lines on the four fixtures, 0 after the fix.
  - A `-g '!**/fixtures/**'` exclusion run from above a root that sits under `benchmarks/fixtures/` excluded the whole root. That is why the script runs `rg` inside each root.
  - The scope filter first split `apps/web/**/*.{ts,tsx}` at the comma inside the braces, and Python `import requests` carries no quotes: 5 in-scope hits → 0. Brace globs are now expanded and unquoted module names read.

## The 3,000-hit path

A monorepo with a broad ban (`@radix-ui/*` → `@acme/ui`) can return thousands of lines. Triage in this order, and record every step in the coverage block:

1. **Intersect with the oracle.** Keep only hits the scope filter assigned to a T1 or T2 rule. Hits under a T2g rule collapse to **one** ratification line per rule ("confirm `ai/conventions.md:41` — 212 sites"), never N rows (§ 28).
2. **Group** by (rule, specifier or helper name): `cut -f2,3 | sort | uniq -c`. One decision covers a group, and the group key is the `consistency` key the fix's sweep gate checks (V393).
3. **Rank** by the newest files first (new code is copied next), then churn (`git log --format= --name-only --since=6.months` with `GIT_OPTIONAL_LOCKS=0`), then user-visible and permission-bearing surfaces (a gate or auth wrapper first).
4. **Read the top 30 groups fully**: one member per group, the wrapper's prop types, and the rule's scope.
5. **Ratchet the rest.** Propose the class rule at `error` with a bulk-suppression baseline (ESLint `--suppress-rule no-restricted-imports`, core since 9.24; depcruise `--baseline`), and report `Live, ratcheted (k groups / n hits)`. Where no ratchet exists, report `Live, unreviewed (k groups / n hits)` with the command that continues them. Never mark them `checked`.

## Scans for

Severity is never Critical: these are convention findings. **High** only when the bypassed wrapper carries a permission, tenant or auth behaviour, or when a measured a11y failure follows. Otherwise **Medium**, and **Low** for a deep import into a package the repo owns end to end.

| § | Class | Default |
|---|---|---|
| 1 | AL-11 raw primitive imported where the declared wrapper exists | medium; high when the wrapper attaches auth, tenant or permission |
| 2 | AL-13 hand-rolled copy of a named helper | medium |
| 3 | AL-14 deep import past a package's public entry | medium; low inside one package's own tests and tools |
| 4 | AL-15 wrapper without a required prop, or a destructive action outside the declared gate | medium; **high** for a gate |
| 5 | AL-22 forbidden or non-allowlisted library | medium |

### 1. Raw primitive where the wrapper exists (AL-11)

```
BAD:   import ky from 'ky'                         // oracle: no-restricted-imports "use @acme/http" (eslint.config.mjs:31)
       import { Root as DialogRoot } from '@radix-ui/react-dialog'     ·  await import('dayjs')  ·  import requests
       fetch(`/api/orders/${id}`)                  // oracle: "api-client.ts is the only module permitted to construct an HTTP request"
GOOD:  import { http } from '@acme/http'  ·  import { Dialog } from '@acme/ui'  ·  formatDate(d)  ·  from app.http_client import get
```
**Read the code:** Does the wrapper export an equivalent for every member the site uses (its `exports`, its re-export list)? If it does not, the row is a wrapper gap → `/unify-surfaces` (§ 9). Is the site the wrapper's own file, story, test or adapter, or the integration layer the oracle names (§ 8)? Is the import type-only (§ 12)? Is the site inside the rule's scope (§ 17)? Does a reasoned disable cover it (§ 3)? **Finding when** a live, in-scope value import or reserved-global call names the raw module, and the wrapper covers what it uses. **Proof:** V400 (import count outside the wrapper's exempt files = 0 after the fix) + a render or call test of the site. The swap is **EQ** when the wrapper's defaults reproduce the raw call's props or options (a prop-diff table read from the wrapper's types), else **VC** (V407).

### 2. Hand-rolled copy of a named helper (AL-13)

```
BAD:   export function computeTax(input) { … }      // in web/src/cart/tax-estimate.ts; the oracle names billing/tax.ts
GOOD:  import { computeTax } from '@acme/billing'  // one implementation
```
**Read the code:** Is the copy a re-export or a thin call into the canonical helper (not a copy)? Run code-quality's `duplication-scan/scripts/clones.py` against the canonical file for renamed (type-2/3) copies the name grep misses. Do the two agree on every input the copy's call sites pass (locale, rounding, time zone, empty input)? A copy in another runtime that cannot import the helper (a Python worker beside a TS API) is context-split (§ 17): report it to code-quality as a divergence candidate, never `dedupe`. **Finding when** a live copy of a helper the oracle names exists outside the canonical file. **Proof:** V403, a differential test (copy vs canonical on the copy's call-site inputs). If they agree: `dedupe`, then knip or `dead-code-scan` shows no orphan. If they diverge: reclassify to code-quality `duplication-scan` §1 → `/quality-fix` (a behaviour change, never a structural row).

### 3. Deep import past the public entry (AL-14)

```
BAD:   import { trapFocus } from '@acme/ui/src/internal/focus-trap'   ·   from '../../../packages/http/src/retry'
GOOD:  import { trapFocus } from '@acme/ui'        // or a subpath `exports` declares: '@acme/ui/focus'
```
**Read the code:** Is the subpath in the package's `exports` (`exports.tsv`)? If it is, the import is public and not a finding. Does a per-app tsconfig alias map the path back to the public entry? Reuse `rank-source-files.py`'s alias and workspace-exports resolution (`~/.claude/scripts/`, code-quality's graph); never re-derive it. Is the importer the package's own test or tooling (§ 11)? **Finding when** a live import resolves into another package's internal path that its `exports` (or the declared entry rule) does not publish. **Proof:** V404, the import resolves through the public entry, and the whole-repo boundary tool is green on every module.

### 4. Wrapper without its required prop, or an action outside its gate (AL-15)

```
BAD:   <DataTable rows={audit} />                  // oracle: read-only pages pass canDelete={false}
       <Button variant="danger" onClick={() => refund(order)}>   // oracle: destructive actions are never rendered ungated
GOOD:  <DataTable rows={audit} canDelete={false} />  ·  <Can action="orders.refund"><Button variant="danger" …/></Can>
```
**Read the code:** Is the prop supplied through a spread (`{...tableProps}`)? Read the spread's source. Does a higher-order wrapper or a route guard apply the gate? Is the wrapper's default already the declared value (then the prop is redundant, not missing)? For a gate: which `action` string does the oracle require, and does `<Can>` exist with that ability? Ast-grep 0.51 expresses the required-prop rule exactly (`kind: jsx_opening_element` named W, `not: has: jsx_attribute` P; for gates, `not: inside:` a `jsx_element` whose opening name is the gate). Write it with BAD/GOOD cases and run `sg test` (Noisy and Missing must be 0) before trusting it over grep 4. **Finding when** a live wrapper element lacks the declared prop, or a declared trigger renders outside the declared gate. **Proof:** V401, a render test with the role that must not see the action (it fails first: the action renders), then the gate or prop added. FN class (`add-gate` with the declared `<Can>`). An AL-28 a11y row closes here only when the wrapper itself requires the label prop.

### 5. Forbidden or non-allowlisted library (AL-22)

```
BAD:   import moment from 'moment'                 // oracle: depcruise forbidden to node_modules/moment
       import { create } from 'zustand'            // oracle: "state: Pinia only" (apps/admin/README, T2)
GOOD:  formatDate(d)  ·  defineStore(…)
```
**Read the code:** Is the site the adapter that wraps the allowed library, or a migration shim an ADR dates (§ 8, § 16)? Is the ban scoped to a layer of a declared layer map? Then it is a layer contract → `architectural-diagnosis` §1 (§ Boundaries). Is the allowlist doc T2 or generated T2g? **Finding when** a live, in-scope value import names a library the oracle bans or omits from its allowlist. **Proof:** V400, the import count outside the allowlist and the adapter = 0.

## Proof

The oracles, their harnesses and the whole-class variants are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Align: V400 (import count to zero), V401 (wrapper render / gate test), V403 (dedupe differential), V404 (boundary whole-repo), and V389 (the oracle quote resolves) on every row. The fix runs `find-and-align`'s ladder: the row's `detector_cmd` is the exact grep line above, narrowed to the row's rule, so `align-sweep-gate.py redetect` can re-run it. **Whole-class variants** a fix must survive: named, default, namespace, aliased and type-mixed imports; re-export; dynamic `import()`; `require`; a barrel hop; a Vue global registration; Python `from x import y` and `import x`; a reserved global through `window.`; a spread prop; a gate applied by a route guard.

## Output

```
wrapper-adoption-scan — lanes: js/ts (eslint 10.13.0 flat, no-restricted-imports 3 paths / 1 pattern), python (ruff 0.17.1 TID251);
  go, .net, ruby, php absent · oracle: T1 4 wrapper rows · T2 2 (wrappers-t2.tsv) · T2g 1 (unratified) · helpers 3 · gates 1

Findings: 2 · Unconfirmed: 1

1. apps/web/src/features/orders/api.ts:3                         [report-with-fix]   medium
   §1 AL-11 raw primitive — `import ky from 'ky'`; oracle: eslint:no-restricted-imports at error for apps/web/**
   (eslint.config.mjs:31, "use @acme/http"). @acme/http exports get/post with the same options (prop-diff: 0).
   Proof: V400 count 1 → 0; render test of OrdersPage. Fix: replace-with-shared → import { http } from '@acme/http'. EQ.

2. apps/web/src/features/orders/OrderRow.tsx:41                  [report-with-fix]   high
   §4 AL-15 gate drop — `<Button variant="danger" onClick={refund}>` outside <Can>; oracle: ai/conventions.md:49
   "Destructive actions are never rendered ungated." Proof: V401, render as role=viewer — the button renders (fails first).
   Fix: add-gate with <Can action="orders.refund"> (src/components/ui/Can.tsx). FN.

3. apps/admin/src/stores/cart.ts:1                               [report-flagged]    medium
   §5 AL-22 — `import { create } from 'zustand'`; oracle: .claude/codebase-profile.md:12 "state: Pinia only" (T2g, generated).
   Unconfirmed until ratified: confirm .claude/codebase-profile.md:12 (1 site).

Routed: api/src/domain/pricing.ts:1 `@prisma/client` → owner: code-quality (architectural-diagnosis §1, layer contract)
        web/src/cart/tax-estimate.ts:11 computeTax copy diverges (reverse charge) → owner: code-quality (duplication-scan §1)
AL-01: 1 candidate row dropped (quote absent from ai/conventions.md)
Verification: 9 candidates → 2 findings · 1 unconfirmed · 2 hardening · 0 pre-existing · 4 refuted

Class coverage:
  §1 AL-11 raw primitive     checked (31 raw hits → 7 in scope → 1 finding; 6 in packages/http, the wrapper itself)
  §2 AL-13 helper copy       checked (3 helpers, 5 definitions → 2 outside canonical → 0 findings, 1 routed, 1 re-export)
  §3 AL-14 deep import       checked (4 hits → 0 findings; 4 subpaths exported by @acme/ui)
  §4 AL-15 prop / gate       checked (1 gate rule, 6 hits → 1 finding) · props: N/A (no declared required prop)
  §5 AL-22 banned library    checked (2 bans, 3 hits → 1 unconfirmed, 1 routed, 1 adapter)
```

`[report-with-fix]`: the oracle row resolves at T1 or T2, the site is in scope and live, the wrapper covers it, and the proof and the closure verb are named. `[report-flagged]`: one link is unproven (a T2g oracle, a spread not read, a wrapper whose coverage of the used member is unknown), and the row names that link and its settling probe. The coverage block lists **all five** classes on every run: `checked (k → m)` only when the grep or tool lane ran; `N/A (<reason>)` when no oracle declares the class (no wrapper, helper, prop or ban rows); `blocked (<reason>)` when a grep exited 2 or a tool failed; `Live, unreviewed` / `Live, ratcheted (k groups / n hits)` for a partial review. Every row carries `oracle:`, `al_class:`, `detector_cmd:` and `proof_class:` for the ledger.

## False positives / precedents

The verifier reads [`precedents/align.md`](../../../../snippets/precedents/align.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10 (the maintainability / conventions column). The ones this skill meets most:
- **The wrapper's own implementation**, its stories, tests and adapters, and the integration layer the oracle names (§ 8).
- **A wrapper gap**: the raw primitive is used for a capability the wrapper does not expose. Route it to `/unify-surfaces` and cite the missing prop or export (§ 9).
- **Composition roots and DI wiring** (§ 10), **tests importing internals** (§ 11), **type-only imports** (§ 12).
- **A rule's own narrowing** (§ 32): `importNames` / `importNamePattern`, a group's `!` re-include, `allowTypeImports`, and an ESLint `paths` name that matches one exact specifier.
- **Context split**: a rule scoped to client code and a server module, a CLI package, another runtime (§ 17). **Frozen or generated code** (§ 16).
- **A majority is not an oracle**: 40 of 41 files using `@acme/http` does not make the 41st a finding if nothing declares the wrapper (§ 1). A generated idiom line is a proposal (§ 28).

## When to run

- Dispatched by `align-detect` on every whole-repo run, and on a diff that adds or changes an import, a JSX element of a declared wrapper, a helper definition, or a package `exports` map.
- Dispatched by `/align-scan` (the audit) and re-run per row by `find-and-align` as the row's `detector_cmd` (V391).
- After a wrapper is introduced by `/unify-surfaces` or `/polish`: the new wrapper becomes a T2 row, and this skill finds the sites that still bypass it.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. Under `/align-scan` that happens in its verification phase. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any row without `oracle:` that resolves (`oracle-map.py quotes`): it is dropped and counted as AL-01, never reported.
- Halt on a wrapper, helper, prop or gate this run inferred from call-site counts. Only T1 and T2 rows produce findings, and T2g rows produce one ratification probe.
- Do not report a grep hit as a finding, and do not dismiss a group without reading one member. A class whose grep exited 2 is `blocked`, never `checked`.
- Do not edit code. This skill is read-only on the audited repo and writes only under `$RUN`.
- Do not re-derive a class another skill owns (§ Boundaries); cross-link it.

## Related

- `convention-oracle` (this pack) builds the oracle map (`oracle-map.py`) every row cites, and runs the AL-01 quote check on this skill's rows.
- `align-detect` (this pack) dispatches this skill; `/align-scan` folds its coverage block into the AL ledger; `find-and-align` closes its rows through the proof ladder and `align-sweep-gate.py`.
- `naming-layout-scan` and `convention-ratchet-scan` (this pack): naming and placement (AL-16–19), and suppressions or ratchets of these rules (AL-29–32).
- `design-token-audit` §6 (ui-ux, when installed) owns AL-12. `architectural-diagnosis` §1–§2 and `duplication-scan` §1 (code-quality) own layer contracts and diverged copies. `a11y-code-scan` §2 (frontend, when installed) owns a dropped accessible name.
- `/unify-surfaces` builds or extends a wrapper; `/polish` introduces one that does not exist.
