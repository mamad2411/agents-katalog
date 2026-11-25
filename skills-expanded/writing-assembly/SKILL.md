---
name: writing-assembly
description: Write small ARM assembly segments for RISC OS with the ObjAsm toolchain, especially veneers, callbacks, module entry points, and other interface-facing `s/*` code.
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(riscos-objasm:*) Bash(riscos-link:*) Bash(riscos-amu:*) Bash(riscos-build-run:*) Bash(riscos-dumpi:*) Bash(riscos-dump:*)
---

# Assembly Development for RISC OS with ObjAsm

This document outlines the procedures, standards, and pitfalls for writing small interface-facing ARM assembly fragments on RISC OS using the `objasm` assembler and `riscos-link`.

## 1. Source File Structure

`objasm` source files are held in an `s/` directory.

### Syntax Rules
*   **Labels**: Must start at the very beginning of the line (Column 1).
*   **Instructions**: Must be indented (at least one space or tab).
*   **Comments**: Start with a semicolon (`;`).
*   **Directives**: Essential for correct object generation.

### Essential Directives
```arm
        AREA    |Name|, CODE, READONLY  ; Define the area name and type
        EXPORT  my_function             ; Make symbol visible to linker
        GET     hdr.swis                ; Include header files
        END                             ; Mandatory end of file
```

When keeping 32-bit ARM and AArch64 variants of the same entry-point source,
use the matching header families rather than sharing the 32-bit ones. For
example, 32-bit code commonly uses `hdr.swis`, `hdr.printmacros`, and
`hdr.procapcs`; AArch64 code should use the corresponding 64-bit headers such as
`hdr.swis64`, `hdr.printmacros64`, and `hdr.procapcs64` when those macros are
needed.

## 2. The Build Process

The standard RISC OS build toolchain uses a two-stage process: Assemble to Object (AOF), then Link to Executable.

### Assembling (objasm)
*   **Default**: Produces an AOF object file.
*   **Command**: `riscos-objasm -o o.mycode s.mycode`
*   **Architecture**: For 32-bit code, use `-32bit` (though often handled by Makefiles).

### Assembling AArch64 (riscos64-objasm)
*   Use `riscos64-objasm` for AArch64 sources. It accepts ObjAsm-style
    directives such as `AREA`, `EXPORT`, labels in column 1, `;` comments, and
    `END`, but the instructions themselves must be AArch64 instructions.
*   Do not copy ARM32 instructions such as `STMFD`, `LDMIA`, `MOV pc, lr`,
    `LDR pc, [...]`, or conditional data-processing forms like `STRVS` into
    AArch64 sources. Use AArch64 forms such as `STP`/`LDP`, `BLR`, `RET`, and
    conditional branches like `BVS`.
*   The `riscos64-objasm` wrapper supports a smaller option set than
    `riscos-objasm`. Old ObjAsm switches such as `-Stamp` and `-quit` are not
    accepted. A typical object build is:

```bash
        riscos64-objasm -o o64.mycode s.mycode64
```

*   For a raw binary blob, prefer direct binary output from the assembler:

```bash
        riscos64-objasm -bin -o driver64,ffd s.driver64
```

    Using `riscos64-link -bin` on a bare assembler object may pull in the
    64-bit C runtime and fail with unresolved `main`, constructor, finaliser, or
    GOT symbols.

### Linking (riscos-link)
*   **Default**: Produces an AIF (Absolute Interface Format) executable.
*   **Utility/Binary Output**: To create a raw binary (e.g., for loading into RMA or as a utility module), you **must** use the `-bin` flag.
*   **Command**: `riscos-link -bin -o mybinary,ffc o.mycode`
*   **Note**: Without `-bin`, the linker adds a header that may cause "Branch through zero" exceptions if you try to jump directly to the start of the file.

### Running AArch64 builds
*   Build 64-bit module targets with `riscos-amu BUILD64=1`.
*   Run AArch64 modules with the 64-bit runner flag:

```bash
        riscos-build-run --64 rm64/ModuleName,ffa test,fd1 --command "RMLoad ModuleName" --command "run test"
```

    Without `--64`, the runner may reject an AArch64 module as an unsupported
    architecture.

## 3. Register Conventions (APCS)

When interfacing with C or the OS, follow the ARM Procedure Call Standard (APCS):

