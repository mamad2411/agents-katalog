---
name: assertion-strength-scan
description: Find tests that cannot fail — no or weak oracle, interaction-only, unreached or un-awaited assertions, swallowed failures, expected values from the code under test, snapshot-only — whole suite, each proved by breaking the code under test.
kind: skill
pack: testing
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: assertion-strength-scan

## Premise

A test that cannot fail is worse than no test: it is counted, it is green, and a reviewer reads
past the behaviour it claims to pin. Six shapes produce it — nothing asserted (or only that
something exists), only an interaction asserted where a result exists, an assertion that never
runs or is never awaited, a failure the test itself catches, an expected value the code under test
computed, and a snapshot that records whatever the code does today. Mutation studies put
"covered but unverified" (pseudo-tested) methods at 1–46% of the methods studied (Vera-Pérez et
al., EMSE 2019).

This skill inventories the **whole suite** for those six classes. It is the read-the-code half of
assertion strength; `mutation-probe` is the measured half, and `.claude/scripts/oracle-check.py`
is the per-case tool lane for § 1.

**Every finding cites the test case `<file:line>` + the production line it claims to pin + the
missing oracle + the probe that proves the test stays green while that line is wrong + the
strengthened assertion.** A grep or tool hit is never a finding. "No weak tests" is never printed
without the class-coverage block (§ Output).

## The rule

A candidate is a finding when all four hold:

1. **The test runs.** A CI job collects and runs it. A test that never runs is `suite-execution-scan` § 3, not a weak oracle.
2. **It claims a behaviour that can break.** The case name or the function it calls names a result, a state or a side effect a regression could change. Logging text, `toString` and generated code are not behaviour.
3. **No other test pins the same behaviour** — searched by name *and* by assertion across unit, integration, e2e, contract and the type system ([`precedents/testing.md`](../../../../snippets/precedents/testing.md) gate 2). The unit of a finding is a behaviour, not a test.
4. **The probe keeps it green.** Break the SUT (a wrong value of the right type, never a `throw`) or flip the test's own expected value, and the test still passes ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Testing). Without a probe run it is **Unconfirmed**, carrying the probe — never promoted on reading alone.

## Boundaries

- **Diff-time weakening** (an assertion deleted, a skip added, a snapshot rewritten in the change) → `.claude/scripts/test-integrity.py`. **Per-case no-assertion / weak / tautology on changed test files** → `.claude/scripts/oracle-check.py` (QG-15). On a diff, run both first and consume their JSON; this skill adds § 2–§ 6 on the changed cases and never re-greps their classes. Without the repo-baseline, their classes run here through the inline lane and the header prints `lane: inline (repo-baseline scripts absent)`.
- **Tests that never run, CI that masks, retries, coverage config** → `suite-execution-scan` (this pack).
- **Measured strength** (surviving mutants, pseudo-tested methods) → `mutation-probe` (this pack); this skill hands it the candidate lines. **Changed lines no test executes** → `coverage-gap` (this pack).
- **A mocked SUT, loose or drifting doubles, test seams in production** → `test-double-scan` (this pack); this skill reports only the mock-echo oracle (§ 5). **Flake sources** (clocks, sleeps, order, network) → `flake-source-scan` (this pack) and `/flaky-test-hunt`, the runtime harness.
- **Missing negative tests on auth or tenant routes** → `coverage-gap` and the QG-3 gate; the hole itself is the security pack's, when installed.

## Adapt to the codebase

Read the runner **and its major version** from the lockfile — four verdicts below change with it
([`precedents/testing.md`](../../../../snippets/precedents/testing.md) § 1–12). Print the lanes you
ran in the output header. A lint lane counts only when CI runs it at error level on test files.

