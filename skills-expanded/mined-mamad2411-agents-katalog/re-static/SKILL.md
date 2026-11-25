---
name: re-static
description: Static reverse-engineering workflow for authorized local binaries — file-type identification, string extraction, entropy analysis, import/export triage, symbol recovery, disassembly (objdump/radare2), and decompilation (Ghidra headless). Offline-only by default; no execution, no debugger attachment, no network lookups unless scope explicitly permits.
disable-model-invocation: true
risk: passive
allowed-modes: [reverse-engineering, forensic, blue-team, ctf]
authorization-required: conditional
evidence-outputs: [analysis-notes, evidence-hash, redacted-evidence, finding-draft]
---

# Static reverse engineering — offline binary analysis

Use this skill to perform static analysis of authorized local binaries, libraries, firmware extracts, or CTF challenge binaries without executing them. Static analysis means inspecting the binary's structure, strings, symbols, imports, disassembly, and decompiled pseudo-code — never running, debugging, or tracing the binary. Keep network access disabled for all suspicious or untrusted samples. Mark all speculative conclusions (guesses about function purpose, algorithm, or data structure) separately from confirmed control-flow and data-flow evidence.

## Required inputs

- Artifact file path with confirmed ownership or explicit authorization for reverse engineering. This may be a binary from a CTF challenge, a vendor-supplied software component, a firmware-extracted executable, or a licensed application where reverse engineering is permitted by the license terms.
- SHA-256 hash of the artifact computed before analysis and recorded in evidence.
- Isolated analysis environment preferred (VM or container). When analyzing potentially malicious or untrusted samples, the environment must have network disabled and no access to host filesystems.
- Architecture context: if the binary's target architecture is known (from firmware analysis, CTF challenge description, or build-system metadata), record it before analysis. Otherwise, architecture detection is Phase 1.
- Valid authorization cache when the artifact is from a customer engagement.
- Explicit scope for any external lookups: symbol servers, public vulnerability databases, or string cross-referencing. These are read-only and safe, but confirm scope before contacting any external service.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` when artifact-handling boundaries exist (license restrictions, data classification, third-party component boundaries).
3. `pentest_agent_validate_target` for local file paths or target-like metadata before any tool invocation.
4. `pentest_agent_check_authorization` before analysis of engagement artifacts. CTF binaries in lab mode require lab proof only.
5. `pentest_agent_build_command` and `pentest_agent_execute_tool` only for approved read-only local tools — static analysis preferred.

## Workflow

### Phase 1 — file identification and triage

1. Hash the artifact: `sha256sum <artifact>`. Record the SHA-256 in all evidence output.
2. Work on a copy: `cp <artifact> /tmp/analysis_copy && sha256sum /tmp/analysis_copy`. Verify hash matches.
3. File type identification:
   - `file <artifact>` — returns file format, architecture, endianness, and linkage type.
   - Example output interpretation:
     - `ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, not stripped` → Linux 64-bit, dynamic linking, symbols preserved.
     - `ELF 32-bit MSB executable, MIPS, statically linked, stripped` → MIPS big-endian, no shared-lib dependencies, symbols removed — harder analysis.
     - `PE32 executable (console) Intel 80386, for MS Windows` → 32-bit Windows executable.
     - `Mach-O 64-bit executable arm64` → macOS ARM64 (Apple Silicon) binary.
4. Additional format-specific header inspection:
   - ELF: `readelf -h <artifact>` — detailed ELF header: entry point address, section header offset, program header count, flags.
   - PE: `objdump -x <artifact> | head -60` — PE optional header, sections, DLL imports.
   - Mach-O: `otool -h <artifact>` (macOS) or `rabin2 -I <artifact>` (radare2, cross-platform).
5. Basic properties:
   - `size <artifact>` — section sizes (text, data, bss).
   - `readelf -S <artifact>` (ELF) — all section headers with sizes, offsets, and flags.
   - Identify: `.text` (code), `.rodata` (read-only data, likely strings/constants), `.data` (initialized writable data), `.bss` (uninitialized data), `.plt` (procedure linkage table for dynamic linking).
6. Stripped vs. not stripped: `file <artifact> | grep "stripped"`. A stripped binary has had symbol names removed — function names from the original source are unavailable, complicating analysis. Note stripped status; it affects analysis strategy (more reliance on import table, string references, and manual function identification).

### Phase 2 — string extraction and pattern analysis

Extract all printable strings from the binary. Strings reveal function names, error messages, debug output, file paths, URLs, registry keys, and hardcoded credentials.

1. ASCII strings: `strings -a -n 6 <artifact> > strings.txt`
   - `-a`: scan the entire file (not just data sections).
   - `-n 6`: minimum string length of 6 characters — filters noise.
2. Unicode (wide-character) strings: `strings -e l -n 6 <artifact> > strings-unicode.txt`
   - `-e l`: 16-bit little-endian encoding (Windows wide strings).
3. Categorized filtering from `strings.txt`:
   - Credentials and secrets: `grep -iE "password|passwd|secret|key|token|api_key|auth|credential" strings.txt > strings-credentials.txt`
   - URLs and domains: `grep -E "https?://|ftp://|[a-zA-Z0-9.-]+\.(com|net|org|io|dev|local)" strings.txt > strings-urls.txt`
   - IP addresses: `grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}" strings.txt | sort -u > strings-ips.txt`
   - File paths: `grep -E "/(etc|usr|home|var|tmp|opt|Windows|Program Files)/" strings.txt > strings-paths.txt`
   - Registry keys (Windows malware): `grep -iE "HKEY_|HKLM|HKCU|Software\\\\Microsoft" strings.txt > strings-registry.txt`
   - Error and debug messages: `grep -iE "error|fail|debug|trace|warning|fatal|assert" strings.txt > strings-errors.txt`
   - Function names (if not stripped): `grep -E "^[a-zA-Z_][a-zA-Z0-9_]{4,}$" strings.txt | head -100 > strings-functions.txt`
