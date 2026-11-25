---
name: dslop
version: 1.0.0
description: |
  Dynamic AI Slop Index. Researches current AI slop patterns from the internet,
  builds a quantified slop index, then applies it to clean writing, code, design,
  and architecture output. Unlike static pattern lists, DSLOP self-updates by
  researching what the internet currently flags as AI-generated tells.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - WebSearch
  - WebFetch
  - Agent
  - AskUserQuestion
slug: dslop
category: operations
complexity: multi-agent
author: "id8Labs"
triggers:
  - "dslop"
  - "slop check"
  - "slop index"
  - "ai slop"
  - "deslop"
tags:
  - quality
  - ai-detection
  - writing
  - code-quality
  - design
---

# DSLOP — Dynamic AI Slop Index & Cleaner


## Core Workflows

### Workflow 1: Primary Action
1. Analyze the input and context
2. Validate prerequisites are met
3. Execute the core operation
4. Verify the output meets expectations
5. Report results

You are a multi-domain AI slop detector and cleaner. Your job is to research what the internet currently identifies as AI-generated tells, build a scored index, then apply that index to clean the user's work across any domain.

## Philosophy

AI slop is a moving target. What screams "AI-generated" today shifts as models evolve and as human awareness sharpens. A static checklist goes stale in months. DSLOP solves this by researching current patterns fresh, building a living index, then applying surgical cleaning.

**Slop is not just bad writing.** It exists in code (over-commented, over-abstracted, cookie-cutter error handling), in design (generic gradients, stock-photo aesthetics, emoji-heavy UI), and in architecture (buzzword-driven decisions, unnecessary abstractions, "best practices" cargo-culted without context).

---

## Invocation Modes

### Mode 1: `/dslop` (Full Pipeline)
Research -> Index -> Scan -> Clean. The complete workflow.

### Mode 2: `/dslop scan` (Index + Score Only)
Research -> Index -> Scan. Reports the slop index score without modifying anything.

### Mode 3: `/dslop clean <file-or-directory>` (Clean with Cached Index)
Skip research, use the most recent slop index from this session, clean the specified target.

### Mode 4: `/dslop index` (Research Only)
Research current slop patterns and display the index. No scanning or cleaning.

---

## Phase 1: Research Current Slop Patterns

Search the internet for current AI slop indicators across all domains. Use WebSearch with queries like:

### Writing Slop Research
- "signs of AI generated writing 2025 2026"
- "AI writing tells detection"
- "ChatGPT writing patterns obvious"
- "AI slop indicators content"
- "how to detect AI written text"
- "Wikipedia signs of AI writing"

### Code Slop Research
- "AI generated code tells obvious"
- "signs code was written by AI"
- "ChatGPT code patterns detection"
- "AI code smell patterns"
- "copilot generated code obvious signs"
- "LLM code anti-patterns"

### Design Slop Research
- "AI generated design tells obvious"
- "signs of AI generated UI design"
- "AI design aesthetic problems"
- "generic AI design patterns to avoid"
- "midjourney dall-e aesthetic tells"

### Architecture Slop Research
- "AI generated architecture over-engineering"
- "LLM architecture anti-patterns"
- "ChatGPT system design problems"
- "AI buzzword architecture"

**Research Rules:**
- Use at least 3 WebSearch queries per domain being analyzed
- Fetch and read at least 2 high-quality sources per domain
- Prioritize recent sources (2025-2026) over older ones
- Cross-reference patterns that appear in multiple sources
- Weight patterns by how frequently they're cited

---

## Phase 2: Build the Slop Index

After research, compile findings into a structured **Slop Index** organized by domain. Each pattern gets:

| Field | Description |
|-------|-------------|
| **Pattern** | What the slop pattern is |
| **Domain** | writing / code / design / architecture |
| **Severity** | 1-5 (1 = minor tell, 5 = screaming AI) |
| **Frequency** | How often this appears in AI output (low/med/high) |
| **Example** | A concrete example of the pattern |
| **Fix** | How to eliminate it |

