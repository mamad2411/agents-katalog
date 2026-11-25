---
name: ransomware-response
description: Provides an end-to-end ransomware incident playbook covering scoping encryption vs exfiltration, isolating without losing evidence, identifying the strain and finding a decryptor, watching the leak site, restoring clean-room in known-good order, and making the payment decision with its legal duties (OFAC, Australia, NYDFS, CIRCIA, UK). Use when the user faces an active or suspected ransomware incident, an extortion demand, or is preparing a ransomware response plan.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Ransomware response

Defensive/IR playbook. A ransomware case is **two incidents at once**: **availability**
(encryption, outage) and usually **confidentiality** (exfiltration, double extortion), so run
two workstreams with separate evidence. Lifecycle: `load_skill incident-response`; commander's
calls: `load_skill incident-response-leadership`; business crisis: `load_skill crisis-management`.
The legal parts are practitioner orientation, not legal advice; counsel owns them.

## First hour (in this order)

1. **Declare Sev 1, go out-of-band.** Assume the actor reads email/chat and the IR channel.
2. **Stop the spread, keep the evidence.** Network-isolate (EDR/switchport/VLAN); don't power
   off, since RAM holds keys and live C2. Power down only a host you can't disconnect that is
   still encrypting. verify: https://www.cisa.gov/stopransomware/ransomware-guide
3. **Save the backups first.** Cut the backup console off from prod identity, rotate its admin
   creds out-of-band, check for retention/immutability changes and deleted jobs, and snapshot
   what survives. `load_skill backup-recovery`.
