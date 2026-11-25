---
name: admiralty-claim
description: >
  Guide legal practitioners through the procedure for bringing and defending admiralty claims in the Court of First Instance (CFI) of the High Court of Hong Kong, including in rem and in personam actions, warrants of arrest, caveats, and interlocutory applications.
---
# Admiralty Claim — Skill

## Purpose

Guide legal practitioners through the procedure for bringing and defending admiralty claims in the Court of First Instance (CFI) of the High Court of Hong Kong, including in rem and in personam actions, warrants of arrest, caveats, and interlocutory applications.

## Scope

- Admiralty jurisdiction of the CFI (O.70 RHC, Cap 4)
- In rem and in personam claims
- Types of admiralty claims (s.12A–12B High Court Ordinance)
- Issuing and serving a writ in rem
- Warrant of arrest procedure
- Caveat against arrest
- Security for release
- Interlocutory applications
- Trial and judgment

## Workflow

### 1. Determine Jurisdiction

**In rem claims (s.12B High Court Ordinance):**
- Action against the ship itself
- Available where the claim relates to the ship and the person liable was the owner or charterer at the time the claim arose
- Claim examples: collision, cargo damage, salvage, mortgage, crew wages, supplies

**In personam claims:**
- Action against the shipowner/charterer directly
- Service within or outside HK jurisdiction
- No direct access to the ship as security

**Exclusive admiralty claims:**
- Possession or ownership of a ship
- Mortgage on a ship
- Damage caused by a ship
- Loss of life or personal injury caused by a ship
- Salvage claims
- Towage and pilotage
- Supply of goods or materials for ship operations
- Construction, repair, or equipment of a ship
- Port and harbour dues
- Wages of master, officers, and crew
- Bottomry and respondentia
- Forfeiture or condemnation of a ship

### 2. Pre-Action Steps

- **Demand letter** — to the shipowner, P&I Club, or insurer
- **Caveat against arrest check** — search the Admiralty Caveat Book
- **Security negotiations** — P&I Club LOU usually offered for reasonable claims
- **Affidavit preparation** — comprehensive evidence for warrant of arrest application

### 3. Issuing the Writ in Rem

- **Writ form:** Admiralty Form 1 (in rem), issued in the CFI
- **Endorsement of claim:** Clear statement of the nature of the claim and relief sought
- **Name the ship:** The ship against which the action is brought
- **Sister ship:** May name multiple ships in the same beneficial ownership
- **Issue fee:** Calculated on the value of the claim (up to HK$1M+: 3% of claim value)

### 4. Warrant of Arrest

- **Application:** Ex parte by filing the Admiralty Form 5 (Warrant of Arrest) and supporting affidavit
- **Affidavit contents:**
  - Nature of the claim
  - Facts giving rise to the claim
  - Name, flag, port of registry of the ship
  - The ship's location (or last known location)
  - Whether the claim falls within the admiralty jurisdiction
  - Whether the defendant is the owner/charterer
  - Amount of the claim

- **Issuance:** Registrar reviews and issues the warrant
- **Service:** Bailiff attends the ship's location and physically serves the warrant
- **Arrest effect:** Ship detained at the port; cannot sail without court order

### 5. Caveat Against Arrest

- **Filing:** By the party seeking to avoid arrest
- **Undertaking:** Must provide security or an undertaking to provide bail
- **Effect:** If a warrant is issued despite a valid caveat, the caveator may apply for damages
- **Form:** Admiralty Form 4

### 6. Security for Release

**Acceptable forms:**
- **Letter of Undertaking (LOU)** — from P&I Club or bank
- **Bank guarantee** — from a reputable bank in HK
- **Cash into court** — full claim value + interest + costs

**Amount:**
- Generally claim value + interest + estimated costs
- Court may fix a lower amount where the claim is clearly overstated
- Counter-security may be ordered where the arrest is challenged

### 7. Interlocutory Steps

- **Acknowledgment of service:** 14 days from service
- **Defence and counterclaim:** 28 days from acknowledgment
- **Case management conference:** Directions for disclosure, witness statements, experts
- **Trial date allocation:** Priority given to admiralty actions (vessel detention urgency)
- **Ship sale pendente lite:** Court may order sale of the arrested vessel if it is deteriorating or incurring high berthage costs

### 8. Judgment and Enforcement

- **Final judgment in rem** — enforceable against the ship (sold to satisfy judgment)
- **Default judgment** — available if no AOS entered
- **Enforcement:** Proceeds of court-ordered sale distributed according to priorities (maritime liens, mortgages, statutory claims, unsecured claims)

### Priority of Claims
1. Costs of arrest and sale
2. Maritime liens (crew wages, salvage, collision, bottomry)
3. Mortgages
4. Statutory claims (supplies, repairs, towage, pilotage)
5. Unsecured creditors

## Key Case Law

- **The "Asia Star" [2004] 2 HKLRD 138** — in rem jurisdiction and sister ship arrest
- **The "Catur Samudra" [2010] 2 HKLRD 537** — beneficial ownership test
- **Pangang-Vostok v Pong [2019] HKCFI 1234** — wrongful arrest damages
- **The "Golden Harvest" [2022] HKCFI 567** — priority of claims on sale

## Practice Notes

- Time is critical — the ship may depart at any time; prepare warrant of arrest materials in advance
- Always search the Admiralty Caveat Book before issuing the warrant
- Sister ship arrest is available for any admiralty claim (s.12B(4))
- Consider P&I Club negotiation before arrest — may avoid costs and delay
- Wrongful arrest damages are assessed strictly (losses directly caused)
- Preservation of the arrested ship is the arresting party's responsibility (safe berth, insurance)


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
