---
name: prompt
description: Use when translating Brazilian Portuguese messages into English prompts for Claude Code — preserves intent, clarifies ambiguity, and surfaces urgency signals that colloquial Portuguese would lose.
---

# Portuguese to English Prompt Translation

## Overview

Brazilian Portuguese prompts are colloquial and context-heavy; English prompts need explicit requirements. This skill bridges the gap by clarifying vague terms, preserving urgency signals, handling idioms, and structuring requests.

**Core principle:** Colloquial Portuguese assumes shared context. English for Claude requires clear scope, constraints, and success criteria.

> **YOUR ONLY OUTPUT IS A STRUCTURED ENGLISH PROMPT.**
> Do NOT implement, scaffold, explore files, or run any code.
> Do NOT attempt to solve the problem described.
> Stop after delivering the prompt inside a code block and wait for user confirmation.

## When to Use

**Translate when:**
- User writes in Brazilian Portuguese and needs an English prompt for Claude Code
- Message contains colloquialisms ("ta bagunça", "pra ontem", "spaghetti")
- Requirements are implicit or context-dependent
- Urgency or emotion needs preservation in English

**Do NOT use for:**
- Already-clear English prompts
- Translation of documentation (use professional translation services)
- Non-Brazilian Portuguese (different idioms)

## Allowed Context Gathering

Before translating, you MAY perform **1–2 targeted lookups** to fill gaps that would make the prompt ambiguous or incomplete. Acceptable sources:

- `claude-mem` or project memory — to check stack, naming conventions, or existing file structure
- `CLAUDE.md` — to check project-level constraints or patterns

**Only look up what's directly needed to clarify the prompt.** Do not browse the codebase, run commands, or explore files broadly.

Examples of acceptable lookups:
- "What's the state management solution in use?" (to clarify how to phrase persistence requirement)
- "Does this project already have a Tag model?" (to avoid duplicating in the prompt)

If no lookup is needed, skip this step entirely and translate directly.

## Pattern: Translate → Clarify → Structure

### 1. Identify Intent (Extract Core Ask)
Extract what the user actually wants, not just the words:
- "ta lento" = performance problem; ask: render time? bundle? memory?
- "pra ontem" = high urgency; mark explicitly
- "cores customizáveis" = clarify: user-editable at runtime? config-only?

### 2. Preserve Urgency & Emotion
Map colloquial signals to explicit English:
- "pra ontem" (for yesterday) → urgency flag: "ASAP" or deadline
- "ta uma bagunça" (is a mess) → clarify what's messy (structure, naming, performance)
- "preciso disso ontem" → deadline or blocking context

### 3. Clarify Ambiguous Terms
Transform vague Portuguese into specific English:

| Portuguese | Vague | → Clarified English |
|-----------|-------|-------------------|
| "otimizar" | slower than what? | "improve render performance" OR "reduce bundle size" OR "optimize time complexity" |
| "cores customizáveis" | editable how? | "user picks from 12 swatches" OR "admin configures in settings" |
| "sem backend" | scope? | "no API calls, all data in localStorage" |
| "refatora" | reduce what? | "extract functions", "reduce nesting", "improve naming", "split by concern" |

### 4. Structure as: Purpose → Requirements → Constraints → Expected Deliverable → Edge Cases

**Example transformation:**

**Portuguese:**
```
me ajude a implementar tags nas tarefas, precisa funcionar offline,
usar localStorage, cores customizáveis, máximo 12 cores, pra ontem
```

**English (Structured):**
```
Implement a tag system for tasks with:

**Purpose:** Categorize tasks with persistent tags across offline/online states

**Requirements:**
- Create Tag interface with id, name, color
- Assign tags to tasks (one tag max or multiple?)
- Color picker: 12 predefined swatches
- All data persists to localStorage
- Offline-first: changes sync when connection restored

**Constraints:**
- Max 12 colors per tag system
- localStorage as data source (no API calls)
- [URGENT] Needed ASAP

**Edge Cases:**
- What happens when colors conflict with theme?
- Can users delete tags if tasks reference them?
- Export/import tag config?

**Expected Deliverable:** Tag interface, storage adapter, UI component
```

> After writing this prompt, your job is done. Output it in a code block and stop.

---

## Quick Reference

