---
name: ctf-pwn-basics
description: Binary exploitation basics for CTF — stack buffer overflow, ret2win, offset calculation via cyclic patterns, return-to-libc (two-stage leak + shell), ROP gadget discovery (pop rdi/rsi/rdx, ret), stack alignment, struct/pointer overwrite, signed integer bypass, format string read/write basics, stack canary bypass via leak or brute-force on forking servers, and got/plt overwrite for authorized lab/competition binaries.
disable-model-invocation: true
risk: caution
allowed-modes: [ctf, reverse-engineering]
authorization-required: yes
evidence-outputs: [artifact-hash, binary-analysis-notes, exploit-notes, redacted-flag]
---

# Binary exploitation basics — stack overflows, ret2libc, ROP, format strings, and canary bypass

Use this skill for memory-corruption exploitation of user-space binaries in authorized CTF competitions, lab exercises, or educational environments. Every technique targets challenge-provided binaries running on challenge-controlled infrastructure. Never apply exploitation techniques to production binaries, third-party software, or any system outside the explicit competition scope. This skill covers the foundational exploitation primitives: stack buffer overflow, control-flow hijack via return-address overwrite, argument-controlled ROP chains, format-string read/write, and common protection bypasses. All exploit development should be performed locally against the provided binary. Remote exploitation is permitted only against the designated challenge service and only after the exploit is confirmed locally.

This skill covers: binary triage with protection-audit tooling, vulnerability discovery through disassembly review, offset calculation via De Bruijn cyclic patterns, ret2win exploitation with stack-alignment correction, return-to-libc two-stage attacks (leak libc address, compute base, call system), ROP gadget search strategy for x86-64 calling-convention registers, struct field-overflow exploitation for arbitrary write, format-string read/write primitives using positional parameters and byte-at-a-time writes, and stack-canary bypass through leak, brute-force, and GOT-overwrite approaches. Each technique is presented as a conceptual workflow with specific decision criteria and tool references.

## Required inputs

- Challenge binary (ELF, PE, or Mach-O) with its SHA-256 hash recorded before any analysis or execution.
- Challenge service endpoint (host, port) if the binary is served remotely. For local-only challenges, the binary itself is sufficient.
- Written scope confirming the binary and service belong to an authorized CTF competition, lab exercise, or educational environment. Include competition name, challenge name, allowed tooling, and any restrictions on exploit development.
- For challenges with libc provided: the libc shared object (`.so` file) used by the remote service. Record its hash alongside the binary hash. The libc version determines gadget addresses and function offsets.
- Valid authorization cache for the CTF engagement. Separate authorization if the exploit requires interaction with multiple services or stages.
- Known binary protections: checksec output (NX, Canary, PIE, RELRO, FORTIFY, RPATH/RUNPATH), architecture (x86, x86-64, ARM, MIPS), and word size (32-bit or 64-bit). These are determined in Phase 1.
- Build environment: if the binary requires specific libraries (libc version, linker), the challenge may provide a Dockerfile or a `ld-linux.so` loader. Use these to replicate the remote environment locally.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before any binary analysis or execution.
2. `pentest_agent_parse_scope` for competition rules, lab targets, challenge binaries, and service endpoints. Record binary hashes in scope.
3. `pentest_agent_validate_target` before any remote service interaction. Validate that the endpoint is within competition infrastructure.
4. `pentest_agent_check_authorization` before remote exploitation. Re-check if the exploit requires multiple connections or reveals new service behavior.
5. `pentest_agent_build_command` for dry-run argument preview when using catalog tools: checksec, objdump, GDB, pwntools, ROPgadget, one_gadget, Z3, Python cryptanalysis libraries. Review arguments before execution.
6. `pentest_agent_execute_tool` for all tool execution — never raw shell. This enforces approval gates, timeout boundaries, disabled-category policy, and output redaction.
7. `pentest_agent_append_evidence` after each phase, `pentest_agent_record_finding` for exploits and flags, and report tools for final handoff.

## Workflow

### Phase 1 — binary reconnaissance and protection audit

Before any exploitation attempt, build a complete profile of the binary: its architecture, enabled protections, imported functions, and interesting symbols.

