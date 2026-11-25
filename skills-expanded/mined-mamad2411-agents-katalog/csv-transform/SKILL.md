---
name: csv-transform
description: "Parse, filter, and transform CSV data files in the shared volume at {{SHARED_VOLUME}}."
metadata:
  openclaw:
    emoji: "📊"
---

# CSV Transform

Process CSV files from the shared volume at `{{SHARED_VOLUME}}`.

## Parse and Filter

```bash
# View CSV headers
head -1 {{SHARED_VOLUME}}/input/data.csv

# Filter rows matching a pattern
awk -F',' '$3 > 100' {{SHARED_VOLUME}}/input/data.csv > {{SHARED_VOLUME}}/output/filtered.csv

# Extract specific columns
cut -d',' -f1,3,5 {{SHARED_VOLUME}}/input/data.csv > {{SHARED_VOLUME}}/output/columns.csv

# Count rows
wc -l {{SHARED_VOLUME}}/input/data.csv
```

## Sort and Deduplicate

```bash
# Sort by column 2
sort -t',' -k2 {{SHARED_VOLUME}}/input/data.csv > {{SHARED_VOLUME}}/output/sorted.csv

# Remove duplicate rows
sort -u {{SHARED_VOLUME}}/input/data.csv > {{SHARED_VOLUME}}/output/unique.csv
```

## Tips for AI Agents

- Use `csvtool` or `miller` for complex CSV operations if available.
- Always check the delimiter (comma, tab, semicolon) before processing.
- Handle quoted fields carefully — use proper CSV parsers for complex data.
