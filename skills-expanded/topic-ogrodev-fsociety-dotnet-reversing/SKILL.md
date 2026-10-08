---
name: dotnet-reversing
description: |
  Activate this skill when the user mentions ".NET", "CLR", "managed code",
  "C# binary", "C# decompile", "decompile C#", "VB.NET", "F# binary",
  "ILSpy", "dnSpy", "de4dot", "dotPeek", ".NET Reflector", "monodis", "ilspycmd",
  "ilasm", "ildasm", "Cecil", "Mono.Cecil", "dnlib",
  ".NET Reactor", "ConfuserEx", "Dotfuscator", "SmartAssembly", "Eazfuscator",
  "Babel obfuscator", "Crypto Obfuscator", "Agile.NET", "Themida .NET",
  "deobfuscate", "deobfuscation", ".NET obfuscation", "unpack .NET",
  "mscoree", "mscorlib", "System.Reflection", "System.Runtime",
  "assembly metadata", "IL code", "MSIL", "CIL", "OpCodes",
  "Common Language Runtime", "CLR hosting", "JIT compilation",
  "NuGet", "Mono", ".NET assembly", ".NET executable", "managed executable",
  ".NET malware", "C# malware", "C# RAT", "C# loader", "C# dropper",
  "C# stager", "C# implant", "C# beacon", "C# payload",
  "BinaryFormatter", "ObjectStateFormatter", "ViewState deserialization",
  "JSON.NET TypeNameHandling", "DataContractSerializer",
  ".NET serialization", "ysoserial.net", "TypeConfuseDelegate",
  "P/Invoke", "DllImport", "Marshal", "unsafe code", "fixed pointer",
  ".NET patching", "IL patching", "Harmony", "runtime hooking",
  "Assembly.Load", "AppDomain", "Reflection.Emit",
  ".NET config extraction", "C2 extraction", "beacon config",
  "Costura.Fody", "ILMerge", "embedded assembly",
  ".NET RE", ".NET reverse engineering", "managed binary analysis",
  or discusses analyzing, decompiling, deobfuscating, patching, or exploiting .NET assemblies.
version: 2.0.0
---

# .NET Reverse Engineering

## Why .NET Is Different

.NET binaries ship IL (Intermediate Language) code with full metadata — type names, method signatures, string literals, inheritance hierarchies. This makes decompilation far more effective than with native code. A clean .NET binary decompiles to near-source-quality C#. Obfuscation raises the bar but never eliminates the metadata entirely because the CLR needs it to execute.

This matters for offensive work: .NET malware leaks intent through its metadata. Even heavily obfuscated samples expose type references to `System.Net.Sockets`, `System.Security.Cryptography`, or `System.Runtime.InteropServices` — revealing capability before you touch the IL.

## Detection — Is This .NET?

Confirm a binary is .NET before choosing your toolchain. Wrong tools waste time.

```bash
# Quick check — file magic
file <binary>
# Look for: "Mono/.Net assembly" or "PE32 executable ... Mono/.Net"

# Confirm via PE imports — .NET binaries import mscoree.dll
r2 -qc 'ii~mscoree' <binary>
# _CorExeMain = .NET EXE, _CorDllMain = .NET DLL

# CLI header presence — Data Directory entry 14
r2 -qc 'iH~CLR' <binary>

# monodis sanity check
monodis --assembly <binary>
```

If the binary is mixed-mode (C++/CLI), it has both native and managed code. Use `monodis` for the managed portion and radare2/Ghidra for native.

## Core Workflow

Follow this sequence for any .NET target. Skip steps that do not apply, but never skip triage.

### Phase 1 — Triage and Metadata Extraction

Goal: understand what you have before deep analysis.

```bash
# Assembly identity
monodis --assembly <binary>

# Type inventory — namespaces reveal purpose
monodis --typedef <binary>

# External dependencies — what frameworks/libraries does it use?
monodis --assemblyref <binary>
monodis --typeref <binary>

# Entry point identification
monodis --method <binary> | grep -A5 "\.entrypoint"

# Embedded resources — configs, encrypted payloads, embedded DLLs
monodis --manifest <binary>

# String extraction — URLs, IPs, registry keys, crypto constants
strings -el <binary>   # Unicode strings (common in .NET)
strings -a <binary>    # ASCII strings
floss <binary>         # FLARE obfuscated string solver
```

