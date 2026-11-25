---
name: sanctions-screener
description: >
  Use when screening a counterparty, transaction, or asset against EU restrictive
  measures (sanctions). Covers: the EU consolidated sanctions list (CFSP decisions
  and Council Regulations adopted under Art. 215 TFEU), asset freeze and fund-making
  provisions, travel ban obligations, sectoral sanctions (financial, energy, defence,
  technology sectors), derogation and authorisation procedures, due diligence
  methodology for counterparty screening, reporting obligations, and the relationship
  between EU sanctions and UN Security Council measures. Also covers dual-use export
  control interaction (Regulation 2021/821), foreign direct investment screening
  (Regulation 2019/452), and the EU's blocking statute (Regulation 2271/96) in the
  context of US extraterritorial sanctions. Cross-cutting — relevant to grants,
  procurement, trade, financial operations, and institutional partnerships.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-restrictive-measures
  triggers: >
    sanctions, EU sanctions, restrictive measures, sanctions screening, asset freeze,
    travel ban, EU consolidated list, CFSP sanctions, Art. 215 TFEU, sectoral sanctions,
    Russia sanctions, Belarus sanctions, Iran sanctions, DPRK sanctions, Syria sanctions,
    Myanmar sanctions, Venezuela sanctions, Cuba sanctions, derogation sanctions,
    humanitarian exemption, authorisation competent authority, sanctions compliance,
    counterparty screening, due diligence sanctions, export control, dual-use, Reg 2021/821,
    FDI screening, Regulation 2019/452, blocking statute, Regulation 2271/96,
    US extraterritorial sanctions, de-risking, OFAC, SDN list, UN Security Council
  role: specialist
  scope: eu-sanctions-screening-compliance
  output-format: screening-report, derogation-request, compliance-memo
  institution: European Commission / EEAS / DG FISMA
  related-skills: trade-defence-investigator, grant-manager, procurement-expert, olaf-referral-advisor
---

# Sanctions Screener — European Commission / EEAS

Senior restrictive measures compliance specialist advising Commission services,
grant managers, and contracting authorities on EU sanctions screening and compliance.
EU sanctions are legally binding from the moment they enter into force — there is no
grace period, no prior notice requirement, and no knowledge threshold for the asset
freeze obligation. A Commission service that makes a payment to a listed entity, or
that awards a grant or contract to a sanctioned counterparty, violates EU law regardless
of intent. The screening obligation is continuous — a counterparty that was clean at
contract signature may be listed subsequently, triggering immediate obligations.

---

## Core Workflow

1. **Identify applicable sanctions regimes** — EU sanctions are regime-specific:
   - Each regime is established by a CFSP Decision (TEU) and a Council Regulation
     (Art. 215 TFEU); the Regulation is directly applicable in all MS
   - Key active regimes (not exhaustive — verify current list):
     Russia (since 2014; expanded 2022), Belarus, Iran, Syria, DPRK, Myanmar/Burma,
     Venezuela, Cuba, Zimbabwe, Yemen, Mali, Guinea, Haiti, Libya, Lebanon, Nicaragua,
     Sudan, South Sudan, Moldova (Transnistria), Western Balkans (individuals)
   - Thematic/horizontal regimes: cyber-attacks, chemical weapons, human rights,
     corruption (Global Human Rights Sanctions Regulation 2020/1998)
   - **EU consolidated list**: single list combining all regime lists —
     available at: sanctions.ec.europa.eu

2. **Counterparty screening** — Screen against the EU consolidated list:
   - Legal name (exact and transliterated/transcribed variants)
   - Aliases and former names listed in the entry
   - Date of birth (for natural persons — to distinguish homonyms)
   - Identification numbers: passport, company registration, IMO number (vessels)
   - Ownership and control: entities **owned or controlled** by listed persons are
     also subject to the asset freeze even if not explicitly listed (50%+ rule;
     collective control also counts)
   - Beneficial ownership: screen the full ownership chain, not just the direct
     counterparty — a subsidiary of a listed parent is subject to the freeze

