---
name: human-in-the-loop-training
description: When the user wants to build or improve a sales bot's ability to learn from human corrections and feedback. Also use when the user mentions "human feedback," "HITL," "human-in-the-loop," "feedback learning," or "correction learning."
---

# Human-in-the-Loop Training

You are an expert in building sales bots that continuously improve through human feedback and corrections. Your goal is to help developers create systems that learn from human expertise to improve automated responses.

## Why Human-in-the-Loop Matters

### The Plateau Problem
```
Without human feedback:
- Bot makes same mistakes repeatedly
- Edge cases never improve
- Quality plateaus quickly
- No domain expertise transfer

With human feedback:
- Mistakes become training data
- Edge cases get handled
- Continuous improvement
- Human expertise scales
```

### The Feedback Loop
```
Bot Response → Human Reviews →
Correction Applied → Bot Learns →
Better Responses → Human Reviews →
...

Each correction makes the bot
permanently smarter.
```

## Feedback Collection

### Review Interface
```python
class HumanReviewQueue:
    def __init__(self):
        self.queue = []
        self.reviewers = {}

    def add_for_review(self, item, reason, priority="medium"):
        """Queue item for human review"""

        review_item = {
            "id": generate_id(),
            "item": item,
            "reason": reason,
            "priority": priority,
            "queued_at": datetime.now(),
            "status": "pending",
            "context": gather_context(item)
        }

        self.queue.append(review_item)
        self.notify_reviewers(review_item)

        return review_item["id"]

    def submit_review(self, review_id, reviewer_id, feedback):
        """Process human review submission"""

        review_item = self.get_review(review_id)

        review_result = {
            "review_id": review_id,
            "reviewer_id": reviewer_id,
            "reviewed_at": datetime.now(),
            "feedback_type": feedback["type"],
            "original": review_item["item"],
            "correction": feedback.get("correction"),
            "rating": feedback.get("rating"),
            "notes": feedback.get("notes"),
            "should_learn": feedback.get("should_learn", True)
        }

        # Process the feedback
        if feedback["type"] == "correction":
            self.process_correction(review_item, feedback)
        elif feedback["type"] == "approval":
            self.process_approval(review_item, feedback)
        elif feedback["type"] == "rejection":
            self.process_rejection(review_item, feedback)

        review_item["status"] = "completed"
        review_item["result"] = review_result

        return review_result


# Reasons for review
REVIEW_TRIGGERS = {
    "low_confidence": {
        "threshold": 0.6,
        "priority": "high",
        "description": "Bot confidence below threshold"
    },
    "negative_sentiment": {
        "threshold": -0.3,
        "priority": "high",
        "description": "Prospect showing negative sentiment"
    },
    "new_objection": {
        "priority": "medium",
        "description": "Objection not seen before"
    },
    "high_value_account": {
        "priority": "high",
        "description": "Account value above threshold"
    },
    "escalation_request": {
        "priority": "urgent",
        "description": "Prospect requested human contact"
    },
    "random_sample": {
        "sample_rate": 0.05,
        "priority": "low",
        "description": "Random quality check"
    }
}
```

### Feedback Types
```python
class FeedbackCollector:
    def __init__(self):
        self.feedback_types = [
            "correction",      # Human provides better response
            "rating",          # Score the bot's response
            "annotation",      # Label specific issues
            "approval",        # Confirm response is good
            "rejection",       # Response should not be sent
            "suggestion"       # Ideas for improvement
        ]

    def collect_correction(self, original_message, context):
        """Collect human correction for bot response"""

        return {
            "type": "correction",
            "original_message": original_message,
            "context": {
                "conversation_id": context.conversation_id,
                "prospect_info": context.prospect,
                "conversation_history": context.messages[-10:],
                "bot_reasoning": context.get("reasoning")
            },
            "fields": {
                "corrected_message": "string",
                "correction_reason": "string",
                "issue_categories": "multi_select",
                "severity": "select",
                "should_learn": "boolean"
            }
        }

    def collect_rating(self, message, context):
        """Collect quality rating"""

        return {
            "type": "rating",
            "message": message,
            "fields": {
                "overall_quality": "scale_1_5",
                "tone_appropriateness": "scale_1_5",
                "relevance": "scale_1_5",
                "clarity": "scale_1_5",
                "would_send": "boolean",
                "improvement_notes": "string"
            }
        }

    def collect_annotation(self, message, context):
        """Collect specific annotations"""

        annotation_labels = [
            "too_formal",
            "too_casual",
            "too_long",
            "too_short",
            "off_topic",
            "factually_incorrect",
            "missing_context",
            "wrong_tone",
            "good_example"
        ]

        return {
            "type": "annotation",
            "message": message,
            "available_labels": annotation_labels,
            "allow_multiple": True,
            "require_justification": True
        }
```

## Learning Pipeline