4. Flag patterns (CTF): `grep -iE "flag\{|HTB\{|CTF\{|FLAG\{|[a-zA-Z0-9_]{20,}\}" strings.txt > strings-ctf.txt`
5. Cross-reference strings with function locations: if the binary is not stripped, strings near known function boundaries suggest purpose. For stripped binaries, strings are often the primary navigation aid.

### Phase 3 — import and export table analysis

Understand what external functionality the binary uses. Imports reveal the binary's capabilities: file operations, network communication, process manipulation, cryptographic operations, and anti-debug techniques.

1. ELF imports:
   - `readelf -d <artifact> | grep NEEDED` — lists required shared libraries (e.g., `libc.so.6`, `libssl.so.3`, `libpthread.so.0`).
   - `objdump -T <artifact> | grep -E "system|popen|execve|fork|socket|connect|send|recv|dlopen|ptrace|memfd_create|strcpy|gets|sprintf"` — flag dangerous function imports.
2. PE imports:
   - `objdump -x <artifact> | grep "DLL Name"` — imported DLLs.
   - `rabin2 -i <artifact>` — clean import table listing.
   - Flag dangerous imports: `VirtualAlloc`, `WriteProcessMemory`, `CreateRemoteThread`, `CreateProcess`, `WinExec`, `RegOpenKeyEx`, `RegSetValueEx`, `InternetOpenUrl`, `URLDownloadToFile`, `CryptEncrypt`, `IsDebuggerPresent`.
3. Exports (shared libraries):
   - `objdump -T <artifact> | grep "\.text"` — exported functions. This is what callers can use.
   - `nm -D <artifact>` — dynamic symbols.
