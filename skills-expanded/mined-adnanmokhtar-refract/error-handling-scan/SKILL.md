---
name: error-handling-scan
description: Find failures the code hides — empty or log-only handlers, failures returned as empty success, unchecked statuses and error returns, floating promises, catch-alls, lost causes, state the error path never restores — each proved by fault injection.
kind: skill
pack: code-quality
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: error-handling-scan

## Premise

A failure that nobody hears about turns an incident into a mystery. A handler swallows the error, or
answers an empty list, or `200`; a promise rejects after the response was sent; an HTTP `500` is
parsed as a body; a lock taken before the failure is never released. The code works on the happy
path, every test that only walks the happy path passes, and the first real failure leaves silent
wrong state behind. This is the most common correctness class in AI-written code, and it is a
**correctness** class, not style: fixing it **changes observable behaviour** on purpose.

This skill is the executor behind `concerns/error-handling.md` (C4) and the single owner of the
swallowed-error, unhandled-I/O and unobserved-async classes. Align's `silent-catch` and
`unhandled-io` detectors and `/audit`'s Unhandled-I/O pass describe the same classes; they dispatch
here.

**Every finding cites the handler or call `<file:line>` + the failure it hides (named: which
dependency, which error) + the entry point that reaches it + what the caller sees instead + the
fault-injection proof (or the test that would settle it) + the fix in the project's own error
primitive.** A grep hit is never a finding by itself, and "no swallowed errors" is never printed
without the class-coverage block (§ Output).

