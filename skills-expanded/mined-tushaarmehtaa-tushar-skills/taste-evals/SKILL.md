---
name: taste-evals
description: Prove a prompt, model or pipeline change makes subjective output better with a held-out set, blind compare and a judge calibrated on real hits and flops. Use when taste decides quality.
license: MIT
---

# Taste evals

Prove that a change makes subjective output better before it ships. Posts, captions, copy, summaries and designs described in text have no answer key. A judge's score means nothing until it has been checked against real outcomes. A win means nothing if the comparison could tell which arm was which.

## Choose a mode

Infer the mode from what the user brings. Ask only if two modes fit equally.

- **Design:** a planned change, no results yet. Return an eval plan with the decision rule written before any run.
- **Run and analyze:** arms to compare, or outputs and scores already in hand. Return a results report.
- **Audit:** an existing eval, judge, scorecard or claim such as "the new prompt wins 70%". Return findings ranked by how much each could change the decision, and say whether the existing verdict survives.

Scope boundaries:

- Live traffic tests with assignment, exposure and conversion belong to the `product-experiments` skill. This skill decides which candidate is worth exposing to users.
- Correctness, format adherence, refusal, latency and cost evals belong to the `ai-product-development` skill. This skill covers the outputs where a person's taste decides what is good.
- Factual accuracy of a generated claim is checked against sources, not judged for taste. A tripwire can flag a claim; it cannot verify one.

Inspect before asking. Read the generator, its prompts, retrieval and memory, any existing eval scripts and results, logs of user picks (post, copy, edit, star, keep, kill), and published outcomes with engagement. Ask only about what changes the design:

- what counts as a real hit, when no recorded outcome exists in the data;
- who the human tiebreaker is;
- the spend ceiling for judge calls, when a full run would be expensive.

## Rules

Each rule exists because breaking it produces a confident wrong answer.

1. **Freeze the set and the context.** Write a manifest before generating: the inputs, each arm's exact system prompt and user message per slot, retrieval results, few-shot examples, model and settings, seeds, and the judge's rubric and anchors in a fixed, seeded order. Retries replay the frozen prompts. Store the judging context with the scores. If context differs between arms or between runs, the comparison measures the drift.
2. **Hold out.** Eval items never appear as few-shot examples, retrieval candidates, judge anchors or memory, for the generator or the judge. Enforce it with ID exclusion in code, not intention. When an arm must reproduce a real held-out item, brief it with a neutral one-line topic that carries none of the original's wording, structure or punchline.
3. **Keep failures in the denominator.** A failed, empty or truncated generation scores as the worst outcome for its arm. Never drop it. Keep every failed candidate, every rejected draft and the judge's stated reasons; they are the analysis material.
4. **Blind and randomize position.** Opaque labels. Position shuffled per input with a stable seed, so reruns match but no arm owns a column. Arm names never appear in the judge prompt or on a review page. Run every pairwise judgment in both orders. A verdict that flips with order is a tie. Report the flip rate.
5. **Calibrate the judge before its score is used.** Test it on labelled real outcomes: known hits and flops, or a person's real picks among candidates. Report AUC with an interval for scores, agreement against chance with a Wilson interval for picks, and kill recall with kappa for keep or kill. Calibrate in the form the eval uses: a pairwise judge on hit-versus-flop pairs, a pick judge on real pick sessions. Compare to a bar written before the calibration run. Below the bar, the judge is not used. AUC well below 0.5 means the judge is inverted. Report that as a finding, change the design (often absolute to pairwise) and recalibrate. Do not flip the sign and ship it. Every rubric revision scored on the same calibration set spends it: iterate on a development split and confirm the final judge once on a split it has never seen.
6. **Prefer pairwise against a real reference.** "Which of these two did the author write" or "which would you post", with the nearest real example as the rival, beats "rate this 1 to 10". A pairwise discrimination score has a fixed meaning: 0.5 is indistinguishable from real. Absolute scores drift with the rubric and reward polish. When the held-out set is real inputs with no real output to compare against, judge arm against arm, pairwise.
7. **Use an independent judge.** Pick a model family different from the generator and from any critic inside the generation loop. Models favor their own outputs. If the loop's critic is also the eval judge, the eval measures how well the loop learned to please its critic.
8. **Tripwires for hard rules.** Deterministic code, per arm, no model: length, banned phrases, em dashes, hashtags, repeated openers within a batch, named templates, invented numbers, and invented first-person claims (any claim about the author's life or work not supported by the input or the author's real record). Add distribution fit: the rate of each feature in the outputs against the base rate in the real corpus. Tripwires catch what judges forgive and explain why a judge prefers what it prefers.
9. **Pre-register the decision rule and the sample size.** Before any generation or judge call: the primary metric, the arms, n, the judge's calibration bar, the win bar, and the action for a win, a loss and a null. Commit it, or record its hash and timestamp, before the first call.
10. **No re-scoring after seeing results.** Do not swap the judge, rubric, anchors, exclusions or thresholds because of which arm they favor. A judge change is legitimate only when calibration motivated it and it is applied to every arm's saved samples. Report the old and new scores side by side.
11. **Human blind review is the tiebreak.** Use it when the judge fails calibration, when the result sits inside its interval, or when judge and tripwires disagree. The decider sees one shuffled deck of single cards with arms mixed and the key kept outside the page. Any prefix of a shuffled deck is a fair sample, so a partial review still counts. Blind human picks outrank the judge.
12. **Report the effect with its uncertainty.** The input is the unit: when an arm writes several drafts per input, reduce them to one verdict per input before counting. Wins, losses and ties per input, win rate on decisive pairs with a Wilson 95% interval, an exact sign test, and what this n can resolve. When the interval spans no difference, write "the eval cannot resolve this", give the n that would, and label any decision made on other grounds as unmeasured.

