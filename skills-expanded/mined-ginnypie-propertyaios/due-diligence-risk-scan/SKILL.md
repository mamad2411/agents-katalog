---
name: due-diligence-risk-scan
description: "Use when you have a property under consideration and want to run a structured due diligence checklist before making an offer or exchanging contracts."
---

# Skill — Due Diligence Risk Scan

**Stage:** 3 — Stress-Test & Diligence
**Hook:** The questions you need answered before you sign anything.
**Use when:** You have a property under consideration and want to run a structured due diligence checklist before making an offer or exchanging contracts.

---

## Purpose

This skill produces a structured due diligence risk scan covering contract and title risks, building and pest risks, strata risks (if applicable), suburb and zoning risks, and financial risks. It generates the questions to ask each professional before signing.

This is preparation for professional due diligence — not a substitute for it.

---

## Reads from

- Property File: SNAPSHOT, SUBURB & DEMAND, RED FLAGS (from prior skills)
- Investor Profile (if available)

## Writes to

- Property File: RED FLAGS (open), VERIFY-WITH-A-PRO

> **Running this standalone:** This skill is self-contained. If you don't have a "Property File" or the paired skills listed below, just fill in the Inputs block — that's all this skill needs. The "Reads from" and "Pairs with" references are optional extras, not requirements.

---

## Inputs required

```
PROPERTY: [address / suburb, property type]
STATE: [VIC / NSW / QLD / SA / WA / TAS / ACT / NT]
PROPERTY AGE: [approximate build year or decade]
STRATA / BODY CORPORATE: [yes / no / unknown]
VENDOR DISCLOSURE DOC: [available / not yet / attached]
PRICE: $[amount or guide]
YOUR ROLE: [buyer / investor / first home buyer]
ANY KNOWN ISSUES: [describe anything you've already flagged]
```

**Vendor disclosure terminology is state-specific — use the term for the STATE supplied:**

| State | Vendor disclosure document (verify current name with your solicitor) |
|---|---|
| VIC | Section 32 vendor statement |
| NSW | Contract for sale + s10.7 planning certificate |
| QLD | Contract + seller disclosure statement |
| SA | Form 1 vendor statement |
| WA | Contract + Joint Form of General Conditions disclosures |
| TAS | Contract + vendor disclosures |
| ACT | Contract + required documents package (incl. building/pest for houses) |
| NT | Contract + disclosures |

*Assumption — verify the exact document name and content with a licensed solicitor or conveyancer in the property's state; the above is a typical AU estimate, not legal advice.*

---

## Output contract

Return exactly these 7 sections:

### 1. CONTRACT AND TITLE FLAGS
Questions to verify with your solicitor or conveyancer:
- Title type: freehold / strata / community title / leasehold
- Easements: drainage, power lines, right of way — on title?
- Caveats or encumbrances: registered interests limiting use or sale
- Planning overlays: heritage, flood, vegetation, development restrictions
- Vendor disclosure: is the state's vendor disclosure document (see the terminology table above for the STATE supplied) available and complete?
- Outstanding permit or building approval history: any unapproved works?
- Settlement terms: any unusual conditions — long settlement, lease-back, subject to finance?

### 2. BUILDING AND PEST FLAGS
Questions for your building and pest inspector:
- Property age and construction type (brick, weatherboard, concrete slab)
- Roof type and condition risk (terracotta, colorbond, asbestos-era materials)
- Moisture, damp, or rising damp indicators
- Pest risk: termites (especially in timber-framed construction), borers
- Structural movement: cracks, subsidence, foundation issues
- Drainage and stormwater condition
- Electrical, plumbing, and hot water system age
- Any visual signs flagged in listing photos (water staining, cracks, sagging)

### 3. STRATA / BODY CORPORATE FLAGS (if applicable)
Questions for your solicitor/strata specialist:
- Is the building in surplus or deficit on the sinking fund?
- Are there any pending special levies?
- Are there any building defect claims or ongoing disputes?
- What is the current strata levy (admin + sinking fund)?
- Are there any NCAT or court proceedings?
- What is the body corporate's insurance coverage?
- Are pets allowed? What are the key bylaws?
- Are there any short-term rental restrictions?

### 4. SUBURB AND ZONING FLAGS
Items to verify with council and state authority:
- Current zoning and permissible uses
- Any planned rezoning or development applications nearby
- Flood zone or overland flow mapping
- Bushfire Attack Level (BAL) rating
- Contaminated land or industrial proximity
- Proposed infrastructure: roads, rail, development that could affect value or amenity

### 5. FINANCIAL FLAGS
Items to verify with your mortgage broker:
- Lender appetite for this property type, suburb, and age
- Any LVR restrictions for this postcode or building?
- Is LMI required at your LVR?
- Is this property in a building with known construction defect history?
- Are there any APRA or lender restrictions on high-density buildings in this postcode?

### 6. RED FLAGS SUMMARY

Rate every flag with this severity rubric so the table is consistent:

- **High** — could stop the purchase or plausibly cost more than ~$10k to resolve (e.g. structural defect, unapproved works, major special levy, contaminated land). *Assumption — the dollar threshold is a rough guide; verify.*
- **Medium** — needs a professional to price or investigate before you can size the risk (e.g. damp indicators, easement affecting a planned extension, lender appetite unknown).
- **Low** — a routine check expected to clear with normal due diligence (e.g. standard drainage easement, minor cosmetic issues).

List all flags identified in a table. For High-severity flags, add a rough "if confirmed" consequence so the flag carries meaning, not just a referral:

| Flag | Source | Severity | If confirmed (rough consequence — estimate, verify) | Verify with |
|---|---|---|---|---|
| [flag] | [listing / suburb / contract / inspection] | [low/medium/high] | [rough cost/meaning, or "N/A" for low] | [professional] |

### 7. DUE DILIGENCE CHECKLIST
A pre-exchange checklist:

- [ ] Solicitor / conveyancer has reviewed the full contract
- [ ] State vendor disclosure document (see terminology table) reviewed and understood
- [ ] Building and pest inspection commissioned and reviewed
- [ ] Strata report obtained and reviewed (if applicable)
- [ ] Finance pre-approval (or subject to finance clause in contract)
- [ ] Flood and fire overlay confirmed
- [ ] Lender appetite for property type and postcode confirmed
- [ ] All red flags resolved or accepted with full understanding

---

## Safety boundaries

- Never advise whether a property is "safe to buy"
- Never interpret a contract — direct all contract questions to a solicitor
- Never advise on pest outcomes — that requires an inspector on site
- Never omit the finance flag on strata buildings in high-density postcodes

---

## Pairs with

- [Suburb Research](suburb-research.md) — suburb and zoning context
- [Broker Prep](broker-prep.md) — finance flags to raise with your broker

---

## Disclaimer

> This output is general information and educational preparation only. It is not legal advice, financial advice, credit advice, a building inspection, or a strata report. All risks identified are starting points for professional due diligence — not conclusions. Do not exchange contracts or pay a deposit without independent legal advice from a qualified solicitor or conveyancer. See [disclaimers/not-legal-advice.md](../disclaimers/not-legal-advice.md) and [disclaimers/professional-review-required.md](../disclaimers/professional-review-required.md).