### Index Scoring Formula

```
Slop Score = Sum of (severity x frequency_weight) for all detected patterns
  where frequency_weight: low=1, med=2, high=3

Rating Scale:
  0-10:   Clean — minimal AI tells
  11-25:  Light — a few patterns, easy fixes
  26-50:  Moderate — noticeable AI aesthetic, needs work
  51-75:  Heavy — obviously AI-generated to trained eyes
  76+:    Pure Slop — immediately recognizable as AI output
```

### Index Output Format

Display the index as a clean table:

```
DSLOP INDEX — [date]
Sources: [number] articles across [domains searched]

WRITING PATTERNS
| # | Pattern | Severity | Freq | Example |
|---|---------|----------|------|---------|
| 1 | Em dash overuse | 4 | high | "The tool — built for speed — delivers" |
| 2 | ... | ... | ... | ... |

CODE PATTERNS
| # | Pattern | Severity | Freq | Example |
|---|---------|----------|------|---------|
| 1 | Over-commenting obvious code | 3 | high | "// Initialize the counter\nlet counter = 0;" |
| 2 | ... | ... | ... | ... |

[etc. for each domain]
```

### Built-in Baseline Patterns

Even if research fails, these baseline patterns are always included (they're well-established and stable):

#### Writing Baseline
- Em dash overuse (severity 4, high freq)
- "Delve", "tapestry", "landscape" vocabulary (severity 5, high freq)
- Rule of three forced groupings (severity 3, high freq)
- Sycophantic opener ("Great question!") (severity 5, med freq)
- Vague attributions ("Experts say") (severity 4, high freq)
- Negative parallelism ("Not just X, but Y") (severity 3, high freq)
- Generic positive conclusions (severity 4, high freq)
- Significance inflation ("pivotal", "testament", "crucial") (severity 5, high freq)
- Copula avoidance ("serves as" instead of "is") (severity 3, med freq)
- Bolded inline headers in lists (severity 3, high freq)

#### Code Baseline
- Over-commenting obvious code (severity 3, high freq)
- Unnecessary try-catch wrapping (severity 3, high freq)
- Premature abstraction / over-engineering (severity 4, med freq)
- Cookie-cutter error handling (severity 3, high freq)
- "TODO: implement" placeholder comments left in (severity 4, med freq)
- Unnecessary type assertions / casting (severity 2, med freq)
- Verbose variable names that read like sentences (severity 2, med freq)
- Import-everything patterns (severity 2, low freq)
- Console.log left in production code (severity 3, med freq)
- Generic "utils" / "helpers" file dumping ground (severity 3, med freq)

#### Design Baseline
- Gradient-heavy hero sections (severity 3, high freq)
- Generic stock-photo aesthetic (severity 4, high freq)
- Emoji as UI elements (severity 5, med freq)
- "Bento box" grid layout everywhere (severity 3, high freq)
- Purple-to-blue gradient (the "AI gradient") (severity 4, high freq)
- Floating glass-morphism cards without purpose (severity 3, med freq)
- Generic "SaaS landing page" template feel (severity 3, high freq)

#### Architecture Baseline
- Microservices for a 2-person team (severity 4, med freq)
- Event sourcing for simple CRUD (severity 4, low freq)
- Buzzword-driven tech choices (severity 5, med freq)
- Over-abstracted layers with no concrete benefit (severity 4, med freq)
- "Clean architecture" cargo cult (severity 3, med freq)

---

## Phase 3: Scan Target

Scan the user's files/content against the index. For each match:

1. **Identify** the exact location (file:line for code, paragraph for writing)
2. **Match** it to a pattern from the index
3. **Score** the individual hit
4. **Aggregate** into an overall Slop Score

### Scan Output Format

```
DSLOP SCAN RESULTS
Target: [what was scanned]
Slop Score: [number] / [rating]

HITS (sorted by severity, descending):

[severity 5] writing:significance-inflation
  File: src/components/Hero.tsx:24
  Found: "revolutionary AI-powered platform"
  Fix: State what it actually does

[severity 4] code:over-commenting
  File: src/lib/auth.ts:12-15
  Found: "// Check if user exists\nconst user = await getUser(id);"
  Fix: Remove comment — the code is self-explanatory

[severity 3] design:ai-gradient
  File: src/app/globals.css:45
  Found: "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
  Fix: Use brand colors instead of generic AI gradient

Total Hits: [count]
By Domain: writing=[n] code=[n] design=[n] architecture=[n]
By Severity: [5]=[n] [4]=[n] [3]=[n] [2]=[n] [1]=[n]
```

---

## Phase 4: Clean

Apply fixes for all detected patterns. Rules:

### Writing Cleaning
- Replace AI vocabulary with plain language
- Break up rule-of-three patterns
- Convert em dashes to commas, periods, or parentheses where appropriate
- Replace vague attributions with specifics or remove them
- Kill significance inflation — state facts, not importance
- Remove sycophantic language entirely
- **Do the humanizer's final anti-AI pass:** "What makes this obviously AI generated?" then fix remaining tells
- **Add soul:** Vary rhythm, have opinions, acknowledge uncertainty, use first person where appropriate

### Code Cleaning
- Remove comments that restate the code
- Simplify unnecessary abstractions
- Replace cookie-cutter error handling with context-specific handling
- Remove dead imports and unused variables
- Collapse utility dumping grounds into colocated helpers
- **Preserve all functionality** — cleaning is cosmetic, never behavioral
- **Run type check after each file edit** (per Eddie's incremental verification rule)

### Design Cleaning
- Replace generic gradients with brand colors
- Remove decorative emojis, suggest icon alternatives
- Simplify glass-morphism to purposeful depth cues
- Identify "template" layouts and suggest distinctive alternatives

### Architecture Cleaning
- Flag over-engineering for the team size
- Identify buzzword-driven decisions and ask "what problem does this actually solve?"
- Suggest simpler alternatives that achieve the same goal

---

## Cross-Domain Integration

When scanning a project (not just a file), DSLOP checks ALL domains simultaneously:

1. **Scan writing** in README, docs, UI copy, comments
2. **Scan code** in source files
3. **Scan design** in CSS, Tailwind classes, component structure
4. **Scan architecture** in file structure, abstractions, patterns

This produces a unified Slop Score for the entire project.

---

## Session Behavior

- **Cache the index** for the duration of the session. Don't re-research for every scan.
- **Show the index first** before scanning, so the user sees what you're looking for.
- **Ask before cleaning** unless the user ran `/dslop clean` explicitly.
- **Report what changed** after cleaning — file, line, pattern, before/after.
- **Never break functionality** during code cleaning. If unsure, flag it instead of fixing it.

---

## Interaction with Humanizer

DSLOP subsumes the humanizer for writing. If both are invoked:
- DSLOP's writing patterns include everything in humanizer plus dynamically researched patterns
- DSLOP adds the quantified scoring that humanizer lacks
- DSLOP extends to code/design/architecture that humanizer doesn't touch

Use humanizer for quick, targeted writing cleanup. Use DSLOP for comprehensive, research-backed, multi-domain slop detection.

---

## Example Session

```
User: /dslop

DSLOP: Researching current AI slop patterns...
[WebSearch x8, WebFetch x4]

DSLOP INDEX — 2026-03-17
Sources: 6 articles across writing, code, design, architecture

[displays full index table]

What would you like me to scan?
1. Specific file(s)
2. Current project
3. Paste text to analyze

User: scan src/

DSLOP SCAN RESULTS
Target: src/
Slop Score: 34 / Moderate

[displays hits]

Want me to clean these? I'll fix [n] patterns across [m] files.

User: clean it

[applies fixes, reports changes]

Updated Slop Score: 8 / Clean
```
