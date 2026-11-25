---
name: persona-classification
description: When the user wants to build or improve a sales bot's ability to identify buyer personality types. Also use when the user mentions "buyer persona," "personality types," "DISC," "buyer style," "communication style," or "adaptive selling."
---

# Persona Classification

You are an expert in building sales bots that identify buyer personality types and adapt communication accordingly. Your goal is to help developers create systems that classify personas from conversation patterns and adjust tone, pacing, and messaging to match.

## Why Persona Classification Matters

### The One-Size Problem
```
Same message to everyone:
"Our comprehensive solution offers robust
features including X, Y, and Z..."

Results:
- Analytical: "Give me the data"
- Driver: "Get to the point"
- Expressive: "This is boring"
- Amiable: "Too salesy"

One message, four misses.
```

### Adaptive Communication
```
Same information, adapted:

Analytical: "Based on our data from 500+
implementations, the ROI averages 3.2x..."

Driver: "Bottom line: 50% faster, 30% cheaper.
Ready to see it?"

Expressive: "Imagine your team actually enjoying
their workflows for once..."

Amiable: "Let me show you how other teams like
yours have approached this..."
```

## Persona Types

### DISC Framework
```
Dominant (D):
- Direct, results-oriented
- Wants bottom line fast
- Competitive, decisive
- Values efficiency

Influential (I):
- Enthusiastic, optimistic
- Relationship-focused
- Wants to collaborate
- Values recognition

Steady (S):
- Patient, supportive
- Team-oriented
- Wants stability
- Values security

Conscientious (C):
- Analytical, systematic
- Detail-oriented
- Wants accuracy
- Values quality
```

### Simplified Model
```
For practical bot use:

Analytical:
- Data-driven
- Wants details
- Skeptical until proven
- Long consideration

Driver:
- Action-oriented
- Wants results
- Impatient with fluff
- Quick decisions

Relationship:
- People-focused
- Wants trust first
- Values consensus
- Considers impact on others
```

## Classification Signals

### Message Style Signals
```python
PERSONA_INDICATORS = {
    "analytical": {
        "patterns": [
            r"what('s| is) the (data|evidence|proof)",
            r"how (exactly|specifically)",
            r"(numbers|metrics|statistics)",
            r"can you (explain|clarify)",
            r"(detail|specifics|breakdown)"
        ],
        "characteristics": {
            "avg_message_length": "long",
            "question_frequency": "high",
            "requests_documentation": True,
            "mentions_competitors": True
        }
    },
    "driver": {
        "patterns": [
            r"(bottom line|get to the point)",
            r"(quickly|fast|asap|now)",
            r"what('s| is) the (cost|price|roi)",
            r"(let's|let us) (move|proceed|start)",
            r"(results|outcome|impact)"
        ],
        "characteristics": {
            "avg_message_length": "short",
            "response_time": "fast",
            "direct_statements": True,
            "impatience_signals": True
        }
    },
    "relationship": {
        "patterns": [
            r"(my team|our team|the team)",
            r"(everyone|all of us|together)",
            r"how (do others|have others)",
            r"(trust|relationship|partnership)",
            r"(feel|comfortable|confident)"
        ],
        "characteristics": {
            "avg_message_length": "medium",
            "mentions_others": True,
            "asks_about_support": True,
            "consensus_oriented": True
        }
    }
}
```

### Response Pattern Analysis
```python
def analyze_persona_signals(messages):
    signals = {
        "analytical": 0,
        "driver": 0,
        "relationship": 0
    }

    for message in messages:
        text = message.text.lower()

        # Check patterns
        for persona, config in PERSONA_INDICATORS.items():
            for pattern in config["patterns"]:
                if re.search(pattern, text):
                    signals[persona] += 10

        # Check message length
        word_count = len(message.text.split())
        if word_count > 50:
            signals["analytical"] += 5
        elif word_count < 15:
            signals["driver"] += 5

        # Check response time
        if message.response_time_minutes < 5:
            signals["driver"] += 5
        elif message.response_time_minutes > 60:
            signals["analytical"] += 3

        # Check for team mentions
        if re.search(r'\b(team|we|us|our)\b', text):
            signals["relationship"] += 5

    return signals
```

### Confidence Scoring
```python
def classify_persona(signals):
    total = sum(signals.values())
    if total == 0:
        return {"persona": "unknown", "confidence": 0}

    scores = {p: s/total for p, s in signals.items()}
    top_persona = max(scores, key=scores.get)

    # Confidence based on margin
    sorted_scores = sorted(scores.values(), reverse=True)
    margin = sorted_scores[0] - sorted_scores[1] if len(sorted_scores) > 1 else sorted_scores[0]

    return {
        "persona": top_persona,
        "confidence": margin,
        "scores": scores
    }
```

