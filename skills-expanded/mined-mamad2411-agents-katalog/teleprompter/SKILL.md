---
name: teleprompter
description: |
  Create read-aloud scripts for teleprompter. Plain prose without headings or bullet lists, calibrated for reading time at a natural reading speed.

  [WHAT] READ-ALOUD SCRIPT — text optimised to be spoken. Format: continuous prose, natural breathing pauses, short to medium sentences, no headings, no bullets. Length calibrated to target time at ~150 words/min as default.

  [WHEN] Use when: teleprompter script, voiceover script, video script, podcast script, "script for X minutes", read-aloud manuscript, YouTube script. NOT for: cue cards (use talking-points), slides (use presentation), op-ed (use op-ed).

  [LANGUAGE] Configurable. Output: plain prose ready to read directly.

  [EXPERTISE] Teleprompter writing, oral rhythm (~150 wpm), natural breathing pauses, scene-building without visual structure, word-counting for length calibration.
allowed-tools: Read, Grep, Glob, Write
---

# Teleprompter — read-aloud script

Role: scriptwriter for teleprompter, voiceover, video, and podcast.

This is not text for readers. It is text to be read OUT LOUD. The difference shapes everything.

## Difference from written text

| Written text | Read-aloud script |
|--------------|-------------------|
| Headings guide the reader's eye | No headings — they break flow |
| Bullets summarise | No bullets — they sound clumsy |
| Long sentences with subordinate clauses | Short to medium, one idea per sentence |
| Complex constructions | Natural speech rhythm |
| Skimmable | Linear, beginning to end |

## Reading speed

| Style | Words per minute | Use |
|-------|------------------|-----|
| Slow, emphatic | 130 | Serious topics, important points |
| Normal | 150 | Default |
| Fast, energetic | 170 | Opening, closing |

**Calibration:**
- 1 minute of text ≈ 150 words
- 3 minutes ≈ 450 words
- 5 minutes ≈ 750 words
- 10 minutes ≈ 1500 words

Always count words in the final version. Adjust to target time.

## Sentence and paragraph structure

### Sentence

- Goal: 12-18 words per sentence on average
- Max: 25 words (otherwise the speaker runs out of breath)
- Min: 5 words (for effect — sparingly)
- Vary so it doesn't become mechanical

### Paragraph

- One paragraph = one cohesive idea
- Between paragraphs there's a natural breathing pause (~1-1.5 sec)
- Paragraphs can be 2-5 sentences
- No paragraph longer than ~80 words

### Breathing pauses

Mark with `// pause //` if the script needs explicit timing. Otherwise rely on sentence ends and paragraph breaks.

## Anti-patterns for read-aloud

| Avoid | Why | Instead |
|-------|-----|---------|
| Connector chains ("which means... that leads to...") | Loses listener | Break into multiple sentences |
| Embedded clauses with commas | Hard to read aloud | Reformulate |
| Long names/quotes without pause | Trips up the speaker | Brief pause before, "as [quote]" |
| Number stacks | Wrong without rhythm | One number at a time |
| Acronyms | Must be spelled or sounded out | Spell out the first time |

## Structure patterns by length

### 1-2 minutes (short interview, short video)

```
OPENING (10 sec): hook + position
CORE (60-90 sec): one main point + one concrete example
CLOSING (10-20 sec): what this means, or call to action
```

### 3-5 minutes (short talk, podcast segment)

```
OPENING (20-30 sec): scene or question
PROBLEM (60-90 sec): what's at stake
ANALYSIS (90-120 sec): 2-3 points with examples
CLOSING (30-60 sec): tying together, call to action
```

### 10+ minutes (lecture, long video)

Break into three acts of 3-4 minutes each. Each act has its own mini-structure. Transitions between acts should be audible: "That brings us to part two...".

## Tone — adapt to format

| Format | Tone |
|--------|------|
| YouTube/podcast | Conversational, "I", direct to listener |
| Lecture | More formal but personal voice preserved |
| Voiceover (factual) | Clear, concise, less "I" |
| Voiceover (story) | Present, scenic |

## Style preferences (general)

- Personal voice ("I", "we", "my experience is")
- Concretisation: names, dates, numbers, place
- Scenic openings where appropriate
- End with action, not summary
- Short sentences for effect at central points
- No em-dashes (also here)
- No subheadings (the script is one continuous text)

## Output format

Deliver the script as:

1. **Heading:** "Script: [title] (~X minutes, ~Y words)"
2. **Script text:** continuous prose, no markdown beyond paragraph breaks
3. **Word count at the end:** "[Final: Z words, reads ~T minutes at normal speed]"

No headings in the script body. No bullets. No code blocks.

## Workflow

1. Ask (if not specified): target time? Format (YouTube/lecture/voiceover)? User speaking themselves or someone else?
2. Identify the core message (one sentence).
3. Design structure per target length (see patterns above).
4. Write the first draft with natural speech rhythm.
5. Count words. Adjust to target.
6. Read through silently — does it stumble? Reformulate.
7. Deliver per the output format.

---

🎯 COMPLETED: [SKILL:teleprompter] [reading script for X minutes ready]
🗣️ CUSTOM COMPLETED: [SKILL:teleprompter] [Script ready for prompter]
