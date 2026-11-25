---
name: video-script-to-thumbnail-psychologist
description: "Analyze video scripts and generate data-backed thumbnail design briefs with emotional hooks, color psychology, and A/B test variations. Use when the user needs YouTube, TikTok, or Reels thumbnails optimized for CTR, audience psychology, and retention benchmarks."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "GOOGLE_VISION_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🎬"
    }
  }
---

# Video Script-to-Thumbnail Psychologist

## Overview

The **Video Script-to-Thumbnail Psychologist** transforms raw video scripts into actionable, psychologically-optimized thumbnail design briefs. This skill bridges the gap between content creation and visual psychology—analyzing emotional arcs, audience retention patterns, and niche-specific benchmarks to recommend thumbnails that command attention and drive clicks.

Instead of guessing which thumbnail works, you get **data-backed design recommendations** that account for:
- **Emotional triggers** identified in your script (urgency, curiosity, humor, fear)
- **Color psychology** calibrated to your niche (tech, beauty, fitness, finance)
- **Retention-critical moments** that warrant visual emphasis
- **A/B test variations** backed by industry CTR benchmarks (YouTube: 4-8%, TikTok: 5-15%)
- **Accessibility & contrast ratios** (WCAG 2.1 AA compliance)
- **Platform-specific constraints** (aspect ratios, text size minimums, safe zones)

**Ideal for:** YouTube creators, TikTok strategists, Instagram Reels producers, course creators, and agencies managing multi-channel video content.

**Integrations:** Works with Zapier (trigger on new scripts), Slack (post briefs to team channels), Google Drive (analyze script PDFs), and Airtable (track A/B test results).

---

## Quick Start

Try these prompts to see the skill in action:

### Example 1: YouTube Tutorial Script
```
Analyze this video script for a YouTube tech tutorial and generate a thumbnail brief:

SCRIPT:
"Hey everyone! Today I'm showing you the one AI tool that replaced my $5,000/month 
SaaS subscription. This literally saved me 40 hours last month. Let's dive in..."

VIDEO METADATA:
- Niche: Tech/AI tools
- Target audience: Solopreneurs, content creators
- Platform: YouTube (16:9 thumbnail, 1280x720px)
- Expected watch time: 8-12 minutes

Generate the full thumbnail psychology brief with color palette, 
text recommendations, facial expression guidance, and 3 A/B variations.
```

### Example 2: TikTok Hook-Focused Script
```
I need a thumbnail brief for this TikTok Reels hook. My audience is fitness enthusiasts, 
and I'm testing different emotional angles.

HOOK SCRIPT:
"POV: You've been doing pushups wrong for 20 years. Watch this 30-second fix that 
elite athletes use..."

What visual elements should I prioritize? What color contrast will stop the scroll? 
Generate A/B test recommendations for skepticism vs. intrigue angles.
```

### Example 3: Course Creator Thumbnail Strategy
```
Generate thumbnail briefs for my 5-module course funnel:
Module 1 hook: "Why your landing page converts 0.5% (hint: it's not the copy)"
Module 2 hook: "The psychology behind $10K customer acquisitions"
Module 3 hook: "How to build a $50K/month digital product in 90 days"

I want consistent branding but emotional variety. Generate 5 briefs with 
color psychology notes for each module. My audience: aspiring entrepreneurs (25-45).
```

---

## Capabilities

### 1. Emotional Arc Analysis
The skill dissects your script to identify emotional triggers and maps them to visual psychology:
- **Urgency/FOMO:** Recommended red/orange accents, deadline text, arrow/progress visuals
- **Curiosity:** Recommendation for blur/cutoff text, question marks, "See what happens next" visual language
- **Humor:** Guidance on bold typography, unexpected color combinations, expressive facial angles
- **Fear/Pain:** Dark backgrounds, stark contrast, problem-oriented imagery
- **Solution/Hope:** Bright, warm colors; upward-facing composition; success indicators

**Example output snippet:**
```
EMOTIONAL HOOKS DETECTED:
1. "This literally saved me 40 hours" → ASPIRATION + RELIEF
   Visual strategy: Warm orange/gold accents, smiling expression with raised eyebrows,
   clock/time-save iconography. CTR benchmark: 5.2% (SaaS niche average: 4.8%)

2. "One AI tool replaced my $5K subscription" → SURPRISE + ENVY
   Visual strategy: Contrasting color (complementary to primary), slightly shocked 
   facial expression, money/savings visual element.
```

### 2. Color Psychology & Contrast Calibration
Analyzes niche benchmarks and recommends color palettes optimized for:
- **Platform-specific CTR data** (what colors perform in your category)
- **Contrast ratios** (WCAG AA: 4.5:1 for text, 3:1 for graphics)
- **Scroll-stopping potential** (color novelty within niche context)
- **Audience demographics** (color preferences by age/geography)

