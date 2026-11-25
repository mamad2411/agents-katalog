---
name: suite-execution-scan
description: Find tests that never run or never fail CI — focus and ownerless skips, files no runner collects, suites no CI job runs, masked exit codes, coverage config that hides code, retries with no flaky gate — each proved by a collection list or a CI canary.
kind: skill
pack: testing
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: suite-execution-scan

## Premise

A green CI run says nothing about a test that never ran, and nothing about a suite whose failure the
job is told to ignore. These are the cheapest defects in a test suite to prove and among the most
damaging: the test exists, it was reviewed, it reads as coverage, and no regression can ever turn it
red. Six shapes produce them — a focused test that hides the rest, a skip nobody owns, a file no
runner collects (or a whole suite no CI job invokes), a CI job or runner switch that turns failure
into success, coverage configuration that hides shipped code, and retries that pass a flake as
green.

This skill reports the **current state** of the suite and its CI. Diff-time weakening — a skip, a
focus, a lowered floor or a removed CI step *added by a change* — is
`.claude/scripts/test-integrity.py`'s. Whether the tests that do run can fail is
`assertion-strength-scan`'s.

**Every finding cites the line that stops the test from running or from failing (`<file:line>`) +
the tests or suite it affects + the CI job that runs them, or the fact that none does + the proof
(the collected list, the canary, the static fact) + the fix and the guard that keeps it fixed.**
A grep hit is never a finding. "Every test runs" is never printed without the class-coverage block
(§ Output).

## The rule

A candidate is a finding when all four hold:

1. **It affects a test that matters.** The skipped, uncollected or masked test claims a behaviour in shipped code — not a helper, an abstract base, a fixture or a deliberately excluded directory ([`precedents/testing.md`](../../../../snippets/precedents/testing.md) § 32).
2. **It holds in the CI job, not only on a laptop.** Read the job that runs the suite: its command, its env (`CI`, the variables a gated suite needs), its shell, its `if:` and path filters, its shard matrix. A suite no job runs is the finding itself (§ 3).
3. **Nothing already neutralises it.** A runtime guard (`forbidOnly`, `--forbid-only`, `xfail_strict`, `--fail-on-risky`, a flaky gate), an error-level lint rule that CI runs, or another job that runs the same tests.
4. **It is not intended and owned.** A skip with a reason, a tracker link and a condition; an advisory job with an owner and an end date; a scheduled workflow that runs the out-of-gate suite (§ 25–29). Intent with no owner or no expiry is still a finding.

## Boundaries

- **New instances in a diff** (an added skip or `.only`, a lowered coverage threshold, a CI test step removed or given `|| true`) → `.claude/scripts/test-integrity.py` (G2) when the repo-baseline is installed. On a diff run, consume its JSON and dedupe by `<file:line>`; this skill reports the state around it.
- **Project-level gates** — QG-7 (no `.only`; a skip carries an owner and a delete-by date) and QG-13 (CI blocks on the tests) — are checked per change by `standards-check.py`; this skill is their whole-repo inventory and covers every stack, where the QG-7 check reads JS focus only.
- **Whether the collected tests can fail** → `assertion-strength-scan` (this pack). **Changed lines no test executes** → `coverage-gap` (this pack). **Flake sources and root causes** → `flake-source-scan` (this pack) and `/flaky-test-hunt`; this skill reports only the retry configuration that hides them (§ 6) and the `--forceExit` switch as masking (§ 4).
- **CI design** (caching, job graph, secrets, runner images) → `@ci-reviewer` when the devops pack is installed; this skill reads CI only for whether tests run and can fail.
- **Suppressions inside test code** — a test-lint rule disabled inline (`eslint-disable jest/expect-expect`, `jest/no-focused-tests`, `# noqa: PT011`, `//nolint:testifylint`) and a silenced `console.error` (`jest.spyOn(console, 'error').mockImplementation(…)`) that hides an error the test should fail on → `suppression-scan` § 2 when the code-quality pack is installed. Without it, list them here as candidates under § 4 tagged `suppression (owner pack not installed)`; never drop them. This skill owns the lint rules switched off or left at warn **in config** only as far as they mask focus and skips (§ 1).

## Adapt to the codebase

Inventory the runners, their configs and the CI files first (grep 0); the verdict of every class
depends on which job runs which config. Print the lanes in the output header.

| Stack | Collected-list oracle (§ 3) | Focus / skip guard (§ 1–2) | Masking switches to look for (§ 4) | Retry and its flaky gate (§ 6) |
|---|---|---|---|---|
| **Jest** 30 | `npx --no jest --listTests --config <cfg>` | no runtime guard: eslint-plugin-jest `no-focused-tests` (error), `no-disabled-tests` (warn) with `--max-warnings 0` | `--passWithNoTests`, `--forceExit` (an un-awaited failing assertion passes under it) | `jest.retryTimes(n)` — no flaky gate |
| **Vitest** | `npx --no vitest list --filesOnly` | `allowOnly` (read the version's default and the CI env); @vitest/eslint-plugin `no-focused-tests` | `--passWithNoTests` | `retry`, `--retry` — no flaky gate |
| **Playwright** 1.63 | `npx --no playwright test --list` | `forbidOnly: !!process.env.CI` | — | `retries` + `--fail-on-flaky-tests` |
| **Mocha** | `mocha --dry-run` | `--forbid-only --forbid-pending` | — | `this.retries(n)` |
| **pytest** 9 | `pytest --collect-only -q`; `-W error::pytest.PytestCollectionWarning` | `-o xfail_strict=true` | `-p no:warnings`, `PYTHONOPTIMIZE` | `--reruns`, `@pytest.mark.flaky` — no flaky gate |
| **Go** | `go test -list '.*' ./...` (and with each build tag) | — | `-run` hard-coded | `gotestsum --rerun-fails` |
| **JVM** | Surefire / Failsafe reports; `*IT` runs only under Failsafe | — | `-DskipTests`, `testFailureIgnore`, `ignoreFailures` | Surefire `rerunFailingTestsCount` + `failOnFlakeCount` (default 0 = unlimited); Gradle test-retry + `failOnPassedAfterRetry` (default false) |
| **Ruby** | `rspec --dry-run --format json` | `RSpec/Focus`; `filter_run_when_matching :focus` audited | — | rspec-retry `retry:` |
| **PHP** | `phpunit --list-tests` | — | `failOnRisky` / `failOnEmptyTestSuite` false (the 13.4 defaults), `--do-not-fail-on-*` | — |
| **.NET** | `dotnet test --list-tests` | — | — | `[Retry]` attributes |
| **Rust** | `cargo test -- --list` | — | — | nextest `retries` + `--flaky-result fail` |

The Jest, Vitest and pytest list commands were run on 2026-10-05; the others are from the research
catalog and the runners' CLI help, not run here — confirm their output shape on the repo's toolchain
before diffing against it.

## Pre-flight

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep
**N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`.`): `rg` with no path
reads stdin whenever stdin is a pipe, which under an agent's shell is a silent zero-hit run. Any
`rg` error on stderr (exit 2) is a failed grep, never zero hits.

