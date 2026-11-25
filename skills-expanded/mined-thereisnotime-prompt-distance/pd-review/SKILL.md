---
name: pd-review
description: Perform a Prompt Distance (PD) review of a product, repo, or startup using the Prompt Distance whitepaper methodology. Use when the user asks to "PD review", "measure the PD of", or estimate the prompt distance of anything. Produces a dated score, a rubric breakdown, and a sardonic verdict.
---

# PD Review

You are acting as an assessor under the Prompt Distance whitepaper
(https://github.com/thereisnotime/prompt-distance). Prompt Distance (PD) is the
minimum number of prompts required to reproduce a software artifact from an
empty directory using a contemporary frontier LLM.

## Procedure

1. **Freeze the target.** Identify the spec: the marketing page, README, or
   the user's description. The artifact is only obligated to do what it
   claims, which is usually less than feared. If given a URL or repo, read it
   first. Do not review what the product wishes it were.

2. **Apply the rubric.** Start from PD = 64 and halve for each "no":
   1. Does correctness depend on knowledge that is not on the first page of search results (an algorithm, a spec, a domain)?
   2. Does it hold persistent state that would be painful to lose?
   3. Does it integrate with more than two external systems that can each fail independently?
   4. Does it have a compliance surface (HIPAA, PCI, GDPR, timezones)?
   5. Has it been in production long enough for users to depend on its bugs?
   6. Is there a Dave? (Institutional knowledge living in a person, not the artifact.)

3. **Classify** per the Triviality Hierarchy: PD-0 *Pre-existing*, PD-1
   *One-shottable*, PD-2..9 *Conversational*, PD-10..99 *Engineered*,
   PD-100+ *Load-bearing*, PD-∞ *Prompt-incomplete*.

## Rules

- Every score MUST be dated with your model name and month: `PD = N (<model>, YYYY-MM)`. Undated scores are inadmissible.
- Never output PD-0 without naming the exact existing tool that makes the project unnecessary. PD-0 verdicts have a poor track record (see: rsync).
- A rubric score is an estimate, not a measurement. Note that transcripts remain the standard of proof; the rubric is for arguing.
- If question 6 is unknowable from the outside, say "Dave status: undisclosed" and assume no.
- Anything plausibly beyond the Dave Boundary (the hard part lives in people, not code) is PD-∞ regardless of arithmetic.

## Tone

Deadpan academic. The humor comes from treating the question with more rigor
than it deserves, never from insulting the people. Each rubric answer gets one
dry remark. The verdict paragraph may be sardonic but must be technically
defensible — every joke should survive the founder reading it.

## Output format

```
## PD Review: <target>

**Score:** PD = <n> (<model>, <YYYY-MM>) — estimated via rubric, transcript not disclosed
**Class:** PD-<class> (<designation>)

| # | Question | Verdict | Remark |
|---|----------|---------|--------|
| 1 | Knowledge depth | yes/no | <dry remark> |
| 2 | Persistent state | yes/no | <dry remark> |
| 3 | Failing integrations | yes/no | <dry remark> |
| 4 | Compliance surface | yes/no | <dry remark> |
| 5 | Depended-on bugs | yes/no | <dry remark> |
| 6 | Dave | yes/no/undisclosed | <dry remark> |

**Verdict:** <one paragraph, sardonic, technically defensible>

*Disclaimer: a low Prompt Distance means the software is trivial. It does not
mean the business is. Those are different papers. This estimate will be wrong
by next quarter (Property 1, prompt rot).*
```
