---
name: voice-fingerprint
description: >
  Analyze writing samples to extract a user's unique voice and produce a Voice Spec
  stored to memory that Claude applies on all future writing. On first use, immediately
  launches the learning session. When a spec exists and the user is writing something,
  offers to apply it. Includes negative-space analysis (what the user conspicuously
  avoids) and a learning loop that captures corrections/approvals to tighten the spec.
  Trigger on: "learn my voice," "write like me," "match my tone," "voice fingerprint,"
  "capture my style," "that doesn't sound like me," "update my voice spec," or when
  writing samples are uploaded. Do NOT use for ghostwriting without samples or style
  guides not derived from the user's own writing.
---

# Voice Fingerprint

A skill that interviews a user, analyzes their writing samples, and produces a
structured Voice Spec — a reusable constraint set that Claude applies to every
future writing task to match the user's natural voice.

## Overview

The skill operates in four phases:

1. **Analysis Phase** — ingest writing samples, extract patterns (including negative-space
   vocabulary analysis), interview the user about deliberate choices and preferences
2. **Spec Generation Phase** — produce a structured Voice Spec document the user can
   store as a memory edit or preference
3. **Application Phase** — apply the spec as governing constraints on writing tasks
4. **Learning Loop** — capture corrections and approvals, batch them, and propose
   spec revisions that make the voice match tighter over time

The output is NOT a vague "tone guide." It's a concrete, example-rich constraint
document that another instance of Claude can read and apply without guessing.

---

## First-Use Detection

**Before doing anything else**, check whether this user already has a Voice Spec.

Call `memory_user_edits` with `command: "view"` and scan for any line containing
"VOICE SPEC". (See Memory Storage Protocol in Phase 3 for the stored format.)

**If no Voice Spec is found:**
This is a first-time user. Do NOT wait for them to ask. Launch the learning session
immediately with this greeting:

> "You don't have a Voice Spec yet — let me fix that. A Voice Spec is a structured
> document that captures exactly how you write: your sentence rhythms, vocabulary,
> what you avoid, and your rhetorical moves. Once built, I'll use it on every writing
> task so the output sounds like *you*, not like a helpful AI.
>
> To get started, I need 3-8 samples of your writing. The more different they are —
> an email, a blog post, a pitch, a memo — the more accurately I can map your range.
>
> Paste your first sample below, or upload files if you have them. I'll analyze each
> one as you add them and ask follow-up questions after I've seen the full set."

Then proceed directly to Phase 1.

**If a Voice Spec is found:**
The user already has a spec. Proceed based on what they're asking:
- If they said "learn my voice" / "capture my style" / "update my voice spec" →
  go to Phase 1 (new spec) or Phase 4 Learning Loop (spec update)
- If they said "write [something]" or are drafting content → go to Proactive Offer
- If they're providing writing samples → go to Phase 1 Analysis

---

## Proactive Offer (Writing Detection)

When the user makes a request that involves writing something — an email, a post, a
bio, a pitch, a document, a message — AND a Voice Spec already exists in memory,
pause before writing and ask:

> "I have your voice fingerprint on file. Want me to write this as you, not as
> generic Claude?"

Keep it short. One sentence with a yes/no implicit. If they say yes (or "obviously"
or "always" or anything affirmative), apply the full spec before drafting. If they
say no or ignore it, write normally.

**When to offer:**
- The request uses words like "write," "draft," "compose," "send," "reply," "post,"
  "caption," "pitch," "respond," or any other content-creation verb
- The request is for a complete piece of writing, not a factual answer or analysis

