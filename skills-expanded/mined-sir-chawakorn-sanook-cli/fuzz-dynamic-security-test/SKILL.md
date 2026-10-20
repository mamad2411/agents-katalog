---
name: fuzz-dynamic-security-test
description: Sets up dynamic security testing — coverage-guided fuzzing of parsers and input handlers (libFuzzer/cargo-fuzz/AFL++/go test -fuzz/atheris) and DAST scanning of a running app (OWASP ZAP/nuclei) — wired into CI with seed corpora, crash minimization, baseline suppression, and regression-corpus commits.
when_to_use: Hardening code that parses untrusted input, or a running web app, with active runtime testing that drives real inputs to provoke crashes/vulns. Distinct from write-tests (functional-correctness tests), security-review (static code audit), remediate-web-vulnerabilities (fixing a known vuln), and load-stress-test (performance under load).
---

## When to Use

Reach for this skill when you want to **actively drive inputs at code or a running app** to provoke crashes/vulns, not reason about them statically:

- "Fuzz this parser / deserializer / protocol decoder / image or PDF loader for crashes"
- "Set up cargo-fuzz / libFuzzer / `go test -fuzz` / atheris / AFL++ with a seed corpus and run it in CI"
- "An input crashes / hangs / OOMs — minimize it and add a regression test"
- "Run OWASP ZAP / nuclei against staging, authenticated, and triage the findings"
- "Wire short fuzz on PR + long nightly fuzz, and DAST on every staging deploy"

NOT this skill:
- Functional correctness / example-based unit tests → write-tests
- Reading code by eye for injection/authz/secret bugs (no execution) → security-review
- Fixing a *specific known* SQLi/XSS/SSRF you already found → remediate-web-vulnerabilities
- Measuring latency/throughput/breaking point under concurrency → load-stress-test
- Reviewing an authorization *design* rather than testing it at runtime → design-authorization-model

If a finding is confirmed, hand the fix to remediate-web-vulnerabilities; this skill *finds and reproduces*, it does not patch app logic.

## Steps

1. **Pick the right tool for the target — do not write a fuzzer by hand.** Coverage-guided engines mutate toward new code paths; random byte-spray finds nothing. Match the language:

   | Target | Engine | Harness entry | Sanitizers |
   |---|---|---|---|
   | C/C++ | **libFuzzer** (clang `-fsanitize=fuzzer`) | `LLVMFuzzerTestOneInput(const uint8_t*, size_t)` | ASan + UBSan (+ MSan separately) |
   | Rust | **cargo-fuzz** (libFuzzer under the hood) | `fuzz_target!(\|data: &[u8]\| { ... })` | ASan on by default |
   | Go | **native `go test -fuzz`** | `func FuzzX(f *testing.F)` + `f.Fuzz(...)` | race + built-in checks |
   | Python | **atheris** (libFuzzer bindings) | `atheris.Setup` + `TestOneInput(data)` | native-ext ASan optional |
   | JS/TS | **Jazzer.js** | `module.exports.fuzz = (data) => {...}` | n/a (catches throws) |
   | Out-of-process C binary | **AFL++** (`afl-fuzz -i in -o out`) | feed stdin/file | persistent mode + cmplog |

   Default to the **in-process libFuzzer-family** engine for the language; reach for AFL++ only when you can't instrument the target (closed binary, weird build).

2. **Fuzz the smallest deterministic boundary, structure-aware.** Target one pure `bytes → parsed value` function — the deserializer, the codec/protocol decode, the template/expression parser — not the whole HTTP handler. Make it deterministic (no clock/network/RNG/global state). For structured formats, decode the byte buffer into typed inputs with `arbitrary` (Rust) / `FuzzedDataProvider` (C++/atheris) so mutations stay valid-ish and reach deep logic instead of dying at the length check. Rust example:

   ```rust
   #![no_main]
   use libfuzzer_sys::fuzz_target;
   use arbitrary::Arbitrary;

   #[derive(Arbitrary, Debug)]
   struct Input { name: String, depth: u8, body: Vec<u8> }

   fuzz_target!(|inp: Input| {
       // never unwrap() inside a harness on the parser's own error path —
       // a clean Err is correct, only a panic/abort is a finding.
       let _ = my_parser::parse(&inp.name, inp.depth, &inp.body);
   });
   ```

3. **Seed the corpus and add a dictionary — this multiplies coverage.** Drop real, valid sample files into `corpus/<target>/` (one input per file). Add a `.dict` of format tokens/magic bytes (`"PDF"`, `"\xFF\xD8"`, keywords) and pass `-dict=tokens.dict`. Without seeds the fuzzer wastes hours rediscovering the file header. Keep the corpus in the repo so CI starts warm.

4. **Run, then minimize every crash before committing it.** Run locally first (`cargo fuzz run target -- -max_total_time=300` / `go test -fuzz=FuzzX -fuzztime=5m`). On a crash, **minimize the input** (`cargo fuzz tmin`, libFuzzer `-minimize_crash=1 -runs=100000`, AFL++ `afl-tmin`) so the repro is small and the root cause is obvious. Add `-rss_limit_mb`, `-timeout=`, and `-max_len=` so OOMs and hangs are reported as findings, not killed silently.

