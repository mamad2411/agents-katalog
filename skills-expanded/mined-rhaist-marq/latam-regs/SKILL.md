---
name: latam-regs
description: "Covers Latin American cyber and data-protection law for security and GRC teams responsible for an entity in the region, at group HQ or locally: Brazil (LGPD, ANPD Res. 15/2024, SCCs, ANEEL REN 964), Chile (Ley 21.663/ANCI, Decreto 295, Ley 21.719), Mexico (LFPDPPP), Colombia (Ley 1581/SIC), Argentina (Ley 25.326/AAIP) and Peru (Ley 29733, DS 016-2024-JUS), with every breach clock, transfer rule and OT angle in one place. Use when the user has entities, sites, mines or offices in Brazil, Chile, Mexico, Colombia, Argentina or Peru, or asks about LGPD, ANPD, ANCI, OIV, Ley 21.719, LFPDPPP, Ley 1581, Ley 25.326 or Ley 29733."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# LATAM cyber & privacy law (practitioner orientation, NOT legal advice)

Written for security and GRC teams responsible for an entity in the region, whether at group HQ or the local entity itself. The laws are enacted in Spanish or Portuguese, so check the original: English versions and summaries are aids.

Latin America has no regional regime: six countries, six laws. The pattern across the region is that **privacy law carries the clocks everywhere, and a binding cyber regime exists mainly in Chile**. One escalation playbook plus a short list of country exceptions works better than six country playbooks. Statuses below are marked V (official text read), S (official site via search summary) or U (unverified); dates checked Nov 2026, so re-verify before advising. Counsel in each country decides what binds a given entity.

## Does it reach this entity?

- **Privacy law reaches every site** that processes personal data of staff, customers or contractors, including OT sites (badge systems, CCTV, shift data). No industry carve-out.
- **Cyber law mostly arrives by designation.** Chile's Ley 21.663 binds institutions qualified as essential-service providers or OIVs (operators of vital importance). A mining or energy subsidiary may be one; qualification is by ANCI. Ask each local entity in writing: has any regulator designated us?
- **Sector rules** touch OT in Brazil's power sector (ANEEL REN 964/2021, U against official text). No general localisation rule was found in any of the six countries.
- **Mexico and Brazil have no general cyber law** (Brazil's Decree 11.856/2023 is policy only; Mexico's federal policy binds federal administration only, secondary source).

## Clocks (the table to keep)

| Country   | Regime                     | Clock                                                                                                                                       | Recipient                                          | Status                  |
| --------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ----------------------- |
| Brazil    | LGPD, Res. CD/ANPD 15/2024 | **3 business days** from knowing personal data was affected; 20 business days to complete                                                   | ANPD and data subjects (doubled for small agents)  | V                       |
| Chile     | Decreto 295 (Ley 21.663)   | Alert **3h**; second report **72h** (**24h** only for an OIV whose essential service is hit); plan **7 days (OIV only)**; final **15 days** | CSIRT Nacional (ANCI), 24/7 platform               | V                       |
| Chile     | Ley 21.719 art. 14 sexies  | Without undue delay, no fixed hours (from 1 Dec 2026)                                                                                       | Data Protection Agency; data subjects in set cases | V                       |
| Mexico    | LFPDPPP art. 19            | **Immediately** to data subjects when property or moral rights are significantly affected; **no authority clock**                           | Data subjects                                      | V                       |
| Peru      | DS 016-2024-JUS art. 34    | **48h**, only for serious incidents (large volumes, many subjects, sensitive data, evident prejudice)                                       | ANPD; digital incidents also to the CNSD           | S                       |
| Colombia  | Ley 1581, SIC rules        | 15 business days reported by secondary sources only                                                                                         | SIC (via RNBD for registered controllers)          | U, treat as unconfirmed |
| Argentina | Ley 25.326                 | **No statutory breach duty** (art. 9 security duty only)                                                                                    | n/a                                                | V                       |

Peru's DS 126-2025-PCM (critical digital incidents to the CNSD in 48h) is S, and whether it reaches other private organisations outside "digital service" providers is U. Brazil's clock yields to any shorter sector-specific deadline. A Chilean incident can trigger both an ANCI report and an Agency report.

## Country notes

**Brazil.** No general cyber law; PL 4.752/2025 sits at the Senate CCT after CCJ approval (10 Dec 2025), not law. ANPD became a regulatory agency under Lei 15.352/2026 (DOU 25 Feb 2026). Records of every incident, notified or not, are kept 5 years (art. 10). LGPD art. 52 fines: up to 2% of Brazilian revenue, capped at R$ 50m per infraction.

**Chile.** Decreto 295 "significant effect" is wide: any unauthorised access and any incident affecting systems holding personal data count (art. 3). Reports must omit personal data. Ley 21.663 fines of up to 20,000 UTM (40,000 for OIVs) and OIV criteria (Decreto 285/2024, one criterion suffices) are secondary only. **Ley 21.719** is in force **1 Dec 2026**; fines are up to 5,000 / 10,000 / 20,000 UTM by tier, and the 2% / 4% of revenue applies only to recidivist grave and very-grave cases, not first offences.