### Correction Processing
```python
class LearningPipeline:
    def __init__(self):
        self.training_buffer = []
        self.model_version = 0
        self.min_samples_for_training = 100

    def process_correction(self, original, corrected, context, metadata):
        """Process human correction into training data"""

        training_example = {
            "input": {
                "conversation_history": context.messages,
                "prospect_info": context.prospect,
                "current_stage": context.stage,
                "trigger": context.trigger
            },
            "original_output": original,
            "corrected_output": corrected,
            "correction_metadata": {
                "reviewer_id": metadata["reviewer_id"],
                "correction_type": metadata["correction_type"],
                "issue_categories": metadata.get("issue_categories", []),
                "timestamp": datetime.now()
            }
        }

        # Validate correction quality
        if self.validate_correction(training_example):
            self.training_buffer.append(training_example)

        # Check if ready to train
        if len(self.training_buffer) >= self.min_samples_for_training:
            self.trigger_training()

        return training_example

    def validate_correction(self, example):
        """Validate correction is suitable for training"""

        # Check correction is meaningfully different
        similarity = calculate_similarity(
            example["original_output"],
            example["corrected_output"]
        )
        if similarity > 0.95:
            return False  # Too similar, not useful

        # Check correction is complete
        if len(example["corrected_output"]) < 10:
            return False  # Too short

        # Check reviewer reliability
        reviewer_stats = get_reviewer_stats(
            example["correction_metadata"]["reviewer_id"]
        )
        if reviewer_stats["agreement_rate"] < 0.7:
            return False  # Reviewer often overruled

        return True

    def trigger_training(self):
        """Trigger model retraining with new examples"""

        # Prepare training batch
        training_batch = self.prepare_training_batch()

        # Fine-tune or update model
        training_job = submit_training_job(
            training_batch,
            base_model=f"model_v{self.model_version}"
        )

        return training_job
```

### Pattern Learning
```python
class PatternLearner:
    def __init__(self):
        self.patterns = {}
        self.pattern_threshold = 3  # Minimum occurrences

    def extract_patterns(self, corrections):
        """Extract learnable patterns from corrections"""

        patterns = defaultdict(list)

        for correction in corrections:
            # Extract what was wrong
            issues = analyze_correction_diff(
                correction["original_output"],
                correction["corrected_output"]
            )

            for issue in issues:
                pattern_key = issue["pattern_type"]
                patterns[pattern_key].append({
                    "original": issue["original_text"],
                    "corrected": issue["corrected_text"],
                    "context": correction["input"]
                })

        # Consolidate patterns
        consolidated = {}
        for pattern_type, examples in patterns.items():
            if len(examples) >= self.pattern_threshold:
                consolidated[pattern_type] = {
                    "examples": examples,
                    "count": len(examples),
                    "rule": self.derive_rule(examples)
                }

        return consolidated

    def derive_rule(self, examples):
        """Derive a rule from correction examples"""

        # Use LLM to generate rule
        prompt = f"""
        Analyze these correction examples and derive a general rule:

        Examples:
        {format_examples(examples[:10])}

        Generate a rule in this format:
        - When: [situation description]
        - Instead of: [pattern to avoid]
        - Do: [correct pattern]
        - Reason: [why this is better]
        """

        rule = llm.generate(prompt)
        return parse_rule(rule)


def analyze_correction_diff(original, corrected):
    """Analyze what changed between original and correction"""

    issues = []

    # Tone changes
    original_tone = analyze_tone(original)
    corrected_tone = analyze_tone(corrected)
    if original_tone != corrected_tone:
        issues.append({
            "pattern_type": "tone_adjustment",
            "original_text": original,
            "corrected_text": corrected,
            "detail": f"Changed from {original_tone} to {corrected_tone}"
        })

    # Length changes
    length_change = len(corrected) / len(original) if original else 1
    if length_change < 0.7:
        issues.append({
            "pattern_type": "over_verbose",
            "original_text": original,
            "corrected_text": corrected
        })
    elif length_change > 1.5:
        issues.append({
            "pattern_type": "under_detailed",
            "original_text": original,
            "corrected_text": corrected
        })

    # Content additions
    added_content = find_additions(original, corrected)
    if added_content:
        issues.append({
            "pattern_type": "missing_content",
            "original_text": original,
            "corrected_text": corrected,
            "additions": added_content
        })

    return issues
```

## Active Learning

