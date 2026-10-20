---
name: editorial-forge
description: >
  This skill should be used when the user asks to "make this my own,"
  "take AI content and add my voice," "forge a chapter," "authoring project,"
  "start an editorial forge project," "transform AI-generated content,"
  "build an authorship record," "forge the next chapter," "pick up where we left off
  on the book," or any request to take AI-generated or co-created starting content
  and transform it into authentically author-owned work through structured editorial
  judgment, voice injection, and narrative framing. Also trigger when the user
  references an existing Editorial Forge project folder in Google Drive, mentions
  the authorship record, or asks about the copyright status of AI-assisted writing.
  This skill should trigger aggressively — if the request touches converting AI
  content into human-owned content, editorial judgment over AI outputs, author voice
  extraction, DOB narrative structure for books or long-form content, or maintaining
  an authorship provenance trail, use it.
version: 0.1.0
---

# Editorial Forge

Transform AI-generated content into authentically author-owned work through structured editorial judgment, voice extraction, and Sorkin DOB narrative framing.

## Why This Exists

Under current US copyright law, AI-generated text without human modification is not copyrightable. What IS copyrightable is the author's **selection, coordination, and arrangement** of AI outputs — their editorial judgment. Most AI writing workflows generate first and edit after, making the author's contribution invisible. Editorial Forge inverts this: the author's intent, judgment, and voice come first. AI provides scaffolding. Every editorial decision gets logged in an authorship record.

## Core Principles

1. **Intent before generation.** No AI prose gets written until the author defines what the piece is, who it's for, and why it matters.
2. **Editorial judgment is the product.** Every selection, rejection, and rearrangement is a copyrightable act. Log all of them.
3. **Voice is extracted, not applied.** Each author gets a voice profile built from structured interview. No preset voice unless explicitly requested (e.g., MoxyWolf voice).
4. **Sorkin DOB always.** Every chapter or section uses the Desire-Obstacle-Battle narrative framework. Multi-chapter works get a book-level narrative throughline with chapter-level DOB execution.
5. **Asymmetric Q&A.** Questions may take hours or days to answer. State persists in Google Drive project folders. Pick up exactly where you left off.

## Operating Modes

### Mode 1: Project Initialization
**Triggers:** "start a new authoring project," "forge-start," "set up editorial forge for [project]," "initialize [book/document] project"

Execute the `/forge-start` command flow. See `references/state-machine.md` for the full initialization sequence.

### Mode 2: Intent Mapping (Phase 1)
**Triggers:** "define the thesis," "who is this for," "map the intent," "what does this work argue," continuing from project initialization

Ask the five intent questions ONE AT A TIME. Wait for each answer before proceeding. Never batch questions — asymmetric Q&A means answers may take days.

**The Five Intent Questions:**

1. **The Thesis**: "What does this work argue? Not what it covers — what it *argues*. Complete this sentence: 'After reading this, the reader will believe _____.'"

2. **The Reader**: "Who specifically is reading this? Not a demographic. A person. What's their title? What just happened to them that made them pick up this work?"

3. **The Refusal**: "What is this work NOT? What would a lazy version look like, and how is yours different?"

4. **The Stakes**: "What happens to your reader if they ignore this? What's the cost of not reading it?"

5. **The Authority**: "Why should this come from YOU? What have you seen, built, or survived that makes your version credible?"

After each answer:
- Write the answer to the appropriate file in `01-intent/`
- Log an `intent_defined` decision in the authorship record (include AI model, version, plugins, tools)
- Update the manifest with current progress
- Ask the next question with context from previous answers

After all five are answered:
- Generate `01-intent/thesis.md`, `01-intent/reader-profile.md`, `01-intent/intent-decisions.md`
- Update manifest: `current_phase: "structure"`
- Present a summary of the intent and confirm with the author before proceeding

### Mode 3: Structure Scaffolding (Phase 2)
**Triggers:** "propose the structure," "organize the chapters," "what should the structure be," "let's work on structure," continuing from intent mapping

1. Read the source material from `02-structure/source-material/`
2. Analyze it against the author's stated intent from Phase 1
3. Propose a structure with clear options for the author at each decision point:
   - Groupings, chapter order, what to cut, merge, split
   - Present each structural decision as a choice, not a fait accompli
   - For counter-playbook structures: propose how opposing frameworks interleave
4. Log EVERY selection, rejection, and rearrangement in the authorship record with the author's reasoning
5. After all structural decisions, generate `02-structure/approved-structure.md`
6. Create the `03-chapters/` (or `03-sections/` or `03-draft/`) skeleton

**Book-Level DOB Throughline** (for multi-chapter works):
After structure is approved, map the book-level narrative arc:
- **Desire**: What the reader viscerally wants (drawn from Phase 1 answers)
- **Obstacle**: The systemic forces working against them
- **Battle**: The journey through the work's argument
Write to `01-intent/book-throughline.md`. Present for author approval.

Update manifest: `current_phase: "voice"`

### Mode 4: Voice Extraction (Phase 3)
**Triggers:** "build [person]'s voice profile," "extract the voice," "let's do the voice interview," "voice architect," continuing from structure

