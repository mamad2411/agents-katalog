---
name: novel-lore-bible
description: "Use when creating, expanding, and curating the comprehensive project story bible — organizes relational character dossiers, world laws, chronological timelines, faction hierarchies, and thematic motifs into a single canonical source of truth."
version: "1.0.0"
category: "continuity"
stage: 6
tags: ["novel", "fiction", "bible", "lore", "worldbuilding", "canon", "continuity", "timeline", "codex"]
---

# Overview & Purpose

This skill establishes, organizes, and curates the canonical Story Bible (`story-bible.md`) for a novel or multi-volume series. As a novel expands across tens of thousands of words, human memory and AI context windows inevitably falter: character eye colors drift, city geographies shift arbitrarily, magical costs are forgotten, and family timelines collide. A disciplined Story Bible acts as the immutable constitution of the fictional universe.

The agent uses this skill to:
- Structure and maintain `story-bible.md` using a **modular, relational markdown taxonomy**.
- Build **Canonical Character Dossiers** (appearance, voice signatures, relationships, scars, secrets, character arcs).
- Log **Chronological Master Timelines** with absolute calendar dates, relative story days, and historical milestones.
- Formalize **Immutable World Rules** (magic/tech limits, economic currencies, faction politics, geography).
- Index **Thematic Motifs and Symbolic Echoes** so the manuscript maintains intellectual and aesthetic unity.

## When to Use & Trigger Phrases

**Activate this skill when:**
- Initializing a new novel project or importing an existing manuscript’s lore.
- Adding a newly invented character, kingdom, weapon, or historical event to the project's permanent canon.
- Reconciling conflicting worldbuilding details or establishing official terminology.
- Documenting magic system rules, costs, or failure modes so future scenes don't break logic.
- Preparing to draft a sequel, spinoff, or long-form narrative that requires deep historical continuity.

**Example trigger phrases:**
- "Create a story bible for my novel"
- "Add [Character Name] to the official lore bible"
- "Document the rules of my magic system in the codex"
- "Log the timeline of events from the prequel wars"
- "Organize my factions and political alliances"
- "Update the story bible with the new details from Chapter 6"

## Core Literary Methodology & Rules

