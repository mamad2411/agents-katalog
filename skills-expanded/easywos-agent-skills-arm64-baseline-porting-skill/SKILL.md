---
name: arm64-baseline-porting
description: >-
  Fallback skill for porting x64 code to ARM64 when no specific spec matches.
  Provides mandatory architectural constraints that ALL ARM64 migrations must
  respect regardless of code pattern — covering both hand-written assembly and
  C/intrinsics output. Use when the dispatcher receives a porting_item with
  port_spec_ids: [] and mode=llm-freeform, OR when the LLM is producing freeform
  ARM64 output (C, intrinsics, or asm) without a more specific leaf skill.
  Ensures freeform porting still adheres to ARM64 correctness invariants:
  Windows ARM64 ABI, weak memory ordering, NEON 128-bit width limits, ARM64EC
  ABI shims, and intrinsic header / target-macro hygiene.
tags:
  - arm64
  - baseline
  - fallback
  - porting
  - constraints
  - arm64ec
  - memory-ordering
---

# ARM64 Baseline Porting Constraints

This skill provides the **minimum correctness guarantees** that every x64→ARM64
migration must satisfy, regardless of whether a specific migration spec matches.

When invoked via `/dispatcher-skill <id> --mode llm-freeform`, apply ALL rules
below before and during the porting attempt.

Sections **1–9** apply to hand-written ARM64 assembly output.
Sections **10–11** apply to **all** freeform output (asm or C/intrinsics).
Section **12** applies specifically to C/intrinsics output.
Section **13** is the verification gate — split by output language.

---

## 1. Calling Convention (Windows ARM64 ABI)

| Rule | Constraint |
|------|-----------|
| Integer arguments | X0–X7 (first 8 args), stack thereafter |
| Float arguments | D0–D7 (first 8 FP/SIMD args) |
| Return value | X0 (integer), D0 (float) |
| Callee-saved GPR | X19–X28, X29 (FP), X30 (LR) |
| Callee-saved SIMD | V8–V15 (lower 64 bits only) |
| Reserved register | X18 — TEB pointer on Windows, NEVER use as scratch |
| Frame pointer | X29 MUST be used as frame pointer when frame is present |

## 2. Stack Alignment

- SP MUST be 16-byte aligned at all times
- Stack allocation MUST use `SUB SP, SP, #N` where N is a multiple of 16
- Paired save/restore: use `STP`/`LDP` with pre-index or signed offset
- No red zone on Windows ARM64 — do not access below SP

## 3. Flag Discipline

- ARM64 arithmetic instructions (ADD, SUB) do NOT set flags by default
- MUST use flag-setting variants (ADDS, SUBS, CMP, TST) before any conditional branch
- Every B.cond MUST have an explicit flag-setting instruction preceding it
- No implicit flag setting from MOV, LDR, STR, or logical shifts

## 4. Immediate Encoding

- ADD/SUB: 12-bit immediate (0–4095), optionally shifted left by 12
- MOV: 16-bit immediate per MOVZ/MOVK; large constants need MOVZ+MOVK sequence
- Bitwise (AND/ORR/EOR): bitmask immediate (not arbitrary 64-bit values)
- If x64 code uses a large immediate, split via MOVZ/MOVK or load from literal pool

## 5. Memory Access

- Unaligned access: generally supported on ARM64 but slower; prefer aligned access
- No x86-style scaled-index `[base + index*scale + disp]` — use shifted register offset: `LDR X0, [X1, X2, LSL #3]`
- Maximum LDR/STR immediate offset: unsigned 12-bit scaled by access size
- For large offsets: compute address in a temp register first

## 6. SIMD / NEON Constraints

- Maximum native vector width: 128-bit (Q registers / V registers)
- No 256-bit or 512-bit native registers; split AVX/AVX-512 into multiple 128-bit ops
- Horizontal reduction across a full vector: prefer `ADDV` / `vaddvq_*` (full reduction). `FADDP` is **pairwise** only — use it only when you actually want pairwise behavior (e.g. iterative tree reduction)
- Movemask analogue: there is no direct `_mm_movemask_epi8`. Common replacements: `vaddvq_u8` on a comparison-mask vector with bit-weights, or `vshrn_n_u16` to compress mask lanes — choose per the matched intrinsic spec
- Use LD1/ST1 for potentially unaligned vector loads/stores
- Floating-point: IEEE 754 compliant; denormals may be flushed to zero depending on FPCR

## 7. Branch and Control Flow

