---
name: ioc-hunter
description: Threat-intel IOC workflow — feed curation (MISP/OpenCTI/vendor/ENISA/CISA), deduplication, confidence scoring (TLP, source reputation, age, sightings), enrichment pipeline to SIEM/EDR, retro-hunt over an N-day window, and lifecycle (expiry + retirement).
---

# IOC Hunter

> **Source discipline and TLP respect**: IOCs come with a share policy (TLP-RED/AMBER/GREEN/CLEAR). Forwarding to parties the feed contract does not allow is a breach of trust and, in some contracts, of license. Sharing where permitted (intra-industry ISAC, CSIRT-NL, sector PAC) is a net-positive habit.

## When to use

IOCs (Indicators of Compromise) are the tactical layer of threat intel: hashes, IPs, domains, URLs, mutexes, certificate fingerprints, JA3/JA4 strings. This skill helps manage feeds, dedup and confidence-score them, plug them into SIEM/EDR, and retro-hunt.

Triggers on:

- A question like "add this IOC feed to our stack", "is this hash known", "retro-hunt the last 30 days against these IOCs", "how do we score IOC confidence", "set up a MISP instance".
- A handoff from `detection-engineer` (rule needs IOC input), `log-triage` or the `threat-hunt` command (enrichment of findings), `malware-triage` (extracted IOCs to be integrated).
- A new APT-campaign publication whose IOCs need processing.
- A periodic (quarterly) feed-hygiene review: which feeds deliver value, which do not.

### When NOT (handoff)

- Writing a detection rule that consumes the IOC → `detection-engineer`. This skill provides the IOC input.
- Triage of the alert that fires from an IOC match → `log-triage`.
- A threat-hunt session itself → the `threat-hunt` command.
- Malware-sample analysis that produces IOCs → `malware-triage`.
- Forensic confirmation of IOC impact → `forensics-assist`.
- Strategic CTI (actor profiles, geopolitical context) is out of scope here — that is separate CTI work, not in this skill.
- Vulnerability feed (CVEs) → `cve-triage`.

## Approach

Six phases. Phase 2 (confidence scoring) and phase 5 (retro-hunt) are where IOC work delivers operational value.

### 1. Feed curation

Which feeds deserve your SIEM bandwidth? Not all of them.

**Source categories**:

- **Government / national CERT**: CISA AIS, NCSC-NL, ENISA feeds, BSI (DE), ANSSI (FR). High-trust, sometimes delayed.
- **ISAC / sector PAC**: FI-ISAC NL for financial, MS-ISAC for government. Sector-specific relevance.
- **Commercial CTI**: Mandiant, Recorded Future, CrowdStrike Intelligence, Mandiant Advantage, IntSights/Rapid7, Group-IB. High quality, high price.
- **Open-source/community**: AlienVault OTX, abuse.ch (URLhaus, MalwareBazaar, ThreatFox), Spamhaus, Emerging Threats. Mixed quality, free or low-cost.
- **Vendor-specific threat intel**: Microsoft Security Graph, Cisco Talos, Palo Alto Unit 42 — often baked into the product license.
- **Internal sources**: your own incidents produce the highest-trust IOCs for your organization. Categorize as "internal" with a separate TTL.

**Curation criteria**:

- Coverage: does the feed cover sectors/regions that touch you?
- Freshness: how quickly after an incident does an IOC appear in the feed?
- Validity: what % of IOCs are still true-positive after 30/60/90 days?
- False-positive history: known noisy feeds (e.g. NRD feeds that flag every newly registered domain) need a separate cadence.
- Format: STIX 2.1 / OpenIOC / MISP event format / CSV. STIX is the de facto standard.

A feed that is not used for matching or retro-hunt does not deserve its ingest slot. Periodically downscale.

### 2. Deduplication and confidence scoring

One IP can show up in 5 feeds. A hash with 12 sources is not 12× more valuable than one with 1 source — but somewhat more. Confidence model:

