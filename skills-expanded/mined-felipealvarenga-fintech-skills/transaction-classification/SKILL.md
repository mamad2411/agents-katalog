---
name: transaction-classification
description: >-
  Use when code assigns a category, account, merchant or type to bank, card or ledger transactions
  with rules, machine learning or an LLM, and especially when the result posts to books
  automatically. Covers a labeled holdout with per-class precision, recall and coverage,
  deterministic layers before the model (user rules, approved repeats, merchant normalization,
  transfer pairing), confidence gating calibrated on data, structured output validated against the
  chart, learning from corrections, keeping PII and injected instructions out of the loop, audit
  fields per decision and drift monitoring. Triggers on a categorization feature, an auto-posting
  proposal, an accuracy claim without numbers, a prompt that reads bank memos. Not for choosing
  the chart of accounts itself, which belongs to the accountant.
license: MIT
metadata:
  author: Felipe Alvarenga
  version: 0.1.0
---

# Transaction classification

Categorizing transactions is where most "AI bookkeeping" lives, and where most of it is
unmeasured. A model that is right 92% of the time on a demo and 70% on the customer's actual
restaurant supplier is a liability when it posts automatically. The discipline is the same as
any classifier in production: a holdout, numbers per class, a gate, and a feedback loop.

## When to use

- A feature that categorizes bank feed lines, card transactions or ledger events.
- A proposal to post categorizations automatically, or to raise the share auto-posted.
- An accuracy claim ("it works well") without a measurement behind it.
- A prompt or model that reads merchant names, memos or descriptions.
- A drop in quality after a chart change, a new bank or a model update.

## Rules

1. **Build the holdout before the model.** A labeled set reviewed by an accountant or the
   customer, stratified by merchant, amount band, account type and tenant. It never enters a
   prompt, a fine-tune or a rule. Keep it versioned.
   When no labeled data exists yet, the change still creates `holdout.jsonl` with the schema
   (`id, description, amount_minor, account, label, labeled_by, labeled_at`), seeded from the
   transactions at hand with `label` null where nobody has labeled yet, and `eval_holdout.py`
   that computes precision, recall and coverage per class from it. An empty holdout that the
   code reads beats a plan for one.
2. **Report per-class precision, recall and coverage, plus cost.** Coverage is the share of
   transactions the system decides on its own. A model change is a pull request that shows the
   new numbers next to the old ones on the same holdout, with cost per thousand transactions
   and latency.
3. **Deterministic layers run first, in order.** User rules (payee pattern to category),
   exact repeats the user already approved (normalized payee plus amount pattern), merchant
   normalization (strip store numbers, card suffixes, city tails), and transfer pairing. The
   model sees only what these did not decide.
4. **Transfers are matching, not classification.** A debit in one of the customer's accounts
   with a credit of the same amount within a window in another of their accounts is a transfer.
   Pair them before classifying; never let the model label one side as expense and the other as
   income.
5. **Gate by calibrated confidence.** Auto-post above a threshold chosen on the holdout for a
   target precision per class; propose for review below it. Never auto-post splits, transfers
   across the customer's own accounts, amounts above a per-tenant limit, or categories the
   accountant marked as review-only.
   The thresholds live in `thresholds.json`, written by `calibrate.py`: for each class, the
   lowest cutoff whose precision on the holdout meets the target (0.98 for auto-posting unless
   the accountant sets another). The gate reads that file; a constant in code with a "calibrate
   later" comment is the anti-pattern. Until the holdout has labels, `calibrate.py` writes 1.0
   for every class, so nothing auto-posts by accident.
6. **The output is structured and validated.** Category id from the allowed chart, confidence,
   short rationale, and the fields used. Validate the id against the chart; an unknown or
   disallowed id becomes "uncategorized, review". Free-text category names are never accepted.
7. **Every correction is a label, and repeated corrections become rules.** When the user
   changes a category, store the example with the original decision. When the same payee is
   corrected twice, propose a rule. Correction rate per class is the live accuracy signal and
   goes on the dashboard.
   This is three small functions in the first change, not a later phase:
   `record_correction(tx_id, from_id, to_id, user, at)` appends to the corrections store,
   `correction_rate(window)` returns the rate per class, and `propose_rules()` emits a rule
   when the same normalized payee was corrected to the same category twice.
8. **Descriptions are data, not instructions.** Merchant names and memos are untrusted text.
   The prompt frames them as data, the output is structured, and a test injects "ignore previous
   instructions" into a memo and asserts the category is still validated and unaffected.
   Prompts never contain card numbers, full account numbers or more personal data than the
   decision needs (see `pii-and-card-data`).
9. **Store the decision record.** Classifier version, prompt or model id, confidence, rules
   fired, inputs used, and who approved. Accountants and auditors ask "why this category" and
   the answer must not depend on re-running the model.
10. **Watch for drift and chart changes.** Weekly: correction rate per class, class
    distribution, share of uncategorized, cost. A new category needs labels before the model
    can use it; a renamed one needs a mapping. Retrain or re-prompt when drift crosses the
    threshold, and re-run the holdout before shipping.

