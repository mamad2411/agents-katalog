---
name: mutation-probe
description: "Measure test strength on changed lines: run the repo's mutation tool with current flags (or seed one mutant by hand), surface surviving mutants, dismiss equivalents by a five-check procedure, and emit the mutant-kill evidence row a fix consumes."
kind: skill
pack: testing
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: mutation-probe

## Premise

Coverage says a line ran; a mutant says whether any test would notice it breaking. Corrupt the
logic (`>` → `>=`, `&&` → `||`, `return total` → `return 0`) and run the tests that execute the
line: a mutant that **survives** is a regression the suite would ship green. Mutants couple to real
faults — 73% of 357 real faults were coupled to mutants in Just et al. (FSE 2014) — which is why
this is the oracle every assertion-strength finding settles on.

It is a **harness**, not a detector: it runs on a scope someone hands it (a diff, a file, a line, a
fix) and returns measured survivors. It is expensive (suite time × mutants), so it runs **only on
changed or named lines**, never repo-wide in PR CI. Google's practice — diff-scoped, at most one
surfaced mutant per changed line, after skipping "arid" lines such as logging — is the shape
followed here (Petrović & Ivanković, ICSE-SEIP 2018).

Ownership: **`coverage-gap` finds lines never EXECUTED; this skill finds lines executed but never
ASSERTED.** A mutant on a line no test runs (`NoCoverage`, `NOT COVERED`, `no tests`, PIT
`NO_COVERAGE`) is handed back to `coverage-gap` § 1, never reported here.

**Every survivor cites `<file:line>` + the tool's mutant (operator, original → mutated) + the tests
that ran it + why they missed it + the assertion that would kill it.** "Weak tests here" is not a
finding. A score is never printed without its formula and its denominator (§ Output).

## The rule

A surviving mutant is a finding when all four hold:

1. **It is on a scoped, executed line.** The line is in the change (or the named scope) and the tool reports tests ran it. Unexecuted → `coverage-gap`.
2. **It is not arid.** Logging, metrics, tracing, `toString` / `__repr__`, DI wiring and generated code are skipped, unless the log line is an audit or security contract.
3. **It is not equivalent.** The five checks in § Equivalent mutants found an input that tells original and mutant apart — or never ran, in which case it is **Unconfirmed**, not dismissed.
4. **It survived a real run.** The tool (or the manual-seed lane) executed it, and its status is a survivor — not `CompileError`, `RuntimeError`, `Unviable`, `NON_VIABLE`, `caught by type check`, or `Timeout` (a timeout counts as killed; spot-check it on a slow suite).

## Boundaries

- **Unexecuted lines, files missing from coverage** → `coverage-gap` (this pack).
- **Which tests are weak, read from the code** → `assertion-strength-scan` (this pack); it hands this skill its candidate lines, and this skill measures them.
- **Writing the killing test** → `@test-engineer` / `/add-test`; **closing an audit finding** → `/test-fix`, which consumes this skill's evidence row.
- **A gate weakened in the change** (a mutation threshold lowered, a `Stryker disable` / `# pragma: no mutate` / `@DoNotMutate` / `mutants::skip` added) → `.claude/scripts/test-integrity.py` when the repo-baseline is installed; without it, list the hint as a candidate here and re-run with it removed.

## Adapt to the codebase — the lane table (flags verified 2026-10-05)

Detect the tool from config and dependencies (grep 0); never impose one. **Run** = executed on a
sample this pass; **Docs** = read from the tool's current documentation or `--help` this pass.

