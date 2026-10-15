---
name: aso-auditor
version: 1.0.0
description: >
  ASO (App Store Optimization) Scoring Checklist Auditor. Triggers automatically
  whenever a user pastes an App Store URL (apps.apple.com) or Google Play Store URL
  (play.google.com/store/apps), or asks to audit, score, review, or optimize an app
  listing, app store page, or app metadata. Also triggers on phrases like "ASO audit",
  "app store checklist", "optimize my app listing", "score my app", "screenshot
  feedback", "keyword review", or any mention of app store ranking, conversion rate,
  or app visibility. Always read this full skill before producing any ASO-related
  output — do not attempt to score or advise without consulting this file.
---

# ASO Scoring Checklist Auditor

A structured, production-grade ASO audit skill built on a 7-pillar, 155-point scoring
framework. Outputs an interactive MDX report, an opportunities table, a 90-day roadmap,
and a keyword testing lab for every audit session.

---

## 1. SKILL METADATA

| Field | Value |
|---|---|
| **Name** | aso-auditor |
| **Version** | 1.0.0 |
| **Trigger** | Fires on any App Store or Google Play URL paste, or on phrases: "ASO audit", "app store score", "optimize app listing", "screenshot review", "keyword field", "app metadata", "Play Store ranking", "app conversion rate" |
| **Platforms covered** | iOS App Store + Google Play Store |
| **Max score** | 155 pts → normalized to 0–100% Optimization Grade |
| **Output format** | Interactive MDX file deployable in Next.js 14 + @next/mdx |

---

## 2. INPUT SCHEMA

### Required inputs
| Field | Format | Example |
|---|---|---|
| `ios_url` | Full App Store URL | `https://apps.apple.com/us/app/example/id123456789` |
| `play_url` | Full Play Store URL | `https://play.google.com/store/apps/details?id=com.example.app` |
| `app_category` | Text string | `Finance`, `Productivity`, `Health & Fitness` |

### Optional inputs
| Field | Format | Notes |
|---|---|---|
| `asc_export` | CSV or JSON from App Store Connect | Keyword ranking data, impressions, CVR |
| `play_export` | CSV or JSON from Google Play Console | Search terms report, install funnel |
| `datai_export` | CSV or JSON from Data.ai / App Annie | Market share, category ranking |
| `competitor_urls` | Comma-separated URLs | Up to 3 competitor listings for gap table |

### Validation rules
- **Only one platform URL provided**: Score available platform only. Flag missing platform.
  Output message: "⚠️ Only [iOS / Android] URL provided. Android / iOS score will be
  marked N/A. Provide the second URL to enable platform delta analysis."
- **URL inaccessible / 404**: Attempt `web_fetch` twice. If both fail, prompt user to
  paste raw listing text (title, subtitle, description, screenshot count, rating).
- **Notion knowledge base JS-blocked**: Fall back to embedded ruleset in this file.
  Do not halt the audit.
- **No competitor URLs**: Skip Section 11 competitor table. Insert placeholder row:
  "No competitor URLs provided — run competitor comparison to unlock gap analysis."

---

## 3. PRE-AUDIT RESEARCH PROTOCOL

Execute in this exact sequence at the start of every audit session.

### Step 3.0 — URL normalisation (do this before any fetch)

Google Play and the App Store both serve JS-heavy pages that block desktop crawlers.
Always rewrite URLs to their mobile-friendly forms before fetching.

**Android — append locale params:**
```
Original:  https://play.google.com/store/apps/details?id=com.example.app
Rewritten: https://play.google.com/store/apps/details?id=com.example.app&hl=en&gl=us
```

**iOS — append country and language params:**
```
Original:  https://apps.apple.com/us/app/example/id123456789
Rewritten: https://apps.apple.com/us/app/example/id123456789?l=en
```

Use the rewritten URLs for all `web_fetch` calls in Steps 3.1 and 3.2.

---

### Step 3.1 — Fetch live listing: iOS
```
web_fetch: {ios_url_rewritten}
```
Extract and log in the **Metadata Extraction Table** (see below):
- App title (count chars)
- Subtitle (count chars)
- Promotional text (count chars, note: not indexed)
- Description first 170 chars (above-fold preview)
- Full description (char count)
- Keyword field (not visible; note "not public-facing")
- Screenshot count
- Screenshot orientations (portrait / landscape)
- App preview video present? — **see critical note below**
- Overall rating (X.X / 5)
- Total review count
- Developer response rate (sample last 10 reviews)

**⚠ CRITICAL — iOS preview video is NEVER detectable from a crawler fetch.**
The App Store serves preview videos as dynamically generated `blob:` URLs
(`src="blob:https://apps.apple.com/..."`). These are resolved in the browser session
and are invisible to `web_fetch`. The crawler will always return no video element,
regardless of whether a video exists on the listing.

**Rule:** Never mark iOS criterion 6.1 as fail based on a crawler result alone.
Always ask the user to confirm before scoring Pillar 6.

The correct protocol is:
1. After fetching, note "iOS preview video — cannot verify via crawler"
2. Ask the user directly: "Does your iOS App Store listing have an app preview video?
   You can check by visiting your listing on a device, or in App Store Connect under
   the relevant version's media assets."
3. Score criterion 6.1 based on the user's answer only.
4. If the user cannot confirm, mark as `[UNVERIFIED — ask user before scoring]`
   and do not auto-fail.

**If the fetch returns a JS-block error or yields < 3 auditable fields:** do not halt.
Proceed immediately to Step 3.1a.

#### Step 3.1a — iOS manual input fallback
If the automated fetch fails or any of the following fields are missing, prompt the user
for each missing field individually in this exact order. Do not ask for all fields at once.

```
"I couldn't fully read your App Store listing automatically. I'll ask for the missing
fields one at a time — you can copy-paste from App Store Connect or from the live listing.

1. What is your app title? (paste exactly as it appears on the listing)
2. What is your subtitle? (paste exactly, or type "none" if not set)
3. What is your promotional text? (paste exactly, or "none" if empty)
4. What is your keyword field? (paste from App Store Connect > App Information > Keywords)
5. Paste your full description text below.
6. How many screenshots are uploaded? Which device sizes?
7. Does your listing have an app preview video? (yes / no — check on your device or
   in App Store Connect; the crawler cannot detect this)
8. What is your current overall rating and total review count?"
```

Log each answer into the Metadata Extraction Table before proceeding to scoring.

---

### Step 3.2 — Fetch live listing: Android
```
web_fetch: {play_url_rewritten}
```
Extract and log:
- App title (count chars)
- Short description (count chars)
- Long description (char count; estimate keyword density for top 3 terms)
- Feature graphic present? (Y/N; describe if logo-only or lifestyle)
- Screenshot count
- Preview video present? (YouTube link if visible)
- Icon dimensions (verify 512×512 standard)
- Overall rating (X.X / 5)
- Total review count
- Developer response rate (sample last 10 reviews)

**Known crawling limitation:** Google Play's short description field is frequently
omitted from desktop crawler responses even when present on the live listing. If short
description is absent from the fetch result, do not assume it is missing from the listing.
Proceed to Step 3.2a before marking it as a gap.

**If the fetch returns a JS-block error or yields < 3 auditable fields:** proceed to
Step 3.2a immediately.

#### Step 3.2a — Android manual input fallback
If the automated fetch fails or any of the following fields are missing, prompt for each
individually in this order:

```
"I couldn't fully read your Play Store listing automatically. I'll ask for the missing
fields one at a time — you can copy-paste from Play Console or from the live listing.

1. What is your app title? (paste exactly)
2. What is your short description? (the 80-char line shown above the fold — paste exactly,
   or type "none" if you haven't set one)
3. Paste your full long description below.
4. How many screenshots are uploaded?
5. Is there a preview video? (Y/N — if yes, paste the YouTube URL)
6. Does your listing have a feature graphic? (Y/N — if yes, describe: lifestyle image,
   product mockup, or logo on solid background?)
7. What is your current overall rating and total review count?"
```

Log each answer into the Metadata Extraction Table before proceeding to scoring.

---

### Step 3.2b — Screenshot and icon image analysis protocol

**Pillar 2 (App Icon) and Pillar 5 (Screenshots) cannot be scored from text alone.**
The following fields require visual inspection:

| Field | Required for | When to request |
|---|---|---|
| App icon image | Pillar 2.1–2.4 | Always — icon is never extractable from fetch text |
| Screenshot images (all uploaded slots) | Pillar 5.2–5.5 | When fetch returns no visible screenshot content |
| Feature graphic image (Android) | Pattern 3 assessment | When fetch does not describe the feature graphic |

**Protocol:**

1. After completing Steps 3.1/3.2 and any manual fallbacks, check whether screenshot
   and icon images were returned in the fetch.
2. If images are absent or descriptions are insufficient to score visual criteria,
   output this exact prompt before scoring Pillars 2 and 5:

```
"To score your icon and screenshots accurately, I need to see the actual images.
Please upload:
  - Your app icon (the square image shown in search results)
  - All screenshots currently live on your listing (drag them in or upload as a zip)

If uploading isn't convenient, describe each screenshot in one sentence:
  Screenshot 1: [what it shows, whether it has a caption, approximate caption text]
  Screenshot 2: [same]
  ...and so on."
```

3. Once images or descriptions are received, score Pillars 2 and 5 using the visual
   criteria in Section 4. If neither images nor descriptions are provided after prompting,
   mark Pillars 2 and 5 as **"Unscored — visual data required"** and exclude them from
   the Optimization Grade calculation, noting the exclusion in the report header.

4. **When images ARE provided:** Claude must reference specific visual observations in
   every Pillar 2 and Pillar 5 finding. Example: "Screenshot 1 shows a white background
   with the app logo centred and no caption text — this fails criterion 5.3 (readable
   captions) and 5.4 (core value communication)." Generic descriptions like "icon appears
   simple" are not acceptable when the actual image is available.

### Step 3.3 — Metadata Extraction Table
Render this table before scoring begins. Every auditable field, both platforms.

| Field | iOS Value | iOS Limit | iOS Utilization | Android Value | Android Limit | Android Utilization |
|---|---|---|---|---|---|---|
| App title | [extracted] | 30 chars | [N/30 = X%] | [extracted] | 30 chars | [N/30 = X%] |
| Subtitle / Short desc | [extracted] | 30 chars (iOS) / 80 chars (Android) | [X%] | [extracted] | 80 chars | [X%] |
| Keyword field | [not public] | 100 chars | [unknown — flag] | N/A — embedded in desc | — | — |
| Promotional text | [extracted] | 170 chars | [X%] | N/A | — | — |
| Full description | [char count] | No hard limit | — | [char count] | 4,000 chars | [X%] |
| Screenshots | [count] | 10 max | [N/10] | [count] | 8 max | [N/8] |
| App preview video | **[UNVERIFIABLE via crawler — always ask user]** iOS videos are blob URLs invisible to web_fetch | 3 max (iOS) | — | [Y/N / YouTube URL — visible in fetch] | 1 video | — |
| Feature graphic | N/A | — | — | [Y/N; lifestyle or logo?] | 1024×500px | — |
| Overall rating | [X.X] | — | — | [X.X] | — | — |
| Review count | [N] | — | — | [N] | — | — |
| Developer responses | [Y/N in last 10?] | — | — | [Y/N in last 10?] | — | — |

### Step 3.4 — Platform rules lock-in (embedded; no external fetch required)

**iOS (App Store) — verified limits:**
- Title: 30 chars max (Apple App Store Connect)
- Subtitle: 30 chars max (Apple App Store Connect)
- Keyword field: 100 chars max; single words separated by commas; no spaces after commas
  (Apple App Store Connect). Not visible to users.
- Promotional text: 170 chars max; updatable without a new app version; NOT indexed by
  the algorithm; conversion-impacting only.
- Screenshots: 1–10 per localization; 2025 mandatory primary sizes:
  - **iPhone**: 6.9" (1320×2868 px or 2868×1320 px) — **required primary as of 2025**
  - **iPad**: 13" (2064×2752 px or 2752×2064 px) — **required primary as of 2025**
  - Older 6.7" / 6.5" / 5.5" sizes still accepted but no longer primary
- App preview video: up to 3 per device size; 15–30 seconds; autoplay is MUTED;
  must be self-explanatory without audio.