4. Categorize imports by capability:
   - **File operations**: `open`, `read`, `write`, `fopen`, `CreateFile`, `ReadFile`, `WriteFile` — the binary reads/writes files. Assess: what files?
   - **Network**: `socket`, `connect`, `send`, `recv`, `bind`, `listen` — network capability. Assess: C2, data exfiltration, or benign network client?
   - **Process manipulation**: `fork`, `execve`, `system`, `CreateProcess`, `ShellExecute` — ability to start new processes. Assess: privilege escalation, lateral movement, or legitimate subprocess?
   - **Memory manipulation**: `mmap`, `mprotect`, `VirtualAlloc`, `VirtualProtect` — memory allocation and permission changes. Assess: shellcode injection, JIT compilation, or custom memory allocator?
   - **Cryptography**: `EVP_*`, `AES_*`, `SHA*`, `MD5`, `CryptEncrypt`, `CryptDecrypt`, `BCrypt*` — encryption capability. Assess: data protection, ransomware, or C2 encryption?
   - **Anti-debug**: `ptrace`, `IsDebuggerPresent`, `CheckRemoteDebuggerPresent`, `NtQueryInformationProcess` — debugger detection. Assess: malware anti-analysis, software protection, or legitimate debugging support?

### Phase 4 — entropy and packing analysis

Determine whether the binary is packed, encrypted, or compressed. Packed binaries hide their true code and require unpacking before meaningful static analysis.

1. Entropy calculation:
   - `ent <artifact>` — overall file entropy. Values near 8.0 (maximum) indicate strong encryption or compression.
   - `binwalk -E <artifact>` — entropy graph per offset. Flat high entropy = uniform encryption. Spikes = compressed blocks. Low entropy = uncompiled code/data.
2. Section-level entropy (PE):
   - Use `peframe` or manual Python: `python3 -c "import pefile; pe = pefile.PE('<artifact>'); [print(f'{s.Name.decode().strip()}: entropy={s.get_entropy():.2f}') for s in pe.sections]"`
   - Flag sections with entropy > 7.0 in `.text` (code section). Normally `.text` entropy is 6.0-6.5 for x86/x86-64. Values > 7.5 strongly suggest packing.
3. Packer signature detection:
   - `strings <artifact> | grep -iE "UPX|ASPack|Themida|VMProtect|MPRESS|Enigma|PECompact|Obsidium|Armadillo|NSPack|RLPack"`
   - `rabin2 -I <artifact>` (radare2) — includes packer detection.
   - `Detect It Easy` (DIE) — dedicated packer identifier with signatures.
4. If packed: the binary's visible strings and imports are from the packer stub, not the original program. The original code is compressed/encrypted and unpacked at runtime. Static analysis cannot proceed on the packed layer — unpacking is required. Delegate to `re-dynamic` for runtime unpacking via execution and memory dump, or use a packer-specific unpacker (UPX: `upx -d`, but only after confirming the packer is unmodified — modified packers may be boobytrapped).
5. If not packed: proceed to Phase 5 with confidence that the visible code, strings, and imports represent the true program.

### Phase 5 — disassembly and control-flow analysis

Disassemble the binary to recover assembly instructions and understand the control flow. Disassembly is a faithful translation of machine code to assembly mnemonics — it does not recover variable names, types, or high-level constructs (those come from decompilation in Phase 6).

1. Linear disassembly with objdump (fast, reliable, no analysis):
   - `objdump -d -M intel <artifact> > disasm-objdump.txt`
   - `-M intel`: Intel syntax (preferred over AT&T for readability). Use `-M att` for AT&T syntax.
   - This is a complete linear disassembly. It includes all code sections but does not differentiate code from embedded data.
2. Recursive disassembly with radare2 (analysis engine resolves function boundaries):
   - `r2 -A -q -c "pd $s @main" <artifact> > disasm-main.txt` — disassemble only the `main` function.
   - `r2 -A -q -c "afl; pdf @main; iz" <artifact> > r2-analysis.txt` — list all functions, disassemble main, list strings.
   - Key r2 commands (inside interactive `r2`):
     - `afl` — list all functions with address, size, and name.
     - `pdf @ <function>` — print disassembly of a function.
     - `s <address>` — seek to an address. `pdf` from there disassembles that function.
     - `iz` — list all strings in the binary with addresses.
     - `ii` — list all imports.
     - `is` — list all symbols.
     - `axt @ <address>` — find all cross-references (callers) to an address.
     - `axf @ <address>` — find all cross-references (callees) from an address.
     - `VV @ <function>` — visual graph mode (ASCII control-flow graph).
     - `afvn <old_name> <new_name>` — rename a function variable.
