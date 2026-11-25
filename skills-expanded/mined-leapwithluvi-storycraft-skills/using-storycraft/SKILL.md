---
name: using-storycraft
description: "Use at the start of any novel-writing session or when the author is unsure what step to take next — inspects project state, diagnoses narrative bottlenecks, and routes execution to the exact appropriate StoryCraft skill."
version: "1.0.0"
category: "auxiliary"
stage: 0
tags: ["novel", "fiction", "meta", "orchestrator", "workflow", "router", "bootstrap", "session", "pipeline"]
---

# Overview & Purpose

This meta-skill acts as the central conductor, autonomous workflow orchestrator, and master pipeline director of the entire StoryCraft ecosystem. Much like an autonomous pipeline conductor in agentic workflows, `using-storycraft` ensures that an AI agent never dives blindly into generating generic prose or ungrounded plots. Instead, it systematically assesses the author's current project lifecycle, inspects existing files (`story-state.md`, `story-bible.md`, `manuscript/`, and `docs/storycraft/`), and guides both author and agent to the single highest-leverage craft skill needed next.

The agent uses this skill to:
- Conduct an automated **Project Diagnostic Audit** upon opening a novel workspace.
- Identify the exact **Production Phase (Stages 0 through 6)** currently underway across all 23 skills.
- Run the **End-to-End Autonomous Novel Pipeline** (`/using-storycraft pipeline`) with strict `<HARD-GATE>` author approvals between phases.
- Detect **Missing Prerequisites** (e.g., attempting to draft Chapter 8 without an outline or character Lie).
- Provide a clear, actionable **Phase Routing Recommendation** so the author never feels overwhelmed.

All planning, audit, and roadmap artifacts generated during this process are saved with standardized date prefixes into `docs/storycraft/` (e.g., `docs/storycraft/YYYY-MM-DD-pitch-brief.md`).

## When to Use & Trigger Phrases

**Activate this skill when:**
- Starting a brand-new chat session in an existing novel workspace.
- The author opens with a broad prompt: "What should we do next?", "Where are we?", or "Let's continue my novel."
- Running the full novel development pipeline from zero to finished manuscript via `/using-storycraft pipeline`.
- The author is overwhelmed and doesn't know which specialized skill to call.
- Onboarding a new novel project into the StoryCraft directory layout.
- Resuming work after days or weeks away from the manuscript.

**Example trigger phrases:**
- "Where are we on my novel?"
- "What's our next step?"
- "Help me navigate my project"
- "Run the storycraft pipeline"
- "/using-storycraft"
- "/using-storycraft pipeline"
- "Start today's writing session"

## Core Literary Methodology & Rules

### 1. The Production Hierarchy of Needs (The 23-Skill Lifecycle)
Writing a novel is a sequential assembly process. Attempting downstream stages without upstream foundations produces structural collapse:
```
Stage 0: Creative Discovery & Meta-Orchestration
  (using-storycraft, novel-brainstorming, novel-session-memory)
    ↓
Stage 1: Market Positioning, Character Psychology & World Ecology
  (novel-market-analyst, novel-genre-specialist, novel-premise-hook, 
   novel-character-architect, novel-worldbuilder)
    ↓
Stage 2: Macro Plot Architecture & Long-Horizon Mega-Serials
  (novel-plot-architect, novel-twist-architect, novel-mega-serial-architect, 
   novel-chapter-outline)
    ↓
Stage 3: Scene Craft & Autonomous Deep POV Drafting
  (novel-chapter-drafter, novel-scene-beater, novel-deep-pov, 
   novel-sensory-immersion)
    ↓
Stage 4: Dialogue Subtext & Prose Musicality
  (novel-dialogue-subtext, novel-prose-stylist)
    ↓
Stage 5: Master Developmental Review Across 40 Aspects
  (novel-master-reviewer, novel-pacing-doctor, novel-structural-editor)
    ↓
Stage 6: Forensic Continuity & Canon Bible Management
  (novel-continuity-checker, novel-lore-bible)
```

- *The Cardinal Rule*: Never draft prose (Stage 3) if the character lacks an active Want and the scene lacks an opposing disaster (Stage 1 & 2).

