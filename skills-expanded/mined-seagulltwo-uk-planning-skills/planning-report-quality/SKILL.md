---
name: planning-report-quality
description: >-
  Measure the quality of a written planning assessment — an officer report,
  delegated report, appeal statement or agent's planning statement — claim by
  claim. Every checkable assertion is tested on four separate axes: is it
  accurate, is it a material planning consideration, what weight is put on it,
  and does the recommendation depend on it. Produces a line-by-line table and
  explainable rates, never a single quality score. England-focused. Not legal
  advice; human review required.
license: MIT
---

# Planning report quality

A planning assessment is an argument built out of assertions. This skill takes it apart one
assertion at a time and asks four questions of each, then reports what it found without
rolling the answers into a grade.

## Dependencies

- `policy-compliance-assessment` and `national-planning-policy` — for what a policy says
  and which framework edition applies.
- `planning-document-search` — for the report itself and the documents it relies on.

Declare these; never copy their content in.

## Standpoint

This skill assesses **whether reasoning holds**, not whether a decision was right.

That is the opposite standpoint from the representation skills in this repo, which produce
the case a party could make. Applied here, an advocate's conclusion is a position to
argue, not a defect in the author's reasoning. The author was not applying that method and is
not bound by it.

A sound report can support a decision you disagree with. Say so when that is what you find.

## When to use

- "Is this officer report any good?"
- "How accurate is this planning statement?"
- "Are there grounds to challenge this decision?" — as the evidence layer beneath that
  question, not as the answer to it.
- Quality assurance across a team's or a consultancy's output.
- Benchmarking one assessment against another, or against a comparator.

Not this skill: finding and ranking defects for someone deciding whether to act — that is
`planning-report-critique`, which consumes this skill's output.

## The four tests, and why these four

Each maps to a way a planning decision actually fails in public law. That is what makes the
numbers explainable to someone who asks where they came from.

| Test | Asks | Public law counterpart |
|---|---|---|
| **Accuracy** | Is the assertion correct? | Material error of fact |
| **Materiality** | Is it a planning consideration at all? | Immaterial consideration taken into account |
| **Weight** | How much is made of it, and is that justified? | Conclusion unsupported by the evidence |
| **Load-bearing** | Does the recommendation depend on it? | — the multiplier on all three |

A fifth check sits outside the claim-by-claim pass:

| **Omissions** | What material consideration was never addressed? | Failure to take a material consideration into account |

**Run the tests in order and do not short-circuit.** An assertion that fails the accuracy
test still gets a materiality verdict, a weight reading and a load-bearing verdict. That is
the only way to find the case that matters most: a wrong claim the recommendation rests on.

## The enumeration rule (read before anything else)

**The denominator is the whole ballgame.** "Claims tested" is itself a judgement, and two
assessors reading the same report will extract different numbers. Where that happens, no rate
is comparable to any other rate, and the output looks precise while meaning nothing.

Enumerate by these rules, and state them in the output:

- **One claim = one assertion that could independently be true or false.** A compound
  sentence splits into its parts.
- **A repetition is one claim.** The same assertion made in two places is a single entry with
  two locations, counted once.
- **Only assertions in the report's own voice.** "The Highway Authority raises no objection"
  is a claim about *what the consultee said* — checkable against the consultation response —
  not a claim that the highway impact is acceptable. Score it as the former.
- **Scope is declared, not assumed.** Default to the whole report including the description
  of development and the consultation summary, because errors in those propagate. Where a
  narrower scope is used, name it in the output and never compare rates across different
  scopes.

## Method

### Step 0 — Classify before testing

Every claim gets a type first, because the accuracy test does not apply to all of them:

| Type | Example | Accuracy testable |
|---|---|---|
| **Fact** | a dimension, a distance, a designation, a date | yes |
| **Policy citation** | "Policy DM3 requires…" | yes |
| **Attributed position** | "The Lead Local Flood Authority objects" | yes |
| **Evaluative judgement** | "the scale would be overbearing" | **no** |