**Mexico.** The 2025 LFPDPPP (INAI dissolved; supervised by the Secretaria Anticorrupcion y Buen Gobierno). Security-breach fines run 200 to 320,000 UMA, doubled for sensitive data. A federal cyber law is not enacted.

**Colombia.** No general cyber law. Ley 1581 sanctions reach 2,000 SMMLV (S). RNBD thresholds and Decreto 338/2022 scope are U.

**Argentina.** Fines are nominal (ARS 1,000 to 100,000), so the AAIP is a weak lever; criminal exposure sits in Penal Code 117 bis and 157 bis. Res. 47/2018 as a de facto security baseline is secondary.

**Peru.** DS 016-2024-JUS in force 31 Mar 2025 (S, El Peruano via search summary). Adaptation periods by size: large companies (over 2,300 UIT sales) 1 year, medium 2, small 3, micro 4, so large firms were due about Mar 2026. Ley 29733 fines run to 100 UIT with a 10% revenue cap; the tier for failing to notify is U.

## International transfers

| Country   | Rule                                                                                                                                                                                                                |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Brazil    | Res. CD/ANPD 19/2024: ANPD standard clauses adopted **unmodified** (grace ended **23 Aug 2025**); BCRs or ANPD-approved specific clauses as alternatives. No foreign SCCs recognised, so EU SCCs do not substitute. |
| Chile     | Ley 21.719 art. 27: adequate country, or contractual clauses/BCRs/other adequate safeguards, or a compliance model/certification; specific non-habitual transfers on explicit consent.                              |
| Colombia  | Art. 26 bars transfers to countries without adequate protection; exceptions include express consent and bank/securities transfers (S).                                                                              |
| Argentina | Art. 12 bars transfers to countries without adequate protection, with listed exceptions (V).                                                                                                                        |
| Mexico    | Intra-group transfers rely on consent exceptions in arts. 35 to 36 (not re-read, U).                                                                                                                                |
| Peru      | Not covered in the sources; check before moving Peruvian personal data.                                                                                                                                             |

For any entity sending Brazilian personal data abroad on the SCC route (the one needing paperwork now): flows to a parent or affiliate abroad (for example an EU/US HQ) need the ANPD clauses signed as written.

## OT / ICS

- **Brazil power assets:** ANEEL REN 964/2021 (in force 1 Jul 2022) requires a cyber-security policy from concessionaires, permissionaires and authorised agents; ONS routine RO-CB.BR.01 sets minimum controls for the regulated cyber environment; serious incidents go to ANEEL. No standard is mandated (ISO/IEC 27019 usable). This is U against official text. Whether a captive plant or self-producer with a grid connection falls under it is an inference to confirm with local counsel.
- **Chile:** essential-service and OIV designation is the OT hook; the 3h alert applies to an entity that is designated. OT content of the Ley 21.663 protocols was not verified.
- Elsewhere in the six countries, OT is bound only through privacy law (and any customer contract).

## Mapping to frameworks (inference, not law)

National rules stand on their own terms, and no country was found to mandate ISO 27001, IEC 62443 or NIST CSF. Mappings are reuse aids that work in both directions. These mappings are working inference: Brazil ANEEL/ONS to IEC 62443 or ISO/IEC 27019 (27019 is explicitly usable); Argentina Res. 47/2018 to ISO 27001 Annex A; Chile Ley 21.663 protocols not mandated to any named standard (U). A group ISMS aligned to ISO 27001 plus 62443 for OT is a sound base, but it does not discharge a local clock; equally, a local programme built on the national rules can feed the group ISMS.

## Watch list (dated Nov 2026)

- **Chile postponement bill (Boletín 18.623-07):** would move Ley 21.719 to 15 Oct 2027 (one source says 1 Dec 2027). **Not law**; its stage is contested (Senate vote 28 Oct vs Constitution Commission 5 Nov). Treat 1 Dec 2026 as binding until published in the Diario Oficial.
- **Brazil PL 4.752/2025:** at the Senate CCT, no later action found.
- **Argentina:** a replacement for Ley 25.326 is reported, status U.
- **Mexico:** a national cybersecurity policy is planned for Q4 2026 (secondary).
- **Colombia:** agency bills and a draft governance decree not enacted.

## Working rules

- Start the clock at **knowledge**, and run the shortest first: Chile 3h (if designated), then Brazil and Peru 48h/3 business days.
- Pre-agree local counsel and Portuguese/Spanish templates; reports omit personal data in Chile.
- Mexico: notify data subjects at once even though no authority clock exists. Argentina: no statutory duty, but contracts and group policy still apply.
- Keep incident records 5 years for Brazil, notified or not.
- Treat U items as open questions for local counsel, never as settled.

## Pairs with

`load_skill breach-notification-matrix`, `load_skill privacy-eu`, `load_skill ot-compliance`, `load_skill choosing-a-framework`, `load_skill third-party-risk`.
