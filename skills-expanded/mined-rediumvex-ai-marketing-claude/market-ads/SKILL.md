---
name: market-ads
description: Platform-native ad copy for Meta (Facebook/Instagram), Google Search, LinkedIn, TikTok, and YouTube with character-limit compliance, audience targeting notes, and creative briefs. Invoke whenever the user says "ad copy", "Facebook ads", "Google Ads", "LinkedIn ads", "TikTok ads", or runs `/market ads <product>`. Respects platform policies.
---

# Market Ads — Platform-Native Ad Copy

Write ads that follow each platform's character limits, creative norms, and policy rules. Ads that break limits get rejected; ads that fit platform conventions perform better.

## Platform Character Limits (2024+)

### Meta (Facebook / Instagram)
| Element | Limit |
|---|---|
| Primary text | 125 chars recommended (2,200 max, truncates) |
| Headline | 27 chars recommended (40 max) |
| Description | 27 chars recommended |
| Link URL | Must be valid and match destination |

### Google Search (Responsive Search Ads)
| Element | Limit | Count |
|---|---|---|
| Headline | 30 chars | 3–15 |
| Description | 90 chars | 2–4 |
| Final URL | — | 1+ |
| Path (display URL) | 15 chars | 2 |

Sitelinks, callouts, structured snippets are separate extensions.

### LinkedIn
| Element | Limit |
|---|---|
| Intro text | 150 chars recommended (600 max) |
| Headline | 70 chars |
| Description | 100 chars |

LinkedIn audiences read; headlines can be longer than Meta.

### TikTok Ads
| Element | Limit |
|---|---|
| Ad text | 100 chars (no emoji in some regions) |
| Display name | 40 chars |
| Video | 5–60s, 9:16 vertical |

### YouTube
| Element | Limit |
|---|---|
| Headline (in-stream) | 15 chars headline, 70 description |
| Discovery ads | 25 char headline, 35 char descriptions (x2) |

## Creative Frameworks

### The Hook-Insight-Offer structure (Meta / TikTok)
- **Hook (line 1):** pattern interrupt, specific pain, or bold claim
- **Insight (line 2):** why this matters / the turn
- **Offer (line 3):** what to do next with a specific incentive

### The Match-the-Intent structure (Google)
The ad must match the search query. If someone searches "crm for small business":
- Headline 1 includes "crm for small business"
- Headline 2 = differentiator
- Headline 3 = CTA or offer
- Description = proof + benefit

### The B2B structure (LinkedIn)
- Intro: name the audience, name the outcome
- Headline: specific result
- Description: proof + CTA

## Output Format (per platform)

```markdown
## [Platform] Ad Set — [Product / Campaign]

**Audience:** [targeting notes]
**Offer:** [incentive]
**Landing page:** [url]

### Variant A — [Angle name]
- **Primary text / Intro:** "[copy]" (X/125 chars)
- **Headline:** "[copy]" (X/27 chars)
- **Description:** "[copy]" (X/27 chars)
- **Angle:** [what this variant is testing — pain, status, curiosity, social proof]

### Variant B — [Different angle]
...

### Variant C — [Different angle]
...

### Creative brief
- Visual: [describe — single image, carousel, UGC-style video, animated]
- Hook second: [first 3s of video or headline of static]
- CTA button: [Shop Now / Learn More / Sign Up / Download]
```

**Always ship at least 3 variants per platform testing different angles.** Ad platforms learn fastest when fed multiple creatives.

## Testing Matrix

| Variable | Test |
|---|---|
| **Audience** | Broad vs lookalike vs interest vs retargeting |
| **Angle** | Pain vs outcome vs identity vs status |
| **Hook type** | Question vs claim vs story vs stat |
| **Creative** | Static vs video vs UGC vs animated |
| **CTA button** | Learn More vs Sign Up vs Get Offer |

Only test **one variable at a time** — changing creative and audience together gives you no learning.

## Policy Checklist (review before shipping)

- [ ] No unsupported health / financial / dating claims
- [ ] No personal attributes ("are you depressed?") — Meta will reject
- [ ] No before/after photos (Meta health policy)
- [ ] No all-caps or excessive punctuation
- [ ] No "you" targeting implications ("Hey Single Moms in Dallas")
- [ ] Landing page matches ad claim
- [ ] Disclaimers on earnings / results claims
- [ ] Trademarked terms handled correctly (Google brand bidding rules)

If a claim is even slightly borderline, flag it explicitly in the output rather than shipping it and risking account suspension.

## Pre-flight

1. Offer / product / price
2. Target audience
3. Platform(s)
4. Landing page URL
5. Any existing winning ads to preserve angles from
6. Brand voice (load BRAND-VOICE.md if present)

## Quality Bar

- Count the characters. Never ship copy over the limit.
- Never copy the organic social copy into ads — they're different mediums.
- Never promise what the landing page doesn't deliver. Mismatch tanks Quality Score on Google and Relevance Score on Meta.
- Each variant must test a distinct angle — "Variant B: same message, different emoji" is useless.
