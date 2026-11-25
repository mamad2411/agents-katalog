---
name: flake-source-scan
description: Find what makes tests flaky — real clock and expiring fixture dates, unseeded randomness, fixed sleeps, real network, leaked shared state, async leaks, parallel-unsafe resources, brittle e2e waits — each proved by a perturbation that flips the test.
kind: skill
pack: testing
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: flake-source-scan

## Premise

A flaky test passes and fails on the same code. The cause is something the test does not control: the wall clock and the zone, a random draw, how long the machine takes, the network, the order other tests ran in, what they left behind, what runs beside it. Order dependence is about half of Java flakes and 59% of Python ones (iDFlakies; Gruber et al., ICST 2021); 75% of flaky tests fail in co-failure clusters, with networking and external dependencies the dominant shared cause (Parry et al., EASE 2025). A flake costs twice: CI goes red for no reason, and a retry added to quiet it hides the day it goes red for a real one.

This skill is the **static, whole-suite** half. `/flaky-test-hunt` is the **runtime** half: it runs the suite N times, root-causes what flips and fixes it; this skill's grep for the root-cause class is its sibling scan. This skill finds the sources before they flip — including the ones that will: a fixture date that expires in three months, a "today" computed in UTC that is yesterday in the server's zone.

**Every finding cites the non-deterministic source `<file:line>` + the test(s) it reaches + the perturbation that flips them (or the probe that would settle it) + the deterministic fix.** A grep hit is never a finding by itself. "No flake source found" is never printed without the class-coverage block (§ Output).

**Detect statically, prove by perturbation, count only as a fallback.** Most classes here have a deterministic oracle: shift the zone, fake the date, change the seed, cut the network, reverse or shuffle the order, double the workers. One red run before the fix and one green run after prove it. Only a timing race needs the repeat-run bound — and then the result is `k of N`, never the word "flaky" or "stable" ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Perturbation and the repeat-run bound).

## The rule

A source is a finding when all four hold:

1. **It reaches an assertion or a branch.** The clock value, the random draw, the network reply, the leaked state or the timing flows into what the test asserts, or into which path the code under test takes. A clock read used only to time a step, an id that is never asserted and has no shape constraint, is not one.
2. **It varies where the suite runs.** CI's zone, date, seed, worker count, CPU and network differ from the author's machine, or will (a fixed date in the future becomes the past). Read the CI job (grep 0a) before ruling: a perturbation the CI job can never meet makes the candidate latent.
3. **Nothing in the test already pins it.** A frozen clock, a seeded generator, a net-disconnect guard, a per-test reset, an automatic restore in the runner config (grep 0a), a per-worker database.
4. **A run can show it.** The perturbation in § Proof flips the test, or the bound is stated. A candidate with no harness to run it is **Unconfirmed**, carrying the exact command.

## Boundaries

- **Retries that mask flakes** (`retryTimes`, `retries:`, `--reruns`, `@RetryingTest`, rspec-retry) → `suite-execution-scan` § 6; its retry-unmask oracle often surfaces the flake this skill then explains.
- **`--forceExit` as a mask** — a Jest run that exits 0 over a floating failing assertion → `suite-execution-scan` § 4, which reads `assertion-strength-scan` § 3 for the pairing. Here (§ 6) it is the symptom of open handles: this skill asks what the handles are. The two runs dedupe by `<file:line>`.
- **An assertion that is not awaited or never reached** (`expect(p).resolves` floating, Playwright `expect(locator)` unawaited, `expect` in a `catch`) → `assertion-strength-scan` § 3. Here: async **actions and queries** whose promise floats (§ 6c), which leak into the next test.
- **`|| true`, `continue-on-error`, path filters on the test job** → `suite-execution-scan` § 4.
- **Shared fixtures that are wrong rather than shared** (invalid factories, cascading graphs) → `test-factories`, which is also the fixer for § 5 fixture isolation.
- **A real production race the test exposes** — the test is right. It goes to `/fix-bug` with the test as its failing-first proof ([`precedents/testing.md`](../../../../snippets/precedents/testing.md) § 42).
- **Selector brittleness and node access in component tests** belong to the frontend pack's review, when installed; § 8 owns only end-to-end suites that drive a browser.

## Adapt to the codebase — the lane table

Read each runner **and its version** from the lockfile, never from memory: Vitest 5 turned `clearMocks` on by default and fails un-awaited `.resolves`, while Vitest 4 does neither; Jest 30's `--randomize` shuffles within a file only ([`precedents/testing.md`](../../../../snippets/precedents/testing.md) § 1–12). Print the lanes you ran in the output header.

| Lane | Freeze clock / zone | Seed and order | Network guard | Leak / race oracle | Repeat (k of N) |
|---|---|---|---|---|---|
| **Jest** 30 | `jest.useFakeTimers()` + `jest.setSystemTime(…)`; `TZ=…` on the command | `--randomize --seed=N` (within a file); cross-file: `jest -i a.test.ts b.test.ts` | nock `disableNetConnect()`, MSW `onUnhandledRequest: 'error'` | `--detectOpenHandles` (runs in band) | no built-in repeat: a shell loop of `npx --no jest --ci -t '<name>' <file>` |
| **Vitest** 4 / 5 | `vi.useFakeTimers()` + `vi.setSystemTime(…)` | `--sequence.shuffle --sequence.seed=N`; cross-file leaks only with `isolate: false` | as Jest | `--reporter=hanging-process` | `--repeats=N --retry=0` |
| **Playwright** 1.63 / **Cypress** 16 | `TZ=…` on the run | no order flag; `--workers`, `--shard` change neighbours | `page.route` / `cy.intercept` | — | `--repeat-each=N --retries=0 --fail-on-flaky-tests` · a loop for Cypress |
| **pytest** 9 | freezegun 1.5.5 `@freeze_time`, time-machine 3.5.1 | pytest-randomly 5.0.0 `--randomly-seed=N`; `detect-test-pollution --failing-test <id> --tests tests/` | pytest-socket 0.8.1 `--disable-socket --allow-hosts=127.0.0.1,::1` | `python -X dev -W error::ResourceWarning -m pytest`; pytest-timeout | pytest-repeat `--count=N -x -p no:randomly` |
| **Go** 1.25+ | an injected clock; `testing/synctest` for virtual time (its clock starts at 2000-01-01 UTC, so date boundaries still need an injected clock) | `-shuffle=on` (within a package; prints the seed) | `httptest.NewServer` | `-race`; goleak v1.3.0 `VerifyTestMain` | `-count=N` (`-count=1` also bypasses the cache) |
| **JVM** (JUnit 6.1, Surefire 3.6) | `Clock.fixed(…)`; `-Duser.timezone=…` | `MethodOrderer$Random` + `junit.jupiter.execution.order.random.seed`; `-Dsurefire.runOrder=random` | WireMock, MockWebServer | NonDex 2.2.5 for hash-order assumptions | `@RepeatedTest(N)` |
| **Ruby** (rspec 3.13) | `travel_to`, Timecop | `--order rand:N`; `--seed N --bisect` finds the polluter | WebMock | — | a loop |
| **PHP** (PHPUnit 13.4) | `Carbon::setTestNow` | `--order-by=random --random-order-seed=N` | `Http::fake` | — | `--repeat N` |
| **.NET** | `FakeTimeProvider` | no seeded shuffle switch is known (research, not verified): run each class alone vs the whole run | — | — | a loop of `dotnet test --filter …` |
| **Rust** | an injected clock; tokio `start_paused` | `--shuffle` is nightly-only; `cargo nextest` (a process per test) vs `cargo test` | — | — | a nextest loop with `--retries 0` |

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`.`): given no path, `rg` reads stdin whenever stdin is a pipe, and under an agent's shell that is a silent zero-hit run. Any `rg` error on stderr is a failed grep, never zero hits. `rg`'s positive `-g` globs override `-t`, so test files are selected by glob per stack family; a stack with no test files returns nothing and its rows print `N/A (no <stack> tests)`.

