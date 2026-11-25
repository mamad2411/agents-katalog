---
name: ctf-pwn-rop
description: Advanced ROP CTF workflow — ret2csu universal gadget, stack pivoting (leave;ret, xchg rsp), mprotect+shellcode (NX bypass via executable-stack staging), SROP (sigreturn syscall frame forgery for register-state hijack), ret2dlresolve (delayed-binding fake relocation entry), bad-byte constraint bypass (null/newline/printable-only), chain verification via GDB single-step debugging, and multi-stage pivot-chain composition for authorized lab/competition binaries.
disable-model-invocation: true
risk: caution
allowed-modes: [ctf, reverse-engineering]
authorization-required: yes
evidence-outputs: [artifact-hash, gadget-notes, exploit-notes, redacted-flag]
---

# Advanced ROP — ret2csu, stack pivoting, mprotect shellcode, SROP, ret2dlresolve, and constraint bypass

Use this skill for advanced Return-Oriented Programming exploitation on user-space binaries in authorized CTF competitions, lab exercises, or educational environments. All techniques target challenge-provided binaries running on challenge-controlled infrastructure. ROP chains construct arbitrary computation by chaining short instruction sequences ending in `ret` ("gadgets") without injecting any new code. This skill covers techniques that go beyond the basic `pop rdi; ret` → `system` pattern covered in `ctf-pwn-basics`.

This skill covers: ret2csu (the universal `__libc_csu_init` gadget for setting rdi, rsi, rdx simultaneously), stack pivoting to attacker-controlled memory when the overflow length is insufficient for a full chain, `mprotect` + shellcode staging when NX must be bypassed for custom payloads, SROP (Sigreturn-Oriented Programming) using the `rt_sigreturn` syscall to forge an entire register state, ret2dlresolve for attacking dynamically-linked binaries without knowing libc offsets, bad-byte constraint bypass strategies (null bytes, newline terminators, printable-only payloads), chain verification via GDB single-step debugging, and multi-stage ROP composition for complex primitives such as open-read-write (ORW) file exfiltration. Each technique is presented as a conceptual workflow with tool references and decision criteria. All exploit development must be performed locally against the provided binary. Remote exploitation is permitted only against the designated challenge service and only after local verification.

## Required inputs

- Challenge binary (ELF) with its SHA-256 hash recorded before any analysis or execution.
- Challenge service endpoint (host, port) if the binary is served remotely.
- The libc shared object (`.so` file) used by the remote service if the ROP chain references libc gadgets or functions. Record its hash. For ret2dlresolve, the libc is not strictly required — the technique resolves library functions through the binary's own PLT/GOT machinery.
- Written scope confirming the binary and service belong to an authorized CTF competition, lab exercise, or educational environment. Include competition name, challenge name, allowed tooling, and any restrictions.
- Valid authorization cache for the CTF engagement. Re-authorization required if the exploit chain spans multiple stages or services.
- Known binary protections from a prior `ctf-pwn-basics` skill run or fresh `checksec` audit: NX (required for ROP — NX must be enabled), Canary (must be bypassed or not present), PIE (if enabled, code addresses must be leaked; if disabled, gadgets are at fixed addresses), RELRO (determines GOT-writable status), and word size (32-bit or 64-bit — calling convention determines gadget requirements).
- Binary disassembly and gadget search results. Gadget availability directly determines which ROP techniques are viable. If the binary is tiny (few useful gadgets) but libc is available, libc gadgets can be used after an address leak.
- For SROP: the `rt_sigreturn` syscall number (15 on x86-64, 119 on i386) must be known, and the binary must have a `syscall; ret` gadget (or the ability to call `sigreturn` through a PLT stub).
- For ret2dlresolve: the binary must be dynamically linked with Partial RELRO (the `.dynamic` and `.rel.plt` sections are writable).

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before any binary analysis or execution.
2. `pentest_agent_parse_scope` for competition rules, lab targets, challenge binaries, libc files, and service endpoints. Record all hashes in scope.
3. `pentest_agent_validate_target` before any remote service interaction. Confirm the endpoint is within competition infrastructure.
4. `pentest_agent_check_authorization` before remote exploitation or any active interaction with the remote service.
5. `pentest_agent_build_command` for dry-run argument preview when using catalog tools: `checksec`, `objdump`, `readelf`, `GDB with pwndbg`, `pwntools`, `ROPgadget`, `one_gadget`, `libc-database`, `patchelf`.
6. `pentest_agent_execute_tool` for all tool execution — never raw shell. This enforces approval gates, timeout boundaries, disabled-category policy, and output redaction.
7. `pentest_agent_append_evidence` after each phase, `pentest_agent_record_finding` for successful exploits and flags, and report tools for final handoff.

## Workflow

### Phase 1 — binary protection recap and gadget source assessment

Before constructing any ROP chain, reassess the binary protections through the lens of gadget availability and chain constraints. The protections determine where gadgets can be sourced, whether addresses need leaking, and whether the chain must include bypass stages.

1. Re-run `checksec` through `pentest_agent_execute_tool` and record the full protection matrix. If this was already done in a prior `ctf-pwn-basics` phase, summarize and confirm the values. Key ROP-relevant implications:
   - **NX enabled**: required for ROP to be necessary. If NX is disabled, shellcode injection directly on the stack is simpler — skip to Phase 5 for mprotect staging only if the stack is non-executable but a heap or data section is executable.
   - **PIE enabled**: all binary code addresses are randomized. Gadgets in the binary require a code leak first. Gadgets in libc require a libc leak. If both PIE and ASLR are enabled, two leaks are needed (one for binary base, one for libc base).
   - **PIE disabled**: binary gadgets are at fixed, known addresses. Only libc gadgets require a leak. This is the most favorable scenario for ROP.
   - **Partial RELRO**: the `.got.plt` section is writable, enabling GOT-overwrite primitives as an alternative to long ROP chains. Full RELRO prevents this.
   - **Canary enabled**: the chain must include a canary bypass (leak or brute-force) before reaching the return address. This adds a stage before the ROP chain proper.
