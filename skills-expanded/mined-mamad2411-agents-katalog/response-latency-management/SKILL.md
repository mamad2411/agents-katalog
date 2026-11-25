---
name: response-latency-management
description: When the user wants to build or improve a sales bot's ability to reply fast enough to feel real-time but not unnaturally instant. Also use when the user mentions "response speed," "reply timing," "bot response delay," "natural pacing," or "message timing."
---

# Response Latency Management for Sales Bots

You are an expert in managing response timing for automated sales bots. Your goal is to help design systems that reply at speeds that feel natural and human-like while maintaining engagement.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What channels is your bot operating on?
   - What type of conversations does it have?
   - What does your bot currently feel like?

2. **Current State**
   - How fast does your bot respond?
   - Does it feel robotic or natural?
   - What feedback have you received?

3. **Goals**
   - What would better latency management achieve?
   - What experience are you trying to create?

---

## Core Principles

### 1. Fast Enough to Engage, Slow Enough to Be Human
- Instant response = clearly a bot
- Too slow = lost engagement
- Sweet spot = quick but believable

### 2. Match Channel Expectations
- Chat: Seconds
- SMS: Seconds to minutes
- Email: Minutes to hours
- Each has different norms

### 3. Context Affects Expectations
- Simple question = faster response expected
- Complex question = slower is acceptable
- Emotional message = thoughtful delay appropriate

### 4. Consistency Matters
- Wildly varying speeds feel off
- Establish a baseline
- Vary within reasonable range

---

## Optimal Response Times

### By Channel

**Live Chat:**
- First response: 1-3 seconds
- Subsequent: 2-5 seconds
- Complex: 5-10 seconds + typing indicator

**SMS:**
- Initial response: 5-30 seconds
- Subsequent: 10-60 seconds
- Complex: 1-2 minutes acceptable

**Phone (AI Voice):**
- Response: 0.5-1.5 seconds
- Pause tolerance: Very low
- Needs to feel real-time

**Email:**
- Not real-time by nature
- Fast: Within 1 hour
- Standard: Within 4-24 hours
- Can be immediate if triggered

### By Message Type

| Message Type | Min Delay | Max Delay | Notes |
|--------------|-----------|-----------|-------|
| Greeting | 1s | 3s | Be responsive |
| Simple question | 2s | 5s | Quick answers |
| Complex question | 5s | 15s | Use typing indicator |
| Emotional message | 3s | 10s | Don't rush empathy |
| Multi-part response | Stagger | Messages | Send in chunks |

---

## Creating Natural Pacing

### Typing Indicators

**Why they matter:**
- Signal that response is coming
- Create anticipation
- Make delays feel intentional

**Best practices:**
- Show typing within 1 second
- Duration should roughly match message length
- Don't show for instant responses

**Implementation:**
```
function sendResponse(message, channel) {
  let typing_duration = estimateTypingTime(message)

  showTypingIndicator()
  wait(typing_duration)
  hideTypingIndicator()
  sendMessage(message)
}

function estimateTypingTime(message) {
  // ~200-300ms per word, with minimum
  let words = message.split(' ').length
  let base_time = words * 250  // ms
  return Math.max(1000, Math.min(base_time, 5000))
}
```

### Message Chunking

**Why chunk:**
- Long messages look bot-like
- Chunks feel conversational
- Allows for engagement between parts

**Example:**
Instead of:
```
"Thanks for reaching out! I'd be happy to help you understand our pricing. We offer three tiers: Basic at $29/month, Pro at $79/month, and Enterprise with custom pricing. Each tier includes different features. Would you like me to explain the differences, or do you have specific questions about any tier?"
```

Send as:
```
[Message 1, 1s delay]
"Thanks for reaching out! I'd be happy to help with pricing."

[Message 2, 2s delay]
"We have three tiers: Basic ($29/mo), Pro ($79/mo), and Enterprise (custom)."

[Message 3, 1.5s delay]
"Want me to break down what's included in each, or do you have a specific question?"
```

### Variable Delays

**Why vary:**
- Consistent timing feels robotic
- Humans have natural variation
- Creates more realistic experience

**Implementation:**
```
function humanizedDelay(base_ms) {
  // Add ±20% randomization
  let variance = base_ms * 0.2
  let random = (Math.random() - 0.5) * 2 * variance
  return base_ms + random
}
```

---

## Context-Aware Timing

### By Conversation State

**Opening:**
- First response: Quick (shows attentiveness)
- Establishes responsiveness

**Discovery:**
- Standard pacing
- Match their response speed

**Complex Discussion:**
- Slower is acceptable
- Shows "thinking"
- Use indicators

**Closing:**
- Slightly quicker
- Maintains momentum
- Shows eagerness to help

### By Prospect Behavior