### Smart Sampling
```python
class ActiveLearningSelector:
    def __init__(self):
        self.uncertainty_threshold = 0.6
        self.diversity_weight = 0.3

    def select_for_review(self, candidates, budget):
        """Select most valuable items for human review"""

        scored_candidates = []

        for candidate in candidates:
            score = self.calculate_learning_value(candidate)
            scored_candidates.append((candidate, score))

        # Sort by learning value
        scored_candidates.sort(key=lambda x: x[1], reverse=True)

        # Select diverse sample
        selected = self.select_diverse_sample(
            scored_candidates,
            budget
        )

        return selected

    def calculate_learning_value(self, candidate):
        """Calculate how valuable this item is for learning"""

        value = 0

        # Uncertainty value - items bot is unsure about
        confidence = candidate.get("confidence", 1.0)
        uncertainty = 1 - confidence
        value += uncertainty * 0.4

        # Novelty value - items unlike training data
        novelty = calculate_novelty(candidate, self.training_data)
        value += novelty * 0.3

        # Impact value - items affecting many similar cases
        impact = estimate_impact(candidate)
        value += impact * 0.2

        # Diversity value - coverage of different scenarios
        diversity = calculate_diversity_contribution(candidate, self.selected)
        value += diversity * 0.1

        return value

    def select_diverse_sample(self, scored_candidates, budget):
        """Select diverse sample within budget"""

        selected = []
        covered_clusters = set()

        for candidate, score in scored_candidates:
            if len(selected) >= budget:
                break

            # Get candidate's cluster
            cluster = get_cluster(candidate)

            # Prefer uncovered clusters
            if cluster not in covered_clusters:
                selected.append(candidate)
                covered_clusters.add(cluster)
            elif score > self.uncertainty_threshold:
                # Include high-value even if cluster covered
                selected.append(candidate)

        return selected
```

### Reviewer Management
```python
class ReviewerManager:
    def __init__(self):
        self.reviewers = {}
        self.specializations = {}

    def register_reviewer(self, reviewer_id, profile):
        """Register human reviewer"""

        self.reviewers[reviewer_id] = {
            "profile": profile,
            "specializations": profile.get("specializations", []),
            "availability": profile.get("availability", "full"),
            "stats": {
                "reviews_completed": 0,
                "agreement_rate": None,
                "avg_review_time": None
            }
        }

    def assign_review(self, review_item):
        """Assign review to best available reviewer"""

        # Find matching reviewers
        matching = []
        for reviewer_id, reviewer in self.reviewers.items():
            if not self.is_available(reviewer_id):
                continue

            match_score = self.calculate_match(reviewer, review_item)
            matching.append((reviewer_id, match_score))

        if not matching:
            return None

        # Select best match
        matching.sort(key=lambda x: x[1], reverse=True)
        return matching[0][0]

    def calculate_match(self, reviewer, review_item):
        """Calculate how well reviewer matches item"""

        score = 0

        # Specialization match
        item_category = review_item.get("category")
        if item_category in reviewer["specializations"]:
            score += 0.4

        # Experience with similar items
        similar_reviews = count_similar_reviews(
            reviewer,
            review_item
        )
        score += min(similar_reviews / 100, 0.3)

        # Quality of past reviews
        if reviewer["stats"]["agreement_rate"]:
            score += reviewer["stats"]["agreement_rate"] * 0.3

        return score

    def update_reviewer_stats(self, reviewer_id, review_result):
        """Update reviewer statistics"""

        stats = self.reviewers[reviewer_id]["stats"]
        stats["reviews_completed"] += 1

        # Update agreement rate
        agreement = check_agreement(review_result)
        old_rate = stats["agreement_rate"] or 0.5
        n = stats["reviews_completed"]
        stats["agreement_rate"] = (old_rate * (n-1) + agreement) / n
```

## Model Updates

### Incremental Learning
```python
class IncrementalLearner:
    def __init__(self, base_model):
        self.base_model = base_model
        self.correction_buffer = []
        self.rule_additions = []

    def apply_correction_immediately(self, correction):
        """Apply correction without full retraining"""

        # Add to prompt examples
        example = format_as_few_shot(correction)
        self.few_shot_examples.append(example)

        # Update rules if pattern detected
        if correction.get("derived_rule"):
            self.rule_additions.append(correction["derived_rule"])

        # Buffer for batch training
        self.correction_buffer.append(correction)

    def generate_with_corrections(self, prompt, context):
        """Generate response using corrections"""

        # Check for relevant corrections
        relevant_corrections = self.find_relevant_corrections(context)

        # Build enhanced prompt
        enhanced_prompt = f"""
        {prompt}

        Recent corrections for similar situations:
        {format_corrections(relevant_corrections)}

        Apply these learnings to your response.
        """

        return self.base_model.generate(enhanced_prompt)

    def should_retrain(self):
        """Determine if full retraining is needed"""

        return (
            len(self.correction_buffer) >= 100 or
            self.performance_degraded() or
            self.significant_pattern_shift()
        )
```

## Metrics

### Learning Effectiveness
```
Track:
- Correction rate over time (should decrease)
- Same-mistake rate (should be near 0)
- Reviewer agreement rate
- Time to incorporate feedback
- Model performance after updates

Goals:
- <5% correction rate after 1000 reviews
- <1% repeated mistakes
- >85% reviewer agreement
```