| Stack | Case declaration · assertion shape | Lint lane (run it when configured) | Runtime switch (proof and guard) |
|---|---|---|---|
| **Jest** 30 | `it` / `test` · `expect().toX`, supertest `.expect(status)` | eslint-plugin-jest 29.16: `expect-expect`, `no-conditional-expect`, `valid-expect` (`alwaysAwait`), `valid-expect-in-promise`, `no-restricted-matchers`, typed `no-unnecessary-assertion`, `valid-expect-with-promise`; `--max-warnings 0` (three rules are WARN in `recommended`) | `setupFilesAfterEnv` with `expect.hasAssertions()`; an un-awaited failing `.resolves` passes beside another file or under `--forceExit` |
| **Vitest** | same | @vitest/eslint-plugin 1.6: `expect-expect` (error), `require-awaited-expect-poll`, `no-conditional-in-test` | `setupFiles` with `expect.hasAssertions()`; Vitest ≥ 5 fails an un-awaited `.resolves` / `expect.poll` natively, ≤ 4 does not |
| **Playwright** | `test` · web-first `await expect(locator)` | eslint-plugin-playwright: `missing-playwright-await`, `prefer-web-first-assertions`, `expect-expect` | `forbidOnly: !!process.env.CI` |
| **TS, any runner** | — | `@typescript-eslint/no-floating-promises` on test globs (`void expect(…)` silences it: `ignoreVoid`) | — |
| **pytest** 9 | `def test_*` · `assert`, `pytest.raises`, `mock.assert_*` | Ruff 0.16: `PT011`, `PT012`, `PT015`, `PT017`, `PT018`, `B011`, `B015`, `B017`, `B018`, `F631`, `PGH005` | `-W error::pytest.PytestUnraisableExceptionWarning` (catches `assert coro()`); `PYTHONOPTIMIZE=1` (assert-based helpers) |
| **Go** | `func TestX(t *testing.T)` · `t.Error`, testify | golangci-lint 2.14 + testifylint 1.6.4: `useless-assert`, `go-require`, `require-error`, `error-nil` | `-race`; a `require` in a goroutine is lost |
| **JVM** | `@Test` · AssertJ, JUnit, Mockito `verify` | error-prone 2.50: `CheckReturnValue`, `MissingFail`, `AssertionFailureIgnored`, `MockitoUsage`, `SelfAssertion`, `TestExceptionChecker`; PMD 7.28: `UnitTestShouldIncludeAssert`, `UnnecessaryBooleanAssertion` | Mockito strict stubs |
| **Ruby** | `it` · `expect().to` | rubocop-rspec 3.10: `RSpec/NoExpectationExample`, `VoidExpect`, `Be`, `IdenticalEqualityAssertion`, `UnspecifiedException` | — |
| **PHP** | `test*` / `#[Test]` · `$this->assert*` | phpstan-phpunit 2.0: `AssertSame*`, `alreadyNarrowedType` | `--fail-on-risky` (13.4 exits 0 on a risky test by default) |
| **.NET** | `[Fact]` / `[Test]` / `[TestMethod]` | xUnit2002, xUnit2014, xUnit2021; MSTEST0032, MSTEST0040, MSTEST0058 | analyzers at error on test projects |
| **Rust** | `#[test]` · `assert!` / `assert_eq!` | clippy `should_panic_without_expect`, `assertions_on_constants`, `assertions_on_result_states` | — |

## Pre-flight

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep
**N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`.`): `rg` with no path
reads stdin whenever stdin is a pipe, which under an agent's shell is a silent zero-hit run. A file
under `T` is a test only if it declares a case — helpers, setup files and fixtures under a test
directory are not. Any `rg` error on stderr (exit 2, `PCRE2: match limit exceeded`) is a failed
grep, never zero hits.

