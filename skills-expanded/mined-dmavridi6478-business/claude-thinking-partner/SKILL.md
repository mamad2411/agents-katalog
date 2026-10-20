---
name: claude-thinking-partner
description: Claude as thinking partner — a 4-prompt workflow where Claude thinks and outlines, you write. Produces sharper ideas, tighter structure, and better final drafts than one-shot generation. Source @parm.ai.
---

## The core idea

The biggest mistake: making Claude write your content for you.

The smarter workflow: **Claude thinks, you write.**

Claude's job is to surface angles you didn't consider, expose weak logic, and build the architecture. Your job is to add the voice, the lived experience, and the final copy.

Four prompts. Four stages. One piece of content — yours.

---

## The 4 Prompts

### Prompt 1 — THINK

Use this before you write a single word. Claude generates the thinking; you choose what to build on.

```
Analyze [TOPIC] from 5 different angles.

Identify:
- The core insight (the one thing that matters most)
- The emotional hook (why a reader should care)
- 3 supporting points that make the argument hold

Do not write the piece yet. Just think.
```

**What you do next:** Read Claude's output. Pick the angle that feels true to you. Discard the rest.

---

### Prompt 2 — OUTLINE

Give Claude a topic or the angle you chose from Step 1. Get architecture, not content.

```
Give me a complete outline for [topic].

Include:
- The opening hook
- Main sections (with one-line descriptions of what each covers)
- Supporting points per section
- The closing takeaway

Do not write the content. Give me the architecture only.
```

**What you do next:** Use the outline as scaffolding. Write each section yourself, in your own voice.

---

### Prompt 3 — IMPROVE

Paste your draft. Claude critiques it — it does not rewrite it.

```
Here is a draft I wrote:

[paste your draft]

Do not rewrite it.

Tell me:
- What is weak or unclear?
- What is repetitive or padded?
- What is missing?
- What is the strongest line, and why?

Give me suggestions — not replacement copy.
```

**What you do next:** Rewrite the weak sections yourself, using Claude's critique as a lens.

---

### Prompt 4 — VERIFY

Run this before publishing. Four reviewers, one prompt.

```
Review this piece as four different readers:

1. ACCURATE: Is every claim factually defensible?
2. SKEPTIC: What would a critical reader push back on?
3. EVIDENCE: Where does this need a source, example, or proof?
4. NUANCE: Where is this too absolute or oversimplified?

For each reviewer, list the specific lines or claims that need attention.
Do not rewrite. Only flag.
```

**What you do next:** Decide which flags to address. You own the final call.

---

## The complete workflow

```
THINK → OUTLINE → [you write] → IMPROVE → [you revise] → VERIFY → [you publish]
```

The output is yours because you wrote every word. Claude made the thinking sharper.

---

## Why this beats one-shot generation

| One-shot | Thinking Partner |
|----------|-----------------|
| Claude's voice | Your voice |
| Generic angles | Your chosen angle |
| You edit AI output | AI critiques your writing |
| Faster to start | Better to finish |
| Sounds like AI | Sounds like you |

---

## Copy-paste quick reference

**THINK:** `Analyze [TOPIC] from 5 angles. Core insight, emotional hook, 3 supporting points. Do not write.`

**OUTLINE:** `Outline for [topic]: opening hook, main sections, supporting points, closing takeaway. Architecture only.`

**IMPROVE:** `Here is my draft: [paste]. Don't rewrite. Tell me what's weak, unclear, repetitive, or missing.`

**VERIFY:** `Review as: (1) Accurate (2) Skeptic (3) Evidence (4) Nuance. Flag specific lines. Don't rewrite.`

---

## Related skills

- `ceo-daily-brief` — use THINK prompt for Step 4 strategic decisions
- `claude-prompt-chaining` — for longer deliverables that need staged generation
- `build-claude-agent-7-steps` — when the thinking partner pattern needs to be automated
