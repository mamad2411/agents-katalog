---
name: reverse-engineer-binary
description: Deconstruct compiled binaries, proprietary protocols, and obfuscated bytecode in air-gapped sandboxes to recover logic, discover vulnerabilities, and produce verifiable REA evidence ledgers. Use when analyzing untrusted binaries, auditing closed-source dependencies, inspecting firmware, or reverse engineering protocols.
allowed-tools: [read_file, write_file, create_file, search_code, execute_command, run_tests, run_linter]
---

# Reverse Engineer Binary

Deconstruct compiled executables, firmware blobs, proprietary protocols, and obfuscated bytecode in air-gapped sandboxes to generate defensible Reverse Engineering Artifact (REA) evidence ledgers.

## When to Use

- Auditing closed-source third-party binaries, libraries, or native dependencies for vulnerabilities
- Triage of suspicious binaries, trojanized packages, or malicious firmware blobs in isolation
- Reverse engineering proprietary network protocols, serialized RPC payloads, or encrypted client-server APIs
- Deobfuscating packed executables, control-flow-flattened code, or stripped virtual machine bytecode
- Producing defensible Reverse Engineering Artifact (REA) evidence reports for formal security audits

## Core Rules

- **Defensive Ethics Invariant**: Analysis is strictly restricted to defensive vulnerability research, malware triage, interoperability, and audit validation. Exploit authoring, DRM circumvention, and keygen generation are strictly barred.
- **Source Code Presence Guard**: If readable source code exists in the repository, bypass binary reverse engineering and audit the source code directly using standard analysis tools.
- **Mandatory Air-Gapped Sandbox**: Untrusted binaries must never run on the host. All inspection must execute in Tier 2 (hardened OCI/gVisor with `--read-only`, `--network=none`, `CAP_DROP=ALL`) or Tier 3 (Firecracker microVM).
- **Dynamic Tracing Confinement**: Dynamic binary instrumentation (DBI) and kernel tracing must execute in isolated guest sandboxes without external network sockets.
- **Evidence Ledger Rigor**: Every discovered defect or recovered routine must reference exact memory offsets, disassembly snippets, and cryptographic hashes in the REA ledger.

## Suggested Process

### 1. Ingest, Hash, and Verify Boundaries
- Compute cryptographic digests: SHA-256 and MD5 checksums, SSDEEP fuzzy hash, and TLSH locality-sensitive hash.
- Confirm repository lacks source code; verify engagement scope is authorized for defensive security research.

### 2. Initialize Air-Gapped Sandbox Environment
- Launch Tier 2 container with read-only root, dropped Linux capabilities (`CAP_DROP=ALL`), non-root UID (10001:10001), and active network air-gap (`--network=none`).
- Mount target artifact into scratch space with `noexec` mount flag during static triage; set resource caps (RAM $\le 2\text{GB}$, CPU $\le 2.0$, PIDs $\le 64$).

### 3. Multi-Architecture Static Decompilation
- **Header & File Classification**: Query format (ELF, PE, Mach-O, Wasm) and CPU architecture (x86, x86_64, ARMv7, AArch64, RISC-V) via header analyzers.
- **Entropy & Packing Analysis**: Calculate section Shannon entropy; detect packers (UPX, Themida, VMProtect) when entropy $H(X) \ge 7.2$.
- **Symbol & String Extraction**: Extract ASCII, UTF-16, and obfuscated strings; map imported symbols and exported functions.
- **Decompiler Protocol**: Run headless Ghidra scripts, IDA Pro microcode decompilation, Binary Ninja MLIL/HLIL, or radare2 (`r2 -c 'aaa; pdc'`) to recover control flow graphs (CFG).

### 4. Dynamic Instrumentation and Kernel Tracing
- **Runtime Hooking**: Attach Frida v16+ (`Interceptor.attach`, `Memory.protect`) inside guest to capture decrypted buffers and trace function arguments.
- **Instruction Tracing**: Deploy Frida `Stalker` or non-invasive eBPF user probes (`uprobes`/`uretprobes` via bpftrace) to log execution paths without triggering anti-debug traps.
- **Emulation**: Use Unicorn or QEMU user emulation for foreign architectures (ARM/MIPS blobs on x86_64 hosts).

### 5. Protocol Dissection and Deobfuscation
- **Traffic Capture & TLS Extraction**: Dissect packet captures with Wireshark/TShark; extract session keys via `SSLKEYLOGFILE` or memory hooks for mitmproxy decryption.
- **Wire Format Reconstruction**: Parse Tag-Length-Value (TLV) framing, gRPC, and Protobuf schemas via `protoc --decode_raw`.
- **Symbolic Execution**: Employ angr or Z3 to resolve dispatcher loops in Control Flow Flattening (CFF) and prune opaque predicates.
- **AST Simplification**: Apply algebraic simplification to normalize Mixed Boolean-Arithmetic (MBA) expressions.

### 6. Mobile and Bytecode Deconstruction
- **Android APK / DEX**: Decompile DEX bytecode with Jadx; extract manifests and smali resources with APKTool.
- **Unity & Native Hybrid**: Run Il2CppDumper to recover class declarations, method offsets, and string literals from `libil2cpp.so`.
- **.NET & JVM**: Decompile managed assemblies using ILSpy, dnSpy, or CFR.