1. Identify the binary architecture using the `file` concept via `pentest_agent_execute_tool`. Record: ELF class (32-bit ELF32 or 64-bit ELF64), instruction set (x86, x86-64, ARM, AArch64, MIPS), endianness (little-endian or big-endian), and whether the binary is dynamically linked or statically linked. A dynamically linked binary imports functions from shared libraries (libc, libpthread); a statically linked binary contains all library code within itself, making ROP gadget availability much higher but also making the binary much larger.
2. Check security protections using `checksec` via `pentest_agent_execute_tool`. Record each protection and its exploitation implications:
   - **NX (Non-Executable stack)**: if enabled, the stack pages are marked non-executable, preventing shellcode placed on the stack from running. This forces a code-reuse attack (ret2libc, ROP) rather than shellcode injection. If NX is disabled (rare in modern CTFs), placing shellcode on the stack and jumping to it is viable.
   - **Stack Canary**: if enabled, a random 8-byte value is placed between the stack buffer and the saved return address. Upon function return, the canary is verified; if corrupted, `__stack_chk_fail` terminates the process. Exploitation requires canary bypass (Phase 9).
   - **PIE (Position Independent Executable)**: if enabled, the binary's code base is randomized at load time (the binary itself is loaded at a random address, like a shared library). All code addresses (functions, gadgets) must be leaked before they can be used. If PIE is disabled, code addresses are fixed and known from the binary file.
   - **RELRO (Relocation Read-Only)**: Partial RELRO means the GOT (Global Offset Table) is writable, allowing GOT overwrite attacks. Full RELRO resolves all GOT entries at load time and marks the GOT read-only, preventing GOT overwrites.
   - **FORTIFY_SOURCE**: if enabled, certain libc functions (`gets`, `sprintf`, `strcpy`) are replaced with bounds-checking variants that abort on buffer overflow. This makes simple stack overflow harder but not impossible — the vulnerability must be in a function that FORTIFY does not guard (e.g., a custom `read()` loop with an incorrect size calculation).
   - **ASLR (Address Space Layout Randomization)**: system-level protection, not binary-level. Randomizes the base addresses of the stack, heap, libc, and (if PIE) the binary itself at each execution. ASLR is typically enabled on the remote server. It does not need to be bypassed directly — instead, leak an address and compute offsets.
3. Extract the symbol table using `objdump` via `pentest_agent_execute_tool`. For dynamic symbols: `objdump -T` shows imported functions (from libc and other libraries) and exported functions. For all symbols (including local): `nm` or `objdump -t`. Look for function names that suggest useful behavior: `win`, `flag`, `shell`, `target`, `get_flag`, `system`, `execve`, `backdoor`, `admin`, `debug`. If the binary has debug symbols (compiled with `-g`), function names and variable names are present in the disassembly, making reverse engineering much easier. If the binary is stripped (no symbols), function names are absent, and analysis must rely on imported-function references and manual reverse engineering.
4. Extract printable strings from the binary: `strings` the binary via `pentest_agent_execute_tool`. Search for: `"/bin/sh"` (the argument string for `system()`), `"flag"`, `"cat flag"`, `"flag.txt"`, file paths (`/home/ctf/flag`), URLs, and error messages. If `"/bin/sh"` exists as a string in the binary, the attacker can pass its address directly to `system()` instead of needing to find it in libc.
5. Disassemble the binary to identify key functions. Use `objdump -d` via `pentest_agent_execute_tool`. Focus on: `main` (entry point logic), any function that reads user input (`gets`, `read`, `scanf`, `fgets`, `recv`), any function that prints output (`puts`, `printf`, `write`, `send`), and any named function from the symbol search (e.g., `win`). If the binary is stripped, locate `main` by finding the function called from `_start` (look for the call instruction after `__libc_start_main` is set up). Identify the vulnerable function by tracing the call path from `main` to any input-reading function with an undersized buffer.

### Phase 2 — vulnerability discovery

Locate the memory-corruption primitive and characterize its constraints.

1. Identify the vulnerable function through disassembly review. Common vulnerable patterns:
   - `gets(buffer)`: reads unlimited input into a fixed-size stack buffer. The canonical stack overflow. The buffer size is visible in the function prologue: `sub $0xNN, %rsp` allocates `0xNN` bytes of stack space.
   - `read(0, buffer, large_size)`: reads up to `large_size` bytes into a buffer smaller than `large_size`. The vulnerability is that `large_size > buffer_capacity`.
   - `scanf("%s", buffer)`: reads a whitespace-delimited string into a fixed-size buffer with no length limit. Equivalent to `gets` but stops at whitespace.
   - `strcpy(dest, src)` / `strcat(dest, src)`: copies a source string into a destination buffer without size checks. If the source string is attacker-controlled and larger than the destination, overflow occurs.
   - `sprintf(buffer, "%s", input)`: formats an attacker-controlled string into a buffer. If the input is larger than the buffer, overflow occurs.
   - Custom `read` loop: a loop that reads one byte at a time until a delimiter (newline, null byte) or a fixed count. If the loop count is larger than the buffer, overflow occurs.