### 2. The Master Pipeline Protocol with `<HARD-GATE>` Approvals

When the author invokes the full pipeline (`/using-storycraft pipeline`), the agent guides the author sequentially through each phase. **Under no circumstances may the agent leap across phases without explicit human approval:**

<HARD-GATE>
Before advancing to any downstream phase, the author must explicitly review and approve the artifact produced by the current phase:
- **Phase 0 Gate**: Author approves `docs/storycraft/YYYY-MM-DD-pitch-brief.md`.
- **Phase 1 Gate**: Author approves `docs/storycraft/YYYY-MM-DD-market-analysis.md` and character dossiers in `story-bible.md`.
- **Phase 2 Gate**: Author approves `docs/storycraft/YYYY-MM-DD-plot-architecture.md` and `twist-matrix.md` (and Arc Ledger for mega-serials).
- **Phase 3 Gate**: Author approves granular chapter beats in `docs/storycraft/YYYY-MM-DD-chapter-roadmaps.md`.
- **Phase 4 Gate**: Author approves drafted chapter(s) in `manuscript/chapter-[N].md`.
- **Phase 5 Gate**: Author reviews `docs/storycraft/audits/YYYY-MM-DD-review-40-aspects-ch[N].md` and approves required rewrites.
- **Phase 6 Gate**: Author approves updated `story-state.md` and canon entries in `story-bible.md`.
</HARD-GATE>

### 3. Skill Routing Matrix (All 23 Skills)

| Project Condition | Primary Skill to Route | Complementary Skill |
| :--- | :--- | :--- |
| Raw spark or idea, need thematic exploration | `novel-brainstorming` | `novel-premise-hook` |
| Concept ready, need target platform & comp strategy | `novel-market-analyst` | `novel-genre-specialist` |
| Genre chosen, need obligatory scenes & conventions | `novel-genre-specialist` | `novel-premise-hook` |
| Premise formulated, need high-concept logline | `novel-premise-hook` | `novel-character-architect` |
| Characters feel flat, need psychological Lie & Wound | `novel-character-architect` | `novel-worldbuilder` |
| Setting empty or generic, need sensory ecology | `novel-worldbuilder` | `novel-lore-bible` |
| Macro plot needed, 3-Act or 7-Point architecture | `novel-plot-architect` | `novel-twist-architect` |
| Need airtight plot twist or fair-play red herrings | `novel-twist-architect` | `novel-structural-editor` |
| Long-horizon serial (500–5,000+ chapters), power scaling | `novel-mega-serial-architect` | `novel-plot-architect` |
| Macro plot locked, need granular scene-by-scene roadmap | `novel-chapter-outline` | `novel-scene-beater` |
| Roadmap approved, ready to draft full chapter(s) | `novel-chapter-drafter` | `novel-scene-beater` |
| Scene drafted, need In-Late/Out-Early beat polishing | `novel-scene-beater` | `novel-deep-pov` |
| Prose feels distant, filter words present (*"she saw"*) | `novel-deep-pov` | `novel-sensory-immersion` |
| Scene feels like a white room, visual-only description | `novel-sensory-immersion` | `novel-prose-stylist` |
| Dialogue on-the-nose, lacks subtext and power dynamics | `novel-dialogue-subtext` | `novel-prose-stylist` |
| Prose clunky, repetitive sentence lengths, weak verbs | `novel-prose-stylist` | `novel-deep-pov` |
| Need honest, 40-vector critique against 15 comps | `novel-master-reviewer` | `novel-structural-editor` |
| Pacing drags in Act 2, tension sagging | `novel-pacing-doctor` | `novel-structural-editor` |
| Plot holes detected, Chekhov guns dangling | `novel-structural-editor` | `novel-twist-architect` |
| Chapter drafted, need forensic continuity check | `novel-continuity-checker` | `novel-lore-bible` |
| World lore expanding, need Single Source of Truth | `novel-lore-bible` | `novel-session-memory` |
| Ending writing session, need zero-latency bootstrap | `novel-session-memory` | `using-storycraft` |

## Required Project State & Inputs

