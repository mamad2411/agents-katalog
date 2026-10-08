---
name: ideal-customer-profile-matching
description: When the user wants to build or improve a sales bot's ability to compare prospects against best customer profiles. Also use when the user mentions "ICP matching," "ideal customer," "customer fit scoring," "profile matching," or "lookalike scoring."
---

# Ideal Customer Profile Matching

You are an expert in building sales bots that compare prospect signals against ideal customer profiles. Your goal is to help developers create systems that identify prospects most similar to their best existing customers.

## Why ICP Matching Matters

### The Qualification Problem
```
Without ICP matching:
- Treat all prospects the same
- Can't prioritize effectively
- Waste time on poor fits
- Miss similar-to-winners

With ICP matching:
- Score fit against known winners
- Prioritize high-ICP prospects
- Focus resources efficiently
- Find more customers like best ones
```

## ICP Definition

### Building Your ICP
```python
def build_icp_from_customers():
    # Get best customers
    best_customers = get_top_customers(
        criteria="revenue_and_retention",
        percentile=20  # Top 20%
    )

    # Extract common attributes
    icp = {
        "firmographics": {
            "company_size": extract_distribution(best_customers, "employees"),
            "revenue_range": extract_distribution(best_customers, "revenue"),
            "industry": extract_frequency(best_customers, "industry"),
            "geography": extract_frequency(best_customers, "region"),
            "growth_stage": extract_frequency(best_customers, "stage")
        },
        "technographics": {
            "tech_stack": extract_frequency(best_customers, "technologies"),
            "integrations": extract_frequency(best_customers, "integrations_used")
        },
        "behavioral": {
            "buying_process": extract_patterns(best_customers, "sales_cycle"),
            "use_cases": extract_frequency(best_customers, "primary_use_case"),
            "entry_point": extract_frequency(best_customers, "initial_product")
        },
        "success_indicators": {
            "time_to_value": median(best_customers, "time_to_first_value"),
            "expansion_rate": median(best_customers, "expansion_revenue_pct"),
            "nps": median(best_customers, "nps_score")
        }
    }

    return icp
```

### ICP Tiers
```
Tier 1 (Perfect fit):
- Company size: 200-2000 employees
- Industry: SaaS, FinTech, Healthcare Tech
- Revenue: $20M-$200M
- Tech stack: Salesforce + modern marketing tools
- Growth stage: Series B-D

Tier 2 (Good fit):
- Company size: 50-200 OR 2000-5000
- Industry: Professional services, E-commerce
- Revenue: $5M-$20M OR $200M-$500M
- Growth stage: Series A or post-IPO

Tier 3 (Possible fit):
- Company size: 20-50 OR 5000+
- Industry: Other B2B
- Revenue: $1M-$5M OR $500M+
- Non-standard tech stack
```

## ICP Scoring

### Attribute Matching
```python
def calculate_icp_score(prospect, icp):
    scores = {}
    weights = {
        "company_size": 0.20,
        "industry": 0.15,
        "revenue": 0.15,
        "tech_stack": 0.15,
        "use_case_fit": 0.15,
        "growth_signals": 0.10,
        "geography": 0.10
    }

    # Company size match
    size_range = icp["firmographics"]["company_size"]
    if size_range["min"] <= prospect.employees <= size_range["max"]:
        scores["company_size"] = 100
    elif size_range["min"] * 0.5 <= prospect.employees <= size_range["max"] * 1.5:
        scores["company_size"] = 70
    else:
        scores["company_size"] = 30

    # Industry match
    if prospect.industry in icp["firmographics"]["industry"]["tier_1"]:
        scores["industry"] = 100
    elif prospect.industry in icp["firmographics"]["industry"]["tier_2"]:
        scores["industry"] = 70
    else:
        scores["industry"] = 30

    # Tech stack match
    tech_overlap = len(set(prospect.tech_stack) & set(icp["technographics"]["tech_stack"]["common"]))
    tech_total = len(icp["technographics"]["tech_stack"]["common"])
    scores["tech_stack"] = (tech_overlap / tech_total) * 100

    # Use case fit
    scores["use_case_fit"] = calculate_use_case_fit(prospect, icp)

    # Weighted total
    total_score = sum(scores[k] * weights[k] for k in scores)

    return {
        "total_score": total_score,
        "component_scores": scores,
        "icp_tier": get_tier(total_score)
    }

def get_tier(score):
    if score >= 80:
        return "tier_1"
    elif score >= 60:
        return "tier_2"
    elif score >= 40:
        return "tier_3"
    else:
        return "poor_fit"
```

### Machine Learning Approach
```python
from sklearn.ensemble import RandomForestClassifier

def train_icp_model():
    # Get labeled data
    customers = get_all_customers()
    labels = [1 if c.ltv_percentile >= 80 else 0 for c in customers]

    # Extract features
    features = extract_features(customers)

    # Train model
    model = RandomForestClassifier()
    model.fit(features, labels)

    return model

def score_prospect_ml(prospect, model):
    features = extract_features([prospect])
    probability = model.predict_proba(features)[0][1]

    return {
        "icp_probability": probability,
        "icp_tier": probability_to_tier(probability),
        "feature_importance": get_important_features(model, prospect)
    }
```

## Real-Time ICP Assessment

