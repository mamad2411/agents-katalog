# Skill: Receipt & Slip Parser

Parse receipt images and payment slip screenshots to extract transaction data for Actual Budget.

## Supported Slip Types

| Type | Description | Examples |
|------|-------------|----------|
| **Bank Transfer** | Domestic bank transfers, P2P payments | Zelle, bank app screenshots, wire confirmations |
| **E-Receipt** | Digital receipts from online purchases | Amazon, PayPal, Venmo confirmations |
| **Food Delivery** | Food and grocery delivery receipts | DoorDash, UberEats, Instacart |
| **Credit Card** | Credit card transaction slips | POS receipts, online charge confirmations |
| **Mobile Payment** | Mobile wallet transactions | Apple Pay, Google Pay, Cash App |

## Extraction Protocol

When you receive an image, extract these fields:

| Field | Format | Rule |
|-------|--------|------|
| `date` | YYYY-MM-DD | Parse from slip; default to today if not visible |
| `amount` | Number | Negative = expense, positive = income (see Amount Rules) |
| `payee` | String | Merchant name, recipient, or shop name |
| `account` | String | Detect from bank logo/colors or ask user; fall back to default |
| `notes` | String | Transaction ref, order ID, item summary |

## Bank / Institution Detection

Customize these rules for the banks and payment services used in your country. The agent uses visual cues (logos, colors, UI layout) to identify the source institution.

### Example Detection Rules

These are examples using Thai banks. Replace or extend with your own:

| Bank / Service | Detection Cues | Account Code |
|----------------|---------------|--------------|
| Bank of America | Blue logo, BofA header | Checking |
| Chase | Blue octagon logo, chase.com | Credit Card |
| Wells Fargo | Red-yellow stagecoach logo | Savings |
| PayPal | Blue PP logo, paypal.com | Checking |
| Venmo | Blue "V" logo, @usernames | Checking |

**Thai bank examples** (for users in Thailand):

| Bank | Detection Cues | Account Code |
|------|---------------|--------------|
| KBank | Green gradient, K PLUS | KBank |
| SCB | Purple theme, SCB EASY | SCB |
| Bangkok Bank | Blue/dark blue, BBL logo | BBL |
| Krungthai | Light blue, KTB logo | KTB |
| PromptPay | QR code with PromptPay branding | Default |

> **Tip:** Add your own bank detection rules by noting the logo colors, app UI patterns, and header text that appear on your payment slips.

## Field Mapping Examples

### Bank Transfer Slip
```
Image shows: Green header, "K PLUS", amount 350, to "Coffee Shop", ref ABC123
Extracted:
  date:    2026-03-01      (from slip date field)
  amount:  -350            (expense - money going out)
  payee:   Coffee Shop     (recipient name)
  account: KBank           (green = KBank detection)
  notes:   Ref: ABC123     (transaction reference)
```

### Credit Card Receipt
```
Image shows: POS receipt, Visa ending 4532, total $47.80, "Mario's Pizza"
Extracted:
  date:    2026-03-01      (from receipt date)
  amount:  -47.80          (expense)
  payee:   Mario's Pizza   (merchant name)
  account: Credit Card     (credit card transaction)
  notes:   Visa *4532      (card identifier)
```

### Income / Deposit
```
Image shows: Direct deposit notification, $3200, from "Acme Corp", ref PAYROLL
Extracted:
  date:    2026-02-28      (from notification date)
  amount:  3200            (positive = income)
  payee:   Acme Corp       (payer name)
  account: Checking        (deposit target account)
  notes:   Payroll deposit  (description)
```

### Food Delivery
```
Image shows: UberEats receipt, total $28.50, "Thai Basil Restaurant", order #UE-9876
Extracted:
  date:    2026-03-01      (from receipt)
  amount:  -28.50          (expense, includes delivery fee + tip)
  payee:   Thai Basil Restaurant (restaurant name)
  account: Credit Card     (payment method shown)
  notes:   UberEats #UE-9876, incl delivery + tip
```

## Amount Rules

| Condition | Sign | Examples |
|-----------|------|----------|
| Money going OUT (purchases, bills, transfers to others) | **Negative** (-) | -90, -350, -47.80 |
| Money coming IN (salary, refunds, incoming transfers) | **Positive** (+) | 3200, 150, 42.00 |
| Transfer between OWN accounts | **Negative** on source, **Positive** on destination | -1000 from Checking, +1000 to Savings |

**Currency:** Use the raw number from the slip. The currency symbol is configured in USER.md.

## After Extraction: Add Transaction

Once all fields are extracted, add the transaction to Actual Budget:

```bash
# Local Windows path for this workspace
node c:/Users/dhana/Desktop/telegram-openclaw/integrations/add-transaction.js \
  '{"amount":-350,"payee":"Coffee Shop","notes":"Ref: ABC123","date":"2026-03-01","account":"Checking"}'
```

Then confirm to the user:
```
Logged!
<date emoji> 01 Mar | <money emoji> -$350 | <shop emoji> Coffee Shop | <bank emoji> Checking
```

## Edge Cases

| Situation | Action |
|-----------|--------|
| **Blurry / unreadable image** | Ask the user for a clearer photo. Never guess amounts. |
| **Multiple transactions in one image** | Extract each separately and confirm all before logging. |
| **Amount seems unusually large** | Double-check with user: "This shows $X,XXX -- want me to log it?" |
| **Can't detect bank / account** | Use the user's default account from USER.md; mention which account was used. |
| **Foreign currency** | Log the amount as-is with currency note. Let the user decide on conversion. |
| **Duplicate slip** | Check recent transactions before adding. Warn if a matching entry exists. |
| **Partial receipt** | Extract what's visible. Ask for missing required fields (amount is mandatory). |
| **QR code only** | QR codes alone don't contain transaction data. Ask for the confirmation screen. |
| **Voided / cancelled transaction** | Do NOT log. Inform the user the transaction was cancelled. |
