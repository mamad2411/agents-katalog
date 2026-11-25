---
name: finding-control-crosswalk
description: Maps a concrete security finding (default credentials, missing MFA, unpatched known-exploited CVE, cleartext protocols, flat IT/OT network, missing logging, insecure remote access, no SBOM, no secure updates, no disclosure process, missing backups, injection/XSS, exposed services) to the regulatory and OT obligations it touches - IEC 62443-3-3 SRs, EU CRA Annex I and NIS2 Art. 21(2) - plus ISO 27001 Annex A. Use when writing up a pentest or OT-assessment finding for a manufacturer or NIS2 entity and the report must say which obligation it breaches, or when building the evidence chain finding to control to report.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Finding → obligation crosswalk (IEC 62443-3-3, CRA, NIS2)

Takes one finding and names the obligations it is evidence against, so the report
reads "this breaches X" instead of "this is bad". For framework↔framework mapping
(ISO ↔ NIST CSF/800-53 ↔ SOC 2 ↔ CIS) use `load_skill control-mapping`; this skill
is the regulatory/OT leg of the same evidence chain.

## Who the obligation binds (decide first)

| Where the finding lives                                       | Primary regime                                                      |
| ------------------------------------------------------------- | ------------------------------------------------------------------- |
| In a **product** you make and place on the EU market          | **CRA** (manufacturer): Annex I Part I = product, Part II = process |
| In the **plant / IT estate** of an essential/important entity | **NIS2** Art. 21(2) (operator)                                      |
| In an **IACS** (the control system as integrated)             | **IEC 62443-3-3** SRs (system capability, per zone/conduit SL-T)    |
| Anywhere in ISMS scope                                        | **ISO/IEC 27001:2022** Annex A                                      |

Don't cite CRA for a misconfigured PLC in a customer plant; that's NIS2 + 62443-3-3.
Cite CRA when the same weakness ships _in the product by default_ (e.g. a hard-coded
password in your firmware). A manufacturer is often both: map both columns, say which.

## Crosswalk

IDs only; read the source text before quoting obligations in a deliverable.
CRA = Annex I Part I point (2)(x) or Part II point (n). NIS2 = Art. 21(2)(x).
"None" means no direct hit; don't stretch one.

| Finding class (CWE pivot)                                        | IEC 62443-3-3 SR (FR)                                                                                                                                                  | CRA Annex I                             | NIS2 Art. 21(2) | ISO 27001:2022 Annex A |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | --------------- | ---------------------- |
| Default / weak / hard-coded credentials (CWE-1392, 521, 798)     | SR 1.5 Authenticator management, SR 1.7 Strength of password-based authentication (FR 1)                                                                               | Part I (2)(b), (2)(d)                   | (i), (g)        | A.5.17, A.8.5          |
| Missing MFA on remote / privileged access (CWE-308)              | SR 1.1 Human user identification and authentication, SR 1.13 Access via untrusted networks (FR 1) ¹                                                                    | Part I (2)(d)                           | (j)             | A.8.5                  |
| Unpatched known-exploited vuln (KEV) (CWE-1395 / CVE)            | None (patch management is IEC 62443-2-3, not a 3-3 SR) ²                                                                                                               | Part I (2)(a), (2)(c); Part II (2), (8) | (e)             | A.8.8                  |
| Cleartext / insecure protocols (CWE-319, 311)                    | SR 3.1 Communication integrity (FR 3); SR 4.1 Information confidentiality, SR 4.3 Use of cryptography (FR 4)                                                           | Part I (2)(e), (2)(f)                   | (h)             | A.8.24, A.8.20         |
| Missing IT/OT segmentation, flat network (CWE-668)               | SR 5.1 Network segmentation, SR 5.2 Zone boundary protection (FR 5)                                                                                                    | Part I (2)(j) (product interfaces only) | (a), (e) ³      | A.8.22, A.8.20         |
| Excessive privileges / broken access control (CWE-269, 639)      | SR 1.3 Account management (FR 1); SR 2.1 Authorization enforcement (FR 2)                                                                                              | Part I (2)(d)                           | (i)             | A.5.15, A.5.18, A.8.2  |
| Missing logging / monitoring (CWE-778)                           | SR 2.8 Auditable events, SR 2.11 Timestamps (FR 2); SR 3.9 Protection of audit information (FR 3); SR 6.1 Audit log accessibility, SR 6.2 Continuous monitoring (FR 6) | Part I (2)(l)                           | (b), (f)        | A.8.15, A.8.16         |
| Insecure remote access (vendor VPN, exposed RDP/VNC, TeamViewer) | SR 1.13 Access via untrusted networks (FR 1); SR 2.6 Remote session termination (FR 2); SR 5.2 Zone boundary protection (FR 5)                                         | Part I (2)(d), (2)(j)                   | (d), (i), (j)   | A.6.7, A.8.5, A.8.20   |
| Vulnerable third-party component / no SBOM (CWE-1104, 1395)      | SR 7.8 Control system component inventory (FR 7) ⁴                                                                                                                     | Part I (2)(a); Part II (1), (6)         | (d), (e)        | A.5.21, A.8.8, A.5.9   |
| No secure / authenticated update mechanism (CWE-494)             | SR 3.4 Software and information integrity (FR 3)                                                                                                                       | Part I (2)(c), (2)(f); Part II (7)      | (e)             | A.8.19, A.8.32         |
| No vulnerability-disclosure process / contact                    | None (product-supplier process: IEC 62443-4-1, not 3-3) ²                                                                                                              | Part II (4), (5), (6)                   | (e)             | A.5.24 ⁵               |
| Missing / untested backups and recovery                          | SR 7.3 Control system backup, SR 7.4 Control system recovery and reconstitution (FR 7)                                                                                 | Part I (2)(h)                           | (c)             | A.8.13, A.5.30         |
| Injection / XSS / SSTI / SSRF web flaws (CWE-79, 89, 1336, 918)  | SR 3.5 Input validation (FR 3)                                                                                                                                         | Part I (2)(a), (2)(f); Part II (3)      | (e)             | A.8.26, A.8.28, A.8.29 |
| Exposed services / unnecessary attack surface (CWE-1188)         | SR 7.7 Least functionality, SR 7.6 Network and security configuration settings (FR 7); SR 5.2 Zone boundary protection (FR 5)                                          | Part I (2)(b), (2)(j)                   | (a), (g)        | A.8.9, A.8.20, A.8.21  |

