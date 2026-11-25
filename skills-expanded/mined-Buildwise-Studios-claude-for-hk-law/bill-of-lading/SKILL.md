---
name: bill-of-lading
description: >
  Guide legal practitioners through the review, drafting, and analysis of bills of lading and analogous shipping documents under the Bills of Lading and Analogous Shipping Documents Ordinance (Cap 440) and the Hague-Visby Rules.
---
# Bill of Lading — Skill

## Purpose

Guide legal practitioners through the review, drafting, and analysis of bills of lading and analogous shipping documents under the Bills of Lading and Analogous Shipping Documents Ordinance (Cap 440) and the Hague-Visby Rules.

## Scope

- Types of shipping documents (bill of lading, sea waybill, ship's delivery order)
- Cap 440 — rights, liabilities, and immunities of carrier and shipper
- Hague-Visby Rules — mandatory application
- Electronic bills of lading (eBL)
- Title to sue and liabilities of the holder
- Documentary credits and letters of credit
- Dispute resolution and jurisdiction clauses

## Workflow

### 1. Identify the Document Type

| Document | Function | Negotiable | Document of Title |
|----------|----------|------------|-------------------|
| **Bill of Lading** | Receipt, contract, document of title | Yes (order/to bearer) | Yes |
| **Sea Waybill** | Receipt, contract | No | No |
| **Ship's Delivery Order** | Delivery instruction | No | Limited |
| **Electronic Bill of Lading** | Same as paper B/L | Yes | Yes (recognised under Cap 440) |
| **Straight Bill of Lading** | Consigned to named party, non-negotiable | No | Limited |

### 2. Review Key Clauses

**Carriage terms:**
- Carrier identity and registered address
- Description of goods (marks, numbers, quantity, weight)
- Apparent order and condition of goods ("clean" vs "claused")
- Port of loading and discharge
- Vessel name and voyage number
- Place of delivery (if combined transport)

**Contractual terms:**
- Paramount clause (incorporation of Hague-Visby Rules)
- Limitation of liability (Hague-Visby Art IV Rule 5: 666.67 SDR per package or 2 SDR/kg, whichever higher)
- Time bar (Hague-Visby Art III Rule 6: 1 year from delivery)
- Jurisdiction and arbitration clause
- General average clause (York-Antwerp Rules)
- Both-to-blame collision clause
- Himalaya clause (extending defences to servants/agents)

### 3. Assess Mandatory Application of Cap 440

Cap 440 applies (mandatorily) to:
- Bills of lading issued in Hong Kong
- Carriage from a Hong Kong port
- Contracts evidenced by a bill of lading governed by HK law

**Effect of mandatory application:**
- Hague-Visby Rules are incorporated as schedule to Cap 440
- Any clause derogating from carrier's liability is void (Art III Rule 8)
- Carrier must exercise due diligence to make the ship seaworthy (Art III Rule 1)
- Carrier liable for loss/damage from failure to load, stow, carry, and discharge properly

### 4. Title to Sue

Under Cap 440, the following have title to sue and are subject to liabilities:
- **The lawful holder** of the bill of lading (s.4)
- **The consignee** identified in the sea waybill (s.5)
- **The person entitled to delivery** under a ship's delivery order (s.6)

**Transfer of rights:**
- Rights pass to the holder as if they were a party to the contract of carriage
- Liabilities pass to the holder only when they take or demand delivery
- The original shipper remains liable until transfer of the bill

### 5. Electronic Bills of Lading (eBL)

- Recognised as equivalent to paper bills under Cap 440
- eBL system (e.g., Bolero, essDOCS, WAVE, TradeLens)
- Must be functionally equivalent (title, transfer, endorsement)
- Requirements: reliable method, authentication, record integrity
- Increasing adoption by major carriers (MSC, Maersk, CMA CGM)

### 6. Documentary Credits (UCP 600)

**Essential requirements for LC compliance:**
- "Clean on board" notation
- Issued by the carrier or their authorised agent
- Description of goods consistent with the LC
- Full set of originals presented
- Date of issuance no later than the shipment date
- No adverse clauses regarding condition of goods

**Common discrepancies:**
- Late shipment / late presentation
- Insufficient insurance cover
- Description of goods mismatch
- Missing or illegible endorsements
- Unauthorised charterparty bill

### 7. Time Bar and Claims

- **Hague-Visby time bar:** 1 year from delivery or the date when goods should have been delivered
- **Cap 440 time bar:** Consistent with Hague-Visby
- **Extension:** Carrier may agree to extend (in writing)
- **Indemnity claims:** Time may run from settlement of the main claim

## Key Case Law

- **Cargill International SA v M/V "NHK Bulk" [2021] HKCFI** — cargo claim under Cap 440
- **The "Eurus" [2017] HKCFI** — clean bill and estoppel
- **Pioneer Shipping v BTP Tioxide Ltd [2022] HKCA** — Himalaya clause effectiveness
- **The "Nordic Star" [2019] HKCFI** — time bar and extension
- **MSC Mediterranean Shipping Co v Cargill [2020] HKCFI** — eBL recognition

## Practice Notes

- Always check whether Cap 440 applies mandatorily — if so, Hague-Visby Rules cannot be contracted out
- Clausing a bill of lading makes it "unclean" — effects on LC and title to sue
- The 1-year time bar is strict and starts from actual or constructive delivery — mark your diary on day 1
- For combined transport, check whether the loss occurred at sea (Hague-Visby) or on land (CMR or local law)
- eBL adoption is growing fast — ensure advice covers the bespoke system terms (Bolero Rulebook, etc.)
- Cargo receivers should present original bills before delivery — delivery without surrender creates liability for the carrier


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
