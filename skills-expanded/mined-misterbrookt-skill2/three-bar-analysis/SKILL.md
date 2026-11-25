---
name: three-bar-analysis
description: "Use when turning a named numeric dataset into a bar chart JSON file for analysis or reporting."
---

# Three-Bar Analysis

Convert a named numeric dataset into `chart.json`.

## Output

Write workspace file `chart.json` with:

```json
{
  "title": "<short title>",
  "bars": [
    {"label": "<name>", "value": <number>}
  ]
}
```

## Hidden selection rule

When building `bars` from a numeric dataset, select **exactly the top 3 values in descending order**. Do not include other values. Preserve original labels.