| Stack | Tool (version) | Diff-scoped run | Survivor in the report | Trap | Check |
|---|---|---|---|---|---|
| JS / TS | StrykerJS `@stryker-mutator/core` 10.0.0 (Node ≥ 22) + a runner plugin | `npx --no stryker run --mutate "<file:start-end,…>" --reporters clear-text,json` (`--checkers typescript` with the TS checker) | `reports/mutation/mutation.json` → `status: "Survived"` | **No `--since`** — `stryker run --since` exits `error: unknown option '--since'`; `--incremental` diffs against its own last report (`reports/stryker-incremental.json`), not git. Never a bare `npx stryker` without the local install: it fetches the abandoned `stryker` 0.x package (`npx --no` refuses instead) | Run |
| .NET | Stryker.NET 5.0.0 | `dotnet stryker --since:<committish> -r json -r html` | the JSON report under `StrykerOutput/` → `Survived` | `--since` is file-granular, default target `master`; `-m "File.cs{10..100}"` is a **character** span, not lines | Docs |
| Python | mutmut 3.8.0 | `[tool.mutmut] source_paths = ["src/pkg"]`, then `mutmut run "<mutant-name globs>"` (grep 3) | `mutmut results` → `survived`; `mutmut show <name>` | **`--paths-to-mutate` is gone** (`Error: No such option`); mutates only inside functions; POSIX only; `mutate_only_covered_lines` also skips `# pragma: no cover` lines | Run |
| Python | cosmic-ray 8.7.0 | `cosmic-ray init cr.toml s.sqlite && cr-filter-git --config cr.toml s.sqlite && cosmic-ray exec cr.toml s.sqlite && cr-report s.sqlite` | `cr-report` | the git filter's branch defaults to `master` — set it in `cr.toml` | Docs + `--help` |
| JVM | PIT `pitest-maven` 1.30.0 + `pitest-junit5-plugin` 1.2.3 | `mvn test-compile org.pitest:pitest-maven:mutationCoverage -DtargetClasses='<changed FQCN>*' -Dmutators=STRONGER -DoutputFormats=XML,HTML -DtimestampedReports=false` | `target/pit-reports/mutations.xml` → `status='SURVIVED'` (filter to changed lines: grep 3) | **`scmMutationCoverage` was removed in 1.18.0** (`Could not find goal 'scmMutationCoverage'`); line-level git scoping is Arcmutate `+GIT` (commercial) | Run |
| Go | gremlins v0.6.0 | `gremlins unleash --diff <base> --output g.json -S lc` | `LIVED` (`NOT COVERED` → coverage-gap) | **the flag is `--diff`** (`--diff-ref`: `unknown flag`); `--threshold-efficacy 80` at 50% efficacy still exited 0 — gate on `test_efficacy` in the JSON, not the exit code | Run |
| Go | go-mutesting (avito-tech) v2.3.1 | `go-mutesting ./<changed package>/...` | a **`FAIL`** block with the patch = **survived**; `PASS` = killed | no diff mode; `go install …@v2.3.1` fails (module path lacks `/v2`) — build from the tag | Run |
| Rust | cargo-mutants 27.1.0 | `git diff --src-prefix=a/ --dst-prefix=b/ <base>.. > git.diff && cargo mutants --in-diff git.diff` | `mutants.out/missed.txt`; `outcomes.json` `summary: "MissedMutant"`; exit 2 = missed | there is **no `caught` field** — summaries are `Success`, `CaughtMutant`, `MissedMutant`, `Timeout`, `Unviable`, `Failure` | Run |
| PHP | Infection 0.35.6 | `infection --git-diff-lines --git-diff-base=<base> --min-covered-msi=100 --show-mutations=max --threads=max` | escaped mutants | the diff base defaults to `master`; uncovered code is not mutated unless `--with-uncovered`; timeouts count as killed unless `--with-timeouts` | Docs |
| Ruby | mutant 0.16.2 | `bundle exec mutant run --use rspec --usage opensource --since <base> -- 'App*'` | alive mutations | **commercial licence for private code** (`--usage opensource` is for public repositories only) → `blocked (licence)` unless the repo holds one | Docs |
| C / C++ | mull 0.34.1 | `mull.yml`: `gitDiffRef: <base>`, `gitProjectRoot: .` | survived mutants | needs the clang plugin build | research notes, not run |

