---
name: uxswe-evaluate
description: Review a built interface and return located defects, each paired with a proposed repair and a severity. Use when asked to review, critique, audit, or QA a UI, to find usability or accessibility problems, to check whether a screen is ready to ship, or when someone asks "what's wrong with this page" or "is this good UX". For building rather than reviewing, use uxswe-build.
---

# uxswe-evaluate

Critique that a developer can act on. Every finding names a location, states the
user impact, and carries a repair. A finding without a repair is an opinion —
do not report it.

## The rule that makes this worth running

**Inspect the states before reporting.** Do not critique from source code alone
or a single screenshot. Feedback, validation, recovery, and responsive failures
only appear after action. If you cannot run or render the artifact, say so
explicitly and label the review static — a static review is legitimate but must
not be presented as a full one.

At minimum reach: the success state, one error state, the empty state, and the
narrowest supported viewport.

## Dimensions

Assess across these seven. They come from UXBench's critique rubric, which is
the validated structure for this kind of report.

| Dimension | The question |
|---|---|
| Goal-state clarity | Can the user tell what this screen is for and whether they succeeded? |
| Navigation scent | Do links and controls predict where they lead? |
| Action feedback | Does every action visibly acknowledge itself? |
| Flow efficiency | How much effort stands between intent and outcome? |
| Error recovery | After a failure, can the user understand and fix it? |
| Trust transparency | Are cost, permissions, data use, and consequences legible before commitment? |
| Scanability and accessibility | Can the content be scanned, and operated by assistive technology? |

Load `references/evaluation-dimensions.md` for the anchors that separate a
strong result from a weak one on each.

## Triage order

Where to look first, ordered by observed frequency in front-end defect studies
rather than by intuition — **alignment** defects dominate at 42.2%, then
**crowding** 18.7%, **occlusion** 18.1%, **overflow** 11.4%, **color and
contrast** 6.6%, **text overlap** 3.0%.

Then the two failures that recur hardest in assistant and interface studies:

- **Error recovery.** Treat this as the likeliest weak point in anything you
  review. The best model measured in UXBench managed effective recovery in 12.8%
  of cases, and apology-without-fix outnumbered actual correction more than
  tenfold. Assume recovery is broken until you have seen it work.
- **Task incompleteness.** The path that starts well and does not finish.

## Reference material

Load only what the review needs — these are detailed and cost context.

| File | Load when |
|---|---|
| `references/evaluation-dimensions.md` | scoring or describing any of the seven dimensions |
| `references/defect-taxonomy.md` | you need the full catalogue of recurring defects |
| `references/error-recovery.md` | assessing error states, messages, undo, or correction |
| `references/safeguards.md` | accessibility, trust, permissions, or user-control checks |

## Reporting a finding

Each finding carries all six. Anything missing makes it unactionable:

1. **Location** — file and line, or the screen and element
2. **Observed state** — what you did and what happened, not what you infer
3. **User impact** — who is blocked or slowed, and how
4. **Severity** — blocking · major · minor
5. **Repair** — the specific change, bounded enough to apply
6. **Confidence** — say when you are unsure rather than flattening it

Order the report by severity. Group by dimension only if there are enough
findings that severity ordering becomes unreadable.

## Safeguards are reported separately

Accessibility, trust transparency, and user control are **not averaged into any
overall assessment**. A testable standard exists for accessibility — report
conformance or pass/fail against it, and never let strong visual design offset a
keyboard trap, a missing label, or an unlabelled status message.

Load `references/safeguards.md` for the checks. State the standard you applied.

## Do not

- **Do not produce a score as the headline.** A profile across dimensions tells
  the reader where to work; a single number does not, and invites false
  precision this method cannot support.
- **Do not report visual similarity to a mockup as a UX finding.** It is an
  artifact metric. A pixel-faithful screen can be unusable.
- **Do not pad the report.** Ten real findings beat forty with thirty guesses in
  them. If the interface is good, say it is good and report the few things worth
  fixing.
- **Do not claim certainty about perceived speed or aesthetics** from inspection
  alone. Those need users.
