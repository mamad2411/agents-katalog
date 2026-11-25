---
name: generate-keyrefs
description: Scans one or more DITA 1.3 topics and automatically generates keydef entries and keyref suggestions. Use this skill when you want to enforce reuse-first authoring, detect repeated inline text or repeated hrefs that should be centralised in the map, or migrate a set of topics to use keyrefs instead of hard-coded values. Returns ready-to-paste keydef XML plus a change list showing exactly which elements to update.
compatibility: Python 3.9+. No third-party dependencies (stdlib only).
---

## Overview

`generate-keyrefs` analyses a set of DITA topics and produces:

1. **`keydefs`** — suggested `<keydef>` entries to add to your root ditamap
2. **`changes`** — a per-file list of elements to replace with `keyref=` attributes
3. **`keydef_block`** — a ready-to-paste XML snippet for your map
4. **`--apply`** mode — rewrites files in place, adding `keyref=` attrs and removing hard-coded values

### Candidate detection rules

| Category | Elements scanned | Condition |
|----------|-----------------|-----------|
| Text keys | `<ph>`, `<term>`, `<keyword>`, `<prodname>`, `<varname>`, `<wintitle>`, `<cmdname>`, `<option>`, `<parmname>`, `<apiname>`, `<filepath>`, `<userinput>`, `<systemoutput>` | Same text appears ≥ N times across all files |
| External URL keys | `<xref href="http…">`, `<link href="http…">` | Same URL appears ≥ N times |
| Image keys | `<image href="…">` | Same image path appears ≥ N times |
| Code ref keys | `<coderef href="…">` | Same path appears ≥ N times |

Elements that already carry a `keyref=` attribute are skipped.

---

## Usage

```bash
# Scan a directory, show suggestions (dry run)
python generate-keyrefs/scripts/generate_keyrefs.py topics/

# Raise the threshold — only suggest if text appears 3+ times
python generate-keyrefs/scripts/generate_keyrefs.py topics/ --min-occurrences 3

# Scan specific files
python generate-keyrefs/scripts/generate_keyrefs.py overview.dita install.dita reference.dita

# Save keydef XML to a file for pasting into your map
python generate-keyrefs/scripts/generate_keyrefs.py topics/ --keydef-output keydefs.xml

# Rewrite topics in place (adds keyref= attrs, removes old values)
python generate-keyrefs/scripts/generate_keyrefs.py topics/ --apply
```

---

## Output schema

```json
{
  "summary": {
    "files_scanned":      3,
    "keydefs_suggested":  4,
    "changes_suggested":  9
  },
  "keydefs": [
    {
      "key":         "acme-product",
      "type":        "text",
      "value":       "ACME Product",
      "occurrences": 6,
      "files":       ["topics/overview.dita", "topics/install.dita"]
    },
    {
      "key":         "ext-docs-acme-com-api",
      "type":        "href",
      "href":        "https://docs.acme.com/api",
      "scope":       "external",
      "occurrences": 3,
      "files":       ["topics/overview.dita"]
    }
  ],
  "changes": [
    {
      "file":        "topics/overview.dita",
      "element":     "ph",
      "change":      "add_keyref",
      "old_text":    "ACME Product",
      "new_keyref":  "acme-product",
      "description": "<ph>ACME Product</ph> → <ph keyref=\"acme-product\"/>"
    }
  ],
  "keydef_block": "<keydef key=\"acme-product\">\n  <topicmeta>…</topicmeta>\n</keydef>\n\n<keydef key=\"ext-docs-acme-com-api\" href=\"https://docs.acme.com/api\" scope=\"external\" format=\"html\"/>"
}
```

When `--apply` is used, the response also includes:

```json
{
  "applied": {
    "topics/overview.dita": 3,
    "topics/install.dita": 2
  },
  "summary": {
    "files_rewritten": 2
  }
}
```

---

## Keydef XML produced

### Text key

```xml
<keydef key="acme-product">
  <topicmeta>
    <keywords>
      <keyword>ACME Product</keyword>
    </keywords>
  </topicmeta>
</keydef>
```

Usage in topic after `--apply`:

```xml
<!-- Before -->
<ph>ACME Product</ph>

<!-- After -->
<ph keyref="acme-product"/>
```

### External URL key

```xml
<keydef key="ext-docs-acme-com-api"
        href="https://docs.acme.com/api"
        scope="external"
        format="html"/>
```

Usage in topic:

```xml
<!-- Before -->
<xref href="https://docs.acme.com/api">API docs</xref>

<!-- After -->
<xref keyref="ext-docs-acme-com-api">API docs</xref>
```

### Image key

```xml
<keydef key="img-header-logo" href="images/header-logo.png" format="png"/>
```

Usage in topic:

```xml
<!-- Before -->
<image href="images/header-logo.png" alt="Logo"/>

<!-- After -->
<image keyref="img-header-logo" alt="Logo"/>
```

---

## Integration into a map

Paste the `keydef_block` output (or the file written by `--keydef-output`) before your first `<topicref>`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE map PUBLIC "-//OASIS//DTD DITA Map//EN" "map.dtd">
<map>
  <title>Product Guide</title>

  <!-- ── Key definitions ─────────────────────────────────── -->
  <keydef key="acme-product">
    <topicmeta>
      <keywords><keyword>ACME Product</keyword></keywords>
    </topicmeta>
  </keydef>
  <keydef key="ext-docs-acme-com-api"
          href="https://docs.acme.com/api"
          scope="external" format="html"/>

  <!-- ── Topics ──────────────────────────────────────────── -->
  <topicref href="topics/overview.dita"/>
  <topicref href="topics/install.dita"/>
</map>
```

---

## Common pitfalls

| Pitfall | Cause | Fix |
|---------|-------|-----|
| Key name collision | Two different values slug to the same key | Script auto-appends `-2`, `-3` suffixes; review and rename if needed |
| `--apply` breaks round-trip | ET serialisation drops CDATA / processing instructions | Back up topics before running `--apply`; check `git diff` |
| Short text over-matched | Single letters or numbers meet the threshold | Raise `--min-occurrences` or post-filter the change list |
| Scope wrong for local images | Image path treated as external | Script detects `http://` prefix; local paths always get `format=<ext>` |
| keyref resolution at build time | Keys must be defined before first reference in map order | Place all `<keydef>` elements at the top of the map |

---

## See also

- `validate-ditamap` — validates that all keyrefs in a map resolve to defined keys
- `validate-dita-topic` — catches malformed keyref attributes in topics
- `dita-best-practices` — flags topics that have hard-coded values instead of keyrefs
- `refactor-dita-content` — broader refactoring including conref extraction
