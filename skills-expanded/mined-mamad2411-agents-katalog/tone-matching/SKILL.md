---
name: tone-matching
description: When the user wants to build or improve a sales bot's ability to adapt formality based on how the prospect communicates. Also use when the user mentions "matching tone," "adapting formality," "mirroring communication style," "voice adaptation," or "matching prospect style."
---

# Tone Matching for Sales Bots

You are an expert in building adaptive communication systems for sales bots. Your goal is to help design bots that adjust their tone and formality to match how prospects communicate.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What channels does your bot operate on?
   - What's your brand voice?
   - What audience do you serve?

2. **Current State**
   - How does your bot currently communicate?
   - Does it sound robotic or natural?
   - Is the tone appropriate for your audience?

3. **Goals**
   - What would better tone matching achieve?
   - What communication style should be the baseline?

---

## Core Principles

### 1. Mirror Their Energy
- Formal prospect → More formal response
- Casual prospect → More casual response
- Match, don't clash

### 2. Stay Within Brand Bounds
- Adaptable doesn't mean chameleon
- Maintain brand voice fundamentals
- Shift within acceptable range

### 3. Authenticity Over Mimicry
- Adapt tone, not personality
- Don't force a style that doesn't fit
- Natural over artificial

### 4. Read Continuously
- Tone can change within conversation
- Stay attuned throughout
- Adjust as they shift

---

## Tone Dimensions

### Formality Spectrum

**Formal:**
"Good afternoon. Thank you for your inquiry. I would be delighted to assist you with..."

**Professional:**
"Hi there. Thanks for reaching out. Happy to help you with..."

**Casual:**
"Hey! Thanks for getting in touch. Let me help you with..."

**Very Casual:**
"Hey there! What's up? Let's figure this out..."

### Energy Spectrum

**High energy:**
"That's awesome! I love that idea. Let's make it happen!"

**Medium energy:**
"Great choice. I think that'll work well for you."

**Low energy:**
"That makes sense. Here's how we can proceed."

### Detail Spectrum

**Detail-oriented:**
"Here's a comprehensive overview of the three options, including pricing tiers, features included in each, and implementation timelines..."

**Summary-focused:**
"Here are your options: A, B, or C. I'd recommend B based on what you've shared."

---

## Detecting Communication Style

### Linguistic Signals

**Formal indicators:**
- Complete sentences
- Professional greetings ("Dear," "Good morning")
- No contractions
- Full words (not abbreviations)
- Technical language
- Longer messages

**Casual indicators:**
- Sentence fragments
- Casual greetings ("Hey," "Hi!")
- Contractions ("I'm," "won't")
- Abbreviations ("pls," "thx")
- Emojis
- Shorter messages

### Analysis Approach

```
function analyzeTone(message) {
  signals = {
    formality: 0,  // -1 (casual) to 1 (formal)
    energy: 0,      // -1 (low) to 1 (high)
    detail: 0       // -1 (brief) to 1 (detailed)
  }

  // Formality signals
  if (hasGreeting(message, ["dear", "good morning", "good afternoon"])) {
    signals.formality += 0.3
  }
  if (hasGreeting(message, ["hey", "hi!", "yo"])) {
    signals.formality -= 0.3
  }
  if (hasEmoji(message)) {
    signals.formality -= 0.2
  }
  if (hasContractions(message)) {
    signals.formality -= 0.1
  }
  if (averageWordLength(message) > 5) {
    signals.formality += 0.1
  }

  // Energy signals
  if (hasExclamationMarks(message)) {
    signals.energy += 0.2 * countExclamations(message)
  }
  if (hasPositiveEmoji(message)) {
    signals.energy += 0.2
  }
  if (hasEnthusiasticWords(message)) {
    signals.energy += 0.2
  }

  // Detail signals
  if (message.length > 200) {
    signals.detail += 0.3
  }
  if (message.length < 50) {
    signals.detail -= 0.3
  }
  if (hasNumbersOrLists(message)) {
    signals.detail += 0.2
  }

  return signals
}
```

### Context Signals

**Consider:**
- Channel (SMS more casual, email varies)
- Industry (finance formal, tech casual)
- Role (C-suite often more direct)
- Time of day (early morning more brief)
- Previous interactions

---

## Adapting Response Tone

### Response Variations

**For the same information, different tones:**

**Formal:**
"Thank you for your inquiry. I would be pleased to schedule a demonstration at your convenience. Please indicate your availability, and I will coordinate accordingly."

**Professional:**
"Thanks for reaching out! I'd be happy to set up a demo. What times work for you this week?"

**Casual:**
"Hey, love to show you a demo! When works for you?"

### Tone Templates

```
templates = {
  "schedule_demo": {
    "formal": "I would be delighted to arrange a demonstration. Please share your availability at your earliest convenience.",
    "professional": "Happy to set up a demo. What times work for you?",
    "casual": "Let's get you a demo! When's good for you?"
  },
  "answer_pricing": {
    "formal": "Regarding pricing, our solutions begin at [X]. I can provide a detailed proposal tailored to your requirements.",
    "professional": "Pricing starts at [X]. Want me to put together a custom quote based on your needs?",
    "casual": "We start at [X], but it depends on what you need. Want me to work up something specific for you?"
  }
}
```

### Dynamic Tone Selection

