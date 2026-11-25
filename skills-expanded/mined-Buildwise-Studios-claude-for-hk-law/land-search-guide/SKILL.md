---
name: land-search-guide
description: Guide to Land Registry searches and title investigation for Hong Kong property under the Land Registration Ordinance (Cap 128), covering registrable instruments, priority rules, caveats, and title verification procedures.
---

# Land Search Guide — Skill

## Purpose

Guide legal practitioners through Land Registry searches and title investigation for Hong Kong property transactions under the Land Registration Ordinance (Cap 128), ensuring proper due diligence and identification of title defects.

## Scope

- Land Registry Integrated Information System
- Types of searches (Property, Name, Form 1/2/3)
- Registrable instruments under Cap 128
- Priority rules and the race-to-register system
- Caveats, pending actions, and bankruptcy orders
- Deeds vs Torrens — HK registration system explained
- Title investigation: 15-year rule, root of title
- Defects identification and resolution

## Workflow

### 1. Understand the HK Registration System

Hong Kong operates a **deeds registration system** (not Torrens title). Registration under Cap 128 gives **priority** but does not **constitute title**. The register:
- Records the existence of deeds and instruments
- Does not guarantee title or ownership
- Priority is determined by order of registration (not execution)
- Unregistered instruments may still be valid between parties

### 2. Conduct the Search

Land Registry search types:

#### By Property (Form 1)
- Search by lot number, street address, or building name
- Returns: current registered owner, encumbrances, deeds registered
- Most common search for conveyancing

#### By Name (Form 1A)
- Search against individual or company name
- Returns: properties registered in that name
- Useful for matrimonial home searches and bankruptcy checks

#### By Reference (Form 2)
- Search by registered memorial number
- Returns: specific deed or instrument details

#### Historical Search (Form 3)
- Trace chain of title over time
- Essential for title investigation

### 3. Examine Search Results

Review the following on a Land Registry search printout:

- **Property description**: Lot, section, floor, unit
- **Current owner**: name (and joint tenancy/tenancy in common)
- **Government lease**: term, conditions of grant, user clause
- **Deeds registered**: chronological list of registered instruments
- **Encumbrances**: charges, mortgages, caveats, pending actions
- **Pending actions**: litigation affecting the property
- **Bankruptcy orders**: against current or previous owners
- **DMC**: Deed of Mutual Covenant recorded

### 4. Title Investigation — 15-Year Rule

- **Root of title**: examine title from at least 15 years back (Conveyancing and Property Ordinance practice)
- **Chain of title**: every transaction in the chain must be properly documented and registered
- **Identity**: ensure each seller in the chain is the same person as the buyer from the prior transaction
- **Completeness**: all material deeds should be present; missing deeds require statutory declaration

#### Steps to Verify Chain

1. Locate the root of title (oldest deed in the chain, at least 15 years old)
2. Trace forward from the root to the current owner
3. Verify each transfer: seller = registered owner at time of sale
4. Check for breaks in the chain: any unregistered transfers?
5. Verify execution: are all deeds properly executed and attested?
6. Check for encumbrances: were they properly discharged?
7. Verify identity: HKID numbers coincide where available

### 5. Common Defects and Resolution

| Defect | Issue | Resolution |
|--------|-------|------------|
| Missing deed | Gap in chain of title | Statutory declaration of loss, indemnity insurance |
| Incorrect name | Seller's name differs across deeds | Statutory declaration of identity, affidavit of fame |
| Unsatisfied charge | Mortgage not formally discharged | Requisition for discharge / confirmation of discharge |
| Caveat registered | Third party claim | Requisition for withdrawal or evidence of consent |
| Pending action | Litigation pending | Requisition for evidence of resolution |
| Government lease breach | Non-compliance with conditions | Confirm waiver or deemed compliance |
| Unauthorised building works | Works done without approval | Requisition for indemnity, building department clearance |
| DMC non-compliance | Breach of DMC terms | Requisition for compliance or indemnity |

### 6. Special Searches

- **RVD**: check rateable value, rates payable, government rent
- **Building Authority**: check building plans, occupation permit, unauthorised works
- **Town Planning**: check zoning, planning applications, enforcement notices
- **Water Authority**: check water supply and drainage connection
- **Fire Services**: check fire safety compliance (commercial properties)
- **Companies Registry**: check corporate seller authority, charges on land

### 7. Report and Advice

Prepare a due diligence report covering:
- Land Registry search summary
- Title investigation findings
- Identified defects and recommended requisitions
- Risk assessment (clean / minor issues / material defects)
- Recommended actions (requisition, indemnity, title insurance, price adjustment)

## Key Provisions (Cap 128)

| Section | Subject | Key Detail |
|---------|---------|------------|
| s.3 | Registration system | Deeds registration; priority by registration date |
| s.5 | Effect of registration | Notice to all persons; priority from registration |
| s.13 | Applications | Form and manner of registration |
| s.20 | Priority of registered instruments | First to register has priority |
| s.21 | Caveats | Lodged by person claiming interest; effect |
| s.21A | Pending actions | Notice of court proceedings affecting land |
| s.22 | Bankruptcy orders | Affect title of bankrupt |

## Tools & Resources

- Land Registry (https://www.landreg.gov.hk) — Integrated Information System, e-Search
- Rating and Valuation Department (https://www.rvd.gov.hk) — Rateable value, government rent
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Cap 128, Cap 219 provisions
- Land Registry Practice Directions
- Law Society of HK Practice Direction on Conveyancing


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