**They're typing fast:**
- Respond quicker
- Match their energy

**They're taking their time:**
- Don't rush
- Give space

**They're frustrated:**
- Don't delay empathetic response
- But don't rush past acknowledgment

---

## Technical Implementation

### Basic Delay System

```
async function respondWithDelay(message, context) {
  let delay = calculateDelay(message, context)

  // Show typing indicator for chat
  if (context.channel === 'chat') {
    showTypingIndicator(context.session)
  }

  await sleep(delay)

  if (context.channel === 'chat') {
    hideTypingIndicator(context.session)
  }

  return sendMessage(message, context)
}

function calculateDelay(message, context) {
  let base = getBaseDelay(context.channel)
  let length_factor = Math.min(message.length / 50, 3)
  let complexity_factor = context.is_complex ? 1.5 : 1

  let delay = base * length_factor * complexity_factor
  return humanizedDelay(delay)
}
```

### Queue Management

**Challenge:** Multiple messages might queue up

**Solution:**
```
let message_queue = []
let is_sending = false

async function queueMessage(message, delay) {
  message_queue.push({ message, delay })

  if (!is_sending) {
    is_sending = true
    await processQueue()
    is_sending = false
  }
}

async function processQueue() {
  while (message_queue.length > 0) {
    let { message, delay } = message_queue.shift()
    await sleep(delay)
    await sendMessage(message)
  }
}
```

---

## Channel-Specific Considerations

### Live Chat

**Expectations:**
- Real-time feel
- Quick responses
- Typing indicators expected

**Implementation:**
- 1-3 second base delay
- Typing indicator always
- Chunk long messages
- Acknowledge immediately if processing takes time

### SMS

**Expectations:**
- Near real-time but not instant
- Slightly longer acceptable
- No typing indicators

**Implementation:**
- 5-30 second delay typical
- Vary more than chat
- Match message length to response time
- Consider carrier delays

### Voice

**Expectations:**
- True real-time
- Natural conversational pace
- Turn-taking

**Implementation:**
- Sub-second response latency
- Handle interruptions
- Use filler phrases if processing
- "Let me check that for you..."

### Email

**Expectations:**
- Not real-time
- Hours acceptable
- Depends on context

**Implementation:**
- Triggered emails: 1-5 minutes
- Scheduled emails: Batch send times
- Reply to email: 15 minutes - 4 hours

---

## Handling Slow Responses

### When Processing Takes Time

**Acknowledge:**
"Good question—let me look that up for you..."

**Update:**
"Still working on finding the best answer..."

**Deliver:**
"Here's what I found..."

### When System is Slow

**Timeout handling:**
```
async function getResponseWithTimeout(input, timeout_ms) {
  let response_promise = generateResponse(input)
  let timeout_promise = sleep(timeout_ms).then(() => {
    throw new Error('timeout')
  })

  try {
    return await Promise.race([response_promise, timeout_promise])
  } catch (e) {
    return "I'm taking a bit longer than usual. Give me a moment..."
  }
}
```

---

## Measuring and Optimizing

### Key Metrics

**Technical:**
- Average response time
- Response time distribution
- Timeout rate

**Experience:**
- Customer satisfaction
- Engagement rate
- Abandonment rate
- "Bot detected" feedback

### A/B Testing

**Test variations:**
- Faster vs. slower base delay
- With vs. without typing indicator
- Chunked vs. single messages

**Measure:**
- Engagement (did they respond?)
- Sentiment (positive/negative)
- Conversion (did they take action?)
- Naturalness ratings (if surveyed)

### Optimization Loop

1. Measure current performance
2. Identify issues (too fast, too slow, inconsistent)
3. Adjust parameters
4. Test changes
5. Roll out winners
6. Continue monitoring

---

## Common Mistakes

### 1. Instant Responses
**Problem:** Feels robotic
**Fix:** Add intentional delay

### 2. Inconsistent Timing
**Problem:** Random fast/slow feels off
**Fix:** Consistent base with small variance

### 3. No Typing Indicators
**Problem:** Messages appear from nowhere
**Fix:** Show typing for chat channels

### 4. Long Messages Instantly
**Problem:** No human types that fast
**Fix:** Delay proportional to length

### 5. Same Delay Every Time
**Problem:** Predictable = robotic
**Fix:** Randomize within range

---

## Questions to Ask

If you need more context:
1. What channels does your bot operate on?
2. What are your current response times?
3. Has feedback indicated the bot feels robotic?
4. What experience are you trying to create?
5. Are there technical constraints on response time?

---

## Related Skills

- **conversational-flow-management**: Overall conversation design
- **tone-matching**: Matching response style
- **handoff-detection**: When delays indicate need for human
- **multi-channel-coordination**: Timing across channels
