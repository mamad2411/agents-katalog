---
name: powershell-reliability-framework
description: PRF v0.1.0 reliability layer for AI-generated PowerShell. Load before generating, modifying, reviewing, or executing any PowerShell / Windows automation. Enforces an Environment-Probe -> Operation-Classification -> Risk-Gate protocol plus hard safety, compatibility, idempotency, error-handling and here-string/heredoc rules, and a propose(-WhatIf)-then-execute loop.
version: 0.1.0
---

# PowerShell Reliability Framework (PRF)

Mission: every PowerShell script an agent emits must be **compatible with the probed
environment, safe by default, idempotent, observable, and reversible**.
LLMs can produce PowerShell *syntax*; this skill exists to make them produce
PowerShell that survives contact with real Windows estates.

## 0. When this skill applies

Apply whenever you are asked to produce, change, review, explain-for-execution, or run:

- `.ps1`, `.psm1`, `.psd1` files or ad-hoc shell commands on Windows
- remoting (`Invoke-Command`/`Enter-PSSession`), scheduled tasks, services, processes
- registry, filesystem ACLs, firewall, network configuration
- Active Directory, Azure (`Az.*`), Microsoft Graph, Exchange Online operations
- here-strings (`@'...'@`, `@"..."@`), generated `.ps1` bodies, or any PowerShell
  produced from bash/sh on a CI runner for execution on a Windows host

## 1. Generation Protocol (mandatory, in order)

### Step 1 — Probe the environment FIRST. Never assume.

Run the canonical probe (`tools/probe-environment.ps1`) or this inline equivalent,
and record the results before writing a single cmdlet:

```powershell
$PSVersionTable.PSVersion            # 5.1 vs 7.x decides COMP-* rules
$PSVersionTable.PSEdition            # Desktop vs Core
[Environment]::OSVersion.VersionString
(New-Object Security.Principal.WindowsPrincipal(
    [Security.Principal.WindowsIdentity]::GetCurrent()
)).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)   # elevated?
Get-ExecutionPolicy -List
(Get-CimInstance Win32_ComputerSystem).PartOfDomain     # AD context?
Get-Module -ListAvailable -Name ActiveDirectory, Az.Accounts, PSScriptAnalyzer
```

If a required module cannot be probed present, **say so and stop** — do not emit a
script that merely assumes it. `CommandNotFoundException` from uninstalled RSAT /
missing modules is the #1 AI-PowerShell failure mode (see `knowledge/compatibility.md`).

### Step 2 — Classify the operation

| Class | Meaning | Examples | Default posture |
|---|---|---|---|
| **R** | Read-only | `Get-*`, `Test-Path`, search/query cmdlets | allowed after probe |
| **W** | Write/update | `Set-*`, `New-*`, `Copy-Item`, registry writes | preview with `-WhatIf` first |
| **D** | Destructive | `Remove-*`, `Stop-*`, format, ACL/ownership changes | `-WhatIf` + explicit human confirmation gate |
| **N** | Network/outbound | `Invoke-RestMethod`, downloads, remoting to new hosts | pin endpoint, enforce TLS 1.2+, never pipe into execution |
| **C** | Credential/identity | passwords, certs, tokens, AD/Azure identity objects | refuse plaintext handling; escalate to human |

A single request can span several classes; classify the *highest* class involved.

### Step 3 — Apply the hard gates (violating any ⇒ rewrite before answering)

1. **No dynamic execution.** Never `Invoke-Expression`, `iex`, `& $string`,
   `[scriptblock]::Create`, or encoded commands. Generate files, not eval. (SEC-001..)
2. **Download ≠ execute.** Never pipe web content into execution. Download →
   verify hash/signature → inspect → execute the file. (SEC-002..004)
3. **Destructive defaults are scoped.** `Remove-Item`/`Stop-*` ship with
   `-WhatIf`, precise `-LiteralPath`/filters, and no bare wildcards on delete. (SAFE-*)
4. **Errors are handled.** State-changing cmdlets get `-ErrorAction Stop` inside
   `try/catch`; native tools get `$LASTEXITCODE` checks. No empty catch. (ERR-*)
5. **Idempotent by construction.** Guard/converge `New-*`/`Set-*` so re-running
   reaches the same state instead of erroring or duplicating. (IDEM-*)
6. **Compatibility declared.** Target the *probed* version. 7+-only constructs
   (`ForEach-Object -Parallel`, ternary, `&&`) are banned unless the probe proves
   7.x; state the requirement explicitly in your answer. (COMP-*)
