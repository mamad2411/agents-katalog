---
name: cross-service-sync
description: Detect schema, type, or API interface changes and find files in other services that may need synchronized updates. Trigger when modifying files under schemas/, types/, or interfaces/ directories — extracts changed class/type names from the diff and searches all other services for references, outputting a list of potentially stale consumers.
---

# cross-service-sync

## Purpose
Detect schema/type/API interface changes and identify files in other services that may need sync.

## Trigger
When schemas, types, or API response structures are modified.

## What it does
1. Detects changed schema/type files
2. Extracts field names and type identifiers
3. Searches other services for matching references
4. Outputs files that may need sync updates

## Usage
```bash
bash .skills/cross-service-sync/scripts/check.sh
```
