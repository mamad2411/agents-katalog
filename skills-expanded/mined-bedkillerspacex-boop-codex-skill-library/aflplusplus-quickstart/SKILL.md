---
name: aflplusplus-quickstart
description: >
  AFL++ fuzzing campaign quickstart for owned targets and labs: build instrumentation,
  seeds, dictionaries, parallel fuzzing, crash triage, and corpus minimization. Use when
  starting AFL++ on C/C++ (or qemu/unicorn modes) parsers and file/network codecs —
  not for unauthorized fuzzing of third-party production systems.
---

# AFL++ Quickstart

## Scope And Authorization

- **In scope:** software you own, open-source under local build, CTF/lab binaries, vendor code under contract.
- **Out of scope:** fuzzing remote production without approval; weaponizing crashes against third parties.
- Run campaigns in isolated VMs/containers with resource caps.
- Treat crash inputs as potentially malicious; do not open in privileged apps casually.
- Pair harness code with `code-quality-standards`.

## When To Use

- First AFL++ campaign on a library API or CLI parser.
- Switching from libFuzzer harnesses to persistent AFL++ mode.
- Building seed corpus + dictionary for structured formats.
- Parallel campaigns (`-M`/`-S`) and triage with `afl-tmin` / `afl-analyze`.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Ghidra/IDA crash analysis | `Ghidra_IDAReverseEngineeringSkill` / `binary-re/static-analysis` |
| Network protocol fuzz design | `NetworkProtocolAnalysisSkill` |
| General security test planning | `recon-and-methodology` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Component | Role |
| --- | --- |
| `afl-clang-fast` / `afl-cc` | Compile-time instrumentation |
| `afl-fuzz` | Mutation fuzzer driver |
| Seeds (`-i`) | Initial corpus |
| Dictionary (`-x`) | Tokens for structured inputs |
| Persistent mode | `__AFL_LOOP` in-process speed |
| ASAN/UBSAN builds | Detection companion binaries |
| CMplog / LAF | Compare / hard path helpers (version features) |

## Workflow

### 1. Confirm target and success criteria

1. Record target function (file parse, packet decode), build system, sanitizer plan.
2. Success: stable execs/s; first coverage growth; unique crashes bucketed; minimized repros.
3. Choose mode: source instrumentation (preferred) vs QEMU (`-Q`) vs Unicorn.

### 2. Write a harness

```c
// harness.c — stdin or AFL persistent
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

extern int parse_buffer(const uint8_t *data, size_t len);

int main(void) {
#ifdef __AFL_HAVE_MANUAL_CONTROL
  __AFL_INIT();
#endif
  unsigned char *buf = NULL;
  size_t len = 0;
#ifdef __AFL_LOOP
  while (__AFL_LOOP(1000)) {
    // re-read input each loop in persistent template variants
#endif
    // simple non-persistent: read file/stdin once
    uint8_t data[4096];
    size_t n = fread(data, 1, sizeof(data), stdin);
    parse_buffer(data, n);
#ifdef __AFL_LOOP
  }
#endif
  return 0;
}
```

Prefer official AFL++ persistent templates for production campaigns.

### 3. Build instrumented binary

```bash
export AFL_PATH=/path/to/AFLplusplus
export CC=afl-clang-fast
export CXX=afl-clang-fast++
# Optional hardening for crash quality
export AFL_USE_ASAN=1   # separate build often better than combining all sanitizers

./configure --disable-shared
make clean && make -j"$(nproc)"
# Build harness linked with target lib
afl-clang-fast -o fuzz_harness harness.c -L. -ltarget
```

1. Verify instrumentation: `afl-fuzz` should not warn “no instrumentation.”
2. Keep an **ASAN** binary for triage, not always for the main fuzzer speed path.

### 4. Seeds and dictionary

```bash
mkdir -p seeds
cp tests/samples/*.bin seeds/
# Optional: afl-cmin to minimize seed set
afl-cmin -i seeds -o seeds_min -- ./fuzz_harness @@

# dictionary example (png-like)
cat > format.dict <<'EOF'
header="\x89PNG"
chunk="IHDR"
EOF
```

1. Seeds should be **valid-ish** tiny files covering features.
2. Dictionaries help magic bytes and keywords.

### 5. Run AFL++

```bash
mkdir -p out
# Single node
afl-fuzz -i seeds_min -o out -x format.dict -- ./fuzz_harness @@

# Parallel: main + secondaries
afl-fuzz -i seeds_min -o out -M main -- ./fuzz_harness @@
afl-fuzz -i seeds_min -o out -S s1 -- ./fuzz_harness @@
```

| Flag | Meaning |
| --- | --- |
| `@@` | Input file path substitution |
| `-t` | Timeout ms |
| `-m` | Memory limit |
| `-V` | Time budget seconds (campaign cap) |

### 6. Triage crashes

```bash
ls out/default/crashes/   # or out/main/crashes
# Reproduce
./fuzz_harness < out/default/crashes/id:000000,*
# Or ASAN build
./fuzz_harness_asan < crash_file

afl-tmin -i crash_file -o crash.min -- ./fuzz_harness @@
afl-analyze -i crash.min -- ./fuzz_harness @@
```

1. Deduplicate by stack hash under ASAN.
2. File bugs with minimized input + build commit + sanitizer log.
3. Do not commit huge corpora to git; use artifact storage.

### 7. Hand off

1. Document harness, seeds origin, AFL++ version, campaign duration, coverage notes.
2. Add crashing tests to CI unit tests when fixed.
3. Plan continuous fuzzing (ClusterFuzz/OSS-Fuzz style) if long-term.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Harness | Small deterministic parse API | Full GUI app undeterministic |
| Seeds | Valid mini corpus | Empty + only random |
| Build | Clean afl-cc instrumentation | Strips coverage |
| Crashes | Minimized + ASAN stack | “It crashed once” without repro |
| Scope | Local owned binary | Unapproved remote prod |

## Output Checklist

- [ ] Authorization and isolation recorded
- [ ] Harness targets pure parse path
- [ ] Instrumented build verified
- [ ] Seeds (+ optional dict) prepared; cmin considered
- [ ] Campaign run with stable execs/s
- [ ] Crashes reproduced and minimized
- [ ] Fixes + regression tests planned
- [ ] AFL++ version and commands documented
- [ ] `code-quality-standards` on harness

## Rules

- Authorized targets only; isolate campaigns.
- Prefer source instrumentation over blind remote fuzzing.
- Minimize and file repros; do not hoard exploit-only notes without fixes for owned code.
- Cap resources; monitor disk for `hangs/` and `crashes/`.
- Never fuzz third-party production services as a “quickstart.”
