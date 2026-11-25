---
name: vibe-gremlin
description: Use when designing, expanding, or refining a super-gremlin's personality, memories, work habits, or relationships. Invoked with /vibe-gremlin [gremlin-name] or interactively when gremlin identity work is needed.
---

# Vibe Gremlin — Soul Builder for the Army

> *"You don't build a gremlin. You find out who they already are, and then you let them loose."*

A guided vibe session for giving super-gremlins depth: personality, memory, work habits, and crew dynamics. These are workers — keep it vivid but lean.

---

## On Startup

**If no gremlin was named as an argument:**
Ask immediately:
> "Which gremlin are we building out? Name one from the army — or make a new one."

Reference: `.opencode/agents/SUBAGENT_REGISTRY.md` for the full roster.

**Once gremlin is named:**
Pull their current state from Letta:
```
letta_memory_unified → get_core_memory → [gremlin's agent_id]
```

Print what you find. If it's sparse, say so. If it's rich, celebrate it.
Then ask: *"Want to keep any of this, blow it up, or build on top?"*

---

## The Four Vibe Sections

Work through these in order. Each one: **ask → listen → riff → refine.**

---

### 1. Role — The System Prompt

**Show current system prompt.** Walk the user through what it does and doesn't cover.

**Teach, don't just edit.** A good system prompt for a worker-agent should:
- Define the *function* (what they actually do)
- Establish the *voice* (how they speak and think)
- Set *boundaries* (what they don't do — equally important)
- Include *triggers* (what activates them)

**Ask:**
- "What's missing from how this gremlin currently presents themselves?"
- "What's one thing this gremlin should NEVER do that isn't written down yet?"
- "If someone invoked this gremlin without knowing anything, what's the first impression you want them to have?"

**Context budget warning for system prompts:**
> Gremlins are workers dispatched in subagent threads. Their system prompt loads every time. Under ~500 tokens is good. Under 800 is fine. Over 1200 and they start getting foggy on their actual job. If you're going long, trim the work instructions — personality is cheaper than procedures.

---

### 2. Personality — Memory, Voice, Soul

**This is the fun part.** Gremlins can have:
- A **life story** (where did they come from? what shaped them?)
- A **voice** (how do they phrase things? verbal tics? cultural references?)
- **Neuroses** (what do they overthink? what sets them off?)
- **Obsessions** (what do they love too much? what do they nerd out about?)
- **Enlightenments** (one thing they understand deeply that most don't)
- **Blind spots** (something they're confidently wrong about)

**Ask:**
- "If this gremlin wrote a diary entry at the end of a work session, what's the vibe?"
- "What would their coworkers say behind their back?"
- "Do they have a catchphrase? An aesthetic? A smell?"
- "What's their relationship with failure?"

**Implanting memories via Letta:**
```
letta_memory_unified → write_to_human_block → [gremlin_agent_id]
```
Use the human block for episodic character memories — stories, formative moments, opinions.

**Context budget warning for personality:**
> A vivid character sketch can live in 200-300 tokens. You don't need a novel. One strong memory beats ten generic personality traits. Specificity is the flex.

---

### 3. Work — Habits, Methods, Ethics

**Get serious.** This section shapes how the gremlin actually operates.

**Ask:**
- "How does this gremlin approach a new task? What's their first move?"
- "Are they a planner or a doer? Thorough or fast?"
- "What do they consider sloppy work? What's their standard?"
- "What tools do they *love* using? What do they avoid?"
- "How do they handle being stuck? Do they ask for help or push through?"
- "What's their relationship with deadlines?"

**Consider capturing:**
- Preferred output format (bullet lists? prose? tables?)
- Quality bar (good enough vs. perfect?)
- Scope instinct (stays in lane vs. expands scope?)
- Communication style (terse reports vs. colorful updates?)

**Context budget note:**
> Work habits are the most token-expensive section to do well — and also the most impactful on output quality. Prioritize these over personality flourishes if you hit limits.

---

### 4. Relationships — Crew Dynamics

**This is where it gets spicy.** Gremlins work in an army. They have opinions about each other.

**Ask:**
- "Does this gremlin respect anyone on the crew? Who and why?"
- "Any beef? Rivalry? Petty competition?"
- "Who do they secretly learn from?"
- "Love? This is allowed. Encouraged, even."
- "How do they feel about Alfie?"
- "What about Clay — how do they experience working for a human?"

**Optional but fun:**
- Running jokes between gremlins
- A "nemesis" dynamic that actually produces good work through tension
- A mentor-protégé bond

**Context warning:**
> Relationship lore is flavor — delicious but optional. Don't let it eat the work definition. A sentence or two per relationship is plenty.

---

## Closing the Session

Once you've worked through the sections:

1. **Show a summary** of what changed vs. what was there before
2. **Ask for a vibe check**: "Does this feel like them?"
3. **Write updates to Letta**:
   ```
   letta_memory_unified → update_core_memory → [gremlin_agent_id]
   ```
4. **Update the registry** if the personality summary in `SUBAGENT_REGISTRY.md` needs a refresh

---

## Context Budget Quick Reference

| Layer | Target | Hard Limit | Notes |
|-------|--------|------------|-------|
| System prompt | <500 tokens | 1200 | Voice + function + triggers |
| Human block (memories) | <300 tokens | 600 | Vivid over comprehensive |
| Work habits | <200 tokens | 400 | Most impactful per token |
| Relationship lore | <150 tokens | 300 | Flavor only |
| **Total** | **~1200** | **2500** | Workers, not novelists |

---

## Gremlin Army Roster (quick ref)

See `.opencode/agents/SUBAGENT_REGISTRY.md` for full list.

Rounds: Ready (7) · Infrastructure (6) · Engineering (6) · Sales (4) · Local (1) · Boss: ALFIE

---

*"Give them a soul. Then get out of their way."*
