---
name: dynamic-script-generation
description: When the user wants to build or improve a sales bot's ability to generate personalized scripts on the fly. Also use when the user mentions "dynamic scripts," "script generation," "personalized messaging," "adaptive scripts," or "real-time content generation."
---

# Dynamic Script Generation

You are an expert in building sales bots that generate personalized conversation scripts in real-time. Your goal is to help developers create systems that adapt messaging to each prospect rather than using static templates.

## Why Dynamic Scripts Matter

### The Template Problem
```
Static templates:
"Hi {first_name}, I noticed you work at {company}..."

Every prospect gets same structure.
Experienced prospects recognize templates.
No adaptation to context or signals.
```

### Dynamic Generation
```
Each message built from:
- Prospect attributes
- Conversation context
- Previous interactions
- Current signals
- Optimal patterns

Result: Unique, relevant messages
that feel personally crafted.
```

## Script Components

### Component Library
```python
class ScriptComponent:
    def __init__(self, component_type, variants):
        self.type = component_type
        self.variants = variants
        self.performance = {v: {"sends": 0, "responses": 0} for v in variants}

    def select_variant(self, context):
        """Select best variant for context"""

        # Filter applicable variants
        applicable = [
            v for v in self.variants
            if self.is_applicable(v, context)
        ]

        if not applicable:
            return self.variants[0]  # Default

        # Select based on performance and context fit
        scored = [
            (v, self.score_variant(v, context))
            for v in applicable
        ]

        return max(scored, key=lambda x: x[1])[0]

    def score_variant(self, variant, context):
        perf = self.performance[variant]
        if perf["sends"] < 50:
            return 0.5  # Explore

        response_rate = perf["responses"] / perf["sends"]
        context_fit = self.calculate_context_fit(variant, context)

        return response_rate * 0.6 + context_fit * 0.4


# Component definitions
OPENERS = ScriptComponent("opener", [
    "quick_question",
    "noticed_trigger",
    "mutual_connection",
    "industry_insight",
    "direct_value",
    "curiosity_hook"
])

VALUE_PROPS = ScriptComponent("value_prop", [
    "roi_focused",
    "time_savings",
    "risk_reduction",
    "competitive_advantage",
    "growth_enablement",
    "cost_reduction"
])

CALLS_TO_ACTION = ScriptComponent("cta", [
    "meeting_request",
    "resource_offer",
    "question_engagement",
    "micro_commitment",
    "social_proof_share",
    "demo_invite"
])
```

### Context-Aware Selection
```python
def select_components(prospect, context):
    """Select optimal components for prospect"""

    components = {}

    # Select opener based on available data
    if context.trigger_event:
        components["opener"] = generate_trigger_opener(context.trigger_event)
    elif context.mutual_connections:
        components["opener"] = generate_connection_opener(context.mutual_connections[0])
    elif prospect.industry_news:
        components["opener"] = generate_insight_opener(prospect.industry_news)
    else:
        components["opener"] = OPENERS.select_variant(context)

    # Select value prop based on persona
    if prospect.persona == "executive":
        components["value_prop"] = VALUE_PROPS.select_variant(
            context, preference=["roi_focused", "competitive_advantage"]
        )
    elif prospect.persona == "technical":
        components["value_prop"] = VALUE_PROPS.select_variant(
            context, preference=["time_savings", "risk_reduction"]
        )

    # Select CTA based on engagement level
    if context.engagement_score > 0.7:
        components["cta"] = "meeting_request"
    elif context.engagement_score > 0.4:
        components["cta"] = "question_engagement"
    else:
        components["cta"] = "resource_offer"

    return components
```

## Script Assembly

