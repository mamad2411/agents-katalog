---
name: ot-threat-landscape
description: Covers OT/ICS adversaries and malware, including the ICS Cyber Kill Chain, MITRE ATT&CK for ICS, named ICS malware families (Stuxnet, Industroyer, TRITON, PIPEDREAM and others), Dragos threat groups, why ransomware is the real plant risk, and why CVSS fails for ICS. Use when the user asks about threats to industrial systems, ICS-targeting actors or malware, or how to rate OT vulnerabilities.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# OT / ICS threat landscape

Two things separate OT threat intel from IT threat intel: the adversary needs
**process knowledge**, not just access; and the outcome is measured in physical
effect, not data loss. Engineering context: `load_skill ot-ics`.

## ICS Cyber Kill Chain: the model that explains rarity

SANS (Assante & Lee, 2015) split the intrusion into two stages:

- **Stage 1: IT intrusion / espionage.** Planning (recon) → Preparation →
  Intrusion → Management & Enablement (C2) → Sustainment, Entrenchment,
  Development & Execution. Ends with a foothold and a route toward the
  industrial network. Looks like any enterprise breach.
- **Stage 2: the ICS attack.** Planning → **Validation** → ICS Attack.
  **Validation is the bottleneck**: the adversary must test the capability on an
  identical or near-identical rig, because getting it wrong in production means
  failing loudly. Building that replica is expensive and slow.

Two consequences for defenders. Most "OT incidents" never leave Stage 1, which
is why they get misfiled as IT. And when intel says a group has **reached Stage
2**, that is a qualitative escalation, not an increment: someone has invested in
learning your process.

Note that Stage 1 can be skipped entirely where an ICS device is directly
internet-exposed, or where the adversary arrives through a compromised vendor.

## ATT&CK for ICS: a separate matrix

Twelve tactics. Two of them have no Enterprise equivalent at all:

Initial Access · Execution · Persistence · Privilege Escalation · Evasion ·
Discovery · Lateral Movement · Collection · Command and Control · **Inhibit
Response Function (TA0107)** · **Impair Process Control (TA0106)** · Impact
(TA0105: Enterprise has its own Impact, TA0040; the ICS matrix just numbers it
differently).

**Inhibit Response Function** is the safety-system-blinding tactic: preventing
alarms, protection relays or the SIS from doing their job. **Impair Process
Control** is manipulating the process itself. Detection engineering that only
covers Enterprise tactics is blind to both: map OT rules against the ICS
matrix explicitly (`load_skill detection-engineering`).
https://attack.mitre.org/matrices/ics/

## Named ICS malware: small list, heavy consequences

Fewer than a dozen families have ever reached Stage 2. Knowing them matters
because they define what is demonstrably possible:

- **Stuxnet** (2010): damaged uranium-enrichment centrifuges via Siemens S7
  PLCs. The proof that code can break machines.
- **Havex** (2014): RAT with an OPC scanning module; espionage/mapping.
- **BlackEnergy2/3** (2015): enabled the Ukraine grid outage; operators
  switched breakers manually via stolen HMI access.
- **Industroyer / CrashOverride** (2016): first malware that _natively speaks
  grid protocols_ (IEC 60870-5-101/104, IEC 61850, OPC DA). Ukraine substation.
- **TRITON / TRISIS** (2017): **targeted a Triconex safety instrumented
  system**. The first malware aimed squarely at defeating a safety function, and
  the reason SIS network isolation is non-negotiable.
- **EKANS / Snake** (2020): ransomware carrying an ICS-process kill list; the
  hinge point where crimeware started caring about OT.
- **Industroyer2** (2022): retooled Industroyer against a Ukrainian substation.
- **PIPEDREAM / INCONTROLLER** (2022, Dragos: CHERNOVITE): a **modular ICS
  attack framework** (Schneider, Omron, OPC UA) discovered _before_ deployment.
  Reusable capability rather than a one-target weapon.
- **FrostyGoop** (2024): used **Modbus TCP** directly to disrupt heating to
  civilian buildings in Ukraine. Notable for needing no OT-specific implant.
- **Fuxnet** (2024): the Ukraine-aligned Blackjack group's malware against
  Moscow's Moscollector sensor network: bricked sensor gateways and flooded their
  Meter-Bus serial links.
- **IOCONTROL** (2024, CyberAv3ngers): Linux implant for IoT/OT devices (PLCs,
  HMIs, routers, fuel-management systems); in ATT&CK for ICS since v20.
