---
name: convert-voice-memos-to-bullets
description: "Convert a transcript or spoken notes into organized bullet points, decisions, and next actions."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["voice-memos", "dictation", "audio-transcripts", "summarization", "productivity", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Convert Voice Memos to Bulleted Action Plans (AI Skill)

## Overview
Speaking your thoughts into a phone voice memo or dictation app is 4x faster than typing (~150 words per minute vs. 40 wpm). However, raw voice transcripts are filled with conversational filler (*"um", "like", "you know"*), false starts, self-corrections, and rambling structure.

The **Voice Memo Structuring Protocol** transforms chaotic spoken audio transcripts into crisp, executive-ready bullet points, categorized takeaways, and prioritized tasks.

---

## The Voice-to-Insight Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                 Voice-to-Insight Pipeline                   │
│                                                             │
│  [ RAW AUDIO DICTATION / SPEECH-TO-TEXT ]                   │
│  • "Um, so I was thinking, maybe we, wait, scratch that..." │
│                           │                                 │
│                           ▼                                 │
│  [ AI DENOISER & STRUCTURING ENGINE ]                       │
│  1. Strip verbal filler & conversational hesitations        │
│  2. Resolve self-corrections (keep only latest thought)     │
│  3. Group fragmented sentences into coherent thematic blocks│
│                           │                                 │
│                           ▼                                 │
│  [ CLEAN EXECUTIVE MEMO & ACTIONABLE TASK LIST ]            │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Voice Memo Cleanup Prompts

### Pattern 1: The Daily Spoken Brain-Dump Cleaner
Use after dictating your morning thoughts or commute reflections:

```markdown
Here is the raw speech-to-text transcript from my voice memo:
[PASTE RAW TRANSCRIPT]

Task:
1. **Denoise**: Remove all verbal fillers ("um", "uh", "like", "sort of", "you know").
2. **Resolve Self-Corrections**: If I changed my mind mid-sentence (e.g., "let's do Tuesday, actually no, Wednesday"), keep only the final corrected decision.
3. **Structure Output**:
  - **Core Thesis / Insight** (1-2 clear sentences)
  - **Key Ideas & Takeaways** (Bulleted with bold headings)
  - **Action Items** (`[ ] Task description`)
```

---

### Pattern 2: The Walking Strategy Memo
Use when dictating complex business strategy while walking:

```markdown
Convert this dictated strategy rant into a formal 3-paragraph executive memo.
- Keep my original perspective, metaphors, and strong opinions intact.
- Organize the arguments in logical progression from Problem $\rightarrow$ Root Cause $\rightarrow$ Proposed Solution.
- Conclude with a Next Steps checklist.
```

---

## Real-World Case Study

### Scenario: Post-Client Call Dictation

#### Raw Spoken Dictation Transcript
> *"Hey, just got out of the sync with Acme Corp, uh, Mark was really concerned about the Q3 delivery date, he thinks October is too late, wants it by mid-September. Lisa agreed we can pull it in if we drop the PDF export feature for v1, wait, actually we can keep the CSV export and just drop the PDF one. Oh and Mark needs the security audit report sent over by this Friday or legal won't sign. I need to ping Dave about that today."*

#### Structured Output (Clean & Actionable)

> ### Acme Corp Q3 Scope & Timeline Alignment
> 
> **Core Decisions**:
> - **Accelerated Launch**: Target release moved up from October to **mid-September** per client request.
> - **Scope Trade-off**: Preserving **CSV Export** for v1, while deferring **PDF Export** to v2 to meet the accelerated timeline.
>
> **Action Items**:
> - [ ] **Security Audit Delivery** (Owner: Dave / Deadline: This Friday) - Send completed SOC2 / security report to Acme Corp legal to unblock contract signing.
> - [ ] **Roadmap Scope Update** - Adjust sprint backlog to remove PDF export from the mid-September release milestone.

---

## Tips for High-Leverage Voice Prompting
- **Don't filter yourself while speaking**: Just talk freely. The AI excels at identifying intent and discarding verbal clutter.
- **Explicitly signal decisions**: Say keywords like *"Action item for Dave..."* or *"Core decision..."* into the mic to make parsing effortless.
