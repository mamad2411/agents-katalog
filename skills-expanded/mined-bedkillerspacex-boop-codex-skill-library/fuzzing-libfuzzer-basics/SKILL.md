---
name: fuzzing-libfuzzer-basics
description: >
  Build and run libFuzzer harnesses for C/C++ (and similar) parsers: LLVMFuzzerTestOneInput,
  corpus design, sanitizers (ASan/UBSan), dictionaries, and crash triage. Use for owned
  libraries and authorized targets—not for networked fuzzing of third-party production
  without permission.
---

# Fuzzing LibFuzzer Basics

## Scope And Authorization

- **In scope:** code you own, open-source you may test, CTF/lab parsers under rules.
- **Out of scope:** unbounded fuzzing against remote production services you do not own.
- Run fuzzers in isolated VMs/containers; watch CPU/disk.
- Redact crash inputs if they contain secrets from corp corpora.
- Pair harness code with `code-quality-standards`.

## When To Use

- Coverage-guided fuzzing of **parse/decode** functions with libFuzzer.
- Finding memory safety issues with ASan/UBSan/MSan as supported.
- Building seed corpora and dictionaries for binary formats.
- Not for HTTP content discovery (`ffuf-fuzz-basics`) or recursive path brute (`feroxbuster-basics`).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| HTTP path fuzzing | `ffuf-fuzz-basics` |
| Format string CTF exploits | `format-string-exploitation` |
| Protocol capture RE | `protocol-reverse-engineering` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Piece | Role |
| --- | --- |
| Harness | `LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size)` |
| Engine | libFuzzer linked via clang `-fsanitize=fuzzer` |
| Sanitizers | `-fsanitize=address,undefined` commonly paired |
| Corpus | Directory of seed inputs; mutates & saves interesting |
| Dict | Tokens for structured formats |
| Artifact | Crash file for repro |

## Workflow

### 1. Confirm scope and success criteria

1. Target function purity (no network/random); library build flags.
2. Success: harness runs N hours; crashes reproduce with ASan logs; bugs filed with minimized input.
3. Resource limits: RSS, timeout per input.

### 2. Write a minimal harness

```cpp
// harness.cc
#include <stdint.h>
#include <stddef.h>
#include "mylib.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
  if (Size == 0 || Size > 1 << 20) return 0;  // optional guard
  mylib_parse(Data, Size);  // target: no exit(), no abort on expected errors
  return 0;
}
```

1. Target should accept invalid data without intentional `abort` on soft errors.
2. Avoid global state without reset; free allocations.

### 3. Build with sanitizers

```bash
clang++ -g -O1 -fsanitize=fuzzer,address,undefined \
  harness.cc mylib.cc -o fuzz_mylib
```

1. Match libstdc++/libc++ consistently.
2. For CMake, use `FUZZING` options or add custom target.

### 4. Corpus and dictionary

```bash
mkdir -p corpus
# add tiny valid files: corpus/seed1.bin
echo 'magic:"XXXX"' > my.dict   # format-specific tokens

./fuzz_mylib corpus -dict=my.dict -max_total_time=3600 -rss_limit_mb=2048
```

1. Seeds: smallest valid documents of each subtype.
2. Dictionaries: keywords, header magics, length field hints.

### 5. Triage crashes

```bash
./fuzz_mylib crash-XXXX  # single file repro
# Minimize
./fuzz_mylib -minimize_crash=1 crash-XXXX
```

1. File issue with: stack, sanitized log, minimized input, commit hash.
2. Fix root cause; add regression unit test from minimized blob.
3. Continue fuzzing after fix (coverage may deepen).

### 6. Verify with evidence

| Check | Evidence |
| --- | --- |
| Build | Binary runs `-help=1` |
| Seed acceptance | No instant ASan on all seeds |
| Campaign | stats: cov, exec/s, features |
| Repro | crash file deterministic under ASan |

### 7. Hand off

1. Document build flags, corpus location, known false positives.
2. CI: short smoke fuzz (seconds–minutes) optional; long runs on dedicated hardware.
3. Apply `code-quality-standards` for harness maintainability.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Target | In-process pure parse | Full HTTP client to prod |
| Seeds | Tiny valid set | Only empty corpus forever |
| Guards | Size caps | Unbounded huge allocs |
| Crashes | Minimized + fixed | Ignore non-repro flakes only |
| Scope | Owned lib | Random Internet service |
| Sanitizers | ASan+UBSan | None, “it crashed somewhere” |

## Output Checklist

- [ ] Target and authorization recorded
- [ ] Harness isolates pure API
- [ ] Sanitizer build works
- [ ] Corpus + optional dict prepared
- [ ] Time-boxed campaign run
- [ ] Crashes reproduced and filed
- [ ] Regression tests added for fixes
- [ ] CI/long-run plan noted
- [ ] `code-quality-standards` applied

## Rules

- Owned/authorized code; isolate fuzz infrastructure.
- Do not fuzz third-party production network endpoints as a substitute for libFuzzer.
- Prefer determinism and minimization for every crash.
- Keep harnesses free of intentional undefined behavior outside the target.
