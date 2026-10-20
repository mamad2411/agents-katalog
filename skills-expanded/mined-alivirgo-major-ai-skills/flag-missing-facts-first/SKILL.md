---
name: flag-missing-facts-first
description: "Identify facts that are required for a reliable answer and distinguish them from optional context."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["fact-checking", "information-readiness", "clarification", "pre-flight-check", "debugging", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Flag Missing Facts First (The 10/10 Information Readiness Check) (AI Skill)

## Overview
When users provide incomplete data to an AI assistant (*"My Python script crashes with an error, how do I fix it?"*), most models begin guessing wild possibilities rather than asking for the stack trace or environment details.

The **10/10 Information Readiness Check** instructs the AI to pause, identify the exact missing variables required to deliver a perfect, definitive answer, and request them in a structured intake checklist.

---

## The Information Readiness Gate

```
┌─────────────────────────────────────────────────────────────┐
│                 Information Readiness Gate                  │
│                                                             │
│  User Initial Prompt (Incomplete Data)                      │
│            │                                                │
│            ▼                                                │
│  [ PRE-FLIGHT AUDIT: Rate Information Completeness /10 ]    │
│            │                                                │
│            ▼                                                │
│  [ List 3-4 Missing Concrete Facts Needed for a 10/10 ]     │
│            │                                                │
│            ▼                                                │
│  User Supplies Missing Facts ──► 100% Definitive Solution   │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Information-Audit Prompt Templates

### Pattern 1: The "10/10 Readiness" Directive
Use before launching any complex analysis, debugging, or proposal:

```markdown
I want to [INSERT PROJECT / TASK: e.g. Design our database sharding strategy].

Here is what I have so far: [PASTE CURRENT NOTES / DATA].

Do NOT attempt to write the final solution yet.
1. Rate the completeness of my prompt on a scale of 1 to 10.
2. List the **top 3 missing facts or parameters** you need from me to give a 10/10 production-ready response.
3. For each missing fact, give an example of what a good answer looks like.

Wait for my response.
```

---

### Pattern 2: The Bug & Diagnostic Intake Form
Use for engineering, IT support, or system troubleshooting:

```markdown
I have a bug in my application: [BRIEF SUMMARY].

Act as a Principal Support Engineer:
- Generate a 4-point diagnostic intake checklist of the exact error logs, environment variables, and reproduction steps you need to pinpoint the root cause.
```

---

## Real-World Case Study

### Scenario: Troubleshooting a Slow React Application

#### Weak Prompt (Guesswork & Speculation)
> **User**: *"My React app is rendering slowly when users scroll the feed. How do I fix it?"*
> 
> ❌ *AI guesses 10 generic optimizations: useMemo, useCallback, React.memo, virtualized lists, image lazy loading, debounce scroll, code splitting... (Leaves the user overwhelmed with trial-and-error).*

#### 10/10 Readiness Prompt & Structured Intake
> **User**: *"Before suggesting fixes, what 3 profiling facts do you need to diagnose why my React feed is lagging?"*

**AI Response**:
> To give you the exact fix rather than generic advice, please provide:
> 1. **Component Tree Depth & State Location**: Is the scroll state held in the root parent or localized?
> 2. **DOM Node Count**: How many DOM nodes are rendered simultaneously when scrolling (e.g. 50 items vs 5,000 items)?
> 3. **React DevTools Profiler Output**: Which specific component shows the highest "Render duration" flamegraph bar?

**Result**: The user checked the Profiler, found that a single un-memoized SVG icon component was re-rendering 2,000 times, and fixed it in 30 seconds.

---

## The 10/10 Rule
> **"1 minute spent providing the missing facts saves 30 minutes of debugging generic AI hallucinations."**
