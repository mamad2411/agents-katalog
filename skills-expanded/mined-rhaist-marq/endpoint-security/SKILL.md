---
name: endpoint-security
description: "Covers endpoint architecture decisions: EDR vs XDR vs MDR, CIS Benchmark hardening, application allowlisting, mobile (MDM/MAM/BYOD), and IoT hardening. Use when the user asks which endpoint protection to buy, what XDR or MDR really means, how to harden Windows/Linux/macOS, app control (WDAC/AppLocker), or managing phones and BYOD. (OT/ICS devices: ot-ics.)"
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Endpoint & device security architecture

The endpoint is where the user, the data, and the attacker all meet. Antivirus
(signature-based) is dead as a primary control: modern detection is
behavior-based. The 2025-2026 reality: attackers actively **blind the sensor**
(BYOVD driver attacks, EDR-killers) or **skip the endpoint entirely** (SaaS/
identity-only intrusions like the Snowflake/UNC5537 campaign). Architect so you
survive a silenced or absent endpoint agent.

## EDR vs XDR vs MDR: what each actually is

|         | What it is                                                                                     | Scope                        | Buy when                                                 |
| ------- | ---------------------------------------------------------------------------------------------- | ---------------------------- | -------------------------------------------------------- |
| **EPP** | Endpoint Protection Platform: the prevention layer (NGAV, device control)                      | One endpoint                 | Table stakes; usually bundled with EDR.                  |
| **EDR** | Detection + response _on the endpoint_: telemetry, behavioral detection, isolate/kill/rollback | Endpoints only (depth)       | You need host-level visibility + response. Baseline.     |
| **XDR** | Correlates telemetry **across** endpoint + identity + email + cloud + network                  | The attack surface (breadth) | Attacks move between domains or bypass the host.         |
| **MDR** | A **service**, not a product: a vendor SOC runs detection/response 24/7 for you                | Your tools + their humans    | You lack a 24/7 SOC (most orgs). Human-led is the point. |

**Decision logic (verify current market via web: it shifts yearly):**

- EDR = depth on the host; XDR = breadth across domains. EDR is right when the
  attack lives on a host; XDR when it moves between domains or never touches one.
- MDR is orthogonal: a delivery model layered on EDR/XDR. "MXDR" = MDR over XDR
  telemetry, but Gartner is firm it must stay **human-led**: automated detections
  plus human judgment + business context, not a pure automation play.
- Pragmatic 2026 default for a mid-size org: **EDR/XDR product + MDR service**. The
  tool without 24/7 humans watching it is alerts no one reads at 3am.
- Verify the current landscape/Gartner positioning before recommending a vendor:
  https://www.crowdstrike.com/en-us/cybersecurity-101/endpoint-security/edr-vs-mdr-vs-xdr/
  and Gartner MDR Market Guide / EPP Magic Quadrant (current year).
- Resilience requirements regardless of tier: **tamper protection on**, agent-health
  alerting (a sensor that goes silent is an event), driver allow/blocklist against
  BYOVD, and identity/cloud telemetry so you still see the intrusion that skips the host.

## Hardening via CIS Benchmarks

- Baseline against **CIS Benchmarks** (per-OS/app, consensus configs): Windows,
  macOS, Linux, browsers, cloud. They ship with **L1** (safe, deploy broadly) and
  **L2** (defense-in-depth, may break workflows) profiles. Start L1 fleet-wide, L2
  on high-value/Restricted-data endpoints. https://www.cisecurity.org/cis-benchmarks
- Or DISA STIGs in gov/defense contexts. Microsoft Security Baselines for Windows/Entra.
- **Measure drift continuously**: a hardened gold image rots. Use CIS-CAT / cloud
  posture tooling to score against the benchmark and alert on regression. A one-time
  hardening is a snapshot, not a control.
- Map hardening to framework controls via `load_skill control-mapping` (CIS Control 4,
  NIST CM-6/CM-7 secure config).

## Application control / allowlisting

- **Allowlisting > blocklisting.** Default-deny execution beats chasing bad hashes.
  This is the single highest-leverage control against ransomware/LOLBins on servers
  and fixed-function hosts.
- Tools: Windows App Control for Business (WDAC) / AppLocker, macOS notarization +
  MDM, Linux fapolicyd. Pair with constrained PowerShell and LOLBin (LOLBAS) blocking.
- Deploy in **audit mode first**, build the allowlist from real usage, then enforce:
  same monitor-then-block discipline as DLP. Block-mode-on-day-one breaks the business.
- Easiest wins: locked-down kiosks, servers, OT/HMI hosts (stable software set).
  Hardest: developer laptops (constantly new binaries): manage by exception/publisher rule.

## Mobile: MDM vs MAM, BYOD

- **MDM** (Mobile Device Management): manages the **whole device**: enrollment,
  config, full wipe. Right for **corporate-owned** devices.
- **MAM** (Mobile App Management): manages only the **corporate apps/data** (app
  protection policies, selective wipe of work data, container). Right for **BYOD**:
  you can't (legally/ethically) full-wipe an employee's personal phone or see their photos.
- **BYOD rule**: default to **MAM / app-protection + Conditional Access**, not full MDM,
  on personal devices. Enforce: managed app container, no copy/paste to personal apps,
  app-level PIN/biometric, block jailbroken/rooted, selective wipe on leaver.
- Tie device posture into access: a non-compliant device fails Conditional Access:
  the endpoint becomes an input to the identity decision (`load_skill iam`).

## IoT / OT: different physics, different rules

- **IoT** (the endpoint problem): devices you cannot install an agent on. Treat
  them as untrusted: own VLAN, no lateral path to user or server segments,
  default creds changed, firmware inventoried, and monitored at the network
  layer since you cannot instrument the host.
- **OT/ICS** (a different discipline, not an endpoint variant): safety and
  availability outrank confidentiality, an active scan can crash a PLC, and
  patching is not the primary control. **`load_skill ot-ics`** for the Purdue
  model, the L3.5 DMZ, IEC 62443 zones/conduits and Security Levels, and the
  regimes (NIS2 manufacturing, CRA, NERC CIP/TSA) that catch a plant.
- Decision: if the asset moves something physical, stop applying this skill and
  load `ot-ics`; the IT playbook (scan, patch, isolate, reimage) is unsafe below
  the IT/OT boundary.
