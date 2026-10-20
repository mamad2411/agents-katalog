# vat-optimization

VAT/GST optimization and compliance.

## When to Activate

- Structuring transactions to optimize VAT recovery
- Assessing VAT treatment of cross-border supplies (goods and services)
- Implementing reverse charge or use tax mechanisms
- Evaluating whether to form a VAT group
- Dealing with partial exemption and input tax attribution
- Setting up e-commerce VAT compliance (OSS/IOSS)
- Preparing for a VAT audit or managing a VAT refund claim
- Building a VAT compliance calendar across multiple jurisdictions

## Core Concepts

### VAT Mechanics (Input/Output)

VAT is a consumption tax collected at each stage of the supply chain. The business acts as a collection agent — it charges output VAT on sales and recovers input VAT on purchases. The net amount is remitted to (or refunded by) the tax authority.

- **Output VAT**: VAT charged on taxable supplies made by the business
- **Input VAT**: VAT incurred on purchases used for making taxable supplies — fully recoverable if attributable to taxable activities
- **Net VAT position**: Output VAT minus input VAT. Positive = payment due; negative = refund claim
- **Exempt supplies**: No output VAT charged, but input VAT on related costs is irrecoverable (e.g., financial services, insurance, healthcare in many jurisdictions)
- **Zero-rated supplies**: Output VAT at 0%, but input VAT is fully recoverable (e.g., exports, certain food items)

### Reverse Charge Mechanism

Shifts the obligation to account for VAT from the supplier to the customer. Eliminates the need for the supplier to register in the customer's jurisdiction.

- **B2B cross-border services**: General rule — reverse charge applies in the customer's jurisdiction (EU Article 44, Place of Supply rules)
- **Domestic reverse charge**: Applied in specific sectors to combat fraud (e.g., construction, electronics, metals in EU member states)
- **Import VAT deferral**: Some jurisdictions allow postponed accounting — VAT on imports declared and recovered on the same return, eliminating cash flow cost

### Cross-Border Services (B2B vs. B2C)

- **B2B general rule**: Taxed where the customer is established — customer accounts for VAT via reverse charge
- **B2C general rule**: Taxed where the supplier is established — supplier must register and charge local VAT
- **Exceptions**: Immovable property services (where the property is located), passenger transport (where it takes place), cultural/entertainment (where performed), telecommunications/broadcasting/electronic services (where the consumer is located for B2C)

### VAT Grouping

Multiple related entities treated as a single taxable person for VAT purposes. Intra-group transactions fall outside the scope of VAT.

- **Benefits**: Eliminates irrecoverable VAT on intra-group supplies (especially relevant when one member makes exempt supplies), simplifies compliance
- **Risks**: Joint and several liability for all group members; administrative complexity on formation/dissolution
- **Eligibility**: Typically requires financial, economic, and organizational links between entities
- **Not available everywhere**: Some jurisdictions do not offer grouping; others limit it to specific sectors

### Partial Exemption

When a business makes both taxable and exempt supplies, input VAT must be apportioned.

- **Direct attribution**: Input VAT directly attributable to taxable supplies is fully recoverable; input VAT on exempt supplies is not
- **Residual input tax**: Overhead costs that cannot be directly attributed are apportioned using a method — typically based on the ratio of taxable to total supplies (turnover-based)
- **Special methods**: Negotiated with the tax authority to achieve a fairer result (e.g., headcount, floor space, transaction count)
- **Annual adjustment**: Provisional recoveries during the year are adjusted against the actual annual ratio
- **De minimis**: If exempt input tax falls below a threshold (e.g., GBP 7,500 per year and less than 50% of total input tax in the UK), full recovery is permitted

### E-Commerce VAT (OSS/IOSS)

- **One-Stop Shop (OSS)**: Single VAT registration for reporting B2C supplies of services and intra-EU distance sales of goods. Eliminates need for multiple registrations
- **Import One-Stop Shop (IOSS)**: For goods imported in consignments not exceeding EUR 150. VAT collected at point of sale, goods cleared without import VAT
- **Deemed supplier rules**: Marketplaces/platforms may be deemed the supplier for VAT purposes — responsible for collecting and remitting VAT
- **Threshold**: EU distance selling threshold is EUR 10,000 aggregate across all member states — above this, VAT is due in the destination state

### VAT Recovery

