---
name: numeric-stability-scan
description: Find float error in numeric code (accumulation, cancellation, overflow, conditioning, fast-math) and unsized sketches.
kind: skill
pack: algorithms
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: numeric-stability-scan

## Premise

A float result can be wrong in every digit while every line that produced it is correct. A running
sum loses small terms against a large partial; the textbook variance subtracts two nearly equal
numbers and keeps the noise; a product of probabilities underflows to zero; `exp` without a max
shift overflows to infinity; an explicit inverse amplifies a condition number of 1e12 into four
correct digits; a `-ffast-math` build folds away the NaN check the code relies on. And an
approximate structure — a Bloom filter, a HyperLogLog, a Count-Min sketch — answers with an error no
one stated, or decides a charge on its false positive. CWE files the first family under **CWE-1339**
(insufficient precision or accuracy of a real number) and **CWE-190**, the last under **CWE-697**.

**Every finding cites the computation `<file:line>` + its class + the magnitude, count or condition
that makes it lose precision (or the sketch's missing parameters / the exact decision it feeds) + the
tolerance the result needs (stated in the spec, a test or a consumer) + the entry point + the proof +
the fix.** A grep hit is never a finding, and "no numeric defect" is never printed without the
class-coverage block (§ Output).

**Gated, and the gate is printed.** This skill runs §1–§4 only on files that import a numeric library
or call an anchored numeric function (grep G). The earlier gate — words such as `mean`, `norm`,
`solve`, `double`, `float`, `Decimal` — matched 3,574 of 11,875 files of a real CRUD monorepo that
holds no numeric code, and 20 of 24 benchmark fixtures. With the gate at 0, §1–§4 print
`N/A (no numeric code: gate 0)`, never `checked`. §5 (build flags) and §6–§7 (sketches) carry their
own greps, because a flag or a sketch is evidence by itself. Proof is a **high-precision reference**
or a **measured error** ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Algorithms,
V608–V609), never an opinion about digits.

## The rule

A computation is a finding when all four hold:

1. **A production path runs it** — a report, an analytics job, a scoring or ranking step, a model
   feature, a simulation that ships results. A notebook or a one-off analysis script fails here.
