---
name: conversational-flow-management
description: When the user wants to build or improve a sales bot's ability to keep exchanges natural while progressing toward outcomes. Also use when the user mentions "conversation design," "dialog flow," "bot conversations," "natural conversations," or "guided conversations."
---

# Conversational Flow Management for Sales Bots

You are an expert in designing conversational flows for automated sales bots. Your goal is to help build bots that keep exchanges natural while systematically progressing toward business outcomes.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What outcomes is your bot trying to achieve?
   - What channels does it operate on?
   - How long are typical conversations?

2. **Current State**
   - Do you have existing conversation flows?
   - Where do conversations break down?
   - What feels unnatural to users?

3. **Goals**
   - What would better flow management help you achieve?
   - What does an ideal conversation look like?

---

## Core Principles

### 1. Goal-Oriented but Human-Feeling
- Every exchange should move toward outcome
- But shouldn't feel like a script
- Balance efficiency with naturalness

### 2. Guide, Don't Force
- Steer conversations gently
- Allow for tangents (within limits)
- Bring back to track naturally

### 3. Context is Everything
- Remember previous exchanges
- Reference what they've said
- Build on the conversation

### 4. Graceful Recovery
- Expect the unexpected
- Have fallbacks for everything
- Never dead-end

---

## Conversation Structure

### The Conversation Arc

**Opening:**
- Greeting
- Set expectations
- Establish purpose

**Discovery:**
- Gather information
- Understand needs
- Build rapport

**Value Exchange:**
- Provide relevant information
- Answer questions
- Address concerns

**Progression:**
- Move toward goal
- Clear next step
- Confirm commitment

**Closing:**
- Summarize
- Confirm action
- Set expectations

### Flow States

```
[Greeting] → [Discovery] → [Qualification] → [Value Delivery] → [CTA] → [Closing]
                ↓               ↓                  ↓              ↓
           [Question]     [Objection]      [Off-Topic]    [Confusion]
                ↓               ↓                  ↓              ↓
           [Answer]        [Handle]          [Redirect]     [Clarify]
                ↓               ↓                  ↓              ↓
        [Return to Flow] [Return to Flow]  [Return to Flow] [Return to Flow]
```

---

## Designing Natural Conversations

### Opening Strategies

**Warm greeting + purpose:**
"Hi! Thanks for reaching out. I'm here to help you find the right solution. What brings you here today?"

**Context-aware opening:**
"Hey [Name]! I see you've been looking at our pricing page. Happy to answer any questions—what would be most helpful?"

**Direct and efficient:**
"Hi there! Quick question: are you looking for [option A] or [option B]?"

### Maintaining Flow

**Acknowledge then advance:**
- Acknowledge what they said
- Provide brief response
- Guide to next topic

**Example:**
User: "I'm frustrated with our current tool"
Bot: "I hear you—that's a common frustration we hear. What specifically isn't working for you? That'll help me point you in the right direction."

### Transitions

**Between topics:**
"Great, that helps. Now let me ask..."
"Thanks for sharing. Related to that..."
"Got it. One more quick question..."

**To qualification:**
"To make sure I point you to the right resource..."
"So I can help you efficiently..."

**To CTA:**
"Based on what you've shared..."
"It sounds like a quick call would help..."

---

## Handling Conversation Branches

### Question Handling

**Acknowledge → Answer → Return**

```
User: "How much does it cost?"

Bot: "Good question! Pricing depends on your needs, but typically ranges
from $X-$Y per month. To give you a more accurate quote, can you tell me
a bit about your team size and what you're looking to accomplish?"
```

### Objection Handling

**Acknowledge → Address → Redirect**

```
User: "This seems expensive"

Bot: "I understand—investment matters. Many of our customers initially
felt the same way, but found the ROI within 3 months. To help me
understand if that would apply to you, what's the biggest problem
you're trying to solve?"
```

### Off-Topic Handling

**Acknowledge → Gently redirect**

```
User: "What's the weather like there?"

Bot: "Ha! I'm actually a bot, so I'm weather-agnostic 😊
But I'm great at helping with [your domain]. Anything I can help you with there?"
```

### Confusion Handling

**Clarify → Simplify → Offer alternatives**

```
User: "I don't understand"

Bot: "Let me try that again more simply. [Simpler explanation].
Does that make more sense? Or if you prefer, I can have someone
call you to walk through it."
```

---

## Conversation State Management

### What to Track

**Conversation context:**
- Current state/topic
- Questions asked/answered
- Information collected
- Sentiment trajectory

**User context:**
- Known information (name, company)
- Previous interactions
- Preferences expressed
- Engagement level

### State Machine Design

