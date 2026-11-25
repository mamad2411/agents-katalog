---

name: mad-census-baby
description: Fetches demographic and census data from the US Census Bureau API based on user-provided location information (city, state, zip code, or address). Outputs data in markdown, CSV, or basic PDF format. Use this skill when you need to retrieve population, housing, or economic data for a specific geographic area.

---
This skill provides a programmatic interface to the US Census Bureau API.

## What This Skill Does

This skill Fetches demographic and census data from the US Census Bureau API based on user-provided location information (city, state, zip code, or address). Outputs data in markdown, CSV, or basic PDF format. Use this skill when you need to retrieve population, housing, or economic data for a specific geographic area.

## Usage

To use this skill, you need to provide location information (e.g., city, state, zip code, or a full address) and specify your desired output format.

**Census API Key:** The API key is configured as a skill environment variable.

## Available Commands

Currently, this skill executes a Python script to fetch and process data.

### `scripts/census_data_fetcher.py`

This script will:
1. Accept location parameters.
2. Make a request to the configured Census API.
3. Parse the JSON response.
4. Format the output based on the requested format.

## Input Parameters:

-   `location_type`: (e.g., `address`, `city-state`, `zip`)
-   `location_value`: (e.g., `"1600 Amphitheatre Parkway, Mountain View, CA"`, `"New York, NY"`, `"10001"`)
-   `output_format`: (`markdown`, `csv`, `pdf`)

## Example

To fetch data for a specific city and state in markdown format:

```bash
exec scripts/census_data_fetcher.py --location-type city-state --location-value "Springfield, IL" --output-format markdown
```

## API Reference

For details on available Census API endpoints and variables, refer to:
[references/census_api_guide.md](references/census_api_guide.md)
