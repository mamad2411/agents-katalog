---
name: verify
description: "Use when someone asks to check a lesson, answer key, or learning material for accuracy, currency, and alignment. Not software code review or tests."
---

# Verify

Teaching something wrong is worse than not teaching it: a confidently learned error is hard to remove and costs points on the exam or worse in a clinic. This skill is a deliberate attempt to **break** the material before the learner does. A check that could not have failed is not verification.

Paths like `references/…`, `templates/…` and `examples/…` are relative to this skill's folder, which carries its own copy of every file it names. Other Myelinate skills are siblings (`../tutor/SKILL.md`) and are installed as their own skills too. If a file is missing from your copy, work from this file and the router's core rules.

## 1. When to run it

Always, before delivery:
- Labs, study packs, answer keys, practice exams, flashcard decks over ~20 cards
- Anything graded, clinical/medical, legal, financial, safety-related
- **Time-sensitive** content: guidelines, drug info, reference ranges, technology versions, laws, statistics, "current" anything, recent discoveries, taxonomy and nomenclature revisions, exam formats (MCAT/USMLE changes)
- Numeric models and simulations
- Claims where the course and the field may disagree

Light version (self-check, §3 steps 1 to 4) for ordinary chat explanations of stable material. Full adversarial review (§4) for the list above.

## 2. Time awareness

Know today's date and treat it as a variable:
- Ask "could this have changed?" for each consequential claim. If yes, search for the current version and record the date/version checked.
- Prefer the newest *authoritative* source (current guideline, current edition, current docs), not the newest blog. Recent ≠ reliable; old foundational work is fine for stable facts.
- Flag claims in the learner's materials that are outdated (e.g., reclassified taxonomy, revised guidelines). Teach the course version for the exam *and* the current version, labeled.
- Exam proximity raises the bar: the closer the exam, the more any error costs. With little time left, verify the highest-weight items first.

## 3. The verification pass

1. **Claim inventory**: list every consequential claim, number, definition, mechanism step, answer and distractor-key.
2. **Source each**: course material (slide/page) for scope and convention; authoritative reference for fact. Read the actual source, not a snippet. Mark: supported / course-only / unsupported / contradicted.
3. **Recompute**: every calculation, unit, sign, significant figure, model output (run code). Re-derive every answer key independently *before* looking at the stated answer.
4. **Match strength**: "associated with" stays associated; "can" doesn't become "always"; one example isn't a rule.
5. **Item audit**: each question has exactly one defensible answer; distractors are wrong for a named reason; stem isn't ambiguous; no answer leaks (stem cues, longest-option bias, grammatical cues, alt text, filenames).
6. **Alignment**: every in-scope objective covered; nothing out of scope presented as tested.
7. **Media**: labels correct, licenses recorded, masked labels fully masked.

## 4. Adversarial review (the important part)

Use an independent reviewer, a fresh subagent with no stake in the draft (or a second model when available). Give it the material, the sources, the course scope and today's date, and instruct it to **find errors, not to approve**:

> You are an adversarial reviewer for teaching material for [audience/course], exam on [date]. Today is [date]. Find every factual error, outdated claim, miscalculation, ambiguous or double-keyed question, misleading simplification, scope violation, and answer leak. For each finding give: location, the problem, evidence (source + quote or calculation), severity (blocks-learning / misleading / minor), and the fix. Check time-sensitive claims against current authoritative sources. Do not praise. If you find nothing in a section, say what you checked.

Then:
- **Triage** each finding yourself against the source; reviewers can be wrong too. Confirmed → fix. Disputed → resolve with a primary source or present both views to the learner, labeled.
- **Re-review** after substantive fixes (only changed parts).
- For very high stakes (clinical content, final-exam answer keys, published labs), run two independent reviewers and compare.
- Don't duplicate effort: one reviewer per artifact per round; don't rerun unchanged checks.

## 5. Report

Use `templates/verification-report.md`. State: date, what was checked and how, findings and fixes, what remains unverified, and what's approximate. Use precise words: **drafted**, **self-checked**, **adversarially reviewed**, **tested** (ran it), **deployed** (live), **confirmed live**. Never "verified" alone without saying by what.

## Anti-patterns

Reviewing your own draft and calling it adversarial · approving because sources "look reputable" · checking only that code runs · trusting a reviewer's finding without checking it · searching once and declaring "current" · silently teaching the course's outdated claim · burying uncertainty.
