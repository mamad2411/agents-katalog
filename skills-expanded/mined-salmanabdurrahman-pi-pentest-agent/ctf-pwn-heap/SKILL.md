---
name: ctf-pwn-heap
description: Heap exploitation CTF workflow — tcache poisoning (glibc 2.27-2.34), safe-linking bypass (glibc 2.32+), fastbin dup/consolidation attacks, unsorted bin libc leak, House of Force (top chunk corruption), House of Botcake (tcache+unsorted overlap), largebin attack for arbitrary write, off-by-one null byte (poisoned null byte consolidation / House of Einherjar), FSOP via _IO_FILE corruption (House of Apple 2), seccomp bypass via alternative syscalls (openat2, execveat, sendfile), and heap grooming/defragmentation for deterministic layout for authorized lab/competition binaries.
disable-model-invocation: true
risk: caution
allowed-modes: [ctf, reverse-engineering]
authorization-required: yes
evidence-outputs: [artifact-hash, heap-analysis-notes, exploit-notes, redacted-flag]
---

# Heap exploitation — tcache, fastbin, unsorted bin, FSOP, and seccomp bypass

Use this skill for heap-based memory-corruption exploitation of user-space binaries in authorized CTF competitions, lab exercises, or educational environments. Every technique targets challenge-provided binaries running on challenge-controlled infrastructure. Heap exploitation relies on corrupting allocator metadata to achieve arbitrary read/write, overlapping chunk allocation, or control-flow hijack. The glibc ptmalloc allocator version determines which techniques are viable and which integrity checks must be bypassed.

This skill covers: glibc version fingerprinting and allocator baseline, heap interaction primitive identification, unsorted bin libc address disclosure, tcache safe-linking decode for heap base recovery, tcache poisoning for arbitrary allocation, fastbin dup and consolidation attacks, off-by-one null byte exploitation via House of Einherjar, House of Botcake for tcache-unsorted overlap, FSOP via _IO_FILE corruption (House of Apple 2), and seccomp policy bypass through alternative syscalls for shell acquisition. Each technique is presented as a conceptual workflow with version-specific decision criteria. All exploit development must be performed locally against the provided binary and matching libc. Remote exploitation is permitted only against the designated challenge service and only after local confirmation.

## Required inputs

- Challenge binary (ELF) with its SHA-256 hash recorded before any analysis or execution.
- Challenge service endpoint (host, port) if the binary is served remotely. For local-only challenges, the binary itself is sufficient.
- The libc shared object (`.so` file) used by the remote service — this is essential for heap exploitation because offsets, hooks, and allocator internals differ between libc builds. Record its hash alongside the binary hash. If no libc is provided, the leak phase must identify the libc version through a database lookup.
- Written scope confirming the binary and service belong to an authorized CTF competition, lab exercise, or educational environment. Include competition name, challenge name, allowed tooling, and any restrictions.
- Valid authorization cache for the CTF engagement. Re-authorization required if the exploit chain spans multiple stages, services, or credential domains.
- Build environment matching the remote: the provided libc, the correct dynamic linker (`ld-linux.so`), and any challenge-supplied Dockerfile or setup script. Use these to replicate the remote heap behavior locally — heap layout is sensitive to environment variables, thread count, and allocator state.
- Known binary protections from a prior `ctf-pwn-basics` skill run or fresh `checksec` audit: NX, Canary, PIE, RELRO, ASLR. Heap exploitation typically requires at least one information leak (libc address, heap address, or both) before control-flow hijack is possible.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before any binary analysis or execution.
2. `pentest_agent_parse_scope` for competition rules, lab targets, challenge binaries, libc files, and service endpoints. Record all hashes in scope.
3. `pentest_agent_validate_target` before any remote service interaction. Confirm the endpoint is within competition infrastructure.
4. `pentest_agent_check_authorization` before remote exploitation or any active heap interaction with the remote service. Re-check if a leak reveals version-specific behavior requiring a different libc.
5. `pentest_agent_build_command` for dry-run argument preview when using catalog tools: `checksec`, `objdump`, `readelf`, `GDB with pwndbg`, `pwntools`, `ROPgadget`, `one_gadget`, `libc-database`, `seccomp-tools`, `patchelf`.
6. `pentest_agent_execute_tool` for all tool execution — never raw shell. This enforces approval gates, timeout boundaries, disabled-category policy, and output redaction.
7. `pentest_agent_append_evidence` after each phase, `pentest_agent_record_finding` for successful exploits and flags, and report tools for final handoff.

## Workflow

### Phase 1 — glibc version fingerprinting and heap allocator baseline

The glibc version determines which heap exploitation techniques are viable. Each version introduces new integrity checks that close previous attack paths while opening new ones. Before any exploitation attempt, identify the exact libc build the binary is linked against.

