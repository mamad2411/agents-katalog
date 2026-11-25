---
name: aso
description: >
  Route or run comprehensive App Store Optimization work for iOS and Android.
  Use for full listing audits, multi-area ASO requests, or when the user does
  not name a more specific ASO task. Covers keyword research, metadata,
  visuals, reviews, competitors, localization, testing, technical health,
  compliance, conversion, launch planning, and seasonal optimization.
---

# ASO — App Store Optimization Skill

## Consolidated Skill Routing

Use five public skills:

- `aso`: full audit, orchestration, and strategy. For roadmap detail, read
  `../skills/aso-plan/GUIDE.md`.
- `aso-listing`: keywords, metadata, localization, and seasonal changes.
- `aso-creative`: screenshots, video, conversion, and experiments.
- `aso-market`: reviews and competitors.
- `aso-release`: technical readiness, compliance, and launch.

The former specialist files are internal `GUIDE.md` references. They preserve
the detailed methods but do not appear as separate skills.

Comprehensive ASO analysis for iOS App Store and Google Play apps. Works in two modes:

1. **Local mode** (default): Run `/aso audit` inside an app project — auto-detects Fastlane metadata, Xcode project, or Gradle project and audits your pre-submission metadata.
2. **Remote mode**: Run `/aso audit <app-id>` with an app ID or store URL — fetches and audits the live listing. Also works for competitor apps.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/aso audit` | Auto-detect local project and audit its metadata |
| `/aso audit <app-id>` | Audit a live listing by app ID or store URL |
| `/aso audit --compare <app-id>` | Audit local metadata AND compare against live listing |
| `/aso keywords <seeds>` | Keyword research — difficulty, volume, placement strategy |
| `/aso metadata` | Optimize local metadata (or `/aso metadata <app-id>` for remote) |
| `/aso visuals` | Analyze local screenshots (or `/aso visuals <app-id>` for remote) |
| `/aso reviews <app-id>` | Reviews — sentiment analysis, response templates, keyword extraction |
| `/aso competitors <app-id>` | Competitor analysis — keyword gaps, metadata comparison |
| `/aso localization` | Audit local locale coverage (or `/aso localization <app-id>`) |
| `/aso ab-testing <app-id>` | A/B testing — iOS PPO / Android experiment design |
| `/aso technical <app-id>` | Technical ASO — Android Vitals, app size, crashes, update cadence |
| `/aso conversion <app-id>` | Conversion — install rate benchmarking, first-impression audit |
| `/aso compliance` | Store policy check — validates metadata against Apple/Google guidelines |
| `/aso plan <category>` | Strategic plan — 4-phase roadmap with category templates |
| `/aso launch` | Launch — pre-launch checklist using local project state |
| `/aso seasonal <app-id>` | Seasonal — trending keyword opportunities, holiday calendar |

## Auto-Detection (Local Mode)

When no app ID is provided, run project detection first:
```bash
uv run python scripts/detect_project.py --json
```

This scans the current directory for:

| Source | What it detects | Files checked |
|--------|----------------|---------------|
| **Fastlane iOS** | Store metadata per locale (name, subtitle, keywords, description) | `fastlane/metadata/{locale}/name.txt`, `subtitle.txt`, `keywords.txt`, etc. |
| **Fastlane Android** | Store metadata per locale (title, short/full description) | `fastlane/metadata/android/{locale}/title.txt`, `full_description.txt`, etc. |
| **Xcode project** | Bundle ID, app name | `*.xcodeproj/project.pbxproj`, `Info.plist` |
| **Gradle project** | Application ID, app name | `app/build.gradle`, `AndroidManifest.xml`, `res/values/strings.xml` |

Priority: Fastlane metadata (richest data) > Xcode/Gradle (basic identifiers only).

If Fastlane metadata is found, all fields are available for validation, keyword analysis, and optimization. If only Xcode/Gradle is found, extract the app ID and optionally fetch the live listing for a full audit.

## Remote Mode

When an app ID or URL is provided, fetch the live listing:

- **iOS**: Numeric ID (`id284882215`), Apple App Store URL (`apps.apple.com/...`)
- **Android**: Package name (`com.whatsapp`), Google Play URL (`play.google.com/store/apps/details?id=...`)

```
iOS:     id284882215  OR  https://apps.apple.com/app/id284882215
Android: com.whatsapp  OR  https://play.google.com/store/apps/details?id=com.whatsapp
```

## Compare Mode

`/aso audit --compare <app-id>` audits BOTH local metadata and the live listing, then shows:
- Fields that differ between local and live
- Whether local changes would improve or regress the score
- Pre-submission validation of pending metadata changes

## Category Detection

After fetching listing data, classify the app:
- **Gaming**: game category, IAP patterns, leaderboards
- **SaaS/Productivity**: subscription model, enterprise features, workspace tools
- **Health/Fitness**: HealthKit/Google Fit, workout terms, wellness
- **E-commerce**: shopping category, payment, cart, product catalog
- **Social**: messaging, feed, connections, sharing
- **Fintech**: banking, payments, investment, crypto
- **Other**: education, travel, utilities, news, entertainment

Category informs which plan templates and benchmarks to apply.

## Audit Orchestration Flow

When running `/aso audit <app-id>`:

### Step 1 — Data Fetch (sequential)
```bash
uv run python scripts/fetch_listing.py <app-id> --country us --json
```
Parse the result to get structured listing data.

### Step 2 — Category Detection (sequential)
Classify app from listing metadata. Load category-specific benchmarks.

### Step 3 — Parallel Subagent Dispatch
Run all applicable specialists in parallel when the harness supports
delegation. Otherwise, load the corresponding specialist skills and run them
sequentially. Do not continue to scoring until all applicable results return.

| Agent | Focus |
|-------|-------|
| `aso-keywords` | Keyword coverage in current metadata |
| `aso-metadata` | Field quality, char limits, keyword placement |
| `aso-visuals` | Screenshot count, narrative, icon, video |
| `aso-reviews` | Sentiment distribution, themes, response rate |
| `aso-competitors` | Top 5 competitor comparison |
| `aso-technical` | App size, update recency, stability signals |
| `aso-conversion` | First-impression elements, CRO signals |
| `aso-localization` | *(conditional: if multi-locale detected)* |

Each agent receives the parsed listing JSON and returns a structured report with scores and findings.

### Step 3.5 — Compliance Validation (sequential)

After all specialists return, run `aso-compliance` with:

1. The original listing metadata.
2. All proposed metadata, keyword, visual, and conversion changes.

Remove any recommendation that violates an Apple or Google policy. Replace it
with a compliant alternative when possible. A policy violation is always a
Critical action item, independent of its numeric score.

### Step 4 — Score Aggregation (sequential)

Calculate weighted **ASO Health Score (0-100)**:

| Category | Weight |
|----------|--------|
| Keyword Optimization | 20% |
| Metadata Quality | 15% |
| Visual Assets | 15% |
| Reviews & Ratings | 15% |
| Competitive Position | 10% |
| Technical Health | 10% |
| Conversion Signals | 10% |
| Policy Compliance | 5% |

### Step 5 — Report Generation (sequential)

Generate two files:

**ASO-AUDIT-REPORT.md**:
- Executive summary (score, platform, category, top 3 issues, quick wins)
- Per-category detailed findings, including policy compliance
- Platform-specific notes

**ASO-ACTION-PLAN.md**:
- **Critical**: Character limit violations, missing keywords in title, <3.5 star rating
- **High**: Poor screenshot narrative, no preview video, low review velocity
- **Medium**: Localization gaps, A/B test opportunities, secondary keyword misses
- **Low**: Seasonal optimization, minor copy improvements, icon A/B test

End with a short user summary of no more than 40 lines. Include the score,
platform, category, category breakdown, exactly three top issues, three to five
quick wins, and paths to both report files. Use only these status words:
Excellent, Good, Needs Work, Poor, Critical.

## Quality Gates

These rules are ALWAYS enforced — never recommend violations:

1. **Character limits are absolute** — violations are always Critical priority
2. **iOS description is NOT indexed** — never optimize it for keywords, only conversion
3. **iOS keyword field**: comma-separated, no spaces after commas, no duplication with title/subtitle
4. **Android description**: primary keyword in first sentence, 2-3% density for primary keyword
5. **No keyword stuffing**: >3 repetitions of same keyword in any field = stuffing
6. **Review health**: <3.5 stars = Critical, <4.0 = High priority
7. **Update recency**: >90 days since last update = warning signal

## Platform Metadata Quick Reference

### iOS App Store

| Field | Limit | Indexed? | Notes |
|-------|-------|----------|-------|
| App Name | 30 chars | YES (high weight) | Primary keyword here |
| Subtitle | 30 chars | YES | Secondary keywords |
| Keywords | 100 chars | YES | Hidden, comma-separated |
| Description | 4,000 chars | NO | Conversion copy only |
| Promotional Text | 170 chars | NO | No review needed to update |
| What's New | 4,000 chars | NO | Update messaging |

### Google Play

| Field | Limit | Indexed? | Notes |
|-------|-------|----------|-------|
| Title | 30 chars | YES (high weight) | Treat every character as premium space |
| Short Description | 80 chars | YES | Visible in some views |
| Full Description | 4,000 chars | YES | Keyword density matters |
| Developer Name | variable | YES (low) | Branding |
| What's New | 500 chars | NO | Shorter than iOS |

## Capability Fallbacks

- If delegation is unavailable, run specialist instructions sequentially.
- If browser or network access is unavailable, use local metadata and mark live
  listing, review, and competitor evidence as unavailable.
- If an app cannot be found, report the accepted identifier formats.
- If data is partial, score only supported categories and label the result
  partial. Do not infer missing evidence.

## Reference Files

Load on demand from `references/`:
- `ios-metadata-specs.md` — Full iOS field specs and indexing rules
- `android-metadata-specs.md` — Full Android field specs and indexing rules
- `keyword-placement-rules.md` — Keyword weight by field position per platform
- `visual-asset-specs.md` — Screenshot/icon/video dimensions per device
- `quality-gates.md` — Thresholds, hard stops, density limits
- `category-taxonomy.md` — iOS/Android category IDs and mapping