**Detect statically, prove by injection.** The proof is a **port fault injection**: make the
dependency throw, reject, time out or answer an error status, and assert the caller-visible outcome
([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Code quality). A candidate read in
code with no harness is **Unconfirmed**, carrying the settling test; it is never dropped, and never
promoted on reading alone ([`refute-before-report.md`](../../../../snippets/refute-before-report.md)
§ 2, gate 6).

## The rule

A handler, call or task is a finding when all four hold:

1. **A failure can happen there.** The dependency can throw, reject, time out, answer 4xx / 5xx,
   return an error value or a partial result — named, not assumed. A pure parse of a constant cannot.
2. **The caller cannot tell.** Nothing above the site propagates, retries, compensates, or degrades
   **visibly**: no rethrow, no typed error, no error status, no error state rendered, no log with
   context **and** no metric. A global filter or error boundary the failure reaches counts as
   handling (`precedents/code-quality.md § 24`).
3. **A real entry point reaches it** — a route, consumer, job, CLI, or a UI event — not a probe
   script, seed or test.
4. **No precedent applies** with its "must be true" clause shown (§ False positives).

## Boundaries

- Outbound timeouts, retries, backoff and circuit breakers → distributed-systems `@resilience-reviewer`, when that pack is installed. Without it, a missing timeout is reported here only when it hangs a handler this skill already flags, tagged `resilience-class (owner pack not installed)`.
- A connection, cursor or query runner not released → database `connection-config-scan` § 9; a multi-write use case with no transaction (partial write) → database `transaction-scan` § 2. Both when the database pack is installed; without it, §7 reports them tagged `data-class (owner pack not installed)`.
- A handle whose cost is exhaustion under load (unconsumed response body, a `.pipe()` chain left open, sockets) → `memory-growth-scan` § 5, when the performance pack is installed. §7 here keeps the paired state whose skip **changes behaviour**: a lock never released, a busy flag stuck true, a written file's close error lost.
- Secrets or PII in an error message or log → security `data-exposure-scan`; a fail-open authorization (a permission check that returns allow, or skips, on failure) → security `@security-auditor`. Both when the security pack is installed.
- A degrade path that leaves no signal at warn or above, and an error logged without its stack or type → observability `log-signal-scan` §1 (LG-01) and §2 (LG-02); level misuse and log shape → its §3–§4; missing metrics → `metric-hygiene-scan`. All when the observability pack is installed; without it such a line is listed tagged `observability-class (owner pack not installed)`, never graded here. A log line that **replaces** propagation is §1 here: the caller acts on a failure as success, whatever the log says.
- Suppressed lint diagnostics → `suppression-scan` (this pack). Error-handling rules switched off in a linter config are listed in grep 0b as context.
- Runtime error clusters from telemetry → `@error-detective`, which reads logs, not source.

## Adapt to the codebase — the analyzer lanes

Read each analyzer's installed version and rule set from the lockfile and its config before
trusting a quiet run. A rule that is configured at **error** in CI owns its class: its hits are the
tool's, and the grep below is the fallback for the code it cannot see
(`precedents/code-quality.md § 2`). Print the lanes you ran in the output header.

| Lane | §1–§3 swallow, success-shaped value, ignored result | §4 async | §5–§6 catch-all, cause, finally | §7 paired state | Runtime hook (proof) |
|---|---|---|---|---|---|
| **TS / JS** — ESLint 10.12, typescript-eslint 8.71 | core `no-empty` (catch blocks), `no-useless-catch` | **type-aware only** (`projectService`): `@typescript-eslint/no-floating-promises`, `no-misused-promises`, `await-thenable`, `return-await`; core `no-async-promise-executor` | core `preserve-caught-error` (ESLint ≥ 9.35), `no-unsafe-finally`; `@typescript-eslint/only-throw-error` | no rule — greps 7a, 7b | `--unhandled-rejections=strict`; Jest `--detectOpenHandles` |
| **Python** — Ruff 0.16.10, pyright 1.1.414 | `S110`, `S112`, `E722`, `PLW0133`, `PLW1510` (`subprocess.run` without `check`) | `RUF006`, `ASYNC1xx`; pyright `reportUnusedCoroutine` | `BLE001`, `B904`, `B012`, `TRY201`, `TRY203`, `TRY400` | `SIM115` | `-W error::RuntimeWarning`, `-X dev -W error::ResourceWarning` |
| **Go** — golangci-lint v2.14 | `errcheck`, `nilerr`; gosec `G104` | govet `lostcancel`; `errgroup` by reading | `errorlint`; govet `errorsas` | `bodyclose`; staticcheck `SA9001` (defer in a loop) | `go test -race`, goleak |
| **JVM** — Error Prone 2.50, SpotBugs 4.10, detekt 1.23 | EP `EmptyCatch`, `CatchAndPrintStackTrace`, `UnusedException`; SpotBugs `DE_MIGHT_IGNORE`, `RV_RETURN_VALUE_IGNORED*`; detekt `SwallowedException` | EP `FutureReturnValueIgnored`; detekt `GlobalCoroutineUsage` | EP `InterruptedExceptionSwallowed`, `Finally`; detekt `TooGenericExceptionCaught`, `ReturnFromFinally` | EP `StreamResourceLeak`, `LockNotBeforeTry`; SpotBugs `UL_UNRELEASED_LOCK_EXCEPTION_PATH` | an interrupted-thread test |
| **C#** — Roslyn, VS Threading 18.7 | CA1031, CA1806 | CS4014, VSTHRD100, VSTHRD110, CA2012 | CA2200 (`throw ex;`) | CA2000 | `TaskScheduler.UnobservedTaskException` |
| **Ruby** — RuboCop 1.91 | `Lint/SuppressedException`, `Lint/UselessRescue` | — | `Lint/RescueException`, `Style/RescueStandardError`, `Lint/EnsureReturn` | block forms, by reading | — |
| **PHP** — PHPStan 2.2 | `catch.neverThrown`; greps | — | grep 6a (`getMessage()` only) | — | — |
| **Rust** — clippy | `let_underscore_must_use`, `unused_result_ok`, `map_err_ignore` | `let_underscore_future` | — | `await_holding_lock` | — |

Lane commands (research catalog, 2026-10-05; installed tools only — an absent one prints `NOT-RUN (<tool> not installed — to enable: <install command>)` and its grep runs): `ruff check --select S110,S112,E722,BLE001,B904,B012,TRY,RUF006,ASYNC,PLW0133,PLW1510,SIM115 --output-format json .` ·
`golangci-lint run --new-from-merge-base=origin/main ./...` with those linters enabled ·
`npx --no pyright --outputjson` · `./gradlew compileJava` (Error Prone runs inside the compiler) or `spotbugsMain` · `dotnet build -warnaserror` (C# / .NET).
For TypeScript, typescript-eslint's plain `recommended` has **no** type-aware rule
(`precedents/code-quality.md § 76`); when the project is not type-aware, run a scratch flat config
beside `eslint.config.*` that spreads the project's exported array and adds
`languageOptions: { parserOptions: { projectService: true } }` plus the four async rules at
`error`, run `npx --no eslint -c <scratch> --format json <roots>`, keep those `ruleId`s, delete the
scratch file and check `git status --porcelain`. An error from that run is `blocked`, never a quiet
lane.

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep
**N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`.`): `rg` given no path
reads stdin whenever stdin is a pipe, and under an agent's shell that is a silent zero-hit run. Lane
absence comes from the lane count the block prints first, never from a quiet grep. Any `rg` error on
stderr (exit 2) is a failed grep, never zero hits. Multi-line greps print the line where the
handler, call or chain **starts**: read down from it.

```bash
# Not production code: vendored, built, tests, specs, mocks, fixtures, stories, migrations, seeds, generated, catalogs, docs, ai/.
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/*.min.*'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,stories,migrations,migrate,seeds,generated,__generated__,locales,i18n}/**'
   -g '!**/*.{spec,test,e2e-spec,mock,stories,test-data,fixture,fixtures}.*' -g '!**/{*_test,*_spec,test_*,conftest}.*' -g '!*.{md,mdx,json,lock,snap,map,svg,yml,yaml,sql,html}' -g '!docs/**' -g '!ai/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')   # drops comment-only lines
Z='(?:\[\]|null|undefined|nil|None|false|False|0|\{\s*\}|""|\x27\x27)'  # a neutral "success" value
for t in js ts py go java kotlin cs ruby php rust; do printf '%-7s %s\n' "$t" "$(rg --files -t "$t" "${X[@]}" . | wc -l)"; done   # 0 = lane absent

# 0. Context: 0a the error primitives every verdict reads (global filter, boundary, process hooks, error tracker);
#    0b the analyzer rules already configured (a configured rule owns its class: its hits are the tool's, not this grep's).
rg -n --pcre2 '@Catch\(|implements\s+ExceptionFilter|\bsetErrorHandler\(|process\.on\(\s*["\x27](?:unhandledRejection|uncaughtException)|\bErrorBoundary\b|componentDidCatch|@(?:ControllerAdvice|RestControllerAdvice|ExceptionHandler)\b|\brescue_from\b|set_exception_handler\(|\bexception_handler\(|add_exception_handler\(|\bSentry\.init\(|\bsys\.excepthook\b|app\.use\(\s*\(\s*err\b' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 'no-floating-promises|no-misused-promises|(?:recommended|strict)TypeChecked|projectService|\bno-empty\b|preserve-caught-error|only-throw-error|\b(?:errcheck|errorlint|bodyclose|nilerr|wrapcheck)\b|\b(?:BLE001|S110|S112|E722|B904|RUF006|SIM115)\b|\bTRY\d{3}\b|EmptyCatch|CatchAndPrintStackTrace|\bCA(?:1031|2000|2200)\b|VSTHRD1\d\d|SuppressedException|unhandled-rejections' -g '{eslint.config.*,.eslintrc*,package.json,pyproject.toml,setup.cfg,ruff.toml,.ruff.toml,.golangci.*,*.csproj,Directory.Build.props,.editorconfig,.rubocop.yml,build.gradle*,pom.xml,phpstan.neon*,Cargo.toml,clippy.toml}' -g '!**/node_modules/**' .

# 1. A handler that drops the error: 1a empty or comment-only (every stack); 1b a body that never reads the caught
#    value (brace stacks, Go `if err != nil`, Python `except … as e`) or a binding-less `catch {` with no throw.
rg -n -U --pcre2 '\bcatch\s*(?:\([^()\n]*\))?\s*\{(?=\s*(?:(?://[^\n]*|/\*(?:[^*]|\*(?!/))*\*/)\s*)*\})|^[ \t]*except\b[^\n:]*:(?=[ \t]*(?:(?:#[^\n]*)?\n(?:[ \t]*(?:#[^\n]*)?\n)*[ \t]*)?(?:pass|\.\.\.|continue)\b)|^[ \t]*rescue\b[^\n]*(?=\n[ \t]*end\b)|\brescue\s+nil\b|\bif\s+err\s*!=\s*nil\s*\{(?=\s*\})|\.catch\(\s*(?:(?:\(\s*\w*\s*\)|\w+)\s*=>\s*(?:\{\s*\}|undefined|null|void\s+0)|noop|_\.noop)\s*\)' "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '\bcatch\s*\(\s*(?:[\w.\\|]+\s+)?\$?(\w+)(?:\s*:\s*[\w.]+)?\s*\)\s*\{(?=(?:(?://[^\n]*|/\*(?:[^*]|\*(?!/))*\*/)|\s)*[^\s}/])(?=(?:(?!\b\1\b)[^{}])*\})|\bcatch\s*\{(?=(?:(?!\bthrow\b)[^{}])+\})|\bif\s+err\s*!=\s*nil\s*\{(?=(?:(?!\berr\b)[^{}])+\})|^([ \t]*)except\b[^\n]*\bas\s+(\w+)\s*:(?=[ \t]*(?:#[^\n]*)?\n(?>(?:\2[ \t]+(?![^\n]*\b\3\b)[^\n]*|[ \t]*)\n)+(?!\2[ \t]+\S))' "${X[@]}" . | "${NC[@]}"

# 2. A failure turned into a success-shaped value: 2a a handler that returns or sets an empty / neutral value or answers 2xx;
#    2b a Go error branch that returns nil.
rg -n -U --pcre2 '\bcatch\s*(?:\([^()\n]*\))?\s*\{(?=(?:[^{}]|\{[^{}]*\})*?(?:\breturn\s+(?:'"$Z"'|Optional\.empty\(\)|Collections\.empty\w*\(\)|List\.of\(\))\s*;?\s*\}|\.status\(\s*2\d\d\s*\)|\b(?:ok|success)\s*:\s*true\b))|\.catch\(\s*(?:\(\s*\w*\s*\)|\w+)\s*=>\s*(?:\(?\s*'"$Z"'\s*\)?|set\w+\(\s*'"$Z"'\s*\)|\{(?=[^{}]{0,200}?\b(?:return\s+'"$Z"'|set\w+\(\s*'"$Z"'\s*\))))|^([ \t]*)except\b[^\n]*:(?=[ \t]*(?:#[^\n]*)?\n(?:\1[ \t]+[^\n]*\n){0,4}?\1[ \t]+return\s+(?:None|False|0|\[\]|\{\}|""|\x27\x27|set\(\))[ \t]*$)' "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '\bif\s+err\s*!=\s*nil\s*\{(?=\s*(?://[^\n]*\s*)*return\s+(?:nil|false|0|""|(?:nil|false|0|""|\w+\{\}),\s*nil)\s*\})' -t go "${X[@]}" . | "${NC[@]}"

# 3. A failure signal never read: 3a Go errors assigned to `_`; 3b Rust `let _ =` / `.ok();`; 3c an HTTP response body
#    parsed with no status check in between (fetch / requests / httpx / net/http); 3d subprocess without check=; 3e a
#    Node-style callback whose err is never read.
rg -n --pcre2 '^\s*_\s*(?:,\s*_\s*)?=\s*[\w.]+\(' -t go "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '^\s*let\s+_\s*=\s*[^;]*\(|\.ok\(\)\s*;' -t rust "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '(?:(?<![\w.$])fetch|\b(?:requests|httpx)\.(?:get|post|put|patch|delete|request)|\bhttp\.(?:Get|Post|PostForm|Head)|\.Do)\((?=(?:(?!\.ok\b|\.status(?:Code|_code)?\b|\bStatusCode\b|raise_for_status|throwHttpErrors|validateStatus|\n\}|\n[ \t]*\n[ \t]*(?:export\s+)?(?:async\s+)?(?:function|def|func)\b)[\s\S])*?(?:\.(?:json|text|blob|arrayBuffer)\(\)|io\.ReadAll\(\s*\w+\.Body|json\.NewDecoder\(\s*\w+\.Body))' "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '\bsubprocess\.(?:run|call)\((?=(?:(?!\bcheck\s*=)[^()]|\([^()]*\))*\))|\bos\.system\(' -t py "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '(?:\bfunction\s*\w*\s*)?\(\s*(err|error)\s*(?::\s*[\w.|<> ]+)?\s*,\s*[^()]*\)\s*(?:=>)?\s*\{(?=(?:(?!\b\1\b)[^{}])*\})' -t js -t ts "${X[@]}" . | "${NC[@]}"

# 4. An async failure nobody observes: 4a async callbacks handed to APIs that drop the promise, dangling tasks, async void;
#    4b `.map(async` not collected by Promise.all / await / return; 4c a `.then(` chain started as a statement with no `.catch(`;
#    4d a promise discarded with `void` inside a function (`void` also silences no-floating-promises: its ignoreVoid default).
rg -n --pcre2 '\.(?:forEach|forEachRight)\(\s*async\b|\bnew\s+Promise\(\s*async\b|\b(?:setTimeout|setInterval|setImmediate|queueMicrotask)\(\s*async\b|^\s*asyncio\.(?:create_task|ensure_future)\(|^\s*(?:self\.)?\w*loop\.create_task\(|\basync\s+void\s+\w+\s*\((?![^)]*EventArgs)|\bGlobalScope\.(?:launch|async)\b' "${X[@]}" . | "${NC[@]}"
#    4a′ an async listener registered as a STATEMENT. A `.once('key', async () => …)` that an arrow returns (`=> ctx.once(…)`) is a memoiser whose promise the caller awaits — not a listener (§ 88).
rg -n -U --pcre2 '(?<!=>\n)^[ \t]*(?:[\w$]+(?:\.[\w$]+)*)?\.(?:on|once|addListener|addEventListener)\(\s*["\x27][\w:.-]+["\x27]\s*,\s*async\b' "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '(?:(?<=[;{}]\n)|\A)[ \t]*(?!(?:return|await|yield|const|let|var|this\.\w+\s*=)\b)(?![^\n]*\bPromise\.\w+\()[^\n]*?\.(?:map|flatMap)\(\s*async\b' -t js -t ts "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '(?:(?<=[;{}]\n)|\A)([ \t]*)(?!(?:return|await|yield|const|let|var|export|void|throw)\b)(?![\w$.]+\(\s*(?:async\s+)?(?:\([^()]*\)|\w+)\s*=>)(?:this\.)?[\w$]+(?:\.[\w$]+)*\((?=(?:(?!\.catch\(|;[ \t]*$|\{[ \t]*$)[\s\S]){0,300}?\.then\((?:(?!\.catch\()[\s\S]){0,300}?;[ \t]*$)' -t js -t ts "${X[@]}" . | "${NC[@]}"
#    Not 4d (§ 89): a framework reply (`void reply.status(…).send(…)` — Fastify's own dispatch handles a rejection), a TanStack
#    cache call (`invalidateQueries`, `refetch`, `prefetchQuery`, …: errors land in the query cache), a confirm dialog helper.
rg -n --pcre2 '^[ \t]+void\s+(?!(?:this\.)?(?:reply|res|response)\.(?:status|code|send|header|headers|type|redirect|hijack)\b)(?![\w$.]*\.(?:invalidateQueries|refetch\w*|prefetch\w*|cancelQueries|resetQueries|ensureQueryData)\()(?!(?:ask)?[Cc]onfirm\w*\()(?:this\.)?[\w$]+(?:\.[\w$]+)*\((?![^\n]*\.catch\()' -t js -t ts "${X[@]}" . | "${NC[@]}"

# 5. Catch-everything: bare except / BaseException / Exception, suppress(Exception), catch Throwable / Exception /
#    RuntimeException, C# catch (Exception), rescue Exception / bare rescue, PHP catch (\Throwable).
rg -n --pcre2 '^\s*except\s*:|^\s*except\s+\(?\s*(?:BaseException|Exception)\b|\bsuppress\(\s*(?:BaseException|Exception)\b|\bcatch\s*\(\s*(?:final\s+)?(?:java\.lang\.)?(?:Throwable|Exception|RuntimeException|Error)\s+\w+\s*\)|\bcatch\s*\(\s*\w+\s*:\s*(?:Throwable|Exception)\s*\)|\bcatch\s*\(\s*(?:System\.)?Exception(?:\s+\w+)?\s*\)|\brescue\s+(?:Exception|StandardError)\b|^\s*rescue\s*(?:=>\s*\w+)?\s*$|\bcatch\s*\(\s*\\?(?:Throwable|Exception)\s+\$\w+\s*\)' "${X[@]}" . | "${NC[@]}"

# 6. The cause or the outcome rewritten: 6a a new error thrown inside a catch without the caught one as cause;
#    6b Python raise inside except without `from`; 6c errors compared by text, Go %v; 6d return/throw in finally,
#    InterruptedException swallowed.
rg -n -U --pcre2 '\bcatch\s*\(\s*(?:[\w.\\|]+\s+)?\$?(\w+)(?:\s*:\s*[\w.]+)?\s*\)\s*\{(?:[^{}]|\{[^{}]*\})*?\K\bthrow\s+new\s+\w++(?=\()(?=(?:(?!\bcause\b|[(,]\s*\$?\1\s*[,)])[^;])*\)\s*;)' "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '^([ \t]*)except\b[^\n]*:[ \t]*\n(?:\1[ \t]+[^\n]*\n|[ \t]*\n)*?\1[ \t]+\Kraise\s+\w+(?:\.\w+)*\((?![^\n]*\bfrom\b)[^\n]*$' -t py "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 'Errorf\([^)]*%v[^)]*\berr\b|\berr\.Error\(\)\s*[!=]=|strings\.Contains\(\s*err\.Error\(\)|\b(?:e|err|error|ex|exc)\.message\s*(?:[!=]==?|\.(?:includes|startsWith|endsWith|match)\()|\bstr\((?:e|err|exc|ex)\)\s*(?:==|!=|\bin\b)|\bgetMessage\(\)\.(?:equals|contains|startsWith)\(' "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '\bfinally\s*\{(?:[^{}]|\{[^{}]*\})*?\K\b(?:return|throw)\b|^([ \t]*)finally\s*:[ \t]*\n(?:\1[ \t]+[^\n]*\n)*?\1[ \t]+\K(?:return|break|continue)\b|\bcatch\s*\(\s*(?:final\s+)?InterruptedException\s+\w+\s*\)\s*\{(?=(?:(?!\binterrupt\(\)|\bthrow\b)[^{}])*\})' "${X[@]}" . | "${NC[@]}"

# 7. Paired state the error path skips: 7a a lock / semaphore taken with no defer or finally visible, a file opened for
#    writing outside with / try-with-resources / using; 7b a busy flag set true in a file with no `finally`.
rg -n -U --pcre2 '^[ \t]*[\w.]+\.R?Lock\(\)(?=[ \t]*\n(?![ \t]*defer\b))|^(?![ \t]*(?:async\s+)?with\b)[^#\n]*(?<![\w.])open\([^)\n]*["\x27][wax]b?\+?["\x27]|^(?![ \t]*(?:try\s*\(|using\b))[^\n]*=\s*new\s+(?:FileOutputStream|FileWriter|BufferedWriter|PrintWriter|OutputStreamWriter|RandomAccessFile|FileStream|StreamWriter)\(|^[ \t]*[\w.]+\.(?:lock|acquire)\(\)\s*;?[ \t]*$|^\s*(?:const|let|var)\s+\w+\s*=\s*await\s+[\w.]+\.(?:acquire|lock)\(' -g '!*.{sh,bash}' "${X[@]}" . | "${NC[@]}"
B='\bset(?:Is)?(?:Loading|Submitting|Saving|Pending|Busy|Processing|Fetching)\(\s*true\s*\)|\b(?:this\.)?(?:is)?(?:loading|submitting|saving|pending|busy|processing|inFlight)\s*=\s*true\b'
rg -l0 --pcre2 "$B" "${X[@]}" . | xargs -0 -r rg -l0 --files-without-match --pcre2 '\bfinally\b' | xargs -0 -r rg -H -n --pcre2 "$B"
```

A finding is a grep hit **plus** a read of the handler and the code it guards **plus** the hops to
an entry point and up to whoever handles the failure. Three blind spots are structural:

- **A floating promise has no syntax.** `emailReceipt(id)` with no `await` looks like any other
  call; only the type checker knows it returns a promise. Greps 4a–4c find the syntactic shapes;
  the type-aware lane (`no-floating-promises`) is the detector for the rest. Without that lane,
  read every call in a changed `async` function whose callee is declared `async`, and print
  `§4 partial (no type-aware lane)`.
- **Brace-nesting depth.** 1b, 2a and 6a read one or two levels of nested braces. A handler whose
  body nests deeper is matched on its first lines only; read the whole handler.
- **The handler can sit in a wrapper.** A shared `safe(fn)` / `tryOr(fn, fallback)` / `useQuery`
  `onError` helper that returns a neutral value is one finding with N call sites. Grep the helper's
  name once you see it, and treat its callers as one group.

**Measured** (2026-10-05). Fixtures: on `node-api`, 1a/1b land on its seeded swallow and 3c on
its seeded unchecked I/O, each on the exact line; on `web-dashboard`, 2a lands on its seeded
swallow and 3c/4c on the start of the seeded chain, two lines above the anchor; on
`review-decoys`, 1b lands on its seeded dropped error, 3c/4c on a data hook, and 7b on a pending
flag left `true` when the `fetch` rejects (not in the answer key; a real §7 candidate). Its seeded
unawaited side-effect call is found by **no** grep — only the type-aware lane sees it. Decoys stay
Hardening on read: an error body parsed tolerantly (§ 15), a URL parse-or-default (§ 16), and a
rejection handled by `then`'s second argument (§ 22). On a real
NestJS-on-Fastify + MikroORM + React monorepo (about 14,200 tracked files; the script runs in about
2 s): 0a 14, 0b 3 (`preserve-caught-error` at error; `recommended`, not type-checked, so no async
rule configured); 1a 349, of which 289 sit in probe and audit scripts and the 60 in shipped code are
46 commented handlers with a stated reason and 14 `.catch(() => undefined | null)`; 1b 176 (137
shipped); 2a 496 (131 shipped: 116 try/catch, 15 promise); 3c 21 (all in probe scripts); 4a 11 (3
shipped: async `ctx.once` listeners); 4b 0; 4c 3 — the first draft printed 147 (method declarations
and `lazy(() => import().then())` arguments) until the statement-start anchor; 5 0 (no Python, JVM
or C#); 6a 7; 6c 13 (domain codes matched with `e.message === 'CODE'`); 7a 0; 7b 0. Grep 4d was added
after `quality-mix` measured its reach (`void this.ledger.post(…)` reached by no grep): on the seven
fixtures it printed 2 — that line and a `void reply.send(…)` — and prints 1 since the § 89
exclusions; top-level `void main()` is excluded by the indent anchor, a `.catch(` on the line by
the lookahead. **Re-measured 2026-10-15** on the same monorepo (history re-rooted, about 11,800
files; about 3 s): 0a 13 (no `process.on('unhandledRejection')` in the API), 0b 3 (still no
type-aware rule: together, the production-bar gap `/quality-audit` prints); 1a 55; 1b 119; 2a 180
(one dropped audit write in a protocol handler was the run's only Finding); 3c 1; 4a 5 → 0 and 4a′ 2
(the three `ctx.once('key', async …)` memoisers, § 88, no longer match); 4c 4; 4d 364 → 136 (Fastify
replies, TanStack cache calls and confirm dialogs dropped; what is left is UI handlers such as
`void vm.submit()`, read with the mutation's `onError`); 5 1; 6a 7 → 6 (a cause passed as the first
constructor argument, `new XError(error)`, was matched because the lookahead started after the
consumed `(`); 6c 5; 7a 0; 7b 2.

## The 3,000-hit path

A repo with many handlers returns hundreds of lines (2a alone: 496 above). Triage in this order and
record every step in the coverage block:

1. **Path class.** Dismiss a whole directory with **one** cited read: `scripts/`, probe and audit
   folders close as "not reachable from production" only after
   `rg -n -g 'Dockerfile*' -g '*.{yml,yaml,toml}' -g 'package.json' -g 'Procfile' -g '!**/node_modules/**' '<dir>/' .`
   shows no image, deployed job or route runs them. 289 of 349 lines above closed this way.
2. **Group.** One group = (enclosing function or shared helper, handler shape, fallback value):
   `rg --json … | jq -r 'select(.type=="match") | "\(.data.path.text):\(.data.line_number)"'`, then
   bucket. A parse-or-default helper used in 40 places is one group.
3. **Rank by what the caller decides.** Writes, money, authorization, webhooks and acknowledgements
   first (a webhook answered `200` after a failed write is redelivered never); then reads shown to
   users as "none"; then display-only and telemetry. Use the context map (0a) to drop handlers whose
   failure reaches a global filter.
4. **Read the top 30 groups fully**, with the read-the-code questions of their §.
5. **Prefer the runtime bulk oracle.** Run the existing suite once with the unhandled-failure hook on
   (`NODE_OPTIONS=--unhandled-rejections=strict`, `pytest -W error::RuntimeWarning`), and run the
   type-aware lane over the roots. Every hook failure and every lane hit is a candidate with its
   location already proven.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues
   them. Never `checked`.

## Scans for

Severity assumes a production entry point. Raise one step when money, persisted data or a public
contract is the sink; drop one for admin-only or internal tooling paths. Critical needs a write the
caller is told succeeded, on a money or persisted-data path. CWE ids are MITRE's, cited under the
CWE Terms of Use; ids MITRE marks Prohibited or Discouraged for mapping (391, 703, 755) are not used.

| § | Class | CWE | Default |
|---|---|---|---|
| 1 | The error is dropped: empty, comment-only or log-only handler; a handler that never reads what it caught | CWE-1069, CWE-390 | high when it guards a write, a transfer or an acknowledgement; medium on a read; low on telemetry |
| 2 | Failure turned into a success-shaped value (`[]`, `null`, `false`, `{}`, a 2xx, `ok: true`) | CWE-392, CWE-393 | high when the caller decides a write, money or what a user is told on it; medium otherwise |
| 3 | A failure signal never read: error return discarded, HTTP status unchecked, exit code ignored | CWE-252 | high on a write or a payment call; medium on a read |
| 4 | An async failure nobody observes: floating promise, `forEach(async`, a dangling task, `async void` | CWE-248, CWE-252 | critical when the dropped work is a money or persisted write the response reports as done; high on a server; medium in UI |
| 5 | Catch-everything around business logic | CWE-396 | medium; high when it swallows an interrupt or cancellation, or turns a programmer error into a domain outcome |
| 6 | The cause or the outcome rewritten: cause lost, error matched by text, `return` in `finally`, interrupt swallowed, wrong status | CWE-584, CWE-393 | medium; high for a `finally` that replaces a failure, a swallowed interrupt, or a validation error answered as 500 |
| 7 | Paired state the error path skips: lock, busy flag, counter, written file's close error | CWE-460, CWE-772 | high for a lock (a hang) or a lost close error on a write; medium for a stuck flag |

### 1. The error is dropped

```
BAD:   } catch (err) { /* provider retries anyway */ }            res.status(200)…  // the write failed; ack says ok
       } catch (e) { return res.status(500).end(); }              // status right, the error itself thrown away: no log, no cause
       except Exception: pass · if err != nil { } · rescue nil · .catch(() => {})
GOOD:  } catch (err) { logger.error({ err, orderId }, 'webhook.apply_failed'); return res.status(503).end(); }   // provider redelivers
       } catch (e) { throw new RefundFailed('refund failed', { cause: e }); }   // the global filter logs and maps it
```
**Read the code** — list the errors this handler can hide (the question Anthropic's
`silent-failure-hunter` asks of every catch): which calls in the `try` can fail, and with what (a
network error, a constraint violation, a `TypeError` from a bug)? Does the caller learn of each one
— rethrow, typed error, status, error state, retry? Is anything half-written when it fires? Is there
a comment, and is its reason true in the code (§ 18)? Is the handler the outermost worker loop
(§ 19) or a best-effort cleanup (§ 17)? **Finding when** a nameable failure reaches the handler and
leaves no trace the caller or an operator can act on. **Proof:** port fault injection: make the
named dependency fail and assert the documented outcome; before the fix the response is success or
silence.

### 2. Failure turned into a success-shaped value

```
BAD:   .catch(() => { if (!cancelled) setData([]); })            // "no orders" when the API is down
       } catch { return []; }   ·   except ProviderError: return None   ·   if err != nil { return nil }
GOOD:  .catch((e) => { if (!cancelled) setError(e); })           // the component renders its error state
       return { ok: false, error: e } · raise · return nil, fmt.Errorf("list charges: %w", err)
```
**Read the code:** Who consumes the value, and what do they decide with it — a write, a charge, an
authorization, or the words "no charges" shown to a user? Can the consumer tell "failed" from
"empty"? Is the degrade declared — logged with context or counted, and documented as the behaviour
(§ 14)? Is this a tolerant parse of an error body (§ 15) or a parse-or-default whose default is the
spec (§ 16)? A permission or feature check that returns `true` on failure is fail-open: route it to
security. **Finding when** a consumer acts on the success-shaped value as if the operation
succeeded. **Proof:** port fault injection with the consumer asserted: the error state renders, the
caller receives a typed failure, nothing is written.

### 3. A failure signal never read

```
BAD:   const res = await fetch(url, opts); const body = await res.json();      // a 500 with a JSON body is "success"
       _ = os.Remove(tmp) on a written file · let _ = tx.send(msg); · subprocess.run(["git", "push"])
GOOD:  if (!res.ok) throw new HttpError(res.status, await res.text()); const body = await res.json();
       if err := f.Close(); err != nil { return err } · subprocess.run([...], check=True)
```
`fetch` resolves on 4xx and 5xx; `requests` and `httpx` return the response without raising unless
`raise_for_status()` is called; `net/http` returns a nil error for a `500`. Grep 3c finds a body read
with no status check in between. **Read the code:** Is the status checked in a shared client the
call goes through (then it is not a finding)? Does the code act on the body — a write, a state
change, a value shown as fact? For a discarded error (3a, 3b, 3e): is the operation a write whose
failure loses data, or a best-effort cleanup (§ 17)? **Finding when** an error status or an error
return is treated as success on a path that acts on it. **Proof:** a local stub answers `500` with a
plausible JSON body (or the fake returns the error); before the fix the code proceeds.

### 4. An async failure nobody observes

```
BAD:   emailReceipt(order.id, payment.id);                        // not awaited, not caught: a crash on Node ≥ 15
       items.forEach(async (i) => { await ledger.post(i); });     // the response is sent before any post finishes
       asyncio.create_task(send_receipt(order))                   # no reference kept: the task can be collected mid-run
GOOD:  await emailReceipt(…) · void emailReceipt(…).catch((e) => logger.warn({ e }, 'notify.failed'))
       await Promise.all(items.map((i) => ledger.post(i))) · tasks.add(t); t.add_done_callback(tasks.discard)
```
**Read the code:** Who awaits this work, and who sees its error? Does the response, the job's
acknowledgement or the UI claim it finished? What does the runtime do with the rejection: Node ≥ 15
exits (measured on 23.8.0) unless grep 0a shows an `unhandledRejection` handler, which turns the
crash into a silent loss (`precedents/code-quality.md § 72`)? Is it deliberate fire-and-forget with
a `.catch` (§ 20) or collected by `Promise.all` (§ 22)? For a `.then` chain (4c): is the rejection
handled by `then`'s second argument? **Finding when** a rejection can occur and nothing observes it,
or the caller reports completion before the work is done. **Proof:** the unhandled-failure hook
plus a deferred dependency — the caller must not report completion before resolution, and a
rejection must reach it.

### 5. Catch-everything around business logic

```
BAD:   try: charge(order) except Exception: log.warning("charge failed")    # also catches KeyError from a bug
       catch (Throwable t) { … } · catch (Exception) { } · rescue Exception => e · except: (catches KeyboardInterrupt)
GOOD:  except (ProviderTimeout, ProviderDeclined) as e: … · catch (IOException e) · rescue Net::ReadTimeout
       a catch-all only at the outermost boundary, which logs, counts and exits non-zero or nacks (§ 19)
```
JavaScript has no typed catch, so every JS `catch` is a catch-all; the question there is whether
programmer errors (`TypeError`, `ReferenceError`) and cancellation leave it (§ 25). **Read the
code:** Is the handler at the outermost boundary or around one business step? Does it rethrow what
it does not recognise? Does a bare `except:` or `except BaseException` swallow `KeyboardInterrupt`,
`SystemExit` or `asyncio.CancelledError`, or a Kotlin `catch (e: Exception)` a
`CancellationException`? **Finding when** a programmer error or a cancellation is converted into a
domain outcome or a silent continue. **Proof:** inject a `TypeError` (or `KeyError`, NPE) and a
cancellation into the guarded block; before the fix both are absorbed.

### 6. The cause or the outcome rewritten

```
BAD:   catch (e) { throw new BillingError('charge failed'); }      // the provider's error and stack are gone
       except ProviderError: raise BillingError("failed")          # no `from e`
       fmt.Errorf("ingest: %v", err)   // callers use errors.Is(err, ErrDuplicate): never matches
       finally { return cached; }      // replaces the throw · catch (InterruptedException e) { }   // flag lost
       if (e.message === 'DUPLICATE_CODE')                         // a reworded message breaks the branch
GOOD:  throw new BillingError('charge failed', { cause: e }) · raise BillingError("failed") from e
       fmt.Errorf("ingest: %w", err) · Thread.currentThread().interrupt(); throw … · a typed error class or code
```
**Read the code:** Does any caller, filter or operator need the original — `errors.Is`, a retry
decision on the cause, the stack in the tracker? Is this a translation at a layer boundary that logs
the original with a correlation id (§ 23)? Does a `finally` return or throw over an earlier failure?
Does the status match the documented contract (validation 400 / 422, not 500)? When
`preserve-caught-error` or Ruff `B904` runs at error level in CI (grep 0b), the cause-lost hits are
the tool's (§ 2). **Finding when** a caller's decision, a retry or a diagnosis depends on what was
lost. **Proof:** the cause-chain assertion (`err.cause`, `__cause__`, `errors.Is`, `hasCause`), the
interrupt test, or the status table.

### 7. Paired state the error path skips

```
BAD:   setPending(true); const res = await fetch(…); …; setPending(false);   // a rejected fetch leaves the button disabled
       const release = await mutex.acquire(); await work(); release();      // a throw in work() keeps the lock forever
       mu.Lock(); doWork(); mu.Unlock() · f = open(path, "w"); f.write(data)   # close error and fd lost on a throw
GOOD:  try { … } finally { setPending(false); } · await mutex.runExclusive(work) · mu.Lock(); defer mu.Unlock()
       with open(path, "w") as f: f.write(data) · try (var w = Files.newBufferedWriter(p)) { … }
```
**Read the code:** For each acquire, walk every exit — return, throw, `break`, `continue`, cancel,
timeout. Does a release sit in `finally` / `defer` / `with` / `using`? Is ownership handed to a
caller that releases it? Is the resource framework-managed (§ 47)? For a written file, is the
`Close` / `flush` error returned? **Finding when** a failure between acquire and release leaves the
pair open and the next caller sees it (a hang, a disabled control, a truncated file). **Proof:**
paired-state restore: inject the failure, then assert the lock is free, the flag is false, `close`
ran once, the close error surfaced.

## Proof — port fault injection

The oracle, its per-stack shapes and the variants are in
[`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Code quality (*Port fault injection*,
*Unhandled-failure hook*, *Cause chain*, *Paired-state restore*; variants V74–V79). The shape:

1. Find the port: the client, repository, gateway or task the guarded code calls. Fake it at that
   boundary (a spy, a fake implementing the interface, a local HTTP stub), never the code under test.
2. Drive the **real entry point** (route, consumer, job, hook) with the failure injected, and assert
   what the caller must see: the documented status or typed error, the cause, nothing published, the
   flag reset.
3. The test **fails before the fix** for the stated reason; paste the failing line. A test that
   passes on unfixed code proves nothing: the candidate goes back to the verifier.
4. Run the class variants (each dependency in turn; a failure inside cleanup), with the happy path
   as the control.

A fix here changes behaviour, so it is **failing-first, never characterization-first**: a
characterization test pins the swallow it is meant to remove. `test-shield` does not run for these
classes, and neither `/refactor` nor align's structural tier applies them.

## Output

```
error-handling-scan — lanes: ts (eslint 10.12 recommended — no type-aware rule), python (ruff 0.16 S110/B904 configured); go, jvm, c#, ruby, php, rust absent
Context: 2 global error primitives (AllExceptionsFilter, ErrorBoundary) · no unhandledRejection handler · Node 22 (package.json engines)

Findings: 3 · Unconfirmed: 1

1. src/webhooks/payments.controller.ts:41                       [report-with-fix]   high
   §1 dropped — the catch around applyPaymentEvent() has a comment-only body, then 200 is sent.
   A failed status write (DB down, constraint) is acknowledged; the provider never redelivers.
   Reached by POST /webhooks/payments. Proof: test/webhooks/payments.fault.e2e-spec.ts — repo.save
   rejects → expected 503, got 200 (fails). Fix: log with the event id and answer 503. CWE-1069

2. web/src/features/statements/useStatements.ts:31               [report-with-fix]   medium
   §2 success-shaped — .catch(() => setData([])): an API outage renders "No statements". Proof:
   msw answers 500 → the empty state renders, the error state does not (fails). Fix: setError(e)
   and render the existing <ErrorState>. CWE-392

3. src/payments/psp-client.ts:14                             [report-with-fix]   high
   §3 unchecked status — createCharge() parses res.json() with no res.ok check; a 402 body is
   returned as a charge. Proof: stub answers 402 {"id":"ch_x"} → the order is marked paid (fails).
   Fix: throw PaymentDeclined(res.status) before parsing, as refund() at :40 already does. CWE-252

4. src/subscriptions/renewal.service.ts:58                      [report-flagged]    high
   §4 floating — sendReceipt() returns a promise, neither awaited nor caught. Unproven link:
   no type-aware lane ran; the callee's async signature was read at receipts.ts:12. Settling test:
   the mailer fake rejects → the process must not exit and the failure must be logged.

Verification: 41 candidates → 3 findings · 1 unconfirmed · 22 hardening · 0 pre-existing · 15 refuted

Class coverage:
  §1  dropped error              checked (60 shipped hits / 21 groups → 1 finding; scripts/ dismissed with one read)
  §2  success-shaped value       checked (131 hits / 34 groups → 1 finding) · Live, unreviewed (12 groups / 40 hits — continue with grep 2a on web/src/features)
  §3  unchecked signal           checked (21 hits → 1 finding)
  §4  unobserved async           partial (no type-aware lane: greps 4a–4c only, 3 hits → 1 unconfirmed)
  §5  catch-all                  N/A (TypeScript only: every catch is a catch-all; read under §1 / §2)
  §6  cause / outcome rewritten  checked (20 hits → 0 findings; preserve-caught-error at error owns 6a)
  §7  paired state               checked (2 hits → 0 findings)
```

`[report-with-fix]`: the failure is named, the path from the entry point is traced, the injection
test failed, and the fix uses the project's own primitive. `[report-flagged]`: one link is
unproven — no harness, no type-aware lane, a callee not read — and the row names it with the
settling test. The coverage block lists **all seven** classes on every run: `checked (k hits → m
findings)` only when the grep ran on a present lane; `partial (<reason>)` when a lane the class
needs did not run; `N/A (<reason>)` only when the repo has no such surface; `blocked (<reason>)`
when a grep failed or code could not be read. A partial review reads
`Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/code-quality.md`](../../../../snippets/precedents/code-quality.md)
(errors and async are § 14–25; resources § 47–48; version precedents § 71–83) and
[`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10. The ones
this skill meets most:

- **A declared degrade mode** — logged or counted, documented as the behaviour (§ 14). On an audit trail or compliance step it flips back: a silently incomplete record is the finding.
- **A comment with a checkable reason** (§ 18). On the real repo above, 46 of 60 shipped empty handlers carried one; each is verified against the code, not accepted as text.
- **Parse-or-default and tolerant error-body parsing** (§ 15, § 16); **best-effort cleanup** on a failed or finished path (§ 17).
- **The failure reaches a global filter or boundary** that logs and maps it (§ 24).
- **Bulk triage is not a verdict.** "All 131 are UI fallbacks" is not a reading; a group is dismissed only with its consumer read.

## When to run

- On any diff that adds or changes a `catch` / `except` / `rescue` / `if err != nil`, a promise
  chain or an `async` callback, an outbound HTTP call, a queue or webhook handler, a lock, or a
  busy flag — the `/review-changes` and `/quality-audit` dispatch signal.
- On every whole-repo `/quality-audit` and `/audit` (its Unhandled-I/O pass dispatches here),
  reporting all seven classes. Align dispatches it for `silent-catch` and `unhandled-io`.
- When an incident had no error in the logs, or a user saw "nothing found" during an outage.

## Halt conditions

- Do not report a high or critical row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/quality-audit` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the site `<file:line>`, the named failure it hides, the entry point, what the caller sees instead, and the fix in the project's own primitive.
- Do not report a grep hit as a finding, and do not dismiss a group without reading its consumer.
- Do not propose a characterization test, a wider catch, a suppression, or a retry around the swallow as the fix. The fix surfaces the failure: propagate, retry with a bound, compensate, or degrade **visibly**.
- Do not print "no swallowed errors" without the class-coverage block. A class whose grep did not run is `blocked`, never `checked`; §4 without a type-aware lane is `partial`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `/quality-audit` dispatches this skill and folds its coverage block into the class ledger; `/quality-fix` closes the findings failing-first, re-runs this detector on the patched line, and sweeps siblings with the [`fix-bug-core.md`](../../../../snippets/fix-bug-core.md) ledger.
- `concerns/error-handling.md` (C4) is the method: the four outcomes and the closure verbs (`surface-to-caller`, `bound-the-retry`, `compensate-partial`, `declare-degrade-mode`, `fail-the-exit-code`, `render-error-state`).
- Align no longer detects error handling: `align-detect` prints `owner: code-quality → /quality-audit` for the legacy `silent-catch` and `unhandled-io` classes and routes such ledger rows to `/quality-fix`. `/audit`'s Unhandled-I/O pass dispatches here (the code-quality pack is universal).
- `type-safety-scan` (this pack) owns the cast that turns an unparsed error body into a typed value; `@error-detective` (this pack) clusters the runtime errors this skill's findings stop hiding.
- `@resilience-reviewer` (distributed-systems), `transaction-scan` and `connection-config-scan` (database), `memory-growth-scan` (performance), `data-exposure-scan` (security), `log-signal-scan` and `metric-hygiene-scan` (observability): the neighbouring classes in § Boundaries.

Method credits: the "list the errors this catch could hide" read step adapts the
`silent-failure-hunter` agent of Anthropic's `pr-review-toolkit` plugin
(<https://github.com/anthropics/claude-plugins-official>, Apache-2.0); rule ids and versions come
from the code-quality research catalog for this pack (2026-10-05).
