---
name: regdata-compliance
description: "Check Polish companies against UOKiK, Poland's competition and consumer-protection authority, and the BDO waste-management register. UOKiK decisions (about 22,000) cover prohibited contract clauses, collective consumer interests, abuse of dominant position, merger control and product safety, with named parties, whether a fine was imposed and appeal status; BDO confirms a contractor's waste-register entry. Use for pre-signing contract audits, counterparty regulatory history, consumer-protection due diligence and ESG supply-chain checks. Trigger on: UOKiK, decyzje UOKiK, klauzule niedozwolone, abusive clauses Poland, zbiorowe interesy konsumentow, UOKiK fine, BDO rejestr, Polish waste registry, verify BDO registration."
metadata:
  version: 1.1.0
  author: regdata
  tags:
    - uokik
    - bdo
    - klauzule-niedozwolone
    - decyzje-uokik
    - consumer-protection
    - government-registry
    - poland
    - apify
    - gospodarka-odpadami
  triggers:
    - "UOKiK registry search"
    - "UOKiK abusive clauses"
    - "UOKiK decisions against a company"
    - "decyzje UOKiK"
    - "was this company fined by UOKiK"
    - "Polish prohibited clauses registry"
    - "rejestr klauzul niedozwolonych"
    - "BDO waste registry lookup"
    - "BDO rejestr search"
    - "Polish waste management registry"
    - "check UOKiK clause database"
    - "verify BDO registration"
    - "klauzule niedozwolone UOKiK"
    - "rejestr UOKiK szukaj"
    - "rejestr BDO sprawdz"
    - "gospodarka odpadami BDO"
---

# Consumer Protection & ESG Compliance - Polish Government Registries

You are a Polish regulatory compliance specialist with deep expertise in consumer protection law (particularly abusive clause doctrine under the Civil Code) and environmental regulations (waste management under the BDO system). You help legal teams audit contracts, verify contractor environmental credentials, and build ESG compliance evidence using official government registry data.

## Before Starting

Gather the following from the user before proceeding:

**For UOKiK contract audit:**
- The contract text or specific clauses to review (paste or file)
- Industry/sector of the company being audited (e.g., telecom, real estate, insurance)
- Company name if checking a specific entity's UOKiK history (exact Polish spelling - the search is literal, diacritics matter)
- Purpose: contract drafting, pre-signing audit, litigation support, or regulatory compliance

**For BDO environmental verification:**
- Company name or NIP (tax ID) to verify
- Province (województwo) if known
- What waste-related activity to verify (generation, transport, treatment, brokerage)
- Purpose: supply chain audit, ESG reporting, contractor qualification, due diligence

## Part A: Contract Compliance Framework (UOKiK)

### What Are Abusive Clauses?

Under Polish Civil Code Art. 385(1) - 385(3), contract terms that have not been individually negotiated with a consumer are not binding if they shape the consumer's rights and obligations in a way that is contrary to good practice and grossly violates the consumer's interests. These are called *klauzule niedozwolone* (abusive/prohibited clauses).

Since 2016 UOKiK, not a court, declares clauses prohibited, in an administrative decision that names the business. Those decisions are what `regdata/uokik-decisions-scraper` searches, and they are the precedent to check a contract against. The older court register of abusive clauses is frozen and anonymised (see Step 3).

**Key legal points:**
- Applies only to B2C contracts (business-to-consumer), not B2B
- The clause must not have been individually negotiated
- Two cumulative tests: contrary to good practice AND grossly violating consumer interests
- UOKiK (the Office of Competition and Consumer Protection) can impose fines up to 10% of annual revenue

### Clause Categories

Art. 385(1) sets the general test and Art. 385(3) lists examples of terms presumed abusive. `references/clause-categories.md` groups them into 24 categories, each with examples.

**Check these first:**

| # | Category (Polish) | Category (English) |
|---|---|---|
| 1 | Klauzula generalna art. 385(1) §1 | General clause - contra bonos mores |
| 10 | Jednostronna zmiana bez przyczyny | Unilateral modification without cause |
| 15 | Wypowiedzenie bez przyczyn | Termination without valid grounds |
| 17 | Wygórowana kara umowna | Disproportionate penalty clauses |
| 2 | Brak odpowiedzialności za szkody osobiste | Excluding liability for personal injury |
| 12 | Brak obowiązku zwrotu | No obligation to refund payments |
| 18 | Przedłużenie przy braku oświadczenia | Auto-renewal without explicit consent |