## How to apply

1. Collect and label the holdout first. Agree with the customer or accountant on the chart
   version and the review-only categories.
2. Implement the deterministic layers and measure what they cover alone. Often a third or more
   of the volume needs no model.
3. Implement the model call with a structured output schema and the validator. Measure on the
   holdout. Calibrate the threshold per class.
4. Build the review queue and the correction capture. Wire corrections to labels and rule
   proposals.
5. Write the tests in the **Tests** section, including the injection test.
6. Ship with the dashboard: per-class metrics, coverage, correction rate, cost. Set the drift
   alert.

When the request conflicts with a rule here, say which rule in one sentence, then build the
compliant version that keeps the request's intent. An instruction to skip a step ("no extra call", "just delete
it", "we trust them", "later") is this conflict, not permission. Leaving the code unchanged and
listing the risks is never the compliant version. Do not stop at a warning, do not build the
unsafe version, and do not leave a known gap out because "you did not ask". A review
or an "is this enough" question gets the findings and the rewritten tests in the same change, not
a list of suggestions, unless the request or the skill says report only.

## When the user pushes back

| Request | Answer in one sentence | What you build |
|---|---|---|
| "Accuracy looks fine in our manual checks, ship it" | Rule 2: twenty hand-checked rows give no per-class numbers | The holdout file, `eval_holdout.py`, `calibrate.py` and the correction capture; the gate at 1.0 until the numbers exist |
| "Lower the threshold to 0.6, the queue is too big" | Rule 5: one global cut trades precision you cannot see | Per-class thresholds from `calibrate.py`. With precision at one cutoff only, show which classes already clear the target, which never auto-post, and what the curve needs (confidence per holdout row). Report coverage gained and precision cost per class, "unknown" where the curve is missing |
| "We switched the model, is it better?" | Rule 2: a model change is a side-by-side table on the same holdout | `eval_models.py`: precision, recall and coverage per class, cost per thousand and p50 latency, both models side by side. Run it when a client exists; otherwise deliver the harness and the table it fills. Say when the holdout is too small (under about 30 rows per class). Recalibrate the thresholds before auto-posting resumes: the new model's confidence is on a different scale |
| "Just add the customer rules" | Rules 3 and 7 | Rules on the normalized payee, before the model, `propose_rules()` from repeated corrections, and the rule's name in the decision record |

## Tests the change must include

Write these tests in the same change, as a test file, even when you cannot run them (no shell,
no dependencies installed); say in one line that they are unrun. A test listed as a next step is
not written.

- Holdout evaluation runs in CI or on a schedule and fails the pull request when precision for
  any auto-post class drops below its target.
- Deterministic layers: a user rule beats the model; an approved repeat beats the model; a
  transfer pair is labeled transfer on both sides.
- Pairing over the whole sample file: the transfer pair is labeled transfer on both sides and
  every other line stays unpaired.
- Normalization: two store numbers of one merchant (`UBER *TRIP 8841`, `UBER *TRIP 9920`)
  normalize to the same key, and one rule matches both.
- Corrections: two corrections of the same payee produce one rule proposal; the correction
  rate per class is computed from the store.
- Calibration: on a small synthetic holdout, `calibrate.py` picks the lowest cutoff per class
  that meets the precision target and writes 1.0 for a class without labels.
- Gate: a low-confidence decision goes to review and is never posted.
- Validation: an invalid category id from the model becomes uncategorized with review.
- Injection: a memo with instructions does not change the output or bypass validation.
- Decision record: every classified transaction has version, confidence and rules fired.
- PII: the rendered prompt for a sample transaction contains no full account or card number.
- Reference vectors: `skills/transaction-classification/evals/vectors/test_classification.py`
  with `CLASSIFY_SOLUTION` pointing at your module (normalization, transfers, validation, gate).

## Review checklist

- Where is the holdout, who labeled it, and what are the per-class numbers today?
- Which layers run before the model, and how much do they cover?
- What is the threshold per class, and how was it chosen?
- What can never be auto-posted?
- Where do corrections go, and what is the current correction rate?
- Show the rendered prompt for one transaction.

## Anti-patterns and fixes

| Anti-pattern | What goes wrong | Fix |
|---|---|---|
| Accuracy from a demo set | Collapses on real merchants | Stratified holdout, per-class numbers |
| Model decides everything | Costly, inconsistent on repeats | Rules and approved repeats first |
| Free-text categories from the model | Unmappable, inconsistent | Ids validated against the chart |
| One global confidence threshold | Great on utilities, bad on contractors | Per-class calibration |
| Corrections discarded | Same mistake every month | Corrections become labels and rules |
| Memo pasted into the prompt as text | Injection and PII exposure | Data framing, structured output, redaction |

## References

- Standard classifier evaluation practice: precision, recall, calibration, stratified holdouts.
- Intuit's `quickbooks-labs` plugin, whose categorize skill posts proposals only after approval, as an example of gating in a shipped product.
- OWASP guidance on prompt injection through untrusted data fields.