Key questions to answer during triage:
- What namespaces exist? (`System.Net` = networking, `System.Security.Cryptography` = crypto)
- Are names readable or garbled? (obfuscation indicator)
- What external assemblies does it reference?
- Are there embedded resources? (common payload delivery vector)
- Does it reference `DllImport`/`P/Invoke`? (native API access)

### Phase 2 — Obfuscation Assessment

Determine if and how the binary is obfuscated. This dictates your next steps.

```bash
# de4dot auto-detection (does not modify — just reports)
de4dot --detect <binary>

# Manual checks
monodis --typedef <binary>    # Garbled names = obfuscation
monodis --customattr <binary> # Obfuscator watermark attributes
```

**Obfuscator Fingerprints:**

| Obfuscator | Indicators |
|------------|------------|
| **ConfuserEx** | Unicode-garbled names, `ConfuserEx` in attributes, proxy delegates, `<Module>.cctor()` initialization |
| **Dotfuscator** | `DotfuscatorAttribute`, PreEmptive watermarks, renamed but structurally intact |
| **.NET Reactor** | `.reacto` section, `__EncryptedAssembly__` resource, native stub loader |
| **SmartAssembly** | `SmartAssembly.Attributes`, `{SmartAssembly}` strings, embedded error reporting |
| **Eazfuscator** | `EazAttribute`, virtualized method bodies, custom opcode interpreter |
| **Babel** | `BabelAttribute`, `BabelObfuscator` strings, resource encryption |
| **Crypto Obfuscator** | `CryptoObfuscator` strings, heavy resource encryption |
| **Agile.NET** | `CliSecure` references, native mode option |
| **Themida/.NET** | Themida-style VM wrapping managed code, very heavy |
| **Costura.Fody** | Not obfuscation — embeds DLL dependencies as resources. `costura.` prefixed resources |

If obfuscated → Phase 2a (deobfuscate first). If clean → skip to Phase 3.

### Phase 2a — Deobfuscation

```bash
# Automatic deobfuscation
de4dot <binary> -o <clean.exe>

# ConfuserEx specifically (use the cex fork)
de4dot-cex <binary> -o <clean.exe>

# Force a specific deobfuscator engine
de4dot <binary> -p <code> -o <clean.exe>
# Codes: an=Agile.NET, ba=Babel, co=CryptoObfuscator, cx=ConfuserEx,
#         df=Dotfuscator, dr=.NETReactor, ef=Eazfuscator, sk=SmartAssembly

# Verify deobfuscation worked
monodis --typedef <clean.exe>
```

If automatic deobfuscation fails, see `references/deobfuscation.md` for manual techniques.

### Phase 3 — Decompilation

```bash
# Full C# source recovery (primary tool)
ilspycmd <binary> -o <outdir>/

# IL-level dump (when C# decompilation fails or you need exact opcodes)
monodis --method <binary> > il-dump.il

# Single type decompilation
ilspycmd <binary> -t <Namespace.TypeName>
```

Decompilation output goes to `extracted/<analysis-name>/dotnet-source/`.

### Phase 4 — Deep Analysis

With readable source, focus on:

**For malware:**
- Entry point and initialization flow
- C2 communication (look for `HttpClient`, `WebClient`, `TcpClient`, `Socket`, `WebSocket`)
- Encryption/decryption routines (look for `Aes`, `RijndaelManaged`, `RSA`, XOR loops)
- Persistence mechanisms (`Registry`, `ScheduledTask`, `WMI`, `Startup`)
- Config extraction (hardcoded strings, resource decryption, embedded JSON/XML)
- Anti-analysis (sleep loops, VM detection, debugger checks via `Debugger.IsAttached`)
- Process injection (`VirtualAllocEx`, `WriteProcessMemory`, `CreateRemoteThread` via P/Invoke)