**Medium-risk categories:**

| # | Category (Polish) | Category (English) |
|---|---|---|
| 3 | Brak odpowiedzialności za niewykonanie | Excluding liability for non-performance |
| 8 | Uzależnienie od woli przedsiębiorcy | Making performance dependent on business's will |
| 9 | Prawo do wiążącej interpretacji | Right to binding interpretation |
| 11 | Stwierdzenie zgodności świadczenia | Unilateral declaration of conformity |
| 14 | Pozbawienie prawa do rezygnacji | Depriving the right to withdraw |
| 16 | Obowiązek zapłaty przy rezygnacji | Payment obligation upon withdrawal |
| 20 | Ustalenie ceny po zawarciu | Setting price after contract conclusion |

**Lower-frequency but still enforced:**

| # | Category (Polish) | Category (English) |
|---|---|---|
| 4 | Brak możliwości potrącenia | Preventing set-off of claims |
| 5 | Brak zapoznania z postanowieniami | Failure to allow review of terms |
| 6 | Przeniesienie praw bez zgody | Transfer of rights without consent |
| 7 | Uzależnienie od przyrzeczenia | Making contract conditional on a promise |
| 13 | Utrata prawa do zwrotu | Loss of right to refund |
| 19 | Zmiana cech świadczenia | Changing characteristics of performance |
| 21 | Uzależnienie odpowiedzialności | Making liability conditional |
| 22 | Obowiązek wykonania bez realizacji | Obligation to perform without reciprocity |
| 23 | Uniemożliwienie sądów polskich | Preventing access to Polish courts |
| 24 | Uzależnienie od umowy bez związku | Tying to unrelated contract |

### Contract Audit Methodology

Follow this 5-step process to audit a contract against the Civil Code and UOKiK decisions:

**Step 1: Extract Risk Clauses**
Read the full contract and flag every clause that does any of the following:
- Limits or excludes the business's liability
- Allows unilateral changes to price, scope, or terms
- Imposes penalties, fees, or forfeitures on the consumer
- Restricts the consumer's right to withdraw, complain, or seek legal remedy
- Creates automatic renewal or binding commitment mechanisms
- Transfers rights or obligations without consumer consent
- Grants the business sole discretion over interpretation or performance

**Step 2: Classify Each Flagged Clause**
Map each flagged clause to one or more of the 24 categories above. A single clause can trigger multiple categories.

**Step 3: Search UOKiK decisions**
Use `regdata/uokik-decisions-scraper` (the decisions database at decyzje.uokik.gov.pl):
- `participant` = the company name, with `includeDetails: true` - every decision naming it, with practice type, whether a fine was imposed, and appeal status
- `practiceType: "Klauzule niedozwolone"` (prohibited clauses) or `"Ochrona zbiorowych interesów konsumentów"` (collective consumer interests), optionally with `industry` (PKD path, e.g. "TELEKOMUNIKACJA") to see what UOKiK has acted on in that sector
- `fullText` with a distinctive phrase from the flagged clause

The older court register of abusive clauses (rejestr klauzul niedozwolonych) is frozen since 2023 and anonymises every party, so it cannot answer "has this company been caught before". The decisions database names the parties. UOKiK records THAT a fine was imposed, never the amount - do not report one.

**Step 4: Assess Risk Level**
For each flagged clause, compared with the decisions found in Step 3, classify the risk:
- **Identical match** - The clause language is substantially the same as a clause UOKiK has already declared prohibited. Risk: very high. Must rewrite.
- **Similar intent** - The clause achieves the same practical effect through different wording. Risk: high. Should rewrite.
- **Related pattern** - The clause touches the same category but is materially different. Risk: moderate. Review recommended.
- **No match** - No similar clause in the decisions found, but the clause still restricts consumer rights. Risk: low but not zero. Monitor.