- Keyword hierarchy (ranking weight): Title > Subtitle > Keyword field
- Prohibited keyword categories (Guideline 2.3.7): competitor app names, Apple product
  names, irrelevant third-party trademarks, category names used deceptively.
- Metadata accuracy (Guideline 2.3.8): metadata must accurately reflect app content and
  functionality; misleading descriptions are grounds for rejection.
- Localization: each additional locale expands keyword indexing (keywords from secondary
  locales are indexed in primary market searches).

**Android (Google Play) — verified limits:**
- Title: 30 chars max (Google Play Console policy)
- Short description: 80 chars max; shown above the fold; primary conversion copy.
- Long description: 4,000 chars max; primary keyword indexing field; no dedicated
  keyword field exists.
- Icon: 512×512 px, 32-bit PNG, max 1 MB.
- Feature graphic: 1024×500 px, JPEG or 24-bit PNG, max 1 MB; occupies ~60% of
  above-fold space on store listing; must be lifestyle or product image, not logo-only.
- Screenshots: minimum 2 required; up to 8 recommended.
- Preview video: via YouTube link; 30–120 seconds; public or unlisted; autoplay is MUTED.
- Keyword indexing: title + short description + long description (no separate keyword field).
- Prohibited title words (Google Play Metadata policy): "free", "sale", "best", "top",
  "#1", "download now", "update", "App of the Year", performance claims, ranking claims,
  ALL CAPS (unless brand name), emojis/emoticons, repeated special characters.
- Keyword density in long description: target ~1% for primary keyword; avoid >2% for any
  single term (keyword stuffing flag risk).
- Google Play indexes only the active interface language locale.

---

## 4. SCORING RUBRIC

**Total maximum: 155 pts. Normalization formula: `Optimization Grade = (Raw Score / 155) × 100`**

Score iOS and Android separately. Flag platform divergence > 15 percentage points.

### PILLAR 1 — App Title + Subtitle (iOS) / App Title + Short Description (Android)
**Max: 25 pts**

| # | Sub-criterion | Max pts | Pass definition | Fail definition | Source |
|---|---|---|---|---|---|
| 1.1 | No duplicate keywords across title and subtitle/short desc | 5 | Zero repeated root words across both fields | Any keyword appears in both fields | Expert benchmark; Apple/Google both penalize keyword duplication across indexed fields |
| 1.2 | Character utilization ≥ 80% of limit | 5 | Title ≥ 24/30 chars; subtitle ≥ 24/30 (iOS) or short desc ≥ 64/80 (Android) | Any field below 80% utilization | Apple/Google field limits; unused chars = wasted indexing surface |
| 1.3 | Most important keyword placed first | 5 | Primary conversion keyword appears in first 15 chars of title | Title leads with brand name only or a weak generic word | Expert benchmark: algorithm weights first tokens more heavily [uncertain — exact weight distribution not public] |
| 1.4 | Keywords combine to form additional search terms | 5 | Title + subtitle word combination unlocks ≥ 2 additional compound search terms | Title and subtitle are standalone fragments with no combinatorial value | Expert ASO benchmark from production audits |
| 1.5 | Short description in full sentences, no keyword stuffing — **Android only** | 5 | Full grammatical sentence; reads naturally; primary keyword appears once | Reads as a keyword list; fragments; brand name leads the sentence | Google Play Metadata policy; conversion copy best practice |

**Pillar 1 total: /25**

---

### PILLAR 2 — App Icon
**Max: 20 pts**

| # | Sub-criterion | Max pts | Pass definition | Fail definition | Source |
|---|---|---|---|---|---|
| 2.1 | Simple, scalable design legible at small sizes | 5 | Recognizable at 29×29px (notification size); no text-heavy or cluttered design | Small icon is indistinct; text unreadable at notification sizes | Apple HIG; Google Play icon specification |
| 2.2 | Strong brand association / recognizability | 5 | Icon uses brand color or logo element consistently with other brand touchpoints | Icon looks unrelated to brand identity; could belong to any app | Expert benchmark from production audits |
| 2.3 | Unique and differentiated from competitors | 5 | Color, shape, and concept clearly distinct from top 5 category competitors | Icon is generic or nearly identical to a competitor | Expert benchmark |
| 2.4 | Eye-catching, draws attention in search results | 5 | Bold contrast, clear focal point, strong color; performs above category CVR average | Muted, low-contrast, or visually crowded; blends into results grid | Expert benchmark; A/B test data from AppRadar / SplitMetrics [uncertain — category-specific] |

**Pillar 2 total: /20**

---

### PILLAR 3 — Keywords & Metadata
**Max: 25 pts**

#### iOS sub-criteria:
| # | Sub-criterion | Max pts | Pass definition | Fail definition | Source |
|---|---|---|---|---|---|
| 3.1 | Keyword field uses simple single-word units, comma-separated | 5 | All tokens are single words; no spaces wasted; no phrases that duplicate title/subtitle | Phrases used instead of single words; duplicates title words; spaces after commas | Apple App Store Connect keyword field best practice |
| 3.2 | 100-char keyword field fully utilized (≥ 95 chars) | 5 | Field is 95–100 chars | Field < 80 chars | Apple App Store Connect field limit |
| 3.3 | High-volume keywords targeted (verified via ASA or third-party tool) | 5 | At least 3 of 5 targeted keywords have popularity score ≥ 40/100 on a tool like AppFollow / App Radar | All keywords are low-volume or unmeasured | Expert benchmark; AppFollow keyword popularity scoring [uncertain — exact threshold varies by category] |
| 3.4 | Top organic ranking achieved for primary keyword | 5 | Ranks in top 10 results for stated primary keyword | Not ranking in top 50 for any targeted keyword | Expert benchmark |
| 3.5 | Ranks above key competitors for ≥ 1 shared keyword | 5 | Outranks at least 1 named competitor on a shared high-volume term | Consistently below all competitors on shared terms | Expert benchmark |

#### Android sub-criteria:
| # | Sub-criterion | Max pts | Pass definition | Fail definition | Source |
|---|---|---|---|---|---|
| 3.1 | 5–7 focus keywords identified and embedded naturally in long description | 5 | 5–7 distinct keyword themes visible; each appears naturally in context | No identifiable keyword strategy; fewer than 3 themes; or pure stuffing | Google Play indexing mechanism; long desc is sole keyword source |
| 3.2 | Keyword density for primary term ~1% (not exceeding 2%) | 5 | Primary keyword appears once per 100 words on average | Primary keyword density >2% (keyword stuffing risk) | Google Play Metadata policy; expert benchmark |
| 3.3 | High-impact terms targeted | 5 | Primary and secondary keywords have measurable search volume | All chosen terms are niche or unmeasured | Expert benchmark |
| 3.4 | Top organic ranking for primary keyword | 5 | Ranks in top 10 for stated primary keyword | Not ranking in top 50 | Expert benchmark |
| 3.5 | Ranks above key competitors for ≥ 1 shared keyword | 5 | Outranks ≥ 1 named competitor on a shared term | Below all competitors on all shared terms | Expert benchmark |

**Pillar 3 total: /25**

---

### PILLAR 4 — Description (iOS Long Desc / Android Long Desc)
**Max: 25 pts**

| # | Sub-criterion | Max pts | Pass definition | Fail definition | Source |
|---|---|---|---|---|---|
| 4.1 | Formatted with clear structure (bullets, line breaks, headers) | 5 | Scannable in 10 seconds; uses line breaks, emoji bullets, or bold headers | Wall of text with no visual breaks | UX best practice; Google Play metadata policy (avoid excessive formatting but structure is required) |
| 4.2 | Covers all identified target keywords | 5 | Every keyword from the keyword field (iOS) or keyword strategy (Android) appears at least once in description | Multiple target keywords absent from description | ASO expert benchmark; description feeds secondary indexing on iOS |
| 4.3 | Builds on title and subtitle — does not repeat them verbatim | 5 | First paragraph introduces new information not in title/subtitle | First sentence restates title; description is a verbatim expansion of header fields | Keyword duplication wastes indexing surface; expert benchmark |
| 4.4 | Clear CTA present | 5 | At least one action phrase (e.g., "Download free", "Start your trial today", "Join X million users") | No CTA anywhere in description | Conversion optimization best practice |
| 4.5 | Branded voice consistent with update notes and listing identity | 5 | Tone, reading level, and brand voice match across description, update notes, and developer reply voice | Inconsistent voice (corporate vs casual); update notes are generic "Bug fixes" | Trust and brand coherence; expert benchmark |

**Pillar 4 total: /25**

---

### PILLAR 5 — Screenshots
**Max: 25 pts**

| # | Sub-criterion | Max pts | Pass definition | Fail definition | Source |
|---|---|---|---|---|---|
| 5.1 | 7 or more screenshots uploaded (iOS: up to 10; Android: up to 8) | 5 | iOS: 7–10 screenshots; Android: 6–8 screenshots | iOS: fewer than 7; Android: fewer than 6 | Apple App Store Connect (1–10 allowed); Google Play (minimum 2, up to 8) |
| 5.2 | Sufficient contrast and visual hierarchy in each frame | 5 | Background-to-text contrast ratio ≥ 4.5:1 (WCAG AA); key element is immediately visible | Low contrast; text washes into background; crowded layout | WCAG 2.1 AA contrast guideline; expert benchmark |
| 5.3 | ≥ 80% of screenshots have readable captions | 5 | At least 6/7 (iOS) or 5/6 (Android) screenshots have caption text ≥ 18pt equivalent | Most screenshots have no captions, or captions are too small to read on a 6" phone | Expert benchmark; caption text is primary keyword surface on visual assets |
| 5.4 | First 2–3 screenshots clearly communicate core value; captions readable at a glance | 5 | Slot 1: main benefit; Slot 2: USP; Slot 3: social proof or key use case; each caption legible without zooming | First screenshot shows a generic feature or app splash screen; no clear value statement | SplitMetrics / StoreMaven A/B test data: first 2 screenshots drive majority of conversion decision [uncertain — exact % varies by category] |
| 5.5 | CTA or download prompt visible in final screenshot | 5 | Last screenshot includes "Download", "Try free", "Start now" or similar prompt | Final screenshot is an arbitrary feature shot with no closing hook | Conversion optimization best practice; expert benchmark |

**Screenshot specifications to verify:**
- iOS 2025 primary required sizes: **6.9" iPhone** (1320×2868 px portrait) and **13" iPad** (2064×2752 px portrait)
- Android: screenshots must be at least 320px on shortest side; JPEG or PNG; max 8 MB each

**Pillar 5 total: /25**

---

### PILLAR 6 — App Preview Video
**Max: 20 pts**

| # | Sub-criterion | Max pts | Pass definition | Fail definition | Source |
|---|---|---|---|---|---|
| 6.1 | Preview video present | 5 | At least 1 app preview video uploaded and visible on listing | No video; screenshots-only listing | Apple App Store Connect (up to 3 per device size); Google Play (YouTube link) |
| 6.2 | Clearly explains app value within first 5 seconds | 5 | Value proposition visible in first 5 seconds without audio; hero moment not buried | Video opens with generic loading screen, logo animation, or lengthy intro | Best practice: autoplay is MUTED on both platforms; first 5 seconds must convert visually |
| 6.3 | Reinforces title and subtitle keywords visually | 5 | On-screen text in video includes ≥ 2 keywords from title/subtitle or keyword field | Video has no text overlays; value is purely audio-dependent | Expert benchmark; video is a visual keyword surface for conversion |
| 6.4 | Includes a clear CTA or closing hook | 5 | Final frame shows download prompt, rating, or strong closing benefit statement | Video ends on a loading screen or generic end card | Conversion optimization best practice |

**Note:** Autoplay is muted on both App Store and Google Play. Content MUST be visually self-explanatory without audio.

**Pillar 6 total: /20**

---

### PILLAR 7 — Ratings & Reviews
**Max: 15 pts**

