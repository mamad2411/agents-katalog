---
name: chatbot-script
description: "Designs chatbot conversation flows with decision trees, handoff triggers, and fallback responses for automated customer interactions."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Chatbot Script

## When to Use This Skill

Use this skill when you need to:
- Design conversation flows for a customer-facing chatbot
- Build decision trees with branching logic and fallback responses
- Define when the chatbot should hand off to a human agent
- Create a chatbot script for sales, support, or onboarding

**DO NOT** use this skill for building or coding the chatbot, choosing chatbot platforms, or writing support response templates. This is for scripting the conversation logic.

---

## Core Principle

A CHATBOT SHOULD RESOLVE SIMPLE QUESTIONS INSTANTLY AND ROUTE COMPLEX ONES TO HUMANS GRACEFULLY — THE WORST CHATBOT IS ONE THAT LOOPS ENDLESSLY WITHOUT HELPING.

---

## Phase 1: Define Scope

Determine what the chatbot will and will not handle.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Chatbot purpose** | "What is the primary goal? (answer FAQs, qualify leads, route support, onboard users)" | Answer FAQs |
| **Platform** | "Where will the chatbot live? (website, Facebook Messenger, WhatsApp, in-app)" | Website |
| **Top scenarios** | "What are the 5-10 most common questions or requests customers have?" | No default |
| **Tone** | "How should the chatbot sound? (professional, friendly, casual)" | Friendly |
| **Business hours** | "When is a human available for handoff?" | 9 AM - 5 PM weekdays |
| **Chatbot name** | "Should the chatbot have a name?" | None / use business name |

### Scope Definition

```
## Chatbot Scope

**Handles (automated):**
- [Scenario 1 — e.g., pricing questions]
- [Scenario 2 — e.g., business hours]
- [Scenario 3]

**Routes to human:**
- [Scenario — e.g., billing disputes]
- [Scenario — e.g., complex technical issues]

**Out of scope (will not address):**
- [Topic — e.g., legal advice]
```

**GATE: Confirm scope before building conversation flows.**

---

## Phase 2: Build Flows

Design the conversation decision trees.

### Welcome Flow

```
## Welcome Message

Bot: "Hi! I am [Name/Bot] from [Business]. I can help with:

1. Pricing and plans
2. Getting started
3. Technical support
4. Talk to a human

What can I help you with?"

[User selects or types]
```

### Conversation Flow Template

For each scenario, map the full conversation:

```
## Flow: [Scenario Name]

**Trigger:** [User selects option or types keyword]

Bot: "[Opening message — acknowledge what they need]"

Bot: "[Clarifying question if needed]"
  → Option A: [Response path A]
  → Option B: [Response path B]
  → Option C: [Route to different flow]

Bot: "[Answer or action]"

Bot: "Did that answer your question?
  → Yes: "Great! Anything else I can help with?" → [Return to main menu or end]
  → No: "Let me connect you with [Name] who can help further." → [Handoff]
```

### Example: Pricing Flow

```
## Flow: Pricing

Bot: "Great question! Are you looking for:
1. Plan details and pricing
2. A custom quote
3. Information about discounts"

→ Plan details:
  Bot: "Here are our current plans:
  - [Plan A]: $X/month — [Key feature]
  - [Plan B]: $X/month — [Key feature]
  - [Plan C]: $X/month — [Key feature]

  Want to learn more about a specific plan?"
  → [User selects plan] → [Plan detail response]
  → "I want to sign up" → [Link to signup page]

→ Custom quote:
  Bot: "I would be happy to help. Let me collect a few details:
  1. What is your business name?
  2. How many [users/units/etc.]?
  3. What is your email?"
  → [Collect info] → "Thanks! Someone from our team will send you a quote within [timeframe]."
  → [Handoff: send collected info to sales]
```

**GATE: Present conversation flows for review.**

---

## Phase 3: Edge Cases

Handle the situations where the chatbot does not know the answer.

### Fallback Responses

```
## Fallback: Bot Does Not Understand

**After 1 failed attempt:**
Bot: "I did not quite catch that. Could you try rephrasing, or choose from these options?
[Show main menu options]"

**After 2 failed attempts:**
Bot: "I want to make sure you get the help you need. Let me connect you with a real person.
[Handoff trigger]"

**Never loop more than 2 times** — after 2 misunderstandings, route to human.
```

### Handoff Protocol

```
## Human Handoff

**When to hand off:**
- User explicitly asks for a human
- Bot fails to understand 2 consecutive inputs
- Topic is in the "routes to human" list
- Sentiment is angry or frustrated

**Handoff message (during business hours):**
"Let me connect you with [Name] on our team. They will be with you in about [X minutes]. While you wait, feel free to share any details about your question."

**Handoff message (after hours):**
"Our team is available [business hours]. I have saved your question — would you like us to email you at [collected email] when someone is available? Or you can reach us at [email/phone]."
```

### Dead End Prevention

Every conversation path must end with either:
1. A resolved question + "Anything else?"
2. A handoff to a human
3. A clear next action (link, email, callback)

Never leave the user with "I cannot help with that" and no alternative.

---

## Phase 4: Test and Optimize

Validate the script and plan for improvement.

### Script Testing Checklist

```
- [ ] Every flow has a clear entry point and exit point
- [ ] No dead-end paths (every branch leads somewhere)
- [ ] Fallback response triggers after 2 misunderstandings
- [ ] Handoff works during and after business hours
- [ ] Tone is consistent across all flows
- [ ] All links and resources are correct
- [ ] The bot does not overpromise or give inaccurate information
```

### Optimization Metrics

```
| Metric | Target |
|--------|--------|
| Resolution rate (resolved without human) | 60%+ |
| Handoff rate | Under 30% |
| User satisfaction (post-chat survey) | 4+/5 |
| Average conversation length | Under 5 exchanges |
| Fallback trigger rate | Under 15% |
```

### Monthly Script Review

1. What are the top questions the bot could not answer? (Add new flows)
2. Where do users drop off? (Fix that flow)
3. What new products, features, or policies need bot coverage?

---

## Anti-Patterns

- **Pretending the bot is human** — users feel tricked when they discover it. Be transparent: "I am a bot and can help with..."
- **Too many menu options** — more than 5 options at once overwhelms. Use progressive disclosure.
- **Infinite loops** — "I did not understand" repeated 5 times destroys trust. Limit to 2, then hand off.
- **No handoff option** — always give users a way to reach a human. Some issues cannot be automated.
- **Personality over function** — a chatbot that tells jokes but cannot answer questions is a liability.

---

## Recovery

- **Users ignore the chatbot:** The welcome message may be too aggressive. Try a passive approach: display the bot only after 30 seconds or on specific pages.
- **Too many handoffs:** The bot scope is too narrow. Add flows for the top handoff reasons.
- **Users type free-form and the bot fails:** Add keyword recognition for common phrases. Map "I want my money back" to the refund flow.
- **User has no chatbot platform yet:** Deliver the script as a document. It works for any platform. Recommend simple tools like Tidio, Drift, or Intercom for implementation.
- **Script is too long and complex:** Start with 3 flows (FAQ, pricing, support routing). Add more only after those work well.