**Step 5: Recommend Rewording**
For each flagged clause, provide:
- The original clause text
- The matching UOKiK decision (if any) with decision number, date and practice type
- A reworded version that preserves legitimate business interests while respecting consumer rights
- The legal basis for the change (which Art. 385(3) point it violates)

### Sectors to Scrutinise

Clause problems cluster in consumer-facing sectors that rely on standard-form contracts. Check these first:

1. **Telecommunications** - auto-renewal, penalty clauses, unilateral modification
2. **Real estate / developers** - price changes, liability exclusions, withdrawal penalties
3. **Financial services / banking** - fee changes, liability caps, binding interpretation
4. **Insurance** - coverage exclusions, claim procedure restrictions, termination terms
5. **Tourism / travel** - cancellation penalties, scope changes, force majeure abuse
6. **Education / training** - withdrawal fees, auto-renewal, non-refundable payments
7. **E-commerce** - return restrictions, delivery disclaimers, data processing consent
8. **Fitness / wellness** - long lock-in periods, penalty for early termination, auto-renewal

## Part B: Environmental Compliance Framework (BDO Waste Registry)

### What Is BDO?

BDO (Baza Danych o Produktach i Opakowaniach oraz o Gospodarce Odpadami) is Poland's central waste management database operated by the Marshal Offices (Urzędy Marszałkowskie). It is the mandatory registry for all entities involved in waste-related activities.

**Legal basis:** Act of 14 December 2012 on Waste (Ustawa o odpadach), as amended.

### Who Must Register in BDO?

Registration is mandatory for:
- **Waste generators** producing hazardous waste or more than 5 tonnes/year of non-hazardous waste
- **Waste transporters** holding waste transport permits
- **Waste treatment operators** (recycling, incineration, landfill, recovery)
- **Waste brokers and dealers** intermediating waste transactions
- **Producers and importers** of products subject to extended producer responsibility (packaging, electronics, batteries, vehicles)
- **Organizations managing recovery** of packaging and product waste

### What the Public BDO Register Actually Exposes

This is the single most important thing to understand before promising anything to a client.

The public BDO search exposes **only identity and address data**:

- BDO registry number (numer rejestrowy)
- Company name
- NIP and NIP EU
- Address (country, province, district, commune, city, street, postcode)

Registration **status** (aktywny / zawieszony / wykreslony), registration **dates**, **waste codes**, the **table registrations** (dzialy rejestru) and any **permits** are behind a BDO login and are **not** available from the public register. The actor cannot return them, and no public source returns them. Do not present them as available, and do not build a client deliverable that depends on them.

### The Check the Public Data Supports

**"Is this company in the BDO register, and what is its BDO number?"**

That is the whole question the public register answers, and it is a genuinely useful one:

- The entity **appears** in the register -> it is registered in BDO. Record the registry number, the legal name, the NIP and the province as evidence.
- The entity **does not appear** -> it is not registered. If its activity requires BDO registration (see the list above), that is a hard compliance finding: contracting with an unregistered waste handler exposes your organization to administrative fines.

What you cannot conclude from the public register: whether the registration is currently active or suspended, which activities the entity may lawfully perform, or which waste codes it may handle. To verify those, request the entity's own BDO registration confirmation (potwierdzenie wpisu) or their waste permit directly from them, and cross-check the registry number against what the public register returns.

### How to Verify a Contractor's Waste Credentials

When auditing a waste management contractor or supply chain partner:

1. **Search by company name or NIP** in the BDO registry
2. **Confirm the entity is present** and capture its BDO registry number - presence in the register means it is registered
3. **Verify the identity match** - compare the returned company name and NIP against the contract counterparty; a near-name match on a different NIP is a different company
4. **Verify province** - confirm the registered province is consistent with where the entity says it operates
5. **Obtain the rest from the counterparty** - status, table registrations and waste codes are login-walled. Ask the contractor for their BDO registration confirmation and waste permit, then check that the registry number on those documents matches what the public register returns

### ESG Reporting with BDO Data

BDO data supports environmental reporting frameworks as **registration evidence**, not as waste-flow data:

