---
name: chatgpt-astra-cheatsheet
description: Cheat sheet for ChatGPT 6 Astra — key capabilities, prompt patterns, and use cases for the multimodal, agentic version of ChatGPT. Use when onboarding to Astra's real-time voice, vision, and computer-use features, or when designing prompts that leverage live context from camera/screen. Source: @51ultron.
---

# ChatGPT 6 Astra — Cheat Sheet

A reference for the capabilities and prompt patterns for ChatGPT 6 Astra (OpenAI's multimodal, agentic assistant).

---

## What makes Astra different from standard ChatGPT

| Feature | Standard ChatGPT | Astra |
|---|---|---|
| Voice | Push-to-talk (Advanced Voice Mode) | Real-time continuous voice conversation |
| Vision | Upload image → analyse | Live camera feed → real-time visual context |
| Screen | Screenshot → analyse | Live screen reading + computer use |
| Memory | Optional persistent memory | Active contextual memory across sessions |
| Agentic | Tool use (Code Interpreter etc.) | Full computer use + autonomous multi-step tasks |

---

## Core prompt patterns

### Real-time vision prompts

```
"Look at what's on my screen and tell me what this error means."
"I'm looking at a physical document — read it and summarise the key points."
"Watch me code and let me know when I make a mistake."
```

### Computer use patterns

```
"Open my email, find the most recent invoice from [Vendor], and tell me the total."
"Search for flights from Athens to London for next Tuesday and show me the cheapest options."
"Fill out this form using the information I'll dictate to you."
```

### Real-time conversation patterns

```
"Let's talk through this architecture decision — I'll share my screen."
"I'm going to interview you as a senior engineer. Ask me technical questions and give feedback."
"Be my live interpreter. I'll speak in English; respond in Greek."
```

---

## Capability reference

### Vision
- **Live camera**: Describe objects, read text, identify plants/products, guide step-by-step tasks
- **Screen sharing**: Debug UI, review code, explain charts/dashboards
- **Document reading**: Handwritten notes, printed forms, whiteboards

### Voice
- **Natural conversation**: Interruption, follow-up, tone adjustment mid-sentence
- **Languages**: 50+ languages with real-time translation
- **Dictation**: Extended voice memos → structured output

### Computer Use
- **Browser**: Navigate, fill forms, extract data from web pages
- **Files**: Open, read, edit documents (Word, PDF, spreadsheets)
- **Apps**: Interact with desktop software via visual understanding

---

## Tips & gotchas

- **Be specific about scope**: "Only look at the top half of the screen" prevents misidentification
- **Confirm before action**: For irreversible computer-use tasks, ask Astra to confirm before executing
- **Chain steps explicitly**: "Do X, then wait for my confirmation, then do Y" prevents runaway execution
- **Image quality matters**: Hold the camera still; real-time vision degrades with motion blur
- **Privacy**: Don't point the camera at sensitive documents in a shared screen-recording scenario

---

## Sample use cases by role

| Role | Use case |
|---|---|
| Developer | Live code review, error debugging, documentation reading |
| Designer | Real-time feedback on UI mockups, colour checks, accessibility |
| Executive | Briefing from a printed document while hands-free |
| Student | Homework explanation via camera on textbook |
| Sales | Real-time CRM navigation + call note capture |

Source: @51ultron
