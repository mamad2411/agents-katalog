---
name: polaris-formatting-currency
description: Format currencies for global merchants. Use this when displaying prices in multi-currency stores, handling store currency vs non-store currency, presentment currency, payout currency, billing currency, short format, explicit format, CLDR localization, currency symbols, ISO codes, decimal separators.
---

# Formatting Localized Currency

Currencies are formatted differently in different countries and languages. The currency formatting framework helps merchants sell globally by localizing currency formatting for merchants and customers everywhere, unifying the display of mixed currencies, and implementing the formatting through APIs.

## Definitions

A store can have more than one type of currency and currency format.

### Store Currency

The main currency of the store and the Shopify default. All sales and reports are shown in the store currency.

### Non-Store Currency

Any other type of currency is called "non-store currency." Types include:
- **Presentment currency:** The type of currency presented to buyers in a merchant's store. Can be different from store currency in multi-currency stores.
- **Payout currency:** The type of currency used to pay merchants for their sales. Can be different from store currency in multi-currency stores.
- **Billing currency:** The type of currency used to bill merchants for themes, app purchases, and monthly subscriptions. Billing currency is in USD only, but might include local currencies for tax purposes.

### Short Format

Includes the currency symbol and currency value. Used for currency that merchants are familiar with.

Examples: $12.50; 12,50 €

### Explicit Format

Includes the currency symbol, currency value, and ISO code. Best used for currency that merchants aren't familiar with and don't expect to see.

Examples: $12.50 CAD; 12,50 € EUR

## Aligning with Global Standards

Shopify uses the Common Locale Database Repository (CLDR) for localization formatting for currency, date, time, and amount. It's the recognized international standard that automatically formats numbers and currency based on the merchant's locale.

CLDR determines:
- Whether the currency symbol appears before or after the amount (e.g., $250, 250 USD, 250 $)
- Whether decimals are used (e.g., no "cents" in Japanese yen)
- Whether the decimal sign is a period or a comma (e.g., 37,50 or 37.50)
- How to group numbers (e.g., 10,000 or 1,0000, or using spaces)

**Important:** CLDR doesn't determine the appropriate level of detail shown in different contexts. For example, it can't determine when to show the currency symbol and value (short format) versus currency symbol, value, and ISO code (explicit format).

Though short format is more efficient, provide clarity for merchants who deal with unfamiliar currencies in multi-currency stores by using explicit format in those cases.

## Design Guidelines

### For Merchants: Store Currency

**Do:**
- Default to short format

**Don't:**
- Use explicit format except when presenting store currency within a mixed-currency context

### For Merchants: Non-Store Currency

- Use explicit format when showing total amounts, an amount within a button, or in a paragraph
- Use short format when showing non-total amounts with total amounts

Example: When the presentment currency is different from store currency, non-total amounts in the paid status card are in short format, and total amounts are in explicit format.

### Negative Amount Display

Always place the negative symbol before the currency and amount in either format.

**Do:**
- -$4.20
- -12,50 €

**Don't:**
- $-4.20
- 12,50 €-

### For Customers

Default to explicit format whenever prices are customer-facing. Use short format for unit prices, itemized prices, and installment prices.

If there are enough indicators to let customers know which currency they're looking at, short format may be sufficient. When using short format, make sure to always use explicit format for cart total, checkout total, and notification totals.

## Guiding Questions for Design Decisions

Use these questions to guide you when making decisions about currency formatting:

1. **Does the merchant know which currency they're looking at?**
   - Which currency do they expect to see?
   - Do they know which currency their orders are in if they have a multi-currency store?

2. **Does the currency format support the merchant's main task?**
   - Is the main task scanning, comparing and analyzing, or taking an action (e.g., refund)?

3. **Are there enough details to make an informed decision?**
   - Do they know the currency of their non-store currency order refund?
   - Can they distinguish between different currency contexts?

4. **Can the UI be simplified without creating confusion?**
   - How can we make currency formatting both simple and accurate?

## Design Tips

- Mock up scenarios where the store, presentment, payout, and billing currencies are all different. This is becoming more common as merchants sell globally.
- Use currencies that share the same symbol to test for clarity (USD, CAD, AUD, HKD, SGD all use "$").
- Use Japanese Yen (JPY) for testing length and space constraints. 1 USD is approximately 100 JPY. If there's enough space for JPY, it should work for most major currencies.
- When in doubt, use the guiding questions to make merchant-focused decisions.

## Major Currencies Reference

| Currency | Locale | Short Format | Explicit Format |
|----------|--------|--------------|-----------------|
| US Dollar ($, USD) | en-US | $12.50 | $12.50 USD |
| Canadian Dollar ($, CAD) | en-CA | $12.50 | $12.50 CAD |
| | fr-CA | 12,50 $ | 12,50 $ CAD |
| Australian Dollar ($, AUD) | en-AU | $12.50 | $12.50 AUD |
| Euro (€, EUR) | de-DE, fr-FR | 12,50 € | 12,50 € EUR |
| | en-IE | €12.50 | €12.50 EUR |
| British Pounds (£, GBP) | en-GB | £12.50 | £12.50 GBP |
| Japanese Yen (¥, JPY) | ja-JP | ¥1250 | ¥1250 JPY |
| New Zealand Dollar ($, NZD) | en-NZ | $12.50 | $12.50 NZD |
| Hong Kong Dollar ($, HKD) | zh-HK | $12.50 | $12.50 HKD |
| Singapore Dollar ($, SGD) | zh-SG | $12.50 | $12.50 SGD |
| Danish Krone (Kr, DKK) | da-DK | 12,50 kr. | 12,50 kr. DKK |

## Implementation

To format currency in a React component, use the Shopify/react-i18n library's formatCurrency method. Select either short or explicit formatting by setting the form option:

```javascript
import { useI18n } from '@shopify/react-i18n';

const [i18n] = useI18n();

i18n.locale = 'de-AT';

const eurDeAt = i18n.formatCurrency(price, {
  currency: 'EUR',
  form: 'short',
});

const eurDeAtExp = i18n.formatCurrency(price, {
  currency: 'EUR',
  form: 'explicit',
});
```