3. Function identification when stripped:
   - Look for the entry point: `readelf -h <artifact> | grep "Entry point"`. Disassemble from the entry point.
   - The entry point in a dynamically linked ELF is usually `__libc_start_main` or `_start`, which calls `main`. Trace the call instruction from `_start` → actual `main`.
   - Use `r2 -A` (auto-analysis) which heuristically identifies function boundaries by finding `call`/`ret` patterns and prologue/epilogue signatures (`push rbp; mov rbp, rsp` / `leave; ret` for x86-64).
4. Key instructions to search for:
   - `call <imported_function>` — calls to external functions reveal capability usage (e.g., `call system`, `call socket`).
   - `cmp` followed by conditional jump (`je`, `jne`, `jg`, `jl`) — comparison (password check, license verification, input validation). The comparison values may be hardcoded constants.
   - `xor` — common in cryptography (key mixing, stream ciphers) and also in simple obfuscation (string encoding).
   - `lea` with string references — loading an address of a string constant is often followed by a function call (e.g., `lea rdi, [rip+0x1234] ; call puts` → printing a string).
   - `syscall` (Linux) / `int 0x80` (Linux 32-bit) / `sysenter` (Windows) — direct system calls bypassing libc.

### Phase 6 — decompilation with Ghidra (headless)

Decompilation lifts assembly to pseudo-C, making the program logic readable. Use Ghidra headless mode for automation; the GUI mode is preferred for interactive exploration.

1. Headless import and auto-analysis:
   - `ghidraRun support/analyzeHeadless /tmp/ghidra-projects MyProject -import <artifact> -analysisTimeoutPerFile 300 -postScript <decompile_script> -log /tmp/ghidra.log`
   - The `-postScript` can be a custom Python/Jython script that exports decompiled functions. Example script: `DecompileFunctions.java` (export all functions to individual `.c` files) or use Ghidra's bundled `ExportProgram`.
2. Common Ghidra workflows (GUI, for deep analysis):
   - Import the binary (File → Import File). Select the correct format and language (auto-detected in most cases).
   - Auto-analyze (Analysis → Auto Analyze). Use default analyzers.
   - Open the Functions list (Window → Functions). Sort by name or size.
   - Locate `main` or `entry` function. Double-click to open the decompiler view.
   - Rename variables: right-click a variable → Rename Variable. This propagates to all references.
   - Retype variables: right-click → Retype Variable. Fix `undefined*` to `char*`, `int`, `long`, etc.
   - Find cross-references: right-click a function name → References → Show References to.
   - Patch bytes (for CTF patching): right-click an instruction → Patch Instruction.
3. Key decompilation patterns to recognize:
   - `strcmp(local_var, "constant_string")` — password or token comparison. The constant is the correct value.
   - `AES_*`, `EVP_EncryptInit`, `EVP_DecryptInit` — symmetric encryption. Find the key and IV nearby (passed as arguments or in global data).
   - `recv(socket, buffer, size, 0)` — network receive. The buffer contains network data.
   - `malloc(0x100)` — heap allocation. Watch for missing `free()` (memory leak) or use-after-free patterns.
   - Loop with `XOR` on a buffer and a hardcoded byte — simple string obfuscation. Recover the original by XORing with the same byte.
4. Decompilation limits:
   - Stripped binaries: function names are lost. The decompiler shows `FUN_00401234` instead of meaningful names.
   - Obfuscated code: control-flow flattening (one giant `switch` block with indirect jumps), opaque predicates (condition always true/false but the decompiler cannot prove it), and MBA (mixed boolean-arithmetic) expressions can confuse the decompiler. Flag these as anti-analysis findings.
   - Inline assembly: decompilers cannot lift inline assembly to C. The function will show raw assembly instructions in the decompiler output.

### Phase 7 — vulnerability discovery and exploit assessment

Only if analysis goals include vulnerability discovery or exploit development. CTF binary exploitation is expected; production binary vulnerability discovery requires explicit scope approval.

