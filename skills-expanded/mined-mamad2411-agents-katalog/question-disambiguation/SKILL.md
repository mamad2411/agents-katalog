---
name: question-disambiguation
description: When the user wants to build or improve a sales bot's ability to clarify vague or ambiguous responses before proceeding. Also use when the user mentions "clarifying questions," "disambiguation," "unclear responses," "vague answers," or "asking for clarity."
---

# Question Disambiguation

You are an expert in building disambiguation systems for sales bots. Your goal is to help developers create bots that gracefully clarify vague responses without frustrating prospects.

## Why Disambiguation Matters

Wrong interpretation → Wrong path → Lost deal

```
Prospect: "We need something for the team"

Without disambiguation:
Bot assumes 5-person team → Quotes wrong pricing
Reality: 500-person team → Deal lost

With disambiguation:
Bot: "Great! Is this for a small team under 20, or a larger organization?"
Prospect: "About 500 people"
Bot: "Perfect—let me share our enterprise options."
```

## Types of Ambiguity

### Referential Ambiguity
What does "it" or "that" refer to?
```
Prospect: "Can it do that?"

Possible meanings:
- Can the product do [last feature mentioned]?
- Can the product do [thing competitor does]?
- Can the product do [something not yet discussed]?

Clarify: "Just want to make sure I answer the right question—
are you asking about [Feature A] or something else?"
```

### Scope Ambiguity
How much/many?
```
Prospect: "We have a few locations"

Could mean: 2? 5? 15? 50?

Clarify: "A few locations—is that closer to 5 or more like 20+?
Pricing works differently at scale."
```

### Temporal Ambiguity
When exactly?
```
Prospect: "We need this soon"

Could mean: This week? This month? This quarter?

Clarify: "When you say soon—are we talking days, weeks, or
a couple months?"
```

### Intent Ambiguity
What do they actually want?
```
Prospect: "Tell me about pricing"

Could mean:
- Give me a quote
- Explain how pricing works
- I think it's too expensive
- I'm comparing to competitors

Clarify: "Happy to! Are you looking for a specific quote,
or more about how our pricing model works?"
```

## Disambiguation Framework

### When to Clarify
```
ALWAYS clarify when:
- Response could change the path significantly
- Number/amount is unclear but needed for quoting
- Timeline is vague but affects urgency
- Decision maker status is unclear

DON'T clarify when:
- Context makes meaning obvious
- Stakes are low (can correct later)
- Clarifying would be condescending
- You can handle multiple interpretations
```

### How to Clarify

**Binary Choice**
```
"Did you mean X or Y?"

Best when: Two clear possibilities
Example: "When you said 'the team,' did you mean your
sales team specifically or the whole company?"
```

**Multiple Choice**
```
"Is it A, B, or C?"

Best when: 3-4 likely options
Example: "For timeline—are you thinking this month,
next quarter, or is this more exploratory?"
```

**Range Confirmation**
```
"Are we in the X-Y range?"

Best when: Quantifying vague amounts
Example: "When you say 'limited budget,' are we talking
under $10k, or more like $20-30k?"
```

**Open Clarification**
```
"Can you tell me more about X?"

Best when: Need more context
Example: "Can you tell me more about what 'flexible'
means for your team?"
```

## Clarification Patterns

### The Soft Clarify
```
Natural, conversational:

Prospect: "We're looking for something enterprise-grade"

Bot: "Enterprise-grade—I love that you're thinking big.
When you say that, what's most important? The scale,
the security, or the support?"
```

### The Assumption Test
```
State your interpretation, let them correct:

Prospect: "We need this for compliance"

Bot: "Got it—sounds like you need SOC 2 or similar
certifications. Is that what you're referring to?"

If wrong, they'll correct you.
```

### The Repeat Back
```
Confirm understanding:

Prospect: "Budget is around fifty"

Bot: "Fifty thousand—is that the total budget or
per year? Want to make sure I quote correctly."
```

### The Context Bridge
```
Use related info to narrow down:

Prospect: "We need it for reporting"

Bot: "Reporting for your execs, your board,
or more day-to-day team metrics?"
```

## Handling Vague Numbers

### Budget Vagueness
```
"Some budget" → "Roughly speaking—under $10k, $10-50k, or above?"
"Not cheap" → "Investing in quality makes sense. Are we in the
               $X-Y range, or should I be thinking higher?"
"Depends" → "Totally fair. If I could show clear ROI, what
             would be a realistic investment?"
```

### Team Size Vagueness
```
"Small team" → "Small like 5 people or small like 50?"
"Growing" → "Congrats! Where are you now, and where do you
            expect to be in 12 months?"
"Several departments" → "Roughly how many people total
                        would be using this?"
```

### Timeline Vagueness
```
"Soon" → "Is soon this month or this quarter?"
"When we're ready" → "What would need to happen for you
                     to be ready?"
"Not in a rush" → "Is this a 2024 priority or more 2025?"
```

## Avoiding Clarification Fatigue

### Don't Over-Clarify
```
❌ Bad: Clarifying every statement
Prospect: "We're a tech company"
Bot: "Tech company—do you mean software, hardware, or services?"
(Unnecessary—doesn't change the conversation)

✓ Good: Clarifying what matters
Prospect: "We want to start soon"
Bot: "Soon—this month or next?" (Affects urgency)
```

### Batch Clarifications
```
❌ Bad:
Bot: "How many users?"
Prospect: "About 50"
Bot: "And what's your timeline?"
Prospect: "Q2"
Bot: "And your budget?"

✓ Good:
Bot: "A few quick questions to make sure I point you
in the right direction: roughly how many users, what
timeline are you working with, and is there a budget
range I should keep in mind?"
```

### Use Context First
```
Before clarifying, check if context makes it clear:

Conversation history:
- Prospect mentioned 200-person company
- Discussed enterprise features
- Asked about SSO

Prospect: "What's the price for us?"

Don't clarify "us"—context makes it clear.
Quote enterprise pricing for ~200 users.
```

## Graceful Phrasing

### Natural Language
```
❌ Robotic:
"Please clarify: Did you mean Option A or Option B?"

✓ Natural:
"Just want to make sure I understand—when you say [X],
do you mean [A] or [B]?"
```

### Acknowledge First
```
✓ "Good question! To answer accurately—[clarify]"
✓ "That's helpful. So I give you the right info—[clarify]"
✓ "Makes sense. Just so I point you right way—[clarify]"
```

### Avoid Blame
```
❌ "I didn't understand what you meant"
❌ "Can you be more specific?"
❌ "That doesn't make sense"

✓ "I want to make sure I answer the right question"
✓ "Just to clarify so I'm helpful"
✓ "Let me make sure I understand correctly"
```

## Recovery from Misunderstanding

### When You Got It Wrong
```
Prospect: "No, I meant [actual meaning]"

Response:
"Ah, got it—thanks for clarifying! So [restate correctly].
[Continue with correct interpretation]."

Not:
"Sorry for the confusion" (unnecessary)
"My mistake" (draws attention to error)
```

### When They're Frustrated
```
Prospect: "I already told you this"

Response:
"You're right, I apologize. Just to make sure I have it
exactly right: [restate what you know]. Does that capture it?"

Then don't ask again—note it in context.
```
