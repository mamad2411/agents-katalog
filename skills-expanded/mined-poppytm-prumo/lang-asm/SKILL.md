---
name: lang-asm
description: x86_64 / ARM64 assembly engineering, ABI calling conventions (System V AMD64 / Microsoft x64), 16-byte stack alignment, CFI unwinding, non-executable stacks, and CET hardening.
---

# Assembly x86/x86-64 Engineering & ABI Safety Contract

## 1. Purpose
Define, author, and audit low-level assembly language routines (x86_64 and ARM64), guaranteeing strict compliance with target platform ABIs (System V AMD64, Microsoft x64, ARM AAPCS64), mathematical 16-byte stack alignment, callee-saved register preservation, complete DWARF CFI unwinding, and modern hardware security mitigations (non-executable stack notes, CET `endbr64`).

---

## 2. Use When
- Implementing high-throughput vectorization routines using AVX2, AVX-512, or ARM NEON.
- Developing context switching, coroutine runtimes, fiber primitives, or JIT compiler stubs.
- Writing cryptographic primitives requiring constant-time execution and memory barrier safety.
- Hand-optimizing hot loops where compiler auto-vectorization fails to match hardware capabilities.

---

## 3. Do Not Use When
- Writing standard business logic or application code easily handled by Go, Rust, C++, C, or Zig.
- Portability across diverse CPU architectures is required without maintaining separate assembly sources.
- The project language provides intrinsics that compile to equivalent assembly with less maintenance burden.

---

## 4. Required Context
Before writing or modifying assembly routines, verify:
1. **Target Architecture & Platform ABI**: x86_64 (System V AMD64 vs Microsoft x64) or AArch64 (ARM AAPCS64).
2. **Assembler Syntax**: GNU Assembler (GAS) `.intel_syntax noprefix` vs AT&T syntax vs NASM/Yasm.
3. **Execution Context**: User space (red zone permitted on System V) vs Kernel/Embedded space (red zone prohibited).
4. **Security Features**: Intel CET (IBT/SHSTK) active, non-executable stack enforcement (`.note.GNU-stack`).

---

## 5. Procedure

### Step 1: Register Allocation & Calling Convention Setup
1. Map procedure arguments strictly to target ABI registers:
   - **System V AMD64 (Linux/macOS)**: `RDI`, `RSI`, `RDX`, `RCX`, `R8`, `R9` (integers/pointers); `XMM0`-`XMM7` (floats/SIMD).
   - **Microsoft x64 (Windows)**: `RCX`, `RDX`, `R8`, `R9` (integers/pointers); `XMM0`-`XMM3` (floats).
2. Protect Callee-Saved Registers:
   - If `RBX`, `RBP`, `R12`, `R13`, `R14`, or `R15` are modified, save them in the function prologue (`push reg`) and restore them in reverse order in the epilogue (`pop reg`).
3. Return values must be placed in `RAX` (integer) and `XMM0` (floating point/vector).

### Step 2: Stack Frame Alignment Mathematics
1. The x86_64 ABI mandates that the stack pointer `RSP` must be a multiple of 16 immediately before any `call` instruction:
   $$\text{RSP} \equiv 0 \pmod{16}$$
2. Upon function entry (immediately after `call`), the CPU pushes the 8-byte return address, leaving:
   $$\text{RSP} \equiv 8 \pmod{16}$$
3. Therefore, before making a nested `call`:
   - If saving `RBP` (`push rbp`), `RSP` becomes $16 \pmod{16}$. Stack adjustment must be a multiple of 16 (`sub rsp, 16 * N`).
   - If not saving a frame pointer, subtract $8 + 16 \cdot N$ (`sub rsp, 8` or `sub rsp, 24`, etc.) so `RSP` is 16-byte aligned before `call`.
4. In leaf functions on System V user space, the 128-byte red zone (`[rsp - 128]` to `[rsp - 1]`) may be used without moving `RSP`.

### Step 3: DWARF Call Frame Information (CFI) Directives
1. Wrap every function in CFI directives to ensure stack unwinders, debuggers, and exception handlers function correctly:
   ```gas
   .globl my_function
   .type my_function, @function
   my_function:
       .cfi_startproc
       push rbp
       .cfi_def_cfa_offset 16
       .cfi_offset rbp, -16
       mov rbp, rsp
       .cfi_def_cfa_register rbp
       ...
       pop rbp
       .cfi_def_cfa rsp, 8
       ret
       .cfi_endproc
   ```

### Step 4: Security & Hardening Hard Gates
1. **Non-Executable Stack Directive**: Every assembly file must declare the GNU stack note at the bottom:
   ```gas
   .section .note.GNU-stack,"",@progbits
   ```
2. **Control-Flow Enforcement (CET)**: Add `endbr64` at the entry point of all global and indirectly called procedures to satisfy Intel Indirect Branch Tracking (IBT).
3. **Direction Flag Hygiene**: Always ensure the direction flag is cleared (`cld`) before executing string instructions (`rep movsb`, `stosq`).

### Step 5: Verification & Assembling
1. Assemble object files with `as` or `gcc -c`.
2. Inspect generated symbols with `nm` or `objdump -d`.
3. Check for executable stack flag using `readelf -l <object> | grep GNU_STACK` (must show `RW`, never `RWE`).

---

## 6. Decision Rules
1. **Preserve Callee-Saved Registers Without Exception**: Never modify `rbx`, `rbp`, `r12`-`r15` without preserving and restoring them.
2. **Mandatory 16-Byte Stack Alignment**: Any `call` instruction executed with unaligned `RSP` is an immediate critical defect that crashes on SSE/AVX instructions (`movaps`).
3. **Always Emit `.note.GNU-stack`**: Omitting the non-executable stack note causes linkers to mark the entire process stack executable, violating security posture.
4. **Position Independent Addressing (RIP-Relative)**: Global variables and constant data must be accessed using RIP-relative addressing (`[rip + my_constant]`) to support ASLR.

---

## 7. Evidence Required
- **Assembler Compilation**: `as -o output.o input.s` exits with code 0.
- **Stack Permissions Verification**: `readelf -l output.o | grep GNU_STACK` shows `RW` permissions (no `E` execute flag).
- **Test Harness Run**: C/Rust/Go test harness calling the assembly function passes all assertions.

---

## 8. Output Contract
A production assembly artifact must include:
1. Formatted `.s` or `.asm` source file with explicit ABI documentation.
2. CFI unwind annotations on all non-trivial stack mutations.
3. `.section .note.GNU-stack,"",@progbits` declaration.
4. Test driver program (in C or assembly) verifying calling conventions and registers.

---

## 9. Stop Conditions
- Assembly compiles cleanly without warnings.
- Stack alignment verified mathematically and via tests.
- Non-executable stack verified via ELF headers.

---

## 10. Escalation Rules
- Escalate to Security Architect if assembly requires executable memory allocation (`mprotect PROT_EXEC`) for runtime JIT generation.
- Escalate to Lead Systems Engineer if platform ABI calling conventions conflict between mixed-compiler toolchains.
