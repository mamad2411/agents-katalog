---
name: interview-case-study-writer
description: >
  Transforms interview transcripts, call recordings, and conversation notes into
  publishable case studies and expert-interview articles. USE THIS SKILL whenever the
  user says anything like "write up this interview", "turn this transcript into a case
  study", "practitioner story", "customer story writeup", "expert interview article",
  "case study from this call", "interview writeup", "turn this call into a blog post",
  "customer success story", or shares a transcript, call notes, or Q&A and wants a
  publishable narrative out of it. Also fires when drafting interview questions ahead
  of a call that will later become a writeup. Works for any domain — engineering,
  healthcare, finance, education — not just tech. For industry/vertical
  case-pattern briefs with no interview transcript, use the sibling
  platform-industry-brief skill.
---

# Interview Case Study Writer

## Purpose

Turn raw interview material (transcripts, call recordings, Q&A notes) into one of two
publishable forms: an expert-interview feature or a company case study. The method is
domain-agnostic: it extracts a defensible narrative from what a real person actually
said, anchors it in numbers, and keeps a bright line between what the source claims
and what is verified.

Default publication context: [publication or team name]. House style reference:
[style guide location, or "none — use the defaults in this skill"].

Related skills: use `research-brief-writer` when the source material is reports and
documents rather than a conversation; feed finished case patterns into
`platform-industry-brief`, whose vertical library consumes them.

## Core model

### Two output archetypes

Pick ONE per piece. If the material supports both, ask which the user wants — or
produce the feature and note that a case study is also extractable.

#### Archetype A — Expert-interview feature

The subject is the argument. The piece exists because this person believes something
specific, earned that belief, and can teach it.

Template:
1. Hook — a contrarian claim or data paradox, stated with numbers, in the first two
   sentences. Not "we talked to an expert about X" but "X% of teams claim A, yet only
   Y% can show B" or the expert's most defensible provocative claim.
2. Main insights — 3-5 bold, single-sentence takeaways, right after the hook, so a
   skimmer gets the whole argument in fifteen seconds.
3. Who the expert is and why they're credible — one paragraph. Role, scale of what
   they've run ("leads an 800-person org", "managed infra for tens of millions of
   concurrent users"), and the specific experience that earns the claim.
4. The core argument unpacked — 3-6 themed sections (each an H1/H2), one idea per
   section, alternating the expert's voice with your framing.
5. The expert's playbook — the reusable steps, framework, or checklist extracted from
   the conversation, written so a reader in a different company could run it.
6. Tension handled — the strongest counterpoint or limitation, raised and answered
   (or honestly left open). A piece with no tension reads as advertising.
7. Key takeaways — 3-5 action-phrased bullets. Each pairs a directive with the reason
   ("Measure before you optimize: without data on where time goes, you can't...").

#### Archetype B — Company case study

The change is the argument. The piece exists because an organization went from state
A to state B and the path is transferable.

