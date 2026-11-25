---
name: ai-micro-interaction-copy-and-friction-point-ux-writer
description: "Generate contextual microcopy from UX friction analysis. Writes button labels, error messages, tooltips, and empty states that reduce user hesitation. Use when the user needs friction-point identification, A/B copy variants, or tone consistency audits."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "✍️"
    }
  }
---

## Overview

The AI Micro-Interaction Copy and Friction-Point UX Writer automates the discovery and remediation of user experience friction points through intelligent microcopy generation. This skill analyzes session recordings, heatmap data, and user behavior patterns to identify moments where users hesitate, then generates contextually appropriate copy that reduces friction and improves conversion.

**Why it matters:**
- **Conversion lift**: Strategic microcopy can increase CTR by 15-30% on key interactions
- **User confidence**: Clear, contextual copy reduces support tickets and cart abandonment
- **Consistency**: Maintains brand voice across all touchpoints (web, mobile, app, email)
- **Speed**: Generates A/B test variants in seconds, not days

**Integrations supported:**
- **Session Recording**: Hotjar, Fullstory, Logrocket, Clarity (Microsoft)
- **Analytics**: Google Analytics 4, Mixpanel, Amplitude
- **Design Tools**: Figma, Adobe XD (for direct annotation)
- **CMS**: WordPress, Webflow, Shopify
- **Collaboration**: Slack (for team notifications), Notion (for copy libraries)
- **A/B Testing**: Optimizely, VWO, Convert

---

## Quick Start

### Example 1: Analyze Checkout Friction & Generate Copy
```
Analyze this checkout flow for friction points:
- Step 1: Product selection (95% completion)
- Step 2: Shipping address (87% completion, 12% bounce)
- Step 3: Payment method (76% completion, 18% drop-off)
- Step 4: Order review (72% completion)

Generate microcopy for:
1. The shipping address form (high hesitation)
2. The payment method selector (highest drop-off)
3. An empty state for saved addresses
4. An error message for invalid postal codes

Include A/B variants for each, tone: friendly but professional.
```

### Example 2: Create Error Message Variants with Tone Audit
```
Our app shows this error when users exceed API rate limits:
"Error 429: Too many requests. Please try again later."

Generate:
1. Three tone variants (formal, friendly, humorous)
2. Contextual copy for a retry button
3. A tooltip explaining what "rate limiting" means
4. An empty state message when the user hits the limit

Audit all variants for consistency with our brand voice: 
"helpful, non-technical, empowering."
```

### Example 3: Empty State & Onboarding Microcopy
```
Our users see an empty state when they first sign up.
Currently it says: "No data yet."

Generate:
1. Three variants of empty state copy (encouraging, curiosity-driven, action-oriented)
2. Microcopy for a "Get Started" button
3. A tooltip for the "Import Data" feature
4. A reassuring message for first-time users

Session data shows 34% of users leave at this point.
Tone should be: warm, reassuring, action-focused.
```

---

## Capabilities

### 1. **Friction Point Identification**
Analyzes user session data to pinpoint moments of hesitation:
- **Scroll depth analysis**: Where users stop reading
- **Form abandonment patterns**: Which fields cause drop-off
- **Click heatmaps**: Misclicked or missed interactive elements
- **Time-on-page metrics**: Unusually long pauses (indicates confusion)
- **Rage clicks**: Repeated clicking on non-interactive elements

**Usage:**
```
Analyze heatmap data from our homepage:
- 40% of visitors scroll past the "Sign Up" CTA
- 23% click the logo 3+ times (expecting navigation)
- Form field "Company Size" has 18% error rate

Generate copy that:
1. Makes the CTA more compelling
2. Clarifies what "Company Size" means with a tooltip
3. Adds a breadcrumb/navigation hint near the logo
```

### 2. **Contextual Microcopy Generation**
Creates purpose-built copy for specific UI elements:
- **Button labels**: Action-oriented, benefit-driven, scannable
- **Form labels & placeholders**: Clear, concise, jargon-free
- **Error messages**: Specific, actionable, non-blaming
- **Success messages**: Confirmatory, encouraging, next-step guidance
- **Tooltips**: Concise explanations (max 100 chars)
- **Empty states**: Reassuring, action-focused, not depressing
- **Loading states**: Progress indicators with personality
- **Confirmation dialogs**: Clear consequences, easy undo options

### 3. **A/B Test Variant Generation**
Produces multiple copy variants optimized for different user segments:
- **Variant A (Control)**: Current or baseline copy
- **Variant B (Benefit-driven)**: Emphasizes user benefit
- **Variant C (FOMO/Urgency)**: Time-sensitive or scarcity language
- **Variant D (Curiosity)**: Question-based or intrigue-driven
- **Variant E (Simplicity)**: Shortest, most direct phrasing

