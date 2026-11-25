---
name: game
description: "Use for a study game, a fun way to drill for an exam, or typed practice that proves they know it. Not making a game (Unity, Godot, code). Decks: flashcards; tests: assess."
---

# Game

A typed retrieval game for an exam or a defined scope. It stays fun by keeping the learner producing answers quickly, with a visible payoff for each one. The fun serves retrieval: every point comes from an unaided answer, and nothing rewards time on the page.

Paths like `references/…` and `templates/…` are relative to this skill's folder, which carries its own copy of every file it names. Other Myelinate skills are siblings (`../tutor/SKILL.md`) and are installed as their own skills too. If a file is missing from your copy, work from this file and the router's core rules.

**Stand down when it isn't wanted.** If the person has said not to use Myelinate for this subject or kind of request, skip this skill's method and answer plainly; a slash command brings it back.

Evidence and limits: the method is retrieval, spacing, interleaving and successive relearning (`references/evidence.md`). No study has tested this game. Never say it raises grades or that a learner is ready; report what they did.

## 0. Rules that override everything else

1. **Never for graded work.** The page source holds every answer. Use `assignment` for graded items. A worksheet, prelab or problem set counts as graded until they say otherwise (router rule 13). A practice set the instructor gave out for exam review is fine. When you decline, don't stop to ask which route they want: in the same reply, load `../assignment/SKILL.md` and start teaching the first idea on a parallel problem with different numbers, then hand them their own problem to try.
2. **Scope comes from the source.** Read the study guide itself before listing what to memorize. See §1.
3. **One engine.** Copy `templates/exam-game.html` and replace only the JSON. Don't hand-build a game page.
4. **Cleared is not ready.** Show items cleared, attempts and practice scores. No readiness percent and no predicted grade (router rule 11).
5. **Rewards stay tied to retrieval.** No penalty for leaving, no daily streak, no prompt to keep playing past a break. The engine suggests a break after `breakMinutes`. Keep bonuses cosmetic. Bright flashes, particles and busy motion stay out unless the learner asks for them.
6. **The learner's own content stays private.** Course material and learner games never go into this repository.

## 1. Read the scope

1. Get the study guide, the exam format and the practice sets. Read each one fully, from the file itself.
2. **Formatting can carry the rule.** Red or blue text, highlights and boxes often mark "memorize" and "provided". Text extraction drops them, so look at a rendered page or read the file's run colors, and quote the legend.
3. **List from the primary source, never from a summary** of it, such as an older deck or chat. If you only have a summary, say so and offer to check the source.
4. **Write a study packet** as soon as you've read the source: the scope, the formula tiers, the exam format and every practice question as text, in the conversation; if they want it kept, in a file or the learner record (nothing is saved unless they ask). Screenshots can drop out of context, and re-reading a course site costs far more than the save.
5. Count before you state a total. Write the list, count it, then write the sentence.

## 2. Formula tiers

Every formula gets a tier, units and a source:

- `memorize`: the exam does not provide it. These form the gate.
- `know`: the guide asks for the skill but doesn't mark the formula.
- `provided`: on the exam. Drill when to use it and what each term means, including when the exam prints formulas without names.

Put units on each one. `unitsFrom` is `source` when the course states them and `derived` when you worked them out; the page labels derived units. If the learner wants to hand-write cards, show all tiers inline with `show_widget` or the host's equivalent, rendered as math, grouped by tier.

## 3. Fill in the JSON

Top level: `title`, `subtitle`, `source`, `settings`, `theme`, `exam`, `formulas`, `topics`.

- `settings`: `recheckHours` (default 8, so an evening session rechecks the next morning), `bonusChance`, `breakMinutes`, `mockTarget`. Set `mockTarget` only when the learner names a target.
- `theme`: `score`, `goal`, `right` (a few short praise lines) and `wrong`. Take these from the subject's world; a population ecology game can use N, K and "Population crash".
- `exam`: `format` in the instructor's words, then `quick`, `math` (item ids) and `free`, in the same mix as the real test.
- Formula: `id`, `name`, `tier`, `lhs`, `rhs`, `alts`, `units`, `unitsFrom`, `hook`, `src`, `obj`, optional `svg`, `caseSensitive`, and, for a `memorize` formula, `apply`, one math item that uses it. Drill `provided` and `know` formulas with topic items. Answers are compared by value, so `alts` needs only forms with different symbols, such as `N_0 R_0^t` beside `N_0 R^t`. Set `caseSensitive: true` when case changes the meaning, such as R and r.
- Topic: `id`, `name`, `sub`, `brief` (a 60-second list), optional `svg`, `items`.
- Item, all types: `id`, `type`, `q`, `src`, `obj` (the guide objective), `why`, optional `need`, `svg`, `table`.
  - `term`: `answers`, and `near` for close wrong answers (`afferent` for `efferent`). Only long words get one typo of grace, and only with the same first letter.
  - `sort`: `options`, `answer` (index). Recognition is weaker than recall, so never let sort items be the only check of an objective.
  - `num`: `answer` for a fixed problem, or `vars`, `expr` and `{name}` / `{=expr}` in `q` and `why` for new numbers each time. Prefer new numbers so answers can't be memorized. Also include each ungraded class problem as a fixed item.
  - `free`: `rubric` (`min`, `points` of `label` and `pattern`) and `model`. Key-word matching is a practice aid, never a grade; `assess` and `print` own real grading.

Math in text goes between `$` signs in plain typed form: `$N_0 e^(rt)$`, `$(K-N)/K$`, `$n_{t+1}$`, `$dN/dt$`. A denominator is one symbol unless it's in parentheses: `a/(bc)`. Write a money sign as `\$`. Draw any `svg` from the actual equation or data, with its answer out of its labels and title. Serialize with a real JSON library and write every `<` as `\u003c`.

## 4. Coverage and checks

Every guide objective gets at least one production item (`term`, `num`, `free` or `formula`), through the coverage map in `references/production-lessons.md`. Work every answer with code. Then open the page and run `gameAudit()`. Don't deliver until `ok` is true and each objective in the guide appears under `objectives`. It reports missing sources or units, formulas whose `alts` miss their own `rhs` or can't be typed, an `apply` that won't run, model answers that fail their own rubric, bad sort answers, numbers that don't compute or display, raw TeX, text mistaken for math, and objectives covered only by sort items. It can't judge whether content is right. With no browser, say the audit didn't run and name what's unchecked. Then play one card of each type at phone width and in dark mode, including one wrong answer. Say exactly what you ran.

## 5. Delivery

Publish it where the learner can return. The gate and the delayed recheck need saved progress, which lives in that browser's local storage, on that device. Some artifact sandboxes block it. Open the page where it will live and read `progressSaves` from `gameAudit()`: if it's false, deliver the HTML file instead and say why, because in that sandbox the gate resets and the next-morning recheck never comes due.

Tell them the order in a line or two: gate, stages, mock, delayed recheck. The night before an exam, plan the recheck for the morning (`study-plan`).

## 6. Reading the evidence

Map outcomes to the router's states. Gate test passed: *Independent this session*. Delayed recheck passed: *Retrieved after delay*. A free answer counted by "I had it": *self-assessed*, shown separately on the page. A key-word match on a free answer is practice, not a grade. The mock's number covers auto-marked items only. Asked "am I ready?", say what they did unaided and what hasn't been checked after a delay; ask them to read you the map if you can't see it. After the real exam, ask what appeared and what cost points, and use that to fix the next game.
