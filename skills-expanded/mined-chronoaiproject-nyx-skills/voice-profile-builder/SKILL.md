---
name: voice-profile-builder
description: "Derive a structured reusable writing-voice profile from supplied sample texts."
metadata:
  category: plain
  tag:
    - "voice"
    - "writing"
    - "style"
version: "0.1"
---


# Voice Profile Builder

You read a writer's **real samples** and distill them into one structured, reusable **VOICE PROFILE** — a compact spec of how this person actually writes. The profile is the deliverable. A later writing step (drafting a post, an email, an essay, a reply) consumes it so the output sounds like the author, not like default AI prose.

This is a pure reasoning task: no external services, no tools, no data fetches. Everything you need is the samples in front of you plus the protocol below. The whole skill is this document.

The core discipline: **every claim in the profile must be earned from the samples.** A voice profile that could describe any competent writer is a failure. Yours must be specific enough that someone reading only the profile could predict how this author would phrase a new sentence — and would recognize an off-voice draft as wrong.


## When to activate

- The user supplies writing samples and wants their voice captured for reuse.
- The user wants future content written "in my voice" / "like this author" and there is real source text to learn from.
- An existing writing lane keeps drifting into generic AI cadence and needs a durable style anchor.
- The user explicitly asks for a style guide, voice spec, or tone profile built from examples.

Do **not** activate to write the final piece — that is the downstream step's job. You produce the profile; you do not ghostwrite from it in the same pass unless the user explicitly asks you to also draft.


## Inputs

**Required — writing samples.** Real text the author actually wrote. Aim for 5–20 representative samples when available; 3 strong ones beat 15 weak ones. More is better only if the extra samples add range, not repetition.

**Optional — guidance.** Anything that steers extraction:
- target medium for downstream use (short social post vs. long essay vs. cold email vs. docs)
- whether to separate a *public/polished* voice from a *private/working* voice when the samples clearly split into both registers
- which samples the author considers most canonical (weight these higher)
- explicit dislikes the author already knows about ("I hate exclamation points", "never use em-dashes")

### Source quality rules

- **Use the strongest real sources, freshest first.** Prefer recent original writing over old; prefer polished published work and outbound that landed over throwaway notes — unless the user says the older or rougher material is more canonical.
- **Never treat generic platform exemplars, template copy, or other people's writing as the author's source.** If a sample was clearly co-written, ghostwritten, or boilerplate, flag it and weight it down or drop it.
- **If samples are thin or low-signal, say so and lower confidence** rather than inventing a richer voice than the evidence supports (see *Quality bars*). Do not pad a sparse profile with plausible-sounding but unevidenced traits.
- **If no usable samples are provided, stop and ask for them.** Do not fabricate a voice from a name alone.


## What to extract (read for these dimensions)

Read the samples specifically hunting for these. Each becomes evidence in the profile. Do not just list adjectives — note *what in the text* shows the trait.

- **Sentence rhythm & length** — short and clipped, long and winding, or deliberately varied? Where do the punches land?
- **Compression vs. explanation** — does the author trust the reader and cut, or spell things out? How much scaffolding per idea?
- **Diction & register** — plain vs. technical, formal vs. casual, jargon density, favored verbs and nouns, words this author reaches for repeatedly.
- **Capitalization & punctuation norms** — sentence case vs. lowercase style, em-dash / parenthetical / colon habits, ellipses, list formatting, emoji or none.
- **Parentheticals & asides** — present or absent, and used for what (qualifying, narrowing, undercutting, joking)?
- **Question use** — frequency and purpose (genuine inquiry, rhetorical setup, or never).
- **Claim sharpness** — how directly are assertions made? Hedged and qualified, or blunt and declarative?
- **Evidence texture** — how often do concrete specifics, mechanisms, numbers, names, or receipts appear vs. abstraction?
- **Transitions & flow** — how do paragraphs and ideas connect — abrupt jumps, earned segues, connective phrases, or white space?
- **Structural habits** — openings (cold-start vs. throat-clearing), closings (button, callback, fade-out), use of lists, headers, one-line paragraphs.
- **Signature moves** — the recognizable things this author does that most writers don't (a recurring rhetorical turn, a cadence, a way of framing).
- **Tells & bans** — what this author **never** does. These are as load-bearing as what they do.


## Output contract — the VOICE PROFILE

Emit exactly one fenced block titled `VOICE PROFILE`, in this structure. Keep it **compact and operational** — short enough to paste into a later writing step's context, dense enough to actually constrain a draft. This is a working spec, not literary criticism.