| # | Sub-criterion | Max pts | Pass definition | Fail definition | Source |
|---|---|---|---|---|---|
| 7.1 | Overall rating ≥ 4.0 (4.5+ = full 5 pts) | 5 | Rating ≥ 4.5 = 5 pts; 4.0–4.49 = 3 pts; 3.5–3.99 = 1 pt; < 3.5 = 0 pts | Rating < 4.0 causes measurable conversion drag; < 3.5 triggers store demotion risk | AppFollow / AppRadar best practice: 4.0+ is minimum viable; 4.5+ signals category leader |
| 7.2 | ≥ 50% of reviews are 5-star | 5 | 5-star reviews comprise majority of visible review mix | Majority are 1–3 star; or 5-star rate < 40% | Expert benchmark |
| 7.3 | Developer responds personally to reviews | 5 | Developer response visible on ≥ 50% of reviews in last 30 days; responses are personalized (not templated) | No developer responses; or all responses are identical templates | Google Play and Apple App Store both surface developer responses; personalized replies increase review quality [uncertain — exact algorithm weight not public] |

**Pillar 7 total: /15**

---

### Scoring summary table (fill per audit)

| Pillar | iOS Raw | iOS Max | Android Raw | Android Max |
|---|---|---|---|---|
| 1. Title + Subtitle / Short Desc | | 25 | | 25 |
| 2. App Icon | | 20 | | 20 |
| 3. Keywords & Metadata | | 25 | | 25 |
| 4. Description | | 25 | | 25 |
| 5. Screenshots | | 25 | | 25 |
| 6. App Preview Video | | 20 | | 20 |
| 7. Ratings & Reviews | | 15 | | 15 |
| **TOTAL** | | **155** | | **155** |
| **Optimization Grade** | **(iOS / 155) × 100 = X%** | | **(Android / 155) × 100 = X%** | |

**Platform delta:** If |iOS% - Android%| > 15, flag: "⚠️ Platform divergence of [X]pp detected. See Section 5 for field-by-field comparison."

---

## 5. PLATFORM DELTA TABLE

Side-by-side reference for every auditable field. Render this table in every audit to anchor scoring decisions.

| Field | iOS App Store | Android Google Play |
|---|---|---|
| Title char limit | 30 | 30 |
| Subtitle / Short desc limit | 30 (subtitle) | 80 (short description) |
| Keyword field | 100 chars; comma-separated single words; NOT shown to users | None — keywords embedded in title + short desc + long desc |
| Promotional text | 170 chars; updatable without app update; NOT indexed | None |
| Long description char limit | No hard limit (recommended < 4,000) | 4,000 chars |
| Keyword hierarchy | Title > Subtitle > Keyword field | Title > Short desc > Long desc |
| Icon spec | No separate upload spec (auto-generated from app binary) | 512×512 px, 32-bit PNG, max 1 MB |
| Feature graphic | None | 1024×500 px, JPEG or 24-bit PNG, max 1 MB |
| Screenshots: min / max | 1 / 10 | 2 / 8 |
| 2025 primary screenshot sizes | 6.9" iPhone (1320×2868 px); 13" iPad (2064×2752 px) | No fixed primary size; minimum 320px shortest side |
| Preview video | Up to 3 per device size; 15–30 sec; autoplay muted; self-hosted | 1 YouTube link; 30–120 sec; public or unlisted; autoplay muted |
| Prohibited title words | Competitor names (2.3.7); misleading claims (2.3.8); Apple trademarks | "free", "sale", "best", "top", "#1", "download now", "update", "App of the Year", ALL CAPS, emojis, ranking claims |
| Localization & keyword indexing | Additional locales expand keyword indexing in primary market | Only active interface language locale is indexed |
| Rating threshold for conversion | 4.0+ minimum; 4.5+ = category leader signal | 4.0+ minimum; 4.5+ = category leader signal |
| Developer reply surface | Visible on product page; public | Visible on product page; public |
| A/B testing native tool | Product Page Optimization (App Store Connect) | Store Listing Experiments (Play Console) |
| Minimum A/B test window | 7 days (recommended) | 14 days (recommended) |

---

## 6. INTERACTIVE HTML REPORT — DELIVERY AND ARCHITECTURE

### How to deliver

Use Claude's **`visualize:show_widget`** tool to render the audit report inline in the
conversation. This requires no build step, no file download, no Next.js, and no MDX
setup. The report renders immediately inside Claude.ai.

**Do not** output the code as a JSX artifact block or a downloadable file. The
`show_widget` tool is the correct delivery mechanism — it streams the HTML directly
into the chat and makes it immediately interactive.

**Technical rules for the HTML widget:**
- Pure HTML + vanilla JS only. No React. No external libraries.
- Inline `style` attributes throughout — no `<style>` blocks except for short shared
  rules (< 15 lines). Never reference Tailwind classes.
- Use CSS variables from Claude's design system: `--color-text-primary`,
  `--color-background-secondary`, `--color-border-tertiary`, `--font-sans`,
  `--border-radius-md`, `--border-radius-lg`. These auto-adapt to light/dark mode.
- No `position: fixed`. No nested scrolling. No `display: none` during initial render.
- All audit data (pillar scores, findings, fixes, opportunity rows, keyword variants,
  roadmap) is hardcoded as `const` arrays at the top of the `<script>` block.
- The widget is fully self-contained. All state lives in plain JS variables, updated
  via `innerHTML` re-render on user interaction.

---

### ⚠️ CRITICAL SCORING ANTI-PATTERNS — never do these

Two bugs have been confirmed in production. Both produce wrong scores. Both are
preventable. Read before writing any score-related code.

**Anti-pattern 1 — Getter double-counting:**
```js
// WRONG — do not do this
const IOS_AUDIT = {
  p1: 25, p2: 15, p3: 20,
  get total() { return this.p1 + this.p2 + this.p3; } // ← DANGER
};
Object.values(IOS_AUDIT).reduce((s, v) => s + v, 0);
// Object.values() INVOKES the getter and includes its return value in the array.
// Result: 25+15+20+60 = 120 — the total is counted TWICE.
// Displayed grade: (120/155)×100 = 77% instead of correct 39%.
```

**Anti-pattern 2 — Dual source of truth drift:**
```js
// WRONG — do not do this
const IOS_AUDIT = { p1: 25, p2: 18, p3: 20 }; // manually set
const pillars = [ /* p2 initial passes only sum to 15, not 18 */ ];
// Frozen score card shows 73%. Pillar bar for P2 shows 15/20.
// User sees inconsistent numbers before touching any checkbox.
```

**The correct pattern — single source of truth:**
```js
// RIGHT — always do this
const INIT_PILLARS = [ /* all criteria with pass: true/false per platform */ ];

// Frozen audit scores: computed ONCE from INIT_PILLARS, never recomputed.
function computeScore(pillars, plat) {
  return pillars.reduce((s, p) =>
    s + p.criteria.reduce((cs, c) => cs + (c[plat].pass ? c.pts : 0), 0), 0);
}
const IOS_AUDIT_SCORE = computeScore(INIT_PILLARS, 'ios'); // plain const, never changes
const AND_AUDIT_SCORE = computeScore(INIT_PILLARS, 'and'); // plain const, never changes

// Live scores: recomputed from mutable state on every toggle.
// In the render loop, always call computeScore(currentPillars, plat).
```

The frozen audit score and the initial live score MUST be equal when the page first
loads. If they differ, there is a source-of-truth mismatch — stop and debug before
delivering.

---

### Binary scoring rule

Every sub-criterion scores either its full `pts` value or `0`. Never assign partial
points within a criterion (e.g., 3/5 or 4/5). The binary constraint is what makes the
live simulation meaningful — toggling a checkbox always produces a clean +5, +5, or
+5 change that the user can map to a specific action.

**When visual data is unavailable** (screenshots not uploaded, icon not visible):
- Still score binary: mark as `pass: false` and add `[ESTIMATED — upload screenshots
  to verify]` to the finding text.
- Do not give partial credit to compensate for uncertainty.
- Do not skip the criterion — mark it false and flag it.

---

### Criterion data structure

Each criterion must follow this exact shape. The nested `ios` / `and` objects are the
proven working pattern. The old flat `passed` / `android_passed` pattern caused
scoring bugs and is deprecated.

```js
{
  id: '2.3',
  label: 'Unique and differentiated from competitors',
  pts: 5,
  ios: {
    pass: false,  // boolean — full pts or 0, never fractional
    finding: 'Dark navy blends with Xoom, Western Union, MoneyGram in search grids...',
    fixes: [
      { t: 'A', x: 'Test icon variant with teal background — copy-only, no designer needed...' },
      { t: 'B', x: 'Run Product Page Optimization: current navy vs teal vs white. 7+ days...' },
      { t: 'C', x: 'Screenshot the "money transfer" search grid at 48px scale. If Remitly...' },
    ]
  },
  and: {
    pass: false,
    finding: 'Same differentiation gap on Android. Finance category is dense with dark blue.',
    fixes: [
      { t: 'A', x: 'Same teal background test as iOS via Store Listing Experiment...' },
      { t: 'B', x: 'Compare tap-through rate of current icon vs lighter-palette variant...' },
      { t: 'C', x: 'If test shows no CTR lift, icon is already optimal — document and move on.' },
    ]
  }
}
```

**Rules:**
- `pass` is always `true` or `false`. Never `null`, never a number.
- `fixes` is only populated when `pass: false`. Empty array `[]` when passing.
- `finding` is always present, for both pass and fail — the passing finding explains WHY it passes.
- Every fix must cite actual listing text or data (see Section 7 mandatory rule).

---

### Score display — three-card hero layout

The hero scoreboard has exactly three metric cards:

| Card | Label | Source | Behaviour |
|---|---|---|---|
| 1 | iOS Audit Score | `IOS_AUDIT_SCORE` (const) | Never changes — frozen baseline |
| 2 | Android Audit Score | `AND_AUDIT_SCORE` (const) | Never changes — frozen baseline |
| 3 | Live Simulation | `computeScore(pillars, plat)` | Updates on every checkbox toggle |

Card 3 has a dashed border to visually distinguish it from the frozen cards.

**Toggle placement — inside the Live card, not below the hero.**
The platform toggle buttons (`🍎 iOS` / `🤖 Android`) must live inside the Live
simulation card header — not in a separate row below the three cards. The toggle
controls what the Live card displays, so they must be co-located with it.

```
┌── iOS frozen ──┐  ┌── Android frozen ──┐  ┌── Live (dashed) ──────────┐
│ 71%            │  │ 74%                │  │ [🍎 iOS] [🤖 Android]      │
│ 100/155 · ...  │  │ 115/155 · ...      │  │ 78%                        │
└────────────────┘  └────────────────────┘  │ 120/155 · toggle below     │
                                             └────────────────────────────┘
```

The toggle switches:
- Which platform's pass states the checklist displays
- Which platform the Live score reflects
- The pillar bar percentages within the checklist

The frozen iOS and Android cards are **always both visible** regardless of which
platform the toggle is set to. They are the permanent audit record and must never
update when checkboxes are toggled.

The footnote `Audit: 71% · Live: 78%` may be shown inline within the Live card or
below it — **do not render a separate toggle row below the three cards.**

---

### Single-platform hero layout

When only one platform URL is provided (iOS-only or Android-only audit):

**The unavailable platform card** shows "N/A" with muted grey styling:
```js
// iOS-only example — Android card is N/A
{ lbl:'Android audit score', na:true, sub:'Android URL not provided' }
```
Render the N/A card with `color: var(--color-text-secondary)`, no progress bar fill,
and the sub-label explaining why. Do not show a score or pts count.

**The Live card** shows a static platform badge inside the card header instead of
toggle buttons — since there is only one platform, no switching is needed:
```
┌── Live (dashed) ──────────────┐
│ LIVE  [iOS only]              │  ← badge replaces toggle buttons
│ 48%                           │
│ 74/155 · Toggle to simulate   │
└───────────────────────────────┘
```

The `[iOS only]` / `[Android only]` badge is a small dark pill: `background:
var(--color-text-primary); color: var(--color-background-primary); font-size: 11px;
padding: 2px 8px; border-radius: 99px;`

