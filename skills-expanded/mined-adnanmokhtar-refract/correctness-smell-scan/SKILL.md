---
name: correctness-smell-scan
description: Find logic that is wrong for one input — discarded pure results, equality and boolean traps, shared or captured state, float money and unsafe parses, non-exhaustive switches, naive time, leftover breakpoints — each proved by a concrete-input test.
kind: skill
pack: code-quality
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: correctness-smell-scan

## Premise

Most logic bugs compile, pass the happy-path tests and look right on review. `title.trim();` throws
its result away. `order.refunded = cents` overwrites the running total the line above checked
against. `amount * 100` on a float turns 1.005 into 100 cents. A `switch` on the order status
answers `'paid'` for the status added last month. `new Date('2026-03-29')` is midnight UTC, which is
the 28th west of Greenwich. Each is correct for most inputs and wrong for one — and that one input
is the proof. This skill hunts the classic bug patterns that analyzers name and code review keeps
missing: the correctness classes `refute-before-report.md` gate 5 keeps, never style.

**Every finding cites the line `<file:line>` + the class + the one concrete input (value, sequence,
time zone, locale) + the wrong output it produces, against the expected output and where that
expectation comes from (a spec, a test name, a doc, a type contract, a sibling call site) + the
entry point that reaches it + the proof (or the test that would settle it) + the fix.** A grep or
analyzer hit is never a finding by itself, and "no logic bugs" is never printed without the
class-coverage block (§ Output).

**Analyzer lane first, then greps, then the read.** A rule the project runs at **error** in CI owns
its class (`precedents/code-quality.md § 2`). The greps below are the fallback for repos that do not
run the rule, and the candidate list for the read. The proof is a **boundary value vector**: the
concrete input at the real entry point, wrong before the fix and right after
([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Code quality, variant V83). A
candidate with no harness is **Unconfirmed** with the settling test written out; it is never
dropped, and never promoted on reading alone.

## The rule

A pattern is a finding when all four hold:

1. **An input makes it wrong.** Name the value, sequence, zone or locale, and the wrong output. A
   pattern with no nameable violating input is maintainability or noise, not this skill's.
2. **The expectation is sourced.** The right output comes from a spec, a doc, a test name, the type
   contract, or a sibling that does the same job correctly — never from the finder's opinion
   (`precedents/code-quality.md § 50`).
3. **A real entry point reaches it** — route, job, consumer, CLI, UI event — with that input
   possible on the way (each validator, schema and constraint upstream is read, not assumed).
4. **No precedent applies** with its "must be true" clause shown (§ False positives).

## Boundaries

This skill owns the classic bug patterns in code. It routes what another skill owns:

- **Business check-then-act races** — a balance, stock, quota or single-use check followed by a write, a double submit that charges twice → security `logic-race-scan` § 4 to § 6, and **client-supplied numbers** out of range (a negative quantity, a client-trusted price) → its § 1 and § 2, when the security pack is installed. A read-modify-write lost update in the database → database `transaction-scan`. Without those packs the candidate runs here and is tagged `security-class (owner pack not installed)` or `data-class (owner pack not installed)` ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 9).
- **Swallowed, converted or unobserved errors**, floating promises, resources the error path skips → `error-handling-scan` (this pack). A shadowed `err` that drops a failure is reported in §3 here and credited to both.
- **Null dereferences, non-null assertions, unchecked casts, checker strictness** → `type-safety-scan` (this pack).
- **Unreachable branches and dead flags** → `dead-code-scan`; **two copies of one rule that drifted** → `duplication-scan` (both this pack).
- **Money and time column types** (float money, timestamp without zone, the DB session zone) → database `schema-integrity-scan`, when installed. §4 and §6 here own the arithmetic and the clock in code; one seeded float price is usually both — dedupe by `<file:line>`.
- **Regexes with a security job** — ReDoS, URL and host allow-lists, trojan-source Unicode → security `injection-scan` § 13 and `ssrf-scan`. **Security rules of the same analyzers** (semgrep, gosec, ruff `S`) → security `sast-scan`; dedupe by `<file:line>`, security wins.
- **Cache staleness and invalidation** in a client → frontend `client-data-scan` §4, judged by `@data-flow-auditor`, when the frontend pack is installed. **UI request races across renders** (a response from an earlier render or input painted over a later one, no cancellation) → `client-data-scan` §3, and **route-param races** (navigation 1's response painted on navigation 2) → `routing-scan` §8, when installed. §3 keeps the stale closure inside one effect; without the frontend pack it also keeps the out-of-order response.
- **`console.log` left in server code** → `standards-check.py` OBS-5. **A debug endpoint** → security `data-exposure-scan`. §7 owns only breakpoints and dump-and-die calls.
- **Time-dependent tests** → testing `flake-source-scan`, when installed; §6 owns the production clock.
- **An algorithm's contract** — sortedness, stability and key-uniqueness preconditions, the distribution of random draws, and geodesy (planar distance, axis order, wrap-around) → algorithms `algorithm-contract-scan`, when installed; the comparator expression itself stays §4 here. Without the algorithms pack, report the contract half here tagged `algorithms-class (owner pack not installed)`.

## Adapt to the codebase — the analyzer lanes

Read each analyzer's version and enabled rules from the lockfile and its config (grep 0b) before
trusting a quiet run, and print the lanes you ran in the output header. Versions are the research
catalog's, verified 2026-10-05.

| Lane | §1 discarded result | §2 equality, logic, regex | §3 shared or captured state | §4 numbers, bounds, order | §5 switch, fallthrough | §6 time, locale, text | §7 breakpoints |
|---|---|---|---|---|---|---|---|
| **TS / JS** — ESLint 10.12, typescript-eslint 8.71, react-hooks 7.1.1 | ts-eslint `no-unused-expressions` | core `eqeqeq` (`{"null":"ignore"}`), `use-isnan`, `no-self-compare`, `no-constant-binary-expression`, `no-cond-assign`, `no-dupe-else-if`, `no-misleading-character-class`; type-aware `no-unsafe-enum-comparison` | `no-loop-func`, `no-param-reassign` (`{props:true}`); react-hooks `exhaustive-deps`, `immutability` | `radix`, `no-loss-of-precision`, `for-direction`; type-aware `require-array-sort-compare` | type-aware `switch-exhaustiveness-check`; core `no-fallthrough` | — (greps 6a, 6e) | `no-debugger` |
| **Python** — Ruff 0.16.10, mypy 2.4.0, pyright 1.1.414 | — (grep 1b) | `E711`, `F632`, `PLR1714`, `PLR0124`, `PLW0177`, `PLW1641`, `B034` | `B006`, `B008`, `B023`, `B031`, `RUF012`, `PLW2901` | `RUF032`, `B905`, `PLE0643` | mypy `exhaustive-match`; pyright `reportMatchNotExhaustive` | `DTZ001`–`DTZ012`, `UP017` | `T100` |
| **Go** — golangci-lint v2.14, staticcheck 2026.2.1 | staticcheck `SA4017`; govet `unusedresult` | `SA4000`, `SA4012`, `errorlint`; govet `bools` | govet `copylocks`, `shadow`, `loopclosure` (only `go` < 1.22), `appends`; `go test -race` | gosec `G115`, `G109`; govet `sortslice`; `durationcheck` | `exhaustive` with `default-signifies-exhaustive: false` | govet `timeformat`; `SA1002` | — |
| **JVM** — Error Prone 2.50, SpotBugs 4.10.4, detekt 1.23 | EP `CheckReturnValue`, `ReturnValueIgnored`, `ArgumentSelectionDefectChecker`; SpotBugs `RV_RETURN_VALUE_IGNORED*` | EP `ReferenceEquality`, `BoxedPrimitiveEquality`, `BigDecimalEquals`, `EqualsHashCode`, `OperatorPrecedence` | SpotBugs `EI_EXPOSE_REP*`, `IS2_INCONSISTENT_SYNC` | EP `IntLongMath`, `BigDecimalLiteralDouble`, `ComparisonContractViolated` | EP `MissingCasesInEnumSwitch`, `FallThrough`; detekt `ElseCaseInsteadOfExhaustiveWhen` | EP `JavaTimeDefaultTimeZone`, `MisusedWeekYear`, `StringCaseLocaleUsage`; detekt `ImplicitDefaultLocale` | — |
| **C#** — Roslyn, VS Threading 18.7 | CA1806 | CA2013, CA2242 | — | `<CheckForOverflowUnderflow>` | CS8509 | CA1304, CA1305, CA1309, CA1311 | — |
| **Ruby** — RuboCop 1.91 | `Lint/Void` | `Lint/BinaryOperatorWithIdenticalOperands`, `Lint/AssignmentInCondition`, `Lint/FloatComparison` | `Lint/SharedMutableDefault`, `Style/MutableConstant` | `Lint/NumberConversion`, `Lint/BigDecimalNew` | — | `Rails/TimeZone` | `Lint/Debugger` |
| **PHP** — PHPStan 2.2 (+ strict-rules; larastan on Laravel) | `method.resultUnused`, `function.resultUnused` | strict-rules `equal.notAllowed` | — | — | `match.unhandled` | — | — |
| **Rust** — clippy | rustc `unused_must_use` | `eq_op`, `float_cmp`, `nonminimal_bool` | `await_holding_lock` | `cast_possible_truncation`, `cast_sign_loss` | `wildcard_enum_match_arm` | `string_slice` | `dbg_macro` |

Lane commands (installed tools only — an absent one prints `NOT-RUN (<tool> not installed — to enable: <install command>)` and its grep runs): `npx --no eslint . --max-warnings=0 -f json`; `ruff check --select B,DTZ,PL,RUF,E711,F632,T100 --output-format json .`; `golangci-lint run ./...`; `./gradlew spotbugsMain`; `dotnet build -warnaserror`; `bundle exec rubocop --only Lint --format json`; `vendor/bin/phpstan analyse -l 9 src`; `cargo clippy --all-targets -- -D warnings`. Three traps, each a precedent: typescript-eslint `recommended` runs no type-aware rule (`precedents/code-quality.md § 76`); golangci's `exhaustive.default-signifies-exhaustive: true` counts any `default` as exhaustive (§ 77); detekt without type resolution skips most potential-bug rules (§ 81). `eslint-plugin-sonarjs` 4.2.2 and `eslint-plugin-unicorn` 77 add rules for §1, §2 and §4 — run them where the project installs them; sonarjs ships under the Sonar Source-Available License, so cite its rule ids and never vendor its docs (§ 83). CodeQL's `<lang>-code-quality.qls` suites (CLI 2.27.1) cover JS/TS, Python, Go, Java, C# and C++; running the CLI on private code needs GitHub Advanced Security, so the lane is optional and never assumed.

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep
**N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`.`): `rg` given no path
reads stdin whenever stdin is a pipe, and under an agent's shell that is a silent zero-hit run. Lane
absence comes from the lane count the block prints first, never from a quiet grep. Any `rg` error on
stderr (exit 2, or `match limit exceeded`) is a failed grep, never zero hits.