| x64 | ARM64 | Notes |
|-----|-------|-------|
| JMP label | B label | Unconditional branch (±128 MB range) |
| JE/JZ | B.EQ | After CMP/SUBS/TST. **B.cond range is only ±1 MB** — for longer ranges use `B.cond skip; B target; skip:` trampoline |
| JNE/JNZ | B.NE | After CMP/SUBS/TST |
| JB/JC | B.LO (unsigned) | After CMP/SUBS |
| JA | B.HI (unsigned) | After CMP/SUBS |
| JL | B.LT (signed) | After CMP/SUBS |
| JG | B.GT (signed) | After CMP/SUBS |
| LOOP | SUBS + B.NE | No LOOP instruction; decrement + branch |
| CALL | BL | Saves return address in X30 (LR); ±128 MB range |
| RET | RET | Branches to address in X30 |

## 8. Prolog / Epilog Pattern

**Prolog template:**
```asm
STP X29, X30, [SP, #-frame_size]!   ; save FP + LR, allocate frame
MOV X29, SP                          ; establish frame pointer
STP X19, X20, [SP, #16]             ; save callee-saved registers
STP X21, X22, [SP, #32]             ; (as many pairs as needed)
```

**Epilog template:**
```asm
LDP X21, X22, [SP, #32]             ; restore callee-saved registers
LDP X19, X20, [SP, #16]
LDP X29, X30, [SP], #frame_size     ; restore FP + LR, deallocate frame
RET
```

## 9. Function Returns and Indirect Calls

- Return via `RET` (uses X30) — never by jumping to an address loaded from the stack
- Indirect call: `BLR Xn` (saves return in X30); indirect tail-call: `BR Xn`
- Pointer authentication (PAC) may be enabled — if so, use `PACIASP`/`AUTIASP` or `RETAA`/`RETAB` per project convention

## 9a. Register-Aliasing Hazards (the most common silent correctness/crash bug)

`Wn` and `Xn` are the **same physical register**; a 32-bit `Wn` write
**zero-extends** and destroys bits 63:32 of `Xn`. This single class of bug
recurs constantly in ported NEON kernels, as a wrong result or (more often) a
crash far from its cause:

- **In-function:** never load a narrow value into `Wn` (`LDRB Wn`, `ADD Wn,...`)
  while `Xn` still holds a live 64-bit pointer. Build addresses in a *different*
  register. (e.g. `LDRB W9,[X2]` then `ADD X9,X2,#1` loses the byte just loaded
  into W9 — use X10 for the pointer.)
- **Across a `BL`:** a helper must NOT return its result in, or scratch, a
  register whose `Xn`-form the caller keeps live across the call (a pointer it
  advances between calls). Return results in a dedicated clobber GPR (e.g.
  X9–X15), never X0 when X0 is a reused argument pointer. The fault PC lands at
  the caller's *next* load/store, not at the helper.
- A doc-comment like "returns in W0, preserves X0" is self-contradictory — W0 IS
  X0. Trust the register algebra.
- **SIMD analogue:** a `.2s`/`.4h`/`.8b`/`D`-form write **zeroes the upper 64
  bits** of the V register — don't reuse a `.4s` accumulator for a `D`-form tail.
- Small inputs / single-iteration paths mask it (the value is consumed before
  the clobbering reuse); exercise the looped/larger-size path.

## 9b. Stale Flags Before CSEL/CSET/B.cond

NZCV holds the result of the **most recent** flag-setting instruction, not the
one your condition name implies. A `CSEL ...,NE` placed after an intervening
`CMP`/`CSET`/branch selects on the *prior* comparison and compiles cleanly.
Re-establish flags with a fresh `CMP`/`TST` immediately before each conditional
select/set/branch whose condition differs from the last one set.

## 9c. Partial Loads Leave Stale Lanes

A narrow load (`LD1 {Vn.S}[0]`, `LDR Sn`/`Bn`) writes only the addressed lanes;
the rest of the register keeps stale contents. A later full-width op
(`.8B`/`.16B`/`.8H`) folds that garbage into the result. Pre-zero with
`MOVI Vn.8B,#0` before the partial load, or use a zero-extending load. A comment
claiming "the upper lanes are 0" is not a guarantee.

---

## 10. Memory Ordering (applies to ALL output: asm AND C/intrinsics)

ARM64 has a **weakly-ordered** memory model; x86 has TSO (total store order). Code that synchronized correctly on x86 by accident often **breaks silently** on ARM64.