```bash
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**' -g '!**/.venv/**'
   -g '!**/*.min.*' -g '!**/__snapshots__/**' -g '!**/docs/**' -g '!ai/**' -g '!**/{load,loadtest,k6,benchmarks}/**')
# Test files. rg's positive -g globs override -t, so the stacks split by glob: JS/TS (TJ) and every other stack (TO).
TJ=(-g '*.{test,spec,e2e-spec,cy}.{js,jsx,ts,tsx,mjs,cjs,mts,cts}' -g '**/{__tests__,test,tests,e2e,cypress,playwright}/**/*.{js,jsx,ts,tsx,mjs,cjs,mts,cts}')
TO=(-g 'test_*.py' -g '*_test.py' -g 'conftest.py' -g '**/tests/**/*.py' -g '*_test.go' -g '**/src/test/**/*.{java,kt}' -g '*{Test,Tests,IT}.{java,kt,cs}'
    -g '*_spec.rb' -g '**/spec/**/*.rb' -g '*_test.rb' -g '*Test.php' -g '**/tests/**/*.{php,rs}' -g '**/*.Tests/**/*.cs')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')   # drops comment-only lines
H='(?!(?:localhost|127\.\d+\.\d+\.\d+|0\.0\.0\.0|\[::1\])(?:[:/"\x27\x60]|$)|[^/"\x27\x60\s]*\.(?:test|example|invalid|localhost)(?:[:/"\x27\x60]|$)|(?:[\w-]+\.)*example\.(?:com|org|net)(?:[:/"\x27\x60]|$))'
FZ='\b(?:jest|vi)\.(?:useFakeTimers|setSystemTime)\b|\bMockDate\b|\btimekeeper\b|FakeTimers\.install|freeze_?time|time_machine|Clock\.fixed|FakeTimeProvider|setTestNow|\btravel_to\b|\bTimecop\b|testing/synctest'
FN="$FZ"'|\b(?:const|let|var)\s+(?:[A-Z_]*NOW[A-Z_]*|now|fixedNow)\b\s*[:=]|\bnow\s*:\s*(?:new Date\(|[\x27"]\d{4})'
K='(?i:expir\w*|valid_?(?:until|to|thru|through)|\buntil\b|\w*Until\b|deadline|due_?(?:at|date|on)\b|\bttl\b|\w+Ttl\b|\bexp\b|\bends?_?at\b|\w+EndsAt\b|renew\w*|cutoff)'
D='["\x27\x60]20(?:2[6-9]|[34]\d)-[01]\d-[0-3]\d'

# 0. Context, not a detector. 0a: shuffle, mock-reset, fake-timer, worker, retry and exit settings in runner configs, scripts
#    and CI. 0b: files holding a network guard. 0c: test files that read the real clock and freeze nothing (an inventory).
rg -n --hidden --pcre2 '\b(?:randomize|shuffle|restoreMocks|clearMocks|resetMocks|unstubEnvs|unstubGlobals|fakeTimers|isolate|maxWorkers|workers|fullyParallel|retries|retry|forbidOnly)\b\s*[:=]|--(?:randomize|seed|sequence\.shuffle|forceExit|detectOpenHandles|runInBand|maxWorkers|workers|retries|repeat-each|reruns|randomly-seed)\b|-p\s+no:randomly|\bpytest-(?:randomly|socket|xdist|timeout|rerunfailures)\b|-shuffle=|\bgoleak\b' -g '*{jest,vitest,playwright,cypress,mocha}*.config.*' -g '.mocharc*' -g 'package.json' -g '{pytest.ini,pyproject.toml,setup.cfg,tox.ini,Makefile}' -g '.github/workflows/*.{yml,yaml}' -g '.gitlab-ci.yml' "${X[@]}" .
rg -l --pcre2 'disableNetConnect|onUnhandledRequest\s*:\s*["\x27]error|--disable-socket|\bdisable_socket\b|\bsetupServer\(|\bMockAgent\b' "${TJ[@]}" "${TO[@]}" "${X[@]}" .
rg -l0 --pcre2 '\bnew\s+Date\s*\(\s*\)|\bDate\.now\s*\(\s*\)' "${TJ[@]}" "${X[@]}" . | xargs -0 -r rg -l --files-without-match --pcre2 "$FZ" | wc -l

# 1. Clock. 1a calendar or zone read off a real or parsed date (flips under TZ); 1b fixed near-future dates by an
#    expiry word, in files that freeze no clock (time bombs) — a JS/TS unit test is kept only when a module it imports
#    (or one those import) reads the real clock, tagged with that line; e2e and other stacks keep every hit; 1c other stacks' real-clock reads in files that freeze none;
#    1d the zone read in a module under test.
rg -n --pcre2 'expect\([^;\n]*(?:new\s+Date\(\s*\)|Date\.now\(\s*\))|\.(?:getDate|getDay|getMonth|getFullYear|getHours|toDateString|toLocaleDateString|toLocaleTimeString|toLocaleString)\(\s*\)|\.toISOString\(\)\s*\.\s*(?:slice|substring|substr|split)\(|\bdatetime\.(?:now|today)\(\s*\)\.(?:date|day|month|year|hour|strftime)|\bdate\.today\(\)' "${TJ[@]}" "${TO[@]}" "${X[@]}" . | "${NC[@]}"
rg -l0 --pcre2 "$K[^\n]{0,80}$D|$D[^\n]{0,80}$K" "${TJ[@]}" "${TO[@]}" "${X[@]}" . | xargs -0 -r rg -l0 --files-without-match --pcre2 "$FN" | xargs -0 -r rg -Hn --pcre2 "$K[^\n]{0,80}$D|$D[^\n]{0,80}$K" | "${NC[@]}" | python3 -c '
import os, re, sys
CLK = re.compile(r"\bnew\s+Date\s*\(\s*\)|\bDate\.now\s*\(|\b(?:datetime|date)\.(?:now|today|utcnow)\s*\(|\btime\.time\s*\(|\btime\.Now\s*\(")
def res(base, spec):                           # a relative or `@/` import → a source file, else None
    if spec.startswith("@/"):
        d = base
        while d and os.path.basename(d) != "src": d = os.path.dirname(d)
        if not d: return None
        p = os.path.join(d, spec[2:])
    elif spec.startswith("."): p = os.path.normpath(os.path.join(base, spec))
    else: return None
    for c in (p, *(p + e for e in (".ts", ".tsx", ".js", ".jsx", ".mjs")), *(os.path.join(p, "index" + e) for e in (".ts", ".tsx", ".js"))):
        if os.path.isfile(c): return c
    return None
def reads(f, depth, seen):                     # the first real-clock read in f or what it imports (2 levels), or None
    if f in seen: return None
    seen.add(f); s = open(f, errors="replace").read()
    for i, l in enumerate(s.split("\n"), 1):
        if CLK.search(l) and not l.lstrip().startswith(("//", "*")): return "%s:%d" % (f, i)
    if depth:
        for spec in re.findall(r"from\s+[\x27\"]([^\x27\"]+)[\x27\"]", s):
            r = res(os.path.dirname(f), spec)
            if r and not re.search(r"\.(?:test|spec)\.", r):
                hit = reads(r, depth - 1, seen)
                if hit: return hit
    return None
cache = {}
for l in sys.stdin:
    f = l.split(":", 1)[0]
    if f not in cache:
        if re.search(r"e2e|\.flow\.|/flows?/|\.py$|\.go$|\.rb$|\.java$|\.kt$|\.cs$|\.php$", f): cache[f] = "  [e2e or non-JS: the app reads the clock — read]"
        else:
            s = open(f, errors="replace").read(); specs = re.findall(r"from\s+[\x27\"]([^\x27\"]+)[\x27\"]", s)
            local = [x for x in specs if x.startswith((".", "@/"))]; rs = [res(os.path.dirname(f), x) for x in local]
            hit = next((h for h in (reads(r, 1, set()) for r in rs if r) if h), None)
            cache[f] = "  [SUT reads the clock: %s]" % hit if hit else "  [imports unresolved — read]" if None in rs else None
    if cache[f]: print(l.rstrip("\n") + cache[f])'
C='\b(?:datetime|date|dt|timezone)\.(?:now|today|utcnow)\s*\(|\btime\.time(?:_ns)?\s*\(\s*\)|\btime\.Now\s*\(\s*\)|\b(?:LocalDate|LocalDateTime|ZonedDateTime|OffsetDateTime|Instant)\.now\s*\(\s*\)|\bSystem\.currentTimeMillis\s*\(|\b(?:Time|Date|DateTime)\.(?:now|today|current)\b|\bCarbon(?:Immutable)?::(?:now|today)\s*\(|\bDateTime(?:Offset)?\.(?:Now|UtcNow|Today)\b|\b(?:Utc|Local)::now\s*\(|\bSystemTime::now\s*\(|(?<![\w>$:])(?:time|microtime|now|today)\s*\(\s*\)|\bnew\s+\\?DateTime(?:Immutable)?\s*\(\s*\)'
rg -l0 --pcre2 "$C" "${TO[@]}" "${X[@]}" . | xargs -0 -r rg -l0 --files-without-match --pcre2 "$FZ" | xargs -0 -r rg -Hn --pcre2 "$C" | "${NC[@]}"
# 1d. The zone read in the code under test (1a sees only the test): a zone-dependent format or calendar read in shipped
#     JS/TS/Python with no timeZone / tz on the line, in a module that a test asserting a date literal imports by name.
#     Prints `source:line <- test:line` (the test's first date-literal assertion): the flake shows in the test, the fix
#     goes on the source line.
ZD='\.toLocale(?:Date|Time)?String\((?![^\n]*timeZone)|\bnew\s+Intl\.DateTimeFormat\((?![^\n]*timeZone)|\.get(?:Date|Day|Month|FullYear|Hours)\(\s*\)|\bdatetime\.fromtimestamp\((?![^\n]*\btz\b)|\.astimezone\(\s*\)'
DL='(?:expect|assert|toBe|toEqual|toHaveTextContent|toContain)[^\n]*["\x27\x60][^"\x27\x60\n]*(?:\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s\d{1,2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b\d{4}-\d{2}-\d{2}["\x27\x60])'
Z=$(mktemp -d "${TMPDIR:-/tmp}/flake-scan.XXXXXX"); rg -n --pcre2 "$ZD" -g '*.{js,jsx,ts,tsx,mjs,cjs,mts,cts,py,vue,svelte}' -g '!*.{test,spec,e2e-spec,cy,stories}.*' -g '!**/{__tests__,test,tests,e2e,cypress,playwright,spec,__mocks__}/**' -g '!{test_*,*_test,conftest}.py' "${X[@]}" . | "${NC[@]}" > "$Z/src"
rg -n --pcre2 "$DL" "${TJ[@]}" "${TO[@]}" "${X[@]}" . > "$Z/dl"; cut -d: -f1 "$Z/dl" | sort -u | tr '\n' '\0' | xargs -0 -r rg -H -o -N --pcre2 "(?:from\s+|require\(\s*|import\s+)['\"][^'\"]+['\"]|^\s*from\s+[\w.]+\s+import\s+[\w, ]+" > "$Z/imp"
python3 - "$Z/src" "$Z/imp" "$Z/dl" <<'PY'
import os, re, sys, collections
src, dl, out = collections.defaultdict(set), {}, collections.defaultdict(set)
for l in open(sys.argv[1], errors='replace'):
    f, n, _ = l.split(':', 2); src[re.sub(r'\.[^./]+$', '', os.path.basename(f))].add(f'{f}:{n}')
for l in open(sys.argv[3], errors='replace'):
    t, n, _ = l.split(':', 2); dl.setdefault(t, n)
for l in open(sys.argv[2], errors='replace'):
    t, spec = l.rstrip('\n').split(':', 1); q = re.search(r"['\"]([^'\"]+)['\"]", spec)
    for b in [re.sub(r'\.(?:[cm]?[jt]sx?|py|vue|svelte)$', '', q[1].rsplit('/', 1)[-1])] if q else re.findall(r'\w+', spec):
        for s in src.get(b, ()): out[s].add(f'{t}:{dl[t]}')
for s in sorted(out): print(f'{s}  <- {", ".join(sorted(out[s]))}')
PY

# 2. Unseeded randomness: 2a JS/TS in files that seed nothing; 2b every other stack.
R='\bMath\.random\s*\(|\bcrypto\.randomUUID\s*\(|\b(?:uuid)?v4\s*\(\s*\)|\bnanoid\s*\(|\bfaker\.(?!seed\b)\w+\.\w+\s*\(|\bchance\.\w+\s*\('
rg -l0 --pcre2 "$R" "${TJ[@]}" "${X[@]}" . | xargs -0 -r rg -l0 --files-without-match --pcre2 '\bfaker\.seed\(|\bseedrandom\b|\.seed\(\s*\d' | xargs -0 -r rg -Hn --pcre2 "$R" | "${NC[@]}"
rg -n --pcre2 '\brandom\.(?:random|randint|randrange|choice|choices|shuffle|sample|uniform|getrandbits)\s*\(|\bnp\.random\.(?:rand|randn|randint|choice|random|shuffle|permutation)\s*\(|\bFaker\s*\(\s*\)|(?<![\w.])rand\.(?:Int|Intn|IntN|Int31n?|Int63n?|Int64N?|Float64|Perm|Shuffle|N)\s*\(|\bnew\s+(?:java\.util\.|System\.)?Random\s*\(\s*\)|\bMath\.random\s*\(|\bThreadLocalRandom\.current\s*\(|\bRandom\.Shared\b|\bFaker::\w+|\$this->faker->|(?<![\w>$:.])(?:mt_rand|random_int|array_rand|str_shuffle)\s*\(|\brand::(?:random|thread_rng|rng)\s*\(|\bfastrand::\w+\s*\(|\buuid\.(?:uuid[14]|New|NewString|NewRandom|NewV7)\s*\(|\bUUID\.randomUUID\s*\(|\bGuid\.NewGuid\s*\(|\bUuid::new_v[47]\s*\(|\bStr::(?:random|uuid|orderedUuid|ulid)\s*\(|\bSecureRandom\.\w+|(?<![\w.:$>])rand\s*\(|\bRandom\.next\w*\s*\(' "${TO[@]}" "${X[@]}" . | "${NC[@]}"

# 3. Fixed sleeps: 3a JS/TS; 3b every other stack; 3c elapsed-time upper bounds asserted in a unit test.
rg -n --pcre2 'new\s+Promise\s*\(\s*\(?\s*(\w+)\s*\)?\s*=>\s*setTimeout\s*\(\s*\1\s*,\s*[1-9]\d*|\bawait\s+(?:setTimeout|sleep|delay|wait|pause)\s*\(\s*[1-9][\d_]*\s*\)|(?<![\w.])(?:sleep|delay|wait)\s*\(\s*[1-9][\d_]*\s*\)' "${TJ[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '(?<![\w.])(?:(?:time|asyncio|trio|anyio|gevent)\.)?sleep\s*\(\s*(?!0(?:\.0*)?\s*\))(?:\d+(?:\.\d*)?|\.\d+)\s*\)|\btime\.Sleep\s*\(|\b(?:Thread\.sleep|TimeUnit\.\w+\.sleep|SystemClock\.sleep)\s*\(|(?<![\w.:])sleep\s+(?!0+(?:\.0+)?(?![\d.]))\d|(?<![\w:>$\\])usleep\s*\(\s*(?!0\s*\))\d|\bThread\.Sleep\s*\(|\bTask\.Delay\s*\(\s*(?!0\s*\)|TimeSpan\.Zero)|\b(?:std::)?thread::sleep\s*\(|\b(?:tokio::time|async_std::task)::sleep\s*\(' "${TO[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 'expect\(\s*\w*(?:[Dd]uration|[Ee]lapsed|[Tt]ook|[Ll]atency|[Mm]s)\w*\s*\)\.toBeLessThan(?:OrEqual)?\(|\bassert\s+\w*(?:duration|elapsed|took|latency)\w*\s*<|\bassert(?:True|That)\s*\(\s*\w*(?:[Dd]uration|[Ee]lapsed|[Ll]atency)\w*\s*<' "${TJ[@]}" "${TO[@]}" "${X[@]}" . | "${NC[@]}"

# 4. A literal external URL called from a test: 4a JS/TS; 4b every other stack. Read 0b first: a hit in a file that
#    holds an interceptor is a read, not a candidate.
rg -n --pcre2 "\b(?:fetch|axios(?:\.(?:get|post|put|patch|delete|head|request))?|got(?:\.\w+)?|superagent\.\w+|request(?:\.\w+)?|https?\.(?:get|request)|ky(?:\.\w+)?)\s*\(\s*[\"'\x60]https?://$H" "${TJ[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 "\b(?:requests|httpx|session|client)\.(?:get|post|put|patch|delete|head|request)\s*\(\s*f?[\"']https?://$H|\burlopen\s*\(\s*[\"']https?://$H|\bhttp\.(?:Get|Head|Post|PostForm|NewRequest(?:WithContext)?)\s*\((?:\s*ctx\s*,)?\s*(?:\"[A-Z]+\"\s*,\s*)?\"https?://$H|\b(?:Net::HTTP\.\w+|HTTParty\.\w+|Faraday\.\w+|RestClient\.\w+|URI\.open)\s*\(\s*(?:URI\s*\(\s*)?[\"']https?://$H|(?:file_get_contents|curl_init|Http::(?:get|post|put|patch|delete))\s*\(\s*[\"']https?://$H|\.(?:GetAsync|PostAsync|PutAsync|DeleteAsync|SendAsync|GetStringAsync|GetFromJsonAsync)\s*\(\s*(?:new\s+Uri\s*\(\s*)?\"https?://$H|\breqwest::(?:blocking::)?get\s*\(\s*\"https?://$H|(?:URI\.create|new\s+URL|\.uri|getForObject|getForEntity|postForObject|postForEntity|exchange)\s*\(\s*\"https?://$H" "${TO[@]}" "${X[@]}" . | "${NC[@]}"

# 5. Shared state. 5a JS/TS env writes in files that restore nothing — a key set then `delete`d, a restore loop, and
#    a module-scope write under Jest (each test file gets its own process.env copy) are dropped; 5b files that spy and never restore (moot when 0a shows
#    restoreMocks); 5c empty module-level containers in files that never reset them; 5d other stacks' process-global writes
#    and module / static state; 5e beforeAll / session / class fixtures that create data, and @DirtiesContext.
E='\bprocess\.env(?:\.\w+|\[\s*[\x27"\x60]?\w+[\x27"\x60]?\s*\])\s*=(?!=)|\bdelete\s+process\.env\b|\bObject\.assign\s*\(\s*process\.env\b'
rg -l0 --pcre2 "$E" "${TJ[@]}" "${X[@]}" . | xargs -0 -r rg -l0 --files-without-match --pcre2 '\bprocess\.env\s*=\s*(?:\{\s*\.\.\.|\w*(?:OLD|ORIG|SAVED|old|orig|saved|original|prev|backup)\w*)|\bObject\.assign\s*\(\s*process\.env\s*,\s*\w*(?:OLD|ORIG|SAVED|old|orig|saved|original|prev|backup)\w*\s*\)|\b(?:vi\.unstubAllEnvs|jest\.replaceProperty|vi\.stubEnv)\b|=\s*process\.env\.\w+\s*;?\s*$' | xargs -0 -r rg -Hn --pcre2 "$E" | "${NC[@]}" | python3 -c '
import os, re, sys, collections
K = r"process\.env(?:\.(\w+)|\[\s*[\x27\"\x60]?(\w+)[\x27\"\x60]?\s*\])"
hits = collections.defaultdict(list)
for l in sys.stdin: f, n, t = l.rstrip("\n").split(":", 2); hits[f].append((n, t))
def jest(f):                                   # Jest gives each test file its own copy of process.env
    d = os.path.dirname(f)
    while True:
        if any(re.match(r"jest(?:\.[\w-]+)?\.config\.[cm]?[jt]s$|jest\.json$", x) for x in os.listdir(d or ".")): return True
        if any(re.match(r"vitest\.config\.", x) for x in os.listdir(d or ".")) or d in ("", "."): return False
        d = os.path.dirname(d)
for f, rows in hits.items():
    src = open(f, errors="replace").read()
    dele = {a or b for a, b in re.findall(r"\bdelete\s+" + K, src)}
    for n, t in rows:
        if re.search(r"\bif\s*\(\s*\w+\s*===?\s*undefined\s*\)\s*delete\s+process\.env|^\s*else\s+process\.env\[", t): continue   # a restore loop
        w = [a or b for a, b in re.findall(K + r"\s*=(?!=)", t)]
        if w and all(k in dele for k in w): continue                       # set, then deleted in this file: restored (read: was it set before?)
        if re.match(r"\s*delete\s", t): continue                            # the restore half
        if jest(f) and not t[:1].isspace(): continue                        # module scope under Jest: the whole file, no order
        print("%s:%s:%s%s" % (f, n, t, "  [jest: per-file env]" if jest(f) else ""))'
rg -l0 --pcre2 '\b(?:jest|vi)\.spyOn\(' "${TJ[@]}" "${X[@]}" . | xargs -0 -r rg -l --files-without-match --pcre2 '\bmockRestore\(|\b(?:jest|vi)\.restoreAllMocks\('
M='^(?:export\s+)?(?:const|let|var)\s+\w+(?:\s*:\s*[^=\n]+)?\s*=\s*(?:\[\s*\]|\{\s*\}|new\s+(?:Map|Set|WeakMap|Array)\s*(?:<[^>\n]*>)?\s*\(\s*\))\s*;?\s*$'
rg -l0 --pcre2 "$M" "${TJ[@]}" "${X[@]}" . | xargs -0 -r rg -l0 --files-without-match --pcre2 '\.length\s*=\s*0|\.clear\(\s*\)|\.splice\(\s*0\b|^\s*\w+\s*=\s*(?:\[\s*\]|\{\s*\}|new\s+(?:Map|Set)\b)' | xargs -0 -r rg -Hn --pcre2 "$M" | "${NC[@]}"
rg -n --pcre2 '\bos\.environ\s*\[[^\]]+\]\s*=(?!=)|\bos\.environ\.(?:update|setdefault|pop|clear)\s*\(|\bos\.(?:putenv|unsetenv)\s*\(|\bpatch(?:\.object|\.dict|\.multiple)?\s*\([^)]*\)\s*\.start\s*\(|\bos\.(?:Setenv|Unsetenv|Clearenv|Chdir)\s*\(|\bSystem\.(?:setProperty|clearProperty|setOut|setErr)\s*\(|\b(?:TimeZone|Locale)\.setDefault\s*\(|\bENV\s*\[[^\]]+\]\s*=(?!=)|(?<![\w>$:])putenv\s*\(|\bdate_default_timezone_set\s*\(|\bEnvironment\.SetEnvironmentVariable\s*\(|\bCultureInfo\.(?:Default)?(?:Current|DefaultThread)(?:UI)?Culture\s*=(?!=)|\b(?:std::)?env::(?:set_var|remove_var|set_current_dir)\s*\(|\bdel\s+os\.environ\b|\b\w*patcher\w*\.start\s*\(|\$_(?:ENV|SERVER)\s*\[[^\]]+\]\s*=(?!=)|\bENV\.(?:store|update|merge!|delete|replace|clear)\b|^(?!__)[A-Za-z_]\w*\s*(?::\s*[^=\n]+)?=\s*(?:\[\s*\]|\{\s*\}|set\(\s*\)|dict\(\s*\)|list\(\s*\)|(?:collections\.)?(?:defaultdict|OrderedDict|Counter|deque)\()|^var\s+(?!_\b)\w+\s*(?:[\w.\[\]*]+\s*)?=\s*(?:map\[|\[\][\w.*]+\{|make\s*\()|^\s*(?:(?:private|protected|public|internal)\s+)?static\s+(?!final\b|readonly\b|class\b|void\b|async\b|function\b|\{)(?![^=;\n]*\b\w*(?:Container|Extension|Server)\b)[\w<>,.?\[\]$\\| ]+?\s+\$?\w+\s*(?:=|;)|\bcompanion\s+object\b[^}\n]*\bvar\s+\w+|^(?:\$\w+|@@\w+)\s*(?:\|\|)?=(?!=)|^\s*(?:(?:private|protected|public)\s+)?static\s+(?:\??[\w\\|]+\s+)?\$\w+\s*(?:=|;)|^\s*(?:pub\s+)?static\s+(?:mut\s+\w+|\w+\s*:\s*(?:Mutex|RwLock|Atomic\w+|RefCell|Cell)\b)' "${TO[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\b(?:beforeAll|before)\s*\(\s*(?:async\s*)?(?:\(\s*\)|function\s*\(\s*\))\s*(?:=>)?\s*\{?\s*\w+\s*=\s*(?:await\s+)?(?!\w*(?:[Ss]tart|[Ll]isten|[Cc]onnect|[Ll]aunch|[Ss]erver|[Cc]lient|[Bb]rowser|[Pp]ool)\b)[\w.]*(?:create|insert|save|seed|build|factory|make)\w*\s*\(|@pytest\.fixture\s*\([^)]*\bscope\s*=\s*[\x27"](?:session|module|package|class)[\x27"]|\bbefore\s*\(\s*:(?:all|context)\s*\)|\bbefore_all\b|\bfunction\s+setUpBeforeClass\s*\(|^\s*@DirtiesContext\b' "${TJ[@]}" "${TO[@]}" "${X[@]}" . | "${NC[@]}"

# 6. Async leaks: 6a forced exit or disabled shuffle in scripts / CI / config; 6b fake timers never restored in the file;
#    6c an async testing-library or user-event call at statement start with no await; 6d intervals never cleared.
rg -n --hidden --pcre2 -e '--forceExit\b|\bforceExit\s*:\s*true|-p\s+no:randomly\b' -g 'package.json' -g '*.{yml,yaml}' -g 'Makefile' -g '*{jest,vitest}*.config.*' -g '{pytest.ini,pyproject.toml,setup.cfg,tox.ini}' "${X[@]}" .
rg -l0 --pcre2 '\b(?:jest|vi)\.useFakeTimers\s*\(' "${TJ[@]}" "${X[@]}" . | xargs -0 -r rg -l --files-without-match --pcre2 '\b(?:jest|vi)\.useRealTimers\s*\('
rg -n -U --pcre2 '[;{][ \t]*\n[ \t]*\K(?:waitFor|screen\.findBy\w+|user(?:Event)?\.(?:click|dblClick|tripleClick|type|clear|selectOptions|deselectOptions|upload|hover|unhover|tab|keyboard|paste|pointer))\s*\(' "${TJ[@]}" "${X[@]}" . | "${NC[@]}"
rg -l0 --pcre2 '\bsetInterval\s*\(' "${TJ[@]}" "${X[@]}" . | xargs -0 -r rg -l --files-without-match --pcre2 '\bclearInterval\s*\(|useFakeTimers'

# 7. Environment: 7a fixed ports and temp paths; 7b concurrent tests in one process; 7c Python set order asserted.
rg -n --pcre2 '\.listen\s*\(\s*(?!0\b)\d{2,5}\b|\b(?:port|PORT)\s*[:=]\s*(?!0\b)\d{4,5}\b|[\x27"]/(?:var/)?tmp/[\w.-]+[\x27"]|\bnet\.Listen(?:TCP|UDP|Packet)?\s*\(\s*"(?:tcp|udp)[46]?"\s*,\s*"[^"]*:(?!0")\d+"' "${TJ[@]}" "${TO[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\b(?:describe|test|it)\.concurrent\b|\bsequence\s*:\s*\{[^}\n]*concurrent\s*:\s*true|parallel\.mode\.default\s*=\s*concurrent' "${TJ[@]}" "${TO[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\blist\(\s*(?:set|frozenset)\([^\n]*\)\s*==|==\s*list\(\s*(?:set|frozenset)\(|\[\s*0\s*\][^\n]*=\s*(?:list\()?\w*set\(' "${TO[@]}" "${X[@]}" . | "${NC[@]}"

# 8. E2E brittleness, in files that drive a browser: fixed waits, networkidle, force, read-once assertions, CSS / XPath / nth.
rg -l0 --pcre2 '@playwright/test|\bcy\.(?:visit|get)\b|\bpage\.goto\(' "${TJ[@]}" "${X[@]}" . | xargs -0 -r rg -Hn --pcre2 "\bwaitForTimeout\s*\(|\bcy\.wait\(\s*\d|\bwaitForLoadState\(\s*['\"]networkidle|\bwaitUntil\s*:\s*['\"]networkidle|\{\s*force:\s*true|expect\(\s*await\s+[^;]*\.(?:isVisible|isHidden|isEnabled|isDisabled|isChecked|textContent|innerText|getAttribute|inputValue)\(\)\s*\)|(?:locator|cy\.get)\(\s*['\"\x60](?:[^'\"\x60]*(?::nth-(?:child|of-type)|\s>\s|\.(?:css|sc|jsx|emotion)-[\w-]+)|//|xpath=)|\.nth\(\s*\d+\s*\)" | "${NC[@]}"
```