```
States:
- GREETING
- DISCOVERY
- QUALIFICATION
- OBJECTION_HANDLING
- BOOKING
- CLOSING
- ESCALATION

Transitions:
- GREETING → DISCOVERY (always)
- DISCOVERY → QUALIFICATION (when ready)
- QUALIFICATION → BOOKING (if qualified)
- QUALIFICATION → NURTURE (if not ready)
- ANY → OBJECTION_HANDLING (on objection detected)
- ANY → ESCALATION (on escalation trigger)
```

### Context Utilization

**Use what you know:**
"Earlier you mentioned [X]. Does that mean [Y]?"
"Since you're interested in [topic]..."
"Given your timeline of [timeframe]..."

**Reference history:**
"Last time we spoke, you were considering [option]..."
"Based on your previous questions about [topic]..."

---

## Multi-Turn Conversation Design

### Managing Long Conversations

**Keep it focused:**
- Each turn should be purposeful
- Don't let conversations ramble
- Natural endpoints

**Track progress:**
- What's been covered?
- What's still needed?
- Are we closer to goal?

**Know when to close:**
- Goal achieved → Close
- Stuck/unproductive → Offer alternative
- Too long → Summarize and close

### Conversation Length Guidelines

**SMS/Chat:**
- Aim for 5-10 exchanges
- Get to point quickly
- Respect the medium

**Voice:**
- 2-3 minutes ideal
- Clear purpose each segment
- Summarize frequently

**Email:**
- Fewer turns expected
- More content per turn
- Clear CTA each message

---

## Response Design

### Message Structure

**Keep messages:**
- Short (2-3 sentences max for SMS/chat)
- Scannable
- One clear point or question

**Bad:**
"Thanks for reaching out to us today. We really appreciate your interest in our company and products. I wanted to let you know that we have several options that might work for you depending on your needs. Would you like to tell me more about what you're looking for so I can point you in the right direction?"

**Good:**
"Thanks for reaching out!

What are you hoping to accomplish? That'll help me point you to the right solution."

### Response Variations

**Have multiple versions of key responses:**
- Prevents feeling scripted
- A/B test effectiveness
- Match to context/sentiment

**Example variations for greeting:**
1. "Hey there! What can I help you with today?"
2. "Hi! Thanks for reaching out. What brings you here?"
3. "Hello! I'm here to help. What are you looking for?"

---

## Error Handling and Recovery

### When Understanding Fails

**Tiered fallback:**
1. Ask for clarification once
2. Offer alternatives
3. Escalate to human

```
Attempt 1: "I want to make sure I understand. Could you rephrase that?"
Attempt 2: "Hmm, I'm having trouble with that one. Are you asking about
           A, B, or something else?"
Attempt 3: "Let me get you to someone who can help. What's the best way
           to reach you?"
```

### When Things Go Wrong

**Acknowledge gracefully:**
"Sorry about that! Let me try again."
"Good question—let me get you a better answer."
"Looks like I got a bit lost there. Let's start fresh."

**Offer escape hatch:**
"If you prefer, I can have someone call you."
"Would you like to speak with a person instead?"

---

## Channel-Specific Considerations

### SMS

- Very short messages
- One question at a time
- Use line breaks
- Respect opt-out immediately
- Comply with TCPA

### Web Chat

- Slightly longer okay
- Can use formatting
- Quick responses expected
- Typing indicators
- Easy handoff to human

### Voice (IVR/Phone Bot)

- Natural speech patterns
- Slower pace
- Confirm understanding
- Clear menu options
- Easy human transfer

### Email

- Longer form acceptable
- Include context/recap
- Clear CTA
- Professional tone
- Signature/contact info

---

## Measuring Flow Effectiveness

### Conversation Metrics

**Completion rates:**
- % reaching goal (booking, qualification)
- Drop-off points
- Average conversation length

**Quality metrics:**
- Human takeover rate
- Repeat/clarification rate
- Sentiment through conversation

**Efficiency metrics:**
- Time to goal
- Messages to goal
- Bot vs human resolution

### Optimization

**Identify friction:**
- Where do users drop off?
- Where do they ask for human?
- Where does sentiment dip?

**Test improvements:**
- A/B test response variations
- Try different flows
- Measure impact

---

## Questions to Ask

If you need more context:
1. What's the primary goal of your bot conversations?
2. Where do conversations typically break down?
3. What channel(s) does your bot operate on?
4. How complex are the topics being discussed?
5. What does success look like for a conversation?

---

## Related Skills

- **intent-detection**: Understanding what users want
- **sentiment-analysis**: Reading emotional tone
- **objection-recognition**: Handling pushback
- **fallback-gracefully**: Managing the unexpected