**No platform toggle is rendered anywhere** in a single-platform audit — not in the
Live card, not below the hero. The checklist label ("iOS only · toggle to simulate
fixes") communicates the platform context without buttons.

**Scoring for the unavailable platform:** all criteria for the missing platform
auto-pass (`pass: true`) with `finding: 'N/A — [platform] not provided.'` and
`fixes: []`. This keeps the data structure consistent but those criteria never
contribute to a visible score. The `computeScore()` call only uses the available
platform's data.

---

### Complete HTML scaffold

```html
<style>
/* Shared rules only — keep under 15 lines */
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font-sans);font-size:14px;color:var(--color-text-primary)}
.card{background:var(--color-background-primary);border:0.5px solid var(--color-border-tertiary);border-radius:var(--border-radius-lg);padding:1.25rem;margin-bottom:1rem}
.lbl{font-size:11px;color:var(--color-text-secondary);text-transform:uppercase;letter-spacing:.03em;margin-bottom:4px}
.pill{display:inline-block;padding:2px 8px;border-radius:20px;font-size:11px;font-weight:500}
.pr{background:#FCEBEB;color:#A32D2D}.pa{background:#FAEEDA;color:#854F0B}.pg{background:#EAF3DE;color:#3B6D11}.pb{background:#E6F1FB;color:#185FA5}
.fix-box{background:var(--color-background-secondary);border-left:2px solid #E24B4A;padding:.65rem .9rem;margin-top:.5rem;font-size:12px;line-height:1.6}
.ft{font-size:10px;font-weight:600;padding:1px 5px;border-radius:3px;display:inline-block;margin-right:4px}
.fa{background:#EAF3DE;color:#3B6D11}.fb{background:#E6F1FB;color:#185FA5}.fc{background:#EEEDFE;color:#534AB7}
.fdg{font-size:12px;color:var(--color-text-secondary);line-height:1.5;margin-top:3px}
table{width:100%;border-collapse:collapse;font-size:12px}
th{background:var(--color-background-secondary);padding:6px 10px;text-align:left;font-weight:500;font-size:11px;color:var(--color-text-secondary);border-bottom:0.5px solid var(--color-border-tertiary)}
td{padding:6px 10px;border-bottom:0.5px solid var(--color-border-tertiary);vertical-align:top}
</style>

<div id="root"></div>

<script>
const MAX = 155;

// ── STEP 1: PILLAR DATA ───────────────────────────────────────────────────
// All pass states, findings, and fixes live here.
// This is the SINGLE SOURCE OF TRUTH for all score computations.
// Binary scoring: pass is true or false. Never fractional.
const INIT_PILLARS = [
  { id:1, name:'Title + Subtitle / Short description', max:25, criteria:[
    { id:'1.1', label:'No duplicate root keywords across fields', pts:5,
      ios:{ pass:{IOS_1_1}, finding:'{IOS_1_1_FINDING}', fixes:[] },
      and:{ pass:{AND_1_1}, finding:'{AND_1_1_FINDING}', fixes:[
        { t:'A', x:'{AND_1_1_FIX_A}' },
        { t:'B', x:'{AND_1_1_FIX_B}' },
        { t:'C', x:'{AND_1_1_FIX_C}' },
      ]}
    },
    { id:'1.2', label:'Character utilization ≥ 80% of limit', pts:5,
      ios:{ pass:{IOS_1_2}, finding:'{IOS_1_2_FINDING}', fixes:[] },
      and:{ pass:{AND_1_2}, finding:'{AND_1_2_FINDING}', fixes:[] }
    },
    { id:'1.3', label:'Most important keyword placed first', pts:5,
      ios:{ pass:{IOS_1_3}, finding:'{IOS_1_3_FINDING}', fixes:[] },
      and:{ pass:{AND_1_3}, finding:'{AND_1_3_FINDING}', fixes:[] }
    },
    { id:'1.4', label:'Keywords combine to form additional search terms', pts:5,
      ios:{ pass:{IOS_1_4}, finding:'{IOS_1_4_FINDING}', fixes:[] },
      and:{ pass:{AND_1_4}, finding:'{AND_1_4_FINDING}', fixes:[] }
    },
    { id:'1.5', label:'Short description in full sentences, no stuffing (Android only)', pts:5,
      ios:{ pass:true, finding:'N/A for iOS — auto-pass.', fixes:[] },
      and:{ pass:{AND_1_5}, finding:'{AND_1_5_FINDING}', fixes:[] }
    },
  ]},
  { id:2, name:'App icon', max:20, criteria:[
    { id:'2.1', label:'Simple, scalable design legible at small sizes', pts:5,
      ios:{ pass:{IOS_2_1}, finding:'{IOS_2_1_FINDING}', fixes:[] },
      and:{ pass:{AND_2_1}, finding:'{AND_2_1_FINDING}', fixes:[] }
    },
    { id:'2.2', label:'Strong brand association / recognizability', pts:5,
      ios:{ pass:{IOS_2_2}, finding:'{IOS_2_2_FINDING}', fixes:[] },
      and:{ pass:{AND_2_2}, finding:'{AND_2_2_FINDING}', fixes:[] }
    },
    { id:'2.3', label:'Unique and differentiated from competitors', pts:5,
      ios:{ pass:{IOS_2_3}, finding:'{IOS_2_3_FINDING}', fixes:[] },
      and:{ pass:{AND_2_3}, finding:'{AND_2_3_FINDING}', fixes:[] }
    },
    { id:'2.4', label:'Eye-catching, draws attention in search results', pts:5,
      ios:{ pass:{IOS_2_4}, finding:'{IOS_2_4_FINDING}', fixes:[] },
      and:{ pass:{AND_2_4}, finding:'{AND_2_4_FINDING}', fixes:[] }
    },
  ]},
  { id:3, name:'Keywords & metadata', max:25, criteria:[
    { id:'3.1', label:'Focus keywords naturally embedded (5–7 themes)', pts:5,
      ios:{ pass:{IOS_3_1}, finding:'{IOS_3_1_FINDING}', fixes:[] },
      and:{ pass:{AND_3_1}, finding:'{AND_3_1_FINDING}', fixes:[] }
    },
    { id:'3.2', label:'Keyword field ≥95% utilized (iOS) / density ~1% (Android)', pts:5,
      ios:{ pass:{IOS_3_2}, finding:'{IOS_3_2_FINDING}', fixes:[] },
      and:{ pass:{AND_3_2}, finding:'{AND_3_2_FINDING}', fixes:[] }
    },
    { id:'3.3', label:'High-volume terms targeted', pts:5,
      ios:{ pass:{IOS_3_3}, finding:'{IOS_3_3_FINDING}', fixes:[] },
      and:{ pass:{AND_3_3}, finding:'{AND_3_3_FINDING}', fixes:[] }
    },
    { id:'3.4', label:'Top organic ranking for primary keyword', pts:5,
      ios:{ pass:{IOS_3_4}, finding:'{IOS_3_4_FINDING}', fixes:[] },
      and:{ pass:{AND_3_4}, finding:'{AND_3_4_FINDING}', fixes:[] }
    },
    { id:'3.5', label:'Ranks above key competitors for ≥1 shared keyword', pts:5,
      ios:{ pass:{IOS_3_5}, finding:'{IOS_3_5_FINDING}', fixes:[] },
      and:{ pass:{AND_3_5}, finding:'{AND_3_5_FINDING}', fixes:[] }
    },
  ]},
  { id:4, name:'Description', max:25, criteria:[
    { id:'4.1', label:'Formatted with clear structure', pts:5,
      ios:{ pass:{IOS_4_1}, finding:'{IOS_4_1_FINDING}', fixes:[] },
      and:{ pass:{AND_4_1}, finding:'{AND_4_1_FINDING}', fixes:[] }
    },
    { id:'4.2', label:'Covers all identified target keywords', pts:5,
      ios:{ pass:{IOS_4_2}, finding:'{IOS_4_2_FINDING}', fixes:[] },
      and:{ pass:{AND_4_2}, finding:'{AND_4_2_FINDING}', fixes:[] }
    },
    { id:'4.3', label:'Builds on title — does not repeat it verbatim', pts:5,
      ios:{ pass:{IOS_4_3}, finding:'{IOS_4_3_FINDING}', fixes:[] },
      and:{ pass:{AND_4_3}, finding:'{AND_4_3_FINDING}', fixes:[] }
    },
    { id:'4.4', label:'Clear CTA present', pts:5,
      ios:{ pass:{IOS_4_4}, finding:'{IOS_4_4_FINDING}', fixes:[] },
      and:{ pass:{AND_4_4}, finding:'{AND_4_4_FINDING}', fixes:[] }
    },
    { id:'4.5', label:'Branded voice consistent with update notes', pts:5,
      ios:{ pass:{IOS_4_5}, finding:'{IOS_4_5_FINDING}', fixes:[] },
      and:{ pass:{AND_4_5}, finding:'{AND_4_5_FINDING}', fixes:[] }
    },
  ]},
  { id:5, name:'Screenshots', max:25, criteria:[
    { id:'5.1', label:'7+ screenshots (iOS: up to 10, Android: up to 8)', pts:5,
      ios:{ pass:{IOS_5_1}, finding:'{IOS_5_1_FINDING}', fixes:[] },
      and:{ pass:{AND_5_1}, finding:'{AND_5_1_FINDING}', fixes:[] }
    },
    { id:'5.2', label:'Sufficient contrast and visual hierarchy', pts:5,
      ios:{ pass:{IOS_5_2}, finding:'{IOS_5_2_FINDING}', fixes:[] },
      and:{ pass:{AND_5_2}, finding:'{AND_5_2_FINDING}', fixes:[] }
    },
    { id:'5.3', label:'≥ 80% of screenshots have readable captions', pts:5,
      ios:{ pass:{IOS_5_3}, finding:'{IOS_5_3_FINDING}', fixes:[] },
      and:{ pass:{AND_5_3}, finding:'{AND_5_3_FINDING}', fixes:[] }
    },
    { id:'5.4', label:'First 2–3 screenshots communicate core value', pts:5,
      ios:{ pass:{IOS_5_4}, finding:'{IOS_5_4_FINDING}', fixes:[] },
      and:{ pass:{AND_5_4}, finding:'{AND_5_4_FINDING}', fixes:[] }
    },
    { id:'5.5', label:'CTA or download prompt in final screenshot', pts:5,
      ios:{ pass:{IOS_5_5}, finding:'{IOS_5_5_FINDING}', fixes:[] },
      and:{ pass:{AND_5_5}, finding:'{AND_5_5_FINDING}', fixes:[] }
    },
  ]},
  { id:6, name:'App preview video', max:20, criteria:[
    { id:'6.1', label:'Preview video present', pts:5,
      ios:{ pass:{IOS_6_1}, finding:'{IOS_6_1_FINDING}', fixes:[] },
      and:{ pass:{AND_6_1}, finding:'{AND_6_1_FINDING}', fixes:[] }
    },
    { id:'6.2', label:'Explains value within first 5 seconds (muted)', pts:5,
      ios:{ pass:{IOS_6_2}, finding:'{IOS_6_2_FINDING}', fixes:[] },
      and:{ pass:{AND_6_2}, finding:'{AND_6_2_FINDING}', fixes:[] }
    },
    { id:'6.3', label:'Reinforces title keywords visually', pts:5,
      ios:{ pass:{IOS_6_3}, finding:'{IOS_6_3_FINDING}', fixes:[] },
      and:{ pass:{AND_6_3}, finding:'{AND_6_3_FINDING}', fixes:[] }
    },
    { id:'6.4', label:'Includes a clear CTA or closing hook', pts:5,
      ios:{ pass:{IOS_6_4}, finding:'{IOS_6_4_FINDING}', fixes:[] },
      and:{ pass:{AND_6_4}, finding:'{AND_6_4_FINDING}', fixes:[] }
    },
  ]},
  { id:7, name:'Ratings & reviews', max:15, criteria:[
    { id:'7.1', label:'Overall rating ≥ 4.0 (4.5+ = full 5 pts)', pts:5,
      ios:{ pass:{IOS_7_1}, finding:'{IOS_7_1_FINDING}', fixes:[] },
      and:{ pass:{AND_7_1}, finding:'{AND_7_1_FINDING}', fixes:[] }
    },
    { id:'7.2', label:'≥ 50% of reviews are 5-star', pts:5,
      ios:{ pass:{IOS_7_2}, finding:'{IOS_7_2_FINDING}', fixes:[] },
      and:{ pass:{AND_7_2}, finding:'{AND_7_2_FINDING}', fixes:[] }
    },
    { id:'7.3', label:'Developer responds personally to reviews', pts:5,
      ios:{ pass:{IOS_7_3}, finding:'{IOS_7_3_FINDING}', fixes:[] },
      and:{ pass:{AND_7_3}, finding:'{AND_7_3_FINDING}', fixes:[] }
    },
  ]},
];

// ── STEP 2: FROZEN AUDIT SCORES ──────────────────────────────────────────
// Single source of truth: computed from INIT_PILLARS, stored in plain consts.
// NEVER use a separate object with manually set pillar totals.
// NEVER use Object.values() on an object that has a getter — getters are invoked
// and their return value is included in the array, causing double-counting.
function computeScore(pillars, plat) {
  return pillars.reduce((s, p) =>
    s + p.criteria.reduce((cs, c) => cs + (c[plat].pass ? c.pts : 0), 0), 0);
}
const IOS_AUDIT_SCORE = computeScore(INIT_PILLARS, 'ios');
const AND_AUDIT_SCORE = computeScore(INIT_PILLARS, 'and');
const IOS_AUDIT_GRADE = Math.round((IOS_AUDIT_SCORE / MAX) * 100);
const AND_AUDIT_GRADE = Math.round((AND_AUDIT_SCORE / MAX) * 100);
// Sanity check: IOS_AUDIT_GRADE + AND_AUDIT_GRADE should both be plausible
// percentages (0–100). If either exceeds 100, there is a data error in INIT_PILLARS.

// ── STEP 3: OPPORTUNITY ROWS ──────────────────────────────────────────────
// One row per failed sub-criterion (score = 0). Sorted P0 → P1 → P2.
const OPPS = [
  // { p:'P0', plt:'Both', opp:'...', why:'...', action:'...', effort:'High', design:'Yes', time:'...' },
  // CLAUDE: Fill with real audit findings. Every failed criterion generates ≥1 row.
];

// ── STEP 4: KEYWORD VARIANTS ──────────────────────────────────────────────
const KWVARS = [
  // { f:'iOS Title — current', c:'App Name', n:8, l:30, h:'Baseline' },
  // { f:'iOS Title — variant A', c:'App Name: Keyword', n:18, l:30, h:'Tests keyword expansion' },
  // CLAUDE: 2–3 candidates per field, with real char counts.
];

// ── STEP 5: ROADMAP ───────────────────────────────────────────────────────
const ROADMAP = [
  { d:'Day 1',    a:'P0 fixes — tailored to this app\'s specific gaps.' },
  { d:'Day 5',    a:'Scorecard + tracking setup.' },
  { d:'Day 10',   a:'Begin implementation of Update 1.' },
  { d:'Day 17',   a:'Update 1 launch. Begin Update 2.' },
  { d:'Day 25',   a:'Update 2 ready.' },
  { d:'Day 30–32',a:'Update 2 launch. Close Update 1 data window.' },
  { d:'Day 35',   a:'30-day check-in vs baseline and competitors.' },
  { d:'Day 45–47',a:'Update 3 launch.' },
  { d:'Day 60',   a:'Update 4 launch. 60-day progress report.' },
  { d:'Day 67',   a:'60-day check-in.' },
  { d:'Day 75',   a:'Update 5 launch. 90-day report.' },
  { d:'Day 90',   a:'Final scorecard. Continue or restructure decision.' },
];

// ── RENDER LOOP ───────────────────────────────────────────────────────────
(function() {
  const root = document.getElementById('root');
  let pillars = JSON.parse(JSON.stringify(INIT_PILLARS));
  let openMap = {};
  let plat = 'ios';

  function liveScore() {
    return computeScore(pillars, plat);
  }

  function gc(g) { return g>=75?'#639922':g>=50?'#BA7517':'#A32D2D'; }
  function gl(g) { return g>=75?'Well optimized':g>=50?'Needs work':'Critical gaps'; }
  function pp(p) { return {P0:'pr',P1:'pa',P2:'pb'}[p]||''; }

  function render() {
    const livS = liveScore();
    const livG = Math.round((livS / MAX) * 100);
    const audG = plat === 'ios' ? IOS_AUDIT_GRADE : AND_AUDIT_GRADE;
    const audS = plat === 'ios' ? IOS_AUDIT_SCORE : AND_AUDIT_SCORE;
    const delta = Math.abs(IOS_AUDIT_GRADE - AND_AUDIT_GRADE);

    root.innerHTML = `<div style="padding:1rem 0">

    <!-- HERO: 3-card layout — iOS frozen | Android frozen | Live simulation -->
    <div class="card">
      <div class="lbl">ASO audit</div>
      <div style="font-size:18px;font-weight:500;margin-bottom:2px">{APP_NAME}</div>
      <div style="font-size:12px;color:var(--color-text-secondary);margin-bottom:1.25rem">
        {APP_CATEGORY} · {APP_ID} · Audited: {AUDIT_DATE}
      </div>

      <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-bottom:1rem">
        ${[
          { lbl:'iOS audit score',    g:IOS_AUDIT_GRADE, raw:IOS_AUDIT_SCORE, sub:'Frozen — checkboxes don\'t affect this' },
          { lbl:'Android audit score',g:AND_AUDIT_GRADE, raw:AND_AUDIT_SCORE, sub:'Frozen — checkboxes don\'t affect this' },
        ].map(s => `
          <div style="background:var(--color-background-secondary);border-radius:var(--border-radius-md);padding:.9rem">
            <div class="lbl">${s.lbl}</div>
            <div style="font-size:30px;font-weight:500;color:${gc(s.g)};line-height:1.1">${s.g}%</div>
            <div style="height:5px;background:var(--color-border-tertiary);border-radius:99px;margin:6px 0 4px;overflow:hidden">
              <div style="width:${Math.min(s.g,100)}%;height:100%;background:${gc(s.g)};border-radius:99px;transition:width .2s"></div>
            </div>
            <div style="font-size:11px;color:var(--color-text-secondary)">${s.raw}/${MAX} pts · ${gl(s.g)}</div>
            <div style="font-size:10px;color:var(--color-text-secondary);margin-top:2px">${s.sub}</div>
          </div>`).join('')}

        <!-- LIVE CARD: toggle buttons live HERE, not below the hero -->
        <div style="background:var(--color-background-secondary);border-radius:var(--border-radius-md);padding:.9rem;border:1.5px dashed var(--color-border-secondary)">
          <!-- Platform toggle buttons sit at the top of the Live card -->
          <div style="display:flex;gap:6px;margin-bottom:8px;align-items:center">
            ${['ios','and'].map(p => `<button onclick="setP('${p}')"
              style="padding:3px 10px;border-radius:99px;border:0.5px solid var(--color-border-${plat===p?'primary':'tertiary'});
              background:${plat===p?'var(--color-text-primary)':'transparent'};
              color:${plat===p?'var(--color-background-primary)':'var(--color-text-secondary)'};
              font-size:11px;cursor:pointer">
              ${p==='ios'?'🍎 iOS':'🤖 Android'}
            </button>`).join('')}
          </div>
          <div class="lbl">Live: ${plat==='ios'?'iOS':'Android'}</div>
          <div style="font-size:30px;font-weight:500;color:${gc(livG)};line-height:1.1">${livG}%</div>
          <div style="height:5px;background:var(--color-border-tertiary);border-radius:99px;margin:6px 0 4px;overflow:hidden">
            <div style="width:${Math.min(livG,100)}%;height:100%;background:${gc(livG)};border-radius:99px;transition:width .2s"></div>
          </div>
          <div style="font-size:11px;color:var(--color-text-secondary)">${livS}/${MAX} pts · ${gl(livG)}</div>
          <div style="font-size:10px;color:var(--color-text-secondary);margin-top:2px">Toggle checkboxes below to simulate fixes</div>
        </div>
      </div>

      ${delta > 15 ? `<div style="background:#FAEEDA;border-radius:var(--border-radius-md);padding:.6rem 1rem;font-size:12px;color:#854F0B;margin-bottom:.75rem">
        ⚠ Platform divergence: ${delta}pp. iOS and Android listings are significantly misaligned. See pillar breakdown below.</div>` : ''}
    </div>

    <!-- 7-PILLAR CHECKLIST -->
    <div style="font-size:15px;font-weight:500;margin:1.5rem 0 .75rem">
      7-pillar checklist
      <span style="font-size:12px;font-weight:400;color:var(--color-text-secondary)">
        — ${plat==='ios'?'iOS':'Android'} · toggle to simulate fixes
      </span>
    </div>
    ${pillars.map(p => {
      const ps = p.criteria.reduce((s,c) => s+(c[plat].pass?c.pts:0), 0);
      const pct = Math.round((ps/p.max)*100);
      const isOpen = !!openMap[p.id];
      return `<div class="card" style="padding:0;margin-bottom:8px">
        <div onclick="togP(${p.id})" style="padding:.85rem 1.25rem;cursor:pointer;display:flex;align-items:center;justify-content:space-between">
          <div style="display:flex;align-items:center;gap:10px">
            <span style="font-size:11px;color:var(--color-text-secondary);font-weight:500">P${p.id}</span>
            <span style="font-size:13px;font-weight:500">${p.name}</span>
          </div>
          <div style="display:flex;align-items:center;gap:10px">
            <div style="width:70px;height:5px;background:var(--color-border-tertiary);border-radius:99px;overflow:hidden">
              <div style="width:${pct}%;height:100%;background:${gc(pct)};border-radius:99px;transition:width .2s"></div>
            </div>
            <span style="font-size:12px;color:var(--color-text-secondary);min-width:36px;text-align:right">${ps}/${p.max}</span>
            <span style="font-size:10px;color:var(--color-text-secondary)">${isOpen?'▲':'▼'}</span>
          </div>
        </div>
        ${isOpen ? `<div style="border-top:0.5px solid var(--color-border-tertiary)">
          ${p.criteria.map(c => {
            const d = c[plat];
            return `<div style="padding:.6rem 1.25rem;border-bottom:0.5px solid var(--color-border-tertiary);background:${d.pass?'var(--color-background-primary)':'#fffbfb'}">
              <label style="display:flex;gap:10px;cursor:pointer;align-items:flex-start">
                <input type="checkbox" ${d.pass?'checked':''} onchange="togC(${p.id},'${c.id}')"
                  style="margin-top:2px;flex-shrink:0;accent-color:var(--color-text-primary)">
                <div style="flex:1">
                  <div style="font-size:13px;font-weight:500;color:${d.pass?'var(--color-text-primary)':'#A32D2D'}">
                    [${c.id}] ${c.label}
                    <span style="font-size:11px;font-weight:400;color:var(--color-text-secondary)">(${c.pts} pts)</span>
                  </div>
                  <div class="fdg">${d.finding}</div>
                  ${!d.pass && d.fixes && d.fixes.length ? `<div class="fix-box">
                    ${d.fixes.map(f => `<div style="margin-bottom:5px"><span class="ft f${f.t.toLowerCase()}">${f.t}</span>${f.x}</div>`).join('')}
                  </div>` : ''}
                </div>
              </label>
            </div>`;
          }).join('')}
        </div>` : ''}
      </div>`;
    }).join('')}

    <!-- OPPORTUNITIES TABLE -->
    <div style="font-size:15px;font-weight:500;margin:1.5rem 0 .75rem">Opportunities</div>
    <div class="card" style="padding:0;overflow-x:auto">
      <table>
        <thead><tr>
          <th>#</th><th>Priority</th><th>Platform</th><th>Opportunity</th>
          <th>Why it matters</th><th>Action</th><th>Effort</th><th>Design?</th><th>Timeline</th>
        </tr></thead>
        <tbody>${OPPS.map((r,i) => `<tr style="background:${i%2===0?'var(--color-background-primary)':'var(--color-background-secondary)'}">
          <td style="color:var(--color-text-secondary)">${i+1}</td>
          <td><span class="pill ${pp(r.p)}">${r.p}</span></td>
          <td style="white-space:nowrap">${r.plt}</td>
          <td style="font-weight:500;max-width:140px">${r.opp}</td>
          <td style="max-width:170px;color:var(--color-text-secondary)">${r.why}</td>
          <td style="max-width:210px">${r.action}</td>
          <td style="white-space:nowrap">${r.effort}</td>
          <td>${r.design}</td>
          <td style="color:var(--color-text-secondary);white-space:nowrap">${r.time}</td>
        </tr>`).join('')}</tbody>
      </table>
    </div>

    <!-- KEYWORD TESTING LAB -->
    <div style="font-size:15px;font-weight:500;margin:1.5rem 0 .75rem">Keyword testing lab</div>
    <div class="card" style="padding:0;overflow-x:auto">
      <table>
        <thead><tr><th>Field</th><th>Candidate</th><th>Chars</th><th>Limit</th><th>Util</th><th>Hypothesis</th></tr></thead>
        <tbody>${KWVARS.map((r,i) => {
          const pct = Math.round((r.n/r.l)*100);
          const over = r.n > r.l;
          const ok = pct >= 80 && !over;
          return `<tr style="background:${i%2===0?'var(--color-background-primary)':'var(--color-background-secondary)'}">
            <td style="font-size:11px;color:${r.f.includes('current')?'var(--color-text-secondary)':'var(--color-text-primary)'};white-space:nowrap">${r.f}</td>
            <td style="font-family:var(--font-mono);font-size:11px">${r.c}</td>
            <td style="text-align:center;font-family:var(--font-mono);color:${over?'#A32D2D':'inherit'}">${r.n}${over?' ⚠':''}</td>
            <td style="text-align:center;font-family:var(--font-mono);color:var(--color-text-secondary)">${r.l}</td>
            <td style="text-align:center"><span class="pill" style="background:${ok?'#EAF3DE':'#FCEBEB'};color:${ok?'#3B6D11':'#A32D2D'}">${pct}%</span></td>
            <td style="font-size:11px;color:var(--color-text-secondary);max-width:210px">${r.h}</td>
          </tr>`;
        }).join('')}</tbody>
      </table>
    </div>

    <!-- 90-DAY ROADMAP -->
    <div style="font-size:15px;font-weight:500;margin:1.5rem 0 .75rem">What happens next — 90-day roadmap</div>
    <div class="card">${ROADMAP.map(r => `
      <div style="display:flex;gap:1rem;align-items:flex-start;margin-bottom:8px">
        <div style="min-width:58px;font-size:11px;font-family:var(--font-mono);color:var(--color-text-secondary);padding-top:2px;flex-shrink:0">${r.d}</div>
        <div style="flex:1;font-size:13px;border-left:2px solid var(--color-border-tertiary);padding-left:1rem;padding-bottom:8px">${r.a}</div>
      </div>`).join('')}
    </div>

    <!-- COMPETITOR GAP (conditional) -->
    <!-- CLAUDE: Render this section only if competitor URLs were provided.
         Otherwise omit it entirely or render a one-line placeholder. -->

    <!-- FOOTER CTA — must appear verbatim per Section 13 -->
    <div style="background:var(--color-background-secondary);border-radius:var(--border-radius-lg);padding:1.5rem;text-align:center">
      <div style="font-size:14px;font-weight:500;margin-bottom:6px">Ready to go deeper?</div>
      <div style="font-size:13px;color:var(--color-text-secondary)">
        Would you like to run a competitor comparison or export these recommendations as a Notion-ready task list?
      </div>
    </div>

    </div>`;
  }

  window.togP = id => { openMap[id] = !openMap[id]; render(); };
  window.setP = p  => { plat = p; render(); };
  window.togC = (pid, cid) => {
    const p = pillars.find(x => x.id === pid);
    const c = p.criteria.find(x => x.id === cid);
    c[plat].pass = !c[plat].pass;
    render();
  };

  render();
})();
</script>
```

**Pre-delivery checklist:**
- [ ] All `{PLACEHOLDER}` values replaced with real audit data
- [ ] `INIT_PILLARS` pass states are correct per scoring rubric — binary true/false only
- [ ] `IOS_AUDIT_SCORE` and `AND_AUDIT_SCORE` are plausible (0–155). If either > 155, there is a data error
- [ ] Frozen audit scores match initial pillar bars — open every pillar and verify before delivering
- [ ] `OPPS` has one row per failed sub-criterion (score = 0), sorted P0 → P1 → P2
- [ ] `KWVARS` has 2–3 candidates per field with real char counts (not estimates)
- [ ] `ROADMAP` Day 1 is tailored to this app's specific P0 actions
- [ ] Footer CTA closing line is present verbatim (see Section 13)
- [ ] **Single-platform audit:** if only one URL was provided, follow the single-platform
  hero layout (see "Single-platform hero layout" section above):
  - Unavailable platform card shows "N/A" in grey with a "URL not provided" sub-label
  - Live card shows a static platform badge ("iOS only" / "Android only") instead of toggle buttons
  - No toggle buttons are rendered anywhere in the report
  - Missing platform criteria auto-pass with `finding: 'N/A — [platform] not provided.'`
  - Only the available platform's score appears in the Live card and checklist

---

## 7. FAILURE PATTERN LIBRARY

The 15 most common ASO failure patterns. Claude references this library when writing
WHY + FIX blocks for every failed sub-criterion in the audit output.

**MANDATORY RULE — listing reference required:**
Every recommendation Claude writes MUST quote or cite actual text, numbers, or
observations from the audited listing. Generic advice ("add a CTA") is never
acceptable when real listing data is available. Correct form: "Your current
description ends with '📥 Start your spiritual journey today!' — extend this by
adding '[App Name] is free. Download in seconds.' to make the download prompt
explicit." If a field was not fetched and the user declined to provide it, state
that explicitly and give a conditional recommendation.

Each pattern below provides **3 strategy variants** per fix:
- **Strategy A — Copy only (Low effort):** no design tools required; implementable
  in < 2 hours in App Store Connect or Play Console.
- **Strategy B — Design + copy (Medium effort):** requires a designer or Figma/Canva;
  1–2 days to produce the asset, then 3–4 weeks A/B test window.
- **Strategy C — Structural / code (High effort):** requires a developer or app
  update; 1–2 sprint cycles.

---

**Pattern 1: Promotional text field left empty (iOS only)**
- **Why it hurts:** The 170-char promotional text field is the only App Store field
  updatable without a new app version. While not indexed by the algorithm, it sits
  above the fold and is the first text users read after the subtitle. An empty field
  wastes the primary conversion surface that can be changed between app reviews.
  Reference the actual subtitle text when writing the fix so the promo text extends
  rather than repeats it.
- **Strategy A — Copy only:** Write a time-sensitive or rotating value statement
  that picks up where the subtitle ends. Template: "[New feature or seasonal hook] —
  [specific benefit from your listing]. Try free." Max 170 chars. Example using a real
  listing: if subtitle = "Set tasks, earn & spend money", promo text = "New: Savings
  Goals — help your child save toward something they want. Free to download."
- **Strategy B — Design + copy:** Coordinate the promo text with a seasonal or
  campaign-specific screenshot set. Run a Product Page Optimization test where
  variant A uses a feature-focused promo text and variant B uses a social-proof
  statement (e.g., "Trusted by [N] families — rated [X] stars"). Measure CVR delta
  over 7+ days.
- **Strategy C — Structural:** Build a scheduled promo text rotation into your
  release process: assign a different promo text to each app update. Treat it as a
  headline ad — write 4–5 evergreen variants (feature highlight, social proof, CTA,
  seasonal, award) and rotate quarterly.

---

**Pattern 2: Brand name leading the Android short description**
- **Why it hurts:** The short description is the only copy shown above the fold on
  Google Play. Starting with the brand name (which the user already read in the title
  directly above) wastes the first 10–20 chars on information with zero new conversion
  value. The algorithm also weights the opening words of the short description more
  heavily for indexing. Quote the current short description's opening word(s) when
  writing the fix.
- **Strategy A — Copy only:** Rewrite the short description to open with a user
  outcome or primary use case, not the brand name. Template: "[Verb] + [primary
  keyword] + [differentiator or social proof]." Example: current = "Mydoh helps kids
  earn money" → fixed = "Kids earn, save, and spend real money — with parental
  controls." Same keywords, no brand name, 56 chars.