A finding is a grep hit **plus** a read of the test **plus** the path from the source to an assertion or branch **plus** the run that flips it. Four blind spots are structural; work around them rather than trust a quiet grep:

- **File-level filters hide mixed files.** 1b, 1c, 2a, 5a, 5c and 6b drop a whole file when it freezes, seeds, restores or resets *anywhere*. A file that freezes the clock in one `describe` and reads it raw in another is missed. When the context map shows a money, auth or date-heavy module, read its test files directly.
- **The source is often in the code under test.** A test that never touches the clock flakes when the service it calls reads `new Date()` or `NOW()`. 0c is the inventory of the test side only. 1d reaches one shape across the boundary — a zone-dependent format or calendar read in a module that a date-asserting test imports by name; a clock read behind a service, a helper or the database (`NOW()`) is still found only by the run in § Proof — perturb the whole suite, not the grep hits.
- **Helpers move the sleep.** 3a keys on `sleep` / `delay` / `wait`. A project helper with another name (`settle()`, `tick(500)`) is missed: add its name to the line after reading `test/support`.
- **Unordered results come from the database.** Rows from a query with no `ORDER BY`, asserted by index (`body.data[0]`), flip with the planner — no grep separates them from single-row results (548 such assertions on the measured repo below, nearly all single-row). Read the query behind every multi-row index assertion in a list test; NonDex 2.2.5 (JVM) and `PYTHONHASHSEED=random` (Python) are the runtime oracles for in-memory order.

