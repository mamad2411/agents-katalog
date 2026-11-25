---
name: inventory-tracker
description: |
  Track inventory, costs, sales, and profit. Organize items by location, calculate true profit after all fees, and generate tax reports.

  Triggers when user mentions:
  - "track my inventory"
  - "calculate profit"
  - "inventory spreadsheet"
  - "tax report"
  - "what's my ROI"
---

# Inventory Tracker

Know exactly what you have, what you paid, what it's worth, and what you've made. True profit calculation after ALL costs.

---

## What It Does

Keeps your business organized:
- **Inventory Log** - What you have, where it is, what condition
- **True Profit Calculator** - After fees, shipping, cost of goods
- **Tax Documentation** - Ready for accountant
- **ROI Analysis** - Which items/channels perform best
- **Storage Organization** - Know where everything lives

---

## Inputs (from User Prompt)

| Input | Required | Description |
|-------|----------|-------------|
| `action` | ✅ Yes | Add item, calculate profit, generate report |
| `item_details` | ✅ Yes (for add) | Description, cost, date purchased |
| `sale_details` | ✅ Yes (for profit) | Sale price, fees, shipping |

---

## Inventory Data Structure

### Item Record

```yaml
item_id: "INV-001"
purchase_date: "2026-01-15"
purchase_location: "Goodwill - Midtown"
item_description: "Vintage Levi's 501 Jeans"
brand: "Levi's"
category: "Denim"
size: "28"
era: "1990s"
condition: "GUC"
cost_of_goods: 12.00
cleaning_repair_cost: 0.00
other_costs: 0.00
total_invested: 12.00
storage_location: "Bin A-3"
status: "Listed"  # Options: Unlisted, Listed, Sold, Donated
platforms_listed: ["Poshmark", "Depop"]
list_date: "2026-01-18"
list_price_poshmark: 55.00
list_price_depop: 50.00
```

### Sale Record

```yaml
item_id: "INV-001"
sale_date: "2026-02-10"
platform: "Poshmark"
sale_price: 48.00
platform_fees: 9.60  # 20%
shipping_cost: 0.00  # Buyer paid
payment_processing: 0.00
total_fees: 9.60
net_proceeds: 38.40
total_invested: 12.00
true_profit: 26.40
roi_percent: 220%
days_to_sell: 23
```

---

## True Profit Calculation

### The Real Math

```
Gross Sale Price
- Platform Fees (% of sale)
- Shipping Cost (if seller-paid)
- Payment Processing
- Cost of Goods (what you paid)
- Cleaning/Repair Costs
- Other Costs (gas, supplies)
= TRUE PROFIT
```

### Example Calculation

**Item:** Vintage Levi's 501
**Purchase:** $12 at Goodwill
**Sale:** $48 on Poshmark

```
Sale Price:           $48.00
Platform Fee (20%):   -$9.60
Shipping:             $0.00 (buyer paid)
Cost of Goods:        -$12.00
Cleaning:             $0.00
-------------------------
TRUE PROFIT:          $26.40

ROI: 220%
Margin: 55%
```

---

## Inventory Categories

### By Status

**Unlisted**
- Purchased but not yet photographed
- Being cleaned/repaired
- Backlog to process

**Listed**
- Active on platform(s)
- Track list date and platforms
- Monitor views/likes

**Sold**
- Completed transactions
- True profit calculated
- Removed from active inventory

**Donated/Written Off**
- Unsold after X days
- Damaged beyond repair
- Not worth listing

---

### By Location

**Storage System:**
```
Bin A: Denim & Pants
  A-1: Levi's
  A-2: Other denim
  A-3: Pants

Bin B: Tops
  B-1: Tees & tanks
  B-2: Blouses & button-ups
  B-3: Sweaters

Bin C: Dresses & Skirts
  C-1: Dresses
  C-2: Skirts

Bin D: Outerwear
  D-1: Jackets
  D-2: Coats

Bin E: Accessories
  E-1: Bags
  E-2: Jewelry
  E-3: Scarves & belts
```

---

## Tax Documentation

### Required Records

**Income:**
- Date of sale
- Platform
- Gross sale amount
- Platform fees
- Net income

**Expenses:**
- Cost of goods (date, location, amount)
- Mileage (sourcing trips - track date, locations, miles)
- Shipping supplies (poly bags, tape, labels)
- Equipment (photography, storage, computer)
- Cleaning/repair costs
- Platform subscription fees
- Home office percentage (if applicable)

### Tax Calculations

