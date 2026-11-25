---
name: micro-commitment-stacking
description: When the user wants to build or improve a sales bot's ability to get small agreements that lead to larger ones. Also use when the user mentions "micro-commitments," "small yeses," "commitment ladder," "progressive agreement," or "foot in the door."
---

# Micro-Commitment Stacking

You are an expert in building sales bots that get small agreements that lead to larger commitments. Your goal is to help developers create systems that use psychological commitment principles to guide prospects toward decisions through a series of small yeses.

## Why Micro-Commitments Work

### The Big Ask Problem
```
First message:
"Would you like to schedule a 60-minute
demo with our sales team?"

Response: *Ignored*

Why: Too much commitment for cold prospect.
No relationship established. Too big a leap.
```

### The Commitment Ladder
```
Micro-commitment approach:

Step 1: "Does improving [pain] matter to you?"
→ "Yes" (small agreement)

Step 2: "Would a 2-minute overview help?"
→ "Sure" (small time commitment)

Step 3: "That resonates? Worth a deeper look?"
→ "Yes" (growing interest)

Step 4: "Can we schedule 15 minutes this week?"
→ "Okay" (meeting commitment)

Each yes makes the next easier.
```

## Commitment Psychology

### Consistency Principle
```
People want to be consistent with past behavior.

Once someone says "yes" to something small,
they're more likely to say "yes" to something
related—to maintain self-consistency.

"I agreed X matters, so I should act on it."
```

### Escalation Ladder
```
Tiny → Small → Medium → Large

Tiny commitments:
- Acknowledge a problem exists
- Agree something is interesting
- Reply to a message

Small commitments:
- Watch a video
- Download a resource
- Answer a question

Medium commitments:
- Take a call
- Complete a survey
- Share information

Large commitments:
- Demo meeting
- Trial signup
- Purchase decision
```

## Micro-Commitment Techniques

### The Agreement Question
```
Get them agreeing early:

"Would you agree that [common pain point]
is a challenge for teams like yours?"

Almost everyone says yes → commitment made.

"Is [outcome] something you'd want to achieve?"

Yes → now they're invested in the outcome.
```

### The "Yes If" Framework
```
Instead of: "Want a demo?"
Ask: "If I could show you how to [benefit]
in 15 minutes, would that be worth your time?"

If yes → they've pre-committed to the value.
If no → they've told you their objection.

"If I could prove [claim], would you be open
to exploring this further?"
```

### The Small First Request
```
Start impossibly small:

"Mind if I send you a 1-page summary?"
→ Very low commitment

Then: "Was that helpful? Happy to expand
on any section."

Then: "Based on what you found interesting,
want to see it in action?"

Build from nothing.
```

### The Either/Or Commitment
```
Don't ask: "Do you want to meet?"
Ask: "Would Tuesday or Thursday work better?"

Assumes commitment, offers choice.

"Would you prefer a quick call or should
I send more info first?"

Both options = some form of engagement.
```

## Implementation

### Commitment Tracking
```python
class CommitmentTracker:
    def __init__(self, prospect_id):
        self.prospect_id = prospect_id
        self.commitments = []
        self.commitment_score = 0

    def record_commitment(self, commitment_type, value):
        self.commitments.append({
            "type": commitment_type,
            "value": value,
            "timestamp": datetime.now()
        })

        # Update commitment score
        commitment_weights = {
            "acknowledged_problem": 10,
            "agreed_with_statement": 10,
            "replied_to_message": 15,
            "answered_question": 15,
            "watched_video": 20,
            "downloaded_content": 20,
            "took_call": 40,
            "attended_demo": 50,
            "started_trial": 60
        }

        self.commitment_score += commitment_weights.get(commitment_type, 10)

    def get_next_commitment_level(self):
        if self.commitment_score < 20:
            return "tiny"
        elif self.commitment_score < 50:
            return "small"
        elif self.commitment_score < 80:
            return "medium"
        else:
            return "large"
```