2. Determine the buffer size from the disassembly. In the function prologue, the instruction `sub $0xXX, %rsp` allocates `0xXX` bytes of stack space for local variables. The buffer is allocated at some offset from RSP. The exact buffer size is the distance from the buffer's start to the saved return address. The saved return address is at `RSP + 0xXX` at function entry (after the `sub` instruction adjusts RSP). The saved RBP is at `RSP + (0xXX - 8)` on x86-64. The buffer starts at some lower offset from RSP. Calculate: `offset_to_ret = (allocated_stack_space) + 8_for_saved_RBP` on x86-64 (or `+ 4` on x86). This gives the number of bytes needed to reach the return address.
3. Check for input constraints that complicate exploitation. Does the vulnerable function stop reading at null bytes (`0x00`)? If so, addresses containing null bytes cannot be written directly — use partial overwrites or find gadgets at null-byte-free addresses. Does the function stop at newline (`0x0A`)? If so, payload bytes cannot contain `0x0A` (or must encode around it). Does the function accept only printable characters? If so, addresses must be composed of printable bytes. Does the function limit the total input length? If the maximum input is less than the offset to the return address, direct return-address overwrite is impossible — look for alternative vulnerabilities (off-by-one, partial overwrite of saved RBP).
4. Map the program's control flow after the vulnerable function returns. Does it return to `main` (looping for another exploit attempt)? Does it call `exit()` (preventing repeated interaction)? Does it print something before returning (allowing a leak)? The post-overflow behavior determines whether a multi-stage exploit is feasible.
5. If the binary has multiple input opportunities, test each independently. A binary might: prompt for a name, then a message. The name buffer might be small but safe, while the message buffer overflows. Or: the first input might not overflow but leaks a stack address, which is then used to bypass ASLR in a second-stage overflow.

### Phase 3 — offset confirmation via cyclic pattern

Before building a payload, confirm the exact byte offset from the buffer start to the return address on the stack.

1. Generate a De Bruijn sequence (cyclic pattern) via `pwntools` through `pentest_agent_execute_tool`. The De Bruijn sequence of order K ensures every K-byte subsequence is unique. A length of 200-500 bytes is typical; generate longer if the buffer is large. `pwntools` provides `cyclic(length)` to generate the pattern and `cyclic_find(value)` to look up the offset.
2. Feed the cyclic pattern as input to the binary. Run the binary locally through `pentest_agent_execute_tool` with the pattern piped to stdin or passed as an argument. The binary crashes with a segmentation fault. The crash reveals which bytes overwrote the return address.
3. On x86-64: when the `ret` instruction executes, it pops the top 8 bytes of the stack into RIP. However, the value at RSP after the overflow is not the return address — it's the 8 bytes that come after the return address in the payload (because the `ret` already popped the return address). To find the actual return-address offset: look at the segmentation fault address reported by the kernel or in the core dump. This address is the corrupted RIP value. Search for this value in the cyclic pattern to find the offset. Alternatively, run under GDB via `pentest_agent_execute_tool`: set a breakpoint at the `ret` instruction of the vulnerable function, examine RSP, and read the 8 bytes at RSP. Those 8 bytes are the cyclic-pattern fragment that landed at the return-address position. Look up those bytes in the pattern to find the offset.
4. On x86 (32-bit): the return address is popped directly into EIP. The crash address is the return-address value. Look up the 4-byte crash address in the cyclic pattern.
5. Once the offset is confirmed, record it in evidence: `offset_to_ret = N bytes`. This is the exact number of padding bytes that must precede the target address in the payload.

### Phase 4 — ret2win (simplest control-flow hijack)

If the binary contains a function that prints the flag or spawns a shell (commonly named `win`, `flag`, `shell`, `get_flag`, `target`, `backdoor`), the exploit is a single-stage payload: padding + address of win function.

1. Find the win function address. If PIE is disabled (confirmed in Phase 1), the address from `objdump -d` is the runtime address. Copy it directly. If PIE is enabled, the address is randomized — this requires a leak first. Skip to Phase 5 (ret2libc leak pattern) but target the win function address instead of a libc address.
2. Build the payload: `padding_bytes + p64(win_address)`. The padding is exactly `offset_to_ret` bytes of any non-null, non-newline filler (e.g., 'A' or any printable character). `p64()` converts the address to an 8-byte little-endian representation. For 32-bit binaries, use `p32()` with 4-byte addresses.
3. Handle stack alignment on x86-64. The System V AMD64 ABI requires the stack to be 16-byte aligned when executing a `call` instruction. When the vulnerable function returns via `ret`, RSP is incremented by 8 (the popped return address). If the stack was 16-byte aligned before the `ret`, it becomes 16-byte aligned + 8 after the `ret` — misaligned for the next function. This manifests as a crash in `movaps` instruction inside libc (`movaps` requires 16-byte alignment). Fix: add a `ret` gadget before the win function address. The gadget `ret` pops another 8 bytes (correcting the alignment) and then jumps to the next address on the stack. Payload becomes: `padding + p64(ret_gadget) + p64(win_address)`. Find a `ret` gadget using `ROPgadget` via `pentest_agent_execute_tool`: search for `: ret$` (a lone `ret` instruction at any address). Use objdump: `objdump -d binary | grep -A1 ret` and pick any address containing the single-byte instruction `0xC3` (ret).
4. Test locally first. Run the binary with the payload via `pentest_agent_execute_tool`. Use `pwntools` to manage process I/O and to receive the flag output. If the local test succeeds (flag printed or shell obtained), the exploit is ready for the remote target.
5. Send the exploit to the remote service via `pentest_agent_execute_tool`. Use `pwntools` remote connection or a custom socket script. Receive the output and extract the flag.