**Supported niches:** Tech, Finance, Beauty/Wellness, Fitness, Education, Entertainment, E-commerce, Gaming, Personal Development.

### 3. Retention-Critical Moment Identification
Scans your script for moments that signal high audience retention and flags them for thumbnail emphasis:
- Unexpected plot twists or reveals
- Specific pain-point acknowledgments
- Solution moments with tangible benefits
- Social proof or authority markers
- Calls-to-action or curiosity questions

### 4. A/B Test Variation Generator
Produces 3-5 thumbnail design variations based on:
- **Emotional angle variations** (curiosity vs. urgency vs. solution-focused)
- **Audience segment testing** (what speaks to beginners vs. advanced users)
- **Industry CTR benchmarks** (recommend which variation has highest predicted CTR)
- **Text vs. no-text trade-offs** (legibility on small screens vs. design clarity)
- **Facial expression alternatives** (if you appear in thumbnail)

### 5. Design Implementation Checklist
Actionable, step-by-step guidance for executing the brief in tools like:
- Canva Pro (templates, font recommendations, export settings)
- Adobe Express (design automation for batch creation)
- Figma (component-based design for consistency)
- Photoshop (advanced compositing techniques)

**Includes:** Font sizes (minimum 24pt for body text), safe zone mapping, file format recommendations (PNG for transparency), and quality assurance steps.

### 6. Platform-Specific Optimization
Generates platform-tailored recommendations:
- **YouTube:** 16:9 aspect ratio, text size for 480p preview, safe zones for channel art overlap
- **TikTok/Reels:** 9:16 aspect ratio, text centering, full-bleed imagery, 2-3 second visual impact window
- **Shorts:** Square 1:1 format, bold typography, minimal text (3-5 words max)

---

## Configuration

### Required Environment Variables
```bash
# OpenAI API access (for script analysis & recommendation generation)
OPENAI_API_KEY=sk-...

# Google Vision API (for contrast ratio & accessibility analysis)
GOOGLE_VISION_API_KEY=...

# Optional: Industry benchmark data source
BENCHMARK_DATA_SOURCE=youtube_analytics  # or tiktok_analytics, industry_report
```

### Setup Instructions

1. **Authenticate APIs:**
   ```bash
   # Verify OpenAI API key
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   
   # Verify Google Vision API
   gcloud auth activate-service-account --key-file=credentials.json
   ```

2. **Configure niche benchmarks** (optional):
   ```json
   {
     "niche": "tech_tools",
     "avg_ctr": 4.8,
     "top_performing_colors": ["#FF6B35", "#004E89", "#F77F00"],
     "target_audience": "solopreneurs_25-45",
     "platform": "youtube"
   }
   ```

3. **Set output preferences:**
   ```json
   {
     "output_format": "markdown",  // or json, pdf
     "include_design_checklist": true,
     "a_b_variations_count": 4,
     "accessibility_standard": "wcag_2_1_aa"
   }
   ```

---

## Example Outputs

### Sample Thumbnail Brief (Output)

