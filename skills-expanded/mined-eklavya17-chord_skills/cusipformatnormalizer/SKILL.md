---
name: CusipFormatNormalizer
description: Normalize input CUSIP format before validation; always required before any CUSIP validation process.
tools:
  - bash
---

# CUSIP Format Normalizer

## Purpose
This skill ensures that any CUSIP input is formatted correctly before proceeding to validation.

## Workflow
1. Take the user's CUSIP query.
2. Run: `python pipeline/skills/CusipFormatNormalizer/scripts/preprocess.py "<raw_cusip>"`
3. Pass the normalized output to `cusip-validator`.
4. Return the validation result to the user.