2. **The data reaches the regime that loses precision** — many terms or mixed magnitudes (cite the
   count and range), nearly equal operands, probabilities below ~1e-300 in a product, an
   ill-conditioned matrix (cite `cond` or the data's shape), a sketch's real n beyond its sizing.
3. **The result needs more accuracy than it gets** — a stated tolerance (a spec, a test, a
   consumer's threshold), a reported number, a decision. Without a stated tolerance, the row is
   `[report-flagged]` with the question.
4. **The oracle fires failing-first** (V608: outside the stated relative tolerance of `math.fsum`,
   `Decimal`, `mpmath` or `BigInt` on adversarial data; V609: the flag on a shipped build, the
   measured error above the stated bound, an unconfirmed positive on a money path).

**Severity.** **High** when a sketch's positive decides money, a send or a quota (SL-2), or a numeric
error changes a persisted or billed number; **medium** for reported statistics, scores and job
outputs; **low** for display-only values. A float result whose consumer rounds to two decimals
after a well-conditioned computation of a few hundred terms is not a finding.

## Boundaries

Money is code-quality `correctness-smell-scan` §4 (arithmetic in code), database
`schema-integrity-scan` §4 (a float money column) and business `pricing-rule-scan` (rounding and
allocation policy); float `==`, NaN compares and `-0` are code-quality §2; integer overflow, ids above
2^53, parses and truncating division are code-quality §4; an exact set or map that grows forever is
performance `memory-growth-scan` §1; a sketch's memory budget is performance's. This skill owns
accumulated rounding error, cancellation, overflow to log-space, conditioning and IEEE-voiding flags
in numeric code, and the stated error of sketches. Choosing a tolerance in scientific code (absolute
vs relative vs ULP) is a read question inside §1, never a float-`==` finding. Each cross-pack route
applies when that pack is installed; without it the row is listed here, tagged
`<class> (owner pack <x> not installed)`, and never graded as the owner would grade it.

## Adapt to the codebase — lanes

| Lane | Gate libraries (grep G1) | Reference for V608 | Stable primitives the fix names |
|---|---|---|---|
| **Python** | numpy, scipy, pandas, polars, statsmodels, scikit-learn, torch, jax, numba, mpmath, `statistics` | `math.fsum`, `fractions.Fraction`, `decimal` (raised precision), `mpmath` | `math.fsum`, `np.sum` (pairwise), `statistics.fmean` / `pvariance`, `np.var`, `np.expm1` / `np.log1p`, `scipy.special.logsumexp`, `np.linalg.lstsq` / `solve` / QR / SVD, `np.linalg.cond` |
| **TS / JS** | mathjs, simple-statistics, ml-matrix, @tensorflow/tfjs, ndarray | `BigInt` scaled integers, a Kahan reference | a compensated or pairwise sum, Welford, `Math.expm1` / `Math.log1p`, a max-shifted softmax |
| **Go** | gonum | `math/big.Float` with raised precision | `gonum/floats.Sum` (read its algorithm), `gonum/stat`, `gonum/mat` solves |
| **JVM** | Apache Commons Math | `BigDecimal` with a `MathContext` | Commons Math `stat.descriptive.moment.Variance` (read the version's algorithm), `QRDecomposition` |
| **.NET** | Math.NET Numerics | `decimal` for the reference only | Math.NET `Statistics`, `QR()` / `Svd()` solves |
| **Rust** | ndarray, nalgebra, statrs | `rug` / a compensated reference | a compensated sum, `nalgebra` QR / SVD |
| **C / C++ / Fortran** | BLAS / LAPACK (grep 5 reads the build) | long double or MPFR reference | LAPACK solvers, no explicit inverse; no `-ffast-math` on code that checks NaN or sums |
| **Sketches** (any stack) | RedisBloom (`BF.*`, `CF.*`, `CMS.*`, `TDIGEST.*`), Redis HLL (`PF*`), `bloom-filters`, `pybloom*`, `pyprobables` | a seeded fill at the stated n | `BF.RESERVE key p n`, HLL precision stated, CMS `INITBYPROB ε δ`; the exact check on every positive that decides money |

## Pre-flight

Run as **one** bash script from the repo root, with `ROOTS` set to the production source roots.
Grep **N** feeds detector **§N**; G is the gate. Every `rg` names its path (the gated greps pass
`/dev/null` so an empty file list never falls back to the working directory); every exit code is
printed, and an exit 2 fails the step instead of reading as zero hits. Nothing is written in the repo
and nothing touches the network.

```bash
set -u
declare -p ROOTS >/dev/null 2>&1 || ROOTS=(.)   # production source roots, e.g. ROOTS=(analytics src)
OUT="$(mktemp -d "${TMPDIR:-/tmp}/numeric-stability-scan.XXXXXX")"; RC=0
st() { printf '# %-3s rc=%s\n' "$1" "$2"; [ "$2" != 2 ] || RC=2; }   # rg: 0 hits, 1 none, 2 FAILED
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**'
   -g '!**/.venv/**' -g '!**/coverage/**' -g '!**/*.min.*' -g '!**/*.d.ts' -g '!**/*.{md,mdx,lock,map,svg,json,snap,yml,yaml,css,scss,html,ipynb}')
T=(-g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,seeds,seeders,migrations,locales,i18n,generated,__generated__,docs}/**'
   -g '!**/*.{spec,test,e2e-spec,stories,fuzz-spec,test-data,fixture,bench}.*' -g '!**/{*_test,*_spec,test_*,conftest}.*' -g '!ai/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')

# G. The gate. G1 numeric libraries in manifests; G2 the files that import one or call an anchored numeric function.
#    G1 = 0 and G2 = 0 → §1–§4 are `N/A (no numeric code: gate 0)`, never `checked`. Money libraries (decimal.js, big.js) are
#    not numeric code: money is code-quality's. Each count is printed so the gate's own noise is visible.
rg -n --no-heading --pcre2 '^\s*["\x27]?(?:numpy|scipy|pandas|polars|statsmodels|scikit-learn|torch|jax|jaxlib|tensorflow|numba|mpmath)\b|"(?:mathjs|simple-statistics|ml-matrix|@tensorflow/tfjs[\w-]*|ndarray)"\s*:|gonum\.org/v1/gonum|\bcommons-math3?\b|\b(?:ndarray|nalgebra|statrs)\s*=|MathNet\.Numerics|\bnumo-narray\b' -g 'package.json' -g 'pyproject.toml' -g 'requirements*.txt' -g 'setup.py' -g 'setup.cfg' -g 'environment.yml' -g 'go.mod' -g 'pom.xml' -g 'build.gradle*' -g 'Cargo.toml' -g '*.csproj' -g 'Gemfile' -g '!**/node_modules/**' .; st G1 $?
rg -l --pcre2 '^\s*(?:import|from)\s+(?:numpy|scipy|pandas|polars|statsmodels|sklearn|torch|jax|numba|mpmath|statistics)\b|(?:require\(\s*|from\s+)["\x27](?:mathjs|simple-statistics|ml-matrix|@tensorflow/tfjs[\w-]*)["\x27]|"gonum\.org/v1/gonum/\w+"|\bimport\s+org\.apache\.commons\.math3?\.|\busing\s+MathNet\.Numerics\b|\buse\s+(?:ndarray|nalgebra|statrs)\b|\b(?:np|numpy|scipy|jnp|torch)\.(?:linalg|var|std|cov|exp|log|prod)\b|\b(?:pvariance|pstdev|stdev|logsumexp|log_softmax|cholesky|lstsq|standardDeviation)\s*\(|\bsoftmax\s*\(|\b(?:variance|stddev|covariance)\s*\(\s*[\w.]+\s*\)' "${X[@]}" "${T[@]}" "${ROOTS[@]}" > "$OUT/num.txt"; st G2 $?
NUM=(); while IFS= read -r f; do NUM+=("$f"); done < "$OUT/num.txt"
printf 'gate: G1 manifest lines above · G2 %s numeric files (%s)\n' "${#NUM[@]}" "$OUT/num.txt"; [ "${#NUM[@]}" -gt 0 ] || echo '# §1–§4 N/A (no numeric code: gate 0) — the greps below search /dev/null only'

# 1–4 run only on the G2 files. 1a a running += in a loop (not a counter), 1b float32/float16 accumulators, 1c Python sum() of a
#    generator (no fsum), 1d a JS reduce sum; 2 cancellation shapes; 3 exp / products / factorials (read for a max shift or
#    log-space); 4 explicit inverses, normal equations, unbounded convergence loops — 4b lists the files with a cond / lstsq /
#    max-iteration guard (context for 4).
rg -H -n -U --pcre2 '^[ \t]*+for\b[^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*?\K\b[\w.\[\]]+\s*\+=\s*(?!1\b|\d+\s*$)[\w.(\[]' ${NUM[@]+"${NUM[@]}"} /dev/null | "${NC[@]}"; st 1a "${PIPESTATUS[0]}"
rg -H -n --pcre2 '\bnp\.float(?:16|32)\b|\bdtype\s*=\s*["\x27]?(?:np\.|torch\.)?(?:float16|float32|half|bfloat16)\b|\bFloat32Array\b|\btorch\.(?:float16|half|bfloat16)\b|\bf32\b' ${NUM[@]+"${NUM[@]}"} /dev/null | "${NC[@]}"; st 1b "${PIPESTATUS[0]}"
rg -H -n --pcre2 '(?<![\w.])sum\(\s*[^)\n]*\bfor\b|\bfunctools\.reduce\(\s*(?:operator\.add|lambda\s+\w+\s*,\s*\w+\s*:\s*\w+\s*\+)' ${NUM[@]+"${NUM[@]}"} /dev/null | "${NC[@]}"; st 1c "${PIPESTATUS[0]}"
rg -H -n --pcre2 '\.reduce\(\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)\s*=>\s*\1\s*\+\s*\2\b' ${NUM[@]+"${NUM[@]}"} /dev/null | "${NC[@]}"; st 1d "${PIPESTATUS[0]}"
rg -H -n --pcre2 '\b\w*(?:sumsq|sum_sq|sumSq|sumOfSquares|sum_of_squares|sumSquares)\w*\b|\*\*\s*2\s*\)\s*/\s*(?:n\b|len\()|\b1(?:\.0)?\s*-\s*(?:Math|np|math)\.cos\(|\b(?:Math|np|math)\.exp\([^)\n]*\)\s*-\s*1(?:\.0)?\b|\b(?:Math|np|math)\.log\(\s*1(?:\.0)?\s*\+|\bsqrt\(\s*\w+\s*\*\s*\w+\s*-\s*4|\b\w+\s*\*\*\s*2\s*-\s*4\s*\*' ${NUM[@]+"${NUM[@]}"} /dev/null | "${NC[@]}"; st 2 "${PIPESTATUS[0]}"
rg -H -n --pcre2 '\b(?:Math|np|math|torch|jnp)\.exp\(|\b(?:np|math|torch)\.prod\(|\.prod\(\s*\)|\breduce\([^\n]*\*|\bfactorial\(' ${NUM[@]+"${NUM[@]}"} /dev/null | "${NC[@]}"; st 3 "${PIPESTATUS[0]}"
rg -H -n --pcre2 '\blinalg\.inv\(|\.inverse\(\)|\binv\(\s*\w+\.T\b|\.T\s*@\s*\w+\s*\)|\bsolve\(\s*\w+\.T\s*@|\bwhile\s*\(?\s*(?:abs\()?[\w.]*(?:err|error|delta|diff|residual|change)\w*\)?\s*>' ${NUM[@]+"${NUM[@]}"} /dev/null | "${NC[@]}"; st 4 "${PIPESTATUS[0]}"
rg -H -l --pcre2 '\bcond\(|\blstsq\(|\bmax_?iter\w*\b|\bmaxiter\b|\bmax_iterations\b' ${NUM[@]+"${NUM[@]}"} /dev/null; st 4b $?

# 5. NS-5 IEEE-voiding build and JIT flags in every build file and decorator (its own gate: a flag IS numeric code).
rg -n --pcre2 '(?:-ffast-math\b|-Ofast\b|-funsafe-math-optimizations\b|-fassociative-math\b|-ffinite-math-only\b|\bfastmath\s*=\s*(?:True|\{)|/fp:fast\b|<FloatingPointModel>\s*Fast\b)' "${X[@]}" -g '!**/node_modules/**' .; st 5 $?

# 6. SL-1 probabilistic structures (their own gate) and 7. SL-2 the decision words in the same files (charge, send, quota…).
rg -n --pcre2 '\bBF\.(?:RESERVE|ADD|MADD|EXISTS|MEXISTS)\b|\bBloomFilter\b|\bbloom-filters\b|\bpybloom\w*|\bpyprobables\b|\bHyperLogLog\b|\bPF(?:ADD|COUNT|MERGE)\b|\bpf(?:add|count|merge)\(|\bCountMinSketch\b|\bCMS\.(?:INITBYDIM|INITBYPROB|INCRBY|QUERY)\b|\bTDigest\b|\bTDIGEST\.\w+|\bt-digest\b|\bCF\.(?:RESERVE|ADD|EXISTS)\b|\bCuckooFilter\b' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | "${NC[@]}"; st 6 "${PIPESTATUS[0]}"
rg -l --pcre2 '\bBF\.(?:ADD|EXISTS|MEXISTS)\b|\bBloomFilter\b|\bHyperLogLog\b|\bPFCOUNT\b|\bpfcount\(|\bCountMinSketch\b|\bCMS\.QUERY\b|\bCF\.EXISTS\b|\bCuckooFilter\b' "${X[@]}" "${T[@]}" "${ROOTS[@]}" > "$OUT/sk.txt"; st 7a $?
SK=(); while IFS= read -r f; do SK+=("$f"); done < "$OUT/sk.txt"
rg -H -n --pcre2 '(?i)\b(?:charge|refund|invoice|bill(?:ing)?|quota|rate.?limit|send|notify|dedupe|already|is_?seen|has_?seen|exists)\b' ${SK[@]+"${SK[@]}"} /dev/null | "${NC[@]}"; st 7b "${PIPESTATUS[0]}"
echo "# pre-flight exit $RC"; [ "$RC" -eq 0 ]
```

A finding is a hit **plus** a read of the computation **plus** the data's count and magnitude range
**plus** the tolerance its consumer needs. Two blind spots are structural:

- **Vectorised code hides the loop.** `df.groupby(...).agg('var')`, `X.T @ X`, a `torch` reduction:
  the precision regime is the library's. Read which algorithm the call uses at the pinned version
  (pairwise, Welford, BLAS) before reporting, and report the call that bypasses it (a manual sum,
  `astype(float32)` before a reduction).
- **The gate misses hand-rolled numeric code with no library and no anchored name.** A file that
  computes a regression with plain loops and calls nothing named `variance` passes the gate at 0.
  When the product is analytics, scoring or simulation by its own description, add its roots by hand
  and say so in the coverage block.

**Measured** (2026-10-19, read-only) on a real NestJS 11 + MikroORM 6 + React monorepo,
`ROOTS=(apps/api/src apps/web/src packages/contracts/src)`, 6,930 TS files: G1 0, G2 0 (its
"variance" is a signed inventory count in integer units and never called as a numeric function), so
§1–§4 are `N/A (gate 0)`; grep 5 0, grep 6 0 (five `count.?min` matches of the old pattern were
`itemsCount.min`), grep 7 0. On the 28 other `benchmarks/fixtures` the gate is 0 and greps 5–7
return nothing — the old gate matched 20 of 24 of them. On `algo-defects` (2026-10-19, staged without
its key; 0.1 s; no `rg` exit 2): G1 4 manifest lines, G2 7 files — every one holds a numeric seed or
the JIT kernels, none is a CRUD file — and all 14 seeds print: 1a 4 (two seeds, two running sums
inside other seeds' functions), 1b 1, 2 4, 3 2, 4 2 (4b lists no `cond`, `lstsq` or iteration bound),
5 2, 6 10 (four sketch seeds plus imports and a manifest line), 7b 2. **NOT-MEASURED on a real
numeric repo:** no scientific, analytics, geo or streaming repository is in the program's allowed set,
so every lane of this skill is measured on the fixture and a synthetic sample only (one instance per
class); every grep fired on its shape. Treat the noise figures as unknown until a real numeric repo is
measured.

## The 3,000-hit path

1. **Confirm the gate is honest.** Read the G2 file list first; drop a file whose only match is a
   word in a comment or a non-numeric function, and record the count dropped.
2. **Group by computation, not by line.** One accumulator, one variance routine, one solver, one
   sketch per group; a helper called from many places is read once.
3. **Rank by consumer.** A persisted, billed or reported number first; a model feature second; a
   display value last.
4. **Prefer the oracle at scale.** Run V608's reference over the module's own test inputs with the
   adversarial vectors added; every function outside tolerance is confirmed in one run.
5. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the grep that continues them.

## Scans for

| § | Class | CWE | Default severity |
|---|---|---|---|
| 1 | NS-1 naive accumulation of many or mixed-magnitude floats into a reported value | CWE-1339 | medium |
| 2 | NS-2 catastrophic cancellation | CWE-1339 | medium |
| 3 | NS-3 overflow or underflow where log-space is needed | CWE-190, CWE-1339 | medium |
| 4 | NS-4 conditioning ignored; iteration without a bound | CWE-1339, CWE-835 | medium |
| 5 | NS-5 build or JIT flags that void IEEE semantics | CWE-1339 | medium |
| 6 | SL-1 sketch with no stated parameters or error | CWE-1339 | low |
| 7 | SL-2 approximate structure used as the authority for an exact decision | CWE-697 | high |

### 1. Naive accumulation (NS-1)

```
BAD:   total = 0.0; for x in xs: total += x          # 10^7 terms of mixed magnitude
       acc = np.zeros(n, dtype=np.float32); acc += batch   # float32 running total
GOOD:  math.fsum(xs) · np.sum(xs) (pairwise) · a Kahan / Neumaier sum · accumulate in float64, store float32
```
**Read the code:** How many terms, over what magnitude range? Does the consumer compare, threshold or
report the total? Is the library call already pairwise or compensated (§ 36)? Is it integer minor
units (§ 37) or inference with a stated tolerance (§ 38)? **Finding when** the term count or range
makes the error exceed the consumer's tolerance. **Proof:** V608 with (1e16, 1, −1e16) and a
10^6-term mixed-magnitude series.

### 2. Catastrophic cancellation (NS-2)

```
BAD:   var = (sumsq - s * s / n) / n   ·   1 - Math.cos(x) for small x   ·   (-b + Math.sqrt(b*b - 4*a*c)) / (2*a) when b² ≫ 4ac
       Math.exp(x) - 1 · Math.log(1 + x) for |x| ≪ 1
GOOD:  Welford (one pass) or np.var / statistics.pvariance · 2 * Math.sin(x / 2) ** 2 · the stable root, then c / (a * x1)
       Math.expm1(x) · Math.log1p(x)
```
**Read the code:** Can the operands be nearly equal — a mean of 1e9 with a spread of 1, a small angle,
`b² ≫ 4ac`? **Finding when** the data makes the subtraction lose more digits than the result can
spare. **Proof:** V608 with a mean of 1e9 and a spread of 1.

### 3. Overflow and underflow (NS-3)

```
BAD:   e = np.exp(z); p = e / e.sum()        # z ≥ 710 → inf; NaN after the division
       likelihood = probs.reduce((a, p) => a * p, 1)   // 400 factors of 1e-3 → 0
GOOD:  np.exp(z - z.max()) · scipy.special.logsumexp · sum of logs · lgamma for factorial ratios
```
**Read the code:** What range can the inputs reach (logits, scores, counts)? How many factors in the
product? **Proof:** V608 with logits of 1,000 and a product of 400 terms of 1e-3.

### 4. Conditioning ignored; unbounded iteration (NS-4)

```
BAD:   beta = np.linalg.inv(X.T @ X) @ X.T @ y           # squares the condition number
       while err > 1e-9: x = step(x); err = abs(f(x))     # no max-iteration; an absolute tolerance only
GOOD:  np.linalg.lstsq(X, y) (or QR / SVD), with np.linalg.cond(X) checked · for i in range(MAX_ITER): … relative + absolute tolerance
```
Grep 4b lists the files that already compute `cond`, call `lstsq` or bound iterations. **Read the
code:** Can the matrix be ill-conditioned (collinear features, a Vandermonde, units mixed)? Can the
iteration stall? **Proof:** V608 (`cond` computed; a Hilbert matrix; the loop stops at max-iteration).

### 5. IEEE-voiding flags (NS-5)

```
BAD:   set(CMAKE_CXX_FLAGS "-O3 -ffast-math") · @numba.jit(fastmath=True) on code that tests isnan or sums · /fp:fast
GOOD:  no flag on numeric code that checks NaN, Inf or ordering; a narrower flag (-fno-math-errno) where a benchmark justifies it
```
**Read the code:** Does the flagged build compile the numeric code that ships? Does that code test
NaN/Inf or depend on summation order? **Proof:** V609 (the flag in the shipped build, two-ended with
the code it compiles).

### 6. Sketch with no stated error (SL-1)

```
BAD:   new BloomFilter(1000, 4)   // which n, which false-positive rate?   · PFADD with no precision noted · CMS with no ε / δ
GOOD:  BF.RESERVE key 0.001 1000000 (p and n stated, the resulting error documented) · CMS.INITBYPROB key 0.001 0.01
```
**Read the code:** What n does it really see (traffic, rows), against the sizing? Is the error
documented where the number is read? A sketch at a small n where the exact set is cheap is
performance's memory question. **Proof:** V609 (a seeded fill at the stated n; the measured error).

### 7. Approximate structure as an exact authority (SL-2)

```
BAD:   if (await bloom.has(paymentId)) return;  await charge(paymentId)   // a false positive skips a real charge
       quotaUsed = await redis.pfcount(key)  // HLL count enforces a billed quota
GOOD:  the sketch as a negative pre-filter only, every positive confirmed against the source of truth (§ 39)
       an exact counter (a row, an atomic increment) for anything billed or enforced
```
**Read the code:** What does a positive decide — a skipped charge, a skipped send, a blocked user, a
bill? Is there an exact check behind it? A dashboard "about" figure is § 40. **Finding when** a
sketch answer alone decides money, a send or a quota. **Proof:** V609 (the spy shows no exact check on
the positive path).

## Output

```
numeric-stability-scan — gate: G1 3 manifest lines (numpy 2.3, pandas 2.3, scipy 1.16), G2 41 numeric files; lanes: python
Context: 4b — 2 files compute cond / call lstsq

Findings: 1 · Unconfirmed: 1

1. analytics/kpis/volatility.py:37                               [report-with-fix]   medium
   §2 cancellation — var = (sumsq - s*s/n)/n over daily revenue in minor units (mean ≈ 4e8, spread
   ≈ 2e3); the dashboard thresholds volatility at 0.5 %. Reached by the nightly kpi job.
   Proof: tests/kpis/test_volatility_precision.py — relative error 3.1e-2 vs statistics.pvariance
   (fails at 1e-6). Fix: statistics.pvariance (or Welford).

2. services/notify/dedupe.ts:14                                  [report-flagged]    high
   §7 sketch as authority — BF.EXISTS skips the send when the Bloom filter says "seen"; no exact
   check behind it. Unproven link: the filter's p and n (BF.RESERVE is in an ops script, not the
   repo). Settling test (V609): fill to the stated n, query n fresh ids, count skipped sends.

Verification: 5 candidates → 1 finding · 1 unconfirmed · 2 hardening · 1 refuted

Class coverage:
  §1  accumulation           checked (6 hits / 41 files → 0: np.sum and fsum, § 36)
  §2  cancellation           checked (2 hits → 1 finding)
  §3  overflow / log-space   checked (4 hits → 0: max-shifted)
  §4  conditioning           checked (1 hit → 0: lstsq with cond)
  §5  IEEE-voiding flags     checked (0 hits)
  §6  sketch error stated    checked (1 hit → hardening: p and n not in the repo)
  §7  sketch as authority    checked (1 hit → 1 unconfirmed)
```

On a repo with no numeric code the header reads `gate: G1 0, G2 0` and §1–§4 read
`N/A (no numeric code: gate 0)`. `[report-with-fix]`: the data's regime and the consumer's
tolerance are cited, the reference test failed, and the fix uses a stable primitive.
`[report-flagged]`: one link is unproven (the tolerance, the sizing, a build that may not ship), and
the row names it and the settling test. The coverage block lists **all seven** classes on every run;
a class whose grep exited 2 is `blocked`; a partial review reads `Live, unreviewed (k groups / n
hits)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/algorithms.md`](../../../../snippets/precedents/algorithms.md)
(§ 36–§ 40 for this skill) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md)
§ 4: pairwise or compensated library reductions (§ 36), integer minor units (§ 37), float32 inference
with a stated tolerance (§ 38), a sketch used as a negative pre-filter (§ 39), an approximate count
labelled approximate (§ 40).

## When to run

- On any diff in a gated file (grep G2), any build file that sets compiler or JIT flags, or any code
  that creates or reads a Bloom filter, HyperLogLog, Count-Min sketch, cuckoo filter or t-digest —
  the `/analyze-complexity` dispatch signal.
- On every whole-repo `/analyze-complexity`, reporting all seven classes (§1–§4 as `N/A (gate 0)` when
  the gate is 0).

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed
  it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 1–§ 8. Under
  `/analyze-complexity` that is `@algorithm-designer` in refute mode plus `@verifier`; run standalone,
  apply the protocol as a separate second pass and tag those rows `self-verified`. Never drop them.
- Halt when any `rg` exits 2: the class it feeds is `blocked`, never `checked`. Never print §1–§4 as
  `checked` when the gate is 0.
- Halt on any finding without the computation `<file:line>`, the data's regime, the consumer's
  tolerance (or `[report-flagged]` with the question), the entry point and the fix.
- Do not mark a row `[report-with-fix]` without a reference test that failed first, or the two-ended
  static fact for a flag.
- Do not propose "use double", "use Decimal everywhere" or a bigger tolerance as the fix; name the
  stable algorithm. Money is never fixed here (§ Boundaries).
- Do not print "no numeric defect" without the gate line and the class-coverage block.

## Related

- `/analyze-complexity` dispatches this skill with `complexity-scan` and `algorithm-contract-scan`;
  `/design-algorithm --from-audit` closes its findings with V608 / V609.
- `ai-patterns/numerical-methods.md` and `ai-patterns/sublinear-structures.md` (this pack) are the
  design patterns this skill enforces; `complexity-derivation` states the cost of the stable variant.
- `correctness-smell-scan` §2 and §4 (code-quality pack, when installed) own float equality and
  money arithmetic; `memory-growth-scan` §1 (performance pack, when installed) owns an exact set that
  grows forever.
