---
name: cimis-cli
description: Query California Irrigation Management Information System (CIMIS) weather data using the cimis CLI. Use when working with irrigation data, weather stations, ET0 (evapotranspiration), or when the user mentions CIMIS, California weather, irrigation scheduling, or cimis.
---

# CIMIS CLI

Query California Irrigation Management Information System (CIMIS) data using the `cimis` command-line tool.

## Prerequisites

```bash
cimis --version
cimis auth status
```

## Authentication

- API key from CIMIS
- Environment variable: `CIMIS_API_KEY`

## Weather Stations

```bash
cimis stations list --active
cimis stations get STATION_ID
cimis stations nearby --zip 95354 --radius 50
```

## Weather Data

### Daily Data

```bash
cimis data daily --station 171 --start 2024-06-01 --end 2024-06-30
cimis data daily --station 171 --days 7 --fields eto,humidity,temp
```

### Hourly Data

```bash
cimis data hourly --station 171 --date 2024-06-15
cimis data hourly --station 171 --start 2024-06-01T00:00 --end 2024-06-01T23:59
```

## ET0 & Irrigation

```bash
cimis eto --station 171 --start 2024-06-01 --end 2024-06-30 --crop coef
cimis waterbudget --station 171 --crop alfalfa --start 2024-06-01
```

## Export & Analysis

```bash
cimis export --station 171 --start 2024-01-01 --end 2024-12-31 --format csv
cimis summary --station 171 --month 6 --year 2024
```

## Agent Best Practices

1. **Station selection**: Use `nearby` for location-based queries
2. **Date formats**: ISO 8601 or YYYY-MM-DD
3. **Fields filtering**: Request only needed fields for faster queries
4. **Units**: Default is metric; use `--imperial` for US units
