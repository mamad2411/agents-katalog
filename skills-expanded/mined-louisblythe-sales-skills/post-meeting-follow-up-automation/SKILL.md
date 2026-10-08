---
name: post-meeting-follow-up-automation
description: When the user wants to build or improve a sales bot's ability to send relevant materials after meetings. Also use when the user mentions "post-meeting follow-up," "meeting recap," "call follow-up," "meeting materials," or "after-meeting automation."
---

# Post-Meeting Follow-Up Automation

You are an expert in building sales bots that send relevant follow-up materials based on what was discussed in meetings. Your goal is to help developers create systems that automatically follow up with personalized content after calls and demos.

## Why Post-Meeting Follow-Up Matters

### The Follow-Up Gap
```
What usually happens:
- Meeting ends
- Rep has 3 more meetings
- "I'll send that over" becomes days later
- Prospect forgets details
- Momentum lost

Missed follow-up = missed opportunity
```

### Automated Follow-Up
```
What should happen:
- Meeting ends
- Bot sends recap within 1 hour
- Relevant materials attached
- Next steps confirmed
- Prospect impressed by speed
- Momentum maintained
```

## Meeting Data Capture

### Information to Capture
```
During or immediately after meeting:

1. Topics discussed
   - Pain points mentioned
   - Features requested
   - Questions asked

2. Stakeholders mentioned
   - Other decision makers
   - Team members to include
   - Approval chain

3. Objections raised
   - Pricing concerns
   - Technical questions
   - Competitor mentions

4. Next steps agreed
   - Follow-up meeting
   - Trial/POC
   - Proposal requested

5. Materials requested
   - Case studies
   - Technical docs
   - Pricing info
```

### Capture Methods
```python
# Manual input (rep fills form)
meeting_notes = {
    "topics": ["integration", "pricing", "support"],
    "materials_requested": ["api_docs", "case_study_saas"],
    "next_steps": "send_proposal",
    "key_concerns": ["implementation_time", "data_migration"],
    "stakeholders_mentioned": ["cto", "finance"]
}

# AI transcription analysis (if recorded)
analyzed_meeting = analyze_transcript(transcript)
"""
Extracts:
- Key topics by frequency and context
- Questions asked (potential follow-up items)
- Commitments made ("I'll send you...")
- Objections detected
- Next steps mentioned
"""

# Integration with meeting tools
# Pull from Gong, Chorus, Zoom AI, etc.
```

## Follow-Up Sequences

### Immediate Follow-Up (Within 1 Hour)
```
Subject: Great talking with you - Materials enclosed

"Hi [Name],

Great connecting today! As promised, here's what
we discussed:

**Key Points:**
• [Topic 1 summary]
• [Topic 2 summary]

**Requested Materials:**
• [Material 1] - [link]
• [Material 2] - [link]

**Next Steps:**
• [Action item with owner]
• [Scheduled follow-up if applicable]

Any questions before [next step]?

[Rep name]"

Speed + organization = professionalism
```

### 24-Hour Value Add
```
Subject: Thought this would help

"Hi [Name],

Following up on our conversation about [topic].

I found this [case study/article/resource] that
directly addresses [their specific concern].

[Brief summary of why it's relevant]

Worth a look before we connect again on [date].

[Rep name]"

Add value, don't just "check in."
```

### Pre-Next-Meeting Follow-Up
```
If next meeting scheduled, 24 hours before:

"Looking forward to continuing our conversation
tomorrow.

Based on what we discussed last time, I've
prepared [specific materials/demo] focused on
[their key interest].

Anything specific you'd like me to cover?"

Show preparation and attentiveness.
```

## Content Matching

### Material Selection Logic
```python
def select_follow_up_materials(meeting_data):
    materials = []

    # Match by topic discussed
    for topic in meeting_data.topics:
        if topic == "integration":
            materials.append("integration_guide")
        elif topic == "security":
            materials.append("soc2_report")
            materials.append("security_whitepaper")
        elif topic == "roi":
            materials.append("roi_calculator")

    # Match by industry
    industry_case_study = find_case_study(
        industry=meeting_data.prospect.industry,
        company_size=meeting_data.prospect.company_size
    )
    if industry_case_study:
        materials.append(industry_case_study)

    # Match by objection
    for objection in meeting_data.objections:
        objection_content = get_objection_response_content(objection)
        if objection_content:
            materials.append(objection_content)

    # Dedupe and prioritize
    return prioritize_materials(materials, max_count=3)
```

### Content Personalization
```python
def personalize_material_description(material, prospect):
    templates = {
        "case_study": f"Case study from {material.company_name}, "
                      f"a {material.industry} company similar to yours "
                      f"that saw {material.key_result}",

        "roi_calculator": f"ROI calculator pre-filled with "
                          f"{prospect.company_name}'s metrics from our call",

        "integration_guide": f"Integration guide for connecting with "
                             f"{prospect.tech_stack} (based on what you mentioned)",
    }

    return templates.get(material.type, material.default_description)
```

## Meeting Type-Specific Follow-Ups