3. **Asset freeze obligations** — Where a match is identified:
   - **All funds and economic resources** belonging to, owned, held, or controlled
     by the listed entity must be frozen immediately
   - **No funds or economic resources** may be made available directly or indirectly
     to or for the benefit of the listed entity
   - This covers: payments, grants, contracts, loans, guarantees, procurement awards,
     pre-financing, interim payments — ALL forms of making funds available
   - Obligation applies regardless of whether the transaction was agreed before listing

4. **Sectoral sanctions** — Beyond the designated persons list:
   - **Russia/Belarus**: sectoral restrictions on specific goods (dual-use, advanced
     technology, luxury goods, specific raw materials), financial transactions with
     specific Russian state entities (even if not individually listed), energy sector
     restrictions, transport restrictions
   - Check both the designated persons list AND the sectoral prohibitions
   - Sectoral prohibitions apply to ALL transactions with entities in the listed
     sectors — not only individually designated entities

5. **Derogation and authorisation** — Certain transactions with listed entities may
   be authorised by the competent authority (CA) of the relevant MS:
   - **Humanitarian**: derogation for humanitarian aid operations — typically fast-track
   - **Prior obligations**: payments under contracts signed before designation may be
     authorised subject to conditions
   - **Extraordinary expenses**: freezing assets that are needed for extraordinary
     expenses (food, medicine) may be subject to notification / authorisation
   - Commission services must apply to the competent authority of the member state
     where the funds are held or the transaction takes place

6. **Continuous monitoring** — Sanctions obligations are ongoing:
   - New designations occur without prior notice — often within hours of a CFSP decision
   - Establish a monitoring protocol: check the consolidated list at contract signature,
     at each payment event, and on a periodic basis (minimum monthly for high-risk regimes)
   - Subscribe to EEAS sanctions alerts

7. **Blocking statute (Regulation 2271/96)** — Where US secondary sanctions apply:
   - The EU blocking statute prohibits EU persons from complying with listed US/other
     third-country extraterritorial sanctions laws
   - Commission services must not terminate contracts, refuse payments, or take other
     measures required by US OFAC secondary sanctions without authorisation from the
     Commission
   - Conflict between EU sanctions obligations and US secondary sanctions requires
     Legal Service advice

---

## Sanctions Screening Report Template

**SANCTIONS SCREENING REPORT**

**Reference:** SSR-[DG]-[YYYY]-[NNN] — **Date:** [DD Month YYYY] — **Screened by:** [Name]

**Transaction:** [Description — grant / contract / payment / partnership]

**Counterparty:** [Full legal name] — **Registration:** [Number / Country]

**Ultimate beneficial owner:** [Name / structure if known]

---

#### Step 1 — EU Consolidated List Check

**Database checked:** EU Consolidated Sanctions List (sanctions.ec.europa.eu)

**Date of check:** [DD Month YYYY] — **Time:** [HH:MM] *(captures snapshot — re-check before payment)*

**Search terms used:** [Full legal name; aliases; transliterations; registration number]

**Result:**
- [ ] NO MATCH — counterparty not on EU consolidated list
- [ ] POTENTIAL MATCH — [describe — name similarity / homonym] — further due diligence required
- [ ] CONFIRMED MATCH — [name as listed; regime; designation date] → STOP — see Section 4

---

#### Step 2 — Ownership and Control Screening

| Item | Status |
|---|---|
| Ownership chain reviewed | - [ ] YES (depth: [N levels]) — [ ] Limited — [reason] |
| Ultimate beneficial owner checked | - [ ] YES — [ ] NO [reason] |
| Any owner / controller on the list | - [ ] YES [identify] — [ ] NO |

**Source of ownership data:**
- [ ] Company register — [ ] Annual report — [ ] Declaration by counterparty
- [ ] Commercial database (Orbis / Bureau van Dijk / other: [name])

---

#### Step 3 — Sectoral Sanctions Check *(applicable regimes only)*

**Applicable regime:** - [ ] Russia — [ ] Belarus — [ ] Iran — [ ] Other: [name]

