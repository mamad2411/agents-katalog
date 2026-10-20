---
name: locating-defender-amsi-bad-bytes-with-gocheck
description: Binary-search a payload, DLL, or script with gocheck to locate the exact bytes Microsoft Defender or AMSI signatures, so the loader/payload author can rewrite only the flagged region instead of guessing.
domain: cybersecurity
subdomain: red-team
tags:
  - av-evasion
  - amsi
  - defender
  - signature-locator
  - payload-prep
  - gocheck
version: '1.0'
license: MIT
execution_environment: windows-operator
---

# Locating Defender / AMSI Bad Bytes with gocheck

Authorized red-team / payload-engineering use only. Run on the operator's
**Windows-operator** box (or an isolated Windows VM if the payload is untrusted)
— never on a customer endpoint.

## When to use

- A loader, DLL, or PowerShell/JS script is being caught by Defender or AMSI
  and you need to know **which bytes** trigger the signature so the next
  iteration is targeted.
- Comparing two versions of a payload to localise the regression that made it
  detectable.
- Vetting a freshly built Boaz/donut shellcode-loader against Defender before
  staging it.

`gocheck` is the modern Go reimplementation of ThreatCheck — multi-engine
(Defender, AMSI, Kaspersky), concurrent, actively maintained. It replaces
ThreatCheck for this harness's payload-prep flow.

## Prerequisites

- Windows 10/11 with Defender installed; Defender *Real-Time Protection* on
  for AMSI scanning, off for raw Defender static scanning (so the file is not
  nuked mid-binary-search).
- Add the working folder to Defender exclusions before scanning:
  `Add-MpPreference -ExclusionPath C:\evasion\work`.
- Go 1.21+ if building from source; otherwise grab the latest release binary.

## Install

```powershell
# Option A — go install
go install github.com/gatariee/gocheck@latest

# Option B — release binary
# Download the latest .exe from https://github.com/gatariee/gocheck/releases
# and drop it on PATH (e.g. C:\Tools\gocheck.exe).
```

## Quick run

```powershell
# Defender static-scan, locate the signatured byte range
gocheck.exe .\loader.exe --defender

# AMSI in-memory scan for a PowerShell payload
gocheck.exe .\amsi-bypass.ps1 --amsi

# Both engines at once (concurrent)
gocheck.exe .\loader.exe --defender --amsi

# Add Kaspersky if installed
gocheck.exe .\loader.exe --defender --amsi --kaspersky

# Verbose binary-search trace
gocheck.exe .\loader.exe --defender --debug
```

The tool reports the offset range of the bad bytes plus the byte content —
fix only that span and re-scan.

## Workflow inside Net-Runner

1. **Generate / build** the payload — see `infra:building-evasive-loaders-with-boaz`
   if you need shellcode or a multi-stage loader to start from.
2. **Locate** the signature with `gocheck`.
3. **Mutate** only the flagged bytes — re-encode, NOP-out the gadget, swap
   the WinAPI call, change the import resolution method, etc.
4. **Verify breadth** with `infra:multi-engine-av-scan-with-multcheck` (don't
   ship a payload that only bypassed Defender if the target environment runs
   anything else).
5. Save the iteration with `nr_save_note` (one note per round) so the chain
   of "what bytes were flagged → what mutation worked" is auditable.

## Output discipline

- Capture every `gocheck` run's stdout to
  `.netrunner/evidence/payload-prep/<payload>-<engine>-<round>.txt`.
- A final clean run (zero hits on the engines you care about) is the evidence
  the payload is ready to stage. Reference it from the finding's evidence
  list, not just from chat.

## Pitfalls

- Running with Real-Time Protection on against a Defender-signatured file
  will delete the file mid-search → set the exclusion path **before**
  starting.
- gocheck writes temp copies under `C:\Temp` — exclude that path too.
- `--kaspersky` flag needs Kaspersky Security Cloud installed; otherwise
  ignore it.
