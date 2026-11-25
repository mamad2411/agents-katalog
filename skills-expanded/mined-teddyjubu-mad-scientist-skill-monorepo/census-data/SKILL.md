---

name: census-data
description: Fetch demographic, economic, and population data from the U.S. Census Bureau API. Use this skill when you need population statistics, housing data, business patterns, income/poverty estimates, or any U.S. government statistical data at national, state, county, metro, tract, or block group levels.
version: 1.0.0
author: James
trigger_phrases:
  - "census data"
  - "population by"
  - "demographic data"
  - "ACS data"
  - "American Community Survey"
  - "county business patterns"
  - "poverty estimates"
  - "housing statistics"
  - "census API"

---
Fetches demographic, economic, housing, and business data from the U.S. Census Bureau Data API.

## What This Skill Does

This skill Fetch demographic, economic, and population data from the U.S. Census Bureau API. Use this skill when you need population statistics, housing data, business patterns, income/poverty estimates, or any U.S. government statistical data at national, state, county, metro, tract, or block group levels.

## When to Use This Skill

Trigger this skill when Charles asks for:
- Population, demographics, or housing data for any U.S. geography
- American Community Survey (ACS) statistics
- Decennial Census data (2000, 2010, 2020)
- Economic indicators (County Business Patterns, Economic Census, trade data)
- Poverty or income estimates (SAIPE)
- Population estimates and projections
- Business statistics by industry and geography
- Any query that needs official U.S. government statistical data

## What This Skill Does

This skill Fetch demographic, economic, and population data from the U.S. Census Bureau API. Use this skill when you need population statistics, housing data, business patterns, income/poverty estimates, or any U.S. government statistical data at national, state, county, metro, tract, or block group levels.

## Available Datasets (Major Categories)

### American Community Survey (ACS)
- **ACS 1-Year** (`acs/acs1`): Areas 65,000+ population, most recent estimates
- **ACS 5-Year** (`acs/acs5`): All geographies down to block group, most detailed
- **ACS Subject Tables** (`acs/acs1/subject`, `acs/acs5/subject`): Themed tables (employment, education, income, etc.)
- **ACS Data Profiles** (`acs/acs1/profile`, `acs/acs5/profile`): High-level summary tables

### Decennial Census
- **2020 Decennial** (`dec/pl`, `dec/dhc`): Redistricting data, demographic and housing
- **2010 Decennial** (`dec/sf1`): Summary File 1 (population and housing by race, age, etc.)
- **2000 Decennial** (`dec/sf1`, `dec/sf3`): Summary Files 1 and 3

### Economic Data
- **County Business Patterns (CBP)** (`cbp`): Establishments, employment, payroll by industry/geography
- **Economic Census** (`ecnbasic`): Comprehensive business data every 5 years
- **Annual Survey of Manufactures** (`asm`): Manufacturing statistics
- **Nonemployer Statistics** (`nonemp`): Businesses with no paid employees
- **Annual Business Survey (ABS)** (`abs`): Business ownership demographics

### Population Estimates
- **Population Estimates** (`pep/population`, `pep/charagegroups`): Annual estimates by age, race, sex
- **Population Projections** (`popproj`): Future population forecasts

### Poverty & Income
- **SAIPE** (`timeseries/poverty/saipe`): Small Area Income and Poverty Estimates (state, county, school district)

### International Trade
- **Exports** (`timeseries/intltrade/exports/enduse`, `timeseries/intltrade/exports/porths`)
- **Imports** (`timeseries/intltrade/imports/enduse`, `timeseries/intltrade/imports/porths`)

### Other
- **Planning Database (PDB)** (`pdb/tract`, `pdb/blockgroup`): Census planning metrics
- **Community Resilience Estimates** (`cre`): Social vulnerability and disaster resilience
- **Health Insurance Statistics (SAHIE)** (`timeseries/healthins/sahie`): Small area health insurance estimates

## Geography Levels

The Census API supports these geography types (use `&for=<geography>:<code>` or `&for=<geography>:*`):

- **us** — United States (code: 1)
- **state** — State (2-digit FIPS, e.g., 01 = Alabama, 24 = Maryland)
- **county** — County (3-digit code within state, e.g., &for=county:*&in=state:24)
- **metropolitan statistical area/micropolitan statistical area** — Metro areas (CBSA codes)
- **place** — Incorporated places (cities, towns)
- **tract** — Census tracts (6-digit code)
- **block group** — Block groups (1-digit code within tract)
- **zip code tabulation area** — ZCTAs (5-digit ZIP approximations)
- **congressional district** — Congressional districts
- **school district** — School districts (elementary, secondary, unified)

### Nested Geographies
Use `&in=` to specify parent geographies:
- `&for=county:*&in=state:24` — All counties in Maryland
- `&for=tract:*&in=state:24&in=county:031` — All tracts in Montgomery County, MD

### Wildcards
Use `*` to get all geographies at a level:
- `&for=state:*` — All 50 states + DC + PR
- `&for=county:*&in=state:24` — All MD counties

## Query Parameters

### Required
- `get=VARIABLE1,VARIABLE2,...` — Variables to retrieve (up to 50, or use `group(TABLEID)` for entire table)

