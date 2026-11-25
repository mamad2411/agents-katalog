---
name: testing-fuzzing-mutation
description: Use when fuzzing parsers and security boundaries or measuring whether tests actually catch bugs — coverage-guided fuzzing, OSS-Fuzz, mutation testing.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [testing-strategy, testing-property-based, security, tdd]
---

# Fuzzing + Mutation Testing

**Iron Law: fuzz parsers and security boundaries. Mutation testing tells you which tests would fail to catch real bugs.**

Two techniques, one skill — they answer different questions:

- **Fuzzing** finds inputs you'd never write that break your code.
- **Mutation** finds tests that exist but assert nothing useful.

|              | Fuzz                                 | Property                             | Mutation                          |
| ------------ | ------------------------------------ | ------------------------------------ | --------------------------------- |
| What it does | Generates raw inputs to find crashes | Asserts invariants over typed inputs | Breaks code, checks if tests fail |
| Guidance     | Coverage feedback                    | Strategies                           | Operator catalog                  |
| Iterations   | Millions–billions, continuous        | Hundreds                             | Once per mutant                   |
| Verdict      | Crash / panic / hang found           | Counterexample found                 | Mutant killed / survived          |

## Fuzzing

### When fuzzing is essential

- **Parsers and deserializers** — JSON, XML, ProtoBuf, image/audio/video decoders, custom binary.
- **Compression/encoding** — anything walking a byte stream by length prefix or tag.
- **Security boundaries** — TLS handshakes, auth tokens, signature verification.
- **Sandboxes / VMs / interpreters** — input _is_ code.
- **Crypto primitives** (paired with formal review).
- **Anything taking user-supplied bytes and producing structured output.**

If your code's first job is to _understand_ an input, fuzz it.

### When fuzzing is overkill

Pure business logic with typed inputs (property tests). DB queries (integration). UI logic (e2e). Code that never sees untrusted input.

### Tool landscape

