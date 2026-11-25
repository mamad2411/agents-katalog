---
name: sitelinks
description: Generate Google Ads sitelink extensions. Use when the user asks to create, write, or generate sitelinks, ad extensions, or site links for a Google Ads campaign.
allowed-tools: Read, Write, Bash
---

# /sitelinks — Generate Google Ads Sitelink Extensions

## Sitelink Specifications (Google Ads Requirements)

| Element          | Max Characters | Required |
|------------------|---------------|----------|
| Sitelink title   | 25            | Yes      |
| Description 1    | 35            | No (but strongly recommended) |
| Description 2    | 35            | No (but strongly recommended) |
| Final URL        | 2048          | Yes      |

- Minimum: 2 sitelinks per campaign (Google recommendation: 4–8)
- Maximum: 20 sitelinks per campaign (Google rotates and tests)
- Sitelinks can be set at account, campaign, or ad group level
- Each sitelink must point to a different page than the ad's Final URL
- Each sitelink must point to a different page than other sitelinks (no duplicate URLs)

## Input Required

Ask the user for the following (skip any already provided):
1. **Campaign / Ad group** — where to apply sitelinks
2. **Landing page registry key or ad group context** — to understand what pages are available
   (load `.claude/skills/landing-pages/SKILL.md` to see registered URLs)
3. **Language** — EN / DE / FR / ES / AR / PL (default: infer from campaign)
4. **Number of sitelinks** — default: 8 (gives Google more options to rotate)
5. **Scope** — campaign-level (shared across ad groups) or ad-group-level (specific)
6. **Current sitelinks** (optional) — if refreshing existing ones

## Execution Steps

### Step 1: Analyze Available Pages
- Load landing pages registry from `.claude/skills/landing-pages/SKILL.md`
- Identify pages that would make good sitelinks (pricing, features, demo, case studies, etc.)
- Load brand voice from `.claude/skills/brand-voice/SKILL.md`
- Load ICP from `.claude/skills/icp/SKILL.md` to align sitelinks with buyer journey
- Load cached page analyses where available

### Step 2: Map Sitelinks to Buyer Journey
Aim for a mix that covers the funnel:

| Journey Stage   | Sitelink Example            | Typical Page       |
|-----------------|-----------------------------|-------------------|
| Awareness       | "How It Works"              | /features         |
| Consideration   | "Customer Stories"          | /case-studies     |
| Consideration   | "Compare Plans"             | /pricing          |
| Decision        | "Start Free Trial"          | /signup           |
| Decision        | "Book a Demo"               | /demo             |
| Support         | "Help Center"               | /support          |
| Trust           | "About Us"                  | /about            |
| Specifics       | "[Feature Name]"            | /features/[name]  |

Don't just list pages — each sitelink title should be a compelling micro-CTA.

### Step 3: Generate Sitelinks
For each sitelink, create:
- **Title** (≤25 chars) — action-oriented, specific, no generic filler
- **Description 1** (≤35 chars) — expand on the title's promise
- **Description 2** (≤35 chars) — add a proof point or secondary benefit
- **Final URL** — resolve from landing pages registry (language-aware)

Output format:
```
Sitelink 1:
  [XX ch] Title: "See Pricing & Plans"
  [XX ch] Desc 1: "Transparent plans from $99/mo"
  [XX ch] Desc 2: "No hidden fees. Cancel anytime."
  URL: https://example.com/pricing
```

### Step 4: Validate
- All titles ≤25 chars
- All descriptions ≤35 chars each
- No duplicate URLs across sitelinks
- No sitelink URL matches the ad's main Final URL
- Each sitelink points to a distinct, relevant page
- Titles are unique — no two say the same thing

### Step 5: Export CSV
Save to `output/sitelinks_[campaign]_[date].csv` in Google Ads Editor format.

**CRITICAL: Write CSV as UTF-8 with BOM** (`encoding="utf-8-sig"` in Python).

```csv
Campaign,Ad Group,Sitelink text,Description 1,Description 2,Final URL
```

If campaign-level (no ad group specified):
```csv
Campaign,Sitelink text,Description 1,Description 2,Final URL
```

### Step 6: Present and Suggest
Show the sitelinks with character counts, then suggest:
- Which sitelinks to pin (if any should always show)
- Mobile vs. desktop considerations (mobile shows fewer — prioritize top 4)
- Seasonal rotations (e.g., "Holiday Offer" sitelink for Q4)

## Quality Rules

1. **No generic titles** — "Learn More" or "Click Here" waste the sitelink
2. **Unique value per sitelink** — each must offer a distinct reason to click
3. **Descriptions matter** — sitelinks with descriptions take more ad real estate
4. **Complement the RSA** — sitelinks should cover angles the headlines don't
5. **CTA-oriented titles** — verbs outperform nouns ("See Plans" > "Pricing Page")
6. **Brand consistency** — tone must match brand voice

## Language-Specific Tips

### English (EN)
- Shortest titles — plenty of room in 25 chars
- CTA conventions: "Get", "See", "Try", "Compare", "Read"

### German (DE)
- Compound nouns are a challenge even at 25 chars
- "Preise vergleichen" (18 ch) > "Preisvergleich ansehen" (22 ch)
- CTA conventions: "Jetzt", "Mehr erfahren", "Ansehen"

### French (FR)
- Articles consume chars: "Voir les tarifs" (15 ch)
- CTA conventions: "Découvrir", "Voir", "Essayer"

### Spanish (ES)
- "Ver precios" (11 ch), "Probar gratis" (13 ch)
- Avoid ¿/¡ in titles to save characters

### Arabic (AR)
- RTL — sitelink titles render right-to-left automatically
- "اكتشف الأسعار" (14 ch), "جرّب مجاناً" (10 ch)
- Keep Latin brand names as-is within Arabic titles

### Polish (PL)
- Verb-first works well: "Sprawdź cennik" (15 ch), "Zobacz demo" (11 ch)
- Diacritics = 1 char each

## Multilingual Sitelinks
When generating sitelinks for multiple languages (used with `/ads-multi`):
- Resolve each sitelink URL per language from the landing pages registry
- Same sitelink structure across languages but native copy (not translations)
- Flag any sitelinks where the target page doesn't exist in a given language
