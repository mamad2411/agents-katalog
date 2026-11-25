---
name: hum-digital-humanities-tei-paleography
description: "Transcribe, encode, and computationally analyze historical manuscripts using Text Encoding Initiative (TEI P5) XML guidelines and digital paleography."
category: humanities
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - humanities
  - digital-humanities
  - tei
  - xml
  - paleography
  - archives
---

# Digital Humanities TEI-XML Encoding & Textual Paleography

## Overview & Core Principles
Transcribe, encode, and computationally analyze historical manuscripts using Text Encoding Initiative (TEI P5) XML guidelines and digital paleography.

### TEI P5 Encoding Standards & Critical Editions
1. **Structural Document Encoding**:
   - Enforce valid XML conforming to TEI schema (`teiHeader`, `sourceDesc`, `profileDesc`, `text`, `body`).
2. **Textual Variants & Scribal Hands**:
```xml
<app>
  <lem wit="#handA">in principio</lem>
  <rdg wit="#handB">ab initio</rdg>
</app>
```
3. **Paleographic Calibration**:
   - Distinguish scribal abbreviations (titulus, brevigraphs) using `<abbr>` and `<expan>` or `<choice>` structures.