Invoke the **voice-architect** skill for this phase. It handles the 8-question interview, voice profile generation, and validation.

If a voice profile already exists in the project's `voice-profiles/` directory (imported from another project), detect it and ask: "I found an existing voice profile for [name]. Use it as-is, or re-interview to update?"

Update manifest: `current_phase: "writing"`

### Mode 5: Chapter Writing with DOB (Phase 4)
**Triggers:** "forge the next chapter," "write chapter [N]," "let's work on [chapter name]," "generate prose for [section]," continuing from voice extraction

For each chapter or section, execute four steps:

**Step 1 — DOB Mapping:**
Map the chapter-level Desire-Obstacle-Battle. Write to `ch-XX-[slug]/dob-map.md`.

For **counter-playbook structures** (like The Assured Playbook):
- **Desire**: The reader wants to succeed with integrity — to win without becoming the person the opposing playbook describes
- **Obstacle**: The opposing framework's rule (e.g., Greene's law) — the power play, the manipulation, the shortcut. Present it honestly; do not strawman it. The reader needs to feel why it's tempting.
- **Battle**: The counter-rule as a structural counter-move that beats the power play through advantage, not naive moralism

Present DOB mapping to author for approval. Log the approval or modifications.

**Step 2 — Chapter-Specific Voice Q&A:**
Ask 3-5 targeted questions per chapter (shorter and more focused than the Phase 3 interview):
- "For [this topic], what's a specific situation you've seen where this played out?"
- "What's the thing most people try first that fails?"
- "If you had 30 seconds to convince a skeptic, what would you say?"
Write answers to `ch-XX-[slug]/qa-transcript.md`.

**Step 3 — Generation:**
Generate prose using ALL of:
- Chapter DOB map
- Author voice profile
- Chapter-specific Q&A answers
- Approved structure
- Book-level throughline context

The author's specific examples and language from Q&A become the backbone. AI provides connective tissue, transitions, and structural coherence. Write to `ch-XX-[slug]/draft-v1.md` and copy to `draft-current.md`.

**Step 4 — Passage-Level Refinement:**
Present the draft section by section. When the author flags a passage:
- Diagnose the issue (too generic, too soft, wrong tone, needs a real example, not how they'd say it)
- Offer targeted refinement options
- Log every refinement decision in the authorship record

After refinement, update `draft-current.md`.

Update manifest after each chapter: increment `chapters_complete`, update `current_chapter`.

### Mode 6: Verification and Delivery (Phase 5)
**Triggers:** "verify the manuscript," "final check," "compile the authorship record," "we're done — wrap it up"

1. **Voice consistency audit**: Read the complete work against the voice profile. Flag passages that drift toward generic AI prose.
2. **DOB integrity check**: Verify each chapter's narrative arc resolves and the book-level throughline holds.
3. **Authorship record summary**: Generate a human-readable "creative provenance" document from the JSON record.
4. **Anti-detection audit**: Run an 11-point checklist calibrated to THIS author's voice profile (not MoxyWolf defaults unless requested):
   - Contraction usage matches author's natural register
   - No forbidden phrases from voice profile
   - No formulaic transitions
   - Sentence length variation matches author's rhythm
   - Intentional fragments where author uses them
   - Specific examples from Q&A are present (not genericized)
   - Paragraph length varies
   - Sentence starters include conjunctions where natural
   - Punctuation matches author's style
   - Emotional register matches author's patterns
   - Technical depth matches author's vocabulary comfort

## Authorship Record

Every decision logged in `authorship-record.json` includes:

```json
{
  "id": "d-NNN",
  "timestamp": "ISO-8601",
  "phase": "intent|structure|voice|writing|verification",
  "type": "thesis_defined|section_rejected|section_rearranged|voice_injection_answer|passage_rejected|dob_approved|...",
  "author": "Author Name",
  "ai_model": "model-identifier",
  "ai_model_version": "version-string",
  "plugins_active": ["editorial-forge", "..."],
  "tools_used": ["google_drive_search", "..."],
  "description": "What was decided",
  "context": "Why — the author's reasoning"
}
```

The project-level `environment` block in the manifest captures baseline model, version, plugin version, and tools. Individual decisions override when anything changes mid-project.

## State Persistence

All state lives in the Google Drive project folder. Read `references/state-machine.md` for the full state machine, manifest schema, and resume logic.

**Critical rule**: On every question asked, write it to the manifest as `pending_question` with full context. On resume, re-present the pending question. Never lose the thread.

## Google Drive Integration

Use `google_drive_search` to find project folders (search for `name contains '[Project Name] – Editorial Forge'`).
Use `google_drive_fetch` to read project files.
Create and update files via Google Drive tools when available, or instruct the user to place files in the appropriate directory.

## What This Skill Does NOT Do

- Does not apply MoxyWolf voice unless explicitly requested. Each author's voice is their own.
- Does not auto-generate without author input. Every phase requires human answers and approvals.
- Does not skip phases. Intent before structure before voice before prose.
- Does not operate at the individual-rule or individual-section level for DOB. DOB is always chapter-level (or piece-level for single works) with a throughline for multi-chapter works.