```bash
V=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/coverage/**')
T=(-g '**/*.{test,spec,e2e-spec,int-spec,flow,cy}.{js,jsx,ts,tsx,mjs,cjs,mts,cts}' -g '**/__tests__/**/*.{js,jsx,ts,tsx}' -g '**/{test_*,*_test}.py'
   -g '**/*_test.go' -g '**/*{Test,Tests,IT,TestCase}.{java,kt}' -g '**/*{Test,Tests}.{php,cs}' -g '**/*.rs')
C=(--hidden -g '.github/workflows/*.{yml,yaml}' -g '**/.gitlab-ci*.yml' -g '**/Jenkinsfile*' -g '.circleci/*.yml' -g '**/azure-pipelines*.yml'
   -g '**/bitbucket-pipelines.yml' -g '.buildkite/**/*.{yml,yaml}' -g '**/package.json' -g '**/{Makefile,*.mk,tox.ini,noxfile.py}' -g '**/scripts/**/*.sh' -g '!**/node_modules/**')
K=(-g '**/{jest,vitest,playwright,cypress,karma,wdio}*.config.{js,cjs,mjs,ts,mts,cts,json}' -g '**/vite.config.{js,ts,mjs,mts}' -g '**/.mocharc*'
   -g '**/{pytest.ini,pyproject.toml,setup.cfg,tox.ini,.coveragerc}' -g '**/phpunit.xml*' -g '**/{pom.xml,build.gradle,build.gradle.kts}'
   -g '**/.config/nextest.toml' -g '**/{.nycrc*,.c8rc*,codecov.yml}' -g '**/package.json' -g '!**/node_modules/**')
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/*.min.*' -g '!*.{md,mdx,json,snap,lock}'
   -g '!**/docs/**' -g '!**/{test,tests,spec,e2e,__tests__,__mocks__,__fixtures__,testdata,generated,__generated__}/**' -g '!**/*{.,_}{test,spec}.*' -g '!**/test_*.py' -g '!**/migrations/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')        # drops comment-only lines
TC='\b(?:jest|vitest|mocha|playwright\s+test|cypress\s+run|pytest|tox|go\s+test|gotestsum|mvn|gradlew?|rspec|phpunit|pest|dotnet\s+test|cargo\s+(?:test|nextest)|(?:npm|pnpm|yarn)\s+(?:run\s+)?test[\w:-]*|turbo\s+run\s+test)\b'
TMP="$(mktemp -d "${TMPDIR:-/tmp}/suite-scan.XXXXXX")"
# 0. Context: runner configs (0a); every test command CI files and scripts run (0b).
rg --files "${K[@]}" . | rg -v 'package\.json$'
rg -n --no-heading --pcre2 "$TC" "${C[@]}" . | "${NC[@]}" | rg -v --pcre2 '^[^:]+:\d+:\s*"[@\w./-]+"\s*:\s*"[~^<>=]*\d'          # minus dependency pins

# 1. §1 focus: focused tests (1a); focus guards in runner config, lint config and CI (1b); name filters hard-coded in the
#    commands CI runs (1c).
rg -n --pcre2 '^\s*(?:it|test|describe|context|suite|specify)\.only\s*\(|^\s*(?:fit|fdescribe|fcontext|ftest|fspecify)\s*\(|@pytest\.mark\.only\b' "${T[@]}" "${V[@]}" . | "${NC[@]}"
rg -n --pcre2 '^\s*(?:fit|fdescribe|fcontext|focus)\s+["\x27]|(?:,|\()\s*(?::focus\b|focus:\s*true)' -g '**/*_spec.rb' "${V[@]}" . | "${NC[@]}"
rg -n --pcre2 'forbidOnly\s*:|allowOnly\s*:|--forbid-only|--forbid-pending|no-focused-tests|no-exclusive-tests|RSpec/Focus|filter_run_when_matching' -g '**/{eslint.config.*,.eslintrc*,.rubocop.yml,.rspec,spec_helper.rb}' "${K[@]}" "${C[@]}" . | "${NC[@]}"
rg -n --pcre2 "$TC"'[^\n]*\s(?:-t|--testNamePattern|--grep|-g|-k|-run|--filter|-m)[ =]["\x27]?[\w^$|.-]' "${C[@]}" . | "${NC[@]}"

# 2. §2 skips: skips and disables, every stack (2a; Ruby on *_spec.rb only, 2b); suites gated on an env var or a
#    capability, inline or helper-built — `const d = HAS_X ? describe : describe.skip` in a test-dir helper, `(sel() ? describe
#    : describe.skip)(` (2c — read whether the CI job provides it; rg the helper's name for the specs it gates); non-strict
#    xfail and the strict switch (2d).
rg -n --pcre2 '^\s*(?:it|test|describe|context|suite|specify)\.(?:skip|todo|fixme)\s*\(|^\s*(?:xit|xdescribe|xtest|xcontext|xspecify)\s*\(|@pytest\.mark\.(?:skip|xfail)\b|\bpytest\.(?:skip|xfail)\(|@unittest\.skip|\bself\.skipTest\(|^\s*pytestmark\s*=.*\bskip|\bt\.Skip(?:f|Now)?\(|@(?:Disabled\w*|Ignore)\b|\[(?:Fact|Theory)\([^\]]*\bSkip\s*=|\[Ignore\b|#\[ignore\b|->markTest(?:Skipped|Incomplete)\(' "${T[@]}" "${V[@]}" . | "${NC[@]}"
rg -n --pcre2 '^\s*(?:xit|xdescribe|xcontext|xspecify|skip|pending)\b' -g '**/*_spec.rb' "${V[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '\b(?:describe|it|test|suite)\.(?:skipIf|runIf)\s*\(|\?\s*(?:describe|it|test)(?:\.\w+)?\s*:\s*(?:describe|it|test)\.skip\b|\?\s*(?:describe|it|test)\.skip\s*:\s*(?:describe|it|test)\b|@pytest\.mark\.skipif\([^)]*\b(?:environ|getenv)\b|os\.(?:Getenv|LookupEnv)\([^)\n]*\)[^\n]*\n?[^\n]*t\.Skip|^//go:build\s+[^\n]*\b(?:integration|e2e|slow|manual)\b|@(?:EnabledIf|DisabledIf)EnvironmentVariable|\bassume(?:True|That)\([^)\n]*getenv|\bprocess\.env\.V1_REPO_PATH\b|\bHAS_V1\b' "${T[@]}" -g '**/{test,tests,__tests__,e2e}/**/*.{js,ts,mjs,cjs,mts,cts}' "${V[@]}" . | "${NC[@]}"
# 2c-TSV. The gate table other packs read (the migration pack's parity-proof-scan: a parity suite gated on V1 presence is
#    NOT-RUN unless CI provides the variable). One row per gate: kind (v1 | env | capability), file:line, the helper (or
#    `inline`), the condition, its env vars (every constant hop followed, imports too), ci_sets per CI job (yes | partial | no
#    | unknown over the `*` jobs — name or commands name the files' directory — then `<file>#<job>[*]=<vars|->`), the specs
#    that use the helper. GATES_TSV=<path> picks the file (default $TMP/gated-suites.tsv); the path is printed.
cat > "$TMP/gates.py" <<'PY'
import glob, os, re, subprocess, sys
G = ['-g', '**/*.{test,spec,e2e-spec,int-spec}.{js,jsx,ts,tsx,mjs,cjs,mts,cts}', '-g', '**/{test,tests,__tests__,e2e,spec}/**/*.{js,ts,mjs,cjs,mts,cts,py}',
     '-g', '**/{test_*,*_test,conftest}.py', '-g', '!**/node_modules/**', '-g', '!**/dist/**', '-g', '!**/.venv/**']
rd = lambda p: open(p, errors='replace').read()
files = subprocess.run(['rg', '--files'] + G + ['.'], capture_output=True, text=True).stdout.split()
src = {f: re.sub(r'(?m)^[ \t]*(?://|#(?!\[)|\*|/\*).*$', lambda m: ' ' * len(m.group(0)), rd(f)) for f in files}   # comment lines blanked
CONST = re.compile(r'(?:const|let|var)\s+(\w+)\s*(?::[^=\n]+)?=\s*([^;\n]+)')
GCONST = dict(kv for s in src.values() for kv in CONST.findall(s))      # an imported HAS_V1 resolves through its own file
def jobs(p):   # [(job id, env-visible text, name + commands)]; workflow-level env / variables reach every job; `services:` env does not
    t = re.sub(r'(?m)^[ \t]*#.*$', '', rd(p)); b = os.path.basename(p); m = re.search(r'(?m)^jobs:[ \t]*$', t)
    if m and not b.startswith('.gitlab'):                                # GitHub Actions, CircleCI
        top = ''.join(re.findall(r'(?m)^(?:env|environment):[ \t]*\n((?:[ \t]+\S.*\n?)*)', t)); body = re.split(r'\n(?=\S)', t[m.end():])[0]
        ind = re.search(r'(?m)^([ \t]+)[\w.-]+:[ \t]*$', body); parts = re.split(r'(?m)^%s([\w.-]+):[ \t]*$' % (ind.group(1) if ind else '  '), body)
        return [('%s#%s' % (b, n), top + re.sub(r'(?m)^([ \t]*)services:[ \t]*\n(?:\1[ \t]+.*\n?)*', '', x), n + ' ' + x) for n, x in zip(parts[1::2], parts[2::2])]
    if b.startswith('.gitlab'):
        d = dict(zip(*[iter(re.split(r'(?m)^([^\s#][^:\n]*):[ \t]*$', t)[1:])] * 2)); top = d.get('variables', '')
        ext = lambda x: x + ''.join(d.get(e, '') for e in re.findall(r'extends:\s*\[?\s*([.\w-]+)', x))
        return [('%s#%s' % (b, n), top + ext(x), n + ' ' + ext(x)) for n, x in d.items() if not n.startswith('.') and n not in
                ('variables', 'stages', 'default', 'include', 'workflow', 'image', 'services', 'before_script', 'after_script', 'cache')]
    return [(b, t, t)]
JOBS = [j for g in ('.github/workflows/*.y*ml', '**/.gitlab-ci*.yml', '**/Jenkinsfile*', '.circleci/*.yml', '**/azure-pipelines*.yml',
        '**/bitbucket-pipelines.yml', '.buildkite/**/*.y*ml') for p in glob.glob(g, recursive=True) for j in jobs(p)]
GENERIC = {'', '.', 'src', 'test', 'tests', '__tests__', 'spec', 'specs', 'e2e', 'apps', 'app', 'packages', 'libs', 'lib', 'support', 'helpers',
           'utils', 'api', 'web', 'server', 'client', 'v1', 'v2'}
def ci_sets(env, paths):   # per job: does it set a gate variable, and does it run these files (`*`: its name or commands name their directory)
    if not env or not JOBS: return 'NO-CI-FILE' if env else 'n/a'
    segs = {x for p in paths for x in os.path.dirname(p).split('/') if x.lower() not in GENERIC}
    per = [(n, [e for e in env if re.search(r'(?m)^\s*-?\s*%s\s*[:=]|\b%s=' % (e, e), et)], any(re.search(r'(?<![\w-])%s(?![\w-])' % re.escape(x), run) for x in segs))
           for n, et, run in JOBS]
    pool = [j for j in per if j[2]] or per; k = sum(bool(j[1]) for j in pool)
    v = ('yes' if k == len(pool) else 'partial' if k else 'no') if pool is not per or len(per) == 1 else ('unknown' if k else 'no')
    return v + ' ' + ' '.join('%s%s=%s' % (n, '*' if r else '', ','.join(s) or '-') for n, s, r in per[:8]) + (' +%d' % (len(per) - 8) if len(per) > 8 else '')
HELPER = re.compile(r'(?:export\s+)?(?:const|let|var)\s+(\w+)\s*(?::[^=\n]+)?=\s*\(?\s*([^?;\n]+?)\s*\)?\s*\?\s*((?:describe|it|test)(?:\.\w+)?)\s*:\s*((?:describe|it|test)(?:\.\w+)?)\b')
INLINE = re.compile(r'\(\s*([^?;\n()]+(?:\([^()\n]*\))?)\s*\?\s*(describe|it|test)(?:\.skip)?\s*:\s*(?:describe|it|test)(?:\.skip)?\s*\)\s*\(|\b(?:describe|it|test|suite)\.(skipIf|runIf)\s*\(([^\n]*?)\)\s*\(')
PYSKIP = re.compile(r'(?:^|\n)\s*(?:(\w+)\s*=\s*)?@?pytest\.mark\.skipif\(([^\n]*)\)')
ENV = re.compile(r'process\.env(?:\.(\w+)|\[\s*[\'"](\w+)[\'"]\s*\])|import\.meta\.env\.(\w+)|os\.(?:environ\.get|getenv|environ\[)\s*\(?\s*[\'"](\w+)[\'"]')
rows = []
for f in files:
    s = src[f]; consts = dict(re.findall(r'(?m)^(\w+)\s*=\s*([^\n]+)', s) if f.endswith('.py') else []); consts.update(CONST.findall(s))
    def gate(expr):   # follow the constant chain to the env read: HAS_V1 -> Boolean(V1_REPO_PATH) -> process.env.V1_REPO_PATH
        text, todo, seen = [expr], [(n, 0) for n in re.findall(r'\b[A-Za-z_]\w*\b', expr)], set()
        while todo and len(seen) < 50:
            n, far = todo.pop()   # far: reached through an imported constant, so read in the defining file's scope
            if n in seen: continue
            seen.add(n); v = consts.get(n) if not far else None
            v = v or (GCONST.get(n, '') if far or re.search(r'\bimport\b[^;]*\b%s\b' % n, s) else ''); far = far or n not in consts
            if v: text.append(v); todo += [(x, far) for x in re.findall(r'\b[A-Za-z_]\w*\b', v)]
        return sorted({x for t in ENV.findall(' '.join(text)) for x in t if x})
    hits = [(m.start(), m.group(1), m.group(2)) for m in HELPER.finditer(s) if '.skip' in m.group(3) + m.group(4)]
    hits += [(m.start(), 'inline', m.group(1) or m.group(4)) for m in INLINE.finditer(s)]
    hits += [(m.start(), m.group(1) or 'inline', m.group(2)) for m in PYSKIP.finditer(s)]
    for pos, helper, expr in hits:
        env = gate(expr)
        v1 = re.search(r'V1', ' '.join(env + [expr, helper]))
        users = [u for u in files if helper != 'inline' and len(re.findall(r'\b%s\b' % re.escape(helper), src[u])) > (u == f)]
        rows.append(('v1' if v1 else 'env' if env else 'capability', '%s:%d' % (f, s.count('\n', 0, pos) + 1), helper, ' '.join(expr.split())[:80],
                     ','.join(env) or '-', ci_sets(env, [f] + users), str(len(users)), ','.join(users[:5]) or '-'))
out = os.environ.get('GATES_TSV') or os.path.join(sys.argv[1], 'gated-suites.tsv')
with open(out, 'w') as fh:
    fh.write('# suite-gates 2\tkind\tat\thelper\tcondition\tenv\tci_sets\tusers\tuser_files\n')
    fh.writelines('\t'.join(r) + '\n' for r in rows)
for r in rows: print('GATE ' + '  '.join(r[:7]))
print('gated-suites TSV: %s (%d gates: %d v1, %d env, %d capability)' % (out, len(rows), *(sum(r[0] == k for r in rows) for k in ('v1', 'env', 'capability'))))
PY
python3 "$TMP/gates.py" "$TMP"
rg -n --pcre2 '@pytest\.mark\.xfail\b(?![^\n]*strict\s*=\s*True)|xfail_strict\s*=' -g '**/*.py' -g '**/{pytest.ini,pyproject.toml,setup.cfg,tox.ini}' "${V[@]}" . | "${NC[@]}"

# 3. §3 never collected, never run: test-looking files no Jest / Vitest / Playwright config claims (3a); test scripts no
#    CI file invokes (3b); never-collected shapes per stack — Go names and signatures, pytest classes with __init__ and
#    off-pattern names, JUnit 4 under Jupiter and private / static / non-void tests, docblock @test, non-public .NET (3c);
#    `*IT` classes no Failsafe runs (3d).
cat > "$TMP/claims.py" <<'PY'
import os, re, subprocess
fs = lambda d: subprocess.run(['rg', '--files', '-g', '!**/node_modules/**', '-g', '!**/dist/**', d], capture_output=True, text=True).stdout.split()
LOOK = re.compile(r'[._-](?:test|spec|e2e-spec|e2e|it|flow|cy)\.[cm]?[jt]sx?$|/__tests__/.+\.[cm]?[jt]sx?$')
cfgs = subprocess.run(['rg', '--files', '-g', '**/{jest,vitest,playwright}*.config.{js,cjs,mjs,ts,mts}', '-g', '!**/node_modules/**', '.'], capture_output=True, text=True).stdout.split()
def glob_rx(g):                                   # a runner glob → a regex: ** / * / ? / [..] / {a,b} / ?(x) +(x) @(x) *(x)
    o, i = '', 0
    while i < len(g):
        c = g[i]
        if g.startswith('**/', i): o += '(?:.*/)?'; i += 3; continue
        if g.startswith('**', i): o += '.*'; i += 2; continue
        if c in '?+@*' and g[i + 1:i + 2] == '(':
            j = g.index(')', i); o += '(?:' + glob_rx(g[i + 2:j]).replace('\\|', '|') + ')' + {'?': '?', '+': '+', '@': '', '*': '*'}[c]; i = j + 1; continue
        if c == '{': j = g.index('}', i); o += '(?:' + '|'.join(glob_rx(p) for p in g[i + 1:j].split(',')) + ')'; i = j + 1; continue
        if c == '[': j = g.index(']', i); o += g[i:j + 1]; i = j + 1; continue
        o += '[^/]*' if c == '*' else '[^/]' if c == '?' else re.escape(c); i += 1
    return o
def strip(s):                                     # comments (a `/*` inside a glob string is not one), then coverage / typecheck / benchmark blocks
    s = re.sub(r'(?:^|(?<=\s))/\*[\s\S]*?\*/', '', s); s = re.sub(r'(?m)(?:^|(?<=\s))//[^\n]*', '', s)
    for m in reversed(list(re.finditer(r'\b(?:coverage|typecheck|benchmark)\s*:\s*\{', s))):
        d, j = 0, m.end() - 1
        for j in range(m.end() - 1, len(s)):
            d += {'{': 1, '}': -1}.get(s[j], 0)
            if d == 0: break
        s = s[:m.start()] + s[j + 1:]
    return s
RXLIT = r'(?<![\w)\]])/((?:\\.|\[[^\]\n]*\]|[^/\\\n\[])+)/[dgimsuyv]*'
def value(s, key):                                # every `key: <expr>` → the expression (an array across lines, else to the line end)
    for m in re.finditer(r'\b' + key + r'\s*:\s*', s):
        rest = s[m.end():]
        if rest.startswith('['):
            d = 0
            for j, ch in enumerate(rest):
                d += {'[': 1, ']': -1}.get(ch, 0)
                if d == 0: yield rest[:j + 1]; break
        else: yield re.split(r',\s*(?:\n|$)|\n', rest, 1)[0]
claimed, dirs = set(), set()
for c in cfgs:
    s = strip(open(c, errors='replace').read()); d = os.path.dirname(c); dirs.add(d); pw = 'playwright' in os.path.basename(c)
    consts = dict(re.findall(r'\b(?:const|let|var)\s+(\w+)\s*=\s*([^;\n]+)', s))
    roots = re.findall(r"['\"]<rootDir>/([^'\"]+)['\"]", ' '.join(value(s, 'roots'))) + re.findall(r"testDir\s*:\s*['\"]([^'\"]+)", s)
    rx = [x.replace('\\\\', '\\') for x in re.findall(r"testRegex\s*:\s*['\"]([^'\"]+)['\"]", s)]
    globs = []
    for key in ('testMatch', 'include'):          # include: Vitest's test.include (coverage.include is stripped); testMatch: Jest / Playwright
        for e in value(s, key):
            e = ' '.join([e] + [consts.get(w, '') for w in re.findall(r'\b[A-Za-z_]\w*\b', e)])   # a ternary or a named constant: every branch
            rx += re.findall(RXLIT, re.sub(r"(['\"`])(?:\\.|(?!\1).)*\1", '""', e))
            globs += [g for g in re.findall(r"['\"`]([^'\"`\n]*[*/.][^'\"`\n]*)['\"`]", e) if not g.startswith('!')]
    if not rx and not globs: rx = [r'\.(?:test|spec)\.[cm]?[jt]sx?$'] + ([] if pw or 'vitest' in c else [r'/__tests__/.+\.[cm]?[jt]sx?$'])   # the runners' default shapes
    grx = [glob_rx(g.lstrip('./')) for g in globs]
    for f in fs(d):
        rel = os.path.relpath(f, d)
        if roots and not any(rel.startswith(r.strip('./').rstrip('/') + '/') for r in roots if '.' not in os.path.basename(r)): continue
        rels = [rel] + [os.path.relpath(f, os.path.join(d, r)) for r in roots if '.' not in os.path.basename(r)]
        if any(re.search(r, f) for r in rx) or any(re.fullmatch(g, x) for g in grx for x in rels): claimed.add(os.path.normpath(f))
    print('config %-44s roots=%s match=%s globs=%s' % (c, roots or '-', rx or '-', globs or '-'))
for d in sorted(dirs):
    for f in fs(d):
        if LOOK.search(f) and os.path.normpath(f) not in claimed: print('UNCLAIMED', f)
PY
python3 "$TMP/claims.py"
cat > "$TMP/ci-reach.py" <<'PY'
import glob, json, re
ci = ''.join(open(p, errors='replace').read() for g in ('.github/workflows/*.y*ml', '**/.gitlab-ci*.yml', '**/Jenkinsfile*', '.circleci/*.yml', '**/azure-pipelines*.yml', '**/bitbucket-pipelines.yml', '.buildkite/**/*.y*ml') for p in glob.glob(g, recursive=True))
if not ci: print('NO-CI-FILE — no workflow found; every test script below runs only by hand')
for pj in glob.glob('**/package.json', recursive=True):
    if 'node_modules' in pj: continue
    for name, cmd in (json.load(open(pj)).get('scripts') or {}).items():
        if not re.match(r'test(?:$|:)', name) or 'watch' in name + cmd: continue
        cfg = re.findall(r'--config[ =](\S+)', cmd)
        hit = re.search(r'(?:run\s+|\s)' + re.escape(name) + r'(?![\w:-])', ci) or any(c in ci for c in cfg) or (name == 'test' and re.search(r'\b(?:turbo|nx)\s+run\s+test\b|(?:pnpm|npm|yarn)\s+(?:-r\s+|run\s+)*test\b', ci))
        print('%-9s %-36s %-18s %s' % ('in-CI' if hit else 'NOT-IN-CI', pj, name, cmd[:90]))
PY
python3 "$TMP/ci-reach.py"
rg -n --pcre2 '^func\s+(?:Test(?=[a-z])\w*|test[A-Z_]\w*)\s*\(\s*\w+\s+\*?testing\.T\s*\)|^func\s+Test\w*\s*\(\s*\w+\s+testing\.T\s*\)' -g '**/*_test.go' "${V[@]}" .
rg -n -U --pcre2 '^class\s+Test\w*[^\n]*:\s*\n(?:[ \t]+[^\n]*\n|[ \t]*\n)*?[ \t]+def\s+__init__\b|^def\s+Test_\w*\(' -g '**/{test_*,*_test}.py' "${V[@]}" . | rg --pcre2 '^[^:]+:\d+:\s*(?:class|def)\b'
rg -l --pcre2 '^\s*(?:async\s+)?def\s+test\w*\s*\(' -g '**/{tests,test}/**/*.py' -g '!**/{test_*,*_test,conftest,__init__}.py' "${V[@]}" .
rg -n -U --pcre2 '^import\s+org\.junit\.Test\s*;|@(?:org\.junit\.jupiter\.api\.)?(?:Test|ParameterizedTest|RepeatedTest)\b[^\n]*\n(?:\s*@[^\n]*\n)*\s*(?:(?:public|protected)\s+)?(?:private\b|static\b|(?!void\b)(?:int|long|boolean|String|Object|[A-Z]\w*(?:<[^>]*>)?)\s+\w+\s*\()' -g '**/*{Test,Tests,IT,TestCase}.{java,kt}' "${V[@]}" . | rg --pcre2 '^[^:]+:\d+:\s*(?:import|@)'
rg -n --pcre2 '<artifactId>(?:junit-vintage-engine|maven-failsafe-plugin|junit-jupiter\w*)</artifactId>|\bjunit-vintage-engine\b' -g '**/{pom.xml,build.gradle,build.gradle.kts}' "${V[@]}" .
# 3d. A missing config has no line, so this is a presence check: an `*IT` class under a Maven pom where neither that pom nor
#     any pom above it declares maven-failsafe-plugin or a Surefire `<include>` of `*IT` — Surefire's defaults never run it.
rg --files -g '**/*IT.{java,kt}' "${V[@]}" . | while IFS= read -r f; do d=$(dirname "$f"); p=; ok=
  while :; do [ -f "$d/pom.xml" ] && { p=${p:-$d/pom.xml}; rg -q --pcre2 'maven-failsafe-plugin|<include>[^<]*IT\b[^<]*</include>' "$d/pom.xml" && ok=1; }
    [ "$d" = . ] || [ "$d" = / ] && break; d=$(dirname "$d"); done
  [ -n "$p" ] && [ -z "$ok" ] && rg -n --pcre2 '^\s*(?:(?:public|internal|open|final)\s+)*class\s+\w+IT\b' "$f" | sed "s|^|NO-FAILSAFE $f:|; s|\$|  (pom: $p)|"
done
rg -n --pcre2 '@test\b|^\s*(?:private|protected)\s+function\s+test\w*\(' -g '**/*Test.php' "${V[@]}" . | "${NC[@]}"
rg -n --pcre2 '\[(?:Fact|Theory|Test|TestMethod|TestCase)\b[^\]]*\]\s*(?:\[[^\]]*\]\s*)*(?!public\b)(?:(?:private|internal|protected)\s+)?(?:static\s+)?(?:async\s+)?(?:void|Task)\s+\w+\(' -g '**/*.cs' "${V[@]}" .

# 4. §4 CI masking: a job allowed to fail, or a test command whose failure the shell swallows (4a); test output piped
#    without pipefail (4b); runner switches that turn a failure or an empty run into success (4c); triggers and `if:`
#    that can skip the test job (4d).
rg -n --pcre2 '^\s*(?:continue-on-error|allow_failure)\s*:\s*(?:true|\$\{\{)|'"$TC"'[^\n]*(?:\|\|\s*(?:true|:|exit\s+0)\b|;\s*exit\s+0\b)' "${C[@]}" . | "${NC[@]}"
rg -n --pcre2 "$TC"'[^\n|]*\|\s*(?:tee|grep|tail|head|sed|awk|go-junit-report|tparse)\b' "${C[@]}" . | "${NC[@]}"
rg -n --pcre2 -e '--passWithNoTests|passWithNoTests\s*:\s*true|--pass-with-no-tests|--no-tests=pass|failOnEmptyTestSuite="false"|--do-not-fail-on-(?:risky|warning|empty-test-suite)|failOn(?:Risky|Warning|Incomplete)="false"|beStrictAboutTestsThatDoNotTestAnything="false"|-DskipTests\b|-Dmaven\.test\.(?:skip|failure\.ignore)=true|<testFailureIgnore>\s*true|<skipTests>\s*true|ignoreFailures\s*=\s*true|\btest\s*\{\s*enabled\s*=\s*false|-p\s+no:warnings|--disable-warnings|-W\s+ignore\b|--forceExit\b|\bPYTHONOPTIMIZE\b|\bpython3?\s+-O{1,2}\b' "${C[@]}" "${K[@]}" . | "${NC[@]}"
rg -n --pcre2 '^\s*paths(?:-ignore)?\s*:|^\s*if\s*:\s*(?:false|\$\{\{\s*false\s*\}\})|^\s*shard(?:Total|Index|s)?\s*:' --hidden -g '.github/workflows/*.{yml,yaml}' -g '**/.gitlab-ci*.yml' .
#    4d (GitHub Actions, when the repo baseline is installed): the required set joined to the job graph — a test job
#    skipped by its `if:` or a needs-skip, a required workflow behind a path filter, no `merge_group` (ci-platform-semantics
#    R1–R5). OFFLINE form: no network call. With a saved settings snapshot (CI_SETTINGS_DIR, the `gh api` JSON) it joins
#    offline; without one it prints `NOT-RUN OFFLINE(…)`, exit 2 — required-ness unknown, never "not required". `--online`
#    (a read-only `gh api`) only when the user allows outbound calls for this run.
G=.claude/scripts/ci-graph.py; [ -f "$G" ] || G="$HOME/.claude/templates/repo-baseline/.claude/scripts/ci-graph.py"
RQ=(--required); [ -n "${CI_SETTINGS_DIR:-}" ] && RQ=(--settings-dir="$CI_SETTINGS_DIR")
if [ -f "$G" ] && [ -n "$(rg --files --hidden -g '.github/workflows/*.{yml,yaml}' .)" ]; then python3 "$G" . "${RQ[@]}"; echo "ci-graph exit=$? (0 clean, 1 rows, 2 NOT-RUN)"; else echo 'ci-graph: N/A (no ci-graph.py or no GitHub workflow)'; fi

# 5. §5 coverage that hides code: pragmas on shipped code (5a); coverage scope, exclusions and floors in runner and CI
#    config (5b) and in dedicated coverage files (5c). Zero 5b and 5c lines means no floor is declared.
rg -n --pcre2 '(?:/\*|//)\s*(?:istanbul|v8|c8)\s+ignore\b|(?i:#\s*pragma:?\s*no\s*(?:cover|branch))\b|^\s*#\s*:nocov:|\[\s*(?:[\w.]+\.)?ExcludeFromCodeCoverage\b|#\[(?:cfg_attr\([^)]*,\s*)?coverage\s*\(\s*off\s*\)|@codeCoverageIgnore(?:Start|End)?\b|//\s*coverage:ignore-(?:line|start|end|file)\b' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 'coveragePathIgnorePatterns|collectCoverageFrom|coverageThreshold|\bcoverage\s*:\s*\{|\bthresholds\s*:|fail_under|--cov-fail-under|--cov\b|sonar\.coverage\.exclusions|minimumCoverage|<minimum>|jacocoTestCoverageVerification|--check-coverage|\b(?:lines|branches|statements|functions)\s*:\s*\d|\[(?:tool\.)?coverage[:.]\w+\]' "${K[@]}" "${C[@]}" . | "${NC[@]}"
rg -n --pcre2 '^\s*(?:omit|exclude|exclude_also|exclude_lines|include|source|informational)\s*[=:]' --hidden -g '**/{.coveragerc,.nycrc*,.c8rc*,codecov.yml}' -g '!**/node_modules/**' .

# 6. §6 retries: configured in runner config, test files or CI (6a; Ruby forms on Ruby files, 6b); flaky gates (6c).
rg -n --pcre2 '\bjest\.retryTimes\s*\(|\bthis\.retries\s*\(\s*[1-9]|^\s*retr(?:y|ies)\s*:\s*(?:[1-9]|process\.env|\{\s*(?:count|runMode|openMode)\s*:\s*[1-9])|--retr(?:y|ies)[= ]+[1-9]|@pytest\.mark\.flaky\b|^\s*@flaky\b|--reruns(?:[= ]+[1-9])|\breruns\s*=\s*[1-9]|@(?:RetryingTest|RepeatedIfExceptionsTest|Flaky|FlakyTest|RetryOnFailure)\b|rerunFailingTestsCount|\bmaxRetries\s*(?:=|\.set\()\s*[1-9]|\[\s*(?:Retry|RetryFact|RetryTheory)\b|--rerun-fails\b|^\s*retries\s*=\s*[1-9]' -g '**/*.{test,spec,e2e-spec,flow,cy}.{js,ts,jsx,tsx,mjs,cjs}' -g '**/{test_*,*_test,conftest}.py' -g '**/*{Test,Tests,IT}.{java,kt,cs}' "${K[@]}" "${C[@]}" . | "${NC[@]}"
rg -n --pcre2 '(?:^|[\s,(])retry:\s*[1-9]|\bdefault_retry_count\b|\brspec-retry\b' -g '**/*_spec.rb' -g '**/{spec_helper.rb,Gemfile}' "${V[@]}" . | "${NC[@]}"
rg -n --pcre2 -e '--fail-on-flaky-tests|failOnFlakyTests|failOnPassedAfterRetry\s*=\s*true|failOnFlakeCount|--flaky-result[= ]fail|flaky-result\s*=\s*"fail"' "${K[@]}" "${C[@]}" .
```

A finding is a hit **plus** a read of the CI job that runs (or does not run) the affected tests
**plus** the proof. The structural blind spots, worked around rather than trusted:

- **Configs are code.** Grep 3a parses literal `roots`, `testDir`, `testRegex`, `testMatch` (regex or glob, every branch of a ternary, a named constant) and Vitest's `test.include` (never `coverage.include`) from Jest, Vitest and Playwright configs; a pattern built by a function call, a workspace file or a `projects` entry in another file prints the config line for reading, and the runner's own list (§ Adapt) is the authority when dependencies are installed.
- **CI reachability is textual.** Grep 3b matches script names and config paths in CI files; a script reached through an alias (`pnpm --filter api test:e2e`) or a reusable workflow reads `NOT-IN-CI` until you follow it — read before reporting.
- **Masking lives in shells, not only in YAML.** A step's default shell decides `pipefail`; read the step's `shell:` and the workflow `defaults` before rating grep 4b. The per-platform defaults are [`ci-platform-semantics.md`](../../../../snippets/ci-platform-semantics.md) S1–S7 (GitHub's bare `run:` is `bash -e` with **no** pipefail; `shell: bash` adds it); `ci-graph.py --shell-of=<file>:<line>` resolves a GitHub step's effective shell.

**Measured** (2026-10-05, read-only) on a real NestJS-on-Fastify + MikroORM + React monorepo of
about 14,200 tracked files with one CI workflow, three Jest configs, two Vitest configs and one
Playwright config: the script runs in about 2 s. 1a–1c: 0 — and no focus guard anywhere (1b empty:
the Playwright config sets no `forbidOnly`, the lint config enables no focused-test rule). 2a: 4,
all in Playwright flow files (`test.skip(!id, …)` and a `test.fixme` queue — read). 2c: 2
capability gates (`runIf(existsSync(dist))` after a CI build step; `runIf(browser available)`).
3a: 0 unclaimed files across the six configs. Re-measured 2026-10-15 on the same repo: 3a had regressed to 1,734 false `UNCLAIMED` (it read Vitest's `coverage.include`, did not expand `{ts,tsx}`, and missed a Playwright `testMatch: VISUAL ? SPEC : /.*\.flow\.ts$/`); it now strips coverage / typecheck blocks and comments, expands braces and extglobs, and takes every regex branch and named constant of a `testMatch` — 2 left, both non-test modules named `*-flow.ts` / `*.flow.ts` under `src/` (§ 32). 2c 2 → 9: seven helper-built gates (`const describeBuilt = built ? describe : describe.skip`, `(suiteSelected('money') ? describe : describe.skip)(`, and a `describeV1` exported from a `test/unit/_v1-reference.ts` helper that seven specs import), which is why 2c also names `process.env.V1_REPO_PATH` and `HAS_V1`, the V1-port shape. 2c-TSV (2026-10-18): 0 gates on every fixture but `brittle-suite` (2: an env gate on `LEDGER_DATABASE_URL` that no CI job sets, used by 1 spec, and a platform `skipif`); on a scratch port shape (`HAS_V1 = Boolean(process.env.V1_REPO_PATH)` behind a `describeV1` helper two specs import, and a pytest `skipif(not os.environ.get("V1_ROOT"))` marker) both rows print kind `v1`, `ci_sets no`, and a commented gate prints nothing. 4d prints `NOT-RUN OFFLINE(…)`: the pre-flight no longer calls GitHub. 3b: the Playwright flow suite (6 files), the Storybook
story-test project and the fuzz suites (money and stock among them) are invoked by no CI file — the
fuzz suites only from a local release script — the run's real § 3 candidates; the root aliases
resolve to in-CI jobs. 3d: 0 (no Maven module). 4a: 1 (`continue-on-error` on an
advisory runtime job with a stated one-quarter window, [`precedents/testing.md`](../../../../snippets/precedents/testing.md)
§ 28). 4b: 2 (a local gate script, run by no CI job). 4c: 5, all `--forceExit` on Jest e2e and fuzz
runs, including the four CI e2e shards (§ 30: masking is real only with a floating assertion, and
`assertion-strength-scan` found none). 5a–5c: 0 — no coverage configuration at all, so no floor is
declared (the QG-9 pre-existing line). 6a–6c: 0; an unscoped `retries` grep returns job-queue
settings in shipped code, which is why grep 6 reads only runner config, test files and CI. On
`benchmarks/fixtures/*` (no CI file in any of them) 3b prints `NO-CI-FILE` and its 9 test scripts as
`NOT-IN-CI` — true, nothing runs them in CI — and every other grep returns 0. On `brittle-suite`
(2.0.1) 3d prints `NO-FAILSAFE …/LedgerRepositoryIT.java:12` — its pom declares Surefire only, an
absence no line grep can cite.

## The 3,000-hit path

1. **Group** by (file, class) — skips by file and by reason string, masking by CI job, pragmas by directory: `rg -c <pattern> "${T[@]}" "${V[@]}" . | sort -t: -k2 -rn`.
2. **Close whole groups with one cited reason**: a directory no config collects *on purpose* (fixtures, helpers), a skip family carrying one tracker link and a condition, an advisory job with an owner and an end date. Count every closure in the coverage line.
3. **Rank by what the affected tests protect**: suites and files on money, auth, tenant, webhook and write paths first; a CI masking line on the required test job above any single skip.
4. **Read the top 30 groups**: the line, the job that runs it, the tests it hides.
5. **Prefer the runtime bulk oracle**: the collected-list diff over every config at once (§ Proof) settles all of § 3 in one run; one canary branch settles every masking line in § 4 for the job it runs; one coverage run with a full `include` settles § 5.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

Severity assumes the affected tests claim behaviour in shipped code. Promote to **critical** when
the line sits on the job that runs the required tests, or hides a money, auth or tenant suite;
drop one step when another job demonstrably runs the same tests.

| § | Class | Research ids · standard | Default |
|---|---|---|---|
| 1 | Focused test committed; no focus guard | TQ-11 · QG-7 | critical on a protected branch; the missing guard alone is hardening |
| 2 | Skip without owner and expiry; gate CI never satisfies; non-strict xfail | TQ-11 · QG-7 | medium; high when the gate is never satisfied in CI or the suite is on a money / auth path |
| 3 | Never collected, or a suite no CI job runs | TQ-12 · QG-13 | high; critical when it hides a money, auth or tenant suite |
| 4 | CI or runner switch that masks failure | TQ-13 · QG-13 | critical on the required test job; else medium |
| 5 | Coverage configuration that hides shipped code | MC-4, MC-6 · QG-9 | medium; high when it hides changed or money logic |
| 6 | Retries with no flaky gate, owner or expiry | FL-13 | medium; high on payments or auth |

### 1. Focused test committed; no focus guard

```
BAD:   it.only('refunds a damaged order', …)  ·  fdescribe('checkout', …)  ·  it 'charges', :focus do
       playwright.config.ts with no forbidOnly · CI: jest -t 'checkout'      // everything else silently skipped
GOOD:  no focus in the tree, plus a guard: forbidOnly: !!process.env.CI · mocha --forbid-only · jest/no-focused-tests at error in CI
```
**Read the code:** Is the hit a real test call (not a string, a comment, a function named `fit`)? Does the runner the CI job uses honour it? Does a guard (1b) already fail the run? **Finding when** a focus reaches the default branch, or a CI command filters by name. **Proof:** static fact — the line, plus the collected count with and without it (V61).

### 2. Skip without owner and expiry; gate CI never satisfies

```
BAD:   it.skip('settles a split payment', …)              // no reason, no ticket, no date
       const d = process.env.RUN_INTEGRATION ? describe : describe.skip;   // and no CI job sets RUN_INTEGRATION
       @pytest.mark.xfail                                 # passes → XPASS, exit 0
GOOD:  it.skip('… — #812, owner @payments, remove by 2026-12-01', …) · a CI job that sets the variable
       @pytest.mark.xfail(strict=True, reason="#812") and xfail_strict = true
```
**Read the code:** Is there an owner and a date or ticket on the line or the line above (QG-7)? For a gated suite (2c, one row per gate in `gated-suites.tsv`; `ci_sets` is per CI job, its `*` a directory-name hint — read the job; `unknown` means some job sets the variable but none is known to run the file), which CI job runs the file and does its `env:` set the variable, build the artefact, install the browser, or pass the build tag? Is the skip runtime-conditional on a previous step's result (a cascade inside one flow)? **Finding when** a skip has no owner and expiry, or its gate is false in every CI job that runs the file. **Proof:** static fact plus the job's env; for a gate, the file absent from the CI run's executed list (V61).

### 3. Never collected, or a suite no CI job runs

```
BAD:   src/billing/refund.test.ts under a config whose testRegex is '\.spec\.ts$'
       test/integration/*.spec.ts outside roots ['<rootDir>/src', '<rootDir>/test/unit']
       func Testrefund(t *testing.T) · class TestOrders: def __init__ · import org.junit.Test under Jupiter without vintage
       LedgerRepositoryIT.java in a module whose pom declares maven-surefire-plugin only — Surefire never runs *IT
       "test:flows": "playwright test" — and no workflow runs it
GOOD:  the file renamed into the pattern or the pattern widened; a CI job (or a scheduled workflow with an owner) that runs the suite
```
**Read the code:** Is the file a test (it declares a case) or a helper? Is it excluded on purpose (a fixture directory, an e2e suite another job runs — name the job)? Does an alias script reach the unclaimed suite? For a 3d row: does CI invoke Failsafe directly (`mvn failsafe:integration-test`) or through a profile in a parent pom outside the repo? A pom that names Failsafe only inside a `<profile>` passes 3d — read whether CI activates it. **Finding when** a file that declares cases is collected by no config, or a configured suite is invoked by no CI job and no scheduled workflow. **Proof:** the collection count — LOOKS − COLLECTED with the runner's own list, or the CI files showing no invocation; after the fix the test is listed **and** fails under break the SUT (V62).

### 4. CI or runner switch that masks failure

```
BAD:   continue-on-error: true on the job that runs `pnpm test` · pytest -q || true · pytest | tee out.txt (no pipefail)
       jest --passWithNoTests · mvn -Dmaven.test.failure.ignore=true · failOnRisky="false" · jest … --forceExit
GOOD:  the required job fails on red; `set -o pipefail` (or `shell: bash`) before a pipe; --forceExit removed after
       --detectOpenHandles names the leak
```
**Read the code:** Is the job the one that runs the required tests, or an advisory job with an owner and an end date (§ 28)? Does the step's shell set `pipefail`? For `--forceExit`, did `assertion-strength-scan` § 3 find a floating assertion in that suite ([`precedents/testing.md`](../../../../snippets/precedents/testing.md) § 2, § 30)? Is the job a required check in the host? Grep 4d's `ci-graph.py --required` settles it on GitHub: a `REQUIRED` row (or `REQUIRED-IF-SKIP` / `REQUIRED-NEEDS-SKIP` / `REQUIRED-PATH-FILTERED`, a required check a skip satisfies or leaves Pending — [`ci-platform-semantics.md`](../../../../snippets/ci-platform-semantics.md) R1–R5) puts the row at the critical default; `OFFLINE` (no snapshot, no `--online`) or `UNREADABLE` (no token or no admin rights) leaves that half Unconfirmed, never "not required". **Finding when** a failing test in that job leaves the job green. **Proof:** the CI canary (V63); where pushing is not allowed, the masking line and its job are the static fact and the canary is the settling probe.

### 5. Coverage configuration that hides shipped code

```
BAD:   coveragePathIgnorePatterns: ['src/billing'] · omit = src/payments/* · /* istanbul ignore next */ over a tax branch
       Vitest coverage with no `include` (only files a test imports are reported) · coverageThreshold { lines: 0 }
GOOD:  include: ['src/**'] with exclusions only for generated code, each with a reason; a floor at the current baseline
```
**Read the code:** Is the excluded path generated, platform-specific or a declared entry stub (§ 31)? Does a pragma carry a reason? Is any floor declared at all — none declared is the QG-9 pre-existing line, not a finding? **Finding when** shipped source is excluded from the report or a pragma sits on hand-written logic without a reason. **Proof:** the coverage inventory — the file or lines absent from the report, then present with their hit counts after the exclusion is removed in a scratch copy (V64).

### 6. Retries with no flaky gate, owner or expiry

```
BAD:   jest.retryTimes(3) in a unit suite · --reruns 2 in CI · rerunFailingTestsCount=2 with failOnFlakeCount unset (0 = unlimited)
       Gradle test-retry with failOnPassedAfterRetry left false · nextest retries with no --flaky-result fail
GOOD:  retries scoped to a quarantine tag with an owner, a ticket and an expiry, at most 2, and the flaky gate on
       (--fail-on-flaky-tests · failOnPassedAfterRetry = true · failOnFlakeCount = 1 · --flaky-result fail)
```
**Read the code:** Is the retry in runner config (not a job queue's `retries` in shipped code)? Is it scoped, visible, owned, bounded and error-scoped (§ 29)? Is it Playwright's scaffold `retries: process.env.CI ? 2 : 0` with flaky results reported? **Finding when** a retry can turn a failing test green with no gate and no owner. **Proof:** the retry unmask — the retried test with retries off fails k of N (V65); `/flaky-test-hunt` takes the root cause.

## Proof

The oracles and their commands are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md)
§ Testing — *Collection count*, *CI canary*, *Coverage inventory*, *Retry unmask*, *Strictness
switches* — with the variant lists V61–V65. A canary branch and every scratch edit are deleted
after the run; no probe is committed.

## Output

```
suite-execution-scan — lanes: jest 30 (3 configs), vitest 4.1 (2 configs), playwright 1.63; CI: .github/workflows/ci.yml

Findings: 2 · Unconfirmed: 2 · Hardening: 2

1. apps/web/package.json:15  "test:flows": "playwright test"                     [report-with-fix]  high
   §3 suite no CI job runs — 6 flow files (apps/web/e2e/flows/*.flow.ts) cover order, auth and warehouse cycles; no
   workflow names test:flows or playwright. Proof: ci.yml invokes jest (unit, e2e shards) and vitest only.
   Fix: an e2e-flows job (or a scheduled workflow with an owner) running `pnpm --filter web test:flows`, plus forbidOnly.

2. apps/api/package.json:25  "test:fuzz" (money and stock)                       [report-with-fix]  high
   §3 suite no CI job runs — the money-invariant fuzz suite runs only from a local release script; no workflow, no
   schedule. Fix: a nightly workflow with an owner reading its result (precedents/testing.md § 27).

3. .github/workflows/ci.yml:197  jest … --forceExit --shard=…                    [report-flagged]   medium
   §4 masking switch on the e2e job — Jest 30 passes an un-awaited failing assertion under --forceExit.
   Unproven link: assertion-strength-scan found no floating assertion today. Settling probe: --detectOpenHandles on one shard.

Verification: 9 candidates → 2 findings · 2 unconfirmed · 2 hardening · 3 refuted

Class coverage:
  §1  focus                       checked (0 focused tests; no forbidOnly or focused-test lint rule → 1 hardening)
  §2  skips and gates             checked (4 skips in flow files, 2 capability gates → 0; both gates satisfied by the CI job)
  §3  never collected / never run checked (0 unclaimed files in 6 configs; 3 suites not in CI → 2 findings, 1 unconfirmed: the story-test project, no owner found)
  §4  CI masking                  checked (1 continue-on-error on an advisory job → hardening; 5 --forceExit → 1 unconfirmed)
  §5  coverage hiding             N/A (no coverage configuration; no floor declared — QG-9 pre-existing line)
  §6  retry masking               checked (0 retries in runner config, tests or CI)
```

`[report-with-fix]`: the line, the affected tests and the CI evidence are traced, and the fix names
the guard that keeps it fixed. `[report-flagged]`: one link is unproven (a job's shell or env not
read, a required-check setting not visible, an alias not followed), and the row names it and the
settling probe. The coverage block lists **all six** classes on every run: `checked (k hits → m
findings)` only when the grep ran on a present lane; `N/A (<reason>)` only when the surface does not
exist (no coverage tool, no retry plugin); `blocked (<reason>)` when a grep failed or a config could
not be read. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/testing.md`](../../../../snippets/precedents/testing.md) (§ 1–12 for
runner versions, § 25–33 for this skill) and
[`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones met most:
a skip with a reason, a ticket and a condition (§ 25); a capability gate the CI job satisfies
(§ 26); an out-of-gate suite a scheduled workflow owns (§ 27); `continue-on-error` on an advisory
job with an end date (§ 28); scoped, gated retries and Playwright's scaffold default (§ 29);
`--forceExit` with no floating assertion (§ 30); reasoned coverage exclusions and an undeclared floor
(§ 31); helpers, abstract bases and fixtures that are not tests (§ 32); declared ordering (§ 33).

## When to run

- On any diff that touches a runner config, a CI workflow, a `package.json` test script, a coverage config or a skip, after `test-integrity.py`.
- On every whole-repo test audit, before `assertion-strength-scan` — a test that never runs makes its assertions moot.
- When a regression shipped although "the tests cover it": check first that they ran.

## Halt conditions

- Do not report a high or critical row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/testing.md`](../../../../snippets/precedents/testing.md) (`agents/verifier.md` in refute mode when the repo-baseline is installed). Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted — never drop them.
- Halt on any finding without the line, the affected tests, the CI job that runs them (or the evidence that none does), and the fix with its guard.
- Do not call a suite "not in CI" from grep 3b alone; follow aliases, reusable workflows and scheduled workflows first.
- Do not propose deleting a test, adding a skip, or raising a retry count as the fix. Do not change a required-check setting or a CI gate without asking: those are the human's.
- Do not leave a canary branch or a scratch config behind; no probe is committed.
- Do not print "every test runs" without the class-coverage block; a grep that did not run is `blocked`, never `checked`.
- Do not re-derive a class another owner holds (§ Boundaries) — cross-link it.

## Related

- `assertion-strength-scan` (this pack) — whether the collected tests can fail; § 4's `--forceExit` verdict reads its § 3.
- `coverage-gap` (this pack) — changed lines with no executing test; this skill's § 5 decides whether the report it reads can be trusted.
- `.claude/scripts/test-integrity.py` (repo-baseline) — diff-time skips, focus, floors and CI steps; `standards-check.py` — the QG-7 and QG-13 per-change checks; `agents/verifier.md` — the independent verifier.
- `parity-proof-scan` (migration pack, when installed) reads 2c's `gated-suites.tsv`: every parity claim resting on a `v1` row no CI job satisfies is NOT-RUN. Without that pack the TSV is only this skill's § 2 worklist.
- `/run-tests` — runs the suite and reports NOT-RUN honestly; `/flaky-test-hunt` — root-causes what § 6's retries were hiding.
- `@ci-reviewer` (devops pack, when installed) — CI design beyond whether tests run and fail.
- [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Testing — the oracles, the anti-cheat rule and V61–V65; `rules/testing-principles.md` — the floor these classes enforce.
