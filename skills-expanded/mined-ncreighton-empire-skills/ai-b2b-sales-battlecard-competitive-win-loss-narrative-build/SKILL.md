---
name: ai-b2b-sales-battlecard-competitive-win-loss-narrative-builder
description: "Generate dynamic B2B sales battlecards from win/loss call recordings and competitor analysis. Use when the user needs competitive intelligence, objection handling frameworks, or personalized buyer persona strategies for enterprise deals."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","GOOGLE_CLOUD_SPEECH_TO_TEXT_KEY","SLACK_WEBHOOK_URL"],"bins":["ffmpeg","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"⚔️"}}
---

## Overview

The **AI B2B Sales Battlecard & Competitive Win/Loss Narrative Builder** transforms raw competitive intelligence into actionable, persona-specific sales battlecards that evolve in real-time based on deal outcomes. 

This skill automates the entire battlecard lifecycle:
- **Ingests** win/loss call recordings, customer interview transcripts, and competitor websites
- **Analyzes** objection patterns, competitive claims, and buyer pain points using GPT-4 + Claude
- **Generates** dynamic battlecards tailored to specific buyer personas (CFO, CTO, VP Sales, etc.)
- **Tracks** which competitor claims actually influence deal outcomes
- **Distributes** via Slack, email, or embedded widgets to sales teams in real-time

Perfect for mid-market and enterprise SaaS companies competing against 3-5 primary rivals. Integrates with **Slack**, **Gong**, **Chorus**, **HubSpot**, **Salesforce**, **Google Drive**, and **Notion** for seamless workflow integration.

---

## Quick Start

### Example 1: Generate a Battlecard from a Win/Loss Call Recording

```
Generate a competitive battlecard from this win/loss call recording:

Audio file: https://drive.google.com/file/d/1xYzAbC123/view
Competitor mentioned: Salesforce
Buyer persona: VP of Sales
Deal value: $150K ACV
Outcome: WON (we beat Salesforce)

Include:
- Salesforce's top 3 claims in this deal
- Our counter-narratives with proof points
- Objection patterns we heard
- Recommended talking points for similar deals
- Confidence score for each counter-narrative
```

### Example 2: Analyze Competitor Website & Create Objection Framework

```
Create a competitive narrative framework:

Competitor: HubSpot
Competitor website: https://www.hubspot.com/products/sales
Our product: [Your SaaS product name]
Target buyer personas: CFO, VP Sales, Sales Operations Manager

Output format:
- Top 5 HubSpot claims extracted from their website
- Our counter-claims (ranked by deal impact)
- Objection patterns we've seen in lost deals
- Persona-specific talking points for each buyer type
- Win probability uplift if we use these narratives
```

### Example 3: Build Dynamic Battlecard Library from Multiple Win/Loss Interviews

```
Generate a battlecard library from multiple customer interviews:

Interviews: 
- Lost deal with Acme Corp (chose Salesforce)
- Won deal with TechCo (beat HubSpot)
- Lost deal with GlobalBank (chose Marketo)

Competitors: Salesforce, HubSpot, Marketo
Buyer personas: CMO, VP Marketing, Marketing Operations
Time period: Last 90 days

Produce:
- 3 separate battlecards (one per competitor)
- Persona-specific variations
- Win/loss ratio for each narrative
- Recommended distribution cadence for sales team
```

---

## Capabilities

### 1. **Automated Win/Loss Call Transcription & Analysis**
- Accepts MP3, WAV, M4A, or video files (auto-transcribes via Google Cloud Speech-to-Text)
- Extracts competitor mentions, objections, and buying signals
- Identifies which competitor claims caused deals to slip away
- Timestamps key moments for sales coaching

**Usage:**
```
Analyze this win recording and extract the competitor's 
top 3 claims that our prospect asked about:
[Upload file or provide Gong/Chorus link]
```

### 2. **Competitor Website Intelligence Extraction**
- Crawls competitor websites and extracts product claims, pricing, positioning
- Identifies messaging changes month-over-month
- Flags new feature announcements and competitive threats
- Builds a competitive claims database (searchable by claim type)

**Usage:**
```
Monitor competitor website changes:
Competitor: Zendesk
Frequency: Weekly
Alert me on: New feature claims, pricing changes, 
new case studies, new integrations
```

### 3. **Buyer Persona-Specific Battlecard Generation**
- Creates separate battlecard versions for CFO, CTO, VP Sales, CMO, etc.
- Tailors language, metrics, and ROI proof points to each persona's priorities
- Includes persona-specific objection handlers
- Recommends which persona to target first in deals

**Usage:**
```
Generate 3 versions of our HubSpot battlecard:
- For CFO: Focus on TCO, implementation cost, ROI timeline
- For VP Sales: Focus on adoption, rep productivity, forecasting
- For Sales Ops: Focus on data integrity, integrations, automation

Include 2-3 proof points per objection for each persona.
```

