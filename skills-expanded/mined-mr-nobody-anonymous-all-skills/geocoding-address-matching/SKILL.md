---
name: geocoding-address-matching
description: "Geocode addresses and match records across datasets: normalisation, fuzzy matching, rooftop versus centroid precision, and accuracy reporting."
type: procedural
category: geospatial
domain: geospatial
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - geocode a list of addresses
  - reverse geocode coordinates
  - fuzzy address matching
  - geocoding accuracy
  - match addresses across datasets
keywords:
  - geocoding
  - address
  - matching
  - fuzzy
  - parcel
  - rooftop
source: custom
enabled: true
---

# Geocoding and Address Matching

## Purpose

Geocode addresses and match records across datasets: normalisation, fuzzy matching, rooftop versus centroid precision, and accuracy reporting.

## When to Use

- A table of addresses must become coordinates for mapping or analysis.
- Two datasets describe the same places with different address formats.
- A map needs to show how trustworthy each plotted location is.

## When NOT to Use

- The address list is heavily incomplete — resolve data quality first.
- Locations must be legally precise (cadastral); use survey or parcel data.
- The volume exceeds provider terms of service for bulk geocoding.

## Capabilities

- Normalise addresses (abbreviations, casing, secondary units, country formats).
- Match with blocking plus fuzzy scoring, and keep a review band.
- Distinguish rooftop, street-interpolation and centroid precision.
- Report match rate and positional uncertainty per record.

## Inputs

- The address table and its schema (street, number, unit, city, postcode, country).
- The geocoder available and its licence for storing results.
- The precision the decision needs: neighbourhood, street or building.

## Workflow

1. Profile the addresses: how many are complete, how many have a unit, which countries.
2. Normalise deterministically first (postal abbreviations, punctuation, casing).
3. Geocode in batches with the provider's rate limit respected, caching results.
4. Send ambiguous or failed records to manual review rather than forcing a low-confidence match.
5. Attach the precision level and score to every output row before mapping.

## Tools

- Nominatim / Photon / commercial geocoder
- PostGIS or `recordlinkage` for fuzzy matching
- QGIS for spot checks

## Examples

- `curl -s "https://nominatim.openstreetmap.org/search?q=Via+Roma+1+Roma&format=jsonv2" -H "User-Agent: my-app"`
- `SELECT *, similarity(addr, :input) AS score FROM addresses WHERE city = :city AND similarity(addr, :input) > 0.6;`
- `allskills route "map our customer addresses"`

## Safety

- Nominatim's public instance forbids bulk geocoding; use a self-hosted or commercial service.
- A rooftop match and a city centroid plotted identically mislead decision-makers — always encode precision.
- Addresses are personal data; minimise, aggregate and protect the output.

## Source

All-Skills canonical library (`skills/geospatial/geocoding-address-matching`). First-party skill, maintained in this repository.

## Notes

- Caching geocodes saves money and makes runs reproducible.
- Country-specific address formats break naive string matching; normalise per locale.
- Pairs with: `geospatial/spatial-reference-systems`, `data/data-quality`.
