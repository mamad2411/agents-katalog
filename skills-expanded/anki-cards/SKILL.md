---
name: anki-cards
description: >
  Distill conversations into Anki flashcards exported as a TSV file. Use this skill whenever the user
  mentions Anki, flashcards, spaced repetition cards, "make cards from this", "distill into cards",
  "I want to memorize this", "create review cards", or any variation of turning conversation content
  into study material. Also trigger when the user says things like "help me remember this",
  "summarize for Anki", "extract key facts for review", or references exporting to Anki/SRS.
  Even if the user just says "cards" or "flashcards" in the context of studying or memorizing
  conversation content, use this skill.
---

# Anki Flashcard Generator

Turn conversation content into high-quality Anki flashcards, exported as a TSV file ready for import.

## Workflow

### 1. Gather Parameters

When the user asks for Anki cards, ask two things before generating:

1. **How many cards?** — Ask for a target number. If the conversation is short, suggest a reasonable range (e.g., "This conversation covered ~3 key topics — I'd suggest 5–10 cards. How many would you like?").

2. **One-sided or double-sided?** — Default suggestion is one-sided. Briefly explain the double-sided option:
   - **One-sided (default):** Front = question, Back = answer.
   - **Double-sided:** Both sides are questions. Knowing either side lets you recall the other. Example:
     - Front: *"What flag has red crosses on a white background?"*
     - Back: *"How does the flag of Georgia look?"*

### 2. Extract Key Facts from the Conversation

Review the conversation and identify the facts, concepts, distinctions, and relationships that the user would benefit from memorizing. Focus on:

- New information the user learned (things they asked about or expressed surprise at)
- Core concepts and definitions
- Key distinctions or comparisons discussed
- Concrete facts (names, numbers, dates, formulas, commands)
- Cause-and-effect relationships
- Corrections or misconceptions that were cleared up

Ignore: pleasantries, meta-discussion about the conversation itself, tangential remarks, and anything the user clearly already knew.

### 3. Write Cards Following Best Practices

Every card **must** follow these principles:

#### Minimum Information Principle
Each card tests exactly **one** atomic fact or association. Never combine multiple facts into a single card.

- BAD: *"What are the three types of heat transfer?"* → *"Conduction, convection, and radiation"*
- GOOD: Three separate cards, each asking about one type, or each asking what category a given type belongs to.

#### No Orphan Cards
Every card must contain enough context to be understood in isolation, months later, without remembering the original conversation. Add brief context cues where needed.

- BAD: *"What does it do?"* → *"It reduces memory fragmentation"*
- GOOD: *"What does tcmalloc do for long-running C++ processes?"* → *"It reduces memory fragmentation compared to glibc's default allocator"*

#### No Ambiguity
Questions must have exactly one correct, unambiguous answer. Avoid questions that could reasonably have multiple different correct responses.

#### Concrete Over Abstract
Prefer cards that test concrete, verifiable facts over vague conceptual understanding. If a concept is abstract, ground it with a specific example.

#### Use HTML Formatting
Anki renders HTML natively, not Markdown. All card content must use HTML tags for formatting:
- Bold: `<b>...</b>`
- Italic: `<i>...</i>`
- Code: `<code>...</code>`
- Line breaks: `<br>` (not newlines — keep each card on one TSV line)

Never use Markdown syntax (`**bold**`, `*italic*`, `` `code` ``) in card text — Anki will display it as raw characters.

#### Keep It Crisp
Long cards are demotivating and hurt retention. Answers should be **telegram-short**: bare facts, no filler, no articles or verbs unless needed for clarity. Target **≤12 words** on the answer side. If an answer exceeds 12 words, look for ways to split or compress.

Rules:
- Strip leading articles ("a", "the") and filler phrases ("it is", "this refers to")
- Use fragments, not sentences: noun phrases, "X → Y" arrows, dashes
- Never restate the question in the answer
- Use symbols and abbreviations where unambiguous (→, ~, vs, e.g.)

- BAD: *"It is a world model that learns to understand, predict, and plan in the physical world from video"*
- GOOD: *"World model — understand, predict, plan from video"*
- BAD: *"6 times the parameters (7B vs ~1.1B) and 12 times the training data (1.7B images vs ~142M)"*
- GOOD: *"6× params (7B vs ~1.1B), 12× data (1.7B vs ~142M images)"*

#### Use Context Cues
Start questions with a domain or topic tag when the fact could belong to multiple fields:

- *"In stereo vision, what does SGM stand for?"* rather than *"What does SGM stand for?"*

#### Bidirectional Cards (Double-Sided Mode)
When the user requests double-sided cards, both the front and back are phrased as questions. The core invariant is:

**Each side's question must *contain* the other side's answer in its wording, and that embedded answer must be wrapped in `<b>...</b>` tags.**