- **Strategy B — Design + copy:** Run a Store Listing Experiment with variant A =
  benefit-led short desc and variant B = social-proof-led short desc (e.g., "Trusted
  by [N] families — kids earn, parents stay in control."). Measure install CVR over
  14+ days against the control.
- **Strategy C — Structural:** If the brand name is legally required to lead the
  short description (trademarked positioning), use the brand name as an adjective
  rather than a noun: "[Brand]: kids earn real money with parental controls." The
  colon keeps the brand but opens a space for the keyword immediately after.

---

**Pattern 3: Feature graphic is logo-only on white or black background (Android)**
- **Why it hurts:** The feature graphic occupies approximately 60% of above-fold
  space on the Google Play store listing. A logo on a blank background conveys no
  value proposition, no product context, and no emotional hook. Describe what the
  current feature graphic shows (if known from the fetch or image upload) when
  writing the recommendation.
- **Strategy A — Copy only:** If replacing the image is not immediately possible,
  overlay the primary value statement as large text on the existing graphic using
  Play Console's built-in text overlay tool (if available in your country). Text
  should be the single most compelling line from your listing — e.g., the opening
  line of the short description.
- **Strategy B — Design + copy:** Commission or build in Figma/Canva a feature
  graphic that uses one of these three proven formats: (1) lifestyle photo — real
  people using the app in context, with the app UI on a phone visible; (2) product
  mockup — a phone showing the app's hero screen with a short headline overlaid in
  large, high-contrast text; (3) bold color block — brand color background, primary
  value statement as headline text (≥ 60pt), app name in smaller type. Test all
  three as Store Listing Experiments over 14+ days.
- **Strategy C — Structural:** Tie the feature graphic to your seasonal content
  calendar. For apps with seasonal peaks (tax apps in April, holiday apps in
  December), build 4 feature graphic variants per year. Each should be a lifestyle
  image relevant to the season with a hook tied to your primary keyword.

---

**Pattern 4: Screenshot captions too small to read on most phone screens**
- **Why it hurts:** Screenshots are shown at thumbnail size in search results. Caption
  text below ~18pt equivalent at the screenshot's native resolution is illegible at
  the sizes most users encounter. Illegible captions turn the keyword surface of
  every screenshot into dead space. When images have been provided, reference the
  specific screenshot number and the approximate caption size observed.
- **Strategy A — Copy only:** Shorten all captions to 5 words or fewer. Shorter
  copy forces larger type even within the same design. Replace multi-line sentences
  with punchy fragments: "Earn real money" not "Kids can earn real money by completing
  their chores." Test legibility by viewing your screenshots at 25% zoom in any image
  editor — if you can't read the caption at that zoom, your users can't either.
- **Strategy B — Design + copy:** Redesign all screenshots with a consistent caption
  template: (1) a solid colour bar (brand colour or high-contrast dark) at the bottom
  25% of the frame; (2) white caption text at minimum 72px at 1080px screenshot width;
  (3) the app UI visible in the top 75%. Run a Product Page Optimization or Store
  Listing Experiment comparing the new captioned set against the current set. Measure
  CVR and tap-through rate.
- **Strategy C — Structural:** Build a screenshot design system in Figma with a
  locked caption component — a shared template where the caption bar, font size, and
  colour contrast are locked at spec. Every new screenshot automatically inherits
  legible captions. This prevents regression every time a new screenshot is added.

---

**Pattern 5: Description not featuring primary ASO keywords**
- **Why it hurts:** On iOS, the long description feeds secondary indexing. On Android,
  it is the primary keyword indexing field. Keywords absent from the description
  cannot rank for those terms regardless of their presence in other metadata fields.
  Quote the specific missing keywords from the audited listing when writing the fix.
- **Strategy A — Copy only:** Identify which target keywords are absent from the
  description (compare against the keyword field on iOS, or against the short
  description's keyword theme on Android). Add a "Key Features" or "What you get"
  section at the end of the description, using one bullet per missing keyword. Each
  bullet should be a full sentence that naturally uses the keyword. Example: if
  "offline mode" is missing, add "📶 Offline access — read and use [App Name] with
  no internet connection, anywhere."
- **Strategy B — Design + copy:** Restructure the entire description using the
  Problem → Promise → Proof → CTA funnel, with each keyword theme assigned to a
  specific section. The Problem section introduces the search context (who is the
  user, what they struggle with), which naturally surfaces the primary keyword. The
  Proof section adds social proof stats or press mentions that introduce brand
  keywords. This restructure serves both indexing and conversion.
- **Strategy C — Structural:** Build a keyword coverage tracking spreadsheet: column
  A = target keyword, column B = appears in title (Y/N), column C = appears in
  subtitle or short desc (Y/N), column D = appears in description (Y/N), column E =
  appears in keyword field / long desc (Y/N). Review and update before every app
  release. Missing cells in column D are immediate copy tasks.

---

**Pattern 6: Keyword density > 2% for any single term in Google Play long description**
- **Why it hurts:** Google Play's metadata policy prohibits keyword stuffing. Density
  above ~2% for any single term is a spam signal that can trigger demotion or a policy
  warning. Target density is ~1% (approximately once per 100 words). When auditing,
  count the exact instances of the offending term from the fetched description text and
  cite the count: "The word '[term]' appears N times in approximately X words, giving a
  density of ~Y%."
- **Strategy A — Copy only:** Paste the long description into a word-frequency counter
  (wordcounter.net or similar). Identify any term appearing more than 4× in 400 words.
  Replace excess instances with natural synonyms drawn from the listing itself — e.g.,
  if the app is called "Sai Satcharitra", replace extra instances with "the sacred text",
  "this holy book", "Baba's teachings", or "the Satcharitra."
- **Strategy B — Design + copy:** Restructure the description into named sections (each
  section covers a different keyword theme) so that the primary keyword naturally
  concentrates in the first section only, while secondary and tertiary keywords fill the
  remaining sections. This reduces primary density while expanding indexing surface.
- **Strategy C — Structural:** Add a pre-submission density check to your release
  process. Build a simple spreadsheet formula: `=COUNTIF(range, "*keyword*")/word_count`
  applied to the pasted description text. Flag any result above 0.02 (2%) before
  submitting to Play Console.

---

**Pattern 7: Duplicate keywords across iOS title, subtitle, and keyword field**
- **Why it hurts:** Apple's algorithm does not give incremental ranking credit for a
  keyword that appears in multiple indexed fields. Each duplicated root word in the
  keyword field wastes a slot that could index a new, distinct search term. When
  auditing, list every root word in title and subtitle and compare against the keyword
  field token by token. Cite the specific duplicates found.
- **Strategy A — Copy only:** Extract every word in the title and subtitle and build a
  blocklist. Open the keyword field in App Store Connect and remove every token on the
  blocklist. Fill the freed characters with long-tail variations that do not appear in
  any other field. Example: if title has "allowance", the keyword field should have
  "spending,saving,earn,chores,rewards" — not "allowance" again.
- **Strategy B — Design + copy:** Treat the three fields as three non-overlapping
  indexing layers with distinct conversion functions: Title = brand + primary keyword
  (ranking anchor); Subtitle = clarification + secondary keyword (conversion hook);
  Keyword field = long-tail variations only (indexing depth). Redesign all three fields
  simultaneously as a single coordinated unit, not independently.
- **Strategy C — Structural:** Build and maintain a three-column keyword allocation
  matrix: Column A = keyword, Column B = assigned field (title / subtitle / keyword
  field / description), Column C = last updated. A keyword may appear in only one
  indexed field. Review this matrix before every keyword update submission.

---

**Pattern 8: Preview video not tested against screenshots-only variant**
- **Why it hurts:** Preview videos autoplay muted and push screenshots further right in
  the carousel. In some categories (utilities, productivity, Books & Reference) a
  screenshots-only listing converts better because screenshots are more scannable
  [uncertain — category-dependent]. Without an A/B test, the assumption "video = better"
  may be costing installs. When auditing, note the category and whether the current video
  has visible text overlays or relies on audio for comprehension.
- **Strategy A — Copy only:** Before running any test, audit the existing video without
  audio. Watch the first 5 seconds on mute. If no value prop is communicated in those
  5 seconds, rewrite the video script or add text overlays as an immediate interim fix.
  This costs no design work if the video was produced in a tool like CapCut or Canva.
- **Strategy B — Design + copy:** Run a native A/B test: Product Page Optimization (iOS,
  7-day minimum) or Store Listing Experiment (Android, 14-day minimum). Variant A =
  current video + current screenshots. Variant B = screenshots only, but with the best
  performing screenshot moved to slot 1. Measure CVR and tap-through rate. Let the data
  decide — do not declare a winner before the minimum window closes.
- **Strategy C — Structural:** Produce a second video variant specifically for the test —
  a tighter, 15-second cut that front-loads the value prop in the first 3 seconds with
  large on-screen text, no audio dependency. Test three-way: original video vs. short
  cut vs. screenshots only. This is the only way to distinguish "video format" from
  "video quality" as the variable.

---

**Pattern 9: App title using < 20 characters of the allowed 30**
- **Why it hurts:** The app title is the highest-weighted indexing field on both
  platforms. An underutilized title (< 67% of 30-char limit) leaves keyword indexing
  capacity on the table. When auditing, state the exact current title, its character
  count, and the specific keywords that could fit in the unused space. Example: "Current
  title 'Mydoh' is 5 chars — 25 chars unused. Primary keyword 'allowance' (9 chars) +
  ' & Chores' (9 chars) would bring total to 23 chars, still 7 under limit."
- **Strategy A — Copy only:** Append a keyword descriptor using one of these templates:
  `[Brand] – [Primary Keyword]` / `[Brand]: [Clarifier]` / `[Brand] [Keyword] [Modifier]`.
  Verify LEN() before submitting. Target 25–30 chars. Example: "Mydoh" → "Mydoh –
  Allowance & Chores" (22 chars) → "Mydoh Allowance & Chores" (24 chars).
- **Strategy B — Design + copy:** If the brand name is short, treat the title as a
  combined brand + product name. "Mydoh" became "Mydoh – Allowance & Chores" — the
  descriptor after the dash becomes part of the brand identity. Update app icon to
  reflect the expanded name so title and icon are visually coherent in search results.
- **Strategy C — Structural:** Run a title A/B test before committing. On iOS, use
  Product Page Optimization (test 7+ days). On Android, use Store Listing Experiments
  (test 14+ days). Test the short brand-name title against 2 expanded variants. Track
  both keyword ranking movement (check after 5–7 days of the variant being live) and
  CVR. Do not shorten a winning title to re-add a lost keyword — title changes affect
  ranking immediately and may cause a temporary ranking dip.

---

**Pattern 10: No developer responses to reviews**
- **Why it hurts:** Developer responses are public and visible to every future visitor
  who reads the reviews section. Unanswered reviews signal disengagement, which reduces
  trust for undecided users. On Google Play specifically, personalized responses have
  been observed to prompt reviewers to update their star rating upward [uncertain —
  platform does not publish data on this]. When auditing, state the exact number of
  unanswered reviews visible and quote any specific review text that represents an
  unresolved issue.
- **Strategy A — Copy only:** Set a weekly 30-minute recurring calendar block for
  review management. Respond to every review in that session — even single-word
  reviews like "Great!" deserve a personal acknowledgment. Template for positive
  reviews: "Thank you [name] — [specific callback to what they mentioned or the app's
  core purpose]. [One sentence about what's coming next]." Template for negative
  reviews: "I'm sorry to hear [specific issue they raised]. [Action you've taken or
  will take]. Please reach out to [support email] so we can resolve this directly."
- **Strategy B — Design + copy:** Build a review response playbook: 5–8 pre-written
  response templates for the most common review categories (praise, bug report,
  feature request, low rating with no text, language complaint). Personalize each
  template with the reviewer's name and one specific reference to their review text.
  Never send a template without personalizing at least two elements.
- **Strategy C — Structural:** Implement an in-app feedback capture before the review
  prompt. When a user would trigger the review request (e.g., after completing a
  task), show an internal "How are we doing? 👍 / 👎" prompt first. Users who tap 👎
  are routed to an in-app feedback form (not to the store). Users who tap 👍 are
  routed to the store review prompt. This filters negative sentiment away from public
  reviews while preserving the positive flow.

---

**Pattern 11: First screenshot shows a generic splash screen or login screen**
- **Why it hurts:** The first screenshot is the highest-conversion visual asset on the
  listing after the icon. Users decide whether to engage with the rest of the page
  within 2–3 seconds of landing. A splash screen or login screen tells the user only
  what the app looks like at its most generic moment — not what it does or why it is
  worth downloading. When images are available, describe exactly what screenshot 1
  currently shows and what specific change is needed.
- **Strategy A — Copy only:** If a redesign is not immediately possible, add a caption
  overlay to the existing screenshot 1 that states the app's primary benefit. Even a
  splash screen with a strong caption ("The complete [Category] app — [primary benefit]")
  converts better than one with no caption. This can be done in Canva or Figma in
  under an hour.
- **Strategy B — Design + copy:** Replace screenshot 1 with the app's hero moment —
  the screen a user reaches after their first meaningful action. For a reading app: a
  chapter open to a compelling passage. For a finance app: the dashboard showing money
  earned. For a productivity app: a completed task list. Add a caption that names the
  benefit, not the feature: "Chapter 1 complete — your daily spiritual practice starts
  here" not "Chapter reading screen." Run a Product Page Optimization or Store Listing
  Experiment comparing the new screenshot 1 against the current splash screen.
- **Strategy C — Structural:** Establish a screenshot hierarchy protocol for your team:
  Slot 1 = hero moment (outcome the user gets); Slot 2 = primary USP (what makes this
  app different from competitors); Slot 3 = social proof or credibility signal; Slots
  4–6 = key use cases; Slots 7–8 = innovative features or recent updates. Lock this
  sequence in a screenshot brief template that is reused for every listing update.

---

**Pattern 12: No CTA in final screenshot**
- **Why it hurts:** Users who scroll to the final screenshot are the highest-intent
  visitors on the product page — they have spent more attention than any other visitor.
  A listing that ends without a download prompt misses the conversion opportunity at
  the exact moment of maximum intent. When auditing, note what the current final
  screenshot shows and confirm whether it has any action-oriented text.
- **Strategy A — Copy only:** If the final screenshot already shows a UI screen, add
  a caption overlay with a download prompt. Template: "Free to download — [one key
  benefit]." or "[Rating] ⭐ from [N] [users/devotees/families] — join them today."
  This is the lowest-effort high-impact change in screenshot optimisation.
