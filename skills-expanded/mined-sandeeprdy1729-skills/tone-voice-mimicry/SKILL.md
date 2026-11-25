---
name: tone-voice-mimicry
description: >
  Target voice and style mimicry skill. Copies any external writing style —
  a brand, a publication, a public figure, a competitor, a historical author,
  a content style guide — from provided samples. Different from voice-auth, which
  authenticates the user's own voice. This skill copies any target voice the user
  points at: write like Paul Graham, match The Economist's tone, copy our competitor's
  blog style, write in the style of Y Combinator rejection emails.
  Extracts structural, tonal, lexical, and rhetorical fingerprints from examples.
  Generates new content that is stylistically indistinguishable from the target
  while carrying the user's intended message.
  Use when user says: write like X, match this style, copy this tone, write in
  the style of, mimic this, sound like our competitor, write like this publication,
  match this brand voice, copy this author, adapt our content to their format,
  style transfer, sound like a YC partner, write in the style of Stripe's docs.
  Do NOT activate for: the user's own voice (use voice-auth instead), harmful
  impersonation of real individuals for deception, deep fake content.
  First response: "Voice Mimicry active. Paste 2–3 samples of the target voice.
  I'll extract the style fingerprint before writing anything."
license: Apache 2.0
---

# Tone & Voice Mimicry

"Write in the style of Paul Graham" produces something that sounds vaguely
essay-like. That's not mimicry — that's pattern-matching to a stereotype.

Real style mimicry requires extracting the structural signature of the target:
sentence length variance, paragraph rhythm, how claims are introduced, how
evidence is deployed, which words appear and which are absent, how uncertainty
is expressed, where the writer breaks convention deliberately. This skill
extracts that fingerprint and then uses it as a constraint on new content.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/fingerprint` | Extract and display the style fingerprint from provided samples |
| `/write <topic>` | Write new content on a topic using the stored fingerprint |
| `/adapt <content>` | Rewrite existing content to match the target style |
| `/contrast <style-a> <style-b>` | Compare two style fingerprints — where do they diverge? |
| `/dial <dimension> <direction>` | Adjust one style dimension: more formal, shorter sentences, etc. |
| `/score <text>` | Score a piece of text for stylistic match to the stored fingerprint |
| `/blend <weight-a> <weight-b>` | Blend two styles with specified weights |
| `/extract-vocab` | List the vocabulary signature: words the style uses, avoids, and overuses |
| `/structure` | Show the structural signature: paragraph length, argument pattern, transitions |
| `/calibrate <feedback>` | Adjust the fingerprint based on feedback |
| `/reset` | Clear the stored fingerprint |

---

## HIGH-LEVEL WORKFLOW

```text
User provides target style samples
    │
    ├─ Phase 1: Style Fingerprinting
    │     Extract structural, lexical, tonal, and rhetorical patterns
    │
    ├─ Phase 2: Fingerprint Output
    │     Present the fingerprint for user validation
    │
    ├─ Phase 3: Content Generation
    │     Write new content constrained to the fingerprint
    │
    ├─ Phase 4: Self-Scoring
    │     Score the output against the fingerprint
    │
    └─ Phase 5: Calibration Loop
          Adjust fingerprint or output based on feedback
```

---

## PHASE 1 — STYLE FINGERPRINTING

A style fingerprint is the set of structural habits that persist across everything
the writer produces. It is not vocabulary — anyone can copy words. It is the
architecture of how meaning is built.

### Fingerprint dimensions

**1. Sentence architecture**
- Average sentence length (short ≤12 words / medium 13–25 / long 26+)
- Sentence length variance (uniform vs. highly variable)
- Opening patterns: how does the writer start sentences? (inverted, declarative, question, fragment)
- Punctuation patterns: em dash, semicolons, parentheticals, fragments

**2. Paragraph structure**
- Average paragraph length (by sentence count)
- Opening sentence function: claim, scene-setting, question, data, anecdote
- Closing sentence function: conclusion, implication, pivot, cliffhanger, callback
- Internal structure: does the paragraph build to a point or start with the point?

**3. Argument pattern**
- Claim-then-support vs. support-then-claim
- Use of counterargument: does the writer steelman opposition or ignore it?
- Evidence style: data-heavy, anecdote-heavy, logical-heavy, authority citation
- How uncertainty is handled: confident, hedged, explicit about limits

**4. Tonal signature**
- Formality level (1 = casual/conversational, 5 = formal/academic)
- Warmth: does the writer address the reader directly?
- Authority posture: does the writer assert or inquire?
- Irony/wit: absent, subtle, explicit
- Emotion: clinical vs. emotionally engaged

**5. Vocabulary signature**
- Characteristic words and phrases the writer returns to
- Words conspicuously absent (never uses jargon / never uses contractions / etc.)
- Complexity level: Flesch–Kincaid grade estimate
- Field-specific vocabulary density

**6. Rhetorical devices**
- Repetition / anaphora
- Contrast and juxtaposition
- Triads (lists of three)
- Rhetorical questions
- Concrete-then-abstract or abstract-then-concrete movement

### Fingerprint output format

```text
STYLE FINGERPRINT: [target name / description]
Samples analyzed: [N]

