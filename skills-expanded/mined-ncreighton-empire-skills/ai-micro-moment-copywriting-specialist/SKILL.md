---
name: ai-micro-moment-copywriting-specialist
description: "Generate hyper-contextual micro-copy for cart abandonment, password resets, onboarding friction, and permission requests. Use when the user needs conversion-optimized copy for specific user moments, A/B testing variations, or brand voice consistency across micro-interactions."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "OPTIONAL_BRAND_VOICE_FILE"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "✨"
    }
  }
---

## Overview

The **AI Micro-Moment Copywriting Specialist** generates high-converting, intent-based micro-copy for the critical moments that drive user behavior: cart abandonment follow-ups, password reset confirmations, onboarding friction points, post-purchase delays, permission requests, and error recovery flows.

Unlike generic copywriting tools that produce bulk content, this skill targets **micro-interactions**—the small, high-impact text strings that appear at decisive moments in the user journey. Research shows that optimized micro-copy can drive **3-7% conversion lifts** by reducing friction, building trust, and reinforcing brand voice at the exact moment users are most receptive.

### Why This Matters

Micro-moments are where conversions are won or lost:
- A password reset email with clear, friendly language increases completion rates by 15-20%
- Permission request copy that explains *why* you need data increases grant rates by 25-40%
- Cart abandonment follow-ups with urgency + reassurance recover 8-12% of lost revenue
- Onboarding friction-point copy that reduces cognitive load improves activation by 18-30%

This skill integrates with **WordPress, Shopify, Stripe, Auth0, Segment, Google Analytics, Slack, and custom APIs** to analyze user flows, generate contextual copy variations, and recommend optimal placement.

---

## Quick Start

### Example 1: Generate Cart Abandonment Email Copy

```
Generate 3 variations of cart abandonment follow-up copy for an e-commerce brand 
(high-end fitness equipment). The email goes out 2 hours after cart abandonment. 
Brand voice: professional, motivational, no pressure. Include a trust element 
(free shipping or guarantee). Target audience: fitness enthusiasts aged 25-45.
```

**Expected Output:**
- Variation A (Urgency-focused): "Your custom kettlebell set is waiting—claim free shipping in the next 12 hours"
- Variation B (Reassurance-focused): "Not sure about your order? 60-day money-back guarantee + free returns"
- Variation C (Social proof-focused): "Join 12,000+ customers who transformed their home gym this month"

---

### Example 2: Password Reset Confirmation Flow

```
Create micro-copy for a 3-step password reset flow for a SaaS fintech app. 
Brand voice: trustworthy, concise, security-conscious. Include: 
1) Initial reset request confirmation 
2) Email link validation message 
3) Success confirmation with next steps. 
Audience: busy professionals who need speed + security assurance.
```

**Expected Output:**
- Step 1: "Password reset requested. Check your email for a secure link (expires in 30 min)"
- Step 2: "Verified. Create a strong password—we recommend 12+ characters"
- Step 3: "Password updated. Your account is secure. Return to login >"

---

### Example 3: Permission Request Optimization

```
Generate permission request copy for a mobile app asking for location access. 
Current conversion rate: 32%. Brand: casual, helpful, privacy-conscious. 
Explain the benefit clearly without being pushy. Include a "learn more" option.
Target: iOS users, 18-35, lifestyle app context.
```

**Expected Output:**
- Default: "We'd like to access your location to show nearby events and save you time"
- Optimized: "See events near you (or anywhere you want to travel) + get personalized recommendations"
- Alt: "Your location stays private. We use it only to show relevant events"

---

## Capabilities

### 1. **Micro-Moment Type Detection & Generation**

The skill identifies the user journey moment and generates contextual copy:

- **Cart Abandonment**: 2-hour, 24-hour, and re-engagement sequences
- **Password Reset**: Multi-step confirmation flows with security messaging
- **Onboarding Friction**: Empty states, permission requests, first-time setup
- **Post-Purchase Delays**: Shipping updates, confirmation reassurance, upsell moments
- **Permission Requests**: Location, contacts, camera, push notifications
- **Error Recovery**: 404s, timeouts, payment failures, auth issues
- **Checkout Optimization**: Shipping cost transparency, trust badges, final-step reassurance

### 2. **A/B Testing Variation Generation**

Generates 3-5 copy variations optimized for different psychological triggers:

```
Generate A/B test variations for a "Complete Your Profile" onboarding prompt. 
Primary trigger: social proof. Secondary: urgency. Tertiary: benefit clarity. 
Include CTAs. Target: B2B SaaS, professional audience.
```

Output includes:
- Variation A (Social Proof): "Join 5,000+ professionals who completed their profiles—takes 2 min"
- Variation B (Urgency): "Finish now to unlock advanced features (limited time)"
- Variation C (Benefit): "Complete profile = better job matches + recruiter visibility"
- Variation D (Friction Reduction): "Just 3 fields left. We'll auto-fill the rest"
- Variation E (Control): "Complete your profile"

