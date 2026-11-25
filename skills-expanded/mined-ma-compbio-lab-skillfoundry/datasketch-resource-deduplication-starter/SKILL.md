# datasketch Resource Deduplication Starter

Use this skill to scan a tiny resource registry sample for near-duplicate text records with MinHash LSH.

## What This Skill Does

- reads a toy JSONL resource list
- tokenizes title and summary text
- builds MinHash sketches with `datasketch`
- returns candidate duplicate pairs above a configurable threshold