*   **R0-R3**: Argument passing and result return (R0). These are "caller-saved" (volatile).
*   **R4-R11**: Variable registers. These **must** be preserved by the called function.
*   **R12**: IP (Intra-Procedure-call scratch register). Often used as a workspace pointer.
*   **R13 (SP)**: Stack pointer. Must be 8-byte aligned at public interfaces.
*   **R14 (LR)**: Link register (return address).
*   **R15 (PC)**: Program counter.

For AArch64 entry-point code, use the AArch64 procedure-call rules:

*   **X0-X7**: Argument passing and result return. These are caller-saved.
*   **X8-X17**: Caller-saved scratch registers. `X16` and `X17` may be used by
    veneers or linkage code.
*   **X19-X28**: Callee-saved variable registers. Use these where the 32-bit
    version would have used preserved registers such as `R4-R9`.
*   **X29**: Frame pointer.
*   **X30**: Link register.
*   **SP**: Stack pointer. Keep it 16-byte aligned at public interfaces and
    before calls into C.

## 4. Interface Stubs And Veneers

For most RISC OS assembly work in this environment, the code being written is a
small boundary layer rather than a complete algorithm. Typical cases are:

*   a veneer that lets C call a routine needing registers outside `R0-R9`
*   a public entry point that external code will call directly
*   a callback or vector handler that must preserve a strict register contract

When writing this kind of code:

*   write down the exact entry contract first: input registers, output
    registers, preserved registers, V flag behaviour, and whether the caller
    expects `R12` to be a private word, workspace, or scratch register
*   preserve every register the contract requires, not just the registers your
    current implementation happens to touch
*   keep the veneer minimal: load registers, call through, translate the
    return convention, and get out
*   if the target routine is C, ensure the entry path establishes the C
    environment correctly; if external code will call into C, this is usually a
    job for a CMHG `generic-veneer`

## 5. RISC OS Error Convention

RISC OS uses the **V flag** (Overflow) to indicate errors:
*   **VC** (V Clear): Success. R0 may contain a result.
*   **VS** (V Set): Failure. R0 contains a pointer to an error block (`int error_number, char error_message[]`).

In your assembly return logic:
```arm
        MOVVC   r0, #0          ; Return NULL on success
        ; V flag is preserved from the last instruction (e.g., a driver call)
        LDMFD   sp!, {r4-r12, pc}
```

For AArch64 module entry points, the common convention is to return an error
pointer or zero in `x0`, and not to rely on setting V. Some legacy-style
driver interfaces may still define a V-flag contract for their callback entry
points. In those veneers, preserve the interface's contract deliberately: for
example, branch on `BVS` after `BLR` if the driver callback promises to return
errors with V set, and only copy result registers back to the caller's register
block on the V-clear path.

Condition flags are only meaningful until the next instruction that changes
them. Do not calculate whether an error pointer is zero with `CMP` and then use
`SWIVS`/`BVS` as though the V flag still represented an earlier SWI or C call.
If the contract is "zero means no error, non-zero means error pointer", branch
on the value directly and then call `OS_GenerateError` on the non-zero path.

## 6. 32-bit Pitfalls

### The Return Instruction
*   **Avoid**: `MOVS pc, lr` in 32-bit user/SVC mode. This is a 26-bit era instruction that restores the PSR from the PC's top bits, which is incorrect in 32-bit mode.
*   **Correct**: Use `MOV pc, lr` for simple returns or `LDMFD sp!, {regs, pc}` to return and pop registers simultaneously.

### The Magic Word Requirement
For certain module-related drivers (like CDFSDriver registration), the code block in memory often requires a "Magic Word" immediately preceding the entry point.
*   **CDFSDriver**: Expects `&EE50EE50` at `entry - 4`.

### Register Blocks (`_kernel_swi_regs`)
*   The standard C structure `_kernel_swi_regs` only contains **10 words** (R0-R9).
*   If you need to pass R11 or R12 to a routine, you cannot put them in that block. You must pass them as separate arguments to an assembly veneer.

## 7. AArch64 Pitfalls

### Register blocks are still 32-bit fields
In the current 64-bit build environment, `_kernel_swi_regs` is still a block of
ten 32-bit `int` fields for R0-R9 style SWI registers. AArch64 veneers that
bridge this structure should load and store `w0`-`w9`, not `x0`-`x9`, unless a
specific API explicitly defines 64-bit slots.

For example:

```arm
        LDR     x10, [sp]          ; x10 -> _kernel_swi_regs
        LDP     w0, w1, [x10, #0]
        LDP     w2, w3, [x10, #8]
        LDP     w4, w5, [x10, #16]
        LDP     w6, w7, [x10, #24]
        LDP     w8, w9, [x10, #32]
```

Apply the same rule to private C structures and workspace blocks: prove the C
field widths and offsets before changing `LDR`/`STR` instructions to their
64-bit `x` forms. A pointer field normally needs an `x` load/store and 8-byte
layout; a retained 32-bit size, handle, or RISC OS register field should use a
`w` load/store. Blindly widening stores can overlap following fields if the
structure was not changed to match.

### Calling through a driver entry
Use `BLR xN` to call a function pointer. If the entry address came from a
32-bit RISC OS register or structure field, load it into a `w` register so it
is zero-extended into the corresponding `x` register before calling:

```arm
        LDR     w10, [sp, #8]      ; 32-bit entry address
        BLR     x10
```

### Stack alignment and link register
Keep the stack 16-byte aligned across public AArch64 calls. Save and restore
`x30` explicitly if your veneer calls onward:

```arm
        STP     x0, x1, [sp, #-48]!
        STR     x30, [sp, #32]
        ; ...
        LDR     x30, [sp, #32]
        ADD     sp, sp, #48
        RET
```

When an entry point allocates its own workspace and stack, round the allocated
size and the eventual stack top to the alignment required by the architecture.
The 32-bit code may also maintain `sl` as a stack-limit register; AArch64 code
usually has no direct equivalent and should not copy `sl` setup mechanically.

### Condition flags
AArch64 has conditional branches such as `BVS` and `BVC`, but not ARM32-style
conditional stores like `STRVS` or `STMVCIA`. Split the success and error paths
with conditional branches.

If a SWI or callback returns an error through V, test V immediately or preserve
the result in a general register before any `CMP`, `TST`, arithmetic-with-flags,
or macro that may alter NZCV. If the next interface uses an error pointer in
`x0` instead, treat that as a separate convention and test `x0`, not V.

### Porting matching ARM and AArch64 entry points
When translating a small ARM entry-point file to AArch64, keep a side-by-side
checklist rather than doing an instruction-for-instruction rewrite:

*   map preserved ARM registers such as `R4-R9` to callee-saved AArch64
    registers such as `X19-X24`
*   replace 32-bit APCS/procedure macros and print/SWI headers with their
    64-bit equivalents
*   preserve the public contract comments, but update register names and mode
    assumptions where the 64-bit environment differs
*   re-check every workspace offset against the C definition after pointer-size
    changes
*   make stack and workspace alignment explicit, especially before calling C
*   check every conditional instruction that depended on ARM's per-instruction
    condition codes and split it into explicit AArch64 branches

## 8. Public Interface Checklist

Before considering an interface stub complete, check:

*   labels are in column 1 and non-label lines are indented, so ObjAsm parses
    the file as intended
*   the symbol is exported if another object must link against it
*   stack push/pop sets match exactly and leave the stack aligned at the public
    boundary
*   `MOVS pc, lr` is not used for a 32-bit return path
*   AArch64 sources use AArch64 instructions and returns (`RET`), not ARM32
    stack or PC-manipulation instructions
*   AArch64 public call paths keep the stack 16-byte aligned and preserve `x30`
    when calling onward
*   AArch64 ports use `w` loads/stores for 32-bit fields and `x` loads/stores
    only for proven 64-bit fields or pointers
*   V-flag checks happen before any flag-clobbering instruction, or the code
    tests an explicit error pointer/value instead
*   success and error exits match the caller's expected convention, especially
    whether `R0`/`x0` should be preserved, cleared, or treated as an error pointer
*   any required magic word or descriptor layout is present at the exact offset
    the consumer expects

## 9. Debugging

*   **Disassembly**: Use `riscos-dumpi <file>` to see the actual instructions generated. This is vital for checking if the linker added unwanted headers or if the `MOVVC`/`STRVS` conditions are correct.
    Use `riscos-dumpi --arm64 <file>` for AArch64 objects or binaries.
*   **Hex Dump**: Use `riscos-dump <file>` to verify byte alignments and magic words.
*   **Branch through zero**: This exception usually means you jumped to a NULL pointer, often caused by an incorrect entry point address or a corrupted stack during a return.