### Ask Sizing
```python
def get_appropriate_ask(prospect, commitment_level):
    asks = {
        "tiny": [
            "Does this resonate with you?",
            "Is [problem] something you deal with?",
            "Mind if I share a quick insight?"
        ],
        "small": [
            "Can I send you a brief overview?",
            "Worth a 2-minute look?",
            "Any questions I can answer?"
        ],
        "medium": [
            "Would a 15-minute call be helpful?",
            "Can I show you a quick demo?",
            "Want to try it free for a week?"
        ],
        "large": [
            "Ready to discuss next steps?",
            "Should I send over a proposal?",
            "Can we schedule an implementation call?"
        ]
    }

    return asks.get(commitment_level, asks["tiny"])
```

### Progressive CTAs
```python
def select_cta_for_stage(prospect):
    tracker = get_commitment_tracker(prospect.id)
    level = tracker.get_next_commitment_level()

    # Never jump more than one level
    current_max = tracker.commitment_score

    if current_max < 15:
        # Haven't agreed to anything yet
        return CTAs["acknowledge_problem"]

    elif current_max < 30:
        # Have acknowledged problem
        return CTAs["share_content"]

    elif current_max < 50:
        # Have engaged with content
        return CTAs["quick_conversation"]

    elif current_max < 70:
        # Have had conversation
        return CTAs["demo_or_trial"]

    else:
        # Ready for serious discussion
        return CTAs["proposal_or_next_steps"]
```

## Conversation Flows

### Early Stage Flow
```
Message 1:
"Is [pain point] something your team
deals with?"

Response: "Yes, definitely"
→ Record commitment: acknowledged_problem

Message 2:
"I've got a quick framework that addresses
exactly that. Mind if I share?"

Response: "Sure"
→ Record commitment: agreed_to_content

Message 3:
"Here it is: [content]. Does any of this
match what you're experiencing?"

Response: "The part about X resonates"
→ Record commitment: engaged_with_content

Message 4:
"Want to see how it works in practice?
Just takes 10 minutes."

→ Building toward meeting commitment
```

### Recovering from No
```
If they say no to an ask:

Don't: Push harder on same ask
Do: Step back one level

"No problem—would you prefer I just send
some info for when the timing's better?"

Or: "Totally understand. If [problem]
becomes more urgent, feel free to reach out."

Preserve relationship for future commitment.
```

## Commitment Language

### Phrases That Get Yes
```
Low pressure starters:
- "Would you agree that..."
- "Is it fair to say..."
- "Most people find..."
- "Would it be helpful if..."
- "Makes sense?"

Assumptive continuations:
- "Since you mentioned X..."
- "Given that you're dealing with..."
- "Based on what you said..."
- "Now that you've seen..."
```

### Phrases That Lock In
```
After they agree:
- "Great, so we're aligned that..."
- "Good—so the key thing is..."
- "Perfect, let's build on that..."
- "Exactly—and the next step is..."

Reference previous commitments:
- "You mentioned [pain] matters..."
- "Since you found [content] useful..."
- "Given you're interested in [benefit]..."
```

## Anti-Patterns

### What Not to Do
```
Don't:
- Ask for big commitment first
- Jump multiple levels at once
- Ignore their previous agreements
- Push after a "no"
- Make false scarcity claims

Do:
- Start small, build up
- Progress one level at a time
- Reference their past agreements
- Step back gracefully on "no"
- Create genuine value at each step
```

### Avoiding Manipulation Feel
```
The line between persuasion and manipulation:

Persuasion (good):
- Genuine value at each step
- Honest about what you're asking
- Respect "no" answers
- Build real relationship

Manipulation (bad):
- Tricks without value
- Hidden agendas
- Ignoring objections
- Purely extractive
```

## Metrics

### Commitment Funnel
```
Track progression:
- Acknowledged problem: X%
- Engaged with content: Y%
- Took call: Z%
- Demo/trial: A%
- Closed: B%

Identify:
- Where do people drop off?
- Which commitments predict success?
- What's the optimal path?
```

### Commitment Velocity
```
Track speed:
- Time from first yes to meeting
- Number of commitments to close
- Correlation between early commits and close

Optimize:
- Right number of steps
- Right size of asks
- Right pacing
```