7. **No plaintext secrets.** Prefer `SecretManagement`/credential objects; never
   echo secrets into output, logs or transcripts. (SEC-014..)
8. **Observable.** Structured output objects, meaningful verbose messages, correct
   exit codes; `Write-Host` is not a data channel.
9. **Strings are carried correctly.** Both here-string delimiters at column one
   (HD-001, HD-002); no bash `<<EOF` in PowerShell, which tokenizes as file
   redirection and runs nothing (HD-003); `-Encoding UTF8` is not a cross-runtime
   fix — 5.1 still writes a BOM (HD-004); no unquoted `-Command` string into a
   POSIX shell (HD-005); no script body through `Invoke-Expression` (HD-006);
   one stdin cannot carry a script and a payload (HD-007); generated artifacts
   written with `[IO.File]::WriteAllText`, not piped into a cmdlet sink (HD-009).

### Step 4 — Self-review against the rule corpus

Before answering, scan your draft against `rules/reliability-rules.yaml`
(categories: `compatibility`, `safety`, `idempotency`, `security`,
`error-handling`, `heredoc`). If you intentionally deviate, quote the violated rule id and
justify it in one sentence.

### Step 5 — Propose → Confirm → Execute → Verify → Report

- Present the script **plus**: assumptions taken from the probe, blast radius,
  and a rollback story.
- For D/C-class operations: run with `-WhatIf` (or `-Confirm`) first and obtain
  explicit human approval for the live run.
- After execution: read back the intended state, capture stderr/events, report
  what changed and how to roll back.

## 2. Quick repair map (bad → good)

| Anti-pattern | Replacement |
|---|---|
| `Invoke-WebRequest url \| iex` | download → verify hash → inspect → invoke saved file |
| `Remove-Item C:\Logs\* -Recurse -Force` | filter by age/name → `-WhatIf` → confirmed scoped delete |
| `cat f.txt \| findstr err` | `Select-String -Path f.txt -Pattern err` |
| `New-Item C:\Temp` unguarded | `if (-not (Test-Path -LiteralPath C:\Temp)) { New-Item C:\Temp \| Out-Null }` |
| `Copy-Item a b` bare | `try { Copy-Item a b -ErrorAction Stop } catch { Write-Error $_; exit 1 }` |
| `ForEach-Object -Parallel` | plain pipeline unless probe proved PowerShell 7+ |
| `Get-WmiObject Win32_Service` | `Get-CimInstance Win32_Service` |
| indented `'@` terminator | `'@` at column one — indentation is a parse error, not a style choice |
| `cmd <<EOF` in pwsh | rewrite in PowerShell — `<<` is file redirection here, nothing runs |
| `Set-Content -Encoding UTF8` on a 5.1 host | `[IO.File]::WriteAllText(... , (New-Object System.Text.UTF8Encoding $false))` |
| `@'...'@ \| Out-File f` | build the string, then `WriteAllText` — cmdlet sinks add CRLF and a runtime-dependent default encoding |
| `pwsh -Command "...\$var..."` from bash | `pwsh -File script.ps1` — write the script from a quoted `<<'PSEOF'` heredoc first |

Full catalog with explanations: `knowledge/anti-patterns.md`.
Here-string and heredoc specifics: `knowledge/here-strings-and-heredocs.md`.

## 3. Deeper references

| File | Contents |
|---|---|
| `knowledge/powershell-model.md` | object pipeline, streams, error semantics |
| `knowledge/compatibility.md` | 5.1 ↔ 7.x deltas, module availability reality |
| `knowledge/security-rules.md` | attack surface & defensive generation posture |
| `knowledge/enterprise-patterns.md` | ShouldProcess, logging, remoting, bulk ops |
| `knowledge/anti-patterns.md` | AP-01..AP-24 catalog with repairs |
| `knowledge/here-strings-and-heredocs.md` | delimiter grammar, bash heredoc collision, 5.1 ↔ 7.x writer divergence, POSIX transport layer |
| `examples/bad/`, `examples/good/` | paired negative/positive scripts |
| `benchmark/cases.json` | scored evaluation rubric (v0.1: 110 cases) |

## 4. Escalation triggers — stop and ask the human

Domain-wide or tenant-wide scope · credential/certificate creation, export or
handling · `Set-ExecutionPolicy`, Defender exclusions, ACL/ownership takeover ·
anything irreversible · probe results contradicting the user's stated environment ·
requests that only make sense via dynamic execution or download-and-run.
