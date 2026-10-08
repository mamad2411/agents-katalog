---
name: emotional-arc-management
description: When the user wants to build or improve a sales bot's ability to guide conversations through optimal emotional progressions. Also use when the user mentions "emotional arc," "conversation flow," "emotional journey," "engagement curve," or "conversation momentum."
---

# Emotional Arc Management

You are an expert in building sales bots that guide conversations through optimal emotional progressions. Your goal is to help developers create systems that manage the emotional journey of prospects to maximize engagement and conversion.

## Why Emotional Arc Matters

### The Flat Conversation Problem
```
Typical bot conversation:
Message 1: "Hi, we do X"
Message 2: "Would you like to learn more?"
Message 3: "Here's why we're great"
Message 4: "Want to meet?"

Emotional flatline. No journey.
No engagement. No conversion.
```

### With Emotional Arc Management
```
Managed conversation:
Phase 1: Curiosity (hook)
Phase 2: Recognition (they see themselves)
Phase 3: Intrigue (want to know more)
Phase 4: Desire (imagine success)
Phase 5: Confidence (can achieve it)
Phase 6: Action (ready to move)

A journey that builds to conversion.
```

## Arc Framework

### Emotional Phases
```python
class EmotionalArc:
    PHASES = {
        "curiosity": {
            "description": "Capture attention, create interest",
            "target_emotions": ["interested", "intrigued", "curious"],
            "typical_position": 0.0,  # Start
            "success_signals": ["question_asked", "quick_response"]
        },
        "recognition": {
            "description": "Prospect sees themselves in the problem",
            "target_emotions": ["understood", "validated", "seen"],
            "typical_position": 0.15,
            "success_signals": ["agreement", "elaboration", "sharing"]
        },
        "pain_awareness": {
            "description": "Acknowledge and amplify the problem",
            "target_emotions": ["frustrated", "motivated", "urgent"],
            "typical_position": 0.30,
            "success_signals": ["pain_admission", "problem_detail"]
        },
        "hope": {
            "description": "Introduce possibility of solution",
            "target_emotions": ["hopeful", "relieved", "optimistic"],
            "typical_position": 0.45,
            "success_signals": ["interest_in_solution", "forward_leaning"]
        },
        "desire": {
            "description": "Create want for the specific solution",
            "target_emotions": ["excited", "eager", "motivated"],
            "typical_position": 0.60,
            "success_signals": ["specific_questions", "use_case_discussion"]
        },
        "confidence": {
            "description": "Build belief they can achieve success",
            "target_emotions": ["confident", "reassured", "trusting"],
            "typical_position": 0.75,
            "success_signals": ["objection_resolution", "stakeholder_mention"]
        },
        "commitment": {
            "description": "Secure decision and next step",
            "target_emotions": ["decisive", "committed", "ready"],
            "typical_position": 0.90,
            "success_signals": ["agreement", "scheduling", "stakeholder_intro"]
        }
    }
```

### Arc Tracking
```python
class ArcTracker:
    def __init__(self, conversation_id):
        self.conversation_id = conversation_id
        self.current_phase = "curiosity"
        self.phase_history = []
        self.emotional_scores = []

    def assess_current_state(self, message, context):
        """Assess where we are in the emotional arc"""

        # Analyze message sentiment and signals
        sentiment = analyze_sentiment(message)
        signals = extract_engagement_signals(message)

        # Determine current emotional state
        emotional_state = {
            "sentiment_score": sentiment.score,
            "sentiment_label": sentiment.label,
            "engagement_level": calculate_engagement(signals),
            "detected_emotions": detect_emotions(message),
            "phase_signals": match_phase_signals(signals)
        }

        # Update phase assessment
        assessed_phase = self.assess_phase(emotional_state, context)

        self.phase_history.append({
            "timestamp": datetime.now(),
            "message_id": message.id,
            "assessed_phase": assessed_phase,
            "emotional_state": emotional_state
        })

        self.current_phase = assessed_phase
        return emotional_state

    def assess_phase(self, emotional_state, context):
        """Determine which phase the conversation is in"""

        # Check for phase-specific signals
        for phase, config in EmotionalArc.PHASES.items():
            matching_signals = [
                s for s in emotional_state["phase_signals"]
                if s in config["success_signals"]
            ]

            if matching_signals:
                # Verify emotional alignment
                emotions = emotional_state["detected_emotions"]
                emotion_match = any(
                    e in config["target_emotions"]
                    for e in emotions
                )

                if emotion_match:
                    return phase

        # Default to progression based on conversation length
        progress = context.message_count / context.expected_messages
        return self.phase_from_progress(progress)

    def get_arc_health(self):
        """Assess overall arc health"""

        if len(self.phase_history) < 2:
            return {"status": "early", "health": "unknown"}

        # Check for progression
        phases_list = list(EmotionalArc.PHASES.keys())
        phase_indices = [
            phases_list.index(h["assessed_phase"])
            for h in self.phase_history
        ]

        # Calculate progression score
        progression = calculate_monotonic_score(phase_indices)

        # Check for regression
        regressions = sum(
            1 for i in range(1, len(phase_indices))
            if phase_indices[i] < phase_indices[i-1]
        )

        return {
            "status": "healthy" if progression > 0.7 else "struggling",
            "progression_score": progression,
            "regressions": regressions,
            "current_phase": self.current_phase,
            "phases_completed": len(set(h["assessed_phase"] for h in self.phase_history))
        }
```

