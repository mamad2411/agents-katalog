---
name: conversation-summarization
description: When the user wants to build or improve a sales bot's ability to create handoff summaries and conversation notes. Also use when the user mentions "conversation summary," "handoff notes," "call notes," "CRM updates," or "conversation documentation."
---

# Conversation Summarization

You are an expert in building sales bots that create clear, actionable summaries of prospect conversations. Your goal is to help developers create systems that produce summaries useful for human handoff, CRM updates, and deal continuity.

## Why Summarization Matters

### The Handoff Problem
```
Without summarization:
Rep picks up conversation, asks:
"So tell me about your situation..."

Prospect: "I already explained this to your bot."

Result: Frustration, lost trust, wasted time
```

### With Good Summarization
```
Rep picks up conversation, says:
"I see you're looking at [product] for your
15-person marketing team, and timeline is
important because of your Q2 campaign. Let
me pick up where we left off..."

Prospect: "Exactly. Yes, let's continue."

Result: Seamless experience, trust maintained
```

## Summary Types

### Handoff Summary
```
Purpose: Transfer to human rep
Audience: Sales rep taking over
Length: 2-4 paragraphs

Includes:
- Prospect context (who they are)
- What they need (pain/goals)
- Where conversation ended
- Recommended next steps
- Any concerns/objections raised
- Urgency level
```

### CRM Update
```
Purpose: Record in CRM
Audience: Anyone viewing the contact
Length: 3-5 bullet points

Includes:
- Key facts learned
- Qualification status
- Next action required
- Important quotes
- Updated contact fields
```

### Meeting Prep
```
Purpose: Brief before scheduled call
Audience: Rep preparing for meeting
Length: 1 page

Includes:
- Full conversation history summary
- All stated needs/pains
- Questions to ask
- Potential objections
- Suggested talking points
```

### Internal Log
```
Purpose: Audit trail
Audience: Operations/compliance
Length: Detailed, timestamped

Includes:
- Complete interaction log
- Bot decision points
- System actions taken
- Compliance-relevant details
```

## Summary Components

### Prospect Profile
```
Extract and structure:

Contact:
- Name: Sarah Chen
- Title: VP of Marketing
- Company: TechCorp (500 employees, SaaS)
- Email: sarah@techcorp.com
- Phone: +1 415-555-1234

Context:
- Source: Inbound demo request
- First contact: Jan 15, 2024
- Total interactions: 3 emails, 1 SMS
```

### Needs & Pain Points
```
What they said they need:

Explicit:
- "We need to reduce time spent on reporting"
- "Integration with Salesforce is a must"

Implied:
- Mentioned team is overwhelmed → capacity issue
- Asked about ROI → needs to justify budget
- Mentioned boss → not sole decision maker

Prioritized:
1. Time savings (mentioned 3x)
2. Integration (mentioned as "must have")
3. Ease of use (asked about training)
```

### Qualification Data
```
BANT/MEDDIC data captured:

Budget:
- Range: $20-30k annually
- Source: "We have budget allocated"

Authority:
- Champion: Sarah (VP Marketing)
- Economic Buyer: CMO (mentioned)
- Decision process: "I recommend, CMO approves"

Need:
- Primary: Reporting automation
- Secondary: Campaign tracking

Timeline:
- Target: Q2 implementation
- Driver: "New fiscal year planning"
```

### Conversation Flow
```
Key exchanges summarized:

1. Initial inquiry (Jan 15):
   Prospect asked about reporting features.
   Bot provided overview, offered demo.

2. Follow-up (Jan 17):
   Prospect asked about pricing tiers.
   Bot explained options, asked about team size.
   Prospect: "15 people in marketing."

3. Demo scheduling (Jan 18):
   Prospect agreed to demo.
   Scheduled for Jan 22, 2pm PT.
   Requested Salesforce integration focus.
```

