---
name: ai-customer-interview-analyst
description: "Analyze customer interview transcripts to extract pain points, feature requests, and sentiment. Use when the user needs market insights, customer research analysis, or product feedback synthesis from interviews."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","ANTHROPIC_API_KEY"],"bins":["ffmpeg","sox"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🎤"}}
---

## Overview

The **AI Customer Interview Analyst** processes raw customer interview transcripts (audio, video, or text) and transforms them into structured, actionable insights. This skill automatically identifies pain points, feature requests, sentiment shifts, buying signals, and customer motivations—then organizes findings by segment, use case, and priority.

### Why This Matters

Product teams and marketers spend weeks manually reviewing interview recordings and transcripts. This skill compresses that workflow into minutes, surfacing the most critical insights while preserving direct customer quotes for stakeholder presentations. Perfect for:

- **Product Managers**: Validate roadmap decisions with data-backed customer themes
- **Marketing Teams**: Identify messaging angles and positioning from real customer language
- **Startup Founders**: Synthesize early customer feedback into product-market fit signals
- **User Researchers**: Automate coding and thematic analysis across 50+ interviews
- **Sales Leaders**: Spot buying signals and objection patterns to coach teams

### Integration Points

Works seamlessly with:
- **Google Drive / OneDrive**: Direct transcript import and report export
- **Slack**: Push key insights and summaries to team channels
- **Notion**: Embed structured reports into product decision databases
- **HubSpot CRM**: Tag accounts by sentiment and buying signals
- **Airtable**: Sync insights into structured databases for filtering/analysis
- **Zapier / Make**: Trigger workflows on insight detection

---

## Quick Start

### Example 1: Analyze a Text Transcript

```
Analyze this customer interview transcript and extract:
1. Top 3 pain points (with quotes)
2. Feature requests (organized by frequency)
3. Sentiment trajectory (beginning → end)
4. Buying signals and objections
5. Customer segment and use case

Transcript:
"We're currently using Slack for all team communication, but it's a mess. 
Messages get lost, and nobody can find decisions from last month. I've asked 
for better search, but honestly, we'd pay for a tool that just archives 
conversations by project. Right now, we're wasting 2 hours a week searching 
for stuff. That's killing our productivity. One thing though—your pricing 
seems high compared to Slack. But if this solves the archive problem, we'd 
definitely try it."

Format the output as JSON with sections for pain_points, feature_requests, 
sentiment, buying_signals, and customer_profile.
```

### Example 2: Batch Process Multiple Interviews

```
I have 12 customer interview transcripts (attached as text files). For each:
1. Extract the top 5 pain points
2. Identify all feature requests
3. Rate sentiment (1-10 scale)
4. Flag any buying signals or budget mentions
5. Categorize by industry and company size

Then create a summary report showing:
- Most common pain points across all interviews
- Feature requests ranked by mention frequency
- Average sentiment by company size
- List of hot leads (high buying signal + budget mention)

Output as a structured CSV and a markdown summary.
```

### Example 3: Sentiment & Objection Analysis

```
Analyze the attached video interview transcript for:
1. Sentiment shifts (when and why the customer's tone changed)
2. All objections raised (price, complexity, integration, etc.)
3. How objections were resolved (if at all)
4. Final likelihood to buy (1-10)
5. Recommended follow-up talking points

Focus on the exact quotes where sentiment changed, so I can coach my sales team 
on how to handle similar objections.
```

---

## Capabilities

### 1. **Transcript Processing & Transcription**
- **Audio/Video Input**: Accepts MP3, WAV, M4A, MP4, MOV files (auto-transcribed via OpenAI Whisper API)
- **Text Input**: Paste or upload raw transcripts (PDF, DOCX, TXT)
- **Language Support**: English, Spanish, French, German, Mandarin, Japanese
- **Speaker Identification**: Detects and labels multiple speakers (Interviewer, Customer, Stakeholder)
- **Timestamp Preservation**: Maintains timestamps for easy reference in video/audio

### 2. **Pain Point Extraction**
Automatically identifies and categorizes customer pain points:
- **Operational Friction**: Time-wasting, manual processes, inefficiency
- **Technical Limitations**: Missing features, poor integrations, performance
- **Cost & ROI**: Pricing objections, budget constraints, value concerns
- **User Experience**: Complexity, learning curve, adoption barriers
- **Competitive Pressure**: Losing to competitors, feature gaps vs. alternatives

Each pain point includes:
- Direct quote from transcript
- Frequency (mentioned once or multiple times)
- Severity rating (1-10 based on emotional intensity)
- Associated customer segment

### 3. **Feature Request & Wish List Synthesis**
- Explicit requests: "We need better search"
- Implicit requests: "It's hard to find old messages" → inferred feature need
- Frequency ranking: Sorted by how many customers mentioned similar needs
- Workaround detection: Identifies manual processes customers use to compensate
- Competitive comparisons: Flags features customers want from competitors