SENTENCE ARCHITECTURE
  Avg length:      [short / medium / long]
  Length variance: [uniform / moderate / high]
  Opening pattern: [description with example]
  Punctuation:     [notable patterns]

PARAGRAPH STRUCTURE
  Avg length:      [N sentences]
  Opening move:    [claim / scene / question / data / anecdote]
  Internal build:  [point-first / build-to-point / both]

ARGUMENT PATTERN
  Structure:       [claim-first / evidence-first / interleaved]
  Counterargument: [ignores / acknowledges / steelmans]
  Evidence style:  [data / anecdote / logic / authority]
  Uncertainty:     [suppressed / hedged / explicit]

TONAL SIGNATURE
  Formality:       [1–5]
  Reader address:  [direct / indirect / absent]
  Authority:       [assertive / questioning / advisory]
  Wit:             [absent / subtle / explicit]

VOCABULARY
  Characteristic:  [list of recurring words/phrases]
  Conspicuously absent: [contractions / jargon / passive voice / etc.]
  Reading level:   [grade estimate]

RHETORICAL DEVICES
  [list devices found with examples]

DEFINING HABIT
  [1–2 sentences: the single most distinctive thing about this voice —
  the thing that, if you got it right, makes everything else secondary]
```

---

## PHASE 2 — CONTENT GENERATION

When generating content using the fingerprint:

### Generation rules

1. **Match the defining habit first.** If the fingerprint's defining habit is "starts every argument with a concrete scene before abstracting," do that first. Get the macro structure right before the vocabulary.

2. **Sentence length variance is not optional.** If the target varies between 5-word punches and 40-word flowing sentences, the output must too. Uniform medium sentences are a dead giveaway.

3. **Respect conspicuous absences.** If the target never uses contractions, never use contractions. If the target never cites sources by name, don't do it.

4. **Opening sentences are load-bearing.** The first sentence of every paragraph is where style is most visible. Match the opening pattern exactly.

5. **Do not over-apply vocabulary.** Characteristic words appear 2–4 times in 1000 words, not every sentence. Overuse turns mimicry into parody.

6. **Match the argument structure.** If the target makes the claim last, put the claim last even when it's unnatural for the content.

### Self-scoring after generation

After generating, score the output:

```text
MIMICRY SCORE: [X]/10

Sentence architecture:  [match / partial / miss]  — [note]
Paragraph structure:    [match / partial / miss]  — [note]
Argument pattern:       [match / partial / miss]  — [note]
Tonal signature:        [match / partial / miss]  — [note]
Vocabulary:             [match / partial / miss]  — [note]
Defining habit:         [match / partial / miss]  — [note]

Biggest divergence: [what most clearly doesn't sound like the target]
Fix: [what to change in the next revision]
```

Score below 7: revise before delivering.

---

## PHASE 3 — STYLE DIMENSIONS AND DIALS

When the user calls `/dial`, adjust a single dimension without changing others.

| Dimension | Dial down | Dial up |
| --- | --- | --- |
| Formality | More contractions, shorter sentences, first person | Remove contractions, longer sentences, third person |
| Sentence length | Break long sentences; add fragments | Merge short sentences; subordinate clauses |
| Confidence | Add qualifiers; soften claims | Remove hedges; state claims flat |
| Warmth | Remove "you", less direct address | Add "you", direct address, questions to reader |
| Concreteness | More abstraction, fewer examples | More examples, data points, scenes |
| Complexity | Simpler vocabulary, shorter paragraphs | Technical vocabulary, longer paragraphs |
| Wit | Remove irony, play it straight | Add contrast, juxtaposition, deliberate understatement |