1. Determine which libc the binary loads using `ldd` through `pentest_agent_execute_tool`. The output shows the path to `libc.so.6` and its base name. If the binary is dynamically linked, libc is loaded from the system path or a challenge-provided directory. If statically linked, heap internals are embedded in the binary itself — the version must be identified by symbol patterns or string references.
2. Extract version identification strings from the libc file. Use `strings` through `pentest_agent_execute_tool` on the libc shared object, filtering for the GNU C Library banner. The banner line typically reads `GNU C Library (Ubuntu GLIBC X.Y-Zubuntu...) stable release version X.Y`. This gives the distribution, upstream version, and package revision. Record the exact banner text in evidence.
3. Understand version-specific allocator characteristics. Key milestone versions and their exploitation implications:
   - **glibc 2.23-2.26**: tcache does not exist. Only fastbin (sizes 0x20-0x80 on x86-64) and regular bins (small, large, unsorted) are available. Fastbin dup is trivial with no integrity checks. `__malloc_hook` and `__free_hook` exist and are primary targets for control-flow hijack.
   - **glibc 2.27-2.28**: tcache introduced — a per-thread cache of singly-linked free lists for sizes 0x20 to 0x410 (up to 64 entries, 7 per size). No integrity checks on tcache fd pointer and double-free detection is absent. Tcache poisoning (corrupting fd to point to an arbitrary address) is the simplest heap exploitation path. `__malloc_hook` and `__free_hook` still present.
   - **glibc 2.29-2.31**: tcache key field added — each freed tcache chunk has a `key` field (at offset 0x8 from the user data start) set to `tcache_perthread_struct` address. When freeing, the allocator checks this key — if it matches, a double-free is detected (the chunk is already in tcache). Bypass: clear the key field before the second free (via UAF write) or use a different size. House of Botcake technique uses tcache filling + unsorted bin consolidation to bypass the key check.
   - **glibc 2.32-2.34**: safe-linking introduced — tcache and fastbin fd pointers are XOR'd with `(chunk_address >> 12)`. Direct fd overwrite no longer works; the attacker must compute the encoded value. The decode formula: `real_ptr = encoded_fd ^ (chunk_address >> 12)`. The heap base must be known (leaked) to encode correct target pointers. `__malloc_hook` and `__free_hook` removed in 2.34 — exploitation must target exit hooks, FSOP, GOT overwrite, or `_IO_list_all`.
   - **glibc 2.35+**: tcache count field encrypted with a random cookie (`protect_ptr` macro generalized). Counts are XOR'd with a per-thread random value stored in `tcache_perthread_struct`. Corrupting the count (to drain tcache and force unsorted bin fallback) requires knowing the cookie.
4. Validate the libc version by leaking a known function address. Even without an exploitation leak, extract a function offset from a provided libc: use `objdump -T` through `pentest_agent_execute_tool` to get the offset of a common function like `puts` or `printf`. Then use `libc-database` by searching with the last 12 bits (3 hex digits) of the function offset. Many libc builds have unique low-12-bit signatures that identify the exact build. This confirms the version before exploitation begins.
5. Identify the allocator build configuration. Some libc builds enable `tcache` with different bin counts or different integrity checks. Recent Ubuntu builds enable all checks; older Debian builds may lag. Check the libc's symbol table for configuration-specific symbols: `__libc_malloc`, `__libc_free`, `tcache_perthread_struct`. The presence and size of these symbols constrain what techniques work.

### Phase 2 — heap interaction primitives and vulnerability identification

Heap exploitation begins with a thorough inventory of the binary's heap operations. Reverse the binary to identify what allocation, deallocation, read, and write primitives are available to the attacker. Each primitive maps to a class of exploitation techniques.