### 1. The Single Source of Truth (SSOT) Architecture
In fiction writing, lore must never live scattered across disjointed scratchpads, author memories, or obsolete conversation logs. 
- **The Golden Law of Canon**: If a detail is not recorded in `story-bible.md`, it is not officially canon.
- **Relational Markdown Linking**: Use cross-referencing between sections (e.g., linking a character's weapon back to the specific magic rules section; linking a battle site back to the master timeline).

### 2. The Granular Lore Taxonomy
The Story Bible is organized into eight non-overlapping relational domains:
1. **Premise & Thematic Anchor**: The Core Dramatic Question, logline, target word count, and narrative tone.
2. **Character Dossiers**:
   - *Physical Anchors*: Height, scars, gait, vocal idiolect, clothing style.
   - *Psychological Anchors*: The Lie, the Ghost, Want vs. Need, Fatal Flaw.
   - *Relational Web*: Who they owe, who they love, who they would murder.
3. **Worldbuilding & Environmental Rules**: Geography, climate, city quarters, currency, legal codes, taboos.
4. **Magic, Technology & Power Systems**: Source, exact costs, physical limitations, failure consequences, historical breakthroughs.
5. **Key Locations & Sensory Anchors**: Concrete sensory signatures for each recurring venue (smells, sounds, architectural grit).
6. **Chronological Master Timeline**: Day-by-day story timeline + deep history epochs.
7. **Factions, Orders & Power Structures**: Internal hierarchy, public front vs. secret agenda, motto, insignia.
8. **Motifs, Themes & Symbolic Echoes**: Recurring sensory motifs (e.g., silver moths, dry well water, ticking clocks).

### 3. The Canonization Protocol
When an author or agent drafts a scene that introduces a new fact (e.g., "Uncle Corin lost his left eye at the siege of Morvath"):
- The fact must immediately be extracted from the prose and committed to `story-bible.md`.
- Future chapters are forbidden from describing Uncle Corin winking with his left eye or stating he lost it in a hunting accident.

## Required Project State & Inputs

**Before executing this skill, check for:**
- `templates/story-bible.template.md` (for new initializations).
- Existing `story-bible.md` in the project root.
- Recent chapter drafts or world notes from `novel-worldbuilder` and `novel-character-architect`.

**If no inputs exist:** Run initialization from `templates/story-bible.template.md` and populate initial sections from author briefing.

## Step-by-Step Execution Protocol

1. **Step 1: Workspace Initialization or Verification**
   - Check if `story-bible.md` exists in the novel directory. If not, instantiate it using `storycraft init` or the project template.

2. **Step 2: Information Extraction & Deduplication**
   - Read the incoming author notes or chapter draft.
   - Extract newly introduced entities: characters, locations, items, timeline dates, and cultural rules.
   - Verify against existing entries to detect contradictions before recording.

3. **Step 3: Dossier Formatting**
   - Format character and location additions using the standardized markdown schema (ensuring Want, Need, Lie, and sensory anchors are explicitly logged).

4. **Step 4: Timeline Synchronization**
   - Insert new chronological milestones into the Master Timeline with relative day markers (`Day 1: Arrival`, `Day 3: The Ball`, `Day 4, 02:00: Vault Breach`).

5. **Step 5: Relational Cross-Referencing**
   - Link related entities (e.g., under Faction A, list all affiliated characters; under Location B, list all scenes taking place there).

## Quality Checklist & Verification Criteria

- [ ] Does `story-bible.md` contain all 8 canonical domains?
- [ ] Are character profiles complete with Lie, Want, Need, physical scars, and distinct voice traits?
- [ ] Are magic and tech rules codified with explicit costs, limits, and failure penalties?
- [ ] Is the timeline organized sequentially without overlapping or missing days?
- [ ] Are all new lore facts established in recent chapters backported into the bible?
- [ ] Is the document free of speculative author chat, functioning purely as an authoritative canon reference?

## Anti-Patterns & Prohibited AI Tropes

- **The Scattered Scrapbook**: Storing lore across five different files (`characters.txt`, `notes.doc`, `magic.md`, `places.json`), making unified agent retrieval impossible.
- **The Decorative Trivia Trap**: Filling character profiles with useless trivia (favorite breakfast cereal, favorite color) while omitting their core Lie, Fatal Flaw, and driving Want.
- **The Unbounded Magic System**: Writing "Magic is limited only by the caster's imagination," which immediately destroys stakes and invites endless plot holes.
- **The Floating Timeline**: Events logged without relative day markers (e.g., "Then they traveled for a while, and later that month something happened"), leading to continuity collapse.
- **The Dead Document**: Writing a story bible once during pre-production and never updating it as the manuscript evolves and discovers new canon during drafting.

## Concrete Examples (Before vs. After Craft Application)

### Example 1: Documenting a New Magic Item / Relic

**Before (Vague & Unbounded):**
> **The Obsidian Dagger:**  
> A magical knife found in the catacombs. It glows with dark power and can cut through almost anything. It has a mysterious curse on it that makes the wielder feel evil.

**After (Standardized Canon Schema, Strict Limitations, Concrete Cost):**
> ### 4.3 Artifact Codex: The Obsidian Dagger of Voros  
> - **Canonical Name:** The Talon of Voros (*Athame of the First Exarch*)  
> - **Physical Description:** 9-inch single-edged blade carved from volcanic volcanic glass, hilt wrapped in boiled eel-skin; blade emits no reflection and is ice-cold to the touch (causes frostbite on bare skin after 60 seconds).  
> - **Power & Mechanics:** Pierces ward-cloth and magical barriers up to Tier 3 by grounding metaphysical resonance into thermal energy.  
> - **The Inflexible Cost:** For every inch of ward-cloth pierced, the blade absorbs the wielder's body heat, reducing core body temperature by 1.5°F. Piercing an entire barrier causes immediate hypothermic shivering and blood-cough.  
> - **Current Custody:** Stolen by Kira Vance in Chapter 7; concealed inside her hollow boot-heel.  
> - **Cross-References:** See *Magic Rules §4.1 (Thermal Siphoning)* and *Character Dossier §2.2 (Kira Vance)*.

### Example 2: Chronological Master Timeline Logging

**Before (Disjointed & Approximate):**
> - Chapter 1: John arrives in town.  
> - Chapter 2: John meets the mayor a few days later.  
> - Chapter 3: Next week the murder happens.  
> - Chapter 4: That night John investigates.

**After (Precise Relational Timeline):**
> ### 6. Chronological Master Timeline  
> - **Year 942, Autumn Month (Harvest Moon):**  
>   - **Day 1 (Monday, Oct 12, 14:00):** John Cross arrives at Port Morvath on the coastal packet *Zephyr*. Checked in at the Anchor & Thistle Inn. (Chapter 1)  
>   - **Day 3 (Wednesday, Oct 14, 09:30):** First audience with Mayor Vane at the Old Guildhall; Vane offers the 500-sovereign commission. John notices Vane’s missing left cufflink. (Chapter 2)  
>   - **Day 8 (Monday, Oct 19, 23:45):** Murder of Guildmaster Thorne at the dry docks. Est. time of death: 23:00–00:30 (tide was receding). (Chapter 3)  
>   - **Day 9 (Tuesday, Oct 20, 02:15):** John breaches Thorne’s office; discovers the ledger is missing and the safe unlocked from the inside. Encounter with the masked assassin. (Chapter 4)

## Session State Hook

When completing Story Bible updates:
1. Verify that all changes to canon are reflected in `story-state.md` under:
   - `## 3. Session Checkpoint & Recent Decisions`
2. Run `novel-continuity-checker` against the newest draft chapters to ensure no violations of newly established lore have occurred.
3. Set the Next Session Bootstrap Prompt toward the next chapter execution or continuity verification.