**Quarterly Estimated Tax:**
```
Net Profit (Income - Expenses)
× Self-Employment Tax Rate (15.3%)
× Income Tax Rate (varies)
÷ 4 = Quarterly Payment
```

**Deductions:**
- Cost of Goods Sold
- Home office space
- Mileage (67 cents/mile in 2024)
- Internet/phone (business portion)
- Education/courses
- Professional services

---

## Performance Metrics

### Key Performance Indicators

**Overall Business:**
- Total Inventory Value (at cost)
- Total Sales (month/quarter/year)
- Average Profit per Item
- Average Days to Sell
- Sell-Through Rate (% listed that sells)
- Return on Investment (ROI)

**By Category:**
- Which categories have highest ROI?
- Which sell fastest?
- Which have highest margins?

**By Platform:**
- Revenue per platform
- Fees per platform
- Average sale price
- Time to sell
- Best categories per platform

**By Sourcing Location:**
- ROI by store
- Cost per item by location
- Hit rate (good finds vs duds)

---

## Reports

### Weekly Activity Report

```markdown
## Week of [Date] - Business Report

### 📦 INVENTORY
- Total Items: [X]
- Listed This Week: [X]
- Sold This Week: [X]
- Awaiting Processing: [X]

### 💰 FINANCIALS
- Gross Sales: $[X]
- Total Fees: $[X]
- Cost of Goods: $[X]
- **NET PROFIT: $[X]**

### 📊 METRICS
- Average Days to Sell: [X]
- Average Profit per Item: $[X]
- ROI: [X]%

### 🎯 TOP PERFORMERS
1. [Item] - $[Profit] profit
2. [Item] - $[Profit] profit
3. [Item] - $[Profit] profit

### ⚠️ ATTENTION NEEDED
- [X] items listed >60 days (consider discounting)
- [X] items unlisted >30 days (need processing)
```

### Quarterly Tax Report

```markdown
## Q[X] 2026 - Tax Summary

### INCOME
Gross Sales: $[X]
Platform Fees: -$[X]
Shipping Costs: -$[X]
**NET INCOME: $[X]**

### EXPENSES
Cost of Goods: $[X]
Mileage ([X] miles): $[X]
Supplies: $[X]
Other: $[X]
**TOTAL EXPENSES: $[X]**

### NET PROFIT
$[X]

### ESTIMATED TAX DUE
Self-Employment Tax (15.3%): $[X]
Income Tax ([X]% bracket): $[X]
**TOTAL ESTIMATED TAX: $[X]**

**QUARTERLY PAYMENT DUE: $[X]**
```

---

## Workflow

### When You Buy Something

1. **Log Purchase:**
   - Date, location, cost
   - Description, brand, size
   - Assign item ID
   - Photo for records

2. **Process Item:**
   - Clean/repair if needed
   - Photograph
   - Measure
   - Grade condition

3. **List Item:**
   - Update status to "Listed"
   - Record platforms
   - Record list prices
   - Assign storage location

4. **When It Sells:**
   - Record sale details
   - Calculate true profit
   - Remove from storage
   - Ship to buyer

5. **Monthly:**
   - Review unsold inventory
   - Consider price drops
   - Plan donations

---

## Examples

### Example 1: Add New Item

**User prompt:**
```
@inventory-tracker Add item: Vintage Levi's 501, bought at Goodwill today for $15, size 28, GUC
```

**Expected behavior:**
- Assign item ID (e.g., INV-047)
- Record details
- Calculate total investment
- Suggest storage location
- Add to "unlisted" queue

### Example 2: Calculate Profit

**User prompt:**
```
@inventory-tracker I sold that Patagonia fleece for $65 on Poshmark. I paid $18 for it.
```

**Expected behavior:**
- Calculate Poshmark fee ($13)
- Calculate net proceeds ($52)
- Calculate true profit ($34)
- Calculate ROI (189%)
- Update inventory status to "Sold"

### Example 3: Tax Report

**User prompt:**
```
@inventory-tracker Generate Q1 tax report
```

**Expected behavior:**
- Sum all Q1 income
- Sum all Q1 expenses
- Calculate net profit
- Calculate estimated tax
- Format for accountant

---

## Common Gotchas & Solutions

| Issue | Solution |
|-------|----------|
| Forgot to log purchase | Estimate based on receipts/memory |
| Don't know true fees | Use platform fee calculator |
| Missing receipts | Log immediately going forward |
| Storage chaos | Implement bin system with locations |
| Don't track mileage | Start now; estimate past trips |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Feb 2026 | Initial release - Inventory tracking, true profit calc, tax docs |
