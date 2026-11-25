---
name: list-manager
description: Use when organizing and managing categorized listings with search tools. Handles apartment listings, inventory, and structured data.
category: productivity
---

# List Manager

## Overview
Organizes and manages categorized listings with search tools. Handles apartment listings, inventory, classifieds, and any structured data that needs sorting, filtering, and searching.

## When to Use
- Managing apartment or rental property listings
- Organizing inventory, product catalogs, or asset registers
- Sorting and filtering classified ads or job postings
- Building a searchable directory of items with multiple attributes
- Comparing listings across multiple dimensions (price, location, specs)

## How It Works
Accepts listings in various formats (CSV, JSON, free text, links). Structures them into a searchable, filterable collection. Supports sorting by any field, full-text search, and exports.

## Steps
1. Accept listing data: paste, upload, or fetch from URLs
2. Parse and structure: identify columns/fields, normalize values
3. Index for search: enable full-text and attribute-based filtering
4. Present interactive options: sort, filter, search, compare
5. Flag duplicates, stale entries, or outliers
6. Export filtered results in CSV, markdown table, or spreadsheet format

## Common Pitfalls
- Inconsistent field names across sources — normalize during import
- Large datasets causing slow search — use indexing and pagination
- Losing sort/filter state between sessions
- Not handling missing or null values gracefully
- Forgetting to timestamp entries for staleness detection
