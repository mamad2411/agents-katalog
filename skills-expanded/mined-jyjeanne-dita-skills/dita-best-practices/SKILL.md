---
name: dita-best-practices
description: Analyzes a DITA topic or map file for quality and maintainability issues beyond basic DTD validity. Use this skill after validate-dita-topic or validate-ditamap when you want to check shortdesc length, topic size, step count, nesting depth, conref chain problems, keyref-vs-href balance, duplicate content, and empty elements. Returns structured JSON with categorized findings.
compatibility: Python 3.9+. No third-party dependencies.
---

## Overview

Runs best-practice checks on a DITA file (topic or map) and returns a JSON report.

## Usage

```bash
# Auto-detect file type
python scripts/best_practices.py path/to/topic.dita

# Pipe XML
cat topic.dita | python scripts/best_practices.py -

# Exit code: 0 = no errors (warnings may still be present), 1 = errors found
```

## Output schema

```json
{
  "file_type": "concept | task | reference | troubleshooting | map | bookmap | unknown",
  "findings": [
    {
      "severity": "error | warning | info",
      "category": "string",
      "element": "string",
      "message": "string"
    }
  ]
}
```

## Checks performed

See [references/RULES.md](references/RULES.md) for the full catalogue.

| Category | Examples |
|---|---|
| `shortdesc` | > 50 words, contains block elements, missing |
| `topic-size` | Body > 300 words or > 50 block elements |
| `nesting` | `<section>` or `<topicref>` depth > 3 |
| `steps` | > 10 steps in one `<steps>` block |
| `reuse` | `href` used without a `keys` definition; repeated paragraph text |
| `conref` | Chained conref (target itself uses `@conref`) |
| `empty` | Empty `<cmd>`, `<title>`, `<shortdesc>`, `<p>` |
| `ids` | Missing `@id` on reusable elements (`<section>`, `<fig>`, `<table>`) |

## Common edge cases

- Chained conref detection requires both files to be on disk; in pipe mode it reports only format warnings
- "Repeated paragraph text" comparison is fuzzy (Jaccard similarity > 0.85); tune threshold in the script if needed
- `info` severity findings are informational only and do not affect exit code
