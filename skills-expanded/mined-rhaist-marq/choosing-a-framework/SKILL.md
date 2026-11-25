---
name: choosing-a-framework
description: Maps a company's drivers (sector, customers, region, data type) to the security and privacy frameworks that apply (ISO 27001, SOC 2, NIST CSF/800-53, CIS, PCI DSS, HIPAA, GDPR, NIS2, DORA) and how they relate. Use when the user asks which framework or certification to pursue, whether a regulation applies to them, or how to avoid duplicate compliance work.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Choosing a framework

Frameworks split into three kinds; pick by **why**:

- **Certifiable / attestable** (you prove it to others): ISO 27001, SOC 2, PCI DSS.
- **Voluntary frameworks** (you structure a program): NIST CSF 2.0, CIS Controls.
- **Law / regulation** (non-optional if in scope): GDPR, NIS2, DORA, HIPAA. PCI DSS is contractual, not law, but enforced like one by card brands.

Most companies end up with a **stack**: one program framework (CSF or ISO) + whatever laws/contracts their data and customers force on them. Don't pick one and ignore the rest.

## Driver → framework

| Driver / situation                                                                                          | Reach for                   | Why                                                                      |
| :---------------------------------------------------------------------------------------------------------- | :-------------------------- | :----------------------------------------------------------------------- |
| Enterprise/EU customers demand a cert in procurement                                                        | **ISO 27001**               | Globally recognized certificate; auditable ISMS                          |
| US SaaS customers demand assurance                                                                          | **SOC 2**                   | The US B2B SaaS default; attestation report, not a cert                  |
| You take card payments (store/process/transmit PAN)                                                         | **PCI DSS v4.0.1**          | Mandatory via card-brand contracts; scope-driven                         |
| US health data (PHI)                                                                                        | **HIPAA**                   | Law for covered entities + business associates                           |
| Any personal data of people in the EU/UK                                                                    | **GDPR** (UK GDPR)          | Extraterritorial; applies by data subject location, not company location |
| EU operator in critical/important sector (energy, transport, health, digital infra, ICT, food, waste, mfg…) | **NIS2**                    | EU directive; broad sector sweep, management accountable                 |
| EU financial entity (bank, insurer, payment, crypto, fund) or critical ICT vendor to one                    | **DORA**                    | EU regulation; ICT operational resilience                                |
| US federal data / want a control catalog under CSF                                                          | **NIST 800-53**             | The control set CSF subcategories map into                               |
| Small/mid org, no mandate, "just get secure" cheaply                                                        | **CIS Controls v8.1 (IG1)** | Prioritized, concrete, free; good starting baseline                      |
| Need a common language across exec + technical, gap assessment                                              | **NIST CSF 2.0**            | Outcome-based lens; maps to ISO/800-53/CIS                               |
| You build, sell, or deploy AI in the EU (incl. HR/recruitment tooling)                                      | **EU AI Act**               | EU regulation; extraterritorial, binds per system (provider vs deployer) |
| Customers ask you to prove AI governance                                                                    | **ISO/IEC 42001**           | The certifiable AI management system; ISO 27001-shaped                   |
| You ship a product with digital elements into the EU                                                        | **EU CRA**                  | EU regulation; per-product CE marking + vulnerability handling           |

## How they relate (avoid double-work)

- **CSF 2.0 = the lens; ISO 27001 / 800-53 / CIS = the controls.** CSF subcategories carry Informative References that map to the others: one control set can satisfy several frameworks. See `load_skill control-mapping`.
- **ISO 27001 ≈ SOC 2 overlap is large** (access control, change mgmt, IR, vendor risk). Companies often run both off one control set; SOC 2 is broader on customer-facing assurance, ISO is a cleaner international cert.
- **CIS IG1 is a fast on-ramp** to ISO/CSF: implement it, then map upward.
- **PCI/HIPAA/GDPR/NIS2/DORA are obligations, not programs**: they tell you _what you must do_; an ISO/CSF program tells you _how to run it_. Run a program framework and treat the laws as additional required controls layered on.

## Region quick-cut

- **EU/UK**: GDPR always (if personal data). + NIS2 if critical sector, + DORA if finance, + **CRA** if you ship products with digital elements, + **AI Act** if AI is in the product or in HR. ISO 27001 is the procurement cert of choice. These stack: a connected industrial product sold by an EU manufacturer can be in all of them at once. UK specifics (NIS Regs + the Cyber Security and Resilience Bill, DUA Act, CAF, Cyber Essentials, PSTI): `load_skill uk-cyber-regs`.
- **US**: SOC 2 for B2B SaaS; HIPAA for health; sector laws (GLBA finance, state privacy e.g. CCPA; verify current). PCI everywhere cards are taken.
- **Global SaaS**: SOC 2 (US buyers) + ISO 27001 (everyone else) + GDPR (EU users) is the common trio.
- **APAC**: no single regime: ISO 27001 is again the procurement cert of choice, but privacy/transfer law is per-country and a common EU/US blind spot: **China PIPL** (data localization + a mandatory cross-border transfer route), **India DPDP Act** (rules notified Nov 2025, phasing in), **Singapore PDPA**, **Japan APPI**, **Australia Privacy Act** (+ **APRA CPS 234** info-security for regulated finance). GDPR compliance does not cover them; verify per country. Per-country detail and breach clocks: `load_skill privacy-apac`.
- **APAC mandatory cyber frameworks** bind by designation, not by sector label: **China MLPS 2.0** (GB/T 22239-2019; level 2 and above filed with public security, level 3 evaluated at least yearly by a PRC-based agency) applies to every network operator, and no jurisdiction accepts ISO 27001, IEC 62443 or NIST CSF in place of the national act. Singapore's **CII code** (2026) requires CII owners to hold Cyber Trust Mark Advocate (Tier 5). `load_skill apac-cyber-regs`.
- **Middle East:** **Saudi NCA ECC-2** (and **OTCC-1:2022** for OT) binds government and CNI entities and reaches others through customer flow-down; no ECC-2 crosswalk to ISO 27001 or NIST CSF is confirmed. **Qatar NIA** has no verified binding scope. Turkey's Law 7545 names Manufacturing Industry and Energy as critical sectors, with duties still pending. `load_skill middle-east-regs`.
- **LATAM:** no country mandates ISO 27001, IEC 62443 or NIST CSF; binding cyber duties sit mainly in **Chile** (Ley 21.663, by designation), the rest is privacy law. `load_skill latam-regs`.

## Next steps

- Deep-dive a specific regime: `load_skill iso27001`, `soc2`, `pci-dss`, `nist-csf`, `privacy-eu` (GDPR), `nis2-dora`, `eu-cra`, `eu-ai-act`, `privacy-us`, `us-sectoral-regs`, `uk-cyber-regs`, `privacy-apac`, `apac-cyber-regs`, `middle-east-regs`, `latam-regs`, `cloud-assurance`, `cmmc-800-171`, `ai-governance`.
- **Plants and machine builders**: `load_skill ot-compliance` (which regimes bind a factory or a shipped machine) and `load_skill ot-ics` (the engineering).
- Confirmed which apply → run a **gap analysis** against the chosen framework: `load_skill gap-analysis`.
- Then map controls once, satisfy many: `load_skill control-mapping`.
- For the canonical current text of any framework named above, web-fetch the source named in its skill; versions and dates move.