- **Source-reputation score** per feed (kept internally based on TP-rate history). High-trust source = higher weight.
- **Age**: the older an IOC, the less relevant. Default decay: confidence halves after 30 days; after 90 days it is a retirement candidate unless there is APT context. Some IOC types age faster (IPs > domains > hashes for sustained malware).
- **Sightings**: number of times reported by different sources. Boosts confidence positively, not linearly.
- **TLP**: not so much confidence as a sharing restriction. TLP-RED = specific audience only, TLP-AMBER = limited external, TLP-GREEN = community, TLP-CLEAR = open. Sharing discipline: never upgrade TLP without source consent.
- **Type-specific**:
  - **Hashes** (SHA-256 preferred): highest precision, long life provided the hash does not change. Low false-positive risk.
  - **IPs**: short-lived in cloud context (CDN-shared, ephemeral cloud resources). Drop confidence quickly, retire after 14–30 days unless confirmed APT infrastructure.
  - **Domains**: medium life; sinkholing and takedowns accelerate retirement. Watch out for wildcard-feed noise.
  - **URLs**: short-lived, exploit-kit rotation. Retire fast.
  - **JA3/JA4 fingerprints**: TLS-handshake fingerprint, sustained as long as the malware author keeps the same TLS stack.
  - **Email addresses / sender domains**: medium life, BEC context.
  - **Mutexes**: implementation detail, sustained.
  - **Yara rules**: a pattern, not an IOC, but a functionally related layer — see `malware-triage`.

**Dedup** implementation: MISP/OpenCTI do this natively when events are merged on the same attribute. A custom stack needs its own normalization (canonical form of IPs, lowercased domains, hash-format normalization).

### 3. Storage and sharing layer

- **MISP** (open-source) — the de facto standard for threat-sharing platforms in the EU. Event-based, multi-tenant, sharing policy per event/attribute. Strong in the NL/EU community via FI-ISAC and CSIRT-NL.
- **OpenCTI** (open-source) — more modern, knowledge-graph oriented, better visualization. Imports STIX 2.1 natively.
- **Anomali ThreatStream**, **EclecticIQ**, **Recorded Future** — commercial alternatives.
- **Commercial-platform choice** is usually contractual with a CTI feed vendor. Open-source self-hosted (MISP) is feasible for medium-size orgs.

**Sharing direction**:

- **Inbound**: integrate feeds via MISP-sync, STIX/TAXII feeds, OpenCTI connectors, or API pulls.
- **Outbound**: what do you generate yourself and share back? Internal IOCs from incidents, thinly confirmed detections. NL FI-ISAC and CSIRT-NL accept contributions. Anonymize where TLP policy requires.

### 4. Enrichment pipeline to SIEM and EDR

An IOC that does not match anywhere is dead weight. Pipeline to make them active:

- **SIEM ingestion**: feeds into lookup tables (Splunk lookup files, Sentinel watchlists, Elastic enrich policies). Fresh feed = fresh lookup. Default refresh cadence hourly to daily depending on feed update tempo.
- **EDR ingestion**: native IOC modules in Microsoft Defender, CrowdStrike Falcon, SentinelOne, Carbon Black accept IOCs as a blocklist or detection trigger. Differentiate detect-only vs. auto-block per type.
- **Network tooling**: firewall blocklists (IP/domain), DNS-RPZ (recursive policy zone) for domain blocking, proxy/SWG categorization.
- **Email gateway**: sender domains, hashes for attachments. Microsoft 365 Defender, Proofpoint, Mimecast.

Enrichment discipline: not every feed in every layer. High-confidence actor feeds → block action; lower-confidence feeds → detect-only with a SIEM alert. Aggressive blocking on weak feeds is operational disruption.

### 5. Retro-hunt and lifecycle

- **Retro-hunt on new IOCs**: with each new high-confidence feed update, sweep the last N days of logs (typically 30–90 days, depending on retention and compute budget). With `siem-query` as the building block.
- **Hits triage**: a retro-hit is not a confirmed compromise — it can be benign historical traffic. Path to confirmation via `log-triage` (was the actor suspicious?) and `forensics-assist` (was there a follow-on action?).
- **IOC lifecycle**:
  - **Active**: in scoring, in lookup tables.
  - **Aging**: confidence falling, in detect-only mode.
  - **Retired**: out of active detection. Keep in archive for later retro-hunt.
  - **Re-promote**: an old IOC reappears in a new feed or incident → re-activated with fresh confidence.
