---
name: ot-ics
description: "Covers OT/ICS security engineering: inverted CIA, the Purdue model and IT/OT DMZ, IEC 62443 (SL-T/SL-C/SL-A, the 7 foundational requirements, which parts matter), NIST SP 800-82r3, safe passive monitoring, and OT incident response. Use when the user asks about securing a plant, factory, SCADA, PLCs or industrial networks, IEC 62443 zones and conduits or security levels, OT monitoring, or responding to an incident on the plant floor."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# OT / ICS Security Engineering

IT security instincts get people hurt in OT. Here **safety and availability
outrank confidentiality** (inverted CIA), uptime is measured in years, and you
cannot just patch or reboot a turbine. A vulnerability scan is itself a hazard.

Applies to plants, factories, utilities, building management: anywhere software
moves something physical. For compliance obligations use
`load_skill ot-compliance`; for actually assessing an environment use
`load_skill ot-assessment`; for adversaries and ICS malware use
`load_skill ot-threat-landscape`.

## Purdue model: the reference segmentation

- **L0** field devices (sensors/actuators) · **L1** controllers (PLC/RTU/DCS) ·
  **L2** supervisory (SCADA/HMI) · **L3** site operations/historian ·
  **L3.5 IDMZ**: the IT/OT boundary, the most important zone you will design ·
  **L4/L5** enterprise IT.
- The hard rule: **no direct L4→L1 path.** All IT/OT traffic brokered through the
  IDMZ: jump hosts, data diodes, replicated historian. If a vendor laptop, a
  cellular modem or a cloud historian punches through it, that is the finding.
- **Safety Instrumented Systems (SIS) are their own zone**, never sharing a
  network with the control system. Compromise here is a life-safety event, not an
  outage; this is exactly what TRITON/TRISIS went after.
- Purdue is a reference, not a mandate. Real plants have wireless, remote vendor
  access and cloud analytics the model never anticipated. Use it to reason about
  **where a boundary belongs**, then enforce with
  `load_skill network-segmentation`.

## IEC 62443: the engineering spine

Purdue says _how to segment_; **IEC/ISA 62443** says _what security each zone
requires_. It is a **horizontal standard** (IEC recognised it as applying across
all sectors in 2021), and it is the language plant engineers and vendors
actually negotiate in.

**The three Security Levels (the most-confused concept in OT, get this right):**

|                       | What it is                                                                                                                                           | Property of        |
| :-------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------- |
| **SL-T** (Target)     | The level a zone _needs_. Output of the **Part 3-2** risk assessment, recorded in the Cybersecurity Requirements Specification.                      | The risk decision  |
| **SL-C** (Capability) | What a system (3-3) or component (4-2) _can_ deliver natively when correctly configured, **without compensating controls**. What a vendor certifies. | The product        |
| **SL-A** (Achieved)   | What the plant _actually has_, measured after commissioning and in operation.                                                                        | The as-built plant |

**SL-C ≥ SL-T does not mean SL-A ≥ SL-T.** Misconfiguration, integration
shortcuts and process gaps live in that difference, and that gap is where your
assessment findings come from. Buying certified components proves nothing on its
own.

Levels 1 to 4 scale by adversary: **1** casual/coincidental · **2** intentional,
simple means, low resources, generic skills · **3** sophisticated means,
moderate resources, **IACS-specific** skills · **4** sophisticated means,
**extended** resources, IACS-specific skills, high motivation. **Don't
gold-plate L0 to SL4**: that is cost with no safety benefit. Set SL-T by consequence.

**The 7 Foundational Requirements** (every technical requirement in 3-3 and 4-2
hangs off these): **FR1** Identification & Authentication Control · **FR2** Use
Control · **FR3** System Integrity · **FR4** Data Confidentiality · **FR5**
Restricted Data Flow · **FR6** Timely Response to Events · **FR7** Resource
Availability.

**Which parts are actually current** (cite these, not the series in general):

- **2-1 (2024)** asset-owner security programme; fully rewritten, the ISMS
  analogue. **2-2 (2025, PAS)** security protection scheme and its rating.
  **2-4 (2023, Ed 2)** service providers. **2-3 (2015, TR)** patch management.
