---
name: planning-report-critique
description: >-
  Find and rank the defects in a planning assessment someone else wrote — an
  officer report, appeal statement or planning statement — for a reader deciding
  whether to act on them. Runs planning-report-quality, then reports only what is
  wrong and matters, ordered by severity, with a verbatim quote for each. Separates
  findings from observations, and treats a true-but-immaterial point as an
  observation rather than a fault. England-focused. Not legal advice; human review
  required.
license: MIT
---

# Planning report critique

Someone has written an assessment and you need to know what is wrong with it — because you
are deciding whether to challenge it, appeal it, respond to it at committee, or send it back.

## Dependencies

- **`planning-report-quality`** — this skill does not re-analyse. It runs that skill and
  reports a filtered, ordered subset of its output.
- `planning-document-search` — for the report itself and the documents it relies on.

Declare these; never copy their content in.

## This skill is a presentation layer

The analysis is entirely `planning-report-quality`'s. What this skill adds is **judgement
about what to raise**, and the discipline to leave the rest out.

That division matters. A defect list built independently of the measurement would drift from
it, and you would end up maintaining two definitions of "defect". Here there is one: a
finding is a claim that failed the accuracy test, or an immaterial consideration given
weight, or a material consideration omitted, or a weight divergence that changes the balance.

## Findings and observations are different things

**A true observation is never a fault in the author.** Identifying something correctly is not
a defect, and whether it is relevant or carries weight is a separate judgement made later and
by someone else.

So the output has two headed sections and they do different work:

| | Contains | Belongs to the reader who |
|---|---|---|
| **Findings** | the reasoning is wrong on the law, or contradicted by the evidence, or omits something material | is deciding whether to act |
| **Observations** | true, possibly worth a sentence, but the decision does not turn on it | wants the full picture |

**Every observation must state, in one line, why it is not a finding.** Without that rule an
assessment relabels wholesale and looks disciplined without having thought. Forcing the
sentence forces the judgement.

## The raise test

A quality-pass result becomes a **finding** only where all three hold:

- it is **wrong**, immaterial-but-weighted, omitted, or mis-weighted — not merely different
  from how you would have put it;
- it bears on something that **could change the outcome**; and
- the author has given **no adequate reason** for the approach taken.

The raise test screens out findings that are too *weak* to record. It does nothing about the
opposite failure, which is the one that costs most here: a finding that is strong, confidently
written and **wrong**. A wrong finding reads exactly like a right one, so it needs its own
gate rather than a closer look at the same evidence:

- **A finding that turns on what a policy says must quote the policy.** Not
  `national-planning-policy`'s summary of it, not a crosswalk — the primary text, read whole.
  This is `planning-report-quality`'s rule at its Step 1; a finding whose "source checked" is
  a summary has not been checked, and does not go in the output.
- **A determinative finding carries the steelman sentence** from the quality pass — the
  strongest reading on which the author is right, and why it fails. No steelman, no finding.

Where a reason is given and it is rational, the point has been addressed rather than ignored.
Record it as an observation. An author who explains why a matter can be conditioned, or why a
survey is required before determination rather than after, has engaged with it — disagreeing
with that judgement is a position to argue, not a defect to report.

Read `references/conventions-not-defects.md` before recording any reasoning defect.

## Severity

Derive it. Do not assign it by feel.

| Severity | Test |
|---|---|
| **A** | Goes to lawfulness or soundness: a statutory test not applied, mitigation relied on but secured by nothing, a material consideration left unassessed, a finding contradicted by the evidence before the decision-maker, **or any incorrect claim the recommendation depends on**. |
| **B** | A substantive weakness: reasoning that does not follow, a consultee position materially altered in transit, a numeric policy requirement never calculated, an objection of substance not engaged with. |
| **C** | An accuracy or drafting defect that does not by itself undermine the decision: a stale policy reference, a template artefact, an internal inconsistency. |

Severity falls out of the quality pass: **accuracy verdict × load-bearing verdict**. An
incorrect determinative claim is an A whatever it is about. A correct-but-mis-weighted
background claim is a C.

## Method

1. **Run `planning-report-quality`** over the report. Do not shortcut it — the ordering
   depends on the load-bearing verdicts, and those come from the full pass.
2. **Apply the raise test** to every non-clean result. Sort into findings and observations.
3. **Derive severity** for each finding from accuracy × load-bearing.
4. **Order findings most serious first.** Within a severity band, order by how much of the
   recommendation rests on the claim.
5. **Write each finding** as: severity · what the report says (verbatim, with document and
   paragraph) · why it is a defect, in two or three sentences · what would cure it.
6. **Write the observations**, each with its one-line reason for not being a finding.
7. **State the coverage** — what was examined, and the denominator from the quality pass.
8. **Check the output against itself before releasing it.** No finding's reasoning may be
   contradicted anywhere else in the same document — most often between the findings and any
   weighting table, summary or advocacy section built from them. Criticising a reading of a
   policy and then relying on that same reading later is a defect this skill would record
   without hesitation if an officer committed it.

## Output format

- **Two-sentence summary.** What the report does well, and the most serious thing wrong with
  it. Both, always: a critique that cannot name a strength has not read carefully.
- **Findings**, numbered, most serious first, in the form at step 5.
- **Observations**, each with its reason for not being a finding.
- **Coverage note** — claims examined, scope, and anything the file could not settle.

Where the answer is that the report is sound, **say so plainly**. "No findings above C" is a
valid and valuable output, and a critique that manufactures findings to look thorough is
worse than useless — it spends the reader's credibility on points that will not survive.

## What "cure it" means

Every finding states what would fix it. This is not padding: it is the test of whether the
finding is real. A defect nobody can articulate a cure for is usually a disagreement about
judgement wearing a defect's clothes.

## Checks

- Every finding carries a verbatim quote with its location.
- Every observation carries its one-line reason for not being a finding.
- No finding rests on a misquotation — check the quote against the source before recording.
- No finding about a policy rests on a summary of that policy. Primary text, quoted.
- No finding's reasoning is contradicted elsewhere in the same document.
- Severity is derived from the quality pass, not assigned independently.
- The conventions reference has been read and applied.
- The summary names a strength as well as the worst defect.
- Nothing is recorded as a defect merely for differing from how you would have written it.

## Stop, or ask

- The evidence base is not complete enough to distinguish "wrong" from "unverifiable" → say
  so and scope the critique; do not report unverifiable claims as errors.
- The document is a committee update or summary rather than the substantive assessment →
  the omissions test will produce false findings. Say which document you have.
- You are being asked to support a predetermined conclusion → the honest output may be that
  the report is sound. Produce that instead.

## Limits

- **Not legal advice, and no warranty.** Whether a defect founds a challenge is for a
  solicitor. This skill locates and characterises.
- **Human review is necessary.** Every quote must be checked against the source.
- **A critique is not a decision.** A report may contain findings and still have reached the
  right outcome.
- **Findings about identifiable people's professional work.** Write about the reasoning, not
  the author. Never impute motive, competence or bad faith, and never name the author.
- **England-focused.**