### 7. Synthesize REA Ledger and Secure Cleanup
- Document all identified entry points, cryptographic algorithms, network endpoints, and data schemas.
- Catalog vulnerabilities with exact virtual addresses, disassembly snippets, and CWE/CVSS scores.
- Terminate ephemeral sandbox containers and shred temporary scratch memory.

## Output Format

Format results into a structured Reverse Engineering Artifact (REA) ledger:

```markdown
# <Artifact Name> - Reverse Engineering Evidence Ledger

## Artifact Identification
- Filename: <binary_name> | Byte Size: <bytes>
- SHA-256: <64-character-hex-hash> | SSDEEP: <fuzzy-hash>
- Architecture: <e.g. x86_64, AArch64, RISC-V, Wasm> | Format: <ELF, PE, Mach-O>
- Detected Toolchain / Packer: <detected signature or Unpacked> | Max Entropy: <value>

## Environment & Provenance
- Sandbox Tier: Tier 2 (OCI / gVisor) | Network: Air-gapped (--network=none)
- Decompiler Toolchain: Ghidra Headless <ver> / Binary Ninja <ver> / radare2 <ver>

## Attack Surface Inventory
- Dynamic Dependencies: <shared objects or DLLs>
- Sensitive Strings & Endpoints: <extracted URLs, IPs, keys>
- Dissected Protocol Wire Schemas: <reconstructed framing or .proto definitions>

## Vulnerability & Defect Matrix
| Virtual Offset | Category | Severity | Root Cause | Remediation |
| :--- | :--- | :--- | :--- | :--- |
| `0x004012A0` | CWE-120 Buffer Overflow | High (CVSS 7.8) | Unbounded memory copy | Enforce bounded copy |
```

## Failure Modes

- **Host execution leak**: Running untrusted binaries outside sandboxes risks host compromise. **Mitigation**: Strictly mandate Tier 2/3 OCI containers with `--read-only`, `--network=none`, and `CAP_DROP=ALL`.
- **Decompiling existing source code**: Reverse engineering binaries when source code is present wastes compute. **Mitigation**: Enforce Source Code Presence Guard in step 1.
- **Network egress during analysis**: Target binaries phoning home or triggering network beacons. **Mitigation**: Enforce container-level network air-gap (`--network=none`).
- **Unverified assembly assertions**: Stating defects exist without virtual addresses or assembly proofs. **Mitigation**: Require proof offsets and decompiled snippets in REA ledger.

## Output Contracts

When completing binary analysis or protocol reverse engineering, emit:

- Structured REA evidence ledger markdown document following the Output Format template.
- If reporting security vulnerabilities, companion contract must adhere to `contracts/schemas/security-audit.json`.
- If reconstructing network or RPC schemas, companion contract must adhere to `contracts/schemas/api-contract-spec.json`.

## Security Guardrails (OWASP ASI)

- **ASI05 Sandbox Escape Guard**: Never enable Docker socket forwarding or privileged flags (`--privileged`) during reverse engineering tasks.
- **ASI06 Binary Data Guard**: Do not output raw unescaped binary byte streams or shellcode sequences into user-facing chat logs.
- **AST03 Egress Guard**: Deny all network egress during dynamic binary execution; enforce fail-closed air-gap boundaries.

## Checklist

- [ ] Defensive audit or vulnerability research authorization confirmed.
- [ ] Source code presence checked; skipped binary analysis if source code is present.
- [ ] Cryptographic checksums (SHA-256, SSDEEP, TLSH) computed and recorded.
- [ ] Tier 2/3 sandbox container initialized with `--read-only`, `--network=none`, and `CAP_DROP=ALL`.
- [ ] Section Shannon entropy calculated to detect packers or encrypted payloads.
- [ ] Disassembler/decompiler (Ghidra, IDA Pro, Binary Ninja, radare2) executed on critical functions.
- [ ] Dynamic instrumentation (Frida, eBPF) conducted inside guest without network exposure.
- [ ] Protocol payloads or bytecode disassembled and reconstructed into schemas.
- [ ] REA evidence ledger populated with exact virtual offsets and remediation guidance.
- [ ] Ephemeral sandbox container destroyed and scratch memory purged upon completion.

## Related Skills

- **security-audit**: Conduct end-to-end vulnerability assessments and CVSS scoring
- **systematic-debugging**: Formulate and verify control flow and execution hypotheses
- **supply-chain-security**: Validate package hashes, provenance, and SBOM attestations
- **prompt-injection-defense**: Analyze embedded agent prompts and adversarial inputs
- **skill-preflight-ast-check**: Validate zero-execution AST scripts and sandbox tier isolation
- **review-code**: Audit decompiled pseudocode and recovered source logic
- **performance-profiling**: Trace instruction execution cycles and memory patterns
- Companion reference: `references/ghidra-radare2-and-rea-evidence-ledgers.md`
- Companion example: `examples/binary-triage-and-vulnerability-dossier.md`
