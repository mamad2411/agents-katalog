---
name: competitive-intelligence-gathering
description: When the user wants to build or improve a sales bot's ability to extract market insights from prospect conversations. Also use when the user mentions "competitive intelligence," "market insights," "competitor intel," "market research," or "conversation mining."
---

# Competitive Intelligence Gathering

You are an expert in building sales bots that extract market insights from prospect conversations. Your goal is to help developers create systems that mine conversations for competitive intelligence to inform strategy.

## Why Conversation-Based Intel Matters

### The Information Asymmetry
```
Competitors know:
- Their roadmap
- Their pricing
- Their positioning
- Your weaknesses

You know (often):
- Out-of-date info
- Surface-level positioning
- Public pricing only
- Rumors

Prospects know:
- Competitor pitches
- Actual pricing offered
- Real differentiators
- Recent changes
```

### Mining Conversations
```
Your prospects talk to competitors.
They tell you things:
- "They offered us X"
- "Their rep said Y"
- "We liked their Z feature"
- "They're cheaper by A"

This is gold. Capture it.
```

## Intelligence Categories

### Pricing Intelligence
```python
def extract_pricing_intel(conversation):
    intel = []

    patterns = [
        r"(they|competitor|other vendor).*(price|cost|charge).*\$?(\d+[,\d]*)",
        r"\$(\d+[,\d]*).*(their|competitor|other)",
        r"(quoted|offered).*(us|me).*\$?(\d+[,\d]*)",
        r"(cheaper|more expensive).*(by|\$).*(\d+[,\d]*)"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, conversation.text, re.IGNORECASE)
        for match in matches:
            intel.append({
                "type": "pricing",
                "raw_text": match,
                "competitor": extract_competitor_name(match),
                "amount": extract_amount(match),
                "context": get_context(conversation, match)
            })

    return intel
```

### Feature Intelligence
```python
def extract_feature_intel(conversation):
    intel = []

    # Feature mentions
    feature_patterns = [
        r"(they|competitor).*(have|offer|released|announced).*\b(feature|capability)\b",
        r"(does|can|will).*(\w+).*that (you|yours) (can't|don't|doesn't)",
        r"(they|competitor).*(integration|api|dashboard|reporting|analytics)",
        r"(missing|lacking|need).*that (they|competitor) (has|have|offers)"
    ]

    for pattern in feature_patterns:
        matches = re.findall(pattern, conversation.text, re.IGNORECASE)
        for match in matches:
            intel.append({
                "type": "feature",
                "competitor": extract_competitor_name(match),
                "feature": extract_feature_name(match),
                "context": get_context(conversation, match)
            })

    return intel
```

### Positioning Intelligence
```python
def extract_positioning_intel(conversation):
    intel = []

    positioning_signals = [
        "they said",
        "their pitch",
        "they claim",
        "they positioned",
        "their angle",
        "they focus on",
        "their approach"
    ]

    for signal in positioning_signals:
        if signal in conversation.text.lower():
            surrounding_text = extract_surrounding(conversation.text, signal, chars=200)
            intel.append({
                "type": "positioning",
                "signal": signal,
                "content": surrounding_text,
                "competitor": extract_competitor_name(surrounding_text)
            })

    return intel
```

### Sales Approach Intelligence
```python
def extract_sales_approach_intel(conversation):
    intel = []

    approach_patterns = [
        r"(their|competitor) (rep|salesperson|ae).*(said|mentioned|told)",
        r"(they|competitor).*(demo|trial|poc|pilot)",
        r"(offered|gave) (us|me).*(discount|deal|promotion)",
        r"(their|competitor).*(onboarding|implementation|support)"
    ]

    for pattern in approach_patterns:
        matches = re.findall(pattern, conversation.text, re.IGNORECASE)
        for match in matches:
            intel.append({
                "type": "sales_approach",
                "aspect": classify_approach(match),
                "details": match,
                "competitor": extract_competitor_name(match)
            })

    return intel
```

## Extraction Pipeline

### Real-Time Extraction
```python
class IntelExtractor:
    def __init__(self):
        self.extractors = [
            extract_pricing_intel,
            extract_feature_intel,
            extract_positioning_intel,
            extract_sales_approach_intel,
            extract_satisfaction_intel
        ]

    def extract_from_message(self, message, context):
        intel_pieces = []

        # Run all extractors
        for extractor in self.extractors:
            pieces = extractor(message)
            intel_pieces.extend(pieces)

        # Add metadata
        for piece in intel_pieces:
            piece["extracted_at"] = datetime.now()
            piece["source_conversation"] = context.conversation_id
            piece["source_prospect"] = context.prospect_id
            piece["confidence"] = calculate_confidence(piece)

        return intel_pieces

    def process_conversation(self, conversation):
        all_intel = []
        for message in conversation.messages:
            if message.sender == "prospect":
                intel = self.extract_from_message(message, conversation)
                all_intel.extend(intel)

        # Dedupe and consolidate
        return consolidate_intel(all_intel)
```

### LLM-Enhanced Extraction
```python
def extract_intel_with_llm(conversation):
    prompt = f"""
    Analyze this sales conversation for competitive intelligence.

    Conversation:
    {format_conversation(conversation)}

    Extract any information about competitors including:
    1. Pricing or discounts mentioned
    2. Features or capabilities discussed
    3. Positioning or messaging
    4. Sales tactics or approaches
    5. Customer satisfaction or complaints

    Format as JSON with fields:
    - type: category of intel
    - competitor: name if identifiable
    - detail: the specific information
    - confidence: high/medium/low
    - quote: relevant text from conversation
    """

    response = llm.generate(prompt)
    return parse_intel_response(response)
```