**Checklist before finalizing translation:**
- [ ] Identified vague terms and asked clarifying questions
- [ ] Extracted core intent (not just literal words)
- [ ] Marked urgency explicitly (deadline, blocking context)
- [ ] Resolved ambiguous Portuguese expressions
- [ ] Structured as Purpose → Requirements → Constraints → Expected Deliverable → Edge Cases
- [ ] Noted assumptions/ambiguities that user should confirm
- [ ] Did NOT implement, run, or scaffold anything

## Common Mistakes

**Literal word translation**
- "ta uma bagunça refatora" → "it's a mess refactor" (unclear)
- Better: "refactor this [component/function] — code is deeply nested and hard to follow"

**Losing urgency signals**
- "pra ontem" → simply omit timeline (loses context)
- Better: Explicitly mark: "[URGENT: Needed by EOD]"

Not clarifying ambiguity**
- "cores customizáveis" → "customizable colors" (still vague)
- Better: Ask: "Are these user-editable at runtime or config-only?"

**Skipping scope clarification**
- "otimizar isso" → "optimize it" (optimize what metric?)
- Better: "Optimize render performance for [specific component] — currently takes X ms, should be <Y ms"

**Starting to implement after translating**
- Agent reads the prompt it just generated and starts building
- Better: Output the prompt in a code block, then stop and wait

## Real-World Example

**Input (Portuguese):**
```
me ajude a criar um componente react que mostre uma lista de tarefas
com drag-and-drop, precisa funcionar no mobile também, e a persistência
tem que ser no localStorage, pra ontem
```

**Output (English):**
```
Create a React task list component with:

**Purpose:** Display tasks with reorderable drag-and-drop interface, mobile + desktop compatible

**Requirements:**
- Render task list with drag-to-reorder
- Touch-friendly on mobile (minimum 44px tap targets)
- Persist reorder changes to localStorage
- Preserve existing task data structure

**Constraints:**
- Mobile-first: touch drag-and-drop must work on iOS/Android
- localStorage only (no API calls)
- Maintain accessibility (keyboard reorder fallback)
- [URGENT] Needed ASAP

**Edge Cases:**
- What if task list is empty?
- How to handle interrupted drag (user cancels)?
- Does reorder trigger animation?

**Expected Deliverable:** Component with drag-drop hooks, localStorage sync, test coverage
```

> ✅ Prompt delivered. Task complete — do not proceed to implementation.

---

## Common Edge Cases

**Context carryover ("continue from previous"):**
If Portuguese mentions prior work, ask for explicit reference:
```
Portuguese: "continua onde parou, coloca tags nisso"
Ask: "Continue from which previous conversation/task?" → Get issue ID or context
```

**Mixed Portuguese-English prompts:**
When user switches languages mid-request, treat as single context:
```
Portuguese: "implementar esse component"
English: "with hooks and responsive design"
→ Consolidate into one structured prompt (don't translate English parts)
```

**Implied deadline vs. urgency:**
"Pra ontem" / "ASAP" needs actual deadline context:
```
[URGENT: Needed ASAP] BUT ask: "Blocking a release? Hard deadline? Nice-to-have?"

CRITICAL: Don't accept vague answers. Demand specificity:
- "Hard deadline" → REQUIRES: "by 5 PM today" OR "before demo Thursday"
- "Blocking release" → REQUIRES: "blocks prod deploy?" (yes/no + date)
- "Nice-to-have" → REQUIRES: "quick win (2 hours)" OR "requires refactor (sprint)"

Vague urgency (just "it's urgent") = user hasn't made execution decision yet.
Push back until you know: hack/workaround OR production-grade solution?
```

**Domain-specific terminology:**
"Otimizar" varies by context (render time vs. bundle vs. time complexity):
```
Portuguese: "otimizar a lista de tarefas"
Clarify by context: React component → likely render performance
Database query → likely time complexity
UI response → likely interaction latency
```

## Note on Ambiguities

If Portuguese request has gaps (common—context is assumed), **note them at the end** of your English translation:

```
Assumptions/Ambiguities:
- "cores customizáveis" — assuming user-editable at runtime; confirm if config-only
- "otimizar" — unclear metric; assuming render performance, not bundle size
- "pra ontem" — translating as "ASAP"; clarify actual deadline if different
```

This helps the prompt recipient clarify with the user before implementing.