- **Foreign VAT refunds**: 8th Directive (EU-to-EU) and 13th Directive (non-EU to EU) refund mechanisms. Strict deadlines — typically September 30 of the following year
- **Blocked items**: Some input VAT is non-recoverable by law (e.g., entertainment, passenger cars, employee benefits — varies by jurisdiction)
- **Time limits**: Input VAT must generally be claimed within a fixed period (often 4 years from the supply)
- **Supporting documentation**: Valid VAT invoice with all required particulars (supplier/customer names, VAT numbers, description, rate, amount)

### Compliance Calendar

VAT compliance involves recurring filing obligations that vary by jurisdiction, registration status, and transaction volume.

- **Periodic returns**: Monthly, quarterly, or annually depending on jurisdiction and turnover
- **Intrastat / EC Sales List**: Reporting of intra-EU movements of goods and supplies of services
- **SAF-T / digital reporting**: Real-time or near-real-time invoice reporting (e.g., Italy SdI, Spain SII, Poland KSeF)
- **Payment deadlines**: Typically aligned with return deadlines, but can differ — late payment triggers interest and penalties

## Methodology

1. **Transaction mapping**: Classify all supply chains by type (goods, services, IP), direction (domestic, cross-border), and customer type (B2B, B2C)
2. **Place of supply determination**: Apply the correct rule for each transaction type to identify which jurisdiction's VAT applies
3. **Rate and exemption analysis**: Determine the applicable rate (standard, reduced, zero, exempt) for each supply
4. **Input VAT recovery assessment**: Identify all input VAT, attribute directly where possible, apply partial exemption method for residual
5. **Structure optimization**: Evaluate VAT grouping, supply chain restructuring (e.g., flash title arrangements), and import deferral schemes
6. **Registration review**: Confirm all required registrations are in place; assess whether OSS/IOSS simplifies compliance
7. **Compliance framework**: Build a calendar of filing and payment deadlines, assign responsibilities, implement controls

## Templates

### VAT Recovery Analysis

```
Category              | Input VAT | Attributable to | Recovery
                      | (EUR K)   |                 |
----------------------|-----------|-----------------|----------
Direct — taxable      | 850       | Taxable sales   | 100%
Direct — exempt       | 120       | Exempt (finance)| 0%
Residual (overhead)   | 400       | Mixed           | 82% (*)
                      |           |                 |
Total input VAT       | 1,370     |                 |
Recoverable           | 1,178     |                 | 86%
Irrecoverable         | 192       |                 | 14%

(*) Partial exemption ratio: Taxable turnover / Total turnover = 82%

Optimization options:
  - VAT grouping to eliminate irrecoverable VAT on interco management fees
  - Renegotiate special method based on headcount (estimated recovery: 88%)
  - Review blocked items — some may qualify under capital goods scheme
```

### Cross-Border VAT Decision Matrix

```
Supply Type          | B2B              | B2C
---------------------|------------------|---------------------------
Services (general)   | Reverse charge   | Supplier's country (or OSS)
Goods (intra-EU)     | Zero-rate + ESL  | Destination VAT (or OSS)
Goods (import)       | Import VAT + RC  | Import VAT (or IOSS < EUR 150)
Digital services     | Reverse charge   | Consumer's country (OSS)
Property services    | Where property   | Where property
Transport            | Where performed  | Where performed
```

### VAT Compliance Calendar (Example)

```
Jurisdiction | Return Frequency | Filing Deadline    | Payment Deadline   | Additional
-------------|-----------------|--------------------|--------------------|------------
Germany      | Monthly         | 10th of following  | 10th of following  | Annual return by May 31
France       | Monthly         | 19th-24th          | Same as filing     | DEB/DES for intra-EU
Netherlands  | Quarterly       | End of month +1    | Same as filing     | ICP listing
UK           | Quarterly       | 1 month + 7 days   | Same as filing     | MTD digital links required
Italy        | Monthly         | 16th of following  | Same as filing     | SdI e-invoicing mandatory
```

## Quality Gate

- [ ] All supplies classified by type, direction, and customer category
- [ ] Place of supply determined correctly for each transaction type
- [ ] VAT registration obligations mapped — no unregistered activity in any jurisdiction
- [ ] Reverse charge applied where required; self-assessment documented
- [ ] Partial exemption method applied and documented; special method considered if beneficial
- [ ] Input VAT on blocked items excluded from recovery
- [ ] Foreign VAT refund claims filed before statutory deadlines
- [ ] All invoices contain required VAT particulars
- [ ] Compliance calendar maintained with filing and payment deadlines
- [ ] E-commerce platform obligations assessed (deemed supplier rules)
- [ ] VAT grouping evaluated for groups with exempt members
- [ ] SAF-T or digital reporting requirements met in applicable jurisdictions
