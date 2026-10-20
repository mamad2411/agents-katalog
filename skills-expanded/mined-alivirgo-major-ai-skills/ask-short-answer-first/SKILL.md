---
name: ask-short-answer-first
description: "Lead with a brief direct answer and place supporting detail afterward when the reader needs a quick decision."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["bluf", "bottom-line-up-front", "conciseness", "token-efficiency", "productivity", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask for Short Answer First (The BLUF Protocol) (AI Skill)

## Overview
Default AI outputs follow an academic narrative structure: preamble $\rightarrow$ historical context $\rightarrow$ analysis $\rightarrow$ conclusion. When you need a fast answer during a meeting or while debugging a live incident, digging through 4 paragraphs to find a single line is frustrating and inefficient.

The **BLUF (Bottom Line Up Front) Protocol** forces the AI into an inverted-pyramid format: deliver the conclusive answer in the first 2 sentences, followed by an optional, structured breakdown.

---

## The Inverted Pyramid Response Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 The BLUF Output Structure                   │
│                                                             │
│  [ LEVEL 1: BLUF (Lines 1-2) ]  ──► Direct verdict / answer │
│                  │                                          │
│  [ LEVEL 2: Quick Bullet Facts] ──► 3 core supporting facts │
│                  │                                          │
│  [ LEVEL 3: Deep Dive (Optional)──► Full context / code     │
└─────────────────────────────────────────────────────────────┘
```

---

## Master BLUF Prompt Templates

### Pattern 1: The Strict 2-Line BLUF Directive
Use for quick facts, terminal commands, or Slack lookups:

```markdown
Answer this question: [INSERT QUESTION]

Formatting:
1. **Line 1 (The BLUF)**: Give the exact, direct answer or solution in bold. No greetings or preambles.
2. **Line 2**: State the primary reason or key caveat.
3. If I need a deeper explanation, I will ask for it.
```

---

### Pattern 2: The Two-Tiered Executive Brief
Use for technical architecture, business proposals, or policy questions:

```markdown
Analyze [SCENARIO / PROBLEM].

Structure your reply in two distinct sections:
### 1. Executive BLUF (Max 50 words)
State the final recommendation, estimated cost/time, and primary trade-off.

### 2. Supporting Breakdown
- 3 key bullet points explaining why this is the best path.
- 1 code snippet or implementation step if applicable.
```

---

## Real-World Comparison

### Scenario: Checking Docker Container Restart Policies

#### Verbose Standard AI Response (High Waste)
> *"Docker is a containerization platform that allows developers to run applications in isolated environments. When configuring containers, managing container lifecycles is essential. Docker provides several restart policies, including `no`, `on-failure`, `always`, and `unless-stopped`. If you want a container to automatically restart whenever Docker restarts or crashes, unless you explicitly stopped it manually, you should use the `unless-stopped` policy..."*

#### BLUF-Optimized Output (Zero Fluff, Instant Value)

> **BLUF**: Use `--restart unless-stopped`.
>
> **Why**: It automatically recovers from crashes and system reboots, but will NOT restart containers you manually stopped with `docker stop`.
>
> ```bash
> docker run -d --restart unless-stopped -p 8080:80 nginx
> ```

---

## The "Progressive Disclosure" Workflow

```
┌──────────────┐      ┌───────────────────────────┐      ┌───────────────────────────────┐
│ Ask for BLUF │ ───► │ Understand immediately in │ ───► │ If needed: "Now expand on     │
│              │      │ 5 seconds                 │      │ section 2 with full code"     │
└──────────────┘      └───────────────────────────┘      └───────────────────────────────┘
```

1. **Step 1**: Always query with a BLUF constraint first.
2. **Step 2**: If the answer is self-evident, move on with your day.
3. **Step 3 (Progressive Disclosure)**: If you need granular details, prompt: *"Expand on that with step-by-step implementation code."*

---

## Key Benefits
- ⚡ **90% Faster Reading Time**: Get straight to the decision without scrolling.
- 💰 **Saves Output Tokens**: Avoid paying for generated filler words.
- 📱 **Mobile & Chat Friendly**: Formatted perfectly for quick copy-pasting into Slack, Teams, or WhatsApp.
