---
name: biosamples-sample-search
description: Use this skill to search EBI BioSamples for public sample metadata by text query or lightweight filters and return compact summaries.
---

## Purpose
Search public sample metadata through the official EBI BioSamples API.

## When to use
- You need a quick metadata-discovery skill for public biospecimens.
- You want sample accessions, organism hints, and a few normalized characteristics.

## When not to use
- You need full sample graph traversal or submission workflows.
- You need to download raw experimental data instead of metadata.

## Inputs
- A free-text search string.
- Optional page and page-size controls.

## Outputs
- A JSON summary with BioSamples accessions and normalized characteristics.

## Requirements
- Network access to `ebi.ac.uk`
- Python standard library only

## Provenance
- BioSamples API overview: https://www.ebi.ac.uk/biosamples/docs/references/api/overview
