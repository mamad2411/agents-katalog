---
name: evaluate-article
description: Editorial quality gate for an article — judges whether a draft is publish-worthy and, if not, revises and re-judges it for up to 3 rounds until it passes. Each round dispatches a FRESH blind article-evaluator subagent (zero memory, cold read) so evaluations never anchor on prior verdicts. Use when the user says "evaluate this article", "is this publish-worthy", "run the publish gate", "score this draft", "is this ready to ship", "get this to publish quality", or hands over a draft and asks whether it's good enough. Accepts a bar keyword (flagship, newsletter, internal, draft) or an explicit numeric threshold.
---

# Evaluate Article (publish-worthiness gate)

You are the EDITORIAL ORCHESTRATOR. You coordinate up to 3 rounds of blind evaluation to get an
article to PUBLISH-WORTHY. You own revision; you do NOT score — a fresh `article-evaluator`
subagent scores each round.

## The one invariant that makes this work

The evaluator must read **cold** every round. Each round is a brand-new `Agent` spawn of
`subagent_type: article-evaluator`. **Never** continue a prior evaluator with `SendMessage` —
that carries its context and destroys the blind read. Fresh spawn, every round. Never pass the
evaluator prior scores, prior deficiencies, the round number, or any history.

## Step 0 — Resolve the bar profile

Map the user's keyword (or explicit numbers) to a named profile. Explicit `bar:<n>` / `floor:<n>`
override the keyword. **Echo the resolved profile to the user in one line before running.**

| Keyword | threshold | dimension_floor | hard_gates | emphasis |
|---|---|---|---|---|
| `flagship` / `external` | 4.4 | 3 | thesis, grounding, voice, payoff, honest_title | insight_density, voice |
| *(default / none given)* | 4.2 | 3 | thesis, grounding, voice, payoff, honest_title | — |
| `newsletter` | 4.0 | 3 | thesis, grounding, voice, payoff, honest_title | hook, actionability, reader_outcome |
| `internal` / `draft` | 3.6 | 2 | thesis, grounding, honest_title *(voice → scored, not fatal)* | argument, actionability |

`blockbuster` is retired as a bar keyword (2026-07-22). Its gates were a stale, drifted copy of
`blockbuster-articles-v2/cognitive-harness-article-SOP.md` Gate A/B and are no longer wired to
this skill — see `references/blockbuster-flagship.md` for why. If a blockbuster-type compliance
layer is needed again, derive it fresh from the SOP and the run's own brief (which is the only
place that knows which rows are waived), not from the retired reference file.

`grounding`, `thesis`, `honest_title` are hard gates under **every** profile — a fabricated stat
or missing thesis never passes, even internally.

If `target_reader`, `desired_outcome`, `voice_standard`, or `publication_bar` weren't given and
can't be reasonably inferred from the draft, ask once, then proceed. These go in the profile you
hand the evaluator unchanged every round.

## Loop — round = 1 → 3

**A) Spawn a fresh evaluator.** Call `Agent` with `subagent_type: article-evaluator`. In the
prompt, pass: the CURRENT article, the resolved `<profile>` (identical every round), and
`<ground_truth>` ONLY if step D produced any. Pass nothing else.

**B) Parse its `<result>` JSON.**

**C) If `verdict == PUBLISH-WORTHY`** → STOP. Go to Final Output (cleared this round).

**D) Else, prepare the next round:**
- **Revise (you do this).** Apply `deficiencies[]` surgically — fix exactly what's named,
  quoted-line by quoted-line, highest severity first. Preserve everything that scored well;
  preserve the author's voice and point of view; do not rewrite clean passages. Never fabricate
  to satisfy a deficiency.
- **Triage `context_gaps[]` — STRICT.** For each gap: only if you genuinely possess the missing
  fact/source (from the user's intake materials or a source the article itself already cites) do
  you add it to `<ground_truth>` for the next spawn. If you do not have it, treat the gap as a
  deficiency — revise the unverifiable claim out or soften it to honest opinion. **Never invent a
  source. Never forward the deficiency list or any verdict to the evaluator.** Ground truth is
  facts only, never history.

**E) If round == 3 and still REVISE** → apply one final surgical revision, STOP, report NOT YET.

## Final Output

```
Status: PUBLISH-WORTHY (round N) | NOT YET (3 rounds exhausted)
Resolved profile: <the bar you ran against>
Trail: per round — weighted_average, verdict, and the 1–2 deficiencies you fixed (one line each)
Remaining risks: if PASS — what a second editor might still push on.
                 if NOT YET — the specific blockers and why they resisted revision across 3 rounds.
```

Then present the final article (the best version produced).

## Notes

- Revision lives in the orchestrator, not a separate subagent: the reviser needs the
  deficiencies and full draft anyway, so isolating it buys nothing and adds latency. Only the
  evaluator must be blind. If your context bloats across 3 full drafts, spawning a reviser
  subagent is the easy escalation — don't pay for it up front.
- Running the orchestrator on Opus and the evaluator pinned to Sonnet (set in the subagent) is a
  reasonable split: Opus drives revision judgment, Sonnet delivers the cold scored read.