### Phase 5 — return-to-libc (two-stage leak + shell)

When the binary has no win function but imports libc functions (`system`, `execve`), redirect execution to `system("/bin/sh")` by first leaking a libc address to bypass ASLR.

1. **Stage 1 — leak a libc address**. The binary calls libc functions (e.g., `puts`, `printf`, `write`, `send`). These functions have their addresses resolved in the GOT at runtime. Their GOT entries contain the actual libc address of the function. Build a ROP chain that calls one of these functions with a GOT entry as the argument:
   - Find a `pop rdi; ret` gadget in the binary (Phase 6). This is needed to pass the first argument.
   - Find the GOT address of a function that has been called at least once (so its GOT entry is resolved). `puts@GOT` is a common target.
   - Find the PLT address of `puts` (the stub that jumps to the resolved libc function).
   - Build the Stage 1 payload: `padding + p64(pop_rdi) + p64(puts_GOT) + p64(puts_PLT) + p64(vuln_func_entry)`. This calls `puts(puts_GOT)`, which prints the raw bytes of the libc address of `puts`, then returns to the vulnerable function's entry point for Stage 2.
   - Receive the leaked address. It will be 6 raw bytes (on x86-64, libc addresses are in the 0x7fXXXXXXXXXX range, with the top 2 bytes zero). Decode the bytes to an integer.
2. **Identify the libc version**. The leaked address of `puts` reveals its offset from the libc base. Use the provided libc (if the challenge provides a `.so` file) or identify the version using a libc database. With the provided libc: read the offset of `puts` from the libc's symbol table (`objdump -T libc.so | grep puts`). The libc base is `leaked_puts_addr - puts_offset_from_libc`.
3. **Find `system` and `/bin/sh` in libc**. Read their offsets from the provided libc: `objdump -T libc.so | grep ' system$'` for the `system` function offset, and `strings -a -t x libc.so | grep /bin/sh` for the `/bin/sh` string offset. Compute runtime addresses: `system_addr = libc_base + system_offset`, `binsh_addr = libc_base + binsh_offset`.
4. **Stage 2 — call system("/bin/sh")**. Build the Stage 2 payload: `padding + p64(ret_gadget_for_alignment) + p64(pop_rdi) + p64(binsh_addr) + p64(system_addr)`. This sets RDI to the address of `"/bin/sh"` and calls `system()`. Send the payload after the leak. The binary spawns a shell. Interact with the shell to read the flag.
5. **Alternative: one_gadget for simpler exploitation**. `one_gadget` is a tool that finds "magic gadgets" in libc — addresses that, when jumped to, execute `execve("/bin/sh", NULL, NULL)` directly if certain register/stack conditions are met. Use `one_gadget` via `pentest_agent_execute_tool` on the provided libc. It outputs a list of candidate addresses and the constraints (e.g., "RSP+0x30 == NULL", "RAX == NULL"). Choose a candidate with constraints that are satisfied at the time of the return (often the simplest ones are satisfied in a basic overflow). Use the one_gadget address instead of the `system` chain: `padding + p64(one_gadget_address)`. This is shorter and requires no argument setup but is libc-version-specific. Test one_gadget locally first — not all candidates work in all stack states.

### Phase 6 — ROP gadget discovery strategy

Return-Oriented Programming (ROP) uses short instruction sequences ending in `ret` ("gadgets") to build arbitrary computation. Essential gadgets for x86-64 calling convention must set registers for function arguments.