**A judgement cannot be correct or incorrect — only reasoned or unreasoned.** Testing it for
truth is a category error, and it is the single most common way an assessment of an
assessment goes wrong: the reviewer demands proof of something that was never a matter of
proof, and reports the absence as a defect.

Judgements are still recorded. They are tested for whether a reason is given and whether the
reason follows from facts established elsewhere in the report.

### Step 1 — Accuracy

For each checkable claim, one verdict:

- **Correct** — the source bears it out.
- **Incorrect** — the source contradicts it.
- **Misleading** — true as far as it goes, but omits a qualifier that changes the sense.
- **Unverifiable on the file** — nothing in the evidence settles it either way.

Two quotes are required: the claim, and the source that settles it. A verdict without both is
not a finding.

**For a policy citation, the source quote must come from the primary text** — the Framework
itself, the PPG page, the development plan. A skill summary, a crosswalk, a guidance note or
any other secondary source **is not a source of record**, however reliable it usually is. It
is a compression, and a compression can invert the policy it compresses: a summary that
reports the first sentence of a rule and drops the sentence that carves it back will read as
authoritative and say the opposite of the law.

Two consequences, and they are not optional:

- **Open the policy.** Quote the operative words, and read the whole policy rather than the
  sentence that answers your question — sub-paragraphs that qualify, disapply or restore a
  rule routinely sit below the one that states it.
- **Where the primary text was not consulted, the verdict is *unverifiable on the file*, not
  *incorrect*.** An author is not wrong because your summary disagrees with them.

**Unverifiable is a verdict, not a failure of the exercise.** It is also not neutral: an
assertion the file does not support is not before the decision-maker and cannot be checked by
a reader. Count it in the denominator without credit.

### Step 2 — Materiality

Apply the *Newbury* test. A consideration is material where it relates to the development and
use of land, serves a planning purpose rather than an ulterior one, and fairly and reasonably
relates to this development.

- **Material**
- **Immaterial**
- **Material only if** — state the condition.

See `references/materiality.md` for the standard not-material list.

Materiality is independent of accuracy. A false claim can still be about a material matter,
and an immaterial claim given weight is a legal error however true it is.

### Step 3 — Weight

Record two values, not one:

- **Weight asserted** by the report — substantial, significant, moderate, limited, little,
  none, or **not stated**.
- **Weight justified** on the evidence — your own reading.

Flag where a statutory or policy weighting applies and whether the report applied it: s38(6)
development plan primacy, s66 and s72 heritage "considerable importance and weight", the
NPPF presumptions.

The finding is the **divergence**. "Not stated" is itself a common defect — weight carried by
implication rather than explained.

### Step 4 — Load-bearing

Does the recommendation depend on this claim?

- **Determinative** — remove it and the recommendation is in doubt.
- **Contributory** — it supports a conclusion that rests on several things.
- **Background** — context; nothing turns on it.

This is the multiplier. A wrong claim carrying no weight is a blemish. A wrong claim carrying
the refusal is a defect that could unmake the decision.

**Steelman every `incorrect` × `determinative` verdict before recording it.** For each one,
write a single sentence giving the strongest reading on which the author would be *right* —
then say why it fails. Both halves, in the output, next to the verdict.

If you cannot write the second half, the verdict does not get recorded as incorrect. It is
your reading that is in doubt, not the report's.

This is the one place the method is deliberately asymmetric in the author's favour, and the
reason is structural. Every other step in this pass invites you to record a defect; none asks
whether the author might be right. A pass built that way finds defects, including where there
are none, and its false positives all point the same way — at the author. The highest-severity
verdict the method can issue is the one where that costs most, so it is the one that has to
survive a sentence written for the other side.

### Step 5 — Omissions

Work inward from the evidence rather than through the report: read the consultation responses
and representations, list the material considerations raised, and record which the report
never addresses.

Nothing in the text points at what is absent, so this cannot come out of the claim-by-claim
pass. Do it separately or it will not be done.

## Output format

Three parts, in this order.