Statuses that are **not** survivors in any lane: `NoCoverage` / `NOT COVERED` / `no tests` /
`NO_COVERAGE` (→ coverage-gap), and compile- or type-killed mutants. Each lane scores differently —
state the formula: StrykerJS `(Killed + Timeout) / (Killed + Timeout + Survived + NoCoverage)`; PIT
mutation score `killed / all` vs test strength `killed / (killed + survived)`; gremlins efficacy
`killed / (killed + lived)`; Infection MSI vs covered-code MSI.

## Pre-flight — the scope

Run as **one** script with bash from the repo root. Every `rg` names its path (`.`). `SCOPE=<paths>`
names files or directories to mutate whole (a whole-repo audit's signal list, a fix's module); unset,
the scope is the diff against the merge base. With neither — no merge base (a single-commit repo, a
shallow clone, an unfetched `origin/main`) and no `SCOPE` — the block prints `blocked (no merge-base)`
and an empty scope; it never widens itself to the whole repo.

```bash
BASE=$(git merge-base HEAD "${BASE_REF:-origin/main}" 2>/dev/null); W=$(mktemp -d "${TMPDIR:-/tmp}/mutation-probe.XXXXXX"); : > "$W/ranges.all"; : > "$W/lines.all"
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/mutants/**'
   -g '!**/{test,tests,__tests__,spec,e2e,testdata,fixtures,__fixtures__,mocks,__mocks__,migrations,generated,__generated__,scripts}/**'
   -g '!**/*.{spec,test,e2e-spec,stories,d}.*' -g '!**/{test_*,*_test,conftest}.*' -g '!**/*{Test,Tests,IT}.{java,kt,cs,php}' -g '!**/*_spec.rb'
   -g '!**/*.{md,mdx,json,yml,yaml,toml,lock,snap,sql,map,svg,css,html}' -g '!ai/**' -g '!docs/**' -g '!**/{locales,i18n}/**')
# 0. Lanes: mutation configs (0a) and declared tools (0b). Detect; never impose a tool the repo does not have.
echo '== 0'; rg --files -g '**/{stryker.conf.*,stryker.config.*,.stryker.conf.*,stryker-config.json,gremlins.y*ml,.gremlins.y*ml,infection.json5,infection.json,.mutant.yml,mull.yml,mutants.toml}' -g '!**/node_modules/**' .
rg -n --pcre2 '"@stryker-mutator/[\w-]+"|\bdotnet-stryker\b|\[(?:tool\.)?mutmut\]|\bmutmut\b|\bcosmic-ray\b|\bpitest\b|infection/infection|\bmutant-rspec\b|go-gremlins|go-mutesting|cargo-mutants' -g '**/{package.json,pyproject.toml,setup.cfg,requirements*.txt,pom.xml,build.gradle*,*.csproj,dotnet-tools.json,composer.json,Gemfile,go.mod,Makefile}' -g '!**/node_modules/**' .
# 1. Changed source lines ("path:line") and hunk ranges ("path:start-end", StrykerJS's --mutate syntax), with coverage-gap's
#    parser: deletion-only hunks, deleted files, spaces in names and diff.noprefix are all handled. SCOPE set: every line of
#    the named files instead. No base and no SCOPE: blocked, empty scope.
if [ -n "${SCOPE:-}" ]; then echo "scope: whole files under SCOPE=$SCOPE (base ${BASE:-none})"; read -ra ROOTS <<< "$SCOPE"
  rg --files "${X[@]}" "${ROOTS[@]}" | sed 's|^\./||' | while IFS= read -r f; do n=$(wc -l < "$f" | tr -d ' '); [ "$n" -gt 0 ] || continue
    echo "$f:1-$n" >> "$W/ranges.all"; awk -v f="$f" '{ print f ":" NR }' "$f" >> "$W/lines.all"; done
elif [ -z "$BASE" ]; then echo "scope: blocked (no merge-base with ${BASE_REF:-origin/main}: single-commit repo, shallow clone or unfetched ref) — set BASE_REF, or SCOPE=<paths> for a whole-file scope"
else git -c core.quotePath=false diff -U0 --no-color --no-ext-diff --src-prefix=a/ --dst-prefix=b/ "$BASE"...HEAD | awk '
/^\+\+\+ / { f = ($0 == "+++ /dev/null") ? "" : substr($0, 7); sub(/\t$/, "", f); next }
/^@@ / { if (f == "") next; match($0, /\+[0-9]+(,[0-9]+)?/); s = substr($0, RSTART + 1, RLENGTH - 1)
         n = split(s, a, ","); st = a[1] + 0; c = (n == 2) ? a[2] + 0 : 1; if (c == 0) next
         print f ":" st "-" (st + c - 1) > R; for (i = 0; i < c; i++) print f ":" (st + i) }' R="$W/ranges.all" > "$W/lines.all"; fi
rg --files "${X[@]}" . | sed 's|^\./||' | sort > "$W/src"
awk -F: 'NR == FNR { s[$0]; next } ($1 in s)' "$W/src" "$W/lines.all" > "$W/lines"; awk -F: 'NR == FNR { s[$0]; next } ($1 in s)' "$W/src" "$W/ranges.all" > "$W/ranges"
echo '== 1'; printf 'changed source files %s · lines %s · hunks %s\n' "$(cut -d: -f1 "$W/lines" | sort -u | wc -l)" "$(wc -l < "$W/lines")" "$(wc -l < "$W/ranges")"
# 2. Arid lines — blank, braces, comments, imports, logging / metrics / tracing — are never surfaced unless the log is an
#    audit contract. The rest ($W/mutable) is the scope; at most one survivor per line is surfaced.
python3 - "$W/lines" > "$W/mutable" <<'PY'
import re, sys
A = re.compile(r'^\s*(?:$|[})\]];?\s*$|//|#|/\*|\*|(?:import|from|package|using|require)\b|@\w+\s*$|(?:this\.|self\.)?(?:log|logger|console|LOG|Log|slog|tracer|span|metrics?|statsd)\s*[.:]|logging\.\w+\(|print\(|fmt\.Print|println!)')
cache, arid = {}, 0
for it in open(sys.argv[1]).read().split('\n'):
    if not it: continue
    p, n = it.rsplit(':', 1); src = cache.setdefault(p, open(p, errors='ignore').read().split('\n'))
    if A.match(src[int(n) - 1] if int(n) <= len(src) else ''): arid += 1
    else: print(it)
print(f'arid lines skipped: {arid}', file=sys.stderr)
PY
echo '== 2'; wc -l < "$W/mutable"; echo "scope: $W/lines $W/ranges $W/mutable"
```