### 4. **Sentiment & Emotional Journey Mapping**
- **Opening Sentiment**: Initial tone and attitude toward your product/category
- **Turning Points**: Moments where sentiment shifted (positive or negative)
- **Closing Sentiment**: Final impression and likelihood to recommend
- **Emotional Drivers**: What caused shifts (frustration, excitement, relief, skepticism)
- **Tone Markers**: Detects sarcasm, hesitation, enthusiasm, resignation

### 5. **Buying Signal Detection**
Flags high-intent indicators:
- Budget mentions: "We allocated $50K for tools"
- Timeline: "We need this by Q2"
- Decision-maker confirmation: "I'd need to discuss with our CFO, but I'm interested"
- Competitive displacement: "We're looking to replace Slack"
- Urgency language: "This is becoming critical"
- Trial interest: "Can we get a 2-week trial?"

### 6. **Objection & Concern Mapping**
- Price objections and budget constraints
- Complexity and implementation concerns
- Integration and compatibility issues
- Security and compliance hesitations
- Vendor lock-in worries
- How each objection was addressed (or left unresolved)

### 7. **Customer Segmentation & Profiling**
Automatically extracts and organizes:
- **Company Size**: Startup, SMB, Enterprise
- **Industry**: SaaS, Healthcare, Finance, Retail, Manufacturing, etc.
- **Use Case**: Primary use case and secondary use cases
- **Maturity Level**: Early-stage, established, scaling
- **Buying Authority**: Individual contributor, manager, C-suite
- **Competitive Context**: Current solutions and switching costs

### 8. **Structured Report Generation**
Produces multiple output formats:
- **JSON**: Machine-readable for CRM/database integration
- **CSV**: Bulk import into Airtable, Notion, Google Sheets
- **Markdown**: Shareable summaries for Slack, email, wikis
- **PDF**: Executive reports with charts and quotes
- **Slide Deck**: Google Slides with key findings and customer quotes

---

## Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...          # For GPT-4 analysis and transcription
ANTHROPIC_API_KEY=sk-ant-...   # For Claude backup analysis (optional but recommended)

# Optional integrations
SLACK_WEBHOOK_URL=https://hooks.slack.com/...  # Auto-post insights to Slack
GOOGLE_DRIVE_API_KEY=...       # Auto-import transcripts from Drive
AIRTABLE_API_KEY=...           # Auto-sync findings to Airtable
HUBSPOT_API_KEY=...            # Tag CRM accounts with insights
```

### Setup Instructions

1. **Obtain API Keys**:
   - OpenAI: https://platform.openai.com/account/api-keys
   - Anthropic: https://console.anthropic.com/
   - Slack (optional): https://api.slack.com/apps

2. **Install Dependencies** (if running locally):
   ```bash
   pip install openai anthropic pydub ffmpeg-python
   brew install ffmpeg sox  # macOS
   apt-get install ffmpeg sox  # Linux
   ```

3. **Set Environment Variables**:
   ```bash
   export OPENAI_API_KEY="your-key-here"
   export ANTHROPIC_API_KEY="your-key-here"
   ```

4. **Test the Skill**:
   ```bash
   claw test ai-customer-interview-analyst
   ```

### Configuration Options

```yaml
analysis_depth: "comprehensive"  # comprehensive, standard, quick
sentiment_scale: 10              # 5 or 10-point scale
include_timestamps: true         # For audio/video transcripts
segment_by: "industry"           # industry, company_size, use_case
export_format: "json"            # json, csv, markdown, pdf
slack_notifications: true        # Auto-post findings to Slack
```

---

## Example Outputs

### Output 1: JSON Structure

```json
{
  "transcript_metadata": {
    "duration_minutes": 45,
    "speakers": ["Interviewer", "Sarah Chen (VP Product, Acme Inc)"],
    "language": "en",
    "transcribed_at": "2024-01-15T10:30:00Z"
  },
  "customer_profile": {
    "company_name": "Acme Inc",
    "industry": "SaaS",
    "company_size": "50-200 employees",
    "role": "VP Product",
    "use_case": "Team communication and project management",
    "buying_authority": "decision_maker"
  },
  "sentiment": {
    "opening": 6,
    "closing": 7,
    "trajectory": "positive_trend",
    "turning_point": "When we discussed the API integration capabilities"
  },
  "pain_points": [
    {
      "category": "Operational Friction",
      "description": "Messages get lost in Slack; no way to archive by project",
      "severity": 9,
      "quote": "Messages get lost, and nobody can find decisions from last month.",
      "frequency": "mentioned_3_times"
    },
    {
      "category": "Technical Limitations",
      "description": "Poor search functionality across historical conversations",
      "severity": 8,
      "quote": "We're wasting 2 hours a week searching for stuff.",
      "frequency": "mentioned_2_times"
    }
  ],
  "feature_requests": [
    {
      "request": "Project-based conversation archiving",
      "type": "explicit",
      "frequency": 3,
      "quote": "We'd pay for a tool that just archives conversations by project."
    },
    {
      "request": "Advanced search with filters",
      "type": "implicit",
      "frequency": 2,
      "inferred_from": "Complaints about finding old messages"
    }
  ],
  "buying_signals": [
    {
      "signal": "Budget allocated",
      "confidence": "high",
      "quote": "We'd definitely try it if this solves the archive problem."
    },
    {
      "signal": "Timeline mentioned",
      "confidence": "medium",
      "detail": "Implied urgency but no specific date"
    }
  ],
  "objections": [
    {
      "objection": "Pricing concern",
      "severity": 6,
      "quote": "Your pricing seems high compared to Slack.",
      "resolution_status": "unresolved"
    }
  ],
  "recommended_next_steps": [
    "Address pricing concern with ROI calculator (2 hours/week saved)",
    "Schedule demo of archive and search features",
    "Prepare case study showing similar SMB success"
  ]
}
```

### Output 2: Markdown Summary Report

```markdown
# Customer Interview Analysis: Acme Inc

