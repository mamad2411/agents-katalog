---
name: multilingual-support
description: When the user wants to build or improve a sales bot's ability to detect prospect language and respond appropriately or route to the right team. Also use when the user mentions "language detection," "multilingual," "non-English," "translation," "language routing," or "international prospects."
---

# Multilingual Support

You are an expert in building multilingual capabilities for sales bots. Your goal is to help developers create systems that detect language, respond appropriately, and route conversations effectively.

## Language Detection

### Detection Methods

**Message Analysis**
```
Analyze incoming message:
- Character set (Latin, Cyrillic, CJK, etc.)
- Common words/patterns
- Language-specific characters (ñ, ü, ç)
- Statistical language models

Confidence scoring:
- High (90%+): Respond in detected language
- Medium (70-90%): Respond in detected, offer alternative
- Low (<70%): Clarify with prospect
```

**Contextual Signals**
```
Other indicators:
- Phone number country code
- Email domain (.fr, .de, .jp)
- IP geolocation
- Prior interactions
- Account settings
- Browser language
```

### Common Detection Challenges
```
Challenge: Similar languages
Spanish vs Portuguese
Dutch vs Afrikaans
Solution: Look for distinctive patterns

Challenge: Code-switching
"I need the pricing por favor"
Solution: Detect primary language, accommodate mixing

Challenge: Transliteration
"Mne nuzhna pomoshch" (Russian in Latin)
Solution: Detect and offer native script

Challenge: English used by non-native
Grammatical patterns may reveal native language
Solution: Consider offering native language option
```

## Response Strategies

### Native Language Response
```
If confident in detection and capability exists:

Prospect: "Bonjour, j'ai besoin d'information sur vos prix"

Bot: "Bonjour ! Je serais ravi de vous aider avec nos tarifs.
Pouvez-vous me dire quelle est la taille de votre équipe ?"
```

### Hybrid Response
```
When confidence is medium:

Bot: "Je vois que vous parlez français ! Je peux continuer
en français ou en anglais—quelle est votre préférence?

I see you're writing in French! I can continue in French
or English—what's your preference?"
```

### Routing Response
```
When no capability in that language:

Bot: "I noticed you're writing in German. Let me connect
you with a colleague who speaks German fluently.

Ich habe bemerkt, dass Sie auf Deutsch schreiben.
Lassen Sie mich Sie mit einem deutschsprachigen
Kollegen verbinden."
```

## Language Capability Matrix

### Define Your Coverage
```
Language       | Bot      | Human     | Materials
               | Support  | Available | Available
───────────────|──────────|───────────|──────────
English        | Full     | Yes       | Yes
Spanish        | Full     | Yes       | Yes
French         | Full     | Yes       | Partial
German         | Partial  | Yes       | Yes
Portuguese     | Routing  | Limited   | No
Mandarin       | Routing  | Yes       | Yes
Japanese       | Routing  | Limited   | Partial
Arabic         | No       | Limited   | No
```

### Capability Levels
```
FULL: Bot can handle entire conversation
- Qualification
- Objection handling
- Scheduling
- Complex queries

PARTIAL: Bot handles basics, escalates complexity
- Initial greeting
- Simple Q&A
- Collecting information
- Routing to human

ROUTING: Detect and route only
- Language detection
- Polite acknowledgment
- Immediate handoff
```

## Conversation Handoff

### Warm Transfer
```
When routing to human:

To prospect:
"Je vous mets en contact avec Marie, qui pourra vous
aider en français. Un instant s'il vous plaît."

To human rep (in internal system):
"Incoming: French-speaking prospect from Paris
Context: Interested in Enterprise plan
Initial need: Pricing for 50-person team
Sentiment: Positive, engaged"
```

### Async Handoff
```
When no human immediately available:

"Thank you for reaching out! I noticed you're more
comfortable in Spanish.

Our Spanish-speaking team member will reach out within
[timeframe]. In the meantime, is there anything I can
help with in English?

Gracias por contactarnos. He notado que prefiere
comunicarse en español. Un miembro de nuestro equipo
que habla español se pondrá en contacto con usted
dentro de [plazo]."
```

## Content Management

### Localized Responses
```
Store responses per language:

greeting:
  en: "Hi! How can I help you today?"
  es: "¡Hola! ¿Cómo puedo ayudarte hoy?"
  fr: "Bonjour ! Comment puis-je vous aider ?"
  de: "Hallo! Wie kann ich Ihnen helfen?"

qualification_question:
  en: "How many people are on your team?"
  es: "¿Cuántas personas hay en tu equipo?"
  fr: "Combien de personnes composent votre équipe ?"
  de: "Wie viele Personen sind in Ihrem Team?"
```

### Dynamic Translation
```
For languages without full coverage:

1. Translate incoming message to English
2. Process in English
3. Generate response in English
4. Translate response to target language
5. Human review for quality (async)

Flag for human review:
- Complex topics
- Nuanced communication
- Legal/contractual language
- Cultural considerations
```

## Cultural Considerations

### Beyond Translation
```
Adapt for culture:

Formality levels:
- German: More formal (Sie vs du)
- Spanish: Varies by region (usted vs tú)
- Japanese: Multiple politeness levels

Business norms:
- US: Get to the point quickly
- Japan: Relationship building first
- Germany: Precision and detail valued
- Brazil: Warmth and rapport important

Time references:
- Dates: MM/DD vs DD/MM vs YYYY-MM-DD
- Time: 12h vs 24h
- Week start: Sunday vs Monday
```

### Regional Variations
```
Spanish:
- Spain: "ordenador" (computer)
- LatAm: "computadora"
- Currency, date formats vary

Portuguese:
- Brazil: Different vocabulary, spelling
- Portugal: More formal constructions

Chinese:
- Simplified (Mainland)
- Traditional (Taiwan, Hong Kong)
```

## Implementation

### Language Preference Storage
```json
{
  "prospect_id": "12345",
  "language_preferences": {
    "detected_language": "es",
    "confirmed_preference": "es",
    "secondary_language": "en",
    "region": "MX",
    "formality": "informal"
  },
  "routing_preference": {
    "preferred_rep_language": "es",
    "acceptable_languages": ["es", "en"],
    "timezone": "America/Mexico_City"
  }
}
```

### Detection Flow
```python
def handle_message(message, prospect):
    # Detect language
    detected = detect_language(message.text)

    # Check against preference
    if prospect.language_preference:
        language = prospect.language_preference
    else:
        language = detected.language
        confidence = detected.confidence

        if confidence < 0.8:
            return clarify_language_preference()

    # Check capability
    if can_handle(language):
        return generate_response(message, language)
    elif can_route(language):
        return route_to_team(message, language)
    else:
        return offer_alternatives(language)
```

### Quality Assurance
```
Monitor:
- Detection accuracy
- Response quality per language
- CSAT scores by language
- Routing accuracy
- Time to qualified human (if routed)

Improve:
- Review misdetections
- Train on new patterns
- Add language coverage
- Localize more content
```
