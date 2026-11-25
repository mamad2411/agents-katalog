---
name: dynamic-resource-aggregator
description: Use when aggregating resources from multiple sources into structured tables. Parses links and creates organized breakdowns of content.
category: productivity
---

# Dynamic Resource Aggregator

## Overview
Aggregates resources from multiple sources into structured tables. Parses links and creates organized breakdowns of content, making it easy to compare, filter, and export curated collections.

## When to Use
- Compiling resources from multiple web pages, articles, or databases
- Creating comparison tables from disparate sources
- Parsing lists of links into structured, sortable data
- Building curated resource directories for a topic
- Extracting and normalizing data from unstructured web content
- Generating markdown or CSV tables from aggregated data

## How It Works
Ingests URLs, raw text, or uploaded lists. Parses content to extract structured data points (title, description, source, date, category). Outputs organized tables with consistent formatting and optional filtering.

## Steps
1. Accept input: URLs, text dumps, file uploads, or manual entries
2. Parse each source to extract key metadata fields
3. Normalize data: consistent date formats, deduplication, category mapping
4. Structure into a table (markdown, CSV, or spreadsheet)
5. Allow user to filter, sort, or reorder columns
6. Export final result in the requested format

## Common Pitfalls
- Over-aggregating — too many columns or sources make the table unusable
- Parsing errors from sites with inconsistent or dynamic layouts
- Losing context when trimming descriptions too aggressively
- Not preserving source URLs for attribution and verification
- Mixing incompatible data types in the same table
