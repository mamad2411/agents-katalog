---
name: paid-ad-fatigue-detector-creative-rotation-strategist
description: "Analyze ad creative performance decay and predict fatigue before CTR tanks. Use when the user needs ad performance monitoring, creative rotation strategies, or audience fatigue analysis across Google Ads, Facebook, and LinkedIn campaigns."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["GOOGLE_ADS_API_KEY","FACEBOOK_ADS_API_KEY","LINKEDIN_ADS_API_KEY","OPENAI_API_KEY"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📊"}}
---

# Paid Ad Fatigue Detector & Creative Rotation Strategist

## Overview

This skill provides AI-driven detection and prevention of ad creative fatigue—the measurable performance degradation that occurs when audiences see the same ad creative too many times. By analyzing historical impression, CTR, CPC, and conversion data across your ad accounts, this skill identifies fatigue patterns specific to your audience segments and predicts exactly when creative performance will decline.

Unlike basic ad reporting tools that show *what happened*, this skill **predicts** fatigue before your CPCs spike and generates actionable creative briefs for replacement assets. It learns from your platform-specific patterns (Google Ads, Facebook Ads Manager, LinkedIn Campaign Manager) and provides rotation recommendations with confidence scoring.

**Ideal for:**
- Performance marketing teams managing 20+ active ad campaigns
- Agencies running multi-client ad operations
- E-commerce brands with seasonal or evergreen campaign rotations
- B2B SaaS companies optimizing lead generation costs
- Marketing teams struggling with declining ROAS due to creative fatigue

**Integrations:** Google Ads API, Facebook Ads Manager API, LinkedIn Campaign Manager, Slack (for alerts), Google Sheets (for data export), HubSpot (for audience insights)

---

## Quick Start

Try these prompts to begin analyzing your ad creative performance:

### Example 1: Detect Current Fatigue Status
```
Analyze my Google Ads account (MCC: 123-456-789) for creative fatigue 
indicators in the "Holiday Campaign 2024" across all ad groups. 
Show me: 1) CTR trend over last 30 days, 2) CPC changes by creative variant, 
3) impression velocity, 4) predicted fatigue risk (high/medium/low) for each creative.
```

### Example 2: Predict Fatigue Timeline
```
My Facebook ad account has 4 active creatives in the "Cold Audience" segment. 
The oldest creative (ID: 123456) has 2.3M impressions and 3.2% CTR. 
Based on my historical data, when will this creative likely hit fatigue (CTR drops >15%)?
Provide: fatigue timeline, confidence level, and rotation recommendation.
```

### Example 3: Generate Creative Rotation Brief
```
My LinkedIn lead gen campaign has 5 creatives in rotation. 
Creative_A (1.8M impressions, 2.9% CTR) is showing fatigue signals. 
Generate a creative brief for a replacement asset that addresses: 
1) Different value prop angle, 2) different visual style, 3) different audience hook. 
Include copy suggestions, visual direction, and audience targeting adjustments.
```

### Example 4: Segment-Specific Fatigue Analysis
```
Analyze fatigue patterns for my Shopify store across three audience segments:
- Warm (website visitors): Which creatives fatigue fastest?
- Cold (lookalike): Which creative themes perform longest?
- Cold (interest-based): Any segment-specific fatigue signals?
Provide rotation recommendations per segment with timing.
```

---

## Capabilities

### 1. **Creative Performance Baseline Analysis**
Establishes individual baseline metrics for each creative asset:
- Initial CTR, CPC, conversion rate, ROAS
- Impression velocity (impressions per day)
- Audience quality score (based on placement diversity)
- Creative lifespan benchmarks (industry-specific)

**Usage Example:**
```
Compare my 6 active Facebook creatives. Show baseline metrics, 
current performance vs. baseline, and how each ranks against 
industry benchmarks for e-commerce video ads.
```

### 2. **Fatigue Pattern Recognition**
Identifies fatigue using multi-variable trend analysis:
- CTR decay curves (linear, exponential, plateau detection)
- CPC inflation tracking (cost per engagement threshold alerts)
- Conversion rate stability (variance from baseline)
- Audience saturation signals (frequency capping impact)
- Impression velocity decline (momentum loss detection)

**Usage Example:**
```
Pull the last 90 days of data for my "Spring Collection" campaign (Google Ads).
Apply polynomial regression to detect when CTR inflection points occur 
for each creative. Flag creatives that have crossed the 80% baseline CTR threshold.
```

### 3. **Fatigue Prediction Engine**
Machine learning model trained on your account's historical data:
- Predicts fatigue onset date (±3 day confidence interval)
- Calculates "Days to Fatigue" countdown
- Scores fatigue risk on 0-100 scale
- Recommends optimal rotation timing before performance tanks
- Audience-segment specific predictions

**Usage Example:**
```
Based on my account's historical pattern, predict when each of my 
8 LinkedIn campaign creatives will hit fatigue (50% CTR decline threshold).
Include: predicted date, confidence %, recommended action date (48 hrs before).
```

### 4. **Creative Element Rotation Recommendations**
Analyzes which specific creative elements drive fatigue resistance:
- Copy angle rotation (benefit vs. urgency vs. scarcity vs. social proof)
- Visual style breakdown (photography, illustration, animation, user-generated content)
- Hook/headline variation impact
- Call-to-action button text analysis
- Creative format performance (static image, video, carousel, collection)
- Audience subgroup responsiveness (by age, gender, interests)

**Usage Example:**
```
My "Sign Up Now" CTA outperforms "Learn More" by 23%. 
But creatives using "Sign Up Now" fatigue 18% faster. 
Why? Recommend CTA rotation strategy to maintain performance 
while extending creative lifespan. Include A/B test recommendations.
```

### 5. **Automated Creative Brief Generation**
Generates production-ready creative briefs for replacement assets:
- Primary value proposition (data-driven angle selection)
- Visual direction (color palette, style, mood)
- Copy templates (headline, primary text, CTA options)
- Audience hooks (specific pain points or desires)
- Format recommendations (based on highest-performing formats in your account)
- Placement optimization notes
- Measurement KPIs for new creative

**Usage Example:**
```
Generate a creative brief to replace my fatiguing "Discount Focus" creative.
The brief should test a new angle (urgency/scarcity). 
Include: 3 headline variations, 3 CTA options, visual mood board direction, 
target audience messaging hooks, and measurement plan.
```

### 6. **Cross-Platform Fatigue Benchmarking**
Compares fatigue patterns across Google Ads, Facebook, and LinkedIn:
- Platform-specific fatigue velocities
- Audience overlap analysis (same users across platforms)
- Creative transferability scores (will this creative work on another platform?)
- Platform-agnostic fatigue signals vs. platform-specific signals

**Usage Example:**
```
My "Educational Content" creative performs well on LinkedIn (4 weeks lifespan) 
but fatigues quickly on Facebook (2 weeks). Analyze why and recommend 
platform-specific adaptations to extend Facebook lifespan to 3+ weeks.
```

### 7. **Slack Alert Integration**
Automated notifications when creatives approach fatigue thresholds:
- "Creative ABC is 72 hours from predicted fatigue—rotate now"
- Daily performance digest with fatigue risk scores
- Weekly rotation calendar with recommended swaps
- Anomaly alerts (unexpected performance changes)

**Setup:**
```
Connect Slack channel: #ad-performance-alerts
Alert triggers: Fatigue risk >75%, CTR variance >20%, CPC spike >15%
Frequency: Daily 9 AM digest + real-time critical alerts
```

---

## Configuration

### Required Environment Variables

```bash
# Google Ads API (required for Google Ads analysis)
export GOOGLE_ADS_API_KEY="your-google-ads-api-key"
export GOOGLE_ADS_CUSTOMER_ID="123-456-7890"

# Facebook Ads API (required for Facebook/Instagram analysis)
export FACEBOOK_ADS_API_KEY="your-facebook-ads-api-token"
export FACEBOOK_ADS_ACCOUNT_ID="act_123456789"

# LinkedIn Campaign Manager API (required for LinkedIn analysis)
export LINKEDIN_ADS_API_KEY="your-linkedin-api-key"
export LINKEDIN_ADS_ACCOUNT_ID="123456789"

# OpenAI (for creative brief generation & analysis)
export OPENAI_API_KEY="sk-your-openai-key"
export OPENAI_MODEL="gpt-4-turbo"

# Optional: Slack integration
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Optional: Google Sheets (for data export)
export GOOGLE_SHEETS_API_KEY="your-google-sheets-api-key"
```

### Configuration Options

```yaml
# Analysis Settings
analysis:
  lookback_window_days: 90          # Historical data to analyze
  fatigue_threshold_ctr_decline: 15 # CTR decline % to flag fatigue
  confidence_interval: 0.95         # Statistical confidence for predictions
  min_impressions_for_analysis: 1000 # Minimum impressions to analyze
  
# Prediction Settings
prediction:
  model_type: "polynomial_regression"  # or "lstm", "arima"
  prediction_horizon_days: 14         # Look ahead period
  alert_lead_time_hours: 72           # Notify before predicted fatigue
  
# Rotation Strategy
rotation:
  recommended_rotation_frequency: "7-14d"  # Suggest rotation every X days
  element_variation_diversity: "high"      # high/medium/low variation
  preserve_winning_elements: true          # Keep high-performing CTAs, hooks
  
# Integrations
integrations:
  slack_alerts: true
  google_sheets_export: true
  hubspot_sync: false
```

---

## Example Outputs

### Output 1: Fatigue Risk Assessment Report

```
CREATIVE FATIGUE ANALYSIS REPORT
Campaign: "Q4 Holiday Campaign" | Period: Oct 1 - Dec 20, 2024
Generated: 2024-12-21 | Confidence: 94%

═══════════════════════════════════════════════════════════════════

CREATIVE: Holiday_Promo_VideoA
├─ Platform: Facebook Ads
├─ Status: ⚠️ HIGH FATIGUE RISK (87/100)
├─ Current Performance:
│  ├─ Impressions: 4.2M | CTR: 2.1% | CPC: $1.23 | ROAS: 3.2x
│  ├─ Baseline (Day 1-7): CTR 3.4% | CPC: $0.89 | ROAS: 4.8x
│  ├─ Performance Decay: CTR -38% | CPC +38% | ROAS -33%
│
├─ Fatigue Prediction:
│  ├─ Predicted Fatigue Date: Dec 28, 2024 (±2 days)
│  ├─ Days Until Fatigue: 7 days
│  ├─ Confidence Level: 91%
│  ├─ Model Used: Polynomial Regression (R² = 0.94)
│
├─ Fatigue Indicators:
│  ├─ CTR Decline Rate: 4.2% per day (↑ acceleration detected)
│  ├─ Frequency Cap Impact: Visible (avg frequency 3.7x)
│  ├─ Cost Inflation: CPC rising faster than platform-wide average
│  ├─ Audience Saturation: 62% of target audience reached
│
└─ Recommendation: ROTATE IMMEDIATELY
   └─ Action: Pause this creative, test new "Gift Guide" angle
   └─ Timeline: Launch replacement by Dec 26

───────────────────────────────────────────────────────────────────

CREATIVE: Holiday_Promo_ImageB
├─ Platform: Google Ads
├─ Status: ✅ STABLE (42/100 risk)
├─ Current Performance:
│  ├─ Impressions: 1.8M | CTR: 1.9% | CPC: $0.78 | Conv: 2.3%
│  ├─ Baseline: CTR 2.0% | CPC: $0.76 | Conv: 2.4%
│  ├─ Performance Decay: CTR -5% | CPC +2.6% | Conv -4%
│
├─ Fatigue Prediction:
│  ├─ Predicted Fatigue Date: Jan 18, 2025 (±4 days)
│  ├─ Days Until Fatigue: 29 days
│  ├─ Confidence Level: 87%
│
└─ Recommendation: MONITOR & PLAN
   └─ Begin creative development for replacement (start in 2 weeks)
   └─ No immediate action needed; creative has 4+ weeks life remaining

═══════════════════════════════════════════════════════════════════
```

### Output 2: Creative Rotation Strategy & Brief

```
CREATIVE ROTATION STRATEGY
Campaign: "B2B SaaS - Lead Generation" | Generated: 2024-12-21

CREATIVE ROTATION CALENDAR
┌─────────────────────┬──────────┬─────────────────┬──────────────┐
│ Creative            │ Status   │ Fatigue Date    │ Action Date  │
├─────────────────────┼──────────┼─────────────────┼──────────────┤
│ Problem_Angle_v1    │ ACTIVE   │ Jan 4, 2025     │ Dec 31, 2024 │
│ Solution_Angle_v1   │ ACTIVE   │ Jan 12, 2025    │ Jan 8, 2025  │
│ Social_Proof_v1     │ ACTIVE   │ Jan 18, 2025    │ Jan 14, 2025 │
│ Demo_Focus_v1       │ RESERVE  │ N/A             │ Ready now    │
└─────────────────────┴──────────┴─────────────────┴──────────────┘

RECOMMENDED CREATIVE BRIEF (Problem_Angle_v1 Replacement)
─────────────────────────────────────────────────────────────────

Campaign Goal: Generate qualified leads for SaaS onboarding software
Target Audience: CTOs, Engineering Managers at 50-5,000 person companies
Primary Value Prop: ROI/Cost Savings (testing Efficiency/Time-Saving angle)

COPY DIRECTION:
Angle: Efficiency & Time Savings (shift from Problem-focused)
Hook: "Your engineers spend 40% of their time on repetitive onboarding tasks."
Headline Options:
  1. "Automate Onboarding. Free Your Best Engineers."
  2. "Cut Onboarding Time From Weeks to Days."
  3. "Your Biggest Resource Drain? We Fixed It."
  
CTA Options:
  1. "See 30-Min Demo" (emphasis on quick time investment)
  2. "Get ROI Calculator" (emphasis on financial benefit)
  3. "Join 500+ Engineering Teams" (social proof angle)

VISUAL DIRECTION:
Style: Clean, modern B2B (shift from previous problem-focused dark tone)
Mood: Optimistic, productive, capability-focused
Color Palette: Bright blue + lime green accent (conveying speed & efficiency)
Format: Single image (test moving from video to static for efficiency angle)
Key Visual: Happy engineer at desk, calendar showing compressed timeline
Avoid: Risk/problem imagery; focus on outcome/productivity

TARGETING & FREQUENCY:
- Segment: Warm (website visitors) + Intent signals (LinkedIn profile visitors)
- Frequency Cap: 2-3x per week (to prevent fatigue in week 2+)
- Audience Size: 45K-120K (sufficient volume while maintaining relevance)
- Geographic: US, UK, Canada (mature SaaS markets)

SUCCESS METRICS (