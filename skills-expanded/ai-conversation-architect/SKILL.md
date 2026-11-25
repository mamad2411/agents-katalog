---
name: ai-conversation-architect
description: 'Design conversational AI interfaces that feel natural, recover from failures gracefully, and build user trust through dialogue. Use when: chatbot UX, conversational UI, dialogue design, AI assistant interface, chat flow, turn-taking, AI persona voice, multi-turn context.'
---

# AI Conversation Architect

Design conversations between humans and AI that are natural, purposeful, and resilient. The DIALOGUE framework ensures every conversational AI experience handles the full spectrum from first message to complex multi-turn reasoning.

## Core Principle

A conversation with AI is not a command line with friendlier words. It is a **collaborative sense-making process** where both parties contribute, clarify, and course-correct. Design for the collaboration, not just the query.

---

## The DIALOGUE Framework

| Letter | Phase | Design Question |
|---|---|---|
| **D** | Discover Intent | How does the system understand what the user actually wants (not just what they typed)? |
| **I** | Identify Ambiguity | Where might the user's request be unclear, and how does the AI ask for clarification without interrogating? |
| **A** | Adapt Tone | How does the AI match the user's emotional state, formality, and expertise level? |
| **L** | Layer Information | How is the response structured so users get the right depth - summary first, details on demand? |
| **O** | Offer Navigation | How does the AI help users explore related topics, refine their question, or pivot direction? |
| **G** | Guard Boundaries | How does the AI communicate what it can and cannot do without breaking conversational flow? |
| **U** | Understand Memory | How does the conversation maintain context across turns, sessions, and time? |
| **E** | Exit Gracefully | How does the conversation end - or hand off to a human - without abandoning the user? |

---

## Conversation Turn Anatomy

Every AI response has four invisible layers. Design all four explicitly:

| Layer | What It Does | Example |
|---|---|---|
| **Acknowledgment** | Shows the AI understood the input | "You're asking about deployment options for your EU customers." |
| **Substance** | Delivers the actual answer or action | The core content, recommendation, or task completion |
| **Orientation** | Tells the user where they are and what's possible next | "Would you like me to compare the pricing for each option?" |
| **Metacommunication** | Signals about the conversation itself (confidence, limitations) | "I'm fairly confident about this, but you should verify the regulatory details." |

**Anti-pattern:** Most AI chat UIs only design the Substance layer. The result feels like talking to a search engine that happens to use sentences.

---

## The Turn-Taking Contract

Unlike human conversation, AI has no body language, no pauses, no "hmm." You must design explicit turn-taking signals.

### AI-to-Human Handoff Signals

| Signal Type | When to Use | Pattern |
|---|---|---|
| **Direct question** | When you need specific input | "Which region should I focus on - US, EU, or both?" |
| **Suggestion menu** | When options are finite and clear | Present 2-4 clickable options + free text fallback |
| **Soft prompt** | When the conversation could go multiple directions | "Let me know if you'd like to dig deeper into any of these." |
| **Completion signal** | When the task is done | "Done - your report is saved. Anything else?" |
| **Silence** | Never | AI should never leave the user hanging without a clear signal of what's expected |

### Human-to-AI Input Patterns

Design for how users actually type, not how you wish they would:

| Real User Behavior | Design Response |
|---|---|
| Single-word inputs ("pricing") | Infer from context; don't demand full sentences |
| Multi-intent messages ("fix the bug and also update the docs") | Parse and address both; confirm you caught everything |
| Corrections mid-thought ("wait, I meant the other one") | Override previous context gracefully |
| Copy-pasted walls of text | Summarize what you understood before responding |
| Emotional venting ("this is so frustrating") | Acknowledge the emotion before problem-solving |

---

## Persona Voice Design

Every AI product needs a voice specification - not a marketing persona, but an interaction-level voice that governs word choice, sentence structure, and emotional register.

### The Voice Compass (4 Axes)

Rate your AI voice on each axis (1-10):