- **ZionSiphon** (2026): Israeli water/desalination-themed, but Dragos assessed
  it **not a credible ICS threat** (broken, likely LLM-generated logic). A name in
  the news is not a capability.

## Threat groups: OT naming is its own namespace

Dragos names OT-focused activity groups separately from CrowdStrike/Mandiant
naming, so the same operators appear under different labels. Treat any name as a
hypothesis and lead with TTPs (`load_skill actor-ttp-attribution`).

As of the **2026 Year in Review** (published Feb 2026, covering 2025), Dragos
tracks **26 groups, 11 active during 2025**, including three new ones:

- **VOLTZITE** (overlaps Volt Typhoon): **elevated to Stage 2**; compromised
  Sierra Wireless Airlink cellular gateways to reach US midstream pipeline
  operations, then manipulated engineering-workstation software to extract
  configuration and alarm data, specifically studying what conditions trigger a
  process shutdown. Living-off-the-land, prepositioning rather than disruption.
- **SYLVANITE** _(new)_: initial-access broker that hands footholds to
  VOLTZITE; observed at US electric and water utilities exploiting Ivanti
  vulnerabilities and extracting AD credentials.
- **AZURITE** _(new, overlaps Flax Typhoon)_: long-term access and **OT data
  theft**: network diagrams, alarm data, process information exfiltrated from
  engineering workstations for later capability development. Manufacturing,
  defence, automotive, energy across US/EU/APAC.
- **PYROXENE** _(new)_: supply-chain compromise and social engineering into OT;
  aviation, aerospace, defence, maritime.
- **ELECTRUM** (overlaps Sandworm): destructive operations and wipers; in Dec
  2025 targeted combined-heat-and-power and renewable-energy management in
  Poland, expanding from transmission to the decentralised grid.
- **KAMACITE**: the access enabler for ELECTRUM; ran sustained reconnaissance of
  US industrial devices Mar to Jul 2025, systematically scanning **entire control
  loops**: HMIs, variable-frequency drives, metering modules, cellular gateways.
- **BAUXITE** (overlaps CyberAv3ngers): hacktivist-presenting, deployed wipers
  in 2025. Representative of the broader shift: hacktivists hitting
  **internet-exposed HMIs, misconfigured engineering workstations and open
  Modbus/TCP and DNP3**, which needs no sophistication at all.

## The unglamorous reality: ransomware

The exotic families get the conference talks; **ransomware causes the outages**.
Per the 2026 report: **119 ransomware groups** targeting industrial organisations
in 2025 (up from 80), **~3,300 organisations** affected, and **manufacturing was
more than two-thirds of all victims**. (Cite those counts rather than a growth
rate: the report's own summary and body quote different year-on-year figures,
49% and 64%.)

Average dwell time in OT environments was **42 days**, but organisations with
comprehensive OT visibility detected and contained in about **5 days**. Visibility
is the variable that moves.

The recurring misdiagnosis: engineering workstations and HMIs run Windows, so
they get classified as IT, so an OT incident gets reported as "IT only" and
recovered with IT procedures. That is how a plant loses days
(`load_skill ot-ics` for why recovery differs).

## Why CVSS fails here

In 2025 Dragos assessed that **25% of ICS-CERT/NVD advisories carried incorrect
CVSS scores**, **26% shipped with no patch or mitigation from the vendor**, and
only **2%** warranted immediate action under a "Now / Next / Never" triage.

So: do not rank OT vulnerabilities by CVSS. Rank by **reachability and process
consequence**, and expect the vendor fix not to exist, which makes the decision
a compensating-control decision, not a patch decision. This compounds the general
collapse in NVD enrichment covered in `load_skill vulnerability-prioritization`.

## Report

- Record which **kill-chain stage** the evidence actually supports. "Stage 1
  foothold on the engineering workstation" and "Stage 2 capability validated" are
  different findings with different urgency.
- Map to **ATT&CK for ICS** technique IDs, not Enterprise ones, and say which
  matrix you used.
- Cite the process consequence in `report_finding`; hand infrastructure pivots to
  `load_skill ioc-pivoting`.

## Pairs with

- `load_skill ot-ics`, `load_skill ot-assessment`, `load_skill ot-compliance`.
- `load_skill actor-ttp-attribution`, `load_skill threat-hunting`,
  `load_skill detection-engineering`.