**A side must NEVER contain its own answer, even as plain-text context.** This is the most common failure mode: you add helpful phrasing like "For NVIDIA GPU codegen, MLIR lowers…" and accidentally reveal the answer that the reader was supposed to recall. If context words overlap with the answer, rephrase to remove the leak.

When you see side A, you can answer it — and that answer appears as a bold word or phrase inside side B's question (and vice versa). Both sides are self-contained questions, but they embed each other's answers in bold.

GOOD example:
- Front: *"What flag has multiple red crosses on a white background?"*
- Back: *"How does the flag of <b>Georgia</b> look?"*
- See front → answer: "Georgia" → back contains "<b>Georgia</b>" ✓
- See back → answer: "red crosses on white" → front contains "red crosses on a white background" (bold the key phrase in the actual TSV) ✓

GOOD example:
- Front: *"In <code>nm</code> output, what does <b>W</b> mean?"*
- Back: *"In <code>nm</code>, which letter marks a <b>weak symbol</b> that can be overridden without linker errors?"*
- See front → answer: "weak symbol" → back contains "<b>weak symbol</b>" ✓
- See back → answer: "W" → front contains "<b>W</b>" ✓

BAD example (answer on neither side):
- Front: *"Which ELF symbol table survives `strip`?"*
- Back: *"Which ELF symbol table does ld.so need at runtime?"*
- Both answer ".dynsym" — but neither side contains ".dynsym"! In Anki review, you'd see a question with no answer on the card.

BAD example (tautological):
- Front: *"In ELF, which symbol table does plain `nm` read?"*
- Back: *"Which ELF section is called .symtab?"*
- See back → answer: ".symtab" → front doesn't help you know it's called .symtab, it just asks a parallel question about the same concept.

BAD example (self-answering — most common failure):
- Front: *"What vendor-specific MLIR dialect does the GPU dialect lower to for <b>NVIDIA</b> GPUs?"*
- Back: *"For NVIDIA GPU codegen, MLIR lowers GPU ops to the <b>NVVM dialect</b>. What vendor is NVVM for?"*
- Back asks "What vendor is NVVM for?" but already says "For NVIDIA GPU codegen" — the reader sees the answer without recalling anything.
- Fix by removing the leaked context: Back → *"Which vendor's GPUs use the <b>NVVM dialect</b> as their MLIR lowering target?"*

After drafting double-sided cards, verify **every** pair with this checklist:
1. "If I see only side A, does side B's text contain my answer in bold?" If no → rewrite.
2. "If I see only side B, does side A's text contain my answer in bold?" If no → rewrite.
3. "Does side A contain its own answer anywhere (even in plain text context)?" If yes → rephrase to remove the leak.
4. "Does side B contain its own answer anywhere (even in plain text context)?" If yes → rephrase to remove the leak.

This checklist must be applied to **every card**, not just the first few. Quality tends to drift on longer batches — if anything, slow down and be more careful on cards 8+.

### 4. Generate the TSV File

Output format:
- **File type:** `.tsv` (tab-separated values)
- **Encoding:** UTF-8 (no BOM)
- **Columns:** Two columns — front and back — separated by a tab. **No header row.**
- **Quoting:** Only quote fields that contain tabs or newlines (which should be rare — keep card text on single lines)
- **Language:** Match the language of the conversation. If the conversation was in German, cards are in German. If mixed, follow the language of the technical content.

Use the computer tools to create the TSV file and present it to the user.

### 5. Offer to Refine

After presenting the cards, offer to:
- Add or remove specific cards
- Rephrase cards that seem unclear
- Adjust difficulty (split complex cards further, or merge overly granular ones)
- Switch between one-sided and double-sided for specific cards

## Edge Cases

- **Very short conversations:** If there are fewer meaningful facts than the user requested, say so and produce only as many quality cards as the material supports. Don't pad with low-value cards.
- **Highly technical content:** Prefer precision over simplicity. The user works in ML/CV/robotics — don't dumb things down. Use correct terminology.
- **Multiple topics in one conversation:** Group cards by topic in the TSV (no explicit grouping column needed — just order them by topic cluster).

## Example Output

For a conversation about Python's GIL:

```
What prevents true parallel execution of Python threads on CPU-bound tasks?	The <b>Global Interpreter Lock</b> (GIL) — a mutex allowing only one thread to hold control of the Python interpreter at a time.
In CPython, what is the GIL?	A global mutex that serializes access to Python objects, preventing multiple native threads from executing Python bytecode simultaneously.
Does the GIL affect I/O-bound multithreaded Python programs?	Minimally — GIL is released during I/O ops, so I/O-bound threads can run concurrently.
Which Python implementation removes the GIL?	Jython (JVM-based), IronPython (.NET-based). CPython 3.13+ has experimental free-threaded mode.
```