1. Identify the allocation primitive (`alloc`): what sizes can the attacker request? Are there minimum or maximum size constraints? Does the binary allocate fixed-size chunks (only one size) or variable-size chunks (within a range)? A binary with only one allocation size limits which bins can be used (all chunks go to the same tcache bin, preventing cross-bin attacks). A binary with variable sizes allows the attacker to place chunks in different tcache bins, fastbins, or the unsorted bin by choosing the allocation size strategically.
2. Identify the deallocation primitive (`free`): can the attacker free an arbitrary index? Is there a limit on the number of frees or a specific order enforced? After freeing, is the pointer set to NULL (preventing UAF) or left dangling (enabling UAF)? Is there a free-list pointer corruption check? Can the same chunk be freed twice (double-free)?
3. Identify the write primitive: does the binary write attacker-controlled data to an allocated chunk after allocation? Is there a write-after-free (writing to a freed chunk, corrupting allocator metadata)? Is there a heap overflow (writing past the allocated chunk boundary into the next chunk's metadata or user data)? How many bytes overflow? Is the overflow controlled (attacker-chosen bytes) or uncontrolled (null byte, or a fixed byte)?
4. Identify the read primitive: does the binary print heap data? Is there a read-after-free (reading freed chunk data, leaking fd/bk pointers)? Is there a heap info leak (uninitialized chunk data printed after allocation)? Is the read constrained by a null terminator (stopping at the first 0x00 byte, which may hide part of a pointer)?
5. Identify the off-by-one condition specifically: a one-byte overflow past the chunk boundary. If the overflow byte is a null byte (`0x00`), it can clear the `PREV_INUSE` bit of the next chunk's size field, enabling backward consolidation tricks (House of Einherjar and poisoned null byte). If the overflow byte is controllable, it can overwrite the least significant byte of the next chunk's size, modifying the chunk size to create overlapping chunks.
6. Classify the vulnerability combination. Common heap vulnerability archetypes and their corresponding exploitation paths:
   - **UAF (Use-After-Free)**: pointer still usable after free. Simplest path: tcache poisoning (modify fd of freed chunk in tcache to arbitrary address).
   - **Double-free**: free the same chunk twice (directly or with an intervening free of another chunk). With tcache key bypass: double-free two different chunks into the same tcache bin, then alloc to overwrite fd.
   - **Heap overflow**: write past chunk boundary. Overwrite the next chunk's metadata (size, fd, bk) or user data. If the next chunk is free, corrupt its fd to redirect allocation.
   - **Off-by-one null byte**: poison the `PREV_INUSE` bit or the least significant byte of the next chunk's size. Enables chunk-overlapping primitives.
   - **Info leak**: printed heap data reveals libc or heap pointers. Essential prerequisite for ASLR bypass with PIE or safe-linking.
7. Document the exact primitive in the evidence log: the operation (alloc/free/edit/read), the index or argument, the observed size constraints, and the behavior (pointer zeroed or not, key field present or absent, tcache used or skipped). This primitive matrix is the blueprint for all subsequent exploitation phases.

### Phase 3 — heap leak: unsorted bin libc address disclosure

The unsorted bin is a doubly-linked circular list. When a chunk larger than the tcache range (above 0x410 on x86-64 for default tcache, or above 0x80 if tcache is full/absent) is freed and consolidated into the unsorted bin as the sole chunk, its `fd` and `bk` pointers both point to `&main_arena.top` inside libc (specifically within the `main_arena` structure). Reading the freed chunk's `fd` pointer reveals a libc address.

1. Allocate a chunk large enough to bypass tcache and fastbin entirely. For default glibc with tcache enabled on x86-64, any chunk size larger than 0x410 (the largest tcache bin, 0x410, holds sizes up to 0x408 user data plus 0x10 chunk header minus 0x8 for the prev_size field reuse) goes directly to the unsorted bin upon freeing. A size of 0x420 or larger is safe. This chunk is the "leak chunk."
2. Allocate a second, smaller "guard" chunk immediately after the leak chunk. The guard chunk prevents the freed leak chunk from consolidating with the top chunk (the wilderness). When a chunk adjacent to the top chunk is freed, the allocator merges it into the top chunk instead of placing it in a bin — the guard chunk prevents this. The guard can be any size; a small allocation (0x20) is sufficient.
3. Free the leak chunk. It enters the unsorted bin. Its `fd` and `bk` now contain a pointer to `main_arena` at a known offset from libc base. The exact offset depends on the glibc version: common values are around `libc_base + 0x3ebca0` for glibc 2.31 or `libc_base + 0x3ebc80` for glibc 2.27. Record the libc's `main_arena` offset from the symbol table for later calculation.
4. Read the freed leak chunk's `fd` through the available read primitive (UAF read, heap print, or format string). The leaked value is a raw 6-byte pointer (high 2 bytes are zero on x86-64 due to canonical addresses). Decode it to an integer: `leaked_main_arena = u64(leaked_bytes.ljust(8, b'\x00'))`.
5. Compute libc base: `libc_base = leaked_main_arena - main_arena_offset`. The `main_arena_offset` is the offset of `main_arena` within the libc file — obtain it from the libc symbol table via `objdump -T` through `pentest_agent_execute_tool`, searching for the `main_arena` symbol or computing from the `__malloc_hook` offset (typically `main_arena = __malloc_hook + 0x10`).
6. If the allocator has a different behavior (different glibc version, or an allocator wrapper like jemalloc or tcmalloc), verify the leak by checking that the leaked address falls within the expected libc memory range (typically `0x7f...` on x86-64). If the address is unexpected, recheck the libc version and the main_arena offset.

### Phase 4 — heap leak: heap base address via tcache safe-linking decode

For glibc 2.32+ with safe-linking, the first freed chunk in a previously empty tcache bin encodes its `fd` pointer. Since the bin was empty, the `next` pointer is NULL, and the encoded value is simply `chunk_address >> 12`. This directly reveals the heap base when decoded.

1. Allocate a chunk of a size within the tcache range (0x20 to 0x410). The exact size should match one that can be read later via the available leak primitive.
2. Free the chunk into an empty tcache bin. The chunk's `fd` (at offset 0 from the user data) is now set to: `encoded_fd = (chunk_address >> 12) ^ NULL`. Since XOR with NULL is identity, `encoded_fd == chunk_address >> 12`.
3. Read the encoded `fd` via the heap read primitive. The value is a raw integer where the bottom 12 bits are zero-shifted. Compute the heap base: `heap_base = (encoded_fd << 12) - chunk_offset_from_heap_base`. The `chunk_offset_from_heap_base` is the offset of the freed chunk from the heap start — the first allocated chunk is typically at `heap_base + 0x2a0` or similar, depending on prior allocations and the size of `tcache_perthread_struct` (which is 0x290 bytes on glibc 2.31+).
4. For pre-glibc 2.32 (no safe-linking), the `fd` is the raw pointer to the next free chunk, or NULL if the bin was empty and the chunk is the only entry. The heap base is obtained by observing the chunk's own address (if an address leak exists) or by analyzing the `tcache_perthread_struct` layout.
5. The `tcache_perthread_struct` is the first allocated chunk at the heap base (chunk at `heap_base + 0x0`, user data at `heap_base + 0x10`). It contains an array of 64 `uint16_t` counts (one per tcache bin) followed by 64 pointers (the head of each bin). Leaking this structure reveals the tcache bin state. If an arbitrary read primitive exists, reading from `heap_base + 0x10` yields the tcache counts; reading from `heap_base + 0x90` yields the bin head pointers.
6. Once both `libc_base` and `heap_base` are known, record them in evidence. These two values are the foundation for all subsequent exploitation phases. Most heap attacks require: libc base (for hook addresses, gadget addresses, `system`, `/bin/sh` string) and heap base (for safe-linking encoding, fake chunk placement, and `tcache_perthread_struct` manipulation).

### Phase 5 — tcache poisoning (arbitrary allocation)

Tcache poisoning forces `malloc()` to return an arbitrary address by corrupting the `fd` pointer of a freed chunk still in the tcache. The allocator follows the corrupted `fd` on the next allocation, returning the attacker-chosen address.

1. Free a chunk of a target size into the tcache. The chunk is now at the head of the bin's singly-linked free list.
2. Overwrite the freed chunk's `fd` pointer with the target address. For glibc < 2.32 (no safe-linking): write the raw target address directly. For glibc >= 2.32 (safe-linking): compute the encoded address — `encoded_target = (chunk_user_data_address >> 12) ^ target_address` — and write the encoded value. Use the known heap base to compute `chunk_user_data_address`.
3. Allocate two chunks of the same size. The first allocation (`malloc(size)`) returns the original freed chunk (the head of the list). The second allocation returns the target address. The attacker now controls memory at the target location.
4. Common target addresses for arbitrary allocation and their exploitation value:
   - `__free_hook` (glibc < 2.34): overwrite with `system` address. Next `free()` call with a chunk containing `/bin/sh` executes `system("/bin/sh")`. This is the most reliable target because the argument to `free()` is directly controlled (the pointer being freed).
   - `__malloc_hook` (glibc < 2.34): overwrite with a `one_gadget` address. Next `malloc()` call triggers the gadget. Less reliable because `one_gadget` constraints vary by libc build.
   - GOT entry: if Partial RELRO, overwrite `printf@GOT` or `exit@GOT` with `system`. On the next call to the overwritten function, execution redirects. The argument to the original function becomes the argument to `system`.
   - `_IO_list_all` pointer: for FSOP (Phase 9). Redirect the `_IO_FILE` linked list to a fake FILE structure on the heap.
   - `exit_funcs` / `tls_dtor_list`: thread-local destructor chain for glibc 2.34+ exploitation when hooks are removed.
   - `tcache_perthread_struct` itself: corrupt the tcache bin counts or head pointers to control future allocations at arbitrary sizes. Useful for crafting overlapping chunk scenarios.
5. If the target address contains a value that conflicts with the memory layout (e.g., a size field that must pass a validation check), use a "misaligned" target. For example, targeting `__malloc_hook - 0x23` places a fake chunk header with a valid size field before the hook, bypassing the chunk-size check in tcache. This technique requires a known 8-byte value at the target location that, when misaligned, reads as a valid size for the requested tcache bin.

### Phase 6 — fastbin attacks (glibc < 2.29, or with safe-linking bypass on later versions)

Fastbins are singly-linked free lists for chunks of size 0x20 to 0x80 (inclusive on x86-64). Fastbin dup exploits a double-free to create a circular list, then allocates from the circle to allocate the same chunk twice, enabling fd corruption.

1. Fastbin dup (double-free without an intervening free): free chunk A, free chunk B, free chunk A again. The fastbin now contains: A → B → A (circular). The double-free works because fastbin only checks whether the most recently freed chunk matches the chunk being freed (a check added in glibc 2.29). Freeing B between the two frees of A bypasses the "top of bin" check — B is at the top when the second free of A is requested.
2. Allocate from the fastbin three times. The first returns A, the second returns B, and the third returns A again — the same chunk is allocated twice (overlapping allocations, also called a "double-alloc"). Between the first and second allocation, the attacker writes the target address into A's `fd` field (which is at the user data start). After the third allocation, the fastbin head points to the target address.
3. Allocate a fourth time — this returns the target address. Use the same target selection as tcache poisoning (Phase 5), but with an additional constraint: the target address must point to memory where the 8 bytes at `target - 0x8` form a valid fastbin size (a value matching the requested bin's size range). The classic target for 0x70 fastbin is `__malloc_hook - 0x23` on x86-64, where the 8 bytes before `__malloc_hook` contain `0x7f` (a valid 0x70 fastbin size after misalignment).
4. For glibc 2.32+ with safe-linking applied to fastbins: the same encoding applies — `fd = (chunk_address >> 12) ^ next_ptr`. The attack proceeds identically, but the target address must be encoded before writing to the fd field. This requires knowing the heap base (to compute the chunk address for the XOR key).
5. Fastbin consolidation attack: when a large chunk (≥ 0x80, above fastbin range) is freed adjacent to a fastbin chunk, the allocator consolidates them if the fastbin chunk's `PREV_INUSE` bit is cleared. By corrupting a fastbin-allocated chunk's size to clear `PREV_INUSE` and set a large `prev_size`, the attacker triggers a backward consolidation that creates an overlapping chunk spanning both the fastbin chunk and the legitimately allocated large chunk. The overlapping chunk can be allocated, giving the attacker read/write access to the still-in-use fastbin chunk.

### Phase 7 — off-by-one null byte: poisoned null byte / House of Einherjar

A one-byte null overflow past the user data of a chunk into the next chunk's `size` field can clear the `PREV_INUSE` bit (bit 0). When the corrupted chunk is later freed, the allocator believes the previous chunk (indicated by the `prev_size` field) is free and consolidates backward.

1. Arrange three consecutive chunks on the heap: chunk P (the "previous" chunk the attacker fully controls), chunk A (the target whose size field is corrupted), and chunk B (a guard or subsequent chunk). The attacker overflows from P into A's size, clearing `PREV_INUSE` and optionally modifying A's `prev_size` to point backward past P to a fake chunk.
2. The fake chunk (let's call it chunk F) is constructed inside P's user data. It has: a crafted `prev_size` (used during backward consolidation to find the chunk to unlink), a crafted `size` field matching a valid bin size, and crafted `fd` and `bk` pointers that satisfy the unlink integrity check (`fd->bk == F` and `bk->fd == F`). If the unlink check passes (requires knowing a pointer to F elsewhere in memory, such as the heap itself), the allocator removes chunk F from its free list and merges it with chunk A.
3. After consolidation, the resulting merged chunk spans from F's header through the end of A. This merged chunk overlaps with P's user data (which is still in use by the binary). The attacker can now read/write into the merged chunk region through the legitimate allocation of P. Free A (now inside the merged chunk) and allocate again — the new allocation covers both F and A, allowing the attacker to overwrite A's user data through the new allocation.
4. House of Einherjar variant: instead of a null byte, the overflow is a controlled byte that modifies the least significant byte of A's size. By changing A's size to a larger value (e.g., from `0x101` to `0x181` by writing `\x81`), the allocator treats A as a larger chunk. When A is freed, it goes to a different bin, and the freed region includes memory that overlaps with the next chunk (B). Allocating a chunk of the new larger size returns memory overlapping B — a classic overlapping chunk primitive.
5. Constraints for the poisoned null byte technique: the `prev_size` of chunk A must align with the distance from A back to the fake chunk F. On glibc 2.29+, the allocator verifies that `prev_size` matches the expected distance when consolidating — the `prev_size` field of A and the `size` field at `F + prev_size` must be consistent. The fake chunk at position `A - prev_size` must have a valid `size` field. Typically, the attacker arranges two fake chunk headers before A's location, with matching `prev_size` chains, to pass all validation.

### Phase 8 — House of Botcake (tcache + unsorted bin overlap, glibc 2.29+)

House of Botcake creates overlapping chunks by exploiting the interaction between the tcache (with its key-based double-free detection) and the unsorted bin (which does not check the tcache key). The technique targets glibc 2.29 to 2.33 where tcache key exists but safe-linking may or may not be present.

1. Allocate a set of chunks of the same size larger than the tcache range (e.g., 0x100 or larger). Designate: chunk X (the primary), chunk Y (adjacent to X), and a guard chunk after Y (to prevent top chunk consolidation). Also allocate 7 "filler" chunks of the same size — these will fill the tcache for this size (7 is the maximum entries per tcache bin).
2. Free all 7 filler chunks. The tcache bin for this size is now full (count = 7). Any subsequent free of a chunk of this size goes to the regular bins (fastbin or unsorted bin), not tcache.
3. Free chunk X. Since tcache is full, X goes to the unsorted bin (its size is above fastbin range). X's `fd` and `bk` now point to `main_arena` (for libc leak, but that's incidental here).
4. Free chunk Y. Y also goes to the unsorted bin. Y is adjacent to X. The allocator consolidates X and Y into a single larger chunk in the unsorted bin. The consolidated chunk spans the memory of both X and Y.
5. Allocate one chunk from the tcache (e.g., `malloc(size)`). The tcache count decreases from 7 to 6 — one slot is now available. The newly allocated chunk comes from the tcache, not from the unsorted bin.
6. Free chunk Y again. Since tcache has a free slot, Y goes to the tcache (not the unsorted bin). However, Y's memory still lies within the consolidated unsorted bin chunk from step 4. The allocator does not check whether a chunk is already in the unsorted bin before placing it in tcache — this is the core overlap. Y is now simultaneously in the tcache free list and inside the consolidated unsorted bin chunk.
7. Allocate a large chunk of size equal to the consolidated chunk (X_size + Y_size + overhead). This allocation comes from the unsorted bin, carving out the entire consolidated region. The attacker now controls memory that includes Y's tcache metadata (its `fd` pointer).
8. Overwrite Y's `fd` (which is now at a known offset within the large allocated chunk) with an encoded target address. Then allocate from the tcache twice: the first returns Y, the second returns the target address. Arbitrary allocation achieved.

### Phase 9 — FSOP (File Stream Oriented Programming) / House of Apple 2

On glibc 2.34+, `__malloc_hook` and `__free_hook` are removed. The most reliable alternative for control-flow hijack is FSOP: corrupting `_IO_FILE` structures to redirect the `_IO_flush_all_lockp` cleanup routine, which is called on `exit()` or `return` from `main`.

1. Understand the `_IO_FILE` linked list. The `_IO_list_all` global pointer points to a linked list of `_IO_FILE_plus` structures. Each structure contains a `_IO_FILE` (the actual file object) followed by a `vtable` pointer. When the program exits, `_IO_flush_all_lockp` traverses this list and calls each file's vtable `__overflow` function.
2. The vtable check (introduced in glibc 2.24) validates that the vtable pointer falls within the legitimate `__libc_IO_vtables` section. Bypass: use a "legitimate" vtable from a different `_IO_FILE` type. The `_IO_wfile_jumps` vtable (for wide-character files) is within the legitimate range and calls through a `_wide_data` pointer in the `_IO_FILE` structure, which can be attacker-controlled.
3. House of Apple 2 sequence:
   - Leak both libc base and heap base (required).
   - Forge a fake `_IO_FILE_plus` structure on the heap at a known address. The structure includes: `_flags` (set to bypass initial checks), `_IO_write_ptr` > `_IO_write_base` (triggers flush), `_IO_buf_base` set to a controlled buffer, `vtable` set to the address of `_IO_wfile_jumps` in libc (legitimate), and `_wide_data` set to a second controlled area on the heap.
   - In the `_wide_data` structure, set `_IO_write_ptr` to a controlled area where the first 8 bytes are the address of `system`. The call chain: `_IO_flush_all_lockp` → `_IO_OVERFLOW(fp)` → vtable `__overflow` → `_IO_wfile_overflow` → wide-character code path → calls through `_wide_data->_IO_write_ptr` → `system`.
   - Overwrite `_IO_list_all` with the address of the fake `_IO_FILE_plus` structure (or inject the fake file into the existing linked list via a corrupted `_chain` pointer in a legitimate FILE object like `_IO_2_1_stderr_`).
4. Trigger the FSOP by causing the program to exit (or by calling `exit()` through a GOT overwrite). The corrupted `_IO_list_all` chain causes `system("/bin/sh")` to be called during the cleanup sequence.
5. Alternative FSOP targets: the `_IO_2_1_stdout_` buffer can be corrupted to leak memory (by modifying `_IO_write_base` to overlap with libc data), or `_IO_2_1_stdin_` can be corrupted to control what `scanf`/`gets` reads. These are information-disclosure primitives that feed into the main FSOP chain.

### Phase 10 — seccomp bypass via alternative syscalls

When the binary applies a seccomp filter (via `prctl` with `PR_SET_SECCOMP` or `seccomp-bpf`) that blocks `execve` (syscall 59), obtaining a shell requires bypassing the filter through alternative syscalls.

1. Dump the seccomp filter using `seccomp-tools` via `pentest_agent_execute_tool`. The `seccomp-tools` tool profiles the binary at runtime and displays which syscalls are blocked and which are allowed. Alternatively, use `pwntools` to connect to the remote service and extract the filter by analyzing the binary's seccomp initialization code — some challenges embed the BPF filter as a byte array in the binary.
2. Analyze the filter: identify which syscalls are blocked. Common blocks: `execve` (59), `fork` (57), `clone` (56) — these prevent process creation and program execution. Often, `open` (2) and `read` (0) are allowed (the binary needs to read files), and `write` (1) is allowed (the binary prints output).
3. Bypass strategies based on what is allowed:
   - **openat2 + read + write (ORW chain)**: if `openat2` (syscall 437), `read` (0), and `write` (1) are allowed, build a ROP chain that: calls `openat2(AT_FDCWD, "flag.txt", how_struct, sizeof(how_struct))` to open the flag file, calls `read(fd, heap_buffer, 100)` to read the flag content into a controlled heap buffer, then calls `write(1, heap_buffer, 100)` to print the flag to stdout. `openat2` (Linux 5.6+) is often not blocked because seccomp filters are authored to block only `open` and `openat` — `openat2` is newer and frequently overlooked.
   - **execveat (syscall 322)**: if `execveat` is allowed, use it to execute a program referenced by a file descriptor. First, use `openat2` (or `open` if allowed) to open `/bin/sh` or `/bin/cat` into a readable fd. Then call `execveat(fd, "", ["/bin/sh", NULL], NULL, AT_EMPTY_PATH)` — this executes the file referenced by the fd. Often unblocked because it's obscure.
   - **sendfile (syscall 40)**: copies data from one fd to another entirely in kernel space, without a userspace buffer. If `sendfile` is allowed and the flag is in a file the binary already has open, call `sendfile(1, flag_fd, NULL, flag_size)` to write the flag directly to stdout. This requires knowing the flag file's fd — sometimes the challenge intentionally opens the flag file early, leaving it at a predictable fd (like fd 3).
   - **socket + connect + dup2 + execveat (reverse shell)**: if `socket` (41), `connect` (42), `dup2` (33), and `execveat` are allowed, build a reverse shell: create a socket, connect to the attacker's IP/host on a controlled port, dup2 the socket fd to stdin/stdout/stderr (fds 0/1/2), then execveat a shell binary. This provides an interactive shell over the network.
4. Build the syscall chain as shellcode (using `pwntools` `asm()` through `pentest_agent_execute_tool`) or as a ROP chain. For ROP: use `syscall; ret` gadgets in libc (the `syscall` instruction followed by `ret`). Set up registers according to the x86-64 syscall convention: RAX = syscall number, RDI = arg1, RSI = arg2, RDX = arg3, R10 = arg4, R8 = arg5, R9 = arg6. Find `pop rax; ret`, `pop rdi; ret`, `pop rsi; ret`, `pop rdx; ret`, and `syscall; ret` gadgets in libc (after leaking libc base). Chain them in order to construct each syscall invocation.
5. If the binary has both seccomp and a stack-based vulnerability, build the ORW or sendfile ROP chain directly as the final payload. If the binary has a heap-based vulnerability, use the heap exploitation primitives from earlier phases to gain arbitrary write, then overwrite a function pointer (GOT, exit hook) with the address of a ROP chain or a stack-pivot gadget that transfers execution to the ROP chain.

## Decision points

- **Stop on libc version mismatch**: if the remote libc cannot be identified and the challenge provides no libc file, halt after the leak phase. Exploitation without knowing offsets is blind guessing.
- **Stop on all hooks removed + no FSOP path**: glibc 2.34+ without a `_IO_list_all` writable primitive requires alternative targets (tls_dtor_list, atexit handler chain). If none are reachable, escalate to broader CTF workflow review.
- **Escalate to `ctf-pwn-rop`**: if the exploitation path requires a complex multi-gadget chain (ORW, reverse shell) rather than a single hook overwrite. Hand off with libc base, heap base, and gadget search results.
- **Prefer tcache poisoning over fastbin**: tcache is simpler, has fewer checks (no size validation on allocation in glibc 2.27-2.28), and typically requires only two allocations to reach the target. Use fastbin only when tcache is full or the vulnerability forces it.
- **Prefer `__free_hook` over `__malloc_hook`**: `free(chunk)` passes the chunk pointer as the first argument to the hook, enabling direct argument control. `malloc(size)` passes only the size, requiring a one_gadget or pre-arranged state.
- **Downgrade to guess-and-test**: if the heap layout is insufficiently controlled (concurrent threads, random allocations), the exploit may only work probabilistically. Compute the expected success rate and decide whether to run repeatedly or to refine grooming.
- **Abandon on fully hardened heap**: if the glibc version has all integrity checks (key, safe-linking, size validation, pointer mangling), the binary has no UAF or overflow, and no info leak exists, heap exploitation may be infeasible.

## Prohibited behavior

- Exploiting heap vulnerabilities in production binaries, third-party software, or any system outside the authorized CTF competition scope.
- Using heap grooming techniques against multi-tenant services or shared infrastructure where other users' data may be corrupted.
- Corrupting heap state in a way that persists after the exploit session — always let the process crash or exit cleanly after flag capture.
- Deploying heap exploits against competition infrastructure at rates that degrade service availability or consume excessive memory.
- Using `sudo` or elevated privileges to modify the challenge binary, libc, or loader for local testing.
- Storing raw exploit scripts with hardcoded offsets, leaked addresses, or shellcode in publicly accessible repositories during an active competition.
- Handling unredacted flags, challenge solutions, or exploit payloads outside the evidence system.

## Stop conditions

- Flag recovered and validated against the competition platform. Stop all heap exploitation on this challenge.
- Heap vulnerability is proven unexploitable under the current glibc version's integrity checks with no bypass available.
- Remote service enters an inconsistent state (heap corruption from a prior attempt leaves the process unable to handle further requests). Document the failure and the likely cause.
- Competition time window expires. Preserve partial evidence and hand off to report.
- Exploit requires heap manipulation that would affect memory belonging to other teams or shared competition infrastructure.
- Binary or libc is determined to be outside the authorized lab/CTF scope.

## Evidence

Record each phase with `pentest_agent_append_evidence`:

```text
Challenge: <competition-name>/<challenge-name>
Binary hash (SHA-256): <64-char hex digest>
Libc hash (SHA-256): <64-char hex digest>
Timestamp: <ISO 8601>

Phase 1 — Libc fingerprint:
  Libc version string: <GNU C Library ...>
  Allocator: <ptmalloc with tcache | ptmalloc without tcache>
  Key integrity features: <tcache key | safe-linking | count encryption | none>
  __malloc_hook present: <yes | no>
  __free_hook present: <yes | no>

Phase 2 — Primitive inventory:
  Alloc sizes: <fixed N | range A-B | unlimited>
  Free behavior: <dangling pointer | NULL'd | ordered-only>
  Write primitive: <UAF write | heap overflow +N bytes | off-by-one (null) | off-by-one (controlled)>
  Read primitive: <UAF read | uninitialized leak | format string>
  Vulnerability archetype: <UAF | double-free | overflow | off-by-one | leak-only>

Phase 3 — Libc leak:
  Method: <unsorted bin fd | largebin bk | tcache_perthread_struct read>
  Leaked main_arena: <0x...>
  Libc base: <0x...>

Phase 4 — Heap base:
  Method: <safe-linking decode | tcache_perthread struct read | heap address leak>
  Heap base: <0x...>

Phase 5-9 — Exploitation:
  Technique: <tcache poisoning | fastbin dup | House of Botcake | House of Einherjar | FSOP | other>
  Target overwritten: <__free_hook | __malloc_hook | GOT | _IO_list_all | tcache_perthread_struct>
  Payload target address: <0x... (hashed if sensitive)>
  Shell/flag obtained: <yes | no>

Phase 10 — Seccomp bypass:
  Blocked syscalls: <list>
  Bypass method: <openat2+read+write | execveat | sendfile | reverse shell>
  Chain type: <shellcode | ROP>

Decision: <stop — flag captured | escalate to ctf-pwn-rop | abandon>
```

Never store: raw exploit payloads with hardcoded addresses, shellcode, libc base addresses for non-CTF infrastructure, flag values in plaintext (use SHA-256 hash), heap grooming scripts with environment-specific offsets, or any data from non-authorized targets.

## Report handoff

1. Use `pentest_agent_record_finding` for each successful exploit. Finding types: `ctf-pwn-heap-tcache-poisoning`, `ctf-pwn-heap-fastbin-dup`, `ctf-pwn-heap-house-of-botcake`, `ctf-pwn-heap-house-of-einherjar`, `ctf-pwn-heap-fsop`, `ctf-pwn-heap-seccomp-bypass`, `ctf-pwn-heap-flag-capture`. Include: challenge identifier, glibc version, vulnerability type, exploitation technique, protection bypass achieved, and flag hash.
2. For challenge writeups: use the `report-ctf` skill. Provide the evidence log. Describe the heap vulnerability in conceptual terms: the primitive (UAF/overflow/double-free), the chosen exploitation technique, the libc version constraints, the leak methodology, and the final control-flow hijack path. Do not include raw shell commands or copy-paste exploit code.
3. For failed exploits: document the glibc version, the vulnerability type, all techniques attempted, the integrity check that blocked each technique, and any partial progress (leaks achieved but no control-flow hijack). Include libc fingerprint data for future database lookups.
4. Clean up: remove heap layout diagrams, exploit scripts, core dumps, GDB session logs, and tmp files. Preserve only the evidence log and finding records.
