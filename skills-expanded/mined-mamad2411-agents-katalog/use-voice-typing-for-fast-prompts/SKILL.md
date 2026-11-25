---
name: use-voice-typing-for-fast-prompts
description: "Turn dictated context into a clear prompt with explicit goals, constraints, and corrected names or numbers."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["voice-dictation", "brain-dump", "workflow-speed", "context-density", "productivity", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Use Voice Typing for Rich Context (The 150-WPM Brain Dump) (AI Skill)

## Overview
The #1 cause of poor AI outputs is **Context Starvation**: users type a rushed, 1-sentence prompt (*"Write an email to my team about our roadmap changes"*) because typing on a keyboard is slow and friction-heavy ($~40\text{ words/minute}$).

Human speech flows at **150 to 180 words per minute**. 

The **Voice Dictation Protocol** leverages speech-to-text tools (Superwhisper, Mac Dictation, Whisper AI, or iOS Voice) to deliver a 60-second raw brain dump of rich nuances, edge cases, and emotional context without typing fatigue.

---

## Typing Fatigue vs. Voice Context Density

```
┌─────────────────────────────────────────────────────────────┐
│                 Prompt Context Density                      │
│                                                             │
│  Typed Prompt (40 WPM / 20 Seconds):                        │
│  "Write an email about moving sprint to next week."         │
│  ↳ 10 words, 0 context, generic output                      │
│                                                             │
│  Voice-Dictated Brain Dump (160 WPM / 20 Seconds):          │
│  "Hey draft an email to the frontend team. We have to move  │
│   the sprint deadline to next Thursday because Dave is on   │
│   sick leave and the Stripe webhook tests are taking longer.│
│   Keep it encouraging, mention pizza on launch day."        │
│  ↳ 50+ rich words, complete nuance, flawless output         │
└─────────────────────────────────────────────────────────────┘
```

---

## The 2-Step Voice Prompting Workflow

```
┌───────────────────────────────────────────────────────────────────────────┐
│ STEP 1: Speak Freely (Don't worry about punctuation, 'ums', or grammar)   │
│ STEP 2: Append the "Cleanup & Structure" Instruction                      │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Master Voice Cleanup Prompt Modifiers

Append this 1-liner to the start or end of any spoken brain dump:

```markdown
I just dictated the following stream of thought using voice typing. 
Filter out conversational filler ("ums", repetitions, self-corrections) and:

1. Extract the core decisions and tasks.
2. Draft the final [DELIVERABLE: e.g. Executive Slack Update / Client Memo].

Dictation:
"[SPOKEN TEXT FROM VOICE TYPING]"
```

---

## Real-World Case Study

### Scenario: Walking Out of a 1-on-1 Client Sync

#### User's 45-Second Voice Dictation (While Walking to Next Meeting)
> *"Okay AI, I just met with Sarah from Acme. She loves the design preview we sent yesterday, but she's super nervous about mobile load times because 80% of their shoppers are on phones. She also asked if we can push back the final sign-off from Friday to next Tuesday so their VP of Product can review it. Draft a warm follow-up email confirming the Tuesday extension and explaining that our WebP image compression pipeline will keep mobile load times under 1.2 seconds."*

#### AI-Generated Output (Generated in 3 Seconds)
> **Subject**: Acme Mobile Design Sync & Tuesday Timeline Confirmation
> 
> Hi Sarah,
> 
> Great catching up today! Thrilled to hear you loved the initial design direction.
> 
> To follow up on our discussion:
> 1. **Timeline Extended**: We've updated the final sign-off date to **next Tuesday, August 29th**, so your VP of Product can participate in the review.
> 2. **Mobile Speed Guarantee**: Mobile performance is our top priority. With our automated WebP compression and CDN edge caching, mobile load times will remain strictly under 1.2 seconds across all devices.
> 
> Looking forward to connecting next Tuesday!
> 
> Best,  
> [Your Name]

---

## Summary Best Practices
- **Never edit your speech while talking**: Speak in continuous stream-of-consciousness; the AI will parse your true intent flawlessly.
- **Use keyboard shortcuts**: Map a single key (e.g. `Fn Fn` or `Caps Lock`) to trigger local Whisper or OS dictation instantly.