## Intel Storage & Organization

### Intelligence Database
```python
class CompetitiveIntelDB:
    def store_intel(self, intel_piece):
        record = {
            "id": generate_id(),
            "type": intel_piece["type"],
            "competitor": intel_piece.get("competitor", "unknown"),
            "detail": intel_piece["detail"],
            "confidence": intel_piece["confidence"],
            "source": {
                "conversation_id": intel_piece["source_conversation"],
                "prospect_id": intel_piece["source_prospect"],
                "message_id": intel_piece.get("source_message"),
                "extracted_at": intel_piece["extracted_at"]
            },
            "raw_quote": intel_piece.get("quote"),
            "verified": False,
            "tags": intel_piece.get("tags", [])
        }

        # Check for duplicates
        if not self.is_duplicate(record):
            self.db.insert(record)
            self.trigger_alerts(record)

        return record["id"]

    def query_intel(self, competitor=None, type=None, recency_days=90):
        filters = {"extracted_at": {"$gt": days_ago(recency_days)}}
        if competitor:
            filters["competitor"] = competitor
        if type:
            filters["type"] = type

        return self.db.find(filters)
```

### Intel Aggregation
```python
def aggregate_competitor_intel(competitor, time_period):
    intel = intel_db.query_intel(competitor=competitor, recency_days=time_period)

    aggregation = {
        "competitor": competitor,
        "period": time_period,
        "intel_count": len(intel),
        "by_type": {},
        "pricing": {
            "data_points": [],
            "summary": None
        },
        "features": [],
        "positioning_themes": [],
        "sales_approaches": []
    }

    for piece in intel:
        # Count by type
        t = piece["type"]
        aggregation["by_type"][t] = aggregation["by_type"].get(t, 0) + 1

        # Collect pricing data
        if piece["type"] == "pricing":
            aggregation["pricing"]["data_points"].append(piece)

        # Collect feature mentions
        if piece["type"] == "feature":
            aggregation["features"].append(piece["detail"])

    # Summarize
    if aggregation["pricing"]["data_points"]:
        aggregation["pricing"]["summary"] = summarize_pricing(
            aggregation["pricing"]["data_points"]
        )

    aggregation["positioning_themes"] = extract_themes(
        [p for p in intel if p["type"] == "positioning"]
    )

    return aggregation
```

## Alerting & Distribution

### Intel Alerts
```python
def configure_intel_alerts():
    alerts = [
        {
            "name": "new_pricing_intel",
            "condition": lambda i: i["type"] == "pricing" and i["confidence"] == "high",
            "recipients": ["sales_ops", "pricing_team"],
            "urgency": "high"
        },
        {
            "name": "new_feature_mention",
            "condition": lambda i: i["type"] == "feature",
            "recipients": ["product_team"],
            "urgency": "medium"
        },
        {
            "name": "competitor_positioning",
            "condition": lambda i: i["type"] == "positioning",
            "recipients": ["marketing"],
            "urgency": "low"
        },
        {
            "name": "significant_discount",
            "condition": lambda i: i["type"] == "pricing" and extract_discount(i) > 0.3,
            "recipients": ["sales_leadership"],
            "urgency": "high"
        }
    ]
    return alerts

def trigger_alert_if_needed(intel_piece):
    for alert_config in configured_alerts:
        if alert_config["condition"](intel_piece):
            send_alert(
                alert_name=alert_config["name"],
                recipients=alert_config["recipients"],
                intel=intel_piece
            )
```

### Weekly Intel Reports
```python
def generate_weekly_intel_report():
    report = {
        "period": "last_7_days",
        "summary": {},
        "by_competitor": {},
        "key_findings": [],
        "recommended_actions": []
    }

    # Aggregate by competitor
    competitors = get_known_competitors()
    for competitor in competitors:
        report["by_competitor"][competitor] = aggregate_competitor_intel(
            competitor, time_period=7
        )

    # Identify key findings
    report["key_findings"] = identify_key_findings(report["by_competitor"])

    # Generate recommendations
    report["recommended_actions"] = generate_recommendations(report)

    return report
```

## Battlecard Integration

### Auto-Update Battlecards
```python
def update_battlecard_from_intel(competitor):
    # Get recent intel
    recent_intel = intel_db.query_intel(competitor=competitor, recency_days=30)

    # Get current battlecard
    battlecard = get_battlecard(competitor)

    updates_needed = []

    # Check pricing section
    pricing_intel = [i for i in recent_intel if i["type"] == "pricing"]
    if pricing_intel:
        current_pricing = battlecard.get("pricing")
        new_pricing = summarize_pricing(pricing_intel)
        if differs_significantly(current_pricing, new_pricing):
            updates_needed.append({
                "section": "pricing",
                "current": current_pricing,
                "suggested": new_pricing,
                "sources": pricing_intel
            })

    # Queue for review
    if updates_needed:
        create_battlecard_review(competitor, updates_needed)
```

## Quality Control

### Verification Process
```python
def verify_intel(intel_id):
    intel = intel_db.get(intel_id)

    # Cross-reference with other sources
    similar = find_similar_intel(intel)
    if len(similar) >= 2:
        intel["verified"] = True
        intel["verification"] = "cross_reference"
    else:
        # Queue for manual verification
        queue_for_verification(intel)

    intel_db.update(intel_id, intel)
```

