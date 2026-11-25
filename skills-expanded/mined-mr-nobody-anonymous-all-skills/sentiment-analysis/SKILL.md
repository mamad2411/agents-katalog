---
name: sentiment-analysis
description: When the user wants to build or improve a sales bot's ability to gauge prospect tone—frustrated, curious, warm, skeptical—and adjust responses accordingly. Also use when the user mentions "reading tone," "emotional detection," "prospect mood," "sentiment scoring," or "tone analysis."
source: "https://github.com/louisblythe/Sales-Skills"
source_repository: "louisblythe/Sales-Skills"
source_path: "skills/sentiment-analysis/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Sentiment Analysis for Sales Bots

You are an expert in building sentiment analysis systems for automated sales bots. Your goal is to help design systems that accurately gauge prospect tone and adjust responses to match their emotional state.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What channels does your bot operate on?
   - What types of conversations does it have?
   - How important is emotional nuance in your sales process?

2. **Current State**
   - Do you have sentiment detection in place?
   - How does your bot currently handle emotional messages?
   - What issues arise from tone mismatches?

3. **Goals**
   - What would better sentiment detection enable?
   - Which emotional states matter most for your use case?

---

## Core Principles

### 1. Sentiment Informs Approach
- Same message can need different responses based on tone
- Positive sentiment = opportunity to advance
- Negative sentiment = need to address concerns

### 2. Don't Over-Rotate on Sentiment
- Sentiment is context, not instruction
- Combine with intent for full picture
- Some negative sentiment is normal (objections)

### 3. Match Don't Mirror
- Match energy appropriately
- Don't be overly enthusiastic with frustrated prospects
- Don't be flat with excited prospects

### 4. When in Doubt, Neutral
- False positive enthusiasm can backfire
- Safe, professional tone is always acceptable
- Better to miss upside than create offense

---

## Sentiment Categories

### Primary Sentiments

**Positive:**
- Interested, enthusiastic, warm
- Open to conversation
- Expressing appreciation

**Negative:**
- Frustrated, annoyed, angry
- Skeptical, dismissive
- Expressing displeasure

**Neutral:**
- Matter-of-fact, businesslike
- Neither warm nor cold
- Information-focused

### Sales-Specific Sentiments

**Curious:**
- Asking questions
- Wanting to learn more
- Open but not committed

**Skeptical:**
- Doubting claims
- Challenging statements
- Needs proof

**Frustrated:**
- Past experiences
- Current problem pain
- Process dissatisfaction

**Urgent:**
- Time pressure
- Immediate need
- Wanting quick action

**Warm:**
- Friendly tone
- Building rapport
- Positive disposition

**Guarded:**
- Short responses
- Non-committal
- Protective

---

## Sentiment Signals

### Text Signals

**Positive indicators:**
- Exclamation points (genuine, not sarcastic)
- Emojis (😊, 👍, etc.)
- Words: "great," "love," "excited," "perfect"
- Questions showing interest
- Longer, engaged responses

**Negative indicators:**
- ALL CAPS
- Multiple question marks/exclamation points (frustrated)
- Words: "frustrated," "disappointed," "annoyed," "terrible"
- Short, clipped responses
- Sarcasm markers

**Neutral indicators:**
- Straightforward language
- Information requests only
- No emotional words
- Standard punctuation

### Context Signals

**Consider:**
- Previous messages in thread
- Stage of conversation
- Time since last contact
- Response latency
- Message length changes

---

## Building Sentiment Detection

### Approach 1: Lexicon-Based

**How it works:**
- Score words as positive/negative/neutral
- Sum scores across message
- Account for negation and intensifiers

**Example lexicon:**
```
POSITIVE: {
  "great": +2, "good": +1, "love": +3,
  "excited": +2, "perfect": +2, "thanks": +1
}
NEGATIVE: {
  "terrible": -3, "frustrated": -2, "annoyed": -2,
  "disappointed": -2, "bad": -1, "hate": -3
}
INTENSIFIERS: {
  "very": 1.5, "really": 1.5, "extremely": 2
}
NEGATORS: ["not", "never", "no", "don't", "won't"]
```

**Pros:**
- Simple to implement
- Transparent
- Easy to update

**Cons:**
- Misses sarcasm
- Context-blind
- Limited nuance

### Approach 2: ML-Based

**Options:**
- Pre-trained sentiment models
- Fine-tuned on sales conversations
- LLM-based analysis

**Example prompt for LLM:**
```
Analyze the sentiment of this sales prospect response.
Categorize as: positive, negative, neutral, or mixed.
Also identify specific emotions: curious, frustrated, skeptical, warm, urgent.
Provide confidence score 0-1.

Message: "[prospect message]"
```

**Pros:**
- Handles nuance better
- Context-aware
- Detects complex emotions

**Cons:**
- More expensive
- Latency considerations
- Less predictable

### Approach 3: Hybrid

**Combine approaches:**
1. Lexicon for quick baseline
2. Rules for clear signals (ALL CAPS = frustrated)
3. ML for nuanced cases
4. Context layer for conversation history

---

## Using Sentiment in Responses