**Measured** (2026-10-05, read-only). On a real NestJS-on-Fastify + MikroORM API (Jest 30) with a React web app (Vitest 4, Playwright 1.63) — about 14,200 tracked files, 3,328 JS/TS test files — the script runs in about 2 s and returns: 0a 16 config lines (`clearMocks` only, no shuffle anywhere, `--forceExit` on the e2e job); 0b 0 guard files; 0c 590 test files read the real clock and freeze nothing (the inventory, not candidates); 1a 111 (`new Date().toISOString().slice(0, 10)` used as "today" in e2e helpers — the UTC day, not the local one; `getDate()` / `getHours()` on parsed dates); 1b 77 raw, 47 after the frozen-clock filter (`expiryDate: '2026-12-31'` in a stock-ledger e2e and `dueDate: '2026-10-20'` — both expire within months; a `settledAt` false hit fixed with `\bttl\b`); 1d 61 source lines in 16 modules, reached by 22 date-asserting test files (local-calendar reads — `getMonth()` / `getDate()` building a `YYYY-MM-DD` — read whether the test builds a local `Date`, zone-safe, or parses a UTC instant, which flips); 2a 120 (unique phones and codes from `Math.random()` — opaque, except `+2010${Math.floor(Math.random() * 1e8)}`, whose digit count depends on the draw); 3a 99 (`setTimeout(resolve, 100)` waits for async processing in e2e — candidates); 3c 2; 4a 0; 5a 29; 5b 47 files; 5c 344 raw, 89 after the reset filter (module-level request recorders); 6a 4; 6c 0 (a line-start form returned 6, all multi-line arrow returns; the statement-start anchor removed them); 7a 3; 8: 20 lines in 6 browser-driving files (`waitForTimeout(300 … 1200)` in flows, one `xpath=ancestor::form`). Re-measured 2026-10-15 on the same repo: 1b 52 → 41 — 11 rows in unit tests whose imported modules never read the real clock (wire mappers: the date is data) dropped; the 21 e2e rows stay; 5a 27 → 8 — keys set in `beforeAll` and `delete`d in `afterAll`, a save-and-`Object.assign` restore, a restore loop and module-scope writes in Jest files dropped (Jest builds one environment per test file, with its own copy of `process.env` — jest-util `createProcessObject`, read 2026-10-15); `brittle-suite` keeps its 1b seed and its four 5a lines. Every other line returned 0. Against the research corpus of tagged positives and decoys for 65 per-stack patterns, the script hits no decoy; its misses are the routed retries and the same-file decoys the file-level filters drop by design. The other `benchmarks/fixtures/*` seed no flake class: at most one line per grep (a SQL `now()` in a fixture insert, a `uuid4()` id). On `brittle-suite` (2.0.1) 1d prints one line, the seeded component and its test — the `toLocaleDateString` with no `timeZone` behind a `Mar 29` assertion — and not the coupon decoy, whose module reads no zone.

