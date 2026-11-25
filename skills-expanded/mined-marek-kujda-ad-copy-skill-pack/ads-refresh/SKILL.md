---
name: ads-refresh
description: Refresh stale Google Ads RSA copy to combat ad fatigue. Use when the user wants to update, rotate, or refresh headlines and descriptions for an existing campaign that has been running for several weeks.
allowed-tools: Read, Write, Bash
---

# /ads-refresh — Refresh RSA Copy to Combat Ad Fatigue

## Input Required

Ask the user for:

1. **Current RSA copy** — CSV file, pasted text, or previous `/ads` output in `output/`
2. **Performance data** — per-asset CTR and impressions (see export guide below)
3. **How long has it been running?** — weeks/months since last refresh
4. **What changed?** (optional) — new features, offers, pricing, seasonal angle
5. **Refresh intensity** — ask the user:
   - **Light** (swap 3–5 weakest headlines, keep top performers)
   - **Medium** (replace ~50% of headlines, refresh 1–2 descriptions)
   - **Full** (keep only the 2–3 proven winners, regenerate everything else)

### How to Export Performance Data from Google Ads

Walk the user through this if they haven't done it before:

1. Open Google Ads → go to the campaign/ad group you want to refresh
2. Click **Ads & assets** in the left menu
3. Click **Assets** tab (not "Ads" tab)
4. Click **"View asset details"** under the RSA you want to refresh
5. You'll see a table with each headline and description showing:
   - **Asset text** (the headline or description)
   - **Type** (Headline or Description)
   - **Performance** label (Best, Good, Low, or Learning)
   - **Impressions**
6. Select all rows → **Download** as CSV or copy-paste into the conversation

Alternatively, for bulk export:
1. Go to **Reports** → Create custom report
2. Dimensions: **Asset text**, **Asset type**, **Campaign**, **Ad group**
3. Metrics: **Impressions**, **Clicks**, **CTR**
4. Filter by the campaign you want to refresh
5. Download as CSV and place in the project root

**Minimum viable data:** If the user can't export the full report, even Google's
performance labels (Best / Good / Low / Learning) per headline are enough to make
informed keep/replace decisions.

### If No Performance Data Is Available

If the user cannot provide any performance data:
1. Clearly state that refresh decisions will be based on copy quality only, not actual performance
2. Run the `/ads-review` audit framework to assess each headline/description
3. Suggest the user exports performance data next time for better results
4. Default to **Medium refresh** intensity (safest without data — replaces enough to test new angles while keeping enough to avoid disruption)

## Execution Steps

### Step 1: Parse Performance Data
Load and structure the data into a table:

```
| #   | Asset Text               | Type        | Impressions | CTR   | Label    |
|-----|--------------------------|-------------|-------------|-------|----------|
| H1  | "Get Marketing Insights" | Headline    | 12,400      | 3.8%  | Best     |
| H2  | "Try It Free Today"      | Headline    | 8,200       | 2.1%  | Good     |
| H3  | "Analytics Platform"     | Headline    | 1,100       | 0.9%  | Low      |
| ... |                          |             |             |       |          |
| D1  | "Turn data into..."      | Description | 15,000      | 3.2%  | Best     |
```

### Step 2: Classify Each Asset

| Bucket      | Criteria                                          | Action                          |
|-------------|---------------------------------------------------|---------------------------------|
| **Winners** | Label: Best, or CTR >3%, high impressions         | Keep — these are proven         |
| **Solid**   | Label: Good, or CTR 2–3%, decent impressions      | Keep on light, consider on full |
| **Weak**    | Label: Low, or CTR <1.5%, shown often             | Replace — actively hurting CTR  |
| **Untested**| Label: Learning, or <500 impressions              | Replace — not contributing      |
| **Stale**   | Any asset unchanged for 8+ weeks, declining trend | Replace — even if formerly good |

