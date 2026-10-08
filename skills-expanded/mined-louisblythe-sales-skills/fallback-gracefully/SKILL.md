---
name: fallback-gracefully
description: When the user wants to build or improve a sales bot's ability to handle unexpected inputs without breaking the conversation. Also use when the user mentions "handling errors," "unexpected input," "bot failures," "graceful degradation," "fallback responses," or "error recovery."
---

# Fallback Gracefully for Sales Bots

You are an expert in building resilient sales bots. Your goal is to help design systems that handle unexpected inputs, errors, and edge cases without breaking conversations or frustrating users.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What type of conversations does your bot have?
   - What unexpected inputs do you encounter?
   - How does your bot currently handle errors?

2. **Current State**
   - Where does your bot break down?
   - What happens when it doesn't understand?
   - How often are fallbacks triggered?

3. **Goals**
   - What would better error handling achieve?
   - What experience should users have when things go wrong?

---

## Core Principles

### 1. Never Dead-End
- Always have a response
- Always provide a path forward
- Never leave them hanging

### 2. Fail Gracefully, Not Obviously
- Don't expose system errors
- Don't make them feel bad
- Don't blame them for confusion

### 3. Escalate When Appropriate
- Know your limits
- Human handoff is a valid response
- Better to escalate than frustrate

### 4. Learn from Failures
- Every failure is feedback
- Track and analyze
- Improve continuously

---

## Types of Failures

### Input Failures

**Can't understand input:**
- Gibberish or typos
- Unexpected language
- Unclear intent

**Unexpected input:**
- Off-topic questions
- Complex requests
- Edge cases

**Ambiguous input:**
- Could mean multiple things
- Not enough context
- Vague responses

### System Failures

**Technical errors:**
- API timeouts
- Service unavailable
- Data fetch failures

**Integration failures:**
- CRM unreachable
- Calendar API down
- Payment system error

**Processing failures:**
- Model errors
- Parsing failures
- Logic bugs

### Context Failures

**Lost context:**
- Session expired
- History unavailable
- Missing information

**Wrong context:**
- Confused identity
- Wrong conversation thread
- Stale data

---

## Fallback Strategy

### The Fallback Hierarchy

```
Attempt 1: Try to understand
  ↓ (fail)
Attempt 2: Ask for clarification
  ↓ (fail)
Attempt 3: Offer alternatives
  ↓ (fail)
Attempt 4: Graceful handoff
```

### Tiered Fallback Responses

**Tier 1 - Clarification:**
"I want to make sure I understand. Could you rephrase that?"
"I'm not sure I followed. Are you asking about [option A] or [option B]?"

**Tier 2 - Alternative paths:**
"I'm having trouble with that one. Here's what I can help with:
- [Option 1]
- [Option 2]
- [Something else]"

**Tier 3 - Human escalation:**
"I want to make sure you get the right help. Let me connect you with someone on our team."

**Tier 4 - Graceful close:**
"I apologize—I'm not able to help with that right now. Here's how to reach us: [contact info]"

---

## Fallback Response Templates

### For Input Understanding Failures

**First attempt:**
"I want to make sure I understand correctly. Could you tell me more about what you're looking for?"

**Second attempt:**
"Hmm, I'm still not quite getting it. Are you trying to:
A) [Common option 1]
B) [Common option 2]
C) Something else"

**Third attempt:**
"I apologize—I'm having trouble understanding. Let me get you to someone who can help directly. What's the best way to reach you?"

### For Off-Topic Inputs

**Redirect gently:**
"Good question! That's a bit outside what I can help with, but I'm great at [your domain]. Anything I can help you with there?"

**With humor (if appropriate):**
"Ha! I wish I knew that one. I'm mostly helpful with [your domain] though. Anything along those lines?"

### For Technical Errors

**To the user:**
"One moment—I'm having a small technical hiccup. Let me try that again..."

**If persistent:**
"I apologize—I'm running into a technical issue. Let me have someone follow up with you directly. What's your email?"

### For Ambiguous Input

**Request clarification:**
"Just to clarify—when you say [their term], do you mean [interpretation A] or [interpretation B]?"

**Educated guess + check:**
"It sounds like you're asking about [best guess]. Is that right, or did you mean something else?"

---

## Implementation

### Basic Fallback System

```
function handleMessage(message, context) {
  try {
    // Attempt to understand and respond
    intent = detectIntent(message)

    if (intent.confidence < CONFIDENCE_THRESHOLD) {
      return handleLowConfidence(message, context)
    }

    response = generateResponse(intent, context)
    return response

  } catch (error) {
    return handleError(error, context)
  }
}

function handleLowConfidence(message, context) {
  attempts = context.clarification_attempts || 0

  if (attempts == 0) {
    context.clarification_attempts = 1
    return clarifyIntent(message)
  }

  if (attempts == 1) {
    context.clarification_attempts = 2
    return offerAlternatives(context)
  }

  return escalateToHuman(context)
}

function handleError(error, context) {
  logError(error, context)

  if (isRetryable(error)) {
    return retryWithBackoff(context)
  }

  return gracefulFallback(context)
}
```

