---
name: analyzing-malicious-onenote-and-html-smuggling
description: 'Analyzes two modern delivery techniques: malicious OneNote (.one) attachments with
  embedded payloads behind fake buttons, and HTML smuggling pages that reconstruct payloads in the
  browser from embedded blobs. Activates for requests to analyze a malicious OneNote file, detect
  HTML smuggling, or extract a smuggled/embedded payload.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - onenote
  - html-smuggling
  - document-malware
  - delivery
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027.006
  - T1204.002
  - T1566.001
d3fend:
  - D3-FCR
  - D3-DA
references:
  - 'MITRE ATT&CK T1027.006 HTML Smuggling — https://attack.mitre.org/techniques/T1027/006/'
  - 'OneNote file format (MS-ONESTORE) — https://learn.microsoft.com/openspecs/office_file_formats/ms-onestore/'
---

# Analyzing Malicious OneNote and HTML Smuggling

## When to Use

- You have a OneNote (`.one`) attachment suspected of hiding an embedded executable/script behind a
  "click to view" lure.
- You have an HTML/SVG page that reconstructs and auto-downloads a payload from an embedded blob
  (HTML smuggling).
- You need to extract the hidden payload without triggering the lure.

**Do not use** OneNote or a browser to open these files for analysis — that is exactly the
delivery mechanism. Carve the embedded data statically.

## Prerequisites

- A static carver (Python) for embedded file signatures; the sample handled inertly.

## Safety & Handling

- Never open the `.one` in OneNote or the HTML in a browser.
- Defang URLs and store carved payloads password-protected.

## Workflow

### Step 1: For OneNote — carve embedded files

OneNote stores attached files in the document. Scan for embedded file signatures (`MZ`, script
headers, archives) and the `FileDataStoreObject` GUIDs, and carve them out.

```bash
python scripts/analyst.py carve sample.one
```

### Step 2: For HTML smuggling — find the embedded blob

Look for large base64/`Blob`/`Uint8Array` constructions, `data:` URIs, and a JS routine that
builds a Blob and triggers a download (`msSaveOrOpenBlob`, anchor `download`, `createObjectURL`).

### Step 3: Reconstruct the payload statically

Decode the embedded base64/byte array (and any XOR/char-code layer) to recover the payload as
data — without executing the page.

### Step 4: Analyze and extract IOCs

Hash carved payloads, identify their type, defang any URLs, and route executables/scripts to the
appropriate analysis workflow.

## Validation

- Embedded payloads are carved/reconstructed from the inert file, not by opening it.
- The recovered payload's type is identified and hashed.
- The lure/trigger mechanism (fake button, Blob download) is documented.

## Pitfalls

- Opening the OneNote/HTML to "see" the lure and executing the payload.
- Decoding only the first layer when the blob is additionally XOR/char-code encoded.
- Missing multiple embedded objects in a single OneNote page.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the carver/decoder.
- ATT&CK T1027.006 and MS-ONESTORE (linked in frontmatter).