Notes:

1. MFA in 62443-3-3 is a _requirement enhancement_ of SR 1.1 / SR 1.13 at higher
   security levels; confirm the RE number and target SL in the full text; the
   finding's severity depends on the zone's SL-T, not on "MFA missing" alone.
2. 62443-3-3 specifies system _capabilities_. Process gaps (patching, PSIRT/CVD) belong
   to other parts of the series; name the part, don't force a 3-3 SR.
3. NIS2 Art. 21(2) has no explicit segmentation point; it lands under (a) risk analysis
   and information system security / (e) network and information systems security. Say
   "indirect" in the report. Commission Implementing Regulation (EU) 2024/2690
   (https://eur-lex.europa.eu/eli/reg_impl/2024/2690/oj/eng) is more
   specific for the digital-infrastructure entities it covers; check it applies.
4. SR 7.8 is an inventory capability, not an SBOM. Use it for "operator can't tell what
   firmware/library is deployed"; the SBOM obligation itself is CRA Part II (1).
5. A.5.24 is incident-management planning; ISO 27001 has no dedicated CVD control;
   mark the ISO cell as partial.

CRA Part I (2)(g) data minimisation, (2)(i) impact on other networks, (2)(k)
exploitation mitigation and (2)(m) secure data removal have no row above; use them
when the finding is literally that (e.g. no factory-reset wipe → (2)(m); no ASLR/DEP/stack
canaries in firmware → (2)(k)).

## Workflow

1. `report_finding` as usual: CWE + CVSS 3.1 vector (it computes the score; your
   explicit severity wins). Pick the row by CWE/intent, not by keyword; a finding can
   hit two rows; map both.
2. Decide the regime column(s) from the table above (product → CRA, plant → NIS2,
   IACS → 62443-3-3). Drop columns that don't apply rather than leaving them empty.
3. Put the mapping in the finding itself so it survives into `render_report`:
   - `references` (one string): `IEC 62443-3-3 SR 5.1; CRA Annex I Part I (2)(j);
NIS2 Art. 21(2)(e); ISO/IEC 27001:2022 A.8.22` plus the CVE/KEV link (CWE goes
     in its own `cwe` field).
   - `recommendation`: name the obligation the fix restores, in plain words ("enforce
     zone boundary protection between L3 and L2 to meet IEC 62443-3-3 SR 5.2 at SL-T 2").
4. `render_report` → `findings.md` carries the references; `findings.csv` does not, so
   cite obligations from the `.md` (or the recommendation text). For a roll-up, count distinct obligations
   touched per regime ("12 findings, touching 7 of 51 62443-3-3 SRs, CRA Part I
   (2)(a)/(b)/(d), NIS2 (e)/(i)/(j)"), which is what a CISO or notified body reads.
5. Hand off: gaps across a whole programme (not one finding) → `load_skill gap-analysis`;
   the same finding across ISO/NIST/SOC 2/CIS → `load_skill control-mapping`.

## Rules

- Never cite an identifier you haven't read in the source. The standard texts move
  (62443-3-3 is under revision; CRA has delegated/implementing acts and harmonised
  standards pending): re-check before a formal deliverable.
- A mapped obligation is not proof of non-compliance. One finding is evidence of a gap
  against a requirement; compliance is judged on the whole system or product at its
  target SL / risk assessment. Write "evidence against", not "non-compliant".
- CRA obligations attach to products placed on the EU market (main obligations from
  11 Dec 2027, reporting from 11 Sep 2026); NIS2 attaches to in-scope entities via
  national transposition; check the national law for the exact wording.
- OT severity: weight by consequence (safety, production loss), not CVSS alone:
  `load_skill ot-assessment`.

## Load for depth

- `load_skill ot-compliance`: IEC 62443 series (zones/conduits, SL-T, 2-1/2-3/3-3/4-1/4-2).
- `load_skill eu-cra`: CRA scope, product classes, conformity assessment, reporting.
- `load_skill nis2-dora`: NIS2 entities, Art. 21 measures, Art. 23 reporting clock.
- `load_skill iso27001`: Annex A and the ISMS around it.
- `load_skill control-mapping`: framework↔framework (ISO, NIST CSF/800-53, SOC 2, CIS).

## Sources

- IEC 62443-3-3:2013 Ed. 1.0, SR/FR titles from the publisher's free table-of-contents
  preview: https://webstore.iec.ch/en/publication/7033
- Regulation (EU) 2024/2847 (CRA), Annex I: https://eur-lex.europa.eu/eli/reg/2024/2847/oj
- Directive (EU) 2022/2555 (NIS2), Art. 21(2): https://eur-lex.europa.eu/eli/dir/2022/2555/oj
- ISO/IEC 27001:2022 Annex A control titles: secondary listing (ISO text is paywalled);
  confirm against your licensed copy.
