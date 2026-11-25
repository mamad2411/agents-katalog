# RapidFuzz Skill Deduplication Starter

Use this skill to scan a tiny skill inventory for near-duplicate names with RapidFuzz.

## What This Skill Does

- reads a toy TSV of skill names and slugs
- computes pairwise fuzzy similarity scores
- returns pairs above a configurable threshold
- emits a compact machine-readable dedup summary