- **3-2 (2020)** risk assessment → zones, conduits and SL-T. **3-3 (2013)**
  system requirements; still normative despite its age, so expect its
  requirements to predate the tech in front of you.
- **4-1 (2018)** secure product development lifecycle. **4-2 (2018)** component
  requirements; the one you put in procurement ("this PLC must be SL-C 2").
- **1-1** terminology is a 2007/2009 technical spec and is showing its age.
- **ISASecure** is the certification programme (bodies must be ISO/IEC 17065
  accredited): **CSA** and **ICSA** certify components to 4-2, **SSA** systems to
  3-3, **SDLA** the supplier's development process to 4-1, and **ACSSA** the
  as-installed automation solution. https://www.isasecure.org/certification

## NIST SP 800-82 Rev 3: the US-federal flavour

**Rev 3 (Sept 2023)** retitled the guide from ICS to **OT**, widening scope to
building automation, physical access control, safety systems and IIoT. It is
**not a parallel control set**: Appendix F is an **OT Overlay on SP 800-53 Rev 5**
with tailored low/moderate/high baselines, marking controls added to and removed
from the 800-53B baselines with OT-specific tailoring. If you already run
800-53, this is the bridge: `load_skill control-frameworks`.

Two gotchas: its CSF mapping is against **CSF v1.1**, not CSF 2.0 (r3 predates
it), so don't expect Govern-function alignment. **Rev 4 is an initial public
draft** (Sept 2026, comments close 30 Nov 2026), restructured around CSF 2.0; r3
stays the citable final until r4 is.
https://csrc.nist.gov/pubs/sp/800/82/r3/final

## Constraints that change the playbook

- **Insecure-by-design protocols**: Modbus/TCP, DNP3, S7comm, EtherNet/IP,
  PROFINET: no authentication, no encryption, and you cannot fix the protocol.
  You isolate it and monitor it. OPC UA is the exception that supports real
  security, but only if signing/encryption is actually enabled, which it often
  is not.
- **Fragile devices**: an active scan can crash a PLC. Passive/OT-aware
  monitoring at L1 to L2, never a generic IT scanner. See `load_skill ot-assessment`
  before touching anything below the IDMZ.
- **Patching is not the primary control.** Vendor validation and safety-case
  re-certification mean months to years, and a quarter of ICS advisories ship
  with no patch at all. Compensating controls (segmentation, allowlisting,
  monitoring) carry the load.
- **Remote vendor access is the recurring root cause**: standing VPN accounts,
  shared credentials, and cellular gateways nobody inventoried (VOLTZITE reached
  US pipeline operations through Sierra Wireless Airlink gateways). Broker every
  session through the IDMZ, time-box it, require plant approval, record it.
- **Engineering workstations are the crown jewels**: they hold project files,
  logic and the ability to download to controllers. They run Windows, so they get
  misfiled as "IT" and swept into IT patching and IT incident response, which is
  how "IT-only" ransomware stops production.

## Incident response is different

Recovery means a **safe physical state**, not clean disks. Network isolation may
itself be unsafe: dropping a link can blind an operator mid-process. The plant
manager, not the SOC, holds shutdown authority. Keep an OT incident plan separate
from the IT one, with named engineering contacts, manual-fallback procedures, and
known-good logic/project-file backups stored offline (a controller reflash needs
the _engineering_ backup, not a VM snapshot).

Pair with `load_skill incident-response-leadership` for the command decisions and
`load_skill backup-recovery` for the restore path.

## Rules

- Segment to Purdue with a real IDMZ before buying any OT security product.
- Set **SL-T by safety consequence** first; verify **SL-A** after commissioning.
  A certificate is a claim about SL-C, not about your plant.
- **Inventory first**: most sites cannot name what sits on L1, and you can
  neither defend nor report on what you have not enumerated.
- Never run an IT playbook (scan, patch, isolate, reimage) below the IDMZ without
  the plant's sign-off. "It's just a scan" is how you stop a production line.

## Pairs with

- `load_skill ot-assessment`, `load_skill ot-threat-landscape`,
  `load_skill ot-compliance`.
- `load_skill network-segmentation`, `load_skill endpoint-security` (IT side),
  `load_skill threat-modeling` (consequence-driven analysis).
