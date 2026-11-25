---
name: property-invariants
description: Find functions whose correctness lives in properties that must hold for ALL inputs — round-trip, idempotence, commutativity, invariants — and generate property-based tests instead of a handful of examples. Use when a pure function (parser, encoder, formatter, sort/dedupe, path builder) has only example tests, or a serialize/parse pair has no round-trip property. Not for I/O-bound or side-effecting code.
kind: skill
pack: testing
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# property-invariants

Some correctness doesn't live in examples. `parse(serialize(x)) == x` must hold for *every* `x`, not the three you typed. A pure, total function tested only by example under-tests its input space — the bug is in the input you didn't think of. This skill finds those functions and generates property-based tests that a generator explores for you.

## Premise

Find real properties, no hand-waves. Every reported candidate cites the function as `<path:line>`, names the specific property class it satisfies (round-trip / idempotence / commutativity / invariant / model-based / oracle), and states the property as an executable predicate over generated inputs — `for all x: parse(serialize(x)) == x`, not "should round-trip". A generated test that has no shrinker, or that swallows the failing seed, is not a finding — it is a flaky test in waiting. "This looks pure, add property tests" is not a finding; "`codec.ts:44 encode`/`codec.ts:71 decode` form a round-trip pair with only 2 example tests, no property" is.

## Halt conditions

