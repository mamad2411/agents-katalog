---
name: dotnet-il-decompile
description: >
  Decompile and inspect .NET assemblies (IL/C#) for owned software, labs, and authorized
  reverse engineering: tools (ilspycmd, ILSpy, dnSpyEx, dotnet-ildasm), symbol strategy,
  trimming/AOT caveats, and malware hygiene. Use when ILSpy, decompile DLL, read C# from
  assembly, audit third-party package you may inspect under license, or CTF .NET RE —
  not for cracking licenses or unauthorized circumvention.
---

# .NET IL Decompile

## Scope And Authorization

- **In scope:** Binaries you own, open source, CTF, or licensed analysis with authorization.
- **Out of scope:** Piracy, license keygen, bypassing protections on third-party commercial software without permission.
- Treat unknown assemblies as potentially malicious—analyze in VM/sandbox.
- Redact secrets found in assemblies from public notes; rotate if real credentials.
- Pair with `binary-re` skills as needed and `code-quality-standards` for reimplementation.

## When To Use

- Understanding behavior of a NuGet dependency without sufficient docs.
- Recovering logic from internal tool when source lost (legal ownership).
- CTF/.NET malware lab triage (authorized).
- Verifying obfuscation effectiveness on **your** product.
- Comparing publicized vulnerability to actual IL.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| EF performance | `dotnet-efcore-query-perf` |
| Native C/C++ RE | `binary-re/static-analysis` etc. |
| Java decompile | jadx-oriented skills |
| Exploit development | Not this skill’s goal |
| Code quality of source | `code-quality-standards` |

## Tooling

| Tool | Role |
| --- | --- |
| ILSpy / ilspycmd | Decompile to C#; browse assemblies |
| dnSpyEx | Debug/decompile (use trusted builds) |
| `dotnet ildasm` / ildasm | IL text |
| `strings` / `Detect It Easy` | Quick triage |
| SO_RE / sandbox | Malware samples |

```bash
# Example: ilspycmd (owned workstation)
# dotnet tool install -g ilspycmd
ilspycmd MyLib.dll -o ./decompiled -p
```

## Workflow

### 1. Confirm legal scope and safety

1. Ownership/license allows decompilation for your purpose.
2. Malware: VM, no secrets network, snapshot.
3. Success: readable understanding of target methods; notes + evidence paths.

### 2. Inventory assembly

```bash
file MyLib.dll
# PowerShell
[System.Reflection.AssemblyName]::GetAssemblyName("MyLib.dll")
# List references with ildasm or ILSpy
```

1. Note target framework (net4x vs net6+), self-contained single-file, ReadyToRun, Native AOT.
2. Single-file/AOT may block classic managed decompile—adjust expectations.

### 3. Decompile

1. Open in ILSpy; export project if needed.
2. Start at `Main`, module initializers, obvious service entrypoints.
3. Search strings for URLs, feature names, error messages.
4. Cross-check IL when C# decompilation looks wrong (async state machines, iterators).

### 4. Handle obfuscation (awareness)

| Symptom | Approach |
| --- | --- |
| Random names | Follow call graph; rename locally in notes |
| Control flow fluff | Focus on dangerous APIs (Process, Registry, WebRequest) |
| Encrypted strings | Dynamic debug in lab if authorized |
| Packers | Unpack only in sandbox |

1. Do not claim full recovery when AOT/native.
2. For **your** product: measure residual clarity after obfuscator—security through obscurity is weak.

### 5. Secrets and supply chain

1. Flag embedded connection strings, API keys, private URLs.
2. Check strong name / Authenticode if validating publisher.
3. Dependency: compare decompiled behavior to expected package (typosquat suspicion).

### 6. Document findings

1. File path, assembly version, method tokens, decompiled snippet, confidence.
2. Prefer re-writing understanding in your own words over redistributing decompiled commercial source.

### 7. Hand off

1. If vulnerability: report via `secure-sdlc` process with minimal repro.
2. If lost source recovery: rebuild plan with tests.
3. Wipe malware samples per policy.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Owned/CTF/authorized | Crack commercial DRM |
| Malware | Sandbox | Run as admin on host |
| Trust | Verify tool hashes | Random dnSpy from ads |
| Secrets | Rotate when found | Paste keys in ticket public |
| AOT | Note limits | Force wrong conclusions |
| Obfuscation | API-focused analysis | Give up without strings |

## Output Checklist

- [ ] Legal/authorization recorded
- [ ] Sandbox used if untrusted
- [ ] Assembly metadata captured
- [ ] Decompilation method documented
- [ ] Key methods and strings analyzed
- [ ] Secrets handled/rotated
- [ ] Limits (AOT/obfuscation) stated
- [ ] Notes stored securely
- [ ] No unauthorized redistributed source
- [ ] Next actions (fix/patch/rebuild) clear

## Rules

- Authorized reverse engineering only; no piracy.
- Sandbox unknown binaries.
- Decompilation accuracy is imperfect—verify critical logic.
- Protect discovered secrets.
- Focus on .NET managed IL/C# inspection workflows.