1. Check exploit mitigations: `checksec --file=<artifact>` (pwntools). Record:
   - RELRO (Full/Partial/None): GOT overwrite feasibility.
   - Stack Canary (Yes/No): stack buffer overflow detection.
   - NX (Enabled/Disabled): stack/heap executable.
   - PIE (Enabled/Disabled): address space layout randomization.
   - FORTIFY_SOURCE: compile-time bounds checking on certain libc functions.
   - RPATH/RUNPATH: if set, may allow library injection.
2. Dangerous function call-sites: `objdump -d <artifact> | grep -E "call.*<gets@plt>|call.*<strcpy@plt>|call.*<sprintf@plt>|call.*<system@plt>|call.*<popen@plt>"` — identify exact addresses of dangerous calls.
3. Buffer size analysis: for each dangerous call, backtrack to find the buffer size and the input source. If user input reaches a buffer of size N but the function writes more than N bytes, it's an overflow.
4. Format string vulnerabilities: `printf(user_input)` without a format specifier. Search for `call printf` preceded by `lea rdi, [user_buffer]` with no second argument (no format string in `rsi`).
5. Integer overflow: arithmetic on user-controlled integers that wraps around. Look for `add`, `sub`, `imul` on values from `atoi()`, `scanf()`, `strtoul()` without bounds checks.
6. Document: vulnerability type, affected function address, trigger condition, exploitation constraints (mitigations present), and proof-of-concept path (for CTF: the input that triggers the vulnerability).

## Decision points

- **Binary is packed**: stop static analysis at the packed layer. Hand off to `re-dynamic` for runtime unpacking or use a packer-specific extractor. Do not attempt to statically analyze packed code — you are looking at the packer stub, not the actual program.
- **Binary is stripped**: analysis takes longer. Prioritize import table analysis and string references as navigation aids. Consider dynamic analysis (`re-dynamic`) if the stripped binary is too complex for practical static reverse engineering.
- **Obfuscation detected (control-flow flattening, MBA, string encryption)**: deobfuscation is time-consuming. For CTF, allocate the time. For production analysis, flag the obfuscation as an anti-analysis finding and consider whether dynamic analysis is permitted.
- **Hardcoded credentials found**: flag as a credential-exposure vulnerability. Do NOT test the credentials against live systems without separate active-testing authorization.
- **Exploit development for CTF**: within scope. Proceed to `re-dynamic` for debugging the exploit. For production binaries: exploit development requires explicit scope permission. Document the vulnerability and stop at proof-of-concept.
- **Third-party library detected**: if the binary statically links a known library (e.g., OpenSSL, zlib, libpng), focus analysis on the application code, not the library. Flag the library version for CVE cross-referencing.

## Prohibited behavior

- Executing or debugging the binary — static analysis only. Dynamic analysis and debugging are in `re-dynamic`.
- Connecting to any network for symbol lookup, string cross-referencing, or CVE search unless scope explicitly permits read-only external lookups.
- Developing and testing exploits against production binaries outside the authorized scope.
- Extracting and reusing hardcoded credentials, keys, or certificates for any purpose beyond analysis documentation.
- Sharing the binary or analysis artifacts outside the engagement scope — the binary is the property of the engagement owner.

## Stop conditions

- Binary is packed and no unpacker is available or permitted → stop, document the packer, and recommend dynamic unpacking.
- Analysis reveals third-party proprietary code or licensed components beyond the engagement scope → stop, document the scope boundary, do not continue reverse engineering the third-party component.
- Binary triggers anti-tamper detection through static inspection of its own integrity (e.g., self-hashing checks in encrypted sections) → this is a static-detected anti-tamper mechanism. Document it and decide: continue with dynamic analysis or stop here.
- Analysis uncovers evidence of illegal content or activity → stop immediately, document the finding, and escalate to the engagement lead or legal authority per organizational policy.

## Depth rules

- Confirm artifact ownership or authorization before any analysis.
- Prefer offline/static review. Never execute, debug, or trace the artifact in this skill — those are `re-dynamic` territory.
- Hash the artifact before analysis. Work on copies. Record SHA-256 in all evidence.
- Record tool names and versions, key addresses (entry point, main, notable functions), offsets, string references, and import categories.
- Mark guesses and speculative conclusions (e.g., "this function appears to be a decryption routine based on the XOR loop and hardcoded key reference") separately from confirmed facts (e.g., "the binary imports AES_set_decrypt_key and calls it with a 16-byte buffer at address 0x402000").
- Redact hardcoded secrets, tokens, keys, certificates, and customer data before evidence or report use.

