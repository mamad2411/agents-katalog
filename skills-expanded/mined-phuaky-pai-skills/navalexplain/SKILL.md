---
name: NavalExplain
description: Visual learning through multi-model explanation, ASCII diagrams, and interactive drill-down. USE WHEN naval-explain, naval explain, explain visually, visual learning, help me understand, break this down visually, diagram this concept, I don't get this, explain like Naval.
---

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/PAI/USER/SKILLCUSTOMIZATIONS/NavalExplain/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.


## 🚨 MANDATORY: Voice Notification (REQUIRED BEFORE ANY ACTION)

**You MUST send this notification BEFORE doing anything else when this skill is invoked.**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the NavalExplain skill to break down a concept visually"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **NavalExplain** skill to break down a concept visually...
   ```

**This is not optional. Execute this curl command immediately upon skill invocation.**


# NavalExplain

Interactive visual learning inspired by Naval Ravikant's approach: query multiple AI models in parallel, identify the clearest explanation, then drill down with diagrams, analogies, and visuals until the "aha moment."

## Core Principles

1. **Simplest level first** — No jargon. Foundational understanding before complexity.
2. **User drives the depth** — Always ask what doesn't click. Never dump information.
3. **Visuals are the medium** — Mermaid diagrams, ASCII art, analogies. Text walls are failure.
4. **Multi-model diversity** — Different models see different angles. Use that.

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Explain** | User pastes text, asks to understand something, or invokes /naval-explain | `Workflows/Explain.md` |
| **DrillDown** | User says what doesn't click, asks for more visuals, wants deeper on a concept | `Workflows/DrillDown.md` |
| **Save** | User explicitly asks to save, /save, "save this session" | `Workflows/Save.md` |

## Mode Detection

| User Input | Route |
|------------|-------|
| Pastes a paragraph + "/naval-explain" | → Explain workflow (full multi-model) |
| Pastes text + "help me understand" | → Explain workflow |
| "I don't get the X part" / "what about Y" | → DrillDown workflow |
| "diagram this" / "show me visually" | → DrillDown workflow |
| "draw me an image of this" / "illustrate" | → DrillDown workflow (with Art skill flag) |
| "save this" / "/save" | → Save workflow |

## Visual Output Defaults

**CRITICAL: NEVER output raw ` ```mermaid ` code blocks.** They render as unreadable text in the terminal.

| Type | When | Format |
|------|------|--------|
| **ASCII diagrams** | Relationships, flows, processes, hierarchies, comparisons | Monospace box-drawing (primary visual format) |
| **Analogies** | Abstract concepts that need grounding | Plain text with concrete comparisons |
| **Rendered PNG** | ONLY when user asks for "render diagram" or "show as image" | Mermaid → PNG via `RenderMermaid.sh` → display with Read tool |
| **AI Images** | ONLY when user explicitly asks for illustration/image | Art skill invocation |

**ASCII is the default.** It renders perfectly in any terminal with zero dependencies. Use box-drawing characters (─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼), arrows (→ ← ↑ ↓ ──▶ ◀──), and tables for all visual explanations.

## Examples

**Example 1: Understanding a dense paragraph**
```
User: [pastes paragraph about quantum entanglement] /naval-explain
→ Invokes Explain workflow
→ Spawns ClaudeResearcher + GeminiResearcher in parallel
→ Synthesizes: "Here are the 3 key concepts in this paragraph..."
→ Asks: "Which of these doesn't click for you?"
→ User: "I get superposition but not how measurement affects the other particle"
→ Invokes DrillDown workflow
→ Generates Mermaid diagram showing measurement → collapse → correlation
→ Asks: "Does this connection make sense now, or should I try a different angle?"
```

**Example 2: Quick concept breakdown**
```
User: "naval-explain option Greeks in finance"
→ Invokes Explain workflow
→ Multi-model query on option Greeks
→ Returns: "4 key concepts: Delta, Gamma, Theta, Vega..."
→ ASCII art showing how each Greek relates to price movement
→ "Which one feels fuzzy?"
```

**Example 3: Save a session**
```
User: "save this"
→ Invokes Save workflow
→ Saves diagrams + explanations to ~/.claude/MEMORY/LEARNING/{date}_{topic}/
→ Confirms what was saved
```

## Integration

### Uses
- **Research** — ClaudeResearcher + GeminiResearcher for multi-model parallel queries
- **Art** — AI image generation (ONLY on explicit request)

### Feeds Into
- **MEMORY/LEARNING/** — Saved sessions become persistent knowledge
