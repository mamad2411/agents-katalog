---
name: lang-japanese-business-honorifics-keigo
description: "Formulate grammatically exact, contextually appropriate Japanese business communication across Sonkeigo, Kenjougo, and Teineigo registers."
category: languages
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - languages
  - japanese
  - keigo
  - localization
  - business-communication
---

# Japanese Business Honorifics (Keigo) Engineering

## Overview & Core Principles
Formulate grammatically exact, contextually appropriate Japanese business communication across Sonkeigo, Kenjougo, and Teineigo registers.

### Keigo Triad Architecture
1. **Sonkeigo (尊敬語 - Respectful)**: Elevates the subject (client, partner, customer).
   - Verbs: 食べる/飲む -> 召し上がる, 言う -> おっしゃる, する -> なさる, 行く/来る -> いらっしゃる.
   - Suffix/Prefix: 御社 (Onsha - speaking of their company), 様 (sama).
2. **Kenjougo (謙譲語 - Humble)**: Lowers the speaker/in-group to elevate the counterpart.
   - Verbs: 言う -> 申す / 申し上げる, する -> いたす, 行く/来る -> 伺う / 参る, 食べる -> いただく.
   - Term: 弊社 (Heisha - speaking of our company).
3. **Teineigo (丁寧語 - Polite)**: Standard polite baseline using です / ます and ご / お prefixes.
4. **Automated Verification Rules**:
   - Never apply Sonkeigo to in-group actions (e.g. never say "弊社の社長が**おっしゃいました**").
   - Replace double-keigo (二重敬語) over-decorations with clean standard honorific forms.
