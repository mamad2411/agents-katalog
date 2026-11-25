---
name: elf-dynamic-linking-basics
description: >
  Explain and inspect ELF dynamic linking on owned/lab Linux binaries: DT_NEEDED,
  rpath/runpath, symbol resolution order, PLT/GOT, ld.so search path, and
  LD_PRELOAD risks. Use when debugging shared library load failures, reviewing
  binary supply-chain linkage, or teaching dynamic linker behavior—not for
  unauthorized host modification.
---

# ELF Dynamic Linking Basics

## Scope And Authorization

- **In scope:** Binaries and hosts you own, CTF/lab samples, or authorized RE engagements.
- **Out of scope:** Planting `LD_PRELOAD` on multi-user production hosts without change control; attacking third-party systems.
- Prefer read-only inspection (`readelf`, `ldd`, `objdump`) before any loader experiments.
- Redact absolute paths that reveal internal product names if reports leave the org.
- Pair exploit-oriented RE with dedicated binary-re skills; this skill is foundational linking literacy.

## When To Use

- `error while loading shared libraries` / wrong `.so` version at runtime.
- Understanding why a symbol resolves to an unexpected library.
- Auditing `RPATH`/`RUNPATH`, setuid + `LD_*` interactions, and preload surfaces.
- Mapping PLT/GOT for reverse engineering or debugging.
- Reviewing container images for library search-path surprises.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| ELF build-id / notes for symbol servers | `elf-notes-build-id` |
| Full static RE / decompilation workflow | `binary-re/static-analysis` |
| Linux privilege escalation via linker | `linux-privilege-escalation` (authorized only) |
| eBPF tracing of syscalls | `ebpf-observability-basics` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| DT_NEEDED | Direct shared deps recorded in dynamic section |
| Search order | RUNPATH/RPATH, `LD_LIBRARY_PATH`, ld cache, defaults |
| PLT/GOT | Lazy binding of imported functions (unless BIND_NOW) |
| Preload | `LD_PRELOAD` / `/etc/ld.so.preload` interposition |
| Security | setuid ignores many `LD_*`; still audit RPATH to writable dirs |
| Tools | `readelf -d`, `ldd`, `LD_DEBUG`, `patchelf` (owned bins) |

## Workflow

### 1. Confirm scope and success criteria

1. Target binary path, architecture, and whether setuid/setgid.
2. Success: explain load graph; fix missing/wrong library; document preload risks.

### 2. Inventory file type and dynamic section

```bash
file ./myapp
readelf -h ./myapp | head
readelf -d ./myapp | grep -E 'NEEDED|RPATH|RUNPATH|SONAME|FLAGS'
```

1. List `NEEDED` entries (e.g. `libssl.so.3`).
2. Note `RPATH` vs `RUNPATH` (RUNPATH allows `LD_LIBRARY_PATH` override semantics differences).

### 3. Baseline resolution

```bash
ldd ./myapp
# More verbose loader trace (stderr noisy)
LD_DEBUG=libs,files ./myapp --help 2>&1 | head -n 80
```

1. Highlight `not found` lines and any libraries resolved from unexpected directories.
2. Compare with `ldconfig -p | grep libname` on the host.

### 4. Explain symbol binding (PLT/GOT)

```bash
objdump -T ./myapp | head
objdump -R ./myapp | head          # relocations
readelf -r ./myapp | head
# Disassemble a PLT stub if needed
objdump -d ./myapp | grep -A3 '<printf@plt>'
```

1. Imports typically go through PLT; GOT holds resolved addresses after bind.
2. `DF_BIND_NOW` / `LD_BIND_NOW` forces eager binding (useful for RELRO completeness discussions).
3. For RE, track which library provides a symbol: `nm -D /path/lib.so | grep sym`.

### 5. Assess LD_PRELOAD and path risks

```bash
# Lab only: demonstrate interposition on a non-setuid binary
# LD_PRELOAD=./libhook.so ./myapp
echo "preload file (host):"; cat /etc/ld.so.preload 2>/dev/null || echo none
```

| Check | Why |
| --- | --- |
| RPATH to `$ORIGIN/../lib` | Good if libs shipped with app and dirs non-writable by others |
| RPATH to `/tmp` or world-writable | Library plant risk |
| setuid binary | Many env overrides ignored—still review companion scripts |
| `ld.so.preload` | Host-wide interposition—requires root to edit |

### 6. Fix load failures (owned builds)

```bash
# Prefer correct packaging over global LD_LIBRARY_PATH hacks
# Example: embed runpath at link time
# gcc -Wl,-rpath,'$ORIGIN/../lib' ...
# Or patchelf on owned binary:
# patchelf --set-rpath '$ORIGIN/../lib' ./myapp
```

1. Ship matching SONAME versions with the application when distro libs differ.
2. In containers, install distro packages instead of copying random `.so` from build hosts.
3. Document glibc compatibility constraints.

### 7. Hand off

1. Record final `readelf -d` + `ldd` evidence.
2. Note any intentional preload (profilers, sanitizers) with owner.
3. Link `elf-notes-build-id` if correlating build ids with debug symbols.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Shipping libs | `$ORIGIN`-relative RUNPATH | Copying `.so` over system paths |
| Debug | `LD_DEBUG` on owned bin | Exporting `LD_PRELOAD` globally on prod |
| Analysis | readelf/ldd evidence | Guessing from `strings` only |
| Security | No writable RPATH entries | RPATH=/var/tmp/lib |
| setuid | Minimal env; careful packaging | Force `LD_LIBRARY_PATH` hacks |

## Output Checklist

- [ ] Binary type and dynamic section captured
- [ ] NEEDED and RPATH/RUNPATH documented
- [ ] `ldd` / resolution order understood
- [ ] PLT/GOT explanation tied to observed imports
- [ ] Preload and writable-path risks reviewed
- [ ] Fix applied or residual load risk noted
- [ ] Evidence commands retained (redacted paths ok)

## Rules

- Authorized binaries/hosts only for invasive experiments.
- Prefer inspection over modifying system linker config.
- Do not recommend silent global preload as a product feature.
- Keep this skill on dynamic linking fundamentals; advanced exploitation routes to RE skills.
- Evidence over folklore about “how ld.so works.”
