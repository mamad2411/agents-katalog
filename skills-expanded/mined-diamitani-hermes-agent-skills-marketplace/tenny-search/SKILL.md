---
name: tenny-search
description: Use when saving apartment listing links and parsing them into organized CSV format. Structures real estate data for comparison.
category: productivity
---

# Tenny Search

## Overview
Saves apartment listing links and parses them into organized CSV format. Structures real estate data for easy comparison, helping renters and buyers evaluate properties side by side.

## When to Use
- Collecting apartment listings from Zillow, Apartments.com, Craigslist, etc.
- Parsing listing details into structured fields for comparison
- Exporting property data to CSV for spreadsheet analysis
- Tracking listing prices and availability over time
- Comparing rental properties by price, sqft, amenities, location

## How It Works
Accepts apartment listing URLs or raw listing text. Extracts structured data points (price, beds, baths, sqft, address, amenities, contact info). Outputs a clean CSV for sorting and comparison.

## Steps
1. Accept listing URLs or copy-pasted listing text
2. Parse each listing to extract: price, beds, baths, sqft, address, neighborhood, amenities, lease terms, contact info, source URL
3. Normalize values: consistent price format, standardized amenities, deduplication
4. Structure into CSV with consistent column headers
5. Highlight best value options based on user criteria
6. Export CSV file for further analysis

## Common Pitfalls
- Parsing errors from inconsistent listing formats across sites
- Missing critical fields like application fees or pet policies
- Not updating listings — prices and availability change quickly
- Mixing different property types (studio vs house) in the same dataset
- Assuming amenities are included when they're actually add-ons
