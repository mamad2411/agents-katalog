---

name: melissa-data-information
description: melissa-data-information lets the user look up a single property address or process a CSV of multiple addresses to enrich them with Melissa Data property and ownership information, which is useful when they want to verify addresses, get property characteristics, or add structured property data to leads without manual research.

---
## What This Skill Does

This skill melissa-data-information lets the user look up a single property address or process a CSV of multiple addresses to enrich them with Melissa Data property and ownership information, which is useful when they want to verify addresses, get property characteristics, or add structured property data to leads without manual research.

## Overview

This skill allows you to access detailed property information from the Melissa Data API, including owner details, assessed value, last sale price, and physical characteristics. It supports both single address lookups and batch processing of addresses from a CSV file.

## Single Address Lookup

To look up a single address, use the `melissa_property_lookup.py` script with the `--address` argument. The license key is required.

```bash
python3 ~/.openclaw/workspace/skills/melissa-data-information/scripts/melissa_property_lookup.py --license-key 'G_iXMbf6s35rOsEeomwnam**nSAcwXpxhQ0PC2lXxuDAZ-**' --address '22382 Avenida Empresa Rancho Santa Margarita, CA 92688'
```

The output will be a JSON object containing the property details.

## Batch Processing from CSV

To process multiple addresses from a CSV file, use the `--input-csv` argument. The script will create a new CSV file with the enriched data.

**Input CSV Format:**

The input CSV must contain a header row, and one of the columns must contain the full address.

Example `addresses.csv`:
```csv
address,city,state,zip
"22382 Avenida Empresa","Rancho Santa Margarita","CA","92688"
"123 Main St","Anytown","USA","12345"
```

**Command:**

```bash
python3 ~/.openclaw/workspace/skills/melissa-data-information/scripts/melissa_property_lookup.py --license-key 'G_iXMbf6s35rOsEeomwnam**nSAcwXpxhQ0PC2lXxuDAZ-**' --input-csv 'path/to/addresses.csv' --output-csv 'path/to/output.csv' --address-column 'address'
```

- `--address-column`: Specifies the name of the column containing the addresses (defaults to 'address').
- `--output-csv`: Specifies the path for the output file (defaults to 'output.csv').

## Resources

### `scripts/melissa_property_lookup.py`

A Python script to look up property data from the Melissa API. It supports both single address lookup and batch processing from a CSV file.

### `references/api_reference.md`

A summary of the Melissa Property API endpoints and key data groups.
