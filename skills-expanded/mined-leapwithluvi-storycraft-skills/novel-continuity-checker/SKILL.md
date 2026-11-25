---
name: novel-continuity-checker
description: "Use when auditing chapters for factual inconsistencies, timeline contradictions, character physical drift, inventory leaks, and magic rule violations — compares draft text against the canonical Story Bible."
version: "1.0.0"
category: "continuity"
stage: 6
tags: ["novel", "fiction", "continuity", "audit", "editing", "lore", "timeline", "consistency", "fact-checking"]
---

# Overview & Purpose

This skill acts as an uncompromising forensic continuity auditor for novel drafts. Over the course of drafting a full-length book, authors constantly make subconscious errors: a character’s eyes change from hazel to blue; a bullet wound sustained on Tuesday is forgotten on Wednesday; a character spends money from an empty coin purse; or travel between two distant cities happens in three hours instead of three days. These continuity fractures shatter reader immersion and undermine narrative credibility.

The agent uses this skill to:
- Cross-examine draft prose against canonical entries in `story-bible.md` and `story-state.md`.
- Audit **Physical & Biometrical Continuity** (scars, eye color, dominant hand, age, height, hair, clothing).
- Track **Inventory, Weapons & Chain of Custody** (verifying that items used in scenes were actually acquired and not lost or expended earlier).
- Verify **Somatic & Wound Continuity** (ensuring physical injuries heal realistically according to medical or magical timelines).
- Validate **Chronology & Spatial Travel Logistics** (checking travel times, lunar phases, day/night cycles, and weather patterns).

## When to Use & Trigger Phrases

**Activate this skill when:**
- A chapter draft has just been completed and needs verification before moving to the next chapter.
- Merging chapters written out of chronological order.
- Auditing a manuscript before submission, querying, or publication.
- A character has suffered an injury or lost an item in previous chapters.
- Resolving timeline ambiguities (e.g., "Wait, what day is it in Chapter 9?").

**Example trigger phrases:**
- "Check Chapter 5 for continuity errors"
- "Audit my draft against the story bible"
- "Did I forget about Marcus's broken arm in this scene?"
- "Check the timeline and travel distances between Chapter 3 and Chapter 4"
- "Run a continuity check on character traits and inventory"
- "Verify that my magic rules weren't violated in this fight"

## Core Literary Methodology & Rules

### 1. The 5-Vector Continuity Matrix
Every chapter audit must evaluate five distinct continuity vectors:
1. **Biometrical & Trait Vector**:
   - Eye/hair color, skin tones, dominant hand, scars, tattoos, physical height relative to other characters in the room.
2. **Somatic & Injury Vector**:
   - Every physical trauma must obey a realistic or magical recovery curve. If a protagonist dislocated their shoulder in Chapter 6, they cannot draw a sixty-pound longbow with that arm in Chapter 7 without excruciating pain and structural failure.
3. **Inventory & Custody Vector**:
   - Every physical prop (keys, guns, coins, scrolls, lockpicks) must have a documented point of origin, chain of custody, and expenditure. Items do not teleport into pockets.
4. **Temporal & Chronological Vector**:
   - Elapsed hours, meal times, sleep cycles, day/night lighting, days of the week, weather consistency, and seasons.
5. **Rules of the Universe Vector**:
   - Magic, technology, and societal laws established in `story-bible.md` must not be bent to allow characters an easy out. Magic costs must be paid in full on the page.

### 2. The Chain of Custody Law
If a character pulls an object out of their pocket in Scene X, the auditor asks three forensic questions:
1. *Where and when did they acquire this object?*
2. *Did they ever surrender it, lose it, or have it confiscated in an intervening scene?*
3. *If it is a consumable resource (ammunition, matches, gold coins, fuel), has the current expenditure been subtracted from their reserve?*

### 3. The Biological Wound Decay Curve
In fiction, characters do not have video-game health bars that reset after a night's sleep. Wounds persist and dictate tactical options:
- **Immediate (0–2 hours)**: Shock, bleeding, loss of grip strength, adrenaline masking pain.
- **Acute (2–24 hours)**: Adrenaline crash, severe throbbing, swelling, fever risk, extreme stiffness.
- **Sub-acute (2–7 days)**: Scabbing, bruising turning yellow/green, risk of bacterial infection, muscle atrophy.
- **Long-term (Weeks–Months)**: Permanent scar tissue, nerve tingling in cold weather, altered gait.

## Required Project State & Inputs

**Before executing this skill, check for:**
- `story-bible.md` (the canonical benchmark for characters, items, magic rules, and world timeline).
- `story-state.md` (active chapter state, recent injuries, inventory log, and timeline tracker).
- The drafted chapter text undergoing audit.

**If no inputs exist:** Alert the author that no canonical `story-bible.md` exists and construct a baseline dossier before auditing.

## Step-by-Step Execution Protocol

1. **Step 1: Ingest Chapter & Map Entities**
   - Read the draft chapter. Highlight every mention of:
     - Characters appearing or referenced.
     - Items handled, fired, exchanged, or spent.
     - Physical actions requiring bodily exertion or injured limbs.
     - References to time, day, season, or weather.
     - Magical spells or specialized technologies used.

2. **Step 2: Compare Against `story-bible.md`**
   - Verify character physical descriptions against §2 (Character Dossiers).
   - Verify magic/tech costs against §4 (Magic Systems).
   - Verify location layouts against §5 (Locations).