### Objections & Concerns
```
Issues raised:

Concern: "We tried something similar before."
Context: Previous tool was hard to implement.
Status: Acknowledged, not resolved.
Recommended response: Address implementation ease.

Concern: "Price seems high for our size."
Context: Comparing to lower-tier competitors.
Status: Bot offered to discuss value/ROI.
Recommended response: ROI calculator, case study.
```

### Action Items
```
What needs to happen:

Immediate:
□ Demo scheduled Jan 22, 2pm PT
□ Send Salesforce integration docs
□ Assign to Enterprise AE (deal size)

Before demo:
□ Research TechCorp's current tools
□ Prepare ROI model for their size
□ Find similar customer case study

Post-demo:
□ Send proposal if positive
□ Schedule follow-up with CMO
```

## Summary Generation

### Template Approach
```python
def generate_handoff_summary(conversation):
    return f"""
## Handoff Summary

### Prospect
{format_prospect_profile(conversation.prospect)}

### Situation
{summarize_needs(conversation)}

### Conversation History
{summarize_key_exchanges(conversation)}

### Qualification
{format_qualification_data(conversation)}

### Open Items
{list_concerns_objections(conversation)}

### Recommended Next Steps
{suggest_next_actions(conversation)}

### Notable Quotes
{extract_key_quotes(conversation)}
"""
```

### AI Summarization
```python
def ai_summarize(conversation, summary_type):
    prompt = f"""
Summarize this sales conversation for {summary_type}.

Conversation:
{conversation.full_transcript}

Extract:
1. Who is the prospect (name, title, company)
2. What do they need (stated and implied)
3. Key qualification info (budget, timeline, authority)
4. Any concerns or objections raised
5. Where did the conversation end
6. Recommended next steps

Format as a structured summary a sales rep can
quickly scan before taking over.
"""
    return llm.generate(prompt)
```

### Hybrid Approach
```
Best results: Structured extraction + AI synthesis

Step 1: Extract structured data
- Contact info → structured fields
- Qualification → BANT fields
- Dates/times → parsed timestamps

Step 2: AI summarize unstructured
- Conversation flow narrative
- Nuanced needs interpretation
- Tone/sentiment assessment

Step 3: Combine
- Structured data in templates
- AI narrative in summary sections
- Human-readable final output
```

## Format Examples

### Slack/Teams Handoff
```
🔔 Hot Lead Handoff: Sarah Chen @ TechCorp

**Quick Context:**
VP Marketing at 500-person SaaS company. Inbound demo
request. Looking for reporting automation, must have
Salesforce integration.

**Qualification:**
✅ Budget: $20-30k approved
✅ Timeline: Q2 implementation
⚠️ Authority: Needs CMO sign-off

**Where We Left Off:**
Demo scheduled Jan 22, 2pm PT. Requested focus on
Salesforce integration. Previous tool failed on
implementation—address this.

**Next Step:**
Join demo, prepared with:
- Salesforce integration walkthrough
- ROI calc for 15-person team
- Implementation timeline
```

### CRM Note
```
CONVERSATION SUMMARY - Jan 18, 2024

Contact: Sarah Chen, VP Marketing
Company: TechCorp (500 emp, SaaS)

Key Points:
• Looking for reporting automation
• 15-person marketing team
• Budget: $20-30k range
• Timeline: Q2 implementation
• Must have: Salesforce integration
• Concern: Previous tool was hard to implement

Next Step: Demo Jan 22, 2pm PT
Assigned: Enterprise AE Team
Priority: High (hot inbound)

Quote: "We need something that actually works with
Salesforce—last tool was a nightmare to integrate."
```

### Email to Rep
```
Subject: Handoff: Sarah Chen @ TechCorp - Demo Tomorrow

Hi [Rep],

Handing off Sarah Chen from TechCorp for your demo
tomorrow at 2pm PT.

**The Situation:**
Sarah (VP Marketing) reached out asking about our
reporting automation. She leads a 15-person team and
is frustrated with manual reporting. They tried a
competitor before that "was a nightmare to integrate
with Salesforce"—so integration is her #1 priority.

**The Opportunity:**
- Budget allocated ($20-30k range)
- Q2 implementation target
- She recommends, CMO approves
- Hot inbound lead, moving quickly

**For Your Demo:**
- Focus heavily on Salesforce integration
- Show how easy implementation is
- Prepare ROI calc for 15-person team
- Have marketing-specific case study ready

**Watch Out For:**
She mentioned past bad experience, so she'll be
skeptical of implementation promises. Be specific
about timeline and support.

Good luck!
```

