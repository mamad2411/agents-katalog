---
name: ads
description: Generate Google Ads Responsive Search Ad copy. Use when the user asks to create, write, or generate RSA headlines and descriptions, Google Ads copy, or search ad variations.
allowed-tools: Read, Write, Bash
---

# /ads — Generate Google Ads RSA Copy

## Input Required
Ask the user for the following (skip any already provided):
1. **Campaign name** — for CSV organization
2. **Ad group name** — for CSV organization
3. **Target keywords** — primary + secondary keywords
4. **Landing page** — one of:
   - A key from the landing pages registry (e.g., `pricing`) — see `.claude/skills/landing-pages/SKILL.md`
   - A full URL (will be analyzed on the fly)
   - Skip if USPs are provided manually
5. **Language** — EN / DE / FR / ES / AR / PL (default: infer from keywords)
6. **Key USPs / offers** — what makes this product/service unique
7. **Target persona** — which persona from `.claude/skills/icp/SKILL.md` to target (or describe inline)
8. **Competitors** (optional) — to differentiate messaging

## Execution Steps

### Step 1: Analyze Context
- Check if landing page was provided as a registry key → load cached analysis from `.claude/skills/landing-pages/cache_[key].md`
- If cache doesn't exist yet, fetch the URL, analyze it, and save cache for future use
- If a raw URL was provided (not a registry key), fetch and analyze it directly
- Review target keywords for search intent (informational, commercial, transactional)
- Load brand voice from `.claude/skills/brand-voice/SKILL.md`
- Load ICP and persona details from `.claude/skills/icp/SKILL.md`
- Load platform rules from `.claude/skills/google-ads-rules/SKILL.md`
- Identify the strongest messaging angles

### Step 2: Generate Headlines (15)
Create exactly 15 headlines, each ≤30 characters. Ensure diversity:
- 3–4 headlines with exact target keyword
- 2–3 benefit-driven headlines
- 2–3 feature-driven headlines
- 2 CTA headlines (action verbs)
- 1–2 social proof / authority headlines
- 1–2 urgency or differentiator headlines

For each headline, output:
```
[XX chars] Headline text | Category: [type]
```

### Step 3: Generate Descriptions (4)
Create exactly 4 descriptions, each ≤90 characters:
- Description 1: Primary value proposition + CTA
- Description 2: Key features/benefits summary
- Description 3: Social proof or trust signal + CTA
- Description 4: Urgency/offer or differentiator + CTA

For each description, output:
```
[XX chars] Description text
```

### Step 4: Validate
- Verify ALL character counts (headlines ≤30, descriptions ≤90)
- Check keyword presence (min 2 headlines with target keyword)
- Check CTA presence (min 1 description with clear CTA)
- Check diversity (no two headlines with identical concept)
- Flag any issues

### Step 5: Export CSV
Save to `output/rsa_[campaign]_[adgroup]_[date].csv` in Google Ads Editor format.

**CRITICAL: Write CSV as UTF-8 with BOM** (`\ufeff` as first byte, or `encoding="utf-8-sig"` in Python).
Without BOM, Google Ads Editor and Excel on Windows will corrupt diacritics (ą, ö, é, ñ → garbage).

```csv
Campaign,Ad Group,Headline 1,Headline 2,...,Headline 15,Description 1,...,Description 4,Path 1,Path 2,Final URL
```

### Step 6: Suggest Iterations
After presenting the copy, suggest:
- Which headlines might underperform and why
- Alternative angles worth testing
- Pin recommendations (which headlines to pin to positions 1–3)

## Iteration Shortcuts
- "more like #3" or "change #7" → regenerate specific items
- "make it more [adjective]" → adjust tone across all copy
- Always re-validate character counts after changes