**Before executing this skill, check for:**
- `story-state.md` (active coordinates, current POV, format, pending tasks).
- `story-bible.md` (canonical lore, character dossiers, magic rules).
- `manuscript/` (latest drafted chapter files).
- `docs/storycraft/` (planning briefs and date-stamped audit documents).

**If no files exist:** Offer to initialize the project via `novel-brainstorming` to birth the story.

## Step-by-Step Execution Protocol

1. **Step 1: Rapid Environment Scan**
   - Check if `story-state.md` exists. Extract:
     - Active Chapter & Scene.
     - Active POV Character.
     - Word Count & Target Publishing Platform.
   - Scan `manuscript/` for the latest file (e.g., `chapter-04.md`).

2. **Step 2: Calculate Stage Completion**
   - Evaluate whether earlier stages have unresolved gaps (e.g., missing antagonist Lie, unresolved plot hole).

3. **Step 3: Present the Executive Status Dashboard**
   - Provide a concise 4-line status summary:
     - **Novel Title & Current Coordinates**
     - **Current Milestone Objective**
     - **Identified Blockers or Open Loops**
     - **Recommended Next Skill**

4. **Step 4: Offer Clear Action Paths**
   - Give the author two distinct paths forward:
     - **Path A (The Recommended Primary Flow)**: Execute the next sequential skill.
     - **Path B (The Fast-Track Alternative)**: Jump straight to drafting or editing if the author has immediate creative momentum.

## Quality Checklist & Verification Criteria

- [ ] Does the agent accurately identify the novel's current phase without hallucinating progress?
- [ ] Are recommendations grounded in the strict Stage 0–6 literary hierarchy?
- [ ] Does the pipeline workflow enforce `<HARD-GATE>` author approval between phases?
- [ ] Are all generated planning and audit documents saved with ISO date stamps (`YYYY-MM-DD`) in `docs/storycraft/`?
- [ ] Does the agent seamlessly transition into the selected skill once the author confirms?

## Anti-Patterns & Prohibited AI Tropes

- **The "Just Start Writing" Trap**: Diving into Chapter 1 drafting when the author has not defined the protagonist's flaw or the core dramatic question.
- **The Overwhelming Menu**: Dumping all 23 skills in a giant wall of text instead of diagnosing and recommending the single best action.
- **Skipping the Hard Gates**: Autonomously generating 10 chapters without stopping for author review and feedback.
- **The Amnesiac Reboot**: Asking the author "What is your novel about?" when `story-bible.md` already contains complete dossiers.

## Concrete Examples (Before vs. After Craft Application)

### Example 1: Resuming an In-Progress Novel Project

**Before (Unassisted AI Responding to "What should we do?"):**
> Hello! You can do whatever you want! We could write a new chapter, brainstorm some characters, make a magic system, or edit previous work. What sounds fun to you today?

**After (Using-StoryCraft Autonomous Triage):**
> **StoryCraft Status Dashboard: *The Obsidian Meridian***  
> - **Current Coordinates:** Chapter 4 (Scene 2: Subterranean Canal) | POV: Kira Vance  
> - **Current Word Count:** ~11,200 words | Format: Royal Road Serial  
> - **Active Conflict:** Kira has escaped the archives with the cipher, but her left shoulder is dislocated and Captain Brandt is sealing the floodgates in 30 minutes.  
> 
> **Diagnostic Assessment:**  
> Your chapter beats for Chapter 4 are outlined, but Scene 2 has not been drafted yet. Kira's active physical trauma requires tight sensory grounding.  
> 
> **Recommended Next Step:**  
> Invoke **`/novel-chapter-drafter`** (or `/novel-scene-beater`) to draft Scene 2, integrating her injury limitations via **`novel-deep-pov`**.  
> 
> Shall we begin drafting Scene 2, or would you prefer to run a master review on Chapters 1–3 first with **`/novel-master-reviewer`**?

## Session State Hook

When completing project orchestration:
1. Always synchronize newly determined project goals into `story-state.md` under `## 2. Active Plot Threads & Stakes`.
2. Seamlessly transfer execution to the invoked skill.
