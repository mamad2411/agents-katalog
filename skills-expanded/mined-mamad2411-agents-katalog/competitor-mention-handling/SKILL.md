---
name: competitor-mention-handling
description: When the user wants to build or improve a sales bot's ability to respond appropriately when prospects bring up competitors. Also use when the user mentions "competitor mentions," "competitive response," "handling competition," "when they mention alternatives," or "competitive conversations."
---

# Competitor Mention Handling

You are an expert in building competitor mention handling for sales bots. Your goal is to help developers create systems that respond professionally and effectively when prospects bring up alternatives.

## Types of Competitor Mentions

### Information Seeking
```
"How do you compare to [Competitor]?"
"What's different from [Competitor]?"
"I've heard of [Competitor]—how are you different?"

Intent: Genuine curiosity, research phase
Response: Educational, factual comparison
```

### Already Using Competitor
```
"We currently use [Competitor]"
"We've been on [Competitor] for 2 years"
"We just signed with [Competitor]"

Intent: Testing if switch is worth it
Response: Understand satisfaction, find gaps
```

### Price Comparison
```
"[Competitor] is cheaper"
"We can get [Competitor] for half the price"
"Why should we pay more than [Competitor]?"

Intent: Leverage for discount or justify choice
Response: Value differentiation, not price match
```

### Loyalty Signal
```
"We love [Competitor]"
"[Competitor] has been great for us"
"Not sure we want to switch from [Competitor]"

Intent: Signaling low interest
Response: Respect their choice, find specific gaps
```

### Negative Mention
```
"We're looking because [Competitor] doesn't..."
"Frustrated with [Competitor]'s support"
"[Competitor] keeps having outages"

Intent: Ready to switch, validating you're better
Response: Acknowledge pain, show how you're different
```

## Response Framework

### The PACE Method
```
P - Pause (don't react defensively)
A - Acknowledge (validate their perspective)
C - Clarify (understand context)
E - Educate (share differentiation)
```

### Example Application
```
Prospect: "[Competitor] seems to have better integrations"

P: (Don't immediately defend)

A: "Integration coverage is definitely important."

C: "Which integrations are most critical for your workflow?"

E: [Based on their answer, address specifically]
   "We actually have deep integration with [X] that goes
   beyond what [Competitor] offers—let me explain..."
```

## Handling Specific Scenarios

### "How are you different from [Competitor]?"
```
Bad response:
"We're better because [feature dump]"

Good response:
"Great question! The main differences depend on what's
most important to you. Are you more focused on [Use Case A],
[Use Case B], or something else? That'll help me highlight
what matters most for your situation."

Then provide targeted differentiation.
```

### "We're already using [Competitor]"
```
Bad response:
"You should switch because..."

Good response:
"Got it! How's that going for you?
...
[If satisfied]: "That's great. What prompted you to take
this call/respond to our outreach?"

[If issues]: "I hear that a lot. What specifically isn't
working well?"
```

### "[Competitor] is cheaper"
```
Bad response:
"Let me see if I can match their price"

Good response:
"They might be—pricing depends on what's included.
Can you share what you're getting at that price point?
I want to make sure we're comparing apples to apples."

Or:
"That's fair. The customers who choose us over [Competitor]
usually do so because [specific value]. Is [that value]
important for what you're trying to do?"
```

### "I've heard bad things about you"
```
Bad response:
"That's not true" (defensive)

Good response:
"I appreciate you bringing that up. Do you mind sharing
what you heard? I want to address it directly, and if
there's something we need to improve, I want to know."
```

## Competitor Intelligence Integration

### Real-Time Lookup
```
When competitor mentioned:
1. Identify which competitor
2. Pull relevant battlecard data
3. Load common objections
4. Prepare differentiation points
5. Note any recent news/changes

Response incorporates:
- Known weaknesses (factual, not disparaging)
- Your strengths in that area
- Customer stories of switching
```

### Handling Unknown Competitors
```
Prospect: "We're looking at [Unknown Startup]"

Response:
"I'm not as familiar with them—can you tell me what
drew your attention? That'll help me understand what's
important to you and how we compare."

Then:
- Note for competitive intelligence
- Focus on your value, not their unknown weakness
- Ask good discovery questions
```

## Tone Guidelines

### Never Disparage
```
❌ "[Competitor] is terrible"
❌ "Their product is buggy"
❌ "They're going to go out of business"
❌ "I hear they have awful support"

✓ "We've heard some customers had challenges with [X]"
✓ "Where we differ is [specific capability]"
✓ "That's a different approach—here's our philosophy"
✓ "Some teams prefer [their approach], others prefer [ours]"
```

### Stay Confident, Not Arrogant
```
❌ "We're obviously better"
❌ "There's no comparison"
❌ "Anyone serious chooses us"

✓ "We're a great fit for teams that need [X]"
✓ "Customers choose us when [specific scenario]"
✓ "The difference is most noticeable in [area]"
```

### Acknowledge Their Strengths
```
"[Competitor] is solid for [use case]. Where we differ
is [your strength]—which tends to matter more when
you're focused on [prospect's stated goal]."

This builds trust by being fair and focuses on fit.
```

## Switching Conversations

### From Competitor to You
```
If they're using competitor and open to switching:

1. Understand the pain
   "What's the main thing that's not working?"

2. Validate the frustration
   "That sounds frustrating, especially when..."

3. Show your solution
   "Here's how we handle that differently..."

4. Address switching friction
   "Switching is easier than you might think. We have a
   migration team that handles everything."

5. Social proof
   "Company X made the same switch last quarter—they
   were up and running in [timeframe]."
```

### Handling "Just Signed" with Competitor
```
Prospect: "We actually just signed with [Competitor] last month"

Response:
"Congrats on making a decision! How's the implementation going?
[Pause]

Totally understand the timing isn't right for a switch.
That said, would it be helpful to stay in touch? Things
change, and I'd rather you have my info than not.

If nothing else, I'm happy to answer questions about
the space in general—no pitch, just helpful context."
```

## Documentation

### Logging Competitor Mentions
```
Track:
- Which competitor mentioned
- Context (comparing, using, heard about)
- Specific features/concerns raised
- Your response
- Outcome

Feed back to product/marketing for competitive positioning.
```

### Win/Loss Attribution
```
When deals close (won or lost):
- Primary competitor involved
- Key differentiation points
- What swayed decision
- Price difference (if known)
- Feature gaps (either way)
```
