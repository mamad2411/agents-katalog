---
name: conversation-velocity-optimization
description: When the user wants to build or improve a sales bot's ability to match reply speed to prospect pace. Also use when the user mentions "response speed," "reply timing," "conversation velocity," "message pacing," or "adaptive timing."
---

# Conversation Velocity Optimization

You are an expert in building sales bots that match their reply speed to prospect behavior. Your goal is to help developers create systems that respond at the pace prospects prefer—fast for fast responders, measured for those who take their time.

## Why Velocity Matters

### The Speed Mismatch Problem
```
Scenario 1: Fast prospect, slow bot
Prospect replies in 30 seconds.
Bot takes 4 hours to respond.
Prospect: Already moved on, talking to competitor.

Scenario 2: Slow prospect, fast bot
Prospect replies after 2 days (thoughtful).
Bot responds in 2 minutes.
Prospect: Feels pressured, backs off.

Matching velocity = matching expectations.
```

### The Velocity Advantage
```
Fast responders get fast replies:
- Feels like real conversation
- Maintains momentum
- Shows responsiveness
- Capitalizes on interest window

Slow responders get measured replies:
- Doesn't feel pushy
- Respects their pace
- Matches their style
- Builds trust through patience
```

## Velocity Detection

### Measuring Prospect Speed
```python
def calculate_prospect_velocity(conversation):
    response_times = []

    for i, message in enumerate(conversation.messages):
        if message.sender == "prospect":
            # Time since our last message
            prev_message = find_previous_bot_message(conversation, i)
            if prev_message:
                response_time = message.timestamp - prev_message.timestamp
                response_times.append(response_time)

    if not response_times:
        return "unknown"

    avg_response = sum(response_times) / len(response_times)

    # Categorize velocity
    if avg_response < timedelta(minutes=5):
        return "very_fast"
    elif avg_response < timedelta(minutes=30):
        return "fast"
    elif avg_response < timedelta(hours=4):
        return "moderate"
    elif avg_response < timedelta(hours=24):
        return "slow"
    else:
        return "very_slow"
```

### Velocity Categories
```
Very Fast (<5 min):
- In active conversation mode
- High engagement
- Expect immediate responses
- Likely on mobile or at computer

Fast (5-30 min):
- Engaged but multitasking
- Checking messages regularly
- Expect quick responses
- Window of high interest

Moderate (30 min - 4 hours):
- Busy but interested
- Checking periodically
- Standard business pace
- Normal response time acceptable

Slow (4-24 hours):
- Low priority or busy
- Daily email checker
- No rush expected
- Patience appreciated

Very Slow (>24 hours):
- Very busy or low interest
- Needs multiple days
- Don't push frequency
- Long-term nurture
```

### Real-Time Velocity Updates
```python
class VelocityTracker:
    def __init__(self, prospect_id):
        self.prospect_id = prospect_id
        self.velocity_history = []
        self.current_velocity = "unknown"

    def update_on_response(self, response_time):
        self.velocity_history.append({
            "time": response_time,
            "timestamp": datetime.now()
        })

        # Weight recent responses more heavily
        recent = self.velocity_history[-5:]  # Last 5
        weighted_avg = self.calculate_weighted_average(recent)

        self.current_velocity = self.categorize(weighted_avg)
        return self.current_velocity

    def get_recommended_reply_time(self):
        VELOCITY_TARGETS = {
            "very_fast": timedelta(minutes=2),
            "fast": timedelta(minutes=10),
            "moderate": timedelta(hours=1),
            "slow": timedelta(hours=4),
            "very_slow": timedelta(hours=12),
            "unknown": timedelta(hours=1)  # Default
        }
        return VELOCITY_TARGETS[self.current_velocity]
```

## Response Timing Strategy

### For Very Fast Prospects
```
Strategy: Match their energy

- Respond within 2-5 minutes
- Use conversational, quick messages
- Keep momentum going
- Multiple short exchanges OK
- Feels like real-time chat

"Got it! So you're saying [x]—that makes sense.
Quick question: [follow-up]"
```

### For Fast Prospects
```
Strategy: Quick but not instant

- Respond within 10-30 minutes
- Thorough but concise
- Don't overwhelm with info
- Keep conversation moving

"Thanks for the quick reply! Based on what you
mentioned about [x], here's what I'd suggest..."
```

### For Moderate Prospects
```
Strategy: Standard business pace

- Respond within 1-4 hours
- More comprehensive responses
- Include relevant details
- Don't expect immediate follow-up

"Hi [Name], thanks for getting back to me.
I've put together some thoughts on [topic]..."
```

### For Slow Prospects
```
Strategy: Patient and thorough

- Respond within 4-12 hours
- Very comprehensive
- Anticipate follow-up questions
- Don't send rapid follow-ups

"Hi [Name], I know you're busy so I wanted to
give you a complete picture in one message..."
```

