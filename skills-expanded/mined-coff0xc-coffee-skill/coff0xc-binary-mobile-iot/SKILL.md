---
name: coff0xc-binary-mobile-iot
description: "Use when the user requests reverse engineering, PWN, kernel, APK/IPA, Frida, firmware, IoT/ICS/SCADA, PLC/Modbus, UART/JTAG/SPI, BLE/RF, CTF, crypto review, constant-time, device packages, or executable analysis. Manual trigger: Use coff0xc-binary-mobile-iot."
---

# coff0xc-binary-mobile-iot

<!-- skill-id: cs-bmi-71e4a0cb -->

## Quick Rules (read this first for everyday tasks)
> **[Sample first]** First record file type, hash, platform, architecture, permissions, entry points, strings, and runtime boundaries.
> **[Evidence gate]** Tie reversing conclusions to offsets, functions, symbols, configuration, network endpoints, permissions, or hardware-interface evidence.
> **[Safe execution]** Static/local isolated analysis by default; bound dynamic debugging to a specific sample, environment, and observation set.
> **[Hard boundary]** Confirm first for unauthorized devices, persistence, bypass, real exploitation, private-data reads, and external communication.

Follow this section first for ordinary binary/mobile/IoT analysis; expand the full workflow only for dynamic exploitation, firmware rewriting, or hardware experiments.

## Capability
Reverse-analysis capability for binaries, mobile, IoT/ICS, firmware, and crypto implementations. It turns samples, firmware, APKs, protocols, and debugging leads into structured understanding, risk points, and a validation path.

## What It Can Deliver
- Sample/firmware structure and entry-point analysis
- Strings, configuration, permissions, communication, and hardware-interface leads
- Memory-safety, crypto-implementation, protocol-parsing, or mobile-risk findings
- Reproduction environment, tool commands, evidence, and remediation recommendations

## What Input It Can Take
- Executables, APK/IPA files, firmware, pcaps, logs, decompilation results
- Ghidra/IDA/Frida output, strings, symbols, crash stacks
- Hardware-interface notes, UART/JTAG/SPI leads, ICS protocol documentation

## Safe-Use Boundaries
- Local sample, authorized-device, and lab-environment analysis can be done directly
- Do not provide unauthorized exploitation, persistence, detection evasion, or real-target attack steps
- Avoid leaking sensitive strings or keys from malicious samples and customer firmware
- Security capabilities are used only for authorized, defensive, detection, hardening, validation, and reporting purposes by default; do not provide unauthorized attack, credential theft, persistence, detection evasion, C2, phishing collection, data exfiltration, or destructive steps.

## Why You Can Trust It
- Does static structure first, then decides on dynamic validation
- Distinguishes evidentiary strings, inferred behavior, and reproduced behavior
- Outputs tool versions, commands, and a reproducible path

## Typical Usage
```text
Use coff0xc-binary-mobile-iot to analyze this APK's permissions, network communication, and Frida hook points.
Use coff0xc-binary-mobile-iot to check this firmware for interfaces, key material leads, and protocol risks.
Use coff0xc-binary-mobile-iot to triage this executable and summarize reverse engineering findings.
```

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## Expand on Demand
- Everyday tasks use only the quick rules, capability boundaries, and typical usage above; do not read the full gates by default.
- Read `references/full-workflow.md` only for deep architecture, complex multi-stage work, quality evaluation, release, formal delivery, or when the current task lacks evidence.
- After reading a reference, keep context to the minimum necessary; do not output long process write-ups or extra self-justifying material just because a reference exists.
