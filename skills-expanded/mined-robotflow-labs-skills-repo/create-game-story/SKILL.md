---
name: create-game-story
description: Interactive game story creator. Use when the user wants to brainstorm, design, or write a game narrative — including world-building, characters, plot arcs, quests, dialogue, and lore. Guides the user step-by-step through story creation with choices at each stage.
---

# Create Game Story

Interactive, step-by-step game story creation. Guide the user through the entire narrative design process using questions and choices at each stage. Never dump the entire story at once — build it collaboratively.

## Process

### Phase 1: Genre & Tone

Ask the user to pick (or describe) the game's genre and tone. Present these as choices:

**Genre:**
- Fantasy (swords, magic, mythical creatures)
- Sci-Fi (space, cyberpunk, post-singularity)
- Horror (survival horror, psychological, cosmic)
- Post-Apocalyptic (wasteland, zombie, nuclear)
- Historical / Realistic (war, mystery, thriller)
- Hybrid (let them combine)

**Tone:**
- Dark & Serious
- Lighthearted & Comedic
- Epic & Heroic
- Mysterious & Atmospheric
- Player-driven (morally gray choices)

**Target audience:** Casual, Core Gamer, Narrative-focused

### Phase 2: World-Building

Based on genre selection, ask focused questions:

1. **Setting** — Where does the game take place? Offer 3 setting options tailored to their genre, plus "describe your own"
2. **Time period** — When? Past, present, future, timeless
3. **Scale** — Single location, city, continent, planet, multiverse
4. **Rules** — What makes this world unique? Magic system, technology level, societal structure
5. **Conflict** — What is the central tension in this world? War, plague, invasion, collapse, mystery

After each answer, reflect back a 2-3 sentence world summary and ask if they want to refine it.

### Phase 3: Characters

Build the cast one character at a time:

1. **Protagonist** — Ask:
   - Name and appearance (brief)
   - Background / origin (offer 3 archetype options + custom)
   - Core motivation (revenge, survival, discovery, redemption, duty)
   - Fatal flaw or internal conflict
   - Starting abilities / skills

2. **Antagonist** — Ask:
   - Nature (person, faction, force, self)
   - Motivation (why they oppose the protagonist)
   - Connection to protagonist (personal, ideological, coincidental)

3. **Supporting cast** — Ask if they want 1-3 key NPCs:
   - Role: Mentor, Companion, Rival, Love Interest, Trickster, Guide
   - One defining trait per NPC

Present a character lineup summary after this phase.

### Phase 4: Plot Structure

Offer a narrative structure choice:

- **Three-Act** — Setup, Confrontation, Resolution
- **Hero's Journey** — Call to adventure through return
- **Branching** — Multiple paths with diverging outcomes
- **Episodic** — Self-contained chapters/missions
- **Open World** — Player-driven with a loose main thread

Then collaboratively build:

1. **Inciting incident** — What triggers the story? Offer 3 options based on world + characters
2. **Act 1 / Setup** — First 20% of the game, what does the player experience?
3. **Midpoint twist** — What changes everything halfway through?
4. **Act 2 / Rising action** — Escalating stakes, what goes wrong?
5. **Climax** — The final confrontation or revelation
6. **Resolution** — How does it end? Offer multiple ending possibilities if branching

### Phase 5: Quests & Missions

For each major story beat, generate:

1. **Main quests** — 5-8 core story missions with:
   - Quest name
   - Objective (1 sentence)
   - Location
   - Key NPCs involved
   - Reward / story unlock

2. **Side quests** (optional) — Ask if they want 3-5 side quests:
   - Tied to world lore or character backstory
   - Optional but enriching

### Phase 6: Dialogue & Lore Samples

If the user wants, generate:

- Opening cinematic / narration (3-5 paragraphs)
- Key dialogue exchange (protagonist meets antagonist)
- 2-3 lore entries (journal entries, codex items, environmental storytelling)
- Item descriptions for key objects

### Phase 7: Story Document Output

Compile everything into a structured markdown document:

```markdown
# [Game Title] — Game Story Document

## Overview
- Genre: ...
- Tone: ...
- Setting: ...
- Target: ...

## World
[World description]

## Characters
### Protagonist: [Name]
### Antagonist: [Name]
### Supporting Cast

## Plot
### Act 1: [Title]
### Act 2: [Title]
### Act 3: [Title]

## Quest Log
### Main Quests
### Side Quests

## Lore & Dialogue
### Opening Narration
### Key Dialogues
### Lore Entries

## Themes & Motifs
```

Save this to `<project>/docs/game-story.md` (or the user's preferred location).

## Rules

- **Always ask, never assume.** Present 2-4 options at each decision point plus a custom option.
- **Summarize after each phase** before moving on. Let the user revise.
- **Keep it concise.** Story beats should be 1-3 sentences. Full prose only in Phase 6.
- **Reference the 3d-game-design skill** when discussing engine capabilities, physics, or technical feasibility.
- **No spoilers upfront.** Build the story incrementally so the user experiences the creative process.
- If the user already has a partial story, ask what's done and fill in the gaps.
