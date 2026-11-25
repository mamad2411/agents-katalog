---
name: format-convert
description: Convert and validate JSON, YAML, TOML, XML, and CSV; minify, prettify, and diff structured data. Use when fixing config files, API payloads, or migration between serialization formats.
---

# Format Convert

Convert structured data between formats with validation at every step. **Parse first, transform second, serialize last.** Never silently drop fields or change types without documenting the transformation.

## When to Use This Skill

| Trigger | Example request |
|---------|-----------------|
| Config migration | "Convert this docker-compose YAML to JSON" |
| API debugging | "Validate and prettify this JSON payload" |
| Data export | "Flatten this nested JSON to CSV" |
| CI validation | "Check if this TOML is valid pyproject" |
| Format comparison | "Diff these two YAML configs structurally" |

## Phase Checklist

```
[ ] 1. Detect source format (extension, content sniff, user input)
[ ] 2. Parse and validate — report line/column on syntax errors
[ ] 3. Document transform rules (null, dates, large integers, nesting)
[ ] 4. Transform with safe parsers only (yaml.safe_load, not load)
[ ] 5. Serialize with consistent indentation (2 spaces default)
[ ] 6. Validate round-trip if fidelity matters
[ ] 7. Present output with warnings about data loss
```

---

## Supported Conversions

| From → To | Fidelity | Notes |
|-----------|----------|-------|
| JSON ↔ YAML | High | Watch `yes`/`no` boolean coercion |
| JSON ↔ TOML | Medium | Tables, arrays of tables, inline tables |
| JSON ↔ XML | Low–Medium | Attribute vs element mapping required |
| JSON → CSV | Low | Flatten nested objects explicitly |
| CSV → JSON | Medium | Type inference is heuristic |
| Minify / prettify | Lossless | JSON, XML, sometimes YAML |

---

## JSON Operations

### Validate and Prettify

```bash
# Validate syntax
python -m json.tool input.json > /dev/null && echo "Valid JSON"

# Prettify (2-space indent)
python -m json.tool input.json

# Minify
python -c "import json,sys; print(json.dumps(json.load(sys.stdin), separators=(',',':')))" < input.json

# Strict parse with error location
python -c "
import json, sys
try:
    json.load(open('input.json'))
    print('Valid')
except json.JSONDecodeError as e:
    print(f'Error at line {e.lineno}, col {e.colno}: {e.msg}')
"
```

### JSON Schema Validation

```python
import json
import jsonschema

data = json.load(open("payload.json"))
schema = json.load(open("schema.json"))

try:
    jsonschema.validate(data, schema)
    print("Schema valid ✓")
except jsonschema.ValidationError as e:
    print(f"Invalid at {e.json_path}: {e.message}")
```

### JSON Diff

```python
import json
import difflib

def json_diff(a_path: str, b_path: str) -> str:
    a = json.load(open(a_path))
    b = json.load(open(b_path))
    a_lines = json.dumps(a, indent=2, sort_keys=True).splitlines(keepends=True)
    b_lines = json.dumps(b, indent=2, sort_keys=True).splitlines(keepends=True)
    return "".join(difflib.unified_diff(a_lines, b_lines, fromfile=a_path, tofile=b_path))

print(json_diff("config.v1.json", "config.v2.json"))
```

For structured diff of large configs, prefer key-path reporting over raw line diff on minified JSON.

---

## YAML Operations

```bash
# YAML → JSON
python -c "
import yaml, json, sys
data = yaml.safe_load(open('config.yaml'))
print(json.dumps(data, indent=2))
"

# JSON → YAML
python -c "
import yaml, json
data = json.load(open('config.json'))
print(yaml.dump(data, default_flow_style=False, sort_keys=False))
"

# Validate YAML syntax
python -c "
import yaml
yaml.safe_load(open('config.yaml'))
print('Valid YAML')
"
```

### YAML Pitfalls

| Issue | Example | Handling |
|-------|---------|----------|
| Boolean coercion | `yes` → True | Quote strings: `"yes"` |
| Null variants | `null`, `~`, empty | Normalize to JSON `null` |
| Multi-document | `---` separators | Split and process each doc |
| Anchors/aliases | `&id`, `*id` | Expand before JSON export |
| Timestamps | `2024-01-01` | Preserve as string or ISO 8601 |

**Security:** Always use `yaml.safe_load()`. Never `yaml.load()` on untrusted input — arbitrary code execution risk.

---

## TOML Operations

```python
import tomllib  # Python 3.11+
import json

with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
print(json.dumps(data, indent=2))
```

```bash
# TOML validate (Python 3.11+)
python -c "
import tomllib
tomllib.load(open('pyproject.toml', 'rb'))
print('Valid TOML')
"
```

### TOML → JSON Mapping

| TOML | JSON |
|------|------|
| `[section]` | `{ "section": {} }` |
| `[[array.of.tables]]` | `{ "array": [{}, {}] }` |
| `key = "value"` | `"key": "value"` |
| Inline table `{ a = 1 }` | `"key": { "a": 1 }` |

---