- Plain loads/stores can be reordered across each other and across atomics
- `volatile` does NOT imply ordering on ARM64 (MSVC's `/volatile:ms` semantics are x86-only and non-portable)
- For inter-thread synchronization, use **acquire/release** atomics or explicit barriers:
  - Acquire load: `LDAR` (asm) / `__atomic_load_n(..., __ATOMIC_ACQUIRE)` or `std::atomic::load(memory_order_acquire)` (C/C++)
  - Release store: `STLR` (asm) / `__atomic_store_n(..., __ATOMIC_RELEASE)` (C/C++)
  - Full fence: `DMB ISH` (asm) / `__atomic_thread_fence(__ATOMIC_SEQ_CST)` (C/C++)
- `_Interlocked*` MSVC intrinsics: on ARM64, the un-suffixed forms imply sequentially consistent ordering; if porting performance-sensitive code consider `_*_acq` / `_*_rel` variants or `__atomic_*` builtins
- LSE atomics (`LDADD`, `SWPAL`, `CAS*`) are faster than `LDXR/STXR` retry loops but require ARMv8.1-A. Detect with `IsProcessorFeaturePresent(PF_ARM_V81_ATOMIC_INSTRUCTIONS_AVAILABLE)` at runtime, or compile with `/arch:armv8.1` / `-march=armv8.1-a` if the deployment target guarantees it

## 11. ARM64EC Awareness

ARM64EC (Emulation Compatible) is a hybrid ABI on Windows that allows ARM64 code to interop with x64 code in the same process. **Freeform output for an ARM64EC target is NOT the same as classic ARM64.**

- Detect target: `_M_ARM64EC` is defined on ARM64EC; `_M_ARM64` is defined on **both** classic ARM64 and ARM64EC. Check `_M_ARM64EC` first
- ARM64EC functions called from x64 must use the EC ABI shim — do NOT emit raw ARM64 calling-convention asm in an ARM64EC translation unit unless you understand the entry/exit thunks
- Header guards: `#if defined(_M_ARM64) || defined(_M_ARM64EC)` is the right pattern for "ARM64-family"; use `#if defined(_M_ARM64) && !defined(_M_ARM64EC)` to mean "classic ARM64 only"
- If you don't know whether the target is classic ARM64 or ARM64EC, **say so explicitly in a code comment** and prefer C/intrinsics over hand-written asm — the compiler emits correct EC thunks; hand-written asm doesn't

## 12. C / Intrinsics Freeform Output Rules

When the freeform output is C/C++ (not assembly):

- Header: `#include <arm_neon.h>` for NEON; `#include <arm_acle.h>` for CRC32, AES, SHA, atomics, etc.
- Target macro guard: wrap NEON code in `#if defined(_M_ARM64) || defined(_M_ARM64EC) || defined(__aarch64__)` (or use the project's existing macro convention if visible in the porting context)
- NEON feature macros: `__ARM_NEON` (always 1 on ARM64), `__ARM_FEATURE_CRC32`, `__ARM_FEATURE_CRYPTO` — gate optional features on these
- Bit-scan / byte-swap mappings:
  - `_BitScanForward` / `_tzcnt_u32` → `__builtin_ctz` (clang/gcc) or `_CountTrailingZeros` (MSVC)
  - `_BitScanReverse` / `_lzcnt_u32` → `__builtin_clz` / `_CountLeadingZeros`
  - `_byteswap_ulong` → `__builtin_bswap32` or vector `vrev32q_u8`
  - `__popcnt` → `__builtin_popcount` (scalar) or `vcntq_u8` + reduce (vector)
- Do NOT leave any `_mm_*` / `_mm256_*` / `__m128i` / `__m256i` token in the output. If you cannot port a specific intrinsic, comment-out the call and emit a `TODO(arm64):` note rather than emitting wrong code
- Do NOT use inline `__asm` blocks unless the matched spec explicitly requires it — MSVC ARM64 does not support inline assembly anyway; use intrinsics or a separate `.s` file
- Type fidelity: pick the NEON type whose lane width and signedness match the x86 op. `_mm_add_epi32` → `vaddq_s32` on `int32x4_t`, NOT `vaddq_u32`. Wrong signedness compiles fine but breaks comparisons and saturation
- **Short-buffer / tail guard (crash risk).** A SIMD kernel whose main loop consumes a fixed stride (16/32/64 bytes) MUST guard the entry: `if (len < STRIDE) return <scalar-fallback>(...)` BEFORE any unconditional `vld1q_u8(ptr)` + `len -= STRIDE`. x86 source usually has this short-input branch; porting only the hot loop drops it. Two failures compound: the unconditional vector load reads out of bounds, AND `len -= STRIDE` on an unsigned `size_t` underflows to a near-`SIZE_MAX` value, turning the next `while (len >= STRIDE)` into an unbounded OOB walk → **segfault**. Watch especially for a separate "fold the initial state in" branch (e.g. `if (crc != 0) { load 16; len -= 16; }`) that also loads unconditionally. Test every kernel at `len ∈ {0,1,STRIDE-1,STRIDE,STRIDE+1}` with a non-default seed — large aligned buffers never exercise this path.
- **MSVC ARM64 intrinsic portability (compile failures).** GCC/Clang accept things MSVC's ARM64 headers reject; verify on MSVC, not just clang:
  - Aggregate brace-init of NEON vectors fails on MSVC (`uint32x4_t v = {a,b,c,d}` → C2078). Build constant vectors from a plain array: `vld1q_u32((const uint32_t[]){...})` or a named `tmp[]` + `vld1q_u32(tmp)`.
  - `poly64_t` is a 64-bit integer on GCC/Clang but the opaque `__n64` on MSVC, so `(poly64_t)some_u64` casts only compile on the former. For `vmull_p64`, the operand form also diverges: ACLE takes a scalar lane (`vgetq_lane_p64(vreinterpretq_p64_u8(x), n)`), MSVC takes a vector lane (`vget_low_p64` / `vget_high_p64`). Split such macros on `#if defined(_MSC_VER)`.
  - `poly128_t` is unnamed on MSVC — only use the 128-bit poly result through `vreinterpretq_u8_p128()`, never as a named type. `<arm_acle.h>` does not exist on MSVC (NEON/crypto/SHA3 intrinsics come from `<arm64_neon.h>` via `<arm_neon.h>`); guard the acle include with `#if !defined(_MSC_VER)`.
- **`#include "*.c"` template reuse defeats incremental builds.** This skilltree's kernels often `#include "<base>.c"` to share `static inline` helpers across variant files. Build systems (CMake/MSBuild) do NOT track `#include` of a `.c` as a dependency, so editing the included base file does NOT recompile the including TUs — they keep an inlined STALE copy of the helper (e.g. a fix in the base appears to "not take"). After editing a file that is `#include`d by siblings, force-rebuild those siblings (touch them, or clean-build) before trusting a test result. Suppress duplicate external symbols from the included `.c` with a `#ifndef <BASE>_HELPERS_ONLY` guard around its non-inline entry points, defined by each includer.

## 13. Verification Checklist

### For ALL output

- [ ] Memory ordering preserved: any `_Interlocked*` / atomic / lock primitive maps to acquire/release-correct ARM64 form
- [ ] Target macro guard distinguishes ARM64EC from classic ARM64 if the code path differs
- [ ] No x86-only intrinsic / mnemonic / register name leaked into output

### For ARM64 assembly output

- [ ] SP remains 16-byte aligned after all stack operations
- [ ] All callee-saved registers used are saved in prolog and restored in epilog
- [ ] X18 is never written or used as scratch
- [ ] Every conditional branch has an explicit flag-setting source
- [ ] No `CSEL`/`CSET`/`B.cond` relies on stale NZCV — flags are freshly set for *its* condition (no `CMP` carried across intervening flag-setting work)
- [ ] No `Wn` write clobbers a live 64-bit pointer/value in `Xn`; no `BL`-reached helper returns in / scratches a register whose `Xn` the caller keeps live across the call
- [ ] Partial/narrow loads (`LD1 {Vn.S}[0]`, `LDR Sn`) zero the unloaded lanes before any full-width op reads them; `D`-form writes don't silently clear an accumulator's upper lanes
- [ ] B.cond ranges fit ±1 MB; long-range conditionals use a trampoline
- [ ] Large immediates are properly split (MOVZ+MOVK)
- [ ] No memory access below SP (no red zone)
- [ ] Vector operations stay within 128-bit NEON width
- [ ] Function returns via RET (using X30), not by jumping to address on stack

### For C / intrinsics output

- [ ] `<arm_neon.h>` (and `<arm_acle.h>` if needed) included
- [ ] Code is wrapped in an ARM64 target-macro guard
- [ ] No `_mm_*` / `_mm256_*` / `__m128i` / `__m256i` tokens remain
- [ ] NEON lane width and signedness match the original x86 intrinsic semantics
- [ ] Vector operations stay within 128-bit (no implicit AVX-style 256-bit assumptions)
- [ ] Bit-scan / byte-swap / popcount use ARM64-portable builtins, not MSVC x86-only ones
- [ ] Any unsupported intrinsic is flagged with a `TODO(arm64):` comment, not silently mistranslated
- [ ] Fixed-stride SIMD kernels guard `len < STRIDE` (and any unconditional initial-state load) with a scalar fallback; tested at `len ∈ {0,1,STRIDE±1}` with a non-default seed (prevents OOB + `size_t` underflow → segfault)
- [ ] Compiles on MSVC ARM64, not only clang/gcc: no NEON-vector brace-init, no `(poly64_t)`/`poly128_t` named-type use, `vmull_p64` lane-extraction split on `_MSC_VER`, `<arm_acle.h>` guarded with `#if !defined(_MSC_VER)`
- [ ] If kernels `#include "*.c"` to share helpers: includers force-rebuilt after editing the base, and base's external entry points guarded by a `*_HELPERS_ONLY` macro to avoid duplicate symbols
