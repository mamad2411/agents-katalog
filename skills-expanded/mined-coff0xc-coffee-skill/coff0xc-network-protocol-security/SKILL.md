---
name: coff0xc-network-protocol-security
description: "Use when the user requests network/protocol security: TLS, DNS, TCP/UDP, HTTP/2, HTTP/3, QUIC, WiFi, Bluetooth/BLE, RF, packet/pcap/Wireshark, packet capture, handshakes, state machines, secure communication, ProVerif, or Mermaid protocol diagrams. Manual trigger: Use coff0xc-network-protocol-security."
---

# coff0xc-network-protocol-security

<!-- skill-id: cs-nps-2e7f6b41 -->

## Quick Rules (read this first for everyday tasks)
> **[Evidence first]** First locate pcaps, logs, RFCs/specs, handshakes, state machines, fields, and anomalous samples.
> **[Protocol gate]** Conclusions must explain message sequences, field semantics, encryption/authentication boundaries, and downgrade/replay/parsing risks.
> **[Verification loop]** Give re-checkable filters, field tables, reproduction conditions, and protection/detection recommendations.
> **[Hard boundary]** Confirm first for active probing, wireless/RF operations, third-party networks, production traffic injection, and fuzzing.

Follow this section first for ordinary protocol/traffic analysis; expand the full workflow only for formal modeling, active testing, or cross-system exercises.

## Capability
Protocol-security analysis capability for network protocols, TLS/DNS/QUIC/HTTP, wireless communication, packet capture, and formal modeling. It turns communication evidence into flow diagrams, risk points, and verification recommendations.

## What It Can Deliver
- Protocol flows, handshakes, and state-machine explanations
- pcap/log field analysis, anomalous fields, and security impact
- TLS/PKI/DNS/HTTP/QUIC/wireless risk inventory
- Modeling recommendations in the Mermaid/ProVerif/Tamarin direction

## What Input It Can Take
- pcaps, Wireshark exports, protocol logs, packet fields
- Protocol specs, implementation code, handshake notes, certificate chains
- Wireless/BLE/RF capture summaries or device communication flows

## Safe-Use Boundaries
- Local packet capture and authorized communication analysis can be done directly
- Do not provide unauthorized eavesdropping, intrusion, bypass, or third-party network interference steps
- Active probing, wireless transmission, and production network testing must have their scope confirmed first
- Security capabilities are used only for authorized, defensive, detection, hardening, validation, and reporting purposes by default; do not provide unauthorized attack, credential theft, persistence, detection evasion, C2, phishing collection, data exfiltration, or destructive steps.

## Why You Can Trust It
- Labels packet fields, code, and specs as separate evidence
- Prioritizes state machines and trust boundaries
- Formal modeling only expresses verifiable protocol properties; it does not exaggerate conclusions

## Typical Usage
```text
Use coff0xc-network-protocol-security to analyze the TLS handshake and anomalous fields in this pcap.
Use coff0xc-network-protocol-security to draw this protocol flow as Mermaid and point out the security boundaries.
Use coff0xc-network-protocol-security to review DNS/QUIC behavior and propose verification checks.
```

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## Expand on Demand
- Everyday tasks use only the quick rules, capability boundaries, and typical usage above; do not read the full gates by default.
- Read `references/full-workflow.md` only for deep architecture, complex multi-stage work, quality evaluation, release, formal delivery, or when the current task lacks evidence.
- After reading a reference, keep context to the minimum necessary; do not output long process write-ups or extra self-justifying material just because a reference exists.