## The 3,000-hit path

1. **Intersect with what runs.** Keep files collected by a runner config and run by a CI job (0a). Dismiss a directory of probes, load scripts or one-off tools with **one** read that shows no config collects it, and name it in the coverage block.
2. **Group.** One group = (source shape, helper or fixture it lives in). A helper used by 80 tests is one group; one decision covers it.
3. **Rank by risk surface.** Money, auth, tenant, webhook and write paths first (the context map from the security and backend packs when present), then tests CI history shows red-then-green on the same commit.
4. **Read the top 30 groups fully.**
5. **Prefer the runtime bulk oracle at scale.** Run the whole suite once per perturbation instead of reading hits: `TZ=Pacific/Kiritimati`, `TZ=America/St_Johns`, a faked date a year ahead, three shuffle seeds, the network off, double the workers. Each test that turns red is a confirmed site; trace it back to its source line. This is the measured way through 590 clock-reading files.
6. **Ledger the rest.** `Live, unreviewed (k groups / n hits)` with the command that continues them; never `checked`.

## Scans for

Severity: a flake proven on a test that guards money, auth, tenant isolation or a write path is **high**; one CI already shows failing (red and green on one commit) is **high**; otherwise the class default. A source the CI job can never meet (a zone it does not run in, a perturbation it does not apply) is latent: Hardening, unless the date makes it certain (§ 1). Research classes FL-01…FL-18 and UI-01…UI-05 map as listed.