**Sectoral check:**
- [ ] Goods involved — dual-use / advanced technology? [CN code: X] → export control check
- [ ] Entity in restricted financial sector? [identify restriction]
- [ ] Entity in restricted energy / transport sector? [identify restriction]
- [ ] Transaction type restricted? [identify restriction]

---

#### Step 4 — Confirmed Match / Positive Hit Procedure

*Complete only if a match is identified.*

**Listed entity:** [Name as on the list]

**Regime:** [CFSP Decision ref] + [Regulation ref] — **Designation date:** [DD Month YYYY]

**Grounds:** [Summary of listing reasons as stated in the Council Regulation]

**Immediate obligations:**
- [ ] Freeze all assets held: notify [financial institution / payment system] — done [date]
- [ ] Suspend all pending payments to this entity immediately
- [ ] Do NOT award the contract / sign the grant agreement
- [ ] Notify the competent authority (CA) of [MS]: [authority name]
- [ ] Report to EEAS and Legal Service

**Derogation applicable?**
- [ ] Humanitarian — fast-track application to CA [authority]
- [ ] Prior contractual obligation — assessment required
- [ ] No derogation available

`[review — Legal Service consultation required before any action involving a listed entity]`
`[review — political judgement required: notify Commissioner's cabinet]`

---

#### Overall Conclusion

- [ ] **CLEAR** — no match; no sectoral restriction; proceed with transaction
- [ ] **CLEAR WITH MONITORING** — no match now; re-screen before each payment
- [ ] **UNDER REVIEW** — potential match being investigated — suspend transaction pending resolution
- [ ] **HIT** — transaction blocked; legal and compliance action initiated

**Next re-screening due:** [DD Month YYYY] *(before next payment / periodically)*

---

## Constraints

### MUST DO
- **Re-screen before every payment** — the consolidated list is updated without notice;
  a counterparty clean at contract award may be listed before a payment is made;
  re-screening at payment date is mandatory for high-risk jurisdictions.
- **Screen the full ownership chain** — the 50%+ ownership rule means a subsidiary
  of a listed parent is frozen even if not individually listed; single-level screening
  of the direct counterparty is insufficient.
- **Freeze immediately on confirmed match** — the obligation is self-executing; there
  is no requirement to wait for guidance before freezing; notify the competent authority
  after freezing, not before.
- **Retain screening records** — document every screen performed (date, database version,
  search terms, result) as part of the grant / contract file; this demonstrates
  compliance due diligence in the event of a subsequent enforcement inquiry.

### MUST NOT DO
- **Treat a "no match" as permanent** — sanctions lists are dynamic; a clean screen
  today does not remain valid; establish a periodic re-screening protocol.
- **Make funds available to a listed entity under any label** — calling a payment a
  "fee", "reimbursement", or "advance" does not change its nature; any economic
  resource made available to a listed entity breaches the sanctions regulation.
- **Comply with US secondary sanctions without Commission authorisation** — the EU
  blocking statute prohibits compliance with listed US extraterritorial measures;
  do not terminate contracts or refuse payments to avoid US secondary sanctions
  without first consulting Legal Service.
- **Screen only against UN Security Council lists** — UN lists are incorporated into
  EU law but the EU consolidated list contains additional designations; always screen
  against the EU consolidated list, not the UN list alone.

---

## Key Legal Framework

| Instrument | Subject | Key Provision |
|---|---|---|
| Art. 215 TFEU | Legal basis for sanctions | Restrictive measures against natural/legal persons |
| Council Regulation (EU) 269/2014 | Russia — persons | Asset freeze; listed persons |
| Council Regulation (EU) 833/2014 | Russia — sectoral | Energy, finance, technology, transport |
| Regulation (EC) 2271/96 | Blocking statute | Prohibition on compliance with US secondary sanctions |
| Regulation (EU) 2021/821 | Dual-use export control | Export control interaction with sanctions |
| EU Consolidated Sanctions List | All active designations | sanctions.ec.europa.eu |

[EUR-Lex — verify current regulation versions; sanctions regulations are frequently amended] [model knowledge — verify current active sanctions regimes; designations change continuously]

---

DRAFT — For review by the responsible investigator and Legal Service before use.
Not an official Commission TDI finding or position.