- **Strategy B — Design + copy:** Create a dedicated "closing frame" screenshot — not
  a UI screenshot at all, but a full-bleed branded card that functions as a closing ad.
  Use a high-contrast background, the app rating, a one-line value statement, and a
  "Download free" prompt. This frame has no UI to show, so it focuses 100% on
  conversion. Test it against the current final screenshot in a Store Listing Experiment.
- **Strategy C — Structural:** Add the closing CTA frame to your screenshot template
  system as a locked final slide. Every time screenshots are updated, this frame is
  automatically included as the last slot. Update only the rating number and review
  count when they change — the frame design stays constant.

---

**Pattern 13: Short description repeats exact app title wording (Android)**
- **Why it hurts:** The short description and title are both displayed above the fold on
  Google Play. Repeating title language doubles down on information the user already has,
  wastes indexing surface, and wastes the only line of copy most users will read before
  making a download decision. When auditing, quote the exact title words that appear in
  the short description and identify what new keywords or value propositions are being
  lost as a result.
- **Strategy A — Copy only:** Establish a hard rule: no word from the title may appear
  in the first 40 characters of the short description. Rewrite using this frame: Title =
  [what the app is]. Short desc = [why to download it right now]. Example: title =
  "Sai Satcharitra in English" → short desc = "Read all 51 chapters offline, free —
  one a day." Zero title words repeated; introduces "chapters", "offline", "daily"
  as new keyword seeds.
