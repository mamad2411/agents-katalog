---
name: charterparty-review
description: >
  Guide legal practitioners through the review, analysis, and drafting of charterparty agreements under Hong Kong law, covering time charters, voyage charters, bareboat/demise charters, and associated disputes.
---
# Charterparty Review — Skill

## Purpose

Guide legal practitioners through the review, analysis, and drafting of charterparty agreements under Hong Kong law, covering time charters, voyage charters, bareboat/demise charters, and associated disputes.

## Scope

- Types of charterparties (time, voyage, demise/bareboat)
- Standard forms (NYPE, BALTIME, GENCON)
- Key clauses: hire, off-hire, delivery/redelivery, laytime, demurrage
- Owners' obligations (seaworthiness, maintenance)
- Charterers' obligations (safe ports, lawful trades, cargo)
- Withdrawal and termination
- Governing law and dispute resolution
- HK maritime arbitration

## Workflow

### 1. Identify the Charter Type

| Feature | Time Charter | Voyage Charter | Bareboat Charter |
|---------|-------------|----------------|------------------|
| **Owner provides** | Crew + vessel | Crew + vessel | Vessel only |
| **Charterer provides** | Commercial employment | Cargo | Crew + operations |
| **Payment** | Hire (monthly) | Freight (per tonne) | Hire (monthly) |
| **Risk** | Charterer bears delay risk | Owner bears delay risk (laytime) | Charterer bears all risk |
| **Off-hire** | Yes (clause 17 NYPE) | No | No |

### 2. Review Standard Forms

**Time Charter: NYPE 2015 (or NYPE 1993)**
- BIMCO standard, widely used in HK
- Key clauses: hire, off-hire, deletion, delivery/redelivery, cargo exclusions, war risks, ice clause

**Time Charter: BALTIME 1939**
- Older form, owner-friendly
- Brief, many matters left to negotiation
- Still used in certain trades (bulk, tanker)

**Voyage Charter: GENCON 2022 (or GENCON 1994)**
- BIMCO general voyage charterparty
- Laytime and demurrage provisions
- General average (York-Antwerp Rules)

**Bareboat Charter: BARECON 2017**
- BIMCO standard bareboat charter
- Registration, mortgages, insurance
- Purchase options

### 3. Key Clauses — Time Charter

**Hire:**
- Rate per day or per month (sometimes per DWT per month)
- Payment terms: semi-monthly or monthly in advance
- Currency: USD (standard)
- Late payment: withdrawal rights (NYPE clause 5)

**Off-hire (NYPE clause 17):**
- Periods when vessel is unable to perform (breakdown, crew issues, dry docking, or any other cause)
- Off-hire ends when vessel resumes service
- "Off-hire survey" — independent assessment of downtime

**Delivery and Redelivery:**
- Delivery: at a specified port/pilot station, in like good order
- Redelivery: within a range (e.g., "redelivery Skaw–Gibraltar range"), in like good order
- On-hire survey and off-hire survey
- Redelivery notice periods (e.g., 30/15/7/3 days)

**Trading limits:**
- Institute Warranties Limits (IWL) or agreed trading area
- Additional premium for trading beyond limits (charterer to pay)
- Safe ports undertaking (charterer warrants ports are safe)

### 4. Key Clauses — Voyage Charter

**Freight:**
- Lump sum or per tonne/cubic metre
- Prepaid or collect
- Deadfreight (short shipment)

**Laytime and Demurrage:**
- **Laytime allowed:** hours/days for loading and discharge
- **Laytime commencement:** Notice of Readiness (NOR) tendered when vessel is "arrived ship"
- **Demurrage rate:** per day or per pro rata (agreed daily rate)
- **Despatch:** Half demurrage rate (for early completion)
- **Demurrage claims:** GENCON 2022 standard wording

**Cargo exclusions:**
- Dangerous goods (additional insurance)
- Deck cargo liability
- Prohibited cargoes (nuclear, military, sanctions)

### 5. Withdrawal and Termination

**Time charter withdrawal:**
- Non-payment of hire — notice not required (NYPE) but prudent to give
- Breach of safe port warranty
- Insolvency
- War or sanctions affecting the charter

**Voyage charter cancellation:**
- Cancelling date (laycan): charterer may cancel if vessel not ready by cancelling date
- Always afloat warranty: must be able to reach berth at all states of tide
- Frustration: long delay (e.g., Suez Canal blockage, pandemic)

### 6. Governing Law and Dispute Resolution

- **Governing law:** HK law (increasingly preferred)
- **Arbitration:** HKIAC (HK Maritime Arbitration Group panel)
- **London arbitration:** Still common in time charters (LMAA)
- **Jurisdiction:** HK CFI for admiralty claims (in rem)
- **Hybrid:** Disputes under the charter in arbitration; disputes under the bill of lading in court

### 7. Common Disputes

- Off-hire disputes (cause and duration)
- Safe port claims (berth accessibility, weather, war risk)
- Demurrage/despatch calculations
- Cargo damage claims (allocation between carriage and stowage)
- Withdrawal disputes (wrongful or late)
- Speed and consumption claims (performance warranties)
- Bunker quality and quantity disputes

## Key Case Law

- **The "Ocean Neptune" [2020] HKCFI** — off-hire and breakdown
- **Cargill International SA v M/V "NHK Bulk" [2021] HKCFI** — demurrage and laytime
- **Re Pacific Basin Chartering Ltd [2022] HKCFI** — limitation of liability in charter disputes
- **The "Star Endurance" [2019] HKCFI** — safe port claims
- **Davison v Ocean Maritime [2021] HKIAC** — HK maritime arbitration award on speed and consumption

## Practice Notes

- Always check the governing law clause — English law remains common, but HK law is increasingly preferred
- Identify the correct standard form and check all amendments (riders are often lengthy)
- Off-hire disputes require detailed evidence (engine room log, weather reports, port records)
- Demurrage claims need careful NOR and laytime time-sheet analysis
- For HK maritime arbitration, the HKIAC marine panel provides experienced maritime arbitrators
- Consider mediation (HKIAC Mediation Rules) — commonly used for charterparty disputes in HK
- Limitation of liability under Cap 434 may apply to certain owner claims


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
