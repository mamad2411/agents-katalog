---
name: visual-lab-qa-agent
description: Use when creating, improving, or accepting polished 3D learning labs where visual quality, GPT Image/imagegen concept references, benchmark screenshot comparison, chemistry/biology detail, or before-and-after demo QA loops matter.
---

# Visual Lab QA Agent

Run this as the visual quality gate before and after every demo-sized 3D lab. Metrics prove budget; screenshots and reference comparison prove whether the lab actually looks convincing.

## Gate

Return one of:

- `PASS`: visual target, screenshot evidence, interaction, mobile layout, and budgets all support shipping.
- `FIX_REQUIRED`: visual target is reachable locally; list the smallest concrete fix set and repeat the end pass after fixes.
- `BLOCKED`: missing screenshots/reference, blank scene, unavailable image tool with no fallback spec, severe asset/budget issue, or repeated failed fix loop.

## Start Pass

1. Read the lab contract or infer: subject, topic, learner level, primary phenomenon, required controls, measured outputs, and target viewport.
2. Create a visual target before implementation:
   - If image generation is available, generate object-focused references with GPT Image/imagegen: front/side/top or exploded view of the 3D object/system to be modeled, plain background, no decorative room/lab scenery unless the scenery itself is the object.
   - If image generation is unavailable, write a compact visual target spec with composition, materials, detail markers, labels, and mobile framing.
   - For biological anatomy, generate multi-view morphology references for the organ/system first; use those shapes as the acceptance target, not only a pretty scene mood board.
3. Start a prompt loop ledger in demo notes, a PR summary, or a local evidence file. It must record the target prompt/spec, reference image paths, morphology anchors, role-gate verdicts, screenshot paths, benchmark file, fix set, and final stop reason.
4. For non-trivial labs, spawn a fresh visual QA/PM subagent if multi-agent tools are available. Give it only the lab goal and target evidence, not your intended implementation.

## End Pass

1. Run the repo benchmark/build/browser flow that produces desktop and mobile screenshots.
2. Compare the actual screenshots against the visual target using `references/visual-rubric.md`.
3. Check that the main phenomenon is immediately recognizable, not hidden behind panels or decorative effects.
4. Check chemistry/biology strictly:
   - Chemistry needs credible lab apparatus, reaction evidence, material/color change, scale, and measurement readouts.
   - Biology needs recognizable organ/specimen/ecosystem structure, dense small details, flow/signal markers, and scale cues.
5. Check performance and FE guardrails from `$threejs-performance-qa`: frame pacing, draw calls, triangles, model size, texture size, text overflow, touch targets, and mobile panel bounds.
6. Append the round result to the prompt loop ledger before deciding `PASS` or `FIX_REQUIRED`.
7. If any score is below the pass threshold, return `FIX_REQUIRED` with specific changes, apply them, rerun screenshots/benchmark, and repeat.

## Locked Loop

Do not skip this loop for visual demo work:

1. `REFERENCE_SET`: generate or write the object-focused front/side/top/cutaway references and list required morphology anchors.
2. `DESIGN_DIRECTOR`: run `$threejs-design-director`; block literal copying of sketch marks, background, or annotation artifacts as real objects.
3. `SCIENCE_MODEL`: run `$science-model-director`; block visual elements that do not map to science causality or measured outputs.
4. `ART_DIRECTOR`: run `$threejs-art-director`; block toy-like visuals, weak material separation, poor composition, or low reference likeness.
5. `IMPLEMENT`: build only after the reference set and all role gates exist.
6. `SCREENSHOT_SET`: capture desktop and mobile screenshots from the benchmark/browser run.
7. `COMPARE`: check each morphology anchor against screenshots.
8. `LOG_ROUND`: write prompt summary, reference path, screenshot path, benchmark path, QA verdict, and concrete fix set.
9. `FIX_REQUIRED`: if any anchor is missing, too primitive, hidden, copied illogically, toy-like, or only represented by a generic sphere/box/cylinder, fix and repeat from screenshot capture.
10. `PASS`: only after morphology, visual quality, interaction, mobile, budgets, and loop ledger all pass.

`detailMarkers`, FPS, and draw calls cannot override a missing morphology anchor.

## Prompt Loop Ledger

For every serious visual demo, preserve the design evolution in a compact ledger. Do not invent exact prompts after the fact; if only a summary is available, mark it as a summary.

Required fields per round:

- `Round`: number and goal.
- `Prompt/spec`: image prompt or written reference spec.
- `Reference`: generated image path or written spec path.
- `Design gate`: `$threejs-design-director` verdict and morphology anchors.
- `Science gate`: `$science-model-director` verdict and required cause/effect mapping.
- `Art gate`: `$threejs-art-director` verdict for likeness, material polish, and composition.
- `3D output`: screenshot paths for desktop and mobile.
- `Benchmark`: result file and important metrics.
- `Decision`: `PASS`, `FIX_REQUIRED`, or `BLOCKED`.
- `Fix set`: concrete geometry/material/camera/label/interaction changes for the next round.

If the user asks how the design improved, answer from this ledger plus screenshot/benchmark evidence, not from memory.

## Output Format

```text
VISUAL_QA: PASS | FIX_REQUIRED | BLOCKED
Reference: image/spec path or prompt summary
Evidence: screenshot paths, benchmark file, browser target
Scores: focal phenomenon, subject fidelity, materials/lighting, detail density, labels/readouts, mobile fit, performance
Fix set: only required when FIX_REQUIRED
Loop: current pass number and stop reason when blocked
Ledger: file/path or PR section containing the prompt rounds
```

## Loop Rules

- Prefer 1-3 tight fix loops over a broad redesign.
- A fix must name concrete scene changes: geometry, material, lighting, camera, label, interaction, or asset-budget action.
- Do not accept "make it prettier", "add details", or "improve design" as a fix.
- Stop as `BLOCKED` if the same visual defect remains after two focused attempts or requires external art/assets the repo does not have.
- Do not claim the benchmark proves beauty. It only proves that the prettier scene still fits the budget.
- Do not accept a demo that merely contains many detail markers if the object silhouette, topology, or morphology does not match the reference.

## Hard Blocks

- No visual target before implementation.
- No prompt loop ledger for a serious visual demo.
- No desktop and mobile screenshots after implementation.
- Canvas blank, badly framed, or covered by UI.
- Biology scene looks like generic blobs or has fewer dense detail markers than the lab budget requires.
- Biology scene lacks the required morphology anchors from the reference, such as chambered heart, branching vessels/airways, alveoli clusters, roots/soil layers, or food-web organism groups.
- Biology, chemistry, or physics scene reads as toy primitives at thumbnail size even if the benchmark passes.
- Chemistry scene lacks credible apparatus or visible reaction evidence.
- Text overlaps, control labels overflow, or mobile touch targets are too small.
- Model/texture/transfer budgets are exceeded without an explicit tradeoff and benchmark evidence.

## References

- Read `references/visual-rubric.md` for scoring, subject prompts, and fix patterns.
- Use `$threejs-performance-qa` for machine benchmark evidence.
- Use `$learning-lab-qa-pm-reviewer` for final product acceptance.
