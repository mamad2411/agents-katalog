---
name: custom-field-population
description: When the user wants to build or improve a sales bot's ability to automatically update CRM fields from conversations. Also use when the user mentions "CRM automation," "field population," "data entry automation," "conversation to CRM," or "auto-fill fields."
---

# Custom Field Population

You are an expert in building sales bots that automatically update CRM fields from conversation data. Your goal is to help developers create systems that eliminate manual data entry by extracting and populating fields from natural language conversations.

## Why Automation Matters

### The Manual Entry Problem
```
After every conversation:
- Rep opens CRM
- Types notes
- Updates 10+ fields
- Often forgets or skips
- Data quality suffers

Time wasted: 30-60 minutes/day
Data accuracy: 50-70%
```

### With Auto-Population
```
During/after conversation:
- Bot extracts key data
- Fields update automatically
- Rep reviews/confirms
- Data always current

Time saved: 25-50 minutes/day
Data accuracy: 90%+
```

## Field Extraction

### Contact Information
```
Extract from conversation:

"My email is john.smith@company.com"
→ email: john.smith@company.com

"Best number is 415-555-1234"
→ phone: +14155551234

"I'm the VP of Marketing"
→ title: VP of Marketing

"We're based in San Francisco"
→ city: San Francisco, state: CA

"We have about 500 employees"
→ company_size: 500

Pattern matching + NER for extraction.
```

### Qualification Data (BANT)
```
Budget extraction:
"We've allocated around $50k for this"
→ budget: 50000, budget_currency: USD

"Budget isn't approved yet"
→ budget_status: not_approved

Authority extraction:
"I make the final call on this"
→ decision_maker: true

"I'll need to run this by my CEO"
→ decision_maker: false, economic_buyer: CEO

Need extraction:
"Our main problem is lead conversion"
→ primary_need: lead_conversion

Timeline extraction:
"We want to implement by Q2"
→ target_timeline: Q2, urgency: medium

"This is urgent, need it next month"
→ target_timeline: next_month, urgency: high
```

### Opportunity Data
```
Product interest:
"We're looking at your enterprise plan"
→ product_interest: enterprise

"Specifically interested in analytics"
→ features_of_interest: [analytics]

Deal size signals:
"We'd need licenses for 100 users"
→ estimated_users: 100
→ estimated_deal_size: 100 * price_per_user

Stage indicators:
"We're just researching right now"
→ stage: research

"Ready to see a proposal"
→ stage: proposal_requested
```

### Engagement Data
```
Preferences:
"Email works best for me"
→ preferred_channel: email

"I'm usually free mornings"
→ preferred_time: morning

"Don't call my cell"
→ contact_preference: no_cell_calls

Relationships:
"Talk to Sarah, she handles vendor selection"
→ additional_contact: Sarah, role: vendor_selection

"Our IT team will need to review"
→ stakeholders: [IT team]
```

## Extraction Implementation

### Rule-Based Extraction
```python
EXTRACTION_RULES = {
    "email": {
        "patterns": [
            r"[\w\.-]+@[\w\.-]+\.\w+",
            r"email is ([\w\.-]+@[\w\.-]+\.\w+)",
            r"reach me at ([\w\.-]+@[\w\.-]+\.\w+)"
        ],
        "field": "email",
        "validation": validate_email
    },
    "phone": {
        "patterns": [
            r"\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}",
            r"call me at ([\d\s\-\(\)]+)",
            r"number is ([\d\s\-\(\)]+)"
        ],
        "field": "phone",
        "validation": validate_phone,
        "transform": normalize_phone
    },
    "company_size": {
        "patterns": [
            r"(\d+)\s*employees",
            r"team of (\d+)",
            r"about (\d+) people",
            r"(\d+)-person company"
        ],
        "field": "company_size",
        "transform": int
    },
    "budget": {
        "patterns": [
            r"\$(\d+[,\d]*)\s*(k|K|thousand|million|M)?",
            r"budget.*?(\d+[,\d]*)\s*(k|K|thousand|million|M)?",
            r"allocated.*?(\d+[,\d]*)\s*(k|K|thousand|million|M)?"
        ],
        "field": "budget",
        "transform": parse_currency
    }
}

def extract_field(text, field_config):
    for pattern in field_config["patterns"]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1) if match.groups() else match.group()
            if "transform" in field_config:
                value = field_config["transform"](value)
            if "validation" in field_config:
                if not field_config["validation"](value):
                    continue
            return value
    return None
```

