---
name: ads-multi
description: Generate Google Ads RSA copy in multiple languages at once. Use when the user wants to create ads in 2+ languages from a single brief — produces native copy per language, not translations.
allowed-tools: Read, Write, Bash
---

# /ads-multi — Multilingual RSA Generation

## Input Required
Ask the user for the following (skip any already provided):
1. **Campaign name** — for CSV organization
2. **Ad group name** — base name (language suffix added automatically, e.g., `brand_awareness_DE`)
3. **Target keywords per language** — e.g., EN: "marketing analytics", DE: "Marketing-Analyse", FR: "analyse marketing", ES: "análisis de marketing", AR: "تحليلات التسويق", PL: "analityka marketingowa"
4. **Landing page** — a registry key (e.g., `pricing`) from `.claude/skills/landing-pages/SKILL.md`. Claude automatically resolves the correct language variant per target language. Or provide URLs per language manually.
5. **Languages** — which languages to generate (e.g., EN, DE, FR, ES, AR, PL)
6. **Key USPs / offers** — describe once; Claude adapts per language
7. **Target persona** — which persona from `.claude/skills/icp/SKILL.md` to target
8. **Output format** — ask the user:
   - **Separate CSVs**: one file per language (`rsa_campaign_adgroup_EN.csv`, `rsa_campaign_adgroup_DE.csv`, …) — easier for upload to language-specific campaigns
   - **Single CSV**: all languages in one file with a `Language` column — easier for overview and review

## Execution Steps

### Step 1: Load Context
- Load brand voice from `.claude/skills/brand-voice/SKILL.md` (check language-specific notes)
- Load ICP and persona from `.claude/skills/icp/SKILL.md`
- Load platform rules from `.claude/skills/google-ads-rules/SKILL.md` (check multilingual notes)
- Resolve landing page per language from `.claude/skills/landing-pages/SKILL.md`:
  - For each target language, pick the matching URL variant (exact → EN fallback → first)
  - Load cached analysis if available, otherwise fetch and cache
  - Flag any languages where no localized page exists

### Step 2: Generate per Language
For EACH language, independently:
- Create 15 headlines (≤30 chars) and 4 descriptions (≤90 chars)
- Write NATIVE copy — do NOT translate from another language
- Adapt tone, idioms, and CTA conventions to the target market
- Respect language-specific character challenges (see below)
- Validate character counts in the target language

### Step 3: Cross-Language Consistency Check
After generating all languages, verify:
- Core value proposition is consistent across all versions
- No language version contradicts another
- Brand name and product names are spelled identically everywhere
- Social proof claims match (same numbers, same certifications)

### Step 4: Validate
For each language:
- All headlines ≤30 characters
- All descriptions ≤90 characters
- At least 2 headlines contain the target keyword for that language
- At least 1 description contains a CTA
Run: `python .claude/skills/ads/validate.py output/<file>.csv`

### Step 5: Export
Based on user's output format choice:

**Separate CSVs:**
```
output/rsa_[campaign]_[adgroup]_EN_[date].csv
output/rsa_[campaign]_[adgroup]_DE_[date].csv
output/rsa_[campaign]_[adgroup]_FR_[date].csv
output/rsa_[campaign]_[adgroup]_ES_[date].csv
output/rsa_[campaign]_[adgroup]_AR_[date].csv
output/rsa_[campaign]_[adgroup]_PL_[date].csv
```

**Single CSV** (extra Language column prepended):
```csv
Language,Campaign,Ad Group,Headline 1,...,Headline 15,Description 1,...,Description 4,Path 1,Path 2,Final URL
EN,...
DE,...
FR,...
ES,...
AR,...
PL,...
```
Save to: `output/rsa_multi_[campaign]_[adgroup]_[date].csv`