2. Identify the gadget source scope. Gadgets come from three regions:
   - **Binary `.text` section**: always available if PIE is disabled. If PIE is enabled, requires a binary leak. Small binaries may have limited gadgets.
   - **Libc `.text` section**: always available after a libc leak. Libc is massive (~2MB+ text on modern systems) and contains nearly every conceivable gadget. This is the richest gadget source.
   - **Linker (`ld-linux.so`) `.text` section**: another large library, sometimes loaded between libc and the stack. If the linker's base can be leaked, its gadgets are alternative sources.
3. Determine the overflow budget: how many bytes can the attacker write past the buffer before reaching the end of the writable region? If the overflow allows writing 8-16 bytes past the return address (e.g., buffer fits exactly one return address plus one argument), only a single-function call is possible — use ret2libc or a one_gadget. If the overflow allows writing 40-100+ bytes past the return address, a longer ROP chain is feasible. If the overflow is extremely short (only reaches the return address with no room for arguments), stack pivoting (Phase 4) is required.
4. Calculate the exact available chain length in 8-byte slots (x86-64) or 4-byte slots (x86). Each gadget in the chain occupies one slot (its address), and each argument occupies one slot (pushed onto the stack as part of the chain). A chain that calls `system("/bin/sh")` requires 2-3 slots (pop rdi gadget + argument + function). A chain that calls `mprotect` with three arguments requires 6-8 slots. A full ORW chain may require 20-40 slots. If the overflow cannot accommodate the chain, stack pivoting is mandatory.

### Phase 2 — gadget taxonomy and discovery strategy

ROP gadgets are short instruction sequences that end in `ret` (x86-64) or `ret`/`pop; ret` (x86). Systematic gadget discovery requires knowing what to search for and understanding which gadget classes serve which purposes.

1. **Argument-setting gadgets** for x86-64 calling convention. These pop values from the stack into argument registers and then return to the next gadget. Essential search targets:
   - `pop rdi; ret`: sets the first argument (RDI). Almost always present in libc; often present in the binary. Search via `ROPgadget --binary <file> --only "pop|ret" | grep "pop rdi"`.
   - `pop rsi; ret`: sets the second argument (RSI). Less common standalone; more often appears as `pop rsi; pop r15; ret`. The extra `pop r15` is harmless — simply add an extra junk 8-byte slot in the chain.
   - `pop rdx; ret`: sets the third argument (RDX). The rarest of the common argument gadgets. Accept variants: `pop rdx; pop rbx; ret`, `pop rdx; pop r12; ret`, `pop rdx; pop rcx; ret`. All are usable — just pad the chain for the extra pops.
   - `pop rcx; ret`: sets the fourth argument (RCX). Rarely needed (most libc functions use at most 3 args); occasionally needed for `mprotect` or `mmap` syscalls.
   - `pop rax; ret`: sets RAX for syscall number. Essential for SROP and syscall-based chains.
2. **Control-flow gadgets** for redirecting execution:
   - `ret`: a standalone `ret` instruction (byte `0xC3`). Used for stack alignment (brings RSP to 16-byte alignment on x86-64 before calling libc functions). Every binary has them — search for any `ret` address.
   - `call rdx` / `call [rax]` / `jmp rsp`: indirect call/jump gadgets. Used when a register can be set to point to attacker-controlled memory (e.g., a heap address containing more gadgets or shellcode).
   - `leave; ret`: the stack pivot gadget. `leave` is equivalent to `mov rsp, rbp; pop rbp`. It sets RSP to the value in RBP, pops the next 8 bytes into RBP from the new stack, and returns. If the attacker controls RBP (from a prior stack frame or a controlled write), this gadget transfers the stack pointer to an attacker-chosen location.
3. **Syscall gadgets** for direct kernel invocation:
   - `syscall; ret`: the canonical syscall gadget on x86-64. Sets up RAX (syscall number) and arguments via `pop` gadgets, then invokes `syscall; ret`. Found in libc (in functions like `read`, `write`, `getpid`) and sometimes in the binary's PLT stubs.
   - `int 0x80; ret`: the 32-bit syscall interface. Works on x86-64 for some syscalls but is limited to 32-bit arguments and has different syscall numbers. Rarely used intentionally but occasionally available.
4. **Data movement gadgets** for memory manipulation:
   - `mov [rdi], rax; ret` / `mov [rsi], rdx; ret`: write-what-where gadgets. If RAX or RDX can be controlled, and RDI/RSI can be pointed to a writable target, these provide an arbitrary write primitive.
   - `xchg rax, rsp; ret` / `xchg rsp, rdi; ret`: exchange gadgets for stack pivoting. If RAX or RDI points to attacker-controlled memory (heap), exchanging with RSP moves the stack there.
5. Search comprehensively using `ROPgadget` through `pentest_agent_execute_tool`. Search the binary first, then libc. Use the `--depth` parameter to find longer gadgets (depth 5-10). Longer gadgets reduce chain length but are less common. Filter results by relevance: keep gadgets that set useful registers, discard gadgets that clobber needed state (unless the clobbered register is unused). Store the gadget list sorted by register/function in the evidence log.
6. For 32-bit x86: arguments are passed on the stack, not in registers. Gadgets are simpler — any instruction sequence ending in `ret` that doesn't clobber critical state is useful. No `pop` gadgets are needed for arguments. The chain directly places function addresses and arguments on the stack. This makes 32-bit ROP chain construction mechanically simpler but the chain is longer (each call consumes more stack slots).

### Phase 3 — ret2csu: the `__libc_csu_init` universal gadget

