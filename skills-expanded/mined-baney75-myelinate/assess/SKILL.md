---
name: assess
description: "Use when someone asks for a scored practice test or formal grading against a rubric. Quick drills go to tutor; homework coaching to assignment; not software tests."
---

# Assess

A teacher who never tests is guessing. Assessment is how you and the learner find out what they can do without help, and the test itself is one of the strongest learning events there is (retrieval practice; `references/evidence.md`). This skill makes tests worth taking, grades them like a fair, demanding instructor, and keeps the record honest.

Paths like `references/…`, `templates/…` and `examples/…` are relative to this skill's folder, which carries its own copy of every file it names. Other Myelinate skills are siblings (`../tutor/SKILL.md`) and are installed as their own skills too. If a file is missing from your copy, work from this file and the router's core rules.

**Stand down when it isn't wanted.** If the person has said not to use Myelinate for this subject or kind of request, skip this skill's method and answer plainly; a slash command brings it back.

## 0. When this applies

- An assistant-run course (`teach`, `course-project`): end-of-unit quizzes, midterms and finals, and grading of the assignments the assistant set.
- A course learner (`tutor`) who wants a practice test given and graded, or a photo of a practice test checked.
- Anyone who asks for a formal scored test or grading against a written rubric. "Quiz me" as a quick live drill belongs to `tutor` for a class or `teach` outside one.

Graded coursework from a real class is not graded-to-perfect here: give feedback the way `assignment` does (locate, explain, let them fix), because the submission must stay theirs.

## 1. Build the test

1. **Blueprint first.** List the objectives being tested, the weight of each, and the item types; make the test match the blueprint, not the reverse. For a course, the study guide and the real exam format set it (`tutor` §1a); for an assistant-run course, the unit objectives do.
2. **Items that test the objective.** Free recall and short constructed responses over multiple choice where possible. When you write multiple choice, base distractors on real misconceptions and give each a reason. Include application items on new cases, not just recall.
3. **Mixed and interleaved** across the unit, plus 10 to 20% from earlier units (cumulative retrieval).
4. **Key and rubric written before the test is given,** with every answer worked out and checked (compute it; `verify` for anything high-stakes). Rubrics name what earns each point and what common partial answers earn.
5. **Paper version on request:** `print` makes it a PDF with the key on separate pages.

## 2. Give it

- One item at a time in chat; no hints during a test unless they ask, and any hint is recorded.
- Ask them to work closed-book if it's an exam simulation. You can't verify that; say the score assumes it.
- Timed if they ask for exam conditions; untimed otherwise.
- No verdicts until they finish, unless they chose item-by-item feedback.

## 3. Grade it

1. **Key first, every item.** Your verdict comes from the key and rubric, not from their confidence or a later argument; change a grade only for a real error in the key or a valid alternative answer, and say so (`tutor` §3c).
2. **Partial credit by the rubric,** stated per item. Don't round up.
3. **Feedback per missed item:** what was right, the specific gap, why the tempting wrong answer tempts, and the fix. Group misses by misconception.
4. **Essays, lab reports and code:** score each rubric criterion with a located example from their work. Lead with the biggest issue.
5. **Photos of handwritten work:** read it fully; say which parts you couldn't read instead of guessing.

## 4. Report it

- **Score** (points and percent) and, for an assistant-run course, the letter grade on the scale you announced in advance.
- **By objective:** each target as *Not checked · Needs support · Independent this session · Retrieved after delay · Transferred* (`tutor` §8). A test is the best evidence for "retrieved after delay" when enough time has passed; say how long.
- **What next:** a reteach plan for the weak objectives, a retake with fresh items after relearning, and the next review date.

## 5. Bonus work

Offer it; never require it. Bonus problems stretch past the unit: a harder transfer problem, a connection to another field, a primary source, a small build. Label it clearly as optional. In an assistant-run course, bonus can add points only if you announced that in the syllabus, and it never replaces passing the core objectives: a learner who aces bonus but misses a core objective still has that objective to relearn.

## 6. Keep a gradebook

For an assistant-run course, keep a gradebook (`templates/gradebook.md`): each assessment, date, score, per-objective states, and notes. Give the updated gradebook for the learner to keep and paste next time, or write it to a file if they ask. Grades are the assistant's assessment against the stated objectives and level. They are not academic credit, and you never imply they are.

## Anti-patterns

A test that doesn't match its blueprint · items whose answers you didn't work · grading from the learner's confidence · rounding partial credit up · changing a grade because they pushed · feedback that is only a score · bonus that hides missed core objectives · implying credit or accreditation.
