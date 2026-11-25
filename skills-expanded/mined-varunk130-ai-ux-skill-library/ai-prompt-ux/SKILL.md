---
name: ai-prompt-ux
description: 'Design the input experience for AI products - how users craft, structure, and refine their instructions to AI systems. Use when: prompt interface, AI input design, prompt templates, prompt suggestions, context window UX, instruction design, AI input affordances, prompt engineering UX.'
---

# AI Prompt UX

Design the input side of AI interactions - how users express their intent, refine their requests, and learn to communicate effectively with AI. The CRAFT framework treats the prompt experience as a design surface, not just a text box.

## Core Principle

A blank text box is not a prompt UX. It is an **abdication of design.** The empty chat input puts 100% of the burden on the user to figure out what to say, how to say it, and what's possible. Great prompt UX reduces that burden to near zero while preserving unlimited expressiveness for power users.

---

## The CRAFT Framework

| Letter | Principle | Design Question |
|---|---|---|
| **C** | Constrain Productively | Does the input interface guide users toward better prompts without limiting expressiveness? |
| **R** | Reveal Capabilities | Can users discover what's possible through the input experience itself? |
| **A** | Assist Construction | Does the interface help users build complex prompts piece by piece? |
| **F** | Format Intelligently | Does the system interpret intent regardless of how the user formatted their input? |
| **T** | Teach Through Interaction | Does each interaction make the user slightly better at prompting? |

---

## The Prompt Input Spectrum

Not every AI product should use a blank text box. Choose the right input pattern for your context:

| Pattern | User Freedom | Guidance Level | Best For | Example |
|---|---|---|---|---|
| **Free text** | Maximum | Minimum | Expert users, open-ended exploration | ChatGPT main input |
| **Guided text** | High | Medium | Most users, most products | Text box with placeholder text: "Ask me to analyze, write, or research..." |
| **Template selection** | Medium | High | Specific workflows, recurring tasks | "Summarize this document" / "Compare these options" / "Draft an email about..." |
| **Structured form** | Low | Maximum | Domain-specific tools, non-technical users | Form fields: Subject, Tone, Length, Audience, Key points |
| **Hybrid** | Variable | Variable | Products serving diverse users | Text box + expandable "Advanced options" panel |

### Selection Criteria

| If your users are... | And the task is... | Use this pattern |
|---|---|---|
| Technical, experienced with AI | Open-ended, creative | Free text or guided text |
| Non-technical, new to AI | Specific, repeatable | Template selection or structured form |
| Mixed expertise | Variable complexity | Hybrid (text + templates + structured options) |
| Under time pressure | High-frequency, quick | Template selection with one-click execution |

---

## Empty State Design

The moment before the first prompt is the most critical UX moment.

### The Empty State Hierarchy

| Priority | Element | Purpose | Example |
|---|---|---|---|
| 1 | **Single clear action** | Tell the user exactly what to do first | Input field with cursor blinking, focused |
| 2 | **Capability hints** | Show 3-4 things the AI can do | Clickable suggestion chips: "Summarize a doc" / "Write an email" / "Analyze data" |
| 3 | **Example prompts** | Show what good prompts look like | "Try: 'Compare the quarterly revenue trends and highlight anomalies'" |
| 4 | **Recent history** | Bring users back to where they left off | "Continue your conversation about Q2 planning" |

**Anti-pattern:** An empty screen with just a text box and "How can I help you?" This communicates nothing about capabilities, nothing about prompt quality, and nothing about what to expect.

---

## Prompt Suggestion Systems

### Suggestion Types

| Type | When It Appears | What It Contains | Example |
|---|---|---|---|
| **Pre-prompt suggestions** | Before user types anything | Common starting points for this context | Chips: "Summarize" / "Translate" / "Explain" |
| **Inline autocomplete** | While user is typing | Completion of the current prompt | User types "Help me write" → suggestion: "...a professional email to decline a meeting" |
| **Follow-up suggestions** | After AI responds | Logical next questions or actions | "Go deeper on point 2" / "Make it shorter" / "Generate alternatives" |
| **Refinement suggestions** | When output quality is low | Ways to improve the prompt | "Try being more specific about the time period" |

### Suggestion Quality Rules

| Rule | Why It Matters |
|---|---|
| Suggestions must be contextual, not generic | "Tell me more" is not useful. "Explain the pricing implications" is |
| Limit to 3-5 suggestions at a time | More than 5 creates decision paralysis |
| Suggestions should be full, executable prompts | One click should produce a result, not just populate the input field |
| Rotate suggestions to prevent stale UX | Same 3 suggestions every time = users ignore them after day 2 |
| Power users should be able to hide suggestions | Don't force training wheels on experts |