### Conversation-Based Scoring
```python
def update_icp_during_conversation(prospect, message):
    # Extract signals from conversation
    signals = extract_conversation_signals(message)

    icp_updates = {}

    # Use case revealed
    if signals.get("use_case"):
        use_case_fit = match_use_case_to_icp(signals["use_case"])
        icp_updates["use_case_fit"] = use_case_fit

    # Tech stack mentioned
    if signals.get("technologies"):
        tech_overlap = calculate_tech_overlap(signals["technologies"])
        icp_updates["tech_stack"] = tech_overlap

    # Team size mentioned
    if signals.get("team_size"):
        icp_updates["team_size_match"] = match_team_size(signals["team_size"])

    # Budget signals
    if signals.get("budget_range"):
        icp_updates["budget_fit"] = match_budget_to_icp(signals["budget_range"])

    # Update prospect's ICP score
    recalculate_icp_score(prospect, icp_updates)
```

### Dynamic ICP Signals
```
Conversation signals that inform ICP:

High fit signals:
- "We have a [target size] team"
- "Currently using [ICP tech stack]"
- "Our main challenge is [ICP use case]"
- "Budget is [in ICP range]"
- "Need to solve this by [reasonable timeline]"

Lower fit signals:
- "Just me/small team"
- "Don't have budget yet"
- "Just researching for now"
- "Our use case is [non-standard]"
- "Using [incompatible tech]"
```

## ICP-Based Actions

### Routing by ICP
```python
def route_by_icp(prospect):
    icp_tier = prospect.icp_tier

    if icp_tier == "tier_1":
        return {
            "queue": "enterprise_fast_track",
            "assignee": get_best_available_ae(),
            "sla": "respond_within_1_hour",
            "treatment": "white_glove"
        }
    elif icp_tier == "tier_2":
        return {
            "queue": "standard_sales",
            "assignee": "round_robin_ae",
            "sla": "respond_within_4_hours",
            "treatment": "standard"
        }
    elif icp_tier == "tier_3":
        return {
            "queue": "qualification_needed",
            "assignee": "sdr",
            "sla": "respond_within_24_hours",
            "treatment": "qualify_further"
        }
    else:
        return {
            "queue": "nurture",
            "assignee": "bot",
            "sla": "automated",
            "treatment": "self_service_focused"
        }
```

### Messaging by ICP
```python
def customize_message_for_icp(base_message, prospect):
    icp_tier = prospect.icp_tier

    if icp_tier == "tier_1":
        # Premium messaging
        return enhance_message(base_message,
            add_enterprise_features=True,
            add_dedicated_support=True,
            add_similar_customers=get_similar_reference_customers(prospect),
            tone="consultative"
        )
    elif icp_tier == "tier_2":
        # Standard messaging
        return enhance_message(base_message,
            add_case_studies=True,
            add_roi_focus=True,
            tone="professional"
        )
    else:
        # Self-service focus
        return enhance_message(base_message,
            add_free_trial=True,
            add_self_service_resources=True,
            tone="helpful"
        )
```

## ICP Visualization

### Fit Matrix
```
                    High Engagement | Low Engagement
High ICP Fit        PRIORITY 1      | RE-ENGAGE
                    (best prospects)| (sleeping giants)
---------------------------------------------------
Low ICP Fit         EVALUATE        | DEPRIORITIZE
                    (could surprise)| (poor fit)

Segment prospects into quadrants for prioritization.
```

### ICP Comparison Report
```python
def generate_icp_comparison(prospect):
    icp = get_current_icp()
    score = prospect.icp_score

    return {
        "overall_fit": score.total_score,
        "tier": score.icp_tier,
        "comparison": {
            "company_size": {
                "prospect": prospect.employees,
                "icp_range": icp["firmographics"]["company_size"],
                "match": score.component_scores["company_size"]
            },
            "industry": {
                "prospect": prospect.industry,
                "icp_industries": icp["firmographics"]["industry"],
                "match": score.component_scores["industry"]
            },
            # ... more dimensions
        },
        "similar_customers": get_similar_won_customers(prospect, limit=3),
        "fit_summary": generate_fit_summary(score)
    }
```

## ICP Evolution

### Updating ICP Over Time
```python
def refresh_icp(cadence="quarterly"):
    # Get recent best customers
    recent_best = get_top_customers(
        timeframe="last_12_months",
        criteria="revenue_and_retention",
        percentile=20
    )

    # Compare to existing ICP
    current_icp = get_current_icp()
    new_icp = build_icp_from_customers(recent_best)

    # Identify changes
    changes = compare_icps(current_icp, new_icp)

    if significant_changes(changes):
        # Update ICP
        update_icp(new_icp)
        notify_team("ICP updated", changes)

        # Re-score existing prospects
        rescore_all_prospects(new_icp)
```

### Market Expansion
```python
def identify_adjacent_icps():
    """Find secondary ICPs for expansion"""

    # Successful customers outside primary ICP
    outliers = get_successful_outliers()

    # Cluster into secondary ICPs
    secondary_icps = cluster_customers(outliers)

    for cluster in secondary_icps:
        if cluster.size >= MIN_VIABLE_SEGMENT:
            create_secondary_icp(cluster)

    return secondary_icps
```

