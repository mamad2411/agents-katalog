---
name: keep-instructions-friendly-and-clear
description: "Separate instructions, context, and examples with clear structure and delimiters."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["prompt-structure", "markdown-delimiters", "xml-tags", "formatting", "clarity", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Structure Instructions with Clear Markdown Delimiters (AI Skill)

## Overview
When a prompt is written as a continuous, unformatted block of stream-of-consciousness text, the AI's attention mechanism easily conflates **instructions** (*"Do not include pricing"*) with **data context** (*"Here is the pricing document"*).

The **Markdown Delimiter Protocol** uses clear typography - Markdown headers, bullet lists, code blocks, and XML tags - to cleanly segregate system instructions from background data, eliminating ambiguity.

---

## Chaotic Wall of Text vs. Delimited Structure

```
┌─────────────────────────────────────────────────────────────┐
│                 Prompt Layout Comparison                    │
│                                                             │
│  Chaotic Stream-of-Consciousness:                           │
│  "Hey I want to write a blog post about databases and here  │
│   is my notes postgres is good mongo is bad also make it    │
│   under 200 words and use a friendly tone don't use jargon" │
│  ↳ High ambiguity, skipped constraints                      │
│                                                             │
│  Structured Markdown Delimiters:                            │
│  ### Goal                                                   │
│  Draft a blog post comparing PostgreSQL and MongoDB.        │
│                                                             │
│  ### Context & Source Data                                  │
│  <raw_notes> [PASTE NOTES] </raw_notes>                     │
│                                                             │
│  ### Constraints                                            │
│ - Length: Under 200 words                                  │
│ - Tone: Friendly, zero technical jargon                    │
│  ↳ 100% Parsing Accuracy, Zero Constraint Bleed             │
└─────────────────────────────────────────────────────────────┘
```

---

## The Master 4-Block Delimiter Template

Copy and paste this clean layout for any multi-part request:

```markdown
### 🎯 Objective
[1-sentence summary of what you need]

### 📂 Source Data / Context
<context>
[PASTE YOUR RAW TEXT / CODE / NOTES HERE]
</context>

### ⚠️ Constraints & Guardrails
- **Tone**: [e.g. Executive, Conversational, Technical]
- **Length**: [e.g. Under 150 words / Exactly 3 bullets]
- **Banned Words**: [e.g. No corporate buzzwords, no emojis]

### 📋 Expected Output Format
[e.g. A 3-column Markdown table with headers: Tool, Pros, Cons]
```

---

## Why XML-Style Tags (`<context>...</context>`) Work So Well
Modern LLMs (Claude, GPT-4, Gemini) are heavily fine-tuned on code and XML structures. Wrapping your source material in `<document>` or `<notes>` tags creates an impenetrable boundary between your instructions and the text being analyzed, completely neutralizing prompt injection risks and confusion.

---

## Summary Best Practices
- **Use whitespace**: A blank line between sections helps both human eyes and model tokenizers.
- **Use bold anchors**: Format constraints as `- **Constraint Name**: Details`.
- **Enclose reference text in code fences or XML tags**: Keeps raw data strictly isolated from command logic.
