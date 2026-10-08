---
name: attachment-media-handling
description: When the user wants to build or improve a sales bot's ability to send brochures, videos, floorplans, or other media contextually during conversations. Also use when the user mentions "sending attachments," "media sharing," "document delivery," "sending brochures," or "content delivery."
---

# Attachment & Media Handling

You are an expert in building contextual media delivery for sales bots. Your goal is to help developers create systems that send the right content at the right moment in conversations.

## Content Types & Use Cases

### Documents
```
Brochures/One-pagers:
- Initial interest → Overview brochure
- Specific feature inquiry → Feature sheet
- Executive audience → Executive summary

Proposals/Quotes:
- Post-qualification → Custom proposal
- Pricing request → Formal quote
- Budget approval → Investment summary

Technical Docs:
- Integration questions → API documentation
- Security concerns → Security whitepaper
- Implementation → Setup guides
```

### Media
```
Videos:
- Product overview (2-3 min demo)
- Feature deep-dives
- Customer testimonials
- How-to tutorials
- CEO/founder message

Images:
- Product screenshots
- Comparison charts
- Infographics
- Before/after examples

Interactive:
- ROI calculators
- Product configurators
- Assessment tools
```

## Contextual Triggering

### Conversation-Based Triggers
```
Trigger: Question about specific feature

Prospect: "Does it integrate with Salesforce?"

Bot: "Yes! We have a native Salesforce integration.
Here's a quick video showing how it works: [link]

Would you like me to send the technical documentation
for your team to review?"
```

### Intent-Based Delivery
```
Intent: Comparing options

"I'm trying to figure out which solution is right for us"

Bot: "I have a comparison guide that might help. It shows
how we stack up on the features that matter most.
[Comparison PDF]

Any specific areas you want me to highlight?"
```

### Stage-Based Content
```
Awareness stage:
- Overview video
- High-level brochure
- Blog posts/thought leadership

Consideration stage:
- Feature comparison
- Case studies
- ROI calculator

Decision stage:
- Detailed proposal
- Implementation guide
- Contract/terms
- Customer references
```

## Delivery Best Practices

### Channel-Appropriate Formats

**Email**
```
Best for:
- PDFs and documents
- Long-form content
- Multiple attachments
- Formal proposals

"I've attached our proposal and implementation timeline.
Let me know if you'd like to walk through it together."
```

**SMS/Chat**
```
Best for:
- Short videos (<2 min)
- Single links
- Quick references
- Mobile-friendly content

"Here's a 90-second video showing exactly how that works: [link]"

Avoid:
- Large file attachments
- Multiple links
- Complex documents
```

### Timing Considerations
```
Send content when:
✓ They asked for it
✓ It directly answers their question
✓ Natural pause in conversation
✓ Moving to next stage

Don't send:
✗ Unsolicited dumps of materials
✗ In the middle of active exchange
✗ Before understanding their needs
✗ When they're clearly on mobile
```

## Content Personalization

### Dynamic Content
```
Customize based on:
- Industry (industry-specific case study)
- Company size (SMB vs Enterprise pricing)
- Role (technical vs executive view)
- Use case (their specific application)
- Stage (awareness vs decision content)
```

### Personalized Elements
```
"Here's a proposal customized for [Company Name].
I've included:
- Pricing for your team of [number]
- The [Industry] case study you asked about
- Implementation timeline based on your Q2 goal"
```

### Smart Recommendations
```
Based on similar prospects:

"Prospects in [industry] often find these helpful:
1. [Industry] Case Study
2. ROI Calculator
3. Integration Guide

Want me to send any of these?"
```

## Technical Implementation

### Content Library Structure
```
content_library/
├── brochures/
│   ├── product-overview.pdf
│   ├── enterprise-overview.pdf
│   └── industry/
│       ├── healthcare.pdf
│       ├── fintech.pdf
│       └── retail.pdf
├── videos/
│   ├── demo-overview.mp4
│   ├── features/
│   │   ├── reporting.mp4
│   │   └── integrations.mp4
│   └── testimonials/
├── case-studies/
├── proposals/
│   └── templates/
└── technical/
    ├── api-docs.pdf
    └── security-whitepaper.pdf
```

### Content Selection Logic
```python
def select_content(context):
    # Based on conversation context
    if context.question_about == "integrations":
        return get_content("integrations", context.specific_tool)

    if context.stage == "decision" and context.role == "executive":
        return get_content("executive-summary", context.industry)

    if context.objection == "security":
        return get_content("security-whitepaper")

    # Based on similar successful conversations
    return recommend_by_similarity(context)
```

### Delivery Tracking
```
Track:
- Content sent (what, when, to whom)
- Delivery confirmation
- Open/view events
- Time spent viewing
- Downloads
- Shares/forwards

Use signals:
- Viewed proposal → Follow up on it
- Watched full video → Higher intent
- Didn't open → Resend or call attention
```

## Handling Media in Conversations

### Pre-Send Framing
```
Don't just drop links. Frame the content:

"Before I send this over—this is a 3-minute video showing
[specific thing]. It'll give you a better picture of
[what they asked about]. Want me to send it?"

Why:
- Sets expectations
- Gets permission
- Increases likelihood they'll view it
```

### Post-Send Follow-Up
```
After sending:

Immediate:
"Just sent that over. Let me know if you have trouble
accessing it or want me to walk you through it live."

Follow-up (if no response):
"Did you get a chance to check out the [content]?
Happy to highlight the most relevant parts if helpful."

Based on engagement:
"I saw you spent some time with the proposal—any
questions I can answer?"
```

### Handling Access Issues
```
"I can't open the attachment"

Options:
1. Resend with different format
2. Share via different channel
3. Provide web-hosted link
4. Walk through live on call

"No problem! Here's a web link instead: [link]
Can you try that? If still an issue, I can walk you
through it on a quick call."
```

## Content Recommendations

### Ask Before Overwhelming
```
"I have several resources that might help:
- Product demo video (3 min)
- Feature comparison guide
- Customer case study

Which would be most useful right now?"
```

### Package Appropriately
```
Early stage:
Send one thing, gauge interest

Late stage:
Bundle related materials
"Here's your proposal package:
- Pricing proposal
- Implementation timeline
- Security documentation
- Customer references"
```

### Channel-Specific Packaging
```
Email: Can include multiple attachments
SMS: One link at a time
Chat: Mix of inline and links
```

## Quality Management

### Content Freshness
```
Track content age:
- Last updated date
- Review schedule
- Deprecation flags

Alert when:
- Content over 6 months old
- Pricing outdated
- Statistics stale
- Screenshots don't match product
```

### Performance Metrics
```
By content piece:
- Send frequency
- Open/view rate
- Time spent
- Correlation with advancement
- Correlation with close rate

Optimize:
- Promote high-performing content
- Update or retire underperforming
- A/B test variations
```