```
═══════════════════════════════════════════════════════════════
THUMBNAIL PSYCHOLOGY BRIEF
Script: "The One AI Tool That Replaced My $5K SaaS"
Platform: YouTube | Duration: 8 min | Niche: Tech Tools
═══════════════════════════════════════════════════════════════

📊 EMOTIONAL HOOKS & VISUAL STRATEGY
───────────────────────────────────────

HOOK #1: "Replaced my $5K subscription"
└─ Primary emotion: SURPRISE + ASPIRATION
└─ Visual priority: Money symbol, bold number, shocked expression
└─ Recommended text: "$5K → FREE" or "Saved $60K/year"
└─ Color strategy: Complementary contrast (see below)
└─ CTR benchmark: 5.2% (tech niche avg: 4.8%)
└─ Predicted performance: HIGH (aspiration + specificity)

HOOK #2: "40 hours saved last month"
└─ Primary emotion: RELIEF + PROOF
└─ Visual priority: Clock/timer icon, checkmark, upward arrow
└─ Recommended text: "40 Hours Saved" (avoid "-40 hrs" which signals loss)
└─ Color strategy: Warm accent (orange/gold)
└─ CTR benchmark: 4.6% (time-saving angle)
└─ Predicted performance: MEDIUM (strong, but secondary to money)

───────────────────────────────────────
🎨 COLOR PSYCHOLOGY PALETTE
───────────────────────────────────────

PRIMARY PALETTE:
  Primary: #004E89 (deep tech blue—authority, trust)
  Accent 1: #FF6B35 (burnt orange—urgency, energy, wealth)
  Accent 2: #F1FAEE (off-white—clarity, breathing room)

RATIONALE:
  Tech niche responds to blue (trust in tools) + orange (premium/exclusive feel).
  CTR data shows 23% higher performance vs. generic red in finance/SaaS.
  Contrast ratio: 7.2:1 (WCAG AAA compliant—exceeds standard).

ALTERNATIVE PALETTE (curiosity angle):
  Primary: #2A2E4E (mysterious dark purple)
  Accent 1: #FFD60A (yellow—attention, novelty)
  Accent 2: #001D3D (near black—sophistication)

───────────────────────────────────────
😊 FACIAL EXPRESSION & TEXT GUIDANCE
───────────────────────────────────────

RECOMMENDED EXPRESSION: Surprised + confident (raised eyebrows, slight smile)
  └─ WHY: Signals discovery + proof of success simultaneously
  └─ AVOID: Neutral expression (converts 18% lower), angry (misaligns with solution)
  └─ GAZE DIRECTION: Eyes slightly up-right (psychologically suggests "thinking" / "eureka")

TEXT OVERLAY SPECS:
  Headline: "$5K → FREE" (20px, bold sans-serif, #FF6B35)
  Subtext: "Works in 2024" (14px, #004E89, medium weight)
  Safety: Place headline in center 60% of thumbnail (visible on mobile)
  Font recommendation: Montserrat Bold or Inter Black (high legibility at 480p)

───────────────────────────────────────
🎯 A/B TEST VARIATIONS
───────────────────────────────────────

VARIATION A (Money-focused):
  Emotional angle: ASPIRATION + GREED
  Visual: Your face (surprised expression) + large "$5K" crossed out + green checkmark
  Text: "$5K → FREE" (primary), "Now available" (secondary)
  Predicted CTR: 5.4% | Recommended audience: Entrepreneurs, course creators

VARIATION B (Time-focused):
  Emotional angle: RELIEF + PROOF
  Visual: Your face + clock icon + "40 HRS" highlighted
  Text: "40 HOURS SAVED" (primary), "This month" (secondary)
  Predicted CTR: 4.7% | Recommended audience: Busy professionals, agencies

VARIATION C (Tool-name focused):
  Emotional angle: CURIOSITY + DISCOVERY
  Visual: Your face (slight confusion → smile progression) + blurred tool interface
  Text: "??? REPLACED MY SaaS" | "See what it is..." (curiosity gap)
  Predicted CTR: 5.1% | Recommended audience: Tech enthusiasts, early adopters

VARIATION D (Social proof angle):
  Emotional angle: FOMO + ASPIRATION
  Visual: Your face + 3 testimonial avatars (real users or stock) + "2,847 saved"
  Text: "2,847 People Saved $60K" (primary)
  Predicted CTR: 4.9% | Recommended audience: Risk-averse, consensus-seekers

WINNER PREDICTION: Variation A (money-focused) for broad tech audience.
                    Test A vs. B first (money vs. time—niche-specific driver).

───────────────────────────────────────
✅ DESIGN IMPLEMENTATION CHECKLIST
───────────────────────────────────────

TOOL: Canva Pro (easiest) | Figma (most control) | Photoshop (professional)

[ ] Step 1: Create 16:9 canvas (1280x720px)
[ ] Step 2: Set background to #004E89 (primary blue)
[ ] Step 3: Add high-contrast image (your face or product screenshot)
[ ] Step 4: Layer headline text—Montserrat Bold, 72px, #FF6B35
[ ] Step 5: Add accent shape (orange rectangle, 4px) under text
[ ] Step 6: Insert symbol ($ icon or clock), size 48px, #FF6B35
[ ] Step 7: Verify contrast ratios (accessibility checker: Stark plugin / Figma)
[ ] Step 8: Export as PNG (transparency safe) + JPG (YouTube backup)
[ ] Step 9: Preview at 480px width (mobile view—critical!)
[ ] Step 10: A/B test all 4 variations. Track CTR for 2 weeks.

QA CHECKLIST:
  ✓ Text legible on 320px mobile phone (test on actual device)
  ✓ Contrast ratio ≥ 4.5:1 for text (use WebAIM contrast checker)
  ✓ No critical content in outer 10% (YouTube logo safe zone)
  ✓ File size < 2MB (optimize images in TinyPNG)
  ✓ Upload as PNG first (preserves quality better than JPG)

───────────────────────────────────────
🔬 PERFORMANCE TRACKING
───────────────────────────────────────

METRICS TO MONITOR:
  • Click-through rate (CTR) — target: 5%+ (up from 4.8% baseline)
  • Impression volume — should increase by 8-15% with optimized thumbnail
  • Audience retention (avg. view duration) — higher CTR often signals better match
  • Thumbnail A/B test winner (YouTube Studio: test Variations A & B simultaneously)

TESTING TIMELINE:
  Week 1-2: Run Variations A & B (500+ impressions each for statistical significance)
  Week 3: Switch to winner + Variation C
  Week 4: Finalize thumbnail strategy; apply learnings to next 5 videos

───────────────────────────────────────
⚠️ PLATFORM-SPECIFIC NOTES
───────────────────────────────────────

YOUTUBE:
  • Dimensions: