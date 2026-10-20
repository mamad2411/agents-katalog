---
name: save-favorite-prompts-cheat-sheet
description: "Organize reusable prompts in a concise reference with clear task labels and editable placeholders."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["cheat-sheet", "prompt-library", "quick-reference", "productivity", "workflows", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Save Favorite Prompts in a Cheat Sheet (The 1-Page Desk Reference) (AI Skill)

## Overview
Searching through dozens of past chat threads to find *"that one prompt that generated the perfect table last month"* wastes cognitive energy.

The **1-Page Prompt Cheat Sheet Protocol** consolidates your top 8 most versatile, battle-tested prompt modifiers into a clean, printable or pin-able Markdown document for instant reference at your desk.

---

## The 4-Category Cheat Sheet Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 1-Page Master Cheat Sheet                   │
│                                                             │
│  [ 1. CODING & DEBUGGING ]    ──► Strict types, null-checks │
│  [ 2. EDITING & POLISH ]      ──► Human voice, no buzzwords │
│  [ 3. DATA & SYNTHESIS ]      ──► TSV tables, BLUF digests  │
│  [ 4. DECISION & STRATEGY ]   ──► Pre-mortem, 3 options     │
└─────────────────────────────────────────────────────────────┘
```

---

## The Master 1-Page Prompt Cheat Sheet

Copy and pin this block into a pinned note in Notion, Apple Notes, or Obsidian:

### 🛠️ 1. Coding & Engineering
```markdown
# Strict Bug Fixer
"Audit this code for thread-safety, memory leaks, and unhandled nulls. 
Provide ONLY the corrected, production-ready code with type hints."

# Unit Test Generator
"Write pytest/vitest unit tests for this function covering happy path, 
empty/null input, and network timeout edge cases."
```

### ✍️ 2. Writing & Communication
```markdown
# Human Voice Polish
"Refactor this draft to sound conversational, confident, and warm. 
Ban 'delve', 'tapestry', 'crucial', 'testament'. Keep under 100 words."

# Negative Preamble Suppressor
"Draft the reply. Output final text ONLY - no introductory or closing chat fluff."
```

### 📊 3. Data & Executive Synthesis
```markdown
# 1-Click Excel TSV Table
"Extract the key data above into a TSV code block with headers: 
Date (YYYY-MM-DD), Item, Category, Amount (Number). No currency symbols."

# Executive 2-Tier BLUF
"Provide: 1) A 2-sentence Executive BLUF at the top in bold, 
2) 3 supporting bullet points with specific numbers."
```

### 🎯 4. Decision & Strategy
```markdown
# 3-Option Spectrum
"Give me exactly 3 options: Option A (Quick fix/Low risk), 
Option B (Balanced best practice), Option C (Bold strategic fix)."

# Pre-Mortem Red Team
"Fast-forward 12 months: this initiative failed completely. 
List the top 3 fatal assumptions that caused the collapse."
```

---

## 3 Rules for Keeping Your Cheat Sheet Useful
1. **Cap it at 1 page**: If your cheat sheet exceeds 8-10 prompts, you will stop using it. Keep only the highest-frequency gems.
2. **Use bracketed placeholders**: Ensure every snippet has `{clipboard}` or `[INSERT_TEXT]` ready for instant pasting.
3. **Prune quarterly**: Delete prompts you haven't used in 90 days.
