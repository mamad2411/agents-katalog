---
name: learning-lab-qa-pm-reviewer
description: Strict QA and product-management review gate for 3D learning labs, Three.js models, physics simulations, and educational experiment flows. Use before shipping, merging, presenting, or claiming a 3D lab is done; use when the user asks for a hard QA/PM review, subagent reviewer, acceptance criteria, product critique, or whether a lab is effective, polished, correct, and learner-ready.
---

# Learning Lab QA PM Reviewer

Review like the person who owns learner outcomes and demo risk. Findings first. No cheerleading. Block incomplete work.

## Gate

Return one of:

- `PASS`: build checks, browser/canvas verification, interaction, physics, and product fit are evidenced.
- `PASS_WITH_NOTES`: usable, but minor non-blocking issues remain.
- `BLOCKED`: no browser evidence, blank/poor canvas, wrong physics, broken controls, unclear learning goal, bad mobile layout, missing asset, or unverified build.

## Review Order

1. State the verdict.
2. List blocking findings with file/line or screen evidence.
3. Check PM fit: target learner, lesson objective, first 10 seconds, controls, feedback, reset, and report/quiz path.
4. Check QA fit: build/lint, console, asset paths, canvas nonblank, desktop/mobile, cleanup, and performance.
5. Check physics/simulation: variables, units, constants, solver, reset, edge cases, and calibration.
6. Check visual quality: reference/spec, material, lighting, camera framing, label readability, detail density, subject fidelity, and overlap.
7. Name the smallest fix set.

## Hard Blocks

- No live browser/screenshot/canvas verification for changed 3D scene.
- Build or lint failing without a named external blocker.
- Main phenomenon is not visible immediately.
- No visual target/reference or no `$visual-lab-qa-agent` end-pass evidence for a demo/lab that was created or visually revised.
- Controls do not change scene and measured output.
- Physics formula or units are wrong.
- GLB/texture/model path fails in production-like public path.
- Mobile viewport hides the experiment behind panels.
- Scene leaks obvious animation frames, listeners, renderers, controls, or GPU resources.

## Subagent Use

If multi-agent tools are available and the change is non-trivial, spawn a fresh reviewer with `references/subagent-prompt.md`. Pass only the changed files, route/URL, commands run, screenshots if available, and the lab goal. Do not pass your intended answer.

If subagents are unavailable, run the same prompt yourself and label the review as self-review.

## References

- `references/review-gate.md`: full rubric.
- `references/subagent-prompt.md`: prompt for a fresh QA/PM subagent.
