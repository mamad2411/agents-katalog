---
name: multi-stakeholder-thread-management
description: When the user wants to build or improve a sales bot's ability to handle conversations involving multiple decision-makers. Also use when the user mentions "multi-stakeholder," "buying committee," "multiple contacts," "group selling," or "consensus building."
---

# Multi-Stakeholder Thread Management

You are an expert in building sales bots that handle conversations involving multiple decision-makers. Your goal is to help developers create systems that track, coordinate, and advance conversations across buying committees.

## Why Multi-Stakeholder Management Matters

### The Complex Deal Reality
```
Modern B2B deals:
- Average 6-10 people in buying decision
- Multiple perspectives and priorities
- Different information needs
- Consensus often required

Single-threaded approach:
- Rely on one champion
- Miss other stakeholders
- Blind to objections elsewhere
- Deal stalls mysteriously
```

### Multi-Threaded Approach
```
Managed stakeholder engagement:
- Map all decision participants
- Understand each person's priorities
- Address concerns individually
- Build consensus systematically

Result: Faster deals, fewer surprises
```

## Stakeholder Mapping

### Identifying Stakeholders
```python
class StakeholderMap:
    def __init__(self, deal_id):
        self.deal_id = deal_id
        self.stakeholders = []

    def add_stakeholder(self, stakeholder):
        self.stakeholders.append({
            "id": generate_id(),
            "name": stakeholder["name"],
            "title": stakeholder["title"],
            "role": classify_role(stakeholder),  # champion, buyer, user, etc.
            "influence": stakeholder.get("influence", "unknown"),
            "sentiment": stakeholder.get("sentiment", "neutral"),
            "priorities": stakeholder.get("priorities", []),
            "objections": stakeholder.get("objections", []),
            "engagement_level": 0,
            "last_contact": None,
            "preferred_channel": stakeholder.get("channel", "email")
        })

def classify_role(stakeholder):
    title = stakeholder["title"].lower()

    if any(x in title for x in ["ceo", "cfo", "cto", "president", "owner"]):
        return "economic_buyer"
    elif any(x in title for x in ["vp", "director", "head of"]):
        return "decision_maker"
    elif any(x in title for x in ["manager", "lead"]):
        return "influencer"
    elif any(x in title for x in ["analyst", "specialist", "coordinator"]):
        return "user"
    else:
        return "unknown"
```

### Stakeholder Discovery
```python
def discover_stakeholders_from_conversation(message, existing_map):
    # Look for mentions of other people
    mentions = extract_person_mentions(message)

    for mention in mentions:
        # "My boss Sarah"
        # "Our CTO will need to review"
        # "The finance team"

        if mention not in existing_map:
            stakeholder = {
                "name": mention.get("name", "Unknown"),
                "title": mention.get("title", "Unknown"),
                "relationship": mention.get("relationship"),  # boss, colleague, etc.
                "mentioned_by": message.sender,
                "discovered_from": message.content
            }
            existing_map.add_stakeholder(stakeholder)

    return existing_map
```

## Conversation Tracking

### Per-Stakeholder Context
```python
class StakeholderConversation:
    def __init__(self, stakeholder_id, deal_id):
        self.stakeholder_id = stakeholder_id
        self.deal_id = deal_id
        self.messages = []
        self.topics_discussed = []
        self.questions_asked = []
        self.objections_raised = []
        self.commitments_made = []
        self.information_shared = []

    def add_interaction(self, interaction):
        self.messages.append(interaction)

        # Extract context
        if interaction.get("questions"):
            self.questions_asked.extend(interaction["questions"])
        if interaction.get("objections"):
            self.objections_raised.extend(interaction["objections"])
        if interaction.get("commitments"):
            self.commitments_made.extend(interaction["commitments"])

    def get_state(self):
        return {
            "last_contact": self.messages[-1]["timestamp"] if self.messages else None,
            "engagement_count": len(self.messages),
            "open_questions": [q for q in self.questions_asked if not q.get("answered")],
            "unresolved_objections": [o for o in self.objections_raised if not o.get("resolved")],
            "sentiment_trend": calculate_sentiment_trend(self.messages)
        }
```

### Cross-Stakeholder View
```python
def get_deal_stakeholder_summary(deal_id):
    stakeholder_map = get_stakeholder_map(deal_id)

    summary = {
        "total_stakeholders": len(stakeholder_map.stakeholders),
        "by_role": {},
        "engagement": {},
        "risks": []
    }

    for stakeholder in stakeholder_map.stakeholders:
        role = stakeholder["role"]
        summary["by_role"][role] = summary["by_role"].get(role, 0) + 1

        conv = get_stakeholder_conversation(stakeholder["id"], deal_id)
        state = conv.get_state()

        summary["engagement"][stakeholder["name"]] = {
            "level": state["engagement_count"],
            "sentiment": stakeholder["sentiment"],
            "last_contact": state["last_contact"]
        }

        # Identify risks
        if state["unresolved_objections"]:
            summary["risks"].append({
                "stakeholder": stakeholder["name"],
                "type": "unresolved_objection",
                "details": state["unresolved_objections"]
            })

        if stakeholder["sentiment"] == "negative":
            summary["risks"].append({
                "stakeholder": stakeholder["name"],
                "type": "negative_sentiment"
            })

    return summary
```

## Coordination Strategies

### Information Consistency
```python
def ensure_consistency(deal_id, message, recipient):
    """Ensure information is consistent across stakeholders"""

    # Get what we've told other stakeholders
    other_conversations = get_all_stakeholder_conversations(deal_id)

    # Check for potential conflicts
    for conv in other_conversations:
        if conv.stakeholder_id != recipient.id:
            conflicts = detect_information_conflicts(
                new_message=message,
                existing_conversation=conv
            )

            if conflicts:
                # Flag for review or auto-reconcile
                handle_conflict(conflicts, message, conv)

    return message
```