### NLP-Based Extraction
```python
def extract_with_nlp(text, field_type):
    # Use NER for entity extraction
    entities = ner_model.extract(text)

    # Use intent classification for context
    intent = classify_intent(text)

    # Combine for extraction
    if field_type == "budget":
        money_entities = [e for e in entities if e.type == "MONEY"]
        if money_entities and intent in ["budget_discussion", "pricing"]:
            return money_entities[0].value

    if field_type == "timeline":
        date_entities = [e for e in entities if e.type == "DATE"]
        if date_entities and intent in ["timeline_discussion", "urgency"]:
            return parse_timeline(date_entities[0].value)

    return None
```

### LLM-Based Extraction
```python
def extract_with_llm(conversation, fields_needed):
    prompt = f"""
    Extract the following information from this conversation:
    {fields_needed}

    Conversation:
    {conversation}

    Return as JSON with extracted values. Use null for any
    fields not mentioned. Include confidence score (0-1).
    """

    response = llm.generate(prompt)
    extracted = json.loads(response)

    return extracted

# Example output:
{
    "budget": {"value": 50000, "confidence": 0.9},
    "timeline": {"value": "Q2 2024", "confidence": 0.85},
    "decision_maker": {"value": false, "confidence": 0.7},
    "company_size": {"value": 500, "confidence": 0.95}
}
```

## CRM Integration

### Field Mapping
```python
CRM_FIELD_MAPPING = {
    # Contact fields
    "email": "Contact.Email",
    "phone": "Contact.Phone",
    "title": "Contact.Title",
    "preferred_channel": "Contact.Preferred_Channel__c",

    # Account fields
    "company_size": "Account.NumberOfEmployees",
    "industry": "Account.Industry",
    "city": "Account.BillingCity",
    "state": "Account.BillingState",

    # Opportunity fields
    "budget": "Opportunity.Amount",
    "target_timeline": "Opportunity.CloseDate",
    "stage": "Opportunity.StageName",
    "product_interest": "Opportunity.Product_Interest__c",

    # Custom fields
    "primary_need": "Opportunity.Primary_Pain_Point__c",
    "decision_maker": "Contact.Is_Decision_Maker__c",
    "urgency": "Opportunity.Urgency__c"
}
```

### Update Logic
```python
def update_crm(extracted_data, record_id, crm_client):
    updates = {}

    for field, value_data in extracted_data.items():
        # Check confidence threshold
        if value_data["confidence"] < 0.7:
            continue  # Skip low-confidence extractions

        # Get CRM field name
        crm_field = CRM_FIELD_MAPPING.get(field)
        if not crm_field:
            continue

        # Check if update is appropriate
        current_value = crm_client.get_field(record_id, crm_field)
        if should_update(current_value, value_data["value"]):
            updates[crm_field] = value_data["value"]

    # Apply updates
    if updates:
        crm_client.update(record_id, updates)
        log_updates(record_id, updates, extracted_data)

    return updates

def should_update(current, new):
    # Don't overwrite with null
    if new is None:
        return False

    # Don't overwrite non-null with different value (require confirmation)
    if current is not None and current != new:
        return False  # Or queue for review

    return True
```