Load context:
- Brand voice from `.claude/skills/brand-voice/SKILL.md`
- ICP from `.claude/skills/icp/SKILL.md`
- Platform rules from `.claude/skills/google-ads-rules/SKILL.md`

### Step 3: Generate Replacements

Based on refresh intensity:

**Light refresh:**
- Replace 3–5 Weak + Untested headlines
- Keep all Winners and Solid
- Keep all descriptions unless one is clearly Weak
- Maintain the same angle distribution

**Medium refresh:**
- Replace all Weak + Untested headlines (~7–8 typically)
- Refresh 1–2 descriptions (keep Best-performing)
- Introduce 1–2 new angles not present in the original set
- Consider refreshing Stale assets even if formerly Good

**Full refresh:**
- Keep only Winners (2–3 headlines, 1 description)
- Regenerate everything else with fresh angles
- Deliberately test new messaging directions
- Rotate out Stale assets regardless of past performance

### Step 4: Ensure Freshness
For all replacement headlines, check:
- No replacement is too similar to a headline being kept
- New copy introduces at least 2 angles not in the original set
- Seasonal or timely references are updated (e.g., "2025" → "2026")
- Any expired offers or outdated claims are removed
- New headlines address gaps found in the performance data (e.g., no social proof headlines were tested)

### Step 5: Validate
- All headlines ≤30 chars, descriptions ≤90 chars
- Keyword coverage maintained (≥2 headlines with target keyword)
- CTA present in at least 1 description
- Run: `python .claude/skills/ads/validate.py output/<file>.csv`

### Step 6: Export
Save refreshed version alongside the original for comparison:
```
output/rsa_[campaign]_[adgroup]_refreshed_[date].csv
```

### Step 7: Present Change Summary

```
## Refresh Summary: [Campaign] / [Ad Group]
Intensity: [Light / Medium / Full]
Based on: [Performance data / Copy quality only]

### Performance Snapshot
- Total headlines analyzed: X
- Winners: X | Solid: X | Weak: X | Untested: X | Stale: X
- Best headline: "..." (X.X% CTR, XX,XXX impressions)
- Worst headline: "..." (X.X% CTR, XX,XXX impressions)

### Kept (X headlines, X descriptions)
- H1: "Headline text" — Winner, 3.8% CTR, 12K impr
- H5: "Headline text" — Solid, 2.4% CTR, 6K impr
- D1: "Description text" — Best, 3.2% CTR

### Replaced (X headlines, X descriptions)
| Slot | Was                     | Performance       | Now                      | Why                    |
|------|------------------------|-------------------|--------------------------|------------------------|
| H3   | "Old headline"         | Low, 0.9% CTR    | "New headline" [28 ch]   | Weak — replace         |
| H7   | "Old headline"         | 340 impr only     | "New headline" [26 ch]   | Untested — not shown   |
| H11  | "Old headline"         | Good but 10 weeks | "New headline" [29 ch]   | Stale — rotate out     |
| D3   | "Old description"      | Low, 1.1% CTR    | "New description" [87 ch]| Weak + no CTA          |

### New Angles Introduced
- [Angle]: H9, H12 — testing urgency (gap in current set)
- [Angle]: H14 — question-based (diversifies the mix)

### Recommended Next Steps
- Upload refreshed CSV to Google Ads Editor
- Let new assets accumulate ≥1,000 impressions before next evaluation
- Next refresh suggested: [date based on cadence]
```

## Suggested Refresh Cadence
- **High-spend campaigns (>€1k/day)**: refresh every 3–4 weeks
- **Medium-spend (€200–1k/day)**: refresh every 6–8 weeks
- **Low-spend (<€200/day)**: refresh every 10–12 weeks or when CTR drops >15%

## Advanced: Automated Data Pull (Optional)
For users who want to skip manual export, Claude Code can connect to Google Ads API
via MCP server (e.g., Adspirer) to pull asset performance data automatically.
Setup: add the MCP server config to `.claude/settings.json`. See README for details.