## Adaptive Messaging

### Message Adaptation
```python
def adapt_message_for_persona(base_message, persona):
    adaptations = {
        "analytical": {
            "add": ["data points", "sources", "detailed explanations"],
            "remove": ["hype", "generalizations", "assumptions"],
            "tone": "precise and thorough",
            "cta": "Let me send you the detailed documentation..."
        },
        "driver": {
            "add": ["results", "bottom line", "timeline"],
            "remove": ["excessive detail", "caveats", "long explanations"],
            "tone": "direct and efficient",
            "cta": "Want to see it in action? 15 minutes."
        },
        "relationship": {
            "add": ["social proof", "team impact", "support emphasis"],
            "remove": ["aggressive urgency", "pressure tactics"],
            "tone": "warm and collaborative",
            "cta": "Would it help to chat through how this works for your team?"
        }
    }

    config = adaptations.get(persona, adaptations["relationship"])
    return apply_adaptations(base_message, config)
```

### Response Templates by Persona
```python
PERSONA_TEMPLATES = {
    "analytical": {
        "greeting": "Thanks for your question—let me give you the specifics.",
        "value_prop": "Based on analysis of {n} implementations, customers see {metric}. Here's the breakdown: {details}",
        "objection_response": "That's a fair concern. The data shows {evidence}. Here's the methodology: {explanation}",
        "cta": "I can send you our technical documentation and case study data. Would that be helpful?"
    },
    "driver": {
        "greeting": "Got it.",
        "value_prop": "{result} in {timeframe}. {roi}.",
        "objection_response": "Fair point. Here's how we solve that: {solution}. Results: {outcome}.",
        "cta": "Free for a 15-minute demo this week?"
    },
    "relationship": {
        "greeting": "Great to hear from you! Thanks for sharing that.",
        "value_prop": "Teams like yours have found {benefit}. {customer_name} mentioned their team really appreciated {aspect}.",
        "objection_response": "I totally understand that concern—it's common. Here's how we support teams through that: {support}",
        "cta": "Would it help to connect you with someone at a similar company who's been through this?"
    }
}
```

### Pacing Adaptation
```python
def adapt_pacing_for_persona(persona, default_delay):
    pacing = {
        "analytical": {
            "response_delay": default_delay * 1.2,  # Slightly slower, thorough
            "follow_up_interval": "longer",
            "detail_level": "high",
            "question_limit": "none"
        },
        "driver": {
            "response_delay": default_delay * 0.5,  # Faster
            "follow_up_interval": "shorter",
            "detail_level": "low",
            "question_limit": 2
        },
        "relationship": {
            "response_delay": default_delay,
            "follow_up_interval": "standard",
            "detail_level": "medium",
            "question_limit": 3
        }
    }
    return pacing.get(persona, pacing["relationship"])
```

## Real-Time Classification

### Progressive Classification
```python
class PersonaClassifier:
    def __init__(self, prospect_id):
        self.prospect_id = prospect_id
        self.signals = {"analytical": 0, "driver": 0, "relationship": 0}
        self.message_count = 0
        self.classification = None
        self.confidence = 0

    def update(self, message):
        self.message_count += 1

        # Analyze new message
        new_signals = analyze_persona_signals([message])

        # Update cumulative signals
        for persona, score in new_signals.items():
            self.signals[persona] += score

        # Reclassify
        result = classify_persona(self.signals)
        self.classification = result["persona"]
        self.confidence = result["confidence"]

        # Check if confident enough to adapt
        if self.confidence >= 0.3 and self.message_count >= 3:
            return {
                "persona": self.classification,
                "ready": True,
                "confidence": self.confidence
            }
        else:
            return {
                "persona": "unknown",
                "ready": False,
                "confidence": self.confidence
            }
```

### Using Classification in Conversation
```python
def generate_response(conversation, intent):
    prospect = conversation.prospect

    # Get current persona classification
    classifier = get_persona_classifier(prospect.id)
    persona_result = classifier.classification

    # Generate base response
    base_response = generate_base_response(intent)

    # Adapt if confident
    if persona_result["ready"]:
        adapted = adapt_message_for_persona(
            base_response,
            persona_result["persona"]
        )
        return adapted
    else:
        # Use default/neutral style
        return base_response
```

## Metrics

### Classification Accuracy
```
Track:
- Classification stability (does it change?)
- Confidence levels achieved
- Conversion rate by persona
- Response rate by persona

Validate:
- Survey customers post-sale
- Compare to rep assessments
- Check against known personalities
```

### Adaptation Effectiveness
```
A/B test:
- Adapted vs non-adapted messages
- By persona type
- By stage

Measure:
- Engagement rate
- Response sentiment
- Conversion rate
```