**1. The line-by-line table.** One row per claim, every claim tested, no sampling.

| # | Claim (verbatim, trimmed) | Location | Type | Accuracy | Source checked | Materiality | Weight asserted | Weight justified | Load-bearing |

**2. The counts.**

| Metric | How it is computed |
|---|---|
| Claims tested | the denominator, with the scope stated |
| Accuracy | correct ÷ checkable |
| **Load-bearing errors** | incorrect **and** determinative — each with its steelman sentence |
| **Claims tested and discharged** | checked against primary source and found correct, listed — particularly any the pass initially suspected and then cleared |
| Immaterial considerations given weight | count, listed |
| Material considerations omitted | count, listed |
| Weight divergences | asserted ≠ justified, listed |

**3. How to read these numbers.** Reproduce this in every output, so the same question gets
the same answer:

> Accuracy is the share of checkable assertions that the evidence bears out. Judgements are
> excluded from it, because a judgement is not the kind of thing that can be correct.
> Unevidenced assertions count against it. **Load-bearing errors are the number that
> matters**: they are the assertions that are both wrong and necessary to the
> recommendation. A report can have a low accuracy rate and no load-bearing errors, and a
> high accuracy rate with one that matters. **Read the discharged count alongside them**:
> a pass that records many load-bearing errors and nothing tested and cleared has probably
> not tested in both directions, and the error list should be treated as things to verify
> rather than as a verdict.

Then the JSON block for downstream processing.

## No composite score

There is deliberately no single quality number.

A composite would recombine exactly what the four tests separate, and the separation is the
point. In source testing, a single precision figure that merged "wrong" with "true but
immaterial" reported a 51% score for work that was 80% accurate — a difference of kind
reported as a difference of degree.

Where one number is wanted for triage, use the **load-bearing error count**. It is a count of
specific quotable things, not an average, and it can be checked by reading six rows.

## Checks

- Every accuracy verdict carries two quotes. No quote, no verdict.
- Every policy-citation verdict quotes the **primary text**. A skill summary or crosswalk as
  the "source checked" is not a verdict — it is an unverified claim.
- Every `incorrect` × `determinative` verdict carries its steelman sentence and the reason
  the steelman fails.
- Every claim has all four axes recorded, including claims that failed accuracy.
- The scope statement appears in the output.
- No evaluative judgement has been given an accuracy verdict.
- The omissions step was run from the evidence, not from the report.
- Where the file cannot settle a claim, the verdict is *unverifiable* — not *incorrect*.

## Stop, or ask

- The adopted development plan cannot be established → stop; policy accuracy is untestable
  without it.
- The evidence base is incomplete, so "unverifiable" cannot be distinguished from "absent
  from the file" → say so and scope the output to what the file supports.
- The report is a summary or committee update rather than the substantive assessment → the
  denominator will not be comparable to a full report. Say which you have.

## Limits

- **Not legal advice, and no warranty.** Whether an error is material in law is for a
  planning professional or a solicitor. This skill locates and characterises; it does not
  advise on challenge.
- **Human review is necessary.** Every quote must be checked against the source before any
  finding is used.
- **England-focused.** The development plan framework and the statutory weightings cited are
  England's.
- **Materiality is a judgement and moves.** In source testing, the same assessor re-scoring
  identical text moved claims between material and immaterial. Accuracy was far more stable.
  Treat accuracy as measurement and materiality as opinion.
- **The denominator is not portable.** Rates from two runs are comparable only where the
  scope statement and the enumeration rules match.
- **A pass designed to find defects will find them, and its false positives cluster against
  the author.** Every step here invites a defect to be recorded; the steelman rule is the
  only one pulling the other way. Read the load-bearing error count as **a list of things to
  verify, not a score** — and treat a run that discharged nothing as a warning about the
  pass rather than a verdict on the report. In use, a pass over a 109-page officer report
  returned three wrong findings and all three ran against the author; each was caught by an
  outside reader with the primary policy text open, not by this skill's own checks.