The `__libc_csu_init` function (present in every glibc-linked x86-64 ELF) contains two gadget sequences — dubbed "gadget 1" and "gadget 2" — that together can set RDI, RSI, and RDX from controlled stack values. This is the universal fallback when `pop rdx; ret` is absent from both the binary and libc.

1. Locate `__libc_csu_init` in the binary disassembly (`objdump -d <binary>` through `pentest_agent_execute_tool`). The function contains a loop that initializes entries in the `.init_array` section. Two code fragments are useful:
   - **Gadget 1** (at the end of the function, just before `ret`): pops RBP and returns — effectively a `pop rbp; ret`. Used as a trampoline.
   - **Gadget 2** (the loop body): a sequence of loads from stack-offsets into registers: typically `mov rdx, r15; mov rsi, r14; mov edi, r13d; call qword [r12 + rbx*8]; ...; ret`. This gadget moves values from R15, R14, and R13 into RDX, RSI, and EDI (the low 32 bits of RDI) and then calls a function pointer at `[r12 + rbx*8]`.
2. Understand the register mapping: R15 → RDX (third argument), R14 → RSI (second argument), R13d → EDI (first argument, lower 32 bits). The function pointer is at `[R12 + RBX*8]` — typically R12 points to the GOT and RBX is set to 0 before entering the gadget, so the call target is `*R12` (the first GOT entry). The caller must control R15, R14, R13, R12, and RBX before entering Gadget 2.
3. Chain composition with ret2csu. The full invocation sequence:
   - **Stage A — set up registers**: use `pop rbx; pop rbp; pop r12; pop r13; pop r14; pop r15; ret` gadget (at the address of Gadget 1 in `__libc_csu_init`). Pop controlled values into RBX (set to 0), RBP (set to 1 — this is used as a loop counter and must be 1 to exit the loop after one iteration), R12 (point to a writable location containing a pointer to the target function — typically a GOT entry that's already resolved, e.g., `_init@GOT`), R13 (argument 1 for the target), R14 (argument 2), R15 (argument 3).
   - **Stage B — execute Gadget 2**: the `ret` at the end of Stage A branches to Gadget 2. Gadget 2 does: `mov rdx, r15` → `mov rsi, r14` → `mov edi, r13d` → `call qword [r12+rbx*8]` (calls the function pointed to by R12, e.g., `_init`). The loop decrements RBP and exits because RBP becomes 0.
   - **Stage C — continue**: after the call returns, Gadget 2 continues with more pops (cleaning up the stack) and returns. The next stack entry after Stage A's payload is the next ROP gadget to execute.
4. Key constraint: `mov edi, r13d` only sets the lower 32 bits of RDI. The upper 32 bits are zeroed. For addresses that require more than 32 bits (libc addresses in the `0x7f...` range), this is insufficient — RDI gets truncated to the lower 32 bits. Mitigation: use ret2csu when the target address fits in 32 bits (PIE-disabled binary where the argument is a local address below `0x100000000`), or use ret2csu only for the second and third arguments and set RDI with a separate `pop rdi; ret` gadget.
5. Alternative target for the call: instead of calling `_init` via GOT, set R12 to point to a controlled memory location where the desired function address is stored. The function address at `*R12` is called with the arguments loaded from R13/R14/R15. This allows calling `system` or `execve` through ret2csu, provided the function address can be placed somewhere writable at a known address.
6. The ret2csu technique is not needed if standalone `pop rdx; ret` exists. Check for simpler gadgets first. Use ret2csu only as a fallback when the binary and libc both lack a clean `pop rdx; ret`.

### Phase 4 — stack pivoting

Stack pivoting moves the stack pointer (RSP on x86-64) from the original stack to an attacker-controlled memory region. This is necessary when the overflow is too short to accommodate a complete ROP chain, when the stack address is unknown (but the heap address is known), or when a secondary write primitive can place a long chain in a controlled location.

1. Identify a stack pivot gadget. Common pivot gadgets and their requirements:
   - `leave; ret`: most common and versatile. `leave = mov rsp, rbp; pop rbp`. Requires controlling RBP. Set RBP to the address of the fake stack minus 8 (because `pop rbp` will increment RSP by 8 before the `ret`). The fake stack must be in a writable region at a known address (heap, `.bss`, `.data`).
   - `xchg rsp, rax; ret` or `xchg eax, esp; ret`: exchange RSP with RAX/EAX. Requires controlling RAX and having it point to the fake stack.
   - `xchg rsp, rdi; ret`: exchange RSP with RDI. Useful if RDI can be set to a heap address through the overflow itself (the buffer address is often passed in RDI).
   - `add rsp, 0xNN; ret`: increment RSP by a fixed amount, skipping part of the original stack. Useful for short jumps within the same stack frame when the overflow length can reach past a canary or saved RBP but not far enough for a full chain.
   - `pop rsp; ret`: directly pops the new RSP from the stack. Requires the overflow to reach the current return address (which gets replaced by the pivot gadget address) and the next 8 bytes (the new RSP value).
2. Choose the fake stack location. Priority order:
   - **Heap buffer**: if the attacker controls a heap allocation of sufficient size, write the full ROP chain there. The heap address must be known (leaked). This is the most common pivot target in heap-overflow challenges.
   - **`.bss`/`.data` section**: if the binary has a global buffer that the attacker controls (e.g., a global char array filled via `scanf` or `read`), write the chain there. Address is known if PIE is disabled.
   - **Environment/argv area**: writable region at a predictable offset from the stack. Less common but available when libc's `environ` pointer is leaked (stack address).
3. Construct the fake stack layout. The fake stack is a contiguous array of 8-byte slots (x86-64) containing the ROP chain. Layout order: `[gadget_1_addr] [arg_1] [gadget_2_addr] [arg_2] ...`. The `leave; ret` pivot executes: `mov rsp, rbp` (RSP now points to fake_stack + 8, because `pop rbp` consumes the first 8 bytes of the fake stack) → `pop rbp` (pops 8 bytes from fake stack into RBP — this can be junk) → `ret` (pops the next 8 bytes from fake stack as the return address — this should be the first gadget of the chain). Therefore, the fake stack should be: `[junk_rbp] [first_gadget_addr] [args...]`.
4. Set up RBP before the pivot triggers. RBP must be set to `fake_stack_address` during the overflow. If the vulnerable function uses `leave; ret` to return (most do), the function's epilogue sets `RBP = [old_RBP]` and `RSP = old_RBP + 8`. The attacker overwrites the saved RBP on the stack with the fake stack address. When the function returns via `leave; ret`, RSP moves to the fake stack. This is the standard "overwrite saved RBP" pivot.
5. Verify the pivot locally in GDB through `pentest_agent_execute_tool`. Set a breakpoint at the `leave; ret` instruction. Before executing it, check: RBP points to fake_stack? The fake stack has valid chain entries? After executing `leave`, RSP points to fake_stack + 8? After `ret`, RIP is the first gadget? If any step fails, recheck the fake stack address arithmetic (8-byte offset for the `pop rbp` consumption). Step through the first few gadgets to confirm the chain is executing from the new stack.

### Phase 5 — mprotect + shellcode staging (NX bypass for custom payloads)

When the ROP chain's goal cannot be achieved with existing code alone (e.g., a complex ORW chain is too long, or a specific shellcode behavior is needed), use the chain to call `mprotect` to make a memory region executable, then jump to shellcode placed there.

1. The `mprotect` syscall signature: `int mprotect(void *addr, size_t len, int prot)`. `addr` must be page-aligned (multiple of 0x1000). `prot` is `PROT_READ | PROT_WRITE | PROT_EXEC` = 7 (or `PROT_READ | PROT_EXEC` = 5). The syscall number is 10 on x86-64.
2. Choose the target region to make executable. Common choices:
   - **Heap**: if the attacker controls a heap buffer containing shellcode, call `mprotect(heap_page_base, 0x1000, 7)` then jump to the shellcode address on the heap.
   - **`.bss`/`.data` section**: if a global buffer is filled with shellcode, the page containing it can be made executable.
   - **Stack** (less common in modern CTFs): make the stack executable, then return to shellcode placed on the stack. Rarely useful because if NX is enabled, the stack is non-executable; making it executable requires calling `mprotect` first, which requires a ROP chain on the stack — a chicken-and-egg problem unless a pivot is used.
3. Build the mprotect ROP chain on x86-64:
   - Chain layout: `[pop_rdi] [page_aligned_addr] [pop_rsi] [0x1000] [pop_rdx] [7] [mprotect_addr_or_syscall_chain] [shellcode_addr]`.
   - If using the libc `mprotect` wrapper function (available via PLT or leaked libc address): set RDI to the page-aligned address, RSI to the region size (typically 0x1000), RDX to 7 (RWX), then call `mprotect@plt` or the libc `mprotect` address. The return address from `mprotect` (next on the stack) should be the shellcode address.
   - If using a `syscall` gadget directly: set RAX to 10 (via `pop rax; ret`), set RDI/RSI/RDX as above, then call `syscall; ret`. The return address from the syscall is the shellcode address.
4. Generate shellcode via `pwntools` through `pentest_agent_execute_tool`. Use `pwntools` `shellcraft` for standard payloads (e.g., `shellcraft.sh()` for an `execve("/bin/sh")` shellcode) or `pwntools` `asm()` for custom assembly. The generated shellcode is a byte string. Place it in the controlled writable region at a known address.
5. For a `syscall`-based `mprotect` chain without a standalone `pop rdx; ret`: use ret2csu (Phase 3) to set RDX to 7, and use `pop rdi; ret` and `pop rsi; ret` for the other arguments. Alternatively, if RDX already holds a large value at the time of the overflow (common: RDX is set to the number of bytes read by `read()`), skip setting RDX entirely — the existing value may be greater than the required page size, and `mprotect` will apply it to the entire specified length (which may be larger than needed but still works).
6. Alternative: `mprotect` + `read` for staged shellcode. If the writable region is not yet filled with shellcode (e.g., the attacker only has a short overflow), the mprotect chain can be followed by a `read(0, executable_address, length)` chain to read shellcode from stdin into the now-executable region. This requires an additional 6-8 gadget slots for the `read` call. Post-chain: the attacker sends shellcode bytes over the wire after the ROP chain triggers.

### Phase 6 — SROP (Sigreturn-Oriented Programming)

SROP exploits the `rt_sigreturn` syscall to forge an entire register state in a single gadget. Instead of chaining many `pop` gadgets to set registers, the attacker places a crafted `sigframe` structure on the stack (or in a pivot region) and invokes `rt_sigreturn`, which restores all registers — including RIP, RSP, RAX, RDI, RSI, RDX, and segment registers — from the attacker-controlled frame.

1. Understand the `rt_sigreturn` mechanism. When a signal handler returns, the kernel restores the process's register state from a `sigframe` structure saved on the stack. The `rt_sigreturn` syscall (number 15 on x86-64) triggers this restoration. If the attacker can place a fake `sigframe` on the stack and invoke `rt_sigreturn`, the kernel will obediently load all registers from the fake frame — including RIP (the program counter), effectively jumping to any address with full register control.
2. The `sigframe` structure (also called `ucontext_t` or `SigreturnFrame` in pwntools) is a fixed-layout structure of approximately 248 bytes on x86-64. The critical fields: `uc_mcontext.gregs[REG_RIP]` — the instruction pointer to jump to; `uc_mcontext.gregs[REG_RSP]` — the stack pointer; `uc_mcontext.gregs[REG_RAX]` — RAX value; similarly for RDI, RSI, RDX, and other registers. `pwntools` provides the `SigreturnFrame()` class to construct the frame with named fields.
3. SROP chain construction:
   - Find a `syscall; ret` gadget (or a `syscall` followed by any instruction that doesn't crash). The gadget address is the first (and often only) gadget in the traditional SROP chain.
   - Construct the `sigframe` using `pwntools` through `pentest_agent_execute_tool`. Set `rip` to the target address (e.g., `system` address, or a `syscall; ret` gadget for an `execve` syscall). Set `rax` to the desired syscall number if the target is a syscall gadget (e.g., RAX=59 for `execve`). Set `rdi` to the first argument (`"/bin/sh"` address). Set `rsi` and `rdx` to 0. Set `rsp` to a valid stack location (or to the fake frame address + frame size).
   - The payload: `padding + p64(syscall_ret_gadget) + p64(0) + bytes(sigframe)`. The `p64(0)` is a dummy return address consumed by the `syscall; ret` gadget's `ret` before the kernel processes the sigreturn (the kernel expects the `sigframe` immediately after the syscall instruction in memory).
4. Key advantages of SROP:
   - **Compact**: a single gadget plus a 248-byte frame replaces dozens of gadget slots. Ideal for short overflows.
   - **Complete register control**: all registers are set in one operation, including flags and segment registers. No need to find specific `pop` gadgets.
   - **Works on any binary**: the only requirement is a `syscall; ret` gadget (or the ability to reach one). No libc version dependency.
   - **Chaining SROP**: after the first `rt_sigreturn`, the restored `rip` can point to another `syscall; ret` gadget, with the next `sigframe` ready on the stack. This allows executing multiple syscalls with full register control in sequence. Chain two SROP frames: first frame calls `mprotect` (RAX=10), second frame calls `execve` (RAX=59).
5. SROP for `execve` shell directly: set `rip` to `syscall; ret`, `rax` to 59, `rdi` to `"/bin/sh"` address, `rsi` to 0, `rdx` to 0. The kernel restores the frame, the `syscall` executes `execve("/bin/sh", NULL, NULL)`, and the shell spawns — all with a single gadget in the overflow.
6. SROP constraint: the `sigframe` is large (248+ bytes). The overflow must be long enough to accommodate `padding + 8 (syscall gadget) + 8 (dummy ret) + 248 (frame)`. Approximately 300 bytes minimum. If the overflow is shorter, use a pivot (Phase 4) to place the frame in a controlled heap buffer and pivot the stack there first.

### Phase 7 — ret2dlresolve (delayed binding fake relocation)

Ret2dlresolve is a technique that resolves an arbitrary libc function through the binary's own PLT/GOT resolution machinery without needing to know any libc addresses. It forges relocation entries and symbol table entries on the writable stack or heap, then invokes the dynamic linker's `_dl_runtime_resolve` function to resolve and call the target function.

1. Understand the delayed binding process. When a dynamically-linked function (e.g., `system@plt`) is called for the first time, the PLT stub pushes a relocation index and jumps to `_dl_runtime_resolve`. The resolver reads the relocation entry at that index from `.rel.plt`, uses it to find the symbol name in `.dynsym`/`.dynstr`, looks up the symbol in loaded libraries, and writes the resolved address to the GOT. Subsequent calls jump directly to the resolved address.
2. Ret2dlresolve subverts this by providing a fake relocation index that points to an attacker-crafted relocation entry, which in turn references an attacker-crafted symbol entry with the name of the desired function (e.g., `"system"`). The resolver faithfully resolves it, and the PLT stub calls the function.
3. Prerequisites: the binary must be dynamically linked with Partial RELRO (the `.rel.plt` and `.dynamic` sections are writable — but we don't need to write to them; we just need the resolver to follow our fake entries). The attacker must know: the address of `.rel.plt` (or the base of the binary), the address of `.dynsym` and `.dynstr`, and the address of a writable region to place the fake structures.
4. Structure of a fake relocation entry (`Elf64_Rela` or `Elf32_Rel`):
   - `r_offset`: the GOT address where the resolved function address will be written. Can be any writable address; choose a safe location in `.bss` or on the heap.
   - `r_info`: encodes the symbol table index and relocation type. For x86-64, `R_X86_64_JUMP_SLOT = 7`. The symbol index must point to a fake symbol entry controlled by the attacker.
   - `r_addend`: typically 0 for PLT relocations.
5. Structure of a fake symbol entry (`Elf64_Sym`):
   - `st_name`: offset into `.dynstr` where the function name string is located. Attacker places the function name (e.g., `"system\0"`) in a controlled writable region and computes `st_name = fake_str_addr - dynstr_base`.
   - `st_info`, `st_other`, `st_shndx`, `st_value`, `st_size`: set to values that pass the resolver's checks. Use `pwntools` `Ret2dlresolvePayload` class to automatically compute these values.
6. Build the ret2dlresolve payload with `pwntools` through `pentest_agent_execute_tool`. Use `Ret2dlresolvePayload(elf, symbol="system", args=["/bin/sh"])` for a complete payload builder. The generated payload includes: the fake relocation entry, fake symbol entry, function name string, and a ROP chain that calls the PLT stub with the fake relocation index.
7. The ROP chain calls the PLT resolver stub (`plt_init` or `dl_resolve` call at PLT[0]) with the fake relocation index pushed as an argument. On 32-bit x86: push the fake index onto the stack and jump to PLT[0]. On x86-64: place the fake index in the chain, call PLT[0], and the resolver processes the fake entries. The target function is called with the specified arguments.
8. Constraints: ret2dlresolve only works for functions not yet resolved (or if the GOT entry can be reset). The target function name must be present in `.dynstr` or created in controlled memory (the fake string). The technique requires known binary addresses (PIE must be disabled or leaked). The technique works on 32-bit and 64-bit but is more common on 32-bit CTF challenges because the 64-bit relocation structures are more complex (use of `_dl_fixup` internally).
9. Modern alternatives: `pwntools` provides `Ret2dlresolvePayload` for automated structure crafting. Manual crafting is error-prone — prefer the library.

### Phase 8 — bad-byte constraint bypass strategies

When the binary's input routine filters or terminates on specific byte values, the ROP chain must avoid those bytes. Common constraints: null bytes (`0x00`) terminating `strcpy`/`gets`/`scanf("%s")`, newline (`0x0A`) terminating `fgets`/`gets`, and printable-only constraints (byte values 0x20-0x7E only) from `isprint` filters.

1. **Null-byte avoidance (0x00)**. Most x86-64 addresses contain null bytes in their upper 2 bytes (canonical addresses are 48-bit sign-extended, so the upper 16 bits are all 0 for userspace addresses). A `strcpy`-based overflow cannot write null bytes — the copy stops at the first null.
   - **Partial overwrite**: if the overflow length reaches the return address or a pointer, overwrite only the lower 1-2 bytes (which are non-null). The upper bytes retain their original values, which may already be correct. This is effective when ASLR randomizes only the upper bytes and the lower 12 bits (page offset) or lower 2 bytes are constant.
   - **Chain truncation at null**: if the required chain contains null bytes within any address, the chain cannot be written with a null-terminated input. The payload stops at the null byte. Mitigation: avoid addresses with null bytes. Gadgets in the binary's `.text` at low addresses (e.g., `0x400000`-`0x400fff` on x86-64 PIE-disabled binaries) have their upper bytes zero, but `0x004008a3` contains a null byte at position 1. Search for gadget addresses where all 8 bytes (or 4 bytes on x86) are non-null. For libc addresses (`0x7f...`), the lower bytes are typically non-null; the nulls are at the high end. If `strcpy` copies the entire payload before the null terminator, and the chain ends with a libc address, the null bytes in the libc address's upper positions terminate the copy prematurely. Mitigation: place the chain in non-strcpy controlled memory (heap, via pivot), or use `read()`-based overflows (which accept null bytes).
2. **Newline avoidance (0x0A)**. `fgets` and `gets` stop at newline. If any gadget address or argument contains `0x0A`, the payload is truncated.
   - Search for gadgets at addresses that do not contain `0x0A`. Both the binary and libc offer many address choices — `ROPgadget` lists all occurrences; filter out any with `0x0A` in the address bytes.
   - For libc gadgets: after leaking libc base, add the gadget offset to the base. If the resulting address contains `0x0A`, choose a different gadget at a different offset. Libc is large enough that there are usually alternatives.
3. **Printable-only payloads (ASCII-armor)**. The most restrictive constraint: every payload byte must be in the range `0x20`-`0x7E` (printable ASCII). Standard gadget addresses (`0x400...`, `0x7f...`) contain non-printable bytes.
   - **Alphanumeric ROP**: search for gadgets whose addresses are entirely composed of alphanumeric bytes (the range `0x30`-`0x39`, `0x41`-`0x5A`, `0x61`-`0x7A`). These gadgets are rare but do exist in large libraries like libc. Use `ROPgadget` and filter addresses against the alphanumeric range.
   - **Self-modifying chain**: use gadgets that can write arbitrary bytes to a writable region, then jump there. The initial chain (using printable-only addresses) constructs the real chain (with arbitrary bytes) in a controlled buffer and pivots there. This requires a write-what-where primitive built from printable gadgets.
   - **Encoding layer**: if the binary decodes the input (e.g., base64 decodes, hex decodes), encode the full ROP chain (with arbitrary bytes) in the printable encoding. The binary decodes it into a buffer, and a pivot gadget transfers execution there. This bypasses the printable-input restriction entirely because the restriction applies to the input format, not the decoded buffer.
4. **Character set constraints**: some challenges restrict input to specific subsets (digits only, letters only, no spaces, no uppercase, etc.). Map the constraint to a byte filter and apply the same bypass strategy. If the constraint is too restrictive for any gadget address to pass, the encoding-layer approach (the binary's own input processing decodes the payload) is the only viable path.

### Phase 9 — chain verification and GDB single-step debugging

ROP chains are fragile. A single misaligned gadget, unexpected register side-effect, or stack-layout error causes a segmentation fault with minimal diagnostic output. Systematic verification is essential.

1. Run the exploit locally under GDB through `pentest_agent_execute_tool`. Use `GDB with pwndbg` for its ROP-chain visualization features. Set a breakpoint at the `ret` instruction of the vulnerable function (the point just before the chain begins executing). This is the first `ret` that pops the attacker's first gadget address.
2. Single-step through each gadget in the chain. Use GDB's `si` (step instruction) or `ni` (next instruction, stepping over calls). After each gadget's `ret`:
   - Verify RIP is the next expected gadget address (or the call target, if the previous gadget was a `call`).
   - Verify argument registers (RDI, RSI, RDX, RCX, R8, R9) hold the expected values.
   - Verify RSP is progressing through the chain correctly (incrementing by 8 per `ret`, or by more if a gadget pops additional values).
   - Verify the stack contents at RSP are the expected values for the next few steps.
3. Common chain failures and their causes:
   - **SIGSEGV at a `ret` when the popped value is not executable memory**: the chain offset is off by 8 bytes (x86-64) or 4 bytes (x86). Recalculate the offset to the return address. The cyclic pattern offset may have been measured incorrectly.
   - **SIGSEGV inside libc `do_system` or `execve`**: stack alignment issue. Insert a `ret` gadget before the function call to restore 16-byte alignment. On x86-64, `movaps` instructions in libc require RSP % 16 == 0 at function entry (= 8 after the `call` pushes the return address, so RSP before the `ret` into the function must be 16-byte aligned + 8).
   - **Function call succeeds but shell does not spawn**: check arguments. `system("/bin/sh")` requires RDI to point to the string. Ensure the string address is valid and the string is null-terminated. `execve` requires three arguments; ensure RSI and RDX are both zero (not just uninitialized).
   - **Chain works locally but not remotely**: environment differences. The remote libc may be a different build (offsets differ). The remote stack may have different environment variables (affecting stack addresses). The remote binary's stdin/stdout may be a socket (not a terminal), requiring different shell handling (e.g., `sh` may not print a prompt to a non-tty). Use `pwntools` `interactive()` or manually send commands after a short sleep to account for non-tty shell behavior.
4. Debug with core dumps if GDB is not feasible. Enable core dumps (`ulimit -c unlimited`) and inspect the crash address and register state post-mortem. The crash RIP and the stack contents at the crash point often reveal whether the chain reached a bad gadget or jumped to an unexpected address.
5. Log the successful gadget sequence. Once the chain works, record each gadget address, its purpose, and the register state before/after in the evidence log. This is the chain's "assembly listing" and is the reference for any subsequent modifications.

### Phase 10 — multi-stage ROP and pivot-chain composition

Complex exploitation goals (ORW file exfiltration, reverse shell under seccomp, multi-fd file descriptor manipulation) exceed what a single linear chain can achieve. Multi-stage ROP chains separate the exploit into stages, each building on the previous stage's output.

1. **Stage 1 — Information leak**: the first chain leaks an address (libc, heap, or binary code) and returns to the vulnerable function's entry point for a second overflow. This is the standard ret2libc two-stage pattern. The chain calls `puts(got_entry)` or `write(1, got_entry, 8)` and then returns to `main` or the vulnerable function. After receiving the leak, the attacker computes the needed base addresses and sends the Stage 2 payload.
2. **Stage 2 — Primary exploitation**: the second chain uses the leaked addresses to achieve the goal (shell, flag read, etc.). If the goal requires more steps (e.g., open-read-write), this stage may itself be a multi-step chain.
3. **Open-Read-Write (ORW) chain composition**. When `execve` is blocked by seccomp, the goal is to read the flag file and write it to stdout. The ORW chain calls three functions (or syscalls) in sequence:
   - `open("flag.txt", O_RDONLY)` → returns fd (typically 3). Set RDI to the flag path string address, RSI to 0 (O_RDONLY). Call `open` via PLT or syscall (RAX=2).
   - `read(fd, buffer, length)` → reads flag content. Set RDI to the returned fd (typically 3, or a known value if open always returns 3 on a clean process). RSI to a writable buffer address (heap or `.bss`). RDX to a sufficient length (e.g., 100). Call `read` via PLT or syscall (RAX=0).
   - `write(1, buffer, length)` → outputs the flag content. Set RDI to 1 (stdout), RSI to the same buffer, RDX to the same length. Call `write` via PLT or syscall (RAX=1).
   The chain must include all three function calls with argument setup for each. Each function returns to the next function's argument-setup gadgets. The full chain length is 20-40 slots, which may require a pivot.
4. **Chain-to-chain handoff**: between stages, execution must return to a location that allows sending the next payload. Options:
   - Return to `main` — the program restarts, accepting new input for the next stage. Simplest.
   - Return to the vulnerable function directly — bypasses `main`'s initialization and may be faster. Requires knowing the vulnerable function's address.
   - Return to a `read` call that reads more data into a controlled buffer — the next stage is delivered via stdin and written to a known location, from which a pivot executes it.
5. **SROP chaining for multi-syscall execution**: use two consecutive SROP frames. Frame 1 calls `mprotect` (making heap executable), then `rip` in Frame 1 points to the `syscall; ret` gadget with Frame 2 already placed on the stack behind Frame 1. After Frame 1's syscall completes, the kernel restores the next frame (Frame 2), which calls `execve` or `read`+`write`. This chains two syscalls with full register control in a compact payload.
6. **GOT-overwrite as a chain-shortening technique**: instead of building a long ORW chain, use a shorter chain to overwrite a GOT entry (e.g., overwrite `printf@GOT` with `system`). On the next `printf(user_input)` call, the input (e.g., `"/bin/sh"`) is passed to `system`. This compresses a multi-step chain into one write + one triggered call. Requires Partial RELRO and a write primitive (format string, arbitrary write from struct overflow, or a `mov [rdi], rax` gadget).
7. Test each stage independently before connecting them. Run Stage 1 alone to confirm the leak is correct and the program returns to the input function. Run Stage 2 with the leaked addresses hardcoded to confirm the exploit works. Then combine them. Staged failures are easier to debug than a monolithic chain failure.

## Decision points

- **Prefer SROP for short overflows**: if the overflow length is only 300-400 bytes and `syscall; ret` exists, SROP is usually the most compact and flexible option.
- **Prefer ret2csu when `pop rdx` is absent**: search for `pop rdx` first; only fall back to ret2csu if the gadget doesn't exist. ret2csu adds 6-7 slots to the chain.
- **Pivot is mandatory when overflow < 40 bytes**: on x86-64, the absolute minimum for a one-gadget is 8 bytes (one address). For a `system("/bin/sh")` call, minimum is 24 bytes (`pop rdi` + binsh addr + system addr). If available space is below the threshold, a pivot is required.
- **Escalate to `ctf-pwn-heap`**: if the vulnerability is heap-based and stack pivoting from a heap buffer is needed. Hand off with the gadget list and pivot plan.
- **Escalate to `ctf-pwn-basics` ret2libc**: if the chain is a simple two-stage leak + `system("/bin/sh")`, the basic skill is sufficient. Use the advanced ROP skill only when `mprotect`, SROP, ret2csu, or ret2dlresolve are needed.
- **Abandon on Full RELRO + tiny binary + no libc leak**: a tiny statically-linked binary with Full RELRO and no information leak has no gadget source. The binary may need a different exploitation approach entirely.
- **Consider one_gadget first**: before building a complex ROP chain, run `one_gadget` on the provided libc through `pentest_agent_execute_tool`. If a one_gadget constraint is satisfied at the overflow point (common: `rsp+0x30 == NULL` is satisfied when the stack is zeroed), a single address in the overflow location may suffice.

## Prohibited behavior

- Building or deploying ROP chains against production binaries, live services, or any system outside the authorized CTF competition scope.
- Using SROP to forge `rt_sigreturn` frames that execute syscalls outside the challenge's intended scope (e.g., making network connections to external hosts from the challenge environment).
- Deploying multi-stage ROP chains that persist across connections in a way that interferes with other participants' access to the challenge service.
- Using `sudo` or elevated privileges to debug, analyze, or test ROP chains on the analyst's host.
- Storing gadget databases, ROP chain scripts, or shellcode payloads in publicly accessible repositories during an active competition.
- Forging `_dl_runtime_resolve` payloads that resolve functions outside the binary's intended library set.
- Automating ROP chain deployment at rates that degrade competition service availability.
- Using `mprotect` to make system-wide memory regions executable — restrict to the specific page containing the attacker's payload.

## Stop conditions

- Flag recovered and validated. Stop all ROP chain development on this challenge.
- Binary is proven to have no usable gadgets (tiny binary, no libc, no syscall instruction). Document the negative gadget search result.
- SROP frame cannot be placed due to insufficient overflow length and no writable heap/bss region for a pivot. The exploitation path is infeasible with current primitives.
- Remote service becomes unresponsive after chain deployment (likely due to process crash from chain error). Halt and debug locally before further attempts.
- Competition time window expires. Preserve evidence and hand off to report.
- Chain requires a gadget at an address that cannot be represented without violating input constraints (bad bytes with no alternative gadget). Document the constraint analysis.

## Evidence

Record each phase with `pentest_agent_append_evidence`:

```text
Challenge: <competition-name>/<challenge-name>
Binary hash (SHA-256): <64-char hex digest>
Libc hash (SHA-256, if used): <64-char hex digest>
Timestamp: <ISO 8601>

Phase 1 — Protection + budget:
  NX: <enabled | disabled>
  PIE: <enabled | disabled>
  Canary: <enabled | disabled | bypassed>
  RELRO: <partial | full>
  Overflow budget: <N bytes usable past return address>
  Chain slots available: <N / 8>

Phase 2 — Gadget inventory:
  pop rdi; ret: <address> (source: <binary | libc>)
  pop rsi; ret: <address> (source: <binary | libc>)
  pop rdx; ret: <address> (source: <binary | libc | not found — using ret2csu>)
  pop rax; ret: <address> (source: <binary | libc>)
  syscall; ret: <address> (source: <binary | libc | not found>)
  leave; ret: <address> (source: <binary>)
  ret (alignment): <address>

Phase 3 — ret2csu (if used):
  Gadget 1 (pop rbx/rbp/r12/r13/r14/r15): <address>
  Gadget 2 (mov rdx/rsi/edi; call): <address>
  Call target via R12: <function name at GOT address>

Phase 4 — Stack pivot (if used):
  Pivot gadget: <address> (<leave;ret | xchg | pop rsp>)
  Fake stack location: <address> (source: <heap | .bss | .data>)
  RBP overwrite value: <fake_stack_address>

Phase 5 — mprotect + shellcode (if used):
  Target page: <address>
  Page size: <0x1000>
  Protection: <7 (RWX)>
  Shellcode length: <N bytes>
  Shellcode hash (SHA-256): <hash>

Phase 6 — SROP (if used):
  syscall; ret gadget: <address>
  Frame target RIP: <address> (system | syscall;ret for execve)
  Frame RAX: <syscall number>
  Frame RDI: <argument>
  Chained frames: <count>

Phase 7 — ret2dlresolve (if used):
  Target function: <system | execve | other>
  Fake .rel.plt entry at: <address>
  Fake .dynsym entry at: <address>
  Function name string at: <address>

Phase 8 — Bad-byte bypass:
  Constraint type: <null bytes | newline | printable-only | other>
  Affected addresses: <list>
  Mitigation: <partial overwrite | alternative gadget | encoding layer>

Phase 9/10 — Chain verification:
  Chain works locally: <yes | no | partial>
  Chain works remotely: <yes | no>
  Flag status: <recovered | not present>

Decision: <stop — flag captured | escalate to ctf-pwn-heap | abandon>
```

Never store: raw ROP chain payloads with hardcoded addresses, shellcode, libc base addresses for non-CTF infrastructure, flag values in plaintext (use SHA-256 hash), gadget databases for production binaries, SROP frame contents with live register state, or any data from non-authorized targets.

## Report handoff

1. Use `pentest_agent_record_finding` for each successful exploit. Finding types: `ctf-pwn-rop-ret2csu`, `ctf-pwn-rop-stack-pivot`, `ctf-pwn-rop-mprotect-shellcode`, `ctf-pwn-rop-srop`, `ctf-pwn-rop-ret2dlresolve`, `ctf-pwn-rop-orw-chain`, `ctf-pwn-rop-flag-capture`. Include: challenge identifier, protection bypasses achieved, technique summary, gadget sources (binary/libc), and flag hash.
2. For challenge writeups: use the `report-ctf` skill. Provide the evidence log. Describe: the overflow budget, the gadget search methodology, the chosen ROP technique and why it was selected over alternatives, the chain layout (conceptual diagram, not raw addresses), any pivoting or staging decisions, constraint bypasses applied, and the verification process. Keep the description conceptual — no raw shell commands or copy-paste gadget addresses.
3. For failed chains: document the gadget availability matrix (which gadgets were found, which were missing), the failed chain layout, the observed crash behavior (SIGSEGV address, register state), and the hypothesis for the failure. Include the libc fingerprint if the chain works locally but fails remotely.
4. Clean up: remove chain build scripts, gadget search caches, GDB session logs, core dumps, and intermediate payload files from the working directory. Preserve only the evidence log, finding records, and gadget inventory summary.
