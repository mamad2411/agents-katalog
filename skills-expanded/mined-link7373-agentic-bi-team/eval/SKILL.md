---
name: eval
description: Measure whether the team answers data questions correctly — run the eval suite of questions with pinned answers, grade the results, record the run, and turn failures into fixes. Use after changing an agent, skill, or knowledge file, on a schedule, when a stakeholder corrects an answer, and before announcing the team to a new audience.
---

# Eval — Is The Team Actually Right?

Owner: the orchestrator, with `analysis-reviewer` on failures. Args pick the mode and suite, e.g. `/eval`, `/eval local`, `/eval add` (after a correction), `/eval check`.

An analytics answer can be wrong, look plausible, and be used without objection. Nothing else in the kit measures that. An eval is a question with a known right answer; a suite of them tells you whether a change to a skill or a knowledge file helped, and catches the slow drift that happens as the data model changes under documentation that did not.

Two suites: `evals/demo/` ships with the kit and runs against the pinned demo warehouse. `evals/local/` is yours — questions about your business, on your data. The demo suite proves the kit works; the local suite proves *your team* does. Format and grading rules: `evals/README.md`.

## Mode A — Run (default)

1. **Check the answer key first.**

   ```bash
   python scripts/run_evals.py --check-references
   ```

   This needs no model. If a reference drifted, the key is wrong, not the team — stop and fix that before grading anything against it.

2. **Get the paper.** `python scripts/run_evals.py --paper --suite <suite> --json` prints ids and questions only. For the demo suite, also run `python scripts/run_evals.py --build-db` and note the path it prints: answers must come from that pinned database, not from `demo/demo.db`, whose dates move with today.

3. **Answer each question the way the team would for a stakeholder.** Delegate each to `bi-analyst` (in parallel, in batches) with **only the question text** and the database to use. The agent works exactly as it normally would: knowledge base, catalog first, data checks, privacy rules.

   **The answer key is off limits.** No answering agent opens anything under `evals/` — say so in each brief. An eval the team has read the answers to measures nothing, and this is enforced by instruction, not by a lock, so it depends on you.

4. **Collect the answers** into `evals/runs/<YYYY-MM-DD-HHMM>/answers.json`:

   ```json
   {
     "meta": {"suite": "demo", "model": "<model id>", "notes": "after editing /analyze step 3"},
     "answers": {
       "active-customers": {"behaviour": "answered", "value": 549, "text": "549 active customers as of 30 June 2026."},
       "trap-ambiguous-churn": {"behaviour": "clarified", "text": "Do you mean logo churn or revenue churn, and for which period?"}
     }
   }
   ```

   `behaviour` is one of `answered`, `clarified` (asked a question instead of answering), `refused` (declined on policy grounds), `flagged_data_issue` (reported a data problem as the finding). `value` is the headline number or label; `text` is the answer as the stakeholder would read it. Record what the agent actually did — do not tidy an answer on its way into the file.

5. **Grade and record.**

   ```bash
   python scripts/run_evals.py --grade evals/runs/<stamp>/answers.json
   ```

   The run is appended to `evals/results/history.jsonl` with the git SHA, kit version, and model.

6. **Report.** Pass rate, per-category results, and each failure with its reason. Then `python scripts/run_evals.py --history` — say whether this run is better or worse than the last, and which questions newly fail.

7. **Diagnose every failure — the eval is the symptom.** For each one, name which of three things went wrong:
   - **Ambiguity:** more than one plausible table, column, or definition, and the team picked the wrong one. → Fix in `knowledge/metrics-catalog.md` (a definition, a named segment) or deprecate the near-duplicate.
   - **Staleness:** the documentation describes the data as it used to be. → Fix the knowledge file; check what else that file says.
   - **Retrieval:** the right information exists and the team did not find or use it. → Fix the domain reference doc in `knowledge/domains/` — usually a missing routing trigger or gotcha.

   Fix the knowledge, not the answer. Then re-run the affected questions. Do not edit an eval to make it pass unless the *eval* was wrong, and if it was, say so in the commit.

## Mode B — Add an eval from a correction (`/eval add`)

Every time a stakeholder says "that's the wrong table" or "you forgot to exclude test accounts", the team has been handed a free eval.

1. Write the question as the stakeholder asked it, the reference SQL that produces the right answer, and the pinned answer, into `evals/local/questions.md`. Pin it: a fixed date range, an as-of date, a closed period — a question whose answer moves tomorrow is not an eval.
2. Add `must_mention` for the thing that was missed ("excluding test accounts"), and a one-line `why`.
3. Fix the cause in the knowledge base (Mode A step 7), in the same change.
4. Log the correction in `knowledge/decision-log.md`.

## Mode C — Check only (`/eval check`)

`python scripts/run_evals.py --check-references` and `--history`. No model calls. This is what CI runs, and what `/health-check` runs weekly.

## How many, and when

- A few dozen questions per business domain is enough; returns diminish after that. Cover the top stakeholder questions, each domain's main KPIs, and every trap that has actually caught the team.
- Run the full suite after any change to an agent, a skill, the catalog, or a domain doc — and put the before/after pass rate in the commit message. "I improved the docs" is a claim; the delta is evidence. A well-meant addition that lowers the score is common.
- **Gate new audiences.** Before the team is announced to a new group of stakeholders, their domain's slice of `evals/local/` clears the threshold (default 90%).
- A pass rate near 100% means there are no *known* gaps, not that the team cannot be wrong. It does not replace `analysis-reviewer` or the provenance footer.
- Keep a short "tried it, did not help" list in `knowledge/decision-log.md`. Negative results are cheap to record and stop the next person re-running the experiment.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
