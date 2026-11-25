---
name: tenancy-review
description: Review residential and commercial tenancy agreements under the Landlord and Tenant (Consolidation) Ordinance (Cap 7), covering standard terms, common pitfalls, rent review mechanisms, and dispute resolution.
---

# Tenancy Review — Skill

## Purpose

Review residential and commercial tenancy agreements for Hong Kong properties under the Landlord and Tenant (Consolidation) Ordinance (Cap 7), advising on standard terms, security of tenure, rent review mechanisms, and dispute resolution options.

## Scope

- Fixed term and periodic tenancies
- Residential tenancies (regulated and unregulated)
- Commercial tenancies (contractual)
- Rent review mechanisms (upward-only, open market)
- Assignment and sub-letting
- Repair and maintenance obligations
- Deposit and security
- Termination and break options
- Dispute resolution (Lands Tribunal, mediation)

## Workflow

### 1. Determine Regulatory Framework

- **Residential tenancy**: Part IV of Cap 7 (limited rent control for post-1981 buildings?)
- **Commercial tenancy**: contractual, no statutory security of tenure for new tenancies
- **Regulated tenancy**: pre-1981 domestic premises — Part II of Cap 7 (rare)
- **Licence vs tenancy**: distinguish based on exclusive possession (Street v Mountford)

### 2. Review Essential Terms

#### Rent and Deposit
- **Monthly rent**: inclusive/exclusive of rates, management fee, government rent
- **Rent payment**: bank transfer, autopay, cash (receipt required under s.12 Cap 7)
- **Deposit**: typically 2 months' rent, held as security
- **Interest on deposit**: not standard but negotiable for high-value tenancies
- **Rent review**: mechanism, frequency (typically every 2–3 years), cap/floor
- **Management fee**: who pays? Confirm amount and escalation mechanism

#### Term and Possession
- **Term**: fixed term (typically 1–3 years), periodic tenancy
- **Option to renew**: at tenant's option, at market rent, with conditions
- **Right of first refusal**: on re-letting (rare in HK)
- **Break clause**: conditions, notice period (typically 1–3 months)
- **Vacant possession**: tenant must deliver up on termination

#### Repair and Maintenance
- **Landlord's obligations**: structural repairs, building services, common areas
- **Tenant's obligations**: internal repairs, decoration, replacement of fittings
- **Schedule of condition**: photographic evidence at commencement
- **Dilapidations**: schedule at termination, tenant's reinstatement obligation
- **Air conditioning**: repair and maintenance (common issue in HK)

#### Use and Alterations
- **Permitted use**: specified in tenancy, must match actual use
- **Alterations**: landlord's prior written consent required (not to be unreasonably withheld)
- **Signage**: often restricted in commercial tenancies
- **Fit-out**: responsibility, removal obligation on termination

#### Assignment and Sub-letting
- **Consent**: landlord's prior written consent required (not to be unreasonably withheld for assignment)
- **Guarantee**: often required on assignment
- **Sub-letting**: typically prohibited or subject to strict landlord consent
- **Sharing**: may be restricted (co-working, serviced offices)

#### Service Charges and Outgoings
- **Management fee**: amount, escalation (usually annually)
- **Rates**: payable by landlord (recoverable from tenant if agreed)
- **Government rent**: payable by landlord
- **Service charge**: common areas, security, cleaning
- **Utilities**: tenant directly pays

#### Insurance
- **Landlord's insurance**: building insurance, public liability
- **Tenant's insurance**: contents, plate glass, public liability
- **Indemnity**: tenant to indemnify landlord for third-party claims

#### Termination and Remedies
- **Landlord remedies**: forfeiture (peaceable re-entry must be peaceable — Billson v Residential Apartments), distress for rent (abolished), court possession order
- **Tenant remedies**: specific performance, damages for loss of quiet enjoyment
- **Surrender**: requirement for deed of surrender
- **Holding over**: double rent (s.121 Cap 7) if tenant remains after term

### 3. Residential Tenancy Specifics

- **Standard leasing arrangement**: Government standard form or EAA form common
- **Rent concessions**: first month free vs rent-free periods (affects stamp duty)
- **Stamp duty**: payable by tenant, capped at HK$100 for tenancies under 3 years
- **Registration**: at Land Registry (optional but advisable)
- **Cap 7 Part IV provisions**: rent increases restricted in certain circumstances
- **Residential tenancy deposit cap**: no statutory cap (practice = 2 months)
- **Residential property management**: DMC compliance, building registration

### 4. Commercial Tenancy Specifics

- **Rent review**: usually upward-only, open market, qualified surveyor
- **Service charge**: often separately managed
- **Fit-out period**: rent-free fit-out period (typically 1–3 months)
- **Car parking**: separate licence or included
- **Signage**: management company approval needed
- **Security deposit**: higher than residential (typically 3–6 months)
- **Rental guarantee**: for retail tenancies — minimum guaranteed rent + turnover rent

### 5. Common Pitfalls

- **Oral tenancies**: unenforceable beyond 3 years (s.6, Law Amendment and Reform Ordinance)
- **No schedule of condition**: disputes at termination
- **Repair obligation**: ambiguous "keep in repair" vs "put in repair" distinction (Lurcott v Wakely)
- **Rent review clause**: missing mechanism for valuer appointment, cost allocation
- **Break clause**: ambiguous timing, failure to give notice strictly
- **Stamp duty**: failure to stamp voids the agreement for enforcement purposes
- **Registration**: failure to register affects priority over subsequent interests

## Key Provisions (Cap 7)

| Section | Subject | Key Detail |
|---------|---------|------------|
| s.5 | Implied covenant | Quiet enjoyment, repair obligation (domestic) |
| s.12 | Receipt for rent | Landlord must provide rent receipt |
| ss.85–90 | Distress | Distress for rent still available (use with care) |
| s.121 | Holding over | Double annual value if tenant holds over |
| s.122 | Notice to quit | Notice period for periodic tenancies |

## Tools & Resources

- Land Registry (https://www.landreg.gov.hk) — search tenancy registrations
- Rating and Valuation Department (https://www.rvd.gov.hk) — check rateable value
- HKLII (https://www.hklii.hk) — tenancy case law
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Cap 7 provisions
- Standard tenancy forms (EAA, Law Society of HK)


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