## Restraint

- Never fabricate hit or flop labels, and never derive them from a model's opinion. Labels come from recorded outcomes: engagement in a fixed window, a person's posts, copies, edits, keeps or kills, an editor's accepts. If none exist, say the judge cannot be calibrated, run blind human review, and mark any judge result "uncalibrated, directional only".
- Check labels by hand before calibrating. Trace three to five labelled items to the real published artifact. Logging bugs, such as recording a card's screen position while storing drafts by planned slot, mislabel silently.
- Small samples get directional language: "leans toward", "no evidence of a difference". Never "the same", "proven" or "significantly better" from an underpowered test.
- Do not optimize to the judge. A generator tuned against the eval judge will win the eval. Keep the eval judge out of the loop, and watch tripwires and human picks for divergence from the judge.
- A change may ship on mechanism (cheaper, simpler, more principled) after a null result. Record it as "not a measured win".
- A run that dies partway, for example on an exhausted API balance, is not interpretable unless the call order was random by design. Log spend per run and stop at the ceiling.
- A judge that agrees with users in general has not been shown to agree with the specific decider. Calibrate on the population whose taste the decision serves, and report other populations as secondary.

## Workflow

### Design

1. Name the change, the decision it serves, and who decides. One change per arm where possible. Hold model and retrieval constant when testing a prompt.
2. Inventory evidence: recorded outcomes usable as labels, real items usable as held-out references, and any existing harness. Decide the held-out shape: real input-output pairs allow pairwise against the real output; real inputs alone allow arm against arm. Extend an existing harness before writing a new one.
3. Size the held-out set from the smallest effect worth acting on. Read [calibration and statistics](references/calibration.md) for the power table. State the smallest win rate this n can detect.
4. Build the calibration set from real outcomes: clear hits and clear flops, the middle band dropped, held-out items and anything in the judge's context excluded. Leave one out when the judge uses few-shot examples from the same pool.
5. Choose arms: the baseline is what production runs today. Add challengers. Include a real-versus-real control when judging discrimination, to see the judge's ceiling.
6. Choose the judge: independent family, pairwise, both orders, rubric and anchors frozen.
7. Write the tripwires and the distribution-fit checks.
8. Write the decision rule, the calibration bar and n. Pre-register them.

### Run and analyze

1. Confirm a committed plan exists. If not, write it now, before looking at any output, and label results already seen as exploratory.
2. Freeze the manifest. Generate every arm. Keep failures.
3. Run tripwires on every arm.
4. Calibrate the judge for this exact rubric, anchors and model. If it misses the bar, stop the judge path and go to blind human review. Do not re-score earlier runs with it.
5. Judge blind, both orders. Record the flip rate and the stated reasons.
6. Analyze with [calibration and statistics](references/calibration.md). Break results down by input category, with each category's n.
7. Send ties, in-interval results and judge-tripwire conflicts to blind human review.
8. Apply the pre-registered rule. Write the decision and what would change it.

### Audit

Check the eval against rules 1 to 12. For each violation, state what it could bias, in which direction, and whether the verdict survives. Common findings:

- the judge was never calibrated, or was calibrated on examples sitting in its own prompt;
- the judge shares a model family with the generator or the in-loop critic;
- held-out items leak into few-shot examples or retrieval;
- failed generations were dropped from the denominator;
- judging ran in one order only;
- anchors were fetched live and unordered, so the rubric drifted between runs;
- a significant verdict from a judge with no demonstrated agreement with the decider;
- a non-significant small effect read as "no difference".

## References

- [Calibration and statistics](references/calibration.md): read when building a calibration set, computing AUC, agreement, kappa, the sign test, intervals or power, or setting a bar.
- [Plan and results templates](references/templates.md): read when writing the eval plan or the results report.

## Output

Return one artifact, using the [templates](references/templates.md):

- **Eval plan** (design mode): change and decision, held-out set, arms, judge and its calibration plan, tripwires, pre-registered rule and n, the smallest detectable effect, spend estimate.
- **Results report** (run mode): set and manifest location, arms, judge calibration with intervals, tripwire table, results with W/L/T, win rate and interval, human review, decision, and what would change it.
- **Audit** (audit mode): violations ranked by impact, the direction of each bias, whether the verdict stands, and the smallest fix that would make it trustworthy.

Separate what was measured from what was inferred. Every number carries its n.

## Verify

- The held-out IDs are excluded in code from every prompt, retrieval call and judge anchor. Grep for the exclusion; do not assume it.
- The manifest replays: rerunning one slot from it reproduces the same prompt bytes.
- Failed generations appear in the denominator.
- Position is shuffled, both orders ran, and the flip rate is reported.
- The judge's calibration result, its bar and the bar's timestamp are in the report, and the bar predates the calibration run.
- The judge's model family differs from the generator's and the critic's.
- The decision follows the pre-registered rule, or the report says why not.
- Language matches the interval: no "better" when the interval spans no difference.

## Sources checked 2026-11-04

Research findings, not vendor defaults. Re-check if a newer study is cited against them.

- Position bias in LLM judges, and balancing by swapping order: Wang et al., "Large Language Models are not Fair Evaluators", https://arxiv.org/abs/2305.17926
- Position, verbosity and self-enhancement biases in LLM judges: Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", https://arxiv.org/abs/2306.05685
- Self-preference linked to self-recognition: Panickssery et al., "LLM Evaluators Recognize and Favor Their Own Generations", https://arxiv.org/abs/2404.13076
- Pairwise preference outperforming direct scoring on the tasks studied: Liu et al., "Aligning with Human Judgement: The Role of Pairwise Preference in Large Language Model Evaluators", https://arxiv.org/abs/2403.16950