## Phase-Specific Strategies

### Curiosity Phase
```python
def generate_curiosity_message(context):
    """Generate message to create curiosity"""

    strategies = [
        {
            "type": "question_hook",
            "template": "Quick question: {provocative_question}",
            "works_best_for": ["busy_executives", "skeptics"]
        },
        {
            "type": "insight_hook",
            "template": "Interesting pattern I noticed about {industry} companies like {company}...",
            "works_best_for": ["analytical", "curious"]
        },
        {
            "type": "result_hook",
            "template": "{similar_company} just {achieved_result}. Curious if {company} is tackling {challenge} similarly?",
            "works_best_for": ["competitive", "growth_focused"]
        },
        {
            "type": "contrarian_hook",
            "template": "Most {role}s I talk to believe {common_belief}. But the data shows...",
            "works_best_for": ["thought_leaders", "innovators"]
        }
    ]

    # Select strategy based on prospect profile
    strategy = select_best_strategy(strategies, context.prospect)

    return build_message(strategy, context)
```

### Pain Awareness Phase
```python
def generate_pain_message(context):
    """Generate message to amplify pain awareness"""

    # Reference their stated pain
    stated_pain = context.get("stated_pain_points", [])

    if stated_pain:
        # Amplify with consequences
        message = amplify_pain(stated_pain[0], context)
    else:
        # Probe for pain
        message = generate_pain_probe(context)

    return message

def amplify_pain(pain_point, context):
    """Amplify awareness of pain consequences"""

    amplification_patterns = {
        "time_waste": "How much time does your team lose to {pain} each week? For most {role}s I talk to, it's 5-10 hours that could go toward {priority}.",
        "revenue_impact": "Have you calculated what {pain} costs in lost {metric}? Companies your size typically see {impact_estimate}.",
        "competitive_risk": "While you're dealing with {pain}, competitors using {solution_type} are already {competitive_advantage}.",
        "team_friction": "Beyond the direct impact, how does {pain} affect your team's morale and velocity?"
    }

    pattern_type = classify_pain_type(pain_point)
    pattern = amplification_patterns.get(pattern_type, amplification_patterns["time_waste"])

    return fill_template(pattern, context)
```

### Desire Phase
```python
def generate_desire_message(context):
    """Generate message to create desire for solution"""

    # Paint the picture of success
    success_vision = create_success_vision(context)

    # Make it specific to them
    personalized_vision = personalize_vision(success_vision, context.prospect)

    # Add social proof
    proof = get_relevant_proof(context)

    message = f"""
    {personalized_vision}

    {proof['company']} achieved this in {proof['timeframe']}.
    The key was {proof['key_factor']}.
    """

    return message.strip()

def create_success_vision(context):
    """Create vision of successful outcome"""

    pain_points = context.get("stated_pain_points", [])
    goals = context.get("stated_goals", [])

    if goals:
        primary_goal = goals[0]
        vision = f"Imagine hitting {primary_goal} ahead of schedule"
    elif pain_points:
        primary_pain = pain_points[0]
        vision = f"Imagine {primary_pain} being completely solved"
    else:
        vision = f"Imagine your {context.prospect.role} responsibilities becoming dramatically easier"

    return vision
```

### Confidence Phase
```python
def generate_confidence_message(context):
    """Generate message to build confidence"""

    # Address any expressed concerns
    concerns = context.get("expressed_concerns", [])

    if concerns:
        # Directly address top concern
        concern_response = address_concern(concerns[0], context)
        return concern_response

    # Proactively build confidence
    confidence_builders = [
        {
            "type": "social_proof",
            "message": generate_social_proof(context, focus="similar_company")
        },
        {
            "type": "risk_reversal",
            "message": generate_risk_reversal(context)
        },
        {
            "type": "implementation_ease",
            "message": generate_ease_message(context)
        },
        {
            "type": "support_assurance",
            "message": generate_support_message(context)
        }
    ]

    # Select based on prospect's likely concerns
    builder = select_confidence_builder(confidence_builders, context)
    return builder["message"]
```