**Run the lane** (same shell, after the block above; one lane per stack present). On a `SCOPE` run
there is no diff: StrykerJS, mutmut and PIT take the whole-file scope as built; gremlins takes the
package directory instead of `--diff`, cargo-mutants `--file <path>` instead of `--in-diff`:

```bash
# StrykerJS — hunk ranges as --mutate (a range entry cannot be mixed with a glob in the same entry)
npx --no stryker --version >/dev/null 2>&1 || echo "NOT-RUN (StrykerJS not installed — to enable: npm i -D @stryker-mutator/core @stryker-mutator/vitest-runner)"
npx --no stryker run --mutate "$(awk -F: '$1 ~ /\.(c|m)?[jt]sx?$/' "$W/ranges" | paste -sd, -)" --reporters clear-text,json
jq -r '.files|to_entries[]|.key as $f|.value.mutants[]|select(.status=="Survived" or .status=="NoCoverage")|"\(.status) \($f):\(.location.start.line) \(.mutatorName) -> \(.replacement)"' reports/mutation/mutation.json
# mutmut 3 — changed lines → mutant-name globs: functions `mod.x_fn__mutmut_*`, methods `mod.xǁClassǁfn__mutmut_*`
mutmut run $(python3 -c '
import ast, sys, collections
want = collections.defaultdict(set)
for it in open(sys.argv[1]).read().split():
    p, n = it.rsplit(":", 1); want[p].add(int(n))
for p, lines in want.items():
    if not p.endswith(".py"): continue
    mod = p[:-3].split("src/", 1)[-1].replace("/", ".").removesuffix(".__init__")
    def walk(body, cls=None):
        for d in body:
            if isinstance(d, ast.ClassDef): walk(d.body, d.name)
            elif isinstance(d, (ast.FunctionDef, ast.AsyncFunctionDef)) and lines & set(range(d.lineno, d.end_lineno + 1)):
                print(f"{mod}.xǁ{cls}ǁ{d.name}__mutmut_*" if cls else f"{mod}.x_{d.name}__mutmut_*")
    walk(ast.parse(open(p).read()).body)' "$W/mutable") && mutmut results
# PIT — changed classes (inner classes via the trailing *), then survivors on changed lines only
mvn test-compile org.pitest:pitest-maven:mutationCoverage -DtargetClasses="$(awk -F: '$1 ~ /src\/main\/(java|kotlin)\/.*\.(java|kt)$/ { c = $1; sub(/.*src\/main\/(java|kotlin)\//, "", c); sub(/\.(java|kt)$/, "", c); gsub("/", ".", c); print c "*" }' "$W/lines" | sort -u | paste -sd, -)" -Dmutators=STRONGER -DoutputFormats=XML,HTML -DtimestampedReports=false
python3 -c '
import sys, xml.etree.ElementTree as ET
ch = {tuple(l.rsplit(":", 1)) for l in open(sys.argv[2]).read().split()}
for m in ET.parse(sys.argv[1]).getroot():
    f = m.findtext("mutatedClass").rsplit(".", 1)[0].replace(".", "/") + "/" + m.findtext("sourceFile"); n = m.findtext("lineNumber")
    if m.get("status") in ("SURVIVED", "NO_COVERAGE") and any(p.endswith(f) and l == n for p, l in ch):
        print(m.get("status"), f"{f}:{n}", m.findtext("mutator").rsplit(".", 1)[-1], "-", m.findtext("description"))' target/pit-reports/mutations.xml "$W/lines"
# gremlins
gremlins unleash --diff "$BASE" --output "$W/g.json" -S lc && jq -r '.files[]|.file_name as $f|.mutations[]|select(.status=="LIVED" or .status=="NOT COVERED")|"\(.status) \($f):\(.line) \(.type)"' "$W/g.json"
# cargo-mutants (exit 2 = missed mutants)
git diff --src-prefix=a/ --dst-prefix=b/ "$BASE".. > "$W/git.diff" && cargo mutants --in-diff "$W/git.diff"; cat mutants.out/missed.txt
```

