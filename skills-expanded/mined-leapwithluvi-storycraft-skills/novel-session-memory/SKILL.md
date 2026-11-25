---
name: novel-session-memory
description: "Use to maintain persistent narrative state across AI sessions, token window limits, and project pauses — manages story-state.md, tracks active chapters and character conditions, and generates zero-latency resume bootstrap prompts."
version: "1.0.0"
category: "auxiliary"
stage: 0
tags: ["novel", "fiction", "session", "memory", "state", "persistence", "context-window", "continuity", "bootstrap"]
---

# Overview & Purpose

This skill functions as the persistent neural backbone of the entire StoryCraft ecosystem. AI language models suffer from finite context windows, conversational truncation, and session resets. Without an automated, disciplined state management mechanism, long-form novel projects inevitably suffer from narrative amnesia: characters forget their recent trauma, plot threads vanish, inventory resets, and the author must spend forty minutes re-explaining the plot every time they open a new chat session.

The agent uses this skill to:
- Maintain and update the living **`story-state.md`** project file after every significant creative milestone.
- Track real-time **Narrative Coordinates** (active chapter, active scene, active POV character, cumulative word count, story timeline day).
- Maintain an active ledger of **Open Plot Threads, Unresolved Loops & Looming Stakes**.
- Record **Session Checkpoints and Tactical Lore Decisions** established during the current working session.
- Generate an authoritative **Next-Session Bootstrap Prompt** that allows any AI agent (Antigravity, Claude, Cursor, Codex) to resume drafting instantly with zero context loss.

## When to Use & Trigger Phrases

**Activate this skill when:**
- Ending a writing or planning session with the author.
- The conversation history is getting long, approaching token limits, or showing warning signs of compaction.
- Starting a brand-new chat session in an existing novel workspace.
- A major plot milestone, character death, romance development, or item loss has just occurred in the manuscript.
- The author asks: "Where were we?", "Summarize where we left off", or "Prepare the resume prompt for next time."

**Example trigger phrases:**
- "Update the story state"
- "Save session progress"
- "Where did we leave off last time?"
- "Prepare the next session bootstrap prompt"
- "Check our active plot threads and unresolved loops"
- "Checkpoint the current chapter before closing"

## Core Literary Methodology & Rules

### 1. The Zero-Latency Bootstrap Philosophy
A novel state file must not be an unstructured dumping ground of conversational transcripts. It must be a precision dashboard engineered for immediate cognitive ingestion by an LLM in under 500 tokens:
- **High Signal-to-Noise**: Only record actionable current facts, active constraints, and immediate forward momentum.
- **Self-Contained**: An agent reading `story-state.md` for the first time should be able to begin drafting the very next paragraph without asking the author "What happened previously?"

### 2. The Four Pillar State Architecture (`story-state.md`)
1. **Pillar 1: Narrative Header Coordinates**:
   - Title, Last Updated Date, Current Active Chapter, Current Active Scene, Active POV Character, Approximate Word Count, Current Story Date/Time.
2. **Pillar 2: Quick Narrative Summary**:
   - 2–3 sentences summarizing the total arc so far, followed by 1 sentence on the immediate preceding scene's climax.
3. **Pillar 3: Active Plot Threads & Stakes**:
   - *Main Plot (A-Plot)*: Immediate active objective and impending catastrophe if delayed.
   - *Subplots (B-Plot / C-Plot)*: Emotional or investigative sub-threads currently in play.
   - *Unresolved Loops*: Secrets, clues, or promises that must be paid off.
4. **Pillar 4: Session Checkpoint & Delta Log**:
   - *Character State & Trauma*: New injuries, fatigue levels, emotional breakthroughs.
   - *Inventory & Currency Delta*: Items acquired, spent, stolen, or lost.
   - *Canonical World Decisions*: Rules or facts established during this session.
5. **Pillar 5: The Master Bootstrap Prompt**:
   - A single, formatted blockquote that the author can copy-paste into a brand-new chat session to resume work flawlessly.

### 3. The Continuous Synchronization Rule
Every creative skill in the StoryCraft catalog (`novel-scene-beater`, `novel-character-architect`, `novel-pacing-doctor`, etc.) ends with a **Session State Hook**. The agent must never declare a task complete without executing the corresponding update to `story-state.md`.

## Required Project State & Inputs

**Before executing this skill, check for:**
- `templates/story-state.template.md` (if initializing for the first time).
- Existing `story-state.md` in the project root.
- Recent changes from drafted scenes or structural plans.

**If no inputs exist:** Run `storycraft init` or copy from `templates/story-state.template.md`, then interview the author to populate current narrative coordinates.

## Step-by-Step Execution Protocol

1. **Step 1: Ingest Current Session Deltas**
   - Identify what changed during the current conversation:
     - Did the chapter number or scene advance?
     - Did a character gain or lose a physical asset or sustain an injury?
     - Was a new secret, alliance, or betrayal canonized?
     - How many words were drafted or revised?

2. **Step 2: Read Existing `story-state.md`**
   - Open the project's `story-state.md`.
   - Reconcile current facts against the previous state (retire resolved plot threads, increment word count, advance the story clock).

3. **Step 3: Update Header & Coordinate Block**
   - Update `**Last Updated:** [Current Timestamp]`.
   - Update `**Current Active Chapter:**` and `**Current Active Scene:**`.
   - Update `**POV Character:**` and `**Word Count:**`.