### 3. **Brand Voice Consistency Engine**

Upload or describe your brand voice, and the skill maintains consistency across all generated copy:

```
My brand voice: conversational, witty, slightly irreverent, empowering. 
We're a women's fitness brand. Generate 4 password reset copy variations 
maintaining this voice while keeping security clear.
```

### 4. **Placement & Context Recommendations**

Suggests optimal placement, timing, and channel for each piece of micro-copy:

- Email subject vs. body vs. CTA button
- In-app modal vs. inline notification vs. banner
- Timing: immediate vs. delayed vs. triggered
- Personalization tokens: {firstName}, {productName}, {cartValue}

### 5. **Conversion Lift Estimation**

Provides estimated impact based on industry benchmarks:

```
Generate post-purchase delay copy (order shipped but not yet delivered) 
for an apparel brand. Estimate conversion lift for retention/upsell metrics.
```

Output includes copy + estimated metrics:
- Baseline re-engagement rate: 8%
- Estimated lift with optimized copy: +2-3% (10-11% total)
- Recommended A/B test duration: 2 weeks / 5,000+ users

### 6. **Integration & Implementation Guidance**

Provides code snippets and integration instructions for:

- **WordPress**: WooCommerce email templates, checkout optimization
- **Shopify**: Liquid template syntax, email notification customization
- **Stripe**: Email template integration, webhook-triggered messaging
- **Auth0**: Custom email templates, MFA prompts
- **Segment**: Event-triggered copy personalization
- **Slack**: Notification copy for alerts and workflows
- **Google Analytics**: Tracking recommendations for A/B testing

---

## Configuration

### Required Environment Variables

```bash
# OpenAI API key for GPT-4 powered generation
export OPENAI_API_KEY="sk-..."

# Optional: Path to your brand voice guidelines document
export OPTIONAL_BRAND_VOICE_FILE="/path/to/brand-voice.md"

# Optional: Slack webhook for sharing generated copy with team
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Optional: Google Sheets ID for logging A/B test results
export GOOGLE_SHEETS_ID="1abc..."
```

### Setup Instructions

1. **Get your OpenAI API key** from https://platform.openai.com/api-keys
2. **Create a brand voice document** (optional but recommended):
   ```markdown
   # Brand Voice Guidelines
   - Tone: [professional/casual/playful]
   - Key values: [list 3-5]
   - Audience: [description]
   - Avoid: [specific phrases/topics]
   - Personality traits: [list]
   ```
3. **Set environment variables** in your `.env` file or terminal
4. **Test the skill** with the Quick Start examples above

### Configuration Options

```
--moment-type: [cart-abandonment|password-reset|onboarding|post-purchase|permission|error|checkout]
--variations: 3-5 (default: 3)
--brand-voice: [path to file or inline description]
--target-audience: [description for personalization]
--channel: [email|sms|in-app|push|web]
--urgency-level: [low|medium|high]
--include-personalization: [true|false]
--include-social-proof: [true|false]
--include-guarantee: [true|false]
--test-duration-days: [7|14|30]
```

---

## Example Outputs

### Output 1: Cart Abandonment Sequence (3-Email Flow)

**Email 1 (2 hours after abandonment)**
```
Subject: Your kettlebell set is waiting for you

Hi Sarah,

You left something great behind—your custom kettlebell set is still in your cart 
(and it's still on sale with free shipping 🎁).

[View Cart >]

No pressure, but this deal expires in 12 hours.

—The Strength Team
```

**Email 2 (24 hours later)**
```
Subject: Sarah, one more thing about your order...

Your kettlebell set + the adjustable stand you were eyeing = a complete home gym 
(and customers say it cuts workout setup time in half).

Still worried? 60-day money-back guarantee. No questions.

[Complete Order >]

—The Strength Team
```

**Email 3 (48 hours, final)**
```
Subject: Your kettlebell set is almost gone

Only 3 left in stock. Free shipping ends tonight.

If you decide it's not for you, we get it. But 12,000+ customers are already 
crushing their goals with this set.

[Claim Yours >]

—The Strength Team
```

---

### Output 2: Permission Request Copy (iOS Location)

**Generated Variations with Metrics:**

| Variation | Copy | Estimated Grant Rate | Trigger |
|-----------|------|----------------------|---------|
| A (Control) | "We'd like to access your location" | 32% | Baseline |
| B (Benefit) | "See events near you + get personalized recommendations" | 45% | Benefit clarity |
| C (Privacy) | "Your location stays private. We only use it to show relevant events" | 48% | Trust/transparency |
| D (Social) | "Join 50K+ users who get personalized event recommendations" | 42% | Social proof |
| E (Friction) | "Just 1 permission to unlock full features" | 38% | Urgency |

