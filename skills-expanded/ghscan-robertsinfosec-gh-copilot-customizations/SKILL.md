---
description: "Brand compliance audit workflow. Use when reviewing user-facing content, UI components, or documentation against docs/BRAND.md. Checks visual consistency, voice and tone, accessibility (WCAG 2.1 AA), and terminology compliance."
name: "brand-standards-check"
generation-source: "generation/skills/brand-standards-check.md"
---

# Brand Standards Check

## When to Use

- Reviewing user-facing content, UI components, or documentation
- Before releasing any public-facing changes
- After updating brand guidelines to verify existing content

## Prerequisites

- `docs/BRAND.md` MUST exist. If missing, STOP and instruct the user to create it first.

## Procedure

### Step 1: Load Brand Standards

Read `docs/BRAND.md` completely. Extract:
- Approved product/company names with exact spelling and capitalization
- Voice and tone guidelines
- Color palette (hex values, token names)
- Typography specifications
- Logo usage rules
- Terminology glossary (approved vs. prohibited terms)

### Step 2: Identify Audit Scope

Scan for user-facing content:
- UI strings in component files (`**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`)
- Documentation (`**/*.md`, `docs/**`)
- Error messages and user-facing logs
- Email templates, notification text
- Alt text, ARIA labels, and other accessible text

### Step 3: Audit Terminology

For each user-facing string, check:
- Product name matches `docs/BRAND.md` exactly (spelling, capitalization, trademark symbols)
- No prohibited terms from the terminology glossary
- Consistent usage across all files (no mixed terminology)

### Step 4: Audit Voice and Tone

For each user-facing text block, verify:
- Matches documented voice guidelines (formal/casual, active/passive, etc.)
- Error messages follow the approved error message pattern
- Documentation follows the approved documentation tone

### Step 5: Audit Visual Identity (if applicable)

For UI code, check:
- Color values match brand palette tokens
- Font specifications match brand typography
- Logo references point to approved assets
- No hardcoded color values that should use brand tokens

### Step 6: Report

Produce a findings table:

| File | Line | Issue | Brand Rule | Recommended Fix |
|------|------|-------|------------|----------------|

Group findings by category: Terminology, Voice/Tone, Visual Identity.

## References

- `docs/BRAND.md` — source of truth for all brand rules
- `.github/instructions/brand-compliance.instructions.md` — governance rules for brand compliance
