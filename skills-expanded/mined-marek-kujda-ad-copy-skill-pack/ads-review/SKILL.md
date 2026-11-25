---
name: ads-review
description: Audit existing Google Ads RSA copy. Use when the user wants to review, analyze, or improve their current responsive search ads — from a CSV export, pasted copy, or Google Ads Editor file.
allowed-tools: Read, Write, Bash
---

# /ads-review — Audit Existing RSA Copy

## Input Required
Ask the user to provide their current RSA copy via one of:
- A CSV file exported from Google Ads Editor (place in project root or `output/`)
- Copy-pasted headlines and descriptions
- A Google Ads account screenshot (describe what you see)

Also ask for:
1. **Target keywords** — what should these ads be ranking for?
2. **Landing page URL** (optional) — to check message match
3. **Performance data** (optional) — CTR, conversions, impressions per headline/description if available
4. **Language** — EN / DE / FR / ES / AR / PL — to apply correct linguistic rules

## Audit Framework

### 1. Character Limit Check
- Flag any headline >30 chars or description >90 chars
- Run: `python .claude/skills/ads/validate.py <file>.csv` if CSV provided

### 2. Keyword Coverage Analysis
- Count how many headlines contain the exact target keyword or close variants
- Minimum benchmark: 2–3 out of 15
- Flag if zero headlines contain the keyword

### 3. Concept Diversity Scan
Group headlines by angle:
- Keyword match
- Benefit-driven
- Feature-driven
- CTA
- Social proof
- Urgency / scarcity
- Question
- Differentiator

Flag:
- Any angle with 0 headlines (missed opportunity)
- Any angle with 4+ headlines (over-indexed)
- Headline pairs that say the same thing differently ("Save Time" / "Work Faster")

### 4. Description Quality Check
- Does every description end with or contain a CTA?
- Is there at least one description with social proof or trust signal?
- Are descriptions complementary or repetitive?

### 5. Message Match (if landing page URL provided)
- Fetch and analyze the landing page
- Flag any ad promise not supported on the landing page
- Flag landing page value props missing from ad copy

### 6. Linguistic Check
- ALL CAPS where it shouldn't be
- Excessive punctuation
- Superlatives without verification ("best", "#1")
- Tone consistency with brand voice (load `.claude/skills/brand-voice/SKILL.md`)

### 7. Performance-Based Insights (if data provided)
- Identify lowest-CTR headlines → suggest replacements
- Identify highest-CTR headlines → suggest similar-angle variations
- Flag headlines with high impressions but low CTR (Google shows them but users don't click)

## Output Format
Present as a structured audit report:

```
## RSA Audit: [Campaign] / [Ad Group]

### Score: [X/10]

### ✅ What's Working
- ...

### ⚠️ Issues Found
1. [Issue] → [Recommendation]
2. [Issue] → [Recommendation]

### 🔄 Suggested Replacements
| #  | Current Headline        | Issue              | Suggested Replacement     |
|----|------------------------|--------------------|--------------------------|
| H3 | [current]              | Duplicate concept  | [new headline] [XX chars] |
| H9 | [current]              | No keyword         | [new headline] [XX chars] |

| #  | Current Description     | Issue              | Suggested Replacement     |
|----|------------------------|--------------------|--------------------------|
| D2 | [current]              | Missing CTA        | [new description] [XX ch] |

### 📊 Diversity Breakdown
| Angle          | Count | Status    |
|----------------|-------|-----------|
| Keyword match  | X/15  | ✅ / ⚠️   |
| Benefit        | X/15  | ✅ / ⚠️   |
| ...            |       |           |
```

After the audit, offer:
- "Want me to generate a full replacement set? I'll keep your best headlines and replace the weak ones."
- "Want me to export the improved version as a CSV?"