### Geography
- `&for=<geography>:<code>` — Primary geography selector
- `&in=<parent_geography>:<code>` — Parent geography for nested queries

### Predicates (filters)
- **String variables**: `&VARIABLE=value` (can repeat for multiple values; wildcards allowed: `&PORT=21*`)
- **Numeric variables**: `&VARIABLE=100000` or `&VARIABLE=0:500000` (range with colon)
- **Time (time series)**: `&time=2019` or `&time=from+2015+to+2020`

### Output Format
- `&outputFormat=json` (default)
- `&outputFormat=csv` — Returns CSV download

### Labels
- `&descriptive=true` — Adds variable labels as second row in JSON output

## Common Query Patterns

### Example 1: Population by State (2019 ACS 1-Year)
```
https://api.census.gov/data/2019/acs/acs1?get=NAME,B01003_001E&for=state:*&key=YOUR_KEY
```
- `B01003_001E` = Total population estimate

### Example 2: Median Household Income by County in Maryland (2021 ACS 5-Year)
```
https://api.census.gov/data/2021/acs/acs5?get=NAME,B19013_001E,B19013_001M&for=county:*&in=state:24&key=YOUR_KEY
```
- `B19013_001E` = Median household income (estimate)
- `B19013_001M` = Margin of error

### Example 3: All Variables in Table (ACS Table B02015 - Asian Alone by Detailed Group)
```
https://api.census.gov/data/2019/acs/acs1?get=group(B02015)&for=state:*&key=YOUR_KEY
```

### Example 4: County Business Patterns - Establishments by Industry, Montgomery County MD (2021)
```
https://api.census.gov/data/2021/cbp?get=NAME,ESTAB,EMP,PAYANN&NAICS2017=54&for=county:031&in=state:24&key=YOUR_KEY
```
- `NAICS2017=54` = Professional, Scientific, and Technical Services

### Example 5: Population Estimates by Age/Race, All States (2022)
```
https://api.census.gov/data/2022/pep/charagegroups?get=NAME,POP&AGEGROUP=0&RACE=1&for=state:*&key=YOUR_KEY
```

### Example 6: Poverty Estimates for All Counties in Virginia (SAIPE 2021)
```
https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEPOVRTALL_PT,SAEMHI_PT&for=county:*&in=state:51&time=2021&key=YOUR_KEY
```

## Finding Variables

Each dataset has a variables endpoint:
```
https://api.census.gov/data/{year}/{dataset}/variables.json
```

Example for 2021 ACS 5-Year:
```
https://api.census.gov/data/2021/acs/acs5/variables.json
```

Or browse the web interface:
```
https://api.census.gov/data/2021/acs/acs5/variables.html
```

### Common Variable Naming Patterns
- **ACS variables**: `B#####_###E` (estimate), `B#####_###M` (margin of error)
  - B = Base table, C = Collapsed table, S = Subject table, DP = Data Profile
  - Example: `B19013_001E` = Median household income
- **Decennial variables**: Often simpler codes like `P001001` (total population in 2010)
- **Economic variables**: Dataset-specific (e.g., `ESTAB`, `EMP`, `PAYANN` in CBP)

## Variable Groups (Tables)

Use `get=group(TABLEID)` to fetch all variables in a table at once (bypasses 50-variable limit):
```
?get=group(B19001)&for=state:*
```

## Rate Limits

- **Without API key**: 500 requests per IP per day
- **With API key**: Unlimited (fair use expected)

Your API key is stored in `.secrets/census.env` and loaded automatically by the skill.

## Usage

### Simple Natural Language Query
```
Get population by state for 2021
```

### Structured Query
```
census-data --dataset acs/acs5 --year 2021 --variables NAME,B01003_001E --for state:* --output population_by_state.csv
```

## Files

- **SKILL.md** — This file (documentation and API reference)
- **run-census-query.js** — Node.js CLI script to execute Census API queries
- **.secrets/census.env** — API key storage (already configured)
- **examples/** — Sample queries and output

## Error Handling

- **Invalid geography**: Check FIPS codes and nesting (use `&in=` for parent geographies)
- **Variable not in dataset**: Verify variable exists in dataset's `/variables.json` endpoint
- **No data**: Returns `null` values (e.g., small geographies may not have ACS 1-Year data)
- **Rate limit**: Add `&key=` to all requests (already handled by skill)

## Tips

1. **Start with 5-Year ACS** for most demographic queries (most geographies, most reliable)
2. **Use wildcards** to explore: `&for=state:*` or `&for=county:*&in=state:24`
3. **Check variable lists** before querying: `https://api.census.gov/data/{year}/{dataset}/variables.html`
4. **Group queries** for entire tables: `get=group(B19001)` instead of listing 50+ variables
5. **Always include NAME** in your `get=` clause for readable geography labels

## References

- **Census Data API Home**: https://www.census.gov/data/developers/data-sets.html
- **API User Guide**: https://www.census.gov/data/developers/guidance/api-user-guide.html
- **Discovery Tool**: https://api.census.gov/data.html
- **Example Queries by Dataset**: Click any dataset at https://www.census.gov/data/developers/data-sets.html
- **FIPS Codes**: https://www.census.gov/library/reference/code-lists/ansi.html

---

**Author**: James  
**Version**: 1.0.0  
**Last Updated**: 2026-03-08
