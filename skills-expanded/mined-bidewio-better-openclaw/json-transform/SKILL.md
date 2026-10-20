---
name: json-transform
description: "Manipulate and query JSON data using jq-style operations in the shared volume at {{SHARED_VOLUME}}."
metadata:
  openclaw:
    emoji: "🔤"
---

# JSON Transform

Process JSON files from the shared volume at `{{SHARED_VOLUME}}`.

## Query and Filter

```bash
# Pretty print JSON
jq '.' {{SHARED_VOLUME}}/input/data.json

# Extract a field
jq '.users[].name' {{SHARED_VOLUME}}/input/data.json

# Filter objects
jq '.items[] | select(.price > 10)' {{SHARED_VOLUME}}/input/data.json > {{SHARED_VOLUME}}/output/expensive.json

# Transform structure
jq '{total: (.items | length), names: [.items[].name]}' {{SHARED_VOLUME}}/input/data.json
```

## Merge and Combine

```bash
# Merge two JSON files
jq -s '.[0] * .[1]' {{SHARED_VOLUME}}/input/a.json {{SHARED_VOLUME}}/input/b.json > {{SHARED_VOLUME}}/output/merged.json
```

## Tips for AI Agents

- `jq` is the standard tool for command-line JSON processing.
- Use `-r` flag for raw string output without quotes.
- Pipe JSON API responses directly to jq for parsing.