| Ecosystem               | Tool                                                                 |
| ----------------------- | -------------------------------------------------------------------- |
| C / C++ / Rust          | **libFuzzer** (LLVM), **AFL++**                                      |
| Rust                    | `cargo-fuzz`, `honggfuzz`                                            |
| Go                      | native `go test -fuzz` (1.18+)                                       |
| Python                  | `atheris` (libFuzzer for Python), Hypothesis with fuzzing strategies |
| Java                    | `Jazzer`, `JQF`                                                      |
| JavaScript / TypeScript | `Jazzer.js`                                                          |
| Cross-language          | **OSS-Fuzz** (Google's continuous infra, free for qualifying OSS)    |

All coverage-guided fuzzers: pick seed → mutate → run → check for crash + new coverage → keep or discard.

### Anatomy of a fuzz target

````pseudo
fuzz_target(data: bytes):
    try:
        result = function_under_test(data)
        # Optional: assert invariants on result
    except (ValidationError, BadInput):     # NEVER bare `except Exception:` or `except:` —
        return  # not interesting              # it swallows sanitizer reports, OOMs, and the
    # Any uncaught exception / panic / crash / hang / sanitizer violation = bug
```                                             # very memory-safety bugs you ran the fuzzer to find.

Keep targets small. One per parser entry point. Deterministic — fuzzers replay corpus constantly. The exception list MUST be the narrow set of input-validation errors the function legitimately raises; anything broader hides bugs.

### Corpus, seeds, dictionaries

- **Seeds** — known-valid inputs to start from. Real examples > synthetic. Use existing test fixtures.
- **Corpus** — inputs the fuzzer decided are "interesting" (each exercises new coverage). Persisted between runs.
- **Dictionary** — tokens to sprinkle into mutations. For JSON: `{ } : , true false null`. Cuts warmup massively.

**Treat corpus like source** — version it, share across machines, never delete without reason. **Never seed from raw production traffic** — request bodies and headers may carry PII or secrets that then land in your repo. Use synthetic data, or sanitize/redact before commit.

### Sanitizers — fuzzing without them is half-blind

In C/C++/Rust (unsafe), run under **ASan + UBSan** always. Finds use-after-free, buffer overflow, integer overflow, null deref, uninitialized reads. For Python (`atheris`), Go (`go test -fuzz`), or other GC'd languages, sanitizer-equivalent signals (interpreter aborts, runtime panics) ALSO need to escape the fuzz target — see the bare-except warning above.

### Continuous fuzzing

| Cadence | Setup |
|---|---|
| **OSS-Fuzz** | For widely-used parsers, crypto, security primitives, long-lived libraries |
| **CI per PR** | Short burst (10 min) extending the existing corpus (not cold-start; fresh corpus finds ~nothing) |
| **CI nightly on main** | Long burst (hours), persist new corpus entries |
| Always | Replay corpus first — catches regressions instantly |

### Triaging findings

For every crash:

1. **Minimize** the input (`-minimize_crash`).
2. **Bisect** to the introducing commit.
3. **Add minimal input as a unit test** (regression).
4. **Add to corpus** so fuzzer learns related variants.
5. **Fix** with `Skill(debugging)` and `Skill(root-cause)`.

### Fuzzing pitfalls

- Non-deterministic targets (fuzzer can't reproduce; corpus poisoned); slow targets (aim sub-ms; fuzzers thrive on exec/sec)
- Known crashes on first run (fix before adding fuzzer); no seeds (wastes hours getting past magic-bytes headers)

## Mutation Testing

Coverage proves a line *ran*. Mutation proves a line was *checked*.

### How it works

1. Parse production code.
2. Generate **mutants** — copies with one small change:
   - `>` → `>=`
   - `+` → `-`
   - `true` → `false`
   - `return x` → `return null`
   - Drop a statement
3. Run tests for each mutant.
4. **Killed** mutant: at least one test failed → tests noticed. Good.
5. **Survived** mutant: every test still passed → tests missed it. Bad.
6. **Mutation score** = killed / (killed + survived) × 100%.

### Tool landscape

| Ecosystem | Library |
|---|---|
| Python | `mutmut`, `cosmic-ray` |
| JavaScript / TypeScript | `Stryker` |
| Rust | `cargo-mutants` |
| Java / JVM | `PIT` |
| Go | `go-mutesting`, `gremlins` |
| C / C++ | `mull` |
| PHP | `Infection` |

### Surviving mutants — what they tell you

| Survivor pattern | What's missing |
|---|---|
| `>` → `>=` survives | No test on the boundary |
| `return x` → `return null` survives | No test asserts return value |
| Statement deletion survives | Dead code OR untested side effect |
| `+` → `-` survives | No test distinguishes the values |
| Constant `42` → `43` survives | Exact value untested |

Fix is almost always "add an example test that pins this exact behavior," sometimes "delete the dead code."

### When mutation pays

**Strong fit:** payments, security checks, parsers, schedulers, encoders. A suite that passes too easily. Libraries with stable APIs. Post-coverage-push.

**Weak fit:** UI/glue code. Suites that already run 30 min (mutation × 10-100). Code that changes hourly.

### The cost

5-second suite × 1000 mutants = 80 min. Strategies:

- **Run on diff only** — mutate just PR-changed lines.
- **Nightly/weekly full**, not per-commit.
- **Parallelize aggressively** — embarrassingly parallel.
- **Test-impact analysis** — skip tests that don't cover mutated lines.
- **Skip equivalent mutants** — `x + 0` → `x - 0` doesn't change behavior.

### Mutation score targets

| Component | Target |
|---|---|
| Money, auth, security checks | 90%+ |
| Core domain logic | 80%+ |
| Adapters, integrations | 60%+ (integration tests catch many seams) |
| UI / glue | Not measured, or 40%+ |

### Mutation pitfalls

- **Gaming the score** — tests asserting private internals to kill mutants. Test behavior, not implementation.
- **Aiming for 100%** — last 10% is mostly equivalent mutants.
- **Blocking PRs on flaky scores** — slow + noisy; nightly + reported is better.
- **Ignoring survivors because "the code is obviously right"** — until you rewrite it.

## Fuzz + mutation together

- Coverage-guided fuzz finds the *inputs* you didn't think of.
- Mutation finds the *assertions* you didn't write.
- Property tests (`Skill(testing-property-based)`) catch many mutants for free — invariants kill "broke the math" mutants without listing each example.

## Anti-patterns

- Fuzzing pure-typed code where bytes never apply; treating corpus as transient
- "Done fuzzing — no crashes for an hour" (fuzzers run for days/weeks); fuzzing without sanitizers
- Calling mutation score "coverage" (they measure different things)
- Mutation testing on every commit blocking PRs; crash found with no regression test added

## Hand-off

For unit/integration foundation: `Skill(testing-strategy)`. For typed invariants: `Skill(testing-property-based)`. For security boundaries: `Skill(security)`. Language harnesses: `Skill(go-testing)`, `Skill(rust-testing)`, `Skill(python-testing)`.
````