**Customer**: Sarah Chen, VP Product  
**Company**: Acme Inc (SaaS, 50-200 employees)  
**Date**: January 15, 2024  
**Duration**: 45 minutes  

## Sentiment Overview
- **Opening**: 6/10 (cautiously interested)
- **Closing**: 7/10 (more positive)
- **Trend**: ↗ Positive (became more interested during discussion of API features)

## Top Pain Points

### 1. Message Loss & Archive Limitations (Severity: 9/10)
> "Messages get lost, and nobody can find decisions from last month."

**Impact**: Wasting 2 hours/week searching for conversations  
**Mentioned**: 3 times  
**Root Cause**: Current tool (Slack) lacks project-based organization

### 2. Poor Search Functionality (Severity: 8/10)
> "We're wasting 2 hours a week searching for stuff. That's killing our productivity."

**Impact**: Productivity loss, decision-making delays  
**Mentioned**: 2 times

## Feature Requests (Ranked by Demand)

1. **Project-based conversation archiving** (3 mentions)
   - Explicit request: "We'd pay for a tool that just archives conversations by project"
   - High commercial signal

2. **Advanced search with filters** (2 mentions)
   - Implicit need inferred from pain points
   - Would directly address time-wasting

## Buying Signals 🔥

✅ **Budget Allocated**: "We'd definitely try it"  
✅ **Willingness to Pay**: "We'd pay for a tool that..."  
⚠️ **Price Sensitivity**: "Your pricing seems high compared to Slack"  

**Likelihood to Buy**: 7/10 (High, pending pricing negotiation)

## Objections & Concerns

| Objection | Severity | Status | Notes |
|-----------|----------|--------|-------|
| Pricing | 6/10 | Unresolved | Expects lower cost than current solution |
| Integration | Not raised | — | Good sign—no concerns about existing tools |
| Implementation | Not raised | — | Suggests low complexity expectations |

## Recommended Actions

1. **Short-term (This week)**:
   - Send ROI calculator showing 2 hrs/week saved = $X annual value
   - Schedule product demo focused on archive + search features

2. **Medium-term (Next 2 weeks)**:
   - Prepare custom pricing proposal for 50-person company
   - Share case study from similar SaaS company

3. **Long-term**:
   - Discuss integration with their existing tools (Jira, Asana)
   - Explore expansion to other teams if pilot succeeds

---

## Key Quotes for Marketing

> "Messages get lost, and nobody can find decisions from last month."

> "We're wasting 2 hours a week searching for stuff. That's killing our productivity."

> "We'd pay for a tool that just archives conversations by project."
```

### Output 3: CSV for Bulk Import

```csv
interview_id,company_name,industry,company_size,role,pain_point,severity,feature_request,buying_signal,objection,sentiment_opening,sentiment_closing,recommended_action
INT-001,Acme Inc,SaaS,50-200,VP Product,Message loss,9,Project archiving,Budget allocated,Pricing,6,7,ROI calculator + demo
INT-002,TechStart,SaaS,10-50,Founder,Poor search,8,Advanced filters,High interest,None,7,8,Schedule trial
INT-003,Enterprise Co,Enterprise,500+,Manager,Integration gaps,7,Slack integration,Timeline Q2,Security review,5,6,Compliance documentation
```

---

## Tips & Best Practices

### 1. **Prepare Interviews for Maximum Insight**
- **Ask open-ended questions**: "What's the biggest challenge you face?" yields more insights than yes/no questions
- **Let customers talk**: Silence is golden—don't interrupt or over-guide
- **Dig into "why"**: When you hear a pain point, ask "why is that a problem?" 3 times to find root causes
- **Record everything**: Audio/video transcripts capture tone and sentiment better than notes

### 2. **Optimize Transcript Quality**
- **Clear