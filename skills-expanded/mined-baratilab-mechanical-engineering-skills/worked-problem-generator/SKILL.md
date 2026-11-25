---
name: worked-problem-generator
description: Generates textbook-style mechanical engineering problems (statics, mechanics of materials, dynamics, machine design, thermo, fluids, heat transfer) at a chosen difficulty and Bloom level, with full step-by-step solutions verified by running code, plus variants with randomized values for exams. Use when the user wants practice problems, homework, exam questions, quiz items, or worked examples for teaching.
---

# Worked Problem Generator

## Workflow
1. **Spec.** Get the topic, the learning objective, the level (intro undergrad / upper undergrad / grad / exec-ed practitioner), the count, the format (open-ended, multiple choice, or both), and the unit system. If the user gave a syllabus or lecture notes, align notation with them.
2. **Design each problem** against the template in `references/problem_template.md`:
   - a realistic context, ideally a real device or failure, in 2–4 sentences;
   - givens with units and realistic magnitudes (check them against `machine-element-sizing/references/materials.md` or CoolProp);
   - a clear ask, with sub-parts building from (a) a direct application to (c) a judgment or design decision;
   - mix the Bloom levels across the set: apply, analyze, evaluate, create.
3. **Solve in code first.** For each problem, write a short Python solution (use `pint` for units) and run it. The worked solution is written from the code output, so the text and the numbers can't disagree. Use the other skills' scripts where they fit.
4. **Write the worked solution**: FBD or schematic description (or a figure via `mechanics-visuals`) → assumptions → governing equations → substitution → answer boxed with units and 3 significant figures → a one-line sanity check (order of magnitude, limiting case) → common mistakes students make on this problem.
5. **Multiple-choice items.** Make distractors from real errors (a forgotten factor of 2, diameter used for radius, a unit slip, the wrong failure theory), each computed in code. Spread correct answers evenly across A/B/C/D.
6. **Exam variants** (when asked): parameterize the givens, generate N variants with seeded random values in realistic ranges, and recompute every answer key in code.
7. **Deliver.** For students, give the problem set without solutions plus a separate solutions document. For a quiz, use the quiz widget (or the format the user asks for). Include the solution scripts in an appendix for instructors.
