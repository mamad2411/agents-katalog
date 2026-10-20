---
name: multi-engine-av-scan-with-multcheck
description: Statically scan a payload against multiple AV engines with MultCheck to confirm a Defender-clean build is not lit up by every other vendor before staging it for a target environment.
domain: cybersecurity
subdomain: red-team
tags:
  - av-evasion
  - multi-engine
  - payload-prep
  - signature-coverage
  - multcheck
version: '1.0'
license: MIT
execution_environment: windows-operator
---

# Multi-engine AV Scan with MultCheck

Authorized red-team / payload-engineering use only.

## When to use

- After `infra:locating-defender-amsi-bad-bytes-with-gocheck` has produced a
  Defender-clean build, **before** staging the payload to a target. Defender
  silence is necessary but not sufficient — the target environment may run
  any of: ESET, Sophos, CrowdStrike, SentinelOne, Bitdefender, Kaspersky,
  Trend Micro, McAfee, Symantec.
- Differential testing across iterations of a loader to see *which engines*
  improve / regress per change.
- Building a coverage table for the engagement report ("payload was clean
  against N of M engines representative of customer's AV vendor").

`MultCheck` is vendor-agnostic — it shells out to whatever AV engines you
have configured locally and aggregates the verdicts. Unlike gocheck (which
locates the bad bytes for *one* engine), MultCheck answers the *breadth*
question across many engines in one pass.

## Prerequisites

- A Windows box with the AV engines you want to test installed and their CLI
  scanners on PATH (each engine MultCheck knows about ships a CLI hook).
- Defender exclusion for the working folder
  (`Add-MpPreference -ExclusionPath C:\evasion\work`).
- Go 1.21+ if building from source.

## Install

```powershell
git clone https://github.com/MultSec/MultCheck.git C:\Tools\MultCheck
cd C:\Tools\MultCheck\src
$env:GOOS="windows"; $env:GOARCH="amd64"
go build -o ..\bin\multcheck.exe
```

Or grab the prebuilt `bin/multcheck_64.exe` from the repo.

## Quick run

```powershell
# Default: scan against every engine configured in config.json
.\bin\multcheck.exe -f .\loader.exe

# Scan against a specific engine
.\bin\multcheck.exe -f .\loader.exe -s defender

# Verbose mode
.\bin\multcheck.exe -f .\loader.exe -d
```

`config.json` in the MultCheck root declares each engine + its CLI invocation
+ the regex/string MultCheck uses to detect a hit. Mirror the engines you
care about for the target environment — drop ones you don't.

## Workflow inside Net-Runner

1. Confirm `gocheck` says the build is Defender + AMSI clean.
2. Run MultCheck against the engine roster you maintain for the customer.
3. If any engines hit, treat the next iteration the same way: locate, mutate,
   re-scan. For engines without a byte-locator like gocheck, iterate by
   swapping obfuscation chains (Boaz `-obf`, `-c`, `-e` options) and re-scan.
4. Save the final coverage table to
   `.netrunner/evidence/payload-prep/<payload>-multcheck-coverage.json`.

## Discipline

- Multi-engine results are static-scan only — runtime EDR detections
  (behavioural / telemetry) are a separate layer and need real detonation in
  a representative VM. MultCheck answers signature coverage, not the
  full kill chain.
- Keep an engine roster note per engagement (the customer's AV/EDR stack)
  and treat MultCheck output as evidence that the payload meets that bar.
- Do **not** upload payloads to public multi-engine services
  (VirusTotal, AnyRun) — that immediately seeds detection signatures and
  burns the engagement. MultCheck runs **locally**; that is the point.