### Confidence-Based Routing

```
function routeByConfidence(intent, context) {
  if (intent.confidence > 0.85) {
    // High confidence: proceed normally
    return processIntent(intent, context)
  }

  if (intent.confidence > 0.6) {
    // Medium confidence: confirm before proceeding
    return confirmIntent(intent, context)
  }

  if (intent.confidence > 0.3) {
    // Low confidence: ask clarifying question
    return clarifyIntent(context)
  }

  // Very low confidence: offer alternatives or escalate
  return offerAlternatives(context)
}
```

### Error Recovery

```
function retryWithBackoff(context, max_retries=3) {
  for (attempt = 1; attempt <= max_retries; attempt++) {
    try {
      wait(exponentialBackoff(attempt))
      return processMessage(context)
    } catch (error) {
      if (attempt == max_retries) {
        return gracefulFallback(context)
      }
    }
  }
}

function exponentialBackoff(attempt) {
  base_delay = 1000  // 1 second
  return base_delay * Math.pow(2, attempt - 1)
}
```

---

## Context Recovery

### Handling Lost Context

**Acknowledge and rebuild:**
"I apologize—I seem to have lost track of our conversation. Could you remind me what you were looking for?"

**Start fresh gracefully:**
"Let me start fresh to make sure I give you accurate help. What's your main question today?"

### Session Management

```
function ensureContext(session_id) {
  context = loadContext(session_id)

  if (!context || isExpired(context)) {
    // Context lost or expired
    return {
      is_new: true,
      message: "Welcome back! How can I help you today?"
    }
  }

  if (isStale(context)) {
    // Context exists but may be outdated
    return {
      is_stale: true,
      context: context,
      message: "Hi again! Were you still looking into [last topic]?"
    }
  }

  return { context: context }
}
```

---

## Specific Failure Scenarios

### Gibberish Input

**Detect:**
- Very short (1-2 chars)
- No recognizable words
- Random characters

**Response:**
"I didn't quite catch that. What are you looking for?"

### Multiple Questions

**Detect:**
- Multiple question marks
- "And" joining topics
- Run-on sentences

**Response:**
"You've got a few questions there! Let me take them one at a time. First, [address first question]. What was the second thing you wanted to know?"

### Emotional Outburst

**Detect:**
- All caps
- Profanity
- Frustration signals

**Response:**
"I can see you're frustrated, and I'm sorry. Let me get you to someone who can help properly. What's the best way to reach you?"

### Request Outside Scope

**Detect:**
- Clearly off-topic
- Unrelated domain
- Personal questions

**Response:**
"That's a bit outside my expertise! I'm best at helping with [your domain]. Is there anything along those lines I can help with?"

### System Down

**Response:**
"I'm experiencing some technical difficulties right now. Can I have someone follow up with you? What's your email or phone number?"

---

## Learning from Fallbacks

### What to Track

**For every fallback:**
- Original input
- Fallback tier triggered
- User's next message
- Ultimate outcome
- Channel and context

### Analysis Questions

- What inputs trigger fallbacks most?
- Are there patterns in misunderstandings?
- Which fallback responses work best?
- What should we train the bot to handle?

### Improvement Loop

1. Collect fallback data
2. Identify patterns
3. Train for common cases
4. Improve fallback responses
5. Monitor and repeat

---

## Measuring Fallback Performance

### Key Metrics

**Fallback rate:**
% of messages triggering fallback

**Recovery rate:**
% of fallbacks that recover vs. escalate

**User satisfaction:**
Post-fallback sentiment and engagement

### Targets

| Metric | Target |
|--------|--------|
| Fallback rate | <10% |
| Recovery rate (Tier 1) | >70% |
| Escalation rate | <5% |
| Abandonment after fallback | <15% |

---

## Common Mistakes

### 1. Exposing Technical Errors
**Bad:** "Error 500: Database connection failed"
**Good:** "I'm having a small technical issue. One moment..."

### 2. Blaming the User
**Bad:** "I don't understand your confusing question."
**Good:** "I want to make sure I understand. Could you rephrase that?"

### 3. Looping Endlessly
**Bad:** Asking for clarification 5 times
**Good:** Escalate after 2-3 attempts

### 4. No Path Forward
**Bad:** "I can't help with that."
**Good:** "I can't help with that directly, but here's how you can get assistance: [options]"

### 5. Not Learning
**Bad:** Same failures happening repeatedly
**Good:** Analyzing fallbacks and training improvements

---

## Questions to Ask

If you need more context:
1. What causes your bot to fail most often?
2. How do users react when the bot doesn't understand?
3. What's your current fallback experience like?
4. What human support is available for escalation?
5. Do you have data on fallback patterns?

---

## Related Skills

- **intent-detection**: Improving understanding to reduce fallbacks
- **handoff-detection**: When to escalate
- **conversational-flow-management**: Recovery and redirection
- **sentiment-analysis**: Detecting frustration
