---
name: add-your-own-human-voice
description: "Revise AI-assisted writing to preserve the author's voice, concrete experience, and intended tone."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["writing", "human-voice", "tone-matching", "authenticity", "anti-ai-cliches", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Add Your Own Human Voice (AI Skill)

## Overview
Default AI writing has recognizable fingerprints: corporate buzzwords (*"delve", "testament", "tapestry", "crucial", "leverage"*), monotonous sentence lengths, forced enthusiasm, and impersonal third-person generalities. 

This skill provides a systematic framework to strip out AI synthetic markers and inject authentic human tone, lived experience, idiosyncratic perspective, and conversational cadence into AI-assisted drafts.

---

## The Human-in-the-Loop Voice Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                    The 4-Layer Voice Stack                    │
│                                                               │
│  Layer 1: The Raw Experience   ──► Personal notes & anecdotes │
│             │                                                 │
│  Layer 2: Style Constraints    ──► Banned words, cadence rules│
│             │                                                 │
│  Layer 3: AI First Pass        ──► Structural drafting only   │
│             │                                                 │
│  Layer 4: Human Polish         ──► Reading aloud, cadence cut │
└───────────────────────────────────────────────────────────────┘
```

1. **Provide the "Messy Human Angle" First**: Never ask an AI to invent a personal story. Provide 2-3 rough bullet points of actual events, quotes, or feelings from your own day.
2. **Set a Negative Constraint List**: Explicitly ban AI tell-tale vocabulary and throat-clearing preambles.
3. **Tone Mirroring via Sample Text**: Feed 200-300 words of your own past writing and instruct the model to analyze and mirror your sentence lengths, vocabulary density, and punctuation quirks.
4. **Vary Sentence Rhythm (Burstiness)**: Human writing mixes ultra-short punchy sentences with longer, compound thoughts. AI writing defaults to uniform 18-word sentences.

---

## The Master Human Voice Prompt Template

Use this prompt wrapper whenever drafting emails, articles, newsletters, or social posts:

```markdown
Draft a [FORMAT: e.g., email / blog section / LinkedIn post] about [TOPIC].

Here is my raw perspective and the core points I want to convey:
- [Point 1: Raw detail or opinion]
- [Point 2: Concrete lesson learned or mistake made]
- [Point 3: Key takeaway or call to action]

Style Guidelines:
1. Tone: Conversational, candid, pragmatic, and direct - like an experienced colleague sharing notes over coffee.
2. Ban all AI clichés: Do not use "delve", "tapestry", "embark", "testament", "beacon", "game-changer", "dive deep", "in today's fast-paced world", or "unleash".
3. Sentence Rhythm: Mix short 2-5 word sentences with longer descriptive sentences. Avoid uniform sentence length.
4. Voice: Use first-person ("I", "we") and active verbs. Avoid passive academic language.
5. Cut the throat-clearing: Start immediately with the hook or insight - no greeting fluff or introductory summaries.
```

---

## Real-World Comparisons

### Example 1: Explaining a Product Launch Delay

#### Generic Robotic AI Output (Ineffective)
> *"In today's fast-paced tech landscape, ensuring seamless user satisfaction is of paramount importance. As a testament to our commitment to excellence, we have made the strategic decision to recalibrate our launch roadmap. This slight detour will empower our development ecosystem to deliver an unparalleled product experience."*

#### Human-Voiced AI Output (Trained & Constrained)
> *"We were supposed to launch our new billing dashboard on Tuesday. We didn't. When we stress-tested 5,000 simultaneous checkouts on staging, payment webhooks failed on 4% of orders. Launching on time with broken billing isn't acceptable. We've traced the bug to a race condition in the Stripe queue, fixed the handler, and rescheduled launch for next Thursday. Thank you for your patience."*

---

### Example 2: LinkedIn Insight Post

#### Master Voice Prompt Recipe
> **User Prompt**:
> *"Write a 120-word post about remote team management. 
> My core point: Daily standup meetings often turn into mindless status reports where nobody listens. We replaced them with a 3-question Slack bot check-in at 9 AM, and engineering velocity jumped 25%.
> Tone: Casual, no cheesy corporate jargon, start with the painful reality."*

#### AI Response
> Most daily standups are a waste of 15 minutes. 
> 
> Eight people sit on Zoom waiting for their turn to speak, secretly tuning everyone else out until their name is called. It breaks flow state before 10 AM.
> 
> Three months ago, we killed the morning meeting. We replaced it with an automated 9 AM Slack prompt:
> 1. What did you ship yesterday?
> 2. What are you building today?
> 3. Where are you blocked?
> 
> It takes 90 seconds to read. People actually read it. Engineering velocity climbed 25%, and our team gets two hours of uninterrupted morning focus back.
> 
> Kill the status meeting. Keep the sync.

---

## The "Banned Words & Clichés" Cheat Sheet

Add these banned tokens to your custom instructions or system prompts:

| Category | Banned AI Words / Phrases | Human Replacement |
| :--- | :--- | :--- |
| **Introductory Fluff** | *"In today's fast-paced digital world..."*, *"It is important to remember..."* | Cut entirely. Start on the action. |
| **Buzzwords** | *Delve, tapestry, testament, revolutionize, beacon, plethora* | *Look into, proof, change, guide, many* |
| **Transitions** | *Furthermore, moreover, in conclusion, it is worth noting* | *Also, but, and, here's why* |
| **Adjective Overkill** | *Paramount, crucial, quintessential, indispensable* | *Key, vital, critical, important* |

---

## Actionable Takeaway Workflow
1. **Speak before you prompt**: Use voice-to-text to dictate your raw, unedited thoughts for 60 seconds.
2. **Feed the transcript to the AI**: *"Organize these spoken thoughts into 3 concise paragraphs. Keep my informal tone and humor intact."*
3. **The Out-Loud Test**: Read the final draft out loud. If you stumble or feel awkward saying a phrase in real life, delete or rewrite it.
