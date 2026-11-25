---
name: lang-arabic-bidi-rtl-localization
description: "Implement culturally authentic, syntactically correct Arabic translations and bidirectional CSS layouts conforming to the Unicode BiDi algorithm."
category: languages
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - languages
  - arabic
  - rtl
  - localization
  - typography
  - i18n
---

# Arabic Bidirectional (BiDi) Layout & Typography Localization

## Overview & Core Principles
Implement culturally authentic, syntactically correct Arabic translations and bidirectional CSS layouts conforming to the Unicode BiDi algorithm.

### BiDi Layout Implementation Invariants
1. **Logical CSS Properties**:
   - Replace `margin-left` / `margin-right` with `margin-inline-start` and `margin-inline-end`.
   - Replace `padding-left` / `padding-right` with `padding-inline-start` and `padding-inline-end`.
   - Set `<html dir="rtl" lang="ar">`.
2. **Typography & Font Shaping**:
   - Arabic requires cursive ligature shaping (OpenType features `init`, `medi`, `fina`, `isol`).
   - Use high-quality Arabic web fonts with appropriate line-height (e.g. Amiri, Cairo, Noto Sans Arabic) to accommodate tall ascenders and deep descenders without vertical clipping.
3. **BiDi Neutral Characters**:
   - Isolate mixed LTR text (code snippets, URLs, English brand names) within Arabic sentences using `<bdi>` elements or Unicode Left-to-Right Marks (`&lrm;` / `U+200E`).
