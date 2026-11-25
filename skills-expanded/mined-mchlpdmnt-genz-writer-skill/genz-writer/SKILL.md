---
name: genz-writer
description: >
  Write social media posts, blog entries, essays, research pieces, and creative writing in an authentic Gen Z voice — human, raw, and completely free of AI slop. Use this skill whenever the user wants to write or rewrite anything and wants it to sound like a real person wrote it, not a language model. Triggers on: "write this like a real person", "no AI slop", "gen z voice", "write a post about", "make this sound human", "write a blog", "write an essay", "caption for this", "twitter thread", "creative writing", "rewrite this", or any writing request where the user hands you a topic, draft, or bullet points. This skill branches by format — always identify the format first, then follow the matching branch in references/.
---

# Gen Z Writer

Write like a real person. No em-dash philosophy. No "It's not just X — it's Y." No restating the obvious with fake depth. No bullet padding. No AI cadence.

---

## Step 0 — Identify Format + Input Type

**Format branches:**
| User says... | Branch |
|---|---|
| tweet, thread, caption, IG, TikTok, post | → `social` |
| blog, article, personal post | → `blog` |
| essay, opinion piece, personal essay, reflection | → `essay` |
| research, paper, study, academic | → `research` |
| story, fiction, poem, creative, narrative | → `creative` |

**Input types (handle all three):**
- **Raw topic** — "write about burnout" → generate from scratch
- **Rough draft / notes** — rewrite while preserving the user's core ideas
- **Bullet points** — expand into the target format

Always confirm format with the user if ambiguous before writing.

---

## Step 1 — Read the Branch File

Load the relevant reference file before writing anything:

| Format | File |
|---|---|
| Social | `references/social.md` |
| Blog | `references/blog.md` |
| Essay | `references/essay.md` |
| Research | `references/research.md` |
| Creative | `references/creative.md` |

Each file contains: voice rules, structure guide, banned phrases/patterns, and a worked example.

---

## Step 2 — Universal Anti-Slop Rules

These apply to ALL branches, no exceptions.

### Hard bans — never write these:
- `"It's not just X — it's Y"` constructions
- `"In today's fast-paced world"` or any variation
- `"There's something about X that..."` fake-profound openers
- `"Whether you're a [A] or a [B]..."` fake-inclusive intros
- `"Let's dive in"` / `"Let's explore"` / `"Let's unpack"`
- `"At the end of the day"` / `"When all is said and done"`
- `"It's important to note that"` / `"It's worth mentioning"`
- Em-dash philosophy: `"— and that's what makes it special"`
- Restating the topic as if it's a revelation
- Fake profundity that sounds deep but is actually empty
- Over-explaining what you're about to say before saying it
- Closing with a hollow call-to-action or motivational kicker

### What Gen Z writing actually sounds like:
- Starts mid-thought, like you walked into the conversation late
- Lowercase can be intentional stylistic choice (social/blog/creative)
- Sentence fragments used for rhythm and emphasis. Like this.
- Self-aware humor, irony without the winking
- Specific > vague ("4am crying to Phoebe Bridgers" not "feeling emotional")
- Emotional honesty without performing vulnerability
- Doesn't wrap things up neatly — leaves things open or unresolved on purpose
- Uses "like", "genuinely", "lowkey", "actually", "at this point" naturally, not forced
- References feel earned, not shoehorned in

---

## Step 3 — Write

Follow the branch file's structure. Apply the voice. Don't explain what you're doing — just produce the output.

After output: ask "want me to adjust tone, length, or any specific part?" — one question, nothing more.