| § | Class | Research ids | Default |
|---|---|---|---|
| 1 | Clock, zone and calendar; fixture dates that expire | FL-04 | medium; **high** for a date that expires within 90 days on a collected test |
| 2 | Unseeded randomness feeding an assertion, a branch or a constrained shape | FL-06, FX-03 | low; medium when the shape constraint can fail |
| 3 | Fixed sleeps as synchronisation; tight elapsed-time bounds | FL-07, FL-16 | medium |
| 4 | Real network from a unit or integration test | FL-10 | medium |
| 5 | Shared mutable state and order dependence | FL-01, FL-02, FL-03, FL-14, FL-15 | medium |
| 6 | Async leaks: open handles behind a forced exit, timers, floating actions | FL-05, FL-12, FL-18 (exit) | medium |
| 7 | Parallel and platform assumptions | FL-08, FL-09, FL-11, FL-17 | medium |
| 8 | Brittle end-to-end waits, actions and selectors | UI-01, UI-03, UI-04, UI-05 | low; medium when the suite is quarantined or retried for it |

Routed: FL-13 (retry masking) → `suite-execution-scan` § 6; FL-18's `|| true` / `continue-on-error` → `suite-execution-scan` § 4. FL-18's "no shuffle anywhere" is reported here as the `order` line of the coverage block (§ Output), never as a finding by itself.

### 1. Clock, zone and calendar

```
BAD:   const today = new Date().toISOString().slice(0, 10);      // the UTC day; local midnight to 03:00 in UTC+3 is "yesterday"
       expect(due.getDate()).toBe(5)                             // parsed in UTC, read in the runner's zone
       { expiresAt: '2026-12-31' }                               // valid today, expired on 1 January; the SUT compares it to now
GOOD:  vi.setSystemTime(new Date('2028-02-29T23:59:59Z')); const today = formatInZone(clock.now(), tz)
       { expiresAt: addDays(clock.now(), 30) }  ·  an injected Clock / FakeTimeProvider / freeze_time
```
**Read the code:** Does the value reach an assertion or a branch, or only a log or a duration? For a fixed date: does the code under test compare it to the real clock (expiry, validity, scheduling)? A pure wire-mapping test that never reads the clock is a precedent. Is the clock frozen elsewhere for this test (a shared setup file, a global `fakeTimers` config)? What zone does the CI job run in, and the production server? For a 1d row: does the test build the date from local parts (`new Date(2026, 2, 29)`, zone-safe) or parse an instant (`'2026-03-29T00:30:00Z'`, a different day west or east of UTC)? Is `TZ` pinned in the runner config or the CI job (then the row is latent — Hardening — until a developer runs it elsewhere)? **Finding when** a real or zone-dependent date reaches an assertion or branch and nothing pins it. **Proof:** the suite (or the file) under `TZ=Pacific/Kiritimati` and `TZ=America/St_Johns`, and under `faketime '<the fixture date + 1 day>'`; red before, green after a frozen or injected clock — deterministic, one run each ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Perturbation and the repeat-run bound; variant V68). The production code often has the same date bug: when the zone run fails in the SUT rather than the test, route it to `/fix-bug`.

### 2. Unseeded randomness

```
BAD:   phone: `+2010${Math.floor(Math.random() * 1e8)}`         // 5 to 12 digits: a short draw fails the validator
       email = faker.internet.email()                            // asserted later; a rare value (apostrophe, unicode) fails
GOOD:  faker.seed(1234) once per file, printed on failure  ·  a sequence: `+2010${String(n).padStart(8, '0')}`
       random.Random(42) · np.random.default_rng(0) · StdRng::seed_from_u64(7) · opaque ids that are never asserted
```
**Read the code:** Is the value asserted, used in a branch, or constrained (length, format, uniqueness)? A unique id whose shape cannot fail validation is a precedent; a draw whose shape varies, or a unique-constraint value with a birthday-bound collision across the suite, is not. pytest-randomly reseeds `random` and Faker per test, so a defect hides within one seed — and `np.random.default_rng()` is not reset at all. **Finding when** the draw can produce a value the test or a validator rejects. **Proof:** three seeds (`--randomly-seed=1..3`, `faker.seed(n)`), or the failing value forced into the probe; else the repeat-run bound (V69).

