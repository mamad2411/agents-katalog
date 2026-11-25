---
name: research-evaluator
description: >
  Measure whether a finished research article is actually supported by the sources it cites.
  Extracts every load-bearing claim, resolves each to the citation it leans on, and grades the
  claim against what that source really says — producing a grounding rate, an unsupported-claim
  list, source coverage, and the run's cost. Use this skill whenever the user says "check my
  article," "is this grounded," "did we hallucinate," "evaluate the research," "grade this
  draft," "run the eval," "how good is this report," "check the claims against the sources,"
  or asks whether a written piece is defensible before it goes out. Also trigger before
  publishing anything produced by content-writer or research-writer, and when a reviewer
  challenges a specific claim's sourcing.
version: 0.1.0
---

# Research Evaluator

`citation-verifier` answers "does this source exist?" This skill answers the harder question: "does the sentence that cites it actually follow from it?"

Those are different failures. A citation can resolve perfectly at CrossRef and still be doing no work — attached to a sentence it doesn't support, stretched past what the abstract claims, or borrowed from a paper about an adjacent topic. That's the failure mode that survives every check we currently run, and it's the one that gets caught in public.

Concept-ported from the hallucination and accuracy eval suites in [gpt-researcher](https://github.com/assafelovic/gpt-researcher) (Assaf Elovic, Apache-2.0). The idea of scoring a generated report against its own retrieved sources, and of recording cost and latency alongside quality, is theirs. The claim-level grading rubric, the model-diverse judging, and the read-only-reporter posture are ours. No code copied.

## Posture: reporter, never rewriter

This skill reports. It does not fix the article, does not rewrite claims, and does not drop citations. Every finding goes to the human with the claim, the source, and the reason — the human decides whether to soften the claim, find a better source, or cut it.

That is not timidity. An evaluator that edits is grading its own work on the next pass, and the grade stops meaning anything. It also crosses the HITL line in `feedback_hitl_queue_no_batch_writes` — a claim-level accept/override surface is a human-decision queue, and Claude does not resolve those in bulk.

## Inputs

- The article — a markdown draft, a published file, or the `content-writer` / `research-writer` output for the run.
- Its bibliography, and the library the citations came from (Supabase `citations` for a research-pipeline run, or the `.bib` for an academic-pipeline run).
- Optional: a focus — a section, a claim, or a specific citation the user is worried about. A focused pass is much cheaper than a full one and is the right default when someone is challenging one claim.

If the article cites sources that aren't in any library, say so and evaluate them by fetching the source directly. Uncited-library mismatch is itself a finding.

## Step 1: Extract load-bearing claims

Walk the article and pull every claim that carries argumentative weight. A claim is load-bearing if the argument changes when it's false.

Take: factual assertions, statistics and figures, causal statements, characterizations of what a source found or argued, statements about the state of a field, and predictions attributed to someone.

Skip: the author's own opinions and framing, transitions, definitions of common terms, and anything explicitly marked as the author's speculation. Grading an opinion against a citation produces noise that buries the real findings.

Record for each claim: the verbatim sentence, its section, and the citation key(s) attached to it or to the sentence immediately preceding it.

## Step 2: Resolve each claim to its evidence

For every claim, pull what the cited source actually says — abstract at minimum, and the full text when it's open access and the claim is specific enough to need it. A numeric claim always needs the real text; abstracts round, drop caveats, and omit the sample size that makes the number mean something.

A claim with no citation anywhere in its vicinity is `UNCITED`. Do not go looking for a source that would support it — that is doing the author's work and it launders an unsourced claim into a sourced one.

## Step 3: Grade

Each claim gets exactly one verdict:

| Verdict | Means |
|---|---|
| `SUPPORTED` | The source states this, or it follows directly. A careful reader checking the citation would be satisfied. |
| `PARTIAL` | Directionally right, overstated in the article. Hedges dropped, scope widened, a correlation written as a cause, a single study written as a consensus. |
| `UNSUPPORTED` | The source does not say this, says something materially different, or is about an adjacent topic. Includes the citation-does-not-mention-it case. |
| `CONTRADICTED` | The source says the opposite. Rare, and always the first thing in the report. |
| `UNCITED` | Load-bearing claim with no citation attached. |
| `UNVERIFIABLE` | The source is paywalled, dead, or too thin to judge, and no substitute is reachable. Report honestly; never guess. |

`PARTIAL` is the verdict that earns this skill its keep. Outright fabrication is rare in a pipeline that discovers before it writes. Quiet overstatement — the hedge dropped, the "suggests" upgraded to "shows" — is common, survives every other check, and is exactly what a hostile reader goes after.

**Judge with a different model than the one that wrote it.** Route the grading through Council's OpenRouter dispatch (`plugins/council/scripts/openrouter_dispatch.py`, key auto-resolved by `openrouter_key.py`) so the grader isn't the author marking its own homework. When OpenRouter is unavailable, grade with a fresh-context sub-agent that gets the claim and the source text and nothing else — no article, no author framing, no knowledge of what the claim is supposed to prove. Context isolation is the cheap approximation of a second model, and the isolation matters more than the model does.

## Step 4: Compute and report

```
Research Eval — "[article title]"
════════════════════════════════════

Grounding rate:      [n]/[total] claims supported  ([pct]%)
  SUPPORTED     [n]
  PARTIAL       [n]     ← overstated; the fixable ones
  UNSUPPORTED   [n]     ← the real problem
  CONTRADICTED  [n]
  UNCITED       [n]
  UNVERIFIABLE  [n]

Source coverage:     [n]/[total] library sources cited at least once ([pct]%)
Citation load:       [n] claims per cited source (mean), max [n] on [source]
Run cost:            $[x] · [n] judge calls · [n]m [n]s wall

Findings, worst first
─────────────────────
1. [CONTRADICTED] §[section] — "[claim verbatim]"
   Cites: [key] — [source title]
   Source says: [what it actually says]
   Fix: [one line]
...
```

Three secondary numbers, because each catches something the grounding rate hides. **Source coverage** below about 60% means the library was built and then ignored, and the article is narrower than the research behind it. **Citation load** concentrated on one or two sources means the piece rests on a couple of papers wearing a bibliography as a costume. **Run cost** exists because an eval nobody can budget for is an eval nobody runs twice.

## Step 5: Hand off

Present the findings and stop. Offer, do not perform:

- Soften the `PARTIAL` claims to what the source supports
- Send the `UNSUPPORTED` and `UNCITED` claims back to `literature-discovery` as targeted queries — those are precisely-specified gaps, the best discovery input there is
- Re-run the eval on a revised draft and show the delta

Write the summary numbers to the library metadata so grounding rate is tracked across drafts. A rate that improves draft over draft is the signal that the pipeline is working; one that doesn't move after a revision means the revision addressed the prose, not the evidence.

## Cost

A full pass is one judge call per load-bearing claim plus source fetches — a 3,000-word article runs 40 to 70 claims, roughly $0.30 to $0.80 through OpenRouter, a few minutes. A focused pass on one section or one contested claim is cents. Declare the estimate before a full run, the same as deep research does.

## Prerequisites

- The article and its bibliography
- **Supabase MCP** for a research-pipeline library, or the `.bib` for an academic-pipeline run
- **`WebFetch`** for retrieving source text
- **OpenRouter key + Council v0.7.0+** for model-diverse judging (falls back to isolated-context sub-agents)
