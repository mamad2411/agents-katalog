---
name: panel-synthesizer
description: Use this skill to synthesize interview feedback from multiple panelists into a single hire/no-hire recommendation memo. Triggers on phrases like "synthesize panel feedback for [candidate]", "consolidate the interview write-ups", "hire/no-hire memo", or when the user references debrief notes from a panel of 3 or more interviewers. Surfaces the hidden veto and weights specificity over volume.
---

# Hiring Panel Feedback Synthesizer

## When to use this skill

A candidate has been interviewed by a panel of 3 or more people. Each panelist has written their own feedback. The hiring manager needs to synthesize this into a single hire/no-hire recommendation. Done casually, this process favors the loudest panelist and under-weights the quiet skeptic. This skill is calibrated to do it correctly.

## Input the user provides

- Candidate name
- Role they are being considered for
- Panelist write-ups (3 to 7 typical)
- Optionally: the rubric or competencies the panel was supposed to evaluate

## What this skill does

1. Reads each panelist's feedback in full
2. Identifies the collective signal across all panelists
3. Specifically surfaces:
   - Areas of strong agreement (both positive and negative)
   - Areas of disagreement (and which panelists are on each side)
   - The most specific concern raised (often the most important signal, regardless of how loudly it was raised)
   - The hidden veto (a panelist saying "strong overall, but..." is often a soft no, calibrate accordingly)
4. Produces a one-page decision memo in the structure below

## Output structure

```
# Candidate: [Name]
*Role: [role]. Panel size: [n]. Interview dates: [range].*

## Recommended decision
[Hire / No-hire / Conditional hire pending further conversation]

## Confidence in this recommendation
[High / Medium / Low], with one-sentence rationale.

## Where the panel agrees
- [Strength 1, cited by N panelists with specific evidence]
- [Strength 2]
- [Concern 1, if there is consensus on a concern]
- [Concern 2]

## Where the panel disagrees
- [Disagreement 1]: [Panelist A] thinks [X]. [Panelist B] thinks [Y]. The deciding question is [Z].
- [Disagreement 2]: same

## The most specific concern raised
[Quote or close paraphrase of the most specific, evidence-backed concern from any panelist. This is often the signal that matters most regardless of how loudly it was raised.]

## The hidden veto check
- Is any panelist saying "strong but" / "I would not block" / "leaning yes but"? If yes, name them and quote the qualifying phrase.
- What is the actual concern under the polite phrasing?

## What would change this recommendation
2-3 specific things, including any further conversations or work product that would resolve the open questions.
```

## Calibration notes

- Weight specificity over volume. A panelist who provides a concrete example of a concern carries more signal than a panelist who provides three superlatives.
- The "hidden veto" check is the highest-leverage section. Most panels lose good no-hire signals because one polite panelist's qualifying language gets read as a yes. This skill forces explicit acknowledgment of the soft no.
- Quote panelists where useful. Their actual words are better than paraphrase.
- If panelists' write-ups are short or contain no evidence, flag this. "Strong communicator" is not feedback. The skill should note when feedback quality itself is the limiting factor.
- Do not invent agreement that does not exist. If the panel is genuinely split, say so and propose a path to resolve.

## Bias awareness

When synthesizing, flag any of the following if they appear:
- Concerns that are phrased in coded language (e.g., "culture fit" without specifics)
- Strengths attributed only to surface traits (confidence, communication style) without skill evidence
- Disagreement that maps to demographic axes among the panelists

These are not automatic disqualifiers, but they warrant explicit examination in the memo.

## When NOT to use this skill

- Single-interviewer feedback (no panel to synthesize)
- Reference checks (different signal structure)
- Performance reviews of existing employees (different rubric)