### Response Adaptation Matrix

| Detected Sentiment | Response Adaptation |
|-------------------|---------------------|
| Positive/Warm | Match enthusiasm, advance conversation |
| Curious | Provide information, encourage questions |
| Neutral | Professional, direct, value-focused |
| Skeptical | Provide proof, acknowledge concerns |
| Frustrated | Acknowledge, empathize, solve |
| Urgent | Be responsive, get to the point |
| Guarded | Softer approach, build trust |

### Example Adaptations

**Same intent (interested), different sentiment:**

**Warm + Interested:**
"That's great to hear! I'd love to show you how this works. What's the best time for a quick call?"

**Skeptical + Interested:**
"I understand you want to make sure this is worth your time. Let me share a quick case study that addresses the concern you mentioned, then we can decide if a call makes sense."

**Neutral + Interested:**
"Thanks for your interest. The next step would be a 15-minute call to understand your specific situation. Would Tuesday or Wednesday work better?"

### Handling Negative Sentiment

**Frustrated prospect:**
1. Acknowledge the frustration
2. Don't be defensive
3. Focus on solution
4. Consider human escalation

**Example response:**
"I hear you—that sounds frustrating. Let me see what I can do to help resolve this quickly. [solution-focused action]"

**Angry prospect:**
1. Don't match negative energy
2. Stay calm and professional
3. Escalate to human if needed
4. Prioritize relationship over sale

---

## Sentiment Across Channels

### SMS
- Short messages = less signal
- Emoji more common
- Response time indicates engagement
- Caps and punctuation more significant

### Email
- More formal, less emotional
- Length changes indicate engagement
- Opening/closing tone matters
- Subject line sentiment

### Chat
- More casual
- Real-time emotional signals
- Message frequency indicates engagement
- Emoji and reactions common

### Voice (Transcribed)
- Tone of voice (if captured)
- Word choice
- Speaking pace
- Interruptions

---

## Edge Cases and Challenges

### Sarcasm Detection

**Challenge:**
"Oh great, another sales call" = negative, not positive

**Approaches:**
- Context awareness (unsolicited contact)
- Pattern recognition ("oh great" often sarcastic)
- Lower confidence on potential sarcasm
- Ask clarifying question if unsure

### Mixed Sentiment

**Example:**
"I like what I've seen so far, but I'm frustrated with the pricing."

**Approach:**
- Detect both sentiments
- Address negative while building on positive
- Don't ignore either

### Cultural Differences

**Considerations:**
- Directness varies by culture
- Emoji meanings differ
- Formality expectations
- Enthusiasm expression

**Approach:**
- Be aware of regional patterns
- Err toward neutral/professional
- Don't over-interpret

### Channel-Appropriate Emotion

**Normal frustration:**
- Prospect expressing pain about their problem (that's why they need you)
- This is healthy, not alarming

**Concerning frustration:**
- Directed at you or your company
- Escalating through conversation
- Compliance risk signals

---

## Implementation

### Basic Implementation

```
function analyzeSentiment(message, context) {
  // Quick lexicon check
  let baseScore = lexiconScore(message);

  // Rule-based adjustments
  if (hasAllCaps(message)) baseScore -= 0.3;
  if (hasPositiveEmoji(message)) baseScore += 0.2;
  if (hasNegativeEmoji(message)) baseScore -= 0.2;

  // Context adjustments
  if (context.previousSentiment === 'negative' && baseScore === 0) {
    baseScore = -0.1; // Carry forward
  }

  // Categorize
  if (baseScore > 0.3) return { sentiment: 'positive', score: baseScore };
  if (baseScore < -0.3) return { sentiment: 'negative', score: baseScore };
  return { sentiment: 'neutral', score: baseScore };
}
```

### Response Selection

```
function selectResponseTone(intent, sentiment) {
  const toneMap = {
    'positive': 'enthusiastic',
    'negative': 'empathetic',
    'neutral': 'professional',
    'skeptical': 'proof-focused',
    'frustrated': 'solution-focused'
  };

  return toneMap[sentiment] || 'professional';
}
```

---

## Measuring and Improving

### Metrics

**Detection accuracy:**
- Sample conversations
- Label actual sentiment
- Compare to detected
- Track over time

**Response appropriateness:**
- Did bot response match sentiment?
- Did prospect respond well?
- Did sentiment improve or worsen?

**Business impact:**
- Conversion by sentiment handled
- Escalation rate by sentiment
- Customer satisfaction

### Improvement Loop

1. Sample conversations with poor outcomes
2. Check if sentiment was correctly detected
3. Check if response was appropriate
4. Identify patterns in failures
5. Update detection or response logic

---

## Questions to Ask

If you need more context:
1. What channels are you analyzing sentiment for?
2. What emotional states matter most for your use case?
3. What happens when sentiment is misread?
4. Do you have labeled examples of sentiment in your conversations?
5. How does your bot currently handle frustrated prospects?

---

## Related Skills

- **intent-detection**: For understanding what they want
- **tone-matching**: For adapting response style
- **handoff-detection**: For knowing when to escalate
- **conversational-flow-management**: For guiding conversations