### Message Builder
```python
class DynamicScriptBuilder:
    def __init__(self):
        self.components = {}
        self.templates = {}
        self.personalization_engine = PersonalizationEngine()

    def build_message(self, prospect, context, message_type):
        """Build complete message from components"""

        # Select components
        components = select_components(prospect, context)

        # Get base structure
        structure = self.get_message_structure(message_type, context)

        # Build each section
        sections = []
        for section in structure:
            content = self.build_section(
                section,
                components.get(section),
                prospect,
                context
            )
            sections.append(content)

        # Assemble message
        message = self.assemble_sections(sections, context)

        # Apply personalization
        message = self.personalization_engine.personalize(message, prospect)

        # Validate
        message = self.validate_and_adjust(message, context)

        return message

    def build_section(self, section_type, component, prospect, context):
        """Build individual message section"""

        if section_type == "opener":
            return self.build_opener(component, prospect, context)
        elif section_type == "value_prop":
            return self.build_value_prop(component, prospect, context)
        elif section_type == "social_proof":
            return self.build_social_proof(prospect, context)
        elif section_type == "cta":
            return self.build_cta(component, prospect, context)

    def build_opener(self, opener_type, prospect, context):
        """Generate opener content"""

        openers = {
            "quick_question": lambda p, c: f"Quick question about {p.company}'s {c.topic_of_interest}",
            "noticed_trigger": lambda p, c: f"Noticed {p.company} {c.trigger_event.description}",
            "mutual_connection": lambda p, c: f"{c.mutual_connections[0].name} suggested I reach out",
            "industry_insight": lambda p, c: f"Given {p.industry}'s shift toward {c.industry_trend}",
            "direct_value": lambda p, c: f"Helping {p.industry} {p.company_size} companies {c.value_statement}",
            "curiosity_hook": lambda p, c: f"Curious how {p.company} handles {c.pain_point}"
        }

        base = openers.get(opener_type, openers["direct_value"])
        return base(prospect, context)
```

### LLM-Powered Generation
```python
def generate_with_llm(prospect, context, constraints):
    """Use LLM for sophisticated script generation"""

    prompt = f"""
    Generate a sales message with these parameters:

    Prospect:
    - Name: {prospect.first_name} {prospect.last_name}
    - Title: {prospect.title}
    - Company: {prospect.company}
    - Industry: {prospect.industry}
    - Company Size: {prospect.company_size}

    Context:
    - Trigger Event: {context.trigger_event}
    - Previous Interactions: {context.interaction_count}
    - Last Response Sentiment: {context.last_sentiment}
    - Stage: {context.sales_stage}

    Constraints:
    - Tone: {constraints.tone}
    - Length: {constraints.max_words} words max
    - Must Include: {constraints.required_elements}
    - Must Avoid: {constraints.forbidden_phrases}
    - CTA Type: {constraints.cta_type}

    Generate a personalized message that:
    1. Opens with relevant hook
    2. Provides specific value for their situation
    3. Includes appropriate social proof
    4. Ends with clear but low-pressure CTA

    Output only the message text.
    """

    response = llm.generate(
        prompt,
        temperature=0.7,
        max_tokens=300
    )

    # Validate output
    validated = validate_generated_message(response, constraints)

    return validated
```

## Personalization Engine

### Deep Personalization
```python
class PersonalizationEngine:
    def __init__(self):
        self.data_sources = []
        self.personalization_rules = []

    def personalize(self, message, prospect):
        """Apply personalization to message"""

        personalized = message

        # Basic replacements
        personalized = self.apply_basic_personalization(personalized, prospect)

        # Dynamic elements
        personalized = self.apply_dynamic_elements(personalized, prospect)

        # Context-specific adjustments
        personalized = self.apply_context_adjustments(personalized, prospect)

        return personalized

    def apply_basic_personalization(self, message, prospect):
        """Replace standard tokens"""

        replacements = {
            "{first_name}": prospect.first_name,
            "{last_name}": prospect.last_name,
            "{company}": prospect.company,
            "{title}": prospect.title,
            "{industry}": prospect.industry
        }

        for token, value in replacements.items():
            if value:
                message = message.replace(token, value)

        return message

    def apply_dynamic_elements(self, message, prospect):
        """Insert dynamic content based on data"""

        # Company-specific insight
        if "{company_insight}" in message:
            insight = self.generate_company_insight(prospect)
            message = message.replace("{company_insight}", insight)

        # Relevant case study
        if "{relevant_proof}" in message:
            proof = self.find_relevant_proof(prospect)
            message = message.replace("{relevant_proof}", proof)

        # Industry-specific language
        message = self.apply_industry_language(message, prospect.industry)

        return message

    def generate_company_insight(self, prospect):
        """Generate relevant insight about company"""

        insights = gather_company_insights(prospect.company)

        if insights.recent_news:
            return f"your recent {insights.recent_news.category}"
        elif insights.job_postings:
            return f"your team's growth in {insights.job_postings.department}"
        elif insights.tech_stack:
            return f"your use of {insights.tech_stack.relevant_tech}"

        return f"companies like {prospect.company}"
```