3. **Step 3: Cross-Reference with `story-state.md`**
   - Check the active inventory: Did the character have this weapon when they entered the building?
   - Check the injury status: Is the character favoring their wounded leg or using it to jump across roofs?
   - Check timeline elapsed: Has enough time passed for travel or healing?

4. **Step 4: Generate Forensic Continuity Report**
   - Document all discrepancies using a standardized severity scale:
     - [CRITICAL] **Critical Breach**: Impossible physical action, resurrection of dead character, violation of core magic law.
     - [MODERATE] **Moderate Discrepancy**: Forgotten injury, inventory teleportation, travel time error.
     - [MINOR] **Minor Drift**: Eye color mismatch, slight clothing change without scene transition, imprecise date.

5. **Step 5: Provide Direct Redline Corrections**
   - For every flagged issue, provide the exact sentence revision that reconciles the text with canon.

## Quality Checklist & Verification Criteria

- [ ] Are all character physical traits identical to their canonical entries in `story-bible.md`?
- [ ] Are all active injuries from previous chapters honored in character movement and dialogue?
- [ ] Does every item used in the scene have an unbroken chain of custody?
- [ ] Do travel times and distances align with the master map and timeline?
- [ ] Were all magical and technological costs paid in full without convenient loopholes?
- [ ] Is the day/night and weather state consistent with preceding and succeeding chapters?

## Anti-Patterns & Prohibited AI Tropes

- **The Magic Pockets Syndrome**: Characters producing rope, chalk, lockpicks, extra ammunition, or disguises that were never packed or purchased.
- **The Wolverine Recovery**: A character getting stabbed in the thigh in Chapter 4 and sprinting across rooftops in Chapter 5 without a limp, bandage, or pain mention.
- **The Shifting Eye Color**: Describing a character's "emerald green eyes" in Chapter 2, "piercing blue eyes" in Chapter 8, and "warm hazel gaze" in Chapter 15.
- **The Teleporting Fleet / Horse**: Moving characters across a continent in two days when the map scale and technology require three weeks.
- **The Free Spell**: A magic user casting their most powerful spell without suffering the nausea, blood loss, or fatigue established in the world rules.

## Concrete Examples (Before vs. After Craft Application)

### Example 1: Somatic & Injury Continuity Audit

**Draft Text (Flagged with Violations):**
> Chapter 8:  
> Marcus kicked open the iron hatch and pulled himself up into the attic using both hands. He drew his heavy broadsword with a flourish, holding it high in his left hand to deflect the assassin's throwing knives, then swung his shield with his right arm to bash the assassin into the chimney.

**Forensic Audit Findings:**
>  **CRITICAL CONTINUITY BREACH:**  
> - In Chapter 6 (two story days ago), Marcus had his left collarbone fractured by a warhammer blow from Captain Brandt. `story-state.md` specifically logs: *"Marcus: Left clavicle fractured, arm strapped to torso in sling; high fever."*  
> - In Chapter 8, Marcus pulls himself through a hatch using "both hands," wields a broadsword single-handedly with his injured left arm, and engages in heavy athletic combat with zero pain, splints, or limitation.

**Redline Correction (Preserving Canon and Deepening Tension):**
> Marcus rammed his right shoulder under the iron hatch, screaming through clenched teeth as the strain pulled against the linen sling binding his broken left collarbone. He couldn't climb; he had to scramble through the opening with one arm and his boots, dragging himself onto the attic floorboards like a half-drowned hound. He couldn't lift the broadsword. Instead, he drew his eight-inch trench knife with his good right hand, dropping behind a cedar trunk as the assassin's throwing knives splintered the shingles above his head.

### Example 2: Inventory & Custody Discrepancy

**Draft Text (Flagged with Violations):**
> Chapter 12:  
> Elena smiled calmly and reached into her velvet evening bag. She pulled out the brass cipher key and handed it to the Duke. "Here is the key to the vault," she said.

**Forensic Audit Findings:**
> [MODERATE] **MODERATE INVENTORY BREACH:**  
> - In Chapter 10, Scene 3, Elena was arrested in the conservatory and had her evening bag, coat, and jewelry confiscated by the palace guards. She escaped from the cellar cell in Chapter 11 with only a stolen butter knife and a bedsheet.  
> - The text never shows Elena retrieving her confiscated bag or recovering the cipher key from the guardroom.

**Redline Correction (Reconciling Chain of Custody):**
> Elena smiled calmly, reaching not into a bag, but into the hollow hem of her riding skirt, where she had stitched the brass cipher key before even entering the palace. She slipped the cold metal from the lining with her thumb and tossed it onto the Duke’s mahogany table. "The guards took my purse and my pearls," she said, "but they didn't search the horsehair petticoats. Here is your key."

## Session State Hook

When completing a continuity check:
1. Save the Forensic Continuity Audit Report into `docs/storycraft/audits/continuity-audit-ch[N].md`.
2. Update `story-state.md` under:
   - `## 3. Session Checkpoint & Recent Decisions` (log resolved continuity issues or canonized adjustments).
   - Check that inventory and injury trackers are 100% synchronized with the latest draft facts.
3. Record any newly introduced facts in `story-bible.md`.
4. Set the Next Session Bootstrap Prompt toward the next chapter drafting phase.
