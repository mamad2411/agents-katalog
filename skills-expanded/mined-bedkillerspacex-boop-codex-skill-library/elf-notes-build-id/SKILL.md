---
name: elf-notes-build-id
description: >
  ELF build-id notes for owned/lab binaries: NT_GNU_BUILD_ID, readelf/eu-unstrip
  workflows, matching debuginfo packages, and symbol server pipelines. Use when
  .note.gnu.build-id, debuginfod, split DWARF, or correlating crash stacks to
  exact builds—not general dynamic linking (see elf-dynamic-linking-basics).
---

# ELF Notes Build-ID

## Scope And Authorization

- **In scope:** Binaries, core dumps, and debuginfo stores you own or are authorized to analyze.
- **Out of scope:** Pulling proprietary debug symbols from third parties without license/authorization.
- Build-ids are not secrets, but paired debuginfo can expose source paths and internals—control access.
- Keep crash dumps with PII under retention policy.
- Pair production profiling with `ebpf-profiler-prod` symbolization needs.

## When To Use

- Matching a stripped production binary to the correct `debuginfo` RPM/deb or symbol bundle.
- Setting up CI to publish build-id → symbols for profilers and crash reporters.
- Explaining `.note.gnu.build-id` vs filename versioning.
- Recovering symbols for a core file from a fleet of historical builds.
- Verifying two artifacts are the same build via identical build-id.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Dynamic linker / RPATH / PLT | `elf-dynamic-linking-basics` |
| Continuous eBPF profiling ops | `ebpf-profiler-prod` |
| Full static malware RE | `binary-re/static-analysis` |
| Implementation quality baseline | `code-quality-standards` |
| Generic documentation process | markdown/docs skills |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Note section | `NT_GNU_BUILD_ID` usually SHA1 of link inputs |
| Strip | Build-id remains in stripped main binary |
| Debuginfo | Separate package named by build-id path layout |
| debuginfod | HTTP fetch of symbols by build-id |
| Tooling | `readelf -n`, `file`, `eu-unstrip`, `gdb` |
| CI | Upload symbols after build; retain by build-id |

## Workflow

### 1. Confirm scope and success criteria

1. Binary/core dump origin and whether debuginfo is available internally.
2. Success: extract build-id; locate matching symbols; produce usable backtrace.

### 2. Extract build-id

```bash
file ./myapp
readelf -n ./myapp | grep -A1 'Build ID'
# Often also:
#   eu-readelf -n ./myapp
#   file shows 'BuildID[sha1]=...'
```

1. Record full hex build-id string.
2. Confirm presence after `strip`—should remain unless intentionally removed.

### 3. Baseline without symbols

```bash
gdb -batch -ex "bt" ./myapp core 2>/dev/null | head
# or llvm-symbolizer with addresses if available
```

1. Note frames that are only addresses / `??`.
2. Capture module load addresses if ASLR matters for offline symbolization.

### 4. Locate debuginfo by build-id layout

Typical on-disk layout (distro/debuginfod style):

```text
/usr/lib/debug/.build-id/ab/cdef0123...89.debug
```

```bash
BUILD_ID=$(readelf -n ./myapp | awk '/Build ID/ {print $3}')
PREFIX=${BUILD_ID:0:2}
REST=${BUILD_ID:2}
ls -l /usr/lib/debug/.build-id/$PREFIX/$REST* 2>/dev/null
# Fedora/RHEL style packages often provide these paths
```

1. For project CI, store `symbols/$PREFIX/$REST.debug` or upload to debuginfod-compatible store.
2. Ensure link step emits build-id: modern `gcc`/`clang` default on many platforms (`-Wl,--build-id`).

### 5. Wire CI symbol publish

```bash
# After cargo/go/c++ release build (illustrative)
BUILD_ID=$(readelf -n target/release/myapp | awk '/Build ID/ {print $3}')
mkdir -p "artifacts/build-id/${BUILD_ID:0:2}"
cp target/release/myapp "artifacts/build-id/${BUILD_ID:0:2}/${BUILD_ID:2}"
# Keep unstripped or .debug companion for symbol server
objcopy --only-keep-debug target/release/myapp "artifacts/build-id/${BUILD_ID:0:2}/${BUILD_ID:2}.debug"
objcopy --strip-debug target/release/myapp
objcopy --add-gnu-debuglink="artifacts/build-id/${BUILD_ID:0:2}/${BUILD_ID:2}.debug" target/release/myapp
```

1. Never delete symbols for builds still in production crash retention window.
2. Profilers (Parca, etc.) need the same build-id pipeline.

### 6. Verify with evidence

```bash
gdb -ex "set debug-file-directory /usr/lib/debug" -ex "bt" -batch ./myapp core | head
# Or debuginfod
export DEBUGINFOD_URLS="https://debuginfod.example.internal/"
gdb ./myapp core
```

1. Confirm frames resolve to file:line for a known crash.
2. Confirm two “identical version tags” with **different** build-ids are not mixed.

### 7. Hand off

1. Document symbol retention TTL vs release TTL.
2. Access control on symbol server (internal only if source paths sensitive).
3. Cross-link packaging so release digests and build-ids appear in SBOM/release notes.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Identity | build-id as primary key | Only `version: 1.2.3` tag |
| Strip | Keep note + external debug | `strip` removes all notes |
| Storage | build-id directory layout | Random zip names without index |
| Privacy | Restrict debuginfo access | Public symbols for private source |
| Matching | Verify id before analysis | Guess “closest” version |

## Output Checklist

- [ ] Build-id extracted from binary (and core’s modules if needed)
- [ ] Matching debuginfo located or gap recorded
- [ ] Symbolized backtrace evidence captured
- [ ] CI publish path documented for new builds
- [ ] Retention and access policy noted
- [ ] Link to profiler/crash systems using the same ids
- [ ] Residual risk (missing historical symbols) noted

## Rules

- Authorized binaries and symbol stores only.
- Do not strip build-id notes from production builds.
- Treat debuginfo as sensitive when it embeds paths or proprietary code.
- Prefer build-id over version strings for exact matching.
- Dynamic linking issues → `elf-dynamic-linking-basics`.
