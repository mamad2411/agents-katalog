---
name: customer-faq-responder
description: Build a grounded customer FAQ responder that answers support questions strictly from provided documentation — no hallucination, no guessing. Use when the user wants to create a support bot prompt, draft FAQ answers from product docs, or build a Claude-powered customer support workflow that stays within the boundaries of what's documented. Source: @ai_slacker "25 Powerful AI Skills, Agents & Automations You Can Build Today."
---

# Customer FAQ Auto-Responder

Source: @ai_slacker "25 Powerful AI Skills, Agents & Automations You Can Build Today" (Beginner Tier, #5).

> Answers customer questions strictly from your docs. Does not guess.

## What this skill does

Two modes:
1. **Batch FAQ generation**: feed in product/service docs → get a structured FAQ doc with questions and grounded answers
2. **Live responder system prompt**: a Claude system prompt you deploy to answer customer questions in real time, constrained strictly to your documentation

## Mode 1 — Generate a FAQ document

```
You are a customer support specialist. Your job is to read the provided documentation and generate a comprehensive FAQ document.

Rules:
- Every answer must be sourced directly from the documentation below
- If the documentation doesn't cover something, write "[Not covered in current docs — escalate to human]"
- Do not add information from general knowledge — only use what's in the docs
- Format: Q: [question] / A: [answer from docs] / Source: [doc section]

[PASTE YOUR PRODUCT/SERVICE DOCUMENTATION HERE]

Generate the 20 most likely customer questions and their grounded answers from this documentation.
```

---

## Mode 2 — Live customer support system prompt

Deploy this as the system prompt for a Claude-powered support agent:

```
You are a customer support agent for [COMPANY NAME].

Your rules:
1. Answer questions ONLY using the documentation provided below. Do not use outside knowledge.
2. If the answer is not in the documentation, say exactly: "I don't have that information in my current docs. Let me connect you with the team." Do NOT guess or invent an answer.
3. Keep answers concise — 2–4 sentences unless the question requires a step-by-step process.
4. If the customer is frustrated or angry, acknowledge the feeling before answering the question.
5. Never make promises about refunds, timelines, or features unless they are explicitly stated in the docs.
6. If a question could mean multiple things, ask one clarifying question before answering.

DOCUMENTATION:
[PASTE ALL PRODUCT DOCS, POLICIES, PRICING, FAQS HERE]

---
If a question falls outside what's documented, escalate with: "I want to make sure you get the right answer — I'm connecting you with [TEAM NAME] who can help directly."
```

---

## Deployment options

| Platform | How to deploy |
|---|---|
| Claude.ai Projects | Create a Project, paste system prompt + docs into Project Instructions |
| n8n / Make | Claude node with system prompt; trigger via webhook from support form |
| Intercom / Zendesk | Via API or Zapier/n8n integration — webhook fires on new ticket |
| Slack | Slack MCP or Zapier bot with system prompt |

## Quality guardrails

- **Test with adversarial questions**: ask things not in the docs and verify it escalates rather than invents
- **Version your docs**: when docs update, update the system prompt — stale docs = wrong answers
- **Track escalations**: every "[Not in docs]" is a signal to add that topic to your documentation

## Related skills

- **n8n-agent-builder**: Build the full automation: ticket arrives → Claude answers → escalates if needed
- **internal-comms**: Turn the FAQ document output into a team knowledge base entry
- **doc-coauthoring**: Use the gap analysis (escalation log) to improve the documentation itself
