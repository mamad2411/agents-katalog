---
name: csv-injection-export-defense
description: >
  Harden CSV/XLSX export pipelines against formula injection on owned systems:
  neutralize leading =+@- and control characters, force string cell types in
  spreadsheet libraries, document user-open risks, and add regression tests.
  Use when implementing or reviewing exports of untrusted data.
---

# CSV Injection Export Defense

## Scope And Authorization

- **In scope:** Export code and file-generation services you maintain.
- **Out of scope:** Guaranteeing all end-user spreadsheet configurations are safe — document residual risk.
- Prefer unit tests with formula-like strings.
- Pair with `csv-formula-injection` for assessment methodology and `code-quality-standards`.

## When To Use

- Building CSV/XLSX downloads containing user or third-party text.
- Remediation after a CSV injection finding.
- Standardizing export helpers across microservices.
- Admin report generators.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Finding/exploiting CSV injection | `csv-formula-injection` |
| General XSS | `xss-cross-site-scripting` |
| Authz on who can export | IDOR / authz skills |
| Excel BI modeling | data skills |
| Implementation quality baseline | `code-quality-standards` |

## Defense strategies

| Strategy | Pros | Cons |
| --- | --- | --- |
| Prefix `'` (apostrophe) | Simple CSV text | Visible apostrophe in some clients |
| Prefix tab/space | Sometimes breaks formula | Fragile; may still be trimmed |
| Escape formula chars | Explicit | Must cover full set + unicode lookalikes carefully |
| XLSX typed as string | Strong for Excel | Need proper library usage |
| Strip leading specials | May alter data | Changes user content |
| Wrap all fields quotes | Needed for CSV commas | Alone does **not** stop formulas |

Recommended default for untrusted text cells: **neutralize leading formula triggers** while preserving readability, and use real string types in XLSX.

## Workflow

### 1. Confirm scope and success criteria

1. All export code paths (sync download, email attachments, S3 batch).
2. Success: formula-like inputs export as non-executing text in target clients; tests locked; docs updated.

### 2. Centralize sanitization

```python
import re

_FORMULA_RE = re.compile(r'^[\t\r\n ]*[=+\-@]')

def neutralize_csv_cell(value: str) -> str:
    if value is None:
        return ''
    s = str(value)
    if _FORMULA_RE.match(s):
        return "'" + s  # Excel treats as text
    return s
```

```js
function neutralizeCsvCell(value) {
  const s = String(value ?? '');
  if (/^[\t\r\n ]*[=+\-@]/.test(s)) return `'${s}`;
  return s;
}
```

Apply to **every** untrusted field; also consider fields that concatenate user input.

### 3. CSV writing

```python
import csv
from io import StringIO

def export_rows(rows: list[dict]) -> str:
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=['id', 'name', 'note'], quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for r in rows:
        writer.writerow({
            'id': r['id'],
            'name': neutralize_csv_cell(r['name']),
            'note': neutralize_csv_cell(r['note']),
        })
    return buf.getvalue()
```

Set content-type `text/csv; charset=utf-8` and safe `Content-Disposition` filename (no CRLF — see `crlf-injection`).

### 4. XLSX string typing

```python
# openpyxl sketch
cell.value = raw_user_string
cell.data_type = 's'  # ensure string; avoid letting Excel parse as formula
# Or prefix neutralize as above before assign
```

Avoid building XLSX via string concat of XML without a library.

### 5. Policy choices

1. **Keep leading apostrophe** vs strip — product decision; document.
2. Numeric columns: export as numbers only when validated numeric, not user free text.
3. Delimiter injection (commas/newlines): rely on proper CSV quoting library — do not hand-roll.

### 6. Tests

```python
def test_formula_prefix_neutralized():
    assert neutralize_csv_cell('=1+1').startswith("'")
    assert neutralize_csv_cell('normal') == 'normal'
    assert neutralize_csv_cell('\t=1+1').startswith("'")
```

Add golden-file test for full CSV line quoting.

### 7. Verify in clients

1. Open sample export in Excel/LibreOffice/Google Sheets lab profiles.
2. Confirm `=1+1` does not become `2` unless user edits.
3. Communicate residual risk: users can still paste unsanitized data elsewhere.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Implementation | Shared helper + tests | One endpoint fixed, five forgotten |
| XLSX | Library + string type | Formula-capable free text cells |
| CSV | csv module + neutralize | `f"{name},{email}"` hand join |
| Filename | Sanitized disposition | User title with CR/LF |
| Docs | “Open exports carefully” | Promise absolute safety |

## Output Checklist

- [ ] All export paths inventoried
- [ ] Shared neutralize helper adopted
- [ ] CSV quoting via standard library
- [ ] XLSX string typing verified
- [ ] Unit/golden tests for formula prefixes
- [ ] Lab client verification done
- [ ] Content-Disposition safe
- [ ] Residual user risk documented
- [ ] Assessment finding closed with evidence
- [ ] `code-quality-standards` applied

## Rules

- Defense in depth: sanitization + safe libraries + user guidance.
- Do not claim spreadsheet clients can never be tricked after user paste.
- Focus on **export pipeline hardening** against CSV formula injection.