Each variant includes predicted performance metrics and audience fit.

### 4. **Tone Consistency Auditing**
Ensures all microcopy aligns with brand voice:
- **Audit scope**: Analyzes 50+ copy elements across your product
- **Voice dimensions**: Formal/Casual, Technical/Non-technical, Friendly/Professional, Urgent/Calm
- **Inconsistency detection**: Flags copy that deviates from brand guidelines
- **Tone report**: Shows coverage % for each voice dimension
- **Recommendations**: Suggests rewrites to improve consistency

**Example output:**
```
TONE AUDIT REPORT
Brand Voice: Friendly, Non-technical, Empowering, Helpful

Consistency Score: 78% (target: 90%)

Issues Found:
- "Invalid credentials" (Button label) → Too formal, should be "Let's try again"
- "Insufficient permissions" (Error) → Too technical, should be "You don't have access yet"
- "Syncing..." (Loading state) → Vague, should be "Getting your data ready..."

Recommendations: 8 rewrites needed to reach 90% consistency
```

### 5. **Integration with Design & Development**
- **Figma annotations**: Auto-comment copy suggestions directly on frames
- **CSV export**: For developer handoff or CMS bulk upload
- **JSON export**: For mobile app localization and A/B testing platforms
- **Slack notifications**: Alert teams when friction points are identified
- **Notion database**: Maintains a searchable library of all generated copy

---

## Configuration

### Environment Variables
```bash
# Required for OpenAI-powered analysis
OPENAI_API_KEY=sk-...

# Required for extended analysis & tone auditing
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Session recording integrations
HOTJAR_API_KEY=...
FULLSTORY_API_KEY=...
CLARITY_API_KEY=...

# Optional: Analytics integrations
GOOGLE_ANALYTICS_4_KEY=...
MIXPANEL_API_KEY=...

# Optional: Slack notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/...

# Optional: Figma annotations
FIGMA_API_TOKEN=...
```

### Setup Instructions

1. **Provide session data** (one of these formats):
   - JSON export from Hotjar, Fullstory, or Clarity
   - CSV with page, element, bounce_rate, time_on_element
   - Figma file link (for direct annotation)

2. **Define brand voice** (optional, but recommended):
   ```
   Brand Voice Guidelines:
   - Tone: Warm, helpful, non-technical
   - Avoid: Jargon, corporate speak, exclamation marks
   - Do: Use contractions, active voice, benefit-driven language
   - Examples of on-brand: "Let's get you started", "Here's what's next"
   ```

3. **Specify target audience** (optional):
   - Primary user type (e.g., "first-time users", "enterprise admins")
   - Pain points or objections they commonly have
   - Preferred communication style

4. **Set output preferences**:
   - Export format: JSON, CSV, Markdown, Figma
   - Include A/B variants? (yes/no)
   - Tone audit required? (yes/no)
   - Slack notifications? (yes/no)

---

## Example Outputs

### Output 1: Friction Point Analysis with Copy Suggestions
```
FRICTION POINT: Shipping Address Form
Severity: High (12% bounce rate, 45 sec avg time-on-page)

Current Copy Issues:
- "Address Line 2" label is unclear (is it optional?)
- "Postal Code" error message: "Invalid format" (not actionable)
- No indication that form is required

Generated Microcopy:

Button Label:
- Original: "Continue"
- Variant A: "Continue to Payment" (context-aware)
- Variant B: "Save & Review Order" (benefit-driven)

Form Field Label (Address Line 2):
- Suggested: "Apartment, suite, or building (optional)"
- Tone: Clear, reassuring, optional status explicit

Error Message (Postal Code):
- Original: "Invalid format"
- Suggested: "Please use format: 12345 or 12345-6789"
- Tone: Specific, actionable, helpful

Empty State (No Saved Addresses):
- Suggested: "No saved addresses yet. Add one to save time on future orders."
- Tone: Encouraging, benefit-focused

Predicted Impact: +8-12% reduction in form abandonment
```

### Output 2: A/B Copy Variants (Email Sign-Up CTA)
```
ELEMENT: Homepage Email Sign-Up Button

Variant A (Control):
"Sign Up"
Predicted CTR: 3.2%
Best for: Existing users, familiar with product

Variant B (Benefit-Driven):
"Get Weekly Tips"
Predicted CTR: 4.1%
Best for: First-time visitors, content-focused

Variant C (Urgency):
"Join 50,000+ Subscribers"
Predicted CTR: 4.8%
Best for: Skeptical users, social proof seekers

Variant D (Curiosity):
"See What's New"
Predicted CTR: 3.9%
Best for: Exploratory users, curious audience

Variant E (Simplicity):
"Subscribe"
Predicted CTR: 3.1%
Best for: Mobile users, minimalist design

Recommendation: Test Variant C first (highest predicted lift)
```

