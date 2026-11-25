---
name: ai-sales-call-trauma-detector-and-objection-reframer
description: "Analyze sales calls to identify hesitation patterns, emotional friction points, and objection triggers. Generate personalized reframes and follow-up scripts. Use when the user needs to improve close rates, understand prospect psychology, or recover stalled deals."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "DEEPGRAM_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🧠"
    }
  }
---

# AI Sales Call Trauma Detector & Objection Reframer

## Overview

The **AI Sales Call Trauma Detector and Objection Reframer** is a production-ready sales psychology tool that transforms raw call recordings into actionable coaching insights. This skill analyzes prospect emotional states, identifies hidden objections rooted in fear or past experiences, and generates personalized reframes that address the *psychology* behind resistance—not just the surface-level objection.

### Why This Matters

Most sales teams treat objections as logical problems to overcome. But 73% of prospect hesitation stems from emotional friction, trust gaps, or past negative experiences (what we call "sales trauma"). This skill bridges that gap by:

- **Detecting micro-signals**: Tone shifts, pause patterns, word choice that reveal emotional resistance
- **Mapping objection psychology**: Distinguishing between "I can't afford it" (budget) vs. "I'm afraid of making the wrong choice" (risk aversion)
- **Generating personalized reframes**: Scripts tailored to *this specific prospect's* psychology, not generic objection-handling templates
- **Automating coaching workflows**: Integrates with Slack, HubSpot, Salesforce, and Pipedrive for team-wide learning

### Integrations & Ecosystem

This skill works seamlessly with:
- **Deepgram** (speech-to-text with emotion detection)
- **OpenAI GPT-4** (psychological analysis and reframe generation)
- **Slack** (team notifications, coaching summaries)
- **HubSpot/Salesforce** (CRM sync for follow-ups)
- **Google Drive** (call recording storage and retrieval)
- **Zapier** (workflow automation)

---

## Quick Start

### Example Prompt 1: Analyze a Call Recording URL

```
Analyze this sales call recording: [paste Google Drive link or Deepgram URL]

Focus on:
1. Emotional friction points (hesitation, skepticism, fear)
2. The psychological root of each objection (not just the surface objection)
3. Prospect's risk tolerance and decision-making style
4. Recommend personalized reframes for the next conversation

Output format: JSON with sections for [friction_points], [objection_psychology], [reframes], [follow_up_script]
```

### Example Prompt 2: Generate Reframes for a Specific Objection

```
My prospect said: "Your solution is great, but we've been burned by similar tools before. We're not ready to commit."

Analyze the psychological root of this objection and generate:
1. Three personalized reframes that address the trust/risk concern
2. A tone-adjusted follow-up email that acknowledges their past experience
3. A low-risk trial structure to rebuild confidence
4. Talking points for the next call that prove incremental value

Consider: This prospect is risk-averse, has had bad vendor experiences, and needs proof before commitment.
```

### Example Prompt 3: Batch Analysis for Sales Team Coaching

```
I have 5 sales calls from this week where we lost deals. Here are the call transcripts:

[Paste transcripts or URLs]

For each call, provide:
1. Prospect hesitation pattern (e.g., "fear of implementation complexity")
2. Sales rep's missed opportunity (where they could have reframed)
3. Personalized reframe the rep should have used
4. Coaching note for the rep (what to work on)

Then generate a team coaching summary highlighting the top 3 patterns across all 5 calls.
```

---

## Capabilities

### 1. **Emotional Friction Detection**

Analyzes call audio/transcripts to identify:
- **Tone shifts**: Prospect confidence drop-offs, sarcasm, defensive language
- **Pause patterns**: Hesitation, thinking (not objecting), uncertainty
- **Word choice signals**: "But," "however," "I'm not sure," "we tried that before"
- **Filler intensity**: Increased "ums," "ahs," "likes" correlate with cognitive load/discomfort

**Usage Example:**
```
Transcript excerpt: "Yeah, the features look good, but... I mean, we've tried 
something similar and it just didn't work out for us. I don't know if your team 
has the bandwidth to support us like we'd need."

Detection output:
- Hesitation marker: "but..." (objection incoming)
- Past trauma signal: "we tried something similar and it didn't work"
- Trust gap: "I don't know if your team has the bandwidth"
- Emotional state: Risk-averse, skeptical, needs proof of support
```

### 2. **Objection Psychology Mapping**

Categorizes objections beyond surface level:

| Surface Objection | Psychological Root | Reframe Strategy |
|---|---|---|
| "It's too expensive" | Fear of wasting budget / ROI uncertainty | Show incremental ROI proof, risk-reversal trial |
| "We're not ready" | Implementation anxiety / change resistance | Break implementation into phases, dedicate support |
| "We've tried this before" | Past failure trauma / vendor distrust | Acknowledge past experience, show what's different |
| "I need to think about it" | Decision paralysis / fear of commitment | Identify missing info, create low-risk next step |

