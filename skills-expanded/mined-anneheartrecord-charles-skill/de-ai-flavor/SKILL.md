---
name: de-ai-flavor
description: Rewrite Markdown / tweets / long-form posts to strip AI tone and produce real-human writing. Use when the user says "remove AI feel", "polish this", "make it sound more human", "this reads too AI", or any variant. Works on Chinese and English text.
version: 0.1.0
---

# de-ai-flavor

Strip AI tone out of a piece of writing and rewrite it so it sounds like the author actually wrote it.

This skill **does not invent voice**. It needs a personal style profile to rewrite against. The profile lives in a Markdown file the user maintains. The skill reads the profile, then applies a fixed checklist.

## When to use

- User hands over a draft and asks to remove AI tone
- User says: "polish this", "less AI please", "make it sound like me", "rewrite this in my voice"
- After generating any public-facing post / tweet / blog Markdown — run it automatically before finalizing

## When NOT to use

- README files, technical docs, code comments — these can stay formal
- Drafts that don't have full logic yet (write first, de-AI later)
- Code itself

## Setup: the style profile

Before first use, the user must create a personal style profile. Default expected location:

```
~/.claude/projects/<project-slug>/memory/writing_style.md
```

If the file is missing, the skill should ask the user where their style profile lives, or help them bootstrap one from 3–5 of their best existing pieces.

A good style profile defines:

1. Narrative structure (does the author open with a scene? a number? a feeling?)
2. Sentence rhythm (long-short alternation? short sentences as standalone paragraphs?)
3. Tone (self-deprecating? hesitant? colloquial words to keep?)
4. Conclusion style (do they end on a quiet beat or a punchline?)
5. AI markers to ban (transition words, symmetric structures, table summaries, etc.)
6. Forced rewrite actions (concrete steps to apply on every pass)

An example profile lives in `examples/style-profile-example.md`.

## Process

### Step 0: Load the style profile

Open the profile file. Read it fully. Keep it in context for the whole pass.

### Step 1: Diagnose — don't rewrite yet

Read the original draft once. Find every instance of these 6 AI-tone problems and **list them for the user**:

1. **Transition glue**: however, therefore, in conclusion, moreover, furthermore, worth noting that, what's more (然而、因此、综上、不仅、更重要的是)
2. **Symmetric triples**: "not A, but B" repeated, three-item parallel structures stacked
3. **Punchline endings**: every paragraph closes with a polished aphorism
4. **Flat abstraction**: the whole piece floats at concept level, never lands on a specific detail
5. **Structuralist itch**: 1/2/3/4 numbered lists, symmetric subheads, summary tables
6. **Over-stuffed paragraphs**: every sentence delivers value — no hesitation, no self-correction, no breathing room

Output format:

```
[AI-tone diagnosis]
1. Paragraph X — [problem type] — "<original snippet>"
2. ...

N issues found.
```

### Step 2: Apply the 5 forced rewrite actions

These are the core of the skill. Apply each one:

- **A. Open with a concrete scene.** Not "I want to talk about X." Start from a moment — a date, a number, a feeling, a thing that happened.
- **B. Break symmetry.** Any time three or more items line up in parallel, kill at least one. Let the structure be uneven.
- **C. Insert "I"-breaks in every paragraph.** Each paragraph needs hesitation, self-deprecation, contradiction, or revision. If the paragraph reads clean, it reads fake.
- **D. Don't end on a punchline.** The best endings settle, they don't peak. Let the last line be quiet.
- **E. Delete transition words.** Grep the whole draft for the words listed in problem 1. Replace with paragraph breaks.

### Step 3: Check abstract-concrete alternation

The deepest tell of AI writing is **flat abstraction level**. Walk through the rewrite paragraph by paragraph and tag each one "abstract" or "concrete":

- All-abstract paragraph → drop in a detail (number, scene, quote, physical action)
- All-concrete paragraph → pull one feeling up to an idea (but don't punchline it)

Target rhythm: abstract → concrete → abstract → concrete. Never two abstracts in a row.

### Step 4: Output a before/after diff — don't overwrite yet

```
## What changed
(one paragraph: what was done, where the biggest changes are, why)

## Key edits

### Edit 1: Opening
Before: ...
After:  ...
Why:    ...

### Edit 2: ...
...

## Full rewrite
(the complete rewritten draft)
```

### Step 5: Wait for confirmation before writing

Do not overwrite the source file until the user explicitly says "OK" / "apply" / "覆盖" / "confirm".

## Anti-example

```
However, the rise of AI is reshaping content creation.
It's not a tool change — it's a paradigm shift.
We need to rethink three things:
1. The nature of content
2. The role of creators
3. The position of platforms
In conclusion, the future belongs to those who understand both AI and humanity.
```

Hits every problem: however / not A but B / numbered triple / in conclusion / aphorism close / 100% abstract.

## Positive example

```
May 22 was my last day. I had dinner with old colleagues that week. People kept asking why I left. I thought about it for a while and the real answer turned out to be simple:

My sense of self got a little too strong.

It sounds kind of edgy when I say it out loud. But it's the most honest reason I have.
```

Concrete opening (date, dinner, the question), self-deprecation ("edgy"), short sentences, no symmetry.

## Notes

- Emoji-numbered subheads (1️⃣ 2️⃣) **are allowed** if the user's style profile permits them. They're not inherently AI.
- Technical writing (code, API tables, model comparisons) can stay slightly more formal — but skeleton, rhythm, tone must still follow the profile.
- "Sounding human" does not mean rambling. Real ≠ verbose. Cut first, then check.
- Cutting words beats adding words. AI-heavy drafts usually need 20–30% removed to feel right.

## Project layout

```
de-ai-flavor/
├── SKILL.md                          ← you are here
├── README.md                         ← Chinese intro
├── README_EN.md                      ← English intro
├── LICENSE
└── examples/
    ├── style-profile-example.md      ← what a personal style profile looks like
    └── before-after-example.md       ← a real rewrite, showing the full process
```
