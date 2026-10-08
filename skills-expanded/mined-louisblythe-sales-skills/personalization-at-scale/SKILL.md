---
name: personalization-at-scale
description: When the user wants to build or improve a sales bot's ability to dynamically insert names, company details, and relevant context into conversations. Also use when the user mentions "dynamic personalization," "merge fields," "personalized outreach," "customizing messages at scale," or "personalization variables."
---

# Personalization at Scale for Sales Bots

You are an expert in building personalized automated sales experiences. Your goal is to help design systems that dynamically insert relevant context into conversations while maintaining scalability.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What data do you have about your prospects?
   - What channels is your bot operating on?
   - How personalized are current conversations?

2. **Current State**
   - Are you using any personalization today?
   - What data sources are available?
   - Where does personalization fall flat?

3. **Goals**
   - What would better personalization help you achieve?
   - What level of personalization is realistic?

---

## Core Principles

### 1. Personalization Should Feel Natural
- Not just inserting names
- Relevant, not creepy
- Adds value to conversation

### 2. Data Quality Determines Quality
- Bad data = bad personalization
- Missing data = fallback needed
- Wrong data = worse than generic

### 3. Tiers of Personalization
- Not everything needs deep personalization
- Match effort to opportunity value
- Scale appropriately

### 4. Test and Validate
- Personalization can backfire
- A/B test effectiveness
- Measure impact

---

## Personalization Hierarchy

### Level 1: Basic (Must-Have)

**Elements:**
- First name
- Company name
- Time-appropriate greeting

**Example:**
"Hi [Sarah], thanks for reaching out from [Acme Corp]!"

**Data required:** Contact record basics

### Level 2: Contextual (Should-Have)

**Elements:**
- Industry references
- Company size context
- Role-specific language
- Geographic relevance

**Example:**
"I see you're in [fintech]—compliance challenges are huge right now."

**Data required:** Enriched contact/company data

### Level 3: Behavioral (Nice-to-Have)

**Elements:**
- Pages viewed
- Content downloaded
- Previous interactions
- Engagement history

**Example:**
"I noticed you were looking at our pricing page. Happy to answer questions!"

**Data required:** Activity tracking, conversation history

### Level 4: Deep (High-Value Only)

**Elements:**
- Recent company news
- Specific challenges mentioned
- Competitive situation
- Personal details (appropriately)

**Example:**
"Congrats on the Series B! As you scale the sales team, [specific challenge] often comes up."

**Data required:** Research, news monitoring, CRM notes

---

## Data for Personalization

### Common Personalization Variables

| Variable | Source | Fallback |
|----------|--------|----------|
| First name | CRM, form | "there" |
| Company name | CRM, enrichment | [omit reference] |
| Industry | Enrichment | "your industry" |
| Company size | Enrichment | "your team" |
| Role/Title | CRM, LinkedIn | "your role" |
| Location | CRM, IP | [omit reference] |
| Page viewed | Analytics | [omit reference] |
| Previous interaction | CRM | "your interest" |

### Data Sources

**CRM:**
- Contact information
- Company information
- Interaction history
- Notes and context

**Enrichment providers:**
- Clearbit, ZoomInfo, etc.
- Firmographics
- Technographics
- Intent signals

**Behavioral tracking:**
- Website activity
- Email engagement
- Content downloads
- Form submissions

**External sources:**
- News APIs
- LinkedIn
- Social media
- Industry databases

---

## Implementing Personalization

### Template Design

**Basic template with variables:**
```
Hi {{first_name | default:"there"}},

{{#if company_name}}
Thanks for reaching out from {{company_name}}.
{{else}}
Thanks for reaching out.
{{/if}}

{{#if viewed_pricing}}
I noticed you were checking out our pricing. Happy to walk through options!
{{else}}
What brings you here today?
{{/if}}
```

### Conditional Logic

**If/else blocks:**
```
{{#if industry == "fintech"}}
Compliance is a big topic in fintech right now.
{{else if industry == "healthcare"}}
HIPAA requirements make this especially important.
{{else}}
[Generic industry-agnostic content]
{{/if}}
```

**Company size adaptation:**
```
{{#if employee_count > 500}}
[Enterprise-focused messaging]
{{else if employee_count > 50}}
[Mid-market messaging]
{{else}}
[SMB messaging]
{{/if}}
```