### 3. **Personalized Reframe Generation**

Generates 3-5 reframes per objection, each tailored to:
- Prospect's risk tolerance (conservative, moderate, aggressive)
- Industry context (enterprise vs. SMB, regulated vs. unregulated)
- Decision-making style (analytical, emotional, consensus-driven)
- Relationship stage (first call, second meeting, final negotiation)

**Example Output:**
```
OBJECTION: "We're not ready to commit. We need to see it work for us first."

PSYCHOLOGICAL ROOT: Implementation anxiety + proof requirement

PERSONALIZED REFRAMES:

Reframe 1 (Risk-Reversal):
"I completely understand. Here's what I'd suggest: Let's set up a 30-day 
pilot with your top 3 use cases. If we don't hit X% efficiency gain by day 25, 
we'll pause and refund your investment. You get proof with zero risk."

Reframe 2 (Incremental Proof):
"Most of our best clients started exactly where you are. What if we began 
with just your [specific department] for 60 days? You'll see results fast, 
and the team will be your internal champions for a broader rollout."

Reframe 3 (Social Proof + Specificity):
"[Company X] had the same concern. They started with [specific workflow], 
and within 6 weeks, they cut processing time by 40%. Want me to introduce you 
to their ops lead so you can ask them directly?"

RECOMMENDED TONE: Confident but empathetic, specific with timelines and metrics
```

### 4. **Follow-Up Script Generation**

Creates email and call scripts that:
- Acknowledge the prospect's emotional concern (not just the objection)
- Provide new information or perspective shift
- Include a clear, low-friction next step
- Reference the specific call context

### 5. **Team Coaching Summaries**

Batch-analyzes multiple calls to identify:
- Top 3-5 objection patterns across the team
- Which reps handle objections well (and what they do differently)
- Missed reframe opportunities
- Recommended coaching focus areas

---

## Configuration

### Required Environment Variables

```bash
# OpenAI API key (for GPT-4 analysis and reframe generation)
export OPENAI_API_KEY="sk-..."

# Deepgram API key (for speech-to-text and emotion detection)
export DEEPGRAM_API_KEY="..."

# Optional: HubSpot CRM sync
export HUBSPOT_API_KEY="pat-..."

# Optional: Slack notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

### Setup Instructions

1. **Get API Keys:**
   - OpenAI: https://platform.openai.com/api-keys
   - Deepgram: https://console.deepgram.com
   - HubSpot: https://app.hubspot.com/l/api-key
   - Slack: https://api.slack.com/apps

2. **Upload Call Recording:**
   - Use Google Drive, Deepgram, or direct file upload
   - Supported formats: MP3, WAV, M4A, OGG (any format Deepgram accepts)
   - Minimum quality: 16kHz sample rate

3. **Choose Analysis Mode:**
   - **Quick Analysis** (2-3 min): Emotion detection + top objections
   - **Deep Analysis** (5-7 min): Full psychology mapping + 5 reframes per objection
   - **Team Coaching** (10-15 min): Batch analysis across multiple calls

---

## Example Outputs

### Single Call Analysis Output

```json
{
  "call_metadata": {
    "duration_minutes": 23,
    "prospect_name": "Sarah Chen",
    "company": "TechCorp Inc.",
    "call_stage": "second_meeting",
    "sales_rep": "Mike Johnson"
  },
  "emotional_friction_points": [
    {
      "timestamp": "5:32",
      "friction_type": "hesitation",
      "signal": "Prospect: 'That's... interesting. But we've had bad experiences with implementation partners before.'",
      "confidence": 0.92,
      "interpretation": "Past trauma + trust gap. Prospect needs proof of support quality."
    },
    {
      "timestamp": "12:15",
      "friction_type": "decision_paralysis",
      "signal": "Prospect: 'I mean, I like it, but I'd need to run this by the team. There are a lot of stakeholders.'",
      "confidence": 0.88,
      "interpretation": "Consensus-driven decision-maker. Needs internal champion strategy."
    }
  ],
  "objection_psychology": [
    {
      "surface_objection": "We've had bad experiences with similar tools.",
      "psychological_root": "Vendor distrust + implementation anxiety",
      "risk_tolerance": "conservative",
      "decision_style": "consensus_driven",
      "reframe_strategy": "acknowledge_past + differentiation + proof"
    },
    {
      "surface_objection": "We need to get internal alignment first.",
      "psychological_root": "Fear of being the sole champion of change",
      "risk_tolerance": "conservative",
      "decision_style": "consensus_driven",
      "reframe_strategy": "internal_champion_support + multi_stakeholder_proof"
    }
  ],
  "personalized_reframes": [
    {
      "objection_index": 0,
      "reframe": "Sarah, I hear you. Implementation failures are painful. That's exactly why we built our process around YOUR team's timeline. We assign a dedicated implementation lead who sits with you weekly. In fact, [Company Y] had the same concern, and their implementation took 3 weeks vs. the 12-week nightmare they had before. Want me to connect you with their ops lead?",
      "tone_notes": "Empathetic, specific, social proof, low risk",
      "expected_impact": "high"
    },
    {
      "objection_index": 0,
      "reframe": "I get it—you want to bring the team in. Here's what I'd suggest: Let's do a 30-minute workshop with your key stakeholders next Tuesday. I'll show them exactly how this works in your workflow. Then they'll have the confidence to champion this internally.",
      "tone_notes": "Collaborative, action-oriented, removes friction",
      "expected_impact": "high"
    },
    {
      "objection_index": 1,
      "reframe": "That's smart to get alignment. Most of our best implementations started with a champion like you. What if we set up a quick demo for your team on [date]? I'll focus on the metrics that matter to operations AND finance. You'll walk in as the hero who found the solution.",
      "tone_notes": "Supportive, flattering (appropriate), specific",
      "expected_impact": "medium"
    }
  ],
  "follow_up_email": {
    "subject": "Let's get your team on board—30-min workshop next Tuesday?",
    "body": "Hi Sarah,\n\nThanks for the great conversation today. I loved learning about your team's past challenges with implementation partners—that context is super valuable.\n\nHere's what I'm thinking: Instead of me just talking at your team, let's do a 30-minute interactive workshop where I show how our process works *in your workflow*. Your ops and finance folks will see exactly how this reduces their workload.\n\nI'm confident they'll see what you already see: this is the right move.\n\nCan we get 30 minutes on your calendars for Tuesday at 2 PM or Wednesday at 10 AM?\n\nLooking forward,\nMike",
    "tone": "collaborative, specific, removes friction"
  },
  "coaching_note_for_sales_rep": {
    "rep": "Mike Johnson",
    "what_went_well": "You acknowledged Sarah's past experience and didn't dismiss it. That built rapport.",
    "missed_opportunity": "When Sarah mentioned needing team alignment, you could have immediately offered to facilitate a multi-stakeholder demo. Instead, you left it vague.",
    "recommended_coaching": "For consensus-driven prospects, always have a 'team workshop' offer ready. It removes friction and positions you as a problem-solver, not a pushy vendor.",
    "next_call_focus": "Lead with the multi-stakeholder demo offer. Make it easy for Sarah to champion this internally."
  },
  "predicted_close_probability": {
    "before_reframe": 0.35,
    "after_implementing_reframes": 0.72,
    "confidence": 0.85
  }
}
```

### Team Coaching Summary Output

```markdown
# Weekly Sales Call Analysis: Top Patterns & Coaching Focus

