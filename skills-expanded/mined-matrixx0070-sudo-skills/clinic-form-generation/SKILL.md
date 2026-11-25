---
name: clinic-form-generation
version: 1.0.0
description: Fill official court or agency forms accurately from verified matter facts for supervising-attorney review before filing.
author: matrixx0070
tags: [legal-clinic, court-forms, filing, immigration, fee-waiver, accuracy]
capabilities: []
---

## When to use
Use this when a clinic matter needs an official court or agency form completed from facts already in the file — a fee-waiver application, an immigration form (for example I-912 or a G-28), a filing cover sheet, or a proof-of-service. You have the source facts, you know the court or agency, and you need a clean, field-accurate draft the supervising attorney can review before it is filed.

**Not for:** deciding what to argue or whether to file (that is legal advice you cannot give independently — Rule 5.5), internal analysis (use clinic-memo), or explaining the form to the client in lay terms (use clinic-plain-language-letters).

## Method
1. Confirm the correct form: exact title, edition/revision date, and jurisdiction. Forms expire — a superseded edition can be rejected.
   **Decision point:** if you cannot verify the current version and jurisdiction from the official source, stop and ask the supervising attorney rather than guessing.
2. Pull each field value from the matter file. Map every field to a documented fact; never let a GenAI draft invent a value, guess a date, or complete a blank to look finished (ABA Op. 512 competence and candor).
3. Strip client identifying details before using any external or GenAI tool; work with placeholders and reinsert protected facts locally (Rule 1.6).
4. Fill required fields; mark any unknown as "[VERIFY — missing]" instead of fabricating.
5. Re-read against the official instructions for signature blocks, attachments, and formatting.
6. Route to the supervising attorney for review and signature. Nothing is filed without that review.

## Example
> Matter: Nguyen fee waiver, Superior Court of California. You confirm form FW-001 (rev. Jan 1, 2024) is current for the county, map income and household-size fields to the intake sheet, flag the missing employer address as "[VERIFY — missing]", and hand the draft to the supervisor for signature.

## Pitfalls
- Using an expired form edition or the wrong jurisdiction's version.
- Letting GenAI auto-complete blanks with plausible but invented values.
- Pasting the client's full name, A-number, or SSN into an external tool (Rule 1.6).
- Treating a filled form as filed — the supervisor must review and sign first (Rule 5.5).

## Output format
```
FORM: <title> (edition/rev date) — <jurisdiction>
MATTER: <id>
FIELDS:
  <field> = <value>  [source: <doc>]
  <field> = [VERIFY — missing]
ATTACHMENTS: <list>
STATUS: DRAFT — awaiting supervising attorney review/signature
```

## Reference
- ABA Formal Op. 512: verify GenAI output; protect client confidentiality; duty of candor.
- Model Rules 1.1 (competence), 1.6 (confidentiality), 5.5 (no unauthorized/independent practice).
- Clinic norm: supervising attorney reviews and signs before any filing.
