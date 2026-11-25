---
name: persuasive-technical-writing
audience: specialist
description: "Use when drafting or revising long-form persuasive technical prose (an essay, post-mortem, launch narrative, or public technical release for X or the web) where the writing must sound human and hold a reader to the end. Do not use for code documentation, changelogs, or short social copy."
---

# Persuasive Technical Writing

Turn raw technical findings into human-sounding, high-retention long-form prose. The rules below are ordered by impact against six failure symptoms; each priority names the symptom it fixes, so jump to your problem. Every rule is mechanically checkable: where a rule states a number, that number is the test a reviewer or a later pass runs with a grep or a count.

## How to use
Run two passes, never one. Pass 1 builds structure and argument: Priority 2 (cohesion), Priority 3 (section titles), Priority 5 (analogies). Pass 2 is a mechanical prose linter over the countable rules: Priority 1 (cadence and blacklist), Priority 4 (quotes), Priority 6 (bolding and hook). Do not lint before the argument holds, and do not ship before the lint passes.

## Priority 1: Human cadence and anti-AI rhythm (fixes "does not sound human")
- Rule 1.1 (Gary Provost burstiness rule): Never write three consecutive sentences of similar length (within ±3 words). In every 200-word block, enforce at least one short punch sentence (<7 words) and at least one rhythmic compound sentence (>25 words).
- Rule 1.2 (hard lexical blacklist): Strictly ban the Kobak et al. excess words. Zero instances permitted. Grep the draft for each token:
  ```
  delve, tapestry, testament, beacon, pivotal, intricate, realm, underscores,
  harnessing, multifaceted, interplay, moreover, furthermore, in conclusion, at its core
  ```
- Rule 1.3 (de-symmetrization): Ban symmetrical parallelism (`not only X, but also Y`; `from X to Y and beyond`). Break formulaic 3-part bullet lists into continuous narrative paragraphs.
- Rule 1.4 (Williams character-action rule): Express characters as grammatical subjects and core actions as active verbs. Ban empty openings (`There is`, `There are`, `It is important that`) and strip nominalizations ending in `-tion`, `-ment`, `-ance`.

## Priority 2: Cohesion and information pacing (fixes "hard to stay with")
- Rule 2.1 (Williams given-before-new): The first 6-8 words of every sentence must connect semantically to a concept established in the immediate prior sentence. Place novel, complex, or heavy technical terms strictly at the end of the sentence (the stress position).
- Rule 2.2 (mobile paragraph ceiling): On mobile and X viewports, cap paragraphs at 1-3 sentences (maximum 40-60 words). Never stack two 3-sentence paragraphs; alternate with 1-sentence pivot paragraphs.
- Rule 2.3 (Minto problem-first flow): Introduce technical solutions only after establishing the Situation and Complication. Maintain forward causal momentum; every paragraph must answer the question raised by the preceding one.

## Priority 3: Argumentative section titling (fixes "section titles unclear")
- Rule 3.1 (headline-as-conclusion): Every H2 and H3 header must be a complete, active assertion stating the causal finding of that section. Strictly forbid descriptive noun labels (`Background`, `Architecture`, `Considerations`, `Analysis`).
- Rule 3.2 (the standalone skim test): A reader reading only the H1 and H2s in sequence must be able to understand the complete logical deduction of the essay without reading the body text.

## Priority 4: Quotation integration (fixes "quotes do not flow")
- Rule 4.1 (the 3-part quotation sandwich): Never drop an orphan quote. Every quotation must follow:
  1. Lead-in claim: state what the quoted speaker demonstrates.
  2. Direct quote: ruthlessly trimmed to the decisive 10-25 words.
  3. Operational translation: state what this quote means for our thesis.
- Rule 4.2 (quotation length ceiling): Inline quotations must not exceed 25 words. If an excerpt exceeds 25 words, either trim it with ellipses or pull it out into a distinct visual asset or screenshot.

## Priority 5: Analogy construction and boundary protocol (fixes "no analogies")
- Rule 5.1 (mandatory physical base): Every complex abstraction (cryptographic primitive, concurrency model, distributed consensus) must map to a concrete physical system.
- Rule 5.2 (Glynn's boundary declaration): Every analogy must explicitly state where it breaks down using the exact syntactic formula:
  > This functions like [Base] because [Relational Mapping]. However, the analogy breaks down at [Boundary Condition] because [Target Divergence].
- Rule 5.3 (domain lock): Lock one analogical domain per section. Never mix metaphors (for example, do not combine hydraulic plumbing with aviation engines).

## Priority 6: Visual hierarchy and bolding discipline (fixes "emphasis not landing")
- Rule 6.1 (the 10% bolding ceiling): Bold text must not exceed 10% of total words in any section. Never bold entire sentences or paragraphs.
- Rule 6.2 (semantic anchor bolding): Bold only the decisive operative noun or the quantitative metric that an F-pattern skimmer needs to find. Never bold rhetorical flourishes or adverbs.
- Rule 6.3 (the 280-character hook formula): The first 280 characters before the X "Show more" fold must contain:
  1. A concrete, counter-intuitive data point or observed failure.
  2. The high stakes of ignoring it.
  3. An open loop that can only be resolved by clicking "Show more".

## Unverified: do not state these as fact
- X ranking weights are not audited. The only documented figures come from the March 2023 open-source release of `twitter/the-algorithm` (relative scores such as reply-with-author-reply ~150x, reply ~27x, retweet ~20x, bookmark ~11x, like 1x). Current production ("Phoenix") weights and dwell-time thresholds are practitioner estimates, not fact. The 280-character fold in Rule 6.3 is a verifiable UI boundary; the ranking rationale behind it is an estimate. Never cite a 2026 weight as audited.
- High burstiness (Rule 1.1) is necessary for lively prose but not sufficient for clarity. Adversarial synonym insertion can raise burstiness scores without improving readability, so treat the linter as a floor, not a certificate of quality.

## Acceptance
- Cadence: no run of three same-length sentences (within ±3 words); every 200-word block has a <7-word sentence and a >25-word sentence; grep returns zero blacklist tokens.
- Cohesion: every sentence opens on given information; every paragraph on mobile is 1-3 sentences and inside 40-60 words.
- Titling: the H1-plus-H2 skim alone reproduces the argument; no noun-label headers remain.
- Quotes: no orphan quotes; every quote is sandwiched and 25 words or fewer.
- Analogies: every complex abstraction has one physical base and one explicit breakdown sentence in the exact formula; one analogical domain per section.
- Emphasis: bolded words are 10% or less per section and mark only operative nouns or metrics; the first 280 characters carry a data point, the stakes, and an open loop.
- No unverified X weight is stated as fact.
