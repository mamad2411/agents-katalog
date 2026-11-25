---
name: zapier-formatter
description: "Utilize Formatter by Zapier for complex data parsing, text manipulation, date/time formatting, and line-item operations."
---

# Zapier Formatter Skill

## Overview
Formatter by Zapier is the Swiss Army knife for manipulating data between steps. This skill focuses on transforming data to ensure compatibility between different applications.

## Core Capabilities

### 1. Text Manipulation
- **Extract Pattern:** Use Regular Expressions (Regex) to pull specific data (like an ID or email) from a block of text.
- **Split Text:** Break a string into multiple parts based on a separator (e.g., splitting a full name into First and Last name).
- **Replace/Capitalize:** Clean up inconsistent data inputs.

### 2. Date / Time Formatting
- Different apps expect dates in different formats (e.g., ISO 8601 vs. Unix Timestamp).
- Formatter can convert timezones, add/subtract time (e.g., `+1 day`), and format output strings exactly as needed (e.g., `YYYY-MM-DD`).

### 3. Numbers
- **Spreadsheet-style formulas:** Perform basic math calculations.
- **Format Number:** Standardize currency or decimal places.

### 4. Utilities
- **Line-item to Text / Text to Line-item:** Essential when moving data from an app that provides arrays (like Shopify line items) to an app that expects a single string (like an email), or vice versa.
- **Lookup Table:** Map values from one system to another (e.g., mapping "Lead" to ID "1", "Customer" to ID "2").

## Best Practices
- **Chain Formatters:** Don't be afraid to use multiple Formatter steps in a row (e.g., Extract Text -> Split Text -> Lookup Table).
- **Regex Testing:** Always test your Regular Expressions externally (e.g., on regex101.com) using Zapier's flavor of regex (Python-based).
- **Timezones:** Be extremely careful with timezones; always verify the input timezone and the desired output timezone.

## Common Scenarios
- Extracting order numbers from an incoming email body.
- Converting line items from an invoice into a readable list for a Slack message.
- Standardizing phone numbers before sending them to a CRM.