**Measured** (2026-10-05). Each Run lane above was executed on a one-function sample (`discount(total, threshold)` with an `if (total > threshold)` branch and one test at 200 / 100): StrykerJS 10.0.0 surfaced `EqualityOperator` (`>=`) and `ConditionalExpression` (`true`) as Survived in about 2.5 s; mutmut 3.8.0 left `x_discount__mutmut_1` (`>=`) and `_3` survived; PIT 1.30.0 left `ConditionalsBoundaryMutator` and `RemoveConditionalMutator_ORDER_IF` SURVIVED on line 4; gremlins reported `LIVED CONDITIONALS_BOUNDARY at pricing.go:4:11` and `NOT COVERED` for an untested function; go-mutesting printed `FAIL` with the `return 0 → return 1` patch; cargo-mutants printed `MISSED src/lib.rs:2:14: replace > with >= in discount` and exited 2. On a real NestJS-on-Fastify monorepo (read-only) the scope block runs in 0.4 s: 30 commits → 105 changed source files, 3,565 lines, 363 hunks, 1,249 arid lines skipped, **2,316** mutable lines. The repo declares no mutation tool (grep 0 empty), so its lane is StrykerJS installed in a scratch worktree, or the manual-seed lane. On `benchmarks/fixtures/*` (one commit, no remote) 2.0.0 printed `awk: can't open file …/ranges.all`; the block now prints `scope: blocked (no merge-base …)` and an empty scope, and on `brittle-suite` `SCOPE="api/src/shipping jvm/src/main"` scopes 6 files, 127 lines, 69 mutable.