### Step 6: Present Results
Show a comparison table:
```
| Language | Example Headline          | Example Description                | Char Issues |
|----------|--------------------------|-------------------------------------|-------------|
| EN       | Get Marketing Insights   | Turn campaign data into pipeline    | None        |
| DE       | Marketing-Einblicke      | Kampagnendaten in Pipeline...       | H7: 31 chars|
| FR       | Analyse marketing        | Transformez vos données en...       | None        |
| ES       | Analítica de marketing   | Convierte datos en pipeline         | None        |
| AR       | تحليلات التسويق          | حوّل بيانات حملاتك إلى نتائج       | None        |
| PL       | Analityka marketingowa   | Zamień dane kampanii w pipeline     | None        |
```

Then suggest:
- Which headlines may need shortening in specific languages
- Cultural differences that might affect CTR (e.g., German preference for formal tone)
- Whether any language version needs more keyword-rich headlines

## Language-Specific Guidelines

### English (EN)
- Shortest average word length — most headroom in 30 chars
- American vs. British spelling: check brand voice skill
- CTA conventions: direct ("Get", "Try", "Start")

### German (DE)
- Compound nouns are the main challenge: "Marketingautomatisierung" = 25 chars alone
- Always prepare shorter alternatives or split compounds
- Formal "Sie" unless brand voice specifies "du"
- CTA conventions: "Jetzt [verb]", "Kostenlos testen"

### French (FR)
- Accents (é,è,ê,à,ç,ù,î,ô) = 1 character each
- Articles consume characters: "l'automatisation du marketing"
- Formal "vous" for B2B unless brand voice specifies "tu"
- CTA conventions: "Découvrez", "Essayez gratuitement", "Demandez une démo"

### Spanish (ES)
- Accents (á,é,í,ó,ú,ñ,ü) = 1 character each
- Inverted punctuation (¿, ¡) counts as a character — avoid in headlines to save space
- Distinguish between Spain (ES-ES) and Latin America (ES-LATAM): vocabulary and "vosotros" vs. "ustedes"
- Formal "usted" for B2B in most markets; "tú" acceptable in startup/tech contexts
- CTA conventions: "Descubre", "Prueba gratis", "Solicita una demo", "Empieza ahora"

### Arabic (AR)
- Right-to-left (RTL) script — Google Ads handles direction automatically, but review carefully
- Arabic characters = 1 character each in Google Ads, same as Latin
- Words can be shorter than English equivalents, but connected script makes visual length deceptive — always validate by character count, not visual width
- Diacritical marks (tashkeel: َ ُ ِ ً ٌ ٍ) are optional in ad copy and count as separate characters — omit them to save space (standard practice in digital Arabic)
- Formal Modern Standard Arabic (MSA/فصحى) for B2B across all Arab markets
- Dialect choice matters for B2C: Gulf (خليجي), Egyptian (مصري), Levantine (شامي) — check brand voice
- Mixed scripts: brand names and technical terms often stay in Latin (e.g., "HubSpot" not "هبسبوت") — each Latin character counts as 1 char
- CTA conventions: "اكتشف" (Discover), "جرّب مجاناً" (Try free), "احجز عرضاً" (Book a demo), "ابدأ الآن" (Start now)
- Review workflow: if you cannot read Arabic, rely on character count validation and have a native speaker verify messaging before upload

### Polish (PL)
- Diacritics (ą,ć,ę,ł,ń,ó,ś,ź,ż) = 1 character each — no penalty
- Words tend to be longer than English due to declension
- Informal "Ty" is increasingly common in B2B digital ads
- CTA conventions: "Sprawdź", "Przetestuj", "Dowiedz się"

## Iteration Shortcuts
- "make DE headlines shorter" → rework only German headlines
- "FR descriptions need stronger CTAs" → adjust French descriptions
- "swap EN and ES headline styles" → cross-pollinate approaches
- "add AR" → generate Arabic version using existing brief
- "PL headlines 3 and 8 are too similar" → diversify Polish variants
- "review AR character counts" → revalidate Arabic headlines