1. Understand the x86-64 System V calling convention: first argument goes in RDI, second in RSI, third in RDX, fourth in RCX, fifth in R8, sixth in R9. Additional arguments go on the stack. For most libc functions (`system`, `execve`, `open`, `read`, `write`), only the first few arguments are needed. For `system("/bin/sh")`: only RDI matters (address of the string). For `write(fd, buf, len)`: RDI = 1 (stdout), RSI = address of buffer, RDX = length. For `execve("/bin/sh", NULL, NULL)`: RDI = address of "/bin/sh", RSI = 0, RDX = 0.
2. Find `pop rdi; ret` — the most essential gadget. It pops the next 8 bytes from the stack into RDI and then returns to the following address. Search the binary first (if PIE disabled or base known) using `ROPgadget` via `pentest_agent_execute_tool`. Supply the binary path and search for `pop rdi`. If the binary itself does not have the gadget, search libc (requires a leak first). Libc is larger and almost always has `pop rdi; ret`.
3. Find `pop rsi; ret` (or `pop rsi; pop r15; ret`, which is common and also works — the extra value popped into R15 is simply discarded). Search both binary and libc.
4. Find `pop rdx; ret` — this is the rarest of the common gadgets. Standalone `pop rdx; ret` is uncommon. More common variants: `pop rdx; pop rbx; ret` or `pop rdx; pop r12; ret`. Accept these — the extra pop into RBX or R12 is harmless (just add padding in the ROP chain). If no `pop rdx` gadget exists, use the `__libc_csu_init` gadget (ret2csu technique): the CSU gadget moves values from R13 into EDI, from R14 into RSI, and from R15 into RDX, then calls a function pointer. This provides a way to set all three argument registers. Set up the registers via prior gadgets, then invoke the CSU gadget.
5. Find `ret` gadget for stack alignment (as described in Phase 4). Any address containing the single byte `0xC3` works.
6. For 32-bit x86: arguments are passed on the stack, not in registers. No `pop` gadgets are needed. The ROP chain places function addresses and arguments directly on the stack in order: `padding + system_addr + dummy_return_addr + binsh_addr`. The `dummy_return_addr` is where `system` returns to after executing (can be a dummy value or a clean exit function). This makes 32-bit exploitation simpler than 64-bit for ROP purposes.
7. Gadget discovery in large binaries (statically linked, or libc): use `ROPgadget --depth 5` to find longer chains. Longer gadgets may combine useful operations: `pop rdi; pop rsi; pop rdx; ret` sets all three registers in one gadget. `mov qword [rax], rdi; ret` provides a write primitive. Filter gadgets by relevance.
8. Verify gadget operability: some gadgets found by automated tools may crash due to preceding instructions that modify the stack or registers in unexpected ways. Test the gadget chain in GDB: set a breakpoint at the first gadget address, step through each instruction, and verify the register values after each gadget. If a gadget behaves unexpectedly, check the preceding 1-2 instructions in the disassembly — the automated tool may have selected the gadget starting mid-instruction or included an unintended prefix.

### Phase 7 — struct and pointer overwrite exploitation

When the overflow does not directly reach the return address, but a struct containing a function pointer or data pointer is adjacent to the buffer on the stack or heap, overwrite the pointer to gain control or achieve arbitrary write.