## XML Operations

```python
import xml.etree.ElementTree as ET
import json

def xml_to_dict(element) -> dict:
    result = {}
    if element.attrib:
        result["@attributes"] = dict(element.attrib)
    children = list(element)
    if children:
        for child in children:
            tag = child.tag.split("}")[-1]  # strip namespace
            child_dict = xml_to_dict(child)
            if tag in result:
                if not isinstance(result[tag], list):
                    result[tag] = [result[tag]]
                result[tag].append(child_dict)
            else:
                result[tag] = child_dict
    elif element.text and element.text.strip():
        result["#text"] = element.text.strip()
    return result

tree = ET.parse("data.xml")
root = tree.getroot()
print(json.dumps({root.tag.split("}")[-1]: xml_to_dict(root)}, indent=2))
```

```bash
# Well-formedness check
python -c "import xml.etree.ElementTree as ET; ET.parse('data.xml'); print('Valid XML')"

# Prettify (if xmllint available)
xmllint --format data.xml
```

Document attribute vs element mapping when converting to JSON. Mixed content (text + elements) may lose fidelity.

---

## CSV Operations

### JSON → CSV

```python
import json
import csv

def flatten(obj, prefix="") -> dict:
    items = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else k
            items.update(flatten(v, key) if isinstance(v, (dict, list)) else {key: v})
    elif isinstance(obj, list):
        items[prefix] = json.dumps(obj)
    return items

data = json.load(open("users.json"))
rows = [flatten(row) for row in data]
if rows:
    with open("users.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=sorted(set().union(*rows)))
        writer.writeheader()
        writer.writerows(rows)
```

### CSV → JSON

```python
import csv
import json

with open("data.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=",")
    rows = list(reader)

print(json.dumps(rows, indent=2))
```

### CSV Rules (State Explicitly)

| Setting | Default | Options |
|---------|---------|---------|
| Delimiter | `,` | `;`, `\t`, `\|` |
| Header row | yes | first row = field names |
| Quote char | `"` | required for fields with delimiter |
| Nested fields | dot notation | `user.name` vs nested object |
| Encoding | UTF-8 | BOM handling for Excel |

---

## Conversion Matrix Quick Reference

```bash
# JSON → YAML
python -c "import yaml,json; print(yaml.dump(json.load(open('f.json')), default_flow_style=False))"

# YAML → JSON
python -c "import yaml,json; print(json.dumps(yaml.safe_load(open('f.yaml')), indent=2))"

# JSON → TOML (manual — no stdlib TOML writer; use tomli-w)
pip install tomli-w -q
python -c "import tomli_w,json; tomli_w.dump(json.load(open('f.json')), open('f.toml','wb'))"
```

---

## Worked Examples

### Example 1: Fix invalid JSON trailing comma

```
Error: Expecting property name at line 5, col 3
Cause: Trailing comma after last object property
Fix:   Remove comma, re-validate with json.tool
```

### Example 2: YAML boolean trap

```yaml
# Input
enabled: yes
country: no

# JSON output (YAML 1.1)
{"enabled": true, "country": false}

# Fix: quote "no" and "yes" if they are country codes
country: "no"
```

### Example 3: Nested JSON to flat CSV

```
Input:  [{"user": {"name": "Alice", "id": 1}}]
Rule:   Flatten with dot notation
Output: user.name,user.id → Alice,1
```

---

## Output Template

```markdown
## {source_format} → {target_format}

| Property | Value |
|----------|-------|
| Validation | ✓ syntax valid |
| Input size | {n} lines / {bytes} bytes |
| Warnings | {list or none} |

```{lang}
{output}
```

### Transform Notes
- Null handling: preserved as `null`
- Keys dropped: none
- Type changes: `"42"` → `42` (CSV inference)
- Data loss: XML namespaces collapsed to local names
```

---

## Decision Rubric

| Input signal | Format | First action |
|--------------|--------|--------------|
| Starts with `{` or `[` | JSON | `json.tool` validate |
| Starts with `---` or key: value | YAML | `safe_load` |
| Starts with `[` section header | TOML | `tomllib.load` |
| Starts with `<?xml` or `<` | XML | ElementTree parse |
| Comma-separated first line | CSV | Detect delimiter, DictReader |
| Minified single line | JSON likely | Parse then prettify |

---

## Anti-Patterns

- `yaml.load()` on untrusted input (code execution risk)
- Silent precision loss on large JSON integers (>2^53 in JS contexts)
- CSV export without escaping commas/quotes in field values
- Converting XML with mixed content without explaining data loss
- Line diff on minified JSON instead of structural diff
- Assuming CSV type inference is always correct
- Dropping unknown TOML keys during round-trip

---

## Cross-References

| Related need | Skill |
|--------------|-------|
| Text-level diff of output | `text-utils` |
| URL-encoded JSON in query strings | `encode-decode` |
| SQL export from CSV | `sql-format` |
| Config values with cron strings | `cron-builder` |
| Color values in JSON theme files | `color-convert` |
| JWT JSON claims formatting | `hash-crypto` |