- **Strategy B — Design + copy:** Run three short description variants in Store Listing
  Experiments: (A) benefit-led ("Read Sai Baba's complete teachings — offline, free."),
  (B) social-proof-led ("Trusted by Sai devotees worldwide — all 51 chapters, in English."),
  (C) use-case-led ("Daily Sai Satcharitra reading, one chapter at a time. Free & offline.")
  Each introduces different secondary keywords. Run each against control for 14+ days.
- **Strategy C — Structural:** Treat short description as a standalone conversion
  headline — brief it separately from the long description and title. Assign it to your
  strongest conversion copywriter (not your SEO writer). Evaluate it by reading it
  immediately after reading the title, as a real user would. If it feels redundant,
  it is.

---

**Pattern 14: iOS keyword field uses phrases instead of single words**
- **Why it hurts:** Apple's algorithm for the keyword field tokenizes single words, not
  phrases. Entering "chore chart" (11 chars, 1 comma slot, yields 2 indexable terms)
  is less efficient than "chore,chart" (11 chars, 1 comma, also yields 2 indexable terms
  but as independent tokens that can combine with other field words). More critically,
  multi-word phrases padded with spaces (e.g., "chore chart") use 11 chars but Apple
  counts the space, reducing the 100-char field to effectively 91 usable chars.
  When auditing, paste the known keyword field and count spaces that could be reclaimed.