### 3. Fixed sleeps and tight timing bounds

```
BAD:   await new Promise((r) => setTimeout(r, 100)); expect(job.status).toBe('done')   // a guess at how long the queue takes
       page.waitForTimeout(500) · time.sleep(1) · Thread.sleep(200)
       expect(elapsedMs).toBeLessThan(100)                                              // a unit test asserting speed
GOOD:  await vi.waitFor(() => expect(repo.find(id)).resolves.toMatchObject({ status: 'done' }))
       Awaitility await().atMost(5, SECONDS).until(…) · Gomega Eventually · synctest.Wait() · fake timers
```
**Read the code:** What is the sleep waiting for? Is there a signal to wait on instead (an event, a row, a promise, a readiness probe)? Under fake timers or `synctest`, a sleep is virtual (precedent). A sleep that *is* the behaviour (a TTL, a debounce) with slack on the safe side is a precedent. **Finding when** a fixed sleep stands in for a condition the test could await. **Proof:** the test under CPU stress (`stress-ng --cpu $(nproc)` beside the run, or `taskset -c 0`) and doubled workers, k of N; halving the sleep is a quick read — still green means it was pointless, red means a race (V69). Sleeps cluster: read the helper and the file's other sleeps before fixing one.

### 4. Real network

```
BAD:   const rate = await fetch('https://api.exchangerate.host/latest')     // in a unit test
       requests.get("https://payments.acme.io/v1/x") · http.Get("https://…")
GOOD:  nock.disableNetConnect() in setup + nock('https://api…').get(…).reply(…) · MSW onUnhandledRequest: 'error'
       pytest --disable-socket · httptest.NewServer · WireMock · a port the project owns, faked
```
**Read the code:** Is the suite a tagged e2e or contract suite outside the unit gate (precedent)? Does the file hold an interceptor (0b), and does it cover this host? Are there calls the grep cannot see — an SDK's default endpoint, an OAuth token fetch, telemetry initialisation? **Finding when** a unit or integration test reaches a host other than loopback, a container or a reserved domain. **Proof:** the offline run of the whole unit suite — `pytest --disable-socket --allow-hosts=127.0.0.1,::1`, `unshare -rn sh -c 'ip link set lo up; <cmd>'`, or `docker run --network none` — red before, green after (V69). A cluster of tests failing together offline is one root cause (Parry et al., EASE 2025).

### 5. Shared mutable state and order dependence

```
BAD:   const sent: Request[] = [];                     // module level; each test pushes, none resets
       process.env.UPLOAD_LIMIT = '10'                 // set in one file, read by the next file in the same worker
       jest.spyOn(clock, 'now').mockReturnValue(1)     // never restored; clearMocks clears calls, not implementations
       @pytest.fixture(scope="session") def cart(): return Cart()   # mutated by the tests that use it
GOOD:  beforeEach(() => { sent.length = 0 }) · vi.stubEnv + unstubEnvs: true · restoreMocks: true · monkeypatch.setenv
       function-scoped fixtures for mutable objects · a per-test transaction or a per-worker database
```
**Read the code:** Is the state mutated by more than one test, or only read? Is it reset in a hook in the same file, or by the runner config (`restoreMocks`, `unstubEnvs`, Vitest 5's default `clearMocks` — which clears records and does **not** restore implementations, [`precedents/testing.md`](../../../../snippets/precedents/testing.md) § 8)? Does the runner isolate files (Jest's per-file module registry; Vitest `isolate`), so the leak is within a file only? Is ordering declared (`describe.serial`, `@Order`, pytest-order — § 33, intended)? **Finding when** a test's outcome depends on what ran before it. **Proof:** three shuffle seeds, the victim alone vs in the suite, then the polluter bisected (`detect-test-pollution`, `rspec --seed S --bisect`, or halving the preceding tests) — the pair is the evidence (V67). With no shuffle available for the runner, the order row prints `NOT TESTED (no shuffle for <runner>)`, never "clean".

### 6. Async leaks

```
BAD:   "test:e2e": "jest --config jest.e2e.config.cjs --forceExit"   // exits over open handles; Jest 30 can also pass a floating assertion
       jest.useFakeTimers() in one test, never useRealTimers()       // the next test's timers never fire
       user.click(save);                                             // user-event v14 returns a promise; the test ends first
GOOD:  close what the suite opens (app.close(), orm.close(), redis.quit()) and drop --forceExit · afterEach(() => vi.useRealTimers())
       await user.click(save) · clearInterval in teardown · goleak.VerifyTestMain(m)
```
**Read the code:** What does `--forceExit` hide — run once with `--detectOpenHandles` and read the handles: a server, an ORM or Redis connection, a queue worker, an interval. Whether the same flag also masks a floating assertion is `suite-execution-scan` § 4's verdict (Jest 30 passes an un-awaited failing `.resolves` with exit 0 under it, [`precedents/testing.md`](../../../../snippets/precedents/testing.md) § 2). Is the floating call's effect asserted later, or does it leak into the next test? **Finding when** a handle, timer or promise outlives its test. **Proof:** `jest --detectOpenHandles`, `vitest --reporter=hanging-process`, goleak, `python -X dev -W error::ResourceWarning`; for a floating action, the [assertion flip](../../../../snippets/proof-oracles.md) inside the `waitFor` callback stays green (§ Assertion flip). A `--forceExit` with a cited upstream reason and no floating assertion in that suite is § 30 Hardening.

### 7. Parallel and platform assumptions

```
BAD:   app.listen(3000) · '/tmp/export.csv' · DATABASE_URL=…/app_test with maxWorkers: 4
       describe.concurrent sharing one mock · t.Parallel() beside os.Setenv · assert list(set(tags)) == ["a", "b"]
GOOD:  listen(0) and read the port · t.TempDir() / tmp_path / mkdtemp · a database per worker (JEST_WORKER_ID,
       VITEST_POOL_ID, PYTEST_XDIST_WORKER) · t.Setenv (refuses t.Parallel) · sorted(…) / assertCountEqual / ElementsMatch
```
**Read the code:** How many workers does the CI job use (0a), and do they share the resource? Is the order assumption on a hash structure (Python sets, Go maps, Java `HashMap`) or on an insertion-ordered one (JS objects, Sets and Maps, Python dicts — precedents)? Does a locale or path separator assumption meet another CI OS? **Finding when** two workers or two platforms can disagree. **Proof:** `pytest -n auto`, `jest --maxWorkers=100%`, `go test -p 8 -race -count=20`, the suite run twice without cleanup, `LANG=tr_TR.UTF-8`, NonDex for JVM hash order, `PYTHONHASHSEED` varied (V69).

### 8. Brittle end-to-end waits, actions and selectors

```
BAD:   await page.waitForTimeout(500) · waitForLoadState('networkidle') · click({ force: true })
       expect(await row.isVisible()).toBe(true)                // read once; races the render
       page.locator('div.css-1x2y3z > span:nth-child(2)') · locator('xpath=ancestor::form[1]')
GOOD:  await expect(page.getByRole('row', { name: 'Order 42' })).toBeVisible()   // web-first, retries until the timeout
       page.getByRole / getByLabel / getByTestId · cy.wait('@alias') · a documented force on a hidden native control
```
**Read the code:** What state is the wait standing in for? Does a web-first assertion exist for it? Is the selector the app's own stable hook (`data-testid`, a role and name) or its styling? Does `force` hide a real overlay a user would hit? eslint-plugin-playwright 2.12.0 names these (`no-wait-for-timeout`, `no-networkidle`, `no-force-option`, `prefer-web-first-assertions`, `no-raw-locators`, `no-nth-methods`); a lint hit is a candidate, not a finding. **Finding when** the test passes or fails on timing or markup rather than behaviour. **Proof:** `npx --no playwright test <file> --repeat-each=50 --workers=4 --retries=0 --fail-on-flaky-tests` with CPU throttling, k of N; for a selector, the markup mutations of V73 (class rename, sibling reorder, wrapper added); for `force`, an overlay over the target must fail the test.

