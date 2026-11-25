---
name: "solve-math-rigorously"
description: "World-class solver-first math skill for reading, mapping, solving, and checking nontrivial math tasks. Use when the user asks to solve an equation or system, find all solutions, prove a claim, optimize a function, work through a derivation step by step, check whether an answer is correct, explain what a worksheet or whiteboard problem says, or read math from an uploaded photo, screenshot, PDF, textbook page, handwritten note, or diagram before solving it carefully and verifying the result."
---

# Solve Math Rigorously

## Overview

This skill is solver-first. Default to understanding the mathematical object, mapping the problem, choosing the right method family, solving in inspectable steps, and testing the result before sounding certain. If the source is a photo, screenshot, or uploaded page, first turn it into a trustworthy transcription and diagram map, then solve from that map. Teaching, worksheets, and lesson generation remain available, but they are secondary to accurate problem solving.

## Claude-First Usage

This skill is intended to work well in Claude Desktop and Claude chat surfaces.

- Treat uploaded images and PDFs as first-class inputs.
- Prefer Claude's native multimodal reading first.
- Use the helper scripts only when the environment actually supports code execution.
- If code execution is unavailable, do not block on tooling. Continue with careful transcription, reasoning, and explicit uncertainty handling.

Read `references/claude-surface-playbook.md` before assuming tools or file-system access.

## Default Solver Mode

Use this mode unless the user explicitly asks for something else.

Core standard:

1. Understand the problem before transforming it.
2. Build a problem map before committing to a method.
3. Solve one hinge step at a time.
4. Check every candidate result aggressively.
5. Present the logic in the order a strong human solver would want to read it.

## Solver Operating Modes

- `solver`: full map, full method selection, clear derivation, and independent verification
- `photo-solver`: inspect the image, transcribe and map the task carefully, resolve or flag ambiguities, then solve and verify
- `fast-answer`: concise visible output, but still do the mapping and verification internally
- `worked-solution`: show the derivation in full, with the hinge step and method choice made explicit
- `proof`: separate exploration from proof, test for counterexamples early, then write a clean argument
- `exam`: minimize exposition, show only essential steps, and make the final answer easy to grade
- `tutor`: reveal the next move or next subgoal rather than dumping the whole solution at once

Secondary educational modes remain available when the user explicitly wants them:

- `diagnostic`
- `worksheet`
- `lesson`
- `review`
- `primary-school`
- `parent-teacher`

## Photo Intake Protocol

If the task comes from a photo, screenshot, scanned page, uploaded PDF, whiteboard, or handwritten note:

1. Inspect the whole image before reading line by line. Determine whether it contains one problem, multiple problems, or a diagram plus text.
2. Delimit the task boundaries. Do not accidentally solve the wrong subproblem from the page.
3. Transcribe the problem exactly, preserving:
   - symbols
   - exponents
   - fractions
   - radicals
   - inequality signs
   - labels on diagrams, axes, and tables
4. Separate `clearly read`, `inferred from context`, and `uncertain` content.
5. For diagrams, record explicit givens separately from what only appears visually plausible. Do not infer exact equality or scale from a sketch unless it is marked or stated.
6. If legibility is poor and code execution is available, use `scripts/math_photo_helper.py` to create enhanced views before solving.
7. When ambiguity still matters after enhancement, state the competing readings and either ask the user to confirm or solve each plausible interpretation.

Read `references/photo-mapping-playbook.md`, `references/diagram-reading-playbook.md`, and `references/claude-surface-playbook.md` for photo-based tasks.

## Problem Mapping Protocol

Before solving, map the task explicitly:

1. Restate the target in mathematical terms.
   - If the source is a photo, restate from the verified transcription, not from a guess.
2. Identify the mathematical object:
   - simplification or evaluation
   - equation or system
   - inequality
   - optimization
   - proof
   - counting or probability
   - recurrence or sequence
   - geometry or trigonometry
   - modeling or word problem
3. Define symbols, givens, unknowns, domain restrictions, units, hidden constraints, and any uncertain glyphs or labels coming from the source.
4. Decide what counts as a complete answer:
   - exact value
   - approximation
   - all solutions
   - proof
   - interval or region
   - extremum and where it occurs
5. List 2-3 plausible method families before choosing one.

Read `references/problem-mapping-playbook.md` when the problem is dense, ambiguous, or easy to misclassify.

## Method Selection

Choose methods by triggers, not habit.

- Factor, substitute, or change form when the expression structure suggests it.
- Use symmetry, invariants, parity, or monotonicity when brute force looks wasteful.
- Use coordinates, vectors, or a diagram when geometry becomes algebra more cleanly than synthetic reasoning.
- Use derivative, convexity, or endpoint analysis for optimization.
- Use complements, conditioning, linearity of expectation, or counting models in probability and combinatorics.
- Use a small-case search or counterexample hunt before attempting a universal proof.

Read `references/method-selection-playbook.md` when choosing between competing approaches.

## Solver Loop

Run the solve loop deliberately:

1. Choose the most promising branch.
2. Carry the branch until a hinge step succeeds or clearly stalls.
3. After each nontrivial step, checkpoint:
   - Is the transformation valid?
   - Did any domain restriction change?
   - Is the new form actually easier?
4. If the branch stalls, pivot instead of forcing it:
   - change representation
   - try a smaller case
   - isolate a subgoal
   - differentiate or factor
   - translate to coordinates or a table
5. Once a candidate answer appears, verify it before polishing the explanation.

Read `references/solver-loop-playbook.md` when the path is not obvious or when a first attempt stalls.

## Step-By-Step Communication Standard

