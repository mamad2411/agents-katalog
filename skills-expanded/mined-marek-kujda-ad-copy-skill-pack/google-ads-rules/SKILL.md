---
name: google-ads-rules
description: Google Ads RSA specifications, character limits, CSV format, DKI syntax, and quality guidelines. Referenced automatically by /ads and /ads-batch.
disable-model-invocation: false
---

# Google Ads RSA — Platform Rules & Best Practices

## Character Limits (Hard)

| Element        | Max Characters |
|----------------|---------------|
| Headline       | 30            |
| Description    | 90            |
| Path 1         | 15            |
| Path 2         | 15            |
| Final URL      | 2048          |

## RSA Structure
- Up to 15 headlines per ad group (min 3, recommended 15)
- Up to 4 descriptions per ad group (min 2, recommended 4)
- Google mixes and matches — each headline/description must work independently
- Never assume headline order — avoid sequential messaging ("First… Then… Finally…")

## Headline Best Practices
1. Include target keyword in 2–3 headlines for ad relevance
2. Use Dynamic Keyword Insertion `{KeyWord:Default Text}` where appropriate — the whole tag counts as the length of the default text
3. Each headline should test a different angle
4. Pin only when necessary (brand name to H1, CTA to H3)
5. Numbers perform well: "50% Off", "In 24h", "From $99/mo"
6. No duplicate concepts: "Save Money" and "Cut Costs" are too similar

## Description Best Practices
1. Lead with value, end with CTA
2. Specific benefits beat vague claims (numbers > adjectives)
3. Use all 90 characters when possible — more ad real estate = better
4. At least one description should reinforce trust (awards, certs, experience)

## Prohibited
- ❌ ALL CAPS (except brand names / acronyms)
- ❌ Excessive punctuation (!!!, ???, …)
- ❌ Gimmicky spacing (F R E E)
- ❌ Phone numbers in headlines (use call extensions)
- ❌ Trademarked terms without authorization
- ❌ Superlatives without third-party verification ("best", "#1", "top-rated")

## Dynamic Keyword Insertion (DKI)

| Syntax                  | Output                    |
|-------------------------|---------------------------|
| `{keyword:default}`     | all lowercase             |
| `{Keyword:Default}`     | First word capitalized    |
| `{KeyWord:Default}`     | Each Word Capitalized     |
| `{KEYWORD:DEFAULT}`     | ALL CAPS                  |

- DKI character count = length of DEFAULT text
- Mix DKI with static headlines — don't use DKI everywhere
- Avoid DKI in descriptions (reads less naturally)

## Google Ads Editor CSV Format

```csv
Campaign,Ad Group,Headline 1,Headline 2,Headline 3,Headline 4,Headline 5,Headline 6,Headline 7,Headline 8,Headline 9,Headline 10,Headline 11,Headline 12,Headline 13,Headline 14,Headline 15,Description 1,Description 2,Description 3,Description 4,Path 1,Path 2,Final URL
```

## Ad Strength
- Google rates RSA Ad Strength from Poor to Excellent
- 15 unique headlines + 4 descriptions + keyword presence + diverse messaging → Excellent
- Ad Strength ≠ performance — a "Good" ad with great copy can outperform "Excellent"

## Multilingual Notes
- French accents (é,è,ê,ë,à,â,ç,ù,û,ü,ï,î,ô) = 1 char each
- Spanish accents (á,é,í,ó,ú,ñ,ü) = 1 char each; avoid ¿/¡ in headlines to save space
- German compound words consume character limits fast — prepare alternatives
- Arabic characters = 1 char each; omit tashkeel diacritics to save space; Latin brand names stay as-is
- Polish diacritics (ą,ć,ę,ł,ń,ó,ś,ź,ż) = 1 char each
- Always count characters in the TARGET language, not a translation