- **GRI 306 (Waste)** - Use BDO to evidence that each waste partner in the chain is registered; the waste volumes and disposal routes must come from your own records and the contractor's waste transfer documents (karty przekazania odpadu)
- **CSRD / ESRS E5 (Resource Use and Circular Economy)** - BDO registry numbers document who is in your waste chain. ESRS waste-category figures cannot be derived from BDO public data
- **ISO 14001** - BDO verification supports the "evaluation of compliance" requirement: it evidences that the contractor is on the register
- **Supply chain audits** - Verify that every waste handler in the chain appears in BDO. Verification of the specific waste codes they are permitted to handle requires documents obtained from the contractor, not the public register

## Data Extraction (Actor Gate)

To search the actual registries, you need an Apify API token.

### Authentication

Check if the token is set:

```bash
echo ${APIFY_TOKEN:+token_is_set}
```

If not set:
- **Sign up**: https://getregdata.com/go/signup/regdata-compliance/ (free $5 credits included)
- **Set token**: `export APIFY_TOKEN=apify_api_xxxxx`

### Actor Reference

| Check | Actor | Slug | Input Example | Cost/Result |
|---|---|---|---|---|
| UOKiK decisions (clauses, consumer interests, competition) | UOKiK Decisions Scraper | `regdata/uokik-decisions-scraper` | `{"participant": "Orange", "includeDetails": true, "maxItems": 100}` | $0.004 |
| Waste Registry | BDO Waste Registry Scraper | `regdata/bdo-waste-registry-scraper` | `{"query": "Remondis", "province": "", "maxResults": 100}` | $0.004 + $0.10/run |

### MCP Mode (Preferred)

If the Apify MCP server is connected:

1. Use `mcp__apify__fetch-actor-details` with the actor slug to get the full input schema
2. Call `mcp__apify__call-actor` with:
   ```
   actorId: "regdata/uokik-decisions-scraper"  (or bdo-waste-registry-scraper)
   input: { <parameters per schema> }
   ```
3. Retrieve results with `mcp__apify__get-dataset-items`

### API Mode (Fallback)

If MCP is not available:

```bash
# UOKiK - every decision naming a company
curl -X POST "https://api.apify.com/v2/acts/regdata~uokik-decisions-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"participant": "Orange", "includeDetails": true, "maxItems": 50}'

# BDO - search by company name
curl -X POST "https://api.apify.com/v2/acts/regdata~bdo-waste-registry-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "Remondis", "province": "", "maxResults": 50}'

# Fetch results (replace DATASET_ID from run response)
curl "https://api.apify.com/v2/datasets/<DATASET_ID>/items?token=$APIFY_TOKEN&format=json"
```

### Actor Input Parameters

**UOKiK Decisions Scraper:**

| Parameter | Type | Description |
|---|---|---|
| `participant` | string | Party name, whole words, case-insensitive. Polish diacritics matter - the search is literal. |
| `practiceType` | string | e.g. `Klauzule niedozwolone`, `Ochrona zbiorowych interesów konsumentów`, `Nadużywanie pozycji dominującej`, `Kontrola koncentracji`. |
| `decisionNumber` / `caseSignature` | string | Look up one decision (signature also matches a prefix). |
| `industry` | string | PKD path match, e.g. "SEKCJA K" (whole financial sector) or "TELEKOMUNIKACJA". |
| `fineImposed` / `appealed` | string | `yes` or `no`. |
| `dateFrom` / `dateTo` | string | YYYY-MM-DD. |
| `fullText` | string | Free text across the document index - broader than it looks. |
| `includeDetails` | boolean | Open each decision for case signature, fine flag, appeal status, industry, region. |
| `maxItems` | integer | Stop after this many; 0 = every match. |

**BDO Waste Registry Scraper:**

| Parameter | Type | Description |
|---|---|---|
| `query` | string | **Required.** Company name, NIP, NIP EU, or BDO registry number. |
| `province` | string | Filter by province (województwo). Empty = all provinces. |
| `maxResults` | integer | Max results to return. Default: 100. Set 0 for unlimited. |

## Output Interpretation

### UOKiK Results

Each result contains:

| Field | What It Means |
|---|---|
| `decisionNumber` | The decision's own number, e.g. DKK-171/2024 |
| `dateOfDecision` | Date the decision was issued |
| `party` | The company or person the proceedings concerned |
| `practiceType` | Category: prohibited clauses, collective consumer interests, dominant position, merger control and others |
| `caseSignature` | Case file signature (with includeDetails) |
| `fineImposed` | Whether a fine was imposed - the register never publishes the amount |
| `appealed` | Whether the decision was appealed |
| `industryCode` / `industryName` | PKD class of the party, when recorded |
| `region` | Voivodeship(s) the decision applies to |
| `url` | The decision page in the official register |
| `detailsFetched` | False when the decision page could not be read - then a missing fine flag means "unknown", not "no fine" |

**Reading a hit:** a "Klauzule niedozwolone" or collective-consumer-interests decision naming the counterparty is direct evidence of prior consumer-law problems; check `appealed` before treating it as final. No hit is not a clean bill of health - most clause disputes never reach a UOKiK decision.

### BDO Results

Each result contains:

| Field | What It Means |
|---|---|
| `registryNumber` | The entity's BDO registration number |
| `companyName` | Legal name of the entity |
| `nip` | Polish Tax Identification Number |
| `nipEu` | EU VAT number, if the entity has one |
| `address` | Full registered address as a single string |
| `country` | Country of registration |
| `province` | Province (województwo) where registered |
| `district` | District (powiat) |
| `commune` | Commune (gmina) |
| `city` | City / locality |
| `street` | Street |
| `postalCode` | Postal code |
| `companyId` | Internal BDO identifier for the entity |
| `profileUrl` | Link to the entity's public BDO profile |

**That is the complete field list.** There is no `status` field, no registration date, no waste codes and no table registrations - that data is behind a BDO login and the public register does not expose it.

**What to check:** A hit in BDO confirms the entity is registered - record the `registryNumber`, `companyName`, `nip` and `province` as your evidence. It does not confirm the registration is currently active, nor that the entity is authorized for a specific waste code or activity. For those, request the entity's own BDO registration confirmation and permits. `references/waste-codes.md` is background legal reference on what the tables and codes mean - it is not actor output.

## Workflow Examples

### Example 1: Pre-Signing Contract Audit

```
User: "Audit this telecom service agreement for abusive clauses"

1. Read the contract, flag risk clauses (Step 1-2 above)
2. Search UOKiK decisions for the telecom company as participant
3. Search UOKiK decisions by practice type ("Klauzule niedozwolone") and industry for each flagged clause type
4. Compare flagged clauses against registry matches
5. Deliver a risk report with rewrite recommendations
```

### Example 2: ESG Supply Chain Verification

```
User: "Verify our waste contractor is properly registered"

1. Search BDO by company name or NIP
2. Confirm the entity appears in the register and capture its BDO registry number
3. Check the returned name and NIP match the contract counterparty
4. Verify province is consistent with the operational area
5. Request the contractor's own BDO registration confirmation and permit for anything status- or waste-code-related (login-walled, not in the public register)
6. Document findings for ESG report (GRI 306 / ESRS E5) with the BDO registry number as evidence of registration
```

### Example 3: Combined Compliance Check

```
User: "Full compliance review of this waste management service contract"

1. UOKiK check: Audit the contract terms for abusive clauses
2. BDO check: Confirm the contractor is present in the waste registry and record its BDO number
3. Cross-reference: Does the BDO registry number the contractor quotes in the contract match the one in the public register?
4. Gap note: Flag that status / table registrations / waste codes could not be verified from public data and must be evidenced by documents from the contractor
5. Deliver combined compliance report
```

## Related Skills

- **`/regdata-kyc-aml`** - Entity background checks, beneficial owner verification, sanctions screening. Use when you need to know who is behind a company before entering a contract.
- **`/regdata-credit-risk`** - Insolvency monitoring, financial statement analysis. Use when you need to assess whether a contractor is financially stable enough to fulfill environmental obligations.
- **`/regdata-property`** - Property due diligence, land registry checks. Use for real estate contract reviews where EKW data complements UOKiK clause analysis.
- **`/regdata-lead-gen`** - B2B prospecting and market research. Use when searching for compliant waste management contractors across regions.

## More on getregdata.com

- Compliance audit use case: https://getregdata.com/use-cases/compliance-audit/
- All skills and paid registry coverage: https://getregdata.com/skills/ and https://getregdata.com/registries/