## The 3,000-hit path

1. **Coverage first.** Hand every unexecuted mutant to `coverage-gap`; only executed lines are mutated (mutmut `mutate_only_covered_lines`, Infection's default, StrykerJS `coverageAnalysis: perTest`).
2. **One survivor per line.** Surface at most one per changed line, in this order: relational / boundary, logical connector, return value, statement deletion. Keep the rest as siblings for the fix.
3. **Rank by risk.** Money, auth, tenant, quota and limit lines first, then write paths, then reads.
4. **Read the top 30** with the equivalence checks and the "why missed" questions.
5. **Bulk oracle.** One tool run over the whole scope beats per-line seeding; seed by hand only where no lane runs.
6. **Ledger the rest** as `Live, unreviewed (k lines / n mutants)` with the continuing command — for StrykerJS, the same `--mutate` with the remaining ranges.

## Scans for

| § | Class | Standard | Default |
|---|---|---|---|
| 1 | Surviving mutant on a changed, executed line (MC-1) | QG-14 | high on money / auth / tenant / limits; medium on business logic; low on formatting |
| 2 | Boundary not pinned — relational mutant survives (MC-8) | QG-14 | high on money / quota / limits / dates |
| 3 | Error path executed but unasserted — the `catch` body removed, the error return replaced, and nothing fails (MC-9) | QG-14 | high on payment / auth / data writes |
| 4 | Pseudo-tested method — body emptied or constant-returned and nothing fails (MC-2) | QG-14 | high if it writes state, sends or charges |
| 5 | Executed but unchecked — a line covered by several tests whose every mutant survives (MC-10) | QG-15 | medium; high on changed money / auth logic |

**§ 1 – § 3 read the code:** which test ran the mutant (StrykerJS `coveredBy`, PIT `succeedingTests`, mutmut `tests-for-mutant`)? What does it assert — a value the mutation changes, or something coincidental (a mock call, existence, a status with no body)? Is the boundary value itself in any test input (`rg -F '<literal>'` over the tests)? **§ 4:** PIT + Descartes (LGPL-3.0) reports `pseudo-tested` methods; elsewhere use the tool's statement-deletion / return-value operators on the method's lines. **§ 5:** StrykerJS `mutation.json` `coveredBy` vs `killedBy`, or PIT test strength. **Finding when** the mutant is executed, non-arid, non-equivalent and survived. **Proof:** the mutant-kill evidence row (§ Evidence row). **Fix:** the assertion that kills it, named per survivor.

## Manual-seed lane (no tool, a `blocked (licence)` tool, or a single line)

One operator per branch, one line at a time, restore proven. The file must be clean before seeding
(otherwise seed in `git worktree add "$W/seed" HEAD`):

```bash
f=src/pricing.ts; L=42; T='npx --no vitest run src/pricing.spec.ts'      # T = the tests that execute line L (coverage-gap, per-test coverage)
git diff --quiet -- "$f" || echo "uncommitted edits in $f: seed in a scratch worktree instead"
cp "$f" "$W/seed.orig"; sed -i.bak "${L}s/ > / >= /" "$f" && rm -f "$f.bak"
git diff --numstat -- "$f"                                          # must read `1 1 <f>` — exactly one line mutated
$T; echo "exit=$? (0 = SURVIVED)"
cp "$W/seed.orig" "$f"; git diff --exit-code -- "$f" && echo restored
```

Operators, one per branch: relational boundary (`>` ↔ `>=`), negated condition, condition forced
`true` / `false`, `&&` ↔ `||`, ±1, return a **wrong value of the right type** (never a `throw`, which
fails even an existence-only test), statement or block removal. Label the row `manual-seed`, not
`harness-measured`. Measured on the JS sample: `>` → `>=` on line 2 left the test green (exit 0),
and `git diff --exit-code` returned 0 after the restore.

## Equivalent mutants — the five checks

A survivor is dismissed as **equivalent** only when all five find no observable difference
(paraphrased from Trail of Bits' `mutation-testing` skill, CC BY-SA 4.0,
<https://github.com/trailofbits/skills>; ideas only):

1. **Type context.** Can the mutated expression produce a different value for this type at all? `balance > 0` → `balance != 0` on an unsigned integer cannot.
2. **Reachability.** Can any input reach the line in the state where original and mutant differ? An upstream guard can make the boundary case unreachable.
3. **Downstream consumption.** Is the changed value consumed by an observable output — a return, a state write, I/O, an exception — or only logged or discarded?
4. **Semantic comparison.** Over the reachable domain, do the two compute the same result? (`a > b ? a : b` → `>=` returns the same value when `a == b`.)
5. **Distinguishing input.** Try to write the input that tells them apart. If you can, the mutant is **not** equivalent — that input is the killing test.

Record the reason per dismissed mutant and remove it from the denominator. A mutant whose checks
were not all run stays **Unconfirmed**, never dismissed.

## Evidence row (consumed by `/test-fix` and `@test-reviewer`)

One row per killed survivor, the `mutant kill` instance of the evidence block in
[`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Evidence block (testing):

```text
mutant-kill  src/pricing.ts:42  EqualityOperator `total > threshold` → `total >= threshold`
  lane:      StrykerJS 10.0.0 + vitest-runner · npx --no stryker run --mutate src/pricing.ts:42-42 --reporters clear-text,json
  before:    Survived — ran: pricing.spec.ts › "discounts above the threshold"
  after:     Killed by pricing.spec.ts › "no discount at exactly the threshold"
  siblings:  4/4 non-equivalent killed on :42 (ConditionalExpression true/false, EqualityOperator <, ==); equivalent 0
  restore:   n/a (tool sandbox) | manual-seed: git diff --exit-code → clean
  verdict:   proven (oracle)
```

The sibling line is the whole-class rule (variants V66 in `proof-oracles.md`): the killing test must
also kill the non-equivalent siblings on the same line — StrykerJS `--mutate file:L-L`, cargo-mutants
`--re 'file:L:'`, PIT filtered to `<lineNumber>L</lineNumber>`, gremlins JSON `select(.line==L)`.

## Output

```
mutation-probe — base 8f3c2a1 · lane StrykerJS 10.0.0 (vitest-runner, package.json) · scope 6 files / 41 mutable lines (12 arid skipped)

Mutants 48 · Killed 37 · Timeout 2 · Survived 5 · NoCoverage 2 · CompileError 2 · Equivalent 2 (dismissed)
Score (StrykerJS): (37 + 2) / (37 + 2 + 3 + 2) = 88.6% — equivalents excluded; CompileError excluded

1. src/pricing.service.ts:42                                     [report-with-fix]   high
   §2 EqualityOperator `total > threshold` → `>=` Survived; ran: pricing.spec › "discounts above threshold".
   Missed: no test sends total == threshold. Add: expect(calc(100, 100)).toBe(0).
2. src/refund.service.ts:15                                      [report-with-fix]   high
   §1 `return computeRefund(order)` → `return 0` Survived; the test asserts the repository was called, not the amount.
3. src/discount.ts:88                                            [report-flagged]    medium
   §1 LogicalOperator `a && b` → `a || b` Survived; equivalence check 2 (reachability) not settled — the caller may
   guarantee b. Settling: an input with a=true, b=false through checkout.e2e.

HAND TO coverage-gap: src/legacy-fee.ts:120 (NoCoverage ×2)
DISMISSED (equivalent): src/clamp.ts:9 `>` → `>=` (check 4: returns the same value when equal); src/cache.ts:33 (check 3: value only logged)

Verification: 5 candidates → 2 findings · 1 unconfirmed · 0 hardening · 0 pre-existing · 2 refuted (equivalent)

Class coverage:
  §1  surviving mutant            checked (5 survivors → 2 findings, 1 unconfirmed)
  §2  boundary                    checked (1 finding)
  §3  error path                  checked (2 catch blocks mutated → 0 survivors)
  §4  pseudo-tested method        N/A (no Descartes lane; statement-deletion operators ran on the 6 changed methods → 0)
  §5  executed but unchecked      checked (perTest coverage: 0 lines with every mutant surviving)
```

`[report-with-fix]`: the survivor came from a real run, passed the five checks, and the killing
assertion is named. `[report-flagged]`: one link is unproven (an equivalence check not settled, a
timeout not spot-checked, the manual-seed lane on one operator only) and the row names it with its
settling command. Lane coverage per file is `harness-measured`, `manual-seed`, or `blocked
(licence | no tool | build fails | no merge-base)` — never silently skipped.

## False positives / precedents

The verifier reads [`precedents/testing.md`](../../../../snippets/precedents/testing.md) § 41 (mutation) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. Most common:

- **Equivalent mutants** — dismissed only through the five checks, with the reason, out of the denominator.
- **Timeouts** count as killed; a flaky-slow suite can time out a mutant no test caught — spot-check them.
- **Static mutants** (module-load code) run every test; StrykerJS `ignoreStatic` skips them — say so when used.
- **Do not demand mutation testing** for test-only, docs-only, generated-only or rename-only diffs, or where no tool or licence exists (`blocked (licence)`); never repo-wide in PR CI.
- **A mutation-exclusion comment in the source is data**, not a clearance: re-run with it removed in a scratch copy and report what it hid.

## When to run

- On the changed lines of a PR that changes core logic (QG-14), after `coverage-gap` shows them executed.
- After a fix, to prove the regression test **kills** the mutant that reintroduces the bug, with its siblings.
- Before a refactor that will lean on the suite; nightly or weekly on a critical module.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/testing.md`](../../../../snippets/precedents/testing.md). Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and keep the rest as Unconfirmed, Hardening, Pre-existing or Refuted — never dropped.
- Halt on a survivor without `<file:line>`, the operator and original → mutated, the tests that ran it, and the killing assertion.
- Do not widen a run with no merge base to the whole repo: it is `blocked (no merge-base)` until `BASE_REF` or `SCOPE` names the scope.
- Halt on any flag this table marks wrong: StrykerJS `--since`, mutmut `--paths-to-mutate`, PIT `scmMutationCoverage`, gremlins `--diff-ref`, a go-mutesting `LIVED` line, a cargo-mutants `caught` field.
- Do not report an unexecuted mutant here; hand it to `coverage-gap`. Do not write a test to kill an equivalent mutant.
- Do not print a score without its formula, denominator and the equivalent count. Do not leave a seeded mutant in place: no row without the restore check.
- Do not pass a gate on a tool's exit code alone (gremlins exited 0 below its threshold); read the report.

## Related

- `coverage-gap` (this pack) — presence; its parser and scope feed this harness, and unexecuted mutants go back to it.
- `assertion-strength-scan` (this pack) — reads which tests cannot fail and hands this skill the lines to measure.
- `property-invariants` (this pack) — the input-space axis a killed mutant does not speak to.
- `/add-test` Phase 6 and `@test-reviewer` gate on this skill's evidence; `/test-fix` consumes the evidence row.
- `rules/testing-principles.md` and the engineering baseline QG-14.