### Discovery Call Follow-Up
```
Focus: Understanding confirmed, value teased

"Thanks for sharing about [their situation].

Based on what you described, I think we can
help with:
1. [Pain point → solution mapping]
2. [Pain point → solution mapping]

For our next conversation, I'd love to show
you [specific capability]. Would [proposed time]
work for a demo?"

Advance to next stage.
```

### Demo Follow-Up
```
Focus: Recap features, address questions

"Great demo today! Recap of what we covered:

**Features Relevant to Your Team:**
• [Feature 1] - addresses [their use case]
• [Feature 2] - solves [their problem]

**Your Questions:**
• [Question 1]: [Answer with link to more info]
• [Question 2]: [Answer with link to more info]

**Next Steps:**
• [Proposal/trial/next meeting]

What other questions came up after our call?"
```

### Proposal Review Follow-Up
```
Focus: Clarify terms, remove blockers

"Thanks for reviewing the proposal with me.

**Summary:**
• Investment: [Amount]
• Timeline: [Implementation duration]
• Includes: [Key items]

**Open Items:**
• [Any unresolved questions]

I've attached the formal proposal document.
Let me know if you need anything adjusted
before presenting to [their team/boss]."
```

## Automated vs Manual Balance

### Fully Automated Elements
```
Can be automated:
- Meeting recap email structure
- Standard material attachment
- Calendar invite for next step
- Basic personalization (name, company)
- Timing of send

"Send recap email with [selected materials]
within 1 hour of meeting end."
```

### Human-in-the-Loop Elements
```
Should involve human:
- Summary of specific discussion points
- Custom answers to questions
- Pricing exceptions
- Unique concerns addressed
- Relationship-specific notes

"Draft prepared for rep review. Rep can edit
and approve before sending."
```

### Hybrid Workflow
```python
def generate_follow_up(meeting_data):
    # Auto-generate structure
    email = FollowUpEmail()
    email.greeting = generate_greeting(meeting_data.prospect)
    email.materials = select_follow_up_materials(meeting_data)
    email.next_steps = format_next_steps(meeting_data.next_steps)

    # Flag sections needing human input
    email.summary = "[REP TO COMPLETE: Key discussion points]"
    email.custom_notes = "[REP TO COMPLETE: Any personal notes]"

    # Queue for review if manual elements present
    if meeting_data.has_custom_questions:
        return queue_for_review(email, priority="high")
    else:
        return queue_for_send(email, delay=timedelta(hours=1))
```

## CRM Integration

### Auto-Update Records
```
After meeting follow-up sent:

1. Log activity
   - Meeting completed
   - Follow-up sent
   - Materials shared

2. Update deal stage
   - Discovery → Demo
   - Demo → Proposal
   - Proposal → Negotiation

3. Create tasks
   - Follow-up on materials in X days
   - Prep for next meeting

4. Update contact info
   - Topics of interest
   - Materials received
   - Engagement score
```

### Material Tracking
```
Track engagement with sent materials:

- Did they open the email?
- Did they click the links?
- How long on case study?
- Did they download proposal?
- Did they share with others?

Use to prioritize follow-ups:
"I noticed you spent time on the security
whitepaper. Any questions about our security
practices?"
```

## Timing Optimization

### When to Send
```
Immediate (within 1 hour):
- Meeting recap
- Requested materials
- Calendar invites

Same day (within 4 hours):
- More detailed follow-up
- Answers to questions that needed research

24-48 hours:
- Value-add content
- Prep for next meeting
- Gentle nudge if no response to recap

Never:
- Late night their time
- Weekends (unless they requested urgency)
- Multiple follow-ups same day
```

### Follow-Up Cadence
```
Day 0: Meeting recap (1 hour after)
Day 1: Value-add if no response (optional)
Day 3: Check-in if no engagement
Day 7: Re-engage with new angle

Don't:
- Send same content twice
- "Just checking in" messages
- Ignore their engagement signals
```

## Template Library

### Meeting Recap Template
```
Subject: [Company Name] + [Your Company] - Meeting Recap

Hi [Name],

Thanks for taking the time to connect today!

**What We Covered:**
[AI-generated or rep-provided summary]

**Materials:**
[Dynamically selected based on discussion]

**Next Steps:**
[Agreed upon actions with dates]

Questions? Just reply here.

Best,
[Rep Name]
```

### Material Share Template
```
Subject: [Specific Material] for [Company Name]

Hi [Name],

As discussed, here's the [material type] you requested:

[Material link with context]

This is particularly relevant for your [specific situation]
because [personalized reason].

Let me know if you have questions.

[Rep Name]
```

## Metrics

### Follow-Up Effectiveness
```
Track:
- Time to follow-up (faster = better)
- Email open rate
- Material engagement rate
- Response rate to follow-up
- Deal progression after follow-up

Optimize:
- Which materials drive engagement?
- What timing gets best response?
- What personalization matters?
```

### Pipeline Impact
```
Measure:
- Deals that received timely follow-up vs not
- Stage conversion rates
- Time in stage
- Close rates

Correlate follow-up quality with outcomes.
```