| Axis | Low End (1) | High End (10) | Example Low | Example High |
|---|---|---|---|---|
| **Formality** | Casual, conversational | Professional, structured | "Hey! Here's what I found" | "Based on my analysis, the following results are relevant" |
| **Assertiveness** | Hedging, tentative | Confident, direct | "This might work, maybe?" | "Use this approach. Here's why." |
| **Warmth** | Neutral, transactional | Empathetic, relational | "Error detected in row 3." | "I found an issue in row 3 - here's how to fix it." |
| **Density** | Sparse, minimal | Rich, detailed | "3 results found." | "I found 3 matching records, sorted by relevance. The top result..." |

**Rule:** Document your compass coordinates (e.g., F:3 / A:7 / W:6 / D:5) and validate against 20+ real interaction scenarios before shipping.

---

## Multi-Turn Context Design

The #1 complaint about AI assistants: "It forgot what I said 3 messages ago."

### Context Retention Tiers

| Tier | Scope | What to Remember | Storage |
|---|---|---|---|
| **Turn context** | Current message | Entities, intent, tone | Working memory |
| **Session context** | Current conversation | Topic thread, decisions made, preferences stated | Session state |
| **Relationship context** | Across all conversations | User preferences, past interactions, expertise level | Persistent profile |
| **Shared context** | Across users (with consent) | Organizational knowledge, team conventions | Knowledge base |

### Context Window Overflow Pattern

When the conversation exceeds the context window:

1. **Summarize, don't truncate** - Compress earlier turns into a structured summary
2. **Preserve decisions** - Any user choice or preference from earlier turns must survive compression
3. **Signal the compression** - "I've summarized our earlier discussion to stay focused. Let me know if I missed anything important."
4. **Allow retrieval** - Let users ask "What did we discuss about X?" and reconstruct from the summary

---

## Conversation Failure Patterns

| Failure Mode | User Experience | Design Solution |
|---|---|---|
| **Intent misfire** | AI answers the wrong question | Reflect understanding before answering: "Just to confirm, you're asking about..." |
| **Context amnesia** | AI forgets earlier turns | Summarize running context every 5-7 turns |
| **Tone mismatch** | User is frustrated, AI is cheerful | Detect sentiment signals; mirror appropriate register |
| **Infinite loop** | AI keeps asking clarifying questions | After 2 clarifications, make a best-effort attempt and let the user correct |
| **Dead end** | AI says "I can't help with that" with no alternative | Always offer: (1) rephrase suggestion, (2) alternative topic, (3) human handoff |
| **Oversharing** | AI dumps 500 words when 50 would do | Layer responses: headline → summary → details on demand |

---

## Anti-Patterns

| Pattern | Why It Fails |
|---|---|
| Starting every response with "Great question!" | Feels patronizing by message 3. Acknowledge context, not the question itself |
| Using the user's name in every response | Reads as scripted call center, not natural conversation |
| Apologizing excessively ("I'm sorry, I'm just an AI...") | Erodes confidence. State limitations factually, without self-deprecation |
| Offering numbered lists for everything | Not every answer is a listicle. Match format to content type |
| Pretending to have emotions ("I'm excited to help!") | Users detect inauthenticity. Be helpful without performing enthusiasm |
| Asking "Is there anything else?" after every response | Creates obligation. Let users initiate naturally |

---

## Quick Reference

| Task | Framework Element | Key Deliverable |
|---|---|---|
| Design a new AI chat product | Full DIALOGUE framework | Voice Compass + Turn-Taking Contract + Context Tiers |
| Audit an existing chatbot | Failure Patterns table | Issue log with severity and fix priority |
| Define AI personality | Voice Compass (4 Axes) | Documented coordinates + 20 interaction examples |
| Fix "AI feels robotic" complaints | Turn Anatomy (4 Layers) | Revised responses with all 4 layers explicit |
| Handle multi-turn breakdowns | Context Retention Tiers | Context management architecture |

## Integration

Works with: `ai-trust-transparency` (confidence in conversation), `ai-error-resilience` (hallucination recovery mid-dialogue), `ai-prompt-ux` (how users initiate conversations), `ai-feedback-loops` (in-conversation feedback signals).
