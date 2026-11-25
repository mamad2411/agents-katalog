---
name: mobile-prototype
description: Turn mobile UX, wireframe, UI, and platform contracts into a testable interaction prototype plan, a standalone browser review runner, or an implementation handoff. Use when Codex needs navigation transitions, gestures, motion, feedback, failure injection, runtime test cases, or an executable prototype scope.
---

# Mobile Prototype

Make the core task observable in motion and runtime. Treat a prototype as a behavior test surface, not as a collection of clickable pictures.

## Choose the prototype target

- **Behavior prototype**: define screens, states, transitions, feedback, interruption, and test cases for a tool such as Figma, ProtoPie, or a native prototype.
- **Browser review runner**: render a self-contained HTML design prototype from `prototype.json`, a UI Design contract, and an optional Design System contract. The default URL is a clean product preview; append `?inspect=1` for state continuity, contract edges, and deterministic failure review before production implementation.
- **Executable spike**: create or hand off a narrow runnable prototype with real text, persistence boundaries, platform surfaces, and deterministic failure hooks.
- **Validation pass**: execute the prototype test matrix and record evidence, limitations, and regressions.

Prefer `mobile-wireframe` before this Skill and `mobile-design-to-code` when the user wants framework code. Preserve upstream Screen, State, Flow, Requirement, Token, and Component IDs.

## Define the runtime contract

1. Select one critical task and one high-risk recovery path.
2. Map each screen/state node to its entry, exit, action, system response, and durable result.
3. Define animation, gesture, haptic, sound, and announcement behavior with a reduced-motion and nonvisual equivalent.
4. Add interruption, background/termination, offline, duplicate submission, permission denial, and destructive recovery where applicable.
5. Define deterministic failure hooks for persistence, network, indexing, permission, and system-surface cases instead of relying on luck.
6. Keep prototype status honest: a plan or static render is not runtime evidence.

Read [references/prototype-rules.md](references/prototype-rules.md) and [references/prototype-schema.md](references/prototype-schema.md) before creating structured output.

## Produce and validate

Create:

- `prototype-map.md` using [assets/prototype-map-template.md](assets/prototype-map-template.md).
- `prototype.json` using [assets/prototype-template.json](assets/prototype-template.json).
- `prototype-test-plan.md` using [assets/prototype-test-plan-template.md](assets/prototype-test-plan-template.md).

Run `python3 scripts/validate_prototype.py <path-to-prototype.json>`. Use the resulting `not-tested` records to drive implementation and device QA; do not convert them to `pass` without evidence.

When the prototype follows UI Design, also run `python3 scripts/validate_ui_prototype_alignment.py --ui-design <path-to-ui-design.json> --prototype <path-to-prototype.json>`. This catches missing state nodes, unmapped explicit interactions, and high-risk states without a recovery hook.

For a clickable design-review surface, run the following after the contract checks. The supplied Design System must contain a locked visual direction copied from `ui-design.json`; an unlocked or legacy theme is a hard stop.

```bash
python3 scripts/render_prototype_html.py \
  --ui-design <path-to-ui-design.json> \
  --design-system <path-to-design-system.json> \
  --prototype <path-to-prototype.json> \
  --output <output-dir>/prototype-runner/index.html
python3 scripts/validate_prototype_runner.py \
  --html <output-dir>/prototype-runner/index.html \
  --prototype <path-to-prototype.json>
```

The default runner URL must show only the product preview: no QA header, inspector, evidence badge, or debug phone chrome. The inspector remains available at `?inspect=1`. The renderer must consume the locked visual fingerprint and semantic UI/Design System tokens for surface, text, action, border, typography, spacing, radius, color hierarchy, and module rhythm; do not reintroduce a generic card-stack, pill-button shell, or a legacy Margin theme. The runner must expose the product's primary task, state jump, outgoing contract edges, and deterministic failure switches for applicable persistence/index/permission/destructive paths in inspect mode. Its report remains `runtimeEvidence: not-tested` until browser, accessibility, interruption, and device evidence exists. A browser runner is a UI/prototype artifact, not production Flutter code.

## Enforce the output order

1. Prototype scope and evidence status.
2. Screen/state nodes and transitions.
3. Feedback, motion, gesture, system-surface, and interruption rules.
4. Failure hooks and test matrix.
5. Implementation handoff, evidence, and open risks.

Do not finish with a happy-path click-through that cannot show recovery, state continuity, accessibility pressure, or system behavior.
