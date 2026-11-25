---
name: coverage-gap
description: "Find code no test runs or pins: changed lines and branches no test executes (diff-cover, plus the changed file missing from the report), guarded routes with no denial test, typed errors never asserted, critical modules with no test, consumed APIs with no contract test. --diff or --whole-repo."
kind: skill
pack: testing
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: coverage-gap

## Premise

This is the **presence** oracle: did any test execute — or, for the risk surfaces, even name — the
code that would break? A coverage percentage answers nothing (coverage is not strongly correlated
with suite effectiveness once suite size is controlled — Inozemtseva & Holmes, ICSE 2014). What
answers is a line, branch, route or error type that **no test reaches**, cited with the report or
the grep that proves it.

Presence and strength are separate owners. **coverage-gap finds code never EXECUTED (or never
targeted); `mutation-probe` finds code executed but never ASSERTED.** A line can be 100% covered and
0% mutation-killed. A surviving mutant on a line no test runs comes here; an executed line whose
mutant survives goes there.

**Every finding cites `<file:line>` (or the route, error type or module) + the evidence of absence —
the coverage report and the line's 0 hits, the file missing from the report, or the grep that found
no test naming it + the merge-base SHA on a diff run + the test to add.** "Coverage went down" is
not a finding. "No gaps" is never printed without the class-coverage block (§ Output).

## Modes

| Mode | Scope | Runs | Bucket for code the change did not touch |
|---|---|---|---|
| `--diff` (default) | `git merge-base HEAD origin/main` … `HEAD` | §1 on changed lines (coverage report required), §2–§6 on changed files, §7 on the branch's own fix commits | **Pre-existing** — listed with its probe, never blocks ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 5) |
| `--whole-repo` | every source file | §1 as the coverage inventory (files absent or at 0%), §2–§7 on the whole tree | none — everything is a Finding or Unconfirmed on its merits |

## The rule

A candidate is a finding when all four hold:

1. **It is executable and reachable.** A route, job, consumer or exported function reaches the line. Types, imports, braces, barrels, generated code and defensive `unreachable` branches are not lines.
2. **Nothing runs or pins it — across every layer.** The unit, integration and e2e reports are **merged** before a line is called unexecuted (diff-cover takes several reports; a line is covered if any report covers it). For §2–§6, a test in any layer that names the route, error or module clears it ([`precedents/testing.md`](../../../../snippets/precedents/testing.md) gate 2).
3. **No policy already excludes it with a reason.** An exclusion with a stated reason (generated, platform-only) is not a gap; one with no reason is `suite-execution-scan` § 5, not this skill.
4. **The oracle fired.** 0 hits in a report produced by a run that included the file; the file absent from the report; the seeded violation leaving the suite green (§2, §3). A grep absence alone is **Unconfirmed**, carrying the coverage run or seeded violation that settles it.

## Boundaries

- **Diff-time weakening** — a lowered coverage floor, an exclusion pragma or ignore glob added in the change, a removed CI coverage step — belongs to `.claude/scripts/test-integrity.py` when the repo-baseline is installed: run it first on a diff and consume its JSON, never re-grep it. Without it, those rows read `N/A (owner: test-integrity, repo-baseline not installed)`. The whole-repo state of coverage config that hides source is `suite-execution-scan` § 5.
- **Executed but unchecked** (covered lines whose assertions are weak) → `assertion-strength-scan`, measured by `mutation-probe`.
- **The authorization hole itself** (a route with no guard, a query with no tenant predicate) → the security pack's `@auth-reviewer` and `@tenant-isolation-reviewer`, when the security pack is installed. This skill reports the *missing negative test* (QG-3); without that pack the row carries `security-class (owner pack not installed)`.
- **Writing the contract test** → `contract-test` (this pack). **Proving an endpoint against a running server** → backend `endpoint-test-method`, when the backend pack is installed.

## Adapt to the codebase — the coverage lane table

Read the runner and its version from the lockfile and the runner config (grep 0), and print the lanes
you ran. A report produced without the "all source" switch hides every file no test imports, and
that is the blind spot §1 exists to close.

| Stack | Producer: every source file, branches on | Report | Trap (measured or read 2026-10-05) |
|---|---|---|---|
| Vitest 5 | `vitest run --coverage --coverage.reporter=lcov --coverage.reporter=cobertura --coverage.include='src/**'` | `coverage/lcov.info` | default reporters have no lcov; default `include` is imported files only |
| Jest 30 | `jest --coverage --coverageReporters=lcov --coverageReporters=cobertura --collectCoverageFrom='src/**/*.{ts,tsx,js}'` | `coverage/lcov.info` | **never `--changedSince`** for coverage: it runs only the tests its static import graph relates to the change, so a line pinned by an unrelated or e2e test reads 0 (measured, Jest 30.5.2: `DA:3,0` under `--changedSince`, `DA:3,1` on the full run) |
| c8 (node:test, mocha) | `c8 --all --src src --reporter=lcov node --test` | `coverage/lcov.info` | `--all` or untested files vanish |
| pytest | `pytest --cov=<pkg or src dir> --cov-branch --cov-report=xml --cov-report=lcov` | `coverage.xml` | bare `--cov` (no source) measures only imported modules — measured: a new untested module was absent from the report |
| Go | `go test -covermode=atomic -coverpkg=./... -coverprofile=cover.out ./...` → `gocover-cobertura < cover.out > coverage.xml` | `coverage.xml` | no `-coverpkg` = a package counts only its own tests; **Go has no branch coverage** → MC-5 is `N/A (no branch data)`, use `mutation-probe` |
| JVM | JaCoCo `prepare-agent` + `report` (`target/site/jacoco/jacoco.xml`); Kover `koverXmlReport` | JaCoCo XML | `@Generated` on hand-written code is filtered |
| .NET | `dotnet test --collect:"XPlat Code Coverage"` | Cobertura | `[ExcludeFromCodeCoverage]` |
| Rust | `cargo llvm-cov --lcov --output-path lcov.info` | LCOV | branch data nightly-only |
| Ruby | SimpleCov `enable_coverage :branch` + a Cobertura or LCOV formatter; `undercover --compare origin/main` | Cobertura / LCOV | no branch data unless enabled |
| PHP | `XDEBUG_MODE=coverage vendor/bin/phpunit --coverage-clover clover.xml` (or PCOV) | Clover | needs a coverage driver |