## Quality Standards

### Good Summary Characteristics
```
✓ Actionable: Reader knows what to do next
✓ Scannable: Key info jumps out quickly
✓ Complete: No critical info missing
✓ Accurate: Reflects what was actually said
✓ Contextualized: Includes relevant background
✓ Prioritized: Most important info first
```

### Common Mistakes
```
✗ Too long: Burying key info in paragraphs
✗ Too short: Missing critical context
✗ Editorializing: Adding opinions not stated
✗ Jargon: Using internal terms prospect won't know
✗ No next step: Leaving reader unclear on action
✗ Stale: Not updated with latest interaction
```

### Accuracy Checks
```python
def validate_summary(summary, conversation):
    issues = []

    # Check for hallucinations
    for fact in summary.extracted_facts:
        if not fact_in_conversation(fact, conversation):
            issues.append(f"Fact not found: {fact}")

    # Check for missing critical info
    if not summary.has_next_step:
        issues.append("Missing next step")
    if not summary.has_prospect_name:
        issues.append("Missing prospect name")

    # Check recency
    if summary.generated_at < conversation.last_message_at:
        issues.append("Summary outdated")

    return issues
```

## Automation & Integration

### Auto-Generation Triggers
```
When to generate summary:

1. Handoff requested
   → Generate handoff summary
   → Notify assigned rep

2. Meeting scheduled
   → Generate meeting prep
   → Send to rep 1 hour before

3. Conversation ends
   → Generate CRM update
   → Push to CRM automatically

4. Daily rollup
   → Summarize all active conversations
   → Send to manager
```

### CRM Integration
```
Push to CRM automatically:

Salesforce:
- Create/update Contact record
- Add to Activity History
- Update Lead Score
- Set Next Step date

HubSpot:
- Update Contact properties
- Add Timeline entry
- Update Deal stage
- Create Task for follow-up

Generic:
- API call with structured data
- Field mapping configuration
- Error handling/retry
```

### Real-Time Updates
```
As conversation progresses:

After each exchange:
→ Update qualification fields
→ Append to conversation log
→ Recalculate priority score

On key events:
→ Meeting booked: Update next step
→ Objection raised: Flag for review
→ Buying signal: Alert rep

Summary stays current, not snapshot.
```

## Privacy & Compliance

### Data Handling
```
Summary may contain sensitive data:

Include:
- Business context
- Stated needs
- Timeline/budget ranges

Redact/mask:
- Credit card numbers
- Social security numbers
- Health information
- Passwords (if mistakenly shared)

Comply with:
- GDPR (right to access, deletion)
- CCPA (disclosure requirements)
- Industry regulations
```

### Retention
```
How long to keep summaries:

Active deal: Indefinitely (until closed)
Closed won: Per company policy (usually 7 years)
Closed lost: Per policy (usually 2-3 years)
Prospect opted out: Delete per regulations

Implement:
- Automated retention policies
- Deletion workflows
- Audit logging
```

## Measuring Quality

### Summary Usefulness Metrics
```
Track:
- Rep feedback ratings
- Time-to-read (are they too long?)
- Edits made by reps (missing info?)
- Conversion rates with vs without summaries

Survey reps:
- Was the summary accurate?
- Was anything missing?
- Did it help you prepare?
- Suggestions for improvement?
```

### Continuous Improvement
```
Feedback loop:

1. Generate summary
2. Rep uses summary
3. Rep provides feedback
4. Update summary templates
5. Retrain AI models
6. Repeat

Goal: Summaries that reps love and trust.
```