## Calls Analyzed
- 5 calls analyzed
- 3 losses, 1 advance, 1 closed deal
- Total duration: 87 minutes

## Top 3 Objection Patterns

### Pattern 1: "We've tried this before" (60% of calls)
**Psychological Root:** Vendor distrust + implementation trauma
**Rep Performance:** Inconsistent
- ✅ Mike Johnson: Acknowledged past experience, offered proof via intro to similar company
- ❌ Sarah Lee: Dismissed concern, pivoted to features (lost deal)
- ❌ James Wu: Over-explained why their previous solution failed (defensive tone)

**Coaching Recommendation:** Train team on "past trauma acknowledgment" + social proof strategy

### Pattern 2: "We need team alignment" (80% of calls)
**Psychological Root:** Fear of being sole champion + consensus decision-making
**Rep Performance:** Weak
- ❌ All reps left this vague ("Sure, get alignment")
- ✅ None offered to facilitate multi-stakeholder demo

**Coaching Recommendation:** Create "multi-stakeholder demo" script. Train reps to offer this proactively.

### Pattern 3: "It's too expensive" (40% of calls)
**Psychological Root:** ROI uncertainty + budget constraints
**Rep Performance:** Strong
- ✅ Mike Johnson: Showed ROI calculator, offered pilot with money-back guarantee
- ✅ Sarah Lee: Broke into phases, reduced initial investment by 60%

**Coaching Recommendation:** Replicate Mike and Sarah's approach across team. Consider making ROI calculator standard.

## Individual Rep Coaching

| Rep | Strength | Growth Area | Recommendation |
|---|---|---|---|
| Mike Johnson | Builds rapport, uses social proof | Needs to offer multi-stakeholder demos earlier | Mentor on consensus-driven prospect strategy |
| Sarah Lee | Confident, good at ROI conversation | Dismisses emotional objections too quickly | Practice empathy-first reframes |
| James Wu | Thorough, knowledgeable | Over-explains, comes across as defensive | Coach on "less is more" approach |

## Team Focus