## Proof — perturbation first, the bound as fallback

The oracles, commands and variants are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Testing — *Perturbation and the repeat-run bound* for every class here, *Assertion flip* for § 6's floating actions, and the class variants V67 (order and shared state), V68 (clock, zone and locale) and V69 (randomness, sleeps, leaks, network and shared resources). The shape:

1. **Record the perturbation**, not just the result: seed, `TZ`, faked instant, worker count, the order file. A flake without its reproduction line is not evidence.
2. **Deterministic first.** A zone, a date, the network off, a seed that fails — one red run before the fix and one green run after prove it, and the fix's mechanism (a frozen clock, a seeded generator, an awaited call) is the argument that the source is gone.
3. **Otherwise the bound.** N = ln(1−c)/ln(1−p): 299 runs to see a 1% flake at 95%. A clean run reports `p < 3/N at 95%`, never "stable" or "not flaky". `/flaky-test-hunt` owns the N-run loop and its table.
4. **The fix removes the source.** Never a retry, a longer sleep, a raised timeout or a skip ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Old test on new code, and the anti-cheat rule).

Write each confirmed row's evidence in the block of `proof-oracles.md` § Evidence block (testing).

## Output

```
flake-source-scan — lanes: jest 30.5 (apps/api), vitest 4.1 + playwright 1.63 (apps/web); pytest, go, jvm absent
Context: shuffle — none in any config or CI job · restore — clearMocks only (no restoreMocks) · network guard — none
         · --forceExit on the e2e job · 590 test files read the real clock and freeze nothing

Findings: 2 · Unconfirmed: 1

1. test/e2e/stock-ledger.e2e-spec.ts:512                              [report-with-fix]  high
   §1 fixture date that expires — expiryDate: '2026-12-31' on a batch the SUT rejects once expired
   (inventory.service.ts:88 compares it to new Date()). Proof: faketime '2027-01-01' → 3 tests red; with
   expiryDate = addDays(clock.now(), 90) → green. Fix: derive fixture dates from the injected clock. V68

2. test/e2e/support/today.ts:20 (used by 14 e2e files)                [report-with-fix]  medium
   §1 zone — new Date().toISOString().slice(0, 10) as "today"; the API buckets by the tenant's zone.
   Proof: TZ=Pacific/Kiritimati → 6 of 14 files red; green with localDayOf(clock.now(), tz). V68

3. test/e2e/orders-webhook.e2e-spec.ts:111                             [report-flagged]   medium
   §3 fixed sleep — setTimeout(resolve, 100) waits for the webhook consumer. Unproven link: no
   stress harness in this run. Settling probe: stress-ng --cpu 8 beside
   `npx --no jest -c jest.e2e.config.cjs <file>` × 59 (p ≈ 5% at 95%). Fix: await the consumer's row.

Verification: 41 candidates → 2 findings · 1 unconfirmed · 31 hardening · 0 pre-existing · 7 refuted

Class coverage:
  order  shuffle                       NOT TESTED (no shuffle configured for jest or vitest; run three seeds to settle)
  §1  clock, zone, calendar           checked (111 + 47 hits / 23 groups → 2 findings; wire-mapping tests: precedent)
  §2  randomness                      checked (120 hits / 4 groups → 0 findings; opaque ids) · 1 group Unconfirmed
  §3  sleeps, timing bounds           checked (101 hits → 0 findings) · Live, unreviewed (61 groups / 88 hits — continue with grep 3a on test/e2e)
  §4  real network                    checked (0 hits; no guard file — Hardening: add disableNetConnect)
  §5  shared state, order             checked (29 + 47 files + 89 hits → 0 findings; Jest isolates files)
  §6  async leaks                     checked (4 hits → 0 findings; --forceExit: 3 open DB / Redis handles, owner: suite-execution-scan § 4)
  §7  parallel, platform              checked (3 hits → 0 findings; e2e runs maxWorkers: 1)
  §8  e2e waits, selectors            checked (20 hits / 6 files → 0 findings) · 1 Unconfirmed (waitForTimeout in flows)
```

`[report-with-fix]`: the source is traced to the assertion or branch, the perturbation flipped the test, and the fix removes the source. `[report-flagged]`: one link is unproven (no harness, a source in code not read, a CI shape not confirmed) and the row names it with the settling command. The coverage block lists **all eight** classes plus the `order` line on every run: `checked (k hits → m findings)` only when the grep ran on a present lane; `N/A (<reason>)` only when the repo has no such surface (no browser e2e, no Python); `blocked (<reason>)` when a grep failed or code could not be read. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/testing.md`](../../../../snippets/precedents/testing.md) (§ 33–42 for determinism) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **Clock reads for durations, timeouts and log stamps**; wall-clock e2e against a real database with explicit margins (§ 35).
- **Sleep under virtual time**, a yield (`sleep(0)`), a bounded poll helper with a deadline, a sleep that is the behaviour under test (§ 34). A Go `time.Sleep` inside `synctest.Test` is virtual.
- **Seeded randomness and opaque ids never asserted**; property frameworks that print and persist the seed (§ 36).
- **Immutable shared fixtures** — servers, pools, containers, read-only reference data (§ 37); real network in a tagged e2e or contract suite (§ 38); declared ordering (§ 33).
- **Insertion-ordered collections.** JS objects, Sets and Maps and Python dicts iterate in insertion order; `[...new Set(x)]` is deterministic.
- **A flake the SUT causes means the test is right** (§ 42) — route the race to `/fix-bug`, never to a wait.
- **A module-scope env write in a Jest test file** — Jest gives each file its own `process.env` (§ 44); **a fixed future date in a unit test whose code reads no clock** is data, not a time bomb (§ 46).
- **Bulk triage is not a verdict.** "590 files read the clock" is an inventory. A group is dismissed only with its read or its perturbation run.

## When to run

- On any diff that adds or changes a test, a test helper, a fixture, a runner config or the CI test job — the `/review-changes` dispatch signal for test files, beside `assertion-strength-scan`.
- On every whole-suite test audit, reporting all eight classes and the `order` line.
- From `/flaky-test-hunt` Phase 4 as the sibling scan: once a flake is root-caused, this skill's grep for that class lists every other test with the same source, so the hunt's `N_found` is a list, not a guess.
- Before turning shuffle, parallel workers or a new CI zone on: the run tells which tests will break.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/testing.md`](../../../../snippets/precedents/testing.md). Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the source `<file:line>`, the test it reaches, the perturbation (or settling command) and the deterministic fix.
- Do not report a grep hit as a finding, and do not call a test "flaky" or "stable" from a run count — report `k of N` with the perturbation, or `p < 3/N`.
- Do not propose a retry, a longer sleep, a raised timeout, a skip or a quarantine as the fix. The fix removes the source.
- Do not print "no flake source found" without the class-coverage block and the `order` line; a class whose grep did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `/flaky-test-hunt` — the runtime harness: N-run sweeps, root cause, the fix and the confidence bound. Run this skill's grep for the root-cause class as its Phase 4 sibling scan; the hunt closes what this skill proves. `/test-fix` closes findings from a whole-suite audit with the same failing-first rule.
- `suite-execution-scan` (retry masking, CI masking), `assertion-strength-scan` (floating and unreached assertions), `test-double-scan` (doubles that lie), `test-factories` (fixture isolation and builders) — this pack.
- [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Testing and [`precedents/testing.md`](../../../../snippets/precedents/testing.md) — the oracles and the settled precedents.
- `rules/testing-principles.md` — no sleeps, a frozen clock, seeded randomness, no real network, state reset: the rules this skill enforces.
- The database pack's proof oracles (§ Data) own concurrency invariants a test exposes, when that pack is installed; a race on money or stock found here goes there as a production bug.