- Expose the hinge step. Do not skip the move that makes the solution work.
- If the source was a photo and the reading was not obvious, show the interpreted statement before solving.
- Justify the operation when it is not immediate.
- Keep notation stable. Do not silently rename objects or switch parameter meanings.
- Separate exact values from approximations.
- For proofs, separate exploration from the final proof.
- For systems or longer derivations, summarize subgoals as you move.
- If a result is only numerically supported, say that clearly.

## Verification And Testing

Escalate verification until confidence is genuinely high:

1. Sanity checks:
   - sign
   - scale
   - units
   - symmetry
   - boundary behavior
   - special values
2. Structural checks:
   - substitute back
   - differentiate or integrate back
   - compare equivalent forms
   - verify constraints and excluded cases
3. Independent checks:
   - solve a second way
   - compute a small case
   - estimate numerically
   - use a geometric or probabilistic interpretation
4. Tool-assisted checks:
   - use `scripts/math_verify.py`
   - use `scripts/math_visualize.py`
   - use `scripts/math_table.py` when a table exposes the pattern better than prose
   - use `scripts/math_photo_helper.py` when better preprocessing is needed to trust the transcription

Read `references/verification-playbook.md` before claiming confidence on nontrivial work.

## Tooling

If code execution is available and `sympy`, `numpy`, or `matplotlib` are unavailable, bootstrap a local environment from the skill root:

```bash
bash scripts/bootstrap_env.sh
```

Then run the helpers with `.venv/bin/python3`. If code execution is not available in the Claude surface, continue without scripts and make the verification status explicit in the response.

### `scripts/math_verify.py`

Use this helper for direct solver-side checks.

Capabilities:

- expression equivalence
- derivative checks
- antiderivative checks
- definite integral checks
- substitution and evaluation
- direct relation satisfaction checks
- system satisfaction checks
- one-sided and two-sided limit checks
- finite solution-set comparisons
- counterexample search for equalities and inequalities on an interval

Examples:

```bash
.venv/bin/python3 scripts/math_verify.py equiv "sin(x)^2 + cos(x)^2" "1"
.venv/bin/python3 scripts/math_verify.py derivative "x^3 * exp(x)" "exp(x) * (x^3 + 3*x^2)" --var x
.venv/bin/python3 scripts/math_verify.py definite-integral "2*x*cos(x^2)" "0" "sqrt(pi)" "sin(pi)" --var x
.venv/bin/python3 scripts/math_verify.py solve "x^2 - 5*x + 6 = 0" --var x --expected 2 --expected 3
.venv/bin/python3 scripts/math_verify.py satisfies "x^2 + y^2 = 25" --assignment x=3 --assignment y=4
.venv/bin/python3 scripts/math_verify.py system --equation "x+y=5" --equation "x-y=1" --assignment x=3 --assignment y=2
.venv/bin/python3 scripts/math_verify.py limit "sin(x)/x" "0" "1" --var x
.venv/bin/python3 scripts/math_verify.py counterexample "sin(x) >= x" --var x --xmin 0.1 --xmax 2
```

Treat `PASS` as strong evidence. Treat `FAIL` as a real warning. Treat `INCONCLUSIVE` as a signal to add another check or change representations.

### `scripts/math_visualize.py`

Use this helper when a plot or shaded figure makes the behavior easier to inspect:

```bash
.venv/bin/python3 scripts/math_visualize.py --expr "sin(x)" --expr "x/2" --xmin -6 --xmax 6 --output /tmp/sine-vs-line.png --title "Intersections of sin(x) and x/2"
.venv/bin/python3 scripts/math_visualize.py --expr "x^2" --shade-upper "x^2" --shade-lower "0" --shade-from 0 --shade-to 2 --xmin -1 --xmax 3 --output /tmp/area.png
```

### `scripts/math_table.py`

Use this helper when a sequence, recurrence, or iteration is easier to inspect as a table:

```bash
.venv/bin/python3 scripts/math_table.py sequence "n^2 + n + 1" --start 1 --end 6
.venv/bin/python3 scripts/math_table.py iterate "cos(x)" --start 1 --steps 6
```

### `scripts/math_photo_helper.py`

Use this helper when a math task comes from a raster image and the raw photo is hard to read cleanly, but only when the Claude surface supports code execution. For uploaded PDFs, prefer Claude's native PDF reading first.

Capabilities:

- upscale and normalize a photo
- produce grayscale, sharpened, and high-contrast variants
- split tall pages into readable tiles
- create a contact sheet for quick re-inspection

Examples:

```bash
.venv/bin/python3 scripts/math_photo_helper.py enhance --input /tmp/problem.jpg --output-dir /tmp/problem-enhanced
.venv/bin/python3 scripts/math_photo_helper.py enhance --input /tmp/worksheet.png --output-dir /tmp/worksheet-enhanced --upscale 2 --tile-height 1200
```

Use the enhanced outputs to verify the transcription before solving.

### Secondary Educational Tools

Use these only when the user explicitly wants educational assets rather than solver-first output:

- `scripts/math_manipulatives.py`
- `scripts/math_practice.py`

### `scripts/run_validation_suite.py`

Use this helper after changing solver tooling:

```bash
.venv/bin/python3 scripts/run_validation_suite.py
```

## Solver References

Load these first for hard solving tasks:

- `references/problem-mapping-playbook.md`
- `references/method-selection-playbook.md`
- `references/solver-loop-playbook.md`
- `references/claude-surface-playbook.md`
- `references/photo-mapping-playbook.md`
- `references/diagram-reading-playbook.md`
- `references/verification-playbook.md`
- `references/proof-playbook.md`
- `references/visualization-playbook.md`

Load these only when the user explicitly wants teaching or educational materials:

- `references/teaching-playbook.md`
- `references/primary-school-playbook.md`
- `references/diagnostic-playbook.md`
- `references/practice-playbook.md`
- `references/lesson-playbook.md`
- `references/mastery-playbook.md`
