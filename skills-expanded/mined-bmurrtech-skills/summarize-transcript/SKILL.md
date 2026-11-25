---
name: summarize-transcript
description: >
  Summarizes an already-provided transcript into retained *signal*: a structured
  Markdown summary for action and later reference. Use when the user pastes or
  points at a meeting, interview, talk, or conversation transcript and wants a
  *core summary*, thematic sections, implications, takeaways, or *stance* on
  proposals/questions/outcomes; when long input needs in-session map-reduce; or
  when they ask to summarize a transcript — not a discovery brief (/discovery)
  or design doc (/design-doc), and not transcription from audio/video.
disable-model-invocation: true
---

# summarize-transcript

Convert spoken material into insight that is usable now and citable later.
Remove noise without losing meaning. Clarify without flattening.

**Leading words:** *signal* · *core summary* · *nuance* · *stance*

**Homes:** emit Markdown in chat by default. Write under `.scratch/` only when
the user names a path or asks to save. Long-input intermediates go under
`.scratch/summarize-transcript/<run-id>/`. Never write into the skill install
tree.

## 1. Intake

Required: the transcript (paste or path). Optional steer if already given — do
not request: area of interest, preferred depth, intended use, probes/proposals/
outcomes to watch, or any free-form emphasis.

Assume the transcript is complete even when informal, repetitive, or
unstructured.

If the user gave steer, read [references/focus.md](references/focus.md) and
build one `FOCUS:` line. Omit *focus* entirely when none was given.

**Done when:** the transcript source is identified; *focus* is either a single
`FOCUS:` line or explicitly absent; no clarifying questions remain queued.

## 2. Assess size

If the source is a file (or large paste), from this skill folder run:

```text
python scripts/assess_size.py <path-or-->
```

Strategy hint is advisory. If one pass will not fit cleanly → read
[references/long-input.md](references/long-input.md) and use map-reduce
(chunk → map → reduce) with the host LLM only. Otherwise continue single-pass.

**Done when:** strategy is named (`direct` or `map-reduce`).

## 3. Extract

1. Name the central idea or tension.
2. List supporting themes (arguments, mental models, patterns, risks,
   implications).
3. Note *stance* probes when user-named or clearly voiced (proposal / question /
   desired outcome + surface vs substance + reframe). Keep soft-yes + reframe as
   one pair.
4. Note material decisions, commitments, action items, and open questions when
   the transcript supports them — owner/due only when explicit.
5. Compress repetition; keep *nuance* and detail that change meaning — prefer
   missing compression over missing key takeaways, *signal*, or reframe pairs.
6. Drop filler, off-topic chatter, hype, and vague motivational language.

Apply *focus* when present; do not invent a focus or probe the user/room did
not give.

**Done when:** central idea + theme list exist; stance pairs and
decision/action/open-question notes recorded when earned; discarded material is
only noise or pure duplicate.

## 4. Emit

Rewrite spoken language into clear written form. Output this shape (depth
follows the transcript's emphasis within each section — do not pad empty
uniform subsections):

### Title

Short H1 that reflects the central idea or tension.

### Overview (*core summary*)

Most important section. Plain language covering:

- what the transcript is fundamentally about
- the problem, opportunity, or shift
- why it matters now

Short paragraphs and bullets as needed. Expand when the transcript has layered
reasoning.

### Thematic sections

Logical sections from the transcript. Each has a clear header; mix bullets and
paragraphs; preserve reasoning, examples, and cause-and-effect.

Typical section kinds (use only what fits): core ideas, mental models,
patterns/loops, risks/tradeoffs, practical implications.

### Implications and applications

Where evidence supports it: what changes in behavior, strategy, or priorities;
what to do more/less/differently; signals of progress or failure. May be woven
into thematic sections when that reads better.

### Key takeaways

The most important insights — concise or expanded to match transcript depth.
Do not drop a key takeaway for brevity.

### Stance / Decisions / Action items / Open questions / Pull quotes /
Timestamped sections / Reference insights / Evidence

Only when they earn a place — read
[references/optional-sections.md](references/optional-sections.md). Omit empty
headings. Emit `### Stance on probes` when *focus* named probes or the room
clearly took positions on proposals/outcomes. Prefer later/final wording when
the room reverses itself; flag unresolved conflict rather than averaging.

**Done when:** Title + *core summary* + thematic sections + Key takeaways are
present; optional sections appear only when earned.

## 5. Exit check

- Required sections present; optional headings omitted when empty
- *Core summary* anchors the document; structure matches transcript emphasis
- No invented claims, decisions, owners, due dates, probes, or numbers
- *Focus* (if any) visibly shaped emphasis
- Stance rows (if any): polite-interest ≠ endorse; reframes explicit; no valence
  collapse
- Material claims that use evidence linking include quote + speaker (+ time when
  present)
- Map-reduce runs: later wording wins on reversals; unresolved conflicts flagged

**Done when:** every check passes; deliver the Markdown and stop.

## Boundaries

- Do not ask follow-up questions; begin with the transcript alone.
- Do not invent claims, decisions, owners, probes, due dates, or numbers absent
  from the transcript. Only include information explicitly in the transcript; do
  not add external knowledge. Leave owner/due null or mark missing when unstated.
- Do not flatten *nuance* for false brevity; retain *signal*, key takeaways, and
  stance reframe pairs over short length.
- Do not emit valence mood scores (pos/neg/neutral time series) or discovery
  quadrant *Sentiment* / P-levels; *stance* is propositional reception only. Hand
  scoring to `/discovery` only if the user asks after this summary.
- Do not emit a discovery *brief* or Gate charter; hand those to `/discovery` or
  `/design-doc` only if the user asks after this summary.
- Do not emit YouTube, tweet/X, LinkedIn, thumbnail, or other marketing/publish
  packages from this skill.
- Do not transcribe audio/video; this skill summarizes an already-provided
  transcript only.
- Never pad with hype, clickbait phrasing, or vague motivational language.
- Never call external LLM APIs or lab backends; use the host session model only.
