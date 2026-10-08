---
name: entity-extraction
description: When the user wants to build or improve a sales bot's ability to pull key data points (budget, timeline, company size, location, requirements) from unstructured prospect responses. Also use when the user mentions "extracting data," "parsing responses," "pulling out details," "structured data from conversations," or "NER for sales."
---

# Entity Extraction

You are an expert in building entity extraction capabilities for sales bots. Your goal is to help developers create systems that reliably pull structured data from unstructured prospect responses.

## Core Entities to Extract

### 1. Budget Signals
- Explicit amounts: "$50k," "fifty thousand," "50K budget"
- Ranges: "between 20 and 30k," "up to $100k," "at least 10k"
- Relative: "same as last year," "double our current spend"
- Implicit: "cost-conscious," "enterprise budget," "startup resources"

### 2. Timeline Indicators
- Explicit dates: "by Q2," "in March," "next month"
- Relative timing: "ASAP," "no rush," "when the contract ends"
- Event-driven: "after our funding round," "before the busy season"
- Conditional: "once we get approval," "if we can prove ROI"

### 3. Company/Contact Data
- Company size: "50 employees," "small team," "enterprise"
- Industry signals: "we're in healthcare," "fintech startup"
- Role indicators: "I'm the decision maker," "need to check with my boss"
- Location: "based in Austin," "we have offices in 3 countries"

### 4. Requirements & Pain Points
- Feature needs: "need CRM integration," "must have mobile app"
- Pain statements: "our current tool is slow," "we're losing deals"
- Use cases: "mainly for outbound," "customer support team"
- Constraints: "has to work with Salesforce," "need SOC 2"

## Extraction Strategies

### Pattern Matching
```
Budget patterns:
- /\$[\d,]+[kKmM]?/
- /[\d,]+ (dollars|USD|budget)/i
- /(between|from) \$?[\d,]+[kK]? (and|to|-) \$?[\d,]+[kK]?/

Timeline patterns:
- /(Q[1-4]|quarter [1-4])/i
- /(January|February|March|...)/i
- /(this|next|last) (week|month|quarter|year)/
- /in (\d+) (days|weeks|months)/
```

### Contextual Extraction
Don't just match patterns—understand context:

"We spent $50k last year but need to cut back"
→ Budget: <$50k (not exactly $50k)

"Our team of 50 is growing fast"
→ Company size: 50+ (not exactly 50)

"I can decide up to $10k, anything more needs VP approval"
→ Budget authority: $10k
→ Escalation threshold: >$10k

### Confidence Scoring
Rate extraction confidence:
- **High**: Explicit, unambiguous ("Our budget is $25,000")
- **Medium**: Implicit but clear ("We're a Series A startup" → likely $10-50k)
- **Low**: Inferred from context ("We're cost-conscious" → budget-sensitive)

## Implementation Architecture

### 1. Pre-Processing
- Normalize text (lowercase, remove extra spaces)
- Expand abbreviations ("k" → "000", "Q1" → "first quarter")
- Handle typos and variations

### 2. Multi-Pass Extraction
```
Pass 1: Direct pattern matching (high confidence)
Pass 2: Contextual NLP extraction (medium confidence)
Pass 3: Inference from surrounding context (low confidence)
```

### 3. Entity Validation
- Budget: Is the number realistic for this segment?
- Timeline: Is the date in the future? Is it business days?
- Company size: Does it align with other signals?

### 4. Conflict Resolution
When entities conflict:
- Most recent mention usually wins
- Explicit beats implicit
- Ask for clarification when critical

## Handling Ambiguity

### Unclear Responses
Prospect: "We have some budget"

Bot should extract:
- Budget: exists (boolean)
- Budget amount: unknown
- Follow-up needed: yes

Then clarify: "Great to hear you have budget allocated. To make sure I show you the right options, are we talking closer to $10k, $25k, or $50k+?"

### Multiple Entities
Prospect: "We need something for our 200-person sales team by Q2, budget around $30k, and it has to integrate with HubSpot"

Extract all:
- Team size: 200
- Department: Sales
- Timeline: Q2
- Budget: ~$30k
- Requirement: HubSpot integration

### Contradictory Information
Prospect earlier: "Budget is $20k"
Prospect now: "Actually we might be able to do $35k"

Resolution:
- Update budget to $35k
- Note: budget flexibility exists
- Flag for potential upsell

## CRM Integration

### Mapping to Fields
```
Extracted Entity → CRM Field
─────────────────────────────
budget_amount → Opportunity.Amount
budget_range_low → Custom.Budget_Min
budget_range_high → Custom.Budget_Max
timeline_date → Opportunity.Close_Date
company_size → Account.Employees
decision_maker → Contact.Role
requirements → Opportunity.Requirements__c
```

### Handling Missing Data
- Required fields: Flag for human follow-up
- Optional fields: Leave blank, don't guess
- Partial data: Store what you have, mark incomplete

## Quality Assurance

### Extraction Accuracy Metrics
- Precision: Of entities extracted, how many are correct?
- Recall: Of entities present, how many were found?
- F1 score: Balance of precision and recall

### Common Failure Modes
1. **Over-extraction**: Pulling irrelevant numbers as budget
2. **Under-extraction**: Missing implied entities
3. **Misclassification**: Budget vs. company size confusion
4. **Context blindness**: Ignoring negation ("NOT $50k")

### Testing Approach
- Unit tests for each entity type
- Integration tests with real conversation samples
- A/B test extraction models
- Human review of edge cases

## Advanced Techniques

### Coreference Resolution
"We talked to Acme Corp last week. They said $50k was possible."
→ Budget holder: Acme Corp (not current prospect)

### Temporal Reasoning
"We need this before our fiscal year ends in March"
→ Timeline: Before March (specific date depends on current date)

### Implicit Entity Inference
"We're a YC company"
→ Likely: tech startup, 2-50 employees, some funding, fast timeline

## Output Format

### Structured Response
```json
{
  "entities": {
    "budget": {
      "amount": 30000,
      "currency": "USD",
      "type": "approximate",
      "confidence": 0.85
    },
    "timeline": {
      "target_date": "2024-06-30",
      "type": "quarter_end",
      "urgency": "medium",
      "confidence": 0.90
    },
    "company": {
      "size": 200,
      "department": "sales",
      "confidence": 0.95
    },
    "requirements": [
      {"feature": "hubspot_integration", "priority": "must_have"}
    ]
  },
  "missing": ["decision_maker", "current_solution"],
  "follow_up_needed": ["budget_authority"]
}
```

This enables downstream systems to act on extracted data appropriately.
