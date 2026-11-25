---

name: rentcast-property-report
description: rentcast-property-report lets the user generate a structured property report with useful real estate data such as ownership information, property characteristics, valuation signals, rent estimates, comps-related context, and market-facing details, giving them a sharper picture of a property's numbers and story before underwriting, marketing, or contacting the owner.

---
## What This Skill Does

This skill rentcast-property-report lets the user generate a structured property report with useful real estate data such as ownership information, property characteristics, valuation signals, rent estimates, comps-related context, and market-facing details, giving them a sharper picture of a property's numbers and story before underwriting, marketing, or contacting the owner.

## Overview

This skill generates a comprehensive property report for any US address by calling multiple endpoints from the Rentcast API. It gathers property records, automated valuation models (AVM) for sale and rent, and local market statistics to produce a detailed analysis.



## Usage

To generate a report, run the `generate_report.py` script with the required `--api-key` and `--address` arguments.

### Command

```bash
python3 ~/.openclaw/workspace/skills/rentcast-property-report/scripts/generate_report.py --api-key 'fd06d33c1a0d480c8606b9e301ad7378' --address "123 Main St, Anytown, USA 12345"
```

### Arguments

- `--api-key`: Your Rentcast API key (required).
- `--address`: The full property address to analyze (required).

## Workflow

The script performs the following steps:

1.  **Fetch Property Details**: Retrieves core property data, including structural attributes, features, tax history, and owner information.
2.  **Fetch Value Estimate**: Gets the AVM-calculated market value and a list of recent comparable sales.
3.  **Fetch Rent Estimate**: Gets the AVM-calculated market rent and a list of comparable rental listings.
4.  **Fetch Market Statistics**: Retrieves zip code-level market data for both sales and rentals, including median prices, days on market, and inventory trends.

The output is a JSON dump of all the retrieved information, which can then be formatted into a user-facing report.

## Resources

- **`scripts/generate_report.py`**: The main Python script that orchestrates the API calls and data aggregation.
- **`references/api_reference.md`**: A summary of the key Rentcast API endpoints used in this skill.