1. Identify the struct layout from the disassembly or decompiled source. Look for accesses to the stack frame at offsets: `[rbp - 0xNN]` or `[rsp + 0xNN]`. The disassembly reveals the buffer address and the pointer address. Calculate the distance from the buffer to the pointer field.
2. For stack-based struct overflows: the buffer is at a lower address; the struct fields (including a pointer) are at a higher address. Overflow the buffer with padding until reaching the pointer field, then overwrite the pointer with a target address.
3. **Function pointer overwrite**: if the struct contains a function pointer that is called later in the program (e.g., `(*handler)(data)` or a vtable dispatch), overwrite the pointer with the address of `win()` or `system()` or a one_gadget. When the pointer is called, execution redirects to the attacker's chosen function.
4. **Data pointer overwrite for arbitrary write**: if the struct contains a data pointer, and later code dereferences and writes to that pointer (e.g., `*grade_ptr = new_value` or `strcpy(record->name, input)`), overwrite the data pointer with a target address. The subsequent write becomes an arbitrary-write primitive. Use this to overwrite a GOT entry: the GOT contains the runtime address of libc functions. Overwrite `printf@GOT` with the address of `system`. Then, the next time the program calls `printf`, it actually calls `system` — with the argument to `printf` passed as the argument to `system`. If the program later calls `printf("/bin/sh")` or `printf(user_input)`, control of the argument grants a shell.
5. **GOT overwrite technique step-by-step**: find the GOT address of a function called after the arbitrary-write primitive executes. Common targets: `exit@GOT` (called when the program terminates), `printf@GOT` (called to print output), `free@GOT` (called to deallocate memory). Compute the target address (win, system, one_gadget). Perform the arbitrary write: overwrite the GOT entry bytes with the target address. On the next call to the overwritten function, execution redirects. For Partial RELRO: the GOT is writable, so this works. For Full RELRO: the GOT is read-only, so this fails — look for alternative writable targets (`__malloc_hook`, `__free_hook` in libc, or function pointers on the heap).
6. **Size field overwrite**: if the struct contains a size field that controls how much data is read in a subsequent input operation, overflow to set the size field to a large value. The subsequent read becomes a secondary overflow with a much larger buffer, reaching the return address. This converts a limited overflow (reaches only the size field) into a full overflow (reaches the return address).
7. **Signed integer bypass**: if the program checks `if (index >= array_size)` but uses a signed comparison, a negative index passes the check. For example, `index < 0` is not checked separately, and `if (index >= 20)` allows `index = -1` (which is `0xFFFFFFFF` as unsigned and greater than 20 in signed comparison, but if the comparison is signed, `-1 < 20` is True — wait, no: `-1 < 20` in signed comparison IS true, so `if (index >= 20)` rejects `-1`. The bypass works when the check is `if (index > 20)` and index is `-1`: `-1 > 20` is false in signed comparison, so the index passes. Test with negative values to see if bounds-checking uses signed comparison. If a negative index is allowed, the accessed offset `base + index * element_size` can point to memory before the array (including the stack canary or return address). Use this to read or write out-of-bounds.

### Phase 8 — format string vulnerability basics

When the binary passes attacker-controlled input directly as the format argument to `printf` (or `sprintf`, `fprintf`, `snprintf`), the attacker can read from and write to arbitrary memory using format specifiers.

1. Confirm the vulnerability: the binary calls `printf(user_input)` where `user_input` is directly from stdin or a network socket. Send `AAAA%p.%p.%p.%p.%p.%p.%p.%p` as input. If the output contains hex values interspersed with `AAAA`, the format string vulnerability is confirmed. If the output contains only the literal input (the `%p` specifiers are not expanded), the binary uses `printf("%s", user_input)` and is not vulnerable.
2. **Find the argument offset**: send a pattern like `AAAA%p` repeated 10-20 times, separated by dots. The output shows the stack values as hex. Locate `0x41414141` (the ASCII representation of "AAAA" as a hex value) in the output. The position where it appears (e.g., at the 6th `%p`) is the offset where the attacker's input starts on the stack. This offset is used in `%<offset>$` syntax to directly reference a specific stack position.
3. **Read primitive via `%s`**: to read a string from an arbitrary address, place the target address at a known stack position (e.g., at the beginning of the format string), then use `%<offset>$s` to dereference that address. The `%s` specifier reads the value at the stack position, interprets it as a pointer, and prints the null-terminated string at that pointer. For example, if the offset is 6, the payload `\x08\xa0\x04\x08%6$s` (with the actual target address bytes) prints the string at address `0x0804a008`. Use this to leak GOT entries (to find libc base) or to read the flag from a known memory location.
4. **Write primitive via `%n`**: the `%n` specifier writes the number of characters printed so far to the address pointed to by the corresponding stack argument. For a byte-at-a-time write: use `%hhn` (writes a single byte). The payload is `[target_address][target_address+1]...[padding]%<offset1>$hhn%<offset2>$hhn...`. The addresses are placed at the beginning of the format string (aligned to 4 or 8 bytes). Each address is at a specific stack offset. The `%<number>c` specifier prints `<number>` characters (used to set the character count for `%n`). Then `%<offset>$hhn` writes the character count as a byte to the address at that stack offset. Chain multiple `%hhn` writes to write a multi-byte value (e.g., a 4-byte or 8-byte address) one byte at a time, from least significant to most significant.
5. **GOT overwrite via format string**: the canonical format-string exploitation target. Place the target GOT addresses (e.g., `printf@GOT`, `printf@GOT+1`, `printf@GOT+2`, `printf@GOT+3` for a 4-byte write) at the start of the format string. Use `%hhn` writes to overwrite each byte of the GOT entry with the corresponding byte of the target address (e.g., `system` or `win`). After the format string is processed, the program continues execution. When the overwritten function is next called, execution redirects to the target.
6. **Alternative write targets**: `__malloc_hook` (in libc, called whenever `malloc()` is invoked, before the actual allocation), `__free_hook` (called whenever `free()` is invoked), `exit_funcs` (the `atexit` handler list, called on program exit), or the return address on the stack (located by the argument offset). For `__malloc_hook` and `__free_hook`: these are writable in libc (even with Full RELRO, because they are in the data segment of libc). Overwrite `__malloc_hook` with the address of `system` or a one_gadget, then trigger a `malloc` call (by sending a large input that forces internal buffer allocation, or by exploiting a code path that calls `malloc`). The hook is called with no controlled arguments, so a one_gadget is typically needed. For `__free_hook`: overwrite it, then trigger a `free` call. The argument to `free` is the pointer being freed — if that pointer points to `"/bin/sh"`, then with `__free_hook` set to `system`, `free(ptr)` becomes `system(ptr)` and spawns a shell.
7. **Bypass format-string length limits**: if the vulnerable `printf` is limited in how many characters it processes (e.g., `printf` with a truncating wrapper), build the minimal payload. Use the stack offset closest to the format string start for the first write. Prefer `%hhn` (1 byte) over `%hn` (2 bytes) over `%n` (4 bytes) to minimize printed character counts. If the target address value would require printing massive numbers of characters (e.g., writing `0x7f` requires printing 127 characters), break it into byte writes: writing `0x7f` directly via `%hhn` requires 127 characters printed, but writing `0x7f12abcd` as four bytes requires four separate `%hhn` writes with character-count padding between them.

### Phase 9 — stack canary bypass techniques

A stack canary is a random 8-byte value placed between the buffer and the return address. It is checked before the function returns — if the canary has changed, `__stack_chk_fail` aborts the process. Bypasses fall into four categories.

1. **Canary leak via information disclosure**: if the binary prints the buffer contents back to the user (e.g., `puts(buffer)` after `read`) and the buffer overflow can reach the canary without overwriting it fully, the printed output reveals the canary bytes. Overflow up to and including the canary byte by byte. For example, if the buffer is 32 bytes and the canary starts at offset 32, send 33 bytes of non-null filler — the 33rd byte overwrites the first byte of the canary with a non-null value. The printed output will contain the remaining 7 canary bytes plus the null terminator. Then send 34 bytes, overwriting 2 bytes of the canary, and recover 6 bytes. Iterate until all 8 canary bytes are known (the first byte of the canary on Linux is always `0x00` to prevent string-based leaks, so only 7 bytes need discovery, but the null byte itself must be preserved in the payload). Reassemble the canary bytes in little-endian order.
2. **Brute-force canary on forking servers**: if the challenge service forks a new child process for each connection, the canary is inherited from the parent and remains constant across connections. Brute-force one byte at a time: for each canary byte position (2 through 8, since byte 0 is always `0x00`), try all 256 possible values. For each candidate, send a payload that overwrites the buffer up to and including the canary byte being tested. If the candidate is correct, the connection stays alive (the program doesn't crash because the canary check passes). If the candidate is wrong, the child crashes (the parent survives). The attacker detects the difference through the connection behavior: a correct byte results in the program proceeding to the next step; an incorrect byte causes a connection drop or an error message. After determining each byte, move to the next position. This requires 256 * 7 = 1792 connections in the worst case. This is feasible within CTF time boxes if the server allows rapid reconnections.
3. **Overwrite canary master copy in TLS**: the canary value is stored in the Thread-Local Storage (TLS) area, at a fixed offset from the `fs` segment register on x86-64 (`fs:0x28`). If the attacker has an arbitrary write primitive (e.g., format string, struct pointer overwrite), overwrite the TLS canary with a known value, then overwrite the stack canary with the same known value. The check passes because both copies match. The TLS address can be found by leaking a stack address (the canary on the stack points to TLS) and computing the TLS base.
4. **Overwrite `__stack_chk_fail` GOT entry**: if Partial RELRO is enabled (GOT is writable), overwrite the GOT entry for `__stack_chk_fail` with the address of a harmless function (or simply with `ret`). When the canary check fails, instead of aborting, the program jumps to `ret` and continues execution. This effectively disables canary protection for the process. Requires either an arbitrary write primitive or a format string vulnerability that executes before the canary check.
5. **Canary bypass on 32-bit x86**: the canary concept is identical, but the canary is 4 bytes instead of 8. Brute-force is slightly faster (256 * 3 = 768 connections for bytes 1-3, assuming byte 0 is null).
6. After recovering the canary, build the payload: `padding + canary_value + saved_RBP_filler + exploit_chain`. The saved RBP filler is the 8 bytes (or 4 bytes on 32-bit) that overwrite the saved base pointer. This value can be arbitrary junk — it does not affect the canary check and is only used when the calling function returns. The `exploit_chain` is the return-address overwrite (ret2win, ret2libc, ROP chain) as described in earlier phases.

## Decision points

- **Stop on ret2win success**: if the binary has a `win` function and PIE is disabled, exploit immediately. No leak needed.
- **Stop on full shell obtained**: after ret2libc or one_gadget shell spawns, read the flag and stop exploitation.
- **Escalate to `ctf-pwn-rop` skill**: if the binary requires a complex multi-stage ROP chain (e.g., `mprotect` + shellcode, SROP, or stack pivot), hand off with the leak and gadget analysis.
- **Escalate to `ctf-pwn-heap` skill**: if the vulnerability is a heap overflow, use-after-free, or double-free rather than a stack overflow.
- **Escalate to `ctf-reverse` skill**: if the binary is complex and the vulnerability is not immediately obvious from disassembly review. The reversing skill can produce a more detailed control-flow analysis.
- **Downgrade to brute-force**: if ASLR entropy is low (e.g., 32-bit without PIE), brute-forcing the return address may be faster than building a leak. Try the exploit with a guessed address; repeat until success.
- **Abandon if binary is fully fortified**: if NX, Full RELRO, PIE, Canary, and FORTIFY are all enabled, AND no information leak is available, stack-based exploitation from a single overflow may be infeasible. Escalate to broader workflow review.
- **Ask for hint on canary bypass**: if three canary bypass approaches fail, the challenge may have an unconventional bypass mechanism. Review the binary for custom canary implementations or check if the challenge description provides a hint about the canary value.

## Prohibited behavior

- Exploiting binaries outside the authorized CTF competition or lab environment.
- Running exploit payloads against production servers, real-world services, or third-party infrastructure.
- Using the shell obtained from exploitation to access other teams' challenge instances, competition infrastructure, or non-challenge systems.
- Reusing exploit techniques discovered in CTF challenges to attack real software without the vendor's authorization.
- Automating exploit deployment at rates that degrade the competition service or trigger anti-abuse defenses.
- Storing exploit scripts, shellcode, or crafted payloads in publicly accessible repositories during an active competition.
- Executing challenge binaries without confinement: run binaries in an isolated container or virtual machine, never directly on the analyst's host operating system.
- Using `sudo` or elevated privileges to debug, analyze, or exploit challenge binaries.
- Modifying challenge binaries (patching, stripping, recompiling) unless the challenge explicitly permits binary modification as a solution technique.
- Sharing unredacted flags, exploit payloads, or challenge solutions during an active competition.

## Stop conditions

- Flag recovered and validated. Stop all exploitation on this challenge.
- Binary analysis reveals that the vulnerability is not exploitable under current protections (e.g., all protections enabled with no leak possible). Cease exploitation attempts; record the analysis in evidence.
- Remote service becomes unresponsive or returns errors indicating the challenge infrastructure has failed. Stop remote interaction; preserve local analysis.
- Competition time window expires. Complete partial evidence and hand off to report.
- Exploit requires a level of privilege escalation that is not permitted by the competition rules (e.g., exploiting the host kernel from inside a container when the challenge scope is user-space only).
- Binary triggers antivirus, EDR, or security monitoring on the analyst's workstation. Isolate the binary and continue analysis in a sandboxed environment.

## Evidence

Record each phase with `pentest_agent_append_evidence`:

```text
Challenge: <competition-name>/<challenge-name>
Binary hash (SHA-256): <64-char hex digest>
Libc hash (SHA-256, if provided): <64-char hex digest>
Timestamp: <ISO 8601>

Phase 1 — Protection audit:
  Architecture: <x86-64 | x86 | ARM | MIPS>
  NX: <enabled | disabled>
  Canary: <enabled | disabled>
  PIE: <enabled | disabled>
  RELRO: <partial | full>
  FORTIFY: <enabled | disabled>
  Interesting symbols: <win, flag, shell, ... | none>
  Useful strings: <"/bin/sh" found at 0x... | not found>

Phase 2 — Vulnerability discovery:
  Vulnerable function: <name or address>
  Vulnerability type: <gets overflow | read overflow | strcpy | format string | struct overflow>
  Buffer size (estimated): <N bytes>
  Offset to return address (estimated): <N bytes>

Phase 3 — Offset confirmation:
  Cyclic pattern length: <N bytes>
  Crash address: <0x...>
  Confirmed offset to return address: <N bytes>

Phase N — Exploitation:
  Technique: <ret2win | ret2libc | one_gadget | GOT overwrite | format string write | struct overwrite>
  Leaked libc address (if applicable): <0x...> → libc base: <0x...>
  Gadgets used: <pop rdi at 0x... | ret at 0x... | one_gadget at 0x...>
  Shell obtained: <yes | no>
  Flag status: <recovered | not present>

Decision: <stop — flag captured | escalate to ctf-pwn-rop | escalate to ctf-pwn-heap | abandon>
```

Never store: raw exploit payloads with hardcoded target addresses, shellcode, leaked libc addresses for real services, flag values in plaintext (use hash), or any data from non-authorized targets.

## Report handoff

1. `pentest_agent_record_finding` for each successful exploit. Finding types: `ctf-pwn-ret2win`, `ctf-pwn-ret2libc`, `ctf-pwn-rop`, `ctf-pwn-format-string`, `ctf-pwn-got-overwrite`, `ctf-pwn-canary-bypass`, `ctf-pwn-flag-capture`. Include: challenge identifier, vulnerability type, protection bypasses achieved, exploitation technique summary, and flag hash.
2. For challenge writeups: use the `report-ctf` skill. Provide the evidence log. Describe: binary protections, vulnerability discovery (which function, what input, what size), offset calculation method, exploitation technique (conceptual, not raw code), canary bypass method (if applicable), and final flag recovery. Keep the description conceptual — no raw shell commands, no copy-paste exploit code.
3. For failed exploits: document all attack paths attempted, the protection that blocked each path, and any partial progress (e.g., "canary leaked but ret2libc fails because libc version is unknown"). Include the libc fingerprint (leaked function addresses, symbol offsets) so a libc database lookup can be attempted later.
4. Clean up: remove exploit scripts, core dumps, GDB session logs, and intermediate payload files from the working directory. Preserve only the evidence log and finding records.