4. **Step 4: Prune and Update Plot Threads**
   - Move resolved threads to the historical summary.
   - Ensure the Main Plot lists the immediate physical obstacle confronting the POV character right now.

5. **Step 5: Formulate the Next Session Bootstrap Prompt**
   - Draft the bootstrap prompt following the exact formula:
     > *"We are writing [Novel Title]. Currently working on Chapter [N], Scene [M] from the POV of [Character]. In the last scene, [Immediate Past Event/Disaster]. Right now, [Character] is [Immediate Objective / Facing Immediate Threat]. Refer to story-state.md and story-bible.md. Continue drafting from beat: [Next Action Beat]."*

6. **Step 6: Write to Disk & Present Confirmation**
   - Save `story-state.md` to the project root.
   - Present the bootstrap prompt to the author as their departure receipt.

## Quality Checklist & Verification Criteria

- [ ] Does `story-state.md` accurately reflect the latest narrative coordinates (Chapter, Scene, POV, Word Count)?
- [ ] Are all active character injuries, somatic conditions, and inventory changes recorded?
- [ ] Are resolved plot threads pruned to prevent cognitive bloat in future sessions?
- [ ] Does the Next Session Bootstrap Prompt contain all necessary context to resume drafting without asking clarifying questions?
- [ ] Is the document free of unnecessary conversational chatter and formatted in clean, parseable Markdown?
- [ ] Does the timeline tracker match the canonical Master Timeline in `story-bible.md`?

## Anti-Patterns & Prohibited AI Tropes

- **The Amnesiac Sign-Off**: Ending a writing session without updating `story-state.md`, leaving the next session completely blind to the work done.
- **The Infinite Accumulator**: Appending every single past scene description into `story-state.md` until the file becomes 50,000 words long, defeating the entire purpose of context-window optimization.
- **The Vague Bootstrap Prompt**: Generating a resume prompt like *"Let's continue writing the novel soon!"* instead of providing exact chapter, scene, POV, and immediate beat instructions.
- **Desynchronized Inventories**: Forgetting to update character assets after an item is stolen or destroyed in the scene.
- **The Hallucinated Word Count**: Leaving word counts blank or guessing wild numbers without verifying actual draft progress.

## Concrete Examples (Before vs. After Craft Application)

### Example 1: Updating Story State After a High-Stakes Vault Breach Scene

**Before (Vague, Informal, Inactionable):**
> I've saved your notes. In our session today, we wrote Chapter 7 where Kira broke into the vault. She got hurt a little bit, but she found the obsidian dagger. Next time, we can write Chapter 8 where she tries to escape. Good job writing today!

**After (Precision Structured State & Authoritative Bootstrap):**
> Updated `/story-state.md` with session deltas:
> 
> ```markdown
> # Novel Project State: The Iron Meridian
> 
> **Last Updated:** 2026-11-01 16:45 UTC  
> **Current Active Chapter:** Chapter 8: The Gilded Leash  
> **Current Active Scene:** Scene 1: South Courtyard Extraction  
> **POV Character (this chapter):** Kira Vance  
> **Word Count (approximate):** 24,800 words  
> **Current Story Date & Time:** Year 942, Day 4 (Midnight, 00:15)  
> 
> ## 1. Quick Narrative Summary
> Inquisitor Thorne framed Kira's guild for the southern arsenal theft. To clear her name, Kira breached the subterranean vault beneath the Glass Pavilion, expecting treasury bonds. Instead, she discovered her comatose brother in stasis and recovered the Obsidian Dagger of Voros.
> 
> ## 2. Active Plot Threads & Stakes
> - **Main Plot (A-Plot):** Evacuate the Glass Pavilion with the Obsidian Dagger before the perimeter cordon seals at 00:30. Stakes: Immediate execution.
> - **Subplot B (Relational):** Captain Brandt believes Kira is a loyal imperial scout; Kira must escape without Brandt seeing her face, or his career and life are forfeit.
> - **Unresolved Loop:** Who paid the stasis fees for Kira's brother? (Signed with signet ring bearing a cracked emerald).
> 
> ## 3. Session Checkpoint & Recent Decisions
> - **Character State:** Kira suffered second-degree frostbite on right thumb and palm from handling the Obsidian Dagger without gloves (-2 Dexterity with right hand).
> - **Inventory Delta:** Acquired *The Talon of Voros* (concealed in left boot-heel); expended 2 smoke pellets; down to 1 grappling cartridge.
> - **World Lore Canonized:** Thermal siphoning rules of obsidian relics verified; stasis pods require imperial ether-batteries.
> 
> ## 4. Next Session Bootstrap Prompt
> > "We are writing 'The Iron Meridian'. Currently drafting Chapter 8, Scene 1 from the Deep POV of Kira Vance. In the previous scene, Kira secured the Obsidian Dagger of Voros from the subterranean vault, but suffered frostbite on her right hand and triggered the silent alarm. She is now standing on the southern glass terrace in heavy rain with 15 minutes before Captain Brandt’s hounds seal the gates. Refer to story-state.md and story-bible.md. Continue drafting from Beat 1: Kira navigating the grease-slick roof gutters toward the stable wall with a numb right hand."
> ```

## Session State Hook

When executing this skill:
1. Always write changes directly to `story-state.md` in the author's novel project root.
2. Confirm that the file has been successfully saved to disk.
3. Present the Next Session Bootstrap Prompt as the final output of the interaction.