5. **Commit each crash as a regression seed — this is the deliverable.** Copy the minimized input to `corpus/<target>/crash-<hash>` (or Go's `testdata/fuzz/FuzzX/`). It now re-runs on every fuzz invocation, so the bug can't silently return. This is what turns a one-off crash into a permanent test. Open a finding (step 7) linking the seed.

6. **For a running app, run DAST against staging — never prod.** Stand up a disposable staging instance with seeded test data, then:
   - **nuclei** for known-CVE/misconfig templates: `nuclei -u https://staging.app -severity medium,high,critical -rl 50`.
   - **ZAP** for app-aware crawling: baseline first, then authenticated active scan. Authenticate (ZAP context + auth script, or pass a session cookie/Bearer) so the scanner reaches logged-in routes — an unauthenticated scan misses ~80% of the surface.
   - **Baseline-suppress accepted findings** instead of muting the whole rule: keep a `zap-baseline.conf` / nuclei exclude list of triaged-and-accepted IDs so the gate only fails on *new* findings. Tune `-rl`/throttle so the active scan doesn't DoS staging.

7. **Triage every finding: reproduce → severity → dedupe → file.** Re-run the exact input/request to confirm it's real (drop scanner false positives — reflected param that's actually encoded, "missing header" on an internal-only route). Rate by realistic impact (RCE/memory-corruption/authn-bypass = Critical; reflected-but-encoded = noise). Dedupe by crash stack / vuln class, not by input bytes — 500 inputs hitting one `parse()` panic are one bug. File with the minimized repro and the committed seed path.

8. **Wire into CI in two tiers + a DAST stage.** Cheap on every PR, deep on a schedule:

   ```yaml
   # PR: smoke-fuzz only the changed/corpus seeds — must finish in <2 min, gates merge
   pr-fuzz:
     run: cargo fuzz run parser -- -runs=0 corpus/parser   # replay corpus, no mutation
   # Nightly: long mutation run, upload new crashes as artifacts, file on failure
   nightly-fuzz:
     run: cargo fuzz run parser -- -max_total_time=3600 -timeout=10 -rss_limit_mb=2048
   # Per staging deploy: DAST gate
   dast:
     run: nuclei -u $STAGING_URL -severity high,critical -ed <accepted.txt> -ni
   ```

   PR job replays the corpus (deterministic, fast, catches regressions); nightly does the expensive mutation. Never put an unbounded mutation run on the PR critical path.

## Common Errors

- **`unwrap()`/`expect()` in the harness on the parser's own error path.** Every malformed input then "crashes" — pure noise. A returned `Err` is correct behavior; only a panic/abort/sanitizer-trip in the *code under test* is a finding.
- **No seed corpus and no dictionary.** The fuzzer burns the whole budget rediscovering the file magic/header and never reaches real logic. Seed with valid samples; add a token `.dict`.
- **Non-deterministic harness.** Reading the clock, network, RNG, or mutating global state makes crashes non-reproducible and corrupts coverage feedback. The harness must be a pure function of `data`.
- **Committing the raw crashing input, not the minimized one.** A 4 MB repro hides the root cause and bloats the corpus. Always `tmin`/`-minimize_crash` first.
- **Fuzzing the whole HTTP handler instead of the parser.** Network/auth/DB setup dwarfs the parse step, so mutations rarely reach it — throughput collapses to a few execs/sec. Target the pure decode boundary in-process.
- **No `-rss_limit_mb`/`-timeout`/`-max_len`.** OOMs and infinite loops get OS-killed and look like a hung job instead of a reported memory/hang bug. Set explicit limits.
- **Sanitizers off (release build).** Use-after-free, OOB read, and integer-UB pass silently without ASan/UBSan — you only catch hard segfaults. Build the fuzz target with sanitizers on.
- **Running ZAP/nuclei against production.** Active scans send malicious payloads, mutate data, and can take the service down. Always a disposable staging instance with test data.
- **Unauthenticated DAST scan.** Misses every logged-in route — the high-value surface. Configure auth (context/script/session token) and verify the scanner is actually inside a session.
- **Muting a whole scanner rule to clear noise.** Hides future real hits of that class. Suppress the specific accepted finding ID in a baseline file so only *new* findings fail the gate.
- **Unbounded mutation fuzz on the PR job.** Blocks every merge for an hour or times out. PR replays the corpus; the long mutation run goes nightly.

## Verify

1. **Engine actually mutates and gains coverage:** a short run shows rising `cov:`/`ft:` and `exec/s` counters (libFuzzer) — not flat. Flat coverage means the harness rejects inputs at the door (wrong shape, missing `arbitrary`/`FuzzedDataProvider`).
2. **Planted-bug catch:** add a deliberate `assert!`/OOB/`panic!` on a specific byte pattern (or use a target with a known-CVE-style flaw), run the fuzzer, and confirm it finds and minimizes the input within minutes. A fuzzer that can't catch a planted bug catches nothing.
3. **Every crash yields a committed seed:** for each crash found, the minimized input lives in the corpus/`testdata` and is tracked in git. Re-running the harness over the corpus reproduces the crash deterministically.
4. **Regression gate works:** with the seed committed but the bug *un*fixed, the PR corpus-replay job fails; after the fix it passes — proving the seed actually guards the regression.
5. **DAST reproduced + authenticated:** at least one scanner finding is independently re-sent (curl/HTTP client) and reproduces; the scan log shows it traversed authenticated routes (logged-in paths visited), not just the login page.
6. **Baseline suppression is scoped:** a previously-accepted finding is silenced by its specific ID, while a freshly introduced vuln of a *different* class still fails the gate (suppression didn't blanket the rule).
7. **CI tiers honored:** PR fuzz finishes under its time cap (corpus replay only); nightly runs the bounded mutation budget and uploads any new crash as an artifact + files it.

Done = the engine provably mutates toward new coverage, a planted bug or known-CVE pattern is caught and minimized, every crash is committed as a regression seed that fails-then-passes across the fix, and DAST runs authenticated against staging with scoped baseline suppression and a two-tier CI wiring.