---

## Multi-Modal Prompt Design

Modern AI accepts more than text. Design for all input modes:

| Input Mode | Design Considerations | UX Pattern |
|---|---|---|
| **Text** | Character limit, formatting support, code blocks | Standard text area with markdown support |
| **File upload** | Supported formats, size limits, processing time | Drag-and-drop zone with format badges |
| **Image/screenshot** | Resolution requirements, what the AI "sees" | Paste or drop with annotation overlay: "What should I focus on in this image?" |
| **Voice** | Transcription accuracy, ambient noise, language | Push-to-talk with real-time transcription preview |
| **URL/link** | What gets fetched, what's processed, privacy implications | Paste field with preview: "I'll read [title] - what would you like to know about it?" |
| **Structured data** | CSV, JSON, database connections | Upload + preview table + "What would you like to analyze?" |

### Multi-Modal Orchestration

When users can input multiple modes simultaneously:

| Combination | Design Pattern | Example |
|---|---|---|
| Text + Image | Text as instruction, image as context | "What's wrong with this UI?" + [screenshot] |
| Text + File | Text as question, file as data source | "Summarize the key findings" + [PDF upload] |
| Text + URL | Text as analysis angle, URL as source | "Compare this pricing page to our competitors" + [URL] |

**Rule:** When multiple inputs are provided, the AI should acknowledge ALL inputs in its response. Don't silently ignore the attachment.

---

## Prompt History & Reuse

### Prompt Library Pattern

For products where users repeatedly need similar AI assistance:

| Feature | Implementation | Benefit |
|---|---|---|
| **Prompt history** | Searchable list of past prompts with their results | Quick reuse of successful prompts |
| **Saved prompts** | User-created templates with variables: "Write a {tone} email to {recipient} about {topic}" | Repeatability without retyping |
| **Shared prompts** | Team-visible prompt library | Organizational knowledge sharing |
| **Prompt analytics** | Show which prompts produce the best results | Data-driven prompt improvement |

---

## The Prompt Refinement Loop

Most good AI interactions require 2-3 iterations. Design for the refinement cycle, not just the first prompt.

### Refinement Patterns

| Pattern | How It Works | When to Use |
|---|---|---|
| **Inline edit** | User modifies the original prompt and re-runs | When the core intent was right but details need adjustment |
| **Follow-up instruction** | "Make it shorter" / "Focus more on the technical details" | When the direction is right but output needs tuning |
| **Branching** | "Try a completely different approach" | When the first attempt was fundamentally wrong |
| **Parameter adjustment** | Sliders or dropdowns for tone, length, formality, creativity | When the AI supports tunable parameters |
| **Undo and rephrase** | Discard current response, try a new prompt | When the user wants a fresh start without losing context |

---

## Anti-Patterns

| Pattern | Why It Fails |
|---|---|
| Blank text box with no guidance | Users don't know what's possible, write bad prompts, get bad results, leave |
| "Be more specific" error messages | Tells the user they're wrong but doesn't help them be right |
| Character limits without explanation | "Prompt too long" - how long? What to cut? Why is there a limit? |
| Hiding prompt history | Users can't learn from their own past successes |
| Suggestion chips that don't do anything | Chips that only populate the text box instead of executing the prompt |
| Auto-submitting on paste | Users paste text as context, not as a prompt. Don't fire automatically |

---

## Quick Reference

| Task | Framework Element | Key Deliverable |
|---|---|---|
| Design input for new AI product | Prompt Input Spectrum + Empty State | Input pattern selection + empty state design |
| Reduce "I don't know what to type" | Suggestion Systems | Pre-prompt, inline, and follow-up suggestion architecture |
| Add multi-modal input | Multi-Modal Prompt Design table | Input mode support matrix + orchestration rules |
| Improve prompt quality across user base | Refinement Loop patterns | Iteration flow design + refinement shortcuts |
| Build enterprise prompt management | Prompt Library Pattern | Shared prompt library with history and analytics |

## Integration

Works with: `ai-onboarding-calibration` (teaching prompting during onboarding), `ai-conversation-architect` (prompt as first turn in dialogue), `ai-feedback-loops` (feedback on prompt suggestions), `ai-personalization-ethics` (personalized prompt suggestions).