### Output 3: Tone Consistency Report
```
TONE AUDIT: SaaS Product Dashboard

Brand Voice Target: Professional, Friendly, Empowering, Non-technical

Overall Consistency: 82% (4 rewrites needed)

Element Breakdown:
✅ Button labels (95% consistent)
⚠️  Error messages (68% consistent) — 3 rewrites needed
✅ Success messages (100% consistent)
⚠️  Tooltips (72% consistent) — 1 rewrite needed
✅ Empty states (94% consistent)

Specific Issues:
1. "Insufficient permissions" → Should be "You don't have access to this yet"
2. "API key regenerated" → Should be "Your new API key is ready"
3. "Rate limit exceeded" → Should be "You've sent a lot of requests. Try again in a minute."

Time to fix: ~15 minutes
Estimated consistency improvement: +18%
```

---

## Tips & Best Practices

### 1. **Combine Quantitative + Qualitative Data**
Don't rely on heatmaps alone. Pair them with:
- User interviews or feedback surveys
- Session recordings (watch actual user struggles)
- Support ticket analysis (what confuses users most?)

```
Generate copy for our "Password Reset" flow.
Session data shows 34% abandon, but support tickets reveal:
- Users don't understand why they need to reset
- They think they've been hacked (anxious)
- They want confirmation it's safe

Tone should be: Reassuring, clear, non-alarmist.
```

### 2. **Test Copy Variants Systematically**
- Run A/B tests for 2-4 weeks minimum (need statistical significance)
- Test one element at a time (avoid confounding variables)
- Track not just CTR, but downstream metrics (conversion, retention, support tickets)
- Use this skill to generate variants, then validate with real users

### 3. **Maintain a Copy Library**
Build a searchable database of all generated copy:
- Tag by element type (button, error, tooltip, etc.)
- Tag by tone (friendly, urgent, technical, etc.)
- Tag by industry/use case
- Track performance of each variant
- Reuse high-performers across your product

### 4. **Localization & Translation**
If you support multiple languages:
- Generate copy in English first (master version)
- Use this skill to create tone-aware English variants
- Then hand off to professional translators (context matters)
- Avoid machine translation for microcopy (loses tone/personality)

### 5. **Mobile-First Microcopy**
Mobile users have less screen space and patience:
- Keep button labels under 15 characters
- Use single-word verbs when possible ("Save", not "Save Changes")
- Avoid abbreviations (spell out "and", don't use "&")
- Test on actual mobile devices, not just desktop

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Generate misleading or deceptive copy**
- Will not create dark patterns or manipulative language
- Will not suggest fake urgency ("Only 2 left!") without data backing
- Will not generate copy that violates FTC guidelines or GDPR

❌ **Replace user research or testing**
- Generates copy suggestions, not guarantees
- Requires A/B testing for validation (no rollout without data)
- Cannot identify friction without actual user behavior data

❌ **Handle sensitive content**
- Will not generate copy for financial transactions without compliance review
- Will not create medical/legal copy (requires licensed professionals)
- Will not generate copy for gambling, tobacco, or regulated industries without legal sign-off

❌ **Automate without human review**
- All generated copy should be reviewed by a human writer
- Tone audit flags are suggestions, not mandates
- Requires approval before deployment to production

### Limitations

- **Data quality dependent**: Garbage in = garbage out. Ensure your session data is accurate.
- **Context limitations**: This skill analyzes UI elements, not full user journeys. Use alongside user research.
- **Language support**: Currently optimized for English. Multi-language support requires translation review.
- **Brand voice accuracy**: Provide clear brand guidelines upfront. Generic tone defaults may not match your brand.
- **Conversion impact varies**: Predicted lift is based on industry benchmarks, not your specific product/audience.

---

## Troubleshooting

### Q: "Generated copy doesn't match our brand voice"
**A:** Provide explicit brand voice guidelines upfront:
```
Our brand voice:
- Tone: Conversational, not corporate
- Avoid: Exclamation marks, ALL CAPS, jargon
- Do: Use contractions, benefit-driven language, active voice
- Examples: "Let's get you set up" (good), "System initialization in progress" (bad)
```

### Q: "Copy variants don't show meaningful differences"
**A:** Specify the audience segment or hypothesis:
```
Generate variants for first-time mobile users who are skeptical.
Variant A: Current copy (control)
Variant B: Add social proof ("Join 10K+ users")
Variant C: Simplify language (remove technical terms)
Variant D: Add benefit ("Save 30 minutes/week")
```

### Q: "Friction points seem obvious/unhelpful"
**A:** Ensure you're providing actual session data, not assumptions:
- Export real heatmap data from Hotjar/Fullstory
- Include time-on-page, scroll depth, click data
- Share 2-3 session recordings for context
- Specify your conversion rate and drop-off points