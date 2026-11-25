---
name: chatbot-architect
description: "Use when building structured chatbot instructions or configuring no-code chatbot platforms (Voiceflow, etc.). Creates downloadable config files and step-by-step platform guides. Consolidates Chatbot Architect, Chatbot Guide Bot, and Custom UI Chatbot Assistant."
version: "1.0"
tags:
  - chatbot
  - voiceflow
  - no-code
  - conversational-design
  - customer-support
  - dialog-flow
---

# Chatbot Architect

## Overview

Designs structured chatbot conversation flows and generates platform-specific configurations for no-code chatbot builders (Voiceflow, Tidio, ManyChat, etc.). Produces downloadable config files, dialog maps, intent taxonomies, and step-by-step platform guides. Covers both rule-based and AI-augmented chatbot architectures.

## When to Use

- A user wants to build a customer support chatbot
- Designing conversation flows for a no-code platform (Voiceflow, etc.)
- Mapping intents, entities, and responses for an NLU-powered bot
- Creating a chatbot that escalates to human agents
- Building a lead generation or FAQ chatbot
- Configuring a multi-channel chatbot (web, WhatsApp, Messenger)

## How It Works

1. **Use Case Definition** — Define the chatbot's job, channel, and success metrics.
2. **Conversation Design** — Map dialog flows, intents, entities, and fallback strategies.
3. **Platform Selection** — Match requirements to the right no-code builder.
4. **Configuration Generation** — Produce platform-specific config (JSON/YAML).
5. **Testing Script** — Generate a conversation test plan for validation.

## Steps

### Step 1: Chatbot Requirements
Define:
- **Primary purpose**: Customer support, lead gen, FAQ, booking, e-commerce?
- **Channel**: Web widget, WhatsApp, Messenger, Slack, SMS?
- **Volume**: Expected conversations per day
- **Language(s)**: Single or multilingual?
- **Escalation**: When/how to hand off to a human agent
- **Tone**: Brand voice (friendly, professional, playful, empathetic)
- **Compliance**: GDPR, industry regulations, data retention

### Step 2: Intent & Entity Taxonomy
Map what users will ask and what data the bot needs to extract:

```
INTENTS:
├── greeting
│   ├── "hi", "hello", "hey there"
│   └── Response: Friendly welcome + "How can I help?"
├── check_order_status
│   ├── "where is my order", "order status", "has my package shipped"
│   └── Entities: order_number (required), email (fallback lookup)
├── return_request
│   ├── "I want to return", "start a return", "send it back"
│   └── Entities: order_number, reason (optional)
├── product_inquiry
│   ├── "do you have X", "tell me about Y", "compare A and B"
│   └── Entities: product_name, attribute (size, color, price)
├── talk_to_human
│   ├── "agent please", "real person", "not helpful"
│   └── Response: Transfer to human + collect context summary
└── fallback
    └── Response: "I didn't catch that. Can you rephrase? Or type 'agent' for help."
```

### Step 3: Dialog Flow Design
Design the conversation as a directed graph:

```
[START]
  │
  ├── intent=greeting ────────────→ [WELCOME] → [ASK_NEED]
  │
  ├── intent=check_order_status ──→ [COLLECT_ORDER_ID]
  │                                    │
  │                              order found? ──YES──→ [SHOW_STATUS] → [ANYTHING_ELSE]
  │                                    │
  │                                    NO──→ [OFFER_LOOKUP_BY_EMAIL] → [SHOW_STATUS]
  │
  ├── intent=return_request ─────→ [COLLECT_ORDER_ID] → [COLLECT_REASON] → [GENERATE_LABEL]
  │
  ├── intent=talk_to_human ──────→ [COLLECT_CONTEXT] → [TRANSFER_TO_AGENT]
  │
  └── intent=fallback ───────────→ [FALLBACK_RESPONSE] → [OFFER_AGENT]
```

### Step 4: Platform Configuration
Generate platform-specific config files:

**Voiceflow export (JSON):**
```json
{
  "version": "2.0",
  "name": "SupportBot",
  "variables": ["order_number", "user_email"],
  "intents": [
    {
      "name": "check_order_status",
      "samples": ["where is my order", "order status", "tracking"],
      "slots": [
        {"name": "order_number", "type": "alphanumeric", "required": true}
      ]
    }
  ],
  "flows": [
    {
      "id": "collect_order_id",
      "type": "question",
      "prompt": "Sure! What's your order number? It's in your confirmation email.",
      "variable": "order_number",
      "validation": "length >= 6",
      "retry_prompt": "That doesn't look right. Order numbers are 6+ characters.",
      "next": "lookup_order"
    }
  ]
}
```

### Step 5: Response & Tone Guidelines
Define voice patterns:
- **Empathy statements**: "I understand how frustrating that is."
- **Confirmation**: "Got it! Just to confirm..."
- **Transitions**: "While I look that up..."
- **Closing**: "Is there anything else I can help with today?"
- **Error recovery**: "I wasn't able to find that. Let me connect you with someone who can help."

### Step 6: Testing Script
Generate a structured test plan:
```
Test Case 1: Order Status - Happy Path
Input: "Where is my order #ABC123?"
Expected: Asks for confirmation → Shows status → Offers further help ✓

Test Case 2: Order Status - No Order Number
Input: "I want to check my order"
Expected: Asks for order number → User doesn't have it → Offers email lookup ✓

Test Case 3: Intent Confusion
Input: "I need help with my order, actually I want to return it"
Expected: Detects return intent → Confirms "Did you want to start a return?" ✓

Test Case 4: Human Escalation
Input: "This is useless, get me a real person"
Expected: Immediate escalation, no retry attempts ✓

Test Case 5: Gibberish
Input: "asdfghjkl"
Expected: Fallback response → Offers agent after 2 fallsbacks ✓
```

## Common Pitfalls

- **Over-automating**: Not everything should be a chatbot. Complex edge cases should escalate quickly, not loop in fallback.
- **No context preservation**: If a user says "it" or "that one", the bot must remember what was just discussed. Store conversation context variables.
- **Aggressive data collection**: Asking for email, phone, order number, and address before providing any value drives users away. Collect incrementally.
- **Ignoring dead ends**: Every flow path must end in resolution or escalation. No orphaned conversation states.
- **Platform lock-in**: Keep dialog logic portable. Platform-specific config should be generated, not hand-crafted, so you can switch vendors.

## Source

Consolidates: Chatbot Architect GPT, Chatbot Guide Bot GPT, Custom UI Chatbot Assistant GPT.
