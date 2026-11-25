---
name: review-dita-guide
version: 1.0.0
description: >
  Reviews an entire DITA publication from a root bookmap or ditamap.
  Traverses the full hierarchy — root map → child ditamaps → leaf topics —
  and produces a consolidated validation report covering structure, DTD
  compliance, best practices, and cross-guide issues (missing files,
  circular map references, duplicate topic IDs) that single-file
  validators cannot detect.
license: MIT
compatibility:
  - claude-code
  - github-copilot
  - mistral
metadata:
  type: validation
  dita-version: "1.3"
  input: bookmap | ditamap
  output: json
allowed-tools:
  - read_file
  - run_script
---

# review-dita-guide

Validates an entire DITA guide by walking the full publication hierarchy
from a root bookmap or ditamap down through all referenced child maps and
leaf topics.

## When to use

- Before a DITA-OT build to catch issues across the whole publication
- After restructuring a guide (moving topics, nesting new child maps)
- During CI/CD to gate publishing on guide-wide validity
- When auditing a large guide for quality and best-practice compliance

## What is checked

### Per-file (each map and topic)
- DTD structural validity (via `validate_bookmap`, `validate_ditamap`,
  `validate_dita_topic`)
- Best practices (shortdesc, step count, nesting depth, duplicate paragraphs)
  when `--best-practices` is supplied

### Cross-guide (spanning multiple files)
| Rule | Severity | Description |
|------|----------|-------------|
| `href-target-missing` | Error | An `@href` in a map points to a file that does not exist |
| `circular-reference` | Error | A map references itself directly or through a chain of maprefs |
| `duplicate-guide-id` | Warning | Two or more topics share the same root `@id` across the guide |

## Output schema

```json
{
  "root":    "<path>",
  "summary": {
    "total_files": 12,
    "maps": 2, "topics": 10, "missing": 0,
    "valid_files": 12, "invalid_files": 0,
    "errors": 0, "warnings": 3,
    "cross_guide_issues": 0
  },
  "files": [
    {
      "path": "relative/path.dita",
      "type": "topic|map|bookmap|missing",
      "depth": 1,
      "is_valid": true,
      "errors": [],
      "warnings": [],
      "best_practices": []
    }
  ],
  "cross_guide": [
    { "rule": "duplicate-guide-id", "message": "...", "paths": ["a.dita","b.dita"] }
  ]
}
```

## Exit codes
- `0` — all files valid, no cross-guide errors
- `1` — one or more errors found
- `2` — usage or IO error
