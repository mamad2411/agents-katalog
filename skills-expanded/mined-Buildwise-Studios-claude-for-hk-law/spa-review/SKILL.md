---
name: spa-review
description: Review and advise on formal Sale and Purchase Agreements for Hong Kong property transactions under the Conveyancing and Property Ordinance (Cap 219), covering key clauses, common pitfalls, title investigation, and completion mechanics.
---

# SPA Review — Skill

## Purpose

Review and advise on formal Sale and Purchase Agreements (SPA) for Hong Kong property transactions, ensuring compliance with Cap 219 and protecting the client's interests through careful scrutiny of key clauses, conditions precedent, and completion mechanics.

## Scope

- Provisional SPA and Formal SPA review
- Conditions precedent (mortgage, building inspection, title)
- Deposit and payment structure
- Title investigation and requisitions
- Completion and delivery obligations
- Risk allocation (vacant possession, encumbrances, unauthorised works)
- Default and termination provisions
- Specific clauses for New Territories land and village houses

## Workflow

### 1. Preliminary Review

- Confirm property details: Lot/Unit number, floor, section, car park spaces
- Verify parties: buyer identity, seller identity, corporate vs individual
- Check consideration: total price, deposit breakdown (initial, further, balance)
- Confirm completion date and time (typically Friday or 14 days after contract)
- Identify any conditions precedent (mortgage approval, building inspection)

### 2. Review Key Clauses

#### Deposit and Payment
- **Initial deposit**: typically 5–10% paid on provisional SPA
- **Further deposit**: brings total to 10–20% on execution of formal SPA
- **Balance payable on completion**: remainder after deducting deposits
- **Stakeholder clause**: who holds the deposit? Usually estate agent or solicitors' firm
- **Interest on deposit**: buyer entitled to interest (or reasonable return) — often overlooked
- **Default interest**: interest on late payment (usually 10–12% pa)

#### Conditions Precedent
- **Mortgage approval**: date for obtaining, amount, bank discretion
- **Building inspection**: right to inspect, scope
- **DMC review**: right to review and accept Deed of Mutual Covenant
- **Title**: right to investigate and raise requisitions
- **Government lease**: condition on acceptable lease terms
- **Unauthorised building works**: seller's warranty and indemnity

#### Title and Encumbrances
- **Vacant possession**: seller warrants property will be delivered vacant
- **Encumbrances**: seller must discharge all mortgages, charges, liens
- **Caveats and pending actions**: seller warrants none pending
- **Restrictive covenants**: confirm not breached
- **Government lease conditions**: confirm not breached
- **Tenancies**: list existing tenancies, if any (vacant possession if none)

#### Property Condition
- **Unauthorised building works**: seller warrants no UBWs or will indemnify
- **Fixture and fittings**: list included/excluded items (appliances, wardrobes, curtains)
- **Fung Shui**: standard exclusion (no warranty on fung shui)
- **Dampness/alterations**: seller warrants none to buyer's detriment

#### Completion
- **Time is of the essence** (standard in HK SPAs)
- **Delivery**: assignment executed, keys delivered, property vacated
- **Apportionment**: rates, government rent, management fees apportioned to date of completion
- **Adjustments**: management fee sinking fund, deposits with contractor
- **Late completion**: penalty interest provision

#### Default and Termination
- **Buyer default**: forfeiture of deposit, seller may resell, claim damages
- **Seller default**: double deposit return, buyer may rescind, specific performance
- **Force majeure**: standard exclusion (epidemics, government orders, inclement weather)
- **Material adverse change**: rare but increasingly negotiated post-COVID

### 3. Title Investigation

- Obtain Land Registry search (Form 1, 2, 3)
- Examine Government lease: term, user clause, building covenant, assignment restriction
- Check chain of title: minimum 15 years, or from root of title
- Verify identity: registered owner matches seller
- Check DMC: management rights, car park, common area, signage
- Check for pending actions, orders, caveats, bankruptcy
- Raise requisitions on any defects

### 4. Special Considerations

- **New Territories**: NT land, Small House Policy, ancestral land
- **Village houses**: ownership structure, licence requirements, user restrictions
- **Corporate seller**: board resolution for sale, stamp duty, capital gains
- **Corporate buyer**: director authorisation, board minutes
- **Joint purchasers**: how to hold (joint tenancy vs tenancy in common)
- **Non-HKPR buyer**: BSD/NRSD implications, trustee holding structure
- **Foreclosure / mortgagee sale**: limited warranties, no vacant possession warranty

### 5. Post-SPA Steps

- Prepare assignment
- Arrange stamp duty adjudication (within 30 days)
- Schedule completion
- Register assignment at Land Registry (within 1 month)
- Follow up on apportionment certificates

## Common Pitfalls

- **Missing root of title**: must go back at least 15 years
- **Unauthorised building works**: seller may refuse to indemnify
- **Government lease non-compliance**: user clause breach, building covenant expired
- **Pre-emption rights under DMC**: some DMCs give owners first right of refusal
- **Time bars**: loan approval condition, requisition deadline
- **Multi-property/complex structures**: ensure correct lot/unit assignment

## Key Provisions (Cap 219)

| Section | Subject | Relevance |
|---------|---------|-----------|
| s.14 | Formalities of deed | Assignment requirements, execution |
| s.41 | Burden of covenants | Runs with land in equity |
| s.50–54 | Mortgagee's power of sale | Foreclosure/mortgagee sales |
| s.58 | Power to appoint receiver | Mortgage remedies |

## Tools & Resources

- Land Registry (https://www.landreg.gov.hk) — title search, memorial, pending actions
- Rating and Valuation Department (https://www.rvd.gov.hk) — rates, government rent, valuation
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Cap 219, Cap 128 provisions
- Standard SPA forms (HKIS / Law Society / Estate Agents Authority)


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
