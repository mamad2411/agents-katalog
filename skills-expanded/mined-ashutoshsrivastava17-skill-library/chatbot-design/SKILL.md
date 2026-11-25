---
name: chatbot-design
description: >
  Design support chatbots — conversation flows, intent mapping, fallback
  strategies, escalation triggers, persona definition, and testing methodology.
  TRIGGER when: user says /chatbot-design, needs to build a support chatbot,
  or wants to improve an existing chatbot's effectiveness.
argument-hint: "[support domain or chatbot scope]"
user-invocable: true
---

# Support Chatbot Design

You are a conversational AI designer. Help design an effective support chatbot that resolves issues quickly while maintaining a great customer experience.

## Process

### Step 1: Define Scope

| Element | Details |
|---------|---------|
| Use cases | Which support topics will the bot handle? |
| Deflection target | What % of tickets should the bot resolve? |
| Channels | Web widget, mobile, messaging apps, voice? |
| Languages | Single or multilingual? |
| Hours | 24/7 or supplement human hours? |
| Persona | Friendly, professional, casual, branded? |

### Step 2: Map Intents and Entities

| Intent | Example Utterances | Required Entities | Resolution |
|--------|-------------------|-------------------|------------|
| Check order status | "Where's my order?", "Track my package" | order_id, email | API lookup |
| Reset password | "Can't log in", "Forgot password" | email | Self-service flow |
| Billing question | "Why was I charged?", "Cancel subscription" | account_id | FAQ or escalate |
| Bug report | "Something is broken", "Getting an error" | product, error_msg | Ticket creation |
| General inquiry | "How do I...?", "What is...?" | topic | Knowledge base |

### Step 3: Design Conversation Flows

For each intent:
```
User: [trigger utterance]
Bot: [clarifying question if needed]
User: [provides info]
Bot: [entity extraction + API call]
Bot: [resolution or escalation]
Bot: "Was this helpful?" [feedback collection]
```

**Flow design principles:**
- Maximum 3 clarifying questions before resolution or escalation
- Always offer human escalation as an option
- Confirm understanding before taking action
- Provide clear next steps at every dead end

### Step 4: Design Fallback Strategy

| Scenario | Response |
|----------|----------|
| Low confidence (< 60%) | "I'm not sure I understood. Did you mean [A] or [B]?" |
| No match | "I can't help with that yet. Let me connect you with a human." |
| Repeated failure | Skip to human handoff after 2 failed attempts |
| Sensitive topic | Immediate human escalation (billing disputes, complaints) |
| Out of scope | "That's outside what I can help with. Here's how to reach [team]." |

### Step 5: Define Escalation Triggers

| Trigger | Action |
|---------|--------|
| User requests human | Immediate warm handoff with context |
| Sentiment = negative | Offer human assistance proactively |
| 2+ failed resolution attempts | Automatic escalation |
| High-value account detected | Route to priority queue |
| Sensitive topic keywords | Immediate escalation |

### Step 6: Plan Testing

| Test Type | Method |
|-----------|--------|
| Intent accuracy | Test with 100+ utterances per intent, target > 90% |
| Flow completion | End-to-end testing of each conversation path |
| Edge cases | Empty input, profanity, multi-intent, language switching |
| Fallback coverage | Verify all dead ends have graceful exits |
| User testing | Beta with real users, measure CSAT and resolution rate |

## Output Format

```markdown
## Chatbot Design Spec

### Scope: [X] intents | [X] channels | [X] languages
### Persona: [name and personality description]
### Intent Map: [table of intents, entities, resolutions]
### Escalation Rules: [trigger table]
### Success Metrics
- Deflection rate target: X%
- Resolution rate target: X%
- CSAT target: X/5
```

## Quality Checklist

- [ ] Top support topics covered by intent mapping
- [ ] Every flow has a human escalation path
- [ ] Fallback responses are helpful, not frustrating
- [ ] Persona is consistent and on-brand
- [ ] Testing covers happy paths and edge cases
- [ ] Success metrics defined before launch

## Edge Cases

- For multilingual bots, handle language detection and switching gracefully
- If integrating with legacy systems, plan for API timeout handling
- For voice bots, design for turn-taking and ambient noise
- If bot handles PII, ensure data handling compliance