```bash
# Not production code: vendored, built, tests, specs, mocks, fixtures, stories, migrations, seeds, generated, catalogs, docs, ai/.
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/*.min.*' -g '!**/*.d.ts'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,stories,migrations,migrate,seeds,generated,__generated__,locales,i18n}/**'
   -g '!**/*.{spec,test,e2e-spec,mock,stories,test-data,fixture,fixtures}.*' -g '!**/{*_test,*_spec,test_*,conftest}.*' -g '!*.{md,mdx,json,lock,snap,map,svg,yml,yaml,sql,html}' -g '!docs/**' -g '!ai/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')   # drops comment-only lines
M='(?i:price|amount|total|subtotal|cost|balance|fee|tax|vat|discount|refund|payout|charge|credit|debit|wallet|cents?|money|currency)'
for t in js ts py go java kotlin cs ruby php rust; do printf '%-7s %s\n' "$t" "$(rg --files -t "$t" "${X[@]}" . | wc -l)"; done   # 0 = lane absent

# 0. Context: 0a language versions and pinned zones (gate 3: Go loop variables, Node, Python; TZ=UTC in the image);
#    0b correctness rules already configured (a rule at error in CI owns its class); 0c date and decimal libraries in use.
rg -n --pcre2 '^go\s+1\.\d+|"node"\s*:\s*"[^"]+"|requires-python|python_requires|^\s*(?:ENV\s+)?TZ\s*[=:]\s*["\x27]?\w|\buser\.timezone\b|InvariantGlobalization|"(?:typescript|eslint|typescript-eslint|@typescript-eslint/eslint-plugin|eslint-plugin-sonarjs|eslint-plugin-unicorn)"\s*:' -g '{go.mod,package.json,.nvmrc,pyproject.toml,setup.cfg,setup.py,Dockerfile*,docker-compose*.yml,compose*.yml,*.csproj,.env.example}' -g '!**/node_modules/**' .
rg -n --pcre2 '\b(?:eqeqeq|use-isnan|no-self-compare|no-constant-binary-expression|no-fallthrough|no-debugger|radix|no-loss-of-precision|switch-exhaustiveness-check|require-array-sort-compare|no-unsafe-enum-comparison|no-shadow|no-loop-func|exhaustive-deps|projectService|(?:recommended|strict)TypeChecked)\b|\b(?:B006|B008|B023|B031|B034|B905|DTZ\d{3}|DTZ|PLR1714|PLR0124|F632|E711|T100|RUF032)\b|\b(?:exhaustive|copyloopvar|durationcheck|gosec)\b|\b(?:MissingCasesInEnumSwitch|ReturnValueIgnored|BigDecimalEquals|JavaTimeDefaultTimeZone)\b|\bCA(?:1304|1305|1309|1311|1806)\b|Lint/Debugger' -g '{eslint.config.*,.eslintrc*,pyproject.toml,setup.cfg,ruff.toml,.ruff.toml,.golangci.*,*.csproj,Directory.Build.props,.editorconfig,.rubocop.yml,build.gradle*,pom.xml,phpstan.neon*,Cargo.toml,clippy.toml}' -g '!**/node_modules/**' .
rg -o --no-filename --pcre2 '\bfrom\s+["\x27]\K(?:luxon|date-fns(?:-tz)?|dayjs|moment(?:-timezone)?|@js-temporal/polyfill|temporal-polyfill|decimal\.js|big\.js|bignumber\.js|dinero\.js|currency\.js)(?=["\x27])|^\s*(?:from|import)\s+\K(?:zoneinfo|pytz|pendulum|arrow|decimal|babel)\b|"github\.com/shopspring/decimal"|\bjava\.math\.BigDecimal\b|\bNodaTime\b' "${X[@]}" . | sort | uniq -c

# 1. A result computed and thrown away: a pure or immutable call used as a statement. 1a JS/TS (statement start only);
#    1b Python; 1c Go; 1d Java / Kotlin; 1e C#; 1f Ruby non-bang methods.
rg -n -U --pcre2 '(?:(?<=[;{}]\n)|\A)[ \t]*(?!(?:return|await|yield|const|let|var|throw|export|if|else|case)\b)(?:this\.)?[\w$]+(?:\.[\w$]+|\[[^\]\n]+\])*\.(?:trim|trimStart|trimEnd|replace|replaceAll|concat|slice|toUpperCase|toLowerCase|padStart|padEnd|normalize|toSorted|toReversed|toSpliced|with|filter|plus|minus|startOf|endOf|setZone|toUTC)\([^;\n]*\)\s*;?\s*$' -t js -t ts "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '^\s*(?!(?:return|yield|await|print|assert|raise)\b)[\w.]+\.(?:strip|lstrip|rstrip|replace|lower|upper|casefold|title|capitalize|removeprefix|removesuffix|zfill|ljust|rjust|center|astimezone)\([^\n]*\)\s*$' -t py "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '^\s*(?:strings|bytes|filepath|path)\.(?:TrimSpace|Trim\w*|ToLower|ToUpper|Title|Replace\w*|Join|Clean|Fields)\(|^\s*append\(|^\s*\w+\.(?:Add|AddDate|Truncate|Round|In|UTC)\([^\n]*\)\s*$' -t go "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '^\s*[\w.]+\.(?:trim|strip|toUpperCase|toLowerCase|concat|substring|replace(?:All|First)?|plus\w+|minus\w+|with(?:Day\w*|Month|Year|Hour|Minute|Second|Nano)|setScale|stripTrailingZeros|negate)\([^;\n]*\)\s*;' -t java -t kotlin "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '^\s*[\w.]+\.(?:Trim\w*|Replace|ToUpper\w*|ToLower\w*|Substring|PadLeft|PadRight|Add(?:Days|Hours|Minutes|Seconds|Months|Years|Ticks|Milliseconds))\([^;\n]*\)\s*;' -t cs "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '^\s*@?\w+(?:\.\w+)*\.(?:strip|gsub|sub|downcase|upcase|squeeze|chomp|merge|compact|uniq|sort|sort_by|reverse|flatten|reject|select|map)(?:\([^\n]*\))?\s*$' -t ruby "${X[@]}" . | "${NC[@]}"

# 2. Equality, boolean and pattern logic: 2a JS loose ==/!= not against null; 2b NaN, an impossible typeof, x != a || x != b;
#    2c Python `is` on a literal, `== None`, `x == a or 'b'`; 2d JVM string ==, BigDecimal.equals, Go time.Time ==,
#    error text compared, PHP in_array without strict; 2e a literal assigned inside a condition, and a guard on `a.b + v`
#    followed by a write of `a.b = v` (the accumulator overwritten); 2f regex API traps, unparenthesised anchored
#    alternation in a validator, split on a metacharacter, a /g regex reused with .test().
rg -n --pcre2 '(?<![=!<>])[=!]=(?!=)\s*(?!null\b)(?=\S)|(?<=\S)\s*(?<![=!<>])(?<!null)\s[=!]=(?!=)' -t js -t ts -g '!*.config.*' "${X[@]}" . | rg --pcre2 '(?<![=!<>])[!=]=(?!=)' | rg -v --pcre2 '[=!]=\s*null\b|\bnull\s*[=!]=(?!=)|=>|<=|>=' | rg -v --pcre2 '\b(?:ARGV|KEYS)\[|redis\.call\(' | "${NC[@]}"
rg -n --pcre2 '[=!]==?\s*NaN\b|\bNaN\s*[=!]==?|\btypeof\s+[\w.$]+\s*[=!]==?\s*["\x27](?!(?:undefined|object|boolean|number|string|function|symbol|bigint)["\x27])|\b(\w+(?:\.\w+)*)\s*!==?\s*[^|&\n]+\|\|\s*\1\s*!==?' -t js -t ts "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bis\s+(?:not\s+)?(?:["\x27\d\[\{]|-\d)|[=!]=\s*None\b|==\s*[^\s=]+\s+or\s+(?:["\x27]|\d)' -t py "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '"[^"\n]*"\s*[=!]=(?!=)|(?<![=!<>])[=!]=\s*"[^"\n]*"|\bBigDecimal\b[^\n]*\.equals\(|\.equals\([^)\n]*BigDecimal' -t java -t kotlin "${X[@]}" . | rg -v --pcre2 '===|!==' | "${NC[@]}"
rg -n --pcre2 '\b\w*(?:Time|At|Date)\s*[=!]=\s*\w*(?:Time|At|Date)\b|\berr\.Error\(\)\s*[=!]=' -t go "${X[@]}" . | "${NC[@]}"; rg -n --pcre2 '\bin_array\((?![^)\n]*,\s*true\s*\))' -t php "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\b(?:if|while)\s*\([^\n]*\(\s*[\w.$\]\[]+\s*=(?![=>])\s*(?:-?\d+|["\x27][^"\x27\n]*["\x27]|true|false|null|None)\s*\)' "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '\b([\w$]+(?:\.[\w$]+)+)\s*\+\s*([\w$.]+)\s*[<>]=?[^\n]*\n(?:[^\n]*\n){0,8}?[^\n]*?\K\b\1\s*=\s*\2\s*;' -t js -t ts -t java -t cs -t php "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bre\.match\(|\bre\.sub\([^)\n]*,\s*re\.[A-Z]+\s*\)|/\^[^/|()$\n]*\|[^/^\n]*\$/[a-z]*\.test\(|\.match\(\s*/\^[^/|()$\n]*\|[^/^\n]*\$/|\.split\(\s*"[.|$^*+?]"\s*\)' "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '\b(?:const|let|var)\s+(\w+)\s*=[ \t]*/(?![/*])(?:\\.|\[(?:\\.|[^\]\n])*\]|[^/\\\n\[])+/[a-z]*g[a-z]*(?=[ \t]*[;,)]|[ \t]*$)(?=[\s\S]{0,2000}?\b\1\.test\()' -t js -t ts "${X[@]}" . | "${NC[@]}"

# 3. Shared, aliased or captured state: 3a Python mutable defaults, [[…]] * n, fromkeys with a mutable value; 3b a caller's
#    props / state / params mutated in place; 3c a loop variable captured late (Python lambda, JS `for (var`, Go `go func()`
#    in a range loop — Go < 1.22 only, per 0a); 3d an effect with an empty dependency list (stale closure); 3e a response
#    body read twice, a request body drained by middleware; 3f Go functions with a named `err` result (read for shadowing).
rg -n --pcre2 '^\s*(?:async\s+)?def\s+\w+\([^)]*=\s*(?:\[\]|\{\}|set\(\)|list\(\)|dict\(\)|defaultdict\(|\[[^\]\n]+\]|\{[^}\n]+\})\s*[,)]|\[\[[^\]\n]*\]\]\s*\*\s*\w+|\bdict\.fromkeys\([^,\n]+,\s*(?:\[\]|\{\}|set\(\))' -t py "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\b(?:props|state|params|args|options|opts)\.(?:\w+\.)*(?:sort|reverse|splice|fill|copyWithin)\(|\b(?:props|state)\.\w+(?:\.\w+)*\.(?:push|pop|shift|unshift)\(' -t js -t ts "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '^([ \t]*)for\s+(\w+)\b[^\n]*\bin\b[^\n]*:[ \t]*\n(?>\1[ \t]+[^\n]*\n|[ \t]*\n){0,30}?\1[ \t]++[^\n]*?\K\blambda\b(?![^:\n]*\b\2\s*=\s*\2\b)[^:\n]*:[^\n]*\b\2\b' -t py "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bfor\s*\(\s*var\s+\w+' -t js -t ts "${X[@]}" . | "${NC[@]}"; rg -n -U --pcre2 '^([ \t]*)for\s+(?:\w+\s*,\s*)?(\w+)\s*:=\s*range\b[^\n]*\n(?>\1[ \t]+[^\n]*\n|[ \t]*\n){0,30}?\1[ \t]++\Kgo\s+func\s*\(\s*\)' -t go "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '\buseEffect\(\s*(?:async\s*)?\(\)\s*=>\s*\{[^\n]*\n(?:(?![^\n]*\buseEffect\()[^\n]*\n){0,25}?[^\n]*?\K\}\s*,\s*\[\s*\]\s*\)' -t js -t ts "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '\b(?:const|let|var)\s+(\w+)\s*=\s*await\s+fetch\((?=(?:(?!\n\}|\bfunction\b)[\s\S])*?\b\1\.(?:json|text|arrayBuffer|blob|formData)\(\)(?:(?!\breturn\b|\bthrow\b|\n\})[\s\S])*?\b\1\.(?:json|text|arrayBuffer|blob|formData)\(\))|\bio\.ReadAll\(\s*r\.Body\s*\)' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '^func\b[^\n]*\)\s*\([^)\n]*\berr\s+error\s*\)\s*\{' -t go "${X[@]}" . | "${NC[@]}"

# 4. Numbers, bounds and order: 4a a boolean comparator, numeric-named arrays sorted with no comparator; 4b JS/TS money
#    through binary floats (parseFloat, toFixed round-trips, x * 100 rounding); 4c the same in Python / Go / JVM / C#;
#    4d parse traps (parseInt without radix, Number() of request input, `| 0`) and Go narrowing; 4e bounds: `<= length`,
#    range(len - 1), reduce without a seed, Math.max/min of a spread, a 1-based page times the page size; 4f a chunk loop
#    that stops a chunk early (drops the tail); 4g a seconds value handed to a milliseconds API (Retry-After).
rg -n --pcre2 '\.sort\(\s*\(\s*\w+\s*,\s*\w+\s*\)\s*=>\s*[\w.\[\]]+\s*[<>]=?\s*[\w.\[\]]+\s*\)|\b\w*(?i:ids|counts?|amounts?|totals?|prices?|scores?|numbers|nums|values|sizes|lengths|ages|years|days|weights|ranks|cents|quantit\w*|qtys?|levels|versions|ports|ind(?:ex|ic)es)\b\)?\.(?:sort|toSorted)\(\s*\)|\.map\(\s*(?:Number|parseInt|parseFloat)\s*\)\.(?:sort|toSorted)\(\s*\)' -t js -t ts "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\b(?:parseFloat|Number)\([^()\n]*\.toFixed\(|\bparseFloat\([^)\n]*'"$M"'|\b\w*'"$M"'\w*\s*=\s*parseFloat\(|\bMath\.round\(\s*[\w.]*'"$M"'\w*\s*\*\s*100\b' -t js -t ts "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bfloat\([^\n]*'"$M"'|'"$M"'\w*\s*=\s*float\(|\bDecimal\(\s*-?\d+\.\d+\s*\)|\bround\([^\n]*'"$M" -t py "${X[@]}" . | "${NC[@]}"; rg -n --pcre2 '\b\w*'"$M"'\w*\s+float(?:32|64)\b|\bfloat(?:32|64)\(\s*\w*'"$M" -t go "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\b(?:double|float|Double|Float)\s+\w*'"$M"'|\bnew\s+BigDecimal\(\s*-?[\d.]+\s*\)|\bMath\.Round\(\s*[^,()\n]*\)' -t java -t kotlin -t cs "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bparseInt\(\s*[^,()\n]+(?:\([^()\n]*\))?\s*\)|\bNumber\(\s*(?:req|request|params|query|body|input|args)\b|\b(?:req|request)\.(?:query|params|body)\.\w+\s*\|\s*0\b' -t js -t ts "${X[@]}" . | "${NC[@]}"; rg -n --pcre2 '\bu?int(?:8|16|32)\(\s*[\w.]+\s*\)' -t go "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\b(?:i|j|k|idx|index)\s*<=\s*[\w.]+(?:\.length|\.size\(\)|\.Count|\.len\(\))|\bi\s*<=\s*len\(|\brange\(\s*len\(\w+\)\s*-\s*1\s*\)|\.reduce\(\s*(?:\([^()\n]*\)|\w+)\s*=>[^,\n]*\)\s*;?\s*$|\bMath\.(?:max|min)\(\s*\.\.\.|\b(?:offset|skip|start|from)\w*\s*=\s*\(?\s*\w*[pP]age(?:Number|No|Index)?\s*\)?\s*\*\s*[\w.]+' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\brange\(\s*0\s*,\s*len\([^()\n]+\)\s*-\s*[\w.]+\s*,\s*[\w.]+\s*\)|<\s*[\w.]+\.length\s*-\s*[\w.]+\s*;\s*\w+\s*\+=\s*[\w.]+' "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\b(?:setTimeout|sleep|delay|wait)\w*\([^,\n]*,?\s*[\w.]*(?i:retry_?after|seconds?|secs)\w*\s*\)' -t js -t ts "${X[@]}" . | "${NC[@]}"

# 5. Switches and transitions: 5a a switch on a status / kind / type / state whose `default` does not throw; 5b the same in
#    Python `case _:`, Kotlin `else ->`, Rust `_ =>`; 5c a case body with statements and no break before the next label,
#    Go `fallthrough`; 5d files that write a status literal (many writers and no transition table → read).
rg -n -U --pcre2 '\bswitch\s*\(\s*[\w.$]*?(?i:status|state|kind|type|stage|phase|step|mode|role|plan|tier|event)\w*\s*\)\s*\{[^\n]*\n(?:(?![^\n]*\bswitch\s*\()[^\n]*\n){0,150}?[^\n]*?\K\bdefault\s*:(?!\s*(?://[^\n]*\s*)*(?:throw\b|return\s+(?:assertNever|exhaustive\w*|unreachable)\w*\(|assertNever\(|exhaustive\w*\(|unreachable\w*\())' -t js -t ts -t java -t cs -t php "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '^([ \t]*)case\s+_\s*:[ \t]*\n\1[ \t]+(?!raise\b|assert_never\b|typing\.assert_never\b)\S|\belse\s*->\s*(?!throw\b|error\(|TODO\()|^\s*_\s*=>\s*(?!unreachable!|panic!|todo!|unimplemented!)' -t py -t kotlin -t rust "${X[@]}" . | "${NC[@]}"
rg -n -U --pcre2 '^[ \t]*case\b[^:\n]+:[ \t]*\n(?:[ \t]*+(?!(?:break|return|throw|continue|case|default|goto)\b|//|/\*|\}|\n)[^\n]*\n)+[ \t]*+(?:case|default)\b' -t js -t ts -t java -t php "${X[@]}" . | "${NC[@]}"; rg -n --pcre2 '^\s*fallthrough\s*$' -t go "${X[@]}" . | "${NC[@]}"
rg -c --pcre2 '\.(?:status|state)\s*=\s*(?:["\x27][A-Za-z_]+["\x27]|[A-Z]\w*\.[A-Z_]\w*)\s*;?\s*$|\bstatus\s*:\s*(?:["\x27][A-Za-z_]+["\x27]|[A-Z]\w*\.[A-Z_]\w*)\s*[,}]' "${X[@]}" . | sort -t: -k2 -rn | head -20

# 6. Time, zone, locale and text: 6a JS/TS date-only parse, literal 0-based month, a calendar day stepped by 24 h, a
#    default-locale format, getYear, a `YYYY` format token (read the library), month rollover; 6b Python naive datetimes; 6c Go local
#    zone, swapped layout; 6d JVM / C# / Ruby / PHP default zone, default locale and week-year; 6e user text cut by code unit;
#    6f a calendar month or year as a fixed day count (read against § 84: an elapsed window is fine, a renewal date is not).
rg -n --pcre2 'new\s+Date\(\s*["\x27\x60]\d{4}-\d{2}-\d{2}["\x27\x60]\s*\)|new\s+Date\(\s*\d{4}\s*,\s*\d{1,2}\s*[,)]|new\s+Date\([^\n]*[-+]\s*[^\n]*(?:\b86400\b|\b864e5\b|\b8640000\b|\b24\s*\*\s*60\s*\*\s*60\b|\b(?:DAY_MS|ONE_DAY\w*|MS_PER_DAY|DAY_IN_MS|MILLIS_PER_DAY)\b)|\.toLocale(?:Date|Time)?String\(\s*\)|\.getYear\(\)|\bformat\w*\([^\n]*["\x27\x60][^"\x27\x60\n]*\bYYYY\b|\bset(?:UTC)?Month\(\s*[\w.]+\.get(?:UTC)?Month\(\)\s*\+' -t js -t ts "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bdatetime\.(?:utcnow|utcfromtimestamp)\(|\bdatetime\.(?:now|today)\(\s*\)|\bdate\.today\(\)|\bdatetime\.fromtimestamp\(\s*[^,()\n]+\)|\.strptime\([^)\n]*\)(?!\.replace\(tzinfo)' -t py "${X[@]}" . | "${NC[@]}"; rg -n --pcre2 '\btime\.Local\b|\.Local\(\)|"2006-02-01|\btime\.Now\(\)\.Format\(' -t go "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bLocalDateTime\.now\(\s*\)|\bLocalDate\.now\(\s*\)|\bnew\s+Date\(\s*\)|\bCalendar\.getInstance\(\s*\)|\bTimeZone\.getDefault\(|\bZoneId\.systemDefault\(|"[^"\n]*\bYYYY\b[^"\n]*"|\.to(?:Lower|Upper)Case\(\s*\)|\bString\.format\(\s*"' -t java -t kotlin "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\bDateTime\.Now\b|\bDateTime\.Today\b|\bDateTime\.Parse\((?![^)\n]*Culture)|\.To(?:Lower|Upper)\(\s*\)' -t cs "${X[@]}" . | "${NC[@]}"; rg -n --pcre2 '\bTime\.now\b|\bTime\.parse\(|\bDate\.today\b|\bDateTime\.now\b' -t ruby "${X[@]}" . | "${NC[@]}"; rg -n --pcre2 '\bdate\(\s*["\x27]|\bstrtotime\(|\bmktime\(' -t php "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\b\w*(?i:name|title|text|body|message|desc\w*|comment|bio|label|subject|summary|content|caption|note|query|search|term|input|reason)\w*(?:\.trim\(\))?\.(?:slice|substring|substr)\(\s*0\s*,\s*[\w.]+\s*\)' -t js -t ts "${X[@]}" . | "${NC[@]}"
rg -n --pcre2 '\btimedelta\(\s*days\s*=\s*(?:28|30|31|365)\s*\)|\b(?:30|31|365)\s*\*\s*(?:24\s*\*\s*60\s*\*\s*60|DAY_MS|ONE_DAY\w*|MS_PER_DAY|86_?400)\b|\bAddDate\(\s*0\s*,\s*0\s*,\s*(?:30|31)\s*\)|\b(?:30|31)\s*\*\s*24\s*\*\s*time\.Hour' "${X[@]}" . | "${NC[@]}"

# 7. A breakpoint or dump-and-die left in shipped code.
rg -n --pcre2 '^\s*debugger\s*;?\s*$|^\s*(?:breakpoint\(\)|import\s+i?pdb\b|from\s+i?pdb\s+import|(?:i?pdb|pudb)\.set_trace\(\))|\bbinding\.(?:pry|irb)\b|^\s*(?:byebug|debugger)\s*$|^\s*(?:dd|dump|var_dump|xdebug_break)\(|\bruntime\.Breakpoint\(\)|\bdbg!\(|\bIEx\.pry\b|\bSystem\.Diagnostics\.Debugger\.(?:Break|Launch)\(' "${X[@]}" . | "${NC[@]}"
```

A finding is a grep hit **plus** a read of the function **plus** the input that breaks it **plus**
the hops to an entry point. Three blind spots are structural:

- **Types decide most of these, and grep has none.** `xs.sort()` is a bug on numbers and correct on
  ISO dates; `a == b` is a bug on boxed `Integer` and fine on `int`. The type-aware lanes
  (`require-array-sort-compare`, `switch-exhaustiveness-check`, `no-unsafe-enum-comparison`, Error
  Prone) are the detectors; without them, print `§2 / §4 / §5 partial (no type-aware lane)`.
- **Statement shapes vary.** A discarded result inside a ternary, a one-line `case` body, a `switch`
  over 150 lines, or a comparator in a named function escape these greps. Read the function around
  each hit, and every `switch` on a domain enum in the files grep 5d ranks first.
- **Names carry 4b, 6e and 5a.** The money, text and status greps key on identifiers. A float amount
  called `v` is missed; follow the value from the parse or the column, not the name.

**Measured** (2026-10-05). Fixtures: on `review-decoys`, 2e lands on its seeded assignment in a
condition and on its overwritten accumulator, 4e on its 1-based page × page size, 3d on its stale
empty-deps effect and 4b on its `parseFloat` amount, each on the seeded line; its decoys —
`Number.parseInt(…, 10)` and the `while ((m = re.exec(s)) !== null)` idiom — stay out. On
`slow-marketplace`, 4b lands on two `Math.round(price * 100)` lines in the checkout service and the
web cart, and 4c on a `float(row["amount"])` importer (the code side of its float-money columns,
which database owns); on `vuln-fullstack`, 4b lands on one import parser. `node-api`, `reward-hack`, `half-built-crm` and
`web-dashboard` produce no §1, §2, §5 or §7 hit. On a real NestJS-on-Fastify + MikroORM + React
monorepo (about 14,200 tracked files; the script runs in about 3 s): 0b no rule of this set
configured and no type-aware rules; 0c no date or decimal library (raw `Date`, integer minor
units); 1a 2 (0 true: a domain method named `replace`, a JSX expression); 2a 2 (0 true: a Lua script
in a string, a message template); 2b–2f 0; 3c 3 (0 true: `for (var` inside generated script text);
3d 21 empty-dependency effects; 4a 0; 4b 73, all shipped — form amounts through `parseFloat` and
`Math.round(unitPrice * 100)` conversions; 4d 10; 4e 34 (12 in `scripts/`); 5a 18, among them a
status-to-bucket map ending `default: return 'other'` on an owned enum (a candidate) beside a vendor
message-type switch (§ 36); 5c 0; 6a 19 (`new Date(now - days * DAY_MS)` retention cutoffs, which
are elapsed durations, beside a daily rollup stepping by 24 h from a UTC midnight); 6e 72 (33 in
`scripts/`); 7 0. The first drafts printed 479 money lines (every `cents / 100` display) and 878
fallthrough lines (a lookahead that let `return` through); both shapes are fixed above. Greps 4f,
4g and 6f were added after `quality-mix` measured its reach: on the seven fixtures each prints its
seeded line (a chunk loop that drops the tail, `setTimeout(resolve, retryAfter)`, a monthly renewal
as `timedelta(days=30)`), and nothing else (6f's other match, `30 * DAY_MS` in a spec, is dropped by the exclusion array).
**Re-measured 2026-10-15** on the same monorepo (history re-rooted, about 11,800 files): 0b 13 (core
correctness rules, still no type-aware set); 1a 2; 2a 2; 3c 3; 3d 16; 4b 44 (form drafts through
`parseFloat`, then the project's string-exact `toMinorUnits` — § 92 — or a display); 4d 10; 4e 21 → 10
once `*.test-data.*` builders left the exclusion gap; 4f 0; 4g 0; 5a 18; 6a 19; 6e 45; 6f 3; 7 0. Go, JVM,
C#, Ruby, PHP and Rust greps are not measured: no measured repo has that code.

## The 3,000-hit path

1. **Path class.** `scripts/`, probes and tooling close with **one** cited read showing no deployed entry point runs them.
2. **Group** by (class, callee or identifier): every `Math.round(<x>.price * 100)` is one group; every `default: return` in one status mapper module is one group (`rg --json … | jq -r 'select(.type=="match") | "\(.data.path.text):\(.data.line_number)"'`).
3. **Rank by sink.** Money, persisted data and external contracts first (§4b, §5a on order and payment status, §6 on billing periods and expiries), then request paths, then UI.
4. **Read the top 30 groups** with the read-the-code questions of their §.
5. **Prefer the analyzer as the bulk oracle.** Turn the type-aware rules on in a scratch config (`switch-exhaustiveness-check`, `require-array-sort-compare`, `no-unsafe-enum-comparison`) or run Ruff with `B,DTZ` and Error Prone's correctness checks at error: every diagnostic is a located candidate. For §6, run the suite once under `TZ=Pacific/Kiritimati` and once under `TZ=Etc/GMT+12`: every test that flips is a confirmed site.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

Severity follows the research catalog's correctness ladder: **critical** when money, persisted data
or an external contract is the sink on a common path; **high** for a wrong result or crash on a
reachable path; **medium** on an edge path; **low** when reachable only after a plausible change.
Drop one step for admin-only paths. CWE ids are MITRE's, cited under the CWE Terms of Use.

| § | Class | Research ids | CWE | Default |
|---|---|---|---|---|
| 1 | A result computed and discarded; a call with same-typed arguments swapped or a unit mismatched | CQ-C16 | CWE-252, CWE-683 | high when the dropped value is written or sent; else medium |
| 2 | Equality, boolean and pattern logic | CQ-C09, C10, C21 | CWE-480, CWE-481, CWE-595, CWE-1077, CWE-777 | high on money, dedupe, cache keys and guards; else medium |
| 3 | Shared, aliased or captured state | CQ-C05 (stale closure), C07 (non-business), C11, C20, C24, C25 | CWE-374, CWE-567, CWE-672 | high when state leaks across requests or a stale value is written; else medium |
| 4 | Numbers, bounds and order | CQ-C08, C13, C14, C23 | CWE-193, CWE-1339, CWE-190, CWE-1389, CWE-1025 | critical on money, tax and ledgers; high on quantities, durations and exports; else medium |
| 5 | Non-exhaustive switch, unintended fallthrough, unguarded transition | CQ-C15, C19 | CWE-478, CWE-484, CWE-841 | critical on order, payment and subscription lifecycles; medium on display |
| 6 | Time, zone, locale and text | CQ-C12, C22 | CWE-178, CWE-135 | critical on billing periods, schedules, expiries and legal deadlines; medium on display |
| 7 | A breakpoint or dump-and-die in shipped code | — | — | high on a server path (a request hangs or dies); low behind a debug-only flag |

### 1. A result computed and discarded

```
BAD:   title.trim();  ·  s.replace('-', '_');  ·  start.plus({ days: 1 });   // luxon, date-fns, dayjs return new values
       name.strip() · strings.TrimSpace(s) · amount.setScale(2, HALF_UP); · date.AddDays(1); · params.merge(defaults)
       transfer(toAccount, fromAccount, cents)            // same-typed arguments in the wrong order
GOOD:  title = title.trim();  ·  const next = start.plus({ days: 1 });  ·  amount = amount.setScale(2, RoundingMode.HALF_UP);
```
**Read the code:** Is the receiver immutable (strings, BigDecimal, `java.time`, luxon, dayjs,
Temporal) so the call returns the only copy of the result? Or is it a domain method with side
effects that happens to share the name (an entity's `replace(draft)`)? Who reads the value next —
does the code below use the untrimmed, unrounded or unshifted one? For a swap, which parameter
names do the arguments' names match, and is there a test with **asymmetric** values? **Finding
when** the value the code goes on to use is the one the discarded call was meant to change. **Proof:**
the entry point with an input the call would change (`"  ab "`, `2.005`, a date one day out) gives
the wrong output; for a swap, a test with asymmetric values shows which account moved.

### 2. Equality, boolean and pattern logic

```
BAD:   if (qty == '')  ·  x === NaN  ·  if (status != 'a' || status != 'b')  ·  if (res.status = 429)
       if order.kind == 'gift' or 'promo':  ·  if code is 200:  ·  a == b on Integer / String  ·  price.equals(BigDecimal("2.00"))
       order.refunded_cents = cents   // the guard above checked order.refunded_cents + cents
       /^admin|root$/.test(user)  ·  re.match(r"\d{4}", s)  ·  line.split(".")  ·  const re = /x/g; re.test(a); re.test(b)
GOOD:  ===, Number.isNaN, &&, ==, `in ('gift','promo')`, `==` on ints, .equals / compareTo(...) == 0, `+=`
       /^(?:admin|root)$/  ·  re.fullmatch  ·  split(Pattern.quote("."))  ·  a fresh RegExp per test, or no /g
```
**Read the code:** Re-derive the condition from the requirement as a truth table of its atoms
(k ≤ 4) and compare. What is the identity of the type — value or reference, scale for decimals,
zone for times, normalisation for strings? Does the write after a guard store what the guard tested
(the accumulator, the sum, the merged list)? For a regex, is the intent a full match or a search,
and is it a validator (a one-character prefix or suffix passes) or a substitution, where
`^a|b$` is the intended "either end"? **Finding when** an input row of the truth table, an equal
pair, or a near-miss string gives the wrong branch. **Proof:** the truth-table test over every
combination, the equal-but-not-identical pair (`Integer 1000`, `BigDecimal 2.0 / 2.00`, `-0 / 0`,
NaN), or the positive / negative / near-miss table (`"aX"`, `"Xb"`, `"a\n"`), red before the fix.

### 3. Shared, aliased or captured state

```
BAD:   def add(item, cart=[]):  ·  props.items.sort()  ·  rows = [[0] * n] * m
       for i in range(3): handlers.append(lambda: i)       # every handler sees 2
       useEffect(() => { load(orderId) }, [])              # React; a Vue or Angular watcher with a stale capture is the same bug
       const r = await fetch(u); log(await r.text()); return r.json();   # the body is already used
       var count map[string]int written from two goroutines · a module-level cache mutated per request
GOOD:  cart=None then cart = cart or [] · [...props.items].sort() / toSorted() · lambda i=i: i
       [orderId] in the dependency list, plus an ignore flag or AbortController for the response · r.clone()
       a mutex, sync.Map or a per-request copy; module state that is immutable after start-up
```
**Read the code:** Who owns the object — did the function create it, or receive it from a caller
that still holds it? Is a default or module-level value reused across calls, requests or users? Does
the closure run after its loop or after its props change? For an effect, which values does its body
read, and can a slower earlier response land after a newer one? For a Go `err` result, does an
inner `:=` shadow it and return nil? For threads, which goroutines, workers or requests touch the
value, and is the library object thread-safe? A check-then-act on a balance, stock, quota or token
is security's (§ Boundaries). **Finding when** a second call, a second request, a changed prop or a
second reader sees the wrong value. **Proof:** call twice and assert the second is independent;
freeze the input (`Object.freeze`, `MappingProxyType`, `List.of`) so a mutation throws; invoke every
closure after the loop; resolve two responses in reverse order and assert the latest wins; `go test
-race` over N goroutines (the race report is the failure).

### 4. Numbers, bounds and order

```
BAD:   const cents = Math.round(parseFloat(amount) * 100)   // "1.005" → 100, not 101
       total.toFixed(2) round-tripped through parseFloat · amount: float(row["amount"]) · double price · new BigDecimal(0.1)
       parseInt(qty) · Number(req.query.limit) → NaN or 0 for "" · int32(n) from int64 · days * 24 * 3600 * 1000 in int
       ids.sort() → [1, 10, 9] · sort((a, b) => a > b) · const offset = page * pageSize   // pages are 1-based
       xs.reduce((a, b) => a + b) on [] · Math.max(...xs) on [] → -Infinity · for (i = 0; i <= xs.length; i++)
GOOD:  integer minor units end to end, or a decimal type with an explicit rounding mode and rounding point
       Number.parseInt(s, 10) with a range check · Math.multiplyExact / checked_* · (a, b) => a - b · (page - 1) * pageSize
       xs.reduce((a, b) => a + b, 0) · an explicit empty-list branch
```
**Read the code:** What is the representation — minor-unit integers, a decimal type, or binary
floats? Where is the rounding mode and the rounding point (per line or per total) stated, and how
many minor units does each currency have (JPY 0, KWD 3)? When the business pack is installed, read
the declared money policy from its `pricing-rule-scan` §1 row (`money-policy.md`: mode, point and
exponent per amount kind) and grade against it; a policy row `UNDECLARED` makes the money row here
`[report-flagged]` with the missing declaration named, since which mode is right is a business rule.
Without the business pack, the stated mode in code or docs is the only oracle. What is the widest realistic value (ms
timestamps, ids above 2^53, files above 2 GiB) against the declared type? What does the parse do with
`""`, `" 1 "`, `"1e3"`, `"08"`, `"12abc"`, `"١٢"`? Is the page index 0- or 1-based on both sides?
Can the list be empty? For a 4b `parseFloat(form value)`: is the float handed **straight** to a
converter that works on the decimal the number prints as (`String(x)` digits scaled with integers,
`Decimal(str(x))`, `BigDecimal.valueOf(double)`)? A typed decimal of ≤ 15 significant digits
round-trips exactly through a double and its shortest print, so that path is § 92, not a finding —
unless arithmetic touches the float first (`parseFloat(a) * qty`, a sum) or the converter multiplies
(`Math.round(x * 100)`). **Finding when** a value from the partitions gives a wrong number, a silent
wrap, an accepted junk string, a dropped or duplicated row, or a crash. **Proof:** the exact-decimal
table (`1.005`, `0.125`, ties `2.5` and `-2.5` under the stated mode, `allocate(100.00, 3)` sums to
`100.00`), the per-type boundary table (MAX, MAX+1, MIN, `2^53+1`), the size table (0, 1, k−1, k, k+1)
with the property `concat(chunks(xs, k)) == xs`, and the adversarial sort array `[10, 9, 1, 100]` with
ties.

### 5. Non-exhaustive switch, fallthrough, unguarded transition

```
BAD:   switch (order.status) { case 'paid': return 'Paid'; …  default: return 'Paid'; }   // PARTIALLY_REFUNDED lands here
       case 'cancel': refund(o);   // no break
       case 'close':  archive(o);
       order.status = 'shipped' written from four services with no check of the current status
GOOD:  default: return assertNever(order.status)  ·  a `satisfies Record<Status, …>` map  ·  match + assert_never
       one transition table, and `UPDATE … SET status = 'shipped' WHERE id = $1 AND status = 'paid'` with the row count checked
```
**Read the code:** Is the switched value an **owned** domain enum (order, payment, subscription
status), or an open set the code does not own — HTTP statuses, a vendor's message types (§ 36)? Does
the `default` throw, return a sentinel the caller handles, or answer as if it were a known case? For
fallthrough, is there a `// falls through` comment or grouped empty labels? For transitions, is
there one place that defines the allowed moves, and can a terminal state be left? An illegal
transition that skips a paid or approved step is security's `logic-race-scan` § 3 (§ Boundaries).
**Finding when** a member added to the enum, or a state reached out of order, takes a silent path.
**Proof:** a test that iterates every enum member (`Object.values(Status)`, `Status.values()`) and
fails if one reaches the default; the (state × event) matrix where each pair is an allowed next state
or a typed `IllegalTransition`; each case label run in isolation with a spy on the next case.

### 6. Time, zone, locale and text

```
BAD:   new Date('2026-03-29')  → UTC midnight, the 28th in New York  ·  new Date(2026, 3, 1) is 1 April
       new Date(start.getTime() + days * 86_400_000)   // a calendar day across a DST change is 23 or 25 hours
       DateTimeFormatter.ofPattern("YYYY-MM-dd")   // week-based year: 2025-12-29 prints 2026-12-29
       datetime.utcnow() · LocalDateTime.now() · DateTime.Now · Time.now · "TITLE".toLowerCase() under tr-TR (JVM) → "tıtle"
       name.slice(0, 20)   // cuts a surrogate pair: "👍" becomes a lone surrogate, then invalid UTF-8
GOOD:  a date-only type (Temporal.PlainDate, LocalDate, date) for dates; an injected clock; zone-aware add (plus({ days: 1 })
       in the business zone); `yyyy`; datetime.now(UTC) · Locale.ROOT for protocol text · Intl.Segmenter or a byte-limit check
```
**Read the code:** Is the value a date, an instant or a wall-clock time in a zone? For a `YYYY` token in a JS formatter, read the library's token table before reporting: it is not the week-based year in every library. Which zone owns
the business rule — the user's, the merchant's, the legal entity's? Is "now" taken directly or from
an injected clock? Is a day an elapsed duration (a TTL, a retention cutoff — fine) or a calendar step
(tomorrow, the billing day — breaks on DST)? Is the text a protocol token, a log line, or something a
user typed and another system stores with a limit counted in bytes, code points or graphemes?
Temporal ships in Node 26, Chrome / Edge 144 and Firefox 139, not Safari (§ 79): a browser fix needs
the polyfill. **Finding when** a zone, a date or a locale from the partitions gives a wrong day, a
wrong period or corrupt text. **Proof:** the suite or the test under `TZ=Pacific/Kiritimati`,
`TZ=Etc/GMT+12` and `TZ=Asia/Kathmandu`; the US gap 2026-03-08 02:30 and overlap 2026-11-01 01:30
(America/New_York), the EU gap 2026-03-29 and overlap 2026-10-25 (Europe/Berlin), 2028-02-29 + 1
year, Jan 31 + 1 month, 2025-12-29 for `YYYY`; `LANG=tr_TR.UTF-8` or `-Duser.language=tr`; `"👍"`,
`"👨‍👩‍👧‍👦"`, NFC vs NFD `"é"` at the length limit.

### 7. A breakpoint or dump-and-die in shipped code

```
BAD:   debugger;  ·  breakpoint()  ·  import pdb; pdb.set_trace()  ·  binding.pry  ·  dd($order)  ·  dbg!(total)
GOOD:  removed; a structured log line at debug level if the value is worth keeping
```
**Read the code:** Does the file ship (the build includes it, the route or job imports it), and
does the statement run in production, or only behind a debug-only flag the build strips? A
`debugger` statement is inert without an attached inspector, but `breakpoint()`, `pdb` and a Rails
`binding.pry` block a worker on a TTY prompt, and Laravel `dd()` ends the response. **Finding when** a shipped path
executes it. **Proof:** a static fact — the line, the import chain to an entry point, and the lint
rule (`no-debugger`, `T100`, `Lint/Debugger`, `dbg_macro`) firing at that line.

## Proof

The oracles and variants are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md)
§ Code quality — *Boundary value vector* and variant **V83** (logic, equality, number and time
traps), with the time partitions above. The fix uses the project's own primitive — the money type,
the clock, the date library, the enum helper — and is **failing-first**: it changes behaviour on
purpose, so a characterization test that pins the old output is the wrong harness. The verifier
re-derives every expected value from a spec, a doc or a sibling and runs a negative control where
the behaviour is correct (`precedents/code-quality.md § 50`).

## Output

```
correctness-smell-scan — lanes: ts (eslint 10.10; typescript-eslint 8.69 recommended, no type-aware rules); python, go, jvm, c#, ruby, php, rust absent
Context: node >= 22 · no date or decimal library · TZ not pinned in the image

Findings: 2 · Unconfirmed: 1

1. src/billing/statement-rows.ts:58                                      [report-with-fix]   critical
   §4 float money — `unitPriceCents: Math.round(r.unitPrice * 100)`; unitPrice arrives as a JS number
   from the numeric column. Input: unitPrice "1.005" → 100 cents; the invoice spec (docs/billing.md)
   says half-up to 101. Proof: test/billing/unit-price.vectors.spec.ts (fails). Fix: read the column
   as a string and convert with the shared toMinorUnits(decimal, currency). CWE-1339

2. src/reports/status-buckets.ts:31                                      [report-with-fix]   high
   §5 non-exhaustive switch — `default: return 'other'` in toBucket(status) over the owned OrderStatus
   enum; `on_hold`, added after the mapper, is counted as 'other' on the payout dashboard. Proof: a test over
   Object.values(OrderStatus) fails on on_hold. Fix: assertNever in the default and an explicit arm. CWE-478

3. src/jobs/usage-rollup.ts:44                                           [report-flagged]    medium
   §6 calendar day by 24 h — `new Date(day.getTime() + DAY_MS)`. Unproven link: whether `day` is
   always a UTC midnight (startOfUtcDay at :43 says yes) or a tenant-local one. Settling test: the
   rollup for 2026-03-29 under TZ=Europe/Berlin returns 24 hourly buckets.

Verification: 41 candidates → 2 findings · 1 unconfirmed · 31 hardening · 0 pre-existing · 7 refuted

Class coverage:
  §1  discarded result            checked (2 hits → 0 findings; a domain method named replace)
  §2  equality / logic / regex    checked (2 hits → 0) · partial (no eqeqeq, no type-aware lane)
  §3  shared / captured state     checked (24 hits / 4 groups → 0; 21 empty-deps effects read)
  §4  numbers / bounds / order    checked (117 hits / 9 groups → 1 finding) · Live, unreviewed (3 groups / 18 hits — continue with grep 4b on web/src/features/merchants)
  §5  switch / transitions        checked (18 hits → 1 finding; 6 open vendor sets, § 36)
  §6  time / locale / text        checked (91 hits → 1 unconfirmed; 33 in scripts/, closed with one read)
  §7  breakpoints                 checked (0 hits; no-debugger not configured)
```

`[report-with-fix]`: the input, the wrong output and the sourced expectation are named, the test
failed, and the fix uses the project's primitive. `[report-flagged]`: one link is unproven — the
type of a value, the zone a date is in, a caller not read, no harness — named with the settling
test. The coverage block lists **all seven** classes on every run: `checked (k hits → m findings)`
only when the grep or the analyzer ran on a present lane; `N/A (<reason>)` only when the repo has no
such surface; `blocked (<reason>)` when a grep or the analyzer failed. A partial review reads
`Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/code-quality.md`](../../../../snippets/precedents/code-quality.md)
(logic, equality, numbers and time are § 33–46; version precedents § 71–83; proof § 49–50) and
[`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10. The ones this
skill meets most:

- **`x == null` in JavaScript** with `eqeqeq` at `{ null: "ignore" }` (§ 33); **identity where identity is the semantics** — Java enums, `is None` (§ 34); **float compare of small exact integers** and measurements with a tolerance (§ 35).
- **A `default` over an open set** the code does not own (§ 36); a `default` that throws, or `assertNever`, is the control (§ 28).
- **Mutating a locally created array**, an Immer draft or a builder (§ 37); **`.sort()` on ISO dates or hex ids**, where code-unit order is intended (§ 38).
- **Go `if err := f(); err != nil { return err }`** (§ 39); **Go ≥ 1.22 loop variables** — a `go.mod` `go` directive at 1.22 or later makes loop-capture findings obsolete (§ 71).
- **Constant conditions from build flags**, `NODE_ENV` or `DEBUG` (§ 40); **integer wrap in hashing or PRNG code** (§ 41).
- **Locale-default formatting in UI** meant to follow the user (§ 42) — never in protocols, cache keys, file names or comparisons; **a documented inclusive or exclusive range** (§ 43); **`time.Time ==` after `.UTC().Round(0)`** (§ 44); **a naive "now" in a system documented UTC-everywhere** stays Low (§ 45).
- **Elapsed durations are not calendar days** (§ 84). A TTL or retention cutoff `now - days * DAY_MS` is correct; only stepping to "the same wall-clock time tomorrow" breaks on DST.
- **Integer minor units shown with `/ 100`** for display are correct (§ 85); the bug is a float converted *into* minor units, or a fixed 100 for a currency whose exponent is not 2.

## When to run

- On any diff that adds or changes arithmetic on money or quantities, a parse of a number or a date, a `switch` or `match` on a status, kind or type, a comparator, a date or time computation, a closure in a loop, an effect's dependency list, a default argument, or a string truncation — the `/review-changes` and `/quality-audit` dispatch signal.
- On every whole-repo `/quality-audit`, reporting all seven classes.
- When a production bug is "off by one day", "off by a cent", "wrong order", "counted as other", or appears only for some users' zones or locales.

## Halt conditions

- Do not report a high or critical row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/quality-audit` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the line `<file:line>`, the concrete input, the wrong output, the sourced expectation, the entry point and the fix.
- Do not report a grep or analyzer hit as a finding, and do not dismiss a group without reading what the value is and where it comes from.
- Do not propose a suppression, a wider type, a special case for the reported input, or a tolerance on money as the fix.
- Do not change a rounding mode, a business time zone, a public enum or a stored format without asking: those are product decisions (`proof-oracles.md` § Code quality, *The fix loop*).
- Do not print "no logic bugs" without the class-coverage block. A class whose grep or analyzer did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `/quality-audit` dispatches this skill and folds its coverage block into the class ledger; `/quality-fix` closes the findings failing-first and re-runs this detector on the patched line.
- `error-handling-scan`, `type-safety-scan`, `dead-code-scan`, `duplication-scan` and `suppression-scan` (this pack) own the neighbouring classes; a suppressed rule from the lane table above is `suppression-scan` § 2.
- Security `logic-race-scan`, `injection-scan` and `sast-scan`; database `transaction-scan` and `schema-integrity-scan`; frontend `client-data-scan` (§3, §4, judged by `@data-flow-auditor`) and `routing-scan` (§8); testing `flake-source-scan` — these own the routed classes when their packs are installed (§ Boundaries).

Rule ids, tool versions and the CQ-C class ids come from the code-quality research catalog for this pack (2026-10-05).
