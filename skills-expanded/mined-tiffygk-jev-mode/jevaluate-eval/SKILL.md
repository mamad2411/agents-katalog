---
name: jevaluate-eval
description: "Use when testing whether the jevaluate rubric and instructions lead graders to the right answers: after a rubric or instruction change, before freezing a rubric, before publishing ratings, or when a grader's calls look wrong."
---

# Jevaluate Eval

Tests whether graders apply the jevaluate rubric correctly, and proposes wording fixes. It never edits `rubric.md`, `read.md` or the library. If `$JEVALUATE_OVERLAY` is set, read that file first; its rules override the defaults here.

The scripts are in `jevaluate-eval/` (the quiz in `jevaluate-eval/quiz/`); every command is in `commands.md`. The runners refuse while `jevaluate/` or `jevaluate-harness/` has uncommitted changes, or `main` is ahead on them: commit or merge first.

## Four instruments, in order
Before each, tell the owner in one line which runs next and what it tests.

1. **Materials check: does what a grader reads say what the rules mean?**
   - `lint_materials.py` must print "lint clean": allowed values, eval-case names, em-dashes, named files, a `jevaluate/enforcement.md` row for every rule, and no sentence over 35 words added since the newest freeze.
   - A fresh reviewer, briefed as a grader, reads them for contradictions.
   - `build_grader_view.py <out.html>` builds the step-by-step view: the rater's start files, what `step.py` serves at each phase, every stakes row, and the eval grader's prompt. The owner reviews it. Schedule that review after any planned task that moves instructions into code, never before.
2. **Quiz: does a grader understand the rules on invented projects?**
   - Ask the owner how many scenarios they'll answer. Default 12: 8 tuning, 4 held out.
   - A writer that never sees the rules writes them (a headless call with no tools). Rewrite any that share 8 words with a rubric example or name an eval case.
   - The owner answers first, on `build_answer_form.py --count N`: type, calls Jev, verdict-1 code and stakes as read, with the type definitions beside each row. Save copies to the clipboard. `build_answer_form.py --key <answers.json>` derives kind and every n.a., and refuses contradictory answers: take each refusal line to the owner.
   - Show each disagreement with your reading, one scenario at a time, with the rule behind it. The owner rules; that is the key.
   - Draw the held-out set at random (record the seed), only after the key and any wording it triggered are final. In the results, name held-out scenarios whose discussion fed wording.
   - Red control first: `run_quiz.py --system vocab` gives only the vocabulary and should miss most answers; at 80% or more, the scenarios give their answers away. Report which rule tags the control passes: those scenarios check that the rules don't confuse a grader, not that it learned them. Then `run_quiz.py --system routing --reps 3` and `score_quiz.py`.
3. **Judgment eval: does a grader route real projects correctly?** `run_eval.py --phase baseline|after --out <runs>/<run>` (runs folder: `$JEVALUATE_RUNS` when set, else `.work/`), then `score.py <run>`. Every gold answer must be provable from its packet; held-out labels come from blind labelers, and the owner answers before seeing them.
   - New cases: packets follow `pick_files.py`. Each blind label goes through `check_labels.py run`, which applies the same call-line rule as `library.py check` and reruns a refused label once, keeping both. The owner answers on the same form as the quiz, built with `build_answer_form.py --cards`: the same fields, the type definitions beside each row, answers kept in the browser and saved to the clipboard. Each row is an evidence card from `build_cards.py` (call lines, README claims, acting lines, one plain sentence each), never a verdict; the card script refuses type, code and stakes words. Acting lines follow the answer to whoever it reaches: quote the line that acts and a line that shows who sees or receives the result (a README usage example counts), so the owner can read stakes and type without the code.

4. **Rater agreement: do two raters agree, and is either right?** For a second rater, such as another model, on real projects. Follow `rater-agreement.md`: name the tuning sample first, lead with held-out agreement and kappa (`rater_agreement/rater_agreement.py agreement`), then score both raters against an answer key the owner labels blind (`facts`, `draw`, `score`). Agreement claims consistency only.

## Rules
- Fix wording only against tuning misses, never naming a held-out scenario or an eval case. Each fix goes to the owner as a before-and-after before the rerun.
- Report per rule tag, propose one wording fix per missed rule, and stop.