- **Expiry discipline**: feed IOCs have a default TTL from the feed policy. Internal IOCs use a manual expiry (default 90 days, revisable).

### 6. Verification-loop

Layer 1: scope (feed curation up to date, no feeds nobody reads anymore?), assumptions (IOC source-reputation scoring based on data, not gut feel?), gaps (TLP policy respected on sharing-out, retro-hunt cadence on new high-conf feeds?). Layer 2: feed sources alive (multiple CTI vendors merge or shut down — verify URLs and API status), TLP classification correct (TLP 2.0 since 2022, the old TLP-AMBER+STRICT no longer exists as such), STIX version consistent (STIX 2.1 default in 2024+).

## Output

Two modes: feed management (in advance, living) and a hunt report (after a retro-hunt or investigation).

**Feed-management mode**:

```
IOC feed inventory
Date: YYYY-MM-DD | Reviewer: <name>

Active feeds:
  Name | Category | Format | Update cadence | Source reputation | TLP policy

Per feed:
  Coverage:           <regions, sectors>
  Freshness:          <average delay between incident and publication>
  Validity rate:      <% TPs after 30/60/90 days>
  TP-rate trend:      <stable / falling / rising>
  Decision:           <retain / downgrade / replace / drop>

Sharing-out:
  Internal IOCs generated: <N>
  Shared via: <FI-ISAC NL / MISP-sync / CSIRT-NL>
  TLP classification: <per IOC>

Coverage gaps:
  <which threat clusters not covered by current feeds>
```

**Hunt report** (after retro-hunt on a new IOC set):

```
IOC retro-hunt — <feed update / campaign name>
Window: last N days | Date: YYYY-MM-DD

Input IOCs:
  Hashes: N | IPs: N | Domains: N | URLs: N | JA3/JA4: N

Hits per type:
  Hash:    N (true-positive: M, false-positive: K, pending triage: L)
  IP:      N (...)
  Domain:  N (...)
  URL:     N (...)

Confirmed sightings:
  - <IOC + match context + system + timestamp + handoff>

Pending triage:
  - <IOC + reason for uncertainty + next step>

Handoffs:
  ir-runbook:         <if confirmed compromise>
  log-triage:         <pending-triage depth>
  detection-engineer: <if IOCs basis for a new rule>
  forensics-assist:   <if post-incident investigation needed>

Verification-loop: ...
```

## References

- **MISP** — [https://www.misp-project.org/](https://www.misp-project.org/). De facto threat-sharing platform, open-source, widely used in EU/NL.
- **OpenCTI** — [https://www.opencti.io/](https://www.opencti.io/). Modern threat-intel platform with a knowledge graph.
- **STIX 2.1** — [https://oasis-open.github.io/cti-documentation/](https://oasis-open.github.io/cti-documentation/). Structured Threat Information Expression standard.
- **TAXII 2.1** — [https://oasis-open.github.io/cti-documentation/taxii/intro](https://oasis-open.github.io/cti-documentation/taxii/intro). Transport mechanism for STIX.
- **TLP 2.0** — [https://www.first.org/tlp/](https://www.first.org/tlp/). Traffic Light Protocol, FIRST-maintained.
- **abuse.ch** (URLhaus, MalwareBazaar, ThreatFox) — [https://abuse.ch/](https://abuse.ch/). Open-source IOC feeds.
- **AlienVault OTX** — [https://otx.alienvault.com/](https://otx.alienvault.com/). Community pulse-based feeds.
- **CISA AIS** — [https://www.cisa.gov/topics/cyber-threats-and-advisories/information-sharing/automated-indicator-sharing-ais](https://www.cisa.gov/topics/cyber-threats-and-advisories/information-sharing/automated-indicator-sharing-ais).
- **NCSC-NL Threat Intel** — [https://www.ncsc.nl/](https://www.ncsc.nl/).
- **MITRE ATT&CK** — [https://attack.mitre.org/](https://attack.mitre.org/). For mapping IOCs to TTPs.

## Categories

- blue