- Halt on a proposed property without a `<path:line>` for the function and a stated for-all predicate.
- Halt on a property test whose generator has no shrinker (or whose framework's shrinking was disabled) — an un-shrunk counterexample is unusable.
- Halt on a property test that does not log/pin the failing seed on failure — non-reproducible property failures are worse than no test.
- Halt on classifying a function as "pure/total" without confirming it has no I/O, no clock/RNG read, and a defined result for every input in the generated domain.

## When to run

- A pure or total function (parser, encoder, formatter, math/geometry, sort/dedupe, path/URL builder) has only example tests.
- A `serialize`/`parse`, `encode`/`decode`, `compress`/`decompress`, or `to`/`from` pair exists with no round-trip property.
- A documented or code-enforced invariant (balance ≥ 0, output sorted, set has no dupes, tree stays balanced) is asserted in one example but never quantified over inputs.
- A reference/brute-force oracle exists (or is cheap to write) that the fast implementation must agree with.
- A state machine / stateful component (cache, queue, allocator, session store) has only scripted happy-path tests.

## Adapt to the codebase

Detect the stack, then use its idiomatic property framework. Do not introduce a new dependency if the repo already pins one.

| Stack | Framework | Generator / shrink notes |
|---|---|---|
| JS / TS | fast-check | `fc.assert(fc.property(gen, pred))`; built-in shrinking; seed via `fc.configureGlobal` / printed on failure |
| Python | Hypothesis | `@given(strategies)`; automatic shrinking; `@seed`/`--hypothesis-seed` to reproduce; `@example` to pin regressions |
| Java / Kotlin | jqwik | `@Property` + `@ForAll`; `@Provide` for custom arbitraries; deterministic `@Seed`. jqwik ≥ 1.10 is reported to carry an "Anti-AI Usage Clause" (business research, 2026-10-19; its text UNVERIFIED): read the installed version's licence and README before generating jqwik code, and stop and ask if it restricts AI-written tests |
| Scala / JVM | ScalaCheck | `forAll`; `Gen`/`Arbitrary`; integrates via ScalaTest/specs2 |
| Haskell | QuickCheck / Hedgehog | `Arbitrary`/`Gen`; Hedgehog has integrated shrinking without separate `Shrink` |
| Rust | proptest / quickcheck | proptest = strategy-based + persisted failure corpus; quickcheck = `Arbitrary` trait |
| Go | testing/quick, rapid | stdlib `quick.Check` (no shrink); `pgregory.net/rapid` for shrinking + stateful |
| Elixir | StreamData / PropCheck | `check all`; stateful via PropCheck's model callbacks |

If no framework is pinned, propose the row above and STATE it — do not silently add a heavy dependency.

## Pre-flight

Run as **one** script from the repo root; every `rg` names its path (`.`). Grep 1 is the candidate
list for the round-trip class; the other three classes (idempotence, algebraic laws, invariants) are
found by reading, ranked by the money, parsing and wire modules on the context map.

```bash
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/coverage/**' -g '!**/*.d.ts'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,fixtures,__fixtures__,testdata,generated,__generated__,migrations}/**' -g '!**/*.{test,spec,e2e-spec,stories,test-data,fixture}.*' -g '!**/{test_*,*_test,conftest}.*')
T=(-g '**/*.{test,spec,e2e-spec}.{js,jsx,ts,tsx,mjs,cjs}' -g '**/{test_*,*_test}.py' -g '**/*_test.go' -g '**/*{Test,Tests}.{java,kt}' -g '**/*_spec.rb' -g '!**/node_modules/**')
# 0. Property frameworks pinned (0a) and the test files that already state a property (0b).
rg -n --pcre2 '"fast-check"|"@fast-check/\w+"|^\s*hypothesis\b|\bjqwik\b|\bproptest\b|pgregory\.net/rapid|\bquickcheck\b|\bscalacheck\b|\bstream_data\b|\bpropcheck\b' -g '**/{package.json,pyproject.toml,requirements*.txt,setup.cfg,pom.xml,build.gradle*,go.mod,Cargo.toml,mix.exs,build.sbt}' -g '!**/node_modules/**' .
rg -l --pcre2 '\bfc\.(?:assert|property|asyncProperty)\(|@given\(|@Property\b|\bproptest!\s*\{|\brapid\.Check\(|\bquick\.Check\(|\bforAll\(|\bcheck\s+all\(' "${T[@]}" . | wc -l
# 1. Codec pairs: a function and its inverse exported from one file (to/from<X>, encode/decode, serialize/deserialize|parse,
#    marshal/unmarshal, format/parse<X>, pack/unpack, compress/decompress), with the test files that name either half and
#    whether any of them states a property. `PAIR … property=no` is the candidate list.
rg -n --pcre2 '^\s*(?:export\s+)?(?:async\s+)?(?:function\s+|const\s+|def\s+|func\s+(?:\([^)]*\)\s*)?|(?:public\s+)?(?:static\s+)?[\w<>\[\]]+\s+)(?:to|from|encode|decode|serialize|deserialize|parse|format|marshal|unmarshal|pack|unpack|compress|decompress|stringify)[A-Z_]\w*\s*(?:[=(:<]|\s*=\s*(?:async\s*)?\()' -g '*.{ts,tsx,js,mjs,py,go,java,kt}' "${X[@]}" . | python3 -c '
import collections, re, subprocess, sys
INV = [("to", "from"), ("encode", "decode"), ("serialize", "deserialize"), ("serialize", "parse"), ("marshal", "unmarshal"), ("format", "parse"), ("pack", "unpack"), ("compress", "decompress"), ("stringify", "parse")]
fns = collections.defaultdict(dict)
for l in sys.stdin:
    f, n, t = l.split(":", 2); m = re.search(r"\b((?:to|from|encode|decode|serialize|deserialize|parse|format|marshal|unmarshal|pack|unpack|compress|decompress|stringify)([A-Z_]\w*))", t)
    if m: fns[f].setdefault(m[1], n)
tests = subprocess.run(["rg", "-l", "--pcre2", ".", "-g", "*.{test,spec}.{ts,tsx,js,mjs}", "-g", "{test_*,*_test}.py", "-g", "*_test.go", "-g", "*Test.{java,kt}", "-g", "!**/node_modules/**", "."], capture_output=True, text=True).stdout.split()
src = {t: open(t, errors="replace").read() for t in tests}; words = {t: set(re.findall(r"\w+", s)) for t, s in src.items()}
PROP = re.compile(r"\bfc\.(?:assert|property)|@given\(|@Property\b|proptest!|rapid\.Check|quick\.Check|\bforAll\(")
pairs = 0
for f, names in sorted(fns.items()):
    for a, b in INV:
        for x in [n for n in names if n.startswith(a) and n[len(a):][:1].isupper()]:
            y = b + x[len(a):]
            if y in names:
                pairs += 1; ts = [t for t, w in words.items() if x in w or y in w]
                print("PAIR %s:%s %s/%s tests=%d property=%s" % (f, names[x], x, y, len(ts), "yes" if any(PROP.search(src[t]) for t in ts) else "no"))
print("pairs=%d" % pairs)'
```

A `PAIR … property=no` row is a candidate, not a finding: read both halves (is it total over a real
domain, or a lossy projection such as `toDay` / `fromDay` that drops the time?) before stating the
predicate. Pairs the regex cannot see — two `to*` functions that invert each other
(`toMinorUnits` / `toMajorUnits`), a codec split across two files, a class with `encode` / `decode`
methods — come from reading the money and wire modules.

**Measured** (2026-10-15, read-only) on a real NestJS + React monorepo: 0a empty (no property
framework pinned), 0b 2 test files state a property; grep 1 finds 49 same-file inverse pairs, 48
with no property test (the portal-claims codec is the one with a property). The money minor/major
pair is not a `to`/`from` pair and is listed by reading. About 1 s; every fixture returns 0 pairs.

## Procedure

1. **Spot candidates.** Scan changed/critical code for the four smells:
   - *Pure/total, examples only* — no side effects, deterministic, defined for all inputs, yet 1-5 hardcoded cases.
   - *Round-trip pair* — a `f`/`f⁻¹` couple (`serialize`/`parse`, `encode`/`decode`, `marshal`/`unmarshal`) with no `decode(encode(x)) == x` test.
   - *Algebraic law* — idempotence (`f(f(x)) == f(x)`: normalize, dedupe, saturating clamp), commutativity/associativity (merge, union, add), monotonicity, identity/inverse elements.
   - *Invariant / oracle* — a postcondition the output must always satisfy (sort → output is sorted AND a permutation of input; balance never negative), or a slow reference implementation the fast one must match.
2. **State the property as a predicate.** Write the for-all explicitly: inputs, the relation that must hold, and the input domain (including edge generators — empty, unicode, NaN, negative, huge).
3. **Design the generator.** Cover the real domain, not just easy values. Prefer the framework's composition (`map`/`filter`/`bind`) over ad-hoc loops. Constrain to the valid input space so failures are real, not precondition violations.
4. **Confirm the shrinker.** Use the framework's built-in shrinking; for custom generators built by hand, ensure a shrink path exists so counterexamples reduce to minimal cases. A generator with no shrinker is a defect (see Halt).
5. **Stateful / model-based** for state machines: define a lightweight model (e.g. a plain map/list), a set of commands, a precondition + postcondition per command, and let the framework generate command sequences. Assert model and real system stay in agreement after every command.
6. **Pin reproducibility.** Ensure the framework prints the failing seed; capture regressions as pinned examples (`@example` / persisted failure corpus / `@Seed`) so a fixed bug never silently returns.

## Output

```
Property candidates — feature/codec-hardening  (base=origin/main)

Functions changed: 6  |  With property tests: 1  |  Candidates found: 4

ROUND-TRIP (high value):
  src/codec.ts:44 encode  /  src/codec.ts:71 decode
    Property: ∀ msg. decode(encode(msg)) deep-equals msg
    Today: 2 example tests. Generator: fc.record over the Message schema.
    Shrinker: fast-check built-in. Seed: printed on failure.

INVARIANT:
  src/ledger.py:88 apply_transaction
    Property: ∀ ops. balance after any op sequence >= 0  (model-based)
    Model: running int; commands = [deposit, withdraw]; withdraw precond balance>=amt.
    Framework: Hypothesis stateful (RuleBasedStateMachine).

IDEMPOTENCE:
  src/paths.go:31 Normalize
    Property: ∀ p. Normalize(Normalize(p)) == Normalize(p)
    Framework: pgregory.net/rapid (shrinking). testing/quick lacks shrink — do not use here.

ORACLE:
  src/sort/fast_sort.rs:20 fast_sort
    Property: ∀ v. fast_sort(v) == { let mut c=v; c.sort(); c }  (stdlib oracle)
    proptest strategy: prop::collection::vec(any::<i32>(), 0..1000)
```

## False positives / gotchas

- **Not actually pure.** A function that reads a clock, RNG, env, or global fails intermittently under a generator for the *right* reason — inject the dependency first (see `test-doubles.md`), or it's a bad property candidate, not a bug.
- **Precondition leakage.** If the generator emits inputs the function legitimately rejects, you'll get false failures. Constrain the generator to the valid domain; don't assert on garbage-in.
- **Float exactness.** `parse(serialize(f)) == f` fails on floating point — assert within epsilon or round-trip through the canonical string, not `==`.
- **Weak generator.** A generator that only emits small ints "passes" while missing the empty/unicode/overflow case. Breadth of the generator *is* the strength of the test.
- **Slow oracle in the hot loop.** An O(n²) reference oracle throttles the run — cap generated size, or gate the oracle property behind a slower CI tier.
- **Flaky seed hidden.** If the framework's default swallows the seed, a red build isn't reproducible. Confirm the seed is logged before trusting any property test.

## Boundary

- `coverage-gap.md` = **presence** — did any test hit this branch at all.
- `mutation-probe.md` = **strength** — do the assertions actually catch a mutation.
- `property-invariants` (this) = **input-space breadth** — does the test hold across the whole domain, not the handful of examples you picked.

A branch can be covered (coverage-gap green), assertion-strong on those examples (mutation-probe green), and still wrong on the input you never generated. That last gap is this skill's job.

Related: `coverage-gap`, `mutation-probe`, `@test-engineer`.