### Batch Processing
```python
def process_conversation_for_crm(conversation):
    # Extract all fields
    extracted = {}

    for message in conversation.messages:
        if message.sender == "prospect":
            message_extractions = extract_all_fields(message.text)
            for field, data in message_extractions.items():
                # Keep highest confidence extraction
                if field not in extracted or data["confidence"] > extracted[field]["confidence"]:
                    extracted[field] = data

    # Validate and clean
    validated = validate_extractions(extracted)

    # Update CRM
    updates = update_crm(
        validated,
        conversation.prospect_id,
        crm_client
    )

    return updates
```

## Human Review

### Review Queue
```
When to queue for review:
- Low confidence (<70%)
- Conflicting extractions
- Significant value change
- Critical fields (budget, close date)

Review interface:
"Extracted: Budget = $50,000 (85% confidence)
From: 'We've set aside around $50k for this project'
Current value: [blank]
[Approve] [Edit] [Reject]"
```

### Confidence Thresholds
```python
CONFIDENCE_THRESHOLDS = {
    # Auto-update
    "high": {
        "threshold": 0.9,
        "action": "auto_update"
    },
    # Update but notify
    "medium": {
        "threshold": 0.7,
        "action": "update_and_notify"
    },
    # Queue for review
    "low": {
        "threshold": 0.5,
        "action": "queue_for_review"
    },
    # Discard
    "very_low": {
        "threshold": 0.0,
        "action": "discard"
    }
}
```

### Feedback Loop
```python
def record_feedback(extraction_id, approved, corrected_value=None):
    # Log the feedback
    feedback = {
        "extraction_id": extraction_id,
        "approved": approved,
        "corrected_value": corrected_value,
        "timestamp": datetime.now()
    }

    # Use for model improvement
    if not approved:
        add_to_training_data(
            original=get_extraction(extraction_id),
            corrected=corrected_value
        )

    # Update extraction rules if pattern failing
    if not approved:
        increment_failure_count(extraction_id)
        if should_disable_rule(extraction_id):
            disable_extraction_rule(extraction_id)
```

## Field-Specific Handling

### Date/Timeline Fields
```python
def parse_timeline(text):
    # Relative dates
    relative_patterns = {
        r"next month": lambda: today() + timedelta(days=30),
        r"next quarter|Q[1-4]": parse_quarter,
        r"end of year": lambda: date(today().year, 12, 31),
        r"(\d+) (days|weeks|months)": parse_relative_duration
    }

    for pattern, handler in relative_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            return handler()

    # Absolute dates
    parsed = dateparser.parse(text)
    if parsed:
        return parsed.date()

    return None
```

### Currency Fields
```python
def parse_currency(text):
    # Remove formatting
    cleaned = re.sub(r'[,$]', '', text)

    # Handle multipliers
    multipliers = {
        'k': 1000, 'K': 1000, 'thousand': 1000,
        'm': 1000000, 'M': 1000000, 'million': 1000000
    }

    for suffix, multiplier in multipliers.items():
        if suffix in text:
            cleaned = re.sub(r'[a-zA-Z]', '', cleaned)
            return float(cleaned) * multiplier

    return float(cleaned)
```

### Picklist Fields
```python
def map_to_picklist(extracted_value, picklist_options):
    # Exact match
    if extracted_value in picklist_options:
        return extracted_value

    # Fuzzy match
    best_match = None
    best_score = 0

    for option in picklist_options:
        score = fuzzy_match(extracted_value.lower(), option.lower())
        if score > best_score and score > 0.8:
            best_match = option
            best_score = score

    return best_match  # May be None
```

## Metrics

### Extraction Quality
```
Track:
- Extraction accuracy (vs human verification)
- Confidence calibration
- Field coverage (% of fields populated)
- False positive rate
- Human override rate

Improve:
- Rules with low accuracy
- Fields with low coverage
- High override rate patterns
```

### Time Savings
```
Measure:
- Data entry time before automation
- Data entry time after automation
- Data quality improvement
- Rep satisfaction

"Automated field population saves reps
35 minutes/day on average."
```