Template:
1. Context — scale, stack/domain, and the binding constraint, with numbers ("deploys
   took 2-3 weeks", "petabytes of data, millions of requests per second").
2. Trigger event — the moment that forced action: an incident, a market shift, a
   number someone finally measured, a leadership change.
3. Approach — the concrete decisions, in order, including the road not taken and why.
   Decisions, not adjectives: "centralized build pipelines while extending team
   ownership", not "embraced modern practices".
4. Outcome — before/after numbers side by side ("1-2 deploys per month → 120,000+",
   "80-90% maintenance load → 40%"). If there are no numbers, say so explicitly and
   lean on described observable change.
5. Transferable lessons — what generalizes, stated for a reader in a different
   industry, and what was situational to this company.
6. What didn't work — at least one genuine failure, dead end, or cost. This section
   is mandatory; it is where the credibility lives.

### Quote craft

- Quote for voice, claims, and color. Paraphrase for mechanics, background, and
  anything the reader needs stated more efficiently than the speaker said it.
- One quote per point, maximum. A strong quote earns its place; three quotes making
  the same point weaken all of them.
- Never stitch fragments from different moments into one quote, and never reorder
  words in a way that shifts meaning. Trimming with ellipses is fine only when the
  cut doesn't change what was claimed.
- Every quote must be traceable to a location in the transcript (timestamp or line).
  Keep a quote ledger during drafting: quote → transcript location.
- Clean up disfluencies ("um", false starts, "right?") but preserve the speaker's
  register — a blunt speaker should still sound blunt, a careful one careful.
- Choose 1-2 pull-quote candidates: short, self-contained, provocative lines that
  survive out of context.

### Evidence discipline

- Separate three tiers in your notes: (1) independently verifiable facts, (2) the
  subject's claims about their own org, (3) the subject's opinions/predictions. Tier
  2 gets attribution in the text ("according to [subject]", "the team reports");
  tier 3 is framed as their view, never as fact.
- Numbers recalled from memory during a conversation are flagged as such until
  confirmed ("roughly 60%, by his recollection"). Never silently promote a
  remembered number to a measured one.
- Ask-the-source checklist — run before drafting, send gaps back as questions:
  - Baseline: what was the number BEFORE, measured how?
  - Timeframe: over what period did the change happen?
  - Team size and scope: how many people, how much of the org?
  - Denominator: percentage of what, exactly? Counted how?
  - Attribution: what else changed at the same time that could explain the result?
- Anonymization (when the subject requires it): keep role and scale ("a platform
  lead at a 2,000-engineer European retailer"), drop names and identifiers, and
  soften details that fingerprint (a unique product, an exact uncommon metric, a
  dated public incident). Default anonymity policy: [named / anonymized / ask].

### Narrative devices

- Paradox hook: two of the subject's (or a dataset's) own numbers that can't both be
  comfortable — "30% say they don't measure, yet only 24% admit not knowing if
  metrics improved." The gap IS the story.
- Before/after ledger: a tight pair or table of old-state vs new-state numbers,
  placed at the moment the reader needs to feel the size of the change.
- "The moment it broke" scene: one concrete, time-stamped incident told in a few
  sentences of narrative — the launch that overwhelmed the forecast, the meeting
  where the measurement came back 80-90%.
- Playbook box: the subject's method as a numbered, reusable list, visually separate
  from the narrative so practitioners can screenshot it.
- Analogy adoption: if the subject offered a strong analogy, build a section around
  it rather than burying it in a quote.

### Interviewing so the writeup writes itself

When this skill is invoked BEFORE the interview, supply a question arc that surfaces
the template beats in order:
1. Baseline — "Walk me through how X worked before. What did it cost you?" (get a
   number.)
2. Trigger — "What made this urgent? Was there a specific moment?"
3. Approach — "What did you actually do first? What did you decide NOT to do?"
4. Outcome — "What changed, and how do you know? What would the before/after numbers
   be?"
5. Numbers audit — re-ask any number: measured or estimated? over what period?
6. Regrets — "What didn't work? What would you do differently?" (never skip; this
   feeds the mandatory failure section.)
7. Quotable close — "What do you believe about this that most of your peers don't?"

## Workflow

1. Intake. Collect: the transcript/notes; consent status and anonymity level; target
   archetype (A or B); audience and venue; desired length (default 1,200-1,800
   words). If consent to publish is unconfirmed, flag it now, not at delivery.
2. Extraction pass. Read the full transcript once. Tag: every claim (with tier),
   every number (with "measured/estimated/unknown"), every quote candidate (with
   location), and the arc beats (baseline / trigger / approach / outcome / regret).
3. Verification pass. Run the ask-the-source checklist against the tags. Produce two
   lists: facts you can check independently (check them) and gaps only the source
   can fill (send them back as a short question list before or during drafting).
4. Draft per the chosen archetype template. Hook first — if you can't write the hook,
   you haven't found the story; go back to the tags and look for the paradox or the
   biggest before/after gap.
5. Quote audit. For each quote in the draft: verify it against the transcript ledger,
   confirm trimming didn't shift meaning, confirm register survived cleanup, and
   confirm no point carries more than one quote.
6. Subject review round. Send the draft to the interviewee for accuracy and quote
   approval. Their corrections to facts and their own quotes are accepted; requests
   to delete the failure section or inflate numbers are negotiated, not silently
   applied.
7. Deliver. Final piece plus a short editor's note listing: anonymity level applied,
   any numbers still flagged as source-recalled, and open verification gaps.

## Guardrails

- No fabricated, composite, or "reconstructed" quotes. Ever. If the transcript
  doesn't contain it, the subject didn't say it.
- No unflagged memory-numbers. Every figure is either verified, attributed as the
  subject's report, or explicitly marked as an estimate.
- Consent before publication: confirmed consent and a completed subject review round
  are prerequisites for any named piece. Named case studies additionally require the
  subject's (and where applicable their employer's) explicit approval.
- Disclose relationships: if the publisher has a vendor, sponsorship, or commercial
  relationship with the subject or their company, say so in the piece.
- Don't sand off failures. The dead ends and regrets carry the transferable lesson;
  a case study with no "what didn't work" section is marketing and should be labeled
  as such.
- Anonymization promises are absolute: once anonymity is agreed, no detail that
  fingerprints the subject survives to the draft, even if it weakens the story.

## Suggested effort

- Extraction and verification are where the time goes: budget roughly 40% tagging
  and checking, 40% drafting, 20% quote audit and revision.
- Standard feature or case study from a 45-60 minute transcript: a focused session
  with one clarifying-questions round back to the source.
- Skip the verification round only for internal, non-published summaries — and say
  in the deliverable that claims are unverified.
- Reasoning effort: medium-high. The judgment calls (claim tiering, quote trimming,
  what fingerprints an anonymous subject) matter more than prose speed.