**Recommendation:** Test Variation C (Privacy-focused) first—highest conversion + strongest trust signal.

---

### Output 3: Onboarding Friction-Point Copy

**Empty State (No Data Yet)**
```
"You haven't added any workouts yet.

Start by logging your first session—takes 60 seconds. 
We'll track progress, suggest improvements, and celebrate your wins.

[Log First Workout >]"
```

**First-Time Setup Completion**
```
"Almost there! Just 3 fields left.

We'll auto-fill the rest from your profile. (You can edit anytime.)"
```

**Success Confirmation**
```
"Profile complete! 🎉

You're all set. Your first personalized workout plan is ready.

[See Your Plan >]"
```

---

## Tips & Best Practices

### 1. **Test Psychological Triggers Strategically**

Different moments respond to different triggers:

- **Cart Abandonment**: Urgency + reassurance (combine deadline with guarantee)
- **Password Reset**: Security + clarity (explain why you need the reset)
- **Permission Requests**: Benefit + privacy (lead with what they gain, reassure about data)
- **Onboarding**: Progress + social proof (show how close they are, who's already done it)
- **Post-Purchase**: Reassurance + delight (confirm order, add unexpected value)

### 2. **Personalization Increases Conversion by 15-25%**

Always include:
- First name or account name
- Product/service name they interacted with
- Specific value or benefit they showed interest in
- Relevant timeline or deadline

```
❌ "Your order has shipped"
✅ "Sarah, your kettlebell set ships tomorrow (free 2-day delivery included!)"
```

### 3. **Keep Micro-Copy Short**

Micro-moments demand micro-content:
- Email subject: 30-50 characters
- Email preview: 85-100 characters
- Button text: 2-5 words
- Modal headline: 1 short sentence
- Body copy: 2-3 short paragraphs max

### 4. **Test One Variable at a Time**

For valid A/B results:
- Test copy variations, not design changes (separate test)
- Run for minimum 2 weeks or 5,000 users
- Track: click-through rate, conversion rate, time-to-completion
- Use statistical significance calculator (95% confidence minimum)

### 5. **Leverage Emotion + Logic**

Best micro-copy combines:
- **Emotional hook**: Why this matters to the user
- **Logical benefit**: What they specifically gain
- **Social proof**: Who else has benefited
- **Clear CTA**: Exactly what to do next

Example:
```
"Join 12,000+ professionals who increased productivity 30% 
(and got their time back). Start your free trial."
```

### 6. **Document What Works**

Create a "Micro-Copy Wins" document:
- Copy variation + conversion lift
- Audience segment + context
- Why it worked (trigger type, personalization, etc.)
- Reusable patterns for future moments

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Generate misleading or deceptive copy** — All output avoids dark patterns, false urgency (fake "last item" claims), or manipulative scarcity tactics

❌ **Create copy for illegal activities** — No gambling, unregulated financial products, or prohibited goods

❌ **Bypass user consent** — Will not generate copy designed to trick users into permissions they don't want to grant

❌ **Violate privacy regulations** — Generated copy respects GDPR, CCPA, and other privacy laws; will not suggest collecting unnecessary data

❌ **Impersonate or deceive** — Will not generate copy pretending to be from law enforcement, financial institutions, or other trusted entities for phishing

❌ **Generate spam or harassment** — Will not create copy for unsolicited marketing to non-opted-in users

### Boundaries & Limitations

- **Brand voice accuracy**: Requires detailed brand guidelines for best results; generic descriptions may produce generic copy
- **Personalization tokens**: User must implement token replacement (e.g., {firstName}) in their system
- **Testing infrastructure**: Skill recommends A/B testing approach but requires user to implement and track results
- **Industry specificity**: Works best for e-commerce, SaaS, and mobile apps; may need customization for highly regulated industries (finance, healthcare)
- **Language**: Currently optimized for English; other languages available but not as thoroughly tested
- **Tone calibration**: May require 1-2 iterations to perfectly match brand voice; provide detailed feedback for refinement

### Ethical Guidelines

- All generated copy should be **honest and transparent**
- Urgency should be **real** (actual deadlines, genuine scarcity)
- Social proof should be **verifiable** (real customer counts, actual testimonials)
- Guarantees should be **honored** (no fine print that contradicts the promise)
- Data requests should be **justified** (explain why you need each permission)

---

## Troubleshooting

### Q: Generated copy doesn't match my brand voice

**A:** The skill learns from detailed brand guidelines. Try:
1. Upload a 500+ word brand voice document with tone examples, do's/don'ts, and audience details
2. Provide 2-3 examples of your best existing copy
3. Specify tone descriptors: "conversational + professional" vs. "playful + irreverent"
4. Request 5+ variations and pick the closest, then ask for refinement: "Make this more [specific adjustment]"

---

### Q