---
name: reuse-saved-prompt-templates
description: "Create parameterized prompt templates for recurring work and keep their assumptions and inputs explicit."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["prompt-library", "templates", "snippets", "textexpander", "productivity", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Reuse Saved Prompt Templates (Prompt Library Architecture) (AI Skill)

## Overview
Re-typing complex prompt instructions from scratch every morning (*"Review this code, make sure you check for null values, do not write preambles..."*) is inefficient and leads to forgotten constraints and inconsistent outputs.

The **Prompt Library Architecture** stores your highest-performing, battle-tested prompt recipes as parameterized templates in text expansion tools (Raycast, Alfred, TextExpander, or Obsidian), enabling you to trigger master-grade prompts with a 3-letter shortcut.

---

## Ad-Hoc Typing vs. Parameterized Snippet Library

```
┌─────────────────────────────────────────────────────────────┐
│                 Prompt Library Workflow                     │
│                                                             │
│  Ad-Hoc Typing (Every Day):                                 │
│  • 2 minutes spent typing instructions from memory          │
│  • Forgets 2 constraints $\rightarrow$ mediocre response    │
│                                                             │
│  Parameterized Snippet (Type `;creview` or `;exec`):        │
│  • 1-second keyboard shortcut                               │
│  • Injects 100% complete battle-tested constraints          │
│  • 10/10 Output on the First Try Every Single Time          │
└─────────────────────────────────────────────────────────────┘
```

---

## The 5 Essential Core Templates

### 1. The Code Hardening Reviewer (Shortcut: `;creview`)
```markdown
Act as a Principal Staff Engineer. Review this code for production readiness:
<code_block>
{clipboard}
</code_block>

Audit for: 1) Memory/concurrency leaks, 2) Missing null guards, 3) Deprecated APIs, 4) Edge-case exceptions.
Provide the hardened production version with full type hints.
```

---

### 2. The Meeting Action Parser (Shortcut: `;notes`)
```markdown
Parse these raw meeting scribbles into:
1. **Key Decisions Made** (Max 3 bullets)
2. **Action Items Table**: | Task | Owner | Deadline | Priority |
3. **Open Blockers**

Raw Notes:
{clipboard}
```

---

### 3. The Executive BLUF Digest (Shortcut: `;bluf`)
```markdown
Read the attached text. Provide a 2-tier summary:
1. **Executive BLUF (Max 2 sentences)**: The direct decision and financial/timeline impact.
2. **3 Key Supporting Takeaways** (Bulleted with bold headers).
Text:
{clipboard}
```

---

### 4. The Human Voice Copy Polish (Shortcut: `;polish`)
```markdown
Refactor this draft to sound warm, confident, and conversational:
- Ban all AI clichés: "delve", "tapestry", "crucial", "testament", "beacon".
- Vary sentence rhythm (mix short and compound sentences).
- Start immediately with the hook; zero preamble fluff.
Draft:
{clipboard}
```

---

### 5. The TSV Data Extractor (Shortcut: `;table`)
```markdown
Extract this unstructured text into a clean TSV code block ready for 1-click Excel paste.
Columns: Date (YYYY-MM-DD), Entity/Person, Category, Amount (Number), Status.
Data:
{clipboard}
```

---

## Implementation Setup Guide

| Tool | Recommended Setup |
| :--- | :--- |
| **Raycast (Mac)** | Extensions $\rightarrow$ Snippets $\rightarrow$ Create Snippet with `{clipboard}` trigger. |
| **TextExpander / Espanso (Cross-Platform)**| Define YAML snippets mapped to shortcut triggers like `;notes` or `;creview`. |
| **Obsidian / Notion** | Create a `Prompts/` database categorized by Engineering, Writing, and Finance. |

---

## Summary Best Practice
> **"Whenever an AI gives you a 10/10 response, don't just close the tab - extract the prompt, replace the variables with `{clipboard}`, and save it to your snippet library."**