### Tone Adaptation
```python
def adapt_tone(message, prospect, context):
    """Adapt message tone to prospect"""

    tone_profiles = {
        "executive": {
            "formality": "high",
            "length": "concise",
            "focus": "outcomes",
            "avoid": ["jargon", "casual_language"]
        },
        "technical": {
            "formality": "medium",
            "length": "detailed",
            "focus": "specifics",
            "include": ["technical_terms", "data_points"]
        },
        "startup": {
            "formality": "low",
            "length": "brief",
            "focus": "agility",
            "style": "casual_professional"
        },
        "enterprise": {
            "formality": "high",
            "length": "moderate",
            "focus": "risk_mitigation",
            "include": ["security", "compliance"]
        }
    }

    profile = determine_tone_profile(prospect)
    tone = tone_profiles.get(profile, tone_profiles["executive"])

    # Apply tone adjustments
    adapted = apply_formality(message, tone["formality"])
    adapted = adjust_length(adapted, tone["length"])
    adapted = emphasize_focus(adapted, tone["focus"])

    return adapted
```

## Script Variants

### A/B Generation
```python
def generate_variants(prospect, context, num_variants=3):
    """Generate multiple variants for testing"""

    variants = []

    # Vary openers
    opener_types = ["quick_question", "direct_value", "curiosity_hook"]

    for i, opener in enumerate(opener_types[:num_variants]):
        variant = DynamicScriptBuilder().build_message(
            prospect,
            context,
            message_type="outreach",
            opener_override=opener
        )

        variants.append({
            "variant_id": f"v{i+1}",
            "opener_type": opener,
            "message": variant,
            "hypothesis": get_hypothesis(opener, prospect)
        })

    return variants

def get_hypothesis(opener_type, prospect):
    """Document hypothesis for each variant"""

    hypotheses = {
        "quick_question": f"Questions engage {prospect.persona} personas",
        "direct_value": f"Direct approach works for busy {prospect.title}s",
        "curiosity_hook": f"Curiosity drives opens in {prospect.industry}"
    }

    return hypotheses.get(opener_type, "Testing variant performance")
```

## Quality Assurance

### Message Validation
```python
def validate_generated_message(message, constraints):
    """Validate generated message meets standards"""

    issues = []

    # Length check
    word_count = len(message.split())
    if word_count > constraints.max_words:
        issues.append(f"Too long: {word_count} words")
        message = truncate_to_length(message, constraints.max_words)

    # Required elements
    for element in constraints.required_elements:
        if not contains_element(message, element):
            issues.append(f"Missing: {element}")

    # Forbidden phrases
    for phrase in constraints.forbidden_phrases:
        if phrase.lower() in message.lower():
            issues.append(f"Contains forbidden: {phrase}")
            message = remove_phrase(message, phrase)

    # Placeholder check
    unresolved = re.findall(r'\{[^}]+\}', message)
    if unresolved:
        issues.append(f"Unresolved placeholders: {unresolved}")

    # Grammar check
    grammar_issues = check_grammar(message)
    issues.extend(grammar_issues)

    return {
        "message": message,
        "valid": len(issues) == 0,
        "issues": issues
    }
```

## Performance Tracking

### Script Analytics
```python
def track_script_performance(message, components, result):
    """Track which components perform best"""

    for component_type, variant in components.items():
        # Update component performance
        component_library[component_type].record_performance(
            variant=variant,
            sent=True,
            responded=result.got_response,
            converted=result.converted
        )

    # Track combination performance
    combination_key = tuple(sorted(components.items()))
    combination_performance[combination_key].append({
        "responded": result.got_response,
        "converted": result.converted,
        "timestamp": datetime.now()
    })
```

## Metrics

### Generation Quality
```
Track:
- Response rate by component combination
- Conversion rate by opener type
- Personalization depth score
- Generation time (latency)
- Validation pass rate

Optimize for:
- Response rate > static templates
- Natural language quality
- Consistent brand voice
```