**When NOT to offer:**
- The request is a question, a research task, a code task, or analysis
- The user already said "use my voice" or "write as me" (they've already answered)
- You've already offered in this conversation and they said no

**After repeated affirmatives:** If the user says "yes" to the offer 3+ times in a
row across conversations (or once says "always use my voice"), add a note to their
Voice Spec memory entry: `AUTO-APPLY: yes`. From then on, apply the spec silently
without asking. They can turn it off with "don't use my voice fingerprint."

---

## Phase 1: Analysis

### Step 1: Collect Writing Samples

Ask the user to provide 3-8 writing samples. More is better. Diversity matters more
than volume — a blog post, a pitch email, a social post, and a strategic memo reveal
more than eight blog posts.

If the user uploads files, read them using the appropriate tool (view for text,
pdf-reading skill for PDFs, docx skill for Word docs). If they paste text inline,
work with that.

Ideal sample set covers:
- Different audiences (peers, executives, public, casual)
- Different formats (long-form, short-form, email, social)
- Different registers (persuasive, informational, personal)

If the user provides fewer than 3 samples, work with what you have but note that
the spec will be less reliable. If they provide only 1, flag that the spec will
capture that one mode but may miss range.

### Step 2: Run the Analysis

For each sample, extract and catalog these dimensions:

**Structural Patterns**
- Average sentence length (word count)
- Sentence length variance (do they mix short punchy with long flowing, or stay consistent?)
- Paragraph length tendencies
- Opening patterns (do they start in the scene? throat-clear? ask a question?)
- Closing patterns (strong charge? summary? question? trail off?)
- Transition habits (conjunctions, em-dashes, paragraph breaks, section headers)
- Use of lists vs. prose for enumeration

**Vocabulary & Register**
- Latinate vs. Anglo-Saxon lean (utilize vs. use, demonstrate vs. show)
- Jargon comfort level and how they handle it (define inline? assume knowledge? mock it?)
- Formality spectrum position
- Industry-specific vocabulary clusters
- Filler/hedge word frequency (just, really, actually, I think, perhaps)
- Profanity comfort level and style

**Negative-Space Vocabulary Analysis**

This is where the real signal lives. Cross-reference the user's vocabulary against
common cliché pools for their domain. A marketing executive who never once writes
"synergy," "leverage," "robust," or "holistic" across 5 samples is making a choice.

Run the samples against these cliché families and flag conspicuous absences:
- Business/consulting: leverage, synergy, robust, holistic, optimize, scalable,
  innovative, disrupt, stakeholder, alignment, bandwidth, circle back, deep dive
- Marketing: unleash, unlock, game-changer, cutting-edge, best-in-class, turnkey,
  thought leader, content is king, move the needle
- Tech: utilize, facilitate, implement, solution, ecosystem, seamless, frictionless,
  end-to-end, paradigm
- General filler: it's worth noting, at the end of the day, that said, moving forward,
  in terms of, the fact that, basically, literally, honestly, genuinely
- Hedge/softener: I think, I feel like, perhaps, maybe, sort of, kind of, arguably,
  it seems like, just

Present absences to the user grouped by family:
"Your samples never use any word from the consulting register — no 'leverage,'
'synergy,' 'optimize,' 'robust.' Is that a deliberate kill list or just instinct?"

The answer matters because one banned word implies a family. If they hate "leverage"
as a verb, they probably also hate "utilize," "optimize," and "incentivize." Probe
for the *reason* behind the ban — the reason reveals the adjacent bans:
- "It sounds like consulting jargon" → ban the whole register
- "It's a dead metaphor" → ban dead metaphors specifically
- "It's imprecise" → ban vague action verbs, keep precise ones

**Rhetorical Moves**
- Argument structure (claim-evidence, narrative-then-point, question-then-answer)
- Use of analogy and metaphor (frequent? rare? what domains do they draw from?)
- Humor type (dry, self-deprecating, absurdist, observational, none)
- Direct address patterns (you/we/one/passive)
- Authority positioning (expert, peer, student, outsider-looking-in)

**Mechanical Preferences**
- Oxford comma (yes/no/inconsistent)
- Em-dash usage (frequency, purpose — parenthetical, pivot, dramatic pause)
- Semicolon usage
- Exclamation mark frequency
- Ellipsis usage
- Parenthetical asides
- Capitalization habits (sentence case? title case? stylistic caps?)
- Quotation style (single vs. double, British vs. American conventions)

**Voice Signature**
- What makes this writer recognizable in 2 sentences?
- What would a parody of this writer exaggerate?
- What do they NEVER do?

### Step 3: Present the Analysis

Show the user a summary of what you found. Organize by dimension. Use specific
examples from their samples — quote short phrases (under 10 words) to illustrate
patterns. This is where the user sees whether you understood them.

Frame it as: "Here's what I'm hearing in your voice. Tell me where I'm right,
where I'm wrong, and what I'm missing."

---

## Phase 2: Interview

After presenting the analysis, ask targeted questions. These are the things samples
alone can't reveal — deliberate choices, aspirations, and constraints.

### Core Interview Questions

Ask these in conversational batches of 2-3, not as a wall of questions. Adapt based
on what the analysis already revealed.

**Deliberate Choices**
1. Present the Negative-Space Analysis first (see Phase 1). Then ask:
   "I noticed your writing avoids [specific cliché family]. Is that a conscious ban
   or just instinct? And if it's a ban — what's the reason? The reason helps me
   catch words you haven't thought to ban yet but would hate if I used them."
   - For each confirmed ban, probe: "What about [adjacent word from same family]?"
   - Distinguish hard bans (never, period) from soft avoidances (only when earned)
2. "Do you have go-to sentence structures you reach for when the writing matters most?"
3. "When you re-read your own writing and think 'that's good,' what specifically makes it good?"

**Localization**
4. "British English, American English, or a hybrid? Any specific conventions?"
   - Probe: -ise/-ize, -our/-or, single/double quotes, date formats, spelling specifics
   - If hybrid: which conventions from which?

**Randomization & Variance**
5. "Good writing has controlled randomness — predictable enough to feel like you, unpredictable
   enough to stay alive. Where do you want variance?"
   - Sentence length (always short? mostly short with occasional long?)
   - Paragraph rhythm (consistent or jazz-like?)
   - Humor frequency (every piece? only when earned? never forced?)
   - Rule-breaking (when do you break your own rules on purpose?)

**Audience Adaptation**
6. "How much does your voice change by audience? Do you have distinct modes, or is it
   always recognizably you with minor adjustments?"
   - If distinct modes: name them and describe the shift

**Aspirational vs. Actual**
7. "Is there a gap between how you write now and how you want to write?
   Any writers you'd like to echo without copying?"

**The Anti-Voice**
8. "Describe writing that makes you cringe. What specific things trigger it?"

### Optional Deep-Dive Questions

Use if the user is engaged and wants to go deeper: how they handle technical content
for non-technical audiences, their relationship with jargon, whether they outline
or discover, how they plan their close, and which of their own sentences they love
and why.

---

## Phase 3: Generate the Voice Spec

Combine the analysis and interview into a structured Voice Spec. The spec must be:

1. **Concrete** — every rule has an example
2. **Actionable** — Claude can apply it without judgment calls
3. **Prioritized** — the 5 most important traits are flagged
4. **Bounded** — includes anti-patterns (what NOT to do)

### Voice Spec Template

Use this structure. Adapt section depth based on what the analysis revealed.

```markdown
# Voice Spec: [User's Name or "Me"]

## Identity Line
[One sentence that captures the voice. Written AS the user, not about them.]

## The Five Signature Traits
[Ranked. These are the non-negotiables — if you get nothing else right, get these right.]

1. [Trait] — [Example from their writing]
2. [Trait] — [Example]
3. [Trait] — [Example]
4. [Trait] — [Example]
5. [Trait] — [Example]

## Structural Patterns
- Sentence length: [range, with distribution note]
- Paragraph length: [tendency]
- Opening move: [pattern]
- Closing move: [pattern]
- Transitions: [habits]

## Vocabulary & Register
- Default register: [position on formality spectrum]
- Jargon handling: [approach]
- Latinate vs. Anglo-Saxon: [lean]
- Hedge words: [policy]
- Profanity: [comfort and style]

## Rhetorical Moves
- Argument structure: [pattern]
- Analogy/metaphor: [frequency and source domains]
- Humor: [type, frequency, placement]
- Authority position: [default stance]
- Direct address: [preference]

## Mechanics
- English variant: [British/American/hybrid with specifics]
- Oxford comma: [yes/no]
- Em-dash: [usage pattern]
- Other punctuation notes: [specifics]
- Capitalization: [convention]

## Audience Modes
[If the user has distinct modes, list them with the key shifts]

## Controlled Variance
[Where to introduce randomness and how much]

## Banned List

### Hard Bans (never use, no exceptions)
[Words, phrases, and structures that violate the voice. Include the reason —
the reason is what catches adjacent violations the list doesn't name.]

| Word/Phrase | Reason | Family |
|---|---|---|
| [example] | [why it's banned] | [what register/pattern it belongs to] |

### Soft Avoidances (use only when no better option exists)
[Words that aren't wrong but weaken the voice. Acceptable in quoted speech,
technical contexts, or when the precise meaning is needed.]

### Structural Bans
[Sentence patterns, opening moves, closing moves, or organizational habits to avoid.
Example: "Never open with a rhetorical question." "Never end with a summary of what
was just said."]

### The Cliché Families
[Group related bans by the underlying reason. When one word from a family appears
in a draft, check the whole family.]
- [Family name]: [list] — Banned because: [reason]

## Anti-Patterns
[What this voice is NOT. Common mistakes a mimic would make.]

## Example Rewrites
[Take 2-3 generic sentences and rewrite them in this voice, showing the transformation]

## Settings
- AUTO-APPLY: [yes/no — whether to silently apply the spec on all writing tasks]

## Version History
- v1.0 — [date] — Initial spec from [N] writing samples
```

### Delivery

After generating the spec:

1. Present it to the user for review
2. Ask: "Read through this. What's wrong? What's missing? What did I nail?"
3. Iterate based on feedback
4. Once approved, save it:
   - Always save as a downloadable markdown file (full verbose spec with examples)
   - Always push a compact version to memory via `memory_user_edits` (see Memory
     Storage Protocol below)
   - The file is the reference document; memory is the working constraint set

### Memory Storage Protocol

The full Voice Spec is too verbose for memory. Compress it into a compact format
that preserves every actionable rule while stripping explanatory prose. The memory
edit should be a single entry that Claude can parse and apply without the full file.

**Step 1: Check existing memory edits.**
Call `memory_user_edits` with `command: "view"` to see current edits. Look for any
existing Voice Spec entry. If one exists, you'll replace it (not add a duplicate).

**Step 2: Serialize the spec.**
Use this compact format — flat, scannable, no markdown rendering needed:

```
VOICE SPEC v[N] — [User's Name] — [date]
IDENTITY: [one-sentence identity line]
AUTO-APPLY: [yes/no]
SIGNATURE TRAITS: 1) [trait] 2) [trait] 3) [trait] 4) [trait] 5) [trait]
STRUCTURE: sentences [range] words, paragraphs [tendency], opens with [pattern], closes with [pattern]
REGISTER: [formality position], [Anglo-Saxon/Latinate lean], [jargon handling]
RHETORIC: [argument structure], humor=[type/frequency], authority=[stance], address=[pattern]
MECHANICS: [English variant], Oxford comma=[y/n], em-dash=[usage], [other notable conventions]
AUDIENCE MODES: [mode1]=[key shifts] | [mode2]=[key shifts]
VARIANCE: [where randomness goes and how much]
HARD BANS: [comma-separated list with family groupings in parens]
SOFT AVOIDS: [comma-separated list]
STRUCTURAL BANS: [list]
ANTI-PATTERNS: [what this voice is NOT — common mimic mistakes]
```

This format typically runs 800-2,000 characters. Well within the 100K limit per edit.

**Step 3: Store it.**
- If no existing Voice Spec entry: `command: "add"`, `control: [serialized spec]`
- If existing Voice Spec entry found: `command: "replace"`, `line_number: [N]`,
  `replacement: [serialized spec]`

**Step 4: Confirm to the user.** Tell them the spec is stored and will apply to all
future conversations. Remind them they can say "update my voice spec" or "that
doesn't sound like me" to trigger the Learning Loop. Tell them they can say
"always use my voice" to skip the per-task offer going forward.

### Memory Revision Protocol

When the Learning Loop triggers a spec revision (see Phase 4):

1. Call `memory_user_edits` with `command: "view"` to find the current Voice Spec entry
   and its line number
2. Re-serialize the updated spec with the new version number
3. Call `memory_user_edits` with `command: "replace"`, `line_number: [N]`,
   `replacement: [updated serialized spec]`
4. Also regenerate and present the full markdown file for the user's records
5. Confirm: "Voice spec updated to v[N]. Changes: [summary of what changed]."

If the Voice Spec entry is missing (user may have cleared memory), offer to
re-store it. Don't assume it's there without checking.

### Applying the Spec

When the Voice Spec exists and the user requests writing, Claude should:

1. Check the AUTO-APPLY flag. If `yes`, apply silently. If `no` or absent, use the
   Proactive Offer above before writing.
2. Read the full spec before writing
3. Apply the Five Signature Traits as primary constraints
4. Use the Banned List as a hard filter on output
5. Match the appropriate Audience Mode if specified
6. Introduce variance per the Controlled Variance section
7. After drafting, self-check against Anti-Patterns

---

## Edge Cases

**User has an existing voice spec or style guide**: Start from their existing doc.
Run the analysis to validate/extend it rather than building from scratch. Flag any
contradictions between the existing spec and what the samples show.

**User wants to create a voice for a brand, not themselves**: The same process works.
Adjust the interview to focus on brand positioning, target audience, and competitive
differentiation rather than personal preference.

**User provides samples in multiple languages**: Build separate specs per language
unless they explicitly want a unified cross-language voice.

**User's samples are inconsistent**: This is information, not a problem. Flag the
inconsistency and ask whether it reflects audience adaptation (intentional) or
voice drift (unintentional). Build the spec around whichever they confirm.

**Updating an existing spec**: When the user comes back with new samples or changed
preferences, don't rebuild from scratch. Diff against the existing spec, show what
changed, and update surgically.

**User declines the Proactive Offer repeatedly**: After 3+ "no" responses to the
offer, stop asking and note in the spec: `AUTO-APPLY: off — user prefers manual
activation`. They can re-enable it by saying "use my voice fingerprint."

---

## Phase 4: Learning Loop

The Voice Spec is a living document. It gets better every time the user corrects
Claude's writing or approves it. This phase defines how corrections and approvals
flow back into the spec.

### Correction Capture

When the user edits Claude's output or says something like "that doesn't sound like me,"
"too formal," "I'd never say it that way," or makes direct edits to a draft:

1. **Identify the violation.** What specific spec rule was broken? If no rule covers it,
   that's a gap in the spec.
2. **Extract the pattern.** Don't just log the single instance. Generalize:
   - "You changed 'utilize' to 'use'" → Is "utilize" already banned? If not, add it.
     Check the cliché family — should the whole Latinate-verb register be banned?
   - "You deleted the opening question" → Is there a structural rule about openings?
     If not, add one: "Never open with a rhetorical question."
   - "You shortened every sentence in paragraph 3" → Does the spec's sentence-length
     guidance match what the user actually wants? Tighten the range.
3. **Classify the correction.**
   - **New rule**: The spec didn't cover this. Add it to the appropriate section.
   - **Rule refinement**: The spec had a rule but it was too loose. Tighten it with
     the new example.
   - **Rule contradiction**: The correction conflicts with an existing rule. Flag it
     to the user: "Your edit here breaks the pattern I have in the spec. Which one
     wins?" Update based on their answer.
4. **Propose the spec update.** Show the user the specific change:
   "Based on your edit, I'd add this to the Banned List: [word] — Reason: [why].
   And I'd update the Sentence Length guidance from [old] to [new]. Sound right?"
5. **Apply only after confirmation.** Never silently update the spec.

### Approval Capture

When the user approves writing ("that's perfect," "nailed it," "yes, exactly"),
the positive signal is equally valuable:

1. **Identify what worked.** Which spec rules produced the result? Were any rules
   bent or broken in a way that worked?
2. **Strengthen the pattern.** If a rule was applied and the result was praised,
   that rule gets a confidence boost. If the same rule gets praised 3+ times, consider
   promoting it to the Five Signature Traits if it isn't already there.
3. **Capture the example.** The approved output becomes a reference example in the spec.
   Replace weaker examples with stronger ones as they accumulate.

### Spec Versioning

The Voice Spec carries a version number and changelog:

```markdown
## Version History
- v1.0 — [date] — Initial spec from [N] writing samples
- v1.1 — [date] — Added "synergy" family to Hard Bans (user correction)
- v1.2 — [date] — Tightened sentence length to 8-15 words default (3 corrections)
- v1.3 — [date] — Promoted "pivot structure" to Signature Trait #2 (4 approvals)
- v1.4 — [date] — Set AUTO-APPLY: yes (user preference)
```

### When to Trigger a Revision

Don't update the spec after every single correction. Batch changes and propose a
revision when any of these thresholds are met:

- **3+ corrections** in the same dimension (e.g., three vocabulary corrections)
- **A contradiction** between a correction and an existing rule
- **A new audience mode** emerges that the spec doesn't cover
- **The user explicitly asks** to update their voice spec
- **New writing samples** are provided that show evolution from the original spec

### Revision Protocol

1. Show the current spec version
2. List all pending changes with their source (which correction or approval triggered them)
3. Show a diff: what's being added, removed, or modified
4. Get user confirmation
5. Increment the version number
6. Update the stored spec (memory edit and/or file)

### Integration with Memory

The Learning Loop and memory storage work together:

1. **Corrections accumulate in-conversation.** During a single conversation, track
   corrections as they happen. Don't call `memory_user_edits` after every correction —
   that's noisy and the user hasn't confirmed anything yet.

2. **Revision threshold triggers memory update.** When corrections hit the threshold
   (3+ in same dimension, contradiction, or user request), follow the Revision Protocol
   above, then follow the Memory Revision Protocol (in Phase 3, Delivery section) to
   push the update to persistent memory.

3. **Cross-conversation continuity.** Because the serialized spec lives in memory,
   the next conversation starts with the latest version. If the user says "that
   doesn't sound like me" in a new conversation, Claude can read the spec from
   memory, identify what went wrong, and propose a targeted update.

4. **Pending corrections that don't hit threshold.** If the user makes 1-2 corrections
   that don't trigger a full revision, note them in conversation but don't push to
   memory. If the conversation ends with pending corrections, ask: "I have [N]
   pending voice corrections that haven't hit the revision threshold yet. Want me
   to update the spec now, or wait until more accumulate?"

5. **Manual sync.** If the user says "sync my voice spec" or "push my voice updates,"
   run the Memory Revision Protocol regardless of threshold.