## Evidence

For each static analysis session, produce an analysis record:

```text
Artifact: challenge_binary (SHA-256: abcdef123456...)
File type: ELF 64-bit LSB executable, x86-64, dynamically linked, not stripped
Entry point: 0x401050
Mitigations: Partial RELRO, Stack Canary, NX enabled, No PIE

Phase 1 — Triage:
  Architecture: x86-64, little-endian, System V ABI.
  Sections: .text (0x1050-0x1a20, 2.5KB), .rodata (0x2000-0x2100), .data, .bss.
  Stripped: No — symbols preserved.

Phase 2 — Strings:
  "Correct password!" at 0x2008
  "Access granted. Flag: %s\n" at 0x2020
  "/bin/sh" at 0x2038
  "admin" at 0x2040
  → Password-check routine identified. Shell string suggests privilege escalation.

Phase 3 — Imports:
  libc.so.6: printf, scanf, strcmp, puts, system, setuid, setgid
  → strcmp: password comparison. system: command execution. setuid/setgid: privilege change.

Phase 4 — Entropy:
  .text: 6.18 (normal), .rodata: 5.02 (normal). Not packed.

Phase 5 — Disassembly:
  main (0x401172):
    0x401180: lea rdi, [rip+0xe99]  # "Enter password: "
    0x401187: call puts
    0x401192: lea rsi, [rbp-0x20]  # user_input buffer (32 bytes)
    0x401196: lea rdi, [rip+0xe8a]  # "%31s"
    0x40119d: call scanf
    0x4011a4: lea rdi, [rbp-0x20]  # user_input
    0x4011a8: lea rsi, [rip+0xe92]  # "admin" (hardcoded password at 0x2040)
    0x4011af: call strcmp
    0x4011b4: test eax, eax
    0x4011b6: jne 0x4011d0           # jump if password wrong
    → Password: "admin". Bypass: provide "admin" to scanf.

Phase 6 — Ghidra decompilation (excerpt):
  int main(void) {
    char input[32];
    puts("Enter password: ");
    scanf("%31s", input);
    if (strcmp(input, "admin") == 0) {
      setuid(0); setgid(0);
      system("/bin/sh");
      return 0;
    }
    puts("Wrong password.");
    return 1;
  }
  → Hardcoded password "admin" → root shell. Critical finding.

Findings:
  [CRITICAL] Hardcoded password "admin" in setuid binary → trivial privilege escalation to root.
  [INFO] Partial RELRO + no PIE — GOT overwrite and fixed base address for exploitation.
  [INFO] /bin/sh hardcoded — the binary is a deliberate backdoor.
```

Aggregate findings per artifact: function inventory with purpose annotations, vulnerability list with affected addresses and trigger conditions, hardcoded secrets inventory (redacted in default evidence), and exploitation complexity assessment (mitigations present, required primitives).

Never store: the artifact itself in evidence (store only SHA-256), unredacted credentials or keys from production artifacts, or decompiled source code that reproduces substantial portions of proprietary software.

## Report handoff

1. `pentest_agent_record_finding` for each significant discovery: hardcoded credentials, missing exploit mitigations, identified vulnerabilities with CVSS estimate, anti-analysis techniques, and outdated or vulnerable library versions.
2. Package findings with: artifact metadata (filename, SHA-256, file type, architecture), analysis environment (tool names and versions), function-by-function purpose annotations, vulnerability assessment with affected addresses, and exploitation feasibility under current mitigations.
3. Recommend: for vulnerabilities — patch, recompile with mitigations, remove hardcoded credentials; for anti-analysis — document as software-protection or malware-evasion technique depending on context; for CTF — the flag or solution path.
4. Explicitly note: all analysis was static (no execution), the artifact was not run or debugged, analysis was performed on a copy with network disabled, and no external systems were contacted.