## Arc Optimization

### Phase Transition
```python
class PhaseTransitionManager:
    def __init__(self):
        self.transition_rules = {}

    def should_transition(self, current_phase, context, emotional_state):
        """Determine if ready to move to next phase"""

        phase_config = EmotionalArc.PHASES[current_phase]

        # Check success signals
        signals_present = [
            s for s in phase_config["success_signals"]
            if s in emotional_state["phase_signals"]
        ]

        if not signals_present:
            return {
                "ready": False,
                "reason": "Success signals not detected",
                "recommendation": "Reinforce current phase"
            }

        # Check emotional state
        emotions = emotional_state["detected_emotions"]
        target_emotions = phase_config["target_emotions"]
        emotion_alignment = any(e in target_emotions for e in emotions)

        if not emotion_alignment:
            return {
                "ready": False,
                "reason": "Emotional state not aligned",
                "recommendation": "Adjust approach to target emotions"
            }

        # Check for negative indicators
        if emotional_state["sentiment_score"] < 0:
            return {
                "ready": False,
                "reason": "Negative sentiment detected",
                "recommendation": "Address concerns before progressing"
            }

        return {
            "ready": True,
            "next_phase": self.get_next_phase(current_phase),
            "recommended_approach": self.get_transition_approach(current_phase)
        }

    def get_next_phase(self, current_phase):
        phases = list(EmotionalArc.PHASES.keys())
        current_index = phases.index(current_phase)
        if current_index < len(phases) - 1:
            return phases[current_index + 1]
        return current_phase  # Stay at commitment

    def handle_regression(self, from_phase, to_phase, context):
        """Handle when conversation regresses to earlier phase"""

        regression_strategies = {
            ("desire", "pain_awareness"): "Re-establish hope with stronger proof",
            ("confidence", "desire"): "Address hidden objection",
            ("commitment", "confidence"): "Provide additional assurance"
        }

        strategy = regression_strategies.get(
            (from_phase, to_phase),
            "Acknowledge and rebuild"
        )

        return {
            "strategy": strategy,
            "recommended_message": generate_recovery_message(from_phase, to_phase, context)
        }
```

### Arc Pacing
```python
def calculate_optimal_pacing(context):
    """Determine optimal pacing through the arc"""

    factors = {
        "urgency_level": context.prospect.urgency,
        "engagement_level": context.engagement_score,
        "complexity": context.deal_complexity,
        "stakeholder_count": len(context.stakeholders)
    }

    # High urgency + high engagement = faster pace
    if factors["urgency_level"] > 0.7 and factors["engagement_level"] > 0.7:
        return {
            "pace": "accelerated",
            "messages_per_phase": 1,
            "skip_phases": ["pain_awareness"]  # They already know their pain
        }

    # Low engagement = slower, more nurturing
    if factors["engagement_level"] < 0.4:
        return {
            "pace": "nurturing",
            "messages_per_phase": 3,
            "emphasis_phases": ["curiosity", "recognition"]
        }

    # Complex deal = thorough
    if factors["complexity"] > 0.7:
        return {
            "pace": "thorough",
            "messages_per_phase": 2,
            "add_phases": ["validation", "stakeholder_alignment"]
        }

    return {
        "pace": "standard",
        "messages_per_phase": 2,
        "skip_phases": []
    }
```

## Emotion Detection

### Signal Analysis
```python
def detect_emotions(message):
    """Detect emotional signals in message"""

    emotion_indicators = {
        "interested": [
            r"tell me more",
            r"curious",
            r"interesting",
            r"how does"
        ],
        "frustrated": [
            r"struggling with",
            r"annoying",
            r"waste.*time",
            r"tired of"
        ],
        "skeptical": [
            r"not sure",
            r"sounds too",
            r"how is this different",
            r"what's the catch"
        ],
        "excited": [
            r"love to",
            r"can't wait",
            r"exactly what",
            r"this is great"
        ],
        "hesitant": [
            r"maybe",
            r"let me think",
            r"not right now",
            r"need to check"
        ],
        "confident": [
            r"makes sense",
            r"let's do",
            r"ready to",
            r"i'm in"
        ]
    }

    detected = []
    for emotion, patterns in emotion_indicators.items():
        for pattern in patterns:
            if re.search(pattern, message.text, re.IGNORECASE):
                detected.append(emotion)
                break

    return list(set(detected))
```

## Metrics

### Arc Performance
```
Track:
- Average arc completion rate
- Phase-to-phase conversion rates
- Regression frequency
- Time in each phase
- Arc completion to conversion correlation

Optimize for:
- Smooth progression (minimal regression)
- Phase timing optimization
- Emotion alignment at each phase
```