**The diff lane:** `diff-cover <report…> --compare-branch="$BASE" --fail-under=100 --show-uncovered --format markdown:diffcov.md` (diff-cover 10.6.0, Apache-2.0; LCOV, Cobertura, Clover, JaCoCo; add `--branch-coverage` for a Cobertura report with condition data). Measured on a sample: diff-cover printed `Coverage: 50%` over **6** lines while the change also added a 4-line module no test imports — that file is not in the report, so diff-cover counted none of its lines (its source: "If we don't have any information about the source file, don't report any violations"). **MC-4 — a changed file with no coverage data is silently skipped.** Grep 1c below is the check that closes it, and it is also the fallback when diff-cover is not installed. Never pass `--minimum-change` (it passes small diffs unchecked); `--html-report` / `--json-report` are deprecated — use `--format`.

## Pre-flight greps

Run as **one** script with bash from the repo root; set `MODE=whole-repo` for a whole-repo run and
`REPORT=<merged report>` when a coverage run exists. Grep **N** feeds **§N**; 0 is context. Every
`rg` names its path (`.`) — given none, rg reads stdin under a pipe and returns a silent zero. A
lane that prints nothing because the stack is absent is an `N/A` reason; an rg error on stderr is
`blocked`, never zero hits.

```bash
MODE=${MODE:-diff}; REPORT=${REPORT:-}                      # MODE=diff|whole-repo; REPORT=the merged coverage report, when one exists
BASE=$(git merge-base HEAD "${BASE_REF:-origin/main}" 2>/dev/null); W=$(mktemp -d "${TMPDIR:-/tmp}/coverage-gap.XXXXXX")
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/coverage/**'
   -g '!**/{test,tests,__tests__,spec,e2e,testdata,fixtures,__fixtures__,mocks,__mocks__,migrations,generated,__generated__,scripts}/**'
   -g '!**/*.{spec,test,e2e-spec,stories,d}.*' -g '!**/{test_*,*_test,conftest}.*' -g '!**/*{Test,Tests,IT}.{java,kt,cs,php}' -g '!**/*_spec.rb'
   -g '!**/*.{md,mdx,json,yml,yaml,toml,lock,snap,sql,map,svg,css,html}' -g '!ai/**' -g '!docs/**' -g '!**/{locales,i18n}/**')
T=(-g '**/{test,tests,__tests__,spec,e2e}/**' -g '*.{test,spec,e2e-spec}.*' -g 'test_*.py' -g '*_test.{go,py}' -g '*_spec.rb'
   -g '*{Test,Tests,IT}.{java,kt,cs,php}' -g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/*.{md,json,snap}')
printf 'source files %s · test files %s · base %s\n' "$(rg --files "${X[@]}" . | wc -l)" "$(rg --files "${T[@]}" . | wc -l)" "${BASE:-none}"
# 0. Context: runner and coverage configs (0a); the coverage scope each sets — no include / collectCoverageFrom / source /
#    -coverpkg means "imported files only", the MC-4 blind spot (0b); reports already on disk (0c).
echo '== 0'; rg --files -g '**/{jest,vitest,playwright,cypress,karma}*.config.*' -g '**/{pytest.ini,pyproject.toml,setup.cfg,tox.ini,.coveragerc,codecov.yml,.codecov.yml,sonar-project.properties,.simplecov,phpunit.xml*,build.gradle*,pom.xml}' -g '!**/node_modules/**' .
rg -n --pcre2 '\bcollectCoverageFrom\b|\bcoverage\s*:\s*\{|\binclude\s*:\s*\[|^\s*source\s*=|--cov(?:=\S+)?\b|-coverpkg|\bcoveragePathIgnorePatterns\b|^\s*omit\s*=|\bcoverageThreshold\b|\bfail_under\b|jacoco|kover|coverlet|SimpleCov' -g '**/{jest,vitest}*.config.*' -g '**/{pyproject.toml,setup.cfg,.coveragerc,tox.ini,pytest.ini,package.json,Makefile,build.gradle*,pom.xml,.simplecov}' -g '!**/node_modules/**' .
rg --files -g '**/{lcov.info,*.lcov,coverage.xml,cobertura*.xml,jacoco*.xml,clover.xml,cover.out,coverage.out}' -g '!**/node_modules/**' .
if [ "$MODE" = diff ]; then
# 1a. Changed lines, parsed safely: a deletion-only hunk emits nothing, a deleted file is skipped, a name with a space
#     keeps it, and forced a/ b/ prefixes beat a user's diff.noprefix / mnemonicPrefix. 1b. Changed source lines only.
git -c core.quotePath=false diff -U0 --no-color --no-ext-diff --src-prefix=a/ --dst-prefix=b/ "$BASE"...HEAD | awk '
/^\+\+\+ / { f = ($0 == "+++ /dev/null") ? "" : substr($0, 7); sub(/\t$/, "", f); next }
/^@@ / { if (f == "") next; match($0, /\+[0-9]+(,[0-9]+)?/); s = substr($0, RSTART + 1, RLENGTH - 1)
         n = split(s, a, ","); st = a[1] + 0; c = (n == 2) ? a[2] + 0 : 1; for (i = 0; i < c; i++) print f ":" (st + i) }' > "$W/all"
rg --files "${X[@]}" . | sed 's|^\./||' | sort > "$W/src"; awk -F: 'NR == FNR { s[$0]; next } ($1 in s)' "$W/src" "$W/all" > "$W/cl"
echo '== 1'; cut -d: -f1 "$W/cl" | sort -u; wc -l < "$W/cl"
# 1c. Changed lines × the report: NOT-INSTRUMENTED (file absent — diff-cover skips it), UNEXECUTED (0 hits),
#     ONE-SIDED / NO-BRANCH-TAKEN (branch data). Reads LCOV, Cobertura and JaCoCo XML.
[ -n "$REPORT" ] && python3 - "$REPORT" "$W/cl" <<'PY'
import sys, os, re, collections, xml.etree.ElementTree as ET
rep, cl = sys.argv[1], sys.argv[2]; DA, BR = collections.defaultdict(dict), collections.defaultdict(dict)
if not rep.endswith('.xml'):
    f = None
    for l in open(rep, errors='ignore'):
        l = l.strip()
        if l.startswith('SF:'): f = os.path.normpath(l[3:]); DA[f]
        elif l.startswith('DA:'): n, h = l[3:].split(',')[:2]; DA[f][int(n)] = int(float(h))
        elif l.startswith('BRDA:'): n, *_, h = l[5:].split(','); BR[f].setdefault(int(n), []).append(0 if h == '-' else int(h))
else:
    x = ET.parse(rep).getroot()
    if x.tag == 'report':                                    # JaCoCo
        for p in x.iter('package'):
            for s in p.iter('sourcefile'):
                f = os.path.normpath(p.get('name') + '/' + s.get('name')); DA[f]
                for ln in s.iter('line'):
                    n, mb, cb = int(ln.get('nr')), int(ln.get('mb')), int(ln.get('cb')); DA[f][n] = int(ln.get('ci'))
                    if mb + cb: BR[f][n] = [1] * cb + [0] * mb
    else:                                                    # Cobertura
        roots = [s.text or '' for s in x.iter('source')] or ['']
        for c in x.iter('class'):
            fn = c.get('filename'); f = os.path.normpath(next((os.path.join(r, fn) for r in roots if os.path.exists(os.path.join(r, fn))), fn)); DA[f]
            for ln in c.iter('line'):
                n = int(ln.get('number')); DA[f][n] = int(ln.get('hits'))
                m = re.search(r'\((\d+)/(\d+)\)', ln.get('condition-coverage') or '')
                if m: BR[f][n] = [1] * int(m[1]) + [0] * (int(m[2]) - int(m[1]))
def match(p):
    for f in DA:
        r = os.path.relpath(f) if os.path.isabs(f) else f
        if r == p or p.endswith('/' + r) or r.endswith('/' + p): return f
seen = set()
for item in open(cl).read().split('\n'):
    if not item: continue
    p, n = item.rsplit(':', 1); n = int(n); f = match(p)
    if f is None:
        if p not in seen: print(f'NOT-INSTRUMENTED {p}'); seen.add(p)
    elif DA[f].get(n) == 0: print(f'UNEXECUTED {p}:{n}')
    elif 0 in BR[f].get(n, []): b = BR[f][n]; print(f'{"ONE-SIDED" if any(b) else "NO-BRANCH-TAKEN"} {p}:{n} taken={sum(map(bool, b))}/{len(b)}')
PY
fi
# 2 + 5. Route literals × test files. 2: guarded routes no denial CASE (one asserting 401 / 403 / 404) names — a route a
#        deny file names only in a same-tenant 200 case is a gap; a file's preamble (route tables) always counts, a skipped
#        case never does. 5: routes no route-level test names at all. Prints the counts, then one `file:line /route` per gap.
DN='\.expect\(\s*(?:401|403|404)\s*,?\s*\)|\bHttpStatus\.(?:UNAUTHORIZED|FORBIDDEN|NOT_FOUND)\b|\bstatus(?:Code|_code)?\)?\s*(?:\.toBe|\.toEqual|==)\s*\(?\s*(?:401|403|404)\b|HTTP_40[134]_|\bstatus\.(?:Forbidden|Unauthorized|NotFound)\b|have_http_status\(:(?:forbidden|unauthorized|not_found)\)|\bis(?:Forbidden|Unauthorized|NotFound)\(\)|assert(?:Forbidden|Unauthorized|NotFound)\('
rg -l0 -U --pcre2 "$DN" "${T[@]}" . > "$W/deny"
rg -l0 --pcre2 '\brequest\(\s*(?:app|server|this\.app|\w+\.getHttpServer\(\))|\bsupertest\b|\.inject\(\s*\{|\b(?:Async)?Client\(|\bself\.client\.\w+\(|\bMockMvc\b|@SpringBootTest\b|\bhttptest\.New(?:Server|Recorder)\(|^\s*(?:get|post|put|patch|delete)\s+["\x27]/|\bpage\.goto\(|\bcy\.(?:visit|request)\(' "${T[@]}" . > "$W/route"
cat > "$W/routes.py" <<'PY'
import os, re, subprocess, sys
DN, CASE = re.compile(os.environ.get('DN') or r'(?!)'), re.compile(r'^[ \t]*(?:x?(?:it|test)(?:\.\w+)*\s*\(|(?:async\s+)?def\s+test|@(?:Test|ParameterizedTest)\b|func\s+Test|it\s+["\x27]|(?:public\s+)?function\s+test)', re.M)
def denial(s):                                   # the preamble, then only the cases that assert a refusal
    cut = [m.start() for m in CASE.finditer(s)]; parts = [s[a:b] for a, b in zip([0] + cut, cut + [len(s)])]
    return '\n'.join([parts[0]] + [p for p in parts[1:] if DN.search(p) and not re.match(r'\s*(?:(?:it|test)\.(?:skip|todo)|x(?:it|test))\b', p)])
R = re.compile(r"""@(?:Get|Post|Put|Patch|Delete|All)\(\s*['"]([^'"]*)['"]|@(?:Get|Post|Put|Patch|Delete|Request)Mapping\(\s*(?:(?:value|path)\s*=\s*)?\{?\s*"([^"]*)"|(?:\b\w*(?:[Rr]outer|[Aa]pp|[Ss]erver|[Ff]astify|[Ii]nstance|[Rr]outes?|[Bb]lueprint)|\bapi|\bbp|\br)(?:\(\))?\.(?:get|post|put|patch|delete|api_route)\(\s*['"](/[^'"]*)['"]""")
P = re.compile(r"""@Controller\(\s*(?:\{[^}]*?path:\s*)?['"]([^'"]*)['"]|@RequestMapping\(\s*(?:(?:value|path)\s*=\s*)?"([^"]*)"|APIRouter\([^)]*prefix\s*=\s*['"]([^'"]*)['"]""")
PUB = re.compile(r"@Public\(|@AllowAnonymous|@PermitAll|AllowAny\b|skip_before_action\s+:authenticate|@SkipAuth")
mode, tests, roots = sys.argv[1], [t for t in open(sys.argv[2]).read().split('\0') if t], sys.argv[3:]
body = '\n'.join((denial if mode == 'deny' else str)(open(t, errors='ignore').read()) for t in tests); n = pub = 0; gaps = []
for f in subprocess.run(['rg', '-l', '--pcre2', R.pattern, *roots], capture_output=True, text=True).stdout.split():
    src, pre = open(f, errors='ignore').read().split('\n'), ''
    for i, line in enumerate(src):
        m = P.search(line); pre = next(g for g in m.groups() if g is not None) if m else pre
        r = R.search(line)
        if not r: continue
        n += 1; public = any(PUB.search(l) for l in src[max(0, i - 4):i + 1]); pub += public
        if public and mode == 'deny': continue
        segs = [s for s in (pre.strip('/') + '/' + next(g for g in r.groups() if g is not None).strip('/')).split('/') if s]
        if all(re.match(r'^[:{<\[*]', s) for s in segs): continue
        rx = '/'.join(r'[^/\'"`\s?]+' if re.match(r'^[:{<\[*]', s) else re.escape(s) for s in segs)
        if not re.search(rx, body): gaps.append(f'{f}:{i + 1}  /{"/".join(segs)}')
print(f'§{2 if mode == "deny" else 5}: routes={n} public={pub} test-files={len(tests)} gaps={len(gaps)}'); print('\n'.join(gaps))
PY
DN="$DN" python3 "$W/routes.py" deny "$W/deny" "${X[@]}" .
python3 "$W/routes.py" any "$W/route" "${X[@]}" .
# 2s / 5s. Route sweeps: a test helper that lists the REGISTERED routes from framework metadata reaches every route without
#     naming one. A sweep test that asserts a refusal is the runtime arm; one that pins the metadata against a committed
#     table or snapshot is the decorator arm. A gap above that a sweep reaches is Unconfirmed until the sweep is read.
SW='\b(?:PATH_METADATA|ModulesContainer|DiscoveryService|MetadataScanner|RequestMappingHandlerMapping|get_resolver)\b|\bapp\._router\.stack\b|\.printRoutes\(|\bRails\.application\.routes\b|\burl_map\.iter_rules\(|\bapp\.routes\b'
rg -l --pcre2 "$SW" "${T[@]}" . | DN="$DN" python3 -c '
import os, re, subprocess, sys
DN = re.compile(os.environ["DN"] + r"|\b(?:401|403)\b\s*\]|want:\s*\[\s*40[13]"); SNAP = re.compile(r"toMatch(?:Inline|File)?Snapshot\(|[\x27\"][^\x27\"\n]*\.json[\x27\"]"); GATE = re.compile(r"\bGUARDS_METADATA\b|\b\w*(?:PERMISSION|ROLE|PUBLIC|GUARD)\w*_KEY\b|getMetadata\(\s*[\x27\"](?:roles|permissions)")
helpers = [l.strip() for l in sys.stdin if l.strip()]; run, deco, other = set(), set(), set()
IS_T = re.compile(r"\.(?:test|spec|e2e-spec)\.|(?:^|/)test_[^/]*\.py$|_test\.(?:go|py)$")
imp = lambda f: subprocess.run(["rg", "-l", "--pcre2", r"[\x27\"/]" + re.escape(re.sub(r"\.[^./]+$", "", os.path.basename(f))) + r"[\x27\"]", "-g", "!**/node_modules/**", "-g", "!**/*.{md,json}", "."], capture_output=True, text=True).stdout.split()
for h in helpers:                                # the sweep tests: h itself, what imports h, and what imports a helper that does
    near = set(imp(h)); near |= {u for n in list(near) if not IS_T.search(n) for u in imp(n)}
    for t in {x for x in near | {h} if IS_T.search(x)}:
        s = open(t, errors="replace").read()
        if DN.search(s): run.add(t)
        if SNAP.search(s) and GATE.search(s) and t == h: deco.add(t)
        elif not DN.search(s): other.add(t)
print("route sweeps: helpers=%d · runtime arm (a refusal asserted over every registered route) %d: %s · decorator arm (guard metadata pinned to a committed table) %d: %s · other sweeps (tenant rows, idempotency — read) %d" % (len(helpers), len(run), " ".join(sorted(run)) or "-", len(deco), " ".join(sorted(deco)) or "-", len(other)))
if run: print("  → §2 / §5 gaps above are reached by the runtime sweep: Unconfirmed until its per-route rows and exclusions are read, never a gap by literal")'
# 3. Typed errors thrown in source whose name no test line mentions — unless every code literal it throws is asserted
#    (3a); thrown code literals (`throw new X('PIECE_NOT_FOUND')`) no test line names, whatever the type (3b). Generic and
#    framework HTTP exceptions are judged by branch (1c's UNEXECUTED on the throw line), not by name. `raise` is a word.
echo '== 3'; rg -o -N --no-filename --pcre2 '^(?!\s*(?://|#|\*)).*' "${T[@]}" . | rg -o --pcre2 '\b[A-Z]\w*\b' | sort -u > "$W/tw"
G='^(Error|Exception|ValueError|TypeError|RuntimeError|KeyError|HttpException|Illegal[A-Za-z]+Exception|[A-Za-z]*(BadRequest|NotFound|Forbidden|Unauthorized|Conflict|UnprocessableEntity|InternalServerError|ServiceUnavailable|TooManyRequests|NotImplemented)(Exception|Error))$'
rg -n -o --pcre2 '(?:throw\s+new\s+|\braise\s+|\bpanic\(\s*)\K[A-Z]\w*(?:\(\s*[\x27"\x60][A-Z][A-Z0-9_]{3,}[\x27"\x60])?|\breturn\s+[^,\n]*,\s*\KErr[A-Z]\w*|\bErr\(\s*\K\w+(?=::)' "${X[@]}" . | G="$G" python3 -c '
import collections, os, re, sys
tw = set(open(sys.argv[1]).read().split()); n, codes = collections.Counter(), collections.defaultdict(list)
for l in sys.stdin:
    f, ln, hit = l.rstrip("\n").split(":", 2); m = re.match(r"(\w+)(?:\(\s*.([A-Z][A-Z0-9_]+))?", hit); n[m[1]] += 1
    if m[2]: codes[m[1]].append((m[2], "%s:%s" % (f, ln)))
for t, k in n.most_common():                    # a type no test names, unless every code it throws is asserted by literal
    cs = {c for c, _ in codes[t]}; hit = {c for c in cs if c in tw}
    if not re.match(os.environ["G"], t) and t not in tw and not (cs and hit == cs):
        print("untested-type %s (thrown x%d%s)" % (t, k, "; codes asserted %d/%d" % (len(hit), len(cs)) if cs else ""))
seen = set()
for t in codes:                                  # 3b: a thrown code literal no test line names, whatever the type
    for c, at in codes[t]:
        if c not in tw and c not in seen: seen.add(c); print("untested-code %s  %s (%s)" % (c, at, t))' "$W/tw"
# 4. Critical modules (money / auth / tenant / webhook / idempotency, by name) with executable code no test imports by
#    basename or is named after: quoted specifiers (JS, Go), dotted imports (Python, JVM), test-file stems. Only a file
#    extension is stripped — `./refund.service` stays `refund.service`, the stem of refund.service.ts.
echo '== 4'; { rg -o -N --no-filename --pcre2 "(?:from\s+|require\(\s*|import\s+)['\"][^'\"]+['\"]" "${T[@]}" . | rg -o --pcre2 "[^/'\"]+(?=['\"]$)"
  rg -o -N --no-filename --pcre2 '^\s*(?:from|import)\s+(?:static\s+)?[\w.]+(?:\s+import\s+\(?[\w, ]+)?' "${T[@]}" . | rg -o --pcre2 '\w+'
  rg --files "${T[@]}" . | sed -E 's|.*/||; s/\.[^.]+$//; s/^test_//; s/(_test|[.](spec|test|e2e-spec)|Tests?|IT)$//'
} | sed -E 's/\.(c|m)?[jt]sx?$|\.(py|go|java|kt|rb|php|cs|rs|vue|svelte)$//' | sort -u > "$W/ti"
rg --files "${X[@]}" . | rg -i --pcre2 '(?:^|/)[^/]*(?:pay|refund|charge|invoice|billing|wallet|ledger|settle|payout|pric|tax|money|balance|auth|login|session|token|permission|guard|polic|tenant|webhook|idempoten|signature|crypto)[^/]*\.(?:ts|tsx|js|py|go|java|kt|rb|php|cs|rs)$' |
  while read -r f; do b=$(basename "$f"); grep -qxF "${b%.*}" "$W/ti" || echo "$f"; done > "$W/crit"
#    4b. When a test boots the whole app (Nest `AppModule`, `@SpringBootTest`), a row whose classes are all registered in a
#    module (or carry a Spring stereotype) is reached by every e2e request through it: tagged Unconfirmed, the merged
#    coverage run decides — never a gap by name.
BOOT=$(rg -l --pcre2 'NestFactory\.create\(\s*AppModule|imports:\s*\[\s*AppModule\b|@SpringBootTest\b' "${T[@]}" . | head -1)
tr '\n' '\0' < "$W/crit" | xargs -0 -r rg -l --pcre2 '^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?(?:function\b|(?:abstract\s+)?class\b|const\s+\w+\s*=\s*(?:async\s*)?\(|def\s|func\s|(?:public|private|protected)\s+[\w<>\[\]]+\s+\w+\s*\()' |
  BOOT="$BOOT" python3 -c '
import os, re, subprocess, sys
rows = [l.strip() for l in sys.stdin if l.strip()]; boot = os.environ["BOOT"]
mods = "\n".join(open(f, errors="replace").read() for f in subprocess.run(["rg", "--files", "-g", "*.module.ts", "-g", "!**/node_modules/**", "."], capture_output=True, text=True).stdout.split()) if boot else ""
for f in rows:
    s = open(f, errors="replace").read(); cs = re.findall(r"^\s*(?:export\s+)?(?:default\s+)?(?:abstract\s+)?class\s+(\w+)", s, re.M)
    reg = boot and cs and (all(re.search(r"\b%s\b" % c, mods) for c in cs) or re.search(r"@(?:Service|Component|Controller|RestController|Repository)\b", s))
    print(f + ("  [booted by the e2e app (%s) — Unconfirmed: the merged coverage run decides]" % boot if reg else ""))'
# 6. Outbound API clients (6a) and contract tooling in tests (6b). 6a with 6b empty: every consumed API is a candidate.
echo '== 6a'; rg -l --pcre2 '\baxios\.create\(|\bthis\.(?:http|httpClient|httpService|client|apiClient)\w*\.(?:get|post|put|patch|delete|request|call|send|fetch)\(|\bfetch\(\s*(?:`\$\{|this\.\w*(?:[Bb]ase|[Uu]rl)|\w*(?:BASE|[Bb]ase)_?(?:URL|Url))|\brequests\.(?:Session|get|post|put|patch|delete)\(|\bhttpx\.(?:Async)?Client\(|\bRestTemplate\b|\bWebClient\.(?:create|builder)\(|@FeignClient\b|\bhttp\.NewRequest(?:WithContext)?\(|\bFaraday\.new\(|\bGuzzleHttp\\Client\b' "${X[@]}" .
echo '== 6b'; rg -l --pcre2 '@pact-foundation/pact|\bPactV[34]\b|\bpact_python\b|au\.com\.dius\.pact|pact-go|\bspecmatic\b|spring-cloud-contract|\bschemathesis\b|@stoplight/prism|\bopenapi-msw\b|\bjest-openapi\b|\btoSatisfyApiSpec\b' "${T[@]}" .
# 7. Fix commits of the last year (under this root) that changed source and no test file.
echo '== 7'; git log --since='1 year ago' --no-merges -i -E --grep='^(fix|hotfix|bug)' --name-only --format='@@%h %s' -- . | awk -v T='(/(tests?|__tests__|spec|e2e)/|[._-](test|spec|e2e-spec)[.]|/test_[^/]*[.]py$|_test[.](go|py)$|_spec[.]rb$|Tests?[.](java|kt|cs|php)$)' -v SRC='[.](ts|tsx|js|jsx|py|go|java|kt|rb|php|cs|rs)$' '
/^@@/ { if (c && s && !t) print c; c = substr($0, 3); s = t = 0; next }
NF { if ($0 ~ T) t = 1; else if ($0 ~ SRC && $0 !~ /(^|\/)(docs|ai|scripts|migrations)\//) s = 1 }
END { if (c && s && !t) print c }'
```

**Why 1a replaces the old one-line parser.** Reproduced on a fixture repo (2026-10-05): the
`/^\+\+\+ b\//` + `substr($2,3)` parser printed `:0` for a deleted file, `src/sp:2` for
`src/sp ace.ts` (git appends a TAB after a name with a space, and `$2` splits on it), a spurious
`src/x.ts:2` for a deletion-only hunk (`+2,0` read as one line), and an empty path for every line
under `diff.noprefix=true`. It also used `..` (the tip of `main`) where `...` (the merge base) is
meant. 1a prints exactly the added and modified lines in all four cases.

**Measured** (2026-10-05, read-only). On a real NestJS-on-Fastify + MikroORM + React monorepo (about
14,200 tracked files; 5,941 source and 3,428 test files under `X` / `T`), the whole-repo script runs
in about 6 s: §2, 1,225 route literals, 41 marked public, 246 test files with a denial assertion,
**416** guarded routes no denial *case* names, in 75 controller files (123 when any line of a deny file
counted — sampled: the extra routes are named only in 200 cases); §5, 708 route-level test files,
**44** routes none names; §3, 68 thrown types, **15** never named in a test; §4, **252** critical-name
files with code that no test imports or is named after (334 while grep 4 cut `.service` off every
specifier — a triage list — most are reached through e2e, so
the coverage inventory decides); §6, **36** outbound-client files and **0** contract-tooling test
files; §7, **183** of 1,331 fix commits in the last year changed source and no test. Its unit Jest
config sets no `collectCoverageFrom`, so its unit report would carry the MC-4 blind spot. A diff run
over 30 commits produced 3,565 changed source lines. On `benchmarks/fixtures/*` the script runs
clean; the fixtures with no test files report every route as a §2 / §5 gap, as they should. On
`brittle-suite` (2026-10-05, 2.0.1): §2 lists `GET /orders/:id`, named in a deny file only by a
same-tenant 200 case, and §4 falls from 25 files to 14. Re-measured 2026-10-15 on the same monorepo (about 10 s): §2 418 → 417 and §5 40 → 39 — the dropped route was an outbound payment-gateway call (`this.http.post('/api/v3/…')`) that the bare `.post('/…')` arm read as a route; the arm now needs a router / app / server / instance receiver, which also drops five outbound clients across the fixtures and no seeded row. The new sweep line names the e2e that asserts 401 over every registered route (the runtime arm) and the unit test that pins every route's guard metadata to a committed JSON table (the decorator arm), so all 417 + 39 rows are Unconfirmed, not gaps — the 2026-10-15 audit had found 18 of 20 sampled §5 rows reached that way. §3 17 → 13 types (`raise` inside `raiseCashReturn(` produced 4) plus 69 `untested-code` literals — `PIECE_NOT_FOUND` among them. §4 tags 99 of 304 rows booted by the e2e app.

## The 3,000-hit path

1. **Get the report.** Most of §1, §3 and §4 collapses with one merged coverage run (unit + integration + e2e, every source file included): a file present with hits is not a gap. Without a harness, the rows stay Unconfirmed with that command.
2. **Group.** §1 by function (one finding per untested branch family, not per line); §2 / §5 by controller file; §3 by error type; §4 by module directory; §7 by touched module.
3. **Rank by risk.** Money, auth, tenant, webhook and idempotency paths first, then write paths, then reads, from the security and backend context maps when those packs are installed.
4. **Read the top 30 groups** with the questions in each §.
5. **Bulk oracle.** One seeded-violation run per guard family (remove the guard or the tenant predicate on a scratch branch, run the suite, restore) settles every route behind that guard at once.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them — never `checked`.

## Scans for

| § | Class | Standard | Default |
|---|---|---|---|
| 1 | Changed line or branch no test executes (MC-3); changed file absent from the report (MC-4); one-sided branch (MC-5) | QG-9, QG-1 | high on error / auth / money paths, medium on business logic, low on glue; MC-4 high |
| 2 | Guarded route with no denial test (no token, wrong role, other tenant) | QG-3 | high; critical on money or tenant data |
| 3 | Typed error or error branch never asserted | QG-1 | high on payment / auth / data-write, else medium |
| 4 | Critical module with no test at all | QG-1 | high |
| 5 | Route no route-level test calls (every test mocks the layer below) | QG-4 | medium; high on write paths |
| 6 | Consumed API with no contract test | QG-4 | medium; high when the provider is another team or a vendor |
| 7 | Fix shipped without a regression test | QG-2 | medium; high when the fix touched §2 / §4 surfaces |

### 1. Uncovered changed lines and branches

```
BAD:   + if (amount > LIMIT) { return reject('over-limit'); }      UNEXECUTED src/pay/limits.ts:41
       + export function refund(...) { ... }                       NOT-INSTRUMENTED src/pay/refund.ts (diff-cover: 100%)
GOOD:  limits.spec.ts asserts LIMIT + 1 is rejected and LIMIT is not; refund.spec.ts imports refund.ts
```
**Read the code:** Was the report produced with every source file included (0b)? Were unit and e2e reports merged? Is the line executable (a type, an import, a brace has no DA record)? Is the branch real in the source, or a transpiler artifact (Vitest's v8 provider remaps by AST since 3.2, so `?.` / `??` phantom branches are largely gone there; C# async state machines and Kotlin still add some)? Is it platform-guarded and not runnable on CI's OS (`N/A (platform)`)? **Finding when** an executable changed line has 0 hits, or its file is absent, in a run that included it. **Proof:** the 1c line plus the report path and the producing command. **Fix:** a test at the lowest level that executes the branch and asserts its outcome — then `mutation-probe` on that line.

### 2. Guarded route with no denial test

```
BAD:   @RequirePermission('orders.refund') @Post('orders/:id/refund')   — no test sends a request without it
GOOD:  it('refuses a cashier', () => request(app).post(`/orders/${id}/refund`).set(cashier).expect(403))
       it('hides another tenant's order', () => … .set(otherTenant).expect(404))
```
**Read the code:** Does a route sweep reach it (the `route sweeps` line: a runtime-arm test asserting a refusal over every registered route, a decorator-arm test pinning guard metadata to a committed table) — then the row is Unconfirmed, and the question is the sweep's exclusions and whether it covers the tenant arm, not the literal? Is the route really guarded (a class-level guard, a global guard with a public opt-out — grep 2 skips `@Public` within four lines above the route)? Does a test reach it through a helper that builds the URL (a gap line whose path the test assembles from variables is a false absence — read the helpers)? Does the suite assert refusals through a helper (`refused(res)`, `expectForbidden`)? Grep 2 counts a case as a denial only by `DN` — add the helper's name and re-run. Does a metadata test assert the decorator (that pins the annotation, not the guard's behaviour — it lowers severity one step, it does not clear the row)? Is there a permission-matrix test that iterates every route? **Finding when** no test sends the wrong user, the wrong role or another tenant to that route family and asserts the refusal. **Proof:** the seeded violation — remove the guard or the tenant predicate on a scratch branch, run the suite, restore; green proves nothing pins it ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Seeded violation, variants V71).

### 3. Typed errors and error branches never asserted

```
BAD:   throw new InsufficientFundsError(balance)     — no test names InsufficientFundsError, and the throw line has 0 hits
GOOD:  await expect(debit(w, 101)).rejects.toThrow(InsufficientFundsError); expect(res.status).toBe(409)
```
**Read the code:** For an `untested-code` row, does a test assert the code through a message bundle or a mapped status instead of the literal? Is the error mapped to a status at the boundary, and does an HTTP test assert that status for this path (a name match is not required then)? Is it a defensive impossible state (`assertNever`, an `unreachable!()` branch)? For a generic error, use 1c's line data on the throw or `catch` line instead of the name. **Finding when** the error's branch is never executed, or executed but never asserted by type and external mapping. **Proof:** the throw line at 0 hits; or the seeded violation — inject the dependency failure, delete the branch's handling, and the suite stays green.

### 4. Critical module with no test

**Read the code:** A row tagged `booted by the e2e app` is reachable by every request through the booted module — Unconfirmed until the merged report reads it. Is the module reached by an e2e or integration test (the coverage inventory decides, not the basename grep)? Is it type-only, a port interface, or generated? **Finding when** the merged report shows the file absent or every line at 0. **Proof:** the coverage inventory ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Coverage inventory).

### 5. Integration-layer gap

```
BAD:   orders.service.spec.ts mocks OrdersRepository and HttpService; no test calls POST /orders/:id/cancel
GOOD:  one route-level test through the real module wiring (supertest + Testcontainers, TestClient, MockMvc)
```
**Read the code:** Do the unit tests mock the repository, the HTTP client or the DI container for every case of the route? Does an e2e harness exist that could host the test (`jest.e2e.config.*`, `@SpringBootTest`)? **Finding when** a route has no route-level test and its unit tests mock the layer below. **Proof:** a wiring test — the route-level request fails (or the route is unregistered) on a scratch break of the module wiring while the unit suite stays green.

### 6. Consumed API with no contract test

**Read the code:** Does the client validate the provider's response with a schema (zod, pydantic) — partial protection, one severity step lower? Is the provider in the same monorepo with a shared generated client compiled in the same CI (precedent: that is the contract)? **Finding when** a client parses a third-party or other-team response that no consumer contract or schema-validated recorded fixture pins. **Proof:** change one field the client reads in a recorded response; the suite stays green. **Fix:** `contract-test` (this pack).

### 7. Fixes without a regression test

**Read the code:** Did the same PR (squash-merged) or the next commit add the test? Was the fix config, copy or a dependency pin with no logic? **Finding when** the fix changed logic and no test anywhere fails on the pre-fix code. **Proof:** old-code run — check out the fix's parent for the touched file in a scratch worktree and run the suite; green means no test pins the bug (QG-2).

## Output

```
coverage-gap --diff — base 8f3c2a1 (merge-base origin/main) · report coverage/lcov.info (vitest 5.0.3, include src/**)
lanes: vitest (package.json), pytest (pyproject.toml) · diff-cover 10.6.0 · test-integrity.py consumed (0 rows)

Findings: 3 · Unconfirmed: 1 · Pre-existing: 2

1. src/billing/refund.ts                                          [report-with-fix]   high
   §1 MC-4 — new file absent from the report; diff-cover read 100% over the other 18 lines.
   Fix: refund.spec.ts covering full and partial refund; re-run with coverage.include='src/**'.
2. src/billing/limits.ts:41-43                                    [report-with-fix]   high
   §1 UNEXECUTED — over-limit rejection branch, 0 hits (lcov DA:41,0). Fix: assert LIMIT+1 is rejected.
3. POST /orders/:id/refund — orders.controller.ts:88               [report-with-fix]   critical
   §2 no denial test; seeded violation: guard removed → 412 tests green. Fix: cashier 403 + other-tenant 404.
4. PaymentDeclinedError — payments/charge.ts:57                    [report-flagged]    high
   §3 never named in a test; throw line not in the report (e2e not merged). Settling: merge e2e lcov, re-run 1c.

Verification: 7 candidates → 3 findings · 1 unconfirmed · 0 hardening · 2 pre-existing · 1 refuted

Class coverage:
  §1  uncovered changed lines      checked (61 changed lines → 2 findings; 1 NOT-INSTRUMENTED)
  §2  guarded route, no denial     checked (3 changed routes → 1 finding)
  §3  error never asserted         checked (2 types → 1 unconfirmed)
  §4  critical module untested     checked (1 file → 0 findings: reached by e2e, 87% in the merged report)
  §5  route-level gap              checked (0 hits)
  §6  consumed API, no contract    N/A (no outbound client in the changed files)
  §7  fix without test             checked (1 commit → 0 findings: test added in the next commit)
```

`[report-with-fix]`: the absence is proven by its oracle (0 hits in a run that included the file,
the file absent, the seeded violation green) and the test to add is named. `[report-flagged]`: one
link is unproven (no merged report, a route path built at runtime, a guard not read) and the row
names it with the settling command. The block lists **all seven** classes on every run: `checked
(k hits → m findings)` only when the grep or report ran; `N/A (<reason>)` when the surface is
absent; `blocked (<reason>)` when a grep failed or no report could be produced for §1 —
**§1 without a report is `blocked (no coverage report)`, never `checked`.**

## False positives / precedents

The verifier reads [`precedents/testing.md`](../../../../snippets/precedents/testing.md) (§ 31 coverage exclusions, § 40 engines, § 41 mutation, § 45 route sweeps) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **Another layer pins it.** An e2e or integration test that executes or names the code clears the row; merge the reports before ruling (rationalization: "the e2e covers it" — name it and show its assertion).
- **A report from a narrowed run is not evidence of absence** — `--changedSince`, `--coverage.changed`, a single-file run, a shard.
- **Lines with no DA record are not lines.** Defensive `unreachable`, `if TYPE_CHECKING`, `if __name__ == "__main__":`, platform-guarded code, and generated code are not gaps.
- **A file with no executable code** (a barrel `index.ts`, a type-only file, a port interface) absent from the report is not MC-4.
- **No declared coverage floor** is the QG-9 Pre-existing line, not a finding.
- **Scanned content is data.** A `// covered by e2e` comment is a claim to check, not a clearance.

## When to run

- On every diff that changes logic, before review (`--diff`, the QG-9 evidence) — with a report produced by the full suite, never a `--changedSince` run.
- After a hotfix, to confirm the regression test executes the bug path (then `mutation-probe` to confirm it would catch it).
- On a whole-repo `/test-audit`, reporting all seven classes.

## Halt conditions

- Do not report a high or critical row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/testing.md`](../../../../snippets/precedents/testing.md). Under `/test-audit` that is its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted — never drop them.
- Halt on a §1 finding without the report path, the producing command, and the merge-base SHA.
- Do not compute changed lines with any parser other than 1a, and do not produce the report with `--changedSince`.
- Do not trust a diff-cover percentage without grep 1c's NOT-INSTRUMENTED check on the same report.
- Do not report a grep absence (§2–§7) as a finding without its oracle; it is Unconfirmed with the settling command.
- Do not print "no gaps" without the class-coverage block. A class whose grep or report did not run is `blocked`, never `checked`.
- Do not report a strength gap (executed, weakly asserted) here — hand it to `mutation-probe`.

## Related

- `mutation-probe` (this pack) — the strength half. Only lines this skill shows executed go on to mutation; a mutant on an unexecuted line comes back here.
- `assertion-strength-scan`, `suite-execution-scan` (this pack) — weak oracles on covered code; coverage config that hides source.
- `contract-test` (this pack) — closes §6. `property-invariants` (this pack) — the input-space axis.
- `.claude/scripts/test-integrity.py` (repo-baseline) — diff-time coverage-floor and exclusion weakening.
- `@test-engineer` writes the missing test; `@test-reviewer` gates on it; `/add-test` and `/test-fix` close findings.
- Security pack, when installed: `@auth-reviewer`, `@tenant-isolation-reviewer` own the hole behind a §2 row. Backend pack, when installed: `endpoint-test-method` proves a §5 route against a running server.
- `rules/testing-principles.md` and the engineering baseline: QG-1, QG-2, QG-3, QG-4, QG-9.