```bash
V=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/target/**' -g '!**/.venv/**'
   -g '!**/coverage/**' -g '!**/*.min.*' -g '!**/__snapshots__/**')
T=(-g '**/*.{test,spec,e2e-spec,int-spec,flow,cy}.{js,jsx,ts,tsx,mjs,cjs,mts,cts}' -g '**/__tests__/**/*.{js,jsx,ts,tsx}' -g '**/{test_*,*_test}.py'
   -g '**/*_test.go' -g '**/*{Test,Tests,IT,TestCase}.{java,kt}' -g '**/*_spec.rb' -g '**/*{Test,Tests}.{php,cs}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')        # drops comment-only lines
OC=.claude/scripts/oracle-check.py; [ -f "$OC" ] || OC="$HOME/.claude/templates/repo-baseline/.claude/scripts/oracle-check.py"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/assert-scan.XXXXXX")"; rg --files "${T[@]}" "${V[@]}" . | sed 's#^\./##' > "$TMP/files"
# 0. Context: test files per lane (0a), runner versions (0b), guards already on — gate 4 (0c).
for g in '*.{test,spec,e2e-spec}.{js,jsx,ts,tsx,mjs,cjs}' '{test_*,*_test}.py' '*_test.go' '*{Test,Tests,IT}.{java,kt}' '*_spec.rb' '*Test.php' '*{Test,Tests}.cs'; do printf '%-48s %s\n' "$g" "$(rg --files -g "$g" "${V[@]}" . | wc -l)"; done
rg -n --no-heading --pcre2 '"(?:jest|vitest|@playwright/test|mocha)"\s*:\s*"[^"]+"|^\s*(?:pytest|pytest-asyncio)\s*[=<>~]=|<artifactId>(?:junit-jupiter\w*|junit-vintage-engine|mockito-\w+)</artifactId>|"phpunit/phpunit"\s*:' -g '**/package.json' -g '**/{pyproject.toml,requirements*.txt,pom.xml,composer.json}' "${V[@]}" .
rg -n --no-heading --pcre2 'expect\.(?:hasAssertions|assertions)\(|assertFunctionNames|(?:jest|vitest|playwright)/(?:expect-expect|valid-expect|no-conditional-expect|missing-playwright-await)|no-floating-promises|failOnRisky|--fail-on-risky|PytestUnraisableExceptionWarning|select\s*=.*\bPT\b' -g '!**/*.{md,snap}' "${V[@]}" .

# 1. §1 — tool lane first: oracle-check.py over every test file (1a: JSON in $TMP/oracle.json); the per-case census, the
#    inline lane for JS/TS and Python (1b: $TMP/census.tsv, columns kind · file:line · case); no-op and tautological
#    assertion APIs on every stack (1c).
[ -f "$OC" ] && { python3 "$OC" --repo=. --files="$(paste -sd, - < "$TMP/files")" --json > "$TMP/oracle.json"; echo "oracle-check exit $? (0 none · 1 rows to triage · 2 failed)"; } || echo "lane: inline (repo-baseline scripts absent)"
cat > "$TMP/census.py" <<'PY'
import re, sys
MJ = re.compile(r'\.((?:not\.)?(?:resolves\.|rejects\.)?to[A-Z]\w*)\(')
WEAK = re.compile(r'^(?:not\.)?(?:resolves\.)?(?:toBeDefined|toBeTruthy|toBeFalsy)$|^not\.(?:toBeNull|toBeUndefined|toThrow\w*)$')
CALL = re.compile(r'^(?:not\.)?toHaveBeen(?:Called|NthCalled|LastCalled)\w*$|^toBeCalled\w*$')
OTHER = re.compile(r'(?<![\w$])\.expect\(\s*\d{3}|\b(?:expect|assert)[A-Z]\w*\(|\bassert\w*\s*\(')   # status oracle, helpers
EXIST = re.compile(r'expect\((?:screen\.|within\([^)]*\)\.)?(?:get|find)(?:All)?By')              # a query that throws when absent
WEB = r'\.(?:not\.)?to(?:Be(?:Visible|Hidden|Enabled|Disabled|Checked|Focused|Editable|Empty|Attached|InViewport)|Have(?:Text|URL|Title|Count|Values?|Attribute|Class|CSS|Id|Screenshot|AccessibleName|Role)|ContainText)\('
for f in sys.argv[1:]:
    src = open(f, errors='replace').read(); L = src.split('\n'); py = f.endswith('.py'); i = 0; pw = '@playwright/test' in src
    FLOAT = re.compile(r'(?:^|[;{]\s*)(?!\s*(?:await|return)\b)\s*(?:(?:const|let|var)\s+(\w+)\s*=\s*)?(expect(?:\.soft)?\([^;]*?\)\s*\.(?:resolves|rejects)\.[^;]*|expect\.poll\([^;]*|test\.step\([^;]*' + (r'|expect(?:\.soft)?\([^;]*?\)' + WEB + '[^;]*' if pw else '') + ')', re.M)
    while i < len(L):
        m = re.match(r'^(\s*)(?:(?:it|test)(?:\.(?:each|concurrent|failing)\b[^(]*)?\s*\(|(?:async\s+)?def\s+test\w*\s*\()', L[i])
        if not m: i += 1; continue
        ind = m.group(1); j = i + 1
        end = (lambda s: s.strip() and len(s) - len(s.lstrip()) <= len(ind)) if py else (lambda s: re.match('^' + re.escape(ind) + r'\}', s))
        if not py:                                   # a signature split over lines: the body opens at the first `=> {` / `) {`
            while j - 1 < len(L) and not re.search(r'(?:=>|\))\s*\{\s*$', L[j - 1]): j += 1
        while j < len(L) and not end(L[j]): j += 1
        body = '\n'.join(L[i:j + 1]); ms = [x.group(1) for x in MJ.finditer(body)]; k = []
        if py:
            a = re.findall(r'^\s*assert\b|\.assert_\w+\(|pytest\.raises|self\.assert\w+\(', body, re.M)
            k += ['no-assertion'] if not a else ['interaction-only'] if all(x.startswith('.assert_') for x in a) else []
        elif not ms and not OTHER.search(body) and not re.search(r'\bexpect\(|\bassert', body): k.append('no-assertion')
        elif ms and not OTHER.search(body):
            if all(CALL.match(x) for x in ms): k.append('interaction-only' + ('' if re.search(r'CalledWith\(|not\.toHaveBeenCalled', body) else ':count-only'))
            elif all(x.endswith('Snapshot') for x in ms): k.append('snapshot-only')
            elif all(WEAK.match(x) for x in ms) and not EXIST.search(body): k.append('weak-sole')
        if not py:
            k += ['floating-async' for s in FLOAT.finditer(body) if not (s.group(1) and re.search(r'\b(?:await|return)\s+' + s.group(1) + r'\b', body))]
        for x in k: print('%s\t%s:%d\t%s' % (x, f, i + 1, L[i].strip()[:100]))
        i = j + 1
PY
rg '\.(?:[cm]?[jt]sx?|py)$' "$TMP/files" | tr '\n' '\0' | xargs -0 -r python3 "$TMP/census.py" > "$TMP/census.tsv"; cut -f1 "$TMP/census.tsv" | sort | uniq -c
rg '^(?:no-assertion|weak-sole)\t' "$TMP/census.tsv"
rg -n --pcre2 '^\s*(?:Assertions\.)?assertThat\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)\s*;|\bverify\(\s*\w+\s*\)\s*;|\bverify\(\s*\w+\.\w+\(|\.assert_(?:called|called_once|not_called|awaited)\w*\s*$|^\s*(?:expect\s*\((?:[^()]|\([^()]*\))*\)|is_expected)\s*(?:#.*)?$|#\[should_panic\s*\]|\braises\(\s*(?:Exception|BaseException)\s*\)|^\s*assert\s*\(.+,\s*[rbuf]?["\x27][^"\x27]*["\x27]\s*\)\s*$|\.assert(?:True|False)\(\s*[^,()]+(?:\([^()]*\))?\s*,(?!\s*(?:[\x27"]|[rfbu][\x27"]|msg\s*=))|\bexpect\(\s*(true|false|null|\d+)\s*\)\.(?:toBe|toEqual)\(\s*\1\s*\)|\b(?:assert|require)\.(?:Equal|EqualValues|Exactly)\(\s*\w+\s*,\s*([\w.]+)\s*,\s*\2\s*[,)]|\$this->assert(?:True|False)\(\s*(?:true|false)\s*\)|\bassert!\(\s*true\s*\)' "${T[@]}" -g '**/*.rs' "${V[@]}" . | "${NC[@]}"

# 2. §2 interaction-only: census rows `interaction-only` (args pinned or a negative call check) and `…:count-only` (2a);
#    JVM / Ruby / Go files whose only checks are verify / receive / mock expectations (2b).
rg '^interaction-only' "$TMP/census.tsv"
rg -l --pcre2 '\bverify\(|\bto\s+(?:have_)?receive\b|\.AssertExpectations\(|\.EXPECT\(\)' "${T[@]}" "${V[@]}" . | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\bassert(?:That|Equals|True|False|Eq)\w*\s*\(|\bassert\.\w+\(|\brequire\.\w+\(|\.to\s+(?:eq|eql|equal|match|include|be_\w+)\b|\bisEqualTo\('

# 3. §3 unreached or un-awaited: census `floating-async` (3a); an `expect` inside a catch whose own case holds no guard
#    (`fail(`, a `throw new` before or after the catch, `.toThrow`, `.rejects`, `expect.assertions`, or a catch that returns a
#    value its caller asserts) — the window is the enclosing case or helper, so a sibling case's guard never hides it (3b);
#    an `expect` in a callback that may never run (3c); assertions in a loop or branch (3d); Python assert in except, a raises block with trailing statements, assert on an un-awaited call in an async test (3e); JUnit 4
#    `expected=`, un-awaited .NET async asserts, async void tests, Go t.Fatal / require in a goroutine (3f).
rg '^floating-async' "$TMP/census.tsv"
rg -n -U --pcre2 'catch\s*(?:\([^)]*\))?\s*\{[^{}]*\bexpect\(' "${T[@]}" "${V[@]}" . | rg --pcre2 '^[^:]+:\d+:\s*(?:\}\s*)?catch\b' | python3 -c '
import re, sys
G = re.compile(r"\bfail\(|(?:^|[;{])\s*throw\s+new\b|\.toThrow|\.rejects\b|expect\.assertions\(", re.M)
ind = lambda s: len(s) - len(s.lstrip())
for l in sys.stdin:                                  # the window is the enclosing case or helper, before AND after the catch
    f, n, _ = l.split(":", 2); L = open(f, errors="replace").read().split("\n"); c = int(n) - 1; j = c
    while j > 0 and not (L[j].strip() and ind(L[j]) < ind(L[c]) and re.search(r"\{\s*$", L[j])): j -= 1
    k = j + 1
    while k < len(L) and not (L[k].strip() and ind(L[k]) <= ind(L[j]) and L[k].lstrip().startswith("}")): k += 1
    e = c + 1
    while e < k and not (L[e].strip() and ind(L[e]) <= ind(L[c])): e += 1
    if G.search("\n".join(L[j:c] + L[e:k + 1])) or re.search(r"^\s*return\s+[^;\s]", "\n".join(L[c:e]), re.M): continue
    print(l.rstrip() + ("  [file sets expect.hasAssertions]" if "expect.hasAssertions(" in "\n".join(L) else ""))'
rg -n --pcre2 '\.(?:on|once|addEventListener|addListener|subscribe|then)\(.*=>\s*\{?\s*expect\(|\bset(?:Timeout|Immediate)\(\s*(?:\(\)\s*=>|function)\s*\{?\s*expect\(' "${T[@]}" "${V[@]}" . | "${NC[@]}"
rg -n --pcre2 '^\s*(?:for\s*\(\s*(?:const|let)\s+\w+\s+of\b|[\w.]+\.forEach\(|if\s*\().*\bexpect\(' "${T[@]}" "${V[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '^\s+(?:if\s+[^\n]+|for\s+\w+(?:,\s*\w+)*\s+in\s+[^\n]+):\s*\n\s+assert\b|^\s*except\b[^\n]*:\s*\n\s+assert\b|with\s+pytest\.raises\([^\n]*\):\s*\n(\s+)[^\n]+\n\1(?!assert\b)\S' -g '**/{test_*,*_test}.py' "${V[@]}" . | "${NC[@]}"
rg -l --pcre2 '^\s*async\s+def\s+test' -g '**/{test_*,*_test}.py' "${V[@]}" . | tr '\n' '\0' | xargs -0 -r rg -n --pcre2 '^\s*assert\s+(?!await\b)(?:not\s+)?[\w.]+\('
rg -n --pcre2 '@Test\s*\(\s*expected\s*=|^(?![^\n]*\b(?:await|return)\s+Assert)[^\n]*\bAssert\.(?:ThrowsAsync|ThrowsAnyAsync)\b|\[(?:Fact|Theory|Test|TestMethod)\b[^\]]*\]\s*public\s+async\s+void\b' "${T[@]}" "${V[@]}" . | "${NC[@]}"
rg -n -U --pcre2 'go\s+func\s*\([^)]*\)\s*\{(?:(?!\n\s*\}\s*\(\)).){0,300}?\b(?:t\.(?:Fatal|Fatalf|FailNow|SkipNow)\(|require\.)' -g '**/*_test.go' "${V[@]}" .

# 4. §4 swallowed: try { … expect … } catch {} (4a); promise .catch that swallows, suppress(AssertionError), recover() in
#    a Go test, catch of AssertionError / Throwable, Mock(unsafe=True) (4b); Python assert in try with a passing except (4c).
rg -n -U --pcre2 'try\s*\{[^{}]*\bexpect\([^{}]*\}\s*catch\s*(?:\([^)]*\))?\s*\{\s*(?://[^\n]*\s*)*\}' "${T[@]}" "${V[@]}" . | rg --pcre2 '^[^:]+:\d+:\s*try\b'
rg -n --pcre2 '\.catch\(\s*(?:\(\s*\w*\s*\)|\w+)\s*=>\s*(?:\{\s*\}|undefined|null|void\s+0)\s*\)|\bsuppress\(\s*(?:AssertionError|Exception|BaseException)\b|\brecover\(\)|catch\s*\(\s*(?:final\s+)?(?:AssertionError|AssertionFailedError|Throwable|Error)\s+\w+\s*\)|\b(?:Mock|MagicMock|AsyncMock|create_autospec|patch(?:\.object)?)\([^)]*\bunsafe\s*=\s*True' "${T[@]}" "${V[@]}" . | "${NC[@]}"
rg -n -U --pcre2 'try:\n(?:[ \t]+.*\n)*?[ \t]+assert\b.*\n(?:[ \t]+.*\n)*?[ \t]*except(?:\s+\(?(?:Exception|BaseException|AssertionError)\b[^:]*)?:\s*\n[ \t]+(?:pass|\.\.\.|return|continue)\b' -g '**/{test_*,*_test}.py' "${V[@]}" .

# 5. §5 expected value from the code under test: the same call on both sides (5a); a mocked return echoed back (5b).
rg -n -U --pcre2 'const\s+(\w+)\s*=\s*([\w.]+)\(([^()\n]*)\);\s*\n\s*expect\(\2\(\3\)\)\.\w+\(\1\)|\bexpect\(\s*([\w.]+)\(([^()\n]*)\)\s*\)\.(?:toBe|toEqual|toStrictEqual)\(\s*\4\(\5\)\s*\)' "${T[@]}" "${V[@]}" .
rg -n -U --pcre2 'mock(?:Resolved|Return)Value(?:Once)?\(([^()\n]+)\)(?:[^\n]*\n){0,8}?[^\n]*expect\([^;\n]*\)\.(?:resolves\.)?(?:toBe|toEqual|toStrictEqual)\(\1\)|(\w+)\.return_value\s*=\s*([^\n]+)\n(?:[^\n]*\n){0,8}?\s*assert\s+[^\n]*==\s*\3\s*$' "${T[@]}" "${V[@]}" . | rg --pcre2 '^[^:]+:\d+:'

# 6. §6 snapshots: census `snapshot-only` cases (6a); snapshot entries over 50 lines (6b); snapshot writing wired into
#    scripts or CI (6c).
rg '^snapshot-only' "$TMP/census.tsv"
rg --files -g '**/__snapshots__/*.snap' -g '!**/node_modules/**' . | tr '\n' '\0' | xargs -0 -r awk 'FNR==1{n=0} /^exports\[`/{if(n>50)print p" "n" lines"; p=FILENAME":"FNR; n=0} {n++} END{if(n>50)print p" "n" lines"}'
rg -n --pcre2 '(?:jest|vitest|playwright\s+test|(?:npm|pnpm|yarn)\s+(?:run\s+)?test[\w:-]*)\b[^\n]*\s(?:-u\b|--updateSnapshot\b|--update-snapshots?\b)|--snapshot-update\b|\binsta\s+accept\b|INSTA_UPDATE\s*[=:]\s*["\x27]?(?:always|new)|UPDATE_SNAPSHOTS?\s*[=:]\s*["\x27]?(?:1|true)' --hidden -g '**/package.json' -g '**/*.{yml,yaml,toml,sh,mk}' -g '**/Makefile' -g '**/Jenkinsfile' "${V[@]}" .
```

A finding is a hit **plus** a read of the case **plus** a read of the production function it calls
**plus** the probe. The structural blind spots, worked around rather than trusted:

- **Helpers hide assertions.** A case that calls `expectOrderTotal(…)` or a supertest chain asserts through it; oracle-check and the census count `expectX(` / `assertX(` / `.expect(<status>)` as assertions, and a helper with another name reads as assertion-free — read the helper before reporting.
- **Case bodies are found by indentation.** The census closes a JS case at the next `})` on the case's own indentation (formatter output); one-line cases and unformatted files are missed — run the lint lane there.
- **Runner semantics decide § 3.** A floating `.resolves` is a red test on Vitest ≥ 5 and a silent pass on Jest 30 beside another file: read the version (grep 0b) before rating.

**Measured** (2026-10-05, read-only) on a real NestJS-on-Fastify + MikroORM + React monorepo of
about 14,200 tracked files (3,334 test files, Jest 30 for the API, Vitest 4.1 for the web app, no
oracle-check installed): the script runs in about 3 s. Lane 1a with the global oracle-check copy
checked 24,986 cases and returned 1,007 rows — 689 were supertest status lines (`.expect(403)` on
refusal tests, [`precedents/testing.md`](../../../../snippets/precedents/testing.md) § 16), 110
were pseudo-cases parsed from comment lines, 20 were Testing Library `getBy*` existence checks
(§ 14), leaving 188 to read. Re-measured 2026-10-15 (3,930 test files, 27,835 cases): 1,044 → 870 rows
after oracle-check stopped parsing cases out of comments (−132), closed arrow `it.each` bodies that span
lines, and counted a lone `not.toHaveBeenCalled()` as an oracle (§ 20); its `precedent` column then
tags 612 `§16 status-4xx` (bulk-close), 35 `§16 2xx-paired`, 61 `§16 2xx-unpaired` (read), 162 untagged. The census returned weak-sole 62, no-assertion 21 (most assert through a helper such as `refused(…)` — read it), interaction-only
380 (55 count-only), snapshot-only 27, floating-async 0. Grep 1c: 0. 3b: 2 sites, both a
`try { parse() } catch (e) { expect(e)… }` whose catch the parser may never enter — real § 3
candidates; the other 17 catch-with-`expect` sites are cleared by a guard in their own case (a
`throw new Error('should have refused')` after the call, or a `.toThrow` on the same call above the
`try`). Until 2.0.1 the guard was read per file, so a sibling case's `.toThrow` hid a site —
`brittle-suite`'s seeded refund-window spec, now listed. Re-measured 2026-10-15 on the same repo: 3b 4 → 0 —
all four were helpers whose `throw new` sits after the catch or whose catch returns the code the caller
asserts, and the window then stopped at the catch; it now spans the enclosing case or helper (`refund-window` still listed). 3c: 5 (`.then(r => expect(…))` inside awaited chains — read). 3d: 149 lines (loops over
fixed vocabularies; read for a length assertion). 4a: 0. 4b: 21 (teardown and navigation `.catch(() => undefined)` — read for an assertion in the chain).
5a: 16 (determinism checks, § 18). 5b: 25. 6: 54 snapshot assertions in 5 files; 13 entries over 50
lines, all in one characterization file (§ 22); 6c: 0. On `benchmarks/fixtures/*` (7 test files, all
JS or Python) every grep returns 0 and the census returns no row.

## The 3,000-hit path

1. **Drop what a precedent closes in bulk, with the reason counted.** From `$TMP/oracle.json`: rows whose `precedent` is `§16 status-4xx` or `§16 2xx-paired` (§ 16 — `§16 2xx-unpaired` stays to read), rows whose case line is a comment (an older oracle-check without the comment mask), rows whose only matcher sits on a `getBy*` / `findBy*` query (§ 14). Each removal is a line in the coverage block, never silence.
2. **Group** by (file, kind, matcher): `python3 -c 'import json,collections,sys; d=json.load(open(sys.argv[1])); c=collections.Counter((f["file"],f["kind"]) for f in d["findings"]); [print(n,k) for k,n in c.most_common()]' "$TMP/oracle.json"`, and `cut -f1,2 "$TMP/census.tsv" | sed 's/:[0-9]*$//' | sort | uniq -c | sort -rn` for the census.
3. **Rank by risk surface** from the context map: money, auth, tenant, webhook and write paths first; a group whose SUT is a pure formatter last.
4. **Read the top 30 groups**: the case, the production function, every other test of that function.
5. **Prefer the runtime bulk oracle.** One run with the strictness switches on (`expect.hasAssertions()` in setup, `-W error::pytest.PytestUnraisableExceptionWarning`, `--fail-on-risky`) turns whole groups red at once; then a scoped mutation run (`mutation-probe`) on the ranked modules. A case that fails under a switch is proven; one that survives a mutant is proven.
6. **Ledger the rest** as `Live, unreviewed (k groups / n rows)` with the command that continues them. Never `checked`.

## Scans for

Severity assumes the test runs in CI and its SUT sits on a production path. Promote one step when
the case was added or changed in the diff under review, or its SUT is money, auth, tenant or data
integrity; drop one step when another layer pins the behaviour only partly (fully pinned is Refuted
at gate 2).

| § | Class | Research ids · standard | Default |
|---|---|---|---|
| 1 | No assertion, weak sole oracle, tautology, no-op assertion API | TQ-01, TQ-02, TQ-04, TQ-10 · QG-15 | high on a write / money / auth path, else medium |
| 2 | Interaction-only where a result exists | MK-03 | medium; high on a write / money path with a count-only check |
| 3 | Assertion unreached or un-awaited | TQ-07, TQ-08, TQ-09 | high (the case cannot fail); runner-dependent |
| 4 | Failure swallowed by the test | TQ-06 | high |
| 5 | Expected value from the code under test; mock echo | TQ-04, MK-02, PBT-03 | high |
| 6 | Snapshot as the sole or self-updating oracle | TQ-03, GM-01 | medium; high when scripts or CI rewrite it, or it is the sole oracle of money logic |

### 1. No assertion, weak sole oracle, tautology

```
BAD:   it('computes the refund', () => { service.refund(order); });
       expect(total(cart)).toBeDefined();                    // `return 0` passes
       assert result is not None · assertTrue(x, 4) · assertThat(order);   // no terminal call
GOOD:  expect(total(cart)).toBe(1_150);                       // independently derived literal
       assert result == Refund(amount=1150, reason="damaged") · assertThat(order.status()).isEqualTo(PAID);
```
**Read the code:** Is existence the behaviour (a lookup that can miss, a handle, a DI resolve)? Does a helper or a supertest chain assert (oracle-check counts `expectX(` names)? Is the weak check a guard before a value check (§ 13)? Is `not.toThrow` an acceptance test paired with a rejection test (§ 17)? **Finding when** the sole check holds for a wrong value of the right type. **Proof:** break the SUT with three probes (V54); the case stays green.

### 2. Interaction-only where a result exists

```
BAD:   await service.close(orderId); expect(repo.save).toHaveBeenCalled();         // saves the wrong total, still green
GOOD:  expect(repo.save).toHaveBeenCalledWith(expect.objectContaining({ id: orderId, status: 'closed', totalCents: 1150 }));
       or assert the returned / persisted state through a real repository
```
**Read the code:** Does the SUT return or persist something checkable? Is the collaborator the *outcome* (a mailer, a publisher, an audit port the project owns — § 20)? Are the arguments pinned? `not.toHaveBeenCalled` pins "no side effect" and is not this class. **Finding when** a result exists and the case pins only that a call happened (the `count-only` rows first). **Proof:** break the SUT so it persists or returns a wrong value but still makes the call (V55).

### 3. Assertion unreached or un-awaited

```
BAD:   expect(service.load()).resolves.toEqual(order);                 // Jest 30: passes beside another file
       try { parse(raw); } catch (e) { expect(e).toBeInstanceOf(ParseError); }   // parse never throws → green
       for (const r of rows) expect(r.total).toBe(5);                   // rows = [] → green
       assert fetch_order(1)                                            # coroutine is truthy
GOOD:  await expect(service.load()).resolves.toEqual(order);
       expect(() => parse(raw)).toThrow(ParseError) · expect(rows).toHaveLength(3) before the loop
       assert await fetch_order(1) == order
```
**Read the code:** Which runner major (grep 0b; [`precedents/testing.md`](../../../../snippets/precedents/testing.md) § 1–3)? Is the promise assigned and awaited later (`const p = expect(…).rejects…; …; await p`)? Can the `catch`, callback or loop body be skipped on the path the case drives? Is `expect.assertions(n)` set in the file or setup? **Finding when** a path through the case reaches its end without executing the assertion. **Proof:** the assertion flip — change the expected value; the case stays green (V57). On Jest, run it beside another file and with the CI job's flags.

### 4. Failure swallowed by the test

```
BAD:   try { expect(calc(2)).toBe(5); } catch (e) { /* tolerate */ }
       except Exception: pass                    # around an assert
       catch (Throwable t) { }                   // around assertEquals
GOOD:  no try around assertions; assert the exception itself with toThrow / pytest.raises(match=…) / assertThrows
```
**Read the code:** Does the catch rethrow, call `fail()`, or assert on the error? Is the swallowed `.catch(() => undefined)` on a teardown call with no assertion in its chain (then it is cleanup, not this class)? `expect.hasAssertions()` does not catch this shape — the swallowed `expect` still counts. **Finding when** an assertion failure inside the case is caught and discarded. **Proof:** the assertion flip (V58).

### 5. Expected value from the code under test; mock echo

```
BAD:   const expected = price(cart); expect(price(cart)).toBe(expected);
       repo.find.mockResolvedValue(order); expect(await service.get(1)).toEqual(order);   // service maps the row
GOOD:  expect(price(cart)).toBe(1_150) · expect(await service.get(1)).toEqual({ id: 1, total: '11.50 EGP' })
```
**Read the code:** Is the both-sides call a deliberate determinism, idempotence or round-trip check (§ 18)? Does the SUT transform the mocked value, or is it a pass-through adapter (§ 21)? Is the expected value built by a helper that copies the SUT's algorithm? **Finding when** the expected side moves whenever the implementation moves. **Proof:** break the SUT (V56) — the case stays green because both sides change.

### 6. Snapshot as the sole or self-updating oracle

```
BAD:   expect(render(<Invoice order={o} />)).toMatchSnapshot();   // a 400-line tree is the only check of the totals
       "test:ci": "jest -u"                                        // CI rewrites every snapshot it would fail on
GOOD:  expect(screen.getByRole('cell', { name: /total/i })).toHaveTextContent('11.50') plus a small focused snapshot
```
**Read the code:** Is the snapshot small, deterministic and reviewed (§ 22)? Is it a characterization snapshot taken before a refactor? Does anything in scripts or CI write snapshots (6c)? **Finding when** a snapshot is the sole oracle of logic that can break, or snapshot writing is wired into a script CI runs. **Proof:** revert or break the SUT, keep the snapshot file as the run writes it — the case passes (V60); for 6c the script line is a static fact.

## Proof

The probes and their exact commands are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md)
§ Testing — *Break the SUT*, *Assertion flip*, *Strictness switches* — with the variant lists V54–V60.
Every probe runs on a scratch copy, is never committed, and ends with `git diff --exit-code` on the
probed files. A probe that turns the case red refutes the candidate.

## Output

```
assertion-strength-scan — lanes: jest 30.5 (apps/api), vitest 4.1 (apps/web), oracle-check (global copy); pytest, go, jvm absent

Findings: 2 · Unconfirmed: 1

1. apps/api/test/unit/refund.spec.ts:41                              [report-with-fix]  high
   §1 weak sole oracle — `expect(service.refund(order)).toBeDefined()` is the only check of RefundService.refund
   (src/refunds/refund.service.ts:58). Probe: refund() → `return { amountCents: 0 }`; the case stays green (V54).
   No other test pins the amount (rg 'refund\(' test/ → 2 call sites, neither asserts amountCents).
   Fix: expect(result).toEqual({ amountCents: 1150, reason: 'damaged' }) from the spec's worked example.

2. apps/api/test/unit/carrier-payload.spec.ts:17                     [report-with-fix]  high
   §3 unreached — expect(error).toBeInstanceOf(CarrierPayloadRefusal) sits in a catch the parser never enters for
   this input. Assertion flip (toBeInstanceOf(TypeError)) stays green. Fix: expect(() => parse(raw)).toThrow(CarrierPayloadRefusal).

3. apps/web/src/orders/use-close-order.test.tsx:88                    [report-flagged]   medium
   §2 interaction-only (count-only) — expect(save).toHaveBeenCalled(); the hook builds the payload.
   Unproven link: no break-the-SUT run yet. Settling probe: payload builder → wrong status; run the file.

Verification: 41 candidates → 2 findings · 1 unconfirmed · 9 hardening · 29 refuted

Class coverage:
  §1  no / weak / tautological oracle   checked (oracle-check 1,007 rows: 689 status, 110 comment pseudo-cases, 20 getBy → 188 read; census 83 → 1 finding)
  §2  interaction-only                  checked (380 cases / 55 count-only → 1 unconfirmed) · Live, unreviewed (31 groups / 325 cases — continue with `rg '^interaction-only\t' census.tsv`)
  §3  unreached / un-awaited            checked (0 floating · 2 catch sites → 1 finding · 149 loop lines, 30 groups read)
  §4  swallowed                         checked (0 try/catch · 21 teardown .catch → 0)
  §5  expected from SUT / echo          checked (16 determinism checks → 0 · 25 echoes → 0)
  §6  snapshot                          checked (27 snapshot-only cases → 0; 13 large entries, one characterization file; 0 rewrite scripts)
```

`[report-with-fix]`: the probe ran and the case stayed green, and the strengthened assertion is
written. `[report-flagged]`: one link is unproven (no probe run yet, a helper not read, a runner
version not resolved), and the row names it and the settling probe. The coverage block lists **all
six** classes on every run: `checked (k hits → m findings)` only when the lane ran on a present
stack; `N/A (<reason>)` only when no test file of any stack exists; `blocked (<reason>)` when the
lane failed or the code could not be read. A partial review reads `Live, unreviewed (k groups / n
rows)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/testing.md`](../../../../snippets/precedents/testing.md) (§ 13–24 for
this skill) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The
ones met most: a guard before a value check (§ 13); existence that is the behaviour, including a
`getBy*` query (§ 14); an exact `undefined` / `null` (§ 15); an HTTP status on a refusal test (§ 16);
`not.toThrow` paired with a rejection test (§ 17); deliberate both-sides calls (§ 18); interactions
that are the contract (§ 20); pass-through echoes (§ 21); small or characterization snapshots (§ 22);
property, contract and type tests (§ 24). Style smells — Assertion Roulette, Magic Number, naming —
are never findings (§ 43).

## When to run

- On any diff that adds or changes a test file, after `test-integrity.py` and `oracle-check.py` (§ 2–§ 6 on the changed cases).
- On a whole-repo test audit, reporting all six classes, and before trusting a coverage number.
- When a regression shipped through a path whose tests were green: run it scoped to that module first.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/testing.md`](../../../../snippets/precedents/testing.md) (`agents/verifier.md` in refute mode when the repo-baseline is installed). Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted — never drop them.
- Halt on any finding without the case `<file:line>`, the production line it claims, the probe and its result, and the strengthened assertion.
- Do not mark a row `[report-with-fix]` without a probe that kept the case green. Never probe with a `throw`.
- Do not propose deleting, skipping or loosening a test, or regenerating a snapshot, as the fix. The fix pins the behaviour named by the spec, never the code's current output.
- Do not commit a probe; end every probe with `git diff --exit-code` on the probed files.
- Do not print "no weak tests" without the class-coverage block; a lane that did not run is `blocked`, never `checked`.
- Do not re-derive a class another owner holds (§ Boundaries) — cross-link it.

## Related

- `suite-execution-scan` (this pack) — whether the cases here run at all; run it first on a whole-repo audit.
- `mutation-probe` (this pack) — measured strength; takes this skill's candidate lines as its mutation scope. `coverage-gap` — changed lines no test executes.
- `.claude/scripts/oracle-check.py` and `.claude/scripts/test-integrity.py` (repo-baseline) — the diff-time and per-case tool lanes; `agents/verifier.md` in refute mode is the independent verifier.
- `@test-reviewer` — the reviewer method whose mutation gate consumes these findings; `/add-test` — writes the strengthened test, with its mutation-verified verdict.
- [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Testing — the probes, the anti-cheat rule and V54–V60.
- `rules/testing-principles.md` — the floor these classes enforce; the engineering baseline states it as QG-15.