```
VOICE PROFILE
Subject: <whose voice — name or "the user">  | Sources: <N samples, kind(s), recency>  | Confidence: <high | medium | low + one-line why>
[Registers: <only if the samples split — e.g. "public (polished) vs. working (terse)"; otherwise omit>]

ONE-LINE ESSENCE
<single sentence a stranger could use to recognize this voice>

TONE & STANCE
- <2–5 bullets: attitude, posture toward reader, default emotional register>

DICTION & VOCABULARY
- <favored words/verbs, register, jargon level — name actual words seen in samples>
- <words/registers this author avoids>

SENTENCE RHYTHM
- <length pattern, where punches land, varied vs. uniform — cite the pattern>

STRUCTURE & FLOW
- <openings, closings, paragraphing, transitions, list/header habits>

MECHANICS
- <capitalization, punctuation, em-dash/parenthetical/ellipsis habits, emoji policy>

SIGNATURE MOVES
- <named, the distinctive recurring moves — each tied to a sample>

DO  (write like this)
- <imperative, specific, checkable rules a drafter can follow>
- <…>

DON'T  (off-voice — rewrite if it appears)
- <imperative bans, including this author's specific tells AND the generic-AI tropes below>
- <…>

EVIDENCE  (proof the profile is grounded, not generic)
- "<short verbatim quote from a sample>" → <which trait it demonstrates>
- "<another quote>" → <trait>
- <3–6 of these; each must be a real excerpt from the supplied samples>
```

Rules for the block:
- **Every DO/DON'T is imperative and checkable** — "open cold on the claim, no throat-clearing", not "be engaging".
- **The EVIDENCE section is mandatory and must use real excerpts** from the supplied samples. It is the proof the profile is earned. If you cannot fill it from the samples, your profile is ungrounded — lower confidence and say what's missing.
- **Name specifics, not abstractions.** "Reaches for 'ship', 'leverage', 'concrete'" beats "uses strong vocabulary". "Sentences average ~8 words, occasional 25-word build" beats "varied rhythm".
- Keep registers separate only if the samples genuinely split; otherwise one profile.


## Avoid generic-AI tells (bake these into the DON'T list)

Unless a sample proves the author actually writes this way, the profile's DON'T list must ban the default-AI texture that makes copy sound machine-made. Carry these forward (and add any author-specific tells you find):

- fake-curiosity hooks ("Ever wondered…", "Here's the thing…")
- the "not X — it's Y" / "it's not just X, it's Y" construction
- empty intensifiers and filler ("no fluff", "truly", "at the end of the day", "in today's world")
- forced lowercase or forced Title Case that the samples don't support
- LinkedIn thought-leader cadence and one-line-paragraph drip used as a tic
- bait questions used to manufacture engagement
- "Excited to share", "I'm thrilled to", "Without further ado"
- generic founder-journey / origin-story filler
- corny or throat-clearing parentheticals
- summary closings that restate what was just said ("In conclusion, …")
- hedge stacks ("it's worth noting that it could be argued that…")
- emoji bullets and decorative emoji, unless the samples use them

If a sample *does* prove the author genuinely uses one of these, move it from DON'T to DO and note it — the samples win over this default list.


## Quality bars (self-check before you emit)

- [ ] **Specific, not portable.** The profile could not be lifted onto an unrelated writer. Every section names something concrete.
- [ ] **Evidence-grounded.** The EVIDENCE block is filled with real verbatim excerpts from the supplied samples, each mapped to a trait. No invented quotes.
- [ ] **Predictive.** Reading only the profile, you could draft a new on-voice line and flag an off-voice one. If it can't do that, it's too vague — tighten it.
- [ ] **DO/DON'T are operational.** Imperative and checkable, not vibes. The DON'T list includes both author-specific tells and the generic-AI bans (minus any the samples justify keeping).
- [ ] **Honest confidence.** Thin or conflicting samples → state `Confidence: low/medium` and name the gap; never overclaim a voice the evidence doesn't support.
- [ ] **Compact.** Tight enough to reuse directly in a downstream writing step's context — trim anything that doesn't constrain a draft.


## Handoff to a downstream writing step

This skill ends at the profile. To produce actual copy, a separate writing step takes the emitted `VOICE PROFILE` block as input and drafts against it — treating the DO/DON'T lists as hard constraints and the EVIDENCE as the bar for "does this sound like the author".

When you finish, state plainly that you produced a **profile**, not finished copy, and that a downstream writing step should consume it to draft. If the user explicitly asked you to also write the piece in the same turn, do that *after* emitting the profile, and obey your own profile's DO/DON'T while drafting.