### Role-Appropriate Messaging
```python
def customize_for_role(base_message, stakeholder):
    role = stakeholder["role"]

    customizations = {
        "economic_buyer": {
            "focus": ["roi", "risk", "strategic_fit"],
            "detail_level": "executive_summary",
            "cta": "Worth a brief discussion on strategic fit?"
        },
        "decision_maker": {
            "focus": ["value", "implementation", "support"],
            "detail_level": "moderate",
            "cta": "Want to dive deeper into how this works?"
        },
        "influencer": {
            "focus": ["features", "workflow", "team_impact"],
            "detail_level": "detailed",
            "cta": "Would a demo for your team be helpful?"
        },
        "user": {
            "focus": ["usability", "training", "daily_workflow"],
            "detail_level": "practical",
            "cta": "Want to try it yourself?"
        }
    }

    config = customizations.get(role, customizations["influencer"])
    return adapt_message(base_message, config)
```

### Stakeholder-Specific Objections
```python
def track_and_address_objections(deal_id):
    stakeholder_map = get_stakeholder_map(deal_id)

    objection_matrix = {}
    for stakeholder in stakeholder_map.stakeholders:
        conv = get_stakeholder_conversation(stakeholder["id"], deal_id)
        objection_matrix[stakeholder["name"]] = conv.objections_raised

    # Identify common objections
    common = find_common_objections(objection_matrix)

    # Identify unique objections
    unique = find_unique_objections(objection_matrix)

    return {
        "common_objections": common,  # Address broadly
        "unique_objections": unique,   # Address individually
        "recommended_actions": generate_objection_actions(common, unique)
    }
```

## Consensus Building

### Alignment Tracking
```python
def assess_buying_committee_alignment(deal_id):
    stakeholder_map = get_stakeholder_map(deal_id)

    alignment = {
        "champions": [],
        "supporters": [],
        "neutral": [],
        "skeptics": [],
        "blockers": []
    }

    for stakeholder in stakeholder_map.stakeholders:
        sentiment = stakeholder["sentiment"]
        if sentiment == "very_positive":
            alignment["champions"].append(stakeholder)
        elif sentiment == "positive":
            alignment["supporters"].append(stakeholder)
        elif sentiment == "neutral":
            alignment["neutral"].append(stakeholder)
        elif sentiment == "negative":
            alignment["skeptics"].append(stakeholder)
        elif sentiment == "very_negative":
            alignment["blockers"].append(stakeholder)

    # Calculate alignment score
    weights = {"champions": 2, "supporters": 1, "neutral": 0, "skeptics": -1, "blockers": -2}
    score = sum(len(alignment[k]) * weights[k] for k in weights)

    return {
        "alignment": alignment,
        "score": score,
        "recommendation": get_alignment_recommendation(alignment)
    }

def get_alignment_recommendation(alignment):
    if alignment["blockers"]:
        return f"Address blockers: {[s['name'] for s in alignment['blockers']]}"
    elif alignment["skeptics"]:
        return f"Convert skeptics: {[s['name'] for s in alignment['skeptics']]}"
    elif not alignment["champions"]:
        return "Develop a champion"
    elif alignment["neutral"]:
        return f"Engage neutral stakeholders: {[s['name'] for s in alignment['neutral']]}"
    else:
        return "Ready to advance"
```

## Communication Orchestration

### When to Contact Which Stakeholder
```python
def plan_stakeholder_outreach(deal_id):
    summary = get_deal_stakeholder_summary(deal_id)
    plan = []

    for stakeholder in summary["stakeholders"]:
        state = summary["engagement"][stakeholder["name"]]

        # Determine need for outreach
        days_since_contact = (now() - state["last_contact"]).days if state["last_contact"] else 999

        if days_since_contact > 14:
            plan.append({
                "stakeholder": stakeholder,
                "reason": "re-engagement",
                "priority": "medium"
            })

        if stakeholder["name"] in [r["stakeholder"] for r in summary["risks"]]:
            plan.append({
                "stakeholder": stakeholder,
                "reason": "risk_mitigation",
                "priority": "high"
            })

    # Sequence outreach appropriately
    return sequence_outreach_plan(plan)
```

### Coordinated Multi-Touch
```python
def execute_coordinated_outreach(deal_id, campaign_type):
    stakeholder_map = get_stakeholder_map(deal_id)

    campaign_configs = {
        "pre_demo": {
            "economic_buyer": {"message": "exec_summary", "timing": "day_before"},
            "decision_maker": {"message": "agenda_preview", "timing": "day_before"},
            "user": {"message": "feature_teaser", "timing": "2_days_before"}
        },
        "post_demo": {
            "economic_buyer": {"message": "roi_summary", "timing": "same_day"},
            "decision_maker": {"message": "detailed_followup", "timing": "same_day"},
            "user": {"message": "trial_invitation", "timing": "next_day"}
        }
    }

    config = campaign_configs.get(campaign_type, {})

    for stakeholder in stakeholder_map.stakeholders:
        role_config = config.get(stakeholder["role"])
        if role_config:
            schedule_message(
                stakeholder=stakeholder,
                message_type=role_config["message"],
                timing=role_config["timing"]
            )
```

## Metrics

### Multi-Stakeholder Health
```
Track:
- Stakeholders identified vs engaged
- Sentiment by stakeholder
- Objection resolution rate
- Consensus score trend
- Deal velocity by stakeholder count
```