### 4. **Real-Time Objection Pattern Recognition**
- Analyzes 50+ win/loss calls to identify the TOP objections that actually move deals
- Ranks objections by frequency AND deal impact (not just frequency)
- Surfaces which objections are "deal-killers" vs. "speed bumps"
- Recommends counter-narratives ranked by effectiveness

**Usage:**
```
Analyze our last 30 win/loss calls.
Show me:
- Top 5 objections that killed deals (lost deals only)
- Top 5 objections that we successfully overcame (won deals)
- Win rate by objection type
- Most effective counter-narratives for each objection
```

### 5. **Dynamic Battlecard Evolution & Feedback Loop**
- Tracks which battlecard narratives actually win deals
- Updates win/loss ratio for each claim and counter-narrative
- Recommends retiring ineffective talking points
- Surfaces emerging competitor threats in real-time

**Usage:**
```
Update our battlecard library with this month's deal outcomes:
- Won deals: [List 5 deal IDs from Salesforce]
- Lost deals: [List 3 deal IDs from Salesforce]

Show me:
- Which narratives correlate with wins
- Which narratives are underperforming
- Recommended changes to our messaging
```

### 6. **Multi-Channel Distribution & Sales Enablement**
- Publishes battlecards to Slack (with daily digest option)
- Embeds interactive battlecards in HubSpot/Salesforce
- Generates PDF versions for sales collateral
- Creates email sequences with objection handlers
- Syncs with Notion for collaborative editing

**Usage:**
```
Publish our updated battlecards:
Channels: Slack #sales-enablement, Salesforce content library, 
          HubSpot knowledge base
Format: Interactive HTML + PDF
Frequency: Weekly updates, daily alerts on new competitor threats
Recipients: All AEs, Sales Managers, Solutions Engineers
```

---

## Configuration

### Required Environment Variables

```bash
# OpenAI API (for battlecard generation & analysis)
export OPENAI_API_KEY="sk-proj-xxxxx"

# Google Cloud (for speech-to-text transcription)
export GOOGLE_CLOUD_SPEECH_TO_TEXT_KEY="path/to/service-account.json"

# Slack (for team notifications & distribution)
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Optional: Salesforce integration
export SALESFORCE_CLIENT_ID="your-client-id"
export SALESFORCE_CLIENT_SECRET="your-client-secret"

# Optional: HubSpot integration
export HUBSPOT_API_KEY="pat-xxx"

# Optional: Google Drive (for transcript storage)
export GOOGLE_DRIVE_FOLDER_ID="your-folder-id"
```

### Configuration Options

```yaml
# battlecard_config.yaml
battlecard:
  # Competitor tracking
  competitors:
    - name: "Salesforce"
      website: "https://www.salesforce.com"
      monitor_frequency: "weekly"
    - name: "HubSpot"
      website: "https://www.hubspot.com"
      monitor_frequency: "weekly"
  
  # Buyer personas to generate
  personas:
    - "CFO"
    - "VP Sales"
    - "Sales Operations Manager"
    - "VP Marketing"
  
  # Objection tracking
  objection_analysis:
    min_calls_for_pattern: 5
    rank_by: "deal_impact"  # not just frequency
    
  # Distribution
  distribution:
    slack:
      enabled: true
      channel: "#sales-enablement"
      frequency: "daily"
    salesforce:
      enabled: true
      sync_frequency: "6h"
    hubspot:
      enabled: true
      knowledge_base_id: "xxx"
```

---

## Example Outputs

### Sample Battlecard Output (HubSpot vs. Our Product)