- **Strategy A — Copy only:** Open the keyword field in App Store Connect. Split every
  multi-word phrase at the space — "chore chart" becomes "chore,chart". Remove all
  spaces after commas. Remove every word that already appears in the title or subtitle.
  Count the reclaimed characters and fill them with new single-word long-tail terms.
  Target: 95–100 chars used, zero duplicates with other fields, zero multi-word phrases.
- **Strategy B — Design + copy:** Build a keyword research brief before touching the
  field. Use a tool (AppFollow, App Radar, or Apple Search Ads suggested bids) to
  score the volume of every candidate token. Prioritise tokens with popularity ≥ 40/100
  that do not already appear in title or subtitle. Fill the field from highest to lowest
  priority until 95+ chars are used.
- **Strategy C — Structural:** Build a keyword field master spreadsheet: Column A =
  token, Column B = char count (LEN), Column C = in title? (Y/N), Column D = in
  subtitle? (Y/N), Column E = popularity score, Column F = included in field? (Y/N).
  Sum Column B (for Y rows in Column F) to verify total char count before submitting.
  This prevents accidental duplicates and space waste on every keyword update.

---

**Pattern 15: Rating below 4.0 with no review management strategy**
- **Why it hurts:** Ratings below 4.0 cause measurable conversion drag on both
  platforms. Below 3.5, both Apple and Google may de-prioritise the app in category
  browse and editorial placements. A low rating without visible developer responses
  compounds the problem — it signals to new users that issues reported by reviewers
  are unresolved. When auditing, state the exact current rating, the total review count,
  and quote any recurring complaint theme from visible review text.
- **Strategy A — Copy only:** Start responding to every review immediately — even
  1-star reviews with no text. Personalized responses that acknowledge the issue and
  offer a resolution path have been observed to prompt rating updates [uncertain —
  platform does not publish data on this]. For reviews that cite a specific bug, reply
  with the exact fix date if known: "This was fixed in version X.X on [date] — if
  you update and still see the issue, please email us at [address]." Simultaneously,
  identify the highest-satisfaction moment in the current UX and add a native review
  prompt (SKStoreReviewRequest / ReviewManager) at that exact moment.
- **Strategy B — Design + copy:** Build a "rating recovery" campaign: (1) respond to
  all unanswered negative reviews in the past 90 days with a personalised update on
  what has changed since their review; (2) release an update that addresses the top
  3 recurring complaints from reviews; (3) add the specific fixes to the update notes
  using language that mirrors the review complaints (e.g., if users said "crashes on
  login", update notes say "Fixed: login crash reported by users on Android 13+").
  This creates a feedback loop that turns negative reviewers into update notice readers.
- **Strategy C — Structural:** Implement a full review management system: (1) in-app
  sentiment gate — internal 👍/👎 prompt before routing to store review; (2) negative
  feedback routed to a support ticket system (not the store); (3) weekly review
  monitoring with a dedicated responder; (4) quarterly review audit — read all 1–3 star
  reviews, tag by theme, feed themes into product roadmap. Rating recovery is a product
  problem as much as a marketing problem. The fastest path to 4.5+ is fixing the bugs
  users are complaining about, not gaming the review prompt.

---

## 8. OPPORTUNITIES TABLE MODULE

**Format for every row Claude must populate from audit findings:**

| Field | Rule |
|---|---|
| **#** | Sequential integer |
| **Priority** | P0 = score-critical gap (≥ 5 pts in any pillar); P1 = conversion-impacting (visible above the fold); P2 = polish (lower ranking impact) |
| **Platform** | iOS / Android / Both |
| **Opportunity** | Short label: what needs to change |
| **Why It Matters** | One sentence: cite the ranking mechanism or conversion impact |
| **Specific Action** | Exact copy or design instruction — not a generic suggestion |
| **Effort** | Low (copywriting only, < 2 hrs) / Medium (design + copy, 1–2 days) / High (design + A/B test, 2+ weeks) |
| **Design Required** | Yes / No |
| **Est. Timeline** | Copywriting only: 1–2 weeks. Design changes: 1–2 weeks asset creation + 3–4 weeks A/B testing |

**Population rules:**
1. Every failed sub-criterion (scored 0) generates at least one opportunity row.
2. Partial failures (scored < max but > 0) generate a row only if the gap is ≥ 3 pts.
3. Sort by Priority: P0 first, then P1, then P2.
4. Do not combine multiple pillar failures into one row — one failure = one row.

---

## 9. 90-DAY ASO PROCESS ROADMAP

Surface this at the end of every audit as "What Happens Next." This timeline is fixed —
do not modify or abbreviate.

| Milestone | Day | Action |
|---|---|---|
| ASO Kickoff | Day 1 | Walk through audit findings; align on top 4–5 priority changes |
| Scorecard + Checklist | Day 5 | Finalize which changes to implement first; set up tracking |
| Audit Walkthrough | Day 10 | Begin implementation of Update 1 |
| Update 1 Launch | Day 17 | Ship first batch of changes; begin Update 2 |
| Update 2 Ready | Day 25 | Have second batch prepared for launch |
| Update 2 Launch | Day 30–32 | Close Update 1 data window; update scorecard with 30-day delta |
| 30-Day Check-In | Day 35 | Compare score to baseline and competitor benchmarks |
| Update 3 Launch | Day 45–47 | — |
| Update 4 Launch | Day 60 | Update 60-day progress report; rescore against competitors |
| 60-Day Check-In | Day 67 | — |
| Update 5 Launch | Day 75 | Complete 90-day progress report |
| 90-Day Check-In | Day 90 | Final scorecard update; decide whether to continue or restructure |

---

## 10. KEYWORD TESTING LAB

Rules and templates Claude uses to generate candidate variant tables.

### Title testing targets
- **iOS:** 25–30 characters. Include brand name + 1–2 descriptor keywords.
- **Android:** 25–30 characters. Same rule applies; no "free", "best", "top", "#1", etc.
- **Formula:** `[Brand Name] [Primary Keyword] [Clarifier]`
- **Example structures:** "Mydoh Allowance & Chores" (25 chars) | "Mydoh – Kids Money App" (22 chars)
- Always compute and display `LEN()` of every candidate.

### Subtitle testing targets (iOS only)
- **Target:** 27–30 characters.
- **Formula:** `[Verb] + [keyword 1] + & + [keyword 2]`
- **Example structures:**
  - "Set tasks, earn & spend money" (29 chars)
  - "For allowance, chores and more" (30 chars)
  - "Track chores, earn real rewards" (31 chars — 1 over; trim)
- No brand name repetition. Must introduce new keywords not in title.

### Short description testing targets (Android)
- **Target:** 65–80 characters.
- **Rules:** Full grammatical sentence. Brand name must NOT be the first word. Lead
  with a user benefit or primary use case. Keyword density: 1 primary keyword, naturally
  embedded. No keyword listing.
- **Example structures:**
  - "Help kids earn, save, and spend — the smart allowance app." (58 chars)
  - "Chore tracker and allowance manager trusted by 500K families." (61 chars)
  - "Teach real money skills: your kids earn, you stay in control." (61 chars)

### Testing rules
- **One hypothesis per test.** Never test title and subtitle simultaneously.
- **Minimum test windows:** 7 days on App Store Connect Product Page Optimization;
  14 days on Google Play Store Listing Experiments.
- **Log baseline score before each test. Log post-test score after data window closes.**
- Track: impressions, conversion rate (CVR), and install volume for each variant.

### Candidate variant table format

Claude renders this table with every audit. Populate with 2–3 candidates per field.

| Field | Candidate Copy | LEN() | Limit | Utilization | Hypothesis |
|---|---|---|---|---|---|
| iOS Title — Current | [current title] | N | 30 | X% | Baseline |
| iOS Title — Variant A | [candidate] | N | 30 | X% | [What this tests] |
| iOS Title — Variant B | [candidate] | N | 30 | X% | [What this tests] |
| iOS Subtitle — Current | [current subtitle] | N | 30 | X% | Baseline |
| iOS Subtitle — Variant A | [candidate] | N | 30 | X% | [What this tests] |
| iOS Subtitle — Variant B | [candidate] | N | 30 | X% | [What this tests] |
| Android Title — Current | [current title] | N | 30 | X% | Baseline |
| Android Title — Variant A | [candidate] | N | 30 | X% | [What this tests] |
| Android Short Desc — Current | [current short desc] | N | 80 | X% | Baseline |
| Android Short Desc — Variant A | [candidate] | N | 80 | X% | [What this tests] |
| Android Short Desc — Variant B | [candidate] | N | 80 | X% | [What this tests] |

---

## 11. COMPETITOR COMPARISON MODULE

**Trigger:** Only render if ≥ 1 competitor URL was provided as input.

**Instructions for Claude:**
1. Run `web_fetch` on each competitor URL and extract the same Metadata Extraction Table
   fields used in Section 3.3.
2. Score each competitor using the 7-pillar rubric (same 155-pt scale).
3. Render a gap table: one column per app (audited app + up to 3 competitors).

### Competitor gap table format

| Pillar | [App Name] | [Competitor 1] | [Competitor 2] | [Competitor 3] | Gap vs. Best |
|---|---|---|---|---|---|
| 1. Title + Subtitle | X/25 | X/25 | X/25 | X/25 | [audited app score - highest competitor score] |
| 2. App Icon | X/20 | X/20 | X/20 | X/20 | — |
| 3. Keywords | X/25 | X/25 | X/25 | X/25 | — |
| 4. Description | X/25 | X/25 | X/25 | X/25 | — |
| 5. Screenshots | X/25 | X/25 | X/25 | X/25 | — |
| 6. Preview Video | X/20 | X/20 | X/20 | X/20 | — |
| 7. Ratings & Reviews | X/15 | X/15 | X/15 | X/15 | — |
| **Total** | **/155** | **/155** | **/155** | **/155** | — |
| **Grade** | **X%** | **X%** | **X%** | **X%** | — |

**After the table:** Identify the top 3 pillars where the audited app is furthest below
the best-in-class competitor. Surface these as P0 opportunities in the Opportunities table.

---

## 12. NOTION EXPORT MODULE

**Trigger:** When user requests Notion export, or in response to the closing CTA.

**Format:** Notion-compatible checklist markdown. One row per failed sub-criterion.

```markdown
## ASO Audit — Action Items: [App Name]
**Audit date:** [DATE] | **iOS Grade:** X% | **Android Grade:** X%

---

### P0 — Score-Critical (address within 2 weeks)

- [ ] **[1.2] Character utilization < 80% — iOS Title** | Effort: Low | Design: No | Owner: ___
  - Action: Expand title to 25–30 chars. Add "[Primary Keyword]" after brand name.
  - Timeline: 1 week copy + submit

- [ ] **[5.1] Fewer than 7 screenshots — Android** | Effort: Medium | Design: Yes | Owner: ___
  - Action: Create screenshots 7–8 showing [specific features].
  - Timeline: 1–2 wks asset + 3–4 wks A/B test

### P1 — Conversion-Impacting (address within 4 weeks)

- [ ] **[4.4] No CTA in description — Both** | Effort: Low | Design: No | Owner: ___
  - Action: Add "Download free — set up in 3 minutes" to final paragraph of description.
  - Timeline: 1 week copy + submit

### P2 — Polish (address within 8 weeks)

- [ ] **[4.5] Inconsistent branded voice — iOS** | Effort: Low | Design: No | Owner: ___
  - Action: Align description tone with update notes; rewrite update notes beyond "Bug fixes".
  - Timeline: 1 week
```

**Rules:**
- One checkbox row per failed sub-criterion.
- Always include: Priority label, Pillar ID, platform, Effort, Design Required, Owner field.
- Sort P0 → P1 → P2.
- Do not include passed criteria in the Notion export.

---

## 13. CLOSING PROTOCOL

**Every audit MUST end with this exact sentence, rendered as a styled call-to-action:**

> **Would you like to run a competitor comparison or export these recommendations as a Notion-ready task list?**

This line appears:
1. In the MDX footer CTA block (see Section 6).
2. As the final line of Claude's conversational response after delivering the audit.

Do not paraphrase. Do not omit. This closing triggers the next phase of the engagement.