4. **Identity:** disable (don't delete) compromised accounts, kill sessions/tokens, block C2 and
   exfil paths (rclone/MEGA egress). Hold the krbtgt double reset until you can hold the line.
5. **Export short-retention telemetry now** (EDR is often 7 to 30 days; also firewall/VPN, cloud
   audit). Keep the ransom note, encrypted samples and a patient-zero memory image, hashed,
   with chain of custody. Don't reimage patient zero before capture.
6. **Call counsel first** (engage the IR firm through counsel for privilege), then the
   **insurer** (notice clause; panel vendors only, or cover can be lost), then law enforcement.
7. **Start the notification matrix:** awareness is today. `load_skill breach-notification-matrix`.

## Scope: encryption vs exfiltration (answer both, separately)

| Question             | Evidence to pull                                                                                          | Why it matters                                                               |
| -------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| What is encrypted?   | Host list, hypervisors (ESXi/vCenter takes whole estates), NAS, backups, cloud storage                    | Recovery size; whether restore beats MTPD (`load_skill business-continuity`) |
| Was data taken?      | rclone/WinSCP/restic artifacts, 7z/RAR staging, egress spikes in NetFlow, cloud API reads, leak-site post | Turns an outage into a breach: GDPR Art. 34, state laws, HIPAA               |
| How did they get in? | Edge device CVE (check KEV), VPN creds without MFA, phishing loader, RMM abuse, third-party access        | Close it before restore or you get re-encrypted                              |
| When?                | Earliest attacker activity, not detonation time                                                           | Sets the clean restore point (dwell is often weeks)                          |
| Still inside?        | New accounts, GPO changes, RMM tools (AnyDesk/ScreenConnect), scheduled tasks, cloud app consents         | Decides when eradication and reconnection are safe                           |

- **Missing logs are not evidence of no exfiltration.** Regulators ask what you could see.
- Encryption-only still counts: it is a GDPR breach (availability) and a presumed HIPAA breach
  unless a low-probability-of-compromise assessment shows otherwise. Data-theft-only extortion
  (no encryption) is common now; run the same playbook without the restore.

## Identify the strain and check for a decryptor

- Fingerprint: note filename/text, encrypted extension, Tor chat URL or TOX ID, leak-site
  brand. Triage the binary on a copy: hash, YARA, capa, rabin2
  (`load_skill malware-triage`). Map TTPs to an actor (`load_skill actor-ttp-attribution`):
  that drives the sanctions check. **Brand ≠ actor**: affiliates move between RaaS programmes
  and sanctioned groups rebrand, so check the infrastructure and the wallet, not the name.
- **No More Ransom** (Europol-led): Crypto Sheriff identifies the strain from a note + sample
  and lists free decryptors. verify: https://www.nomoreransom.org/ . ID Ransomware does the
  same, but uploading is disclosure: send the note, not a sensitive file. Ask LE too:
  takedowns (e.g. LockBit, Operation Cronos 2024) have yielded keys before any public tool.
- **Test any decryptor (free or paid) on copies**, never in place; actor decryptors are slow
  and buggy on large VM disks. Keep the encrypted copies in case a decryptor appears later.

## Leak-site and extortion watch

- Track the group's leak site through TI feeds/trackers or an isolated research VM over Tor,
  never from a corporate browser. `load_skill ti-research`, `load_skill ioc-pivoting`.
- Record post time, countdown and every sample file: samples are your best evidence of
  **what** was taken. They can be recycled from an older breach, so verify them, but the
  regulatory clock keeps running. Never say "no data taken" publicly before you know.
- Expect pressure on others (calls to customers and staff, DDoS, harassment of executives).
  Brief the service desk and comms. Downloading the leaked set is a counsel decision; if
  approved, work in an isolated enclave. It is the best input for who must be notified.

## Clean-room restore (known-good order)

Never restore into the compromised environment. Build an isolated recovery environment
(new network segment, clean admin workstations, EDR on everything brought up), then:

1. **Identity plane:** AD forest recovery from a pre-compromise DC backup (or a rebuild);
   krbtgt reset twice with replication in between; all privileged/service accounts reset.
   Cloud IdP: review federation trusts, app registrations, conditional-access changes.
2. **Core services:** DNS/DHCP, PKI (re-issue if the CA was touched), the backup platform itself.
3. **Critical business apps** in BIA/RTO order, minimum viable first (`load_skill disaster-recovery`).
4. **Endpoints/servers:** reimage from golden images and restore **data**, not system state.

- Pick a recovery point **before initial access**, not before detonation. Mount and scan
  backups for the case's IOCs/persistence (YARA) before restoring.
- Reconnect only when the entry vector is closed and eradication exit criteria are met
  (hunt clean: `load_skill threat-hunting`). Getting hit again soon after is common.

## The payment decision

The board/exec decides with counsel and the insurer, not the IR lead. Any actor contact
goes through a specialist negotiator (often from the insurer's panel), never ad hoc staff.

- **Primary question:** can we restore within MTPD without paying? If yes, payment buys only a
  deletion promise you cannot enforce ("deleted" sets resurface). If it buys a decryptor, demand proof of
  decryption on sample files and keep recovery and eradication running in parallel.
- Payment marks you for re-targeting. Document alternatives considered and the legal
  analysis; regulators, the insurer and the board will read this record.

| Regime                                     | Who                                                                       | Duty                                                                                                                                                                                                                                                                                                                                           | Status (Nov 2026)                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------------------------------------ | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **US OFAC**                                | US persons, and anyone causing a US person to violate                     | Strict liability for paying an SDN or a comprehensively sanctioned jurisdiction. Licence requests face a presumption of denial. A prompt, complete report to LE/CISA counts as voluntary self-disclosure and a significant mitigating factor, as do strong security controls. Banks facilitating the payment file SARs (FinCEN FIN-2021-A004). | **21 Sep 2021 advisory is still current.** verify: https://ofac.treasury.gov/media/48301/download?inline=                                                                                                                                                                                                                                                                                                        |
| **UK OFSI / AU DFAT**                      | Anyone paying                                                             | Trilateral US/UK/AU designations (LockBit leadership 2024, Evil Corp Oct 2024) make paying these actors an offence                                                                                                                                                                                                                             | Live; screen the actor and wallet                                                                                                                                                                                                                                                                                                                                                                                |
| **Australia** Cyber Security Act 2024 Pt 3 | Turnover ≥ AUD 3M, or a SOCI responsible entity                           | Report the payment to ASD within **72h** of paying (or of learning it was paid on your behalf). No payment, no report. Civil penalty 60 penalty units.                                                                                                                                                                                         | In force 30 May 2025. Phase 2 "compliance and education" since 1 Jan 2026; a 2026 review will decide when active enforcement starts. verify: https://www.cyber.gov.au/report-and-recover/report/ransomware-payment-and-cyber-extortion-payment-reporting                                                                                                                                                         |
| **NYDFS** 500.17(c)                        | NY DFS licensees                                                          | Notice within **24h** of an extortion payment. Within 30 days, a written explanation of why payment was needed, alternatives considered and sanctions diligence.                                                                                                                                                                               | Live (`load_skill us-sectoral-regs`)                                                                                                                                                                                                                                                                                                                                                                             |
| **CIRCIA**                                 | Covered critical-infrastructure entities                                  | Ransom-payment report to CISA within **24h** (72h for covered incidents)                                                                                                                                                                                                                                                                       | **Not in force.** The final rule went to OIRA on 1 Oct 2026; text not public; effective ≥60 days after publication. Until then, voluntary reports to CISA/FBI. verify: https://www.cisa.gov/topics/cyber-threats-and-advisories/information-sharing/cyber-incident-reporting-critical-infrastructure-act-2022-circia                                                                                             |
| **UK** Home Office proposals               | Public sector and regulated CNI (ban); everyone else (pre-payment notice) | Targeted payment ban; a payment-prevention regime (notify intent, Home Office may block); mandatory reporting in 72h                                                                                                                                                                                                                           | **Not law.** The Jul 2025 consultation response committed to all three, but the ban was left out of the 2026 King's Speech. The Cyber Security and Resilience (NIS) Bill (24h/72h incident reporting for regulated entities) was still in Parliament in early Nov 2026. verify: https://www.gov.uk/government/consultations/ransomware-proposals-to-increase-incident-reporting-and-reduce-payments-to-criminals |
| **EU**                                     | NIS2/DORA entities                                                        | No payment-report duty yet; the incident itself runs the NIS2/DORA/GDPR clocks                                                                                                                                                                                                                                                                 | The Jan 2026 NIS2 amendment proposal would add payment reporting (`load_skill nis2-dora`)                                                                                                                                                                                                                                                                                                                        |
| **US states**                              | Public bodies in some states (e.g. North Carolina, Florida)               | Statutory bans on paying with public funds                                                                                                                                                                                                                                                                                                     | verify per state                                                                                                                                                                                                                                                                                                                                                                                                 |

- **Insurer:** get written consent before engaging vendors and before paying. Check the
  extortion sublimit, the war exclusion and control warranties (`load_skill legal-contractual`).
  For UK decisions, see the NCSC guidance written with ABI/BIBA/IUA (2023).
- **Law enforcement** (FBI field office/IC3, CISA, NCA/NCSC, ASD ReportCyber) can bring keys
  from takedowns, wallet tracing, actor intel and the OFAC mitigation credit. LE won't run
  your recovery and won't normally ask you to stop restoring.
- Paying never removes a notification duty; the data was still accessed.

## Close-out

`report_finding` each confirmed TTP (ATT&CK id), the entry vector and every control gap
(unprotected backup path, edge device without MFA, missed restore RTO), then run `render_report`.
Feed the gaps into `load_skill risk-assessment` and `load_skill detection-engineering`.