### Fallback Strategy

**Always have fallbacks:**
```
// Good
"Hi {{first_name | default:'there'}}, ..."

// Bad
"Hi {{first_name}}, ..." // Breaks if missing
```

**Graceful degradation:**
1. Try specific personalization
2. Fall back to category-level
3. Fall back to generic

---

## Personalization by Channel

### SMS

**Keep it brief:**
"Hi {{first_name}}, quick question about {{company_name}}'s approach to [topic]. Worth a chat?"

**Be careful:**
- Character limits
- Less context expected
- Can feel intrusive if overdone

### Email

**More room for personalization:**
- Subject line: "{{first_name}}, question about {{company_name}}'s [area]"
- Opening reference to specific trigger
- Role/industry-specific content
- Relevant case study

### Chat

**Dynamic, conversational:**
"I see you're from {{company_name}}—we work with a lot of [similar companies/industry]. What brings you here today?"

**Behavioral context:**
"Noticed you were on our [specific page]. Looking for [inferred need]?"

### Voice

**Natural integration:**
"Hi, is this [first name]? I'm calling from [company] about your interest in [specific topic]."

---

## Avoiding Personalization Pitfalls

### The Creepy Line

**Too much:**
"Hi Sarah, I see you were on our pricing page at 3:47pm yesterday, right after visiting Competitor's site. Your company's revenue growth of 34% suggests you're ready to invest..."

**Just right:**
"Hi Sarah, I noticed you were exploring our pricing. Happy to answer any questions!"

### Data Errors

**Misspelled names:**
- Validate data quality
- Have human review flagged issues
- Better generic than wrong

**Outdated information:**
- "Congrats on joining [old company]!" → Bad
- Validate recency of data

**Wrong industry/size:**
- Don't assume enrichment is right
- Use softer language when uncertain
- "Companies like yours" vs. "In fintech"

### Over-Personalization

**When it backfires:**
- Every sentence personalized → Feels like surveillance
- Irrelevant personalization → Shows you don't understand them
- Forced personalization → Feels unnatural

---

## Measuring Personalization Impact

### A/B Testing

**Test:**
- Personalized vs. generic
- Different personalization levels
- Different variables

**Measure:**
- Response rates
- Sentiment
- Conversion
- Opt-out rates

### Metrics to Track

**Engagement:**
- Open rates (email)
- Response rates
- Conversation length
- Sentiment

**Quality:**
- Personalization error rate
- Fallback frequency
- Negative reactions

**Business:**
- Conversion by personalization level
- Revenue per contact
- Cost of personalization vs. return

---

## Building Personalization Systems

### Architecture

```
[Data Sources] → [Data Pipeline] → [Personalization Engine] → [Channel Delivery]
                       ↓
              [Unified Contact Profile]
```

### Components

**Data pipeline:**
- Ingest from sources
- Clean and validate
- Merge duplicates
- Update profiles

**Personalization engine:**
- Template management
- Variable resolution
- Fallback handling
- A/B test management

**Delivery system:**
- Channel-specific formatting
- Rate limiting
- Compliance checking
- Logging

### Data Model

```
Contact Profile:
  - identity (name, email, phone)
  - company (name, industry, size)
  - behavioral (pages viewed, emails opened)
  - conversational (past interactions, objections, interests)
  - personalization_preferences (channels, frequency)
```

---

## Scale Considerations

### High Volume Operations

**Challenges:**
- Data lookup latency
- Template rendering speed
- Error rate at scale
- Monitoring complexity

**Solutions:**
- Cache frequently used data
- Pre-compute where possible
- Robust error handling
- Sampling-based monitoring

### Quality at Scale

**Maintain quality:**
- Automated data validation
- Error alerting
- Regular audits
- Feedback loops

---

## Questions to Ask

If you need more context:
1. What data do you have on your prospects?
2. What personalization are you doing today?
3. What channels are you personalizing for?
4. What's your volume of outreach?
5. Where has personalization gone wrong before?

---

## Related Skills

- **lead-qualification-logic**: For collecting personalization data
- **conversation-memory**: For using conversation context
- **data-enrichment-integration**: For enhancing contact data
- **tone-matching**: For adapting style to prospect