### For Very Slow Prospects
```
Strategy: Measured and respectful

- Respond within 12-24 hours
- Complete, standalone messages
- Don't send multiple messages
- Long intervals between sequences

"Hi [Name], following up from last week.
I've attached everything you'd need to
evaluate this at your own pace..."
```

## Adaptive Response System

### Dynamic Timing Engine
```python
class AdaptiveResponder:
    def __init__(self):
        self.velocity_tracker = {}

    def should_respond_now(self, prospect_id, message_ready_at):
        tracker = self.get_tracker(prospect_id)
        target_time = tracker.get_recommended_reply_time()

        # Calculate when to send
        send_at = message_ready_at + target_time

        # Add small human-like variation
        variance = random.uniform(-0.2, 0.3) * target_time
        send_at += variance

        # Respect business hours
        send_at = adjust_to_business_hours(send_at)

        return send_at

    def schedule_response(self, prospect_id, response):
        send_at = self.should_respond_now(
            prospect_id,
            datetime.now()
        )

        if send_at <= datetime.now():
            # Send immediately
            return self.send_now(response)
        else:
            # Schedule for later
            return self.schedule_send(response, send_at)
```

### Velocity-Adjusted Content
```python
def adjust_content_for_velocity(response, velocity):
    if velocity in ["very_fast", "fast"]:
        # Shorter, punchier
        response = shorten_response(response)
        response = add_quick_cta(response)

    elif velocity in ["slow", "very_slow"]:
        # More comprehensive
        response = add_context(response)
        response = anticipate_questions(response)
        response = make_standalone(response)

    return response
```

## Channel-Specific Velocity

### Email Velocity
```
Typical email pace:
- Fast: Same-day response
- Normal: Within 24 hours
- Slow: 2-3 days

Adjust:
- Fast emailers: Reply within hours
- Slow emailers: Don't expect same-day
- Very slow: Weekly cadence max
```

### SMS Velocity
```
Typical SMS pace:
- Fast: Within minutes
- Normal: Within hours
- Slow: Same day

SMS generally expects faster:
- Even "slow" SMS prospects expect same-day
- Don't let SMS responses go overnight
- Match their speed closely
```

### Chat Velocity
```
Chat expectation:
- Real-time conversation
- Responses within seconds-minutes
- Leaving chat = ending conversation

Chat-specific:
- Always respond fast
- Typing indicators helpful
- Don't make them wait
```

## Velocity Transitions

### Detecting Velocity Changes
```python
def detect_velocity_shift(tracker):
    recent = tracker.velocity_history[-3:]
    historical = tracker.velocity_history[:-3]

    if len(recent) < 2 or len(historical) < 2:
        return None

    recent_avg = average(recent)
    historical_avg = average(historical)

    if recent_avg < historical_avg * 0.5:
        return "accelerating"
    elif recent_avg > historical_avg * 2:
        return "decelerating"
    else:
        return "stable"
```

### Responding to Shifts
```
Velocity accelerating:
"Great to catch you! Since you're available,
want to just knock this out now?"
→ Capitalize on their attention

Velocity decelerating:
"I know you're busy—no rush on a response.
Here's everything you need when you have time."
→ Reduce pressure
```

## Human-Like Variation

### Avoid Robotic Timing
```
Too consistent:
- Always responds in exactly 5 minutes
- Feels automated
- Lacks authenticity

Better:
- 3-7 minute range for "fast"
- Some responses quicker, some slower
- Occasional "I'm looking into this"

Add variance:
base_time + random(-20%, +30%)
```

### Typing Simulation
```
For real-time channels:

1. Show typing indicator
2. Duration based on message length
3. Small variance in timing
4. Occasional corrections/edits

Makes bot feel human, not instant.
```

## Metrics

### Velocity Matching Performance
```
Track:
- Velocity match rate (did we match their speed?)
- Response satisfaction by velocity tier
- Conversion rate by velocity tier
- Engagement continuation rate

Optimize:
- Tighten timing accuracy
- Identify optimal variance
- Channel-specific tuning
```

### Velocity Impact Analysis
```
Compare outcomes:
- Fast-matched vs mismatched
- Slow-matched vs too-fast responses

Questions:
- Does matching improve conversion?
- What's the optimal response time per tier?
- Does faster always help?
```

## Edge Cases

### Sudden Availability
```
Slow prospect suddenly responds fast:

"Let me grab you while you're here—
any questions I can answer right now?"

Capitalize on rare attention window.
```

### Time-Sensitive Urgency
```
Even for slow prospects, respond fast when:
- They mention urgency
- Decision deadline mentioned
- Competitor comparison active
- "I need to know by..."

Override normal velocity for urgency.
```

### After-Hours Activity
```
Prospect responding at 11pm:
- They're choosing to engage
- Match their energy? Or wait?

Options:
- Auto-respond acknowledging receipt
- Full response during business hours
- Match if high intent detected
```