```markdown
# HubSpot Competitive Battlecard
**Generated:** 2024-01-15 | **Confidence Score:** 92% | **Win Rate:** 67%

## Executive Summary
- **Competitor:** HubSpot
- **Last Updated:** Weekly from 47 win/loss calls
- **Your Win Rate vs. HubSpot:** 67% (↑ 8% from last month)
- **Top Emerging Threat:** HubSpot's new AI-powered forecasting

---

## Top 3 HubSpot Claims (from their website + sales calls)

### Claim #1: "HubSpot is the #1 CRM for SMBs"
**Frequency in calls:** 12/47 (26%)
**Deal impact:** HIGH (mentioned in 8/12 lost deals)
**Our counter-narrative:** 
> "HubSpot excels for SMBs, but enterprise teams need [Your Product]'s 
> advanced forecasting and custom workflows. 73% of our customers moved 
> FROM HubSpot because they outgrew it."
**Proof point:** Case study - TechCorp (saved $400K by switching)
**Recommended for personas:** VP Sales, Sales Ops

### Claim #2: "Easy to implement in 30 days"
**Frequency in calls:** 9/47 (19%)
**Deal impact:** MEDIUM
**Our counter-narrative:**
> "HubSpot's 30-day timeline assumes basic use cases. Enterprise 
> implementations with custom workflows take 60-90 days. Our implementation 
> is transparent and includes change management."
**Proof point:** Median implementation time: 45 days (vs. HubSpot's hidden costs)
**Recommended for personas:** CFO, IT Director

### Claim #3: "Best-in-class AI forecasting"
**Frequency in calls:** 5/47 (11%)
**Deal impact:** MEDIUM (emerging threat)
**Our counter-narrative:**
> "HubSpot's AI is powered by historical data only. [Your Product] uses 
> real-time signals (email engagement, meeting sentiment, buying signals) 
> for 40% higher forecast accuracy."
**Proof point:** Gartner Magic Quadrant positioning
**Recommended for personas:** VP Sales, CFO

---

## Persona-Specific Talking Points

### For CFO
- **ROI:** $1.2M saved in 12 months (vs. HubSpot's hidden upgrade costs)
- **TCO:** 32% lower 3-year cost of ownership
- **Risk:** HubSpot's pricing increases 20% annually; ours are fixed

### For VP Sales
- **Adoption:** 85% team adoption in 60 days (vs. HubSpot's 45%)
- **Productivity:** 12 hours/month saved per rep on forecasting
- **Accuracy:** 40% better forecast accuracy = better pipeline visibility

### For Sales Ops
- **Integrations:** Native integrations with 200+ tools (vs. HubSpot's 150)
- **Customization:** Unlimited custom fields & workflows (HubSpot limits)
- **Data:** Real-time data sync (vs. HubSpot's 6-hour delay)

---

## Top Objections We've Overcome

| Objection | Win Rate | Best Counter | Proof Point |
|-----------|----------|--------------|-------------|
| "HubSpot is cheaper" | 82% | TCO analysis (3-year cost) | Gartner report |
| "HubSpot has better AI" | 71% | Real-time signal advantage | Case study |
| "HubSpot is easier to use" | 65% | Demo + onboarding plan | Customer testimonial |

---

## Recommended Next Steps
1. Schedule a 30-min ROI analysis call (focus on CFO)
2. Offer a 2-week POC with your top 5 power users
3. Share TechCorp case study (similar company size/industry)
```

---

## Tips & Best Practices

### 1. **Feed the Engine with Quality Win/Loss Data**
- Conduct structured win/loss interviews (not just sales reps' opinions)
- Ask: "What competitor did you consider?" and "Why did you choose us/them?"
- Record all calls (with consent) for transcription accuracy
- Include lost deals (not just wins) for balanced analysis

### 2. **Refresh Competitor Websites Weekly**
- Competitor messaging changes fast; set automated crawls
- Track pricing pages, feature announcements, and case studies
- Flag new integrations and partnerships (emerging threats)
- Share competitive alerts via Slack #sales-enablement daily

### 3. **Tailor Battlecards to Your Sales Cycle**
- Enterprise deals (12+ months): Focus on TCO, implementation, risk mitigation
- Mid-market deals (3-6 months): Focus on ROI, adoption, time-to-value
- SMB deals (1-3 months): Focus on ease of use, pricing, quick wins

### 4. **Measure Battlecard Effectiveness**
- Track which battlecards are used in Salesforce opportunities
- Correlate battlecard usage with win/loss outcomes
- Retire talking points with <50% win rate
- Promote high-performing narratives to sales team

### 5. **Create Persona-Specific Versions**
- Don't send one battlecard to all stakeholders
- CFO wants ROI and TCO; CTO wants architecture and security
- Use HubSpot/Salesforce to route the right battlecard to the right buyer
- A/B test different narratives on similar deals

### 6. **Integrate with Sales Workflows**
- Embed battlecards in Salesforce opportunity records
- Trigger battlecard suggestions based on competitor mention in Gong calls
- Send Slack alerts when a competitor is mentioned in a deal
- Include battlecard links in sales playbooks and email templates

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Create false or misleading claims** about competitors  
- All counter-narratives are grounded in real customer feedback and data
- Proof points must be verifiable (case studies, analyst reports, customer testimonials)
- Avoids FUD (Fear, Uncertainty, Doubt) tactics; focuses on factual differentiation

❌ **Violate competitor intellectual property**  
- Does not reproduce competitor marketing materials verbatim
- Summarizes and analyzes competitor claims; does not plagiarize
- Respects copyright and trademark regulations

❌ **Share confidential customer data**  
- Anonymizes all customer names and deal details in battlecards
- Removes sensitive financial information from transcripts
- Complies with NDA agreements in win/loss interviews

❌ **Generate battlecards without human review**  
- All AI-generated content requires sales leadership approval before distribution
- Recommend a 24-hour review period before publishing
- Flag any claims that lack supporting evidence

❌ **Assume one-size-fits-all messaging**  
- Requires explicit persona selection; does not auto-target
- Battlecards must be customized per buyer type and deal stage
- Warns if battlecard is used in wrong context

### Limitations

⚠️ **Transcription accuracy depends on audio quality**  
- Requires clear, single-speaker audio for best results
- Background noise reduces transcription accuracy to 70-80%
- Recommend professional transcription service for critical calls

⚠️ **Competitor website crawling may be limited by robots.txt**  
- Respects competitor