**For application security:**
- Serialization vulnerabilities (see `references/serialization-attacks.md`)
- Reflection abuse (`Assembly.Load`, `Activator.CreateInstance`, `Type.InvokeMember`)
- P/Invoke surface (see P/Invoke Analysis below)
- Hardcoded secrets (connection strings, API keys, certificates)
- Cryptographic weaknesses (ECB mode, static IVs, weak key derivation)
- SQL injection in ORM bypass patterns
- Path traversal in file operations

See `references/malware-analysis.md` for detailed malware analysis patterns.

### Phase 5 — Patching and Instrumentation

When you need to modify behavior — bypass license checks, neutralize anti-analysis, redirect C2:

```bash
# Roundtrip: decompile IL → edit → reassemble
monodis <binary> > code.il
# Edit code.il (modify IL instructions)
ilasm code.il -output:<patched.exe>

# Verify patch
monodis --method <patched.exe> | grep -A10 "<target-method>"
```

See `references/patching.md` for IL patching patterns and runtime instrumentation.

## P/Invoke Analysis

P/Invoke (`DllImport`) calls bridge managed code to native APIs. In malware, this is where the dangerous operations happen — process injection, privilege escalation, AV evasion.

```bash
# Extract all P/Invoke declarations
monodis --implmap <binary>

# In decompiled source, search for DllImport
grep -rn "DllImport" <outdir>/
grep -rn "extern static" <outdir>/
```

**Critical P/Invoke patterns in malware:**

| API | Technique |
|-----|-----------|
| `VirtualAllocEx` + `WriteProcessMemory` + `CreateRemoteThread` | Classic process injection |
| `NtCreateSection` + `NtMapViewOfSection` | Section-based injection |
| `QueueUserAPC` + `NtTestAlert` | APC injection |
| `SetWindowsHookEx` | Hook injection |
| `RtlMoveMemory` with delegate marshaling | Shellcode execution |
| `AmsiScanBuffer` | AMSI bypass (patching target) |
| `EtwEventWrite` | ETW bypass |
| `NtSetInformationThread` | Anti-debug (hide from debugger) |

## Embedded Assembly Extraction

.NET malware frequently embeds additional assemblies as resources, loading them at runtime via `Assembly.Load()`.

```bash
# List resources
monodis --manifest <binary>

# Common patterns:
# 1. Costura.Fody — look for costura.*.dll.compressed resources
# 2. Custom loader — look for AppDomain.AssemblyResolve handler
# 3. Encrypted payload — resource loaded, decrypted, then Assembly.Load()

# Extract resources with ilspycmd
ilspycmd <binary> --resource-dir <outdir>/resources/
```

After extraction, analyze each embedded assembly as a separate target.

## Output Format

Report .NET analysis findings using this structure:

```
## .NET Analysis: <binary-name>

### Assembly Identity
- **Name**: <assembly-name>
- **Version**: <version>
- **Framework**: <target-framework>
- **Entry Point**: <Namespace.Class.Method>
- **Obfuscation**: <obfuscator or "None detected">

### Architecture
- **Namespaces**: <count> (<key namespaces>)
- **Types**: <count>
- **Methods**: <count>
- **P/Invoke Imports**: <count>
- **Embedded Resources**: <count>

### Key Findings
1. <finding with severity>
2. ...

### Indicators of Compromise
- **C2**: <addresses/domains>
- **Mutexes**: <mutex names>
- **Persistence**: <mechanism>
- **File Drops**: <paths>

### Deobfuscation Notes
- **Tool Used**: <de4dot/manual/none>
- **Obfuscator**: <identified obfuscator>
- **Success Level**: <full/partial/failed>
```

## Reference Documents

| Document | Coverage |
|----------|----------|
| `references/clr-internals.md` | PE structure, metadata tables, token resolution, JIT compilation, assembly loading, type system |
| `references/deobfuscation.md` | de4dot usage, manual deobfuscation for each major obfuscator, anti-tamper removal, string decryption |
| `references/malware-analysis.md` | C2 extraction, config decryption, loader patterns, .NET RAT families, anti-analysis bypass |
| `references/patching.md` | IL instruction editing, method replacement, runtime hooking with Harmony, Frida for .NET |
| `references/serialization-attacks.md` | BinaryFormatter, JSON.NET, ViewState, DataContractSerializer, ysoserial.net gadget chains |