```
function selectTone(detected_signals, brand_limits) {
  // Map detected tone to response tone
  if (detected_signals.formality > 0.5) {
    base_tone = "formal"
  } else if (detected_signals.formality < -0.3) {
    base_tone = "casual"
  } else {
    base_tone = "professional"
  }

  // Apply brand limits
  if (brand_limits.min_formality == "professional" && base_tone == "casual") {
    base_tone = "professional"
  }

  return base_tone
}
```

---

## LLM-Based Tone Matching

### Prompt Engineering

```
system_prompt = """
You are a sales assistant. Adapt your tone to match the prospect's communication style:

- If they're formal (complete sentences, professional language), respond formally
- If they're casual (abbreviations, emojis, fragments), respond casually
- Match their energy level

Brand guidelines:
- Always professional and helpful
- Can use humor if they do
- Never use profanity
- Stay within [formal - professional - friendly] range
"""

function generateResponse(message, context) {
  tone_analysis = analyzeTone(message)

  prompt = `
  Prospect's tone: ${describeTone(tone_analysis)}
  Prospect's message: ${message}
  Context: ${context}

  Respond in a matching tone while staying professional.
  `

  return llm.generate(system_prompt, prompt)
}
```

### Few-Shot Examples

```
examples = [
  {
    input: "Hey! Super interested in your product. What's the price?",
    tone: "casual, high energy",
    output: "Hey! Glad to hear it! 😊 Pricing depends on your team size—usually ranges from $X-$Y/month. What's your setup like?"
  },
  {
    input: "Good morning. I would like to inquire about your enterprise pricing structure.",
    tone: "formal, low energy",
    output: "Good morning. Thank you for your inquiry. Our enterprise pricing is customized based on several factors. I would be happy to discuss your specific requirements. Would you have time for a brief call this week?"
  },
  {
    input: "Quick q - do you integrate with Salesforce?",
    tone: "casual, brief",
    output: "Yep! Full Salesforce integration. Want details?"
  }
]
```

---

## Channel-Specific Tone

### SMS

**Default:** Casual to professional
**Adjustments:**
- Shorter regardless of their length
- Emojis acceptable if they use them
- Less formal greetings

### Email

**Default:** Professional
**Adjustments:**
- Match their formality level
- Longer is acceptable if they write longer
- Professional signature

### Chat

**Default:** Friendly professional
**Adjustments:**
- More casual acceptable
- Real-time feel
- Quicker, shorter messages

### Voice

**Default:** Professional conversational
**Adjustments:**
- Match their pace
- Mirror energy level
- Adapt formality

---

## Maintaining Brand Voice

### Brand Guardrails

**Define:**
- Minimum formality level
- Maximum casualness
- Acceptable/unacceptable words
- Emoji policy
- Humor boundaries

**Example:**
```
brand_guidelines = {
  min_formality: "friendly_professional",
  max_casualness: "casual",  // Never "very_casual"
  emoji_allowed: true,
  emoji_max: 1,  // Per message
  humor_allowed: true,
  humor_type: ["light", "friendly"],  // Not sarcasm
  banned_words: ["..."certain terms..."],
  always_include: ["professional signature on email"]
}
```

### Voice Consistency

**Core elements to maintain:**
- Helpfulness
- Professionalism
- Brand personality
- Value-focused

**Elements to adapt:**
- Formality
- Energy
- Detail level
- Greetings/closings

---

## Measuring Tone Matching

### Metrics

**Engagement:**
- Response rate by tone match
- Conversation length by tone match
- Sentiment changes through conversation

**Quality:**
- Human review of tone appropriateness
- Customer feedback
- Brand guideline compliance

### A/B Testing

**Test:**
- Matching tone vs. fixed tone
- Different matching algorithms
- Tone ranges for different segments

**Measure:**
- Engagement
- Conversion
- Satisfaction

---

## Common Mistakes

### 1. Over-Matching
**Problem:** Mirroring everything, losing brand identity
**Fix:** Adapt within brand boundaries

### 2. Under-Matching
**Problem:** Fixed tone regardless of prospect
**Fix:** Detect and respond to their style

### 3. Jarring Shifts
**Problem:** Sudden tone changes feel unnatural
**Fix:** Gradual adaptation, consistent conversation

### 4. Matching Negativity
**Problem:** Prospect is angry, bot matches anger
**Fix:** Match formality, not negativity

### 5. Forced Casualness
**Problem:** Casual tone where inappropriate
**Fix:** Industry/context awareness

---

## Implementation Checklist

### Phase 1: Basic Tone Detection
- [ ] Detect formality level
- [ ] Detect energy level
- [ ] Categorize messages

### Phase 2: Response Adaptation
- [ ] Create tone-varied templates
- [ ] Select templates by detected tone
- [ ] Test and refine

### Phase 3: Dynamic Generation
- [ ] LLM-based tone matching
- [ ] Brand guideline enforcement
- [ ] Continuous learning

---

## Questions to Ask

If you need more context:
1. What's your brand voice today?
2. What audience do you serve?
3. What channels does your bot operate on?
4. What tone problems have you observed?
5. What are your brand's communication boundaries?

---

## Related Skills

- **sentiment-analysis**: Detecting emotional state
- **adaptability**: Human adaptability principles
- **conversational-flow-management**: Natural conversation
- **personalization-at-scale**: Personalizing communication
