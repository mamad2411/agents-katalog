---
description: >
  Generates orthographic and structural variations of a name for use in U.S.
  database searches. Expands: inverted order, accent-stripped, initials,
  surname-only, relative variations. Works for any nationality.
argument-hint: "Full Name"
---

You will expand the name in $ARGUMENTS into search variations for U.S. databases.

Act as the sub-skill defined in `skills/expand-brazilian-identity/SKILL.md`.

Use the script `skills/expand-brazilian-identity/scripts/expand_identity.py`
if available, passing `--origin-country` for non-Brazilian targets.

All output must be in **English**.

## Expected output

List the generated variations in this format:
1. Full name as provided
2. Full name without accents
3. First name + last surname
4. Last surname + first name (American order)
5. Initials + surname (e.g., C. Ferreira, C.E. Ferreira)
6. Surname only

Then ask the user:
- Are there relatives to include? (name + relationship)
- Are there known aliases or nicknames?
- Do you approve the variations or want to adjust before proceeding?

> **Note for non-Latin names:** Transliteration coverage is lower for
> Chinese, Arabic, Nigerian, and other non-Latin names. Review variations
> carefully before running searches.
