---
name: validate-bookmap
description: Validates a DITA 1.3 bookmap file against structural rules derived from the DITA 1.3 bookmap DTD. Use this skill when you need to check bookmap element order (title, bookmeta, frontmatter, chapter, part, appendix, backmatter), booktitle completeness, appendices vs appendix mixing, and chapter presence. Returns structured JSON with errors and warnings.
compatibility: Python 3.9+. No third-party dependencies.
---

## Overview

Validates a DITA 1.3 `<bookmap>` file and returns a JSON report.

## Usage

```bash
python scripts/validate_bookmap.py path/to/bookmap.ditamap
cat bookmap.ditamap | python scripts/validate_bookmap.py -
```

## Output schema

```json
{
  "is_valid": true,
  "errors": [{ "element": "string", "rule": "string", "message": "string", "line": 0 }],
  "warnings": [{ "element": "string", "rule": "string", "message": "string", "line": 0 }]
}
```

## Rules applied

See [references/RULES.md](references/RULES.md) for the full catalogue.

| Category | Key rules |
|---|---|
| Root | Must be `<bookmap>` |
| Order | DTD order enforced: `(title\|booktitle)?, bookmeta?, frontmatter?, chapter*, part*, (appendices?\|appendix*), backmatter?, reltable*` |
| Chapters | At least one `<chapter>` or `<part>` required |
| Booktitle | `<booktitle>` must contain `<mainbooktitle>` |
| Appendix | `<appendices>` and bare `<appendix>` must not be mixed |

## Common edge cases

- A bookmap with only `<part>` elements (no bare `<chapter>`) is valid — parts are checked
- `<backmatter>` before `<chapter>` → Error (order violation)
- `<booktitle>` without `<mainbooktitle>` → Error
